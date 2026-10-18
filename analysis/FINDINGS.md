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

## Per game: which parameters performed well (`per_game_leads.py`)

[PER_GAME_LEADS.md](PER_GAME_LEADS.md) lists, for each game on its own, the top single parameters and pairs
for each pattern, with their z in all three periods. Over the four ticket patterns and four games, 137
parameter sets had z > 1 in all three periods; the shifted calendars give 160 on average. Each game's most
consistent ticket lead (6/50 karana × Venus rashi, cold; 6/55 year yin/yang × day god, cold; 6/58 Jupiter
rashi × Jupiter retrograde, hot; Life Moon rashi × Mars combust, position) is logged as `per_game_best`.

## Leads chosen without the last 5 draws, tested on them (`holdout_leads.py`)

A fresh search on each game's history minus its last 5 draws (7–17 Oct 2026), then tested on those 5 draws
([HOLDOUT_LEADS.md](HOLDOUT_LEADS.md)). Each game's top 20 leads together matched about as many numbers as fair
tickets: 6/50 63 vs 72.0, 6/55 67 vs 65.5, 6/58 60 vs 62.1, Life 156 vs 177.8. The same selection on shifted
calendars gave 52–89. The #1 picks: Life Moon rashi × Mars combust (position) matched 13 vs 8.9 (a fair ticket
does this 6.5% of the time); 6/58 Jupiter rashi × Jupiter retrograde (hot) 6 vs 3.1 (7.4%); 6/55 year yin/yang
× day god (cold) 3 vs 3.3; 6/50 tithi × 19:00 hour stem (position) 2 vs 3.6. A lead's ranking before the hold-out
does not predict its hold-out score (correlation −0.06 to +0.01 over all 12,324 tickets per game).

**Same test with 6-number tickets in every game** (`holdout_leads.py --ticket 6 --games ml8`,
[HOLDOUT_LEADS_T6.md](HOLDOUT_LEADS_T6.md)): Magnum Life's search and selection redone with 6 picks. Its top 20 matched 121
vs 133.3 expected (shifted calendars 80–138). The new #1, hora lord × Venus rashi (position), matched 4 vs 6.7.
Moon rashi × Mars combust is no longer consistent with 6 numbers (weakest period z +0.50, not in the top 20); on the
held-out draws its 6-number ticket matched 9 vs 6.7 (p 0.19). Its earlier strength depended on the ticket size. With
equal tickets, the best #1 pick is Supreme Toto's Jupiter rashi × Jupiter retrograde (6 vs 3.1, p 0.07).

**Supreme Toto, last 10 draws held out** (`holdout_leads.py --hold 10 --games toto58`,
[HOLDOUT_LEADS_H10.md](HOLDOUT_LEADS_H10.md)): searched again without 26 Sep – 17 Oct 2026. Jupiter rashi × Jupiter
retrograde (hot) is #1 again and matched 11 vs 6.2 over the 10 draws (p 0.035), i.e. 5 vs 3.1 on the 5 draws not in
the earlier test. The other 19 leads matched 94 vs 117.9; all 20 together 105 vs 124.1 (shifted calendars 95–136).
Its ticket (15 39 42 44 48 54) is the same for every draw, because Jupiter stayed in Karka, direct. A plain
"hottest 6 of the last 100 draws" ticket also matched 11 (last 50 / 201 / 300 draws: 8, 5, 8), so the result does
not need Jupiter.

