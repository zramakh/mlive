#!/usr/bin/env python3
"""Within every lead (all 45,892 per game), do particular value combinations ("cells", e.g. venus_rashi = Tula ×
mercury_nakshatra = Swati) carry it, and do the good cells stay good?

Every lead (the 114 parameters alone and in pairs, × 7 patterns) is scored on each draw by how many drawn numbers
fall in its top k numbers (k = 8 Magnum Life, 6 Toto: one ticket), built from earlier draws only; chance is exactly
k × k / n per draw (hypergeometric variance). Draws are grouped by the lead's cell.

  z         a cell's hits against chance over its draws (cells with at least 8 scored draws)
  z1 / z2   the same in the first and the second half of the history (cells with 4+ draws in each)
  repeat    if some cells really predicted, cells good in the first half would stay good in the second
Real calendar and shifted calendars (the parameter values rolled against the draws). Also the cells that every lead is
in for the next draw, with their records.

python3 analysis/cells_all.py 2026-10-24 [--shifts 3]  -> analysis/CELLS_ALL.md, cells_all.json
"""

import itertools
import json
import math
import os
import shutil
import sys
from multiprocessing import Pool

import numpy as np

NEXT = [a for a in sys.argv[1:] if a[:2] == "20"][0]
NSH = int(sys.argv[sys.argv.index("--shifts") + 1]) if "--shifts" in sys.argv else 3
sys.argv = [sys.argv[0], NEXT]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import watch_predict as wp  # noqa: E402  (placeholder row for the next draw)
sys.argv = [sys.argv[0], "--shifts", "1"]
import lead_full as lf  # noqa: E402

common, ls, xa = lf.common, lf.ls, lf.xa
A = os.path.join(common.ROOT, "analysis")
PATS = lf.PATS
LABEL = {"ml8": "Magnum Life", "toto50": "Star Toto", "toto55": "Power Toto", "toto58": "Supreme Toto"}
NAMES = common.ALL_PARAMS + xa.extra_params()
SETS = [(i,) for i in range(len(NAMES))] + list(itertools.combinations(range(len(NAMES)), 2))
MIN_N = 8
G = {}


def setup(key):
    ls.init(key)
    W = ls.W
    d = W["d"] - 1                                                    # the last row is the placeholder (next draw)
    rng = np.random.default_rng(99)
    R = W["d"] - ls.HOLD
    G.update(key=key, d=d, lo=100, mid=(100 + d) // 2,
             shifts=[0] + [int(x) for x in rng.choice(np.arange(160, R - 160), NSH, replace=False)])


