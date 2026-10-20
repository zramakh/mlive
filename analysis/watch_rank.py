#!/usr/bin/env python3
"""Rank every watchlist lead (watch_score.WATCH) from best to worst on one scorecard.

Each lead and format is replayed over the whole history (numbers for a draw from earlier draws only, official prizes,
from a quarter of the way in, as in lead_full.py), on the real calendar and on the same 20 shifted calendars as
lead_full.py (the parameter values rolled against the draws; the pattern and the numbers' own history unchanged, so
the shifted calendars show what the lead would do with no real link between the sky and the draws). Per entry:
  return      payout / stake over the history (random about 55% Magnum Life, 35% Star, 20% Power / Supreme)
  z return    real return against its own 20 shifted calendars
  z high      real high hits (7+ Magnum Life, 5+ Toto) against its own 20 shifted calendars
  steady      the smaller of the return z in the first and in the second half of the history (a lead that beats its
              shifted calendars only in one stretch scores low)
Score = average of the three ranks (z return, z high, steady); 1 = best. The 2026-10-18 draw is shown separately
(a single draw, and some leads were picked because of it).

python3 analysis/watch_rank.py  -> analysis/WATCH_RANK.md
"""

import os
import re
import sys

import numpy as np

sys.argv = [sys.argv[0]]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import watch_score as ws  # noqa: E402

common, ls, pr, tp, tf, xa = ws.common, ws.ls, ws.pr, ws.tp, ws.tf, ws.xa
A = ws.A
NSH = 20
LAST10 = "2026-09-26"
CUT = "2026-10-18"
LABEL = {"ml8": "Magnum Life", "toto50": "Star Toto", "toto55": "Power Toto", "toto58": "Supreme Toto"}
SECTION_FROM = {                      # watchlist section -> (how it was found, data the choice used)
    "Profitable before and during the last 10 draws": ("profit before and during the last 10 draws", CUT),
    "Rare, big hits": ("big hit in the last 10 draws", CUT),
    "Rare earlier, quiet now": ("big hits earlier", LAST10),
    "Frequent small winners": ("most winning draws", LAST10),
    "Steady ball-catcher, no profit": ("most numbers caught", LAST10),
    "New-pattern leads (cold+100, hot/cold100, cold/hot100)": ("7-pattern run / 18 Oct winners", "2026-10-19"),
    "History-window leads (last round, last 5 / 10, decayed)": ("history-window run / 18 Oct winners", "2026-10-19"),
    "D9 (navamsa) family leads": ("D9 family run", CUT),
    "Other divisional-chart leads": ("divisional-chart run", LAST10),
    "Star Toto 6/50": ("Toto watchlist: last 10 draws / earlier record", CUT),
    "Power Toto 6/55": ("Toto watchlist: last 10 draws / earlier record", CUT),
    "Supreme Toto 6/58": ("Toto watchlist: last 10 draws / earlier record", CUT),
}


def watchlist_notes():
    """lead|pattern -> (section, why) from WATCHLIST.md."""
    notes, sec, game = {}, "", ""
    for line in open(os.path.join(A, "WATCHLIST.md")):
        if line.startswith("# "):
            game, sec = line[2:].strip(), line[2:].strip()
        elif line.startswith("## "):
            sec = line[3:].strip()
        elif line.startswith("| ") and not line.startswith("| Lead") and not line.startswith("| Game") and "---" not in line:
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if c[0] in LABEL.values():
                c = c[1:]
            if len(c) >= 3:
                notes.setdefault((c[0], c[1]), (sec, c[2]))
                notes.setdefault(c[0].split(" (")[0], (sec, c[2]))
    return notes


def ranking(codes, cols, pat):
    """watch_score.ranking with a given code matrix."""
    W = ls.W
    old = W["codes"]
    W["codes"] = codes
    try:
        return ws.ranking(cols, pat)
    finally:
        W["codes"] = old


def score(key, rk, fmt, lo):
    W = ls.W
    k, n, H, d = W["k"], W["n"], W["H"], W["d"]
    Bn = ws.bonus(key, d, n)
    if fmt in ("10 tickets", "10 sets"):
        pats = ls.swap_patterns(k)
        size = k
    else:
        pats = ws.SYS[fmt]
        size = len(pats[0])
    if key == "ml8":
        T, price = pr.pay_table(size), 1
    else:
        T, price = (tp.pay_table(key) if size == 6 else tf.sys_table(key, size)), tp.PRICE[key]
    cost = price * sum(ws.math.comb(len(p), k) for p in pats)
    pay = np.zeros(d)
    best = np.zeros(d, int)
    rows = np.arange(d)[:, None]
    for p in pats:
        idx = rk[:, p]
        m = H[rows, idx].sum(1).astype(int)
        b = Bn[rows, idx].sum(1).astype(int)
        pay += T[m, np.minimum(b, T.shape[1] - 1)]
        best = np.maximum(best, m)
    pay[:lo] = 0
    best[:lo] = 0
    return pay, best, cost


