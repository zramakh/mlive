#!/usr/bin/env python3
"""Lead search of our own: which numbers, positions and gaps go with which
Vedic / Chinese conditions?

For every game and every parameter set (78 single Vedic / Chinese parameters
and their 3,003 pairs), a draw's "cell" is its value of that set, e.g.
"Moon in Rohini" or "Moon in Rohini & Wu day". At every draw, using only the
earlier draws in the same cell (walk-forward), four tickets are built and
two predictions are made:

  hot        the k numbers drawn most often in the cell (relative to expected)
  cold       the k numbers drawn least often in the cell
  pos        per sorted position (smallest .. largest), the number most often
             seen at that position in the cell; duplicates skipped
  gap        the cell's most common smallest number, then its most common
             difference to the next number, and so on (n2-n1, n3-n2, ...);
             numbers past the top are replaced by the cell's hot numbers
  pos_hit    exact hits of the per-position prediction, against the same
             prediction made from all earlier draws regardless of cell
  gap_hit    exact hits of the per-position gap prediction, same baseline

Ticket metrics are z of numbers matched against k*k/n per ticket (the same for
every ticket under fair draws). Hit metrics are paired z of (cell
prediction - unconditioned prediction) hits. Positional and gap
distributions are smoothed towards the unconditioned ones (5 pseudo-draws).

Periods (by draw order, as in common.py): early = 25-50%, valid = 50-70%,
test = 70-100%. Leads are chosen on early + valid only, then read off the
test. The whole search is repeated on circularly shifted parameter calendars,
to show what the best lead and its test score look like when no real link
exists.

Selection rules (fixed before the test was looked at):
  best_valid   highest valid z
  stable       highest min(early z, valid z)
per game, metric and family (vedic, chinese, vedic x vedic, chinese x chinese, vedic x chinese,
and all), and "my lead" per game = the stable rule over all four ticket metrics.

python3 analysis/own_leads.py                    (~15 min on 4 cores) -> analysis/own_leads_results.json
python3 analysis/own_leads.py --log 2026-10-18 2026-10-21   append each game's lead tickets to forward_log.csv
"""

import csv
import datetime as dt
import itertools
import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

PARAMS = common.VEDIC + common.CHINESE
NV = len(common.VEDIC)
SETS = [(i,) for i in range(len(PARAMS))] + list(itertools.combinations(range(len(PARAMS)), 2))
METRICS = ["hot", "cold", "pos", "gap", "pos_hit", "gap_hit"]
TICKETS = METRICS[:4]
PERIODS = {"early": (0.25, 0.5), "valid": (0.5, 0.7), "test": (0.7, 1.0)}
SMOOTH = 5.0
SHIFTS = 8
MIN_SHIFT = 160
OUT = os.path.join(common.ROOT, "analysis", "own_leads_results.json")
LOG = os.path.join(common.ROOT, "analysis", "forward_log.csv")
REF_4D = ("mercury_nakshatra", "venus_rashi")

G = {}


def family(s):
    kinds = ["vedic" if j < NV else "chinese" for j in s]
    return kinds[0] if len(s) == 1 else " x ".join(sorted(kinds, reverse=True))


def setup(key, extra_date=None):
    g = common.load_game(key)
    dates = g["dates"] + ([extra_date] if extra_date else [])
    codes, values = common.codes_for(dates, PARAMS)
    d, k, n = len(g["dates"]), g["k"], g["n"]
    srt = np.sort(g["nums"], 1)
    H = g["hit"][:, 1:].astype(np.float32)
    P = np.zeros((d, k, n), np.float32)
    P[np.arange(d)[:, None], np.arange(k)[None, :], srt - 1] = 1
    gaps = np.diff(srt, axis=1)                                     # 1 .. n-k+1
    ng = n - k + 2
    GP = np.zeros((d, k - 1, ng), np.float32)
    GP[np.arange(d)[:, None], np.arange(k - 1)[None, :], gaps] = 1
    t = np.maximum(np.arange(d), 1)[:, None, None]
    pglob = (np.cumsum(P, 0) - P) / t                               # unconditioned, earlier draws only
    gglob = (np.cumsum(GP, 0) - GP) / t
    rng = np.random.default_rng(11)
    shifts = rng.choice(np.arange(MIN_SHIFT, d - MIN_SHIFT), SHIFTS, replace=False)
    G.clear()
    G.update(key=key, g=g, codes=codes, values=values, d=d, k=k, n=n, srt=srt, gaps=gaps, H=H, P=P, GP=GP,
             pglob=pglob, gglob=gglob, base_pos=pglob.argmax(2), base_gap=gglob.argmax(2),
             noise=rng.random((d, n)).astype(np.float32) * 1e-3,
             shifts=[0] + [int(s) for s in shifts],
             e=k * k / n, v=k * k / n * (1 - k / n) * (n - k) / (n - 1),
             period_rows={p: (int(a * d), int(b * d)) for p, (a, b) in PERIODS.items()})


