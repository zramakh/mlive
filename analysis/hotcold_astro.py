#!/usr/bin/env python3
"""Hot / cold numbers combined with an astrology lead in one score.

For every number at draw t (walk-forward, earlier draws only):
  Fh  = standardised count over the previous Nh draws ((count - Nh k/n) / sd), likewise Fc for Nc
  A   = standardised count over earlier draws of the same astrology cell (own_leads.py "hot" cell signal)
  score = alpha * Fh + beta * Fc + gamma * A           (alpha, beta < 0 = cold)
Ticket = the k top-scoring numbers.

Menu: Nh, Nc in WINDOWS; alpha, beta in {-1, 0, 1}; gamma in GAMMAS; the astrology set is one of the
TOP_SETS parameter sets (singles and pairs) that ranked best on the early and validation periods of
own_leads.py (min of the two z of its hot pattern; the test period was not used).
Chosen on draws 25-70%, tested on 70% .. D-HOLD and on the last HOLD draws.
Control: the same on SHIFTS shifted parameter calendars (the astrology part re-selected on them), so the
hot/cold part is identical and only the astrology link is broken.

python3 analysis/hotcold_astro.py  (~10 min on 4 cores) -> analysis/hotcold_astro_results.json
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
import own_leads as ol  # noqa: E402

WINDOWS = [20, 100, 300]
SIGNS = [-1.0, 0.0, 1.0]
GAMMAS = [0.0, 0.5, 1.0, 2.0]
TOP_SETS = 20
SHIFTS = 5
HOLD = 10
OUT = os.path.join(common.ROOT, "analysis", "hotcold_astro_results.json")
TICK = ol.METRICS.index("hot")


def window_feature(h, N, k, n):
    d = len(h)
    cum = np.vstack([np.zeros((1, n)), np.cumsum(h, 0)])
    F = np.full((d, n), np.nan, np.float32)
    e = N * k / n
    F[N:] = (cum[N:d] - cum[:d - N] - e) / math.sqrt(e * (1 - k / n))
    return F


def cell_feature(codes, s, h, k, n):
    cid = ol.cell_of(codes, s)
    order = np.argsort(cid, kind="stable")
    cs = cid[order]
    first = np.r_[0, np.flatnonzero(np.diff(cs)) + 1]
    starts = np.repeat(first, np.diff(np.r_[first, len(cid)]))

    def ex(X):
        xs = X[order]
        c = np.cumsum(xs, 0) - xs
        c = c - c[starts]
        out = np.empty_like(X)
        out[order] = c
        return out

    cnt = ex(h)
    dp = ex(np.ones((len(h), 1)))
    e = dp * k / n
    return ((cnt - e) / np.sqrt(e * (1 - k / n) + 1e-9)).astype(np.float32)


def zs(m, k, n):
    e = k * k / n
    v = e * (1 - k / n) * (n - k) / (n - 1)
    return (m.sum(0) - len(m) * e) / np.sqrt(len(m) * v)


def run(task):
    key, shift_ix = task
    ol.setup(key)
    g = ol.G["g"]
    h = ol.G["H"].astype(np.float64)
    k, n = g["k"], g["n"]
    d = len(h)
    codes = np.roll(ol.G["codes"], ol.G["shifts"][shift_ix], axis=0)
    z = np.load(os.path.join(common.ROOT, "analysis", "own_leads_z.npz"))[key][shift_ix]
    rank_score = np.minimum(z[:, TICK, 0], z[:, TICK, 1])
    sets = [ol.SETS[i] for i in np.argsort(-rank_score)[:TOP_SETS]]
    Fw = {N: window_feature(h, N, k, n) for N in WINDOWS}
    noise = np.random.default_rng(3).random((d, n)).astype(np.float32) * 1e-4
    s0, s1, t1 = int(0.25 * d), int(0.7 * d), d - HOLD
    rows = np.arange(max(WINDOWS), d)
    combos, cols = [], []
    for si, s in enumerate(sets):
        A = np.nan_to_num(cell_feature(codes, s, h, k, n))
        for Nh, Nc in itertools.product(WINDOWS, WINDOWS):
            for a, b in itertools.product(SIGNS, SIGNS):
                if (a == 0 and Nh != WINDOWS[0]) or (b == 0 and Nc != WINDOWS[0]):
                    continue                                        # unused windows: keep one copy
                base = a * Fw[Nh][rows] + b * Fw[Nc][rows]
                for gm in GAMMAS:
                    if gm == 0 and si > 0:
                        continue                                    # no astrology: same for every set
                    if a == 0 and b == 0 and gm == 0:
                        continue
                    S = base + gm * A[rows] + noise[rows]
                    top = np.argpartition(-S, k - 1, 1)[:, :k]
                    cols.append(h[rows[:, None], top].sum(1))
                    combos.append({"set": " × ".join(ol.PARAMS[j] for j in s), "Nh": Nh, "Nc": Nc,
                                   "alpha": a, "beta": b, "gamma": gm})
    M = np.array(cols).T                                            # rows x combos
    r = lambda lo, hi: (rows >= lo) & (rows < hi)  # noqa: E731
    sel = zs(M[r(s0, s1)], k, n)
    test = zs(M[r(s1, t1)], k, n)
    last = M[r(t1, d)].sum(0)
    best = int(np.argmax(sel))
    c = combos[best]
    # the same combination with the astrology term removed
    twin = next((i for i, x in enumerate(combos) if x["gamma"] == 0 and x["alpha"] == c["alpha"] and x["beta"] == c["beta"]
                 and x["Nh"] == c["Nh"] and x["Nc"] == c["Nc"]), None)
    no_astro = [i for i, x in enumerate(combos) if x["gamma"] == 0]
    best_na = no_astro[int(np.argmax(sel[no_astro]))]
    return key, shift_ix, {
        "combinations": len(combos), "chosen": c, "select_z": round(float(sel[best]), 2),
        "test_z": round(float(test[best]), 2), "last10": int(last[best]),
        "same_without_astrology": None if twin is None else {"select_z": round(float(sel[twin]), 2),
                                                             "test_z": round(float(test[twin]), 2), "last10": int(last[twin])},
        "best_without_astrology": {"combo": combos[best_na], "select_z": round(float(sel[best_na]), 2),
                                   "test_z": round(float(test[best_na]), 2), "last10": int(last[best_na])},
        "astro_sets": [" × ".join(ol.PARAMS[j] for j in s) for s in sets[:5]],
        "last10_expected": round(HOLD * k * k / n, 2)}


def main():
    tasks = [(key, s) for key in common.GAMES for s in range(SHIFTS + 1)]
    with Pool(4) as pool:
        out = list(pool.imap_unordered(run, tasks))
    res = {"games": {}}
    for key in common.GAMES:
        rows = {s: r for k2, s, r in out if k2 == key}
        real = rows[0]
        sh = [rows[s] for s in range(1, SHIFTS + 1)]
        res["games"][key] = {"label": common.GAMES[key][1], "real": real, "shifted": sh}
        c = real["chosen"]
        print(f"{common.GAMES[key][1]} ({real['combinations']} combos): chosen gamma {c['gamma']} set {c['set']} "
              f"alpha {c['alpha']} Nh {c['Nh']} beta {c['beta']} Nc {c['Nc']} | select {real['select_z']:+.2f} "
              f"test {real['test_z']:+.2f} last10 {real['last10']}/{real['last10_expected']} | without astrology "
              f"{real['same_without_astrology']} | best no-astro {real['best_without_astrology']['test_z']:+.2f}")
        print("    shifted: select", [x["select_z"] for x in sh], "test", [x["test_z"] for x in sh],
              "gamma", [x["chosen"]["gamma"] for x in sh], "last10", [x["last10"] for x in sh])
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
