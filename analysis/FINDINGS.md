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

**Cold numbers, same test** (`hot_window.py --cold`, [COLD_WINDOW.md](COLD_WINDOW.md)): least-frequent numbers of the
previous N draws, decayed counts, and "overdue" (longest gap since last drawn). Chosen look-backs: 6/50 N=200 → test z
+1.37; 6/55 half-life 20 → +0.03; 6/58 N=200 → +0.16; Life N=15 → +0.31 (fair histories −1.8 to +1.9). Re-optimised
every draw: +0.33, +0.26, +0.21, −0.16. Overdue: +1.75, +0.26, −0.42, −0.07. Last 10 draws: 8/7.2, 5/6.5, 6/6.2,
21/17.8. Selection-vs-test correlation across look-backs −0.40 to +0.34; fair histories have SD ≈ 0.3 for this, so
Magnum Life's +0.26–0.34 happens 18% of the time. No cold rule works either.

**Hot + cold in one ticket** (`hot_cold_mix.py`, [HOT_COLD_MIX.md](HOT_COLD_MIX.md)): h hottest of the last Nh draws +
(k − h) coldest of the last Nc (or overdue), 295–400 combinations per game. Chosen: 6/50 3 hot (300) + 3 cold (200) →
test z +0.98; 6/55 6 cold (50) → −0.30; 6/58 4 hot (100) + 2 cold (200) → −1.60; Life 1 hot (50) + 7 cold (10) →
−0.64 (fair histories, same pipeline: about −1.7 to +1.6). The chosen combinations' selection z (+2.14 to +2.69) is what
the same menu gives on fair histories (+2.19 to +2.36). Re-chosen every draw: +0.27, −1.29, −0.03, −2.08. Last 10:
8/7.2, 6/6.5, 12/6.2, 18/17.8.

**Hot / cold + astrology in one score** (`hotcold_astro.py`): score = α·hot/cold(Nh) + β·hot/cold(Nc) + γ·astrology cell
signal, the astrology set one of the 20 that ranked best on the early/validation periods of `own_leads.py`; ~3,000
combinations per game chosen on draws 25–70%. Chosen: 6/50 γ 2 (Mercury combust × day officer) → test z −2.64 (same mix
without astrology −1.73); 6/55 γ 2 (karana × adhika masa) → −1.15 (+0.93 without); 6/58 γ 2 (paksha × Rahu rashi) →
−0.52 (+0.16 without); Life γ 0.5 (Venus nakshatra × planets with Moon) → +0.89 (+0.51 without). Selection z +3.8 to
+4.8 here and +3.1 to +4.8 on 5 shifted calendars, which also always choose γ > 0; their test z −1.28 to +1.32. The
astrology term wins the selection because it adds flexibility to fit noise, and it does not help on later draws.

## Further astrological factors from web research (`extra_astro.py`, [EXTRA_ASTRO.md](EXTRA_ASTRO.md))

Practitioner sources (no tested evidence found) suggested the Part of Fortune, Western aspects, KP ruling planets,
date numerology and He Tu numbers; the daily Nine Star and Plum Blossom trigrams were added from the almanac. Eleven
direct number rules (no fitting) × 4 games: z −2.28 to +2.83, 3 with |z| > 1.96 vs 2.2 on shifted calendars, mean z
+0.08 (29% of shifts higher). The best, Star Toto's universal day number (numbers with the date's digital root), is
1.08× (z +2.83, positive in all three thirds of its history), but it is the best of 44 tests (8.5% of shifted
calendars beat it) and absent from Power and Supreme Toto, drawn the same evenings (thirds −0.95/−0.27/+0.12 and
−2.47/+1.37/+0.39); its last 10: 3 vs 6.7. Logged as `universal_day` for 18 and 21 Oct. As lead parameters the new
factors match the shifted calendars (replication lift 0.966–1.001 vs 0.980–1.007; walk-forward leads −1.57 to +2.12).

## Ten tickets per draw on the last 10 draws (`ten_tickets.py`, [TEN_TICKETS.md](TEN_TICKETS.md))

