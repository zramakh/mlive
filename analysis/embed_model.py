#!/usr/bin/env python3
"""Word-embedding / small language-model approach: every draw is a "sentence" of
tokens, the parameter values of its date and time (e.g. moon_rashi=Vrishabha,
day_god=Jade Hall; all 83 parameters of common.py) and the numbers drawn
(N07, N23, ...). Vectors are learned for every token, in the spirit of
word2vec ("king - man + woman = queen"), and a date's numbers are predicted
by vector arithmetic: add up the date's parameter vectors and take the
numbers whose vectors are closest.

Models (per game, numpy only)
  ppmi      word2vec-equivalent embedding (Levy & Goldberg 2014): token x token
            co-occurrence within draws -> positive PMI (context smoothing 0.75)
            -> truncated SVD. Score(n) = cosine(sum of the date's parameter
            vectors, vector of N<n>).
  neural    fastText-style language model: context = mean of the date's
            parameter-token embeddings, softmax over number tokens
            (logit = context . output vector + bias), trained with Adam and
            L2, early stopping on validation loss.
  neural+prev  the same, with the previous draw's numbers as extra context
            tokens (like the previous words an LLM reads).
Ticket = the k highest-scoring numbers.

Protocol (per game, the last HOLD draws kept aside):
  R = all draws but the last HOLD.
  1. settings chosen by training on R[0:60%] and validating on R[60:80%];
  2. retrained on R[0:80%] and tested on R[80%:100%];
  3. retrained on all of R and used on the HOLD held-out draws (never seen).
  The whole pipeline is repeated on SHIFTS circularly shifted parameter calendars
  (parameters moved against the draws), which shows what chance gives.
Also: nearest neighbours and analogies in the ppmi space, to show what the vectors learn.

python3 analysis/embed_model.py  (~10 min) -> analysis/embed_results.json, analysis/EMBEDDINGS.md
"""

import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

PARAMS = common.ALL_PARAMS
HOLD = 10
SHIFTS = 5
PPMI_DIMS = [10, 30, 100]
NEURAL_GRID = [(8, 1e-3), (32, 1e-3), (32, 1e-2)]          # (dimensions, L2)
OUT = os.path.join(common.ROOT, "analysis", "embed_results.json")
MD = os.path.join(common.ROOT, "analysis", "EMBEDDINGS.md")


# ------------------------------------------------------------------ data
def tokens(key, shift=0):
    g = common.load_game(key)
    codes, values = common.codes_for(g["dates"], PARAMS)
    codes = np.roll(codes, shift, axis=0)
    offset = np.r_[0, np.cumsum([len(v) for v in values])[:-1]]
    X = codes + offset                                            # draws x P global parameter-token ids
    names = [f"{p}={v}" for p, vals in zip(PARAMS, values) for v in vals]
    Y = g["hit"][:, 1:].astype(np.float64)                        # draws x n multi-hot numbers
    return g, X, names, Y


# ------------------------------------------------------------------ ppmi + svd
def ppmi_vectors(X, Y, V, dims):
    """Embedding of V parameter tokens and n number tokens from co-occurrence within draws."""
    d, n = Y.shape
    M = np.zeros((d, V + n))
    M[np.arange(d)[:, None], X] = 1
    M[:, V:] = Y
    C = M.T @ M
    np.fill_diagonal(C, 0)
    tot = C.sum()
    row = C.sum(1)
    col = row ** 0.75
    col = col / col.sum()
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log((C / tot) / (row[:, None] / tot) / col[None, :])
    P = np.where(np.isfinite(pmi) & (pmi > 0), pmi, 0.0)
    U, S, _ = np.linalg.svd(P, full_matrices=False)
    out = {}
    for k in dims:
        W = U[:, :k] * np.sqrt(S[:k])
        W = W / np.maximum(np.linalg.norm(W, axis=1, keepdims=True), 1e-12)
        out[k] = W
    return out