def predictions(cid, last=None):
    """Tickets (rows x k numbers, 0-based) and positional / gap predictions for every row.
    `last`: only rows >= last are needed (for live tickets)."""
    k, n, H = G["k"], G["n"], G["H"]
    order = np.argsort(cid, kind="stable")
    cs = cid[order]
    first = np.r_[0, np.flatnonzero(np.diff(cs)) + 1]
    starts = np.repeat(first, np.diff(np.r_[first, len(cid)]))     # group start of each sorted row

    def ex(X):
        """Per row: sum of X over earlier rows in the same cell."""
        xs = X[order]
        c = np.cumsum(xs, 0) - xs
        c = c - c[starts]
        out = np.empty_like(X)
        out[order] = c
        return out

    d = len(cid)
    Hx = np.vstack([H, np.zeros((d - len(H), n), np.float32)]) if d > len(H) else H
    Px = np.concatenate([G["P"], np.zeros((d - len(H),) + G["P"].shape[1:], np.float32)]) if d > len(H) else G["P"]
    Gx = np.concatenate([G["GP"], np.zeros((d - len(H),) + G["GP"].shape[1:], np.float32)]) if d > len(H) else G["GP"]
    dprev = ex(np.ones((d, 1), np.float32))
    rows = slice(last, None) if last is not None else slice(None)
    hc = ex(Hx)[rows]
    dp = dprev[rows]
    noise = G["noise"] if d == len(G["noise"]) else np.random.default_rng(5).random((d, n)).astype(np.float32) * 1e-3
    exc = hc - dp * (k / n) + noise[rows]
    hot = np.argpartition(-exc, k - 1, 1)[:, :k]
    cold = np.argpartition(exc, k - 1, 1)[:, :k]
    pg, gg = G["pglob"], G["gglob"]
    if d > len(H):                                                  # live: unconditioned = all draws
        pg = np.concatenate([pg, np.repeat(G["P"].mean(0, keepdims=True), d - len(H), 0)])
        gg = np.concatenate([gg, np.repeat(G["GP"].mean(0, keepdims=True), d - len(H), 0)])
    pc = (ex(Px)[rows] + SMOOTH * pg[rows]) / (dp[:, :, None] + SMOOTH)
    gc = (ex(Gx)[rows] + SMOOTH * gg[rows]) / (dp[:, :, None] + SMOOTH)
    pos_mode = pc.argmax(2)
    gap_mode = gc.argmax(2)
    m = len(dp)
    taken = np.zeros((m, n), bool)
    pos = np.zeros((m, k), int)
    for p in range(k):
        s = np.where(taken, -1.0, pc[:, p, :] + noise[rows] * 1e-3)
        pos[:, p] = s.argmax(1)
        taken[np.arange(m), pos[:, p]] = True
    chain = pos_mode[:, :1] + np.c_[np.zeros(m, int), np.cumsum(gap_mode, 1)]      # 0-based numbers
    mask = np.zeros((m, n), bool)
    ok = chain < n
    r = np.repeat(np.arange(m), k).reshape(m, k)
    mask[r[ok], chain[ok]] = True
    hot_rank = np.argsort(-exc, 1)[:, :2 * k]
    for j in range(2 * k):
        need = mask.sum(1) < k
        c = hot_rank[:, j]
        add = need & ~mask[np.arange(m), c]
        mask[np.arange(m)[add], c[add]] = True
    gap = np.argsort(~mask, 1, kind="stable")[:, :k]
    return {"hot": hot, "cold": cold, "pos": pos, "gap": gap, "pos_mode": pos_mode, "gap_mode": gap_mode,
            "dprev": dp[:, 0]}


