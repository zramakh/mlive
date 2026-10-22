#!/usr/bin/env python3
"""The ranked 4D leads (4DPrediction, analysis/score_leads.py) tried on Magnum Life and Sports Toto.

Each lead's parameters, with its history version ((a) every earlier same-value day = window "all", (b) the previous
same-value day only = window "last1"), in all 7 patterns and every format, replayed over the whole history as in
watch_rank.py (numbers from earlier draws only, official prizes), on the real calendar and 20 shifted calendars,
plus the last 3 draws. S1 (hot digits) corresponds to the hot pattern, S2 (cold digits) to cold.

python3 analysis/leads4d_lotto.py  -> analysis/LEADS4D_LOTTO.md
"""

import json
import os
import sys

import numpy as np

sys.argv = [sys.argv[0]]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import watch_rank as wr  # noqa: E402

ws, ls, common, xa = wr.ws, wr.ls, wr.common, wr.xa
A = wr.A
LEADS = [("1", "karana × day_pillar", "last1", "S1"),
         ("2", "kp_moon_number × year_element", "last1", "2+9"),
         ("3", "tithi × sun_nakshatra", "last1", "2+9"),
         ("4", "kp_asc_number × year_pillar", "last1", "5+6"),
         ("5", "mercury_nakshatra × venus_rashi", "all", "S1"),
         ("6", "jupiter_nakshatra × mercury_combust", "all", "S2"),
         ("7", "mars_nakshatra × mars_rashi × mercury_combust", "all", "S1 / S2"),
         ("8", "mercury_navamsa × venus_rashi", "last1", "S2")]
PATS = ["hot", "cold", "pos", "hot+100", "cold+100", "hot/cold100", "cold/hot100"]
FMTS = {"ml8": ["10 tickets", "System 10 × 1", "System 9 × 2 overlap", "System 9 × 2 disjoint"],
        **{k: ["10 sets", "System 7 × 2 overlap", "System 7 × 2 disjoint", "System 8 × 1"] for k in ("toto50", "toto55", "toto58")}}
LAST3 = ["2026-10-17", "2026-10-18", "2026-10-21"]


def main():
    names = common.ALL_PARAMS + xa.extra_params()
    out = []
    for key in FMTS:
        ls.init(key)
        W = ls.W
        d, R = W["d"], W["d"] - ls.HOLD
        dates = W["g"]["dates"]
        rng = np.random.default_rng(2024)
        shifts = [0] + [int(x) for x in rng.choice(np.arange(160, R - 160), wr.NSH, replace=False)]
        lo = int(0.25 * R)
        hi = 7 if key == "ml8" else 5
        tend = len(dates)
        t3 = [dates.index(x) for x in LAST3 if x in dates]
        for num, lead, win, kind in LEADS:
            cols = [names.index(x) for x in lead.split(" × ")]
            for pat in PATS:
                p = pat if win == "all" else f"{pat}@{win}"
                rks = [wr.ranking(np.roll(W["codes"], s, axis=0), cols, p) for s in shifts]
                for f in FMTS[key]:
                    ret, high, h1, h2 = [], [], [], []
                    mid = (lo + tend) // 2
                    for c, rk in enumerate(rks):
                        pay, best, cost = wr.score(key, rk, f, lo)
                        ret.append(pay[lo:tend].sum() / (cost * (tend - lo)))
                        h1.append(pay[lo:mid].sum() / (cost * (mid - lo)))
                        h2.append(pay[mid:tend].sum() / (cost * (tend - mid)))
                        high.append(int((best[lo:tend] >= hi).sum()))
                        if c == 0:
                            last3 = [(int(best[t]), float(pay[t] - cost)) for t in t3]
                            hits = [f"{dates[t]} ({int(best[t])})" for t in range(lo, tend) if best[t] >= hi]
                            cost0 = cost
                    ret, high = np.array(ret), np.array(high, float)
                    zr = (ret[0] - ret[1:].mean()) / max(ret[1:].std(), 1e-9)
                    zh = (high[0] - high[1:].mean()) / max(high[1:].std(), 0.5)
                    zs = min((h[0] - np.mean(h[1:])) / max(np.std(h[1:]), 1e-9) for h in (h1, h2))
                    out.append(dict(game=wr.LABEL[key], num=num, lead=lead, kind=kind, pat=p, fmt=f, cost=cost0,
                                    ret=float(ret[0]), ret_sh=float(np.median(ret[1:])), zr=float(zr), zs=float(zs),
                                    high=int(high[0]), high_sh=float(high[1:].mean()), zh=float(zh), last3=last3,
                                    hits=hits))
            print(key, num, flush=True)
    json.dump(out, open(os.path.join(A, "leads4d_lotto.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
