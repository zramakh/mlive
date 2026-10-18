#!/usr/bin/env python3
"""Predicting draws by vector analogy, the "king - man + woman = queen" idea
turned into a forecaster:

    numbers(today)  ~  numbers(A) - conditions(A) + conditions(today)

where A is a past draw, numbers(X) is the mean vector of the numbers drawn on X,
and conditions(X) the mean vector of the 83 parameter tokens of X's date and
time. Vectors are the word2vec-equivalent PPMI + SVD embedding of embed_model.py,
trained only on draws before the ones being predicted. The ticket is the k
numbers whose vectors are closest (cosine) to the predicted vector.

Methods (lambda = strength of the astrology term, chosen on validation draws;
lambda = 0 means "astrology adds nothing")
  last       A = the previous draw:  q = y(A) + lambda * (p(today) - p(A))
  similar    A = the 10 earlier draws sharing the most parameter values with today (averaged)
  map        a learned analogy direction: ridge map W from condition vectors to number vectors
             (fitted on the training draws), q = y(A_similar) + lambda * (p(today) - p(A_similar)) W
  direct     q = p(today) W  (the map alone, no past draw)
Controls are the same with lambda = 0 (numbers of the past draws only).

Scores: numbers matched by the ticket vs k*k/n per draw (z), and AUC = probability a drawn
number ranks above an undrawn one (0.5 = chance).
Protocol (per game; the last HOLD draws kept aside, R = the rest): embedding and map on
R[0:60%], settings (dimensions, lambda) chosen on R[60:80%]; retrained on R[0:80%] and
tested on R[80:100%]; retrained on R and used on the last HOLD draws. The whole pipeline
is repeated on SHIFTS circularly shifted parameter calendars.

python3 analysis/analogy_model.py  (~10 min) -> analysis/analogy_results.json
"""

import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import embed_model as em  # noqa: E402

HOLD = 10
SHIFTS = 5
DIMS = [30, 100]
LAMBDAS = [0.0, 0.5, 1.0, 2.0]
SIMILAR = 10
RIDGE = 1.0
METHODS = ["last", "similar", "map", "direct"]
OUT = os.path.join(common.ROOT, "analysis", "analogy_results.json")


def space(X, Y, V, upto, dims):
    """Per dims: (parameter vectors, number vectors, ridge map W) from draws [0, upto)."""
    vecs = em.ppmi_vectors(X[:upto], Y[:upto], V, dims)
    out = {}
    for d, Wv in vecs.items():
        Pv, Nv = Wv[:V], Wv[V:]
        p = Pv[X[:upto]].mean(1)
        y = (Y[:upto] @ Nv) / Y[:upto].sum(1, keepdims=True)
        M = np.linalg.solve(p.T @ p + RIDGE * np.eye(d), p.T @ y)
        out[d] = (Pv, Nv, M)
    return out


def similar_draws(X, rows):
    """For each target row: the SIMILAR earlier draws sharing the most parameter values."""
    out = []
    for t in rows:
        shared = (X[:t] == X[t]).sum(1)
        out.append(np.argsort(-shared, kind="stable")[:SIMILAR])
    return out


def queries(method, lam, sp, X, Y, rows, sims):
    Pv, Nv, M = sp
    p = Pv[X].mean(1)                                              # condition vector of every draw
    y = (Y @ Nv) / np.maximum(Y.sum(1, keepdims=True), 1)          # numbers vector of every draw
    q = []
    for i, t in enumerate(rows):
        if method == "last":
            a = [t - 1]
            delta = p[t] - p[a].mean(0)
        elif method in ("similar", "map"):
            a = sims[i]
            delta = p[t] - p[a].mean(0)
            if method == "map":
                delta = delta @ M
        else:                                                      # direct
            q.append(p[t] @ M)
            continue
        q.append(y[a].mean(0) + lam * delta)
    q = np.array(q)
    return q / np.maximum(np.linalg.norm(q, axis=1, keepdims=True), 1e-12) @ Nv.T


