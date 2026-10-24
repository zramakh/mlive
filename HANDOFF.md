# Handoff: state of the research (read this first)

Last updated 2026-10-24. Branch `claude/focused-franklin-ajsdm9`. Results data run to the **2026-10-24** draw
(Magnum Life 439/26, Sports Toto 6202/26). Full history of questions and answers:
[docs/conversation.md](docs/conversation.md). Detailed summary of every test: [analysis/FINDINGS.md](analysis/FINDINGS.md).

## 1. The question and the bottom line

Can Vedic / KP / Chinese astrological parameters of the draw date (19:00 Malaysia time) predict Magnum Life 8/36 (+2
bonus), Star Toto 6/50 (+1 bonus), Power Toto 6/55, Supreme Toto 6/58?

**Answer so far: no method has beaten chance on draws it was not chosen on.** Every apparent lead appears just as
often when the parameter values are rolled against the draws (shifted calendars). Two small effects survive the
fair tests (section 4), both small and still losing money.

## 2. Method conventions (keep these so results stay comparable)

- **Lead** = one parameter or a pair (or triple) × a **pattern**. The draw's "cell" = all earlier draws with the same
  parameter value(s); numbers are ranked from that cell using **earlier draws only**.
- **7 patterns** (`lead_full.py`, `fair_oos.scores`): hot, cold, pos (positional), hot+100, cold+100 (−zc − hot100),
  hot/cold100 (zc − hot100), cold/hot100 (−zc + hot100). hot100 = the number's z over the last 100 draws.
- **History windows**: all (default), last_round, last1, last5, last10, decay10 (`lead_full.window_ex`; pattern
  string "hot@last5").
- **Formats** and official prizes: Magnum Life 10 tickets / System 10 / System 9 × 2 overlap / disjoint; Toto 10 sets /
  System 7 × 2 overlap / disjoint / System 8 (`profit_rank.py`, `toto_profit.py`, `toto_full.py`, `watch_score.SYS`).
- **Main sensitive measure** (all recent tests): drawn numbers in the lead's top ticket (8 Magnum Life, 6 Toto) vs exact
  chance k·k/n, hypergeometric spread → ratio and z.
- **Luck checks**: shifted calendars (np.roll of the parameter codes, ≥160 draws); for date rules, the same rule centred
  on other dates. **Fair test** (`fair_oos.py`): before each year, the top 1% of leads on earlier years only are
  "chosen" and scored blind that year. Everything new should pass this before being called a lead.
- Parameter families are added with `enable()` hooks that append columns after the 114 base parameters
  (`d9.py` → `vargas.py` → `chinese_div.py`); newer ones are CSV tables read by `family_fair.py` / `watch_score.lead_cols`.

## 3. What has been tested (do not redo; verdict = chance unless noted)

| Area | Scripts | Report |
|---|---|---|
| Fairness of the draws, hot/cold/recency, numerology, kernels, embeddings, analogy | fairness, recency, hot_window, numerology, astro_model, embed_model, analogy_model | FINDINGS.md |
| 114 base parameters, singles + pairs × 7 patterns × 4 formats, profit / high hits / 20 shifted calendars | lead_full, profit_rank, toto_full, high_hits_null | LEADS7_*.md, PROFIT_*.md, TOTO_*.md |
| History windows | lead_full --window | WINDOWS_COMPARE*.md |
| D9 navamsa; divisional charts D2-D60 | d9, vargas, *_report | D9_REPORT.md, VARGAS_REPORT.md |
| Da Liu Ren, Mei Hua Yi Shu, Tai Yi Shen Shu | chinese_div (kinliuren, kintaiyi) | CHINESE_DIV_REPORT.md |
| Tai Yi / Mei Hua numbers played directly | number_rules_cn | NUMBER_RULES_CN.md |
| Exact positions, muhurta (Rahu Kalam, choghadiya, void Moon, eclipses, stations), transits to each game's first-draw chart, triples of base parameters | astro_more, family_fair | FAMILY_FAIR_*.md |
| Shadbala (simplified) and Ashtakavarga | strength, family_fair strength | FAMILY_FAIR_STRENGTH.md |
| Draw shape (sum, odd, high, consecutive) by astrology | shape_astro | SHAPE_ASTRO.md |
| Value combinations inside leads ("cells", e.g. Tula × Swati); persistence | lead_cells, cells_all | LEAD_CELLS.md, CELLS_ALL.md |
| Consistency like the 4D Karana × Day pillar lead | consistency | CONSISTENCY.md |
| Fair yearly re-choice of all leads | fair_oos, fair_oos_pool | FAIR_OOS.md |
| Same-date repeats, solar and lunar, 7 patterns | seasonal, seasonal_check, seasonal7 | SEASONAL*.md |
| Star lunar rule: ticket plans, windows, fair choice | lunar_rule_10, lunar_tickets, lunar_opt | LUNAR_*.md |
| Combining observed leads | combine_leads | COMBINE_LEADS.md |
| 4D project's ranked leads applied to lotto | leads4d_lotto | LEADS4D_LOTTO.md |