Every ticket-producing method (choices frozen without the last 10 draws) played its 10 best k-number sets per draw on
26 Sep – 17 Oct 2026; chance from 20,000 simulated fair draw sets on the same tickets. 92 methods × games: 10 below 5%
(4.6 expected), 1 below 1% (0.9 expected), and the low ones are near-copies of each other. Top: Power Toto
selected-parameter analogy (tropical Moon sign + Jupiter nakshatra) 116 vs 65.3 matches (p 0.009), but 7 of its 9
three-number tickets came from one draw (30 Sep, when its overlapping tickets all held 28 33 34), and "replay the
previous draw" scored 105 (p 0.035). Supreme Toto's hot+cold mix, Jupiter cell lead and plain "hot last 100" are the
same recent-hot-number signal (101–111 vs 62). Random tickets scored at chance in every game.

## Lead search for more numbers in one ticket (`lead_search10.py`, [LEAD_SEARCH10.md](LEAD_SEARCH10.md))

114 astrological parameters (83 + 31 new) and all pairs × 4 patterns (hot, cold, position, hot+recent) = 26,220 leads per
game, 10 tickets per draw, ranked without the last 10 draws by the weakest of three period z-scores of the best-ticket
matches. Leads consistent in all three periods (z > 1): 31, 40, 131, 62 vs 28–61, 29–80, 65–131, 48–108 on shifted
calendars. The top 10 per game on the last 10 draws (best ticket per draw, summed): 6/50 121 vs 106.3 expected (shifted
selections 66–113), 6/55 93 vs 96.7 (98–104), 6/58 83 vs 91.9 (93–113), Life 247 vs 236.5 (233–257). Best single
result: 6/55 Venus nakshatra × Na Yin element (position) 14 vs 9.7, 11 three-number tickets vs 1.3 (chance 7.9%). No
ticket matched more than 3 numbers in the Toto games or 4 in Magnum Life. No new lead emerged.

**Same search with 20 tickets per draw** ([LEAD_SEARCH20.md](LEAD_SEARCH20.md)): top 10 per game on the last 10 draws
(best ticket summed) 6/50 132 vs 122.8 (shifted 84–127), 6/55 109 vs 112.3 (98–115), 6/58 97 vs 106.9 (101–134), Life 262
vs 257.6 (255–266). Magnum Life's Mars rashi × month (cold) is #1 with 10 and with 20 tickets: 34 vs 25.8 (chance 1.2%),
103 three-or-more tickets vs 47.3; it is the best of about 40 leads tested on these draws and of the near-identical
"year × month" cold leads (27 each). New in Star Toto: Mercury rashi × lunar month (position) 19 vs 12.3 (1.4%). The
10-ticket leads mostly kept their ranks but stayed at chance on the last 10.

## Magnum Life System 9 × 2 (`lead_search10.py --system 9`, `system_methods.py`)

Two 9-number System entries per draw (disjoint: ranks 1–9 and 10–18; overlap: ranks 1–9 and 1–6 + 10–12); outcome =
drawn numbers inside the better set. New searches over all parameters and pairs: top 10 on the last 10 draws 264 vs
270.3 expected (disjoint; shifted 257–267) and 224 vs 238.7 (overlap; shifted 231–248) — no new lead
([LEAD_SEARCHSYS9_DISJOINT.md](LEAD_SEARCHSYS9_DISJOINT.md), [LEAD_SEARCHSYS9_OVERLAP.md](LEAD_SEARCHSYS9_OVERLAP.md)).
Earlier leads: Mars rashi × month (cold) 29 vs 27.0 (disjoint, 30%) and 31 vs 23.9 (overlap, 2.5%); Mars rashi ×
tropical Sun sign 35 vs 27.0 (disjoint, 0.6%) but it ranks 16,410th on the earlier periods; Moon rashi × Mars combust
caught 6 of 8 in one overlap set. Non-parameter methods ([SYSTEM9_METHODS.md](SYSTEM9_METHODS.md)): best analogy
"direct" 31 vs 27.0 (11%) and 29 vs 23.9 (8%). A set with 5+ of 8 is expected about once in 37 draws.

