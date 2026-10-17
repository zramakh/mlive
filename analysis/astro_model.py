#!/usr/bin/env python3
"""Toto / Magnum Life prediction formulas built only from Vedic and/or Chinese
parameters, tuned on the validation draws and forward-tested draw by draw on
the test draws (splits in common.py). The same design as the 4DPrediction
repo's astro_model.py, adapted from 4-digit numbers to 6-from-n games.

Formulas (one set per game)
  vedic    the 52 Vedic / KP parameters in common.VEDIC
  chinese  the 26 Chinese almanac parameters in common.CHINESE
  both     the union
  kernel   "similar days": past draws weighted by exp(beta x number of the 78
           Vedic + Chinese parameters they share with the target date)

Nothing else enters a score: no hot numbers, no recency. Every term is a ratio
"how often X was drawn on dates with this parameter value" / "how often X was
drawn overall", so a number that is simply common gains nothing.

For a draw on date t, with v_f = value of parameter f on t:

  score(n) = scale * sum over the formula's terms (f, kind)  L_kind(f, v_f, n)

  L_num  (f,v,n) = log[(draws of n on dates with f=v + 10) / (expected + 10)]
  L_dec  (f,v,n) = same for n's decade (1-9, 10-19, ...), pseudo-count 50
  L_last (f,v,n) = same for n's last digit, pseudo-count 50
  kernel score(n) = log[weighted share of draws containing n / unweighted share]

The ticket is the k top-scoring numbers (one play: 6 numbers, 8 for Magnum
Life). For likelihoods each number is given P(drawn) = k * softmax(score)_n.

Tuning: counts from the train draws, scored on the validation draws by the
log-likelihood of the real results. Every (parameter, kind) term is scored on
its own, the ones that helped are ranked, and the best prefix length and scale
are kept. The kernel's beta is chosen the same way (walk-forward through the
validation draws). The result is frozen in astro_model_formulas.json, which is
committed before the test is run.

Forward test: every test draw is predicted from all draws strictly before
it, then added to the counts.

Usage (repo root):
  python3 analysis/astro_model.py tune                 choose and freeze the formulas (~1 min)
  python3 analysis/astro_model.py test                 forward-test the frozen formulas (~2 min)
  python3 analysis/astro_model.py predict --date 2026-10-18 [--game toto55]
  python3 analysis/astro_model.py log --date 2026-10-18     append picks to forward_log.csv before the draw
  python3 analysis/astro_model.py score                     score forward_log.csv against data/*.csv
"""

import argparse
import csv
import datetime as dt
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

FORMULAS = os.path.join(common.ROOT, "analysis", "astro_model_formulas.json")
RESULTS = os.path.join(common.ROOT, "analysis", "astro_model_results.json")
LOG = os.path.join(common.ROOT, "analysis", "forward_log.csv")
VARIANTS = {"vedic": common.VEDIC, "chinese": common.CHINESE, "both": common.VEDIC + common.CHINESE}
KINDS = ["num", "dec", "last"]
ALPHA = {"num": 10.0, "dec": 50.0, "last": 50.0}
PREFIXES = [1, 2, 3, 5, 8, 12, 20, 30]
SCALES = [0.1, 0.25, 0.5, 1.0, 2.0]
BETAS = [0.03, 0.1, 0.2, 0.3, 0.5, 1.0]
KERNEL_PARAMS = common.VEDIC + common.CHINESE