## 4. What survived (the only things worth following)

1. **Star Toto same-lunar-date effect**: numbers drawn most within ±3-15 days of the same Chinese lunar date in earlier
   years (hot, pos, hot/cold100 patterns) beat chance (z +2 to +3.8), the real date ranks 1-4 of 60 dates, every year
   2018-2026 above chance at ±7. Window chosen after a first scan. Still loses money: fair walk-forward return about
   RM0.26-0.31 per RM1 (other dates 0.17). Moon Shadbala leads in Star (moon_phase × sb_moon) are probably the same effect.
2. **Magnum Life mars_rashi × month (cold)**: best blind record in the fair test (picked in advance 2022-2026, ×1.073,
   z +3.5), slightly above shifted calendars; its triples top the triples test.
3. Weaker: Supreme day_of_month × aspect_venus_mars (cold/hot100), Star lagna_rashi × lunar_month (pos), Power karana ×
   aspect_mercury_jupiter (hot/cold100), Magnum Life rahu_nakshatra × aspect_moon_venus (cold/hot100).

Picking leads by past record in general does **not** work: leads chosen before each year score ×0.99-1.00 the next
year in every family. Combining leads makes them weaker.

## 5. Frozen observation lists (do not change them; judge after about 50 draws from 2026-10-24)

- **Short list** (`watch_score.SHORTLIST`, WATCHLIST.md "Short list"): the 9 leads ranked in section 4 plus Power
  year_stem × lagna_navamsa_lord (cold) and Supreme plum_trigrams × saturn_navamsa (hot/cold100); the lunar rule is the
  pseudo-lead `lunar_date` with pattern `hot/cold100@7`. WATCH_LOG.md has the running hits-vs-chance table.
- **Watchlist** (`watch_score.WATCH`, 86 entries) - the user wants every tier reported.

## 6. Routine after each draw

1. Get the results (4dnow.app or 4dmoon.com; check draw numbers follow on), append to `data/*.csv`.
2. `python3 analysis/watch_score.py DATE` (scores watchlist + short list → watch_log.csv, WATCH_LOG.md);
   `python3 analysis/lead_today.py DATE` (all leads on the draw).
3. Numbers for the next draw: `python3 analysis/watch_predict.py DATE` (PREDICT_DATE.md), `consensus.py DATE`.
4. Commit and push. A scheduled update is set for 2026-10-24 21:30 MYT in the original session (may not carry over).

## 7. Open ideas not yet tested

- Machine / ball-set bias in shorter periods (the only real effect 4D ever found was a 2019-2025 Magnum digit bias).
- Machine-learning models (gradient boosting, nearest similar days, small neural net) on all parameters at once.
- Change-point, autoregression and gap (hazard) models of the numbers.
- 4D results of the same evening as predictors of the lotto numbers.
- Full Shadbala (Drik bala, Kala bala, speed-based Chesta) instead of the simplified version.
- Check the two exact repeat draws in Star data (2017-11-07 = 2022-05-07; 2024-01-21 = 2026-06-03) against official
  results.

## 8. Environment notes

`pip install -r requirements.txt` (kinliuren / kintaiyi only needed to rebuild `data/astro_params_chinese_div.csv`).

On Windows set `PYTHONUTF8=1` (or run `python -X utf8 ...`): the scripts open files without an explicit encoding, and the
Chinese-chart table and the `×` in lead names need UTF-8.
`analysis/profit_arrays/` (git-ignored, several GB) holds working arrays; every one is rebuilt by its script. Long jobs:
`analysis/runs/`. The 4D sister project: github.com/zramakh/4DPrediction (branch claude/4d-results-scraper-9ptbd5).
