#!/usr/bin/env python3
"""New parameter families for the 19:00 Malaysia draw time (values for every date of data/astro_params.csv).

muhurta  (data/astro_params_muhurta.csv)
    day_part_19h        which eighth of the day (D1-D8, sunrise-sunset) or night (N1-N8) 19:00 falls in
    rahu_kalam / yamaganda / gulika      19:00 inside that daytime period (weekday rules)
    choghadiya, choghadiya_quality       the day / night choghadiya at 19:00 (good: Amrit, Shubh, Labh)
    moon_void_of_course the Moon makes no Ptolemaic aspect to Sun-Saturn before leaving its tropical sign
    moon_out_of_bounds  |Moon declination| > 23.44°
    eclipse_season      Sun within 16° of a lunar node
    eclipse_days        days to the nearest eclipse (0-7, 8-14, 15-30, 31-90, 91+)
    station_<planet>    days to the nearest station of Mercury / Venus / Mars / Jupiter / Saturn (0-3, 4-7, 8-14, 15+)
    panchaka            Moon in the second half of Dhanishta to Revati
continuous  (data/astro_params_continuous.csv)
    lonb_<body>         sidereal longitude of Sun, Moon, Mars, Mercury, Venus, Jupiter, Saturn, Rahu, Lagna in 10° bins
    sep_<a>_<b>         angle between two of them, folded to 0-180°, in 15° bins
transit, per game  (data/astro_params_transit_<game>.csv): the chart of the game's first draw (19:00) as a birth chart
    tr_<body>_house     whole-sign house of today's Sun, Moon, Mars, Mercury, Venus, Jupiter, Saturn, Rahu from its Lagna
    tr_conj / tr_hard / tr_soft   today's Sun-Saturn in conjunction / square-opposition / sextile-trine (orb 3°) with
                        its Sun, Moon, Mars, Mercury, Venus, Jupiter, Saturn, Lagna (counts, 4 = 4 or more)
    tr_solar_return     today's Sun within 15° of its Sun;  tr_lunar_return: today's Moon within 12° of its Moon

python3 analysis/astro_more.py
"""

import csv
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import ephemeris as eph  # noqa: E402
import kp  # noqa: E402
import vedic  # noqa: E402

