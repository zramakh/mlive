#!/usr/bin/env python3
"""Vedic numerology: does the ruling planet's number show up in the winning numbers?

Planet numbers (Ank Jyotish): Sun 1, Moon 2, Jupiter 3, Rahu 4, Mercury 5,
Venus 6, Ketu 7, Saturn 8, Mars 9. For each ruling planet of the draw (weekday
lord, hora lord, nakshatra lord, KP star and sub lords of the Moon, Ascendant
and Sun) we count winning numbers whose digital root equals the planet's
number, and winning numbers that contain it as a digit. Chance is the share
of 1..n with that property, with the hypergeometric variance of a draw.
The tests overlap (e.g. the nakshatra lord is the Moon's KP star lord), so
the count of |z| > 1.96 is compared with the same scan on 200 circularly
shifted parameter calendars.

python3 analysis/numerology.py  -> analysis/numerology_results.json
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import vedic  # noqa: E402

LORDS = ["weekday", "hora_lord", "nakshatra_lord", "kp_moon_star_lord", "kp_moon_sub_lord",
         "kp_asc_star_lord", "kp_asc_sub_lord", "kp_sun_star_lord", "kp_sun_sub_lord"]
WEEKDAY_LORD = {"Mon": "Moon", "Tue": "Mars", "Wed": "Mercury", "Thu": "Jupiter", "Fri": "Venus",
                "Sat": "Saturn", "Sun": "Sun"}
SHIFTS = 200
OUT = os.path.join(common.ROOT, "analysis", "numerology_results.json")


def root(x):
    return 1 + (x - 1) % 9


def tables(g):
    """Per property: share of 1..n with it, and per-draw count of winners with it (index = planet number)."""
    allnums = np.arange(1, g["n"] + 1)
    return {prop: (np.array([test(allnums, p).sum() / g["n"] for p in range(10)]),
                   np.array([[test(nums, p).sum() for p in range(10)] for nums in g["nums"]]))
            for prop, test in PROPS}


def zscores(g, tab, pnum):
    """z for every lord x property; pnum[d, l] = planet number of lord l on draw d."""
    k, n = g["k"], g["n"]
    out = {}
    for prop, (share, hit) in tab.items():
        obs = np.take_along_axis(hit, pnum, 1).sum(0)
        m = share[pnum]
        exp = (k * m).sum(0)
        var = (k * m * (1 - m) * (n - k) / (n - 1)).sum(0)
        out[prop] = (obs, exp, (obs - exp) / np.sqrt(var))
    return out


PROPS = (("digital_root", lambda x, p: root(x) == p),
         ("contains_digit", lambda x, p: np.char.find(x.astype(str), str(p)) >= 0))


def replication(table):
    """Each |z| > 1.96 result on the train+valid draws (common.splits), re-scored on the test draws."""
    out = []
    for key in common.GAMES:
        g = common.load_game(key)
        ts = common.splits(len(g["dates"]))[1]
        pnum = np.array([[vedic.PLANET_NUMBER[WEEKDAY_LORD.get(table[d][l], table[d][l])] for l in LORDS]
                         for d in g["dates"]])
        parts = []
        for sl in (slice(0, ts), slice(ts, None)):
            gg = dict(g, nums=g["nums"][sl])
            parts.append(zscores(gg, tables(gg), pnum[sl]))
        for prop, _ in PROPS:
            for i, l in enumerate(LORDS):
                z0, z1 = parts[0][prop][2][i], parts[1][prop][2][i]
                if abs(z0) > 1.96:
                    out.append({"game": key, "lord": l, "property": prop, "z_before_test": round(float(z0), 2),
                                "z_test": round(float(z1), 2), "same_sign": bool(z0 * z1 > 0)})
    return out


def main():
    table = common.load_params()
    res = {}
    rng = np.random.default_rng(3)
    real_z, shifted_z = [], [[] for _ in range(SHIFTS)]
    for key in common.GAMES:
        g = common.load_game(key)
        pnum = np.array([[vedic.PLANET_NUMBER[WEEKDAY_LORD.get(table[d][l], table[d][l])] for l in LORDS]
                         for d in g["dates"]])
        tab = tables(g)
        z = zscores(g, tab, pnum)
        res[key] = {l: {prop: {"observed": int(z[prop][0][i]), "expected": round(float(z[prop][1][i]), 1),
                               "ratio": round(float(z[prop][0][i] / z[prop][1][i]), 4),
                               "z": round(float(z[prop][2][i]), 2)} for prop, _ in PROPS}
                    for i, l in enumerate(LORDS)}
        real_z += [x for prop, _ in PROPS for x in z[prop][2]]
        d = len(g["dates"])
        for s in range(SHIFTS):
            zs = zscores(g, tab, np.roll(pnum, int(rng.integers(160, d - 160)), axis=0))
            shifted_z[s] += [x for prop, _ in PROPS for x in zs[prop][2]]
        print(g["label"], {l: (v["digital_root"]["z"], v["contains_digit"]["z"]) for l, v in res[key].items()})
    signed, sh_signed = np.array(real_z), np.array(shifted_z)
    real_z = np.abs(signed)
    sh = np.abs(sh_signed)
    res["summary"] = {"tests": len(real_z), "max_abs_z": round(float(real_z.max()), 2),
                      "n_abs_z_gt_1.96": int((real_z > 1.96).sum()),
                      "expected_if_independent": round(0.05 * len(real_z), 1),
                      "shifted_calendars": SHIFTS,
                      "shifted_mean_n_abs_z_gt_1.96": round(float((sh > 1.96).sum(1).mean()), 1),
                      "shifted_max_abs_z_mean": round(float(sh.max(1).mean()), 2),
                      "share_of_shifts_with_at_least_as_many": round(float(((sh > 1.96).sum(1) >= (real_z > 1.96).sum()).mean()), 3),
                      "share_of_shifts_with_larger_max": round(float((sh.max(1) >= real_z.max()).mean()), 3),
                      # a real "planet number boosts" effect would be positive
                      "n_z_gt_1.96": int((signed > 1.96).sum()),
                      "shifted_mean_n_z_gt_1.96": round(float((sh_signed > 1.96).sum(1).mean()), 1),
                      "mean_z": round(float(signed.mean()), 3),
                      "share_of_shifts_with_higher_mean_z": round(float((sh_signed.mean(1) >= signed.mean()).mean()), 3),
                      "replication": replication(table)}
    print(res["summary"])
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
