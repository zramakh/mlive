#!/usr/bin/env python3
"""Baseline: do the four games behave like fair, independent draws?

Every chance level comes from simulating the same number of draws with every
number equally likely (Monte Carlo, 2000 runs), so no distributional
approximation is needed.

Tests per game
  uniform        are all numbers equally frequent? (chi-square)
  year drift     do number frequencies change from year to year? (number x year chi-square)
  persistence    correlation of each number's excess between the two halves of the history
  weekday        number x weekday chi-square
  repeats        overlap with the draw 1, 2, 5 and 10 draws back
  sum / odd / consecutive  shape of each draw
Across games: do Star, Power and Supreme Toto on the same evening share numbers more than chance?
Strategies (walk-forward on the test period, see common.py): hot all-time, hot last 100, cold,
repeat last draw. Each picks one ticket of k numbers per draw.

python3 analysis/fairness.py   (~1 min)  -> analysis/fairness_results.json
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

SIMS = 2000
OUT = os.path.join(common.ROOT, "analysis", "fairness_results.json")


def simulate(d, k, n, rng):
    """d fair draws of k from 1..n as a d x n 0/1 matrix."""
    order = np.argsort(rng.random((d, n)), axis=1)[:, :k]
    m = np.zeros((d, n), np.int8)
    np.put_along_axis(m, order, 1, axis=1)
    return m


def chi_uniform(h):
    c = h.sum(0)
    e = c.mean()
    return float(((c - e) ** 2 / e).sum())


def chi_groups(h, g):
    """Homogeneity chi-square of number frequencies across groups g."""
    tot = 0.0
    p = h.sum(0) / h.sum()
    for v in np.unique(g):
        c = h[g == v].sum(0)
        e = c.sum() * p
        tot += float(((c - e) ** 2 / np.where(e > 0, e, 1)).sum())
    return tot


def persistence(h):
    a, b = h[: len(h) // 2].mean(0), h[len(h) // 2:].mean(0)
    return float(np.corrcoef(a, b)[0, 1])


def overlap(h, lag):
    return float((h[lag:] * h[:-lag]).sum(1).mean())


def shape(h, nums):
    s = nums.sum(1)
    odd = (nums % 2).sum(1)
    srt = np.sort(nums, 1)
    consec = (np.diff(srt, axis=1) == 1).sum(1)
    return float(s.mean()), float(s.std()), float(odd.mean()), float(consec.mean())


def p_value(real, sims):
    sims = np.asarray(sims)
    return float((1 + (sims >= real).sum()) / (1 + len(sims)))


def strategies(g):
    """Walk-forward tickets on the test period; matches per ticket vs k*k/n."""
    h, k, n = g["hit"][:, 1:], g["k"], g["n"]
    _, start = common.splits(len(h))
    cum = np.cumsum(np.vstack([np.zeros((1, n), int), h]), 0)    # cum[i] = counts before draw i
    rng = np.random.default_rng(1)
    out = {}
    picks = {
        "hot_all_time": lambda i: np.argsort(-(cum[i] + rng.random(n) * 1e-3))[:k],
        "hot_last_100": lambda i: np.argsort(-(cum[i] - cum[max(0, i - 100)] + rng.random(n) * 1e-3))[:k],
        "cold_all_time": lambda i: np.argsort(cum[i] + rng.random(n) * 1e-3)[:k],
        "repeat_last_draw": lambda i: np.flatnonzero(h[i - 1]),
        "random": lambda i: rng.choice(n, k, replace=False),
    }
    exp = k * k / n
    for name, f in picks.items():
        m = np.array([h[i, f(i)].sum() for i in range(start, len(h))])
        d = len(m)
        sd = np.sqrt(d * exp * (1 - k / n) * (n - k) / (n - 1))       # hypergeometric variance
        out[name] = {"draws": d, "matches": int(m.sum()), "expected": round(d * exp, 1),
                     "lift": round(m.sum() / (d * exp), 3), "z": round((m.sum() - d * exp) / sd, 2),
                     "draws_3plus": int((m >= 3).sum())}
    return out


def main():
    rng = np.random.default_rng(2026)
    res = {}
    games = {k: common.load_game(k) for k in common.GAMES}
    for key, g in games.items():
        h, k, n = g["hit"][:, 1:], g["k"], g["n"]
        d = len(h)
        years = np.array([x[:4] for x in g["dates"]])
        wd = np.array([common.dt.date.fromisoformat(x).weekday() for x in g["dates"]])
        real = {"uniform": chi_uniform(h), "year_drift": chi_groups(h, years), "persistence": persistence(h),
                "weekday": chi_groups(h, wd), **{f"repeat_lag{l}": overlap(h, l) for l in (1, 2, 5, 10)}}
        sums = shape(h, g["nums"])
        sims = {key2: [] for key2 in real}
        sim_shape = []
        for _ in range(SIMS):
            s = simulate(d, k, n, rng)
            sims["uniform"].append(chi_uniform(s))
            sims["year_drift"].append(chi_groups(s, years))
            sims["persistence"].append(persistence(s))
            sims["weekday"].append(chi_groups(s, wd))
            for l in (1, 2, 5, 10):
                sims[f"repeat_lag{l}"].append(overlap(s, l))
            nums = np.argsort(-s, 1)[:, :k] + 1
            sim_shape.append(shape(s, nums))
        tests = {}
        for t, v in real.items():
            arr = np.array(sims[t])
            tests[t] = {"value": round(v, 4), "chance_mean": round(float(arr.mean()), 4),
                        "chance_sd": round(float(arr.std()), 4),
                        "z": round(float((v - arr.mean()) / arr.std()), 2),
                        "p_high": round(p_value(v, arr), 4), "p_low": round(p_value(-v, -arr), 4)}
        ss = np.array(sim_shape)
        for j, t in enumerate(("sum_mean", "sum_sd", "odd_mean", "consecutive_mean")):
            tests[t] = {"value": round(sums[j], 3), "chance_mean": round(float(ss[:, j].mean()), 3),
                        "z": round(float((sums[j] - ss[:, j].mean()) / ss[:, j].std()), 2)}
        counts = h.sum(0)
        res[key] = {"label": g["label"], "draws": d, "first": g["dates"][0], "last": g["dates"][-1],
                    "tests": tests,
                    "most_frequent": [[int(i + 1), int(counts[i])] for i in np.argsort(-counts)[:5]],
                    "least_frequent": [[int(i + 1), int(counts[i])] for i in np.argsort(counts)[:5]],
                    "expected_per_number": round(d * k / n, 1),
                    "strategies": strategies(g)}
        print(g["label"], {t: (v["z"], v.get("p_high")) for t, v in tests.items()})

    # same-evening overlap between the three Sports Toto games
    cross = {}
    for a, b in (("toto50", "toto55"), ("toto50", "toto58"), ("toto55", "toto58")):
        ga, gb = games[a], games[b]
        ib = {d: i for i, d in enumerate(gb["dates"])}
        pairs = [(i, ib[d]) for i, d in enumerate(ga["dates"]) if d in ib]
        m = min(ga["n"], gb["n"])
        ov = np.array([(ga["hit"][i, 1:m + 1] * gb["hit"][j, 1:m + 1]).sum() for i, j in pairs])
        exp = m * (ga["k"] / ga["n"]) * (gb["k"] / gb["n"])
        sd = np.sqrt(len(ov)) * ov.std()
        cross[f"{a}_vs_{b}"] = {"dates": len(ov), "shared": int(ov.sum()), "expected": round(len(ov) * exp, 1),
                                "z": round(float((ov.sum() - len(ov) * exp) / sd), 2)}
    res["same_evening_overlap"] = cross
    print(cross)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
