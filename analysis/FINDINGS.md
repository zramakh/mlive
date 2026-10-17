# Findings: can Vedic / Chinese almanac parameters predict Toto and Magnum Life?

Data: STAR TOTO 6/50 (from 2017), POWER TOTO 6/55 (from 2009), SUPREME TOTO 6/58 (from 2010)
and Magnum Life 8/36 (from 2018), up to 17 Oct 2026, main numbers only. Parameters: 83 Vedic,
KP, Chinese almanac and calendar values per draw date at 19:00 MYT (`common.py`, with the
`almanac.py` stack from 4DPrediction). Full details are in [REPORT.md](REPORT.md).

**Short answer: no parameter, pair of parameters or formula has shown an edge on draws it was
not chosen on.** One lead carried over from 4D is positive and is being tracked live (below).

## How things were tested

- Per game: train on the first 50% of draws, validate on the next 20%, test on the last 30%,
  in date order. The formulas were frozen and committed (9d5446a) before the test was run.
- Chance levels come from simulated fair draws, or from the exact overlap variance of two fair
  draws.
- Multiple testing is handled by rerunning every scan on circularly shifted parameter calendars.
  That keeps every rhythm but breaks any real link.

## What was tried (all at chance)

| Approach | Script | Result |
|---|---|---|
| Fairness: uniformity, yearly drift, weekday, repeats, draw shape, same-evening overlap | `fairness.py` | all \|z\| < 2.5 |
| Hot / cold / repeat-last tickets | `fairness.py` | 0.90–1.07× |
| Same numbers recurring when a parameter (83) or pair (3,403) recurs | `conditional.py` | same as shifted calendars |
| Each cell's top-k numbers learned before the test, replayed in the test | `conditional.py` | 0.985–1.008× |
| Best pre-test parameter / pair, scored on the test | `conditional.py` | z −1.29 to +1.32 |
| Vedic numerology (planet number as digital root or digit) | `numerology.py` | not directional; no replication |
| Vedic-only, Chinese-only and combined formulas, frozen, forward-tested draw by draw | `astro_model.py` | 0.94–1.04× (validation had shown 1.05–1.37×) |
| Similar-days kernel over 78 Vedic + Chinese parameters | `astro_model.py` | 1.00–1.06×; tuning chose almost no astrology weight |
| Own lead search: hot, cold, per-position and neighbour-gap patterns for 78 parameters and 3,003 pairs, chosen on early + validation draws | `own_leads.py` | my 4 leads: test z −0.49, −2.77, −1.37, +0.59; selected leads average below 0, like shifted calendars |

Every formula fits the real results worse than "all numbers equally likely".

## Own leads vs earlier leads (test draws, z)

| Lead | 6/50 | 6/55 | 6/58 | Life |
|---|---|---|---|---|
| My leads: lagna × lunar month (hot), karana × adhika masa (hot), Rahu rashi × Saturn retro (position), pada × day officer (position) | −0.49 | −2.77 | −1.37 | +0.59 |
| 4D lead, Mercury nakshatra × Venus rashi (static / draw-by-draw) | +0.81 / +0.16 | +0.59 / −0.68 | +0.73 / +0.22 | +2.75 / +0.83 |

Each of my leads was +2 to +3.7 z in two separate periods before the test, then fell to chance.
None did better than the earlier leads. Per-position and gap predictions get *worse* when
conditioned on any parameter (fewer draws per cell, more noise).

## Is the 4D lead special? (`lead_4d_robustness.py`, `lead_hunt.py`)

No. Scored the same way:
- Random pairs with no selection beat it. Sun nakshatra × Na Yin sums +6.24 over the four games
  against the lead's +4.70, and 2 of 200 random pairs beat it.
- The 58 sets 4D picked average +0.07 here, the same as random. The lead is the best of them,
  which happens by chance 42% of the time.
- Three other 4D picks score almost as high (+4.52, +4.39, +4.10).

## Lead worth watching (now explained as chance)

| Lead | Evidence | Problem |
|---|---|---|
| 4D lead #1, Mercury nakshatra × Venus rashi: replay the cell's 8 most frequent numbers (Magnum Life) | Chosen on 4D data, so out of sample here; 643 matches vs 590 expected in 2024–2026 (z +2.75, top 0.1% of pairs); positive in both test halves and slightly positive in all three Toto games | Best of 8 checks (corrected p ≈ 0.02); only +0.83 when its ticket is updated draw by draw; same-cell draws don't share numbers more than chance; 1.94 vs 1.78 numbers per ticket |

## Live checks

Tickets for 18 and 21 Oct 2026 (four formulas, `lead_4d` and `own_lead`, all four games) are in
`forward_log.csv`, logged before the draws. Once results are in `data/`, score them with
`python3 analysis/astro_model.py score`.
