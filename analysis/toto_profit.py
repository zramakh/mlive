#!/usr/bin/env python3
"""Sports Toto (Star 6/50, Power 6/55, Supreme 6/58): every lead and method as 10 sets of 6 numbers per draw,
scored with the official prize table, on the last 10 draws.

Prize per 6-number set (Sports Toto prize structure; jackpots counted at their minimum, shared jackpots ignored):
    Star 6/50 (RM1, 6 numbers + 1 bonus):  6 = Jackpot 1 RM1,188,888 | 5 + bonus = Jackpot 2 RM100,000 | 5 = RM2,008
                                           4 + bonus = RM788 | 4 = RM28 | 3 + bonus = RM18 | 3 = RM8
    Power 6/55 (RM1):                      6 = Jackpot RM3,000,000 | 5 = RM3,300 | 4 = RM40 | 3 = RM3
    Supreme 6/58 (RM2):                    6 = Jackpot RM8,888,888 | 5 = RM6,888 | 4 = RM80 | 3 = RM8

Leads: 114 parameters and their pairs, plus plain hot / cold over all draws, x hot / cold / position / hot+100;
the 10 sets are the top 6 numbers and one- and two-number swaps (lead_search10.py), built before each draw from
earlier draws only. Methods: the non-parameter generators of ten_tickets.py (hot / cold look-backs, hot+cold,
hot/cold + astrology, analogy, embedding / language models, selected parameters, baselines), choices frozen
before the last 10 draws, 10 sets by ten_tickets.ten_tickets().

python3 analysis/toto_profit.py   -> analysis/toto_profit_results.json, analysis/TOTO_PROFIT.md
"""

import csv
import itertools
import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

