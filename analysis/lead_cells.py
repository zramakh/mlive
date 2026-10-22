#!/usr/bin/env python3
"""Within each watchlist lead, which value combinations ("cells", e.g. mercury_nakshatra = Swati × venus_rashi = Tula)
carry its results, and do the good cells stay good?

For every watchlist entry (lead, pattern and format as watched) the numbers of every draw are built as always (from
earlier draws only), scored with the official prizes from a quarter of the way into the history, and grouped by the
lead's cell on that draw. Per cell: draws, winning draws, high hits (7+ Magnum Life, 5+ Toto), return.

  z win      the cell's winning-draw rate against the lead's own rate over all its cells (binomial)
  repeat     the persistence test: cells are ranked on the first half of the history and scored on the second half.
             If some cells were really better, cells that were good early would stay above the lead's rate later.
Also the cell the lead is in for the next draw, with its record.

python3 analysis/lead_cells.py 2026-10-24  -> analysis/LEAD_CELLS.md, lead_cells.json
"""

import csv
import json
import math
import os
import shutil
import sys

import numpy as np

NEXT = [a for a in sys.argv[1:] if a[:2] == "20"][0] if len(sys.argv) > 1 else None
sys.argv = [sys.argv[0], NEXT or "2026-01-01"]          # watch_predict reads a date
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import watch_predict as wp  # noqa: E402
sys.argv = sys.argv[:1]
import watch_rank as wr  # noqa: E402
import d9  # noqa: E402
import vargas  # noqa: E402
import chinese_div  # noqa: E402

ws, ls, common, xa = wr.ws, wr.ls, wr.common, wr.xa
A = wr.A
MIN_N = 8                                     # cells with fewer scored draws are listed but not tested
NSHUF = 10
NULL = {"z2": 0.0, "pers": []}


def values():
    V = {d: dict(r) for d, r in common.load_params().items()}
    for T in (xa.load_extra(), d9.table(), vargas.table(), chinese_div.table()):
        for d, r in T.items():
            V.setdefault(d, {}).update(r)
    return V


def main():
    V = values()
    if NEXT:
        wp.DATE = NEXT
        common.DATA = wp.with_placeholder()
    ranked = json.load(open(os.path.join(A, "watch_rank.json")))
    order = {(o["game"], o["lead"], o["pat"], o["fmt"]): i + 1 for i, o in enumerate(ranked)}
    names = common.ALL_PARAMS + xa.extra_params()
    out, pers = [], []
    for key in ws.WATCH:
        ls.init(key)
        W = ls.W
        dates = W["g"]["dates"]
        d = len(dates) - (1 if NEXT else 0)                          # scored draws exclude the placeholder
        lo = int(0.25 * (W["d"] - ls.HOLD))
        mid = (lo + d) // 2
        hi = 7 if key == "ml8" else 5
        for lead, pat, fmts in ws.WATCH[key]:
            cols = lead.split(" × ")
            rk = ws.ranking([names.index(x) for x in cols], pat)
            cell = [" × ".join(f"{p}={V[x][p]}" for p in cols) for x in dates]
            for f in fmts:
                pay, best, cost = wr.score(key, rk, f, lo)
                win = pay[lo:d] > 0
                rate = win.mean()
                C = {}
                for t in range(lo, d):
                    c = C.setdefault(cell[t], dict(n=0, w=0, hi=0, pay=0.0, n1=0, w1=0, n2=0, w2=0, hits=[]))
                    c["n"] += 1
                    c["w"] += int(pay[t] > 0)
                    c["pay"] += float(pay[t])
                    if best[t] >= hi:
                        c["hi"] += 1
                        c["hits"].append(f"{dates[t]} ({int(best[t])})")
                    h = "1" if t < mid else "2"
                    c["n" + h] += 1
                    c["w" + h] += int(pay[t] > 0)
                r1 = win[:mid - lo].mean()
                r2 = win[mid - lo:].mean()
                for c in C.values():
                    c["ret"] = c["pay"] / (c["n"] * cost)
                    c["z"] = (c["w"] - c["n"] * rate) / math.sqrt(max(c["n"] * rate * (1 - rate), 1e-9))
                    if c["n1"] >= MIN_N // 2 and c["n2"] >= MIN_N // 2:
                        z1 = (c["w1"] - c["n1"] * r1) / math.sqrt(max(c["n1"] * r1 * (1 - r1), 1e-9))
                        z2 = (c["w2"] - c["n2"] * r2) / math.sqrt(max(c["n2"] * r2 * (1 - r2), 1e-9))
                        pers.append((z1, z2))
                        c["z1"], c["z2"] = z1, z2
                tested = {k: c for k, c in C.items() if c["n"] >= MIN_N}
                # the same counts with the lead's wins shuffled over its draws within each half (no link to the cell)
                cl = np.array(cell[lo:d])
                rng = np.random.default_rng(7)
                h1 = np.arange(len(cl)) < mid - lo
                for _ in range(NSHUF):
                    ww = win.copy()
                    ww[h1] = rng.permutation(ww[h1])
                    ww[~h1] = rng.permutation(ww[~h1])
                    for k in tested:
                        m = cl == k
                        n, w = m.sum(), ww[m].sum()
                        NULL["z2"] += ((w - n * rate) / math.sqrt(max(n * rate * (1 - rate), 1e-9)) > 2) / NSHUF
                    for k, c in C.items():
                        if "z1" in c:
                            m1, m2 = (cl == k) & h1, (cl == k) & ~h1
                            z1 = (ww[m1].sum() - m1.sum() * r1) / math.sqrt(max(m1.sum() * r1 * (1 - r1), 1e-9))
                            z2 = (ww[m2].sum() - m2.sum() * r2) / math.sqrt(max(m2.sum() * r2 * (1 - r2), 1e-9))
                            NULL["pers"].append((z1, z2))
                top = sorted(tested.items(), key=lambda kv: -kv[1]["z"])[:3]
                nxt = cell[-1] if NEXT else None
                out.append(dict(rank=order.get((wr.LABEL[key], lead, pat, f), 999), game=wr.LABEL[key], lead=lead,
                                pat=pat, fmt=f, rate=float(rate), ncells=len(C), ntested=len(tested),
                                n_z2=sum(c["z"] > 2 for c in tested.values()),
                                top=[(k, c) for k, c in top], next_cell=nxt, next=C.get(nxt) if nxt else None))
        print(key, flush=True)
    if NEXT:
        shutil.rmtree(common.DATA)
    pers = np.array(pers)
    json.dump(dict(entries=out, persistence=pers.tolist()), open(os.path.join(A, "lead_cells.json"), "w"), default=float)
    report(out, pers, np.array(NULL["pers"]))


