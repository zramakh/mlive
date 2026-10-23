#!/usr/bin/env python3
"""Ashtakavarga and Shadbala at the 19:00 Malaysia draw time, as a parameter family "strength"
(data/astro_params_strength.csv; tested with family_fair.py strength).

Ashtakavarga (Parashari benefic places; totals checked: Sun 48, Moon 49, Mars 39, Mercury 54, Jupiter 56, Venus 52,
Saturn 39, Sarva 337):
  bav_<planet>       the planet's own bindus in the sign it occupies (0-8)
  sav_moon / sav_lagna / sav_sun    Sarvashtakavarga bindus of the Moon's, Lagna's, Sun's sign, in bands
  sav_best_sign_house  house (from Lagna) of the sign with the most Sarva bindus
Shadbala, simplified (no Drik bala, Chesta from retrogression only, Kala bala from paksha only):
  sthana (uchcha from deep exaltation + rashi dignity by natural friendship), dig (from the house cusp of the
  planet's direction: Sun / Mars 10th, Moon / Venus 4th, Mercury / Jupiter 1st, Saturn 7th), paksha, chesta
  (retrograde 60, direct 30, Sun / Moon 30), naisargika
  sb_<planet>        its total in quintile bands over all dates
  sb_strongest / sb_weakest         the planet with the highest / lowest total
  sb_benefics_minus_malefics        Jupiter + Venus + Mercury + Moon − Sun − Mars − Saturn, quintile band

python3 analysis/strength.py
"""

import csv
import datetime as dt
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import astro_more as am  # noqa: E402
import common  # noqa: E402
import ephemeris as eph  # noqa: E402
import vedic  # noqa: E402

PL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
REFS = PL + ["Lagna"]
BAV = {  # planet -> reference -> benefic houses counted from the reference
    "Sun": {"Sun": [1, 2, 4, 7, 8, 9, 10, 11], "Moon": [3, 6, 10, 11], "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
            "Mercury": [3, 5, 6, 9, 10, 11, 12], "Jupiter": [5, 6, 9, 11], "Venus": [6, 7, 12],
            "Saturn": [1, 2, 4, 7, 8, 9, 10, 11], "Lagna": [3, 4, 6, 10, 11, 12]},
    "Moon": {"Sun": [3, 6, 7, 8, 10, 11], "Moon": [1, 3, 6, 7, 10, 11], "Mars": [2, 3, 5, 6, 9, 10, 11],
             "Mercury": [1, 3, 4, 5, 7, 8, 10, 11], "Jupiter": [1, 4, 7, 8, 10, 11, 12], "Venus": [3, 4, 5, 7, 9, 10, 11],
             "Saturn": [3, 5, 6, 11], "Lagna": [3, 6, 10, 11]},
    "Mars": {"Sun": [3, 5, 6, 10, 11], "Moon": [3, 6, 11], "Mars": [1, 2, 4, 7, 8, 10, 11], "Mercury": [3, 5, 6, 11],
             "Jupiter": [6, 10, 11, 12], "Venus": [6, 8, 11, 12], "Saturn": [1, 4, 7, 8, 9, 10, 11], "Lagna": [1, 3, 6, 10, 11]},
    "Mercury": {"Sun": [5, 6, 9, 11, 12], "Moon": [2, 4, 6, 8, 10, 11], "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
                "Mercury": [1, 3, 5, 6, 9, 10, 11, 12], "Jupiter": [6, 8, 11, 12], "Venus": [1, 2, 3, 4, 5, 8, 9, 11],
                "Saturn": [1, 2, 4, 7, 8, 9, 10, 11], "Lagna": [1, 2, 4, 6, 8, 10, 11]},
    "Jupiter": {"Sun": [1, 2, 3, 4, 7, 8, 9, 10, 11], "Moon": [2, 5, 7, 9, 11], "Mars": [1, 2, 4, 7, 8, 10, 11],
                "Mercury": [1, 2, 4, 5, 6, 9, 10, 11], "Jupiter": [1, 2, 3, 4, 7, 8, 10, 11], "Venus": [2, 5, 6, 9, 10, 11],
                "Saturn": [3, 5, 6, 12], "Lagna": [1, 2, 4, 5, 6, 7, 9, 10, 11]},
    "Venus": {"Sun": [8, 11, 12], "Moon": [1, 2, 3, 4, 5, 8, 9, 11, 12], "Mars": [3, 5, 6, 9, 11, 12],
              "Mercury": [3, 5, 6, 9, 11], "Jupiter": [5, 8, 9, 10, 11], "Venus": [1, 2, 3, 4, 5, 8, 9, 10, 11],
              "Saturn": [3, 4, 5, 8, 9, 10, 11], "Lagna": [1, 2, 3, 4, 5, 8, 9, 11]},
    "Saturn": {"Sun": [1, 2, 4, 7, 8, 10, 11], "Moon": [3, 6, 11], "Mars": [3, 5, 6, 10, 11, 12], "Mercury": [6, 8, 9, 10, 11, 12],
               "Jupiter": [5, 6, 11, 12], "Venus": [6, 11, 12], "Saturn": [3, 5, 6, 11], "Lagna": [1, 3, 4, 6, 10, 11]},
}
LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
EXALT = {"Sun": 10, "Moon": 33, "Mars": 298, "Mercury": 165, "Jupiter": 95, "Venus": 357, "Saturn": 200}
FRIEND = {"Sun": ({"Moon", "Mars", "Jupiter"}, {"Venus", "Saturn"}), "Moon": ({"Sun", "Mercury"}, set()),
          "Mars": ({"Sun", "Moon", "Jupiter"}, {"Mercury"}), "Mercury": ({"Sun", "Venus"}, {"Moon"}),
          "Jupiter": ({"Sun", "Moon", "Mars"}, {"Mercury", "Venus"}), "Venus": ({"Mercury", "Saturn"}, {"Sun", "Moon"}),
          "Saturn": ({"Mercury", "Venus"}, {"Sun", "Moon", "Mars"})}