def ppmi_scores(W, X, V):
    q = W[X].sum(1)                                               # sum of the date's parameter vectors
    q /= np.maximum(np.linalg.norm(q, axis=1, keepdims=True), 1e-12)
    return q @ W[V:].T                                            # cosine with every number vector


# ------------------------------------------------------------------ neural language model
def incidence(X, Yprev, V, n, prev):
    """draws x tokens 0/1 matrix of context tokens: the date's parameter tokens, plus the previous
    draw's numbers (token V+i) when prev; the first draw gets a "no previous draw" token (V+n)."""
    A = np.zeros((len(X), V + (n + 1 if prev else 0)), np.float32)
    A[np.arange(len(X))[:, None], X] = 1
    if prev:
        A[:, V:V + n] = Yprev
        A[Yprev.sum(1) == 0, V + n] = 1
    return A / A.sum(1, keepdims=True)                            # rows average their tokens


class LM:
    def __init__(self, T, n, dim, l2, seed=0):
        r = np.random.default_rng(seed)
        self.l2 = l2
        self.E = r.normal(0, 0.1, (T, dim))
        self.U = r.normal(0, 0.1, (n, dim))
        self.b = np.zeros(n)
        self.m = [np.zeros_like(a) for a in (self.E, self.U, self.b)]
        self.v = [np.zeros_like(a) for a in (self.E, self.U, self.b)]
        self.t = 0

    def logits(self, A):
        return (A @ self.E) @ self.U.T + self.b

    def loss(self, A, Y):
        z = self.logits(A)
        z = z - z.max(1, keepdims=True)
        logp = z - np.log(np.exp(z).sum(1, keepdims=True))
        return float(-(Y * logp).sum(1).mean() / Y.sum(1).mean())

    def step(self, A, Y, lr=0.02):
        c = A @ self.E
        p = softmax(c @ self.U.T + self.b)
        g = (p - Y / Y.sum(1, keepdims=True)) / len(A)
        grads = (A.T @ (g @ self.U) + self.l2 * self.E, g.T @ c + self.l2 * self.U, g.sum(0))
        self.t += 1
        for i, (a, gr) in enumerate(zip((self.E, self.U, self.b), grads)):
            self.m[i] = 0.9 * self.m[i] + 0.1 * gr
            self.v[i] = 0.999 * self.v[i] + 0.001 * gr * gr
            a -= lr * (self.m[i] / (1 - 0.9 ** self.t)) / (np.sqrt(self.v[i] / (1 - 0.999 ** self.t)) + 1e-8)


def train_lm(n, dim, l2, Atr, Ytr, Ava=None, Yva=None, epochs=None, max_epochs=400):
    """Full-batch Adam. With validation data: early stopping, returns (model, best epoch).
    Without: trains for `epochs`."""
    lm = LM(Atr.shape[1], n, dim, l2)
    best, best_ep, best_state = math.inf, 0, None
    for ep in range(1, (epochs or max_epochs) + 1):
        lm.step(Atr, Ytr)
        if Ava is not None and ep % 5 == 0:
            l = lm.loss(Ava, Yva)
            if l < best - 1e-6:
                best, best_ep, best_state = l, ep, [x.copy() for x in (lm.E, lm.U, lm.b)]
            elif ep - best_ep >= 40:
                break
    if best_state is not None:
        lm.E, lm.U, lm.b = best_state
    return lm, best_ep


# ------------------------------------------------------------------ scoring
def ticket_stats(score, Y, k):
    n = Y.shape[1]
    noise = np.random.default_rng(0).random(score.shape) * 1e-9
    top = np.argsort(-(score + noise), 1)[:, :k]
    m = Y[np.arange(len(Y))[:, None], top].sum(1)
    e = k * k / n
    v = e * (1 - k / n) * (n - k) / (n - 1)
    return {"draws": len(Y), "matches": int(m.sum()), "expected": round(len(Y) * e, 2),
            "z": round(float((m.sum() - len(Y) * e) / math.sqrt(len(Y) * v)), 2)}, top