def group_matrix(n, kind):
    """n x groups 0/1 matrix mapping numbers 1..n (columns 0..n-1) to groups."""
    if kind == "num":
        return np.eye(n)
    g = [(x // 10) if kind == "dec" else (x % 10) for x in range(1, n + 1)]
    m = np.zeros((n, max(g) + 1))
    m[np.arange(n), g] = 1
    return m


class Game:
    def __init__(self, key):
        g = common.load_game(key)
        self.key, self.label, self.k, self.n = key, g["label"], g["k"], g["n"]
        self.dates = g["dates"]
        self.h = g["hit"][:, 1:].astype(float)
        self.codes, self.values = common.codes_for(self.dates)
        self.col = {p: i for i, p in enumerate(common.ALL_PARAMS)}
        self.train_end, self.test_start = common.splits(len(self.dates))
        self.gm = {kind: group_matrix(self.n, kind) for kind in KINDS}

    def counts(self, upto, params):
        """Per parameter: wins[value, number] and draws[value] over draws [0, upto)."""
        out = {}
        for p in params:
            c = self.codes[:upto, self.col[p]]
            v = len(self.values[self.col[p]])
            w = np.zeros((v, self.n))
            np.add.at(w, c, self.h[:upto])
            out[p] = (w, np.bincount(c, minlength=v).astype(float))
        return out

    def term(self, cnt, upto, p, kind, rows):
        """L_kind for parameter p on draws `rows` (their own parameter values) -> rows x n."""
        w, dv = cnt[p]
        gm = self.gm[kind]
        share = self.h[:upto].sum(0) @ gm / upto                    # per group, per draw
        v = self.codes[rows, self.col[p]]
        obs = w[v] @ gm
        exp = dv[v][:, None] * share[None, :]
        a = ALPHA[kind]
        return (np.log((obs + a) / (exp + a))) @ gm.T


def loglik(score, hits, k):
    """Bernoulli log-likelihood gain over uniform, nats per draw."""
    n = score.shape[1]
    s = score - score.max(1, keepdims=True)
    p = np.clip(k * np.exp(s) / np.exp(s).sum(1, keepdims=True), 1e-9, 1 - 1e-9)
    ll = (hits * np.log(p) + (1 - hits) * np.log(1 - p)).sum(1)
    u = k / n
    ll0 = (hits * np.log(u) + (1 - hits) * np.log(1 - u)).sum(1)
    return float((ll - ll0).mean())


def ticket_matches(score, hits, k, seed=0):
    noise = np.random.default_rng(seed).random(score.shape) * 1e-9
    top = np.argsort(-(score + noise), 1)
    return hits[np.arange(len(hits))[:, None], top[:, :k]].sum(1), hits[np.arange(len(hits)), top[:, 0]]


def shared_params(g, rows, upto_each):
    """For each target row t: number of kernel parameters shared with each draw before upto_each[t]."""
    cols = [g.col[p] for p in KERNEL_PARAMS]
    c = g.codes[:, cols]
    return [(c[:u] == c[t]).sum(1) for t, u in zip(rows, upto_each)]


def kernel_scores(g, rows, upto_each, beta, shared=None):
    shared = shared or shared_params(g, rows, upto_each)
    out = np.zeros((len(rows), g.n))
    for i, (s, u) in enumerate(zip(shared, upto_each)):
        w = np.exp(beta * (s - s.max()))
        w = w / w.mean()
        prior = 20.0
        base = g.h[:u].mean(0)
        wf = (w @ g.h[:u] + prior * base) / (w.sum() + prior)
        out[i] = np.log(wf / base)
    return out


# ------------------------------------------------------------------ tuning
def tune_game(g):
    rows = np.arange(g.train_end, g.test_start)
    hits = g.h[rows]
    cnt = g.counts(g.train_end, common.VEDIC + common.CHINESE)
    single = {}
    for p in common.VEDIC + common.CHINESE:
        for kind in KINDS:
            sc = g.term(cnt, g.train_end, p, kind, rows)
            single[(p, kind)] = (sc, loglik(sc, hits, g.k))
    out = {}
    for var, params in VARIANTS.items():
        cand = sorted(((t, ll) for t, (_, ll) in single.items() if t[0] in params), key=lambda x: -x[1])
        helped = [t for t, ll in cand if ll > 0]
        best = {"terms": [], "scale": 0.0, "valid_ll_gain": 0.0}
        for m in PREFIXES:
            if m > len(helped):
                break
            tot = sum(single[t][0] for t in helped[:m])
            for sc in SCALES:
                ll = loglik(sc * tot, hits, g.k)
                if ll > best["valid_ll_gain"]:
                    best = {"terms": [list(t) for t in helped[:m]], "scale": sc, "valid_ll_gain": ll}
        best.update(terms_tried=len(cand), terms_helped=len(helped),
                    top_single_terms=[[*t, round(ll, 5)] for t, ll in cand[:10]])
        if best["terms"]:
            tot = best["scale"] * sum(single[tuple(t)][0] for t in best["terms"])
            m, t1 = ticket_matches(tot, hits, g.k)
            best["valid_ticket_lift"] = round(float(m.mean() / (g.k * g.k / g.n)), 4)
        out[var] = best
        print(f"  {g.label:<18} {var:<8} terms {len(best['terms']):>2}/{len(helped)}/{len(cand)} "
              f"scale {best['scale']} valid LL gain {best['valid_ll_gain']:+.5f}")
    shared = shared_params(g, rows, rows)
    kb = []
    for b in BETAS:
        ll = loglik(kernel_scores(g, rows, rows, b, shared), hits, g.k)
        kb.append([b, ll])
    b, ll = max(kb, key=lambda x: x[1])
    out["kernel"] = {"beta": b, "valid_ll_gain": ll, "all_betas": kb}
    print(f"  {g.label:<18} kernel   beta {b} valid LL gain {ll:+.5f}")
    return out


def tune():
    res = {"created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"), "games": {}}
    for key in common.GAMES:
        g = Game(key)
        res["games"][key] = {"label": g.label, "train": [g.dates[0], g.dates[g.train_end - 1]],
                             "valid": [g.dates[g.train_end], g.dates[g.test_start - 1]],
                             "test_from": g.dates[g.test_start], **tune_game(g)}
    with open(FORMULAS, "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote", FORMULAS)


# ------------------------------------------------------------------ scoring with frozen formulas
def formula_scores(g, f, rows, upto_each):
    """Scores of a frozen formula for target rows, each from draws before upto_each."""
    out = np.zeros((len(rows), g.n))
    if not f["terms"]:
        return out
    params = sorted({p for p, _ in f["terms"]})
    last = None
    for i, (r, u) in enumerate(zip(rows, upto_each)):
        if u != last:
            cnt, last = g.counts(u, params), u
        out[i] = f["scale"] * sum(g.term(cnt, u, p, kind, [r])[0] for p, kind in f["terms"])
    return out


def scores_for(g, frozen, variant, rows, upto_each):
    if variant == "kernel":
        return kernel_scores(g, rows, upto_each, frozen["kernel"]["beta"])
    return formula_scores(g, frozen[variant], rows, upto_each)


def test():
    frozen = json.load(open(FORMULAS))["games"]
    res = {}
    for key in common.GAMES:
        g = Game(key)
        rows = np.arange(g.test_start, len(g.dates))
        hits = g.h[rows]
        exp = g.k * g.k / g.n
        var1 = exp * (1 - g.k / g.n) * (g.n - g.k) / (g.n - 1)
        out = {"label": g.label, "test": [g.dates[rows[0]], g.dates[rows[-1]]], "draws": len(rows),
               "expected_matches_per_ticket": round(exp, 4)}
        hot = np.log((g.h.cumsum(0)[rows - 1] + 10) / (rows[:, None] * g.k / g.n + 10))
        for var in list(VARIANTS) + ["kernel", "hot_numbers"]:
            sc = hot if var == "hot_numbers" else scores_for(g, frozen[key], var, rows, rows)
            m, t1 = ticket_matches(sc, hits, g.k)
            tot = int(m.sum())
            out[var] = {"matches": tot, "expected": round(len(rows) * exp, 1),
                        "lift": round(tot / (len(rows) * exp), 4),
                        "z": round((tot - len(rows) * exp) / np.sqrt(len(rows) * var1), 2),
                        "tickets_3plus": int((m >= 3).sum()),
                        "tickets_3plus_expected": round(len(rows) * p_at_least(3, g.k, g.n), 1),
                        "top1_hit_rate": round(float(t1.mean()), 4), "top1_chance": round(g.k / g.n, 4),
                        "ll_gain_per_draw": round(loglik(sc, hits, g.k), 5) if sc.any() else 0.0}
            print(f"  {g.label:<18} {var:<12} matches {tot}/{len(rows) * exp:.1f} lift {out[var]['lift']:.3f} "
                  f"z {out[var]['z']:+.2f}  3+ {out[var]['tickets_3plus']}/{out[var]['tickets_3plus_expected']} "
                  f"LL {out[var]['ll_gain_per_draw']:+.5f}")
        res[key] = out
    with open(RESULTS, "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote", RESULTS)


def p_at_least(m, k, n):
    """P(a ticket of k matches >= m of the k numbers drawn from n)."""
    from math import comb
    return sum(comb(k, j) * comb(n - k, k - j) for j in range(m, k + 1)) / comb(n, k)


# ------------------------------------------------------------------ live picks
def picks(key, date):
    frozen = json.load(open(FORMULAS))["games"][key]
    g = Game(key)
    if date <= g.dates[-1]:
        sys.exit(f"{date} is not after the last {g.label} draw in data/ ({g.dates[-1]})")
    # append the target date as a pseudo-row so its parameter values can be looked up
    codes, _ = common.codes_for([date])
    g.codes = np.vstack([g.codes, codes])
    r, u = len(g.dates), len(g.dates)
    out = {}
    for var in list(VARIANTS) + ["kernel"]:
        sc = scores_for(g, frozen, var, [r], [u])[0]
        if not sc.any():
            out[var] = None
            continue
        out[var] = sorted(int(x) + 1 for x in np.argsort(-sc)[:g.k])
    return out


def cmd_predict(a):
    for key in ([a.game] if a.game else common.GAMES):
        for var, nums in picks(key, a.date).items():
            print(f"{common.GAMES[key][1]:<18} {var:<8} " + (" ".join(f"{x:02d}" for x in nums) if nums
                                                             else "(no terms survived tuning: random)"))


def cmd_log(a):
    new = not os.path.exists(LOG)
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes")
    with open(LOG, "a", newline="") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["draw_date", "game", "variant", "numbers", "logged_utc"])
        for key in ([a.game] if a.game else common.GAMES):
            for var, nums in picks(key, a.date).items():
                if nums:
                    w.writerow([a.date, key, var, " ".join(f"{x:02d}" for x in nums), now])
    print("appended picks for", a.date, "to", LOG)