def chunk(task):
    """Per cell (with enough draws) of each lead: z, z1, z2, draws, and whether it is the next draw's cell."""
    sh, i0, i1 = task
    W = ls.W
    k, n, H, D = W["k"], W["n"], W["H"], W["d"]
    d, lo, mid = G["d"], G["lo"], G["mid"]
    codes = np.roll(W["codes"][:d], G["shifts"][sh], axis=0)
    codes = np.vstack([codes, W["codes"][d:]])                        # the next draw keeps its real values
    exp = k * k / n
    var = k * (k / n) * (1 - k / n) * (n - k) / (n - 1)
    Zs, P1, P2, rows, nxt_n, nxt_b = [], [], [], [], 0, 0
    for j, s in enumerate(SETS[i0:i1]):
        cid = np.zeros(D, np.int64)
        for c in s:
            cid = cid * 1000 + codes[:, c]
        order = np.argsort(cid, kind="stable")
        cs = cid[order]
        first = np.r_[0, np.flatnonzero(np.diff(cs)) + 1]
        starts = np.repeat(first, np.diff(np.r_[first, D]))
        ex = lf.window_ex(order, starts, D)
        dp = ex(np.ones((D, 1), np.float32))
        cnt = ex(H)
        e = dp * k / n
        zc = (cnt - e) / np.sqrt(e * (1 - k / n) + 1e-6)
        uq, inv = np.unique(cid[lo:d], return_inverse=True)
        h1 = np.arange(lo, d) < mid
        n1 = np.bincount(inv, weights=h1, minlength=len(uq))
        n2 = np.bincount(inv, weights=~h1, minlength=len(uq))
        nn = n1 + n2
        nxt = np.searchsorted(uq, cid[d])
        nxt = nxt if nxt < len(uq) and uq[nxt] == cid[d] else -1
        keep = nn >= MIN_N
        pos = None
        for p, pat in enumerate(PATS):
            if pat == "pos":
                if pos is None:
                    pos = ((ex(W["P"]) + ls.SMOOTH * W["pglob"]) / (dp[:, :, None] + ls.SMOOTH)).sum(1)
                S = pos
            else:
                S = {"hot": cnt - e, "cold": e - cnt, "hot+100": zc + W["hot100"], "cold+100": -zc - W["hot100"],
                     "hot/cold100": zc - W["hot100"], "cold/hot100": -zc + W["hot100"]}[pat]
            top = np.argpartition(-(S[lo:d] + W["tie"][lo:d]), k, axis=1)[:, :k]
            hits = np.take_along_axis(H[lo:d], top, 1).sum(1) - exp
            s1 = np.bincount(inv, weights=hits * h1, minlength=len(uq))
            s2 = np.bincount(inv, weights=hits * ~h1, minlength=len(uq))
            z = (s1 + s2) / np.sqrt(np.maximum(nn, 1) * var)
            z1 = np.where(n1 >= 4, s1 / np.sqrt(np.maximum(n1, 1) * var), np.nan)
            z2 = np.where(n2 >= 4, s2 / np.sqrt(np.maximum(n2, 1) * var), np.nan)
            Zs.append(z[keep].astype(np.float32))
            P1.append(z1[keep].astype(np.float32))
            P2.append(z2[keep].astype(np.float32))
            both = keep & (z1 > 2) & (z2 > 2)
            for c in np.flatnonzero(both):
                rows.append((i0 + j, p, int(uq[c]), int(nn[c]), float(z[c]), float(z1[c]), float(z2[c]), c == nxt))
            if nxt >= 0 and keep[nxt]:
                nxt_n += 1
                nxt_b += int(both[nxt])
    cat = lambda L: np.concatenate(L) if L else np.zeros(0, np.float32)  # noqa: E731
    return sh, cat(Zs), cat(P1), cat(P2), rows, nxt_n, nxt_b


def label(si, cidv):
    """Readable cell: decode the composite code back to parameter values."""
    s = SETS[si]
    vals = []
    for c in reversed(s):
        vals.append(cidv % 1000)
        cidv //= 1000
    vals = vals[::-1]
    return " × ".join(f"{NAMES[c]}={G['vals'][c].get(v, v)}" for c, v in zip(s, vals))


def main():
    wp.DATE = NEXT
    common.DATA = wp.with_placeholder()
    res = {}
    for key in LABEL:
        setup(key)
        W = ls.W
        # value labels: codes are indices into each parameter's sorted values (common.codes_for / extra codes)
        dates = W["g"]["dates"]
        V = {}
        T = common.load_params()
        X = xa.load_extra()
        for c, nm in enumerate(NAMES):
            src = T if nm in T[dates[0]] else X
            V[c] = {int(W["codes"][t, c]): src[dates[t]][nm] for t in range(len(dates))}
        G["vals"] = V
        tasks = [(sh, i, min(i + 150, len(SETS))) for sh in range(NSH + 1) for i in range(0, len(SETS), 150)]
        cal = [dict(Z=[], P1=[], P2=[], rows=[], nn=0, nb=0) for _ in range(NSH + 1)]
        with Pool(4) as pool:
            for sh, Z, P1, P2, rows, nn, nb in pool.imap_unordered(chunk, tasks):
                C = cal[sh]
                C["Z"].append(Z), C["P1"].append(P1), C["P2"].append(P2)
                C["rows"] += rows
                C["nn"] += nn
                C["nb"] += nb
        g = {"label": LABEL[key], "calendars": []}
        for sh, C in enumerate(cal):
            rows = C["rows"]
            Z = np.concatenate(C["Z"])
            P = np.stack([np.concatenate(C["P1"]), np.concatenate(C["P2"])], 1)
            ok = ~np.isnan(P).any(1)
            P = P[ok]
            good1 = P[:, 0] > 2
            summ = dict(cells=len(Z), z2=int((Z > 2).sum()), z3=int((Z > 3).sum()),
                        pers=int(ok.sum()), corr=float(np.corrcoef(P[:, 0], P[:, 1])[0, 1]),
                        good1=int(good1.sum()), good1_mean2=float(P[good1, 1].mean()),
                        good1_above=float((P[good1, 1] > 0).mean()),
                        both2=int(((P[:, 0] > 2) & (P[:, 1] > 2)).sum()),
                        both2_exp=float(good1.mean() * (P[:, 1] > 2).mean() * len(P)))
            if sh == 0:
                both = sorted([r for r in rows if r[5] > 2 and r[6] > 2], key=lambda r: -min(r[5], r[6]))[:25]
                summ["both_top"] = [dict(lead=" × ".join(NAMES[c] for c in SETS[r[0]]), pattern=PATS[r[1]],
                                         cell=label(r[0], r[2]), n=r[3], z=r[4], z1=r[5], z2=r[6], next=bool(r[7]))
                                    for r in both]
                nx = sorted([r for r in rows if r[7] and r[5] > 2 and r[6] > 2], key=lambda r: -min(r[5], r[6]))[:20]
                summ["next_top"] = [dict(lead=" × ".join(NAMES[c] for c in SETS[r[0]]), pattern=PATS[r[1]],
                                         cell=label(r[0], r[2]), n=r[3], z=r[4], z1=r[5], z2=r[6]) for r in nx]
                summ["next_both2"] = C["nb"]
                summ["next_cells"] = C["nn"]
            g["calendars"].append(summ)
        res[key] = g
        print(key, "done", flush=True)
    shutil.rmtree(common.DATA)
    json.dump(res, open(os.path.join(A, "cells_all.json"), "w"), indent=1, default=float)
    report(res)


