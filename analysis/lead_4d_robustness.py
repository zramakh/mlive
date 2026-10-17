#!/usr/bin/env python3
"""Is the 4D lead (Mercury nakshatra x Venus rashi) special on these games?

1. Rank among all 3,403 pairs: the 4D lead's replication z (conditional.py
   statistic) in each game, and summed over the four games, against every
   other pair, on the real calendar and on 10 shifted calendars.
2. Cross-game consistency: if some parameter pairs carried a real signal,
   their replication z would correlate between games.
3. Robustness of the Magnum Life result: ticket size and the date the
   tickets are learned up to are varied; a real effect should not depend on them.
4. Rank in the walk-forward lead search (own_leads.py, test period).

python3 analysis/lead_4d_robustness.py  (~3 min on 4 cores) -> analysis/lead_4d_robustness_results.json
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
import conditional as cd  # noqa: E402

NAMES = common.ALL_PARAMS
PAIRS = list(itertools.combinations(range(len(NAMES)), 2))
LEADS = {"4D lead #1": ("mercury_nakshatra", "venus_rashi"), "4D lead #2": ("karana", "day_pillar")}
SHIFTS = 10
OUT = os.path.join(common.ROOT, "analysis", "lead_4d_robustness_results.json")


def rep_all(task):
    key, sh = task
    cd.G.clear()
    _, _, _, out = cd.run((key, PAIRS, sh))
    return key, sh, np.array([o["rep_z"] for o in out])


def replication(key, lead, k_ticket, learn_frac):
    """Static replication z of one pair with a ticket of k_ticket numbers learned on draws before learn_frac."""
    g = common.load_game(key)
    codes, _ = common.codes_for(g["dates"], list(lead))
    cell = codes[:, 0] * 1000 + codes[:, 1]
    k, n = g["k"], g["n"]
    ts = int(len(cell) * learn_frac)
    rng = np.random.default_rng(0)
    hits = draws = 0
    for c in set(cell[ts:]):
        before = cell[:ts] == c
        if not before.any():
            continue
        cnt = g["hit"][:ts][before, 1:].sum(0) + rng.random(n) * 1e-3
        ticket = np.argsort(-cnt)[:k_ticket] + 1
        after = np.flatnonzero(cell[ts:] == c) + ts
        hits += int(np.isin(g["nums"][after], ticket).sum())
        draws += len(after)
    e = k * k_ticket / n
    v = e * (1 - k / n) * (n - k_ticket) / (n - 1)
    return {"draws": draws, "hits": hits, "expected": round(draws * e, 1), "z": round((hits - draws * e) / math.sqrt(draws * v), 2)}


def main():
    ix = {p: i for i, p in enumerate(NAMES)}
    lead_ix = {name: PAIRS.index(tuple(sorted(ix[p] for p in lead))) for name, lead in LEADS.items()}
    tasks = [(key, sh) for key in common.GAMES for sh in range(SHIFTS + 1)]
    Z = {}
    with Pool(4) as pool:
        for key, sh, z in pool.imap_unordered(rep_all, tasks):
            Z[(key, sh)] = z
    games = list(common.GAMES)
    res = {"rank": {}, "cross_game": {}, "robustness": {}, "walk_forward_rank": {}}

    for name, li in lead_ix.items():
        r = {}
        for key in games:
            z = Z[(key, 0)]
            r[key] = {"z": float(z[li]), "pairs_at_least_as_high": int((z >= z[li]).sum()),
                      "share": round(float((z >= z[li]).mean()), 4)}
        tot = sum(Z[(key, 0)] for key in games)
        r["sum_over_games"] = {"z_sum": round(float(tot[li]), 2), "pairs_at_least_as_high": int((tot >= tot[li]).sum()),
                               "share": round(float((tot >= tot[li]).mean()), 4)}
        # same rank on shifted calendars, where no pair can carry a real signal
        r["sum_over_games"]["shifted_best_z_sum"] = [round(float(sum(Z[(key, s)] for key in games).max()), 2)
                                                     for s in range(1, SHIFTS + 1)]
        r["sum_over_games"]["real_best_z_sum"] = round(float(tot.max()), 2)
        r["sum_over_games"]["real_best_pair"] = " x ".join(NAMES[j] for j in PAIRS[int(tot.argmax())])
        res["rank"][name] = r
        print(name, r)

    corr = {}
    for a, b in itertools.combinations(games, 2):
        corr[f"{a}~{b}"] = {"real": round(float(np.corrcoef(Z[(a, 0)], Z[(b, 0)])[0, 1]), 3),
                            "shifted": [round(float(np.corrcoef(Z[(a, s)], Z[(b, s)])[0, 1]), 3)
                                        for s in range(1, SHIFTS + 1)]}
    res["cross_game"] = corr
    print("cross-game correlation of replication z:", {k: v["real"] for k, v in corr.items()})

    rob = {}
    for kt in (4, 6, 8, 10, 12):
        for lf in (0.6, 0.7, 0.8):
            rob[f"ticket {kt}, learned on first {int(lf * 100)}%"] = replication("ml8", LEADS["4D lead #1"], kt, lf)
    res["robustness"]["ml8"] = rob
    for k2, v in rob.items():
        print("  ml8", k2, v)

    zf = np.load(os.path.join(common.ROOT, "analysis", "own_leads_z.npz"))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import own_leads as ol
    oi = ol.SETS.index(tuple(sorted(ol.PARAMS.index(p) for p in LEADS["4D lead #1"])))
    pair_rows = [i for i, s in enumerate(ol.SETS) if len(s) == 2]
    for key in games:
        test = zf[key][0][:, :, 2]
        res["walk_forward_rank"][key] = {
            m: {"z": round(float(test[oi, mi]), 2),
                "share_of_pairs_at_least_as_high": round(float((test[pair_rows, mi] >= test[oi, mi]).mean()), 3)}
            for mi, m in enumerate(ol.METRICS)}
    print("walk-forward ranks:", res["walk_forward_rank"])
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
