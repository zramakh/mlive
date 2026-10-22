#!/usr/bin/env python3
"""Is any lotto lead as consistent as the 4D lead Karana × Day pillar (chosen on the early years, then above chance
in 14 of 15 later years)?

Every lead (the 114 base parameters, alone and in pairs, × 7 patterns = 45,892 per game) is scored on every draw by
how many of the drawn numbers fall in its top k numbers (k = 8 Magnum Life, 6 Toto: one ticket), built from earlier
draws only. Chance is exactly k × k / n per draw. Per lead: the ratio to chance over the selection years and in
each later year.

  chosen   the top 5 leads of each pattern on the selection years (35 per game), then counted forward:
           years above chance and the forward ratio
  best     the most consistent lead over the later years in hindsight (most years above chance, then ratio)
  null     the same two numbers with the parameter values on shifted calendars (no link to the sky)

Selection years: Magnum Life and Star to 2021 (forward 2022-2026), Power and Supreme to 2016 (forward 2017-2026).

python3 analysis/consistency.py [--shifts 10]  -> analysis/CONSISTENCY.md, consistency.json
"""

import itertools
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

NSH = int(sys.argv[sys.argv.index("--shifts") + 1]) if "--shifts" in sys.argv else 10
sys.argv = [sys.argv[0], "--shifts", "1"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lead_full as lf  # noqa: E402

common, ls = lf.common, lf.ls
A = os.path.join(common.ROOT, "analysis")
PATS = lf.PATS
SPLIT = {"ml8": 2021, "toto50": 2021, "toto55": 2016, "toto58": 2016}
LABEL = {"ml8": "Magnum Life", "toto50": "Star Toto", "toto55": "Power Toto", "toto58": "Supreme Toto"}
G = {}
NAMES = common.ALL_PARAMS + lf.xa.extra_params()                 # the 114 parameters of the full runs


def setup(key):
    ls.init(key)
    W = ls.W
    d = W["d"]
    years = np.array([int(x[:4]) for x in W["g"]["dates"]])
    lo = 100                                                          # hot100 needs 100 earlier draws
    sel = (np.arange(d) >= lo) & (years <= SPLIT[key])
    fy = sorted(set(years[years > SPLIT[key]]))
    G.update(key=key, years=years, sel=sel, fy=fy, k=W["k"], n=W["n"],
             names=NAMES, sets=[()] + [(i,) for i in range(len(NAMES))] + list(itertools.combinations(range(len(NAMES)), 2)))
    rng = np.random.default_rng(99)
    R = d - ls.HOLD
    G["shifts"] = [0] + [int(x) for x in rng.choice(np.arange(160, R - 160), NSH, replace=False)]


def chunk(task):
    sh, i0, i1 = task
    W = ls.W
    k, n, H, d = W["k"], W["n"], W["H"], W["d"]
    codes = np.roll(W["codes"], G["shifts"][sh], axis=0)
    exp = k * k / n
    years, sel, fy = G["years"], G["sel"], G["fy"]
    ym = [years == y for y in fy]
    out = np.zeros((i1 - i0, len(PATS), 1 + len(fy)), np.float32)    # ratio on selection years, then per forward year
    for j, s in enumerate(G["sets"][i0:i1]):
        cid = np.zeros(d, np.int64)
        for c in s:
            cid = cid * 1000 + codes[:, c]
        order = np.argsort(cid, kind="stable")
        cs = cid[order]
        first = np.r_[0, np.flatnonzero(np.diff(cs)) + 1]
        starts = np.repeat(first, np.diff(np.r_[first, d]))
        ex = lf.window_ex(order, starts, d)
        dp = ex(np.ones((d, 1), np.float32))
        cnt = ex(H)
        e = dp * k / n
        zc = (cnt - e) / np.sqrt(e * (1 - k / n) + 1e-6)
        pos = None
        for p, pat in enumerate(PATS):
            if pat == "pos":
                if pos is None:
                    pos = ((ex(W["P"]) + ls.SMOOTH * W["pglob"]) / (dp[:, :, None] + ls.SMOOTH)).sum(1)
                S = pos
            else:
                S = {"hot": cnt - e, "cold": e - cnt, "hot+100": zc + W["hot100"], "cold+100": -zc - W["hot100"],
                     "hot/cold100": zc - W["hot100"], "cold/hot100": -zc + W["hot100"]}[pat]
            top = np.argpartition(-(S + W["tie"]), k, axis=1)[:, :k]
            hits = np.take_along_axis(H, top, 1).sum(1)
            out[j, p, 0] = hits[sel].mean() / exp
            for q, m in enumerate(ym):
                out[j, p, 1 + q] = hits[m].mean() / exp
    return sh, i0, out


def summarise(R, fy, ny):
    """R: leads x patterns x (1 + years) ratios -> chosen and best summaries."""
    chosen = []
    for p in range(R.shape[1]):
        for i in np.argsort(-R[:, p, 0])[:5]:
            f = R[i, p, 1:]
            chosen.append((int(i), p, float(R[i, p, 0]), int((f > 1).sum()), float(np.average(f, weights=ny))))
    F = R[:, :, 1:]
    above = (F > 1).sum(2)
    fr = (F * ny).sum(2) / ny.sum()
    score = above + fr / 10                                           # most years above chance, then the ratio
    i, p = np.unravel_index(np.argmax(score), score.shape)
    best = (int(i), int(p), int(above[i, p]), float(fr[i, p]))
    return chosen, best, int(above.max()), np.bincount(above.ravel(), minlength=len(fy) + 1).tolist()


def main():
    res = {}
    for key in LABEL:
        setup(key)
        fy, nset = G["fy"], len(G["sets"])
        ny = np.array([(G["years"] == y).sum() for y in fy], float)
        R = np.zeros((NSH + 1, nset, len(PATS), 1 + len(fy)), np.float32)
        tasks = [(sh, i, min(i + 200, nset)) for sh in range(NSH + 1) for i in range(0, nset, 200)]
        with Pool(4) as pool:
            for sh, i0, o in pool.imap_unordered(chunk, tasks):
                R[sh, i0:i0 + len(o)] = o
        name = lambda i: " × ".join(NAMES[c] for c in G["sets"][i]) or "no parameters"  # noqa: E731
        g = {"label": LABEL[key], "split": SPLIT[key], "forward_years": [int(y) for y in fy], "calendars": []}
        for sh in range(NSH + 1):
            chosen, best, mx, dist = summarise(R[sh], fy, ny)
            g["calendars"].append(dict(
                chosen=[dict(lead=name(i), pattern=PATS[p], sel_ratio=sr, years_above=ya, fwd_ratio=fr) for i, p, sr, ya, fr in chosen],
                best=dict(lead=name(best[0]), pattern=PATS[best[1]], years_above=best[2], fwd_ratio=best[3],
                          per_year=[float(x) for x in R[sh, best[0], best[1], 1:]]),
                max_years=mx, dist=dist))
        g["no_param"] = {PATS[p]: dict(sel_ratio=float(R[0, 0, p, 0]), years_above=int((R[0, 0, p, 1:] > 1).sum()),
                                       per_year=[float(x) for x in R[0, 0, p, 1:]]) for p in range(len(PATS))}
        res[key] = g
        print(key, "done", flush=True)
    json.dump(res, open(os.path.join(A, "consistency.json"), "w"), indent=1)
    report(res)


def report(res):
    md = ["# Is any lotto lead as consistent as Karana × Day pillar in 4D?", "",
          "Generated by `analysis/consistency.py`. Every lead (45,892 per game: the 114 base parameters alone and in pairs, × 7 "
          "patterns) scored on each draw by how many drawn numbers fall in its top 8 (Magnum Life) / top 6 (Toto) numbers, "
          "built from earlier draws only; *ratio* = hits / chance (exactly k × k / n). *Chosen* = the top 5 of each pattern "
          "on the selection years, counted forward; *best* = the most consistent lead in hindsight. *Shifted* = the same "
          "with the parameter values on shifted calendars (no link to the sky).", ""]
    for key, g in res.items():
        fy = g["forward_years"]
        real, sh = g["calendars"][0], g["calendars"][1:]
        ny = len(fy)
        ch = real["chosen"]
        md += [f"## {g['label']} (selection to {g['split']}, forward {fy[0]}-{fy[-1]}: {ny} years)", "",
               "| | Real calendar | Shifted calendars (median, range) |", "|---|---|---|",
               f"| Chosen leads: average years above chance | {np.mean([c['years_above'] for c in ch]):.2f} of {ny} | "
               f"{np.median([np.mean([c['years_above'] for c in s['chosen']]) for s in sh]):.2f} "
               f"({min(np.mean([c['years_above'] for c in s['chosen']]) for s in sh):.2f}-{max(np.mean([c['years_above'] for c in s['chosen']]) for s in sh):.2f}) |",
               f"| Chosen leads: most years above chance | {max(c['years_above'] for c in ch)} | "
               f"{np.median([max(c['years_above'] for c in s['chosen']) for s in sh]):.0f} ({min(max(c['years_above'] for c in s['chosen']) for s in sh)}-{max(max(c['years_above'] for c in s['chosen']) for s in sh)}) |",
               f"| Chosen leads: average forward ratio | ×{np.mean([c['fwd_ratio'] for c in ch]):.3f} | "
               f"×{np.median([np.mean([c['fwd_ratio'] for c in s['chosen']]) for s in sh]):.3f} |",
               f"| Leads above chance in all {ny} forward years (hindsight) | {real['dist'][-1]:,} of {sum(real['dist']):,} | "
               f"{np.median([s['dist'][-1] for s in sh]):,.0f} ({min(s['dist'][-1] for s in sh):,}-{max(s['dist'][-1] for s in sh):,}) |", "",
               "Chosen leads with the most forward years above chance:", "",
               "| Lead | Pattern | Selection ratio | Years above chance | Forward ratio |", "|---|---|---|---|---|"]
        for c in sorted(ch, key=lambda c: (-c["years_above"], -c["fwd_ratio"]))[:8]:
            md.append(f"| {c['lead']} | {c['pattern']} | ×{c['sel_ratio']:.3f} | {c['years_above']} of {ny} | ×{c['fwd_ratio']:.3f} |")
        b = real["best"]
        md += ["", f"Most consistent in hindsight: **{b['lead']} ({b['pattern']})**, {b['years_above']} of {ny} years, "
               f"forward ×{b['fwd_ratio']:.3f}; per year " + ", ".join(f"{y} ×{r:.2f}" for y, r in zip(fy, b["per_year"])) + ".",
               "", "No parameters (each pattern on the numbers' own history): " + "; ".join(
                   f"{p} {v['years_above']}/{ny}" for p, v in g["no_param"].items()) + ".", ""]
    open(os.path.join(A, "CONSISTENCY.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
