#!/usr/bin/env python3
"""Score the watchlist (WATCHLIST.md) on new draws.

For each watched lead and format, the numbers for a draw are built from earlier draws only (the same rules as
the analyses), then scored with the official prizes. Every scored draw is appended to analysis/watch_log.csv
(re-scoring a date replaces its rows) and analysis/WATCH_LOG.md summarises the log so far.

python3 analysis/watch_score.py 2026-10-18 [2026-10-21 ...]
"""

import csv
import math
import os
import sys

import numpy as np

DATES = [a for a in sys.argv[1:] if a[:2] == "20"]
sys.argv = [sys.argv[0], "--games", "ml8,toto50,toto55,toto58"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import extra_astro as xa  # noqa: E402
import lead_search10 as ls  # noqa: E402
import profit_rank as pr  # noqa: E402
import toto_full as tf  # noqa: E402
import toto_profit as tp  # noqa: E402

A = os.path.join(common.ROOT, "analysis")
LOG = os.path.join(A, "watch_log.csv")
MD = os.path.join(A, "WATCH_LOG.md")
FIELDS = ["date", "game", "lead", "pattern", "format", "numbers", "main", "bonus", "best", "payout", "cost", "profit"]

# (lead, pattern, [formats]) per game, from WATCHLIST.md
WATCH = {
    "ml8": [("mercury_nakshatra × saturn_combust", "cold", ["System 10 × 1", "10 tickets"]),
            ("day_pillar × aspect_jupiter_saturn", "pos", ["System 10 × 1"]),
            ("paksha × venus_rashi", "cold", ["10 tickets", "System 10 × 1"]),
            ("ayana × lunar_leap_month", "hot+100", ["System 9 × 2 disjoint"]),
            ("aspect_venus_jupiter × universal_day", "hot", ["System 9 × 2 overlap"]),
            ("saturn_combust × plum_trigrams", "cold", ["System 10 × 1"]),
            ("pof_rashi × aspect_venus_jupiter", "cold", ["System 9 × 2 overlap"]),
            ("kp_sun_sub_lord × year_yinyang", "hot", ["System 10 × 1"]),
            ("ayana × kp_moon_star_lord", "pos", ["System 9 × 2 overlap"]),
            ("mars_rashi × month", "cold", ["System 10 × 1"])],
    "toto50": [("hour_stem_19h × sun_sign_tropical", "pos", ["System 8 × 1"]),
               ("hora_lord × mars_retrograde", "cold", ["10 sets"]),
               ("hora_lord × adhika_masa", "cold", ["10 sets"]),
               ("rahu_nakshatra × kp_asc_sub_lord", "hot", ["System 8 × 1"]),
               ("sun_rashi × planets_with_moon", "cold", ["System 8 × 1"]),
               ("lagna_rashi × day_officer", "cold", ["System 7 × 2 disjoint"]),
               ("saturn_retrograde × nayin", "hot", ["10 sets"]),
               ("karana × masa", "cold", ["System 8 × 1"])],
    "toto55": [("lunar_month × sun_sign_tropical", "hot+100", ["System 8 × 1"]),
               ("sun_sign_tropical × aspect_moon_saturn", "hot+100", ["10 sets", "System 8 × 1"]),
               ("masa × day_god", "hot", ["10 sets"]),
               ("masa × adhika_masa", "hot+100", ["System 8 × 1"]),
               ("month_branch × aspect_venus_jupiter", "hot+100", ["System 8 × 1"]),
               ("lagna_rashi × saturn_retrograde", "hot+100", ["System 7 × 2 overlap"]),
               ("kp_sun_star_lord × month_pillar", "hot+100", ["10 sets"])],
    "toto58": [("moon_rashi × aspects_hard", "cold", ["System 8 × 1"]),
               ("kp_sun_star_lord × day_stem", "hot", ["System 7 × 2 disjoint"]),
               ("nakshatra × nayin", "hot+100", ["10 sets"]),
               ("kp_moon_number × nayin_element", "hot+100", ["System 7 × 2 overlap"]),
               ("nakshatra × sun_sign_tropical", "hot+100", ["10 sets"])],
}
# new-pattern leads from lead_full.py (7 patterns, chosen on draws up to 2026-10-17)
WATCH["ml8"] += [("mercury_rashi × kp_asc_sub_lord", "cold+100", ["System 10 × 1", "System 9 × 2 overlap"]),
                 ("mars_retrograde × moon_phase", "hot/cold100", ["System 9 × 2 disjoint"]),
                 ("mercury_rashi × day_branch", "cold+100", ["System 9 × 2 overlap"]),
                 ("month_stem × kp_ruling_planets", "hot/cold100", ["System 9 × 2 disjoint"]),
                 ("aspect_moon_mars × aspect_mercury_mars", "cold+100", ["System 10 × 1"])]
WATCH["toto50"] += [("hora_lord × mars_combust", "cold/hot100", ["10 sets", "System 7 × 2 overlap"]),
                    ("saturn_retrograde × aspect_mercury_jupiter", "cold/hot100", ["System 7 × 2 disjoint"]),
                    ("aspect_sun_mars × aspect_moon_venus", "hot/cold100", ["System 7 × 2 disjoint"]),
                    ("day_of_month × aspect_venus_jupiter", "hot/cold100", ["System 7 × 2 disjoint"]),
                    ("mars_combust × aspect_moon_mercury", "hot/cold100", ["10 sets"])]
WATCH["toto55"] += [("mercury_nakshatra × aspects_soft", "cold/hot100", ["System 7 × 2 disjoint"]),
                    ("mars_combust × aspect_jupiter_saturn", "cold/hot100", ["10 sets"])]
WATCH["toto58"] += [("saturn_rashi × kp_asc_star_lord", "cold+100", ["System 7 × 2 disjoint"]),
                    ("kp_asc_star_lord × year_pillar", "hot/cold100", ["System 7 × 2 overlap"]),
                    ("lagna_rashi × lunar_day", "hot/cold100", ["System 8 × 1"]),
                    ("sun_nakshatra × lunar_month", "cold/hot100", ["System 7 × 2 overlap"])]
SYS = {"System 10 × 1": [list(range(10))], "System 9 × 2 overlap": [list(range(9)), list(range(6)) + [9, 10, 11]],
       "System 9 × 2 disjoint": [list(range(9)), list(range(9, 18))], **tf.SYS_PATS}


def bonus(key, d, n):
    B = np.zeros((d, n), np.float32)
    rows = list(csv.DictReader(open(os.path.join(common.DATA, common.GAMES[key][0]))))
    for i, r in enumerate(rows):
        for c in ("bonus", "bonus1", "bonus2"):
            if r.get(c):
                B[i, int(r[c]) - 1] = 1
    return B


def ranking(cols, pat):
    """Every draw's numbers ranked by the lead (scores use earlier draws only)."""
    W = ls.W
    k, n, H = W["k"], W["n"], W["H"]
    d = len(H)
    cid = np.zeros(d, np.int64)
    for j in cols:
        cid = cid * 1000 + W["codes"][:, j]
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
    S = {"hot": cnt - e, "cold": e - cnt,
         "pos": ((ex(W["P"]) + ls.SMOOTH * W["pglob"]) / (dp[:, :, None] + ls.SMOOTH)).sum(1),
         "hot+100": zc + W["hot100"], "cold+100": -zc - W["hot100"], "hot/cold100": zc - W["hot100"],
         "cold/hot100": -zc + W["hot100"]}[pat] + W["tie"]
    return np.argsort(-S, 1)


def score_game(key, dates):
    ls.init(key)
    W = ls.W
    g = W["g"]
    k, n, d = W["k"], W["n"], W["d"]
    Bn = bonus(key, d, n)
    names = common.ALL_PARAMS + xa.extra_params()
    out = []
    for lead, pat, fmts in WATCH[key]:
        rk = ranking([names.index(x) for x in lead.split(" × ")], pat)
        for date in dates:
            if date not in g["dates"]:
                continue
            t = g["dates"].index(date)
            win = set(int(x) for x in g["nums"][t])
            bon = set(int(x) + 1 for x in np.flatnonzero(Bn[t]))
            for f in fmts:
                if f in ("10 tickets", "10 sets"):
                    pats = ls.swap_patterns(k)
                    size = k
                else:
                    pats = SYS[f]
                    size = len(pats[0])
                if key == "ml8":
                    T = pr.pay_table(size)
                    price = 1
                else:
                    T = tp.pay_table(key) if size == 6 else tf.sys_table(key, size)
                    price = tp.PRICE[key]
                sets = [sorted(int(rk[t, q]) + 1 for q in p) for p in pats]
                pay = 0.0
                best = (0, 0)
                for s in sets:
                    m, b = len(win & set(s)), len(bon & set(s))
                    pay += T[m, b]
                    best = max(best, (m, b))
                cost = price * sum(math.comb(len(s), k) for s in sets)
                out.append({"date": date, "game": g["label"], "lead": lead, "pattern": pat, "format": f,
                            "numbers": " | ".join(" ".join(f"{x:02d}" for x in s) for s in sets),
                            "main": best[0], "bonus": best[1], "best": f"{best[0]}" + (f"+{best[1]}b" if best[1] else ""),
                            "payout": round(pay, 2), "cost": cost, "profit": round(pay - cost, 2)})
    return out


def main():
    rows = []
    for key in WATCH:
        rows += score_game(key, DATES)
    old = []
    if os.path.exists(LOG):
        old = [r for r in csv.DictReader(open(LOG)) if r["date"] not in DATES]
    allr = old + [{k: str(v) for k, v in r.items()} for r in rows]
    allr.sort(key=lambda r: (r["date"], r["game"], r["lead"], r["format"]))
    with open(LOG, "w", newline="") as fh:
        w = csv.DictWriter(fh, FIELDS)
        w.writeheader()
        w.writerows(allr)
    # summary
    md = ["# Watchlist log", "", "Generated by `analysis/watch_score.py`: the leads of WATCHLIST.md scored on draws after the "
          "list was frozen (numbers built from earlier draws only, official prizes). Random entries return about 55% "
          "(Magnum Life), 35% (Star Toto) and 20% (Power / Supreme Toto) of the stake.", ""]
    for date in sorted({r["date"] for r in allr}):
        md += [f"## {date}", "", "| Game | Lead | Pattern | Format | Best match | Payout (RM) | Stake (RM) | Profit (RM) |",
               "|---|---|---|---|---|---|---|---|"]
        for r in [r for r in allr if r["date"] == date]:
            md.append(f"| {r['game']} | {r['lead']} | {r['pattern']} | {r['format']} | {r['best']} | {float(r['payout']):,.0f} | "
                      f"{r['cost']} | {float(r['profit']):+,.0f} |")
        md.append("")
    md += ["## Running total", "", "| Game | Lead | Format | Draws | Stake (RM) | Payout (RM) | Profit (RM) | Best match |",
           "|---|---|---|---|---|---|---|---|"]
    keyf = lambda r: (r["game"], r["lead"], r["pattern"], r["format"])  # noqa: E731
    for kk in sorted({keyf(r) for r in allr}):
        rr = [r for r in allr if keyf(r) == kk]
        st, po = sum(float(r["cost"]) for r in rr), sum(float(r["payout"]) for r in rr)
        bm = max(rr, key=lambda r: (int(r["main"]), int(r["bonus"])))["best"]
        md.append(f"| {kk[0]} | {kk[1]} ({kk[2]}) | {kk[3]} | {len(rr)} | {st:,.0f} | {po:,.0f} | {po - st:+,.0f} | {bm} |")
    with open(MD, "w") as fh:
        fh.write("\n".join(md) + "\n")
    for r in rows:
        print(r["date"], r["game"][:12], r["lead"][:42], r["pattern"], r["format"], r["best"], r["payout"], r["profit"], "|", r["numbers"][:60])


if __name__ == "__main__":
    main()