def metrics(cid):
    """z per metric and period -> array (len(METRICS), len(PERIODS))."""
    pr = predictions(cid)
    H, srt, gaps = G["H"], G["srt"], G["gaps"]
    ar = np.arange(len(H))[:, None]
    per_draw = {t: H[ar, pr[t]].sum(1) for t in TICKETS}
    pos_diff = ((pr["pos_mode"] == srt - 1).sum(1) - (G["base_pos"] == srt - 1).sum(1)).astype(float)
    gap_diff = ((pr["gap_mode"] == gaps).sum(1) - (G["base_gap"] == gaps).sum(1)).astype(float)
    seen = pr["dprev"] >= 1
    out = np.zeros((len(METRICS), len(PERIODS)), np.float32)
    for j, (a, b) in enumerate(G["period_rows"].values()):
        sel = np.zeros(len(H), bool)
        sel[a:b] = True
        sel &= seen
        c = sel.sum()
        if not c:
            continue
        for i, t in enumerate(TICKETS):
            out[i, j] = (per_draw[t][sel].sum() - c * G["e"]) / math.sqrt(c * G["v"])
        for i, dd in ((4, pos_diff[sel]), (5, gap_diff[sel])):
            sd = dd.std()
            out[i, j] = dd.sum() / (sd * math.sqrt(c)) if sd > 0 else 0.0
    return out


def cell_of(codes, s):
    c = codes[:, s[0]].astype(np.int64)
    for j in s[1:]:
        c = c * 1000 + codes[:, j]
    return c


def run(task):
    key, shift_ix, lo, hi = task
    if G.get("key") != key:
        setup(key)
    codes = np.roll(G["codes"], G["shifts"][shift_ix], axis=0)
    return key, shift_ix, lo, np.stack([metrics(cell_of(codes, s)) for s in SETS[lo:hi]])


def detail(key, s):
    """Raw counts of a set's metrics per period (real calendar)."""
    if G.get("key") != key:
        setup(key)
    pr = predictions(cell_of(G["codes"], s))
    H, srt, gaps = G["H"], G["srt"], G["gaps"]
    ar = np.arange(len(H))[:, None]
    seen = pr["dprev"] >= 1
    out = {}
    for p, (a, b) in G["period_rows"].items():
        sel = np.zeros(len(H), bool)
        sel[a:b] = True
        sel &= seen
        c = int(sel.sum())
        o = {"draws": c, "expected_matches": round(c * G["e"], 1)}
        for t in TICKETS:
            o[f"{t}_matches"] = int(H[ar, pr[t]].sum(1)[sel].sum())
        o["pos_hits"] = int((pr["pos_mode"] == srt - 1)[sel].sum())
        o["pos_hits_baseline"] = int((G["base_pos"] == srt - 1)[sel].sum())
        o["gap_hits"] = int((pr["gap_mode"] == gaps)[sel].sum())
        o["gap_hits_baseline"] = int((G["base_gap"] == gaps)[sel].sum())
        out[p] = o
    return out


def select(z, fam_ix):
    """z: sets x metrics x periods. Returns {rule: {metric: {family: set index}}}."""
    out = {"best_valid": {}, "stable": {}}
    for mi, m in enumerate(METRICS):
        for rule, score in (("best_valid", z[:, mi, 1]), ("stable", np.minimum(z[:, mi, 0], z[:, mi, 1]))):
            out[rule][m] = {f: int(np.flatnonzero(ix)[np.argmax(score[ix])]) for f, ix in fam_ix.items()}
    tick = [METRICS.index(t) for t in TICKETS]
    stable = np.minimum(z[:, tick, 0], z[:, tick, 1])
    si, mi = np.unravel_index(int(np.argmax(stable)), stable.shape)
    out["my_lead"] = (int(si), TICKETS[mi])
    return out


