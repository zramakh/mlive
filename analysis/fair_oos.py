#!/usr/bin/env python3
"""A fair unseen-draw test for every lead: re-choose before each year with earlier draws only, then score that year.

Each draw is scored by how many drawn numbers fall in a lead's top ticket (8 Magnum Life, 6 Toto), built from earlier
draws only; chance is exact (k × k / n, hypergeometric spread). For every year Y of the history (after the first two):

  1. every lead's record before Y (all its earlier draws) is turned into a z against chance;
  2. leads in the top 1% of their game before Y count as "chosen for Y";
  3. their hits in Y are their unseen test.

So every lead, watchlist or not, gets the same test: whenever its earlier record would have put it on a list, the
next year is played blind. Pooled over all years this gives many unseen draws per game. Run on the real calendar and
on shifted calendars (parameter values rolled against the draws), and for the "all leads" pool (45,892 per game: the
114 parameters alone and in pairs, × 7 patterns) as well as each watchlist lead (D9, divisional and Chinese charts
included, ranked against the same pool).

python3 analysis/fair_oos.py [--shifts 3]  -> analysis/FAIR_OOS.md, fair_oos.json
"""

import itertools
import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

NSH = int(sys.argv[sys.argv.index("--shifts") + 1]) if "--shifts" in sys.argv else 3
sys.argv = [sys.argv[0]]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import watch_rank as wr  # noqa: E402  (enables D9, divisional and Chinese parameters for the watchlist)
import lead_full as lf  # noqa: E402

ws, ls, common, xa = wr.ws, wr.ls, wr.common, wr.xa
A = wr.A
PATS = lf.PATS
LABEL = wr.LABEL
NAMES = common.ALL_PARAMS + xa.extra_params()
SETS = [()] + [(i,) for i in range(114)] + list(itertools.combinations(range(114), 2))   # the 114 base parameters
TOP = 0.01
G = {}


def setup(key):
    ls.init(key)
    W = ls.W
    d = W["d"]
    years = np.array([int(x[:4]) for x in W["g"]["dates"]])
    lo = 100
    ys = sorted(set(years[lo:]))
    rng = np.random.default_rng(99)
    R = d - ls.HOLD
    G.update(key=key, d=d, lo=lo, years=years, ys=ys,
             shifts=[0] + [int(x) for x in rng.choice(np.arange(160, R - 160), NSH, replace=False)])


def yearly(hits):
    """Hits summed per year (draws from lo on)."""
    ys, years, lo = G["ys"], G["years"], G["lo"]
    return np.array([hits[lo:][years[lo:] == y].sum() for y in ys], np.float32)


def scores(codes, s):
    W = ls.W
    k, n, H, d = W["k"], W["n"], W["H"], W["d"]
    cid = np.zeros(d, np.int64)
    for c in s:
        cid = cid * 1000 + codes[:, c]
    order = np.argsort(cid, kind="stable")
    cs = cid[order]
    first = np.r_[0, np.flatnonzero(np.diff(cs)) + 1]
    starts = np.repeat(first, np.diff(np.r_[first, d]))
    ex = lf.window_ex(order, starts, d)
    dp = ex(np.ones((d, 1), np.float32))
    cnt = ex(H)
    e = dp * k / n
    zc = (cnt - e) / np.sqrt(e * (1 - k / n) + 1e-6)
    pos = None
    for pat in PATS:
        if pat == "pos":
            if pos is None:
                pos = ((ex(W["P"]) + ls.SMOOTH * W["pglob"]) / (dp[:, :, None] + ls.SMOOTH)).sum(1)
            S = pos
        else:
            S = {"hot": cnt - e, "cold": e - cnt, "hot+100": zc + W["hot100"], "cold+100": -zc - W["hot100"],
                 "hot/cold100": zc - W["hot100"], "cold/hot100": -zc + W["hot100"]}[pat]
        top = np.argpartition(-(S + W["tie"]), k, axis=1)[:, :k]
        yield np.take_along_axis(H, top, 1).sum(1)


def chunk(task):
    sh, i0, i1 = task
    codes = np.roll(ls.W["codes"], G["shifts"][sh], axis=0)
    out = np.zeros((i1 - i0, len(PATS), len(G["ys"])), np.float32)
    for j, s in enumerate(SETS[i0:i1]):
        for p, h in enumerate(scores(codes, s)):
            out[j, p] = yearly(h)
    return sh, i0, out


def zcum(Y, ny, e, v):
    """Leads x years of hits -> z of each lead's record before each year (column y uses years < y)."""
    c = np.cumsum(Y, -1) - Y
    nc = np.cumsum(ny) - ny
    return (c - nc * e) / np.sqrt(np.maximum(nc, 1) * v)


