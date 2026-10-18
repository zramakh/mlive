#!/usr/bin/env python3
"""Every lead plays 10 tickets per draw on the last 10 draws (which no choice saw).

Each method gives every number a score at every draw (walk-forward: only earlier draws;
every choice - look-back, weights, parameters, settings - frozen before the last 10).
Ticket 1 = the k best numbers; tickets 2-10 = the next-best k-number sets by total
score (one or two numbers swapped). Chance for each method's actual tickets comes from
SIMS simulated fair sets of 10 draws, so the overlap between its tickets is accounted for.

Methods (each game)
  hot / cold / hot+cold        the look-back or mix chosen by hot_window.py / hot_cold_mix.py
  hot/cold + astrology         the combination chosen by hotcold_astro.py
  analogy last/similar/map/direct, embedding ppmi / neural   settings chosen by analogy_model.py / embed_model.py
  selected params (direct/last x top_m/greedy)               param_select.py
  cell lead #1-#5              fresh own_leads search without the last 10 draws (hot, cold and
                               position patterns ranked by the weakest of their three period z)
  baselines                    replay previous draw, hot last 100, 10 random tickets

python3 analysis/ten_tickets.py  (~5 min) -> analysis/ten_tickets_results.json, analysis/TEN_TICKETS.md
"""

import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analogy_model as am  # noqa: E402
import common  # noqa: E402
import embed_model as em  # noqa: E402
import holdout_leads as hl  # noqa: E402
import hot_cold_mix as hcm  # noqa: E402
import hotcold_astro as ha  # noqa: E402
import own_leads as ol  # noqa: E402
import param_select as ps  # noqa: E402

HOLD = 10
NT = 10
SIMS = 20000
OUT = os.path.join(common.ROOT, "analysis", "ten_tickets_results.json")
MD = os.path.join(common.ROOT, "analysis", "TEN_TICKETS.md")
A = os.path.join(common.ROOT, "analysis")


def load(name):
    return json.load(open(os.path.join(A, name)))


# ------------------------------------------------------------------ tickets from scores
def ten_tickets(s, k):
    """Ticket 1 = top k; then the best one- and two-number swaps by total score."""
    order = np.argsort(-s)
    t1 = list(order[:k])
    base = s[t1].sum()
    cand = {tuple(sorted(t1)): base}
    outs = list(order[k:k + 12])
    for i in t1:
        for j in outs:
            t = tuple(sorted(set(t1) - {i} | {j}))
            cand[t] = base - s[i] + s[j]
    weak = list(order[max(0, k - 4):k])
    for a in range(len(weak)):
        for b in range(a + 1, len(weak)):
            for c in range(len(outs)):
                for d in range(c + 1, len(outs)):
                    t = tuple(sorted(set(t1) - {weak[a], weak[b]} | {outs[c], outs[d]}))
                    cand[t] = base - s[weak[a]] - s[weak[b]] + s[outs[c]] + s[outs[d]]
    best = sorted(cand, key=lambda t: -cand[t])[:NT]
    return [list(t) for t in best]


def score_lead(tickets, W, k, n, rng):
    """tickets: per draw a list of NT tickets (0-based numbers); W: HOLD x n winners."""
    T = np.zeros((len(tickets), NT, n), bool)
    for i, ts in enumerate(tickets):
        for j, t in enumerate(ts):
            T[i, j, t] = True
    m = (T & W[:, None, :]).sum(2)                                   # draws x tickets
    total, best, ge3 = int(m.sum()), int(m.max(1).sum()), int((m >= 3).sum())
    sim_tot = np.zeros(SIMS)
    sim_best = np.zeros(SIMS)
    sim_ge3 = np.zeros(SIMS)
    for i in range(len(tickets)):
        Wsim = np.zeros((SIMS, n), bool)
        Wsim[np.arange(SIMS)[:, None], np.argsort(rng.random((SIMS, n)), 1)[:, :k]] = True
        ms = (Wsim[:, None, :] & T[i][None]).sum(2)                  # SIMS x tickets
        sim_tot += ms.sum(1)
        sim_best += ms.max(1)
        sim_ge3 += (ms >= 3).sum(1)
    return {"total": total, "expected_total": round(float(sim_tot.mean()), 2),
            "p_total": round(float((sim_tot >= total).mean()), 4),
            "best_per_draw_sum": best, "expected_best": round(float(sim_best.mean()), 2),
            "p_best": round(float((sim_best >= best).mean()), 4),
            "tickets_3plus": ge3, "expected_3plus": round(float(sim_ge3.mean()), 3),
            "p_3plus": round(float((sim_ge3 >= ge3).mean()), 4),
            "per_draw": m.tolist(),
            "tickets": [[sorted(int(x) + 1 for x in t) for t in ts] for ts in tickets]}


