#!/usr/bin/env python3
"""D9 (navamsa) family of parameters, at the 19:00 Malaysia draw time like every other parameter.

    sun / mars / mercury / venus / jupiter / saturn / rahu / lagna _navamsa   navamsa sign of each body and of the
                                                                                Ascendant (moon_navamsa already exists)
    moon_navamsa_lord, lagna_navamsa_lord     ruler of the Moon's and the Ascendant's navamsa sign
    moon_vargottama                           Moon in the same sign in D1 and D9
    vargottama_count                          bodies (Sun..Rahu, Moon, Ascendant) in the same sign in D1 and D9

Values for every date of data/astro_params.csv go to data/astro_params_d9.csv. enable() appends the family to
extra_astro.extra_params() / codes_all() (after all existing parameters, so their indices do not change), and
FAMILY lists the family's names (moon_navamsa included).

python3 analysis/d9.py   (builds the CSV, then prints a self-check)
"""

import csv
import datetime as dt
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import almanac  # noqa: E402
import common  # noqa: E402
import ephemeris as eph  # noqa: E402
import extra_astro as xa  # noqa: E402
import kp  # noqa: E402
import vedic  # noqa: E402

CSV = os.path.join(common.DATA, "astro_params_d9.csv")
BODIES = ["Sun", "Mars", "Mercury", "Venus", "Jupiter", "Saturn", "Rahu"]
NEW = [f"{b.lower()}_navamsa" for b in BODIES] + ["lagna_navamsa", "moon_navamsa_lord", "lagna_navamsa_lord",
                                                    "moon_vargottama", "vargottama_count"]
FAMILY = ["moon_navamsa"] + NEW
SIGN_LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]


def nav(lon):
    return int(lon * 9 // 30) % 12


def factors(date):
    day = dt.date.fromisoformat(date)
    t = dt.datetime.combine(day, dt.time(11))                        # 19:00 MYT
    jd = eph.julian_day(t)
    sid = {b: vedic.sidereal(b, jd) for b in ["Moon"] + BODIES}
    sid["Lagna"] = (kp.ascendant_tropical(jd) - vedic.ayanamsa(jd)) % 360
    out = {f"{b.lower()}_navamsa": vedic.RASHIS[nav(sid[b])] for b in BODIES}
    out["lagna_navamsa"] = vedic.RASHIS[nav(sid["Lagna"])]
    out["moon_navamsa_lord"] = SIGN_LORD[nav(sid["Moon"])]
    out["lagna_navamsa_lord"] = SIGN_LORD[nav(sid["Lagna"])]
    varg = {b: int(sid[b] // 30) == nav(sid[b]) for b in sid}
    out["moon_vargottama"] = varg["Moon"]
    out["vargottama_count"] = sum(varg.values())
    return {k: str(v) for k, v in out.items()}


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
    """Append the new D9 parameters to extra_astro's parameter list and code matrix (idempotent)."""
    if _orig:
        return
    _orig.update(params=xa.extra_params, codes=xa.codes_all)

    def extra_params():
        return _orig["params"]() + NEW

    def codes_all(dates):
        xa.extra_params = _orig["params"]                            # the original reads its own list
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


if __name__ == "__main__":
    build()
    T = table()
    P = common.load_params()
    bad = sum(1 for d in P if almanac.vedic.RASHIS.index(P[d]["moon_navamsa"]) != almanac.vedic.RASHIS.index(
        vedic.RASHIS[nav(vedic.sidereal("Moon", eph.julian_day(dt.datetime.combine(dt.date.fromisoformat(d), dt.time(11)))))]))
    print("moon_navamsa recomputed vs stored, mismatches:", bad)
    for p in NEW:
        print(p, sorted({r[p] for r in T.values()})[:12])
