#!/usr/bin/env python3
"""Validate raw lotto-8.com transcripts in data/raw/ and write tidy CSVs to data/.

Raw line format (one draw per line, as scraped from www.lotto-8.com):
    DD/MM/YY|n1 n2 ... nk|b1 [b2]
The bonus field is absent for games without a bonus number.
"""
import csv
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data"

GAMES = {
    # key: (raw file, output csv, label, main count, max number, bonus count)
    "toto50": ("toto50.txt", "star_toto_6_50.csv", "STAR TOTO 6/50", 6, 50, 1),
    "toto55": ("toto55.txt", "power_toto_6_55.csv", "POWER TOTO 6/55", 6, 55, 0),
    "toto58": ("toto58.txt", "supreme_toto_6_58.csv", "SUPREME TOTO 6/58", 6, 58, 0),
    "ml8": ("ml8.txt", "magnum_life.csv", "Magnum Life 8/36", 8, 36, 2),
}


def parse(path, n_main, max_no, n_bonus):
    rows, errors, warnings = [], [], []
    for lineno, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        parts = line.split("|")
        try:
            date = dt.datetime.strptime(parts[0], "%d/%m/%y").date()
        except ValueError:
            errors.append(f"{path.name}:{lineno}: bad date {parts[0]!r}")
            continue
        main = [int(x) for x in parts[1].split()]
        bonus = [int(x) for x in parts[2].split()] if n_bonus else []
        if len(main) != n_main or len(bonus) != n_bonus:
            errors.append(f"{path.name}:{lineno}: wrong number count {line!r}")
            continue
        if not all(1 <= x <= max_no for x in main + bonus):
            errors.append(f"{path.name}:{lineno}: number out of range {line!r}")
        if len(set(main + bonus)) != n_main + n_bonus:
            errors.append(f"{path.name}:{lineno}: repeated number {line!r}")
        if main != sorted(main):
            warnings.append(f"{path.name}:{lineno}: numbers not ascending on source {line!r}")
        rows.append((date, main, bonus))
    return rows, errors, warnings


def main():
    failed = False
    for key, (raw, out, label, n_main, max_no, n_bonus) in GAMES.items():
        rows, errors, warnings = parse(RAW / raw, n_main, max_no, n_bonus)
        dates = [r[0] for r in rows]
        dupes = sorted({d for d in dates if dates.count(d) > 1})
        errors += [f"{raw}: duplicate draw date {d}" for d in dupes]
        for msg in warnings:
            print("warning:", msg)
        if errors:
            failed = True
            print("\n".join(errors), file=sys.stderr)
            continue

        rows.sort(key=lambda r: r[0])
        header = ["draw_date", "day"] + [f"n{i}" for i in range(1, n_main + 1)]
        header += ["bonus"] if n_bonus == 1 else [f"bonus{i}" for i in range(1, n_bonus + 1)]
        with open(OUT / out, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(header)
            for date, nums, bonus in rows:
                w.writerow([date.isoformat(), date.strftime("%a").upper()]
                           + [f"{x:02d}" for x in nums + bonus])
        print(f"{label}: {len(rows)} draws, {rows[0][0]} .. {rows[-1][0]} -> data/{out}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
