#!/usr/bin/env python3
"""Further astrological factors suggested by practitioner sources, and the number
rules they imply, tested on all four games (19:00 MYT, Kuala Lumpur).

New factors
  Part of Fortune (Arabic lot of fortune): Asc + Moon - Sun by day, Asc + Sun - Moon by
      night (day = 19:00 before sunset); its tropical sign, sidereal rashi and nakshatra
  draw_in_daylight
  Western aspects of the 7 classical planets (conjunction 8 deg, sextile 4, square 6,
      trine 6, opposition 8): 21 pair parameters + counts of soft (trine/sextile) and hard
      (square/opposition) aspects
  KP ruling planets: Moon sign and star lords, lagna sign and star lords, day lord
  daily Nine Star (flying star of the day: from the Jia Zi day nearest the winter solstice
      ascending from 1, from the one nearest the summer solstice descending from 9;
      standard rule, not checked against a printed almanac)
  universal day number (digital root of YYYYMMDD)
  Plum Blossom (Mei Hua) trigrams: upper = (year branch + lunar month + lunar day) mod 8,
      lower = (... + hour branch Xu = 11) mod 8
Number rules (no fitting, the rule names the numbers for each draw)
  pof / asc / moon / jupiter   longitude scaled to 1..n (pof3: that number and its two neighbours)
  pof_degree                   Part of Fortune degree within its sign + 1
  kp_numbers                   KP numbers of Moon, Ascendant, Sun reduced to 1..n
  ruling_planets               numbers whose digital root is a ruling planet's number
  universal_day                numbers with digital root = universal day number
  he_tu                        numbers ending in the day element's He Tu digits
                               (Water 1,6 Fire 2,7 Wood 3,8 Metal 4,9 Earth 5,0)
  nine_star                    numbers with digital root = the daily star
Test 1: every rule on every game over all draws and the last 10, against 200 circular
  shifts of the rule calendar.
Test 2: the new factors as lead parameters (singles, and pairs with all 83 old and the
  new parameters) with conditional.py's recurrence / replication statistics, real vs
  20 shifted calendars.

python3 analysis/extra_astro.py  (~5 min) -> data/astro_params_extra.csv,
    analysis/extra_astro_results.json, analysis/EXTRA_ASTRO.md
"""

import csv
import datetime as dt
import functools
import itertools
import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import almanac  # noqa: E402
import common  # noqa: E402
import conditional as cd  # noqa: E402
import ephemeris as eph  # noqa: E402
import kp  # noqa: E402
import vedic  # noqa: E402

EXTRA_CSV = os.path.join(common.DATA, "astro_params_extra.csv")
OUT = os.path.join(common.ROOT, "analysis", "extra_astro_results.json")
MD = os.path.join(common.ROOT, "analysis", "EXTRA_ASTRO.md")
PLANETS7 = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
ASPECTS = [("conjunction", 0, 8), ("sextile", 60, 4), ("square", 90, 6), ("trine", 120, 6), ("opposition", 180, 8)]
HETU = {"Water": (1, 6), "Fire": (2, 7), "Wood": (3, 8), "Metal": (4, 9), "Earth": (5, 0)}
SIGNS = eph.ZODIAC
RULE_SHIFTS = 200


# ------------------------------------------------------------------ factors
@functools.lru_cache(None)
def solstice(year, lon):
    """Date of the solstice (Sun at tropical longitude lon) in `year`."""
    month = 12 if lon == 270 else 6
    for d in range(15, 28):
        a = eph.sun_longitude(eph.julian_day(dt.datetime(year, month, d, 12)))
        b = eph.sun_longitude(eph.julian_day(dt.datetime(year, month, d + 1, 12)))
        if (a - lon) % 360 > 180 and (b - lon) % 360 < 180:
            return dt.date(year, month, d + 1)
    raise ValueError("solstice not found")


def nearest_jiazi(day):
    j = almanac.jdn(day)
    best = min(range(-30, 31), key=lambda o: (abs(o) if (j + o - 11) % 60 == 0 else 99))
    return day + dt.timedelta(days=best)


def daily_star(day):
    switches = []
    for y in (day.year - 1, day.year):
        switches.append((nearest_jiazi(solstice(y, 270)), "yang"))
        switches.append((nearest_jiazi(solstice(y, 90)), "yin"))
    switches += [(nearest_jiazi(solstice(day.year, 90)), "yin")]
    past = max((s for s in switches if s[0] <= day), key=lambda s: s[0])
    days = (day - past[0]).days
    return 1 + days % 9 if past[1] == "yang" else 9 - days % 9


def digital_root(x):
    return 1 + (x - 1) % 9


