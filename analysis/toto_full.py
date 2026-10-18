#!/usr/bin/env python3
"""Sports Toto (Star 6/50, Power 6/55, Supreme 6/58): the Magnum Life analyses repeated for every astrological
lead, with the official prizes, in four formats, against 20 shifted calendars.

Formats per draw (ranks of the lead's numbers, 0 = best):
    10 sets                 the top 6 and one- / two-number swaps (lead_search10.py), 10 ordinary bets
    System 7 × 2 overlap    ranks 1-7 and ranks 1-4 + 8-10 (2 x 7 bets)
    System 7 × 2 disjoint   ranks 1-7 and 8-14 (2 x 7 bets)
    System 8 × 1            ranks 1-8 (28 bets)
A System S entry is every 6-number combination of its S numbers, each paid as an ordinary bet (RM1 a bet, RM2 for
Supreme). Prizes as in toto_profit.py (jackpots at their minimum).

Leads: 114 parameters and their pairs, plus plain hot / cold over all draws, x hot / cold / position / hot+100,
built before each draw from earlier draws in the same cell. Calendars: the real one and SHIFTS rolled by random
offsets (same draws, astrological codes out of line with them).

Outputs (analysis/):
    TOTO_SYSTEM_PROFIT.md     profit, winning draws, earlier choices, re-ranking before every draw, per format
    TOTO_COMBINED.md          all formats ranked by margin and winning draws
    TOTO_HIGH_HITS_NULL.md    5- and 6-number hits over the whole history, real vs shifted, + Magnum Life comparison
    TOTO_LEAD_HIGH_HITS.md    leads with the most 5+ hits against their own shifted calendars, + the top lead in detail
    toto_full_results.json
python3 analysis/toto_full.py
"""

import itertools
import json
import math
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