def report(out, pers, npers):
    out.sort(key=lambda o: o["rank"])
    r = float(np.corrcoef(pers[:, 0], pers[:, 1])[0, 1])
    good = pers[pers[:, 0] > 2]
    n_t = sum(o["ntested"] for o in out)
    n_z2 = sum(o["n_z2"] for o in out)
    md = ["# Within each lead: which value combinations carry it?", "",
          "Generated by `analysis/lead_cells.py`. Every watchlist entry as watched (lead, pattern, format), its draws grouped by "
          "the lead's cell (the parameters' values on the draw). *Win rate* = share of draws with any prize; *z win* = the "
          "cell's winning draws against the lead's own rate (cells with at least 8 scored draws). High hits = 7+ Magnum "
          "Life / 5+ Toto.", "",
          "## Do good cells stay good?", "",
          f"- {n_t:,} cells were tested across the {len(out)} entries; {n_z2:,} have z win above 2 "
          f"(with the lead's wins shuffled over its draws, {NULL['z2']:,.0f} on average).",
          f"- Persistence: {len(pers):,} cells with draws in both halves of the history. The correlation between a cell's "
          f"z in the first half and in the second half is **{r:+.3f}** (0 = no carry-over).",
          f"- Cells with z above 2 in the first half: {len(good):,}; their average z in the second half is "
          f"**{good[:, 1].mean():+.2f}** ({(good[:, 1] > 0).mean():.0%} above 0); with the wins shuffled "
          f"{npers[npers[:, 0] > 2][:, 1].mean():+.2f} ({(npers[npers[:, 0] > 2][:, 1] > 0).mean():.0%} above 0)."
          if len(good) else "- No cell had z above 2 in the first half.", ""]
    md += ["## Best cells of each entry, and the cell for the next draw", "",
           "| # | Game | Lead (pattern, format) | Lead win rate | Best cells (draws, wins, high hits, return, z win; z first / second half) | Next draw's cell: draws, wins, high hits, return |",
           "|---|---|---|---|---|---|"]
    for o in out:
        tops = "<br>".join(f"{k.replace(' × ', ' & ')}: {c['n']}, {c['w']}, {c['hi']}, {100 * c['ret']:.0f}%, {c['z']:+.1f}"
                           + (f"; {c['z1']:+.1f} / {c['z2']:+.1f}" if "z1" in c else "") for k, c in o["top"])
        nx = o["next"]
        nxt = (f"{o['next_cell'].replace(' × ', ' & ')}: " + (f"{nx['n']}, {nx['w']}, {nx['hi']}, {100 * nx['ret']:.0f}%" if nx else "new cell, no record")) if o["next_cell"] else ""
        md.append(f"| {o['rank']} | {o['game']} | {o['lead']} ({o['pat']}, {o['fmt']}) | {100 * o['rate']:.0f}% | {tops} | {nxt} |")
    open(os.path.join(A, "LEAD_CELLS.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md[:12]))


if __name__ == "__main__":
    main()