**System 10 × 1** (`lead_search10.py --system 10 --sets 1`, [LEAD_SEARCHSYS10.md](LEAD_SEARCHSYS10.md),
[SYSTEM10_METHODS.md](SYSTEM10_METHODS.md)): one 10-number set (the top 10) per draw. Top 10 new leads on the last 10 draws
227 vs 222.7 expected (shifted 210–235). Mars rashi × month (cold) ranked #2 on the earlier periods and caught 30 vs 22.3
(chance 2.3%), no draw above 4 of 8. Best other methods: analogy "direct" 28 (6.9%) and "map" 28 (7.4%, one set with 6).

**System play with bonus balls** (`--bonus`; [LEAD_SEARCHSYS9_DISJOINT_BONUS.md](LEAD_SEARCHSYS9_DISJOINT_BONUS.md),
[LEAD_SEARCHSYS9_OVERLAP_BONUS.md](LEAD_SEARCHSYS9_OVERLAP_BONUS.md), [LEAD_SEARCHSYS10_BONUS.md](LEAD_SEARCHSYS10_BONUS.md),
SYSTEM9/10_METHODS_BONUS.md): sets scored on all 10 balls (8 main + 2 bonus), results split main + bonus. Top 10 new leads
on the last 10 draws: System 9 disjoint 310 vs 325.9 (shifted 325–339), overlap 303 vs 292.1 (292–318), System 10 280 vs
278.1 (260–299) — at chance. Earlier leads (10 balls): Mars rashi × month 32 vs 32.6 / 34 vs 29.2 / 34 vs 27.8, but only 3–4
bonus balls (about 5.5 expected); Mars rashi × Venus combust 36 vs 29.2 (overlap, 4%) and 35 vs 27.8 (System 10, 4.3%);
Mars rashi × tropical Sun sign 40 vs 32.6 (disjoint, 1.2%) but ranked 9,007th on the earlier periods.

## Re-choosing the lead before every draw (`rolling_select.py`)

The hot / cold counts inside every lead were already updated before each draw; what was fixed was the *choice* of lead. Here all ~26,000 leads (parameters and pairs × hot / cold / position / hot+recent) are re-ranked before each of the last 10 draws on every earlier draw (weakest of three period z-scores of balls caught), and the #1 lead and the top 10 are played. Balls caught over the 10 draws (main + bonus for the System formats):

| Format | Re-chosen #1 | Re-chosen top 10 (avg) | Frozen #1 | Frozen top 10 (avg) | Expected | Shifted calendars, re-chosen #1 |
|---|---|---|---|---|---|---|
| STAR TOTO 6/50, 10 tickets | 13 | 11.7 | 13 | 11.5 | 10.63 | 11, 11 |
| POWER TOTO 6/55, 10 tickets | 9 | 9.9 | 9 | 9.3 | 9.67 | 13, 12 |
| SUPREME TOTO 6/58, 10 tickets | 9 | 7.5 | 9 | 8.3 | 9.19 | 9, 10 |
| Magnum Life, 10 tickets | 17 | 24.0 | 21 | 24.9 | 23.65 | 20, 28 |
| Magnum Life System 9 × 2 overlap + bonus | 27 | 29.9 | 29 | 30.3 | 29.21 | 34, 29 |
| Magnum Life System 9 × 2 disjoint + bonus | 33 | 31.6 | 33 | 31.6 | 32.59 | 30, 35 |
| Magnum Life System 10 × 1 + bonus | 29 | 28.0 | 29 | 28.5 | 27.81 | 29, 29 |

Re-choosing does not help: one extra draw hardly moves a ranking built on 1,300-2,800 draws, so the #1 lead mostly stays the same (1-4 different leads over the 10 draws), and where it changes the result is equal or worse. Every row is within chance and the shifted calendars do as well. Details in `ROLLING_*.md`.

## Magnum Life leads ranked by profit (`profit_rank.py`)

Official Magnum Life prize table per 8-number combination (8 = Grand, RM1,000 a day for 20 years, counted as RM7.3m; 7+bonus RM100,000; 7 RM6,000; 6+bonus RM600; 6 RM100; 5+bonus RM30; 5 RM10; 4+bonus RM5; a combination with both bonus numbers wins its +bonus prize twice), System 9 = 9 combinations (RM9), System 10 = 45 (RM45). All 26,224 leads, tickets built before each draw from counts updated on every earlier draw. Profit over the last 10 draws (RM):