# ------------------------------------------------------------------ score generators
def window_scores(h, N, sign, k, n):
    """Score of every number at every draw from the previous N draws (0 = all); half-life if N < 0."""
    d = len(h)
    if N < 0:
        a = 0.5 ** (1 / -N)
        w, out = np.zeros(n), np.zeros((d, n))
        for t in range(d):
            out[t] = w
            w = a * w + h[t]
        return sign * out
    cum = np.vstack([np.zeros((1, n)), np.cumsum(h, 0)])
    out = np.zeros((d, n))
    st = N if N else 1
    out[st:] = cum[st:d] - (cum[:d - st] if N else 0)
    return sign * out


def parse_window(label):
    if label.startswith("half-life"):
        return -int(label.split()[1])
    v = label.split("=")[1]
    return 0 if v == "all" else int(v)


def generators(key):
    """{name: HOLD x n score matrix} for the last HOLD draws."""
    g = common.load_game(key)
    k, n = g["k"], g["n"]
    h = g["hit"][:, 1:].astype(float)
    d = len(h)
    rows = np.arange(d - HOLD, d)
    rng = np.random.default_rng(1)
    tie = rng.random((d, n)) * 1e-6
    G = {}
    # hot / cold look-backs
    for fname, sign, label in (("hot_window_results.json", 1, "hot"), ("cold_window_results.json", -1, "cold")):
        ch = load(fname)["games"][key]["chosen"]
        if ch == "overdue":
            last, sc = np.full(n, -1.0), np.zeros((d, n))
            for t in range(d):
                sc[t] = t - last
                last[h[t] > 0] = t
        else:
            sc = window_scores(h, parse_window(ch), sign, k, n)
        G[f"{label} numbers ({ch})"] = (sc + tie)[rows]
    # hot + cold mix: the chosen h hot get a bonus above every cold score, the rest ranked by cold score
    res = load("hot_cold_mix_results.json")["games"][key]
    for c in hcm.combos(k):
        if hcm.label(c, k) == res["chosen"]:
            hh, wh, wc = c
    R = hcm.ranks(h, np.random.default_rng(1))
    sc = np.zeros((d, n))
    if hh < k:
        sc = -(R[wc][2]).astype(float)                               # cold rank 0 = coldest -> best
    if hh:
        sc = np.where(R[wh][1] < hh, 1000 - R[wh][1], sc)
    G[f"hot+cold ({res['chosen']})"] = sc[rows]
    # hot/cold + astrology
    c = load("hotcold_astro_results.json")["games"][key]["real"]["chosen"]
    ol.setup(key)
    s = tuple(ol.PARAMS.index(p) for p in c["set"].split(" × "))
    Aft = np.nan_to_num(ha.cell_feature(ol.G["codes"], s, h, k, n))
    Fh = np.nan_to_num(ha.window_feature(h, c["Nh"], k, n))
    Fc = np.nan_to_num(ha.window_feature(h, c["Nc"], k, n))
    G[f"hot/cold + astrology ({c['set']})"] = (c["alpha"] * Fh + c["beta"] * Fc + c["gamma"] * Aft + tie)[rows]
    # analogy and embedding models (vectors from all draws before the last HOLD)
    gg, X, names, Y = em.tokens(key, 0)
    V = len(names)
    R_ = d - HOLD
    an = load("analogy_results.json")["games"][key]["real"]
    sims = am.similar_draws(X, rows)
    for m in am.METHODS:
        sp = am.space(X, Y, V, R_, [an[m]["dims"]])[an[m]["dims"]]
        G[f"analogy {m}"] = am.queries(m, an[m]["lambda"], sp, X, Y, rows, sims)
    eb = load("embed_results.json")["games"][key]["real"]
    W_ = em.ppmi_vectors(X[:R_], Y[:R_], V, [eb["ppmi"]["dims"]])[eb["ppmi"]["dims"]]
    G["embedding ppmi"] = em.ppmi_scores(W_, X[rows], V)
    Yprev = np.vstack([np.zeros((1, n)), Y[:-1]])
    for m, prev in (("neural", False), ("neural+prev", True)):
        Ainc = em.incidence(X, Yprev, V, n, prev)
        lm, _ = em.train_lm(n, eb[m]["dims"], eb[m]["l2"], Ainc[:R_], Y[:R_], epochs=eb[m]["epochs"])
        G[f"embedding {m}"] = lm.logits(Ainc[rows])
    # selected-parameter forecasters
    sel = load("param_select_results.json")["games"][key]
    for f, (method, lam) in ps.FORECASTERS.items():
        for kind in ("top_m", "greedy"):
            prm = sel[f]["real"][kind]["params"]
            if not prm:
                continue
            Xs, Vs = ps.subset(X, [common.ALL_PARAMS.index(p) for p in prm])
            dd = min(ps.DIM, Vs + n - 1)
            sp = am.space(Xs, Y, Vs, R_, [dd])[dd]
            G[f"selected params {f}/{kind} ({' + '.join(prm[:3])}{'…' if len(prm) > 3 else ''})"] = \
                am.queries(method, lam, sp, Xs, Y, rows, None)
    # baselines
    G["baseline: replay previous draw"] = (np.vstack([np.zeros((1, n)), h[:-1]]) + tie)[rows]
    G["baseline: hot last 100"] = (window_scores(h, 100, 1, k, n) + tie)[rows]
    G["baseline: random"] = np.random.default_rng(5).random((HOLD, n))
    return G


