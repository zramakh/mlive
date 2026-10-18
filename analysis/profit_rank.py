#!/usr/bin/env python3
"""Magnum Life: rank every lead by the money it would have made, using the official prize table.

Prize per 8-number combination (magnum4d.my, Magnum Life and System Play 9 / 10 prize sheets):
    8 winning                 Grand  RM1,000 a day for 20 years (counted as RM7,300,000)
    7 winning + bonus         2nd    RM1,000 a day for 100 days (RM100,000)
    7 winning                 3rd    RM6,000
    6 winning + bonus         4th    RM600
    6 winning                 5th    RM100
    5 winning + bonus         6th    RM30
    5 winning                 7th    RM10
    4 winning + bonus         8th    RM5
A combination holding both bonus numbers wins its "+ bonus" prize twice (System Play sheets, e.g. System 10
with 8 + 2 bonus = 1 Grand, 16 x 2nd, 56 x 4th). An ordinary bet costs RM1; System 9 = 9 combinations (RM9),
System 10 = 45 combinations (RM45), each combination paid as above.

Every lead (114 parameters and their pairs, plus plain hot / cold over all draws, x hot / cold / position /
hot+100) builds its tickets before each draw from counts updated on every earlier draw. For each lead:
  - profit on the last 10 draws (the hindsight ranking),
  - profit on the earlier draws (25-100% of the history before the last 10) and the last-10 profit of the
    leads that ranked best there (an honest choice made before the 10 draws),
  - rolling: before each of the last 10 draws, re-rank by profit on all earlier draws and play the #1 lead.
Controls: the same on SHIFTS shifted calendars, and the expected loss of random tickets.

python3 analysis/profit_rank.py --tickets 10 --bonus                         10 ordinary RM1 tickets
python3 analysis/profit_rank.py --system 9 --sets 2 --structure overlap --bonus
python3 analysis/profit_rank.py --system 9 --sets 2 --structure disjoint --bonus
python3 analysis/profit_rank.py --system 10 --sets 1 --bonus
    -> analysis/profit_<tag>_results.json, analysis/PROFIT_<TAG>.md
"""

import itertools
import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