| Format (cost over 10 draws) | Random tickets, expected | Best lead (hindsight) | Shifted calendars, best | #1 by earlier profit | Top 10 by earlier profit, average | Re-ranked by profit before every draw |
|---|---|---|---|---|---|---|
| 10 tickets (RM100) | -45 | +7,330,300 (paksha × venus_rashi, cold) | +24,500, +8,170 | -100 | -94 | -100 |
| System 10 × 1 (RM450) | -202 | +7,398,350 (paksha × venus_rashi, cold) | +20,010, +121,430 | -450 | -339 | -450 |
| System 9 × 2 overlap (RM180) | -81 | +110,060 (aspect_venus_jupiter × universal_day, hot) | +12,900, +110,400 | -180 | -156 | -180 |
| System 9 × 2 disjoint (RM180) | -81 | +110,020 (ayana × lunar_leap_month, hot+100) | +110,060, +110,060 | -160 | -87 | -160 |

Paksha × Venus rashi (cold) caught all 8 numbers on 26 Sep 2026 (checked independently: 67 earlier draws in that cell, 7 of the winners in its cold top 8 and the 8th at rank 10). It is luck, not a lead: it ranked 12,375th (10 tickets) and 8,135th (System 10) on the earlier draws, where it lost money, and 26,224 leads × 10 draws give a jackpot-sized lottery among themselves. The leads with the most earlier profit are all leads that once hit the Grand prize (ritu × year_yinyang, mars_combust × ritu, hora_lord × saturn_nakshatra ...); the shifted calendars have just as many (best earlier profit RM7.3-8.1m on every calendar), and on the last 10 draws they won almost nothing. Re-ranking by profit before every draw keeps the same past jackpot winner and loses the full stake. Every honest choice lost about what random tickets lose or more.

**Combined ranking (`profit_combined.py`, `PROFIT_COMBINED.md`).** All 104,896 lead × format rows (10 ordinary tickets, System 10 × 1, System 9 × 2 overlap / disjoint) scored by the average of their rank by profit margin (profit ÷ stake) and by winning draws. Best on the last 10 draws: Rahu rashi × aspect Mercury–Saturn (cold), System 9 × 2 disjoint, +RM12,685 on RM180 with 4 winning draws (one 7-number hit), earlier margin −82%. Rows in profit with 3+ winning draws: 319 (shifted calendars 188, 224). The top 10 by the same score on the earlier draws (all System 9 disjoint, margins of +530-550% from an earlier Grand prize) lost RM152 on average on the last 10 with 0.7 winning draws (shifted −172, −199).

**6-, 7- and 8-number hits against 20 shifted calendars (`high_hits_null.py`, `HIGH_HITS_NULL.md`).** Counting, over all 26,224 leads and the whole history after warm-up, the lead × draw hits whose best 8-number combination holds 6+, 7+ or 8 winning numbers: the real calendar has slightly more than the shifted calendars in every format, 6+ by 1-4% (rank 2/21 in three formats, 6/21 for System 9 disjoint) and 7+ by 9-16% (rank 3-5/21); System 10 Grand-level hits 39 vs 25 on average (rank 1/21, max shifted 38). The four formats and the "earlier" / "whole history" rows reuse the same leads and draws, so this is about one test at p ≈ 0.05-0.10, not many. It is a small population-wide tilt that no lead chosen in advance has captured (all earlier forward tests lost), and a few percent more 6- and 7-number hits is far from turning the 45% expected loss into a profit.

## Sports Toto with the official prizes, 10 sets of 6 (`toto_profit.py`, `TOTO_PROFIT.md`)

Star 6/50 (RM1 a set; 6 = RM1,188,888 minimum, 5 + bonus = RM100,000, 5 = RM2,008, 4 + bonus = RM788, 4 = RM28, 3 + bonus = RM18, 3 = RM8), Power 6/55 (RM1; 6 = RM3m minimum, 5 = RM3,300, 4 = RM40, 3 = RM3), Supreme 6/58 (RM2; 6 = RM8.89m minimum, 5 = RM6,888, 4 = RM80, 3 = RM8). Random sets return 35%, 20% and 20% of the stake with jackpots at their minimum. All 26,224 leads and the non-parameter methods, 10 sets per draw, last 10 draws:

| Game (stake over 10 draws) | Random, expected | Best lead (hindsight) | Shifted, best | #1 by earlier profit | Top 10 by earlier profit | Best non-parameter method |
|---|---|---|---|---|---|---|
| Star 6/50 (RM100) | −65 | +8,100 (hora_lord × mars_retrograde, cold: 5 numbers on 7 Oct) | +8,100, +8,116 | −100 | −97 | −28 (replay previous draw) |
| Power 6/55 (RM100) | −80 | +3,023,083 (masa × day_god, hot: jackpot on 27 Sep) | +3,023,080, +3,016,566 | −100 | −82 | −70 (embedding neural) |
| Supreme 6/58 (RM200) | −160 | +27,856 (nakshatra × nayin, hot+100: 5 numbers on 11 Oct) | +7,192, +7,264 | −200 | −146 | −160 (analogy similar) |

Two Power Toto leads hit the jackpot on the last 10 draws (shifted calendars: 6 and 1); on the earlier draws the real calendar had 8 jackpot-level lead × draw hits against 15 and 25 shifted (Star 18 vs 15, 18; Supreme 13 vs 15, 13). 5-number hits on the last 10 were more common on the real calendar (Star 28 vs 11, 25; Power 146 vs 101, 77; Supreme 22 vs 2, 5) but each game's come mostly from one draw (Star 7 Oct, Power and Supreme 11 Oct) shared by many related leads. Every choice made before the 10 draws lost about the whole stake, the leaders by earlier profit being past jackpot winners.

**Toto, the Magnum Life analyses repeated (`toto_full.py`, `param_excess.py`).** Four formats (10 sets, System 7 × 2 overlap / disjoint, System 8 × 1; a System S entry = all its 6-number combinations as ordinary bets), all 26,224 leads, real calendar vs 20 shifted calendars. Choosing by earlier profit, by the combined score or by re-ranking before every draw lost roughly the stake in every game and format, as on the shifted calendars (`TOTO_SYSTEM_PROFIT.md`, `TOTO_COMBINED.md`). Over the whole history, 5-number hits (all leads together) rank 1st of 21 on the real calendar in all four Star Toto formats (+11-16%; all leads together z +3.7), but 10th-17th in Power and Supreme Toto; 6-number hits are ordinary or low in all three (`TOTO_HIGH_HITS_NULL.md`). Magnum Life's 6+ excess is z +1.4. The Star Toto excess comes mostly from slow, seasonal parameters (solar term, lagna nakshatra, adhika masa, Mercury / Venus retrograde, KP star lords, ritu), not from day-based ones, and no parameter is strong in all four games (`PARAM_EXCESS.md`). The per-lead top 10 by 5+ hits against their own shifted calendars got 0-1 5+ hits on the last 10 draws, as expected for any 10 leads (`TOTO_LEAD_HIGH_HITS.md`). With 100 shifted calendars (`toto_null100.py`, `TOTO_NULL100_TOTO50.md`) the Star Toto excess shrinks to p = 0.02-0.08 over the whole history (the shifted calendars have heavier tails than 20 suggested); it is absent in the first half of the history (p 0.20-0.40), present in the second (p 0.02-0.05) and absent on the last 10 draws (p 0.32-0.59): borderline and not steady over time.

**History windows (`lead_full.py --window`, `WINDOWS_COMPARE.md`).** Instead of all earlier draws of a lead's cell: only the most recent unbroken run (last_round), the 5 or 10 most recent (last5, last10), or all with weight halving every 10 occurrences (decay10); 7 patterns, four games, all analyses. Choices made before the last 10 draws lost about the stake in every window and game, as on the shifted calendars, apart from single leads (Magnum Life last_round: day_element × aspect_moon_jupiter hot, one 6 + bonus; Star last10 10 sets: top 10 +RM122). Over the whole history the real calendar's high-hit rank is best with all draws (Star Toto 1st of 21 in every format) and mostly 10th-21st with the shorter windows; short windows also make many leads pick the same numbers (Supreme last_round: 2,955 leads won the same RM272 on 2026-10-18). Forward draw 2026-10-18: the biggest wins came from leads with poor earlier records in every window (Star last5 karana × aspect_venus_mars hot: 5 + bonus, RM112,216, rank 33,653).

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