def cell_leads(key):
    """Fresh lead search without the last HOLD draws; scores of the top 5 hot / cold / position leads."""
    hl.HOLD = HOLD
    ol.TICKET_K = None
    z = np.vstack([hl.scan((key, 0, lo, min(lo + 300, len(ol.SETS))))[3] for lo in range(0, len(ol.SETS), 300)])
    pats = ["hot", "cold", "pos"]
    weakest = np.stack([z[:, ol.METRICS.index(p), :].min(1) for p in pats], 1)
    order = np.argsort(-weakest, axis=None)[:5]
    g = common.load_game(key)
    k, n = g["k"], g["n"]
    ol.setup(key)                                                    # full history: walk-forward inputs
    out = {}
    for r, idx in enumerate(order, 1):
        si, pi = divmod(int(idx), len(pats))
        s, pat = ol.SETS[si], pats[pi]
        cid = ol.cell_of(ol.G["codes"], s)
        sc = cell_score(cid, pat, k, n)
        out[f"cell lead #{r}: {' × '.join(ol.PARAMS[j] for j in s)} ({pat}, weakest z {weakest.ravel()[idx]:+.2f})"] = sc[-HOLD:]
    return out


def cell_score(cid, pat, k, n):
    H, P = ol.G["H"].astype(float), ol.G["P"].astype(float)
    order = np.argsort(cid, kind="stable")
    cs = cid[order]
    first = np.r_[0, np.flatnonzero(np.diff(cs)) + 1]
    starts = np.repeat(first, np.diff(np.r_[first, len(cid)]))

    def ex(X):
        xs = X[order]
        c = np.cumsum(xs, 0) - xs
        c = c - c[starts]
        o = np.empty_like(X)
        o[order] = c
        return o
    dp = ex(np.ones((len(cid), 1)))
    tie = np.random.default_rng(2).random((len(cid), n)) * 1e-6
    if pat in ("hot", "cold"):
        exc = ex(H) - dp * k / n
        return (exc if pat == "hot" else -exc) + tie
    pg = (np.cumsum(P, 0) - P) / np.maximum(np.arange(len(cid)), 1)[:, None, None]
    pc = (ex(P) + ol.SMOOTH * pg) / (dp[:, :, None] + ol.SMOOTH)
    return pc.sum(1) + tie                                           # chance of the number at any position


