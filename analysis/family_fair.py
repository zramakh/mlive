#!/usr/bin/env python3
"""One fair test for a family of new parameters (astro_more.py), or for triples of the 114 base parameters.

Leads: each family parameter alone, paired with each other and with the 114 base parameters (or, for "triples", every
triple of base parameters), × 7 patterns. Each draw is scored by how many drawn numbers fall in a lead's top ticket
(8 Magnum Life, 6 Toto), built from earlier draws only; chance is exact. Real calendar and shifted calendars (all
parameter values rolled against the draws). Per game:

  A  whole history: leads with z above 2 / 3 against chance, the best z           (luck check: shifted calendars)
  B  fair yearly choice: before each year the top 1% of the family's leads on earlier years only, scored on that year
  C  the leads' blind records (their hits in the years they were chosen), best and count above 3

python3 analysis/family_fair.py muhurta|continuous|transit|triples [--shifts 3]
  -> analysis/FAMILY_FAIR_<FAMILY>.md, profit_arrays/ff_<family>_<game>_<calendar>.npy (resumable)
"""

import csv
import itertools
import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

FAM = sys.argv[1]
NSH = int(sys.argv[sys.argv.index("--shifts") + 1]) if "--shifts" in sys.argv else 3
sys.argv = [sys.argv[0], "--shifts", str(NSH)]               # fair_oos draws the same shifted calendars
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fair_oos as fo  # noqa: E402

ls, common, lf = fo.ls, fo.common, fo.lf
A = os.path.join(common.ROOT, "analysis")
PA = os.path.join(A, "profit_arrays")
PATS = fo.PATS
LABEL = fo.LABEL
BASE = (common.ALL_PARAMS + fo.xa.extra_params())[:114]
G = {}


def family_table(key):
    f = {"muhurta": "astro_params_muhurta.csv", "continuous": "astro_params_continuous.csv",
         "transit": f"astro_params_transit_{key}.csv"}[FAM]
    rows = {r.pop("date"): r for r in csv.DictReader(open(os.path.join(common.DATA, f)))}
    names = [p for p in next(iter(rows.values())) if len({r[p] for r in rows.values()}) > 1]
    return rows, names


def setup(key):
    fo.setup(key)
    W = ls.W
    base = W["codes"][:, :114]
    if FAM == "triples":
        names, codes = list(BASE), base
        sets = list(itertools.combinations(range(114), 3))
    else:
        T, new = family_table(key)
        cols = []
        for p in new:
            vals = sorted({r[p] for r in T.values()})
            ix = {v: i for i, v in enumerate(vals)}
            cols.append([ix[T[d][p]] for d in W["g"]["dates"]])
        codes = np.hstack([base, np.array(cols).T])
        names = list(BASE) + new
        fam = range(114, 114 + len(new))
        sets = [(i,) for i in fam] + list(itertools.combinations(fam, 2)) + [(b, i) for i in fam for b in range(114)]
    G.update(key=key, names=names, codes=codes, sets=sets)


def chunk(task):
    sh, i0, i1 = task
    codes = np.roll(G["codes"], fo.G["shifts"][sh], axis=0)
    out = np.zeros((i1 - i0, len(PATS), len(fo.G["ys"])), np.float32)
    for j, s in enumerate(G["sets"][i0:i1]):
        for p, h in enumerate(fo.scores(codes, s)):
            out[j, p] = fo.yearly(h)
    return i0, out


def calendar(key, sh):
    path = os.path.join(PA, f"ff_{FAM}_{key}_{sh}.npy")
    if os.path.exists(path):
        return np.load(path)
    n = len(G["sets"])
    Y = np.zeros((n, len(PATS), len(fo.G["ys"])), np.float32)
    step = 400 if FAM == "triples" else 150
    with Pool(4) as pool:
        for i0, o in pool.imap_unordered(chunk, [(sh, i, min(i + step, n)) for i in range(0, n, step)]):
            Y[i0:i0 + len(o)] = o
    np.save(path, Y)
    return Y


