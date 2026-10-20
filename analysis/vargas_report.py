#!/usr/bin/env python3
"""Do the divisional charts (D2 ... D60, and D9) play a role? From lead_full.py --family dN runs and the full run.

For every chart and game (history window "all" unless --window): the family's leads together, high hits over the
whole history (7+ Magnum Life, 5+ Toto), real calendar vs 20 shifted calendars; each family parameter's excess
z; choices made before the last 10 draws; the 2026-10-18 forward draw. One summary table across charts, then the
details per chart.

python3 analysis/vargas_report.py [--window all]  -> analysis/VARGAS_REPORT.md
"""

import json
import os
import statistics as st
import sys

import numpy as np

WIN = sys.argv[sys.argv.index("--window") + 1] if "--window" in sys.argv else "all"
sys.argv = [sys.argv[0], "--family", "d2", "--shifts", "1"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lead_full as lf  # noqa: E402
import d9  # noqa: E402
import vargas  # noqa: E402

A = os.path.join(lf.common.ROOT, "analysis")
DATE = "2026-10-18"
CHARTS = [f"d{D}" for D in sorted(vargas.DS + [9])]
LABEL = {"ml8": "Magnum Life", "toto50": "Star Toto", "toto55": "Power Toto", "toto58": "Supreme Toto"}


def tag(fam):
    return ("" if WIN == "all" else f"_{WIN}") + (f"_{fam}" if fam else "")


def family(fam):
    return d9.FAMILY if fam == "d9" else vargas.family(int(fam[1:]))


def main():
    names = lf.common.ALL_PARAMS + lf.xa.extra_params()
    base = {}
    for key in LABEL:
        pa = os.path.join(A, "profit_arrays", f"leads7{tag(None)}_{key}.npz")
        if os.path.exists(pa):
            h = np.load(pa)["ST"][:, :, :, 1].sum((0, 2)).astype(float)
            base[key] = (int((h[1:] > h[0]).sum()) + 1, (h[0] - h[1:].mean()) / h[1:].std())
    allres = json.load(open(os.path.join(A, f"leads7{tag(None)}_results.json")))
    summary, detail = [], []
    for fam in CHARTS:
        p0 = os.path.join(A, f"leads7{tag(fam)}_results.json")
        if not os.path.exists(p0):
            continue
        res = json.load(open(p0))
        lf.FAMILY = fam
        sets = lf.lead_sets(names[:len(names) - len(vargas.NEW)] if fam == "d9" else names)
        fl = family(fam)
        member = np.zeros((len(sets) * lf.NP, len(fl)), bool)
        for si, s in enumerate(sets):
            for fj, p in enumerate(fl):
                if names.index(p) in s:
                    member[si * lf.NP:(si + 1) * lf.NP, fj] = True
        today = os.path.join(A, f"leads7{tag(fam)}_today_{DATE}.json")
        T = json.load(open(today)) if os.path.exists(today) else {}
        Ta = json.load(open(os.path.join(A, f"leads7_today_{DATE}.json")))
        cells, dl = [], [f"### {fam.upper()} ({len(sets):,} singles and pairs × 7 patterns = {len(sets) * lf.NP:,} leads)", "",
                         "| Game | Family rank / z (all leads) | Top parameters (z) | Top 10 by earlier profit, best format (shifted) | Combined top 10 (shifted) | Leads winning on 18 Oct (all leads) |",
                         "|---|---|---|---|---|---|"]
        for key in LABEL:
            pn = os.path.join(A, "profit_arrays", f"leads7{tag(fam)}_{key}.npz")
            if not os.path.exists(pn) or key not in res:
                cells.append("–")
                continue
            ST = np.load(pn)["ST"]
            h = ST[:, :, :, 1].sum((0, 2)).astype(float)
            rk, z = int((h[1:] > h[0]).sum()) + 1, (h[0] - h[1:].mean()) / h[1:].std()
            X = ST[:, :, :, 1].sum(2).astype(float)
            nc = X.shape[1]
            score = np.zeros((nc, len(fl)))
            for c in range(nc):
                oth = [x for x in range(nc) if x != c]
                score[c] = (member * (X[:, c] - X[:, oth].mean(1))[:, None]).sum(0) / np.maximum(member.sum(0), 1)
            pz = (score[0] - score[1:].mean(0)) / np.maximum(score[1:].std(0), 1e-9)
            top = np.argsort(-np.abs(pz))[:3]
            g = res[key]
            bf = max(g["formats"], key=lambda f: g["formats"][f]["real"]["frozen10"])
            F = g["formats"][bf]
            win = ""
            if key in T:
                nl = len(sets) * lf.NP
                wf = max(T[key]["formats"], key=lambda f: T[key]["formats"][f]["won"] / nl)
                win = (f"{100 * T[key]['formats'][wf]['won'] / nl:.1f}% ({100 * Ta[key]['formats'][wf]['won'] / 45892:.1f}%) "
                       f"in {wf}, best RM{T[key]['formats'][wf]['best']:,.0f}")
            dl.append(f"| {LABEL[key]} | {rk}/21, {z:+.1f} ({base[key][0]}/21, {base[key][1]:+.1f}) | "
                      + ", ".join(f"{fl[j]} {pz[j]:+.1f}" for j in top)
                      + f" | {F['real']['frozen10']:+,.0f} ({st.median(F['shifted']['frozen10']):+,.0f}) {bf} | "
                      f"{g['combined']['picked_profit_mean']:+,.0f} ({st.median(g['combined']['control']):+,.0f}) | {win} |")
            cells.append(f"{rk} ({z:+.1f}); max |z| {np.abs(pz).max():.1f}")
        summary.append(f"| {fam.upper()} | " + " | ".join(cells) + " |")
        detail += dl + [""]
    md = ["# Divisional charts compared", "",
          f"Generated by `analysis/vargas_report.py` (history window: {WIN}; history to 2026-10-17). Each chart's family "
          "(the sign of Moon, Sun, Mars, Mercury, Venus, Jupiter, Saturn, Rahu and Lagna in that chart, the Moon's and the "
          "Lagna's sign lords, and the count of bodies in the same sign as in D1; D9 as in d9.py) is run alone and paired "
          "with each other and with the 114 base + D9 parameters, × 7 patterns, through every analysis of lead_full.py. "
          "*Rank / z* = the family's leads together, high hits over the whole history (7+ Magnum Life, 5+ Toto), real "
          "calendar among 21; *max |z|* = the strongest single parameter of the family (with 12 parameters, about one "
          "|z| > 2 per chart and game is expected by chance).", "",
          "| Chart | " + " | ".join(LABEL.values()) + " |", "|---|" + "---|" * len(LABEL),
          "| all leads | " + " | ".join(f"{base[k][0]} ({base[k][1]:+.1f})" for k in LABEL) + " |"] + summary + ["", "## Per chart", ""] + detail
    out = os.path.join(A, f"VARGAS_REPORT{'' if WIN == 'all' else '_' + WIN.upper()}.md")
    with open(out, "w") as fh:
        fh.write("\n".join(md) + "\n")
    print("\n".join(md[:8 + len(summary) + 1]))


if __name__ == "__main__":
    main()