def run(key):
    g = common.load_game(key)
    k, n = g["k"], g["n"]
    W = g["hit"][-HOLD:, 1:].astype(bool)
    G = generators(key)
    G.update(cell_leads(key))
    rng = np.random.default_rng(11)
    out = {}
    for name, S in G.items():
        if name == "baseline: random":
            r = np.random.default_rng(6)
            tk = [[list(r.choice(n, k, replace=False)) for _ in range(NT)] for _ in range(HOLD)]
        else:
            tk = [ten_tickets(S[i], k) for i in range(HOLD)]
        out[name] = score_lead(tk, W, k, n, rng)
    return key, out, g["dates"][-HOLD:]


def main():
    with Pool(4) as pool:
        res = {key: (out, dates) for key, out, dates in pool.imap_unordered(run, list(common.GAMES))}
    allrows = []
    md = ["# Ten tickets per draw on the last 10 draws", "",
          "Generated by `analysis/ten_tickets.py`. Every method's choices were made without the last 10 draws; tickets "
          "use earlier draws only. Ticket 1 = the method's top k numbers, tickets 2–10 = its next-best k-number sets. "
          f"*Chance* = share of {SIMS:,} simulated fair sets of 10 draws in which the same tickets match at least as many "
          "numbers. *Best* = sum over draws of the best ticket's matches. *3+* = tickets matching 3 or more numbers.", ""]
    for key in common.GAMES:
        out, dates = res[key]
        md += [f"## {common.GAMES[key][1]} ({dates[0]} – {dates[-1]})", "",
               "| Method | Matches, 100 tickets (expected) | Chance | Best ticket per draw, summed (expected) | Chance | 3+ tickets (expected) | Chance |",
               "|---|---|---|---|---|---|---|"]
        for name, r in sorted(out.items(), key=lambda x: x[1]["p_total"]):
            md.append(f"| {name} | {r['total']} ({r['expected_total']}) | {100 * r['p_total']:.1f}% | {r['best_per_draw_sum']} "
                      f"({r['expected_best']}) | {100 * r['p_best']:.1f}% | {r['tickets_3plus']} ({r['expected_3plus']}) | "
                      f"{100 * r['p_3plus']:.1f}% |")
            allrows.append((r["p_total"], common.GAMES[key][1], name, r))
        md.append("")
    allrows.sort(key=lambda x: x[0])
    md += ["## All methods, ranked by chance of their total matches", "",
           "| Rank | Game | Method | Matches (expected) | Chance |", "|---|---|---|---|---|"]
    for i, (p, game, name, r) in enumerate(allrows, 1):
        md.append(f"| {i} | {game} | {name} | {r['total']} ({r['expected_total']}) | {100 * p:.1f}% |")
    ps_ = np.array([x[0] for x in allrows])
    md += ["", f"{len(ps_)} methods: {int((ps_ < 0.05).sum())} at chance < 5% (about {0.05 * len(ps_):.1f} expected if "
           f"nothing works), {int((ps_ < 0.01).sum())} below 1%."]
    with open(OUT, "w") as fh:
        json.dump({k2: v[0] for k2, v in res.items()}, fh, indent=1, default=float)
    with open(MD, "w") as fh:
        fh.write("\n".join(md) + "\n")
    for p, game, name, r in allrows[:15]:
        print(f"{p:.4f} {game:<18} {name[:70]:<70} {r['total']}/{r['expected_total']} best {r['best_per_draw_sum']}/{r['expected_best']} 3+ {r['tickets_3plus']}/{r['expected_3plus']}")
    print(len(ps_), "methods; p<0.05:", int((ps_ < 0.05).sum()), "p<0.01:", int((ps_ < 0.01).sum()))


if __name__ == "__main__":
    main()
