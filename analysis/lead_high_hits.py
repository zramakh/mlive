#!/usr/bin/env python3
"""Magnum Life: which leads get the most 6- and 7-number hits compared with themselves on shifted calendars?

Per lead (26,224) and calendar (real + SHIFTS shifted), counts of draws whose best 8-number combination holds
6+ and 7+ winning numbers, for each format (10 tickets, System 10 x 1, System 9 x 2 overlap / disjoint), on the
earlier draws (25-100% of the history before the last 10) and on the last 10. Score = z of the lead's 6+ hits
summed over the four formats on the earlier draws against the same lead on the shifted calendars. The top 10
by score are played on the last 10 draws. Control: the same selection treating each shifted calendar as "real".

python3 analysis/lead_high_hits.py  -> analysis/lead_high_hits_results.json, analysis/LEAD_HIGH_HITS.md
"""

import itertools
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import high_hits_null as hn  # noqa: E402  (same leads, formats and shifted calendars)

ls, common, xa = hn.ls, hn.common, hn.xa
TOP = 10
OUT = os.path.join(common.ROOT, "analysis", "lead_high_hits_results.json")
MD = os.path.join(common.ROOT, "analysis", "LEAD_HIGH_HITS.md")
ARR = os.path.join(common.ROOT, "analysis", "profit_arrays")


def count(task):
    """Per lead in the chunk: hits (6+, 7+) per format on earlier draws and on the last 10."""
    sh, sets = task
    hn.setup()
    codes = np.roll(ls.W["codes"], hn.G["shifts"][sh], axis=0)
    k, n, H, Bn, R = ls.W["k"], ls.W["n"], ls.W["H"], ls.W["Bn"], ls.W["R"]
    d = len(H)
    lo = int(0.25 * R)
    out = []
    for s in sets:
        cid = np.zeros(d, np.int64)
        for j in s:
            cid = cid * 1000 + codes[:, j]
        order = np.argsort(cid, kind="stable")
        cs = cid[order]
        first = np.r_[0, np.flatnonzero(np.diff(cs)) + 1]
        starts = np.repeat(first, np.diff(np.r_[first, d]))

        def ex(X):
            xs = X[order]
            c = np.cumsum(xs, 0) - xs
            c = c - c[starts]
            o = np.empty_like(X)
            o[order] = c
            return o
        dp = ex(np.ones((d, 1), np.float32))
        cnt = ex(H)
        e = dp * k / n
        zc = (cnt - e) / np.sqrt(e * (1 - k / n) + 1e-6)
        scores = (cnt - e, e - cnt,
                  ((ex(ls.W["P"]) + ls.SMOOTH * ls.W["pglob"]) / (dp[:, :, None] + ls.SMOOTH)).sum(1),
                  zc + ls.W["hot100"])
        for S in scores:
            S = (S + ls.W["tie"])[lo:]
            top = np.argpartition(-S, hn.KT - 1, 1)[:, :hn.KT]
            top = np.take_along_axis(top, np.argsort(-np.take_along_axis(S, top, 1), 1), 1)
            war = np.take_along_axis(H[lo:], top, 1).astype(np.int8)
            warb = np.take_along_axis(Bn[lo:], top, 1).astype(np.int8)
            row = np.zeros((len(hn.FORMATS), 2, 2), np.int16)          # format, level (6+, 7+), span
            for fi, pats in enumerate(hn.G["fmts"].values()):
                best = np.zeros(len(war), np.int8)
                for q in pats:
                    m = np.minimum(war[:, q].sum(1), 8)
                    best = np.maximum(best, m)
                for li, lv in enumerate((6, 7)):
                    hit = best >= lv
                    row[fi, li, 0] = hit[:R - lo].sum()
                    row[fi, li, 1] = hit[R - lo:].sum()
            out.append(row)
    return sh, sets[0], np.array(out)