def main():
    names = PARAMS
    fams = [family(s) for s in SETS]
    fam_ix = {f: np.array([x == f for x in fams]) for f in sorted(set(fams))}
    fam_ix["all"] = np.ones(len(SETS), bool)
    chunk = 150
    tasks = [(key, sh, lo, min(lo + chunk, len(SETS))) for key in common.GAMES for sh in range(SHIFTS + 1)
             for lo in range(0, len(SETS), chunk)]
    Z = {key: np.zeros((SHIFTS + 1, len(SETS), len(METRICS), len(PERIODS)), np.float32) for key in common.GAMES}
    with Pool(4) as pool:
        for i, (key, sh, lo, z) in enumerate(pool.imap_unordered(run, tasks), 1):
            Z[key][sh, lo:lo + len(z)] = z
            if i % 40 == 0:
                print(f"{i}/{len(tasks)}", flush=True)
    np.savez_compressed(os.path.join(common.ROOT, "analysis", "own_leads_z.npz"), **Z)

    label = lambda s: " x ".join(names[j] for j in s)  # noqa: E731
    ref = tuple(sorted(names.index(p) for p in REF_4D))
    res = {"metrics": METRICS, "periods": list(PERIODS), "sets": len(SETS), "shifts": SHIFTS, "games": {}}
    for key in common.GAMES:
        z = Z[key]
        real = z[0]
        sel_real = select(real, fam_ix)
        sel_null = [select(z[s], fam_ix) for s in range(1, SHIFTS + 1)]
        game = {"label": common.GAMES[key][1], "selected": {}, "null": {}, "top_valid": {}}
        for rule in ("best_valid", "stable"):
            game["selected"][rule] = {}
            game["null"][rule] = {}
            for m in METRICS:
                mi = METRICS.index(m)
                game["selected"][rule][m] = {
                    f: {"set": label(SETS[si]), "early_z": round(float(real[si, mi, 0]), 2),
                        "valid_z": round(float(real[si, mi, 1]), 2), "test_z": round(float(real[si, mi, 2]), 2)}
                    for f, si in sel_real[rule][m].items()}
                game["null"][rule][m] = {
                    f: {"valid_z": [round(float(z[s + 1][sn[rule][m][f], mi, 1]), 2) for s, sn in enumerate(sel_null)],
                        "test_z": [round(float(z[s + 1][sn[rule][m][f], mi, 2]), 2) for s, sn in enumerate(sel_null)]}
                    for f in fam_ix}
        for m in METRICS:
            mi = METRICS.index(m)
            order = np.argsort(-real[:, mi, 1])[:10]
            game["top_valid"][m] = [{"set": label(SETS[i]), "family": fams[i],
                                     **{p: round(float(real[i, mi, j]), 2) for j, p in enumerate(PERIODS)}}
                                    for i in order]
            # how the test z of all sets is spread, real vs shifted (a real effect lifts the mean)
            game.setdefault("all_sets_test_z", {})[m] = {
                "real_mean": round(float(real[:, mi, 2].mean()), 3),
                "shifted_means": [round(float(z[s, :, mi, 2].mean()), 3) for s in range(1, SHIFTS + 1)],
                "valid_test_corr_real": round(float(np.corrcoef(real[:, mi, 1], real[:, mi, 2])[0, 1]), 3),
                "valid_test_corr_shifted": [round(float(np.corrcoef(z[s, :, mi, 1], z[s, :, mi, 2])[0, 1]), 3)
                                            for s in range(1, SHIFTS + 1)]}
        si, m = sel_real["my_lead"]
        game["my_lead"] = {"set": label(SETS[si]), "family": fams[si], "metric": m,
                           **{p: round(float(real[si, METRICS.index(m), j]), 2) for j, p in enumerate(PERIODS)},
                           "detail": detail(key, SETS[si])}
        game["my_lead_null_test_z"] = [round(float(z[s + 1][sn["my_lead"][0], METRICS.index(sn["my_lead"][1]), 2]), 2)
                                       for s, sn in enumerate(sel_null)]
        ri = SETS.index(ref)
        game["lead_4d_same_framework"] = {"set": label(ref), **{m: {p: round(float(real[ri, METRICS.index(m), j]), 2)
                                                                     for j, p in enumerate(PERIODS)} for m in METRICS}}
        res["games"][key] = game
        print(game["label"], "my lead:", {k2: v for k2, v in game["my_lead"].items() if k2 != "detail"})
        print("   null test z of my-lead rule:", game["my_lead_null_test_z"])
        for m in METRICS:
            s = game["selected"]["stable"][m]["all"]
            print(f"   stable {m:<8} {s['set']:<40} early {s['early_z']:+.2f} valid {s['valid_z']:+.2f} test {s['test_z']:+.2f}")
        print("   4D lead here:", {m: game["lead_4d_same_framework"][m]["test"] for m in METRICS})
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote", OUT)


def log(dates):
    res = json.load(open(OUT))
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes")
    with open(LOG, "a", newline="") as fh:
        w = csv.writer(fh)
        for date in dates:
            for key in common.GAMES:
                lead = res["games"][key]["my_lead"]
                s = tuple(PARAMS.index(p) for p in lead["set"].split(" x "))
                setup(key, extra_date=date)
                pr = predictions(cell_of(G["codes"], s), last=len(G["codes"]) - 1)
                nums = sorted(int(x) + 1 for x in pr[lead["metric"]][0])
                w.writerow([date, key, "own_lead", " ".join(f"{x:02d}" for x in nums), now])
                print(date, key, lead["set"], lead["metric"], nums)


if __name__ == "__main__":
    if "--log" in sys.argv:
        log(sys.argv[sys.argv.index("--log") + 1:])
    else:
        main()
