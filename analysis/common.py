"""Shared loading code: draw history of the four games and the astrological
parameters of every draw date.

Parameters come from almanac.py (Vedic / KP / Chinese almanac, ported from the
4DPrediction repo) plus a few calendar and Western values, all evaluated for
19:00 Malaysia time, when Sports Toto and Magnum Life draw. They are cached in
data/astro_params.csv; delete it (or run `python3 analysis/common.py`) to rebuild.

Splits (per game, by draw order, fixed before any model was run):
  train  first 50% of draws
  valid  next 20%            (used to choose formulas and settings)
  test   last 30%            (only scored after the formulas were frozen)
"""

import csv
import datetime as dt
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import almanac  # noqa: E402
import ephemeris as eph  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
PARAMS_CSV = os.path.join(DATA, "astro_params.csv")

# key: (csv, label, main numbers drawn, highest number)
GAMES = {
    "toto50": ("star_toto_6_50.csv", "STAR TOTO 6/50", 6, 50),
    "toto55": ("power_toto_6_55.csv", "POWER TOTO 6/55", 6, 55),
    "toto58": ("supreme_toto_6_58.csv", "SUPREME TOTO 6/58", 6, 58),
    "ml8": ("magnum_life.csv", "Magnum Life 8/36", 8, 36),
}
TRAIN_FRAC, VALID_FRAC = 0.5, 0.2
# Dates the parameter table also covers, so picks can be made before a draw.
FUTURE_DAYS = 120

VEDIC = ["tithi", "paksha", "nakshatra", "nakshatra_lord", "nakshatra_pada", "yoga", "karana", "weekday",
         "hora_lord", "moon_rashi", "sun_rashi", "sun_nakshatra", "mars_rashi", "mars_nakshatra",
         "mercury_rashi", "mercury_nakshatra", "venus_rashi", "venus_nakshatra", "jupiter_rashi",
         "jupiter_nakshatra", "saturn_rashi", "saturn_nakshatra", "rahu_rashi", "rahu_nakshatra",
         "lagna_rashi", "lagna_nakshatra", "moon_navamsa", "mercury_retrograde", "venus_retrograde",
         "mars_retrograde", "jupiter_retrograde", "saturn_retrograde", "mercury_combust", "venus_combust",
         "mars_combust", "jupiter_combust", "saturn_combust", "planets_with_moon", "masa", "adhika_masa",
         "ritu", "ayana", "samvatsara", "kp_moon_star_lord", "kp_moon_sub_lord", "kp_moon_number",
         "kp_asc_star_lord", "kp_asc_sub_lord", "kp_asc_number", "kp_sun_star_lord", "kp_sun_sub_lord",
         "kp_sun_number"]
CHINESE = ["year_animal", "year_stem", "year_element", "year_yinyang", "year_pillar", "lunar_month",
           "lunar_day", "lunar_leap_month", "solar_term", "month_branch", "month_stem", "month_pillar",
           "day_stem", "day_branch", "day_element", "day_pillar", "nayin", "nayin_element", "hour_stem_19h",
           "day_officer", "day_god", "yellow_black_path", "mansion_28", "day_vs_year_branch",
           "nine_star_year", "nine_star_month"]
OTHER = ["month", "day_of_month", "moon_phase", "moon_sign_tropical", "sun_sign_tropical"]
ALL_PARAMS = VEDIC + CHINESE + OTHER


def all_factors(date):
    day = dt.date.fromisoformat(date)
    out = almanac.factors(date)
    w = eph.describe(dt.datetime.combine(day, dt.time(11)))       # 19:00 MYT = 11:00 UTC
    out.update(weekday=day.strftime("%a"), month=day.strftime("%b"), day_of_month=day.day,
               moon_phase=w["phase"], moon_sign_tropical=w["moon_sign"], sun_sign_tropical=w["sun_sign"])
    return {k: str(out[k]) for k in ALL_PARAMS}


def load_game(key):
    """Draw dates and a draws x (N+1) 0/1 matrix of main numbers (column 0 unused)."""
    fname, label, k, n = GAMES[key]
    dates, rows = [], []
    with open(os.path.join(DATA, fname)) as fh:
        for r in csv.DictReader(fh):
            dates.append(r["draw_date"])
            rows.append([int(r[f"n{i}"]) for i in range(1, k + 1)])
    m = np.zeros((len(rows), n + 1), np.int8)
    for i, nums in enumerate(rows):
        m[i, nums] = 1
    return {"key": key, "label": label, "k": k, "n": n, "dates": dates, "nums": np.array(rows), "hit": m}


def splits(n_draws):
    a = int(n_draws * TRAIN_FRAC)
    b = int(n_draws * (TRAIN_FRAC + VALID_FRAC))
    return a, b


def build_params():
    dates = set()
    for key in GAMES:
        dates.update(load_game(key)["dates"])
    last = dt.date.fromisoformat(max(dates))
    dates.update((last + dt.timedelta(days=i)).isoformat() for i in range(1, FUTURE_DAYS + 1))
    with open(PARAMS_CSV, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date"] + ALL_PARAMS)
        for d in sorted(dates):
            f = all_factors(d)
            w.writerow([d] + [f[p] for p in ALL_PARAMS])
    print(f"wrote {PARAMS_CSV}: {len(dates)} dates x {len(ALL_PARAMS)} parameters")


def load_params():
    """{date: {param: value string}} for every draw date and the next FUTURE_DAYS days."""
    if not os.path.exists(PARAMS_CSV):
        build_params()
    with open(PARAMS_CSV) as fh:
        return {r.pop("date"): r for r in csv.DictReader(fh)}


def codes_for(dates, names=ALL_PARAMS):
    """Integer-code matrix (len(dates) x len(names)); codes are shared across games so
    a value means the same in every game. Returns (codes, value lists)."""
    table = load_params()
    out = np.zeros((len(dates), len(names)), np.int32)
    values = []
    for j, p in enumerate(names):
        vals = sorted({r[p] for r in table.values()})
        ix = {v: i for i, v in enumerate(vals)}
        out[:, j] = [ix[table[d][p]] for d in dates]
        values.append(vals)
    return out, values


if __name__ == "__main__":
    build_params()