def report(res):
    md = ["# Within every lead: do particular value combinations predict?", "",
          f"Generated by `analysis/cells_all.py`. All 45,892 leads per game (the 114 parameters alone and in pairs, × 7 "
          "patterns), each draw scored by how many drawn numbers fall in the lead's top 8 (Magnum Life) / top 6 (Toto) "
          "numbers, built from earlier draws only; chance is exact. Draws grouped by the lead's cell (its parameters' "
          f"values); cells with at least {MIN_N} draws. *z1 / z2* = first / second half of the history. Shifted = the "
          "parameter values rolled against the draws (no link to the sky).", ""]
    for key, g in res.items():
        r, sh = g["calendars"][0], g["calendars"][1:]
        f = lambda k, fmt="{:,.0f}": fmt.format(r[k]) + " (" + ", ".join(fmt.format(s[k]) for s in sh) + ")"  # noqa: E731
        md += [f"## {g['label']}", "", "| | Real calendar (shifted calendars) | Expected if no cell predicts |", "|---|---|---|",
               f"| Cells tested | {f('cells')} | |",
               f"| Cells with z above 2 | {f('z2')} | about {0.023 * r['cells']:,.0f} (2.3%) |",
               f"| Cells with z above 3 | {f('z3')} | about {0.00135 * r['cells']:,.0f} (0.13%) |",
               f"| Correlation of z first half vs second half | {f('corr', '{:+.3f}')} | 0 |",
               f"| Cells with z1 above 2: their average z2 | {f('good1_mean2', '{:+.3f}')} | 0 |",
               f"| ... share with z2 above 0 | {f('good1_above', '{:.1%}')} | about 50% |",
               f"| Cells with both z1 and z2 above 2 | {f('both2')} | {r['both2_exp']:,.0f} if the halves are independent |",
               f"| Cells active on {NEXT} with both halves above 2 | {r['next_both2']:,} of {r['next_cells']:,} | |", "",
               "Cells good in both halves (real calendar, strongest first):", "",
               "| Lead | Pattern | Cell | Draws | z | z1 / z2 | Active on " + NEXT + " |", "|---|---|---|---|---|---|---|"]
        for c in r["both_top"][:15]:
            md.append(f"| {c['lead']} | {c['pattern']} | {c['cell']} | {c['n']} | {c['z']:+.1f} | {c['z1']:+.1f} / {c['z2']:+.1f} | {'yes' if c['next'] else ''} |")
        md += ["", f"Leads whose {NEXT} cell was good in both halves:", "",
               "| Lead | Pattern | Cell | Draws | z | z1 / z2 |", "|---|---|---|---|---|---|"]
        for c in r["next_top"][:10]:
            md.append(f"| {c['lead']} | {c['pattern']} | {c['cell']} | {c['n']} | {c['z']:+.1f} | {c['z1']:+.1f} / {c['z2']:+.1f} |")
        md.append("")
    open(os.path.join(A, "CELLS_ALL.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
