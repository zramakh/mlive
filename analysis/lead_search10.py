#!/usr/bin/env python3
"""Lead search aimed at more numbers in one ticket, with 10 tickets per draw.

Parameter sets: all 114 astrological parameters (the 83 of common.py + the 31 of
extra_astro.py) and all their pairs. A draw's cell = its value(s) of the set.
Patterns (every number scored from earlier draws of the same cell, walk-forward):
  hot      cell count minus expected
  cold     the reverse
  pos      chance of being drawn at any sorted position in the cell (smoothed)
  hot+100  standardised cell count + standardised count over the last 100 draws
Tickets: the numbers ranked by score; ticket 1 = ranks 1..k, tickets 2-10 = a fixed set
of one- and two-number swaps with ranks k+1..k+3 (the same structure for every lead).
Objective: matches of the best of the 10 tickets per draw (and tickets with 3+ matches).

Selection without the last HOLD draws: history R = all but the last HOLD, periods
early 25-50%, valid 50-70%, late 70-100% of R; z of the best-ticket matches per period
against fair draws (simulated for this ticket structure); leads ranked by the weakest
of the three. The top TOP per game are then scored on the last HOLD draws.
Control: the same search on SHIFTS circularly shifted parameter calendars.

python3 analysis/lead_search10.py  (~15 min on 4 cores) -> analysis/lead_search10_results.json, analysis/LEAD_SEARCH10.md
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
import extra_astro as xa  # noqa: E402

HOLD = 10
SHIFTS = 4
TOP = 10
SMOOTH = 5.0
PATTERNS = ["hot", "cold", "pos", "hot+100"]
SIMS = 200000
OUT = os.path.join(common.ROOT, "analysis", "lead_search10_results.json")
MD = os.path.join(common.ROOT, "analysis", "LEAD_SEARCH10.md")
W = {}


def swap_patterns(k):
    """10 tickets as lists of rank positions (0-based)."""
    base = list(range(k))
    a, b, c = k, k + 1, k + 2
    rep = lambda drop, add: sorted(set(base) - set(drop) | set(add))  # noqa: E731
    return [base, rep([k - 1], [a]), rep([k - 1], [b]), rep([k - 2], [a]), rep([k - 1, k - 2], [a, b]),
            rep([k - 1], [c]), rep([k - 2], [b]), rep([k - 3], [a]), rep([k - 1, k - 2], [a, c]), rep([k - 2], [c])]


def chance_best(k, n):
    """Per-draw distribution of best-of-10 matches and of 3+ tickets for this ticket structure on fair draws."""
    rng = np.random.default_rng(0)
    pats = swap_patterns(k)
    war = np.zeros((SIMS, k + 3), bool)
    pos = np.argsort(rng.random((SIMS, n)), 1)[:, :k]                # winning ranks
    for j in range(k + 3):
        war[:, j] = (pos == j).any(1)
    m = np.stack([war[:, p].sum(1) for p in pats], 1)
    best = m.max(1)
    return best.mean(), best.std(), (m >= 3).sum(1).mean(), (m >= 3).sum(1).std(), np.bincount(best, minlength=k + 1) / SIMS


def init(key):
    g = common.load_game(key)
    k, n = g["k"], g["n"]
    H = g["hit"][:, 1:].astype(np.float32)
    d = len(H)
    srt = np.sort(g["nums"], 1)
    P = np.zeros((d, k, n), np.float32)
    P[np.arange(d)[:, None], np.arange(k)[None, :], srt - 1] = 1
    t = np.maximum(np.arange(d), 1)[:, None, None]
    pglob = ((np.cumsum(P, 0) - P) / t).astype(np.float32)
    cum = np.vstack([np.zeros((1, n)), np.cumsum(H, 0)])
    e100 = 100 * k / n
    hot100 = np.zeros((d, n), np.float32)
    hot100[100:] = (cum[100:d] - cum[:d - 100] - e100) / math.sqrt(e100 * (1 - k / n))
    codes = xa.codes_all(g["dates"])
    R = d - HOLD
    eb, sb, e3, s3, _ = chance_best(k, n)
    rng = np.random.default_rng(23)
    shifts = [0] + [int(x) for x in rng.choice(np.arange(160, R - 160), SHIFTS, replace=False)]
    W.clear()
    W.update(key=key, g=g, k=k, n=n, H=H, P=P, pglob=pglob, hot100=hot100, codes=codes, d=d, R=R,
             pats=swap_patterns(k), eb=eb, sb=sb, e3=e3, s3=s3, shifts=shifts,
             periods=[(int(0.25 * R), int(0.5 * R)), (int(0.5 * R), int(0.7 * R)), (int(0.7 * R), R), (R, d)],
             tie=np.random.default_rng(3).random((d, n)).astype(np.float32) * 1e-4)


def evaluate(cid):
    """For each pattern: per period (sum of best-of-10, sum of 3+ tickets) and hold-out details."""
    k, n, H = W["k"], W["n"], W["H"]
    order = np.argsort(cid, kind="stable")
    cs = cid[order]
    first = np.r_[0, np.flatnonzero(np.diff(cs)) + 1]
    starts = np.repeat(first, np.diff(np.r_[first, len(cid)]))

    def ex(X):
        xs = X[order]
        c = np.cumsum(xs, 0) - xs
        c = c - c[starts]
        o = np.empty_like(X)
        o[order] = c
        return o
    dp = ex(np.ones((len(cid), 1), np.float32))
    cnt = ex(H)
    e = dp * k / n
    zc = (cnt - e) / np.sqrt(e * (1 - k / n) + 1e-6)
    scores = {"hot": cnt - e, "cold": e - cnt,
              "pos": ((ex(W["P"]) + SMOOTH * W["pglob"]) / (dp[:, :, None] + SMOOTH)).sum(1),
              "hot+100": zc + W["hot100"]}
    out = {}
    for p, S in scores.items():
        S = S + W["tie"]
        top = np.argpartition(-S, k + 2, 1)[:, :k + 3]
        top = np.take_along_axis(top, np.argsort(-np.take_along_axis(S, top, 1), 1), 1)
        war = np.take_along_axis(H, top, 1)                          # draws x (k+3): rank j drawn?
        m = np.stack([war[:, q].sum(1) for q in W["pats"]], 1)
        best = m.max(1)
        ge3 = (m >= 3).sum(1)
        per = [(float(best[a:b].sum()), float(ge3[a:b].sum()), b - a) for a, b in W["periods"]]
        out[p] = {"per": per, "hold_best": best[W["R"]:].tolist(), "hold_m": m[W["R"]:].tolist(),
                  "hold_tickets": [[sorted(int(x) + 1 for x in top[r, q]) for q in W["pats"]] for r in range(W["R"], W["d"])]}
    return out


def zper(s, cnt, mean, sd):
    return (s - cnt * mean) / (sd * math.sqrt(cnt)) if cnt else 0.0


def run(task):
    key, sh, sets = task
    if W.get("key") != key:
        init(key)
    codes = np.roll(W["codes"], W["shifts"][sh], axis=0)
    res = []
    for s in sets:
        cid = codes[:, s[0]].astype(np.int64)
        for j in s[1:]:
            cid = cid * 1000 + codes[:, j]
        ev = evaluate(cid)
        for p, v in ev.items():
            z = [zper(b, c, W["eb"], W["sb"]) for b, _, c in v["per"][:3]]
            res.append((s, p, min(z), z, v))
    # keep only the best few per task to save memory (selection is on the weakest z)
    res.sort(key=lambda r: -r[2])
    return key, sh, [(s, p, w, z, {kk: vv for kk, vv in v.items()}) for s, p, w, z, v in res[:TOP]], \
        [(s, p, w) for s, p, w, z, v in res]


def main():
    names = common.ALL_PARAMS + xa.extra_params()
    sets = [(i,) for i in range(len(names))] + list(itertools.combinations(range(len(names)), 2))
    chunk = 200
    tasks = [(key, sh, sets[i:i + chunk]) for key in common.GAMES for sh in range(SHIFTS + 1)
             for i in range(0, len(sets), chunk)]
    best, allw = {}, {}
    with Pool(4) as pool:
        for i, (key, sh, top, w) in enumerate(pool.imap_unordered(run, tasks), 1):
            best.setdefault((key, sh), []).extend(top)
            allw.setdefault((key, sh), []).extend(x[2] for x in w)
            if i % 50 == 0:
                print(f"{i}/{len(tasks)}", flush=True)
    res = {"sets": len(sets), "patterns": PATTERNS, "games": {}}
    md = ["# Lead search for more numbers in one ticket (10 tickets per draw)", "",
          "Generated by `analysis/lead_search10.py`. 114 astrological parameters and all their pairs × 4 patterns "
          f"({len(sets) * 4:,} leads per game). Leads ranked, without the last {HOLD} draws, by the weakest of three "
          "period z-scores of the best-ticket matches; the top 10 are scored on the last 10 draws. *Chance* for a lead = "
          "share of fair 10-draw sets in which the best ticket per draw sums to at least as much. Control: the same search "
          f"on {SHIFTS} shifted calendars.", ""]
    for key in common.GAMES:
        g = common.load_game(key)
        k, n = g["k"], g["n"]
        eb, sb, e3, s3, dist = chance_best(k, n)
        # distribution of the sum of best-of-10 over HOLD draws
        tot = np.array([1.0])
        for _ in range(HOLD):
            tot = np.convolve(tot, dist)
        p_ge = lambda x: float(tot[int(x):].sum())  # noqa: E731
        game = {"label": g["label"], "expected_best_per_draw": round(float(eb), 3), "expected_3plus_per_draw": round(float(e3), 3)}
        for sh in range(SHIFTS + 1):
            top = sorted(best[(key, sh)], key=lambda r: -r[2])[:TOP]
            rows = []
            for s, p, w, z, v in top:
                hb = sum(v["hold_best"])
                rows.append({"set": " × ".join(names[j] for j in s), "pattern": p, "weakest_z": round(w, 2),
                             "z_periods": [round(x, 2) for x in z], "hold_best_sum": int(hb), "hold_expected": round(HOLD * eb, 2),
                             "hold_chance": round(p_ge(hb), 4), "hold_max": int(max(max(r) for r in v["hold_m"])),
                             "hold_3plus": int(sum(sum(1 for x in r if x >= 3) for r in v["hold_m"])),
                             "hold_3plus_expected": round(HOLD * e3, 2), "hold_tickets": v["hold_tickets"]})
            ws = np.array(allw[(key, sh)])
            game["real" if sh == 0 else f"shift{sh}"] = {"top": rows, "best_weakest_z": round(float(ws.max()), 2),
                                                         "n_weakest_z_gt_1": int((ws > 1).sum())}
        real = game["real"]
        sh = [game[f"shift{i}"] for i in range(1, SHIFTS + 1)]
        game["summary"] = {
            "real_top10_hold_best": sum(r["hold_best_sum"] for r in real["top"]),
            "shifted_top10_hold_best": [sum(r["hold_best_sum"] for r in s["top"]) for s in sh],
            "expected_top10_hold_best": round(TOP * HOLD * eb, 1),
            "real_best_weakest_z": real["best_weakest_z"], "shifted_best_weakest_z": [s["best_weakest_z"] for s in sh],
            "real_n_consistent": real["n_weakest_z_gt_1"], "shifted_n_consistent": [s["n_weakest_z_gt_1"] for s in sh]}
        res["games"][key] = game
        S = game["summary"]
        print(f"{g['label']}: top-10 leads' best-ticket sum on last {HOLD}: {S['real_top10_hold_best']} vs {S['expected_top10_hold_best']} "
              f"(shifted {S['shifted_top10_hold_best']}); best weakest z {S['real_best_weakest_z']} (shifted {S['shifted_best_weakest_z']}); "
              f"leads with z>1 in all periods {S['real_n_consistent']} (shifted {S['shifted_n_consistent']})")
        for r in real["top"][:5]:
            print(f"   {r['set']:<45} {r['pattern']:<7} weakest {r['weakest_z']:+.2f} | last10 best {r['hold_best_sum']}/{r['hold_expected']} "
                  f"chance {r['hold_chance']:.3f} max {r['hold_max']} 3+ {r['hold_3plus']}/{r['hold_3plus_expected']}")
        md += [f"## {g['label']}", "",
               f"A fair draw gives this ticket structure a best ticket of {eb:.2f} matches on average ({HOLD * eb:.1f} over {HOLD} draws) "
               f"and {e3:.2f} tickets with 3+ per draw.", "",
               f"Top 10 together on the last {HOLD} draws: best-ticket sum {S['real_top10_hold_best']} vs {S['expected_top10_hold_best']} expected; "
               f"the same selection on shifted calendars: {', '.join(map(str, S['shifted_top10_hold_best']))}. Best weakest-period z "
               f"{S['real_best_weakest_z']} (shifted {', '.join(map(str, S['shifted_best_weakest_z']))}); leads with z > 1 in all three "
               f"periods {S['real_n_consistent']} (shifted {', '.join(map(str, S['shifted_n_consistent']))}).", "",
               "| # | Lead | Pattern | z early / valid / late | Last 10: best-ticket sum (expected) | Chance | Max in one ticket | 3+ tickets (expected) |",
               "|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(real["top"], 1):
            md.append(f"| {i} | {r['set']} | {r['pattern']} | {' / '.join(f'{x:+.2f}' for x in r['z_periods'])} | "
                      f"{r['hold_best_sum']} ({r['hold_expected']}) | {100 * r['hold_chance']:.1f}% | {r['hold_max']} | "
                      f"{r['hold_3plus']} ({r['hold_3plus_expected']}) |")
        md.append("")
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1, default=float)
    with open(MD, "w") as fh:
        fh.write("\n".join(md) + "\n")
    print("wrote", OUT, "and", MD)


if __name__ == "__main__":
    main()