def main():
    res = {}
    for key in LABEL:
        setup(key)
        W = ls.W
        k, n = W["k"], W["n"]
        e, v = k * k / n, k * (k / n) * (1 - k / n) * (n - k) / (n - 1)
        ys, years, lo = G["ys"], G["years"], G["lo"]
        ny = np.array([(years[lo:] == y).sum() for y in ys], float)
        Y = np.zeros((NSH + 1, len(SETS), len(PATS), len(ys)), np.float32)
        tasks = [(sh, i, min(i + 200, len(SETS))) for sh in range(NSH + 1) for i in range(0, len(SETS), 200)]
        with Pool(4) as pool:
            for sh, i0, o in pool.imap_unordered(chunk, tasks):
                Y[sh, i0:i0 + len(o)] = o
        test_years = list(range(2, len(ys)))                          # two years of record before the first choice
        g = {"label": LABEL[key], "years": [int(y) for y in ys], "test_years": [int(ys[t]) for t in test_years],
             "calendars": []}
        thr_real = None
        for sh in range(NSH + 1):
            F = Y[sh].reshape(-1, len(ys))                            # all leads x years
            Z = zcum(F, ny, e, v)
            hits = draws = 0.0
            per_year = []
            thr = []
            for t in test_years:
                cut = np.quantile(Z[:, t], 1 - TOP)
                thr.append(float(cut))
                ch = Z[:, t] >= cut
                hits += F[ch, t].sum()
                draws += ch.sum() * ny[t]
                per_year.append(float(F[ch, t].sum() / (ch.sum() * ny[t] * e)))
            zz = (hits - draws * e) / math.sqrt(draws * v)
            # the same choice with each lead's record judged on the year itself (hindsight) for scale
            g["calendars"].append(dict(ratio=float(hits / (draws * e)), per_year=per_year, z_pooled=float(zz),
                                       chosen_per_year=int(round(TOP * F.shape[0]))))
            if sh == 0:
                thr_real = thr
                Zreal, Freal = Z, F
        # no-parameter leads (the patterns on the numbers' own history)
        g["no_param"] = {PATS[p]: float(Y[0, 0, p, test_years].sum() / (ny[test_years].sum() * e)) for p in range(len(PATS))}
        # every watchlist lead: its z before each test year, whether that put it in the top 1%, and its hits that year
        names = NAMES
        wl = []
        for lead, pat, fmts in ws.WATCH[key]:
            pat0 = pat
            rk = ws.ranking([names.index(x) for x in lead.split(" × ")], pat0)
            h = np.take_along_axis(W["H"], rk[:, :k], 1).sum(1)
            yh = yearly(h)
            zc_ = zcum(yh[None, :], ny, e, v)[0]
            chosen = [t for i, t in enumerate(test_years) if zc_[t] >= thr_real[i]]
            ch_h = float(sum(yh[t] for t in chosen))
            ch_n = float(sum(ny[t] for t in chosen))
            allt_h, allt_n = float(yh[test_years].sum()), float(ny[test_years].sum())
            wl.append(dict(lead=lead, pat=pat0, fmt=fmts[0], chosen_years=[int(ys[t]) for t in chosen],
                           chosen_draws=int(ch_n), chosen_hits=ch_h,
                           chosen_ratio=ch_h / (ch_n * e) if ch_n else None,
                           chosen_z=(ch_h - ch_n * e) / math.sqrt(ch_n * v) if ch_n else None,
                           all_ratio=allt_h / (allt_n * e), all_z=(allt_h - allt_n * e) / math.sqrt(allt_n * v),
                           per_year=[float(yh[t] / (ny[t] * e)) for t in test_years],
                           pre_z=[float(zc_[t]) for t in test_years]))
        g["watch"] = wl
        res[key] = g
        print(key, "done", flush=True)
    json.dump(res, open(os.path.join(A, "fair_oos.json"), "w"), indent=1)
    report(res)


def report(res):
    md = ["# A fair unseen-draw test for every lead", "",
          "Generated by `analysis/fair_oos.py`. Before each year, every lead's record on the earlier years only is turned "
          "into a z against chance (drawn numbers in its top ticket: 8 Magnum Life, 6 Toto); the top 1% of leads of the "
          "game are \"chosen\" and that year is their blind test. Pooled over every year after the first two, so each game "
          "gets thousands of unseen lead-draws. Shifted = parameter values rolled against the draws (no link to the sky).", "",
          "## Chosen before each year, scored on that year", "",
          "| Game | Test years | Chosen leads: hits vs chance (real) | Shifted calendars | No parameters (best pattern) |",
          "|---|---|---|---|---|"]
    for key, g in res.items():
        r, sh = g["calendars"][0], g["calendars"][1:]
        np_best = max(g["no_param"].items(), key=lambda kv: kv[1])
        md.append(f"| {g['label']} | {g['test_years'][0]}-{g['test_years'][-1]} ({len(g['test_years'])}) | ×{r['ratio']:.4f} (z {r['z_pooled']:+.1f}) | "
                  + ", ".join(f"×{s['ratio']:.4f} ({s['z_pooled']:+.1f})" for s in sh)
                  + f" | ×{np_best[1]:.4f} ({np_best[0]}) |")
    md += ["", "Per year (real calendar, chosen leads' ratio): "]
    for key, g in res.items():
        md.append(f"- {g['label']}: " + ", ".join(f"{y} ×{x:.3f}" for y, x in zip(g["test_years"], g["calendars"][0]["per_year"])))
    md += ["", "## Every watchlist lead on the same test", "",
           "*Chosen years* = years its earlier record put it in the top 1% of its game; *blind hits* = its hits in those "
           "years only (its fair unseen test). *All test years* = every year after the first two, for scale (this one is "
           "not blind: the lead was picked later with these years in view).", "",
           "| # | Game | Lead (pattern) | Chosen years | Blind draws | Blind ratio | Blind z | All test years: ratio (z) |",
           "|---|---|---|---|---|---|---|---|"]
    rows = []
    for key, g in res.items():
        for w in g["watch"]:
            rows.append((g["label"], w))
    rows.sort(key=lambda r: (r[1]["chosen_z"] is None, -(r[1]["chosen_z"] or 0)))
    for i, (lab, w) in enumerate(rows, 1):
        cy = ", ".join(str(y) for y in w["chosen_years"]) or "never"
        md.append(f"| {i} | {lab} | {w['lead']} ({w['pat']}) | {cy} | {w['chosen_draws']} | "
                  + (f"×{w['chosen_ratio']:.3f} | {w['chosen_z']:+.1f}" if w["chosen_draws"] else "– | –")
                  + f" | ×{w['all_ratio']:.3f} ({w['all_z']:+.1f}) |")
    open(os.path.join(A, "FAIR_OOS.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md[:20]))


if __name__ == "__main__":
    main()
