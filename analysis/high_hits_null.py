#!/usr/bin/env python3
"""Magnum Life: do the real astrological calendars give more 6-, 7- and 8-number hits than shifted calendars?

For every lead (114 parameters and their pairs, plus plain hot / cold over all draws, x hot / cold / position /
hot+100; tickets built before each draw from counts on earlier draws only) and every format (10 ordinary
tickets, System 10 x 1, System 9 x 2 overlap / disjoint), the best 8-number combination of the entry is found
for every draw. Counted over all leads: lead x draw hits with 6+, 7+ and 8 winning numbers, on the whole
history after a warm-up (draws from 25% of the history on), on the draws before the last 10, and on the last 10.
The same counts on SHIFTS calendars rolled by random offsets (the draws stay the same, the astrological codes
move) give the chance distribution; the real calendar's rank among them is the test.

python3 analysis/high_hits_null.py  -> analysis/high_hits_null_results.json, analysis/HIGH_HITS_NULL.md
"""

import itertools
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

sys.argv += ["--tickets", "10", "--bonus", "--games", "ml8"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import extra_astro as xa  # noqa: E402
import lead_search10 as ls  # noqa: E402

KEY = "ml8"
SHIFTS = int(sys.argv[sys.argv.index("--shifts") + 1]) if "--shifts" in sys.argv else 20
LIMIT = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None   # sets, for timing
OUT = os.path.join(common.ROOT, "analysis", "high_hits_null_results.json")
MD = os.path.join(common.ROOT, "analysis", "HIGH_HITS_NULL.md")
FORMATS = {"10 tickets": None, "System 10 × 1": [list(range(10))],
           "System 9 × 2 overlap": [list(range(9)), list(range(6)) + [9, 10, 11]],
           "System 9 × 2 disjoint": [list(range(9)), list(range(9, 18))]}
KT = 18
LEVELS = (12, 14, 16)            # tier codes: 6+, 7+, 8 winning numbers in the best 8-combination
G = {}


def setup():
    if not G:
        ls.init(KEY)
        R = ls.W["R"]
        rng = np.random.default_rng(2024)
        G["shifts"] = [0] + [int(x) for x in rng.choice(np.arange(160, R - 160), SHIFTS, replace=False)]
        G["fmts"] = dict(FORMATS, **{"10 tickets": ls.W["pats"]})


def count(task):
    """Per calendar: hits per draw (summed over the chunk's leads) by format and level."""
    sh, sets = task
    setup()
    codes = np.roll(ls.W["codes"], G["shifts"][sh], axis=0)
    k, n, H, Bn = ls.W["k"], ls.W["n"], ls.W["H"], ls.W["Bn"]
    d = len(H)
    out = {f: np.zeros((len(LEVELS), d), np.int32) for f in G["fmts"]}
    for s in sets:
        cid = np.zeros(d, np.int64)
        for j in s:
            cid = cid * 1000 + codes[:, j]
        order = np.argsort(cid, kind="stable")
        cs = cid[order]
        first = np.r_[0, np.flatnonzero(np.diff(cs)) + 1]
        starts = np.repeat(first, np.diff(np.r_[first, d]))

        def ex(X):
            xs = X[order]
            c = np.cumsum(xs, 0) - xs
            c = c - c[starts]
            o = np.empty_like(X)
            o[order] = c
            return o
        dp = ex(np.ones((d, 1), np.float32))
        cnt = ex(H)
        e = dp * k / n
        zc = (cnt - e) / np.sqrt(e * (1 - k / n) + 1e-6)
        scores = (cnt - e, e - cnt,
                  ((ex(ls.W["P"]) + ls.SMOOTH * ls.W["pglob"]) / (dp[:, :, None] + ls.SMOOTH)).sum(1),
                  zc + ls.W["hot100"])
        for S in scores:
            S = S + ls.W["tie"]
            top = np.argpartition(-S, KT - 1, 1)[:, :KT]
            top = np.take_along_axis(top, np.argsort(-np.take_along_axis(S, top, 1), 1), 1)
            war = np.take_along_axis(H, top, 1).astype(np.int8)
            warb = np.take_along_axis(Bn, top, 1).astype(np.int8)
            for f, pats in G["fmts"].items():
                best = np.zeros(d, np.int8)
                for q in pats:
                    m = np.minimum(war[:, q].sum(1), 8)
                    b = np.minimum(warb[:, q].sum(1), 8 - m)
                    best = np.maximum(best, np.where(m == 8, 16, 2 * m + (b > 0)).astype(np.int8))
                for li, lv in enumerate(LEVELS):
                    out[f][li] += best >= lv
    return sh, out


def main():
    t0 = time.time()
    names = common.ALL_PARAMS + xa.extra_params()
    sets = [()] + [(i,) for i in range(len(names))] + list(itertools.combinations(range(len(names)), 2))
    if LIMIT:
        sets = sets[:LIMIT]
    tasks = [(sh, sets[i:i + 100]) for sh in range(SHIFTS + 1) for i in range(0, len(sets), 100)]
    tot = {}
    with Pool(4) as pool:
        for j, (sh, out) in enumerate(pool.imap_unordered(count, tasks), 1):
            acc = tot.setdefault(sh, {f: np.zeros_like(v) for f, v in out.items()})
            for f, v in out.items():
                acc[f] += v
            if j % 200 == 0:
                print(f"{j}/{len(tasks)} tasks, {time.time() - t0:.0f}s", flush=True)
    setup()
    g = common.load_game(KEY)
    d = len(g["dates"])
    R = d - ls.HOLD
    lo = int(0.25 * R)
    spans = {"whole history (after warm-up)": (lo, d), "earlier draws": (lo, R), "last 10 draws": (R, d)}
    res = {"leads": len(sets) * 4, "shifts": SHIFTS, "spans": {k: list(v) for k, v in spans.items()},
           "shift_offsets": G["shifts"][1:], "formats": {}}
    md = ["# Magnum Life: 6-, 7- and 8-number hits, real calendar vs shifted calendars", "",
          f"Generated by `analysis/high_hits_null.py`. All {len(sets) * 4:,} leads, tickets built before each draw from "
          "earlier draws only. A *hit* = one lead on one draw whose best 8-number combination holds 6+ (or 7+, or 8) "
          f"winning numbers; counts are summed over all leads. Real calendar against {SHIFTS} calendars rolled by random "
          "offsets (same draws, astrological codes out of line with them). *Rank* = the real calendar's place among the "
          f"{SHIFTS + 1} (1 = most hits); *share ≥ real* = fraction of shifted calendars with at least as many.", ""]
    lab = {12: "6+", 14: "7+", 16: "8"}
    for f in FORMATS:
        rf = {}
        md += [f"## {f}", "", "| Draws | Level | Real | Shifted: mean (min-max) | Rank | Share ≥ real |", "|---|---|---|---|---|---|"]
        for sname, (a, b) in spans.items():
            for li, lv in enumerate(LEVELS):
                vals = np.array([int(tot[sh][f][li, a:b].sum()) for sh in range(SHIFTS + 1)])
                real, null = vals[0], vals[1:]
                rank = int((null > real).sum()) + 1
                share = float((null >= real).mean())
                rf[f"{sname} | {lab[lv]}"] = {"real": int(real), "shifted": null.tolist(), "rank": rank, "share_ge_real": share}
                md.append(f"| {sname} | {lab[lv]} | {real:,} | {null.mean():,.0f} ({null.min():,}-{null.max():,}) | "
                          f"{rank}/{SHIFTS + 1} | {share:.2f} |")
        # per-draw 6+ counts on the last 10
        per = [int(tot[0][f][0, t]) for t in range(R, d)]
        nul = np.array([[int(tot[sh][f][0, t]) for t in range(R, d)] for sh in range(1, SHIFTS + 1)])
        rf["last10_per_draw_6plus"] = {"dates": g["dates"][R:], "real": per, "shifted_mean": nul.mean(0).round(1).tolist()}
        md += ["", "6+ hits per draw on the last 10: " + ", ".join(f"{dt[5:]} {r} ({m:.0f})" for dt, r, m in
                                                                  zip(g["dates"][R:], per, nul.mean(0))) + " (shifted mean in brackets).", ""]
        res["formats"][f] = rf
    res["seconds"] = round(time.time() - t0)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
    with open(MD, "w") as fh:
        fh.write("\n".join(md) + "\n")
    print("\n".join(md))
    print("wrote", OUT, "and", MD, f"in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