def extra_factors(date):
    day = dt.date.fromisoformat(date)
    t = dt.datetime.combine(day, dt.time(11))
    jd = eph.julian_day(t)
    trop = {p: vedic.planet_longitude(p, jd) for p in PLANETS7}
    asc = kp.ascendant_tropical(jd)
    sunset = vedic.sun_rise_set(day)[1]
    daylight = t < sunset
    pof = (asc + trop["Moon"] - trop["Sun"]) % 360 if daylight else (asc + trop["Sun"] - trop["Moon"]) % 360
    ay = vedic.ayanamsa(jd)
    pof_sid = (pof - ay) % 360
    out = {"pof_sign": SIGNS[int(pof // 30)], "pof_rashi": vedic.RASHIS[int(pof_sid // 30)],
           "pof_nakshatra": vedic.NAKSHATRAS[int(pof_sid // (360 / 27))], "draw_in_daylight": daylight}
    soft = hard = 0
    for a, b in itertools.combinations(PLANETS7, 2):
        sep = abs((trop[a] - trop[b] + 180) % 360 - 180)
        name = next((nm for nm, ang, orb in ASPECTS if abs(sep - ang) <= orb), "none")
        out[f"aspect_{a.lower()}_{b.lower()}"] = name
        soft += name in ("trine", "sextile")
        hard += name in ("square", "opposition")
    out["aspects_soft"], out["aspects_hard"] = soft, hard
    c = kp.chart(t)
    ruling = sorted({c["Moon"]["sign_lord"], c["Moon"]["star_lord"], c["Ascendant"]["sign_lord"],
                     c["Ascendant"]["star_lord"], vedic.VARA_LORDS[day.weekday()]})
    out["kp_ruling_planets"] = "+".join(ruling)
    out["nine_star_day"] = daily_star(day)
    out["universal_day"] = digital_root(sum(int(ch) for ch in day.strftime("%Y%m%d")))
    lm, ld, _ = eph.lunar_date(day)
    ch = almanac.chinese(day, eph.sun_longitude(jd))
    yb = almanac.BRANCHES.index(ch["year_pillar"].split()[1]) + 1
    up, lo = (yb + lm + ld) % 8 or 8, (yb + lm + ld + 11) % 8 or 8
    out["plum_trigrams"] = f"{up}-{lo}"
    # continuous values used by the number rules
    out.update(_pof=pof, _asc=asc, _moon=trop["Moon"], _jupiter=trop["Jupiter"],
               _ruling_numbers=" ".join(str(vedic.PLANET_NUMBER[p]) for p in ruling))
    return out


def build_extra():
    dates = sorted(common.load_params())
    rows = [dict(date=d, **extra_factors(d)) for d in dates]
    with open(EXTRA_CSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {EXTRA_CSV}: {len(rows)} dates")


def load_extra():
    if not os.path.exists(EXTRA_CSV):
        build_extra()
    with open(EXTRA_CSV) as fh:
        return {r.pop("date"): r for r in csv.DictReader(fh)}


EXTRA_PARAMS = None


def extra_params():
    global EXTRA_PARAMS
    if EXTRA_PARAMS is None:
        first = next(iter(load_extra().values()))
        EXTRA_PARAMS = [p for p in first if not p.startswith("_")]
    return EXTRA_PARAMS


# ------------------------------------------------------------------ test 1: number rules
def rule_sets(dates, n):
    """{rule: draws x n boolean matrix} (column j = number j+1)."""
    ex, base = load_extra(), common.load_params()
    nums = np.arange(1, n + 1)
    roots = 1 + (nums - 1) % 9
    out = {r: np.zeros((len(dates), n), bool) for r in
           ("pof", "pof3", "pof_degree", "asc", "moon", "jupiter", "kp_numbers", "ruling_planets",
            "universal_day", "he_tu", "nine_star")}
    scale = lambda deg: int(float(deg) / 360 * n)  # noqa: E731 (0-based index)
    for i, d in enumerate(dates):
        e, b = ex[d], base[d]
        p = scale(e["_pof"])
        out["pof"][i, p] = True
        out["pof3"][i, [(p - 1) % n, p, (p + 1) % n]] = True
        deg = int(float(e["_pof"]) % 30)
        if deg < n:
            out["pof_degree"][i, deg] = True
        for r, key in (("asc", "_asc"), ("moon", "_moon"), ("jupiter", "_jupiter")):
            out[r][i, scale(e[key])] = True
        for key in ("kp_moon_number", "kp_asc_number", "kp_sun_number"):
            out["kp_numbers"][i, (int(b[key]) - 1) % n] = True
        out["ruling_planets"][i] = np.isin(roots, [int(x) for x in e["_ruling_numbers"].split()])
        out["universal_day"][i] = roots == int(e["universal_day"])
        out["he_tu"][i] = np.isin(nums % 10, HETU[b["day_element"]])
        out["nine_star"][i] = roots == int(e["nine_star_day"])
    return out


def rule_z(S, W, k, n):
    m = S.sum(1)
    hits = (S & W).sum()
    exp = (m * k / n).sum()
    var = (m * (k / n) * (1 - k / n) * (n - m) / (n - 1)).sum()
    return float(hits), float(exp), float((hits - exp) / math.sqrt(var)) if var > 0 else 0.0


def test_rules():
    rng = np.random.default_rng(17)
    res, all_real, all_sh = {}, [], np.zeros((RULE_SHIFTS, 0))
    for key in common.GAMES:
        g = common.load_game(key)
        k, n = g["k"], g["n"]
        W = g["hit"][:, 1:].astype(bool)
        R = rule_sets(g["dates"], n)
        d = len(W)
        shifts = rng.integers(160, d - 160, RULE_SHIFTS)
        game = {}
        sh_z = []
        for r, S in R.items():
            hits, exp, z = rule_z(S, W, k, n)
            lh, le, lz = rule_z(S[-10:], W[-10:], k, n)
            zs = np.array([rule_z(np.roll(S, int(s), 0), W, k, n)[2] for s in shifts])
            lzs = np.array([rule_z(np.roll(S, int(s), 0)[-10:], W[-10:], k, n)[0] for s in shifts])
            game[r] = {"hits": int(hits), "expected": round(exp, 1), "ratio": round(hits / exp, 4), "z": round(z, 2),
                       "share_shifts_z_ge": round(float((zs >= z).mean()), 3),
                       "last10_hits": int(lh), "last10_expected": round(le, 2),
                       "last10_share_shifts_ge": round(float((lzs >= lh).mean()), 3)}
            all_real.append(z)
            sh_z.append(zs)
        all_sh = np.hstack([all_sh, np.array(sh_z).T])
        res[key] = game
        print(common.GAMES[key][1], {r: (v["ratio"], v["z"], v["last10_hits"], v["last10_expected"]) for r, v in game.items()})
    real = np.array(all_real)
    res["summary"] = {"tests": len(real), "max_z": round(float(real.max()), 2), "min_z": round(float(real.min()), 2),
                      "n_abs_z_gt_1.96": int((np.abs(real) > 1.96).sum()),
                      "shifted_mean_n_abs_z_gt_1.96": round(float((np.abs(all_sh) > 1.96).sum(1).mean()), 1),
                      "share_shifts_max_z_ge": round(float((all_sh.max(1) >= real.max()).mean()), 3),
                      "mean_z": round(float(real.mean()), 3),
                      "share_shifts_mean_z_ge": round(float((all_sh.mean(1) >= real.mean()).mean()), 3)}
    print(res["summary"])
    return res


# ------------------------------------------------------------------ test 2: new factors as leads
def codes_all(dates):
    base, _ = common.codes_for(dates)
    ex = load_extra()
    cols = []
    for p in extra_params():
        vals = sorted({r[p] for r in ex.values()})
        ix = {v: i for i, v in enumerate(vals)}
        cols.append([ix[ex[d][p]] for d in dates])
    return np.hstack([base, np.array(cols).T])


def scan(task):
    key, shift_ix, sets = task
    if cd.G.get("key") != key:
        cd.setup(key)
        cd.G["codes"] = codes_all(cd.G["g"]["dates"])
        cd.G["key"] = key
    codes = np.roll(cd.G["codes"], cd.G["shifts"][shift_ix], axis=0)
    out = []
    for s in sets:
        cell = codes[:, s[0]].astype(np.int64)
        for j in s[1:]:
            cell = cell * 1000 + codes[:, j]
        out.append(cd.evaluate(cell))
    return key, shift_ix, sets, out


def test_leads():
    names = common.ALL_PARAMS + extra_params()
    new = list(range(len(common.ALL_PARAMS), len(names)))
    singles = [(i,) for i in new]
    pairs = sorted({tuple(sorted((i, j))) for i in new for j in range(len(names)) if j != i})
    chunk = 150
    tasks = [(key, sh, singles) for key in common.GAMES for sh in range(cd.SHIFTS + 1)]
    tasks += [(key, sh, pairs[i:i + chunk]) for key in common.GAMES for sh in range(cd.SHIFTS + 1)
              for i in range(0, len(pairs), chunk)]
    R = {}
    with Pool(4) as pool:
        for key, sh, sets, out in pool.imap_unordered(scan, tasks, chunksize=2):
            R.setdefault(key, {}).setdefault(sh, {}).update(zip(sets, out))
    label = lambda s: " x ".join(names[j] for j in s)  # noqa: E731
    res = {}
    for key, by in R.items():
        game = {}
        for kind, sets in (("singles", singles), ("pairs", pairs)):
            summ = cd.summarise([by[0][s] for s in sets], len(sets))
            shifted = [cd.summarise([by[sh][s] for s in sets], len(sets)) for sh in range(1, cd.SHIFTS + 1)]
            summ["shifted_mean"] = {f: round(float(np.mean([x[f] for x in shifted])), 3) for f in shifted[0] if f != "tests"}
            summ["real_beats_shifts"] = {f: sum(summ[f] > x[f] for x in shifted) for f in shifted[0] if f != "tests"}
            order = sorted(sets, key=lambda s: -by[0][s]["pre_rec_z"])
            summ["walk_forward_leads"] = [{"params": label(s), "pre_rec_z": by[0][s]["pre_rec_z"],
                                           "test_rep_hits": by[0][s]["rep_hits"], "test_rep_expected": by[0][s]["rep_expected"],
                                           "test_rep_z": by[0][s]["rep_z"]} for s in order[:5]]
            order = sorted(sets, key=lambda s: -by[0][s]["rep_z"])
            summ["top_replication"] = [{"params": label(s), "rep_z": by[0][s]["rep_z"], "pre_rec_z": by[0][s]["pre_rec_z"]}
                                       for s in order[:5]]
            game[kind] = summ
        res[key] = game
        print(common.GAMES[key][1], {k2: (v["max_rec_z"], v["rep_lift"], v["max_rep_z"], v["shifted_mean"]["max_rep_z"],
                                          v["walk_forward_leads"][0]["params"], v["walk_forward_leads"][0]["test_rep_z"])
                                     for k2, v in game.items()})
    return res


def main():
    load_extra()
    rules = test_rules()
    leads = test_leads()
    with open(OUT, "w") as fh:
        json.dump({"rules": rules, "leads": leads}, fh, indent=1, default=float)
    md = ["# Further astrological factors and number rules", "",
          "Generated by `analysis/extra_astro.py`. Factors: Part of Fortune, Western aspects, KP ruling planets, daily Nine "
          "Star, universal day number, Plum Blossom trigrams (see the script). *Shifts* = share of 200 circularly shifted "
          "rule calendars scoring at least as high.", "",
          "## Number rules (no fitting)", "",
          "| Rule | " + " | ".join(common.GAMES[k][1] + " ratio (z; shifts)" for k in common.GAMES) + " | Last 10 (hits / expected) |",
          "|---|" + "---|" * (len(common.GAMES) + 1)]
    for r in rules["toto50"]:
        md.append(f"| {r} | " + " | ".join(f"{rules[k][r]['ratio']:.3f} ({rules[k][r]['z']:+.2f}; {rules[k][r]['share_shifts_z_ge']:.2f})"
                                          for k in common.GAMES) + " | " +
                  ", ".join(f"{rules[k][r]['last10_hits']}/{rules[k][r]['last10_expected']}" for k in common.GAMES) + " |")
    s = rules["summary"]
    md += ["", f"{s['tests']} tests: z from {s['min_z']:+.2f} to {s['max_z']:+.2f}; {s['n_abs_z_gt_1.96']} with |z| > 1.96 "
           f"(shifted calendars: {s['shifted_mean_n_abs_z_gt_1.96']} on average); mean z {s['mean_z']:+.3f} "
           f"({100 * s['share_shifts_mean_z_ge']:.0f}% of shifts higher); best z beaten by {100 * s['share_shifts_max_z_ge']:.0f}% of shifts.",
           "", "## New factors as lead parameters", "",
           "| Game | Set | Best recurrence z (shifted) | Replication lift (shifted) | Best replication z (shifted) | Walk-forward lead → test z |",
           "|---|---|---|---|---|---|"]
    for key, game in leads.items():
        for kind, v in game.items():
            w = v["walk_forward_leads"][0]
            md.append(f"| {common.GAMES[key][1]} | {kind} | {v['max_rec_z']:+.2f} ({v['shifted_mean']['max_rec_z']:+.2f}) | "
                      f"{v['rep_lift']:.4f} ({v['shifted_mean']['rep_lift']:.4f}) | {v['max_rep_z']:+.2f} "
                      f"({v['shifted_mean']['max_rep_z']:+.2f}) | {w['params']} → {w['test_rep_z']:+.2f} |")
    with open(MD, "w") as fh:
        fh.write("\n".join(md) + "\n")
    print("wrote", OUT, "and", MD)


if __name__ == "__main__":
    main()
