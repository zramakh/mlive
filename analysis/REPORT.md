# Can Vedic / Chinese almanac astrology predict Malaysian Toto and Magnum Life?

**Short answer: no.** 8,425 draws from STAR TOTO 6/50, POWER TOTO 6/55, SUPREME TOTO 6/58 and
Magnum Life 8/36 behave like fair, independent draws. No astrological parameter, pair of
parameters or tuned formula picked numbers better than chance on draws it had not seen. One
lead carried over from the 4D project is worth watching, but it is not strong enough to rely on
(section 6).

This is the same analysis as the [4DPrediction](https://github.com/zramakh/4DPrediction) repo's
astrology work, adapted from 4-digit numbers to "6 numbers from n" games. The four games are
analysed separately because their number ranges differ.

| Game | Draws | History | Tuning (train / valid) | Test |
|---|---|---|---|---|
| STAR TOTO 6/50 | 1,437 | 2017-10-21 – 2026-10-17 | to 2022-06-28 / to 2024-02-28 | 2024-03-02 – 2026-10-17 (432) |
| POWER TOTO 6/55 | 2,856 | 2009-10-31 – 2026-10-17 | to 2017-11-05 / to 2021-05-29 | 2021-05-30 – 2026-10-17 (857) |
| SUPREME TOTO 6/58 | 2,786 | 2010-03-20 – 2026-10-17 | to 2018-01-14 / to 2021-10-24 | 2021-10-26 – 2026-10-17 (836) |
| Magnum Life 8/36 | 1,346 | 2018-04-25 – 2026-10-17 | to 2022-09-27 / to 2024-05-01 | 2024-05-04 – 2026-10-17 (404) |

The splits are the first 50% of each game's draws (train), the next 20% (validation) and the last
30% (test). They were fixed in `common.py` before any test was run. Only main numbers are used;
bonus numbers are ignored.

## 0. Parameters

`common.py` computes **83 parameters** for every draw date at 19:00 Malaysia time, the draw time.
They are cached in `data/astro_params.csv` (every draw date, plus the next 120 days for
predictions). The astronomy and almanac code (`ephemeris.py`, `vedic.py`, `kp.py`, `almanac.py`)
is copied unchanged from 4DPrediction. Each module self-checks against published values: moon
phases, ingresses, Chinese New Year, KL sunrise/sunset, the panchanga of known dates, almanac day
pillars, mansions, officers and Nine Star. Run any of them directly to repeat its check.

* **Vedic / KP (52):** tithi, paksha, nakshatra (+pada, lord), yoga, karana, weekday (vara),
  hora lord; the rashi and nakshatra of the Sun, Mars, Mercury, Venus, Jupiter, Saturn and Rahu;
  Moon rashi and navamsa; lagna rashi and nakshatra; retrograde and combust flags; planets with
  the Moon; masa, adhika masa, ritu, ayana, samvatsara; KP star lord, sub lord and number of the
  Moon, Ascendant and Sun.
* **Chinese (26):** year animal, stem, element, yin/yang and pillar; lunar month, day and leap
  month; solar term; month and day pillars (stem, branch, element); Na Yin and its element; 19:00
  hour stem; 12 officers; 12 day gods; Yellow/Black path; 28 mansions; Tai Sui relation; year and
  month Nine Star.
* **Other (5):** month, day of month, moon phase, and the tropical Moon and Sun signs.

## 1. Are the draws fair? (`fairness.py`)

Every chance level comes from 2,000 simulated histories with the same number of draws, so no
approximation is involved.

| Test | 6/50 | 6/55 | 6/58 | Life |
|---|---|---|---|---|
| All numbers equally frequent (chi-square z) | −0.85 | −0.37 | +1.31 | −0.04 |
| Frequencies drift year to year (number × year) | −0.67 | +0.78 | +0.23 | +0.76 |
| Number excess persists between the two halves of the history | +0.17 | −0.55 | +0.67 | +0.56 |
| Weekday effect (number × weekday) | −0.73 | −0.11 | −0.62 | −0.06 |
| Repeats from the previous draw | −0.46 | +1.20 | −0.01 | −0.49 |
| Sum, odd count and consecutive numbers per draw | all \|z\| < 1.9 | | | |

(z against simulated fair draws.) The "hot" and "cold" numbers are what luck produces. For
example, Power Toto's most frequent number, 14, came up 348 times against 311.6 expected, and
its least frequent, 26, came up 280 times. That spread is normal for 55 numbers.

Star, Power and Supreme Toto are drawn on the same evenings. On those evenings they do not share
numbers more than chance (z = +1.32, −0.83, +0.23).

**Simple strategies on the test draws** (one ticket per draw; wins are the numbers matched):

| Strategy | 6/50 | 6/55 | 6/58 | Life |
|---|---|---|---|---|
| Hot numbers (all-time) | 0.97× | 1.00× | 0.97× | 1.04× |
| Hot numbers (last 100 draws) | 0.95× | 0.99× | 0.97× | 0.99× |
| Cold numbers | 1.03× | 1.02× | 0.90× | 0.97× |
| Repeat the last draw | 0.97× | 1.07× | 0.99× | 0.97× |
| Random ticket | 1.05× | 0.98× | 1.02× | 0.98× |

All are within luck. The largest, cold numbers on 6/58 at 0.90× (z = −2.5), is in the wrong
direction for a strategy.

## 2. Do numbers depend on the conditions of the date? (`conditional.py`)

A cell is one value of a parameter ("Moon in Rohini"), or a pair of values ("Moon in Rohini &
Jupiter in Mesha"). Every single parameter (83) and every pair (3,403) was scanned, per game:

1. **Recurrence:** do two draws in the same cell share more numbers than two fair draws
   (k²/n on average)? The z uses the exact variance of that overlap.
2. **Replication:** learn each cell's k most frequent numbers on the train+valid draws, then play
   that ticket on the same cell's test draws.
3. **Strongest association:** the single cell and number with the largest excess, i.e. the kind
   of claim a search produces ("number 3 comes up on tithi 16").

The scan was repeated on **20 circularly shifted parameter calendars**: every parameter is moved
by the same number of draws, at least a year's worth. That keeps every natural rhythm and breaks
only the link between dates and numbers, so it shows how extreme the best of thousands of tests
gets by luck.

| Game | Scan | Best recurrence z (shifted avg) | Sets with z > 3 (shifted avg) | Replication lift (shifted avg) | Strongest association z (shifted avg) |
|---|---|---|---|---|---|
| 6/50 | singles | 2.34 (1.82) | 0 (0.0) | 0.985 (0.985) | 4.56 (4.63) |
| 6/50 | pairs | 3.33 (3.24) | 2 (1.6) | 0.991 (0.992) | 6.68 (6.23) |
| 6/55 | singles | 3.37 (2.30) | 1 (0.1) | 0.998 (0.999) | 5.24 (5.21) |
| 6/55 | pairs | 3.75 (3.41) | 7 (4.2) | 0.999 (1.001) | 6.72 (6.67) |
| 6/58 | singles | 2.86 (2.38) | 0 (0.1) | 0.993 (0.994) | 5.07 (5.19) |
| 6/58 | pairs | 3.77 (3.33) | 7 (3.9) | 1.001 (1.000) | 6.78 (6.80) |
| Life | singles | 1.83 (2.22) | 0 (0.1) | 1.008 (1.004) | 3.88 (4.08) |
| Life | pairs | 2.77 (3.32) | 0 (4.7) | 1.000 (1.001) | 5.22 (5.00) |

The real calendars look like the shifted ones. Replication is about 1.00× everywhere, so
whatever a cell "favoured" before the test period, it did not favour afterwards.

The one single parameter that beat 19 of the 20 shifts is Power Toto's Venus nakshatra
(recurrence z = 3.37). It is the best of 83 × 4 games, and its replication on the test draws is
z = +0.10, i.e. nothing.

The strongest associations look striking on their own. Examples: Supreme Toto number 50 came up
10 times in 15 draws with Jupiter in its rashi and the same month branch, against 1.55 expected;
Star Toto number 9 came up 9 times in 11 draws with the same KP Ascendant sub lord and year
element, against 1.32. But the shifted calendars produce equally extreme ones.

**Walk-forward leads.** The parameter or pair with the best recurrence on the train+valid draws
was then scored on the test draws:

| Game | Chosen before the test (pre-test z) | Test replication z |
|---|---|---|
| 6/50 | day officer (2.59); day element × day officer (4.03) | −0.83; −0.58 |
| 6/55 | karana (2.14); karana × Saturn retrograde (3.18) | −1.17; −0.94 |
| 6/58 | Yellow/Black path (2.35); KP Ascendant star lord × Yellow/Black path (3.47) | +0.44; +1.32 |
| Life | samvatsara (2.16); nakshatra pada × day officer (3.75) | −0.30; −1.29 |

## 3. Vedic numerology (`numerology.py`)

Planet numbers (Sun 1, Moon 2, Jupiter 3, Rahu 4, Mercury 5, Venus 6, Ketu 7, Saturn 8, Mars 9)
were tested for nine ruling planets of the draw: weekday lord, hora lord, nakshatra lord, and the
KP star and sub lords of the Moon, Ascendant and Sun. Two questions: do winning numbers have that
digital root, or contain that digit, more often? That gives 72 tests.

* 8 tests reached |z| > 1.96, against 3.5 on average on 200 shifted calendars (4.5% of shifts
  had as many). That looks borderline, but a planet-number effect would make the results
  positive. 3 of the 8 are negative, including the largest (Supreme Toto, Ascendant star lord's
  digital root, z = −3.23). The average z is +0.14, and 27% of shifted calendars do better.
* Of the six results with |z| > 1.96 on the train+valid draws, the three positive ones fell to
  +0.08, +0.12 and −0.88 on the test draws.

## 4. Astrology-only formulas, frozen and forward-tested (`astro_model.py`)

This has the same structure as 4DPrediction's section 8. Each term compares how often a number,
its decade (1–9, 10–19, …) or its last digit came up on dates with the same parameter value
against how often it came up overall. Only Vedic and/or Chinese parameters enter: no hot numbers,
no recency.

```
score(n) = scale * Σ terms  log[(draws of n (or its group) with f = today's value + a) / (expected + a)]
kernel:   score(n) = log[share of past draws containing n, weighting each past draw by
                         exp(beta * number of the 78 Vedic+Chinese parameters it shares with today)
                         / unweighted share]
ticket   = the k highest-scoring numbers (6, or 8 for Magnum Life)
```

**Tuning:**
1. Count on the train draws, then score every (parameter, kind) term alone on the validation
   draws, by the likelihood of the real results.
2. Keep the best-ranked terms that helped, choosing the prefix length and scale.
3. Choose the kernel's beta the same way.

The formulas were written to `astro_model_formulas.json` and **committed (9d5446a) before the
test was run.** Then every test draw was predicted from all earlier draws only, and added to the
counts afterwards.

| Game | Formula | Terms | Validation ticket lift | **Test matches / expected** | Test lift (z) | Tickets with 3+ (expected) | Fit vs uniform |
|---|---|---|---|---|---|---|---|
| 6/50 | Vedic | 30 | 1.33× | 313 / 311.0 | 1.01× (+0.13) | 5 (7.6) | worse |
| 6/50 | Chinese | 8 | 1.17× | 309 / 311.0 | 0.99× (−0.13) | 5 (7.6) | worse |
| 6/50 | Both | 20 | 1.37× | 321 / 311.0 | 1.03× (+0.64) | 6 (7.6) | worse |
| 6/50 | Kernel β=0.03 | – | – | 329 / 311.0 | 1.06× (+1.15) | 9 (7.6) | worse |
| 6/55 | Vedic | 12 | 1.22× | 556 / 560.9 | 0.99× (−0.23) | 15 (11.4) | worse |
| 6/55 | Chinese | 5 | 1.16× | 534 / 560.9 | 0.95× (−1.27) | 13 (11.4) | worse |
| 6/55 | Both | 12 | 1.25× | 538 / 560.9 | 0.96× (−1.08) | 16 (11.4) | worse |
| 6/55 | Kernel β=0.03 | – | – | 567 / 560.9 | 1.01× (+0.28) | 14 (11.4) | worse |
| 6/58 | Vedic | 12 | 1.14× | 490 / 518.9 | 0.94× (−1.40) | 5 (9.5) | worse |
| 6/58 | Chinese | 5 | 1.05× | 527 / 518.9 | 1.02× (+0.39) | 8 (9.5) | worse |
| 6/58 | Both | 20 | 1.19× | 514 / 518.9 | 0.99× (−0.24) | 8 (9.5) | worse |
| 6/58 | Kernel β=0.03 | – | – | 522 / 518.9 | 1.01× (+0.15) | 14 (9.5) | worse |
| Life | Vedic | 12 | 1.15× | 724 / 718.2 | 1.01× (+0.27) | 100 (95.2) | worse |
| Life | Chinese | 5 | 1.13× | 746 / 718.2 | 1.04× (+1.31) | 96 (95.2) | worse |
| Life | Both | 20 | 1.17× | 696 / 718.2 | 0.97× (−1.05) | 94 (95.2) | worse |
| Life | Kernel β=0.03 | – | – | 720 / 718.2 | 1.00× (+0.08) | 99 (95.2) | worse |
| (baseline) | Hot numbers | – | – | | 0.95–1.03× | | worse |

**Reading it.**
* Every formula looked 5–37% better than chance on the validation draws it was tuned on. On the
  test draws all 16 are between 0.94× and 1.06×, which is the spread of random tickets.
* Every formula, and the hot-number baseline, fits the real results *worse* than "every number
  equally likely". The terms that "helped" during tuning were fitting noise: of 78–234 terms
  tried per formula, 6–43 looked useful, which is about what chance gives.
* The kernel's best beta was the smallest tried (0.03). That is a near-zero weight on
  astrological similarity, i.e. the tuning itself preferred to switch the astrology off.

For scale, a fair ticket matches 0.72 numbers per draw on 6/50, 0.65 on 6/55, 0.62 on 6/58 and
1.78 on Magnum Life. The jackpot odds are 1 in 15.9 million (6/50), 29.0 million (6/55),
40.5 million (6/58) and 30.3 million (Magnum Life, all 8 numbers). A 5% lift on the match count,
the best seen, would not change those odds in any useful way.

## 5. Live forward log

`python3 analysis/astro_model.py log --date YYYY-MM-DD` appends each formula's ticket for a
future draw to `forward_log.csv`, with the time it was made. `lead_4d_check.py --log` does the
same for the lead in section 6. `python3 analysis/astro_model.py score` scores every logged
ticket once its draw is in `data/`; tickets logged after their draw are refused. Tickets for
**18 and 21 Oct 2026** were logged on 17 Oct 2026 (14:20 UTC).

## 6. The 4D project's leads on these games (`lead_4d_check.py`)

4DPrediction's top two leads, chosen on 4D data alone, were re-scored here with the statistics
of section 2. Because they were picked before this data was looked at, they count as an honest
out-of-sample check (2 leads × 4 games):

| Game | Mercury nakshatra × Venus rashi: replication z (recurrence z) | Karana × Day pillar |
|---|---|---|
| 6/50 | +0.81 (+0.95) | +0.23 (−0.18) |
| 6/55 | +0.59 (−0.01) | +2.41 (+1.41) |
| 6/58 | +0.73 (+0.53) | −0.82 (−0.34) |
| Life | **+2.75** (+0.74) | +0.69 (+1.68) |

On Magnum Life, Mercury nakshatra × Venus rashi ranks in the top 0.1% of all 3,403 pairs for
replication. The replication z is well calibrated: SD 0.94–1.00 over all pairs, on both real and
shifted calendars. The lead is positive in both halves of the test period (+1.69, +1.91) and
positive in the three Toto games (+0.6 to +0.8).

Against it:
* It is the best of 8 checks; allowing for that, its p ≈ 0.02.
* Draws in the same cell do not share numbers more than chance (recurrence z = +0.74; −0.09
  before the test period). A real "cell favours numbers" effect should show up there too.
* In 4D it was a different statistic (positional hot digits), and it had faded there since 2019.
* The effect size is small: 643 matches against 590 expected, i.e. 1.94 instead of 1.78 numbers
  per Magnum Life ticket.

It is logged as variant `lead_4d` in `forward_log.csv` so that future draws, which nothing here
has seen, can settle it. Note that its ticket for a cell only changes when Venus changes rashi
or Mercury changes nakshatra.

### How unusual is the 4D lead? (`lead_4d_robustness.py`)

Because the lead was chosen on unrelated 4D data, the fair question is how its score here ranks
among all 3,403 pairs:

| | 6/50 | 6/55 | 6/58 | Life | Sum over the 4 games |
|---|---|---|---|---|---|
| Replication z | +0.81 | +0.59 | +0.73 | +2.75 | +4.89 |
| Pairs scoring at least as high | 498 (15%) | 842 (25%) | 778 (23%) | 4 (0.1%) | 24 (0.7%) |

* **As a pick made in advance, it is about a 1-in-140 result,** or about 1 in 70 counting both
  4D leads that were tried. That is unusual, but it comes almost entirely from one game. In the
  three Toto games it is an ordinary pair.
* **No pair is consistently good across games.** The correlation of pairs' replication z
  between any two games is −0.05 to +0.06. If some parameter combinations really steered
  numbers, the same pairs would tend to score well in several games.
* **Other pairs score much higher by chance.** The best real pair over the four games (paksha ×
  solar term, sum +8.01) and the best pair on every shifted calendar (+6.0 to +8.2) are far above
  +4.89.
* **The Magnum Life result depends on the cut-off date.** Learned on the first 70% or 80% of
  draws, z = +2.0 to +3.4 for tickets of 4–12 numbers. Learned on the first 60% (and so tested on
  more draws), z = +0.4 to +1.3. Updated draw by draw, z = +0.83, which is 17% of pairs. A
  stable effect would not depend on where the line is drawn.

So the lead is a genuinely low-probability coincidence, roughly 1 in 70–140, but it is not
evidence of a mechanism. The forward log will show whether it continues.

### Hunting for leads that beat it (`lead_hunt.py`)

If the 4D lead were special, honest ways of picking leads (ways that, like the 4D lead's,
choose without seeing the test draws) should rarely do as well. Seven methods were tried, each
scored with exactly the statistic that gave the 4D lead its result. In this run the lead scored
+2.96 on Magnum Life and +4.70 summed over the four games; tie-breaking noise moves it slightly
from section 6.

| Method | Picks (sets × games) | Mean test z | Best single score | Scores ≥ lead's +2.96 | Best sum over 4 games |
|---|---|---|---|---|---|
| **4D picks:** all 58 sets 4DPrediction chose on 1985–2011 4D data (lead #1 among them) | 232 | +0.07 | +3.10 (yoga × day pillar, 6/58) | 3 | +4.70 (the lead) |
| Within-game, best on validation | 20 | −0.08 | +1.44 | 0 | – |
| Within-game, stable over two validation windows | 20 | +0.03 | +1.18 | 0 | – |
| Transfer: best on the other three games | 20 | +0.27 | +1.85 | 0 | – |
| Pooled validation over all games | 20 | −0.14 | +1.77 | 0 | +1.51 |
| Triples, best on validation (30,000 sampled) | 20 | +0.16 | +2.54 | 0 | – |
| **Random pairs, no selection** | 800 | −0.08 | **+3.40** (Sun nakshatra × Na Yin, 6/50) | 2 | **+6.24** (Sun nakshatra × Na Yin) |

* **Random pairs beat it.** Out of 200 pairs drawn at random, two scored a higher four-game sum.
  The best, Sun nakshatra × Na Yin (+3.40, +0.43, +1.58, +0.84), totals +6.24 against the lead's
  +4.70.
* **Among the 4D picks, the lead's score is what the best of 58 gets by chance.** The 58 sets
  4D picked average +0.07 here, the same as random pairs. For one pick, a four-game sum of +4.70
  is about a 1-in-106 result. For the best of 58 picks it is a **42%** result. Three other 4D
  picks come close (+4.52, +4.39, +4.10). The lead was promoted to "#1" in 4D because it had the
  best 2012–2026 score of those 58, so the fair comparison is with all 58, not with one
  pre-chosen pick.
* **The 4D ranking does not carry over.** Without the lead itself, the correlation between a
  pick's 2012–2026 4D score and its score here is +0.15 over 57 picks (standard error ≈ 0.13).
* **The honest within-game methods** found nothing better (best +2.54 out of 100 picks). That is
  what chance gives 100 picks.

So the lead's result here is matched or beaten by unselected random pairs and by other 4D
picks, and it is about what the luckiest of the 4D picks should score. It is chance.

## 7. Our own lead search: hot, cold, positional and gap patterns (`own_leads.py`)

The leads in section 6 came from the 4D project. This section finds leads from scratch, using
only these games' own history. For each game, and each of the 78 Vedic and Chinese parameters
and their 3,003 pairs, a draw's cell is its value of that set (e.g. "lagna in Mesha & lunar
month 3"). At every draw, using only the **earlier draws of the same cell**, it builds:

| Pattern | What it predicts |
|---|---|
| hot | the k numbers drawn most often in the cell (relative to expected) |
| cold | the k numbers drawn least often in the cell |
| pos | per sorted position (smallest … largest), the number most often seen there in the cell |
| gap | the cell's most common smallest number, then its most common differences to the next number (n2−n1, n3−n2, …) |
| pos_hit | how often the per-position number is exactly right, against the same prediction from all earlier draws ignoring the cell |
| gap_hit | the same for the per-position differences |

Positional and gap distributions are smoothed towards the unconditioned ones (5 pseudo-draws).
Draws are split into early (25–50%), validation (50–70%) and test (70–100%) periods.

The selection rules were committed (11db295, before the test was read):
* **best valid:** the highest validation z, per pattern and per family (Vedic, Chinese,
  Vedic × Vedic, Chinese × Chinese, Vedic × Chinese, all).
* **stable:** the highest min(early z, validation z), same breakdown.
* **my lead:** per game, the stable rule over the four ticket patterns.

The whole search was repeated on 8 shifted calendars, to show what the selected leads score when
no real link exists. That is 3,081 sets × 6 patterns × 4 games × 9 calendars.

**My leads (one per game), chosen on early + validation only:**

| Game | Lead | Pattern | Early | Validation | **Test** |
|---|---|---|---|---|---|
| 6/50 | lagna rashi × lunar month | hot | 310 / 257.8 (1.20×, z +3.66) | 237 / 205.9 (1.15×, +2.44) | **302 / 309.6 (0.98×, −0.49)** |
| 6/55 | karana × adhika masa | hot | 511 / 467.3 (1.09×, +2.25) | 422 / 373.1 (1.13×, +2.82) | **502 / 560.9 (0.90×, −2.77)** |
| 6/58 | Rahu rashi × Saturn retrograde | pos | 468 / 428.9 (1.09×, +2.09) | 383 / 343.2 (1.12×, +2.37) | **487 / 515.2 (0.95×, −1.37)** |
| Life | nakshatra pada × day officer | pos | 323 / 295.1 (1.09×, +2.06) | 354 / 314.7 (1.12×, +2.81) | **528 / 517.3 (1.02×, +0.59)** |

(numbers matched / expected for fair tickets.) All four looked good in two separate periods and
then dropped to chance, or below it, on the test draws. The same rule applied to shifted
calendars gives test z between −1.4 and +2.3, so a lead that is "good twice" is what a search of
12,000 candidates per game produces by luck.

**All selected leads.** That is 4 ticket patterns × 6 families × 2 rules, so 48 leads per game:

| Game | Best-valid leads, test z mean (sd) | Stable leads | Same rules on shifted calendars |
|---|---|---|---|
| 6/50 | −0.36 (0.73) | −0.01 (1.06) | +0.05 / +0.04 |
| 6/55 | −0.55 (0.79) | −0.40 (1.22) | +0.03 / −0.06 |
| 6/58 | −0.27 (1.01) | −0.27 (1.05) | −0.21 / −0.21 |
| Life | −0.12 (1.00) | −0.23 (0.83) | +0.01 / −0.14 |

A real effect would put the selected leads above zero, and above the shifted ones. They are at
or below both. The best validation z of the real search (2.8–4.3 for the ticket patterns) is the same size as
the best of the shifted searches (2.7–3.7 on average).

**Does validation predict the test at all?** Across all 3,081 sets, the correlation between a
set's validation z and its test z is −0.11 to +0.08 for the ticket patterns. That matches the
shifted calendars (−0.14 to +0.07). The only sizeable correlations are for pos_hit and gap_hit,
and they are just as large on shifted calendars. They measure how much the cell size hurts
those predictions, not astrology.

**Positions and gaps.** Predicting the number at each position, or the gap to the next number,
from the cell is *worse* than ignoring the cell: on average across sets, z −0.9 to −3.6 against
the unconditioned prediction, the same as on shifted calendars. For example, my Supreme Toto
lead's positional predictions hit 252 times on the test draws against 308 for the unconditioned
ones. Cells hold few draws, and their "most common" value is mostly noise.

One selected lead did well on the test: Magnum Life, best-valid positional, Moon rashi ×
samvatsara, z +2.19. It is 1 of 48 selected leads per game, and the rest average below zero.

### Comparison with the earlier leads

All scores are on the same test draws, as z against fair tickets:

| Lead | 6/50 | 6/55 | 6/58 | Life |
|---|---|---|---|---|
| **My leads (this section)** | −0.49 | −2.77 | −1.37 | +0.59 |
| 4D lead, Mercury nakshatra × Venus rashi, static ticket (section 6) | +0.81 | +0.59 | +0.73 | +2.75 |
| Same 4D lead, walk-forward hot ticket (this section's method) | +0.16 | −0.68 | +0.22 | +0.83 |
| Astrology formulas, best of 4 per game (section 4) | +1.15 | +0.28 | +0.39 | +1.31 |
| Earlier walk-forward best pair (section 2) | −0.58 | −0.94 | +1.32 | −1.29 |

My own leads did **not** beat the earlier ones. They scored lower on the test draws, but every
row is within the spread expected from selection luck. The 4D lead's Magnum Life +2.75 depends on
how its ticket is built: it is +0.83 when the ticket is updated draw by draw like every other
lead here. Tickets for my leads on 18 and 21 Oct are logged as `own_lead` in `forward_log.csv`.

## 8. Word vectors and a small language model (`embed_model.py`)

Inspired by word embeddings ("king − man + woman = queen"): each draw is a sentence of tokens, the 83 parameter values
of its date and time plus the numbers drawn. Two models per game, numpy only:

* **PPMI + SVD** (mathematically equivalent to word2vec): token co-occurrence within draws, positive PMI with context
  smoothing, truncated SVD (10, 30 or 100 dimensions, chosen on validation). A date's ticket = the numbers whose vectors
  are closest (cosine) to the sum of its parameter vectors.
* **Neural language model** (fastText-style): the date's parameter tokens are embedded and averaged, and a softmax
  over number tokens is trained (Adam, L2, early stopping on validation). A second variant adds the previous draw's
  numbers to the context, like the previous words an LLM reads.

Protocol per game: the last 10 draws kept aside; settings chosen on R[0–60%] → R[60–80%]; tested on R[80–100%] after
retraining on R[0–80%]; then retrained on all of R and used on the last 10. Everything repeated on 5 shifted calendars.
Results are in FINDINGS.md and `embed_results.json`.

**What the vectors learn.** Where 100 dimensions were chosen (6/58, Magnum Life), the parameter vectors recover real
structure: Moon in Vrishabha − Rohini + Ashwini ≈ Moon in Mesha (Ashwini lies in Mesha); Jupiter in Karka's nearest
token is Jupiter in Ashlesha (a nakshatra inside Karka); the Jia Zi day sits next to Na Yin 0 (its own Na Yin). Number
tokens, however, only sit next to the most common tokens (flags such as "not retrograde", "planets with Moon = 0"),
because they co-occur with everything about equally. In the 10-dimension spaces (6/50, 6/55) nearly all tokens are at
cosine 0.95–0.98 of each other.

**What it predicts.** Nothing beyond chance. PPMI tickets land within the range of the shifted calendars in every game.
The neural model never achieves a validation loss below "all numbers equally likely", so early stopping halts it after
5–20 epochs; its tickets are identical on shifted calendars (6/55: z +1.72 every time), i.e. they follow overall number
frequency, not the parameters. On the test draws every language model fits the results worse than uniform.

### Using the analogy itself as the forecaster (`analogy_model.py`)

"King − man + woman = queen" as a predictor: numbers(today) ≈ numbers(A) − conditions(A) + conditions(today), with
the astrology term weighted by λ and A a past draw (previous draw, or the 10 most similar earlier draws), or a learned
condition→numbers map ("direction" vectors fitted by ridge regression). λ ∈ {0, 0.5, 1, 2} and the dimensions were
chosen on validation draws; λ = 0 would mean the astrology term does not help. Validation chose λ = 0 in 5 of 12
settings; test scores (z −0.84 to +2.20 over 16 method × game results) and ranking quality (AUC 0.487–0.509) are
inside the shifted-calendar range (z −2.51 to +2.37, AUC 0.491–0.514). The two best scores (6/50 +2.20, Life +1.83)
are what the best of 16 tries gives by chance, and the 6/50 one has the astrology term switched off. Details in
FINDINGS.md and `analogy_results.json`.

## Conclusion

The Toto and Magnum Life draws are fair for practical purposes. Vedic, KP and Chinese almanac
conditions, single or paired, carry no information that survives on later draws. That holds
for the formulas built from them, and for hot, cold, positional and gap patterns found
by our own search. The one surviving lead (from the 4D project) is a small effect that is not
significant once selection is accounted for. It also weakens when scored draw by draw.

## Reproduce

```sh
python3 analysis/common.py                # rebuild data/astro_params.csv (~6 s)
python3 analysis/fairness.py              # ~40 s
python3 analysis/conditional.py           # ~1 min on 4 cores
python3 analysis/numerology.py            # ~3 s
python3 analysis/astro_model.py tune      # rewrites the frozen formulas: only to re-tune
python3 analysis/astro_model.py test      # ~2 min
python3 analysis/lead_4d_check.py
python3 analysis/own_leads.py             # ~15 min on 4 cores
python3 analysis/lead_4d_robustness.py    # ~30 s, after own_leads.py
python3 analysis/lead_hunt.py             # ~1 min (reads ../4DPrediction for the 4D picks)
python3 analysis/embed_model.py           # ~25 min on 4 cores
python3 analysis/astro_model.py predict --date 2026-10-21
```

numpy only. After adding new draws to `data/raw/` and running `scripts/build_csv.py`, run
`python3 analysis/common.py` to extend the parameter table.
