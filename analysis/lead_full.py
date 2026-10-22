#!/usr/bin/env python3
"""Every astrological lead with seven hot / cold patterns, for Magnum Life and the three Sports Toto games: profit in
four formats with the official prizes, re-ranking before every draw, combined ranking, real calendar against
SHIFTS shifted calendars, per-lead high hits against their own shifted calendars.

Same method as toto_full.py, extended to Magnum Life and to seven patterns per lead:
    hot, cold, pos, hot+100 (as before), and new: cold+100 (cold in the cell and over the last 100 draws),
    hot/cold100 (hot in the cell, cold over the last 100), cold/hot100 (cold in the cell, hot over the last 100).
Formats: Magnum Life 10 tickets / System 10 x 1 / System 9 x 2 overlap / disjoint (prizes of profit_rank.py);
Toto 10 sets / System 7 x 2 overlap / disjoint / System 8 x 1 (toto_full.py).
*High* hits: 7+ (Magnum Life) or 5+ (Toto) winning numbers in one combination; *top*: 8 or 6.

--until DATE   use the draws up to DATE only (the last 10 of them are the test draws)
--shifts N     shifted calendars (default 20)
python3 analysis/lead_full.py --until 2026-10-17
    -> analysis/LEADS7_*.md, analysis/leads7_results.json, analysis/profit_arrays/leads7_<game>.npz
"""

import itertools
import json
import math
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