def scores(S, Y, k):
    n = Y.shape[1]
    noise = np.random.default_rng(0).random(S.shape) * 1e-9
    top = np.argsort(-(S + noise), 1)[:, :k]
    m = Y[np.arange(len(Y))[:, None], top].sum(1)
    e = k * k / n
    v = e * (1 - k / n) * (n - k) / (n - 1)
    rank = np.argsort(np.argsort(S + noise, 1), 1)                 # 0 = lowest score
    pos = Y.astype(bool)
    auc = ((rank * pos).sum(1) - k * (k - 1) / 2) / (k * (n - k))
    return {"draws": len(Y), "matches": int(m.sum()), "expected": round(len(Y) * e, 2),
            "z": round(float((m.sum() - len(Y) * e) / math.sqrt(len(Y) * v)), 2),
            "auc": round(float(auc.mean()), 4)}, top


def run(task):
    key, shift = task
    g, X, names, Y = em.tokens(key, shift)
    k, V = g["k"], len(names)
    R = len(Y) - HOLD
    a, b = int(R * 0.6), int(R * 0.8)
    rows = {"valid": np.arange(a, b), "test": np.arange(b, R), "hold": np.arange(R, len(Y))}
    sims = {p: similar_draws(X, r) for p, r in rows.items()}
    sp_valid = space(X, Y, V, a, DIMS)
    res = {}
    for method in METHODS:
        grid = []
        for d in DIMS:
            for lam in (LAMBDAS if method != "direct" else [1.0]):
                st, _ = scores(queries(method, lam, sp_valid[d], X, Y, rows["valid"], sims["valid"]), Y[rows["valid"]], k)
                grid.append((st["auc"], d, lam, st))
        auc, d, lam, vst = max(grid, key=lambda x: x[0])
        sp_test = space(X, Y, V, b, [d])[d]
        tst, _ = scores(queries(method, lam, sp_test, X, Y, rows["test"], sims["test"]), Y[rows["test"]], k)
        sp_all = space(X, Y, V, R, [d])[d]
        hst, top = scores(queries(method, lam, sp_all, X, Y, rows["hold"], sims["hold"]), Y[rows["hold"]], k)
        res[method] = {"dims": d, "lambda": lam, "valid": vst, "test": tst, "hold_out": hst,
                       "valid_auc_by_lambda": {f"{dd}/{ll}": st["auc"] for _, dd, ll, st in grid},
                       "hold_out_tickets": [sorted(int(x) + 1 for x in t) for t in top]}
        # the same past draws with the astrology term switched off (lambda = 0), on the test draws
        if method in ("last", "similar"):
            cst, _ = scores(queries(method, 0.0, sp_test, X, Y, rows["test"], sims["test"]), Y[rows["test"]], k)
            res[method]["test_without_astrology"] = cst
    return key, shift, res, g["dates"][R:]


def main():
    games = list(common.GAMES)
    rng = np.random.default_rng(13)
    tasks = []
    for key in games:
        d = len(common.load_game(key)["dates"])
        tasks += [(key, s) for s in [0] + [int(x) for x in rng.choice(np.arange(160, d - 160), SHIFTS, replace=False)]]
    with Pool(4) as pool:
        out = list(pool.imap_unordered(run, tasks))
    res = {"hold_out_draws": HOLD, "games": {}}
    for key in games:
        rows = {s: r for k2, s, r, _ in out if k2 == key}
        held = next(h for k2, s, _, h in out if k2 == key and s == 0)
        real = rows[0]
        game = {"label": common.GAMES[key][1], "held_out": held, "real": real,
                "shifted": {m: {"test_z": [rows[s][m]["test"]["z"] for s in rows if s],
                                "test_auc": [rows[s][m]["test"]["auc"] for s in rows if s],
                                "lambda": [rows[s][m]["lambda"] for s in rows if s],
                                "hold_matches": [rows[s][m]["hold_out"]["matches"] for s in rows if s]}
                            for m in METHODS}}
        res["games"][key] = game
        print(game["label"])
        for m in METHODS:
            r = real[m]
            ctl = r.get("test_without_astrology")
            print(f"  {m:<8} dims {r['dims']:>3} lambda {r['lambda']:<3} | test {r['test']['matches']}/{r['test']['expected']} "
                  f"z {r['test']['z']:+.2f} AUC {r['test']['auc']:.4f}"
                  + (f" (no astrology: z {ctl['z']:+.2f} AUC {ctl['auc']:.4f})" if ctl else "")
                  + f" | last {HOLD}: {r['hold_out']['matches']}/{r['hold_out']['expected']}"
                  f" | shifted z {game['shifted'][m]['test_z']} lambda {game['shifted'][m]['lambda']}")
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
