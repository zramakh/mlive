#!/usr/bin/env python3
"""The other Parashari divisional charts (vargas), at the 19:00 Malaysia draw time like every other parameter.

D2 hora, D3 drekkana, D4 chaturthamsa, D7 saptamsa, D10 dasamsa, D12 dwadasamsa, D16 shodasamsa, D20 vimsamsa,
D24 chaturvimsamsa, D27 bhamsa, D30 trimsamsa, D40 khavedamsa, D45 akshavedamsa, D60 shashtiamsa (D1 = the rashi
parameters, D9 = d9.py). For each chart D the family is 12 parameters:
    moon / sun / mars / mercury / venus / jupiter / saturn / rahu / lagna _d<D>   the body's sign in that chart
    moon_d<D>_lord, lagna_d<D>_lord                                                ruler of that sign
    vargottama_d<D>_count                                                          bodies in the same sign in D1 and D
Values for every date of data/astro_params.csv go to data/astro_params_vargas.csv. enable() appends all of them to
extra_astro's parameter list and code matrix after the D9 family (d9.enable() first), so earlier indices stay.

python3 analysis/vargas.py   (builds the CSV and checks every chart's sign rules on sample longitudes)
"""

import csv
import datetime as dt
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import d9  # noqa: E402
import ephemeris as eph  # noqa: E402
import extra_astro as xa  # noqa: E402
import kp  # noqa: E402
import vedic  # noqa: E402

CSV = os.path.join(common.DATA, "astro_params_vargas.csv")
DS = [2, 3, 4, 7, 10, 12, 16, 20, 24, 27, 30, 40, 45, 60]
BODIES = ["Moon", "Sun", "Mars", "Mercury", "Venus", "Jupiter", "Saturn", "Rahu", "Lagna"]
SIGN_LORD = d9.SIGN_LORD


def varga(lon, D):
    """Sign index (0 = Mesha) of sidereal longitude `lon` in divisional chart D (Parashari rules)."""
    s, deg = int(lon // 30) % 12, lon % 30
    odd = s % 2 == 0                                                  # Mesha (0) is an odd sign
    mode = s % 3                                                      # 0 movable, 1 fixed, 2 dual
    if D == 2:
        return (4 if deg < 15 else 3) if odd else (3 if deg < 15 else 4)     # Simha (Sun) / Karka (Moon) horas
    if D == 3:
        return (s + 4 * int(deg // 10)) % 12
    if D == 4:
        return (s + 3 * int(deg // 7.5)) % 12
    if D == 7:
        return (s + (0 if odd else 6) + int(deg * 7 // 30)) % 12
    if D == 10:
        return (s + (0 if odd else 8) + int(deg // 3)) % 12
    if D == 12:
        return (s + int(deg // 2.5)) % 12
    if D == 16:
        return ([0, 4, 8][mode] + int(deg * 16 // 30)) % 12
    if D == 20:
        return ([0, 8, 4][mode] + int(deg * 20 // 30)) % 12
    if D == 24:
        return ((4 if odd else 3) + int(deg * 24 // 30)) % 12
    if D == 27:
        return ([0, 3, 6, 9][s % 4] + int(deg * 27 // 30)) % 12       # fire, earth, air, water signs
    if D == 30:
        if odd:
            return 0 if deg < 5 else 10 if deg < 10 else 8 if deg < 18 else 2 if deg < 25 else 6
        return 1 if deg < 5 else 5 if deg < 12 else 11 if deg < 20 else 9 if deg < 25 else 7
    if D == 40:
        return ((0 if odd else 6) + int(deg * 40 // 30)) % 12
    if D == 45:
        return ([0, 4, 8][mode] + int(deg * 45 // 30)) % 12
    if D == 60:
        return (s + int(deg * 2)) % 12
    raise ValueError(D)


def family(D):
    return [f"{b.lower()}_d{D}" for b in BODIES] + [f"moon_d{D}_lord", f"lagna_d{D}_lord", f"vargottama_d{D}_count"]


NEW = [p for D in DS for p in family(D)]


def factors(date):
    day = dt.date.fromisoformat(date)
    jd = eph.julian_day(dt.datetime.combine(day, dt.time(11)))       # 19:00 MYT
    sid = {b: vedic.sidereal(b, jd) for b in BODIES[:-1]}
    sid["Lagna"] = (kp.ascendant_tropical(jd) - vedic.ayanamsa(jd)) % 360
    out = {}
    for D in DS:
        v = {b: varga(sid[b], D) for b in BODIES}
        for b in BODIES:
            out[f"{b.lower()}_d{D}"] = vedic.RASHIS[v[b]]
        out[f"moon_d{D}_lord"] = SIGN_LORD[v["Moon"]]
        out[f"lagna_d{D}_lord"] = SIGN_LORD[v["Lagna"]]
        out[f"vargottama_d{D}_count"] = sum(int(sid[b] // 30) == v[b] for b in BODIES)
    return {k: str(x) for k, x in out.items()}


def build():
    dates = sorted(common.load_params())
    with open(CSV, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date"] + NEW)
        for d in dates:
            f = factors(d)
            w.writerow([d] + [f[p] for p in NEW])
    print(f"wrote {CSV}: {len(dates)} dates x {len(NEW)} parameters")


_T = {}


def table():
    if not _T:
        if not os.path.exists(CSV):
            build()
        with open(CSV) as fh:
            _T.update({r.pop("date"): r for r in csv.DictReader(fh)})
    return _T


_orig = {}


def enable():
    """Append every varga parameter after the D9 family (idempotent)."""
    if _orig:
        return
    d9.enable()
    _orig.update(params=xa.extra_params, codes=xa.codes_all)

    def extra_params():
        return _orig["params"]() + NEW

    def codes_all(dates):
        xa.extra_params = _orig["params"]
        try:
            base = _orig["codes"](dates)
        finally:
            xa.extra_params = extra_params
        T = table()
        cols = []
        for p in NEW:
            vals = sorted({r[p] for r in T.values()})
            ix = {v: i for i, v in enumerate(vals)}
            cols.append([ix[T[d][p]] for d in dates])
        return np.hstack([base, np.array(cols).T])
    xa.extra_params, xa.codes_all = extra_params, codes_all


def self_check():
    """Textbook examples of the sign rules."""
    R = vedic.RASHIS
    ex = [(2, 5, "Simha"), (2, 20, "Karka"), (2, 35, "Karka"), (3, 15, "Simha"), (3, 25, "Dhanu"), (4, 10, "Karka"),
          (7, 32, "Vrischika"), (9, 0.5, "Mesha"), (9, 32, "Makara"), (9, 62, "Tula"), (10, 31, "Makara"),
          (12, 29, "Meena"), (16, 31, "Simha"), (20, 61, "Simha"), (24, 1, "Simha"), (24, 31, "Karka"),
          (27, 1, "Mesha"), (27, 31, "Karka"), (30, 3, "Mesha"), (30, 33, "Vrishabha"), (30, 29, "Tula"),
          (40, 30.5, "Tula"), (40, 31, "Vrischika"), (45, 30.5, "Simha"), (45, 31, "Kanya"), (60, 0.6, "Vrishabha")]
    bad = []
    for D, lon, want in ex:
        got = R[d9.nav(lon)] if D == 9 else R[varga(lon, D)]
        if got != want:
            bad.append((D, lon, want, got))
    print("sign-rule examples failing:", bad or "none")


if __name__ == "__main__":
    self_check()
    build()
    T = table()
    for D in DS:
        print(f"D{D}:", {p: len({r[p] for r in T.values()}) for p in family(D)[:1] + family(D)[-3:]})
