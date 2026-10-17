#!/usr/bin/env python3
"""Five tickets per lead for the top leads in top_leads.json, logged before the draws.

Leads are taken in rank order; a lead whose cells split the draws exactly like
an already-chosen lead of the same game and pattern (e.g. solar term x month
pillar = solar term x month stem) gives identical tickets and is skipped.

For a draw date, with the earlier draws of the same cell:
  hot / cold  score = excess count of the number in the cell (cold: negated)
  pos         score = log P(number at sorted position p | cell), smoothed as in own_leads.py
Ticket 1 is the lead's ticket (the same as own_leads.py builds). Tickets 2-5
replace one number of ticket 1 with the next-best candidate, in order of the
smallest score loss.

python3 analysis/top_tickets.py --leads 5 --log 2026-10-18 2026-10-21
  appends variants top<rank>_t<1-5> to forward_log.csv and writes analysis/TOP_TICKETS.md
"""

import csv
import datetime as dt
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import own_leads as ol  # noqa: E402

TOP = os.path.join(common.ROOT, "analysis", "top_leads.json")
LOG = os.path.join(common.ROOT, "analysis", "forward_log.csv")
MD = os.path.join(common.ROOT, "analysis", "TOP_TICKETS.md")
GAME_KEY = {v[1]: k for k, v in common.GAMES.items()}


def same_partition(a, b):
    n = len(np.unique(a))
    return n == len(np.unique(b)) == len(np.unique(a * 100000 + b))


def tickets_for(key, s, pattern, date):
    ol.setup(key, extra_date=date)
    G = ol.G
    k, n = G["k"], G["n"]
    cell = ol.cell_of(G["codes"], s)
    same = cell[:-1] == cell[-1]
    d = int(same.sum())
    noise = (np.random.default_rng(5).random((len(cell), n)).astype(np.float32) * 1e-3)[-1]
    if pattern in ("hot", "cold"):
        exc = G["H"][same].sum(0) - d * k / n + noise
        score = exc if pattern == "hot" else -exc
        t1 = list(np.argsort(-score)[:k])
        swaps = sorted((score[i] - score[j], i, j) for i in t1 for j in range(n) if j not in t1)
    else:
        pc = (G["P"][same].sum(0) + ol.SMOOTH * G["P"].mean(0)) / (d + ol.SMOOTH)
        with np.errstate(divide="ignore"):
            s_ = np.log(pc) + noise * 1e-3      # impossible numbers at a position: -inf, never swapped in
        t1 = []
        for p in range(k):
            sc = np.where(np.isin(np.arange(n), t1), -np.inf, pc[p] + noise * 1e-3)
            t1.append(int(sc.argmax()))
        swaps = sorted((s_[p, t1[p]] - s_[p, j], t1[p], j) for p in range(k) for j in range(n) if j not in t1)
    out = [sorted(int(x) + 1 for x in t1)]
    for _, i, j in swaps:
        t = sorted(int(x) + 1 for x in (set(t1) - {i}) | {j})
        if t not in out:
            out.append(t)
        if len(out) == 5:
            break
    return out, d


def main():
    nleads = int(sys.argv[sys.argv.index("--leads") + 1]) if "--leads" in sys.argv else 5
    dates = sys.argv[sys.argv.index("--log") + 1:] if "--log" in sys.argv else []
    top = json.load(open(TOP))
    chosen = []
    for lead in top:
        key = GAME_KEY[lead["game"]]
        s = tuple(ol.PARAMS.index(p) for p in lead["set"].split(" × "))
        codes, _ = common.codes_for(common.load_game(key)["dates"], list(ol.PARAMS))
        cell = ol.cell_of(codes, s)
        if any(c["key"] == key and c["pattern"] == lead["pattern"] and same_partition(cell, c["cell"]) for c in chosen):
            print(f"skip #{lead['rank']} {lead['set']}: same cells as an earlier lead")
            continue
        chosen.append({**lead, "key": key, "s": s, "cell": cell})
        if len(chosen) == nleads:
            break
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes")
    md = ["# Tickets for the top leads", "", f"Logged {now} before the draws (also in `forward_log.csv`, variants "
          "`top<rank>_t<n>`). Ticket 1 is the lead's own ticket; 2-5 swap one number for the next-best candidate. "
          "These leads were chosen using all of their game's history so far, so only future draws test them.", ""]
    rows = []
    for c in chosen:
        md += [f"## #{c['rank']} {c['game']}: {c['set']} ({c['pattern']})", "",
               f"z early {c['early']:+.2f}, valid {c['valid']:+.2f}, test {c['test']:+.2f}.", "",
               "| Draw | Earlier draws in this cell | Ticket 1 | Ticket 2 | Ticket 3 | Ticket 4 | Ticket 5 |",
               "|---|---|---|---|---|---|---|"]
        for date in dates:
            ts, d = tickets_for(c["key"], c["s"], c["pattern"], date)
            fmt = [" ".join(f"{x:02d}" for x in t) for t in ts]
            md.append(f"| {date} | {d} | " + " | ".join(fmt) + " |")
            for j, t in enumerate(fmt, 1):
                rows.append([date, c["key"], f"top{c['rank']}_t{j}", t, now])
            print(f"#{c['rank']} {c['game']} {c['set']} {c['pattern']} {date} ({d} earlier draws): {fmt}")
        md.append("")
    if dates:
        with open(LOG, "a", newline="") as fh:
            csv.writer(fh).writerows(rows)
        with open(MD, "w") as fh:
            fh.write("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