def analyse(Y, ny, e, v):
    F = Y.reshape(-1, Y.shape[-1])
    tt = list(range(2, F.shape[1]))
    tot, nd = F[:, :].sum(1), ny.sum()
    zall = (tot - nd * e) / math.sqrt(nd * v)
    Z = fo.zcum(F, ny, e, v)
    ch = np.zeros_like(F, bool)
    for t in tt:
        ch[:, t] = Z[:, t] >= np.quantile(Z[:, t], 1 - fo.TOP)
    hits, draws = (F * ch).sum(), (ch * ny).sum()
    hh, nn = (F * ch).sum(1), (ch * ny).sum(1)
    m = nn > 0
    bz = np.full(len(F), np.nan)
    bz[m] = (hh[m] - nn[m] * e) / np.sqrt(nn[m] * v)
    return dict(leads=int(len(F)), all_ratio=float(tot.sum() / (len(F) * nd * e)), z2=int((zall > 2).sum()),
                z3=int((zall > 3).sum()), zmax=float(zall.max()), chosen_ratio=float(hits / (draws * e)),
                chosen_z=float((hits - draws * e) / math.sqrt(draws * v)), blind_leads=int(m.sum()),
                blind_z3=int((bz[m] >= 3).sum()), blind_max=float(np.nanmax(bz))), zall, bz


def main():
    res = {}
    for key in LABEL:
        setup(key)
        W = ls.W
        k, n = W["k"], W["n"]
        e, v = k * k / n, k * (k / n) * (1 - k / n) * (n - k) / (n - 1)
        ys, years, lo = fo.G["ys"], fo.G["years"], fo.G["lo"]
        ny = np.array([(years[lo:] == y).sum() for y in ys], float)
        cals = []
        for sh in range(NSH + 1):
            Y = calendar(key, sh)
            s, zall, bz = analyse(Y, ny, e, v)
            if sh == 0:
                lab = lambda i: (" × ".join(G["names"][c] for c in G["sets"][i // len(PATS)]), PATS[i % len(PATS)])  # noqa: E731
                s["top_all"] = [dict(zip(("lead", "pattern"), lab(i)), z=float(zall[i])) for i in np.argsort(-zall)[:8]]
                order = np.argsort(-np.nan_to_num(bz, nan=-99))[:8]
                s["top_blind"] = [dict(zip(("lead", "pattern"), lab(i)), z=float(bz[i])) for i in order]
            cals.append(s)
            print(key, sh, {x: s[x] for x in ("all_ratio", "z2", "zmax", "chosen_ratio", "chosen_z", "blind_max")}, flush=True)
        res[key] = dict(label=LABEL[key], calendars=cals, sets=len(G["sets"]))
    json.dump(res, open(os.path.join(A, f"family_fair_{FAM}.json"), "w"), indent=1)
    report(res)


def report(res):
    md = [f"# Fair test: {FAM}", "",
          f"Generated by `analysis/family_fair.py {FAM}` (see the script for the leads). Real calendar first, shifted calendars "
          "in brackets. Hits = drawn numbers in a lead's top ticket (8 Magnum Life, 6 Toto) against exact chance.", "",
          "| Game | Leads | All leads: ratio | Leads z > 2 | Best z | Chosen before each year: next-year ratio (z) | Best blind z | Blind z ≥ 3 |",
          "|---|---|---|---|---|---|---|---|"]
    for key, g in res.items():
        r, sh = g["calendars"][0], g["calendars"][1:]
        br = lambda f, x: f.format(r[x]) + " (" + ", ".join(f.format(s[x]) for s in sh) + ")"  # noqa: E731
        md.append(f"| {g['label']} | {r['leads']:,} | {br('×{:.4f}', 'all_ratio')} | {br('{:,}', 'z2')} | {br('{:+.1f}', 'zmax')} | "
                  f"×{r['chosen_ratio']:.4f} ({r['chosen_z']:+.1f}) [" + ", ".join(f"×{s['chosen_ratio']:.4f}" for s in sh) + "] | "
                  f"{br('{:+.1f}', 'blind_max')} | {br('{:,}', 'blind_z3')} |")
    for key, g in res.items():
        r = g["calendars"][0]
        md += ["", f"## {g['label']}: best leads (real calendar)", "", "| Whole history | z | Blind (chosen beforehand) | z |", "|---|---|---|---|"]
        for a, b in zip(r["top_all"], r["top_blind"]):
            md.append(f"| {a['lead']} ({a['pattern']}) | {a['z']:+.1f} | {b['lead']} ({b['pattern']}) | {b['z']:+.1f} |")
    open(os.path.join(A, f"FAMILY_FAIR_{FAM.upper()}.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md[:10]))


if __name__ == "__main__":
    main()