UNTIL = sys.argv[sys.argv.index("--until") + 1] if "--until" in sys.argv else None
NSH = int(sys.argv[sys.argv.index("--shifts") + 1]) if "--shifts" in sys.argv else 20
# which earlier draws of a lead's cell count: all (default), last_round (the most recent unbroken run of draws in the
# cell), last5 / last10 (the 5 / 10 most recent draws in the cell), decay10 (all, weight halving every 10 occurrences)
WINDOW = sys.argv[sys.argv.index("--window") + 1] if "--window" in sys.argv else "all"
# --family d9: only the singles and pairs that involve a D9 (navamsa) parameter (d9.py), the family appended to the
# parameter list
FAMILY = sys.argv[sys.argv.index("--family") + 1] if "--family" in sys.argv else None
TAG = ("" if WINDOW == "all" else f"_{WINDOW}") + (f"_{FAMILY}" if FAMILY else "")
if "--games" not in sys.argv:
    sys.argv += ["--games", "ml8,toto50,toto55,toto58"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import extra_astro as xa  # noqa: E402
import lead_search10 as ls  # noqa: E402
import toto_profit as tp  # noqa: E402
import profit_rank as pr  # noqa: E402

CHINESE_DIV = ("dlr", "mh", "ty")                # Da Liu Ren, Mei Hua, Tai Yi (chinese_div.py)
if FAMILY == "d9":
    import d9  # noqa: E402
    d9.enable()
elif FAMILY in CHINESE_DIV:
    import d9  # noqa: E402
    import vargas  # noqa: E402
    import chinese_div  # noqa: E402
    chinese_div.enable()
elif FAMILY:                                   # another divisional chart: d2, d3, ... d60 (vargas.py)
    import d9  # noqa: E402
    import vargas  # noqa: E402
    vargas.enable()

if UNTIL:                                   # a copy of the data cut at UNTIL, used by every loader
    _cut = os.path.join(common.ROOT, "analysis", "profit_arrays", f"data_until_{UNTIL}")
    os.makedirs(_cut, exist_ok=True)
    for _f in [x for x in os.listdir(common.DATA) if x.endswith(".csv")]:
        with open(os.path.join(common.DATA, _f)) as _i, open(os.path.join(_cut, _f), "w") as _o:
            for _ln in _i:
                if _f.startswith("astro") or _ln.startswith("draw_date") or _ln[:10] <= UNTIL:
                    _o.write(_ln)
    common.DATA = _cut

A = os.path.join(common.ROOT, "analysis")
SHIFTS = NSH
TOPN = 20
KT = 18
PATS = ["hot", "cold", "pos", "hot+100", "cold+100", "hot/cold100", "cold/hot100"]
NEW = {"cold+100", "hot/cold100", "cold/hot100"}
NP = len(PATS)
FMTS = {"ml8": ["10 tickets", "System 10 × 1", "System 9 × 2 overlap", "System 9 × 2 disjoint"]}
for _k in ("toto50", "toto55", "toto58"):
    FMTS[_k] = ["10 sets", "System 7 × 2 overlap", "System 7 × 2 disjoint", "System 8 × 1"]
SYS_PATS = {"System 7 × 2 overlap": [list(range(7)), list(range(4)) + [7, 8, 9]],
            "System 7 × 2 disjoint": [list(range(7)), list(range(7, 14))],
            "System 8 × 1": [list(range(8))],
            "System 10 × 1": [list(range(10))],
            "System 9 × 2 overlap": [list(range(9)), list(range(6)) + [9, 10, 11]],
            "System 9 × 2 disjoint": [list(range(9)), list(range(9, 18))]}
OUTP = os.path.join(common.ROOT, "analysis")
G = {}


def sys_table(key, s):
    """Payout of an s-number system entry by winning / bonus numbers inside it (every 6-combination paid)."""
    T = tp.pay_table(key)
    nb = 1 if key == "toto50" else 0
    P = np.zeros((s + 1, 2))
    for m in range(s + 1):
        for b in range(nb + 1):
            if m + b > s:
                continue
            o = s - m - b
            P[m, b] = sum(math.comb(m, a) * math.comb(b, c) * math.comb(o, 6 - a - c) * T[min(a, 6), c]
                          for a in range(min(m, 6) + 1) for c in range(b + 1) if 0 <= 6 - a - c <= o)
    return P


def bonus_all(key, d, n):
    import csv
    B = np.zeros((d, n), np.float32)
    for i, r in enumerate(csv.DictReader(open(os.path.join(common.DATA, common.GAMES[key][0])))):
        for c in ("bonus", "bonus1", "bonus2"):
            if r.get(c):
                B[i, int(r[c]) - 1] = 1
    return B


def setup(key):
    if G.get("key") != key:
        ls.init(key)
        k = ls.W["k"]
        ls.W["Bn"] = bonus_all(key, ls.W["d"], ls.W["n"])
        R = ls.W["R"]
        rng = np.random.default_rng(2024)
        fm = FMTS[key]
        G.clear()
        if key == "ml8":
            tables = {"10 tickets": pr.pay_table(8), **{f: pr.pay_table(len(SYS_PATS[f][0])) for f in fm[1:]}}
            price = 1
        else:
            tables = {"10 sets": tp.pay_table(key), **{f: sys_table(key, len(SYS_PATS[f][0])) for f in fm[1:]}}
            price = tp.PRICE[key]
        G.update(key=key, k=k, fmt=fm, hi=2 * (k - 1), top=2 * k, nb=2 if key == "ml8" else (1 if key == "toto50" else 0),
                 shifts=[0] + [int(x) for x in rng.choice(np.arange(160, R - 160), SHIFTS, replace=False)],
                 pats={fm[0]: ls.W["pats"], **{f: SYS_PATS[f] for f in fm[1:]}}, tables=tables,
                 cost={f: price * (10 if f == fm[0] else sum(math.comb(len(q), k) for q in SYS_PATS[f])) for f in fm})


def series(task):
    """Per lead: earlier profit / winning draws / 5+ / 6 hits, last-10 profit and best set per draw, per format;
    per draw: 5+ and 6 hits summed over the chunk's leads."""
    key, sh, sets = task
    setup(key)
    codes = np.roll(ls.W["codes"], G["shifts"][sh], axis=0)
    k, n, H, Bn, R = ls.W["k"], ls.W["n"], ls.W["H"], ls.W["Bn"], ls.W["R"]
    d = len(H)
    lo = int(0.25 * R)
    nl = len(sets) * NP
    k6, hi, tp_ = G["k"], G["hi"], G["top"]
    pre = np.zeros((nl, 4), np.float32)
    stat = np.zeros((nl, 4, 3), np.int16)                 # winning draws, 5+ hits, 6 hits (earlier draws)
    hold = np.zeros((nl, 4, ls.HOLD), np.float32)
    hcode = np.zeros((nl, 4, ls.HOLD), np.int8)
    agg = np.zeros((4, 2, d), np.int32)                    # format, (5+, 6), draw
    li = 0
    for s in sets:
        cid = np.zeros(d, np.int64)
        for j in s:
            cid = cid * 1000 + codes[:, j]
        order = np.argsort(cid, kind="stable")
        cs = cid[order]
        first = np.r_[0, np.flatnonzero(np.diff(cs)) + 1]
        starts = np.repeat(first, np.diff(np.r_[first, d]))

        ex = window_ex(order, starts, d)
        dp = ex(np.ones((d, 1), np.float32))
        cnt = ex(H)
        e = dp * k / n
        zc = (cnt - e) / np.sqrt(e * (1 - k / n) + 1e-6)
        h100 = ls.W["hot100"]
        scores = (cnt - e, e - cnt,
                  ((ex(ls.W["P"]) + ls.SMOOTH * ls.W["pglob"]) / (dp[:, :, None] + ls.SMOOTH)).sum(1),
                  zc + h100, -zc - h100, zc - h100, -zc + h100)
        for S in scores:
            S = S + ls.W["tie"]
            top = np.argpartition(-S, KT - 1, 1)[:, :KT]
            top = np.take_along_axis(top, np.argsort(-np.take_along_axis(S, top, 1), 1), 1)
            war = np.take_along_axis(H, top, 1).astype(np.int64)
            warb = np.take_along_axis(Bn, top, 1).astype(np.int64)
            for fi, f in enumerate(G["fmt"]):
                T = G["tables"][f]
                pay = np.zeros(d)
                best = np.zeros(d, np.int64)
                for q in G["pats"][f]:
                    m, b = war[:, q].sum(1), warb[:, q].sum(1)
                    pay += T[m, b]
                    m6 = np.minimum(m, k6)
                    b6 = np.minimum(b, k6 - m6)
                    best = np.maximum(best, 2 * m6 + (b6 > 0) * (m6 < k6))
                prof = pay - G["cost"][f]
                pre[li, fi] = prof[lo:R].sum()
                stat[li, fi] = ((pay[lo:R] > 0).sum(), (best[lo:R] >= hi).sum(), (best[lo:R] >= tp_).sum())
                hold[li, fi] = prof[R:]
                hcode[li, fi] = best[R:]
                agg[fi, 0] += best >= hi
                agg[fi, 1] += best >= tp_
            li += 1
    return key, sh, sets[0], pre, stat, hold, hcode, agg


def window_ex(order, starts, d):
    """Exclusive per-cell sums of a draws x ... array over the draws chosen by WINDOW (earlier draws only)."""
    pos = np.arange(d)
    if WINDOW == "all" or WINDOW.startswith("last") and WINDOW != "last_round":
        lo = starts if WINDOW == "all" else np.maximum(pos - int(WINDOW[4:]), starts)
    elif WINDOW == "last_round":
        di = order                                                    # draw index of each sorted position
        new = (pos == starts) | np.r_[True, di[1:] != di[:-1] + 1]
        rs = np.maximum.accumulate(np.where(new, pos, 0))             # start of each position's run
        lo = np.where(pos > starts, rs[np.maximum(pos - 1, 0)], pos)
    elif WINDOW.startswith("decay"):
        lam = 0.5 ** (1 / float(WINDOW[5:]))
        rel = (pos - starts).astype(np.float64)
        a, back = lam ** (-rel), lam ** (rel - 1)

        def ex(X):
            xs = X[order].astype(np.float64)
            sh = xs.shape
            xs = xs.reshape(d, -1) * a[:, None]
            P0 = np.vstack([np.zeros((1, xs.shape[1])), np.cumsum(xs, 0)])
            c = ((P0[pos] - P0[starts]) * back[:, None]).reshape(sh).astype(np.float32)
            o = np.empty_like(X)
            o[order] = c
            return o
        return ex
    else:
        raise ValueError(WINDOW)

    def ex(X):
        xs = X[order]
        sh = xs.shape
        xs = xs.reshape(d, -1)
        P0 = np.vstack([np.zeros((1, xs.shape[1]), xs.dtype), np.cumsum(xs, 0)])
        c = (P0[pos] - P0[lo]).reshape(sh)
        o = np.empty_like(X)
        o[order] = c
        return o
    return ex


def lead_sets(names):
    """The parameter sets (singles and pairs) of the run: all, or those involving the --family."""
    sets = [()] + [(i,) for i in range(len(names))] + list(itertools.combinations(range(len(names)), 2))
    if FAMILY == "d9":
        fam = {names.index(p) for p in d9.FAMILY}
        sets = [s for s in sets if fam & set(s)]
    elif FAMILY in CHINESE_DIV:                # the system's parameters, alone, paired with each other, with the other
        fam = {names.index(p) for p in chinese_div.family(FAMILY)}         # two systems and with the 114 base + D9
        nb = len(common.ALL_PARAMS) + len(xa.extra_params()) - len(chinese_div.NEW) - len(vargas.NEW)
        partners = set(range(nb)) | {names.index(p) for p in chinese_div.NEW}
        sets = [s for s in sets if fam & set(s) and set(s) <= partners]
    elif FAMILY:                               # the chart's parameters, alone, paired with each other and with the
        fam = {names.index(p) for p in vargas.family(int(FAMILY[1:]))}     # 114 base + D9 parameters
        partners = set(range(len(common.ALL_PARAMS) + len(xa.extra_params()) - len(vargas.NEW))) | fam
        sets = [s for s in sets if fam & set(s) and set(s) <= partners]
    return sets


def rank_desc(x):
    order = np.argsort(-x, kind="stable")
    xs = x[order]
    r = np.empty(len(x))
    first = np.r_[0, np.flatnonzero(np.diff(xs)) + 1]
    r[order] = np.repeat(first + 1, np.diff(np.r_[first, len(x)]))
    return r


def tier(c, k=6):
    return f"{k}" if c == 2 * k else f"{c // 2}{'+b' if c % 2 else ''}"


def main():
    t0 = time.time()
    names = common.ALL_PARAMS + xa.extra_params()
    sets = lead_sets(names)
    idx = {s: i for i, s in enumerate(sets)}
    pats = PATS
    lab = lambda i: (" × ".join(names[j] for j in sets[i // NP]) if sets[i // NP] else "all draws (no astrology)", pats[i % NP])  # noqa: E731
    NL = len(sets) * NP
    res = {}
    md_p = ["# Magnum Life and Sports Toto, 7 patterns: leads ranked by profit", "",
            "Generated by `analysis/lead_full.py` (7 patterns: hot, cold, pos, hot+100, cold+100, hot/cold100, cold/hot100; history up to the --until date, last 10 draws = test draws). Every astrological lead (45,892; with --family only the family's) in four formats (Magnum Life: 10 tickets, System 10 × 1, System 9 × 2 "
            "overlap / disjoint; Toto: 10 sets, System 7 × 2 overlap / disjoint, System 8 × 1). A System S "
            "entry = every 6-number combination of its S numbers, each paid as an ordinary bet (System 7 = 7 bets, "
            "System 8 = 28). Prizes: official tables, jackpots at their minimum (see TOTO_PROFIT.md). Numbers built before "
            f"each draw from earlier draws only. Shifted calendars: {SHIFTS}, shown as median (min-max).", ""]
    md_c = ["# Magnum Life and Sports Toto, 7 patterns: all formats ranked by stake, profit and winning draws", "",
            "Generated by `analysis/lead_full.py` (7 patterns: hot, cold, pos, hot+100, cold+100, hot/cold100, cold/hot100; history up to the --until date, last 10 draws = test draws). Every lead × format is one row; *score* = average of its rank by margin "
            "(profit ÷ stake over the last 10 draws) and by winning draws (lower is better).", ""]
    md_n = [f"# Magnum Life and Sports Toto, 7 patterns: high hits, real calendar vs {SHIFTS} shifted calendars", "",
            "Generated by `analysis/lead_full.py` (7 patterns: hot, cold, pos, hot+100, cold+100, hot/cold100, cold/hot100; history up to the --until date, last 10 draws = test draws). A *hit* = one lead on one draw whose best combination holds 7+ (or 8) "
            "winning numbers in Magnum Life, 5+ (or 6) in Toto, summed over all leads of the run. *Rank* = the real calendar's place among all calendars (1 = most); "
            "*share ≥ real* = fraction of shifted calendars with at least as many.", ""]
    md_l = ["# Magnum Life and Sports Toto, 7 patterns: leads with the most high hits against their own shifted calendars", "",
            "Generated by `analysis/lead_full.py` (7 patterns: hot, cold, pos, hot+100, cold+100, hot/cold100, cold/hot100; history up to the --until date, last 10 draws = test draws). *High hits* = draws whose best combination holds 7+ (Magnum Life) or 5+ (Toto) winning "
            "numbers, summed over the four formats. Chosen on the earlier draws: *z* = the lead's high hits on the real "
            "calendar against the same lead on 20 shifted calendars; then played on the last 10 draws. Control: the same "
            "choice made with each shifted calendar treated as real.", ""]
    for key in ls.RUN_GAMES:
        g = common.load_game(key)
        d = len(g["dates"])
        R = d - ls.HOLD
        lo = int(0.25 * R)
        nc = SHIFTS + 1
        PRE = np.zeros((NL, nc, 4), np.float32)
        ST = np.zeros((NL, nc, 4, 3), np.int16)
        HO = np.zeros((NL, nc, 4, ls.HOLD), np.float32)
        HC = np.zeros((NL, nc, 4, ls.HOLD), np.int8)
        AG = np.zeros((nc, 4, 2, d), np.int64)
        tasks = [(key, sh, sets[i:i + 100]) for sh in range(nc) for i in range(0, len(sets), 100)]
        with Pool(4) as pool:
            for j, (_, sh, s0, pre, stat, hold, hcode, agg) in enumerate(pool.imap_unordered(series, tasks), 1):
                i0 = idx[s0] * NP
                PRE[i0:i0 + len(pre), sh] = pre
                ST[i0:i0 + len(pre), sh] = stat
                HO[i0:i0 + len(pre), sh] = hold
                HC[i0:i0 + len(pre), sh] = hcode
                AG[sh] += agg
                if j % 500 == 0:
                    print(f"{key}: {j}/{len(tasks)} tasks, {time.time() - t0:.0f}s", flush=True)
        setup(key)
        cost = G["cost"]
        FMT = G["fmt"]
        kk = G["k"]
        hl, tl = f"{kk - 1}+", f"{kk}"
        np.savez_compressed(os.path.join(A, "profit_arrays", f"leads7{TAG}_{key}.npz"), PRE=PRE, ST=ST, HO=HO, HC=HC, AG=AG,
                            dates=np.array(g["dates"][R:]))
        game = {"label": g["label"], "cost": cost, "formats": {}}
        ev = {}
        for f in FMT:
            T = G["tables"][f]
            s = kk if f == FMT[0] else len(G["pats"][f][0])
            nb = G["nb"]
            k, n = g["k"], g["n"]
            e1 = sum(math.comb(k, m) * math.comb(nb, b) * math.comb(n - k - nb, s - m - b) / math.comb(n, s) * T[m, b]
                     for m in range(min(s, k) + 1) for b in range(nb + 1) if m + b <= s)
            ev[f] = e1 * len(G["pats"][f]) if f != FMT[0] else e1 * 10
        fmtm = lambda x: f"{x:+,.0f}"  # noqa: E731
        med = lambda v: f"{np.median(v):+,.0f} ({np.min(v):+,.0f} to {np.max(v):+,.0f})"  # noqa: E731
        md_p += [f"## {g['label']}", ""]
        for fi, f in enumerate(FMT):
            c = cost[f]
            exp10 = ls.HOLD * (ev[f] - c)
            summ = []
            for sh in range(nc):
                pre, hold = PRE[:, sh, fi].astype(float), HO[:, sh, fi].astype(float)
                hs = hold.sum(1)
                fo = np.argsort(-pre, kind="stable")[:10]
                cum = pre[:, None] + np.c_[np.zeros(NL), np.cumsum(hold, 1)[:, :-1]]
                roll = sum(hold[int(np.argmax(cum[:, t])), t] for t in range(ls.HOLD))
                summ.append({"best": hs.max(), "in_profit": int((hs > 0).sum()), "mean": hs.mean(),
                             "frozen1": hs[fo[0]], "frozen10": hs[fo].mean(), "rolling": roll})
            R0, SH = summ[0], summ[1:]
            pre0, hold0 = PRE[:, 0, fi].astype(float), HO[:, 0, fi].astype(float)
            hs0 = hold0.sum(1)
            wins0 = (hold0 + c > 0.5).sum(1)
            rank_pre = np.empty(NL, int)
            rank_pre[np.argsort(-pre0, kind="stable")] = np.arange(1, NL + 1)
            ret_pre = 1 + pre0 / (c * (R - lo))
            cum0 = pre0[:, None] + np.c_[np.zeros(NL), np.cumsum(hold0, 1)[:, :-1]]
            picks = [int(np.argmax(cum0[:, t])) for t in range(ls.HOLD)]
            row = lambda i: {"lead": lab(i)[0], "pattern": lab(i)[1], "profit": round(float(hs0[i]), 1),  # noqa: E731
                             "wins": int(wins0[i]), "best": [int(x) for x in HC[i, 0, fi]], "rank_earlier": int(rank_pre[i]),
                             "return_earlier": round(float(ret_pre[i]), 4)}
            game["formats"][f] = {"cost": c, "expected_profit_10": round(exp10, 1),
                                  "real": {k_: float(v) for k_, v in R0.items()},
                                  "shifted": {k_: [float(x[k_]) for x in SH] for k_ in R0},
                                  "top_profit": [row(i) for i in np.argsort(-hs0, kind="stable")[:TOPN]],
                                  "top_wins": [row(i) for i in np.lexsort((-hs0, -wins0))[:10]],
                                  "top_earlier": [row(i) for i in np.argsort(-pre0, kind="stable")[:10]],
                                  "rolling": [{"date": g["dates"][R + t], "lead": " ".join(lab(i)), "profit": float(hold0[i, t])}
                                              for t, i in enumerate(picks)]}
            F = game["formats"][f]
            md_p += [f"### {f} (RM{c} a draw)", "",
                     f"Random entries, expected over 10 draws: {fmtm(exp10)} (return {100 * ev[f] / c:.0f}%).", "",
                     "| | Real calendar | 20 shifted calendars: median (range) |", "|---|---|---|",
                     f"| Best lead, last 10 (hindsight) | {fmtm(R0['best'])} | {med(F['shifted']['best'])} |",
                     f"| Leads in profit, last 10 | {R0['in_profit']:,} | {np.median(F['shifted']['in_profit']):,.0f} ({min(F['shifted']['in_profit']):,.0f}-{max(F['shifted']['in_profit']):,.0f}) |",
                     f"| Average lead, last 10 | {fmtm(R0['mean'])} | {med(F['shifted']['mean'])} |",
                     f"| #1 by earlier profit, played on the last 10 | {fmtm(R0['frozen1'])} | {med(F['shifted']['frozen1'])} |",
                     f"| Top 10 by earlier profit, average | {fmtm(R0['frozen10'])} | {med(F['shifted']['frozen10'])} |",
                     f"| Re-ranked by profit before every draw, #1 played | {fmtm(R0['rolling'])} | {med(F['shifted']['rolling'])} |", "",
                     "| # | Lead | Pattern | Profit, last 10 (RM) | Winning draws | Best set per draw | Rank earlier | Earlier return |",
                     "|---|---|---|---|---|---|---|---|"]
            for i, r in enumerate(F["top_profit"][:10], 1):
                md_p.append(f"| {i} | {r['lead']} | {r['pattern']} | {fmtm(r['profit'])} | {r['wins']}/10 | "
                            f"{' '.join(tier(x, kk) for x in r['best'])} | {r['rank_earlier']:,} | {100 * r['return_earlier']:.0f}% |")
            md_p += ["", "Re-ranked before every draw (#1 lead each draw): " + "; ".join(
                f"{x['date'][5:]} {x['lead']} {fmtm(x['profit'])}" for x in F["rolling"]) + ".", ""]
        # ---------------- combined
        rows = []
        for fi, f in enumerate(FMT):
            c = cost[f]
            h = HO[:, 0, fi].astype(float)
            for i in range(NL):
                rows.append((i, f, c, h[i].sum(), int((h[i] + c > 0.5).sum()), float(PRE[i, 0, fi]), int(ST[i, 0, fi, 0])))
        margin = np.array([r[3] / (10 * r[2]) for r in rows])
        wins = np.array([r[4] for r in rows])
        sc = (rank_desc(margin) + rank_desc(wins)) / 2
        pmar = np.array([r[5] / ((R - lo) * r[2]) for r in rows])
        prate = np.array([r[6] / (R - lo) for r in rows])
        psc = (rank_desc(pmar) + rank_desc(prate)) / 2
        best = np.argsort(sc, kind="stable")[:20]
        pick = np.argsort(psc, kind="stable")[:10]
        pick_profit = float(np.mean([rows[i][3] for i in pick]))
        ctrl = []
        for sh in range(1, nc):
            pm = np.concatenate([PRE[:, sh, fi] / ((R - lo) * cost[f]) for fi, f in enumerate(FMT)])
            pr_ = np.concatenate([ST[:, sh, fi, 0] / (R - lo) for fi, f in enumerate(FMT)])
            pk = np.argsort((rank_desc(pm) + rank_desc(pr_)) / 2, kind="stable")[:10]
            hp = np.concatenate([HO[:, sh, fi].sum(1) for fi in range(4)])
            ctrl.append(float(hp[pk].mean()))
        game["combined"] = {"top": [{"lead": " ".join(lab(rows[i][0])), "format": rows[i][1], "stake": 10 * rows[i][2],
                                     "profit": rows[i][3], "margin": float(margin[i]), "wins": rows[i][4], "score": float(sc[i])}
                                    for i in best],
                            "picked_profit_mean": pick_profit, "control": ctrl,
                            "picked": [{"lead": " ".join(lab(rows[i][0])), "format": rows[i][1], "profit": rows[i][3],
                                        "wins": rows[i][4], "earlier_margin": float(pmar[i])} for i in pick]}
        C = game["combined"]
        md_c += [f"## {g['label']}", "",
                 f"Top 10 by the same score on the earlier draws, average profit on the last 10: {fmtm(pick_profit)} "
                 f"(the same choice on the 20 shifted calendars: median {np.median(ctrl):+,.0f}, range {min(ctrl):+,.0f} to {max(ctrl):+,.0f}).", "",
                 "| # | Lead | Format | Stake (RM) | Profit (RM) | Margin | Winning draws | Score |", "|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(C["top"], 1):
            md_c.append(f"| {i} | {r['lead']} | {r['format']} | {r['stake']} | {fmtm(r['profit'])} | {100 * r['margin']:+,.0f}% | {r['wins']}/10 | {r['score']:,.0f} |")
        md_c += ["", "Chosen on the earlier draws:", "", "| # | Lead | Format | Earlier margin | Profit, last 10 (RM) | Winning draws |", "|---|---|---|---|---|---|"]
        for i, r in enumerate(C["picked"], 1):
            md_c.append(f"| {i} | {r['lead']} | {r['format']} | {100 * r['earlier_margin']:+.0f}% | {fmtm(r['profit'])} | {r['wins']}/10 |")
        md_c.append("")
        # ---------------- null test over the whole history
        spans = {"whole history": (lo, d), "earlier draws": (lo, R), "last 10 draws": (R, d)}
        game["null"] = {}
        md_n += [f"## {g['label']}", "", "| Format | Draws | Level | Real | Shifted: mean (min-max) | Rank | Share ≥ real |", "|---|---|---|---|---|---|---|"]
        for fi, f in enumerate(FMT):
            for sname, (a, b) in spans.items():
                for li, lvn in enumerate((hl, tl)):
                    v = AG[:, fi, li, a:b].sum(1)
                    real, null = int(v[0]), v[1:]
                    rk = int((null > real).sum()) + 1
                    share = float((null >= real).mean())
                    game["null"][f"{f} | {sname} | {lvn}"] = {"real": real, "shifted": null.tolist(), "rank": rk, "share": share}
                    md_n.append(f"| {f} | {sname} | {lvn} | {real:,} | {null.mean():,.0f} ({null.min():,}-{null.max():,}) | {rk}/{nc} | {share:.2f} |")
        md_n.append("")
        # ---------------- per-lead 5+ hits against own shifted calendars
        five = ST[:, :, :, 1].sum(2).astype(float)                     # leads x calendars
        six = ST[:, :, :, 2].sum(2)

        def choose(c_):
            oth = [x for x in range(nc) if x != c_]
            mu, sd = five[:, oth].mean(1), five[:, oth].std(1)
            z = (five[:, c_] - mu) / np.maximum(sd, 1.0)
            return np.lexsort((-five[:, c_], -z))[:10], z, mu
        top, z, mu = choose(0)
        fwd = int((HC[top, 0] >= G["hi"]).sum())
        ctrl5 = [int((HC[choose(c_)[0], c_] >= G["hi"]).sum()) for c_ in range(1, nc)]
        hits5 = (ST[:, 0, :, 1].sum(1))
        game["lead_hits"] = {"top": [{"lead": " ".join(lab(i)), "z": float(z[i]), "five_earlier": int(five[i, 0]),
                                      "shifted_mean": float(mu[i]), "six_earlier": int(six[i, 0]),
                                      "five_last10": int((HC[i, 0] >= G["hi"]).sum()),
                                      "profit_last10": [float(HO[i, 0, fi].sum()) for fi in range(4)]} for i in top],
                             "forward_real": fwd, "forward_control": ctrl5,
                             "avg_lead_five_last10": float((HC[:, 0] >= G["hi"]).sum((1, 2)).mean())}
        LH = game["lead_hits"]
        md_l += [f"## {g['label']}", "",
                 f"| # | Lead | Pattern | Earlier {hl} hits (shifted mean) | z | Earlier {tl}-number hits | Last 10: {hl} hits | Last 10 profit (RM): {' / '.join(FMT)} |",
                 "|---|---|---|---|---|---|---|---|"]
        for num, (i_, r) in enumerate(zip(top, LH["top"]), 1):
            ld, pt = lab(i_)
            md_l.append(f"| {num} | {ld} | {pt} | {r['five_earlier']} ({r['shifted_mean']:.1f}) | {r['z']:+.2f} | {r['six_earlier']} | "
                        f"{r['five_last10']} | {' / '.join(fmtm(x) for x in r['profit_last10'])} |")
        md_l += ["", f"Forward check: the 10 leads got {fwd} {hl} hits on the last 10 draws (all formats); an average lead gets "
                 f"{LH['avg_lead_five_last10']:.3f}, 10 leads ≈ {10 * LH['avg_lead_five_last10']:.2f}. The same choice on each shifted "
                 f"calendar: {', '.join(map(str, ctrl5))}.", ""]
        # how unusual is the top lead among all leads
        me = int(five[top[0], 0])
        md_l += [f"Top lead {' '.join(lab(top[0]))}: {me} {hl} hits on the earlier draws. Leads with at least {me}: "
                 f"{int((five[:, 0] >= me).sum())} on the real calendar; shifted calendars "
                 f"{', '.join(str(int((five[:, c_] >= me).sum())) for c_ in range(1, nc))}.", ""]
        game["lead_hits"]["top_lead_rarity"] = {"hits": me, "real": int((five[:, 0] >= me).sum()),
                                                "shifted": [int((five[:, c_] >= me).sum()) for c_ in range(1, nc)]}
        # ---------------- each pattern: high hits of all its leads, real vs shifted (whole history)
        pat_of = np.arange(NL) % NP
        game["patterns"] = {}
        md_n += ["", f"Each pattern on its own ({hl} hits over the whole history, all formats, all its leads):", "",
                 "| Pattern | Real | Shifted mean (min-max) | Rank | z |", "|---|---|---|---|---|"]
        for pi, pn in enumerate(PATS):
            v = ST[pat_of == pi][:, :, :, 1].sum((0, 2)).astype(float)
            real, null = v[0], v[1:]
            z = float((real - null.mean()) / max(null.std(), 1e-9))
            rk = int((null > real).sum()) + 1
            game["patterns"][pn] = {"real": real, "mean": float(null.mean()), "rank": rk, "z": z}
            md_n.append(f"| {pn}{' (new)' if pn in NEW else ''} | {real:,.0f} | {null.mean():,.0f} ({null.min():,.0f}-{null.max():,.0f}) | {rk}/{nc} | {z:+.2f} |")
        md_n.append("")
        res[key] = game
        with open(os.path.join(A, f"leads7{TAG}_results.json"), "w") as fh:
            json.dump(res, fh, indent=1, default=float)
        print(g["label"], "done", f"{time.time() - t0:.0f}s", flush=True)
    for name, md in ((f"LEADS7{TAG.upper()}_PROFIT.md", md_p), (f"LEADS7{TAG.upper()}_COMBINED.md", md_c),
                     (f"LEADS7{TAG.upper()}_HIGH_HITS_NULL.md", md_n), (f"LEADS7{TAG.upper()}_LEAD_HIGH_HITS.md", md_l)):
        md.insert(2, f"History window: **{WINDOW}** (which earlier draws of each lead's cell are counted).")
        md.insert(3, "")
        with open(os.path.join(A, name), "w") as fh:
            fh.write("\n".join(md) + "\n")
    print("wrote all in", f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