**The same lead on Sports Toto 4D** (`lead_on_4d.py`, 4DPrediction's data/sportstoto.csv): 16-number tickets
from earlier 4D draws with the same Jupiter rashi and retrograde state. Over the last 30% of 4D draws it scored 55
hits vs 60.5 expected (whole numbers) and 58 vs 60.5 (digit combinations); in the last 10 draws, 0 vs 0.37. That is
below 67–82% of 200 random pairs. The 4D lead (Mercury nakshatra × Venus rashi) on the same test: 68 vs 60.2 and
57 vs 60.2. On Magnum 4D (test from 2014-06-04) it scored 85 vs 75.3 (number, z +1.12; 20% of random pairs as high)
and 84 vs 75.3 (digit, +1.00; 12%); on Da Ma Cai (from 2016-02-14) 69 vs 63.3 (+0.72; 30%) and 74 vs 63.3 (+1.34;
11%). Last 10 draws: 1 hit vs 0.37 (Magnum), 0 (Da Ma Cai). None of the six scores is significant; the 4D lead,
scored the same way, ranges from z −1.27 to +1.51.

## Embedding / language-model approach (`embed_model.py`, [EMBEDDINGS.md](EMBEDDINGS.md))

Each draw as a "sentence" of tokens (its 83 parameter values + the numbers drawn); word2vec-style vectors (PPMI + SVD)
and a small neural language model (averaged parameter embeddings → softmax over numbers, optionally with the previous
draw's numbers as context). Settings chosen on validation draws; tested on later draws and on the last 10 draws; the
whole pipeline repeated on 5 shifted calendars.

| Game | Vector arithmetic (PPMI): test z / last 10 | Shifted calendars | Neural LM: test z / last 10 | Neural, shifted | LM validation loss vs uniform |
|---|---|---|---|---|---|
| 6/50 | +1.65 / 8 vs 7.2 | −1.48 to +1.26 / 6–12 | +0.63 / 6 vs 7.2 | +0.01 to +0.24 | 3.9115 vs 3.9120 |
| 6/55 | −0.06 / 5 vs 6.6 | −1.85 to +0.97 / 3–9 | +1.72 / 7 vs 6.6 | +1.72 (all 5) | 4.0092 vs 4.0073 |
| 6/58 | +0.59 / 3 vs 6.2 | −0.18 to +1.72 / 3–7 | −0.36 / 4 vs 6.2 | −1.26 to −0.07 | 4.0635 vs 4.0604 |
| Life | +0.61 / 22 vs 17.8 | −1.07 to +0.85 / 15–20 | +0.50 / 19 vs 17.8 | +0.15 to +0.26 | 3.5850 vs 3.5835 |

The vectors do learn real astronomy (Moon in Vrishabha − Rohini + Ashwini ≈ Moon in Mesha; Jupiter in Karka sits next
to Jupiter in Ashlesha), but number tokens only sit next to generic, common tokens. The neural model's validation loss
never beats "all numbers equally likely", early stopping keeps it at 5–20 epochs, and its tickets come out the same on
shifted calendars, i.e. they ignore the parameters and follow overall number frequency. Every LM fits the test draws
worse than uniform (log-likelihood −0.008 to −0.035 nats per draw).

## Analogy forecaster (`analogy_model.py`)

numbers(today) ≈ numbers(A) − conditions(A) + λ·conditions(today), with A = the previous draw (`last`), the 10 most
similar earlier draws (`similar`), the same through a learned condition→numbers map (`map`), or the map alone
(`direct`). λ (the weight of the astrology term) and dimensions chosen on validation draws; test on later draws and the
last 10; 5 shifted calendars as control.

| Game | last (λ) | similar (λ) | map (λ) | direct | Shifted calendars, all methods | AUC real / shifted |
|---|---|---|---|---|---|---|
| 6/50 | −0.54 (2) | +2.20 (0) | +2.20 (0) | +0.08 | −0.78 to +1.10 | 0.487–0.504 / 0.491–0.507 |
| 6/55 | +1.26 (0) | −0.01 (0) | −0.01 (0) | +0.74 | −1.16 to +1.72 | 0.504–0.509 / 0.496–0.510 |
| 6/58 | −0.24 (2) | −0.60 (2) | +0.71 (2) | −0.36 | −2.51 to +2.37 | 0.498–0.501 / 0.494–0.510 |
| Life | +1.83 (2) | +0.38 (2) | −0.84 (2) | −0.49 | −0.90 to +1.72 | 0.504–0.509 / 0.498–0.514 |

(test z of ticket matches.) Validation chose λ = 0 (astrology term off) in 5 of the 12 analogy settings. The two
highest scores do not need the analogy: 6/50 `similar` / `map` +2.20 has λ = 0, and Magnum Life `last` +1.83 is one of
16 scores, inside what the shifted calendars produce (up to +2.37). No method's AUC (how well the real numbers rank) is
above the shifted calendars'. Last 10 draws: all within the shifted range (e.g. Life 20–23 vs 17.8 expected, shifted
12–23).

## Fewer parameters (`param_select.py`)

The vector forecasters (`direct` map and `last`-draw analogy) rebuilt from a selected subset of parameters, chosen on
validation draws only: top-m by single-parameter validation AUC (m ∈ 1, 3, 5, 10, 20) or greedy forward selection
(≤ 10). Selection repeated on 4 shifted calendars.

| Game / forecaster | All 83 (test z) | top-m: chosen → test z | greedy: chosen → test z |
|---|---|---|---|
| 6/50 direct | +0.08 | ritu → −0.39 | ritu, Jupiter rashi, day element → −0.86 |
| 6/50 last | +0.32 | day element → +1.26 | day element, nakshatra, tropical Sun sign → +0.40 |
| 6/55 direct | +2.30 | Venus nakshatra, 19:00 hour stem, day officer → −0.70 | Venus nakshatra, Na Yin, KP Asc star lord, Moon rashi → −0.75 |
| 6/55 last | +1.20 | 5 params → −0.47 | tropical Moon sign, Jupiter nakshatra → +1.38 |
| 6/58 direct | −0.66 | KP Sun star lord → +0.23 | 5 params → −0.66 |
| 6/58 last | −0.84 | hora lord → +0.59 | 6 params → +0.53 |
| Life direct | −0.49 | Jupiter rashi, lagna nakshatra, Mercury combust → +0.32 | Jupiter rashi, samvatsara → −0.84 |
| Life last | +1.08 | 20 params → +1.54 | 5 params → −0.72 |

Reduced sets average test z +0.05 (all 83: +0.37); shifted-calendar selections range −2.88 to +2.18. Every game and
forecaster picks different parameters, and the shifted calendars pick equally plausible-looking ones. One last-10
result stands out: 6/55 `last` with tropical Moon sign + Jupiter nakshatra matched 13 vs 6.6 (p 0.008 for one ticket
set; about 12% for the best of the 16 hold-out results here), while a shifted calendar also reached 13.

Draw by draw, that lead's tickets are mostly the previous draw's numbers (e.g. 4 Oct ticket 21 28 32 39 51 52 vs 3 Oct
result 21 28 37 39 51 52), and the last 10 Power Toto draws repeated many numbers from the draw before (28 came up 5
times). A plain "replay the previous draw" ticket matched 12 numbers over those 10 draws (p 0.021); the same analogy with
200 random parameter pairs matched 9.6 on average, and 10% of them reached 13 or more (best 16). The lead adds one
match over replaying the last draw, and a random pair of parameters does that well 10% of the time.

## Recent repeats and hot streaks, without astrology (`recency.py`, [RECENCY.md](RECENCY.md))

Against 500 simulated fair histories per game: Power Toto's last 10 draws are genuinely unusual (12 numbers repeated
from the previous draw, top 2.2%; number 28 in 6 of 10 draws, 0.8%; confirmed against lottolyzer), and Supreme Toto's
last 10 drew its 100-draw hot numbers 11 times (top 2.6%). But windows like these occur in each game's history at the
normal rate, hot-number runs do not carry over from one 10-draw window to the next (correlation −0.02 to +0.07, fair
≈ 0), and number frequencies are no more uneven than chance in any game, recently or overall (no ball or machine
bias). Repeats from the previous draw do cluster slightly in all four games (window-to-window +0.03 to +0.14; combined
p ≈ 0.01), but a strategy that plays the repeat ticket only after a high-repeat window returned 0.79–1.05× of chance.

## Optimising the hot-number look-back (`hot_window.py`, [HOT_WINDOW.md](HOT_WINDOW.md))

Hot ticket = k most frequent numbers of the previous N draws (N = 5 … 500 or all) or exponentially weighted (half-life
5–200). Chosen on draws 25–70%, tested on 70% → last 10, and on the last 10. Chosen look-backs: 6/50 N=300 → test z
−2.05; 6/55 half-life 5 → +0.03; 6/58 N=100 → −0.47; Life N=150 → +0.22 (fair histories, same pipeline: −1.7 to +1.8).
Re-optimising every draw over the previous 200: −1.54, −2.33, +0.11, −0.79. A look-back's selection score does not
predict its test score (correlation −0.50, +0.06, −0.03, +0.00; fair ≈ 0). No look-back works.

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