def main():
    t0 = time.time()
    names = common.ALL_PARAMS + xa.extra_params()
    sets = [()] + [(i,) for i in range(len(names))] + list(itertools.combinations(range(len(names)), 2))
    idx = {s: i for i, s in enumerate(sets)}
    tasks = [(sh, sets[i:i + 100]) for sh in range(hn.SHIFTS + 1) for i in range(0, len(sets), 100)]
    A = np.zeros((len(sets) * 4, hn.SHIFTS + 1, len(hn.FORMATS), 2, 2), np.int16)
    with Pool(4) as pool:
        for sh, s0, out in pool.imap_unordered(count, tasks):
            i0 = idx[s0] * 4
            A[i0:i0 + len(out), sh] = out
    pats = ["hot", "cold", "pos", "hot+100"]
    lab = lambda i: (" × ".join(names[j] for j in sets[i // 4]) if sets[i // 4] else "all draws (no astrology)",  # noqa: E731
                     pats[i % 4])
    six = A[:, :, :, 0, 0].sum(2).astype(float)                       # leads x calendars: 6+ hits, earlier, all formats

    def pick(c):
        """Top leads when calendar c is treated as real and the other calendars as its null."""
        others = [x for x in range(hn.SHIFTS + 1) if x != c]
        mu, sd = six[:, others].mean(1), six[:, others].std(1)
        z = (six[:, c] - mu) / np.maximum(sd, 1.0)
        return np.lexsort((-six[:, c], -z))[:TOP], z, mu

    res = {"calendars": hn.SHIFTS + 1, "control": []}
    top, z, mu = pick(0)
    fnames = list(hn.FORMATS)
    rows = []
    prof = {}
    for tag, f in (("10_bonus", "10 tickets"), ("sys10_bonus", "System 10 × 1"), ("sys9_overlap_bonus", "System 9 × 2 overlap"),
                   ("sys9_disjoint_bonus", "System 9 × 2 disjoint")):
        p = os.path.join(ARR, f"{tag}_sh0.npz")
        if os.path.exists(p):
            zz = np.load(p)
            prof[f] = {lb: float(h.sum()) for lb, h in zip(zz["labels"], zz["hold"])}
    for i in top:
        ld, pt = lab(i)
        r = {"lead": ld, "pattern": pt, "z": round(float(z[i]), 2), "six_earlier": int(six[i, 0]),
             "six_earlier_shifted_mean": round(float(mu[i]), 1),
             "seven_earlier": int(A[i, 0, :, 1, 0].sum()),
             "last10": {f: {"six": int(A[i, 0, fi, 0, 1]), "seven": int(A[i, 0, fi, 1, 1]),
                            "profit": prof.get(f, {}).get(f"{ld}|{pt}")} for fi, f in enumerate(fnames)}}
        rows.append(r)
    res["top"] = rows
    real_fwd = int(A[top, 0, :, 0, 1].sum())
    ctrl = []
    for c in range(1, hn.SHIFTS + 1):
        t, _, _ = pick(c)
        ctrl.append(int(A[t, c, :, 0, 1].sum()))
    res["forward_six_hits_top10"] = {"real": real_fwd, "shifted": ctrl,
                                     "share_ge_real": round(float(np.mean(np.array(ctrl) >= real_fwd)), 3)}
    # what an average lead gets on the last 10 (all formats, 6+)
    avg = float(A[:, 0, :, 0, 1].sum(1).mean())
    res["average_lead_last10_six"] = round(avg, 3)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
    md = ["# Magnum Life: the 10 leads with the most 6- and 7-number hits against their own shifted calendars", "",
          "Generated by `analysis/lead_high_hits.py`. *6+ hits* = draws whose best 8-number combination holds 6 or more "
          "winning numbers, summed over the four formats (10 tickets, System 10 × 1, System 9 × 2 overlap and disjoint). "
          f"Chosen on the earlier draws only: *z* = the lead's 6+ hits on the real calendar against the same lead on "
          f"{hn.SHIFTS} shifted calendars. Then played on the last 10 draws.", "",
          "| # | Lead | Pattern | Earlier 6+ hits (shifted mean) | z | Earlier 7+ hits | Last 10: 6+ / 7+ hits (10 tickets, Sys 10, Sys 9 overlap, Sys 9 disjoint) | Last 10 profit (RM): 10 tickets / Sys 10 / Sys 9 overlap / Sys 9 disjoint |",
          "|---|---|---|---|---|---|---|---|"]
    for n_, r in enumerate(rows, 1):
        hits = ", ".join(f"{v['six']}/{v['seven']}" for v in r["last10"].values())
        pr = " / ".join("—" if v["profit"] is None else f"{v['profit']:+,.0f}" for v in r["last10"].values())
        md.append(f"| {n_} | {r['lead']} | {r['pattern']} | {r['six_earlier']} ({r['six_earlier_shifted_mean']}) | {r['z']:+.2f} | "
                  f"{r['seven_earlier']} | {hits} | {pr} |")
    F = res["forward_six_hits_top10"]
    md += ["", f"Forward check: the 10 leads together got {F['real']} 6+ hits on the last 10 draws (all four formats); an average "
           f"lead gets {avg:.2f}, so 10 average leads ≈ {10 * avg:.1f}. The same selection made on each shifted calendar got "
           f"{', '.join(map(str, F['shifted']))} (share ≥ real {F['share_ge_real']:.2f}).", ""]
    with open(MD, "w") as fh:
        fh.write("\n".join(md) + "\n")
    print("\n".join(md))
    print(f"done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
