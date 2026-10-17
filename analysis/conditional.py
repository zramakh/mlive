#!/usr/bin/env python3
"""Do numbers depend on the astrological conditions of the draw date?

For every game, every single parameter (83) and every pair of parameters
(3,403), a "cell" is a value (or pair of values), e.g. "Moon in Rohini" or
"Moon in Rohini & Jupiter in Mesha". Three questions per parameter set:

1. Recurrence: do two draws in the same cell share numbers more often than two
   independent fair draws (k*k/n numbers on average)? z uses the exact
   variance of the overlap of two fair draws; the overlaps of different pairs
   of draws are uncorrelated under fairness.
2. Replication: learn each cell's k most frequent numbers on the train+valid
   draws, then play that ticket on the test-period draws of the same cell.
   Matches are compared with k*k/n per draw.
3. Strongest single association: the (cell, number) with the largest excess
   (cells with at least 10 draws), i.e. the kind of "number X comes up when Y"
   claim a search would produce.

Multiple testing: Bonferroni over the scan, and the whole scan is repeated on
circularly shifted parameter calendars (every parameter moved by the same
number of draws, at least a year's worth). That keeps every natural rhythm
of the parameters and of the draws and only breaks the link between them, so
the shifted scans show what the best of thousands of tests looks like by luck.

Walk-forward lead: the pair with the best recurrence z on the train+valid draws is
chosen first and then scored on the test period (the analogue of the 4D
"Mercury nakshatra x Venus rashi" lead).

python3 analysis/conditional.py   (~10 min on 4 cores) -> analysis/conditional_results.json
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

SHIFTS = 20
MIN_SHIFT = 160          # draws, a little over a year (about 3 draws a week)
OUT = os.path.join(common.ROOT, "analysis", "conditional_results.json")

G = {}                   # per-worker game data


def setup(key):
    g = common.load_game(key)
    codes, _ = common.codes_for(g["dates"])
    d = len(g["dates"])
    _, test_start = common.splits(d)
    rng = np.random.default_rng(7)
    shifts = rng.choice(np.arange(MIN_SHIFT, d - MIN_SHIFT), SHIFTS, replace=False)
    k, n = g["k"], g["n"]
    G.update(g=g, codes=codes, d=d, test_start=test_start, shifts=[0] + [int(s) for s in shifts],
             entry_draw=np.repeat(np.arange(d), k), entry_num=(g["nums"] - 1).ravel(),
             e_pair=k * k / n, v_pair=k * k / n * (1 - k / n) * (n - k) / (n - 1))


def evaluate(cell):
    """All statistics for one assignment of draws to cells."""
    g, d, ts = G["g"], G["d"], G["test_start"]
    k, n = g["k"], g["n"]
    _, cid = np.unique(cell, return_inverse=True)
    nc = int(cid.max()) + 1
    ed, en = G["entry_draw"], G["entry_num"]
    cnt = np.bincount(cid[ed] * n + en, minlength=nc * n).reshape(nc, n).astype(float)
    dc = np.bincount(cid, minlength=nc).astype(float)
    pairs = (dc * (dc - 1) / 2).sum()
    shared = (cnt * (cnt - 1) / 2).sum()
    rec_z = (shared - pairs * G["e_pair"]) / math.sqrt(pairs * G["v_pair"]) if pairs else 0.0

    pre = ed < ts
    cpre = np.bincount(cid[ed[pre]] * n + en[pre], minlength=nc * n).reshape(nc, n).astype(float)
    dpre = np.bincount(cid[:ts], minlength=nc)
    noise = np.random.default_rng(cid.sum() % 2**32).random((nc, n)) * 1e-3
    top = np.argpartition(-(cpre + noise), k - 1, axis=1)[:, :k]
    ticket = np.zeros((nc, n), bool)
    np.put_along_axis(ticket, top, True, axis=1)
    tcells = cid[ts:]
    seen = dpre[tcells] > 0
    tdraw = np.arange(ts, d)[seen]
    hits = int(ticket[cid[tdraw][:, None], g["nums"][tdraw] - 1].sum())
    nt = int(seen.sum())
    rep_z = (hits - nt * G["e_pair"]) / math.sqrt(nt * G["v_pair"]) if nt else 0.0

    big = dc >= 10
    best = None
    if big.any():
        e = dc[:, None] * k / n
        ex = np.where(big[:, None], (cnt - e) / np.sqrt(e), -np.inf)
        c, num = np.unravel_index(int(np.argmax(ex)), ex.shape)
        rows = np.flatnonzero(cid == c)
        best = {"z": round(float(ex[c, num]), 2), "number": int(num + 1), "wins": int(cnt[c, num]),
                "expected": round(float(e[c, 0]), 2), "draws": int(dc[c]), "first_draw": int(rows[0])}
    # recurrence z on pre-test draws only, for the walk-forward lead
    cid_pre = cid[:ts]
    dcp = np.bincount(cid_pre, minlength=nc).astype(float)
    pp = (dcp * (dcp - 1) / 2).sum()
    pre_z = ((cpre * (cpre - 1) / 2).sum() - pp * G["e_pair"]) / math.sqrt(pp * G["v_pair"]) if pp else 0.0
    return {"rec_z": round(rec_z, 3), "pre_rec_z": round(pre_z, 3), "rep_hits": hits,
            "rep_expected": round(nt * G["e_pair"], 2), "rep_z": round(rep_z, 3), "best": best}


def run(task):
    key, sets, shift_ix = task
    if G.get("key") != key:
        setup(key)
        G["key"] = key
    codes = np.roll(G["codes"], G["shifts"][shift_ix], axis=0)
    out = []
    for s in sets:
        cell = codes[:, s[0]].astype(np.int64)
        for j in s[1:]:
            cell = cell * 1000 + codes[:, j]
        out.append(evaluate(cell))
    return key, shift_ix, sets, out


def summarise(rows, ntests):
    z = np.array([r["rec_z"] for r in rows])
    rz = np.array([r["rep_z"] for r in rows])
    best = max((r["best"] for r in rows if r["best"]), key=lambda b: b["z"])
    return {"max_rec_z": round(float(z.max()), 2), "n_rec_z_gt3": int((z > 3).sum()),
            "mean_rec_z": round(float(z.mean()), 3), "max_rep_z": round(float(rz.max()), 2),
            "mean_rep_z": round(float(rz.mean()), 3),
            "rep_lift": round(sum(r["rep_hits"] for r in rows) / sum(r["rep_expected"] for r in rows), 4),
            "best_assoc_z": best["z"], "tests": ntests}


def main():
    names = common.ALL_PARAMS
    singles = [(i,) for i in range(len(names))]
    pairs = list(itertools.combinations(range(len(names)), 2))
    chunk = 120
    tasks = []
    for key in common.GAMES:
        for sh in range(SHIFTS + 1):
            tasks += [(key, singles, sh)]
            tasks += [(key, pairs[i:i + chunk], sh) for i in range(0, len(pairs), chunk)]
    results = {}
    with Pool(4) as pool:
        for i, (key, sh, sets, out) in enumerate(pool.imap_unordered(run, tasks, chunksize=4), 1):
            results.setdefault(key, {}).setdefault(sh, {}).update(zip(sets, out))
            if i % 200 == 0:
                print(f"{i}/{len(tasks)}", flush=True)

    res = {}
    for key, by_shift in results.items():
        g = common.load_game(key)
        k, n = g["k"], g["n"]
        ts = common.splits(len(g["dates"]))[1]
        label = lambda s: " x ".join(names[j] for j in s)  # noqa: E731
        real = by_shift[0]
        game = {"label": g["label"], "test_from": g["dates"][ts]}
        for kind, sets in (("singles", singles), ("pairs", pairs)):
            rows = [real[s] for s in sets]
            shifted = [summarise([by_shift[sh][s] for s in sets], len(sets)) for sh in range(1, SHIFTS + 1)]
            summ = summarise(rows, len(sets))
            summ["shifted"] = {f: [x[f] for x in shifted] for f in shifted[0] if f != "tests"}
            summ["real_beats_shifts"] = {f: sum(summ[f] > x for x in summ["shifted"][f])
                                         for f in summ["shifted"]}
            order = sorted(sets, key=lambda s: -real[s]["rec_z"])
            summ["top_recurrence"] = [{"params": label(s), **real[s]} for s in order[:10]]
            order = sorted(sets, key=lambda s: -real[s]["rep_z"])
            summ["top_replication"] = [{"params": label(s), **real[s]} for s in order[:10]]
            order = sorted((s for s in sets if real[s]["best"]), key=lambda s: -real[s]["best"]["z"])
            summ["top_associations"] = [{"params": label(s), **real[s]["best"],
                                         "first_draw": g["dates"][real[s]["best"]["first_draw"]]}
                                        for s in order[:10]]
            # walk-forward: chosen on pre-test recurrence only
            order = sorted(sets, key=lambda s: -real[s]["pre_rec_z"])
            summ["walk_forward_leads"] = [{"params": label(s), "pre_rec_z": real[s]["pre_rec_z"],
                                           "test_rep_hits": real[s]["rep_hits"],
                                           "test_rep_expected": real[s]["rep_expected"],
                                           "test_rep_z": real[s]["rep_z"]} for s in order[:5]]
            game[kind] = summ
            print(g["label"], kind, {f: summ[f] for f in ("max_rec_z", "n_rec_z_gt3", "rep_lift",
                                                           "best_assoc_z", "real_beats_shifts")})
            print("   lead:", summ["walk_forward_leads"][0])
        res[key] = game
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
