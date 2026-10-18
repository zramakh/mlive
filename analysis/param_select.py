#!/usr/bin/env python3
"""Do fewer parameters work better? Parameter selection for the vector forecasters
of analogy_model.py.

Forecasters (PPMI + SVD vectors, 30 dimensions, built only from the chosen parameters)
  direct    q = conditions(today) W   (learned condition -> numbers map)
  last      q = numbers(previous draw) - conditions(previous draw) + conditions(today)
Selection, on validation draws only (AUC: chance that a drawn number ranks above an undrawn one)
  top_m     score every parameter alone; keep the m best, m in {1, 3, 5, 10, 20} chosen on validation
  greedy    forward selection: add the parameter that raises validation AUC most; stop when
            nothing helps or at 10 parameters
Protocol per game (last HOLD draws aside, R = the rest): vectors on R[0:60%], selection on
R[60:80%]; test on R[80:100%] with vectors rebuilt on R[0:80%]; last HOLD draws with vectors on R.
The whole selection is repeated on SHIFTS circularly shifted parameter calendars.

python3 analysis/param_select.py  (~10 min on 4 cores) -> analysis/param_select_results.json
"""

import json
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analogy_model as am  # noqa: E402
import common  # noqa: E402
import embed_model as em  # noqa: E402

HOLD = 10
SHIFTS = 4
DIM = 30
TOP_M = [1, 3, 5, 10, 20]
MAX_GREEDY = 10
FORECASTERS = {"direct": ("direct", 1.0), "last": ("last", 1.0)}
OUT = os.path.join(common.ROOT, "analysis", "param_select_results.json")
NAMES = common.ALL_PARAMS


def subset(Xfull, cols):
    sub = Xfull[:, cols]
    uniq, inv = np.unique(sub, return_inverse=True)
    return inv.reshape(sub.shape), len(uniq)


def evaluate(Xfull, Y, cols, upto, rows, method, lam, k):
    X, V = subset(Xfull, list(cols))
    d = min(DIM, V + Y.shape[1] - 1)
    sp = am.space(X, Y, V, upto, [d])[d]
    st, top = am.scores(am.queries(method, lam, sp, X, Y, rows, None), Y[rows], k)
    return st, top


def run(task):
    key, shift, fname = task
    method, lam = FORECASTERS[fname]
    g, Xfull, _, Y = em.tokens(key, shift)
    k = g["k"]
    R = len(Y) - HOLD
    a, b = int(R * 0.6), int(R * 0.8)
    valid, test, hold = np.arange(a, b), np.arange(b, R), np.arange(R, len(Y))
    vauc = lambda cols: evaluate(Xfull, Y, cols, a, valid, method, lam, k)[0]["auc"]  # noqa: E731
    single = np.array([vauc([j]) for j in range(len(NAMES))])
    order = np.argsort(-single)
    res = {"single_valid_auc": {NAMES[j]: round(float(single[j]), 4) for j in order[:15]}}
    # top-m
    m_auc = {m: vauc(order[:m]) for m in TOP_M}
    m_best = max(m_auc, key=m_auc.get)
    chosen = {"top_m": [int(j) for j in order[:m_best]]}
    res["top_m"] = {"m": m_best, "valid_auc_by_m": {str(m): round(v, 4) for m, v in m_auc.items()}}
    # greedy forward
    sel, best = [], 0.5
    while len(sel) < MAX_GREEDY:
        cand = [(vauc(sel + [j]), j) for j in range(len(NAMES)) if j not in sel]
        auc, j = max(cand)
        if auc <= best:
            break
        sel.append(j)
        best = auc
    chosen["greedy"] = sel
    res["greedy"] = {"valid_auc": round(best, 4)}
    for name, cols in chosen.items():
        if not cols:
            res[name].update(params=[], test=None, hold_out=None)
            continue
        tst, _ = evaluate(Xfull, Y, cols, b, test, method, lam, k)
        hst, top = evaluate(Xfull, Y, cols, R, hold, method, lam, k)
        res[name].update(params=[NAMES[j] for j in cols], test=tst, hold_out=hst,
                         hold_out_tickets=[sorted(int(x) + 1 for x in t) for t in top])
    # reference: all 83 parameters, same forecaster and dimensions
    allc = list(range(len(NAMES)))
    res["all_params"] = {"valid_auc": round(vauc(allc), 4),
                         "test": evaluate(Xfull, Y, allc, b, test, method, lam, k)[0]}
    return key, shift, fname, res


def main():
    games = list(common.GAMES)
    rng = np.random.default_rng(14)
    tasks = []
    for key in games:
        d = len(common.load_game(key)["dates"])
        for s in [0] + [int(x) for x in rng.choice(np.arange(160, d - 160), SHIFTS, replace=False)]:
            tasks += [(key, s, f) for f in FORECASTERS]
    with Pool(4) as pool:
        out = list(pool.imap_unordered(run, tasks))
    res = {"games": {}}
    for key in games:
        game = {"label": common.GAMES[key][1]}
        for f in FORECASTERS:
            rows = {s: r for k2, s, f2, r in out if k2 == key and f2 == f}
            real = rows[0]
            sh = [rows[s] for s in rows if s]
            game[f] = {"real": real, "shifted": {
                sel: {"test_z": [r[sel]["test"]["z"] if r[sel]["test"] else None for r in sh],
                      "test_auc": [r[sel]["test"]["auc"] if r[sel]["test"] else None for r in sh],
                      "valid_auc": [r[sel].get("valid_auc", r[sel].get("valid_auc_by_m", {}).get(str(r[sel].get("m"))))
                                    for r in sh],
                      "hold_matches": [r[sel]["hold_out"]["matches"] if r[sel]["hold_out"] else None for r in sh],
                      "params": [r[sel]["params"] for r in sh]} for sel in ("top_m", "greedy")}}
            print(f"{game['label']} / {f}: all 83 params test z {real['all_params']['test']['z']:+.2f} "
                  f"AUC {real['all_params']['test']['auc']:.4f}")
            for sel in ("top_m", "greedy"):
                r = real[sel]
                if r["test"]:
                    print(f"   {sel:<7} {len(r['params'])} params {r['params'][:6]}{'...' if len(r['params']) > 6 else ''}"
                          f" | test {r['test']['matches']}/{r['test']['expected']} z {r['test']['z']:+.2f} AUC {r['test']['auc']:.4f}"
                          f" | last {HOLD}: {r['hold_out']['matches']}/{r['hold_out']['expected']}"
                          f" | shifted z {game[f]['shifted'][sel]['test_z']} AUC {game[f]['shifted'][sel]['test_auc']}")
                else:
                    print(f"   {sel:<7} no parameter improved validation AUC")
        res["games"][key] = game
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
