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

## Conclusion

The Toto and Magnum Life draws are fair for practical purposes. Vedic, KP and Chinese almanac
conditions, single or paired, and the formulas built from them carry no information that
survives on later draws. The one surviving lead is a small effect that is not significant once
selection is accounted for.

## Reproduce

```sh
python3 analysis/common.py                # rebuild data/astro_params.csv (~6 s)
python3 analysis/fairness.py              # ~40 s
python3 analysis/conditional.py           # ~1 min on 4 cores
python3 analysis/numerology.py            # ~3 s
python3 analysis/astro_model.py tune      # rewrites the frozen formulas: only to re-tune
python3 analysis/astro_model.py test      # ~2 min
python3 analysis/lead_4d_check.py
python3 analysis/astro_model.py predict --date 2026-10-21
```

numpy only. After adding new draws to `data/raw/` and running `scripts/build_csv.py`, run
`python3 analysis/common.py` to extend the parameter table.
