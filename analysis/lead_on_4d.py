#!/usr/bin/env python3
"""The Supreme Toto lead (Jupiter rashi x Jupiter retrograde, hot) applied to
Sports Toto 4D (data/sportstoto.csv in the 4DPrediction repo, 1992-2026).

At every 4D draw, using only earlier draws on dates with the same Jupiter
rashi and retrograde state, two tickets of 16 numbers are built:
  number  the 16 four-digit numbers that won most often (any of the 23 prizes)
  digit   the 2 most frequent digits in each position -> 2^4 = 16 numbers (the
          4D repo's S1 style)
Hits are winning numbers on the ticket; chance is 16 x winners / 10,000 per draw.

Periods: hold-out = the last 10 draws; test = the last 30% of draws.
For comparison, the same is done for the 4D project's lead (Mercury nakshatra
x Venus rashi) and 200 random Vedic / Chinese pairs (the chance spread).

python3 analysis/lead_on_4d.py  (~3 min) -> analysis/lead_on_4d_results.json
"""

import csv
import itertools
import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

SRC = os.path.join(common.ROOT, "..", "4DPrediction", "data", "sportstoto.csv")
OUT = os.path.join(common.ROOT, "analysis", "lead_on_4d_results.json")
PARAMS = common.VEDIC + common.CHINESE
LEADS = {"Supreme Toto lead": ("jupiter_rashi", "jupiter_retrograde"),
         "4D lead": ("mercury_nakshatra", "venus_rashi")}
K = 16
HOLD = 10
TEST_FRAC = 0.3
N_RANDOM = 200
D = {}


def load():
    draws = {}
    for r in csv.DictReader(open(SRC)):
        draws.setdefault(r["date"], set()).add(int(r["4d_number"]))
    dates = sorted(draws)
    vals = {}
    codes = np.zeros((len(dates), len(PARAMS)), np.int64)
    for i, d in enumerate(dates):
        f = common.all_factors(d)
        for j, p in enumerate(PARAMS):
            codes[i, j] = vals.setdefault((p, f[p]), len(vals))
    return dates, [np.array(sorted(draws[d])) for d in dates], codes


def init():
    if not D:
        dates, wins, codes = load()
        D.update(dates=dates, wins=wins, codes=codes)


def run(pair):
    """Hits / expected of both tickets in the hold-out and the test period, walk-forward."""
    init()
    dates, wins, codes = D["dates"], D["wins"], D["codes"]
    n = len(dates)
    test_from, hold_from = int(n * (1 - TEST_FRAC)), n - HOLD
    cell = codes[:, pair[0]] * 100000 + codes[:, pair[1]]
    num, dig = {}, {}
    rng = np.random.default_rng(int(sum(pair)))
    out = {p: {t: [0, 0.0] for t in ("number", "digit")} for p in ("test", "hold_out")}
    ticket_last = None
    for i in range(n):
        c = cell[i]
        w = wins[i]
        if i >= test_from and c in num:
            cn = num[c] + rng.random(10000) * 1e-3
            t_num = np.argpartition(-cn, K - 1)[:K]
            dd = dig[c] + rng.random((4, 10)) * 1e-3
            top2 = np.argsort(-dd, 1)[:, :2]
            t_dig = np.array([a * 1000 + b * 100 + cc * 10 + e for a, b, cc, e in itertools.product(*top2)])
            e = K * len(w) / 10000
            for per in (["test"] + (["hold_out"] if i >= hold_from else [])):
                out[per]["number"][0] += int(np.isin(w, t_num).sum())
                out[per]["digit"][0] += int(np.isin(w, t_dig).sum())
                for t in ("number", "digit"):
                    out[per][t][1] += e
            if i >= hold_from:
                ticket_last = {"number": sorted(f"{x:04d}" for x in t_num), "digit": sorted(f"{x:04d}" for x in t_dig)}
        num.setdefault(c, np.zeros(10000))[w] += 1
        dg = dig.setdefault(c, np.zeros((4, 10)))
        for pos, div in enumerate((1000, 100, 10, 1)):
            np.add.at(dg[pos], (w // div) % 10, 1)
    for per in out:
        for t, (h, e) in out[per].items():
            out[per][t] = {"hits": h, "expected": round(e, 2), "z": round((h - e) / math.sqrt(e), 2) if e else 0.0}
    return pair, out, ticket_last


def main():
    init()
    ix = {p: i for i, p in enumerate(PARAMS)}
    pairs = list(itertools.combinations(range(len(PARAMS)), 2))
    rng = np.random.default_rng(8)
    rand = [pairs[i] for i in rng.choice(len(pairs), N_RANDOM, replace=False)]
    lead_pairs = {name: tuple(sorted(ix[p] for p in lead)) for name, lead in LEADS.items()}
    todo = list(dict.fromkeys(list(lead_pairs.values()) + rand))
    with Pool(4, initializer=init) as pool:
        res = {pr: (o, t) for pr, o, t in pool.imap_unordered(run, todo)}
    dates = D["dates"]
    n = len(dates)
    out = {"game": "Sports Toto 4D", "draws": n, "test_from": dates[int(n * (1 - TEST_FRAC))],
           "hold_out": dates[-HOLD:], "ticket_size": K, "leads": {}, "random_pairs": {}}
    for name, pr in lead_pairs.items():
        o, t = res[pr]
        out["leads"][name] = {"pair": " x ".join(LEADS[name]), **o, "last_ticket": t}
        for per in ("test", "hold_out"):
            for tk in ("number", "digit"):
                zs = np.array([res[r][0][per][tk]["z"] for r in rand])
                out["leads"][name][per][tk]["share_of_random_pairs_at_least"] = round(float((zs >= o[per][tk]["z"]).mean()), 3)
        print(name, json.dumps({p: o[p] for p in ("test", "hold_out")}))
    for per in ("test", "hold_out"):
        for tk in ("number", "digit"):
            zs = np.array([res[r][0][per][tk]["z"] for r in rand])
            out["random_pairs"][f"{per}_{tk}"] = {"mean_z": round(float(zs.mean()), 3), "sd_z": round(float(zs.std()), 3),
                                                  "max_z": round(float(zs.max()), 2)}
    print("random pairs:", out["random_pairs"])
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