if "--games" not in sys.argv:
    sys.argv += ["--games", "toto50,toto55,toto58"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import extra_astro as xa  # noqa: E402
import lead_search10 as ls  # noqa: E402

GAMES = ls.RUN_GAMES
SHIFTS = 2
TOPN = 20
PRIZES = {"toto50": {(6, 0): 1188888, (5, 1): 100000, (5, 0): 2008, (4, 1): 788, (4, 0): 28, (3, 1): 18, (3, 0): 8},
          "toto55": {(6, 0): 3000000, (5, 0): 3300, (4, 0): 40, (3, 0): 3},
          "toto58": {(6, 0): 8888888, (5, 0): 6888, (4, 0): 80, (3, 0): 8}}
PRICE = {"toto50": 1, "toto55": 1, "toto58": 2}
NB = 10
OUT = os.path.join(common.ROOT, "analysis", "toto_profit_results.json")
MD = os.path.join(common.ROOT, "analysis", "TOTO_PROFIT.md")


def pay_table(key):
    """Prize of one 6-number set by (winning, bonus) numbers in it."""
    P = PRIZES[key]
    T = np.zeros((7, 2))
    for m in range(7):
        for b in range(2):
            T[m, b] = P[(m, 0)] if m == 6 else (P.get((m, 1), P.get((m, 0), 0)) if b else P.get((m, 0), 0))
    return T


def bonus_matrix(key, d, n):
    B = np.zeros((d, n), np.float32)
    if key == "toto50":
        rows = list(csv.DictReader(open(os.path.join(common.DATA, common.GAMES[key][0]))))
        for i, r in enumerate(rows):
            B[i, int(r["bonus"]) - 1] = 1
    return B


def init(key):
    ls.init(key)
    ls.W["Bn"] = bonus_matrix(key, ls.W["d"], ls.W["n"])
    ls.W["T"] = pay_table(key)


def series(task):
    """Profit per draw and best set per draw (2 x winning + bonus) for a chunk of sets, all four patterns."""
    key, sh, sets = task
    if ls.W.get("key") != key:
        init(key)
    codes = np.roll(ls.W["codes"], ls.W["shifts"][sh], axis=0)
    k, n, H, T = ls.W["k"], ls.W["n"], ls.W["H"], ls.W["T"]
    cost = NB * PRICE[key]
    out_p, out_c, labels = [], [], []
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
            prof = -float(cost) * np.ones(len(H))
            best = np.zeros(len(H), np.int64)
            for q in ls.W["pats"]:
                m, b = war[:, q].sum(1), warb[:, q].sum(1)
                prof += T[m, b]                      # prizes are per bet (a bet = 1 set at PRICE)
                best = np.maximum(best, 2 * m + (b > 0) * (m < 6))
            out_p.append(prof.astype(np.float32))
            out_c.append(best.astype(np.int8))
            labels.append((s, p))
    return key, sh, labels, np.array(out_p), np.array(out_c)


def expected(key, k, n):
    """Exact expected payout of one set (one bet), and chance a set wins anything, on a fair draw."""
    T, nb = pay_table(key), (1 if key == "toto50" else 0)
    ev = pw = 0.0
    for m in range(7):
        for b in range(nb + 1):
            o = n - k - nb
            if m + b > 6:
                continue
            p = math.comb(k, m) * math.comb(nb, b) * math.comb(o, 6 - m - b) / math.comb(n, 6)
            ev += p * T[m, b]
            pw += p * (T[m, b] > 0)
    return ev, pw


def win_chance(key, k, n, sims=200000):
    """Chance that the 10 sets together win something on a fair draw (sets share numbers)."""
    rng = np.random.default_rng(1)
    T = pay_table(key)
    kt = ls.ktop(k)
    nb = 1 if key == "toto50" else 0
    pos = np.argsort(rng.random((sims, n)), 1)[:, :k + nb]
    w = np.stack([(pos[:, :k] == j).any(1) for j in range(kt)], 1).astype(int)
    b = np.stack([(pos[:, k:] == j).any(1) for j in range(kt)], 1).astype(int)
    pay = sum(T[w[:, q].sum(1), b[:, q].sum(1)] for q in ls.swap_patterns(k))
    return float((pay > 0).mean())


TIER = {12: "6 (Jackpot)", 11: "5 + bonus", 10: "5", 9: "4 + bonus", 8: "4"}


def methods(key):
    """Non-parameter methods on the last 10 draws: profit per draw and best set per draw."""
    import ten_tickets as tt
    g = common.load_game(key)
    k, n = g["k"], g["n"]
    d = len(g["dates"])
    W = g["hit"][-ls.HOLD:, 1:].astype(bool)
    Bw = bonus_matrix(key, d, n)[-ls.HOLD:].astype(bool)
    T = pay_table(key)
    out = {}
    for name, S in tt.generators(key).items():
        prof, best = [], []
        for i in range(ls.HOLD):
            tk = tt.ten_tickets(S[i], k)
            if name == "baseline: random":
                r = np.random.default_rng(100 + i)
                tk = [list(r.choice(n, k, replace=False)) for _ in range(NB)]
            ms = [(int(W[i, t].sum()), int(Bw[i, t].sum())) for t in tk]
            prof.append(sum(T[m, b] for m, b in ms) - NB * PRICE[key])
            best.append(max(2 * m + (b > 0) * (m < 6) for m, b in ms))
        out[name] = (np.array(prof), np.array(best))
    return out


def main():
    names = common.ALL_PARAMS + xa.extra_params()
    lab = lambda s: " × ".join(names[j] for j in s) if s else "all draws (no astrology)"  # noqa: E731
    sets = [()] + [(i,) for i in range(len(names))] + list(itertools.combinations(range(len(names)), 2))
    res, md = {}, ["# Sports Toto: 10 sets of 6 numbers per draw, scored with the official prizes", "",
                   "Generated by `analysis/toto_profit.py`. Every astrological lead (114 parameters and their pairs, plus plain "
                   "hot / cold over all draws, × hot / cold / position / hot+100) and every non-parameter method plays 10 sets "
                   "of 6 numbers per draw, built before the draw from earlier draws only (hot / cold counts updated every draw). "
                   "Prizes per set (jackpots at their minimum): Star 6/50, RM1 a set: 6 = RM1,188,888, 5 + bonus = RM100,000, "
                   "5 = RM2,008, 4 + bonus = RM788, 4 = RM28, 3 + bonus = RM18, 3 = RM8. Power 6/55, RM1: 6 = RM3,000,000, "
                   "5 = RM3,300, 4 = RM40, 3 = RM3. Supreme 6/58, RM2: 6 = RM8,888,888, 5 = RM6,888, 4 = RM80, 3 = RM8. "
                   "*Winning draws* = draws on which the 10 sets won anything. Shifted calendars: the same leads with the "
                   "astrological codes rolled out of line with the draws.", ""]
    for key in GAMES:
        g = common.load_game(key)
        k, n = g["k"], g["n"]
        d = len(g["dates"])
        R = d - ls.HOLD
        lo = int(0.25 * R)
        cost = NB * PRICE[key]
        tasks = [(key, sh, sets[i:i + 200]) for sh in range(SHIFTS + 1) for i in range(0, len(sets), 200)]
        store = {}
        with Pool(4) as pool:
            for _, sh, labels, p, c in pool.imap_unordered(series, tasks):
                st = store.setdefault(sh, {"labels": [], "p": [], "c": []})
                st["labels"] += labels
                st["p"].append(p)
                st["c"].append(c)
        if ls.W.get("key") != key:
            init(key)
        ev, pw1 = expected(key, k, n)
        pwin = win_chance(key, k, n)
        exp10 = ls.HOLD * (NB * ev - cost)
        game = {"label": g["label"], "cost_per_draw": cost, "return_per_rm": round(ev / PRICE[key], 4),
                "win_chance_per_draw": round(pwin, 4), "expected_profit_10": round(exp10, 2)}
        for sh in range(SHIFTS + 1):
            st = store[sh]
            P = np.vstack(st["p"]).astype(np.float64)
            C = np.vstack(st["c"])
            L = st["labels"]
            pre, hold = P[:, lo:R].sum(1), P[:, R:].sum(1)
            wins = (P[:, R:] + cost > 0.5).sum(1)
            rate_pre = (P[:, lo:R] + cost > 0.5).mean(1)
            rank_pre = np.empty(len(P), int)
            rank_pre[np.argsort(-pre, kind="stable")] = np.arange(1, len(P) + 1)
            fo = np.argsort(-pre, kind="stable")[:10]
            fr = np.lexsort((-pre, -rate_pre))[:10]
            row = lambda i: {"lead": lab(L[i][0]), "pattern": L[i][1], "profit": round(float(hold[i]), 1),  # noqa: E731
                             "wins": int(wins[i]), "per_draw": [round(float(x), 1) for x in P[i, R:]],
                             "best": [int(x) for x in C[i, R:]], "rank_earlier": int(rank_pre[i]),
                             "return_earlier": round(float(1 + pre[i] / (cost * (R - lo))), 4),
                             "win_rate_earlier": round(float(rate_pre[i]), 4)}
            hi = np.argwhere(C[:, R:] >= 8)
            out = {"summary": {"leads": len(P), "best_profit": round(float(hold.max()), 1),
                               "in_profit": int((hold > 0).sum()), "mean_profit": round(float(hold.mean()), 2),
                               "most_wins": int(wins.max()),
                               "frozen_top1": round(float(hold[fo[0]]), 1), "frozen_top10_mean": round(float(hold[fo].mean()), 1),
                               "rate_top10_mean": round(float(hold[fr].mean()), 1),
                               "rate_top10_wins": round(float(wins[fr].mean()), 2),
                               "hits": {TIER[c]: int((C[:, R:] == c).sum()) for c in TIER},
                               "hits_earlier": {TIER[c]: int((C[:, lo:R] == c).sum()) for c in TIER}}}
            if sh == 0:
                out["top_profit"] = [row(i) for i in np.argsort(-hold, kind="stable")[:TOPN]]
                out["top_wins"] = [row(i) for i in np.lexsort((-hold, -wins))[:TOPN]]
                out["top_earlier"] = [row(i) for i in fo]
                out["top_rate_earlier"] = [row(i) for i in fr]
                out["high_hits"] = sorted(({"lead": lab(L[i][0]), "pattern": L[i][1], "date": g["dates"][R + t],
                                            "tier": TIER[int(C[i, R + t])], "code": int(C[i, R + t]),
                                            "payout": round(float(P[i, R + t] + cost), 1), "profit": round(float(hold[i]), 1),
                                            "rank_earlier": int(rank_pre[i])} for i, t in hi if C[i, R + t] >= 10),
                                          key=lambda r: (-r["code"], -r["payout"]))
            game["real" if sh == 0 else f"shift{sh}"] = out
        M = methods(key)
        game["methods"] = sorted(({"method": m, "profit": round(float(p.sum()), 1), "wins": int((p + cost > 0.5).sum()),
                                   "per_draw": [round(float(x), 1) for x in p], "best": [int(x) for x in b]}
                                  for m, (p, b) in M.items()), key=lambda r: (-r["profit"], -r["wins"]))
        res[key] = game
        # ---------------- markdown
        S0 = game["real"]["summary"]
        shs = [game[f"shift{i}"]["summary"] for i in range(1, SHIFTS + 1)]
        f = lambda x: f"{x:+,.0f}"  # noqa: E731
        j = lambda key_: ", ".join(f(x[key_]) for x in shs)  # noqa: E731
        md += [f"## {g['label']} (RM{cost} a draw for 10 sets)", "",
               f"Random sets return RM{ev / PRICE[key]:.2f} per RM1 staked, so 10 draws are expected to give {f(exp10)}; 10 random sets win "
               f"something on {100 * pwin:.1f}% of draws.", "",
               "| | Real calendar | Shifted calendars |", "|---|---|---|",
               f"| Leads tested | {S0['leads']:,} | |",
               f"| Best lead on the last 10 draws (hindsight) | {f(S0['best_profit'])} | {j('best_profit')} |",
               f"| Leads in profit on the last 10 | {S0['in_profit']:,} | {', '.join(format(x['in_profit'], ',') for x in shs)} |",
               f"| Average lead, last 10 | {f(S0['mean_profit'])} | {j('mean_profit')} |",
               f"| #1 by earlier profit, played on the last 10 | {f(S0['frozen_top1'])} | {j('frozen_top1')} |",
               f"| Top 10 by earlier profit, average | {f(S0['frozen_top10_mean'])} | {j('frozen_top10_mean')} |",
               f"| Top 10 by earlier win rate, average | {f(S0['rate_top10_mean'])} ({S0['rate_top10_wins']} winning draws) | {j('rate_top10_mean')} |",
               "| Lead × draw hits, last 10: " + ", ".join(TIER[c] for c in sorted(TIER, reverse=True)) + " | "
               + " / ".join(str(S0["hits"][TIER[c]]) for c in sorted(TIER, reverse=True)) + " | "
               + "; ".join(" / ".join(str(x["hits"][TIER[c]]) for c in sorted(TIER, reverse=True)) for x in shs) + " |", ""]
        tier_txt = lambda r: " ".join(("6" if c == 12 else f"{c // 2}{'+b' if c % 2 else ''}") for c in r["best"])  # noqa: E731
        md += [f"### Top {TOPN} leads by profit on the last 10 draws (hindsight)", "",
               "| # | Lead | Pattern | Profit (RM) | Winning draws | Best set per draw | Rank earlier | Earlier return |",
               "|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(game["real"]["top_profit"], 1):
            md.append(f"| {i} | {r['lead']} | {r['pattern']} | {f(r['profit'])} | {r['wins']}/10 | {tier_txt(r)} | "
                      f"{r['rank_earlier']:,} | {100 * r['return_earlier']:.0f}% |")
        md += ["", f"### Top {TOPN} leads by winning draws on the last 10 (hindsight)", "",
               "| # | Lead | Pattern | Winning draws | Profit (RM) | Best set per draw | Earlier win rate |", "|---|---|---|---|---|---|---|"]
        for i, r in enumerate(game["real"]["top_wins"], 1):
            md.append(f"| {i} | {r['lead']} | {r['pattern']} | {r['wins']}/10 | {f(r['profit'])} | {tier_txt(r)} | "
                      f"{100 * r['win_rate_earlier']:.1f}% |")
        md += ["", "### Top 10 by earlier profit, played on the last 10", "",
               "| # | Lead | Pattern | Earlier return | Profit, last 10 (RM) | Winning draws | Best set per draw |", "|---|---|---|---|---|---|---|"]
        for i, r in enumerate(game["real"]["top_earlier"], 1):
            md.append(f"| {i} | {r['lead']} | {r['pattern']} | {100 * r['return_earlier']:.0f}% | {f(r['profit'])} | {r['wins']}/10 | {tier_txt(r)} |")
        hh = game["real"]["high_hits"]
        md += ["", f"### Every 5- and 6-number set on the last 10 draws ({len(hh)})", "",
               "| Lead | Pattern | Draw | Best set | Payout that draw (RM) | Profit, 10 draws (RM) | Rank earlier |", "|---|---|---|---|---|---|---|"]
        for r in hh[:60]:
            md.append(f"| {r['lead']} | {r['pattern']} | {r['date']} | {r['tier']} | {r['payout']:,.0f} | {f(r['profit'])} | {r['rank_earlier']:,} |")
        if len(hh) > 60:
            md.append(f"| … {len(hh) - 60} more in `toto_profit_results.json` | | | | | | |")
        md += ["", "### Non-parameter methods (hot / cold look-backs, mixes, analogy, embedding / language models, baselines)", "",
               "| # | Method | Profit (RM) | Winning draws | Best set per draw |", "|---|---|---|---|---|"]
        for i, r in enumerate(game["methods"], 1):
            md.append(f"| {i} | {r['method']} | {f(r['profit'])} | {r['wins']}/10 | {tier_txt(r)} |")
        md.append("")
        print(g["label"], "cost", cost, "return per RM", round(ev / PRICE[key], 3), "win chance", round(pwin, 3), "real", S0)
        for x in shs:
            print("  shift", x)
        for r in game["methods"][:5]:
            print("  method", r["method"], r["profit"], r["wins"])
        with open(OUT, "w") as fh:
            json.dump(res, fh, indent=1)
        with open(MD, "w") as fh:
            fh.write("\n".join(md) + "\n")
    print("wrote", OUT, "and", MD)


if __name__ == "__main__":
    main()
