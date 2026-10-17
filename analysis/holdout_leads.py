#!/usr/bin/env python3
"""Fresh lead search with each game's last 5 draws held out, then a test on those 5.

For each game, the last HOLD draws are removed. On the remaining history the
own_leads.py search is rerun from scratch: 78 Vedic / Chinese parameters and
3,003 pairs, hot / cold / pos / gap tickets, walk-forward z in three periods of
the shortened history (early 25-50%, valid 50-70%, test 70-100%). No earlier
lead is reused.

Selection (on the shortened history only): each (set, pattern) is ranked by its
weakest period z; the top 20 per game are the leads.

Hold-out test: each lead's ticket for every held-out draw is built from the
pre-hold-out draws of the same cell only (never from the held-out draws), and
the numbers matched over the 5 draws are counted against 5 * k*k/n.

Chance comparisons:
  - the same selection on 4 circularly shifted parameter calendars, scored on the same 5 draws
  - every (set, pattern) on the real calendar scored on the 5 draws: what the best of ~12,000 tickets gets

python3 analysis/holdout_leads.py  (~8 min on 4 cores) -> analysis/holdout_leads_results.json, analysis/HOLDOUT_LEADS.md
"""

import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import own_leads as ol  # noqa: E402

HOLD = 5
SHIFTS = 4
TOPN = 20
OUT = os.path.join(common.ROOT, "analysis", "holdout_leads_results.json")
MD = os.path.join(common.ROOT, "analysis", "HOLDOUT_LEADS.md")
TICK = [ol.METRICS.index(t) for t in ol.TICKETS]


def calendars(key):
    g = common.load_game(key)
    codes, _ = common.codes_for(g["dates"], ol.PARAMS)
    d = len(g["dates"]) - HOLD
    rng = np.random.default_rng(31)
    shifts = [0] + [int(x) for x in rng.choice(np.arange(160, d - 160), SHIFTS, replace=False)]
    # every shift rolls the full calendar (history + held-out dates) together
    return g, codes, shifts


def prepare(key, shift):
    g, codes, shifts = calendars(key)
    ol.setup(key, drop_last=HOLD)
    rolled = np.roll(codes, shifts[shift], axis=0)
    return g, rolled


def scan(task):
    """Walk-forward z on the shortened history for a chunk of sets."""
    key, shift, lo, hi = task
    g, rolled = prepare(key, shift)
    hist = rolled[:-HOLD]
    ol.G["codes"] = hist
    return key, shift, lo, np.stack([ol.metrics(ol.cell_of(hist, s)) for s in ol.SETS[lo:hi]])


def holdout(task):
    """Numbers matched on the held-out draws for (set index, pattern) pairs."""
    key, shift, items = task
    g, rolled = prepare(key, shift)
    ol.G["codes"] = rolled
    d = len(rolled)
    actual = g["hit"][-HOLD:, 1:].astype(bool)
    out = []
    by_set = {}
    for si, t in items:
        by_set.setdefault(si, []).append(t)
    for si, pats in by_set.items():
        pr = ol.predictions(ol.cell_of(rolled, ol.SETS[si]), last=d - HOLD)
        for t in pats:
            tk = pr[t]
            per_draw = actual[np.arange(HOLD)[:, None], tk].sum(1)
            out.append((si, t, per_draw.tolist(), [sorted(int(x) + 1 for x in row) for row in tk]))
    return key, shift, out


def p_at_least(m, k, n, draws):
    """P(total matches over `draws` fair tickets >= m) (each ticket hypergeometric)."""
    one = np.array([math.comb(k, j) * math.comb(n - k, k - j) for j in range(k + 1)], float)
    one /= one.sum()
    dist = np.array([1.0])
    for _ in range(draws):
        dist = np.convolve(dist, one)
    return float(dist[m:].sum())