D = common.DATA
BODIES = ["Sun", "Moon", "Mars", "Mercury", "Venus", "Jupiter", "Saturn", "Rahu", "Lagna"]
PLANETS = ["Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
RAHU = {0: 1, 1: 6, 2: 4, 3: 5, 4: 3, 5: 2, 6: 7}            # weekday (Mon 0) -> daytime eighth index (0-7)
YAMA = {6: 4, 0: 3, 1: 2, 2: 1, 3: 0, 4: 6, 5: 5}
GULI = {6: 6, 0: 5, 1: 4, 2: 3, 3: 2, 4: 1, 5: 0}
DAY_CH = ["Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog"]
DAY_FIRST = {6: "Udveg", 0: "Amrit", 1: "Rog", 2: "Labh", 3: "Shubh", 4: "Char", 5: "Kaal"}
NIGHT_CH = ["Shubh", "Amrit", "Char", "Rog", "Kaal", "Labh", "Udveg"]
NIGHT_FIRST = {6: "Shubh", 0: "Char", 1: "Kaal", 2: "Udveg", 3: "Amrit", 4: "Rog", 5: "Labh"}
GOOD = {"Amrit", "Shubh", "Labh"}


def t19(day):
    return dt.datetime.combine(day, dt.time(11))                # 19:00 MYT in UTC


def lon_trop(body, jd):
    if body == "Moon":
        return eph.moon_longitude(jd)
    if body == "Sun":
        return eph.sun_longitude(jd)
    if body == "Lagna":
        return kp.ascendant_tropical(jd)
    if body == "Rahu":
        return (vedic.sidereal("Rahu", jd) + vedic.ayanamsa(jd)) % 360
    return vedic.planet_longitude(body, jd)


def lon_sid(body, jd):
    if body == "Lagna":
        return (kp.ascendant_tropical(jd) - vedic.ayanamsa(jd)) % 360
    return vedic.sidereal(body, jd)


def sdiff(a, b):
    return (a - b + 180) % 360 - 180


def void_of_course(jd):
    m0 = eph.moon_longitude(jd)
    sign = int(m0 // 30)
    prev = None
    for h in range(0, 72):
        j = jd + h / 24
        m = eph.moon_longitude(j)
        if int(m // 30) != sign:
            return True
        f = {(p, a): sdiff(m - lon_trop(p, j), a) for p in PLANETS for a in (0, 60, -60, 90, -90, 120, -120, 180)}
        if prev:
            for key, v in f.items():
                u = prev[key]
                if u < 0 <= v and v - u < 30:
                    return False
        prev = f
    return True


def moon_declination(t):
    import ephem
    m = ephem.Moon(ephem.Date(t))
    return float(m.dec) * 57.29578


def band(x, cuts, labels):
    for c, lab in zip(cuts, labels):
        if x <= c:
            return lab
    return labels[-1]


def build():
    dates = sorted(common.load_params())
    days = [dt.date.fromisoformat(d) for d in dates]
    first, last = days[0] - dt.timedelta(days=200), days[-1] + dt.timedelta(days=200)
    # stations and eclipses over the whole span
    span = [first + dt.timedelta(days=i) for i in range((last - first).days + 1)]
    stations = {p: [] for p in ("Mercury", "Venus", "Mars", "Jupiter", "Saturn")}
    prev = None
    for day in span:
        jd = eph.julian_day(t19(day))
        r = {p: vedic.is_retrograde(p, jd) for p in stations}
        if prev:
            for p in stations:
                if r[p] != prev[p]:
                    stations[p].append(day)
        prev = r
    eclipses = []
    pe = None
    for day in span:
        jd = eph.julian_day(t19(day))
        e = eph.elongation(jd)
        if pe is not None:
            for target in (0, 180):
                if sdiff(pe, target) < 0 <= sdiff(e, target) and abs(sdiff(e, target)) < 30:
                    node = lon_trop("Rahu", jd)
                    dist = abs(sdiff(eph.sun_longitude(jd), node))
                    dist = min(dist, 180 - dist)
                    if dist < (16 if target == 0 else 12):
                        eclipses.append(day)
        pe = e
    print("stations", {p: len(v) for p, v in stations.items()}, "eclipses", len(eclipses), flush=True)

    mu, co = [], []
    for i, (d, day) in enumerate(zip(dates, days)):
        t = t19(day)
        jd = eph.julian_day(t)
        wd = day.weekday()
        rise, sset = vedic.sun_rise_set(day)
        nrise, _ = vedic.sun_rise_set(day + dt.timedelta(days=1))
        if t < sset:
            part = int((t - rise) / ((sset - rise) / 8))
            dpart = f"D{part + 1}"
            ch = DAY_CH[(DAY_CH.index(DAY_FIRST[wd]) + part) % 7]
        else:
            part = int((t - sset) / ((nrise - sset) / 8))
            dpart = f"N{part + 1}"
            ch = NIGHT_CH[(NIGHT_CH.index(NIGHT_FIRST[wd]) + part) % 7]
            part = -1
        node = lon_trop("Rahu", jd)
        sdist = abs(sdiff(eph.sun_longitude(jd), node))
        sdist = min(sdist, 180 - sdist)
        ed = min(abs((day - e).days) for e in eclipses)
        msid = lon_sid("Moon", jd)
        r = {"date": d, "day_part_19h": dpart, "rahu_kalam": part == RAHU[wd], "yamaganda": part == YAMA[wd],
             "gulika": part == GULI[wd], "choghadiya": ch, "choghadiya_quality": "good" if ch in GOOD else ("neutral" if ch == "Char" else "bad"),
             "moon_void_of_course": void_of_course(jd), "moon_out_of_bounds": abs(moon_declination(t)) > 23.44,
             "eclipse_season": sdist < 16, "eclipse_days": band(ed, (7, 14, 30, 90), ("0-7", "8-14", "15-30", "31-90", "91+")),
             "panchaka": msid >= 300}                                    # second half of Dhanishta to the end of Revati
        for p, st in stations.items():
            dd = min(abs((day - s).days) for s in st)
            r[f"station_{p.lower()}"] = band(dd, (3, 7, 14), ("0-3", "4-7", "8-14", "15+"))
        mu.append(r)
        L = {b: lon_sid(b, jd) for b in BODIES}
        c = {"date": d, **{f"lonb_{b.lower()}": int(L[b] // 10) for b in BODIES}}
        for a in range(len(BODIES)):
            for b in range(a + 1, len(BODIES)):
                s = abs(sdiff(L[BODIES[a]], L[BODIES[b]]))
                c[f"sep_{BODIES[a].lower()}_{BODIES[b].lower()}"] = int(min(s, 179.999) // 15)
        co.append(c)
        if i % 500 == 0:
            print(d, flush=True)
    for name, rows in (("muhurta", mu), ("continuous", co)):
        with open(os.path.join(D, f"astro_params_{name}.csv"), "w", newline="") as fh:
            w = csv.DictWriter(fh, list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    # transits, per game
    for key, (fname, *_rest) in common.GAMES.items():
        if key not in ("ml8", "toto50", "toto55", "toto58"):
            continue
        g0 = dt.date.fromisoformat(common.load_game(key)["dates"][0])
        jd0 = eph.julian_day(t19(g0))
        N = {b: lon_sid(b, jd0) for b in BODIES}
        lag = int(N["Lagna"] // 30)
        rows = []
        for d, day in zip(dates, days):
            jd = eph.julian_day(t19(day))
            T = {b: lon_sid(b, jd) for b in BODIES}
            r = {"date": d}
            for b in BODIES[:-1]:
                r[f"tr_{b.lower()}_house"] = (int(T[b] // 30) - lag) % 12 + 1
            conj = hard = soft = 0
            for b in ("Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"):
                for n in ("Sun", "Moon", "Mars", "Mercury", "Venus", "Jupiter", "Saturn", "Lagna"):
                    a = abs(sdiff(T[b], N[n]))
                    conj += a < 3
                    hard += min(abs(a - 90), abs(a - 180)) < 3
                    soft += min(abs(a - 60), abs(a - 120)) < 3
            r.update(tr_conj=min(conj, 4), tr_hard=min(hard, 4), tr_soft=min(soft, 4),
                     tr_solar_return=abs(sdiff(T["Sun"], N["Sun"])) < 15, tr_lunar_return=abs(sdiff(T["Moon"], N["Moon"])) < 12)
            rows.append(r)
        with open(os.path.join(D, f"astro_params_transit_{key}.csv"), "w", newline="") as fh:
            w = csv.DictWriter(fh, list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print("transit", key, g0, flush=True)


if __name__ == "__main__":
    build()