DIG = {"Sun": 270, "Mars": 270, "Moon": 90, "Venus": 90, "Mercury": 0, "Jupiter": 0, "Saturn": 180}   # offset from Lagna
NAIS = {"Sun": 60, "Moon": 51.4, "Venus": 42.9, "Jupiter": 34.3, "Mercury": 25.7, "Mars": 17.1, "Saturn": 8.6}
BENEFIC = {"Jupiter", "Venus", "Mercury", "Moon"}


def self_check():
    tot = {p: sum(len(v) for v in BAV[p].values()) for p in PL}
    want = {"Sun": 48, "Moon": 49, "Mars": 39, "Mercury": 54, "Jupiter": 56, "Venus": 52, "Saturn": 39}
    bad = {p: (tot[p], want[p]) for p in PL if tot[p] != want[p]}
    print("ashtakavarga totals:", tot, "sarva", sum(tot.values()), "failures:", bad or "none")


def factors(day):
    jd = eph.julian_day(am.t19(day))
    L = {b: am.lon_sid(b, jd) for b in REFS}
    S = {b: int(L[b] // 30) for b in REFS}
    bav = {p: [0] * 12 for p in PL}
    for p in PL:
        for r, houses in BAV[p].items():
            for h in houses:
                bav[p][(S[r] + h - 1) % 12] += 1
    sav = [sum(bav[p][s] for p in PL) for s in range(12)]
    out = {f"bav_{p.lower()}": bav[p][S[p]] for p in PL}
    for b in ("Moon", "Lagna", "Sun"):
        out[f"sav_{b.lower()}"] = sav[S[b]]
    out["sav_best_sign_house"] = (int(np.argmax(sav)) - S["Lagna"]) % 12 + 1
    elong = abs(am.sdiff(L["Moon"], L["Sun"]))
    sb = {}
    for p in PL:
        uch = 60 * (1 - abs(am.sdiff(L[p], EXALT[p])) / 180)
        lord = LORD[S[p]]
        if S[p] == int(EXALT[p] // 30):
            dig_r = 60
        elif (S[p] + 6) % 12 == int(EXALT[p] // 30):
            dig_r = 0
        elif lord == p:
            dig_r = 45
        elif lord in FRIEND[p][0]:
            dig_r = 30
        elif lord in FRIEND[p][1]:
            dig_r = 7.5
        else:
            dig_r = 15
        dig = 60 * (1 - abs(am.sdiff(L[p], L["Lagna"] + DIG[p])) / 180)
        pak = elong / 3 if p in BENEFIC else 60 - elong / 3
        if p in ("Sun", "Moon"):
            che = 30
        else:
            che = 60 if vedic.is_retrograde(p, jd) else 30
        sb[p] = uch + dig_r + dig + pak + che + NAIS[p]
    out["_sb"] = sb
    return out


def band(x, edges):
    return int(np.searchsorted(edges, x))


def build():
    self_check()
    dates = sorted(common.load_params())
    F = [factors(dt.date.fromisoformat(d)) for d in dates]
    sbm = {p: np.array([f["_sb"][p] for f in F]) for p in PL}
    edges = {p: np.quantile(sbm[p], [0.2, 0.4, 0.6, 0.8]) for p in PL}
    bm = np.array([sum(f["_sb"][p] for p in BENEFIC) - sum(f["_sb"][p] for p in ("Sun", "Mars", "Saturn")) for f in F])
    bme = np.quantile(bm, [0.2, 0.4, 0.6, 0.8])
    savb = lambda x: band(x, [22, 25, 28, 31])  # noqa: E731
    rows = []
    for d, f, x in zip(dates, F, bm):
        r = {"date": d, **{k: v for k, v in f.items() if k.startswith("bav_")}}
        r.update(sav_moon=savb(f["sav_moon"]), sav_lagna=savb(f["sav_lagna"]), sav_sun=savb(f["sav_sun"]),
                 sav_best_sign_house=f["sav_best_sign_house"])
        for p in PL:
            r[f"sb_{p.lower()}"] = band(f["_sb"][p], edges[p])
        r["sb_strongest"] = max(PL, key=lambda p: f["_sb"][p])
        r["sb_weakest"] = min(PL, key=lambda p: f["_sb"][p])
        r["sb_benefics_minus_malefics"] = band(x, bme)
        rows.append(r)
    with open(os.path.join(common.DATA, "astro_params_strength.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print("wrote", len(rows), "dates x", len(rows[0]) - 1, "parameters")


if __name__ == "__main__":
    build()