def cmd_score(_):
    games = {k: common.load_game(k) for k in common.GAMES}
    with open(LOG) as fh:
        for r in csv.DictReader(fh):
            g = games[r["game"]]
            if r["draw_date"] not in g["dates"]:
                print(r["draw_date"], r["game"], r["variant"], "not drawn yet")
                continue
            if r["logged_utc"][:10] > r["draw_date"]:
                print(r["draw_date"], r["game"], r["variant"], "logged after the draw, not scored")
                continue
            won = set(g["nums"][g["dates"].index(r["draw_date"])].tolist())
            mine = {int(x) for x in r["numbers"].split()}
            print(f"{r['draw_date']} {g['label']:<18} {r['variant']:<8} {r['numbers']}  "
                  f"matched {len(mine & won)} ({' '.join(f'{x:02d}' for x in sorted(mine & won))})  "
                  f"expected {g['k'] * g['k'] / g['n']:.2f}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("tune")
    sub.add_parser("test")
    for name in ("predict", "log"):
        p = sub.add_parser(name)
        p.add_argument("--date", required=True)
        p.add_argument("--game", choices=list(common.GAMES))
    sub.add_parser("score")
    a = ap.parse_args()
    {"tune": lambda _: tune(), "test": lambda _: test(), "predict": cmd_predict, "log": cmd_log,
     "score": cmd_score}[a.cmd](a)


if __name__ == "__main__":
    main()
