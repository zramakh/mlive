#!/usr/bin/env python3
"""The 4DPrediction repo's top-ranked lead (Mercury nakshatra x Venus rashi) and
runner-up (karana x day pillar) scored on the Toto / Magnum Life games with
the recurrence and replication statistics of conditional.py. These pairs were
chosen on 4D data, so they are an independent out-of-sample check here.

Also: the replication split into the two halves of the test period, and the
lead's ticket for upcoming dates (the k numbers drawn most often in the same
Mercury nakshatra x Venus rashi cell), appended to forward_log.csv as variant
"lead_4d".

python3 analysis/lead_4d_check.py [--log 2026-10-18 2026-10-21]  -> analysis/lead_4d_check_results.json
"""

import csv
import datetime as dt
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import conditional as cd  # noqa: E402

LEADS = [("mercury_nakshatra", "venus_rashi"), ("karana", "day_pillar")]
OUT = os.path.join(common.ROOT, "analysis", "lead_4d_check_results.json")
LOG = os.path.join(common.ROOT, "analysis", "forward_log.csv")


def halves(key, lead):
    """Replication hits in each half of the test period (tickets learned before the test period)."""
    g = common.load_game(key)
    codes, _ = common.codes_for(g["dates"], list(lead))
    cell = codes[:, 0] * 1000 + codes[:, 1]
    k, n = g["k"], g["n"]
    ts = common.splits(len(cell))[1]
    rng = np.random.default_rng(0)
    tickets = {}
    for c in set(cell[:ts]):
        cnt = g["hit"][:ts][cell[:ts] == c, 1:].sum(0) + rng.random(n) * 1e-3
        tickets[c] = set((np.argsort(-cnt)[:k] + 1).tolist())
    e, v = k * k / n, k * k / n * (1 - k / n) * (n - k) / (n - 1)
    rows = [i for i in range(ts, len(cell)) if cell[i] in tickets]
    out = []
    for part in (rows[: len(rows) // 2], rows[len(rows) // 2:]):
        hits = sum(len(tickets[cell[i]] & set(g["nums"][i].tolist())) for i in part)
        out.append({"from": g["dates"][part[0]], "to": g["dates"][part[-1]], "draws": len(part), "hits": hits,
                    "expected": round(len(part) * e, 1), "z": round((hits - len(part) * e) / np.sqrt(len(part) * v), 2)})
    return out


def ticket(key, lead, date):
    g = common.load_game(key)
    codes, _ = common.codes_for(g["dates"] + [date], list(lead))
    cell = codes[:, 0] * 1000 + codes[:, 1]
    same = cell[:-1] == cell[-1]
    cnt = g["hit"][same, 1:].sum(0) + np.random.default_rng(0).random(g["n"]) * 1e-3
    return sorted((np.argsort(-cnt)[:g["k"]] + 1).tolist()), int(same.sum())


def main():
    ix = {p: i for i, p in enumerate(common.ALL_PARAMS)}
    res = {}
    for key in common.GAMES:
        cd.G.clear()
        _, _, sets, out = cd.run((key, [tuple(ix[p] for p in lead) for lead in LEADS], 0))
        res[key] = {" x ".join(lead): {k: v for k, v in o.items() if k != "best"} for lead, o in zip(LEADS, out)}
        print(common.GAMES[key][1], res[key])
        for lead in LEADS:
            res[key][" x ".join(lead)]["test_halves"] = halves(key, lead)
            print("   ", " x ".join(lead), res[key][" x ".join(lead)]["test_halves"])
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
    if "--log" in sys.argv:
        now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes")
        with open(LOG, "a", newline="") as fh:
            w = csv.writer(fh)
            for date in sys.argv[sys.argv.index("--log") + 1:]:
                for key in common.GAMES:
                    nums, draws = ticket(key, LEADS[0], date)
                    w.writerow([date, key, "lead_4d", " ".join(f"{x:02d}" for x in nums), now])
                    print(date, key, "lead_4d", nums, f"(from {draws} earlier draws in the same cell)")


if __name__ == "__main__":
    main()
