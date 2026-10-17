#!/usr/bin/env python3
"""Hunt for leads that beat the 4D lead (Mercury nakshatra x Venus rashi), using
several selection methods that, like the 4D lead, choose without looking at
the test draws they are scored on.

Score (the statistic that gave the 4D lead z = +2.75 on Magnum Life): for a
parameter set, each cell's k most frequent numbers are learned on the first
70% of a game's draws and played on the same cell's draws in the last 30%
(test); z of numbers matched against k*k/n per ticket.

Methods (each picks its top 5 sets per game unless stated):
  4d_picks      every set the 4DPrediction repo picked on 1985-2011 4D draws (top 5 of each of
                its 12 S1/S2 columns, recurrence_s12_forward_results.json), lead #1 among them
  valid         learn on 0-50%, score on 50-70%, best pairs
  stable        best min(z on 35-50% learned on 0-35%, z on 50-70% learned on 0-50%), pairs
  transfer      best summed full-history z over the OTHER three games (unrelated draws, like 4D)
  pooled        best summed 50-70% validation z over all four games (one list for every game)
  triples       30,000 random triples, best on the 50-70% validation
  random        200 random pairs, no selection at all (the chance baseline)

python3 analysis/lead_hunt.py  (~2 min on 4 cores) -> analysis/lead_hunt_results.json
"""

import itertools
import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

NAMES = common.ALL_PARAMS
IX = {p: i for i, p in enumerate(NAMES)}
PAIRS = list(itertools.combinations(range(len(NAMES)), 2))
TOP = 5
N_TRIPLES = 30000
N_RANDOM = 200
LEAD = tuple(sorted((IX["mercury_nakshatra"], IX["venus_rashi"])))
S12_FORWARD = os.path.join(common.ROOT, "..", "4DPrediction", "analysis", "recurrence_s12_forward_results.json")
OUT = os.path.join(common.ROOT, "analysis", "lead_hunt_results.json")

G = {}


def setup(key):
    g = common.load_game(key)
    codes, _ = common.codes_for(g["dates"])
    G.clear()
    G.update(key=key, g=g, codes=codes, d=len(g["dates"]), k=g["k"], n=g["n"],
             noise=np.random.default_rng(21).random((len(g["dates"]), g["n"])) * 1e-3)


def rep_z(s, learn_end, lo, hi):
    """Replication z of set s: tickets learned on draws [0, learn_end), scored on [lo, hi)."""
    g, k, n, d = G["g"], G["k"], G["n"], G["d"]
    cell = G["codes"][:, s[0]].astype(np.int64)
    for j in s[1:]:
        cell = cell * 1000 + G["codes"][:, j]
    _, cid = np.unique(cell, return_inverse=True)
    nc = int(cid.max()) + 1
    a, b = int(learn_end * d), int(lo * d)
    c = int(hi * d)
    pre = np.repeat(np.arange(a), k)
    cnt = np.bincount(cid[pre] * n + (g["nums"][:a] - 1).ravel(), minlength=nc * n).reshape(nc, n)
    seen = np.bincount(cid[:a], minlength=nc) > 0
    top = np.argpartition(-(cnt + G["noise"][:nc]), k - 1, 1)[:, :k]
    ticket = np.zeros((nc, n), bool)
    np.put_along_axis(ticket, top, True, 1)
    rows = np.arange(b, c)
    rows = rows[seen[cid[rows]]]
    hits = int(ticket[cid[rows][:, None], g["nums"][rows] - 1].sum())
    e = k * k / n
    v = e * (1 - k / n) * (n - k) / (n - 1)
    return (hits - len(rows) * e) / math.sqrt(len(rows) * v) if len(rows) else 0.0


def scores(task):
    """For one game and a list of sets: test z, validation z (0-50 -> 50-70) and early z (0-35 -> 35-50)."""
    key, sets = task
    if G.get("key") != key:
        setup(key)
    return key, sets, [(rep_z(s, 0.7, 0.7, 1.0), rep_z(s, 0.5, 0.5, 0.7), rep_z(s, 0.35, 0.35, 0.5)) for s in sets]


def four_d_picks():
    r = json.load(open(S12_FORWARD))
    out = []
    for col, picks in r["columns"].items():
        for p in picks:
            names = p["test"].split(" x ")
            if all(x in IX for x in names):
                s = tuple(sorted(IX[x] for x in names))
                if s not in out:
                    out.append(s)
    return out