if "--games" not in sys.argv:
    sys.argv += ["--games", "ml8"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import extra_astro as xa  # noqa: E402
import lead_search10 as ls  # noqa: E402  (reads the same command-line options)

KEY = "ml8"
SHIFTS = 2
TOPN = 20
GRAND = 1000 * 365 * 20
PRIZE = {(8, 0): GRAND, (7, 1): 100000, (7, 0): 6000, (6, 1): 600, (6, 0): 100, (5, 1): 30, (5, 0): 10, (4, 1): 5}
SET = ls.SYSTEM or 8
OUT = os.path.join(common.ROOT, "analysis", f"profit_{ls.TAG}_results.json")
MD = os.path.join(common.ROOT, "analysis", f"PROFIT_{ls.TAG.upper()}.md")
ARR = os.path.join(common.ROOT, "analysis", "profit_arrays")                 # per-lead arrays (not committed)


def prize8(m, b):
    """One 8-number combination with m winning and b bonus numbers."""
    if m == 8:
        return PRIZE[(8, 0)]
    if b == 0:
        return PRIZE.get((m, 0), 0)
    return b * PRIZE.get((m, 1), 0)


def pay_table(s):
    """Payout of an s-number entry (all its 8-number combinations) by winning / bonus numbers inside it."""
    T = np.zeros((9, 3))
    for m in range(9):
        for b in range(3):
            if m + b > s:
                continue
            o = s - m - b
            T[m, b] = sum(math.comb(m, a) * math.comb(b, c) * math.comb(o, 8 - a - c) * prize8(a, c)
                          for a in range(m + 1) for c in range(b + 1) if 0 <= 8 - a - c <= o)
    return T


PAY = pay_table(SET)
COST = math.comb(SET, 8) * len(ls.swap_patterns(8))


def expected_return():
    """Exact expected payout per draw of this entry for a fair draw (8 winning + 2 bonus of 36)."""
    n, s = 36, SET
    tot = 0.0
    for m in range(9):
        for b in range(3):
            if m + b <= s:
                p = math.comb(8, m) * math.comb(2, b) * math.comb(26, s - m - b) / math.comb(n, s)
                tot += p * PAY[m, b]
    return tot * len(ls.swap_patterns(8))


def win_chance(sims=200000):
    """Chance that this entry wins any prize on a fair draw (Monte Carlo over the ranks the tickets use)."""
    rng = np.random.default_rng(1)
    pats = ls.swap_patterns(8)
    kt = ls.ktop(8)
    pos = np.argsort(rng.random((sims, 36)), 1)[:, :10]
    w = np.zeros((sims, kt), np.int64)
    b = np.zeros((sims, kt), np.int64)
    for j in range(kt):
        w[:, j] = (pos[:, :8] == j).any(1)
        b[:, j] = (pos[:, 8:] == j).any(1)
    pay = sum(PAY[w[:, q].sum(1), b[:, q].sum(1)] for q in pats)
    return float((pay > 0).mean())


def series(task):
    """Profit per draw for a chunk of sets (all four patterns)."""
    sh, sets = task
    if ls.W.get("key") != KEY:
        ls.init(KEY)
    codes = np.roll(ls.W["codes"], ls.W["shifts"][sh], axis=0)
    k, n, H = ls.W["k"], ls.W["n"], ls.W["H"]
    out, labels = [], []
    for s in sets:
        cid = np.zeros(len(H), np.int64)
        for j in s:
            cid = cid * 1000 + codes[:, j]
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
        dp = ex(np.ones((len(cid), 1), np.float32))
        cnt = ex(H)
        e = dp * k / n
        zc = (cnt - e) / np.sqrt(e * (1 - k / n) + 1e-6)
        scores = {"hot": cnt - e, "cold": e - cnt,
                  "pos": ((ex(ls.W["P"]) + ls.SMOOTH * ls.W["pglob"]) / (dp[:, :, None] + ls.SMOOTH)).sum(1),
                  "hot+100": zc + ls.W["hot100"]}
        kt = ls.ktop(k)
        for p, S in scores.items():
            S = S + ls.W["tie"]
            top = np.argpartition(-S, kt - 1, 1)[:, :kt]
            top = np.take_along_axis(top, np.argsort(-np.take_along_axis(S, top, 1), 1), 1)
            war = np.take_along_axis(H, top, 1).astype(np.int64)
            warb = np.take_along_axis(ls.W["Bn"], top, 1).astype(np.int64)
            prof = -float(COST) * np.ones(len(H))
            for q in ls.W["pats"]:
                prof += PAY[war[:, q].sum(1), warb[:, q].sum(1)]
            out.append(prof.astype(np.float32))
            labels.append((s, p))
    return sh, labels, np.array(out)


def main():
    names = common.ALL_PARAMS + xa.extra_params()
    lab = lambda s: " × ".join(names[j] for j in s) if s else "all draws (no astrology)"  # noqa: E731
    sets = [()] + [(i,) for i in range(len(names))] + list(itertools.combinations(range(len(names)), 2))
    tasks = [(sh, sets[i:i + 200]) for sh in range(SHIFTS + 1) for i in range(0, len(sets), 200)]
    store = {}
    with Pool(4) as pool:
        for sh, labels, o in pool.imap_unordered(series, tasks):
            st = store.setdefault(sh, {"labels": [], "prof": []})
            st["labels"] += labels
            st["prof"].append(o)
    g = common.load_game(KEY)
    d = len(g["dates"])
    R = d - ls.HOLD
    lo = int(0.25 * R)
    er = expected_return()
    exp10 = round(ls.HOLD * (er - COST), 2)
    pwin = win_chance()
    res = {"format": ls.TLAB, "cost_per_draw": COST, "win_chance_per_draw": round(pwin, 4), "expected_return_per_draw": round(er, 4),
           "expected_profit_10_draws": exp10, "prize_table": {f"{m}+{b}": float(PAY[m, b]) for m in range(9)
                                                              for b in range(3) if PAY[m, b]}}
    for sh in range(SHIFTS + 1):
        st = store[sh]
        P = np.vstack(st["prof"]).astype(np.float64)
        L = st["labels"]
        pre = P[:, lo:R].sum(1)
        hold = P[:, R:].sum(1)
        rank_pre = np.empty(len(P), int)
        rank_pre[np.argsort(-pre, kind="stable")] = np.arange(1, len(P) + 1)
        picks = []
        for t in range(R, d):
            i = int(np.argmax(P[:, lo:t].sum(1)))
            picks.append({"date": g["dates"][t], "lead": lab(L[i][0]), "pattern": L[i][1],
                          "profit_before": round(float(P[i, lo:t].sum()), 1), "profit": round(float(P[i, t]), 1)})
        fo = np.argsort(-pre, kind="stable")[:10]
        wins = (P[:, R:] + COST > 0.5).sum(1)
        rate_pre = (P[:, lo:R] + COST > 0.5).mean(1)
        hits = np.lexsort((-hold, -wins))[:TOPN]
        hits_pre = np.lexsort((-pre, -rate_pre))[:10]
        ho = np.argsort(-hold, kind="stable")
        row = lambda i: {"lead": lab(L[i][0]), "pattern": L[i][1], "profit_last10": round(float(hold[i]), 1),  # noqa: E731
                         "per_draw": [round(float(x), 1) for x in P[i, R:]], "profit_earlier": round(float(pre[i]), 1),
                         "earlier_per_draw": round(float(pre[i] / (R - lo)), 3), "rank_earlier": int(rank_pre[i]),
                         "wins_last10": int(wins[i]), "win_rate_earlier": round(float(rate_pre[i]), 4)}
        os.makedirs(ARR, exist_ok=True)
        np.savez_compressed(os.path.join(ARR, f"{ls.TAG}_sh{sh}.npz"), hold=P[:, R:].astype(np.float32),
                            pre=pre, rate_pre=rate_pre, labels=np.array([f"{lab(x[0])}|{x[1]}" for x in L]))
        res["real" if sh == 0 else f"shift{sh}"] = {
            "summary": {"best_last10": round(float(hold.max()), 1), "leads_in_profit_last10": int((hold > 0).sum()),
                        "leads": len(P), "frozen_top1": round(float(hold[fo[0]]), 1),
                        "frozen_top10_mean": round(float(hold[fo].mean()), 1),
                        "rolling_top1": round(sum(x["profit"] for x in picks), 1),
                        "all_leads_mean_last10": round(float(hold.mean()), 2),
                        "best_earlier": round(float(pre.max()), 1),
                        "leads_in_profit_earlier": int((pre > 0).sum()),
                        "most_wins_last10": int(wins.max()), "leads_with_most_wins": int((wins == wins.max()).sum()),
                        "best_win_rate_earlier": round(float(rate_pre.max()), 4),
                        "top_rate_earlier_wins_last10": round(float(wins[hits_pre].mean()), 1),
                        "top_rate_earlier_profit_last10": round(float(hold[hits_pre].mean()), 1)},
            "top_hits_last10": [row(i) for i in hits], "top_hits_earlier": [row(i) for i in hits_pre],
            "top_last10": [row(i) for i in ho[:TOPN]], "top_earlier": [row(i) for i in fo],
            "named": [row(i) for i in range(len(L)) if (lab(L[i][0]), L[i][1]) in
                      {(a, b) for a, b in ls.NAMED["ml8"]} | {("mars_rashi × sun_sign_tropical", "cold"),
                                                              ("venus_nakshatra × kp_moon_sub_lord", "hot")}]
            if sh == 0 else [],
            "rolling": picks}
    R0 = res["real"]
    shs = [res[f"shift{i}"]["summary"] for i in range(1, SHIFTS + 1)]
    s0 = R0["summary"]
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
    fmt = lambda x: f"{x:+,.0f}"  # noqa: E731
    join = lambda key, f: ", ".join(f.format(x[key]) for x in shs)  # noqa: E731
    md = [f"# Magnum Life: leads ranked by profit ({ls.TLAB})", "",
          "Generated by `analysis/profit_rank.py`. Official Magnum Life prize table per 8-number combination: 8 = Grand "
          "(RM1,000 a day for 20 years, counted as RM7.3m), 7+bonus = RM100,000, 7 = RM6,000, 6+bonus = RM600, 6 = RM100, "
          "5+bonus = RM30, 5 = RM10, 4+bonus = RM5; a combination with both bonus numbers wins its +bonus prize twice. "
          f"Cost RM{COST} per draw. Hot / cold counts are updated before every draw (each lead's tickets for a draw use "
          "only earlier draws).", "",
          f"Random tickets return RM{er:.2f} of every RM{COST} on average (prizes are mostly the Grand prize), so the "
          f"expected result over 10 draws is RM{exp10:+,.2f}.", "",
          "| | Real calendar | Shifted calendars |", "|---|---|---|",
          f"| Leads tested | {s0['leads']:,} | |",
          f"| Best lead's profit on the last 10 draws (hindsight) | {fmt(s0['best_last10'])} | {', '.join(fmt(x['best_last10']) for x in shs)} |",
          f"| Leads in profit on the last 10 draws | {s0['leads_in_profit_last10']:,} | {join('leads_in_profit_last10', '{:,}')} |",
          f"| Average lead, last 10 draws | {fmt(s0['all_leads_mean_last10'])} | {', '.join(fmt(x['all_leads_mean_last10']) for x in shs)} |",
          f"| #1 lead by earlier profit, played on the last 10 | {fmt(s0['frozen_top1'])} | {', '.join(fmt(x['frozen_top1']) for x in shs)} |",
          f"| Top 10 by earlier profit, average on the last 10 | {fmt(s0['frozen_top10_mean'])} | {', '.join(fmt(x['frozen_top10_mean']) for x in shs)} |",
          f"| Re-ranked by profit before every draw, #1 played | {fmt(s0['rolling_top1'])} | {', '.join(fmt(x['rolling_top1']) for x in shs)} |",
          f"| Leads in profit on the earlier draws | {s0['leads_in_profit_earlier']:,} | {join('leads_in_profit_earlier', '{:,}')} |",
          "", f"## Top {TOPN} leads by profit on the last 10 draws (hindsight)", "",
          f"*Rank earlier* = rank by profit on the {R - lo} earlier draws (of {s0['leads']:,}).", "",
          "| # | Lead | Pattern | Profit, last 10 (RM) | Per draw (RM) | Rank earlier | Profit earlier (RM) |",
          "|---|---|---|---|---|---|---|"]
    for i, r in enumerate(R0["top_last10"], 1):
        md.append(f"| {i} | {r['lead']} | {r['pattern']} | {fmt(r['profit_last10'])} | {' '.join(fmt(x) for x in r['per_draw'])} | "
                  f"{r['rank_earlier']:,} | {fmt(r['profit_earlier'])} |")
    md += ["", "## Top 10 leads by profit on the earlier draws, played on the last 10", "",
           "| # | Lead | Pattern | Profit earlier (RM) | Profit, last 10 (RM) | Per draw (RM) |", "|---|---|---|---|---|---|"]
    for i, r in enumerate(R0["top_earlier"], 1):
        md.append(f"| {i} | {r['lead']} | {r['pattern']} | {fmt(r['profit_earlier'])} | {fmt(r['profit_last10'])} | "
                  f"{' '.join(fmt(x) for x in r['per_draw'])} |")
    md += ["", "## Earlier leads", "", "| Lead | Pattern | Profit, last 10 (RM) | Per draw (RM) | Rank earlier | Profit earlier (RM) |",
           "|---|---|---|---|---|---|"]
    for r in sorted(R0["named"], key=lambda r: -r["profit_last10"]):
        md.append(f"| {r['lead']} | {r['pattern']} | {fmt(r['profit_last10'])} | {' '.join(fmt(x) for x in r['per_draw'])} | "
                  f"{r['rank_earlier']:,} | {fmt(r['profit_earlier'])} |")
    sh_w = ", ".join(str(x["most_wins_last10"]) for x in shs)
    md += ["", f"## Top {TOPN} leads by winning draws on the last 10 (hindsight)", "",
           f"*Winning draw* = the entry wins any prize. A random entry wins on {100 * pwin:.1f}% of draws "
           f"({ls.HOLD * pwin:.1f} of 10). Most winning draws by any lead: {s0['most_wins_last10']} "
           f"({s0['leads_with_most_wins']:,} leads; shifted calendars: {sh_w}). Ties broken by profit.", "",
           "| # | Lead | Pattern | Winning draws | Profit, last 10 (RM) | Per draw (RM) | Earlier win rate | Rank earlier (profit) |",
           "|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(R0["top_hits_last10"], 1):
        md.append(f"| {i} | {r['lead']} | {r['pattern']} | {r['wins_last10']}/10 | {fmt(r['profit_last10'])} | "
                  f"{' '.join(fmt(x) for x in r['per_draw'])} | {100 * r['win_rate_earlier']:.1f}% | {r['rank_earlier']:,} |")
    md += ["", "## Top 10 leads by win rate on the earlier draws, played on the last 10", "",
           f"Average on the last 10: {s0['top_rate_earlier_wins_last10']} winning draws, profit {fmt(s0['top_rate_earlier_profit_last10'])} "
           f"(shifted calendars: {', '.join(str(x['top_rate_earlier_wins_last10']) for x in shs)} winning draws, "
           f"{', '.join(fmt(x['top_rate_earlier_profit_last10']) for x in shs)}).", "",
           "| # | Lead | Pattern | Earlier win rate | Profit earlier (RM) | Winning draws, last 10 | Profit, last 10 (RM) | Per draw (RM) |",
           "|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(R0["top_hits_earlier"], 1):
        md.append(f"| {i} | {r['lead']} | {r['pattern']} | {100 * r['win_rate_earlier']:.1f}% | {fmt(r['profit_earlier'])} | "
                  f"{r['wins_last10']}/10 | {fmt(r['profit_last10'])} | {' '.join(fmt(x) for x in r['per_draw'])} |")
    md += ["", "## Re-ranked by profit before every draw", "",
           "| Draw | #1 lead | Pattern | Profit before this draw (RM) | Profit on this draw (RM) |", "|---|---|---|---|---|"]
    for x in R0["rolling"]:
        md.append(f"| {x['date']} | {x['lead']} | {x['pattern']} | {fmt(x['profit_before'])} | {fmt(x['profit'])} |")
    with open(MD, "w") as fh:
        fh.write("\n".join(md) + "\n")
    print(ls.TLAB, "cost", COST, "expected return", round(er, 3), "expected 10-draw", exp10)
    print("real", s0)
    for i, x in enumerate(shs, 1):
        print(f"shift{i}", x)
    for r in R0["top_last10"][:10]:
        print(f"  {r['lead'][:50]:<50} {r['pattern']:<8} {r['profit_last10']:>10,.0f} rank earlier {r['rank_earlier']}")
    print("wrote", OUT, "and", MD)


if __name__ == "__main__":
    main()