def main():
    notes = watchlist_notes()
    names = common.ALL_PARAMS + xa.extra_params()
    out = []
    for key in ws.WATCH:
        ls.init(key)
        W = ls.W
        d, R = W["d"], W["d"] - ls.HOLD
        dates = W["g"]["dates"]
        rng = np.random.default_rng(2024)
        shifts = [0] + [int(x) for x in rng.choice(np.arange(160, R - 160), NSH, replace=False)]
        lo = int(0.25 * R)
        hi = 7 if key == "ml8" else 5
        t10 = dates.index(next(x for x in dates if x >= LAST10))
        tend = dates.index(CUT) + 1
        for lead, pat, fmts in ws.WATCH[key]:
            cols = [names.index(x) for x in lead.split(" × ")]
            rks = [ranking(np.roll(W["codes"], s, axis=0), cols, pat) for s in shifts]
            sec, why = notes.get((lead, pat)) or notes.get(lead, ("", ""))
            how, chosen_to = SECTION_FROM.get(sec, (sec, CUT))
            t_after = dates.index(next(x for x in dates if x >= chosen_to)) if chosen_to <= dates[-1] else d
            for f in fmts:
                ret, high, h1, h2 = [], [], [], []
                mid = (lo + tend) // 2
                for c, rk in enumerate(rks):
                    pay, best, cost = score(key, rk, f, lo)
                    stake = cost * (tend - lo)
                    ret.append(pay[lo:tend].sum() / stake)
                    h1.append(pay[lo:mid].sum() / (cost * (mid - lo)))
                    h2.append(pay[mid:tend].sum() / (cost * (tend - mid)))
                    high.append(int((best[lo:tend] >= hi).sum()))
                    if c == 0:
                        p0, b0 = pay, best
                        after = float(pay[t_after:tend].sum() - cost * (tend - t_after)) if t_after < tend else None
                        wins = int((pay[lo:tend] > 0).sum())
                        last10 = float(pay[t10:tend - 1].sum() - cost * (tend - 1 - t10))
                        oct18 = float(pay[tend - 1] - cost)
                        hits = [f"{dates[t]} ({int(b0[t])})" for t in range(lo, tend) if b0[t] >= hi]
                ret, high = np.array(ret), np.array(high, float)
                zr = (ret[0] - ret[1:].mean()) / max(ret[1:].std(), 1e-9)
                zh = (high[0] - high[1:].mean()) / max(high[1:].std(), 0.5)
                zs = min((h[0] - np.mean(h[1:])) / max(np.std(h[1:]), 1e-9) for h in (h1, h2))
                oct_picked = "2026-10-18" in why or "18 Oct" in why
                out.append(dict(game=LABEL[key], lead=lead, pat=pat, fmt=f, ret=ret[0], ret_sh=float(np.median(ret[1:])),
                                zr=zr, zs=zs, oct_picked=oct_picked, ret1=h1[0], ret2=h2[0], high=int(high[0]), high_sh=float(high[1:].mean()), zh=zh, wins=wins,
                                draws=tend - lo, last10=last10, oct18=oct18, after=after, n_after=tend - t_after,
                                how=how, why=why, hits=hits))
            print(key, lead, pat, f"{zr:+.1f} {zh:+.1f}", flush=True)
    # ranks: higher is better; leads with no draws after selection take the middle rank on that measure
    def rank(vals):
        v = np.array(vals, float)
        r = np.empty(len(v))
        r[np.argsort(-v, kind="stable")] = np.arange(1, len(v) + 1)
        return r
    rz, rh = rank([o["zr"] for o in out]), rank([o["zh"] for o in out])
    ra = rank([o["zs"] for o in out])
    for i, o in enumerate(out):
        o["rz"], o["rh"], o["ra"] = rz[i], rh[i], ra[i]
        o["score"] = (rz[i] + rh[i] + ra[i]) / 3
    out.sort(key=lambda o: o["score"])
    md = ["# Watchlist leads ranked", "",
          "Generated by `analysis/watch_rank.py`. Every watchlist lead and format replayed over the whole history (numbers "
          "from earlier draws only, official prizes, from a quarter of the way in) on the real calendar and on 20 "
          "shifted calendars (the parameter values rolled against the draws: what the same lead does with no real "
          "link between the sky and the draws).", "",
          "- *Return*: payout / stake over the history; in brackets the shifted calendars' median (random entries about "
          "55% Magnum Life, 35% Star, 20% Power / Supreme).",
          "- *z return*, *z high*: the real calendar against the lead's own shifted calendars, for return and for high "
          "hits (7+ Magnum Life, 5+ Toto). Positive = the astrological parameter adds something; around 0 = the lead "
          "does as well with the dates scrambled.",
          "- *Steady*: the smaller of the return z in the first and second halves of the history.",
          "- *18 Oct*: profit on 2026-10-18 (* = the lead was picked because of this draw, so it is not a test).",
          "- *Score* = average of the three ranks among all entries (1 = best).", "",
          "| # | Game | Lead | Pattern | Format | Return (shifted) | z return | High hits (shifted) | z high | Steady | 18 Oct | Score | How found |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, o in enumerate(out, 1):
        aft = f"{o['zs']:+.1f} | {o['oct18']:+,.0f}{'*' if o['oct_picked'] else ''}"
        md.append(f"| {i} | {o['game']} | {o['lead']} | {o['pat']} | {o['fmt']} | {100 * o['ret']:.0f}% ({100 * o['ret_sh']:.0f}%) | "
                  f"{o['zr']:+.1f} | {o['high']} ({o['high_sh']:.1f}) | {o['zh']:+.1f} | {aft} | {o['score']:.0f} | {o['how']} |")
    md += ["", "## High hits of each entry (date, numbers)", ""]
    for i, o in enumerate(out, 1):
        md.append(f"{i}. {o['game']} — {o['lead']} ({o['pat']}, {o['fmt']}): " + (", ".join(o["hits"]) or "none"))
    with open(os.path.join(A, "WATCH_RANK.md"), "w") as fh:
        fh.write("\n".join(md) + "\n")
    import json
    json.dump(out, open(os.path.join(A, "watch_rank.json"), "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