def main():
    games = list(common.GAMES)
    chunk = 150
    tasks = [(key, sh, lo, min(lo + chunk, len(ol.SETS))) for key in games for sh in range(SHIFTS + 1)
             for lo in range(0, len(ol.SETS), chunk)]
    Z = {key: np.zeros((SHIFTS + 1, len(ol.SETS), len(ol.METRICS), 3), np.float32) for key in games}
    with Pool(4) as pool:
        for i, (key, sh, lo, z) in enumerate(pool.imap_unordered(scan, tasks), 1):
            Z[key][sh, lo:lo + len(z)] = z
            if i % 50 == 0:
                print(f"scan {i}/{len(tasks)}", flush=True)

        # leads per game and calendar, chosen on the shortened history only
        leads = {}
        for key in games:
            for sh in range(SHIFTS + 1):
                weakest = Z[key][sh][:, TICK, :].min(2)                 # sets x 4 patterns
                order = np.argsort(-weakest, axis=None)[:TOPN]
                leads[(key, sh)] = [(int(i // len(TICK)), ol.TICKETS[i % len(TICK)],
                                     float(weakest.ravel()[i])) for i in order]
        htasks = [(key, sh, [(si, t) for si, t, _ in leads[(key, sh)]]) for key in games for sh in range(1, SHIFTS + 1)]
        # every (set, pattern) on the real calendar, in chunks
        for key in games:
            items = [(si, t) for si in range(len(ol.SETS)) for t in ol.TICKETS]
            htasks += [(key, 0, items[i:i + 600]) for i in range(0, len(items), 600)]
        H = {}
        for i, (key, sh, out) in enumerate(pool.imap_unordered(holdout, htasks), 1):
            for si, t, per_draw, tks in out:
                H[(key, sh, si, t)] = (per_draw, tks)
            if i % 20 == 0:
                print(f"hold-out {i}/{len(htasks)}", flush=True)

    res = {"hold_out_draws": HOLD, "games": {}}
    md = ["# Leads found without the last 5 draws, tested on them", "",
          "Generated by `analysis/holdout_leads.py`. For each game the last 5 draws were removed, the lead search "
          "of `own_leads.py` was rerun from scratch on the rest (78 Vedic / Chinese parameters and 3,003 pairs; hot, "
          "cold, position and gap tickets), and the 20 most consistent leads (best weakest z over three periods of "
          "that history) were chosen. Their tickets for the 5 held-out draws use pre-hold-out draws only.", ""]
    for key in games:
        g = common.load_game(key)
        k, n = g["k"], g["n"]
        e5 = HOLD * k * k / n
        held = g["dates"][-HOLD:]
        rows = []
        for rank, (si, t, w) in enumerate(leads[(key, 0)], 1):
            per_draw, tks = H[(key, 0, si, t)]
            rows.append({"rank": rank, "set": " × ".join(ol.PARAMS[j] for j in ol.SETS[si]), "pattern": t,
                         "weakest_z_before": round(w, 2),
                         **{p: round(float(Z[key][0][si, ol.METRICS.index(t), j]), 2)
                            for j, p in enumerate(("early", "valid", "test"))},
                         "holdout_matches": int(sum(per_draw)), "per_draw": per_draw, "tickets": tks})
        sel = sum(r["holdout_matches"] for r in rows)
        sh_sel = [sum(sum(H[(key, sh, si, t)][0]) for si, t, _ in leads[(key, sh)]) for sh in range(1, SHIFTS + 1)]
        allm = np.array([sum(H[(key, 0, si, t)][0]) for si in range(len(ol.SETS)) for t in ol.TICKETS])
        best = int(allm.max())
        corr_w = np.array([Z[key][0][si, ol.METRICS.index(t)].min() for si in range(len(ol.SETS)) for t in ol.TICKETS])
        game = {"label": g["label"], "held_out": held, "expected_per_lead": round(e5, 2), "leads": rows,
                "selected_total": sel, "selected_expected": round(TOPN * e5, 1),
                "shifted_selected_totals": sh_sel,
                "all_tickets": {"count": int(len(allm)), "mean": round(float(allm.mean()), 3),
                                "max": best, "n_at_max": int((allm == best).sum()),
                                "p_fair_ticket_at_least_max": round(p_at_least(best, k, n, HOLD), 5),
                                "corr_weakest_z_vs_holdout": round(float(np.corrcoef(corr_w, allm)[0, 1]), 3)}}
        res["games"][key] = game
        print(f"{g['label']}: top-{TOPN} leads matched {sel} vs {TOPN * e5:.1f} expected "
              f"(shifted-calendar leads: {sh_sel}); best of all {len(allm)} tickets {best} "
              f"(fair-ticket chance {game['all_tickets']['p_fair_ticket_at_least_max']}, {game['all_tickets']['n_at_max']} tickets)")
        md += [f"## {g['label']}", "", f"Held-out draws: {', '.join(held)}. A fair ticket matches {e5:.2f} numbers "
               f"over these 5 draws on average.", "",
               "| # | Lead (chosen without the last 5) | Pattern | Early | Valid | Test | Matches in last 5 (per draw) |",
               "|---|---|---|---|---|---|---|"]
        for r in rows:
            md.append(f"| {r['rank']} | {r['set']} | {r['pattern']} | {r['early']:+.2f} | {r['valid']:+.2f} | "
                      f"{r['test']:+.2f} | **{r['holdout_matches']}** ({' '.join(map(str, r['per_draw']))}) |")
        md += ["", f"Top {TOPN} together: {sel} matches vs {TOPN * e5:.1f} expected. The same selection on 4 shifted "
               f"calendars: {', '.join(map(str, sh_sel))}. Best of all {len(allm):,} tickets on the real calendar: "
               f"{best} matches ({game['all_tickets']['n_at_max']} tickets; a single fair ticket reaches that with "
               f"probability {game['all_tickets']['p_fair_ticket_at_least_max']:.4f}).", ""]
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
    with open(MD, "w") as fh:
        fh.write("\n".join(md) + "\n")
    print("wrote", OUT, "and", MD)


if __name__ == "__main__":
    main()