if "--games" not in sys.argv:
    sys.argv += ["--games", "toto50,toto55,toto58"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import extra_astro as xa  # noqa: E402
import lead_search10 as ls  # noqa: E402
import toto_profit as tp  # noqa: E402

A = os.path.join(common.ROOT, "analysis")
SHIFTS = 20
TOPN = 20
KT = 14
FMT = ["10 sets", "System 7 × 2 overlap", "System 7 × 2 disjoint", "System 8 × 1"]
SYS_PATS = {"System 7 × 2 overlap": [list(range(7)), list(range(4)) + [7, 8, 9]],
            "System 7 × 2 disjoint": [list(range(7)), list(range(7, 14))],
            "System 8 × 1": [list(range(8))]}
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


def setup(key):
    if G.get("key") != key:
        tp.init(key)
        R = ls.W["R"]
        rng = np.random.default_rng(2024)
        G.clear()
        G.update(key=key, shifts=[0] + [int(x) for x in rng.choice(np.arange(160, R - 160), SHIFTS, replace=False)],
                 pats={"10 sets": ls.W["pats"], **SYS_PATS},
                 tables={"10 sets": tp.pay_table(key), **{f: sys_table(key, len(p[0])) for f, p in SYS_PATS.items()}},
                 cost={f: tp.PRICE[key] * (10 if f == "10 sets" else sum(math.comb(len(q), 6) for q in SYS_PATS[f])) for f in FMT})


def series(task):
    """Per lead: earlier profit / winning draws / 5+ / 6 hits, last-10 profit and best set per draw, per format;
    per draw: 5+ and 6 hits summed over the chunk's leads."""
    key, sh, sets = task
    setup(key)
    codes = np.roll(ls.W["codes"], G["shifts"][sh], axis=0)
    k, n, H, Bn, R = ls.W["k"], ls.W["n"], ls.W["H"], ls.W["Bn"], ls.W["R"]
    d = len(H)
    lo = int(0.25 * R)
    nl = len(sets) * 4
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
            war = np.take_along_axis(H, top, 1).astype(np.int64)
            warb = np.take_along_axis(Bn, top, 1).astype(np.int64)
            for fi, f in enumerate(FMT):
                T = G["tables"][f]
                pay = np.zeros(d)
                best = np.zeros(d, np.int64)
                for q in G["pats"][f]:
                    m, b = war[:, q].sum(1), warb[:, q].sum(1)
                    pay += T[m, b]
                    m6 = np.minimum(m, 6)
                    b6 = np.minimum(b, 6 - m6)
                    best = np.maximum(best, 2 * m6 + (b6 > 0) * (m6 < 6))
                prof = pay - G["cost"][f]
                pre[li, fi] = prof[lo:R].sum()
                stat[li, fi] = ((pay[lo:R] > 0).sum(), (best[lo:R] >= 10).sum(), (best[lo:R] >= 12).sum())
                hold[li, fi] = prof[R:]
                hcode[li, fi] = best[R:]
                agg[fi, 0] += best >= 10
                agg[fi, 1] += best >= 12
            li += 1
    return key, sh, sets[0], pre, stat, hold, hcode, agg


def rank_desc(x):
    order = np.argsort(-x, kind="stable")
    xs = x[order]
    r = np.empty(len(x))
    first = np.r_[0, np.flatnonzero(np.diff(xs)) + 1]
    r[order] = np.repeat(first + 1, np.diff(np.r_[first, len(x)]))
    return r


def tier(c):
    return "6" if c == 12 else f"{c // 2}{'+b' if c % 2 else ''}"


def main():
    t0 = time.time()
    names = common.ALL_PARAMS + xa.extra_params()
    sets = [()] + [(i,) for i in range(len(names))] + list(itertools.combinations(range(len(names)), 2))
    idx = {s: i for i, s in enumerate(sets)}
    pats = ["hot", "cold", "pos", "hot+100"]
    lab = lambda i: (" × ".join(names[j] for j in sets[i // 4]) if sets[i // 4] else "all draws (no astrology)", pats[i % 4])  # noqa: E731
    NL = len(sets) * 4
    res = {}
    md_p = ["# Sports Toto system play and 10 sets: leads ranked by profit", "",
            "Generated by `analysis/toto_full.py`. Every astrological lead (26,224) in four formats: 10 sets, System 7 × 2 "
            "(overlap: ranks 1-7 and 1-4 + 8-10; disjoint: ranks 1-7 and 8-14) and System 8 × 1 (ranks 1-8). A System S "
            "entry = every 6-number combination of its S numbers, each paid as an ordinary bet (System 7 = 7 bets, "
            "System 8 = 28). Prizes: official tables, jackpots at their minimum (see TOTO_PROFIT.md). Numbers built before "
            f"each draw from earlier draws only. Shifted calendars: {SHIFTS}, shown as median (min-max).", ""]
    md_c = ["# Sports Toto: all formats ranked by stake, profit and winning draws", "",
            "Generated by `analysis/toto_full.py`. Every lead × format is one row; *score* = average of its rank by margin "
            "(profit ÷ stake over the last 10 draws) and by winning draws (lower is better).", ""]
    md_n = ["# Sports Toto: 5- and 6-number hits, real calendar vs 20 shifted calendars", "",
            "Generated by `analysis/toto_full.py`. A *hit* = one lead on one draw whose best 6-number combination holds 5+ "
            "(or 6) winning numbers, summed over all 26,224 leads. *Rank* = the real calendar's place among 21 (1 = most); "
            "*share ≥ real* = fraction of shifted calendars with at least as many.", ""]
    md_l = ["# Sports Toto: leads with the most 5-number hits against their own shifted calendars", "",
            "Generated by `analysis/toto_full.py`. *5+ hits* = draws whose best 6-number combination holds 5 or 6 winning "
            "numbers, summed over the four formats. Chosen on the earlier draws: *z* = the lead's 5+ hits on the real "
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
                i0 = idx[s0] * 4
                PRE[i0:i0 + len(pre), sh] = pre
                ST[i0:i0 + len(pre), sh] = stat
                HO[i0:i0 + len(pre), sh] = hold
                HC[i0:i0 + len(pre), sh] = hcode
                AG[sh] += agg
                if j % 500 == 0:
                    print(f"{key}: {j}/{len(tasks)} tasks, {time.time() - t0:.0f}s", flush=True)
        setup(key)
        cost = G["cost"]
        np.savez_compressed(os.path.join(A, "profit_arrays", f"toto_full_{key}.npz"), PRE=PRE, ST=ST, HO=HO, HC=HC, AG=AG)
        game = {"label": g["label"], "cost": cost, "formats": {}}
        ev = {}
        for f in FMT:
            T = G["tables"][f]
            s = 6 if f == "10 sets" else len(G["pats"][f][0])
            nb = 1 if key == "toto50" else 0
            k, n = g["k"], g["n"]
            e1 = sum(math.comb(k, m) * math.comb(nb, b) * math.comb(n - k - nb, s - m - b) / math.comb(n, s) * T[m, b]
                     for m in range(min(s, k) + 1) for b in range(nb + 1) if m + b <= s)
            ev[f] = e1 * len(G["pats"][f]) if f != "10 sets" else e1 * 10
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
                            f"{' '.join(tier(x) for x in r['best'])} | {r['rank_earlier']:,} | {100 * r['return_earlier']:.0f}% |")
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
                for li, lvn in enumerate(("5+", "6")):
                    v = AG[:, fi, li, a:b].sum(1)
                    real, null = int(v[0]), v[1:]
                    rk = int((null > real).sum()) + 1
                    share = float((null >= real).mean())
                    game["null"][f"{f} | {sname} | {lvn}"] = {"real": real, "shifted": null.tolist(), "rank": rk, "share": share}
                    md_n.append(f"| {f} | {sname} | {lvn} | {real:,} | {null.mean():,.0f} ({null.min():,}-{null.max():,}) | {rk}/21 | {share:.2f} |")
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
        fwd = int((HC[top, 0] >= 10).sum())
        ctrl5 = [int((HC[choose(c_)[0], c_] >= 10).sum()) for c_ in range(1, nc)]
        hits5 = (ST[:, 0, :, 1].sum(1))
        game["lead_hits"] = {"top": [{"lead": " ".join(lab(i)), "z": float(z[i]), "five_earlier": int(five[i, 0]),
                                      "shifted_mean": float(mu[i]), "six_earlier": int(six[i, 0]),
                                      "five_last10": int((HC[i, 0] >= 10).sum()),
                                      "profit_last10": [float(HO[i, 0, fi].sum()) for fi in range(4)]} for i in top],
                             "forward_real": fwd, "forward_control": ctrl5,
                             "avg_lead_five_last10": float((HC[:, 0] >= 10).sum((1, 2)).mean())}
        LH = game["lead_hits"]
        md_l += [f"## {g['label']}", "",
                 "| # | Lead | Pattern | Earlier 5+ hits (shifted mean) | z | Earlier 6-number hits | Last 10: 5+ hits | Last 10 profit (RM): 10 sets / Sys 7 overlap / Sys 7 disjoint / Sys 8 |",
                 "|---|---|---|---|---|---|---|---|"]
        for i_, r in zip(top, LH["top"]):
            ld, pt = lab(i_)
            md_l.append(f"| {len(md_l)} | {ld} | {pt} | {r['five_earlier']} ({r['shifted_mean']:.1f}) | {r['z']:+.2f} | {r['six_earlier']} | "
                        f"{r['five_last10']} | {' / '.join(fmtm(x) for x in r['profit_last10'])} |")
        md_l += ["", f"Forward check: the 10 leads got {fwd} 5+ hits on the last 10 draws (all formats); an average lead gets "
                 f"{LH['avg_lead_five_last10']:.2f}, 10 leads ≈ {10 * LH['avg_lead_five_last10']:.1f}. The same choice on each shifted "
                 f"calendar: {', '.join(map(str, ctrl5))}.", ""]
        # how unusual is the top lead among all leads
        me = int(five[top[0], 0])
        md_l += [f"Top lead {' '.join(lab(top[0]))}: {me} 5+ hits on the earlier draws. Leads with at least {me}: "
                 f"{int((five[:, 0] >= me).sum())} on the real calendar; shifted calendars "
                 f"{', '.join(str(int((five[:, c_] >= me).sum())) for c_ in range(1, nc))}.", ""]
        game["lead_hits"]["top_lead_rarity"] = {"hits": me, "real": int((five[:, 0] >= me).sum()),
                                                "shifted": [int((five[:, c_] >= me).sum()) for c_ in range(1, nc)]}
        res[key] = game
        with open(os.path.join(A, "toto_full_results.json"), "w") as fh:
            json.dump(res, fh, indent=1, default=float)
        print(g["label"], "done", f"{time.time() - t0:.0f}s", flush=True)
    # Magnum Life comparison
    try:
        mn = json.load(open(os.path.join(A, "high_hits_null_results.json")))
        md_n += ["## Compared with Magnum Life", "",
                 "Magnum Life (high_hits_null.py): real calendar's rank of 21 for 6+ and 7+ hits over the whole history.", "",
                 "| Magnum Life format | 6+ rank | 7+ rank |", "|---|---|---|"]
        for f, v in mn["formats"].items():
            md_n.append(f"| {f} | {v['whole history (after warm-up) | 6+']['rank']}/21 | {v['whole history (after warm-up) | 7+']['rank']}/21 |")
        md_n += ["", "| Toto game | Format | 5+ rank | 6 rank |", "|---|---|---|---|"]
        for key, gm in res.items():
            for f in FMT:
                md_n.append(f"| {gm['label']} | {f} | {gm['null'][f + ' | whole history | 5+']['rank']}/21 | {gm['null'][f + ' | whole history | 6']['rank']}/21 |")
        md_n.append("")
    except FileNotFoundError:
        pass
    for name, md in (("TOTO_SYSTEM_PROFIT.md", md_p), ("TOTO_COMBINED.md", md_c), ("TOTO_HIGH_HITS_NULL.md", md_n),
                     ("TOTO_LEAD_HIGH_HITS.md", md_l)):
        with open(os.path.join(A, name), "w") as fh:
            fh.write("\n".join(md) + "\n")
    print("wrote all in", f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