def main():
    rng = np.random.default_rng(4)
    games = list(common.GAMES)
    k = len(NAMES)
    triples = set()
    while len(triples) < N_TRIPLES:
        triples.add(tuple(sorted(rng.choice(k, 3, replace=False).tolist())))
    triples = sorted(triples)
    four_d = four_d_picks()
    rand = [PAIRS[i] for i in rng.choice(len(PAIRS), N_RANDOM, replace=False)]
    sets = sorted(set(PAIRS) | set(triples) | set(four_d) | {LEAD})
    chunk = 600
    tasks = [(key, sets[i:i + chunk]) for key in games for i in range(0, len(sets), chunk)]
    S = {key: {} for key in games}
    with Pool(4) as pool:
        for key, ss, out in pool.imap_unordered(scores, tasks):
            S[key].update(zip(ss, out))
    label = lambda s: " x ".join(NAMES[j] for j in s)  # noqa: E731

    picks = {m: {} for m in ("4d_picks", "valid", "stable", "transfer", "pooled", "triples", "random")}
    pooled = sorted(PAIRS, key=lambda s: -sum(S[g][s][1] for g in games))[:TOP]
    for key in games:
        sc = S[key]
        picks["4d_picks"][key] = four_d
        picks["valid"][key] = sorted(PAIRS, key=lambda s: -sc[s][1])[:TOP]
        picks["stable"][key] = sorted(PAIRS, key=lambda s: -min(sc[s][1], sc[s][2]))[:TOP]
        others = [g for g in games if g != key]
        picks["transfer"][key] = sorted(PAIRS, key=lambda s: -sum(S[g][s][0] for g in others))[:TOP]
        picks["pooled"][key] = pooled
        picks["triples"][key] = sorted(triples, key=lambda s: -sc[s][1])[:TOP]
        picks["random"][key] = rand

    lead = {key: round(S[key][LEAD][0], 2) for key in games}
    lead_sum = sum(S[key][LEAD][0] for key in games)
    res = {"score": "replication z, tickets learned on first 70%, scored on last 30%",
           "lead_4d": {"set": label(LEAD), "test_z": lead, "sum": round(lead_sum, 2)}, "methods": {}}
    print(f"4D lead {label(LEAD)}: {lead}  sum {lead_sum:+.2f}")
    print(f"{'method':<10} {'picks':>6} {'mean z':>7} {'sd':>5} {'max z':>6} {'>= lead (any game)':>20}  best pick")
    for m, by_game in picks.items():
        zs, rows = [], []
        for key in games:
            for s in by_game[key]:
                z = S[key][s][0]
                zs.append(z)
                rows.append({"game": key, "set": label(s), "test_z": round(z, 2), "valid_z": round(S[key][s][1], 2),
                             "early_z": round(S[key][s][2], 2)})
        zs = np.array(zs)
        best = max(rows, key=lambda r: r["test_z"])
        entry = {"picks": len(zs), "mean_test_z": round(float(zs.mean()), 3), "sd_test_z": round(float(zs.std()), 3),
                 "max_test_z": round(float(zs.max()), 2), "n_at_least_lead_ml8_z": int((zs >= lead["ml8"]).sum()),
                 "best": best, "all": sorted(rows, key=lambda r: -r["test_z"])}
        # sets picked once for every game: compare the sum over games with the 4D lead's
        if m in ("4d_picks", "pooled", "random"):
            sums = sorted(((sum(S[g][s][0] for g in games), s) for s in by_game[games[0]]), reverse=True)
            entry["n_sum_at_least_lead"] = sum(t >= lead_sum for t, _ in sums)
            entry["best_sum"] = {"set": label(sums[0][1]), "sum": round(sums[0][0], 2),
                                 "by_game": {g: round(S[g][sums[0][1]][0], 2) for g in games}}
        res["methods"][m] = entry
        print(f"{m:<10} {len(zs):>6} {zs.mean():>+7.3f} {zs.std():>5.2f} {zs.max():>+6.2f} {entry['n_at_least_lead_ml8_z']:>20}  "
              f"{best['set']} ({best['game']}, {best['test_z']:+.2f})"
              + (f"  | best sum {entry['best_sum']['set']} {entry['best_sum']['sum']:+.2f}, "
                 f"{entry['n_sum_at_least_lead']} sets >= lead sum" if "best_sum" in entry else ""))
    allp = np.array([S[g][s][0] for g in games for s in PAIRS])
    res["all_pairs_share_at_least_lead_ml8_z"] = round(float((allp >= lead["ml8"]).mean()), 5)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
    print("share of all game x pair scores >= 4D lead's ML8 z:", res["all_pairs_share_at_least_lead_ml8_z"])


if __name__ == "__main__":
    main()