def ll_gain(prob, Y, k):
    """Bernoulli log-likelihood gain per draw over 'every number equally likely' (nats)."""
    n = Y.shape[1]
    p = np.clip(k * prob, 1e-9, 1 - 1e-9)
    u = k / n
    return float(((Y * np.log(p / u) + (1 - Y) * np.log((1 - p) / (1 - u))).sum(1)).mean())


def softmax(z):
    z = z - z.max(1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(1, keepdims=True)


def run(task):
    key, shift = task
    g, X, names, Y = tokens(key, shift)
    k, n = g["k"], g["n"]
    V = len(names)
    Yprev = np.vstack([np.zeros((1, n)), Y[:-1]])
    R = len(Y) - HOLD
    a, b = int(R * 0.6), int(R * 0.8)
    res = {}

    # ppmi: choose dims on validation, then test and hold-out
    vecs = ppmi_vectors(X[:a], Y[:a], V, PPMI_DIMS)
    val = {d: ticket_stats(ppmi_scores(W, X[a:b], V), Y[a:b], k)[0]["z"] for d, W in vecs.items()}
    dbest = max(val, key=val.get)
    W80 = ppmi_vectors(X[:b], Y[:b], V, [dbest])[dbest]
    test, _ = ticket_stats(ppmi_scores(W80, X[b:R], V), Y[b:R], k)
    Wall = ppmi_vectors(X[:R], Y[:R], V, [dbest])[dbest]
    hold, top = ticket_stats(ppmi_scores(Wall, X[R:], V), Y[R:], k)
    res["ppmi"] = {"dims": dbest, "valid_z": val, "test": test, "hold_out": hold,
                   "hold_out_tickets": [sorted(int(x) + 1 for x in t) for t in top]}

    for name, prev in (("neural", False), ("neural+prev", True)):
        A = incidence(X, Yprev, V, n, prev)
        best = None
        for dim, l2 in NEURAL_GRID:
            lm, ep = train_lm(n, dim, l2, A[:a], Y[:a], A[a:b], Y[a:b])
            vl = lm.loss(A[a:b], Y[a:b])
            if best is None or vl < best[0]:
                best = (vl, dim, l2, max(ep, 5))
        _, dim, l2, ep = best
        uniform_loss = math.log(n)                                # cross-entropy of "all equal"
        lm80, _ = train_lm(n, dim, l2, A[:b], Y[:b], epochs=ep)
        z = lm80.logits(A[b:R])
        test, _ = ticket_stats(z, Y[b:R], k)
        test["ll_gain_per_draw"] = round(ll_gain(softmax(z), Y[b:R], k), 4)
        lmall, _ = train_lm(n, dim, l2, A[:R], Y[:R], epochs=ep)
        zh = lmall.logits(A[R:])
        hold, top = ticket_stats(zh, Y[R:], k)
        res[name] = {"dims": dim, "l2": l2, "epochs": ep, "valid_loss": round(best[0], 4),
                     "uniform_loss": round(uniform_loss, 4), "test": test, "hold_out": hold,
                     "hold_out_tickets": [sorted(int(x) + 1 for x in t) for t in top]}
    return key, shift, res, (Wall if shift == 0 else None), names, g["dates"][R:]


# ------------------------------------------------------------------ what the vectors learn
def neighbours(W, names, n, token, top=5):
    allnames = names + [f"N{i:02d}" for i in range(1, n + 1)]
    i = allnames.index(token)
    s = W @ W[i]
    s[i] = -9
    return [(allnames[j], round(float(s[j]), 3)) for j in np.argsort(-s)[:top]]


def analogy(W, names, n, a, b, c, top=3):
    """a - b + c = ?  (excluding the three inputs)"""
    allnames = names + [f"N{i:02d}" for i in range(1, n + 1)]
    ix = {t: i for i, t in enumerate(allnames)}
    q = W[ix[a]] - W[ix[b]] + W[ix[c]]
    s = W @ q / np.linalg.norm(q)
    for t in (a, b, c):
        s[ix[t]] = -9
    return [(allnames[j], round(float(s[j]), 3)) for j in np.argsort(-s)[:top]]


def main():
    games = list(common.GAMES)
    tasks = [(key, s) for key in games for s in range(SHIFTS + 1)]
    rng = np.random.default_rng(12)
    shift_of = {}
    for key in games:
        d = len(common.load_game(key)["dates"])
        shift_of[key] = [0] + [int(x) for x in rng.choice(np.arange(160, d - 160), SHIFTS, replace=False)]
    with Pool(4) as pool:
        out = list(pool.imap_unordered(run, [(key, shift_of[key][s]) for key, s in tasks]))
    res = {"hold_out_draws": HOLD, "games": {}}
    md = ["# What the embedding / language-model approach learns", "",
          "Generated by `analysis/embed_model.py`. Vectors trained on each game's draws (parameters of the date and "
          "time + numbers drawn), word2vec-style (PPMI + SVD).", ""]
    for key in games:
        rows = {s: r for k2, s, r, *_ in out if k2 == key}
        real = rows[0]
        W, names, held = next((w, nm, h) for k2, s, r, w, nm, h in out if k2 == key and s == 0)
        g = common.load_game(key)
        game = {"label": g["label"], "held_out": held, "real": real, "shifted": {}}
        for m in ("ppmi", "neural", "neural+prev"):
            game["shifted"][m] = {"test_z": [rows[s][m]["test"]["z"] for s in rows if s != 0],
                                  "hold_out_matches": [rows[s][m]["hold_out"]["matches"] for s in rows if s != 0]}
        res["games"][key] = game
        print(g["label"])
        for m in ("ppmi", "neural", "neural+prev"):
            r = real[m]
            print(f"  {m:<12} test {r['test']['matches']}/{r['test']['expected']} z {r['test']['z']:+.2f}"
                  + (f" LL {r['test'].get('ll_gain_per_draw', 0):+.4f}" if "ll_gain_per_draw" in r["test"] else "")
                  + f" | last {HOLD}: {r['hold_out']['matches']}/{r['hold_out']['expected']}"
                  f" | shifted test z {game['shifted'][m]['test_z']} hold {game['shifted'][m]['hold_out_matches']}")
        # neighbours and analogies (real calendar, all non-held-out draws)
        n = g["n"]
        md += [f"## {g['label']}", ""]
        probes = ["nakshatra=Rohini", "moon_rashi=Vrishabha", "jupiter_rashi=Karka", "day_pillar=Jia Zi", "N07", "N23"]
        md.append("| Token | Nearest tokens (cosine) |")
        md.append("|---|---|")
        for t in probes:
            if t in names or t.startswith("N"):
                md.append(f"| {t} | " + ", ".join(f"{a} ({c})" for a, c in neighbours(W, names, n, t)) + " |")
        md += ["", "| Analogy | Answer (cosine) |", "|---|---|"]
        for a, b, c in (("moon_rashi=Vrishabha", "nakshatra=Rohini", "nakshatra=Ashwini"),
                        ("day_stem=Jia", "day_pillar=Jia Zi", "day_pillar=Bing Yin"),
                        ("N07", "nakshatra=Rohini", "nakshatra=Ashwini")):
            md.append(f"| {a} − {b} + {c} | " + ", ".join(f"{x} ({cc})" for x, cc in analogy(W, names, n, a, b, c)) + " |")
        # how strongly numbers attach to parameters: mean |cosine| number vs parameter tokens, real vs shifted
        md.append("")
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
    with open(MD, "w") as fh:
        fh.write("\n".join(md) + "\n")
    print("wrote", OUT, "and", MD)


if __name__ == "__main__":
    main()
