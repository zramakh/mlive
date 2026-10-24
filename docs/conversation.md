# Conversation log (this analysis session)

Questions and answers in order, from the session transcript. Tool calls, tool output and system notices are left out.

---

**User:**

> Firstly scrape using tiny fish [www.loto-8.com](https://www.loto-8.com) for all the results of STAR TOTO 6/50, POWER TOTO 6/55, SUPREME TOTO 6/58 and 	Magnum life all the available historical results and save it into mlive repo

**Answer:**

Let me look at the site structure first.

**Answer:**

The domain `loto-8.com` doesn't resolve; the actual site is `www.lotto-8.com`. Exploring it.

**Answer:**

Pages are fetchable via TinyFish. Let me check page counts for each game and whether a larger page size exists.

**Answer:**

Page counts: 6/50 → 63, 6/55 → 125, 6/58 → 122, Magnum Life → 59. Let me check whether large tool outputs are persisted to disk (so I can parse rather than retype).

**Answer:**

TinyFish output isn't saved to disk, so I'll transcribe each batch into compact raw files and convert to CSV with a script at the end. Starting with Star Toto 6/50 pages 54–63.

**Answer:**

Correct count (9×23+11). Adding the page-1 data I already fetched for all four games.

**Answer:**

Next: Star Toto 6/50 pages 44–53.

**Answer:**

Progress: 931 of ~1,450 Star Toto 6/50 draws captured (pages 1, 24–63 done). Continuing with pages 14–23.

**Answer:**

Pages 12–13 remain for 6/50; I'll fetch them along with Power Toto 6/55 pages 2–9.

**Answer:**

Star Toto 6/50 complete (1,437 draws, matches 62×23+11). Power Toto 6/55: pages 1–9 done. Continuing.

**Answer:**

Committing progress so far, then continuing with 6/55 pages 30–39.

**Answer:**

Push succeeded (branch tracks origin). 6/55 at 897 draws; next pages 40–49.

**Answer:**

Still scraping: Power Toto 6/55 at 1,587 draws (pages 1–69 of 125, back to Dec 2016). Continuing with pages 70–79.

**Answer:**

6/55 now at 2,277 draws (back to Feb 2013). Fetching pages 100–109.

**Answer:**

Last 6/55 batch (pages 120–125), plus Supreme 6/58 pages 2–5.

**Answer:**

Power Toto 6/55 complete (2,855 draws = 124×23+3, back to Oct 2009). Committing, then Supreme 6/58.

**Answer:**

Supreme 6/58 at 805 draws (pages 1–35 of 122). Continuing with pages 36–45.

**Answer:**

Supreme 6/58 at 1,495 draws (pages 1–65, back to Jun 2017). Continuing with pages 66–75.

**Answer:**

Supreme 6/58 at 2,185 draws (to Aug 2013). Fetching pages 96–105.

**Answer:**

Last 6/58 pages (116–122), plus Magnum Life pages 2–4.

**Answer:**

Supreme 6/58 complete (2,786 = 121×23+3, back to Mar 2010). Magnum Life: pages 1–4 done; fetching 5–14.

**Answer:**

Magnum Life at 782 draws (pages 1–34 of 59). Fetching 35–44.

**Answer:**

Final Magnum Life pages (55–59).

**Answer:**

I scraped every available draw for all four games from the site with TinyFish and pushed them to `mlive` on branch `claude/focused-franklin-ajsdm9`.

The address you gave, `www.loto-8.com`, doesn't resolve, so I used the actual site, `www.lotto-8.com`.

| Game | Draws | Date range | File |
| --- | --- | --- | --- |
| STAR TOTO 6/50 | 1,437 | 2017-10-21 → 2026-10-17 | `data/star_toto_6_50.csv` (6 numbers + bonus) |
| POWER TOTO 6/55 | 2,855 | 2009-10-31 → 2026-10-17 | `data/power_toto_6_55.csv` |
| SUPREME TOTO 6/58 | 2,786 | 2010-03-20 → 2026-10-17 | `data/supreme_toto_6_58.csv` |
| Magnum Life 8/36 | 1,346 | 2018-04-25 → 2026-10-17 | `data/magnum_life.csv` (8 numbers + 2 bonus) |

Each CSV has `draw_date`, `day` and the numbers, sorted oldest first. The site only goes back to 2017 for STAR TOTO 6/50 and 2018 for Magnum Life.

**One thing to know:** TinyFish returned the pages only as text to me, so I retyped every draw into `data/raw/` myself. A script, `scripts/build_csv.py`, then checks the data and builds the CSVs. These checks all pass:
- Each game's draw count matches the site's page count exactly (23 draws per page).
- Every date is valid and falls on a draw day (Wed, Sat, Sun, or a Tuesday special draw).
- No duplicate dates, out-of-range numbers, or repeated numbers within a draw.
- The draw dates line up across the four games, which share a schedule.

These checks can't catch a mistyped number that is still in range, and I didn't re-check the numbers against a second fetch. Spot-check a few draws against the official results before relying on them.

**Errors on the site itself, kept as published** (also listed in `data/README.md`):
- POWER TOTO 6/55 has no draw for 2023-04-05, though the other games drew that day.
- The 2017-01-01 POWER TOTO 6/55 numbers are listed out of order.
- Magnum Life shows identical results on back-to-back dates three times in 2025 (22/23 Feb, 26/29 Mar, 26/27 Apr). These look like the site's own errors, so check them against Magnum's official results.

---

**User:**

> for the errors you may check them by searching them through other webpages

**Answer:**

lottolyzer.com and gidapp.com both have per-draw history. Fetching the six Magnum Life dates in question from gidapp:

**Answer:**

gidapp blocks bots. Trying lottolyzer's Magnum Life history instead:

**Answer:**

Markdown dropped the numbers (they're probably styled elements). Retrying page 6 as HTML:

**Answer:**

April 26 matches; **April 27** differs on lottolyzer. Now the two Power Toto 6/55 items:

**Answer:**

That slug returned the wrong game (numbers only go up to 45). Looking up lottolyzer's real URL for Power Toto:

**Answer:**

The slug is `power-toto`:

**Answer:**

Lottolyzer serves 50 rows per page whatever I ask for, so I'll use its draw numbers to find the right pages:

**Answer:**

Both draws found. I'll apply the fixes and check the neighbouring rows against my data.

**Answer:**

The neighbouring rows match lottolyzer. Now I'll update the README and push.

**Answer:**

I checked each error I'd reported against lottolyzer.com and fixed all of them in the mlive repo. The changes are pushed to `claude/focused-franklin-ajsdm9`.

| Game | Date | What lotto-8.com had | Fixed to |
| --- | --- | --- | --- |
| Power Toto 6/55 | 2023-04-05 | Missing | `04 29 32 39 41 48` |
| Power Toto 6/55 | 2017-01-01 | `04 09 08 44 46 50` | `04 08 09 44 46 50` (same numbers, just put in order) |
| Magnum Life | 2025-02-23 | A copy of the 22 Feb result | `02 05 10 11 17 18 34 35` with bonus `08 29` |
| Magnum Life | 2025-03-29 | A copy of the 26 Mar result | `02 12 23 24 27 33 34 35` with bonus `01 08` |
| Magnum Life | 2025-04-27 | A copy of the 26 Apr result | `06 09 10 13 16 19 25 34` with bonus `07 31` |

- **Magnum Life:** in all three pairs, the earlier date's result was correct. lotto-8.com had copied it onto the next draw.
- **Power Toto 6/55:** now has 2,856 draws. The other games' counts are unchanged.
- **Tuesday draws:** the two Magnum Life draws on 2018-06-19 and 2018-08-14 are real special draws, so I kept them.
- **Rebuild:** I regenerated the CSVs and they passed all the validation checks. The draws next to the 2023 and 2017 fixes also match lottolyzer.
- **README:** `data/README.md` now has a table of these corrections with the lottolyzer draw numbers, replacing the old "Quirks" section.

These fixes are checked against only one other site. The other site I tried, gidapp.com, blocks automated access.

---

**User:**

> OK now if you look at the 4d repo there's certain astrological analysis that was done to create a predictive model, i want you to do a similar analysis to create a predictive model, and all the analysis and data must be saved in mlive repo

**Answer:**

Now I'll write the shared loader and parameter table for mlive.

**Answer:**

Parameter table built (2,978 dates × 83 parameters). Next, the baseline fairness tests: are the draws uniform and independent before any astrology is applied?

**Answer:**

The shifted runs recompute a per-draw loop each time, which is too slow. I'll hoist it out of the loop.

**Answer:**

The formulas are tuned and frozen. As the 4D repo did, I'll commit them before running the forward test, so the test can't influence which formula was chosen.

**Answer:**

Now the write-up: a findings summary, a full report, and a root README.

**Answer:**

I'll check the draw counts quoted in the report against the results files.

**Answer:**

Now the short findings file and a root README.

**Answer:**

I ran the 4D repo's astrology analysis on the four games, and none of the astrology-based models picked numbers better than random on draws they hadn't seen. Everything is saved in the mlive repo and pushed to `claude/focused-franklin-ajsdm9`. Start with `analysis/FINDINGS.md`; the full write-up is `analysis/REPORT.md`.

**What I did**
- **Astrology parameters:** I copied the 4D repo's ephemeris, Vedic, KP and Chinese almanac code unchanged and computed 83 parameters for every draw date at 19:00 Malaysia time. They are saved in `data/astro_params.csv`.
- **Testing method:** for each game, the oldest 50% of draws were used for counting, the next 20% for tuning, and the newest 30% for testing. I committed the tuned formulas before running the test, so the test couldn't influence them. Where many things were tried at once, I compared the results with the same scan run on a deliberately misaligned calendar, which shows how good the best result looks by pure luck.

**Results**
- **Fairness:** all four games behave like fair draws. There are no hot or cold numbers beyond normal luck, no weekday effect, and no repeats from the previous draw. Star, Power and Supreme Toto drawn on the same evening don't share numbers more than chance.
- **Single parameters and pairs** (83 single, 3,403 pairs): the real calendar looks the same as the misaligned ones. When each condition's favourite numbers were learned on older draws and replayed on newer draws of the same condition, they matched 0.985–1.008 times as often as random.
- **Numerology (planet numbers):** there was a small excess of results that passed the threshold, but it wasn't in the predicted direction and disappeared on the newer draws.
- **Prediction formulas** (Vedic-only, Chinese-only, combined, and a "similar days" model): they looked 5–37% better than chance on the draws they were tuned on. On the newer draws they scored 0.94–1.06 times random, and every one of them fitted the real results worse than "all numbers equally likely".

**One lead worth watching**

The 4D repo's top pattern, Mercury's nakshatra × Venus's rashi, was chosen on 4D data, so it's a fair test here. On Magnum Life it gives about 1.94 matching numbers per ticket against 1.78 expected (z = +2.75, top 0.1% of all pairs). It holds in both halves of the newest draws and is slightly positive on all three Toto games. But it was the best of 8 checks (p ≈ 0.02 after allowing for that), it doesn't show up in the other statistic for the same pattern, and it's far too small to change the jackpot odds.

**Picks for the next draws**

I logged picks for 18 and 21 Oct for all four games before the draws, in `analysis/forward_log.csv`. Once the results are added to `data/`, `python3 analysis/astro_model.py score` checks them. For picks on any later date, run `python3 analysis/astro_model.py predict --date YYYY-MM-DD`.

---

**User:**

> I feel like you cheated by analyzing the previous leads from 4d, you need to do the analysis yourself based on your own method, probably which number appears often or rarely at certain parameters, what number tend to appear at that particular position, what is the difference of one number with the neihbouring number and etc, from single parameter or pair for vedic, chinese or combination, and check if they perform better than your own leads

**Answer:**

You're right: borrowing 4D's leads was a shortcut. I'll build my own lead search. For every Vedic, Chinese and combined parameter and pair (78 singles + 3,003 pairs, per game), it will test four ways of building a ticket from that condition's history, plus two direct prediction checks:

- **Hot:** the numbers that appear most often under that condition.
- **Cold:** the numbers that appear least often.
- **Position:** the number that most often appears at each sorted position (smallest, 2nd, … largest).
- **Gap:** the most common difference between neighbouring numbers, chained from the predicted smallest number.
- **Direct hit-rate checks:** how often the position and gap predictions are exactly right, compared with the same prediction made without the condition.

Everything is walk-forward. Leads are chosen only on older draws, then scored on the newest 30%. The whole search is also rerun on shifted calendars to show what "the best lead" looks like by luck. Finally I'll compare the results with the earlier leads.

**Answer:**

The search is running. I'll wait for it to finish.

**Answer:**

The search is still running in the background; I'll pick up the results when it finishes.

**Answer:**

The lead-search script is now committed and pushed, so its selection rules are on record before any test results come in. The search itself is still running in the background (about 20 minutes). When it finishes I'll commit the results, compare them with the earlier leads, and log the new leads' tickets for 18 and 21 Oct.

**Answer:**

Now the write-up of the new lead search and the comparison with the earlier leads.

**Answer:**

I ran my own lead search from scratch, and my leads did not beat the earlier ones: all four fell to chance on the newest draws. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`. The details are in section 7 of `analysis/REPORT.md` and the summary in `analysis/FINDINGS.md`.

**What I tested.** For each game, I took every Vedic and Chinese parameter (78) and every pair of them (3,003), alone or combined. For each, I built predictions using only earlier draws that had the same value:
- **Hot:** the numbers that come up most often under that condition.
- **Cold:** the numbers that come up least often.
- **Position:** the number that most often appears at each sorted position (smallest, 2nd, … largest).
- **Gap:** the most common smallest number, then the most common differences to the next number.
- **Position and gap accuracy:** how often those per-position predictions are exactly right, compared with the same prediction made without the condition.

Leads were chosen using only older draws, and I committed the rules for choosing them before looking at the newest 30%. I then reran the whole search on calendars shifted out of line with the draws, to see what the "best lead" looks like by pure luck.

**My leads.** Each looked good in two separate older periods (z +2 to +3.7), then dropped on the newest draws:

| Game | Lead | Older draws | Newest draws |
|---|---|---|---|
| Star Toto 6/50 | lagna rashi × lunar month, hot | 1.20× and 1.15× chance | 0.98× (z −0.49) |
| Power Toto 6/55 | karana × adhika masa, hot | 1.09× and 1.13× | 0.90× (z −2.77) |
| Supreme Toto 6/58 | Rahu rashi × Saturn retrograde, position | 1.09× and 1.12× | 0.95× (z −1.37) |
| Magnum Life | nakshatra pada × day officer, position | 1.09× and 1.12× | 1.02× (z +0.59) |

**Comparison with the earlier leads** (newest draws, z):

| Lead | 6/50 | 6/55 | 6/58 | Life |
|---|---|---|---|---|
| My new leads | −0.49 | −2.77 | −1.37 | +0.59 |
| 4D lead, Mercury nakshatra × Venus rashi | +0.81 | +0.59 | +0.73 | +2.75 |
| Same 4D lead, rebuilt draw by draw like my leads | +0.16 | −0.68 | +0.22 | +0.83 |
| Best astrology formula per game | +1.15 | +0.28 | +0.39 | +1.31 |

My leads came out lower, but every row is within the range that luck in picking a lead produces.

**What else the search showed:**
- **Picking the best doesn't help.** All the leads the rules selected (48 per game) average below zero on the newest draws, about the same as leads picked the same way from the shifted calendars.
- **Past performance didn't carry forward.** How well a pattern did on the older draws had essentially no relationship (correlation −0.11 to +0.08) with how it did on the newest draws, the same as on the shifted calendars.
- **Conditions make position and gap predictions worse.** Predicting the number at a position, or the gap to the next number, under a condition is less accurate than ignoring the condition (z −0.9 to −3.6), and equally so on shifted calendars. Each condition has too few draws, so its "most common" value is mostly noise.
- **The 4D lead is weaker than it first looked.** Its Magnum Life +2.75 depends on how its ticket is built: when the ticket is updated draw by draw like every other lead, it drops to +0.83.

My leads' tickets for 18 and 21 Oct are logged as `own_lead` in `analysis/forward_log.csv`, alongside the earlier picks. Once those results are added to the data, `python3 analysis/astro_model.py score` checks them.

---

**User:**

> wait, like does this proof that 4D lead, Mercury nakshatra × Venus rashi is a real thing? how is that even possible? this is stunning

**Answer:**

No, it doesn't prove that. The +2.75 is the kind of number that turns up by luck when you check enough things.

**Why it isn't proof:**

1. **It's the best of several checks, and of a much larger project.** I scored two 4D leads on four games, which is 8 checks, and +2.75 was the best one. Allowing for that, the chance of seeing it by luck is about 2%. Across both repos we've run tens of thousands of tests, so a 1-in-50 result is expected somewhere.

2. **It mostly disappears when the ticket is built differently.** Scored the original way, the ticket is learned once from the older draws and then frozen; that gives +2.75. Rebuilt draw by draw, it also learns from each new draw as it arrives, and the score drops to +0.83. If the effect were real, learning from more data should make the ticket better, not worse.

3. **A closely related test shows nothing.** If this cell really favoured certain numbers, two draws in the same cell would share numbers more often than chance. They don't (z +0.74, and −0.09 on the older draws).

4. **It isn't the same signal as in 4D.** There it was positional hot digits in 4-digit numbers, not lotto numbers, and it had faded there since 2019.

5. **The effect is tiny even if real:** 1.94 matching numbers per Magnum Life ticket instead of 1.78. That doesn't change jackpot odds of 1 in 30 million in any useful way.

**Is there any way it could be real?** Not through the planets: the balls and drums have no physical connection to where Mercury and Venus appear in the sky. The one ordinary route would be a time effect. Venus changes rashi about monthly and Mercury changes nakshatra every week or two, so each cell is a set of short calendar windows. If the draw machine drifted over time, those windows could pick that up. But the shifted-calendar comparison keeps exactly that structure and gives SD ≈ 1 with no excess, so drift doesn't explain it either. What remains is luck.

**What it is:** a leftover worth tracking, not a discovery.

**How to settle it:** keep scoring its live tickets, since no future draw has influenced it. At this effect size it would take about 170 Magnum Life draws, a bit over a year, to tell it apart from chance with any confidence. A single good or bad draw on 18 or 21 Oct won't mean anything either way.

---

**User:**

> i mean because you couldnt find any other leads better than that was found from 4d, and this game and 4d game is not related at all, the chances are sooo low especially with that many parameters and also the 4d lead is a combination of parameter

**Answer:**

You're right to push on this. A pair picked on unrelated 4D data landing in the top 0.1% of 3,403 pairs is a fair argument, and the way to settle it is to measure rather than argue. I'll test the things a real signal would have to show:

1. Is it near the top when its scores in all four games are combined, compared with every other pair?
2. Does any pair score consistently across games?
3. Does it hold up if the ticket size or the date the ticket is learned up to changes?

**Answer:**

You're right that it's unlikely. I measured it properly, and as a pick made in advance it comes out at roughly 1 in 70 to 140. That is unusual, but it's still not proof.

**Where your argument holds.** The pair was chosen on unrelated 4D data, so it's a fair test here. On Magnum Life only 4 of the 3,403 pairs score as high (top 0.1%). Summed over all four games, it ranks 24th of 3,403 (top 0.7%). Allowing for the two 4D leads I tried, that's about a 1-in-70 chance.

**Where it breaks down:**

- **"I couldn't find a better lead" compares hindsight with foresight.** On the newest draws, 3 pairs beat it on Magnum Life. Summed over all four games, 23 pairs beat it, and the best (paksha × solar term) scores +8.01 against its +4.89. Nobody can pick those in advance, including me. My own leads had to be chosen before the test; the comparison only looks bad for them because the 4D lead happened to land well.
- **It comes almost entirely from one game.** In the three Toto games it's an ordinary pair, ranked in the top 15–25%. A real effect from these planet positions should show up in all four games, which are drawn on the same evenings.
- **No pair works across games.** The correlation between how pairs score in one game and in another is about zero (−0.05 to +0.06). If parameter combinations really steered numbers, the same pairs would tend to do well in several games.
- **It depends on where the line is drawn.** Learned on the first 70–80% of draws, it gives z = +2.0 to +3.4. Learned on the first 60%, so tested on more draws, it drops to +0.4 to +1.3. Updated draw by draw, it's +0.83, an ordinary top-17% pair. A real, stable effect wouldn't swing like that with the cut-off date.
- **Rare things happen when this much has been checked.** Across both repos we've run tens of thousands of tests. A 1-in-100 coincidence surfacing somewhere is expected.

**What I make of it:** a genuinely low-probability coincidence, not something that works. There's also no physical route by which Venus's sign could steer the balls in a draw machine, so a result this size can't outweigh that.

**What would change my mind:** if it keeps matching more numbers than chance on Magnum Life draws it has never seen, over roughly the next year (about 170 draws), it would deserve to be taken seriously. Its tickets are already in `forward_log.csv`.

I saved this check as `analysis/lead_4d_robustness.py` and added it to section 6 of `analysis/REPORT.md`. It's committed and pushed.

---

**User:**

> rather than doing that you may find different ways or method to find a better lead to disprove that Mercury nakshatra × Venus rashi is just chance, why dont you find different methods to find somethign that performs better than this

**Answer:**

To be fair, a "better lead" has to be picked the way the 4D lead was: before looking at the test draws. In hindsight, plenty of pairs beat it (24 of 3,403 summed over the four games), but anyone can find those after the fact. So I'll run several different selection methods, each choosing only from data it's allowed to see, score every pick on the same test the 4D lead got, and count how often an honest pick does as well or better.

One check is especially direct: the 4D project ranked many pairs, and Mercury nakshatra × Venus rashi was its #1. If its #2, #3, … #50 do nothing here, the ranking doesn't transfer and #1's score is luck. I'll look at how the 4D repo stored that ranking.

**Answer:**

I found leads that beat it, and the most telling ones came from random pairs with no selection at all. That's strong evidence Mercury nakshatra × Venus rashi is chance.

I scored every pick with exactly the statistic that gave the 4D lead its result. In this run, with slightly different tie-breaking, the 4D lead scored +2.96 on Magnum Life and +4.70 summed over the four games.

**What beat it:**
- **Random pairs:** out of 200 pairs drawn at random, 2 had a higher four-game total. The best, **Sun nakshatra × Na Yin**, totals **+6.24** (+3.40 on Star Toto, +0.43, +1.58, +0.84), against the lead's +4.70. Nobody chose it for any reason.
- **Other 4D picks:** yoga × day pillar scored +3.10 on Supreme Toto, higher than the lead's best single game. Three more 4D picks total nearly as much as the lead: +4.52, +4.39 and +4.10.

**Why it's chance.** The 4D lead was never a single pick made in advance. The 4D project picked 58 parameter sets on 1985–2011 data, then crowned the one that scored best on 2012–2026. So the fair question is how the luckiest of 58 picks does here:
- All 58 average +0.07 here, the same as random pairs (−0.08).
- A four-game total of +4.70 is about 1 in 106 for one pick, but for the best of 58 it happens **42% of the time**.
- How well a pick did in 4D doesn't predict how it does here (correlation +0.15 over the other 57, within noise).

**The honest selection methods** (best on validation, stable over two windows, transfer from the other games, pooled, and triples) produced 100 picks between them. The best scored +2.54 and none reached +2.96, which is what 100 picks give by chance.

The results table is in the 4D-lead section of `analysis/REPORT.md` (`analysis/lead_hunt.py`), and `analysis/FINDINGS.md` now marks the lead as explained by chance. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Sun nakshatra × Na Yin tell me more about this on why is this the best lead?

**Answer:**

Short version: Sun nakshatra × Na Yin isn't a real lead. It's a random pair that happened to land high on the test draws, and I used it only to show that chance alone produces scores like the 4D lead's. I'll pull its numbers to show what it is and how fragile the score is.

**Answer:**

It's not really the best lead. It's the pair that happened to score highest out of 200 picked at random, on one test window, with one random tie-break. It's only in the report as a demonstration that chance alone can beat the 4D lead.

**What the two parameters are:**
- **Sun nakshatra:** which of the 27 nakshatras the Sun is in (sidereal). The Sun spends about 13–14 days in each, on roughly the same dates every year. For example, it's in Chitra until about 23 Oct, then Swati.
- **Na Yin:** one of 30 Chinese "sound elements" of the day pillar. Each covers 2 consecutive days and repeats every 60 days. Sunday 18 Oct is Na Yin 0 (Jia Zi / Yi Chou, "Sea Metal"); Wednesday 21 Oct is Na Yin 2 (Wu Chen / Ji Si, "Big Forest Wood").
- **Together:** a cell means "this 2-week window of the year and this 2-day slot of the 60-day cycle". That gives 810 possible cells, so each one comes up only once every few years.

**Why its score means nothing:**
- **Its tickets are built from almost no data.** When the ticket is learned, a typical cell has only **2 earlier draws** (median 2 in every game). The ticket is "the 6 most frequent numbers" among about 12 numbers that each appeared once, so which 6 get chosen comes down mostly to the random tie-break.
- **The tie-break alone moves its score.** On Power Toto it scored +0.43 in the hunt and −0.72 here, with the same pair, same data and same cut-off; only the tie-breaking differed.
- **It swings with the cut-off date:**

  | Learned on first | 60% | 70% | 80% |
  |---|---|---|---|
  | Star Toto 6/50 | +0.92 | +2.70 | +3.22 |
  | Power Toto 6/55 | +1.26 | −0.72 | +0.70 |
  | Supreme Toto 6/58 | +0.99 | +2.25 | +0.82 |
  | Magnum Life | +1.35 | +1.42 | −0.84 |

- **Built draw by draw**, it ranks in the top 2% of pairs on Star Toto but in the bottom 20% on Magnum Life.
- **Before the test it looked ordinary.** Its validation scores were between −1.08 and +1.77. None of the honest selection methods would have picked it.

**What it does show:** a pair picked at random, using 2-draw tickets, can outscore Mercury nakshatra × Venus rashi when you look afterwards. That's the point it makes in the report, not that it works. Its cells have far less history behind them than the 4D lead's (the 4D lead's logged ticket for 18 Oct drew on 20 earlier draws), which makes it even less believable as a real effect.

I haven't logged tickets for it, because it would just be another chance pick. I can add it to `forward_log.csv` next to the 4D lead if you'd like to watch them side by side.

---

**User:**

> ok i found the issue, you pooled all 4 draws, you need to do separate analysis for each draw and tell me which parameter either single or pair perform well for each of those draws

**Answer:**

A quick correction first: the analyses weren't pooled. Every scan, model and lead search ran separately for each game, with each game's own draws and its own early/validation/test periods. The only pooled figure was the "sum over 4 games", which I added when comparing against the 4D lead.

I can still give you exactly what you're asking for: a separate list for each game of which single parameters and which pairs (Vedic, Chinese, or combined) performed well. I'll rank them by how consistently they did across all three periods of that game's own history, and compare each list with shifted calendars to show how many "consistent performers" chance alone produces.

**Answer:**

Here is each game analysed on its own. I ranked every single parameter and pair by its weakest score across the three periods of that game's history, so a parameter only ranks high if it did well in all three. The analyses were already separate per game; only the four-game sums in the 4D-lead comparison were pooled.

**Most consistent lead per game** (z for early / validation / test periods):

| Game | Best lead | Pattern | Early | Valid | Test |
|---|---|---|---|---|---|
| Star Toto 6/50 | karana × Venus rashi | cold numbers | +1.58 | +1.40 | +1.62 |
| Power Toto 6/55 | year yin/yang × day god | cold numbers | +2.30 | +1.86 | +1.69 |
| Supreme Toto 6/58 | Jupiter rashi × Jupiter retrograde | hot numbers | +1.86 | +1.83 | +1.75 |
| Magnum Life | Moon rashi × Mars combust | position | +1.91 | +1.84 | +1.88 |

**Best single parameters and pairs per game:**

| Game | Hot numbers | Cold numbers | Number at each position | Gap to next number |
|---|---|---|---|---|
| 6/50 | lagna rashi × KP Sun sub lord (+1.24 / +1.98 / +2.60) | karana × Venus rashi | Saturn nakshatra × month Nine Star | samvatsara × month branch |
| 6/55 | paksha × Jupiter retrograde; single: Mars nakshatra (+0.60 / +1.80 / +2.63) | year yin/yang × day god; single: paksha | Venus rashi × Saturn combust | weekday × Jupiter nakshatra |
| 6/58 | Jupiter rashi × Jupiter retrograde; single: nakshatra | Venus combust × 28 mansions | solar term × month stem | day stem × month Nine Star |
| Life | yoga × Mars rashi; single: Moon rashi (test +2.35) | Mars rashi × Venus combust | Moon rashi × Mars combust | yoga × hora lord |

Single parameters are generally weaker than pairs. On their own, Vedic and Chinese parameters perform about the same. The full top-5 lists for every pattern, with all three period scores, are in `analysis/PER_GAME_LEADS.md`.

**Don't read too much into these lists.** I reran the same search on shifted calendars, where the parameters can't possibly be linked to the numbers. It finds about as many consistent performers:

| Game | Sets with z > 1 in all 3 periods | Chance (shifted calendars) |
|---|---|---|
| 6/50 | 33 | 35.6 |
| 6/55 | 40 | 51.9 |
| 6/58 | 46 | 43.3 |
| Life | 18 | 29.1 |
| **Total** | **137** | **160** |

The real calendar produces fewer consistent performers than chance does. The top leads are about as strong as chance's best: on Supreme Toto (+1.75 vs +1.52) and Magnum Life (+1.84 vs +1.48) they edge it slightly, and in the other two games they fall below it.

Out of about 12,000 candidates per game, a handful will always look good in all three periods. Nothing here suggests these particular ones will keep working.

I logged each game's best lead's tickets for 18 and 21 Oct as `per_game_best` in `analysis/forward_log.csv`:

| Game | 18 Oct | 21 Oct |
|---|---|---|
| 6/50 | 04 14 21 26 44 48 | 07 20 24 35 36 44 |
| 6/55 | 13 15 16 26 30 36 | 05 09 19 31 32 43 |
| 6/58 | 15 39 42 44 48 54 | 15 39 42 44 48 54 |
| Life | 01 05 10 17 18 25 30 36 | 01 06 10 13 18 26 31 36 |

The script is `analysis/per_game_leads.py`, and its results are committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> so far what is the best lead that you think needs to be observed?

**Answer:**

If I had to pick one, it's **Moon rashi × Mars combust on Magnum Life**, using the position pattern. I expect it to fall back to chance like everything else so far, but it has the best case of anything found.

**Why this one:**
- **It's consistent.** It matched more numbers than chance in all three periods: 636 vs 599 expected (early), 510 vs 478 (validation) and 758 vs 718 (test). Every other candidate was strong in one or two periods and weak in another.
- **It beats chance's best.** Its weakest period scores z = +1.84, against +1.48 for the best lead the shifted calendars produce. Only it and the Supreme Toto lead below clear that bar.
- **It has enough history.** It covers 1,010 draws, and each cell has plenty of past draws behind it, unlike Sun nakshatra × Na Yin's 2-draw tickets.

**Runner-up: Jupiter rashi × Jupiter retrograde on Supreme Toto** (hot numbers). It's also consistent: 463 vs 428, 372 vs 341, and 555 vs 519 matches, and it slightly beats chance's best (+1.75 vs +1.52). The catch is that Jupiter stays in one sign for about a year, so its ticket barely changes. In practice it's "this year's hot numbers", and the fairness tests found hot numbers don't carry forward.

**Keep the 4D lead (Mercury nakshatra × Venus rashi on Magnum Life) as a benchmark, not a contender.** It's the best of 58 picks by chance, and it drops to an ordinary score when rebuilt draw by draw.

**Why I'm still cautious:**
- I chose these two using all three periods, so no unseen data is left to check them on. Only future draws can.
- The edges are tiny even if real: 1.89 matching numbers per Magnum Life ticket instead of 1.78, and 0.67 instead of 0.62 on Supreme Toto. Neither changes the jackpot odds in any meaningful way.

**How to judge them.** Their tickets are logged as `per_game_best` in `forward_log.csv`; run `python3 analysis/astro_model.py score` after each draw.
- **Magnum Life:** an edge this small needs about 350 draws, roughly 2 years, to be confirmed. If it's at or below expected after about 150 draws (a year), drop it.
- **Supreme Toto:** the edge is so small it would take around 800 draws, about 5 years, to confirm, so it's mostly there for completeness.

---

**User:**

> If I had to pick one, it’s Moon rashi × Mars combust on Magnum Life, ok since this is first give me top 20 of all others

**Answer:**

Here are the next 20 leads after Moon rashi × Mars combust. They're ranked the same way: by the weakest of their three period scores, across all games and all four ticket patterns. The last column is the best weakest score the same game and pattern reach on shifted calendars, i.e. by pure chance. A lead is above chance only if its weakest score beats that number.

| # | Game | Parameter(s) | Pattern | Early | Valid | Test | Weakest | Chance best |
|---|---|---|---|---|---|---|---|---|
| 2 | Supreme 6/58 | Jupiter rashi × Jupiter retrograde | hot | +1.86 | +1.83 | +1.75 | **+1.75** | +1.52 |
| 3 | Power 6/55 | year yin/yang × day god | cold | +2.30 | +1.86 | +1.69 | **+1.69** | +1.62 |
| 4 | Supreme 6/58 | solar term × month stem | pos | +1.46 | +2.22 | +1.61 | +1.46 | +1.56 |
| 5 | Supreme 6/58 | solar term × month pillar | pos | +1.46 | +2.22 | +1.61 | +1.46 | +1.56 |
| 6 | Magnum Life | Mars rashi × Venus combust | cold | +1.82 | +1.42 | +1.92 | +1.42 | +1.44 |
| 7 | Power 6/55 | Mercury nakshatra × 28 mansions | cold | +1.77 | +2.09 | +1.41 | +1.41 | +1.62 |
| 8 | Power 6/55 | Moon navamsa × 28 mansions | cold | +2.90 | +1.80 | +1.41 | +1.41 | +1.62 |
| 9 | Star 6/50 | karana × Venus rashi | cold | +1.58 | +1.40 | +1.62 | +1.40 | +1.47 |
| 10 | Power 6/55 | KP Ascendant sub lord × lunar month | cold | +1.85 | +1.40 | +2.44 | +1.40 | +1.62 |
| 11 | Supreme 6/58 | Saturn rashi × Rahu nakshatra | hot | +1.39 | +1.47 | +1.87 | +1.39 | +1.52 |
| 12 | Power 6/55 | Mars nakshatra × KP Ascendant sub lord | cold | +1.57 | +2.34 | +1.36 | +1.36 | +1.62 |
| 13 | Magnum Life | nakshatra lord × Yellow/Black path | pos | +1.39 | +1.61 | +1.36 | +1.36 | +1.48 |
| 14 | Power 6/55 | yoga × Jupiter nakshatra | cold | +1.57 | +2.23 | +1.35 | +1.35 | +1.62 |
| 15 | Star 6/50 | Saturn nakshatra × month Nine Star | pos | +1.60 | +1.58 | +1.35 | +1.35 | +1.82 |
| 16 | Supreme 6/58 | Jupiter retrograde × year element | pos | +1.34 | +2.53 | +1.36 | +1.34 | +1.56 |
| 17 | Power 6/55 | Moon rashi × Jupiter retrograde | cold | +1.83 | +1.34 | +1.51 | +1.34 | +1.62 |
| 18 | Power 6/55 | Venus nakshatra × KP Sun sub lord | cold | +1.41 | +1.34 | +1.44 | +1.34 | +1.62 |
| 19 | Magnum Life | yoga × Mars rashi | hot | +1.44 | +1.63 | +1.34 | +1.34 | +1.42 |
| 20 | Star 6/50 | tithi × 19:00 hour stem | pos | +1.84 | +2.45 | +1.34 | +1.34 | +1.82 |
| 21 | Power 6/55 | ayana × KP Moon number | cold | +1.31 | +2.08 | +1.57 | +1.31 | +1.62 |

**How to read it:**
- **Only #2 and #3 beat chance's best**, and #3 only barely (+1.69 vs +1.62). Everything from #4 down is no better than the best pair from a meaningless calendar.
- **#4 and #5 are the same lead.** The month stem and month pillar both follow from the solar term, so they produce identical tickets.
- **Pairs fill the whole list; no single parameter makes the top 21.**
- **"Cold" leads on Power Toto make up 9 of the 20.** That isn't a signal: cold tickets on Power Toto are the pattern where chance produces the most consistent performers (36.5 on average across the shifted calendars).
- **All of these were chosen using all three periods**, so only future draws can test them.

If you want to watch more than #1, I'd add **#2 (Jupiter rashi × Jupiter retrograde, Supreme Toto)** and **#3 (year yin/yang × day god, Power Toto)**. Both already have tickets logged in `forward_log.csv` as `per_game_best`. I can log tickets for the rest of the top 20 too.

The table is saved at the end of `analysis/PER_GAME_LEADS.md`, with the data in `analysis/top_leads.json`; both are committed and pushed.

---

**User:**

> ok for top 5 log tickets and give me 5 of the best for each

**Answer:**

Two notes before I log them:

- **#5 duplicates #4.** Solar term × month pillar puts every draw in the same group as solar term × month stem, so it would produce identical tickets. I'll skip it and take the next distinct lead, #6 (Mars rashi × Venus combust, Magnum Life, cold).
- **"5 of the best for each":** for each lead, ticket 1 is its top pick. Tickets 2–5 are the nearest alternatives, each swapping one number for the next-best candidate with the smallest drop in that lead's score.

**Answer:**

Ticket 1 matches the tickets already logged for those leads. I'll silence the harmless log(0) warning and log everything.

**Answer:**

I logged 5 tickets for each of the top 5 leads, for the 18 Oct (Sunday) and 21 Oct (Wednesday) draws. They're in `analysis/forward_log.csv` as `top<rank>_t1`–`t5`, with tables in `analysis/TOP_TICKETS.md`. I skipped #5 (solar term × month pillar) because it gives exactly the same tickets as #4, and used #6 instead.

**#1 Magnum Life: Moon rashi × Mars combust (position)**

| Ticket | 18 Oct (96 earlier draws in this cell) | 21 Oct (94 earlier draws) |
|---|---|---|
| 1 | 01 05 10 17 18 25 30 36 | 01 06 10 13 18 26 31 36 |
| 2 | 01 05 10 17 18 28 30 36 | 02 06 10 13 18 26 31 36 |
| 3 | 01 05 10 11 18 25 30 36 | 01 06 09 13 18 26 31 36 |
| 4 | 01 05 10 14 18 25 30 36 | 01 06 07 13 18 26 31 36 |
| 5 | 01 05 08 17 18 25 30 36 | 01 06 10 13 18 26 31 35 |

**#2 Supreme Toto 6/58: Jupiter rashi × Jupiter retrograde (hot), same tickets both days**

| Ticket | 18 and 21 Oct (201 earlier draws) |
|---|---|
| 1 | 15 39 42 44 48 54 |
| 2 | 15 31 39 44 48 54 |
| 3 | 15 31 42 44 48 54 |
| 4 | 15 39 44 48 54 57 |
| 5 | 15 19 39 44 48 54 |

**#3 Power Toto 6/55: year yin/yang × day god (cold)**

| Ticket | 18 Oct (117 earlier draws) | 21 Oct (124 earlier draws) |
|---|---|---|
| 1 | 13 15 16 26 30 36 | 05 09 19 31 32 43 |
| 2 | 13 15 16 24 26 30 | 09 19 31 32 43 45 |
| 3 | 13 15 16 26 30 38 | 05 09 31 32 43 45 |
| 4 | 13 15 16 24 26 36 | 05 09 19 31 43 45 |
| 5 | 13 16 24 26 30 36 | 05 09 19 32 43 45 |

**#4 Supreme Toto 6/58: solar term × month stem (position), same tickets both days**

| Ticket | 18 and 21 Oct (24 earlier draws) |
|---|---|
| 1 | 05 07 31 34 38 54 |
| 2 | 05 09 31 34 38 54 |
| 3 | 05 07 16 34 38 54 |
| 4 | 05 07 28 34 38 54 |
| 5 | 05 21 31 34 38 54 |

**#6 Magnum Life: Mars rashi × Venus combust (cold), same tickets both days**

| Ticket | 18 and 21 Oct (14 earlier draws) |
|---|---|
| 1 | 04 05 09 10 17 20 26 32 |
| 2 | 04 05 09 10 17 20 32 33 |
| 3 | 04 05 09 10 17 20 31 32 |
| 4 | 04 05 09 17 20 26 32 33 |
| 5 | 04 05 09 10 17 20 26 33 |

**Things to know:**
- **Tickets 2–5 overlap heavily with ticket 1** (each differs by one number), so playing all five spreads very little extra coverage.
- **#4 and #6 rest on few earlier draws** (24 and 14 in today's group), so their tickets are the least reliable of the five.
- **#2's tickets won't change** until Jupiter changes sign or direction.
- **None of these leads beats random so far.** Only #1 and #2 clearly beat chance's best, and all of them still need future draws to show anything. Run `python3 analysis/astro_model.py score` once the 18 and 21 Oct results are added to `data/`.

The script is `analysis/top_tickets.py`, committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> ok before that lets do the same analysis to find for leads but dont train them on the last 5, and then test them on the last 5, i want to know in this scenario which lead performs better, dont use the previous leads since they are biased

**Answer:**

To be clear about the design:

- **Hold-out:** for each game, I take its last 5 draws off the end. These run 6–17 Oct for Star, Power and Supreme Toto, and 7–17 Oct for Magnum Life.
- **Search:** I rerun the whole lead search from scratch on everything before those 5 draws. That's 78 parameters and 3,003 pairs, with hot, cold, position and gap tickets, ranked by consistency over three periods of that shorter history.
- **Test:** the chosen leads build tickets from pre-hold-out draws only, and I score them on the 5 held-out draws.
- **No earlier leads are reused.** As a check on luck, I repeat the same selection on shifted calendars.

One caution up front: 5 draws is very little. A fair 6/50 ticket matches only 3.6 numbers in total over 5 draws, so luck will dominate. The shifted-calendar comparison will show how much.

First, `own_leads.py` needs an option to drop the last draws.

**Answer:**

The tests pass and the full run is going. I'll wait for it to finish.

**Answer:**

The hold-out search is running: a fresh lead search on everything except each game's last 5 draws, then a test on those 5. It should take about 8–10 minutes, and I'll report when it finishes.

**Answer:**

The hold-out scripts are committed and pushed now, so the selection rule is on record before any result comes in. The run itself is still going in the background, and I'll report the results when it finishes.

**Answer:**

I reran the lead search from scratch for each game with its last 5 draws removed (7, 10, 11, 14 and 17 Oct), picked the top 20 leads, and tested them on those 5 draws. No earlier lead was reused.

**Overall, the selected leads did no better than random tickets:**

| Game | Top 20 leads' total matches | Fair tickets would average | Same selection on shifted calendars |
|---|---|---|---|
| Star Toto 6/50 | 63 | 72.0 | 56–89 |
| Power Toto 6/55 | 67 | 65.5 | 61–80 |
| Supreme Toto 6/58 | 60 | 62.1 | 52–63 |
| Magnum Life | 156 | 177.8 | 162–171 |

**The #1 pick in each game** (the most consistent lead before the hold-out):

| Game | #1 lead | Matches in last 5 (per draw) | Fair ticket average | How often a fair ticket does this well |
|---|---|---|---|---|
| Magnum Life | **Moon rashi × Mars combust** (position) | **13** (2, 3, 2, 4, 2) | 8.9 | 6.5% |
| Supreme 6/58 | **Jupiter rashi × Jupiter retrograde** (hot) | **6** (0, 1, 1, 2, 2) | 3.1 | 7.4% |
| Power 6/55 | year yin/yang × day god (cold) | 3 | 3.3 | average |
| Star 6/50 | tithi × 19:00 hour stem (position) | 2 | 3.6 | below average |

So the answer to your question: **Moon rashi × Mars combust on Magnum Life performed best.** It was again the #1 lead, even with the last 5 draws hidden, and it matched 13 numbers against 8.9 expected, at least 2 in every draw. The Supreme Toto Jupiter lead came second, with 6 against 3.1. These two were also #1 and #2 in the earlier full-history ranking.

**Why this isn't proof yet:**
- **A result this good happens by chance 6–7% of the time** for any single fair ticket. That's suggestive, not significant.
- **The other two #1 picks did average or worse,** and the top 20 as a group were below expectation in three of the four games.
- **Ranking before the hold-out didn't predict the hold-out score.** Across all 12,324 tickets per game, the correlation is between −0.06 and +0.01.
- **Other leads also scored high, but further down the list.** On Magnum Life, #4 Mars rashi × Venus combust also got 13, and #20 got 11. On Star Toto, #3 Sun rashi × Mercury rashi got 7. One random ticket somewhere always does well. The best of all 12,324 tickets got 19 on Magnum Life, but nobody could have picked it in advance.

**Bottom line:** Moon rashi × Mars combust is the one lead that has now passed a clean test it couldn't have seen, so it's the right one to keep watching. It needs many more draws before it means anything. Its 18 and 21 Oct tickets are already logged.

The full per-game top-20 tables are in `analysis/HOLDOUT_LEADS.md`, with a summary in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> but you know for toto you need to pick only 6 numbers but for magnum life you pick me more numbers lets redo the analysis to make it fair

**Answer:**

A clarification first: Magnum Life's own rules have you pick 8 numbers (8 from 1–36), while Toto has you pick 6. That's why its tickets were 8 numbers. Each game was also judged against its own chance level: 13 matches against 8.9 expected for an 8-number Magnum Life ticket, and 6 against 3.1 for Supreme Toto. So the earlier comparison wasn't tilted.

Still, a like-for-like check is easy. I'll redo the Magnum Life hold-out with 6-number tickets, so every game is scored on 6 picks. Each pattern then keeps its 6 strongest numbers:
- **Hot / cold:** the top 6 by count.
- **Position:** the 6 positions it is most confident about.
- **Gap:** the first 6 numbers of the chain.

**Answer:**

The 6-number tickets work. Now the full Magnum Life redo: a fresh search and selection with 6-number tickets, then the hold-out test.

**Answer:**

The code change is committed and pushed, and the Magnum Life redo with 6-number tickets is running in the background. It reruns the full search and selection on everything before the last 5 draws, then tests on those 5. It should take about 3 minutes, and I'll report the results when it finishes.

**Answer:**

With 6-number tickets, Moon rashi × Mars combust drops out of Magnum Life's top 20 entirely. I'll check how it scores at that ticket size.

**Answer:**

You were right to check, because it changes the picture: with 6-number tickets, Moon rashi × Mars combust is no longer a leading lead. I redid the Magnum Life search and selection with 6-number tickets, still without the last 5 draws, and tested on those 5 draws.

**Magnum Life with 6-number tickets:**
- **As a group, the leads did no better than random.** The top 20 together matched 121 numbers against 133.3 expected; the same selection on shifted calendars gave 80–138.
- **The new #1, hora lord × Venus rashi (position), matched 4 against 6.7 expected.** That's below average.
- **The best in the top 20 were #11 Moon navamsa × day pillar (hot) and #18 Mars rashi × Venus combust (cold),** with 10 against 6.7 each. A fair ticket does that 9% of the time.
- **Moon rashi × Mars combust drops out.** With 6 numbers it wasn't consistent before the hold-out (its validation period was only z +0.50), so it didn't make the top 20. Its 6-number ticket matched 9 against 6.7 on the last 5 draws, which a fair ticket does 19% of the time. Its earlier strength came from picking 8 numbers, which points to noise rather than a real effect.

**All four games on 6 numbers, #1 picks only:**

| Game | #1 lead (chosen without the last 5) | Matched in last 5 | Fair ticket average |
|---|---|---|---|
| Star 6/50 | tithi × 19:00 hour stem (position) | 2 | 3.6 |
| Power 6/55 | year yin/yang × day god (cold) | 3 | 3.3 |
| Supreme 6/58 | **Jupiter rashi × Jupiter retrograde** (hot) | **6** | 3.1 |
| Magnum Life | hora lord × Venus rashi (position) | 4 | 6.7 |

**With equal tickets, the best lead is Supreme Toto's Jupiter rashi × Jupiter retrograde,** matching 6 against 3.1 expected. That's still only a 1-in-14 chance result, and the other three #1 picks did at or below average. So even on a level playing field, no lead stands out from luck.

**My recommendation:** keep Jupiter rashi × Jupiter retrograde (Supreme Toto) as the lead to watch, and treat Moon rashi × Mars combust as not confirmed.

The Magnum Life 6-number tables are in `analysis/HOLDOUT_LEADS_T6.md`, with a summary in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Supreme 6/58	Jupiter rashi × Jupiter retrograde (hot)	6	3.1 redo the this by training all except last 10 and then test the last 10 draw, check if the same lead appears

**Answer:**

I'll rerun the Supreme Toto search with the last 10 draws held out, then check where Jupiter rashi × Jupiter retrograde ranks and how it does on those 10 draws. First the script needs a hold-out-size option.

**Answer:**

Yes. With the last 10 draws hidden (26 Sep – 17 Oct), the search on Supreme Toto again ranks **Jupiter rashi × Jupiter retrograde (hot) as #1**, and it did well on those 10 draws.

| | Matched in last 10 | Fair ticket average | Chance a fair ticket does this well |
|---|---|---|---|
| **#1 Jupiter rashi × Jupiter retrograde** | **11** (1, 1, 0, 1, 2, 0, 1, 1, 2, 2) | 6.2 | 3.5% |
| The other 19 of the top 20 | 94 | 117.9 | below average |
| All 20 together | 105 | 124.1 | shifted calendars: 95–136 |

**Its ticket was the same for all 10 draws: 15 39 42 44 48 54.** Jupiter stayed in Karka and direct the whole time, so every draw fell in the same group.

**Why this still isn't proof:**
- **Half of it isn't new evidence.** The last 10 draws include the 5 from the previous test. On the 5 new draws (26 Sep – 4 Oct) it matched 5 against 3.1 expected.
- **A plain ticket with no astrology did just as well.** Taking the 6 most frequent numbers of the last 100 draws also matched **11**. The same idea over the last 50, 201 and 300 draws matched 8, 5 and 8. So a result like this doesn't need Jupiter.
- **The cell is mostly two time blocks.** Its 191 earlier draws come from 2014–15 and 2025–26, the two periods when Jupiter was in Karka and direct. That makes its ticket close to "numbers that were hot in those years", and the earlier tests found recent-hot numbers don't beat chance over the long run (0.97×).
- **The rest of the selection did worse than chance,** which is what you'd expect if picking #1 is mostly luck.

**Bottom line:** it's the most persistent lead so far. It came out #1 with the last 5 and the last 10 draws hidden, and it beat chance both times. But a ticket with no astrology at all matched its result, so there's no sign Jupiter is doing the work.

**What to watch:** Jupiter is now in Karka, direct, so it keeps the same ticket (15 39 42 44 48 54) until Jupiter changes direction or sign. That's already logged for 18 and 21 Oct. A fair test is to compare it with the plain last-100-draws hot ticket on the next draws; I can log that one alongside it if you'd like.

The tables are in `analysis/HOLDOUT_LEADS_H10.md`, with a summary in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> ok just to confirm how does this lead compare to toto 4d?

**Answer:**

"Toto 4D" here means Sports Toto 4D, whose history is in the 4DPrediction repo (`data/sportstoto.csv`). I'll test the same lead, Jupiter rashi × Jupiter retrograde with hot numbers, on Sports Toto 4D in two ways:

- **Whole numbers:** the 16 four-digit numbers that won most often under the same Jupiter condition.
- **Digits:** the 2 most frequent digits in each position under that condition (16 combinations). This mirrors how the 4D repo built its leads.

Both are scored on the last 10 draws, and on the most recent 30% of the history draw by draw. For comparison, I'll score 200 random pairs and the Mercury nakshatra × Venus rashi 4D lead the same way.

**Answer:**

On Sports Toto 4D the Jupiter lead does nothing; it actually comes out slightly below chance. I built 16-number tickets from earlier 4D draws with the same Jupiter sign and direction, in the two ways described above.

| Test on Sports Toto 4D | Whole-number ticket: hits / expected | Digit ticket: hits / expected |
|---|---|---|
| Last 30% of draws (2016-08-21 to 2026-10-17) | 55 / 60.5 (z −0.70) | 58 / 60.5 (z −0.32) |
| Last 10 draws (26 Sep – 17 Oct) | 0 / 0.37 | 0 / 0.37 |
| Share of 200 random pairs doing at least as well (last 30%) | 82% | 67% |

For comparison, the Mercury nakshatra × Venus rashi 4D lead scored 68 against 60.2 (z +1.0) and 57 against 60.2 on the same test.

**How it compares with Supreme Toto:**
- **On Supreme Toto it was #1 in both hold-outs** and beat chance (6 vs 3.1 on the last 5, 11 vs 6.2 on the last 10).
- **On Sports Toto 4D it's below average.** Most random pairs do better.
- **The last 10 draws can't tell us much for 4D.** A 16-number ticket expects only 0.37 hits in 10 draws, so the comparison rests on the long period. There it lost to chance.

If Jupiter's position really influenced draws, it should show up in both games, which are drawn by the same operator on the same evenings. It doesn't. That fits the earlier finding that its Supreme Toto ticket matched a plain "hot numbers over the last 100 draws" ticket: what it's picking up is a run of recently hot numbers in that one game, not Jupiter.

This test is in `analysis/lead_on_4d.py`, and its results are summarised in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> How about for Magnum and Da Ma Cai?

**Answer:**

I'll run the same test on Magnum 4D and Da Ma Cai, using the same tickets, periods and random-pair comparison as for Sports Toto. First I'll make the script take the operator as an option.

**Answer:**

On Magnum and Da Ma Cai the Jupiter lead does slightly better than chance, but not by enough to mean anything. I ran exactly the same test as for Sports Toto: 16-number tickets built from earlier draws with the same Jupiter sign and direction, scored draw by draw. The test period is the last 30% of each operator's draws, and each result is compared with 200 random pairs.

| 4D operator (test period) | Whole-number ticket: hits / expected (z) | Random pairs doing as well | Digit ticket: hits / expected (z) | Random pairs doing as well |
|---|---|---|---|---|
| Sports Toto (2016–2026) | 55 / 60.5 (−0.70) | 82% | 58 / 60.5 (−0.32) | 67% |
| Magnum (2014–2026) | 85 / 75.3 (+1.12) | 20% | 84 / 75.3 (+1.00) | 12% |
| Da Ma Cai (2016–2026) | 69 / 63.3 (+0.72) | 30% | 74 / 63.3 (+1.34) | 11% |

**Last 10 draws:** 1 hit against 0.37 expected on Magnum, 0 on Da Ma Cai and 0 on Sports Toto. With 16 numbers, 10 draws are too few to say anything for 4D.

**How to read it:**
- **None of the six results is significant.** The best, the digit ticket on Da Ma Cai at z +1.34, is matched or beaten by about 1 in 9 random pairs.
- **It's mixed rather than consistent:** below chance on Sports Toto, mildly above on Magnum and Da Ma Cai. A real Jupiter effect would show clearly across all three, and in Supreme Toto with the same strength.
- **The 4D lead does no better.** Mercury nakshatra × Venus rashi, scored the same way, ranges from z −1.27 to +1.51 across these operators. Both leads behave like random pairs.

**Overall:** Jupiter rashi × Jupiter retrograde is the strongest lead within Supreme Toto. It came out #1 in both hold-outs and beat chance on the held-out draws. But it doesn't carry over to Sports Toto 4D, Magnum or Da Ma Cai, and a plain recent-hot-numbers ticket matched its Supreme Toto result. Everything points to luck in one game rather than an effect of Jupiter. Keep watching its Supreme Toto ticket (15 39 42 44 48 54); I wouldn't expect it to hold up.

Results are in `analysis/lead_on_4d_magnum_results.json` and `analysis/lead_on_4d_damacai_results.json`, with a summary in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Ok, this time to find a lead for the magnum live and sports toto lotto, I want you to do this. Use all the parameters for that date and time and the numbers won for a specific draw. Represent all this as a vector, and create a predictive llm which is able to predict the win? Just like how llm work king-man+woman= queen? Please do analysis based on this method

**Answer:**

This is a good idea to test, and it maps onto real techniques. "king − man + woman = queen" comes from **word embeddings** (word2vec). They learn a vector for every word from which words appear together, so related words end up close together. Here's how I'll apply it:

1. **Each draw becomes a "sentence"** of tokens: every parameter value at that date and time (e.g. `moon_rashi=Vrishabha`, `day_god=Jade Hall`) plus the numbers drawn (`N07`, `N23`, …).
2. **Two embedding models**, trained per game on the older 70% of draws only:
   - **Co-occurrence embedding:** the matrix method that word2vec is mathematically equivalent to.
   - **Small neural "language model":** it reads a date's parameter tokens and learns to predict which number tokens follow. This is the predictive version you described, fastText-style.
3. **Prediction by vector arithmetic:** add up the date's parameter vectors and take the numbers whose vectors lie closest.
4. **Honest test:**
   - score the tickets on the newest 30% and on the last 10 draws;
   - compare with the same models trained on shifted calendars;
   - run analogy checks to see what the vectors actually learned.

First I'll check which libraries are available.

**Answer:**

The full run is taking longer on the larger games (Power and Supreme Toto have about 2,800 draws each). It's continuing in the background, and I'll report when it finishes.

**Answer:**

The embedding and language-model script is committed and pushed. The full run, covering all four games on the real calendar and 5 shifted ones, is still going in the background. I'll commit its results and report when it finishes.

**Answer:**

I built the vector / language-model approach, and it can't predict the numbers. The vectors learn the astrology itself very well, but they learn nothing about which numbers come up. I tested it on all four games, Magnum Life and the three Sports Toto lotto games.

**What I built:**
- **Each draw became a "sentence" of tokens:** all 83 parameter values at 19:00 on that date (e.g. `moon_rashi=Vrishabha`, `day_god=Jade Hall`) plus the numbers drawn (`N07`, `N23`, …).
- **Word vectors (word2vec-style):** every token gets a vector based on which tokens appear together. A date's ticket is the numbers whose vectors lie closest to the sum of that date's parameter vectors. That's the "king − man + woman" idea.
- **A small neural language model:** it reads a date's parameter tokens and predicts the number tokens. A second version also reads the previous draw's numbers, the way an LLM reads the previous words.
- **Testing:** settings were chosen on older draws, then tested on later draws and on the last 10 draws, which the models never saw. Everything was rerun on 5 shifted calendars to show what chance produces.

**The analogies work, but only for astrology:**
- **Moon in Vrishabha − Rohini + Ashwini ≈ Moon in Mesha.** That's correct, because Ashwini lies in Mesha.
- **Jupiter in Karka's nearest neighbour is Jupiter in Ashlesha,** a nakshatra inside Karka.
- **The Jia Zi day sits next to its own Na Yin.**
- **Number tokens (N07, N23 …) only sit next to the most common tokens,** such as "not retrograde" or "no planets with the Moon". They appear alongside everything about equally, so they carry no astrological meaning.

**Prediction results (z on the later test draws; matches on the last 10 draws vs expected):**

| Game | Vector arithmetic | Shifted calendars | Neural model | Neural, shifted |
|---|---|---|---|---|
| Star 6/50 | +1.65; 8 vs 7.2 | −1.48 to +1.26 | +0.63; 6 vs 7.2 | +0.01 to +0.24 |
| Power 6/55 | −0.06; 5 vs 6.6 | −1.85 to +0.97 | +1.72; 7 vs 6.6 | +1.72 every time |
| Supreme 6/58 | +0.59; 3 vs 6.2 | −0.18 to +1.72 | −0.36; 4 vs 6.2 | −1.26 to −0.07 |
| Magnum Life | +0.61; 22 vs 17.8 | −1.07 to +0.85 | +0.50; 19 vs 17.8 | +0.15 to +0.26 |

**Reading it:**
- **Vector arithmetic stays within the range of the shifted calendars.** The best result, Star Toto at +1.65, is the kind of score a meaningless calendar also produces.
- **The neural model never beat "all numbers equally likely" on unseen draws.** Training stopped after 5–20 passes because more training only made it worse on the validation draws.
- **Its tickets come out the same on shifted calendars,** e.g. +1.72 every time on Power Toto. That means it ignores the astrology and just follows how often each number has come up overall.
- **On the test draws, every language model fit the real results slightly worse than pure chance.**

The method works as designed: it found the real relationships among the planets, signs and calendar cycles. It simply finds no relationship between those and the winning numbers, which matches all the earlier tests.

The script is `analysis/embed_model.py`. The neighbours and analogies are in `analysis/EMBEDDINGS.md`, and the summary is in `analysis/FINDINGS.md` and section 8 of `analysis/REPORT.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Bro, “Moon in Vrishabha − Rohini + Ashwini ≈ Moon in Mesha. That's correct, because Ashwini lies in Mesha.” This is just an example. You need to find a way to use this concept so that it is able to be made as a predictive model

**Answer:**

You're right. The analogy itself isn't the goal; the goal is to use that kind of arithmetic to predict a draw. Here is how to do that.

**The analogy, used for prediction:**
- **The formula:** king − man + woman = queen becomes numbers(past draw A) − conditions(A) + conditions(today) = numbers(today).
- **What it means:** take a past draw's numbers, remove the "astrological signature" of that day, and add today's signature. If the planets and almanac really shape the numbers, the result should point to today's numbers.

I'll build several predictive versions on the word vectors, each trained only on draws before the ones it predicts:

1. **Analogy from the last draw:** numbers(previous draw) − conditions(previous draw) + conditions(today).
2. **Analogy from similar days:** the same, averaged over the 10 past draws whose conditions most resemble today's.
3. **Learned analogy map:** like learning the "man → woman" direction. A learned transformation turns a day's condition vector into a predicted numbers vector, then the analogy is applied from the similar days.
4. **Strength of the astrology term, chosen on validation draws only:** prediction = numbers(A) + λ × (conditions(today) − conditions(A)), with λ = 0, 0.5, 1 or 2. **If validation picks λ = 0, the astrology part adds nothing.** That makes it a direct test of whether the analogy carries information.
5. **Controls without the astrology term:** the same past draws' numbers alone. Everything is also rerun on 5 shifted calendars.

All of this is scored on the later test draws and the last 10 draws, using ticket matches and how well the real numbers rank (AUC, where 0.5 = chance).

**Answer:**

The analogy forecaster is committed and pushed. The full run, all four games on the real calendar plus 5 shifted calendars each, is going in the background and should take about 10 minutes. I'll report when it finishes, including whether the Magnum Life z = +1.83 beats what the shifted calendars produce.

**Answer:**

I turned the analogy into a real forecaster and tested it on all four games. It doesn't predict the numbers better than chance.

**How it predicts:** the analogy becomes numbers(today) ≈ numbers(A) − conditions(A) + λ × conditions(today).
- **A** is a past draw: the previous draw ("last"), or the 10 earlier draws whose conditions most resemble today's ("similar").
- **"map"** adds a learned direction that converts a change in conditions into a change in numbers, like learning the "man → woman" direction.
- **"direct"** uses that map alone, on today's conditions.
- **λ** is how much weight the astrology term gets. It was chosen on validation draws only (0, 0.5, 1 or 2); λ = 0 means the astrology term doesn't help.
- **The ticket** is the numbers whose vectors lie closest to the predicted vector.

**Results** (z of numbers matched on the later test draws; λ chosen in brackets):

| Game | last | similar | map | direct | Shifted calendars |
|---|---|---|---|---|---|
| Star 6/50 | −0.54 (λ 2) | **+2.20 (λ 0)** | +2.20 (λ 0) | +0.08 | −0.78 to +1.10 |
| Power 6/55 | +1.26 (λ 0) | −0.01 (λ 0) | −0.01 (λ 0) | +0.74 | −1.16 to +1.72 |
| Supreme 6/58 | −0.24 (λ 2) | −0.60 (λ 2) | +0.71 (λ 2) | −0.36 | −2.51 to +2.37 |
| Magnum Life | **+1.83 (λ 2)** | +0.38 (λ 2) | −0.84 (λ 2) | −0.49 | −0.90 to +1.72 |

**What it shows:**
- **In 5 of the 12 analogy settings, validation switched the astrology term off (λ = 0),** meaning adding today's conditions made predictions worse on unseen draws.
- **The best score, Star Toto +2.20, had the astrology term switched off.** It's the numbers of similar past days alone.
- **Magnum Life "last" at +1.83 is the one case where the astrology term helped:** +0.03 without it, +1.83 with it. But it's one of 16 results, and the meaningless shifted calendars reach as high as +2.37 elsewhere.
- **How well the real numbers rank (AUC, 0.5 = chance) stays between 0.487 and 0.509,** inside the shifted calendars' 0.491–0.514.
- **On the last 10 draws, every method is inside the shifted range.** Magnum Life's best scored 23 against 17.8 expected, while shifted calendars gave 12–23.

**Why it can't work here:** the analogy works for words because "man → woman" is a consistent direction found in millions of sentences. Here, the direction from one day's conditions to another's carries no consistent information about the numbers. The vectors capture the astrology correctly, as the Vrishabha/Mesha example showed, but there is no stable link from those vectors to the numbers drawn. That's the same conclusion every other method reached.

The script is `analysis/analogy_model.py`, with results in `analysis/analogy_results.json`, a summary in `analysis/FINDINGS.md` and section 8 of `analysis/REPORT.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> I think you must have included all the parameters, maybe some parameters don’t play a role compared to others, try again by reducing the parameters

**Answer:**

Good idea to test. If most of the 83 parameters are noise, they could drown out a few that matter. The one rule is that the parameters must be chosen without looking at the draws they're tested on; otherwise any subset can look good in hindsight.

I'll add parameter selection to the vector models, using two forecasters: the condition→numbers map ("direct"), and the analogy from the last draw at full astrology weight (λ = 1). Two selection methods:

1. **Rank and keep the top m:** score each parameter alone on validation draws, then keep the top m (1, 3, 5, 10 or 20), with m also chosen on validation.
2. **Greedy forward selection:** start with no parameters and repeatedly add the one that most improves validation accuracy, stopping when nothing helps (at most 10).

The chosen subsets are then tested on later draws and the last 10 draws. The entire selection is repeated on shifted calendars, because selecting parameters on noise also produces a "best subset".

**Answer:**

Using fewer parameters didn't help: on average the reduced sets did slightly worse on unseen draws than using all 83.

For each game, I picked parameters using validation draws only, in two ways: keep the best few by solo score, or add parameters one at a time while accuracy improves. I then tested those subsets on later draws and the last 10 draws. I repeated the whole selection on 4 shifted calendars.

**What got selected, and how it did on the later test draws (z):**

| Game / forecaster | All 83 | Best few | Added one at a time |
|---|---|---|---|
| Star 6/50, map | +0.08 | ritu → −0.39 | ritu, Jupiter rashi, day element → −0.86 |
| Star 6/50, analogy | +0.32 | day element → +1.26 | day element, nakshatra, tropical Sun sign → +0.40 |
| Power 6/55, map | +2.30 | Venus nakshatra, 19:00 hour stem, day officer → −0.70 | 4 params → −0.75 |
| Power 6/55, analogy | +1.20 | 5 params → −0.47 | tropical Moon sign, Jupiter nakshatra → +1.38 |
| Supreme 6/58, map | −0.66 | KP Sun star lord → +0.23 | 5 params → −0.66 |
| Supreme 6/58, analogy | −0.84 | hora lord → +0.59 | 6 params → +0.53 |
| Magnum Life, map | −0.49 | Jupiter rashi, lagna nakshatra, Mercury combust → +0.32 | Jupiter rashi, samvatsara → −0.84 |
| Magnum Life, analogy | +1.08 | 20 params → +1.54 | 5 params → −0.72 |

**What it shows:**
- **No improvement.** The reduced sets average z +0.05 on the test draws, against +0.37 with all 83. The shifted calendars' selections range from −2.88 to +2.18, so every real result is inside the chance range.
- **No parameter keeps winning.** Each game and method picks a different subset. The shifted calendars pick equally believable-looking ones (lunar day, yoga, nakshatra …), because when parameters are selected on noise, something always looks best.
- **Selection sometimes hurts.** Power Toto's map scored +2.30 with all 83, but its selected subsets fell to −0.70 and −0.75, and matched only 2 and 1 numbers on the last 10 draws (against 6.6 expected).

**One result to note:** on Power Toto, the analogy using only **tropical Moon sign + Jupiter nakshatra** matched **13 numbers on the last 10 draws, against 6.6 expected**. For a single method that happens 0.8% of the time. But it's the best of 16 hold-out results here, which brings it to about 12%. One shifted calendar also reached 13, and on the longer test the same pair scored only +1.38.

Combined with everything else, reducing parameters finds no subset that holds up; it just finds whichever subset fit the validation noise best. I can log tickets for the Power Toto Moon-sign × Jupiter-nakshatra analogy for the coming draws if you'd like to track it.

The script is `analysis/param_select.py`, with results in `analysis/param_select_results.json` and a summary in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> So from all the current lead how does this perform?

**Answer:**

The fair way to compare is to score every current lead on the same window: each game's last 10 draws, with tickets built only from earlier draws. Not every lead has been scored on that window yet, so I'll compute the missing ones.

**Answer:**

On the last 10 draws, the new Power Toto lead (tropical Moon sign × Jupiter nakshatra analogy) scored best of all the current leads, with the Supreme Toto Jupiter lead second.

| Rank | Lead | Game | Last 10 draws: matched / expected | How often a fair ticket does as well | Longer test (z) |
|---|---|---|---|---|---|
| 1 | **Tropical Moon sign × Jupiter nakshatra** (analogy from last draw) | Power 6/55 | **13 / 6.6** (2.0×) | **0.8%** | +1.38 |
| 2 | **Jupiter rashi × Jupiter retrograde** (hot) | Supreme 6/58 | **11 / 6.2** (1.8×) | 3.5% | +1.75 |
| 3 | Mars rashi × Venus combust (cold) | Magnum Life | 21 / 17.8 | 21% | +1.92 |
| 4 | Moon rashi × Mars combust (position) | Magnum Life | 20 / 17.8 (6 numbers: 15 / 13.3) | 30% (34%) | +1.88 |
| 5 | year yin/yang × day god (cold) | Power 6/55 | 8 / 6.6 | 33% | +1.69 |
| 6 | karana × Venus rashi (cold) | Star 6/50 | 8 / 7.2 | 43% | +1.62 |
| 7 | 4D lead: Mercury nakshatra × Venus rashi (hot) | Magnum Life | 18 / 17.8 | 53% | +0.83 |
| 8 | solar term × month stem (position) | Supreme 6/58 | 3 / 6.2 | 96% | +1.61 |

"Longer test" is the z each lead scored on its game's later test draws, in whichever analysis found it.

**How to read it:**
- **#1 and #2 were chosen without seeing the last 10 draws,** so their scores are clean. Leads #3–#6 were picked using data that included some of these 10 draws, which flatters them slightly, and they still didn't stand out.
- **Even the top lead isn't strong evidence.** Its 0.8% applies to one lead tested once. It was the best of 16 hold-out results in its run, which raises the real chance to about 12%, and one shifted calendar also scored 13.
- **The two top leads come from different games and different methods**: one is an analogy that changes every draw, the other a fixed hot-number ticket. Nothing links them, which is what you'd expect from luck rather than a shared effect.
- **The old 4D lead is now just average** on the recent draws.

**Recommendation:** watch #1 and #2 side by side on the next draws.
- **Jupiter (#2):** its ticket for both 18 and 21 Oct is 15 39 42 44 48 54, already logged.
- **Power Toto analogy (#1):** its tickets aren't logged yet. Its ticket changes every draw, so I'd need to add a small live-prediction step. I can set that up if you want both tracked.

---

**User:**

> For number 1 try to test on its performance forthe last 10 draw and tell me its performance

**Answer:**

Over the last 10 draws, the #1 lead (tropical Moon sign × Jupiter nakshatra, analogy from the previous draw) matched 13 numbers against 6.6 expected. That looks strong, but almost all of it comes from replaying the previous draw's numbers, not from the astrology. Every ticket was built only from draws before it.

| Draw | Ticket | Drawn | Matched |
|---|---|---|---|
| 26 Sep | 01 05 08 17 19 38 | 05 06 14 28 32 51 | 1 (05) |
| 27 Sep | 06 22 32 40 51 52 | 13 14 15 22 33 42 | 1 (22) |
| 30 Sep | 28 33 34 41 42 45 | 13 28 33 34 39 44 | **3** (28 33 34) |
| 3 Oct | 11 28 32 34 39 44 | 21 28 37 39 51 52 | 2 (28 39) |
| 4 Oct | 21 28 32 39 51 52 | 05 20 23 31 32 40 | 1 (32) |
| 7 Oct | 07 13 23 32 36 40 | 05 07 17 30 48 50 | 1 (07) |
| 10 Oct | 05 16 18 20 50 55 | 01 03 11 28 35 50 | 1 (50) |
| 11 Oct | 01 03 28 35 49 50 | 11 14 26 28 31 54 | 1 (28) |
| 14 Oct | 11 26 28 29 44 50 | 28 31 32 36 46 49 | 1 (28) |
| 17 Oct | 21 28 36 41 46 49 | 01 07 19 21 43 47 | 1 (21) |
| **Total** | | | **13** vs 6.6 expected |

**Why it isn't evidence for astrology:**
- **The tickets are mostly the previous draw's numbers.** The 4 Oct ticket is 21 28 32 39 51 52, and the 3 Oct result was 21 28 37 39 51 52. The 11 Oct ticket shares 5 numbers with the 10 Oct result. Recent Power Toto draws kept repeating numbers; 28 came up 5 times in these 10 draws.
- **A plain "replay the previous draw" ticket with no astrology matched 12**, just one fewer than the lead.
- **Turning down the astrology term makes it worse.** At weight 0 or 0.5 it matched 10; at full weight (1) it matched 13; at double weight (2) it matched 11. The peak at exactly 1 looks like noise, not a dose-response.
- **Random pairs do as well.** Using the same method with 200 random parameter pairs gave an average of 9.6 matches; 10% reached 13 or more, and the best reached 16.

So its strong last-10 result mostly reflects a stretch where Power Toto numbers repeated from one draw to the next. Over the longer test the same method was only mildly positive (z +1.38), and earlier tests found "repeat the last draw" no better than chance over the long run.

The breakdown is added to `analysis/FINDINGS.md`, committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Now rerank the leads based on last 10 test

**Answer:**

I'll rerank every current lead by its last-10 result. Games have different chances of matching, so I'll rank by how often a fair ticket would do at least as well. For context, I'll also score two no-astrology baselines on the same 10 draws in each game: "replay the previous draw" and "6 hottest numbers of the last 100 draws".

**Answer:**

Here are the current leads reranked on the last 10 draws (26 Sep – 17 Oct), with the two no-astrology baselines included for each game:

| Rank | Lead | Game | Matched / expected | Chance a fair ticket does as well |
|---|---|---|---|---|
| 1 | Tropical Moon sign × Jupiter nakshatra (analogy, last draw) | Power 6/55 | 13 / 6.5 | 0.8% |
| 2 | *Baseline: replay previous draw* | Power 6/55 | 12 / 6.5 | 2.1% |
| 3 | Jupiter rashi × Jupiter retrograde (hot) | Supreme 6/58 | 11 / 6.2 | 3.5% |
| 4 | *Baseline: hottest of last 100 draws* | Supreme 6/58 | 11 / 6.2 | 3.5% |
| 5 | Mars rashi × Venus combust (cold) | Magnum Life | 21 / 17.8 | 21% |
| 6 | Moon rashi × Mars combust (position) | Magnum Life | 20 / 17.8 | 30% |
| 7 | year yin/yang × day god (cold) | Power 6/55 | 8 / 6.5 | 33% |
| 8 | *Baseline: hottest of last 100 draws* | Power 6/55 | 8 / 6.5 | 33% |
| 9 | *Baseline: replay previous draw* | Magnum Life | 19 / 17.8 | 41% |
| 10 | karana × Venus rashi (cold) | Star 6/50 | 8 / 7.2 | 43% |
| 11 | Mercury nakshatra × Venus rashi (4D lead, hot) | Magnum Life | 18 / 17.8 | 53% |
| 12 | *Baseline: replay previous draw* | Star 6/50 | 7 / 7.2 | 60% |
| 13 | *Baseline: hottest of last 100 draws* | Magnum Life | 17 / 17.8 | 64% |
| 14 | *Baseline: hottest of last 100 draws* | Star 6/50 | 4 / 7.2 | 95% |
| 15 | solar term × month stem (position) | Supreme 6/58 | 3 / 6.2 | 96% |
| 16 | *Baseline: replay previous draw* | Supreme 6/58 | 3 / 6.2 | 96% |

Ranks 1, 3 and 15 were chosen without seeing these 10 draws. The others were chosen on data that overlaps them, which slightly flatters them, and none of them stands out anyway.

**Each top lead sits right next to a no-astrology baseline from the same game:**
- **#1 vs #2:** the Power Toto analogy beats "replay the previous draw" by just one number (13 vs 12). Its tickets are largely the previous draw.
- **#3 vs #4:** the Supreme Toto Jupiter lead ties exactly with "6 hottest of the last 100 draws" (11 each), because both pick numbers that were hot recently.
- **So the strong results reflect what happened in those games recently,** not the astrology on top. Power Toto kept repeating numbers from the previous draw, and Supreme Toto kept drawing its recent hot numbers.

**Everything from #5 down is within normal chance (21–96%),** including the old 4D lead and the Magnum Life leads.

If you track anything forward, track each top lead next to its baseline:
- the Power Toto analogy against "replay previous draw";
- the Jupiter ticket (15 39 42 44 48 54) against the last-100 hot ticket.

If the astrology leads don't keep beating their baselines, they add nothing.

The table is saved in `analysis/LAST10_RANKING.md`, committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Ok now rather than focusing on astrology, try to investigate this “So the strong results reflect what happened in those games recently, not the astrology on top. Power Toto kept repeating numbers from the previous draw, and Supreme Toto kept drawing its recent hot numbers.”

**Answer:**

Good direction. The question becomes whether these "recently hot" patterns are a real, lasting feature of the draws (for example a machine or ball-set quirk) or ordinary streaks that come and go. I'll test it per game against simulated fair draws:

1. **How unusual is the recent stretch?** How often has the history had 10-draw windows with this many repeats from the previous draw, or this many hot-number hits? And how often do fair draws produce them?
2. **Do streaks persist?** If a window had many repeats or hot hits, does the next window too? Persistence beyond chance would mean something real.
3. **Single-number streaks**, such as 28 appearing 5 times in 10 Power Toto draws: how rare is that in fair draws?
4. **Uneven number frequencies:** over rolling 100- and 300-draw windows, are some numbers more common than chance allows, especially recently? That's what a ball or machine bias would look like.
5. **Can it be exploited?** A walk-forward strategy plays "repeat last draw" or "hot numbers" only after a window where that pattern was working. That's what someone would do after noticing it.

**Answer:**

Power Toto's recent stretch is genuinely unusual, but it's the kind of streak that turns up from time to time in fair draws, and it doesn't continue long enough to use. I compared each game with 500 simulated histories of fair draws.

**What's unusual (Power and Supreme Toto, last 10 draws):**

| Pattern | Game | Last 10 draws | Share of fair draws as extreme |
|---|---|---|---|
| Numbers repeated from the previous draw | Power 6/55 | 12 (6.5 expected) | 2.2% |
| One number repeating: **28 came up 6 times** | Power 6/55 | 6 of 10 draws | 0.8% |
| Hits from the 6 hottest of the last 100 draws | Supreme 6/58 | 11 (6.2 expected) | 2.6% |

I checked the last 11 Power Toto draws against lottolyzer and they match exactly, so 28 really came up on 26 Sep, 30 Sep, 3, 10, 11 and 14 Oct. Earlier I said 5 times; it's 6.

**Why it's still not usable:**
- **These streaks are normal over a long history.** Each game has hundreds of 10-draw windows, and fair draws produce stretches like this regularly. Power Toto's best-ever window had 16 repeats, which fair histories beat 29% of the time. Single numbers coming up 6 or 7 times in 10 draws happen at the normal rate.
- **Hot streaks don't carry over.** A window where hot numbers did well tells you nothing about the next window (correlation −0.02 to +0.07, the same as fair draws). Supreme Toto's hot run is ordinary luck.
- **There's no ball or machine bias.** Number counts over rolling 100- and 300-draw windows are no more uneven than chance in any game, recently or overall. Star Toto's recent counts are actually more even than usual.
- **The data isn't the cause.** Consecutive draws sharing 3 or more numbers occur at the expected rate (e.g. Power Toto 47 vs 38.1 expected), so no copy errors are inflating the repeats.

**One small real-looking effect:** repeats from the previous draw cluster slightly in time in all four games. When one 10-draw window has many repeats, the next tends to have slightly more than usual: +0.03 to +0.14, where fair draws give about 0. Combined across the four games that's p ≈ 0.01, so it may be real, perhaps from how ball sets or machines are rotated.

But it's far too weak to profit from. Playing "repeat the previous draw" only right after a high-repeat window returned 1.00×, 1.04×, 1.05× and 0.79× of chance, all within the normal range for fair draws.

**Bottom line:** the patterns behind the "best leads" are real in the sense that they happened, but they're the normal ups and downs of a fair lottery. They don't persist enough to predict the next draw, so following Power Toto's "28 streak" or Supreme Toto's hot numbers won't give an edge.

The analysis is `analysis/recency.py`, with tables and checks in `analysis/RECENCY.md` and a summary in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Ok now check if the hot numbers by changing the number of previous rounds to be tested for predicting and optimize the number of previous rounds it to get a predicting mechanism

**Answer:**

I'll tune the look-back for the hot-number ticket per game: the k numbers that came up most in the previous N draws, for N = 5, 10, 15, 20, 30, 50, 75, 100, 150, 200, 300, 500, and all draws. I'll also try a time-decay version (recent draws count more, with half-lives of 5–200 draws).

To keep it honest:
1. **Choose N on older draws only** (25–70% of each game's history), then test that N on the later draws (70% up to the last 10) and on the last 10 draws.
2. **Re-optimise N every draw:** use whichever N worked best over the previous 200 draws. That's what someone would do in practice.
3. **Compare with 500 simulated fair histories.** Optimising N on pure noise also produces a "best N", so this shows how good an optimised look-back looks by chance.

**Answer:**

Tuning the look-back doesn't create a working predictor. In every game, the look-back that did best on older draws failed on later ones.

For each game I tried hot-number tickets built from the last 5, 10, 15, 20, 30, 50, 75, 100, 150, 200, 300 or 500 draws, or all draws. I also tried a time-weighted version where recent draws count more (half-lives of 5–200 draws). The best look-back was chosen on draws 25–70% of each game's history, then frozen and tested on the later draws and the last 10 draws.

| Game | Best look-back on older draws (z) | Later test draws (z) | Last 10: matched / expected | Re-optimised every draw (z) |
|---|---|---|---|---|
| Star 6/50 | 300 draws (+1.87) | **−2.05** | 11 / 7.2 | −1.54 |
| Power 6/55 | half-life 5 (−0.12) | +0.03 | 9 / 6.5 | −2.33 |
| Supreme 6/58 | 100 draws (+1.85) | −0.47 | 11 / 6.2 | +0.11 |
| Magnum Life | 150 draws (+0.30) | +0.22 | 16 / 17.8 | −0.79 |

"Re-optimised every draw" uses whichever look-back worked best over the previous 200 draws.

For comparison, I ran the same pipeline on 300 simulated fair histories, where no look-back can work:
- **The best look-back on older draws looked as good there as it does here:** about z +1.4 to +1.5, against +1.87 and +1.85 for Star and Supreme Toto.
- **The chosen look-back's later test score ranged from about −1.7 to +1.8.** All four real results fall inside that range.

**What it shows:**
- **Older performance doesn't predict later performance.** Across look-backs, the correlation between how a look-back did on older draws and how it did later is −0.50, +0.06, −0.03 and +0.00. Fair draws give about 0. Star Toto's −0.50 means the look-backs that did best earlier did *worst* later.
- **Re-optimising constantly doesn't help.** Chasing whichever look-back has been working lately scored below chance in three games.
- **The good last-10 results only look good after the fact.** Supreme Toto's chosen look-back (100 draws) got 11 against 6.2, but the same look-back was below chance over the longer test (−0.47). It's the recent hot streak from the last analysis, not a stable rule. The result also depends on how ties between equally frequent numbers are broken: Power Toto's 100-draw ticket matched 10 or 13 on the last 10 depending on the tie-break.

**Bottom line:** there's no look-back that turns hot numbers into a predictor. Every length works for a while and then stops, exactly as in fair draws. That matches the earlier finding that hot streaks don't carry over from one window to the next.

The script is `analysis/hot_window.py`, with the full curve for every look-back in `analysis/HOT_WINDOW.md` and a summary in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> now try the same for cold numbers

**Answer:**

I'll run exactly the same test with cold numbers: the k numbers that came up *least* often over the last N draws, or with time-decayed counts. I'll also add the classic **"overdue"** version, which picks the numbers with the longest gap since they last appeared. As before, the look-back is chosen on older draws, tested on later draws and the last 10, and compared with 300 simulated fair histories.

**Answer:**

Cold numbers come out the same as hot numbers: no look-back turns them into a predictor. I ran the identical test, with the look-back chosen on older draws, frozen, then tested on later draws and the last 10, and compared with 300 fair histories. I also added "overdue" numbers, the ones with the longest gap since they last appeared.

| Game | Best look-back on older draws (z) | Later test draws (z) | Last 10: matched / expected | Re-optimised every draw (z) | Overdue numbers (z) |
|---|---|---|---|---|---|
| Star 6/50 | 200 draws (+1.56) | +1.37 | 8 / 7.2 | +0.33 | +1.75 |
| Power 6/55 | half-life 20 (+1.65) | +0.03 | 5 / 6.5 | +0.26 | +0.26 |
| Supreme 6/58 | 200 draws (+1.29) | +0.16 | 6 / 6.2 | +0.21 | −0.42 |
| Magnum Life | 15 draws (+2.30) | +0.31 | 21 / 17.8 | −0.16 | −0.07 |

On fair histories, where nothing can work, the same pipeline's test score ranges from about −1.8 to +1.9.

**What it shows:**
- **Everything is inside the chance range.** The best result, Star Toto's 200-draw cold ticket at +1.37, is the sort of score fair draws produce regularly. Overdue numbers at +1.75 on Star Toto are also ordinary (the earlier fairness check had overdue numbers at 0.90× on Supreme Toto).
- **The look-back that looks best on older draws doesn't hold up.** Magnum Life's 15-draw cold ticket looked strongest of all on older draws (+2.30) and dropped to +0.31 later.
- **Magnum Life's apparent consistency is normal.** Its look-backs that did well before did a bit better later too (correlation +0.26 to +0.34). But because the look-backs overlap so much, fair histories swing ±0.3 on this measure and reach that level 18% of the time. In the other three games the correlation is negative (−0.12 to −0.40).

**Hot vs cold, side by side:** neither direction carries information. The same game can look "hot" in one period and "cold" in another; for example, Star Toto's 300-draw hot ticket failed (−2.05) while its 200-draw cold ticket did mildly well (+1.37). That's what you'd expect if numbers come up independently and the swings are noise.

The run is `analysis/hot_window.py --cold`, with the full table for every look-back in `analysis/COLD_WINDOW.md` and a summary in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> now combine hot and cold numbers into one ticket

**Answer:**

I'll build mixed tickets: the h hottest numbers from one look-back plus the (k − h) coldest from another, with no overlap.

- **Hot share:** h runs from 0 (all cold) to k (all hot), so the pure versions are included.
- **Hot look-back:** 10, 20, 50, 100, 200, 300 draws, or all draws.
- **Cold look-back:** the same options, plus "overdue" (longest gap since last drawn).

That's 392–504 combinations per game. The protocol is the same as before: choose on older draws, freeze, test on later draws and the last 10, re-optimise every draw as a second strategy, and compare with fair histories.

**Answer:**

The `label` helper I just wrote is garbled; I'll rewrite it before running.

**Answer:**

Each game history takes about 2 seconds, so I'll use 100 fair histories per game (about 13 minutes in total) and run it in the background.

**Answer:**

The mixed hot + cold search is committed and running in the background: 295 combinations per Toto game and about 400 for Magnum Life, plus 100 fair histories each. It should take around 13 minutes, and I'll report the results when it finishes.

**Answer:**

Mixing hot and cold numbers in one ticket doesn't help either; it gives the optimiser more combinations to overfit with. I tried every mix of h hot numbers from one look-back and the rest cold from another (or overdue), from all-cold to all-hot: 295 combinations per Toto game and about 400 for Magnum Life. As before, the best mix was chosen on older draws, frozen, and tested on later draws and the last 10.

| Game | Best mix on older draws (z) | Later test draws (z) | Last 10: matched / expected | Re-chosen every draw (z) |
|---|---|---|---|---|
| Star 6/50 | 3 hot (last 300) + 3 cold (last 200) (+2.60) | +0.98 | 8 / 7.2 | +0.27 |
| Power 6/55 | 6 cold (last 50), i.e. no hot at all (+2.14) | −0.30 | 6 / 6.5 | −1.29 |
| Supreme 6/58 | 4 hot (last 100) + 2 cold (last 200) (+2.64) | −1.60 | 12 / 6.2 | −0.03 |
| Magnum Life | 1 hot (last 50) + 7 cold (last 10) (+2.69) | −0.64 | 18 / 17.8 | −2.08 |

**Compared with fair draws** (same pipeline on 100 simulated fair histories per game):
- **The "best mix" scores just as high on noise.** Fair histories average z +2.19 to +2.36 for their best mix, against +2.14 to +2.69 here. With hundreds of combinations, something always looks good on older draws.
- **On later draws the chosen mixes fall back to chance or below.** Fair histories range from about −1.7 to +1.6, and Supreme Toto's mix (−1.60) is at the bottom of that range.
- **Re-choosing the mix every draw is worse still.** Magnum Life at −2.08 is below what fair draws usually give.
- **Supreme Toto's 12 matches on the last 10 draws come from the same mix that failed on the longer test (−1.60).** It's the recent hot streak in that game again, not a stable rule.

**The bigger picture:** every way of tuning the hot/cold pattern behaves exactly like fair, independent draws. That covers pure hot, pure cold, overdue, any look-back, and any mix. This includes the time-decayed versions and re-optimising every draw. What looks best on past draws reflects past noise, and it doesn't carry forward.

The script is `analysis/hot_cold_mix.py`, with the top-10 combinations per game in `analysis/HOT_COLD_MIX.md` and a summary in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> now try combining hot cold with the astrology leads

**Answer:**

I'll combine the three signals into one score per number:

**score = α·(hot/cold over the last Nh draws) + β·(hot/cold over the last Nc draws) + γ·(astrology cell signal)**

- **Astrology signal:** how often the number came up before on dates with the same parameter values. It's chosen from the 20 best single parameters and pairs, ranked only on the older periods of the earlier lead search; that ranking never used the test draws.
- **Weights:** α, β ∈ {−1, 0, +1} (a negative weight turns hot into cold); γ ∈ {0, 0.5, 1, 2}; Nh, Nc ∈ {20, 100, 300}.
- **Size of the search:** about 6,500 combinations per game, chosen on draws 25–70%, then tested on later draws and the last 10.
- **The key checks:** whether the chosen mix uses astrology at all (γ > 0), and whether it beats the same mix with astrology removed.
- **Control:** the whole search repeated on 5 shifted calendars, where the astrology part is meaningless.

**Answer:**

Combining hot/cold with the astrology leads didn't help. The optimiser always picked a strong astrology weight, but in three of four games the result did worse on later draws than the same hot/cold mix without astrology.

Each number got one score: a hot or cold count over one look-back, plus another over a second look-back, plus an astrology signal (how often it came up on dates with the same parameter values). The astrology set was one of the 20 that ranked best on the earlier lead search's older periods. That gave about 3,000 combinations per game, chosen on older draws and tested on later draws and the last 10.

| Game | Chosen mix | Astrology weight | Older draws (z) | **Later draws (z)** | Same mix without astrology (z) | Last 10 |
|---|---|---|---|---|---|---|
| Star 6/50 | hot (last 300) + Mercury combust × day officer | 2 | +4.01 | **−2.64** | −1.73 | 9 / 7.2 |
| Power 6/55 | hot (20) − hot (100) + karana × adhika masa | 2 | +4.75 | **−1.15** | +0.93 | 6 / 6.5 |
| Supreme 6/58 | hot (last 300) + paksha × Rahu rashi | 2 | +4.31 | **−0.52** | +0.16 | 5 / 6.2 |
| Magnum Life | cold (last 300) + Venus nakshatra × planets with Moon | 0.5 | +3.81 | **+0.89** | +0.51 | 22 / 17.8 |

**Shifted-calendar control** (same search on 5 calendars where astrology can't be linked to the numbers):
- **The chosen mix always used astrology there too** (weight 0.5–2).
- **It scored just as high on older draws:** z +3.1 to +4.8.
- **It scored −1.28 to +1.32 on later draws,** the same range as the real calendar.

**Why:** adding the astrology term doesn't add information; it adds flexibility. With 20 astrology sets and several weights to choose from, the search can fit the noise in the older draws better. That's why the older-draw scores jump from about +2 (hot/cold alone) to +4, and on meaningless calendars too. On later draws that fitted noise is gone, and the astrology version usually ends up worse.

Only Magnum Life's chosen mix did slightly better with astrology (+0.89 vs +0.51). That's well inside the shifted calendars' range, so it's noise too.

**Overall:** hot/cold alone, astrology alone, and the two combined all behave the same way: they look strong on the draws they were tuned on and revert to chance afterwards. That's consistent with every other test in this project: these games behave like fair, independent draws.

The script is `analysis/hotcold_astro.py`, with results in `analysis/hotcold_astro_results.json` and a summary in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Try to find some other ways for predictive model, do research in the web, on probably with other astrological factors

**Answer:**

Before building anything new, I'll search the web for astrological methods people use for lottery numbers that we haven't tried yet.

**Answer:**

I searched the web for other astrological ways people pick lottery numbers, and tested the new factors I found. Nothing came out as a reliable predictor; one rule on Star Toto is worth watching.

**What the research found:** practitioner methods, but no source with tested evidence that any of them predict lottery results. Even a BaZi/Feng Shui practitioner [warns against using it as a gambling tool](https://www.masterseanchan.com/blog/leverage-bazi-feng-shui-win-lottery/). The factors I hadn't tried yet:
- **Part of Fortune**, the Arabic "lot of luck": Ascendant + Moon − Sun by day, reversed at night ([Wikipedia](https://en.wikipedia.org/wiki/Arabic_parts), [Skyscript](https://www.skyscript.co.uk/glossary/part-of-fortune));
- **Western aspects** between planets: conjunctions, sextiles, squares, trines, oppositions;
- **KP ruling planets**: Moon's sign and star lord, lagna's sign and star lord, and the day lord ([RoxyAPI KP guide](https://roxyapi.com/blogs/kp-astrology-krishnamurti-paddhati-sub-lord-horary-guide), [Vikaspedia](https://en.vikaspedia.in/viewcontent/education/education-best-practices/krishnamurti-paddhati-(kp)-astrology?lgn=en));
- **date numerology**, Pythagorean or Chaldean ([lucky number calculator](https://rapidtoolset.com/en/tool/lucky-number-calculator));
- **He Tu numbers** for the five elements ([Source Library](https://sourcelibrary.org/book/untitled-250/page/6992cffff5b4f75c1a4c9ef1)).

From the Chinese almanac, I also added the **daily Nine Star** and the **Plum Blossom trigrams**. The Nine Star uses the standard rule, which I haven't checked against a printed almanac.

**Test 1: rules that name numbers directly.** Examples: the Part of Fortune degree turned into a number, KP numbers, numbers sharing the date's digit sum, He Tu digits for the day's element. These need no training, so they can't be overfitted. That's 11 rules across 4 games, 44 tests:
- **The spread matches chance:** results range from z −2.28 to +2.83. Three passed |z| > 1.96, against 2.2 on average for shifted calendars, and the average z (+0.08) is beaten by 29% of shifted calendars.
- **The best rule is the universal day number on Star Toto.** It picks the numbers whose digit sum matches the date's (e.g. 18 Oct → digit sum 2 → 02 11 20 29 38 47). It scored 1.08× chance (z +2.83), and it was positive in all three thirds of Star Toto's history.
- **But it's the best of 44 tests** (8.5% of shifted calendars do as well), and it's absent from Power Toto and Supreme Toto, which are drawn the same evenings by the same operator. A date-based effect would have to appear in all three. On the last 10 draws it matched 3 against 6.7 expected.

**Test 2: the new factors as lead parameters.** This used about 30 new parameters, alone and paired with all existing ones, with the same replication test and shifted-calendar control as before.
- **The results match the shifted calendars.** How well past favourites carried over was 0.966–1.001× here, against 0.980–1.007× there.
- **The walk-forward leads (picked before the test draws) scored −1.57 to +2.12 on the later draws,** within what shifted calendars produce.
- **The Plum Blossom trigrams on Supreme Toto clustered a little more than shifted calendars do, but that didn't carry forward** to the later draws (test z +0.54).

**What I logged:** the universal-day tickets for Star Toto, so future draws can settle it:
- 18 Oct: **02 11 20 29 38 47**
- 21 Oct: **05 14 23 32 41 50**

**Bottom line:** these extra factors behave like everything tested before: within chance, with the occasional standout that doesn't repeat across games or periods.

The script is `analysis/extra_astro.py`; the new factors for every date are in `data/astro_params_extra.csv`, and the tables are in `analysis/EXTRA_ASTRO.md` and `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

Sources:
- [Arabic parts (Wikipedia)](https://en.wikipedia.org/wiki/Arabic_parts)
- [Skyscript: Part of Fortune](https://www.skyscript.co.uk/glossary/part-of-fortune)
- [Hermetic Lots (Benebell Wen)](https://benebellwen.com/astrology-2/hermetic-lots/)
- [KP Astrology guide (RoxyAPI)](https://roxyapi.com/blogs/kp-astrology-krishnamurti-paddhati-sub-lord-horary-guide)
- [Krishnamurti Paddhati (Vikaspedia)](https://en.vikaspedia.in/viewcontent/education/education-best-practices/krishnamurti-paddhati-(kp)-astrology?lgn=en)
- [Lucky Number Calculator](https://rapidtoolset.com/en/tool/lucky-number-calculator)
- [He Tu and the Five Elements (Source Library)](https://sourcelibrary.org/book/untitled-250/page/6992cffff5b4f75c1a4c9ef1)
- [Can You Leverage BaZi & Feng Shui to Win the Lottery? (Master Sean Chan)](https://www.masterseanchan.com/blog/leverage-bazi-feng-shui-win-lottery/)

---

**User:**

> Ok so far rank the leads based

**Answer:**

Your message looks cut off after "based". I'll rank on the same basis as last time, the last 10 draws, now including every lead from the newer methods. To keep it fair:
- each lead is scored by how often a fair ticket of the same size would do at least as well;
- I note whether each lead was chosen without seeing those 10 draws ("clean");
- I add each lead's longer-test score where it has one.

**Answer:**

Your message cut off after "based", so I've ranked on the last 10 draws (26 Sep – 17 Oct) as before. This time all 100 leads, rules and baselines are in, across every method we've tried. Here's the top 10:

| Rank | Lead | Method | Game | Matched / expected | Chance a fair ticket does as well | Longer test (z) |
|---|---|---|---|---|---|---|
| 1 | Tropical Moon sign × Jupiter nakshatra | analogy, selected params | Power 6/55 | 13 / 6.5 | 0.8% | +1.38 |
| 2 | 4 hot (last 100) + 2 cold (last 200) | hot/cold mix | Supreme 6/58 | 12 / 6.2 | 1.4% | **−1.60** |
| 3 | *Baseline: replay previous draw* | no astrology | Power 6/55 | 12 / 6.5 | 2.1% | — |
| 4 | Moon longitude → number | number rule | Star 6/50 | 4 / 1.2 | 2.4% | −0.12 |
| 5 | KP numbers of Moon/Asc/Sun → numbers | number rule | Supreme 6/58 | 7 / 3.1 | 2.8% | +1.31 |
| 6 | Jupiter rashi × Jupiter retrograde (hot) | lead search | Supreme 6/58 | 11 / 6.2 | 3.5% | +1.75 |
| 7 | *Hot numbers, last 100 draws* | hot look-back | Supreme 6/58 | 11 / 6.2 | 3.5% | −0.47 |
| 8 | Jupiter longitude → number | number rule | Magnum Life | 5 / 2.2 | 5.0% | −0.34 |
| 9 | Analogy model "direct" | analogy | Magnum Life | 23 / 17.8 | 8.0% | −0.49 |
| 10 | Part of Fortune degree → number | number rule | Power 6/55 | 3 / 1.1 | 8.7% | +0.03 |

All ten were chosen without seeing these 10 draws, apart from the no-astrology baseline.

**How to read it:**
- **The count of "winners" is what chance predicts.** 8 of the 100 entries reached the 5% level; if nothing works, about 5 would. That's how it looks when every lead is just luck.
- **The top results don't hold up over longer periods.** #2, the Supreme hot/cold mix, scored −1.60 on its longer test. The number rules at #4 and #8 are about average across their whole histories (−0.12 and −0.34).
- **The two leads that also have a positive longer-test score are #1 and #6.** Each is matched by a plain no-astrology ticket in its own game: #1 is one number ahead of "replay previous draw" (#3), and #6 ties exactly with "hot numbers, last 100 draws" (#7). The astrology adds at most one number on top of what recent draws already explain.
- **The universal-day rule (Star Toto)** was the best number rule over all draws (z +2.83), but it's near the bottom on the last 10 (3 vs 6.7).

**What I'd watch:** #1 and #6, each alongside its plain baseline. Only if they keep beating those baselines on new draws would it suggest anything real. Their tickets for 18 and 21 Oct are already logged, except #1's, which I can add.

The full 100-row table is in `analysis/LAST10_RANKING.md`, committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Ok now rather than the leads choosing only 1 ticket, I want you to redo the analysis for all the leads and make it produce top 10 tickets. And then, train and test them for the 10 unseen test.

**Answer:**

Here's how I'll set this up:

**Which leads.** Every ticket-producing method, each with the choice it already made without seeing the last 10 draws:
- hot look-back, cold look-back, hot/cold mix, hot/cold + astrology;
- the 4 analogy models, 3 embedding/language models, and 16 selected-parameter models;
- a fresh astrology lead search per game with the last 10 draws hidden, keeping the top 5 hot/cold/position leads;
- baselines: replay previous draw, hot last 100, and 10 random tickets.

Number rules name only 1–6 numbers, so they can't make 10 tickets and are left out.

**10 tickets per draw.** Each method gives every number a score. Ticket 1 is the top k numbers; tickets 2–10 are the next-best combinations by total score, made by swapping one or two numbers.

**Test.** I'll score the last 10 draws, still walk-forward: each draw can use the draws before it, but every model choice stays frozen. Measures:
- total matches across all 10 tickets;
- the best ticket per draw;
- the number of tickets with 3 or more matches.

**Chance.** For each method's actual tickets, I'll simulate 20,000 fair sets of 10 draws. That accounts for how much its tickets overlap.

**Answer:**

With 10 tickets each, the same two leads come out on top again, Power Toto's analogy and Supreme Toto's Jupiter lead. But in both games, plain no-astrology tickets did almost as well, so they're still the recent-draw patterns rather than astrology.

I re-ran 23 ticket-producing methods per game, 92 in all, each making **10 tickets per draw**:
- ticket 1 is its top pick; tickets 2–10 are its next-best combinations;
- every choice was frozen without seeing the last 10 draws (26 Sep – 17 Oct);
- each draw uses only earlier draws.

I scored all 100 tickets per method against the actual draws. Chance comes from 20,000 simulated fair sets of 10 draws on the same tickets, which accounts for how much the tickets overlap.

**Top methods per game** (total matches over 100 tickets vs chance; tickets with 3+ matches):

| Game | Method | Matches (expected) | Chance | 3+ tickets (expected) |
|---|---|---|---|---|
| Power 6/55 | **Analogy: tropical Moon sign + Jupiter nakshatra** | 116 (65.3) | 0.9% | 9 (1.3) |
| Power 6/55 | *Baseline: replay previous draw* | 105 (65.4) | 3.5% | 4 (1.3) |
| Power 6/55 | *Baseline: hot last 100* | 101 (65.3) | 4.8% | 7 (1.3) |
| Supreme 6/58 | **Hot+cold mix (4 hot / 2 cold)** | 110 (61.9) | 1.3% | 0 (1.1) |
| Supreme 6/58 | **Jupiter rashi × Jupiter retrograde (hot)** | 111 (62.1) | 1.4% | 3 (1.1) |
| Supreme 6/58 | *Baseline: hot last 100* | 101 (62.1) | 3.3% | 0 (1.2) |
| Magnum Life | Moon rashi × Mars combust (position) | 234 (178.0) | 3.3% | 41 (23.6) |
| Magnum Life | Analogy "direct" | 232 (178.1) | 4.1% | 41 (23.6) |
| Star 6/50 | Hot numbers, last 300 | 100 (72.1) | 9.8% | 0 (1.8) |
| every game | *10 random tickets* | at chance (29–78%) | — | — |

**How to read it:**
- **Overall, it looks like chance.** 10 of the 92 methods reached the 5% level, against about 4.6 expected. Even that excess is inflated, because the low ones are near-copies of each other: in Supreme Toto, four methods all pick the same recent hot numbers.
- **Power Toto's top lead is lumpy, not consistent.** 7 of its 9 three-number tickets came from one draw (30 Sep), when its overlapping tickets all held 28 33 34 and the draw was 13 28 33 34 39 44. On most other draws its tickets matched 0–2 numbers. Replaying the previous draw gave 105 matches without any astrology.
- **Supreme Toto's leaders are all the same signal.** The hot+cold mix, the Jupiter lead and plain "hot last 100" are all riding the game's recent hot streak, which the earlier recency check showed doesn't persist.
- **Magnum Life and Star Toto leaders are at 3–10% chance,** which is ordinary for the best of 23 methods.

**What 10 tickets doesn't change:** playing more tickets raises the number of matches in proportion, but it doesn't make a method more predictive. The ranking looks the same as with 1 ticket: the leads that do well are the ones copying the last few weeks' draws in that game.

Full tables per game, including the tickets themselves, are in `analysis/TEN_TICKETS.md`, from the script `analysis/ten_tickets.py`; a summary is in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Actually I’m looking for more number match in one ticket, which one perform the best in this for 10 tickets?

**Answer:**

Since you want the most numbers matched within a single ticket, I'll re-rank by two measures:
- the best ticket each draw, summed over the 10 draws;
- the highest number of matches any single ticket got.

I'll also count tickets with 3+ and 4+ matches, and work out exactly how likely those counts are by chance for the same tickets.

**Answer:**

For the most numbers in one ticket, the best was in **Magnum Life: the "direct" and "map" analogy models each produced a ticket matching 6 of 8 numbers**. In the Toto games, no ticket from any method got more than 3.

**The 6-of-8 tickets:** on 11 Oct 2026 the draw was 02 07 14 15 16 22 25 27. Two tickets from the direct analogy model matched 6 numbers each:
- 02 14 16 21 22 25 27 28 matched 02 14 16 22 25 27;
- 02 14 15 16 21 22 27 28 matched 02 14 15 16 22 27.

The map model produced the same two tickets. For these exact tickets, a fair draw gives a 6+ match somewhere in the 10 draws about 2% of the time.

**Best-ticket ranking** (best ticket's matches each draw, summed over the 10 draws):

| Rank | Game | Method | Best per draw, summed (expected) | Chance | Most in one ticket | 3+ tickets (expected) | 4+ tickets (expected) |
|---|---|---|---|---|---|---|---|
| 1 | Power 6/55 | *Baseline: replay previous draw* | 19 (11.7) | 0.5% | 3 | 4 (1.3) | 0 |
| 2 | Power 6/55 | Analogy: tropical Moon sign + Jupiter nakshatra | 17 (10.3) | 1.1% | 3 | 9 (1.3) | 0 |
| 3 | Magnum Life | Moon rashi × Mars combust (position) | 31 (24.1) | 2.9% | 5 | 41 (23.6) | 13 (5.4) |
| 4 | Supreme 6/58 | Hot+cold mix (4 hot / 2 cold) | 15 (9.9) | 4.2% | 2 | 0 (1.1) | 0 |
| 5 | Magnum Life | **Analogy "direct"** | 31 (25.2) | 4.7% | **6** | 41 (23.6) | 13 (5.4) |
| 6 | Supreme 6/58 | Jupiter rashi × Jupiter retrograde (hot) | 15 (10.6) | 6.6% | 3 | 3 (1.1) | 0 |
| 7 | Magnum Life | Mars rashi × Venus combust (cold) | 30 (24.6) | 7.0% | 5 | 42 (23.5) | **22** (5.4) |

**What to take from this:**
- **The best single-ticket method in the Toto games has no astrology in it.** "Replay the previous draw" ranks first: it got the most matches from its best ticket each draw. It's riding Power Toto's recent run of repeated numbers.
- **In Magnum Life, 4+ matches came up far more than chance:** Mars rashi × Venus combust got 22 tickets with 4+ against 5.4 expected, and Moon rashi × Mars combust 13. But each method's 10 tickets are near-copies of each other, so one good draw lifts many tickets at once. The 6-of-8 tickets all came from the same draw (11 Oct).
- **The 2% chance for the 6-of-8 is for one method.** With about 23 Magnum Life methods tried, at least one hitting 6 is about a 40% event.
- **In the Toto games nobody reached 4 numbers** in a ticket. That's normal: 100 Toto tickets average only about 0.06 tickets with 4+ matches by chance.

**If you want the single-ticket favourites to track forward:**
- **Magnum Life:** the analogy "direct" model and the Mars rashi × Venus combust cold lead;
- **Power Toto:** the analogy lead, alongside "replay previous draw";
- **Supreme Toto:** the Jupiter lead.

Just keep in mind that no method has yet beaten its no-astrology baseline in a way that held up.

The full table is in `analysis/TEN_TICKETS_BEST.md`, committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Now redo all the analysis for the astrological parameter single and pair, where they produce 10 tickets and you can try the llm methods, cold, hot, and all other that we have done. And see if a new lead emerges where the focus is to get more numbers that matches the result

**Answer:**

This is a full redo, so here's the design.

**Search space**
- **Parameters:** 114 astrological parameters (the 83 original plus the 31 new ones from the web research), alone and in all pairs: about 6,550 sets per game.
- **Four ways to score numbers within each set's cell:**
  1. hot: numbers seen most often in that cell;
  2. cold: numbers seen least;
  3. position: numbers likely at any sorted position;
  4. hot + recent: the cell's hot score plus each number's hot score over the last 100 draws, like the hot/cold + astrology mix.
- **10 tickets per draw,** built from each method's ranking with a fixed pattern of one- or two-number swaps, so every method's tickets have the same structure.

**What counts as success: more numbers in one ticket.** Each draw is scored by its best ticket's matches, summed over the draws, with the count of 3+ tickets reported alongside.

**Selection without the last 10 draws.** Leads are ranked by how consistently their best ticket beat chance in all three earlier periods of each game's history. The top 10 per game are then tested on the last 10 draws.

**Comparisons**
- **Chance:** the same search repeated on 4 shifted calendars.
- **Earlier methods:** the LLM/embedding, analogy and hot/cold results from the previous 10-ticket run.

The analogy and embedding models aren't per-parameter methods, so they're too heavy to rerun for 6,550 sets. Their 10-ticket results from the previous run are the comparison.

**Answer:**

The new 10-ticket lead search is committed and running in the background. It covers every one of the 114 astrological parameters and their pairs, with 4 scoring patterns, selected on best-ticket matches and repeated on 4 shifted calendars. It should take about 10–15 minutes, and I'll report the top leads per game and how they did on the last 10 draws when it finishes.

**Answer:**

No new lead emerged. I searched every astrological parameter (all 114, including the 31 new ones) and every pair, with 4 ways of scoring numbers in each: about 26,000 candidates per game. Each produced 10 tickets per draw, judged by its best ticket's matches. Leads were chosen without the last 10 draws, on how consistently they beat chance in three earlier periods, and the top 10 per game were then tested on those 10 draws.

**Did the selected leads do better on the last 10 draws?**

| Game | Top 10 leads: best ticket per draw, summed (expected) | Same selection on 4 shifted calendars | Leads beating chance in all 3 earlier periods (shifted calendars) |
|---|---|---|---|
| Star 6/50 | 121 (106.3) | 66, 103, 106, 113 | 31 (28–61) |
| Power 6/55 | 93 (96.7) | 98, 98, 104, 104 | 40 (29–80) |
| Supreme 6/58 | 83 (91.9) | 93, 104, 105, 113 | 131 (65–131) |
| Magnum Life | 247 (236.5) | 233, 238, 239, 257 | 62 (48–108) |

- **The real calendar produces no more consistent leads than meaningless shifted calendars.** In each game the count sits inside the shifted range.
- **The top leads did no better than the shifted calendars' top leads** on the last 10 draws. In Power and Supreme Toto they did slightly worse than chance; in Star Toto and Magnum Life slightly better, but within the shifted range.

**Best individual results among the selected leads:**
- **Power 6/55, Venus nakshatra × Na Yin element (position):** 14 vs 9.7, and 11 tickets with 3 matches (1.3 expected). A fair draw does this about 8% of the time. All 11 came from its 10 near-copy tickets, which move together.
- **Star 6/50, karana × KP Moon star lord (hot):** 14 vs 10.6 (15%).
- **Magnum Life:** the best single ticket matched 4 of 8 numbers, ordinary for Magnum Life.
- **No ticket matched more than 3 numbers in any Toto game.**

**Compared with the earlier methods** on the same 10 draws, the strongest single tickets still came from:
- "replay the previous draw" on Power Toto: best-ticket sum 19 vs 11.7;
- the analogy models on Magnum Life: two tickets matched 6 of 8.

Both reflect the recent-draw patterns found earlier, not the astrology.

**Bottom line:** searching specifically for "more numbers in one ticket" across every astrological parameter and pair finds nothing beyond chance. Whatever ranks top is replaced by different parameters in the next period, just as happens on calendars with no astrological meaning.

The script is `analysis/lead_search10.py`. The top-10 tables per game, with the tickets they played, are in `analysis/LEAD_SEARCH10.md`, and the summary is in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Show me the leads

**Answer:**

Here are the top 10 leads per game from the new search. Each was chosen without the last 10 draws, on how consistently its best ticket beat chance in three earlier periods (z for early / validation / late). The columns on the right show how it did on the last 10 draws, playing 10 tickets per draw.

**Star Toto 6/50** (a fair best ticket averages 10.6 over 10 draws)

| # | Lead | Pattern | z early / valid / late | Last 10 best-ticket sum | Chance | Most in one ticket | 3+ tickets (exp. 1.8) |
|---|---|---|---|---|---|---|---|
| 1 | nakshatra lord × karana | hot | +2.41 / +1.71 / +2.12 | 13 | 24% | 2 | 0 |
| 2 | karana × KP Moon star lord | hot | +1.80 / +1.51 / +1.50 | 14 | 15% | 2 | 0 |
| 3 | Mars retrograde × KP Sun star lord | hot | +1.50 / +2.88 / +1.61 | 10 | 65% | 3 | 3 |
| 4 | nakshatra lord × karana | position | +1.50 / +1.44 / +1.67 | 10 | 65% | 2 | 0 |
| 5 | KP Moon star lord × KP Sun star lord | position | +2.29 / +1.51 / +1.39 | 12 | 37% | 3 | 4 |
| 6 | Part of Fortune nakshatra × Sun–Saturn aspect | cold | +1.37 / +1.51 / +2.90 | 13 | 24% | 3 | 4 |
| 7 | year yin/yang × day god | cold | +1.31 / +1.51 / +1.34 | 8 | 88% | 2 | 0 |
| 8 | KP Asc sub lord × KP Sun star lord | hot | +1.93 / +1.37 / +1.22 | 14 | 15% | **4** | **8** |
| 9 | Venus nakshatra × Mercury–Jupiter aspect | cold | +1.31 / +1.23 / +1.17 | 14 | 15% | 3 | 1 |
| 10 | Jupiter retrograde × month | hot | +1.25 / +1.99 / +1.17 | 13 | 24% | 3 | 5 |

**Power Toto 6/55** (fair best ticket: 9.7)

| # | Lead | Pattern | z early / valid / late | Last 10 best-ticket sum | Chance | Most in one ticket | 3+ tickets (exp. 1.3) |
|---|---|---|---|---|---|---|---|
| 1 | Jupiter nakshatra × Mars retrograde | cold | +1.86 / +1.84 / +1.89 | 9 | 66% | 2 | 0 |
| 2 | Jupiter nakshatra | cold | +2.08 / +1.64 / +1.65 | 9 | 66% | 2 | 0 |
| 3 | Jupiter nakshatra × Rahu rashi | cold | +1.64 / +1.84 / +1.56 | 11 | 37% | 3 | 4 |
| 4 | **Venus nakshatra × Na Yin element** | position | +1.73 / +1.49 / +1.56 | **14** | **7.8%** | 3 | **11** |
| 5 | Mars nakshatra × Mercury–Saturn aspect | hot | +1.77 / +1.69 / +1.48 | 5 | 98% | 2 | 0 |
| 6 | Jupiter nakshatra × lunar leap month | cold | +1.68 / +1.74 / +1.44 | 8 | 79% | 2 | 0 |
| 7 | hora lord × Moon–Venus aspect | cold | +1.81 / +1.49 / +1.40 | 10 | 51% | 3 | 3 |
| 8 | Jupiter nakshatra × ayana | cold | +2.17 / +1.39 / +2.05 | 11 | 37% | 2 | 0 |
| 9 | KP Moon star lord × hard aspects | position | +1.37 / +2.24 / +1.85 | 8 | 79% | 3 | 2 |
| 10 | nakshatra lord × hard aspects | position | +1.32 / +1.84 / +1.97 | 8 | 79% | 3 | 4 |

**Supreme Toto 6/58** (fair best ticket: 9.2)

| # | Lead | Pattern | z early / valid / late | Last 10 best-ticket sum | Chance | Most in one ticket | 3+ tickets (exp. 1.2) |
|---|---|---|---|---|---|---|---|
| 1 | year animal × Plum Blossom trigrams | position | +2.67 / +1.74 / +2.49 | 9 | 59% | 2 | 0 |
| 2 | Mercury–Saturn aspect × Plum Blossom trigrams | hot+recent | +1.75 / +1.94 / +1.69 | 9 | 59% | 2 | 0 |
| 3 | Mercury nakshatra × Moon navamsa | position | +1.93 / +1.69 / +1.98 | 7 | 85% | 2 | 0 |
| 4 | KP Asc sub lord × Venus–Mars aspect | hot+recent | +1.61 / +1.89 / +2.19 | 12 | 19% | 2 | 0 |
| 5 | Yellow/Black path × Mercury–Jupiter aspect | hot | +1.61 / +1.64 / +2.32 | 9 | 59% | 2 | 0 |
| 6 | Part of Fortune nakshatra × Plum Blossom trigrams | position | +2.39 / +2.35 / +1.61 | 5 | 97% | 2 | 0 |
| 7 | year yin/yang × Plum Blossom trigrams | hot | +1.93 / +1.58 / +1.73 | 8 | 73% | 1 | 0 |
| 8 | year yin/yang × Plum Blossom trigrams | position | +1.66 / +1.58 / +1.69 | 6 | 93% | 1 | 0 |
| 9 | paksha × Plum Blossom trigrams | hot | +1.52 / +1.99 / +1.65 | 9 | 59% | 2 | 0 |
| 10 | Jupiter rashi × 19:00 hour stem | hot+recent | +1.80 / +1.84 / +1.48 | 9 | 59% | 2 | 0 |

**Magnum Life 8/36** (fair best ticket: 23.6)

| # | Lead | Pattern | z early / valid / late | Last 10 best-ticket sum | Chance | Most in one ticket | 3+ tickets (exp. 23.7) |
|---|---|---|---|---|---|---|---|
| 1 | Venus nakshatra × KP Moon sub lord | hot | +1.60 / +1.81 / +1.58 | 21 | 82% | 4 | 21 |
| 2 | paksha × Mercury retrograde | cold | +1.75 / +1.59 / +1.39 | 25 | 40% | 4 | 27 |
| 3 | month pillar × day element | cold | +1.40 / +2.20 / +1.39 | 24 | 51% | 4 | 12 |
| 4 | Moon navamsa × Moon–Mars aspect | hot | +1.75 / +1.54 / +1.30 | 25 | 40% | 4 | 26 |
| 5 | Venus rashi × Rahu nakshatra | cold | +1.30 / +1.37 / +1.89 | 25 | 40% | 4 | 25 |
| 6 | **Mars rashi × month** | cold | +2.60 / +2.09 / +1.26 | **33** | **0.6%** | 4 | **57** |
| 7 | Moon navamsa × Moon–Mars aspect | position | +1.30 / +1.59 / +1.26 | 25 | 40% | 4 | 27 |
| 8 | month pillar × Sun–Venus aspect | cold | +1.35 / +2.76 / +1.26 | 19 | 93% | 4 | 13 |
| 9 | karana × day pillar | hot | +1.40 / +1.20 / +1.21 | 25 | 40% | 4 | 34 |
| 10 | Moon rashi × Mars–Jupiter aspect | position | +1.35 / +1.20 / +1.35 | 25 | 40% | **5** | 27 |

**Two results stand out:**
- **Magnum Life #6, Mars rashi × month (cold): best-ticket sum 33 vs 23.6, and 57 tickets with 3+ matches against 23.7 expected.** For one lead, that's a 0.6% chance; I missed it in my last summary, which only covered each game's top 5.
  - **Against it:** it's the best of 40 leads tested on these draws, which makes about a 1-in-5 chance that one does this well. Its 10 tickets are near-copies, so a good draw lifts many of them together.
  - **For it:** Mars rashi with cold numbers also appeared earlier as a Magnum Life lead (Mars rashi × Venus combust, cold).
- **Power Toto #4, Venus nakshatra × Na Yin element (position):** 14 vs 9.7, with 11 tickets of 3 matches (7.8% chance).

**Overall:** most leads landed near or below chance on the last 10 draws. Taken together, the top 10 did no better than the top 10 from shifted calendars in any game.

If you'd like, I can log Mars rashi × month's 10 Magnum Life tickets for the next draws so we can see whether it holds. Mars stays in each rashi for about 6 weeks, so its tickets change slowly.

---

**User:**

> Are they all the results of the last 10 draws?

**Answer:**

Partly. Each table mixes two kinds of results:

- **The last-10 columns are results on the last 10 draws:** best-ticket sum, chance, most in one ticket, and 3+ tickets. For all four games those are the draws from 26 Sep to 17 Oct 2026, with 10 tickets per draw.
- **The z early / valid / late column is not.** It's how each lead did across the earlier history, which is what it was selected on. The three periods together run from 2019 (Star Toto), 2013 (Power Toto), 2014 (Supreme Toto) and 2020 (Magnum Life) up to 23 Sep 2026. Those draws are different from the last 10, so the last-10 columns are a clean test the leads never saw.

So, for example, Mars rashi × month (Magnum Life) had a best-ticket sum of 33 against 23.6 expected, and 57 tickets with 3+ matches against 23.7, all over the last 10 draws. Its +2.60 / +2.09 / +1.26 comes from 2020 to 23 Sep 2026.

---

**User:**

> Ok now repeat all the analysis again but for 20 tickets and create the same table for each lotto, I want to see if new leads appear or how the old leads perform

**Answer:**

I'll make the ticket count a setting and rerun the full search with 20 tickets per draw: same parameters, patterns, selection rule, last-10 test and shifted-calendar control.

- **Tickets 11–20** come from further one- and two-number swaps.
- **The 10-ticket run stays as it was,** with the same 10 swap patterns.
- **I'll also re-score the previous run's top 10 leads per game with 20 tickets,** so you can see how the old leads do alongside any new ones.

**Answer:**

The 20-ticket search is committed and running in the background: every astrological parameter and pair, 4 patterns, 20 tickets per draw, with 4 shifted calendars and the previous run's top leads re-scored. When it finishes I'll show you the same tables for each lotto, the new top 10 alongside how the old leads did with 20 tickets.

**Answer:**

With 20 tickets per draw, the old lead held up best: **Mars rashi × month (cold) on Magnum Life** came out #1 again. One new lead appeared, on Star Toto. Everything else stayed at chance on the last 10 draws.

As before, z early / valid / late is from the earlier history the leads were selected on; the remaining columns are the last 10 draws (26 Sep – 17 Oct), playing 20 tickets per draw. "Best sum" is each draw's best ticket's matches, added up over the 10 draws.

### Star Toto 6/50 (fair best-ticket sum: 12.3; 3+ tickets: 3.5)

| # | Lead | Pattern | z early / valid / late | Best sum | Chance | Most in one ticket | 3+ tickets |
|---|---|---|---|---|---|---|---|
| 1 | nakshatra lord × karana | hot | +2.59 / +1.50 / +1.84 | 13 | 46% | 2 | 0 |
| 2 | month pillar × 19:00 hour stem | position | +1.43 / +2.38 / +1.78 | 11 | 74% | 2 | 0 |
| 3 | Mercury retrograde × month | hot | +1.68 / +1.43 / +1.73 | 14 | 32% | 3 | **19** |
| 4 | Venus retrograde × lunar month | position | +1.37 / +1.77 / +1.67 | 13 | 46% | 2 | 0 |
| 5 | karana × KP Moon star lord | hot | +2.10 / +1.36 / +1.39 | 14 | 32% | 2 | 0 |
| 6 | Mercury combust × KP Sun star lord | hot | +1.43 / +1.70 / +1.34 | 16 | 12% | 3 | 4 |
| 7 | **Mercury rashi × lunar month** (new) | position | +1.31 / +1.77 / +1.51 | **19** | **1.4%** | 3 | 14 |
| 8 | day god × Moon–Mars aspect | cold | +1.31 / +1.90 / +1.67 | 11 | 74% | 2 | 0 |
| 9 | nakshatra lord × karana | position | +1.98 / +1.29 / +1.95 | 10 | 84% | 2 | 0 |
| 10 | Mercury retrograde × month | position | +1.55 / +1.90 / +1.28 | 11 | 74% | 3 | 18 |

**Old leads from the 10-ticket run:** 3 are still in the top 10 (nakshatra lord × karana hot #1 and position #9, karana × KP Moon star lord #5). On the last 10 draws they scored 10–16, at chance (12–84%). The best was KP Asc sub lord × KP Sun star lord, with one 4-number ticket.

### Power Toto 6/55 (fair best-ticket sum: 11.2; 3+ tickets: 2.7)

| # | Lead | Pattern | z early / valid / late | Best sum | Chance | Most in one ticket | 3+ tickets |
|---|---|---|---|---|---|---|---|
| 1 | Jupiter nakshatra × Saturn combust | cold | +3.05 / +1.72 / +1.68 | 10 | 74% | 2 | 0 |
| 2 | Mars nakshatra × Mercury–Saturn aspect | hot | +2.21 / +1.87 / +1.48 | 8 | 92% | 2 | 0 |
| 3 | day god × Sun–Mars aspect | cold | +1.51 / +1.47 / +1.60 | 10 | 74% | 3 | 2 |
| 4 | Venus nakshatra × Mercury–Venus aspect | hot | +1.47 / +1.62 / +2.24 | 12 | 45% | 2 | 0 |
| 5 | Mars nakshatra × draw in daylight | hot | +1.34 / +1.77 / +1.80 | 14 | 20% | 3 | 8 |
| 6 | Mars nakshatra × Venus–Jupiter aspect | hot | +1.34 / +1.47 / +1.36 | 13 | 31% | **4** | 9 |
| 7 | day god × Venus–Jupiter aspect | cold | +1.56 / +1.57 / +1.32 | 13 | 31% | 2 | 0 |
| 8 | day vs year branch × month Nine Star | hot | +1.29 / +1.67 / +1.36 | 9 | 85% | 2 | 0 |
| 9 | Moon–Mercury aspect × universal day | hot | +1.29 / +1.62 / +1.32 | 10 | 74% | 2 | 0 |
| 10 | Jupiter nakshatra × lunar leap month | cold | +2.04 / +1.28 / +1.44 | 10 | 74% | 2 | 0 |

**Old leads:** the Jupiter-nakshatra cold leads mostly stayed in the top 25, scoring 9–14 at chance. The previous best, Venus nakshatra × Na Yin element (position), fell to rank 25: 14, with 17 three-number tickets (20% chance).

### Supreme Toto 6/58 (fair best-ticket sum: 10.7; 3+ tickets: 2.3)

| # | Lead | Pattern | z early / valid / late | Best sum | Chance | Most in one ticket | 3+ tickets |
|---|---|---|---|---|---|---|---|
| 1 | Part of Fortune nakshatra × Plum Blossom trigrams | position | +2.17 / +2.05 / +2.08 | 7 | 95% | 2 | 0 |
| 2 | nakshatra pada × Mars–Saturn aspect | position | +2.04 / +2.36 / +1.96 | 10 | 67% | 2 | 0 |
| 3 | Moon–Venus aspect × Plum Blossom trigrams | position | +2.49 / +1.90 / +2.29 | 12 | 37% | 3 | 3 |
| 4 | Sun–Mars aspect × Plum Blossom trigrams | hot+recent | +2.49 / +1.60 / +2.04 | 11 | 52% | 2 | 0 |
| 5 | Moon–Venus aspect × Plum Blossom trigrams | hot | +2.58 / +1.55 / +1.84 | 12 | 37% | 2 | 0 |
| 6 | nakshatra × Part of Fortune rashi | hot+recent | +1.95 / +2.00 / +1.55 | 10 | 67% | 2 | 0 |
| 7 | Jupiter rashi × 19:00 hour stem | hot+recent | +2.44 / +1.85 / +1.55 | 9 | 79% | 2 | 0 |
| 8 | paksha × Jupiter rashi | position | +1.54 / +1.85 / +2.00 | 9 | 79% | 2 | 0 |
| 9 | KP Sun star lord × Mercury–Saturn aspect | position | +2.04 / +1.50 / +2.08 | 12 | 37% | 3 | 2 |
| 10 | KP Moon number × Mercury–Venus aspect | position | +1.45 / +1.55 / +1.59 | 5 | 99% | 2 | 0 |

**Old leads:** the Plum Blossom trigram leads stayed highly ranked, but on the last 10 draws every old lead scored 7–14, at or below chance. Together the top 10 scored 97 against 106.9 expected, below all four shifted calendars (101–134).

### Magnum Life 8/36 (fair best-ticket sum: 25.8; 3+ tickets: 47.3)

| # | Lead | Pattern | z early / valid / late | Best sum | Chance | Most in one ticket | 3+ tickets |
|---|---|---|---|---|---|---|---|
| 1 | **Mars rashi × month** (old lead) | cold | +2.42 / +2.74 / +1.86 | **34** | **1.2%** | 5 | **103** |
| 2 | Venus nakshatra × KP Moon sub lord | hot | +2.17 / +1.72 / +1.81 | 24 | 75% | 5 | 42 |
| 3–5 | year animal / year stem / year pillar × month | cold | +1.61 / +1.72 / +1.62 | 27 | 41% | 4 | 50 |
| 6 | KP Asc sub lord × hard aspects | cold | +2.01 / +1.94 / +1.53 | 29 | 21% | 5 | 61 |
| 7 | Mars rashi × tropical Sun sign | cold | +1.66 / +1.77 / +1.48 | 27 | 41% | 4 | 56 |
| 8 | Rahu nakshatra × month | cold | +1.76 / +1.49 / +1.48 | 27 | 41% | 4 | 50 |
| 9–10 | year animal / year stem × day stem | cold | +2.11 / +1.94 / +1.39 | 20 | 97% | 4 | 19 |

Leads 3–5 and 9–10 are effectively the same lead: the year animal, stem and pillar all change together, so they produce identical tickets.

**Old leads:** Mars rashi × month rose from #6 to #1, and Venus nakshatra × KP Moon sub lord is #2. The rest scored 21–29, at chance.

### What changed with 20 tickets

- **Mars rashi × month (Magnum Life, cold) is the only lead that came out strong in both runs.** With 10 tickets it scored 33 vs 23.6 (0.6% chance), and with 20 it scored 34 vs 25.8 (1.2%), with 103 three-plus tickets against 47 expected. A closely related lead, Mars rashi × tropical Sun sign (cold), is #7.
- **The 20-ticket run isn't independent evidence, though.** Both runs scored the same 10 draws, and the 20 tickets include the 10 from before. It's still the best of about 40 leads tested on these draws, and its tickets are near-copies of each other, so one good draw lifts many at once.
- **The new Star Toto lead, Mercury rashi × lunar month (position), scored 19 vs 12.3 (1.4%).** It's one of 40 leads tested here too.
- **Taken together, the top 10 still match the shifted calendars in every game:** Star 132 (shifted 84–127), Power 109 (98–115), Supreme 97 (101–134), Magnum Life 262 (255–266). Star Toto is slightly above the shifted range, Supreme slightly below; the others are inside it.

**What I'd track forward:**
- Mars rashi × month (cold) on Magnum Life;
- Mercury rashi × lunar month (position) on Star Toto.

Only new draws can show whether either is more than this period's luck. I can log both leads' 20 tickets for the next draws.

The full tables, with every ticket played, are in `analysis/LEAD_SEARCH20.md`, with a summary in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Ok now, for magnum life let’s say I want to play system play 9 for 2 tickets, redo the analysis for the magnum life existing leads and also for all other astrological parameter as usual pairs and single, hot, cold, mix etc

**Answer:**

For Magnum Life System 9: you pick 9 numbers, and the entry covers all 9 combinations of 8 from them. So what matters is how many of the 8 drawn numbers fall inside your 9. Two System 9 entries means two sets of 9 numbers per draw. I'll build them from each method's ranking in two ways:
- **Disjoint:** set A is the top 9 numbers, set B is ranks 10–18. That gives 18 different numbers, two separate chances.
- **Overlapping:** set A is the top 9, set B is the top 6 plus ranks 10–12. That puts more weight on the strongest numbers.

The outcome measure is the best of the two sets each draw (0–8 numbers matched). I'll also count sets that catch 5+ and 6+ of the 8.

The search is the same as before: all 114 parameters, singles and pairs, with hot, cold, position and hot+recent patterns. Leads are chosen without the last 10 draws, then tested on them, with shifted calendars as the chance control. I'll also re-score the existing Magnum Life leads, and the hot/cold/mix/analogy/LLM methods, as System 9 × 2.

**Answer:**

The report headings still say "10 tickets" and "3+". I'll make them adapt to system play.

**Answer:**

For Magnum Life System 9 with 2 entries per draw, no new lead emerged. Mars rashi × month is still the most consistent of the earlier leads, and Moon rashi × Mars combust produced one set that caught 6 of the 8 drawn numbers.

A System 9 entry covers every 8-number combination of your 9 numbers. So what matters each draw is how many of the 8 drawn numbers land inside the better of your two 9-number sets. I tried two layouts:
- **Disjoint:** the top 9 numbers, plus ranks 10–18 (18 different numbers).
- **Overlap:** the top 9, plus the top 6 with ranks 10–12.

By chance, the better set catches about 2.7 numbers per draw (disjoint) or 2.4 (overlap). A set catching **5 or more** happens about once every 37 draws.

**1. New search over all 114 parameters, singles and pairs** (hot, cold, position, hot+recent), chosen without the last 10 draws:

| Layout | Top 10 leads on the last 10 draws (better set, summed) | Expected | Shifted calendars |
|---|---|---|---|
| Disjoint | 264 | 270.3 | 257–267 |
| Overlap | 224 | 238.7 | 231–248 |

Both layouts come out at or below chance. The best of the new disjoint top 10 was month pillar × hard aspects (cold): 31 vs 27.0 (11% chance), with one set catching 5. Everything else was 70–90% chance.

**2. Earlier Magnum Life leads, as System 9 × 2:**

| Lead | Pattern | Disjoint: sum (expected 27.0) | Chance | Overlap: sum (expected 23.9) | Chance | Most caught in one set |
|---|---|---|---|---|---|---|
| **Mars rashi × month** | cold | 29 | 30% | **31** | **2.5%** | 4 |
| Mars rashi × tropical Sun sign | cold | **35** | **0.6%** | 27 | 22% | 4 |
| **Moon rashi × Mars combust** | position | 30 | 19% | 29 | 8.5% | **6** (overlap) |
| Mars rashi × Venus combust | cold | 31 | 11% | 29 | 8.5% | 5 (3 sets with 5+) |
| Venus nakshatra × KP Moon sub lord | hot | 25 | 81% | 21 | 84% | 4 |
| Mercury nakshatra × Venus rashi (4D lead) | hot | 27 | 57% | 24 | 54% | 4 |

**3. Other methods as System 9 × 2:**

| Method | Disjoint (expected 27.0) | Overlap (expected 23.9) | Most caught in one set |
|---|---|---|---|
| Analogy "direct" | 31 (11%) | 29 (8%) | 5 |
| Analogy "map" | 29 (30%) | 27 (21%) | **6** (overlap) |
| Hot/cold + astrology | 31 (11%) | 28 (14%) | 4 |
| Embedding (word vectors) | — | 28 (14%) | 5 |
| Hot numbers (last 150) | 28 (42%) | — | 4 |

**How to read this:**
- **Mars rashi × month (cold) is the only lead with good results in every format:** 6 tickets, 10 tickets, 20 tickets, and System 9 overlap (31 vs 23.9). It's still the same 10 draws each time, so this is one lucky stretch measured several ways, not independent confirmations.
- **Mars rashi × tropical Sun sign's 35 (0.6%) only looks good with hindsight.** It ranks 16,410th on the earlier history, so no honest selection would have picked it.
- **The 6-of-8 sets (Moon rashi × Mars combust, analogy "map") are within luck.** One method out of roughly 30 catching 6 in one of its 20 sets is not unusual.
- **System play doesn't create an edge.** It puts more numbers in one entry, so it catches more, and chance rises by exactly the same amount.

**If you play System 9 × 2 on Magnum Life:** the honest pick is the **overlap layout of Mars rashi × month (cold)**, as the lead to track. Its tickets change only when Mars changes sign (about every 6 weeks) or the month changes. I can log its two 9-number sets for the next draws so we can see whether it keeps beating 23.9 per 10 draws.

The tables are in `analysis/LEAD_SEARCHSYS9_DISJOINT.md`, `analysis/LEAD_SEARCHSYS9_OVERLAP.md` and `analysis/SYSTEM9_METHODS.md`, with a summary in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> So tell me the performance of disjoint, overlap for Mars rashi x month and mars rashi x tropical sun sign for the last 10 draws and how many they caught for each of the 10 draws for 2 of their tickets

**Answer:**

Here's how the two leads did on Magnum Life's last 10 draws (26 Sep – 17 Oct), playing two System 9 sets per draw. Each number is how many of the 8 drawn numbers that set caught. A single 9-number set catches 2.0 on average by chance, and the better of two catches about 2.7 (disjoint) or 2.4 (overlap).

**Summary**

| Lead | Layout | Better set, summed over 10 draws | Expected | Chance | Most caught in one set |
|---|---|---|---|---|---|
| Mars rashi × month (cold) | Disjoint | 29 | 27.0 | 30% | 4 |
| Mars rashi × month (cold) | Overlap | **31** | 23.9 | **2.5%** | 4 |
| Mars rashi × tropical Sun sign (cold) | Disjoint | **35** | 27.0 | **0.6%** | 4 |
| Mars rashi × tropical Sun sign (cold) | Overlap | 27 | 23.9 | 21% | 4 |

**Per draw: numbers caught by set A / set B (better set in bold)**

| Draw | Drawn numbers | Mars × month, disjoint | Mars × month, overlap | Mars × Sun sign, disjoint | Mars × Sun sign, overlap |
|---|---|---|---|---|---|
| 26 Sep | 01 05 07 10 14 18 22 35 | **2** / 0 | **2** / **2** | **3** / **3** | **3** / **3** |
| 27 Sep | 02 10 14 15 20 21 31 33 | **3** / 1 | **3** / **3** | **3** / 1 | **3** / 2 |
| 30 Sep | 10 11 20 24 32 33 34 36 | **3** / 1 | **3** / 1 | 1 / **4** | 1 / **2** |
| 3 Oct | 03 07 08 10 11 12 19 21 | **3** / 2 | **3** / **3** | 1 / **4** | **1** / **1** |
| 4 Oct | 01 02 15 17 21 28 30 31 | 3 / **4** | **3** / **3** | 2 / **4** | **2** / 1 |
| 7 Oct | 06 12 15 19 21 23 24 35 | **2** / **2** | **2** / 1 | **3** / 0 | **3** / 2 |
| 10 Oct | 22 23 25 28 30 31 32 36 | **3** / 2 | 3 / **4** | **3** / **3** | **3** / 2 |
| 11 Oct | 02 07 14 15 16 22 25 27 | **3** / 1 | **3** / **3** | 0 / **4** | 0 / **3** |
| 14 Oct | 06 09 13 14 16 24 26 35 | **2** / **2** | 2 / **4** | **4** / 2 | **4** / **4** |
| 17 Oct | 05 08 11 13 14 20 25 27 | **4** / 1 | **4** / 3 | **3** / **3** | **3** / 1 |
| **Better set, total** | | **29** | **31** | **35** | **27** |

**What it shows:**
- **No set caught more than 4 of the 8 numbers on any draw.** Both leads did well by being steady (3–4 almost every draw), not by hitting big.
- **Mars rashi × month is steady in both layouts.** Set A caught 2–4 every draw, so the overlap layout (which leans on the same strong numbers) did best.
- **Mars rashi × tropical Sun sign only did well in the disjoint layout,** and mostly through set B (ranks 10–18), which caught 4 on five different draws. Its top 9 (set A) often caught only 0–1. That suggests luck rather than a good ranking: if the ranking meant something, the top 9 would do better than the next 9, not worse.
- **These are both cold-number leads, so their sets change slowly.** Many numbers (13, 29, 17, 23, 04, 09) stay in every set, because Mars and the month changed little over these weeks.

The full tickets for these and the other leads are in `analysis/LEAD_SEARCHSYS9_DISJOINT.md` and `analysis/LEAD_SEARCHSYS9_OVERLAP.md`, both committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Now redo just like what you did for system 9 for 2 tickets with system 10 for 1 ticket for the last 10 draws  for all the parameters, single pair, cold hot etc

**Answer:**

For System 10 you pick 10 numbers per entry, which covers every 8-number combination of them (45 combinations). So the outcome per draw is how many of the 8 drawn numbers fall inside your 10.

The run is the same as for System 9 × 2:
- Magnum Life only, with one 10-number set per draw: the top 10 numbers of each method's ranking;
- every parameter, alone and in pairs, with the hot, cold, position and hot+recent patterns;
- leads chosen without the last 10 draws, then tested on them, with shifted calendars as the chance control;
- the earlier leads and the other methods (analogy, embedding, hot/cold) re-scored too.

First I'll update both scripts for a single set.

**Answer:**

Mars rashi × month came out #2 in the fresh System 10 search, chosen without seeing the last 10 draws, and it scored 30 against 22.3. I'll pull its draw-by-draw results.

**Answer:**

With one System 10 set per draw on Magnum Life, **Mars rashi × month (cold)** was the best lead again: it caught 30 numbers over the last 10 draws against 22.3 expected. No new lead emerged.

A 10-number set catches about 2.2 of the 8 drawn numbers per draw by chance. I searched every parameter alone and in pairs, with the hot, cold, position and hot+recent patterns. Leads were chosen without seeing the last 10 draws (26 Sep – 17 Oct), then tested on them.

**New search, top 10** (z = how consistently it beat chance in the earlier history; the rest is the last 10 draws):

| # | Lead | Pattern | z early / valid / late | Caught over 10 draws (expected 22.3) | Chance | Most in one draw |
|---|---|---|---|---|---|---|
| 1 | Mercury rashi × Part of Fortune nakshatra | cold | +1.89 / +1.69 / +1.85 | 22 | 58% | 4 |
| 2 | **Mars rashi × month** | cold | +2.32 / +2.18 / +1.45 | **30** | **2.3%** | 4 |
| 3 | paksha × Jupiter retrograde | cold | +2.81 / +1.42 / +1.45 | 22 | 58% | 3 |
| 4 | planets with Moon × KP Asc number | cold | +1.45 / +1.58 / +1.36 | 22 | 58% | 4 |
| 5 | Venus nakshatra × Jupiter nakshatra | cold | +1.36 / +1.80 / +1.63 | 23 | 47% | 4 |
| 6 | Rahu rashi × month Nine Star | cold | +1.55 / +1.31 / +2.11 | 25 | 26% | 3 |
| 7 | tithi × Venus–Mars aspect | position | +1.31 / +1.37 / +1.76 | 19 | 85% | 3 |
| 8 | month pillar × day element | cold | +1.74 / +2.29 / +1.27 | 22 | 58% | 4 |
| 9 | nakshatra pada × day stem | hot | +1.26 / +1.37 / +1.58 | 18 | 91% | 3 |
| 10 | karana × day pillar | hot | +1.36 / +1.26 / +1.54 | 24 | 36% | 4 |

All 10 together caught 227 against 222.7 expected; the shifted calendars' top 10 caught 210–235. So the list as a whole is at chance.

**Mars rashi × month, draw by draw:**

| Draw | Its 10 numbers | Drawn | Caught |
|---|---|---|---|
| 26 Sep | 04 07 13 15 18 21 23 24 31 32 | 01 05 07 10 14 18 22 35 | 2 (07 18) |
| 27 Sep | 13 15 20 21 23 24 29 31 32 34 | 02 10 14 15 20 21 31 33 | **4** (15 20 21 31) |
| 30 Sep | 04 06 08 13 23 24 29 31 32 34 | 10 11 20 24 32 33 34 36 | 3 (24 32 34) |
| 3 Oct | 07 10 12 13 15 17 23 27 29 31 | 03 07 08 10 11 12 19 21 | 3 (07 10 12) |
| 4 Oct | 06 13 15 17 20 23 27 29 31 36 | 01 02 15 17 21 28 30 31 | 3 (15 17 31) |
| 7 Oct | 08 09 12 13 17 20 23 27 29 31 | 06 12 15 19 21 23 24 35 | 2 (12 23) |
| 10 Oct | 08 09 10 13 14 23 27 29 31 32 | 22 23 25 28 30 31 32 36 | 3 (23 31 32) |
| 11 Oct | 07 08 09 10 13 14 17 20 27 29 | 02 07 14 15 16 22 25 27 | 3 (07 14 27) |
| 14 Oct | 06 08 09 10 13 17 20 27 29 31 | 06 09 13 14 16 24 26 35 | 3 (06 09 13) |
| 17 Oct | 08 10 12 13 17 20 27 29 33 36 | 05 08 11 13 14 20 25 27 | **4** (08 13 20 27) |
| **Total** | | | **30** |

**Earlier leads, re-scored as System 10:**

| Lead | Pattern | Caught (expected 22.3) | Chance | Most in one draw |
|---|---|---|---|---|
| Mars rashi × Venus combust | cold | 28 | 7.4% | 5 |
| Moon rashi × Mars combust | position | 28 | 7.4% | 5 |
| Mars rashi × tropical Sun sign | cold | 26 | 18% | 4 |
| Venus nakshatra × KP Moon sub lord | hot | 19 | 85% | 4 |
| Mercury nakshatra × Venus rashi (4D lead) | hot | 23 | 47% | 4 |

**Other methods as System 10:** the analogy "direct" model caught 28 (6.9%) and analogy "map" 28 (7.4%), including one draw where it caught 6 of 8. Embedding, hot/cold+astrology and the rest caught 24–26, at chance.

**How to read it:**
- **Mars rashi × month is steady, not spectacular.** It caught 2–4 on every draw, never fewer than 2, but never more than 4. A System 10 prize needs at least 5 of the 8, so on these 10 draws it would not have won anything big.
- **It's the one lead that has come out on top across every format:** 6, 10 and 20 tickets, System 9 × 2, and now System 10. This time it was picked without seeing these draws. But every format scored the same 10 draws, so it's still one good stretch, not five separate confirmations.
- **Its set barely changes.** Numbers like 13, 29, 27, 31 and 17 sit in almost every set, because Mars stayed in the same sign over these weeks. That makes it close to a "cold numbers during this Mars period" ticket.

If you want to follow it, its next System 10 set for the coming draws would be built the same way. I can log it now, so the next draws give a true out-of-sample test.

The tables are in `analysis/LEAD_SEARCHSYS10.md` and `analysis/SYSTEM10_METHODS.md`, with a summary in `analysis/FINDINGS.md`. Everything is committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Just to check does the history has that 2 bonus that was picked other than 8 lots?

**Answer:**

Yes. The Magnum Life history has both bonus numbers for every draw: `data/magnum_life.csv` has `bonus1` and `bonus2` columns alongside the 8 main numbers, and none of the 1,346 draws is missing them. For example, 17 Oct 2026 is 05 08 11 13 14 20 25 27 with bonus 02 10.

**But all the analysis so far used only the 8 main numbers.** The bonus numbers were left out of every model, lead search and score, including the System 9 and System 10 results.

For a sense of how much they'd add, here's the Mars rashi × month System 10 set on the last 10 draws with the bonus numbers counted:

| Draw | Main caught (of 8) | Bonus caught (of 2) |
|---|---|---|
| 26 Sep | 2 | – |
| 27 Sep | 4 | – |
| 30 Sep | 3 | 08 |
| 3 Oct | 3 | – |
| 4 Oct | 3 | 27 |
| 7 Oct | 2 | – |
| 10 Oct | 3 | – |
| 11 Oct | 3 | – |
| 14 Oct | 3 | 31 |
| 17 Oct | 4 | 10 |

It caught 4 bonus numbers over the 10 draws, against about 5.6 expected by chance, so the bonus numbers don't strengthen this lead.

Magnum Life prizes do depend on the bonus numbers as well as the main ones. If you'd like, I can redo the System 9 / System 10 analysis scoring main and bonus together, the way the prize tiers count them; I'd need to confirm the current prize table first.

---

**User:**

> redo system 10 including the bonus numbers

---

**User:**

> [Request interrupted by user]

---

**User:**

> Redo system 9 and system 10 with bonus but you need to mention how many real+bonus caught since the prize structure is different

**Answer:**

I'll redo both formats, System 9 × 2 (disjoint and overlap) and System 10 × 1, counting both kinds of numbers. Here's how it changes:
- **Each set is scored on how many of the 10 drawn balls it catches** (8 main + 2 bonus). That total is used to rank and select leads, chosen without the last 10 draws as before.
- **Every result shows main and bonus separately** (e.g. "3+1" means 3 main and 1 bonus), because the prize tiers depend on the combination. Tables also show main-only totals.
- **The patterns still learn from the main numbers only;** the bonus counts only in scoring.
- **Same controls as before:** shifted calendars, earlier leads re-scored, and the other methods (analogy, embedding, hot/cold) included.

**Answer:**

Now the report: a draw-by-draw "main+bonus" column for each lead's better set, plus main-only and bonus totals.

**Answer:**

The chance figure checks out: a 10-number set catches 2.78 of the 10 drawn balls on average. Now the same bonus option for the analogy, embedding and hot/cold methods script.

**Answer:**

All three runs are done. I'll pull the per-draw main+bonus splits for the key leads: Mars rashi × month, Mars rashi × tropical Sun sign, and the best new ones.

**Answer:**

Counting the bonus balls doesn't change the picture: the new search finds nothing beyond chance in any format. I re-scored every set on all 10 balls drawn (8 main + 2 bonus) and split each result into **main + bonus**, e.g. **3+1** means 3 main and 1 bonus number in your set. Leads were again chosen without the last 10 draws (26 Sep – 17 Oct), and the patterns still learn only from main numbers.

**Expected by chance over 10 draws (better set, main+bonus combined):** System 9 × 2 disjoint 32.6, System 9 × 2 overlap 29.2, System 10 × 1 27.8. Of that, roughly 5.5 is bonus balls.

### 1. New search (all parameters, singles and pairs, every pattern)

| Format | Top 10 leads together | Expected | Shifted calendars |
|---|---|---|---|
| System 9 × 2 disjoint | 310 | 325.9 | 325–339 |
| System 9 × 2 overlap | 303 | 292.1 | 292–318 |
| System 10 × 1 | 280 | 278.1 | 260–299 |

All at chance. The best new leads:

| Format | Lead | Total (main / bonus) | Chance | Per draw, main+bonus |
|---|---|---|---|---|
| Sys 9 overlap | karana × year yin/yang (cold) | 34 (26 / 8) | 12% | 2+1 2+0 4+1 **5+0** 3+0 1+1 3+2 3+1 2+1 1+1 |
| Sys 9 disjoint | 28 mansions × Moon–Saturn aspect (cold) | 34 (28 / 6) | 38% | 2+2 2+1 2+1 3+0 2+0 3+1 4+0 2+1 3+0 **5+0** |
| Sys 10 | Mars nakshatra × Venus nakshatra (cold) | 31 (24 / 7) | 24% | 2+0 2+0 1+1 3+1 2+1 2+0 2+2 2+1 **5+0** 3+1 |

### 2. Existing leads, main+bonus per draw

**Mars rashi × month (cold)**

| Format | Total (main / bonus) | Expected | Chance | 26 Sep | 27 Sep | 30 Sep | 3 Oct | 4 Oct | 7 Oct | 10 Oct | 11 Oct | 14 Oct | 17 Oct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sys 9 disjoint | 32 (28 / 4) | 32.6 | 64% | 2+0 | 3+0 | 3+1 | 3+0 | 3+1 | 2+0 | 3+0 | 3+0 | 2+1 | 4+1 |
| Sys 9 overlap | 34 (31 / 3) | 29.2 | 12% | 2+0 | 3+0 | 3+1 | 3+0 | 3+1 | 2+0 | 4+0 | 3+0 | 4+0 | 4+1 |
| Sys 10 | 34 (30 / 4) | 27.8 | 7.1% | 2+0 | 4+0 | 3+1 | 3+0 | 3+1 | 2+0 | 3+0 | 3+0 | 3+1 | 4+1 |

**Mars rashi × Venus combust (cold)**

| Format | Total (main / bonus) | Expected | Chance | 26 Sep | 27 Sep | 30 Sep | 3 Oct | 4 Oct | 7 Oct | 10 Oct | 11 Oct | 14 Oct | 17 Oct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sys 9 disjoint | 36 (29 / 7) | 32.6 | 17% | 2+0 | 3+1 | 1+2 | 2+1 | 3+0 | **5+0** | 3+1 | 2+1 | **5+1** | 3+0 |
| Sys 9 overlap | 36 (28 / 8) | 29.2 | **4.0%** | 2+0 | 3+1 | 1+2 | 2+1 | 3+1 | **5+0** | 3+1 | 2+1 | **5+1** | 2+0 |
| Sys 10 | 35 (28 / 7) | 27.8 | **4.3%** | 2+0 | 4+1 | 1+2 | 2+1 | 3+0 | **5+0** | 3+1 | 2+1 | **5+1** | 1+0 |

**Mars rashi × tropical Sun sign (cold)**

| Format | Total (main / bonus) | Expected | Chance | 26 Sep | 27 Sep | 30 Sep | 3 Oct | 4 Oct | 7 Oct | 10 Oct | 11 Oct | 14 Oct | 17 Oct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sys 9 disjoint | **40 (35 / 5)** | 32.6 | **1.2%** | 3+1 | 3+1 | 4+1 | 4+0 | 4+1 | 3+0 | 3+1 | 4+0 | 4+0 | 3+0 |
| Sys 9 overlap | 33 (27 / 6) | 29.2 | 18% | 3+1 | 3+1 | 2+1 | 1+1 | 2+0 | 3+0 | 3+1 | 3+1 | 4+0 | 3+0 |
| Sys 10 | 32 (26 / 6) | 27.8 | 17% | 4+1 | 3+1 | 2+1 | 1+1 | 2+0 | 3+0 | 3+1 | 1+1 | 4+0 | 3+0 |

**Moon rashi × Mars combust (position)**

| Format | Total (main / bonus) | Expected | Chance | 26 Sep | 27 Sep | 30 Sep | 3 Oct | 4 Oct | 7 Oct | 10 Oct | 11 Oct | 14 Oct | 17 Oct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sys 9 overlap | 35 (28 / 7) | 29.2 | 7.0% | 3+0 | 1+1 | **6+0** | 1+1 | 3+1 | 4+0 | 2+1 | 4+0 | 2+1 | 2+2 |
| Sys 10 | 34 (28 / 6) | 27.8 | 7.1% | 3+0 | 1+1 | **5+1** | 1+0 | 3+1 | 4+0 | 2+1 | 4+0 | 2+1 | 3+1 |

### What changed with the bonus balls

- **Mars rashi × month drops back.** It's steady on main numbers (2–4 every draw), but it caught only 3–4 bonus balls over 10 draws against about 5.5 expected. With the bonus counted, the search ranks it 22nd (System 10), 291st (overlap) and 3,884th (disjoint), no longer a top pick.
- **Mars rashi × Venus combust is the best existing lead with the bonus included:** 36 (overlap) and 35 (System 10), about 4% chance. It got two big draws, **5+0 on 7 Oct and 5+1 on 14 Oct**, in every format. Remember it was originally found by looking at these same draws, so it's not a clean test.
- **Mars rashi × tropical Sun sign was the steadiest:** 3–4 main every draw in the disjoint layout (40 total, 1.2%). But it ranks 9,007th on the earlier history, so nobody would have picked it in advance.
- **The biggest single hit was Moon rashi × Mars combust's overlap set on 30 Sep: 6+0,** six main numbers in one 9-number set.

**Bottom line:** the bonus balls don't reveal any new lead. The three Mars leads all did reasonably on these 10 draws, but no method picks them consistently in advance. All of this rests on the same 10 draws, and fair draws give a 5+ set roughly once every 12–37 draws. I can log the System 10 sets for Mars rashi × Venus combust and Mars rashi × month for the next draws, with main+bonus tracked, so the coming results give a proper test.

Everything is in `analysis/LEAD_SEARCHSYS9_DISJOINT_BONUS.md`, `analysis/LEAD_SEARCHSYS9_OVERLAP_BONUS.md`, `analysis/LEAD_SEARCHSYS10_BONUS.md` and the `analysis/SYSTEM*_METHODS_BONUS.md` files, with a summary in `analysis/FINDINGS.md`. It's all committed and pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Ok now I’m just wondering, the hot and cold needs to be updated, so for all 10 days, update each day before and carry out a new prediction. Check and see if this made it to predict better?

**Answer:**

A clarification first, then the test. The hot and cold counts were already updated before each of the 10 draws. Each draw's tickets used every earlier draw, including the earlier ones among the 10. What stayed frozen was the choice of lead: which parameter, pair and pattern to play was decided once, before the 10 draws.

So the real question is whether **re-choosing the lead before every draw**, using everything up to the day before, predicts better. I'll test that like this:
- For each of the last 10 draws, rank all ~26,000 leads (every parameter, pair and pattern) on all draws up to the day before, with the same three-period consistency rule.
- Play the #1 lead's tickets on that draw, and separately the top 10 leads.
- Compare with the frozen choice, with chance, and with the same rolling procedure on shifted calendars.

I'll run it for the formats we've used:
- 10 tickets in all four games, main numbers only;
- Magnum Life System 9 × 2 (disjoint and overlap) and System 10 × 1, scored on main + bonus.

**Answer:**

I've started the test that re-chooses the lead before each draw. It's running in the background on all four formats: 10 tickets for each game, then Magnum Life System 9 × 2 (overlap and disjoint) and System 10 × 1, both with the bonus balls.

Before each of the last 10 draws it ranks all ~26,000 leads again, using only the draws up to the day before. It then plays the top lead and the top 10 on that draw. Each result is compared with the choice made once before the 10 draws, with chance, and with the same procedure on shifted calendars. I'll report the numbers as each format finishes.

**Answer:**

I've committed and pushed the new script, `analysis/rolling_select.py`, to `claude/focused-franklin-ajsdm9`.

The test itself is still running in the background, so there are no results yet. When each format finishes, I'll commit and push its output, add a paragraph to FINDINGS.md, and tell you whether re-choosing the lead before each draw caught more than the one-time choice, chance, and the shifted calendars.

**Answer:**

STAR TOTO 6/50 has finished; the other three games and formats are still running.

| Choice | Caught over the 10 draws | Shifted calendars |
|---|---|---|
| Re-chosen before each draw, top lead | 13 | 11, 11 |
| Re-chosen before each draw, top 10 (average) | 11.7 | not in this summary line |
| Chosen once before the 10 draws, top lead | 13 | not in this summary line |
| Chosen once, top 10 (average) | 11.5 | not in this summary line |
| Expected by chance | 10.63 | |

- **Same lead every time:** re-ranking before each draw picked the same top lead all 10 times. It is the same lead as the one-time choice, so both caught 13.
- **No real improvement:** the top 10 moved from 11.5 to 11.7, which is noise. 13 against an expected 10.63 is also within normal variation for 10 draws.
- **Little to change:** one extra draw barely shifts a ranking built on about 1,400 earlier draws. The hot and cold counts inside each lead were already updated before every draw.

I'll report Power Toto, Supreme Toto and Magnum Life as they finish.

**Answer:**

Power Toto 6/55 has finished. Supreme Toto and Magnum Life are still running.

| Choice | Caught over the 10 draws | Shifted calendars |
|---|---|---|
| Re-chosen before each draw, top lead | 9 | 13, 12 |
| Re-chosen before each draw, top 10 (average) | 9.9 | not in this summary line |
| Chosen once before the 10 draws, top lead | 9 | not in this summary line |
| Chosen once, top 10 (average) | 9.3 | not in this summary line |
| Expected by chance | 9.67 | |

- **Same lead every time:** re-ranking before each draw kept the same top lead all 10 times, the same one chosen once, so both caught 9.
- **No improvement:** that is just under chance.
- **Shifted calendars did better:** the same procedure on both shifted calendars caught 13 and 12, more than the real calendar.

**Answer:**

Supreme Toto 6/58 has finished. Magnum Life is still running.

| Choice | Caught over the 10 draws | Shifted calendars |
|---|---|---|
| Re-chosen before each draw, top lead | 9 | 9, 10 |
| Re-chosen before each draw, top 10 (average) | 7.5 | not in this summary line |
| Chosen once before the 10 draws, top lead | 9 | not in this summary line |
| Chosen once, top 10 (average) | 8.3 | not in this summary line |
| Expected by chance | 9.19 | |

- **Lead changed, result didn't:** re-ranking before each draw switched between 3 different top leads over the 10 draws, yet it still caught 9. That is the same as the one-time choice and just under chance.
- **Top 10 did worse:** re-ranked before each draw, the top 10 averaged 7.5, against 8.3 when chosen once.
- **Shifted calendars:** they caught 9 and 10, the same as the real calendar or better.

**Answer:**

Magnum Life 8/36 (10 tickets, main numbers) has finished, which completes the 10-ticket test for all four games. The System 9 and System 10 bonus runs are still going.

| Choice | Caught over the 10 draws | Shifted calendars |
|---|---|---|
| Re-chosen before each draw, top lead | 17 | 20, 28 |
| Re-chosen before each draw, top 10 (average) | 24.0 | not in this summary line |
| Chosen once before the 10 draws, top lead | 21 | not in this summary line |
| Chosen once, top 10 (average) | 24.9 | not in this summary line |
| Expected by chance | 23.65 | |

- **Re-choosing did worse here:** the top lead caught 17, against 21 when chosen once and 23.65 expected by chance. It switched between 2 different leads over the 10 draws.
- **Top 10 changed nothing:** it averaged 24.0 against 24.9, both about chance.
- **Shifted calendars did better:** they caught 20 and 28.

Across the four games, re-choosing the lead before each draw did not predict better:

| Game | Top lead, re-chosen | Top lead, chosen once | Expected by chance |
|---|---|---|---|
| STAR TOTO 6/50 | 13 | 13 | 10.63 |
| POWER TOTO 6/55 | 9 | 9 | 9.67 |
| SUPREME TOTO 6/58 | 9 | 9 | 9.19 |
| Magnum Life 8/36 | 17 | 21 | 23.65 |

- **Toto games:** the top lead mostly stayed the same, so the result was identical.
- **Magnum Life:** re-choosing was worse.
- **Overall:** everything sits within chance, and the shifted calendars did as well as or better than the real one.

**Answer:**

I've committed and pushed the 10-ticket results to `claude/focused-franklin-ajsdm9`, as `analysis/ROLLING_10.md` and `analysis/rolling_10_results.json`.

Magnum Life System 9 × 2 (overlap and disjoint) and System 10 × 1 with the bonus balls are still running. When they finish I'll commit those too and add a paragraph to FINDINGS.md.

**Answer:**

Magnum Life System 9 × 2 (overlap sets, main + bonus balls) has finished. The disjoint and System 10 runs are still going.

| Choice | Caught over the 10 draws | Shifted calendars |
|---|---|---|
| Re-chosen before each draw, top lead | 27 | 34, 29 |
| Re-chosen before each draw, top 10 (average) | 29.9 | not in this summary line |
| Chosen once before the 10 draws, top lead | 29 | not in this summary line |
| Chosen once, top 10 (average) | 30.3 | not in this summary line |
| Expected by chance | 29.21 | |

- **Re-choosing did worse:** the top lead caught 27, against 29 when chosen once and 29.21 expected by chance. It switched between 3 different leads over the 10 draws.
- **Top 10 changed nothing:** it averaged 29.9 against 30.3, both about chance.
- **Shifted calendars did as well or better:** they caught 34 and 29.

**Answer:**

I've committed and pushed the Magnum Life System 9 × 2 overlap results with bonus balls to `claude/focused-franklin-ajsdm9`, as `analysis/ROLLING_SYS9_OVERLAP_BONUS.md` and `analysis/rolling_sys9_overlap_bonus_results.json`.

The System 9 disjoint and System 10 × 1 runs are still going. When they finish I'll commit those too and add a paragraph to FINDINGS.md.

**Answer:**

Magnum Life System 9 × 2 (disjoint sets, main + bonus balls) has finished. Only System 10 × 1 is still running.

| Choice | Caught over the 10 draws | Shifted calendars |
|---|---|---|
| Re-chosen before each draw, top lead | 33 | 30, 35 |
| Re-chosen before each draw, top 10 (average) | 31.6 | not in this summary line |
| Chosen once before the 10 draws, top lead | 33 | not in this summary line |
| Chosen once, top 10 (average) | 31.6 | not in this summary line |
| Expected by chance | 32.59 | |

- **No change:** re-choosing switched between 4 different leads, yet it caught exactly the same as the one-time choice: 33 for the top lead and 31.6 for the top 10.
- **About chance:** both are within normal variation of the expected 32.59.
- **Shifted calendars:** they caught 30 and 35, so the real calendar sits between them.

**Answer:**

I've committed and pushed the Magnum Life System 9 × 2 disjoint results with bonus balls to `claude/focused-franklin-ajsdm9`, as `analysis/ROLLING_SYS9_DISJOINT_BONUS.md` and `analysis/rolling_sys9_disjoint_bonus_results.json`.

Only the System 10 × 1 run is still going. When it finishes I'll commit it and add a paragraph to FINDINGS.md.

**Answer:**

No, choosing the lead again before each draw did not predict better. Before each of the last 10 draws I re-ranked all ~26,000 leads using only the draws up to the day before. I then played the top lead and the top 10 on that draw. Across all seven formats, the results were the same as choosing once before the 10 draws, or worse, and all were at chance.

Numbers are balls caught over the 10 draws, counting the 8 main plus 2 bonus balls for the System formats.

| Format | Re-chosen each draw, top lead | Re-chosen each draw, top 10 (average) | Chosen once, top lead | Chosen once, top 10 (average) | Expected by chance | Shifted calendars |
|---|---|---|---|---|---|---|
| STAR TOTO 6/50, 10 tickets | 13 | 11.7 | 13 | 11.5 | 10.6 | 11, 11 |
| POWER TOTO 6/55, 10 tickets | 9 | 9.9 | 9 | 9.3 | 9.7 | 13, 12 |
| SUPREME TOTO 6/58, 10 tickets | 9 | 7.5 | 9 | 8.3 | 9.2 | 9, 10 |
| Magnum Life, 10 tickets | 17 | 24.0 | 21 | 24.9 | 23.7 | 20, 28 |
| Magnum Life System 9 × 2 overlap | 27 | 29.9 | 29 | 30.3 | 29.2 | 34, 29 |
| Magnum Life System 9 × 2 disjoint | 33 | 31.6 | 33 | 31.6 | 32.6 | 30, 35 |
| Magnum Life System 10 × 1 | 29 | 28.0 | 29 | 28.5 | 27.8 | 29, 29 |

- **The top lead barely changes:** one more draw hardly moves a ranking built on 1,300–2,800 earlier draws. Over the 10 draws the top lead used only 1 to 4 different leads; on STAR TOTO and POWER TOTO it was the same lead all 10 times. The hot and cold counts inside each lead were already updated before every draw.
- **Changing it doesn't help:** where the lead did change (Magnum Life, SUPREME TOTO), the result was equal or worse.
- **Shifted calendars do as well:** the same procedure on shifted calendars caught about the same, and sometimes more.
- **Leads not comparable with earlier tables:** this test ranks leads on total balls caught. The earlier tables ranked them on draws with 3+ (or 5+), so the "chosen once" lead here is not always Mars rashi × month.

For System 10 × 1 the top lead caught 29 balls: 24 main and 5 bonus. Main versus bonus counts for every draw, in all three System formats, are in the MD files.

Everything is pushed to `claude/focused-franklin-ajsdm9`, with a summary paragraph added to FINDINGS.md. Files are in `analysis/`:
- `ROLLING_10.md`
- `ROLLING_SYS9_OVERLAP_BONUS.md`
- `ROLLING_SYS9_DISJOINT_BONUS.md`
- `ROLLING_SYS10_BONUS.md`

---

**User:**

> So for magnum life what is the best lead?

**Answer:**

The best Magnum Life lead is **Mars rashi × month, cold pattern**: it is the only one that looked good on the history before the last 10 draws and then also did well on those 10 draws. That said, I don't think it's a real edge, for the reasons further down.

Mars rashi × month, cold, on the last 10 draws:

| Format | Rank on the earlier draws (of ~26,000 leads) | Caught over the last 10 draws | Expected by chance | Chance of doing this well |
|---|---|---|---|---|
| 10 tickets | 6 | 33 | 23.7 | 0.6% |
| 20 tickets | **1** | 34 | 25.8 | 1.2% |
| System 9 × 2 overlap, with bonus | 291 | 34 (31 main + 3 bonus) | 29.2 | 11.6% |
| System 9 × 2 disjoint, with bonus | 3,884 | 32 (28 main + 4 bonus) | 32.6 | 63.7% |
| System 10 × 1, with bonus | 22 | 34 (30 main + 4 bonus) | 27.8 | 7.1% |

- **Its strength is main numbers:** it caught 3 or 4 main numbers in most draws. It catches the bonus balls poorly, 3–4 against about 5.5 expected.
- **Best format for it:** System 10 × 1 or the overlap System 9 × 2. With the disjoint sets it was only average.
- **Its numbers drift slowly:** Mars stays in one rashi for about 1.5 months, so the lead is effectively "numbers that have been cold in this Mars-sign and month combination".

Two other leads score higher on the last 10 draws, but only in hindsight:

| Lead | Best result on the last 10 draws | Rank on the earlier draws |
|---|---|---|
| Mars rashi × Venus combust (cold) | 36 caught; 5+1 on 14 Oct, 5+0 on 7 Oct | 707–9,809 |
| Mars rashi × tropical Sun sign (cold) | 40 with System 9 × 2 disjoint | 9,007 |

Neither looked good beforehand, so picking them now just means choosing whatever happened to win.

Why I don't think Mars rashi × month is a genuine edge:
- **Only one test:** its good result comes from the same last 10 draws in every format, not 10 separate confirmations.
- **No better than shifted calendars:** the top 10 leads as a group were at chance (247 vs 236.5 expected at 10 tickets). Shifted calendars, where the dates no longer line up with the real sky, produce leads that look just as strong.
- **It didn't win the per-draw re-ranking:** when I re-chose the lead before each draw, Mars rashi × month was never picked first.

If you want to play one lead, Mars rashi × month (cold) as System 10 × 1 is the best-supported choice from all this work. Treat it as a fun pick, not an advantage over chance. I can generate its 10 numbers for the next Magnum Life draw and log them, so we can check them against the result.

---

**User:**

> Ok Google the prize structure of magnum life and re rank the leads based on how much profit that can be gained if the exact rules were followed for 10 days, but make sure the hot and cold is updated

**Answer:**

The official Magnum site is blocked from this container, so I'm fetching the prize tables another way.

**Answer:**

Got the official prize tables (via a fetch service, since the site is blocked here). Now checking how the lead-search code builds tickets so I can attach the real prize rules to it.

**Answer:**

Cleaning up two awkward lines before running.

**Answer:**

The profit ranking is running for all four formats (10 ordinary tickets, System 10 × 1, System 9 × 2 overlap and disjoint). I'll report when it finishes.

**Answer:**

I've committed and pushed the profit-ranking script, `analysis/profit_rank.py`, to `claude/focused-franklin-ajsdm9`.

It is still running on all four formats, so there are no profit numbers yet:
- 10 ordinary tickets
- System 10 × 1
- System 9 × 2, overlap sets
- System 9 × 2, disjoint sets

When it finishes I'll commit the results and report:
- the leads that made the most money over the last 10 draws, which is hindsight;
- how the leads that made the most on the earlier draws did on those 10 draws;
- what re-ranking by profit before each draw would have made;
- how that compares with shifted calendars and with random tickets.

**Answer:**

One lead shows a Grand prize hit (all 8 numbers) on 26 Sep. That's rare enough (about 1 in 30 million per ticket) that I'm checking it independently for look-ahead before trusting it.

**Answer:**

The Grand hit is genuine under the method's rules. Using only the 67 earlier draws with the same Paksha and Venus-rashi combination, the cold ranking put 7 of the 8 winning numbers in its top 8 and the last one at rank 10. One of the 10 tickets, [1, 5, 7, 10, 14, 18, 22, 35], was exactly the 26 Sep draw.

The lead was nothing special beforehand, though: it ranked 12,375th on profit over the earlier draws. Waiting on the System 9 and System 10 formats now.

**Answer:**

I've committed and pushed the 10-ticket profit results to `claude/focused-franklin-ajsdm9` (`analysis/PROFIT_10_BONUS.md` and `analysis/profit_10_bonus_results.json`).

The System 10 × 1 and both System 9 × 2 runs are still going. Once they finish I'll commit them and report the profit ranking across all four formats.

**Answer:**

No lead would have made money if you had picked it before the 10 days and played it by the official rules. One lead did hit the Grand prize on 26 Sep, but it was nowhere near the top of the ranking beforehand. Hot and cold counts were updated before every draw throughout.

**Prize rules used** (from Magnum's official Magnum Life page and the System Play 9 / 10 prize sheets):

| Match in an 8-number combination | Prize |
|---|---|
| 8 | Grand: RM1,000 a day for 20 years (counted as RM7.3m) |
| 7 + bonus | RM100,000 (RM1,000 a day for 100 days) |
| 7 | RM6,000 |
| 6 + bonus | RM600 |
| 6 | RM100 |
| 5 + bonus | RM30 |
| 5 | RM10 |
| 4 + bonus | RM5 |

- **Both bonus numbers:** a combination holding both pays its "+ bonus" prize twice. This comes from the System sheets; for example, System 10 with 8 winning + 2 bonus pays 1 Grand, 16 × 2nd and 56 × 4th.
- **System entries:** System 9 is 9 combinations (RM9) and System 10 is 45 combinations (RM45). Each combination is paid by the table above.
- **Expected return:** random tickets return about 55% of the stake, and most of that is the Grand prize.

**Profit over the last 10 draws (RM), across all 26,224 leads:**

| Format (stake) | Random tickets, expected | Best lead in hindsight | Shifted calendars, best | Best lead chosen beforehand | Top 10 chosen beforehand (average) | Re-ranked before every draw |
|---|---|---|---|---|---|---|
| 10 tickets (RM100) | −45 | **+7,330,300** | +24,500 / +8,170 | −100 | −94 | −100 |
| System 10 × 1 (RM450) | −202 | **+7,398,350** | +20,010 / +121,430 | −450 | −339 | −450 |
| System 9 × 2 overlap (RM180) | −81 | +110,060 | +12,900 / +110,400 | −180 | −156 | −180 |
| System 9 × 2 disjoint (RM180) | −81 | +110,020 | +110,060 / +110,060 | −160 | −87 | −160 |

**The jackpot lead: Paksha × Venus rashi, cold.**
- **What it did:** on 26 Sep 2026 one of its 10 tickets, [1, 5, 7, 10, 14, 18, 22, 35], matched all 8 numbers. Its System 10 set held all 8 winning numbers as well.
- **No look-ahead:** I checked it independently. It used only the 67 earlier draws with the same Paksha and Venus rashi. Seven of the winning numbers were in its cold top 8 and the eighth was at rank 10.
- **It wasn't a lead beforehand:** on the earlier draws it ranked 12,375th (10 tickets) and 8,135th (System 10), and it was losing money (−RM8,140 with 10 tickets).
- **Luck is the likely explanation:** with 26,224 leads, each playing 10 tickets for 10 draws, a jackpot somewhere among them is not surprising.

**Ranking by earlier profit doesn't work either:**
- **The leaders are past jackpot winners:** every top lead by earlier profit (Ritu × year yin-yang, Mars combust × Ritu, Hora lord × Saturn nakshatra and so on) is there because it hit the Grand prize once before.
- **Shifted calendars produce them too:** the best earlier profit was RM7.3–8.1m on every calendar.
- **They lost on the 10 draws:** those leaders won almost nothing and lost close to the full stake.
- **Re-ranking keeps the same lead:** the past jackpot outweighs everything else, so re-ranking before every draw keeps the same lead and also lost the full stake.

**The earlier leads under real prizes:**
- **Mars rashi × month (cold):** lost RM80 of RM100 with 10 tickets and RM400 of RM450 with System 10. Its "good" results were mostly 3–4 main numbers, which pay nothing.
- **Mars rashi × Venus combust:** about broke even (+RM145, +RM20, +RM25).
- **Moon rashi × Mars combust:** +RM200 on System 9 overlap, from one 6+1.

Nothing is genuinely profitable here; only hindsight finds winners, and the shifted calendars produce them just as easily.

Results are in `analysis/PROFIT_*.md`, with a summary added to FINDINGS.md. Everything is pushed to `claude/focused-franklin-ajsdm9`.

Sources:
- [Magnum4D – Magnum Life](https://www.magnum4d.my/games/magnum-life)
- [Magnum Life System Play 9 prize structure (PDF)](https://www.magnum4d.my/getmedia/3ffc9f26-674c-42f9-9d75-530c1a933f51/MagnumLife-SystemPlay9-PrizeStructure.pdf)
- [Magnum Life System Play 10 prize structure (PDF)](https://www.magnum4d.my/getmedia/f3ee53ed-0e06-4c95-bebd-289eab1820cd/MagnumLife-SystemPlay10-PrizeStructure.pdf)
- [Public Gaming Research Institute – Magnum Life launch](https://www.publicgaming.com/news-categories/company-news/2870-magnum-s-new-game-offers-winners-rm1-000-a-day-for-20-years)

---

**User:**

> Ok rank the new leads based on the profit margin for me to see the performance

**Answer:**

Every new lead had a huge profit margin on the last 10 draws, but each one lost money on the 1,002 earlier draws, mostly more than random tickets. Random tickets lose 45% of the stake in every format.

The ranking below covers the top 20 leads by profit in each of the four formats. Margin is profit ÷ stake over the last 10 draws. *Earlier margin* is the same lead on the earlier draws, and *rank earlier* is its rank by profit there, out of 26,224.

| # | Lead | Pattern | Format | Stake | Profit | Margin | Winning draws | Earlier margin | Rank earlier |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Paksha × Venus rashi | cold | 10 tickets | RM100 | +7,330,300 | +7,330,300% | 1/10 | −81% | 12,375 |
| 2 | Paksha × Venus rashi | cold | System 10 × 1 | RM450 | +7,398,350 | +1,644,078% | 1/10 | −77% | 8,135 |
| 3 | Aspect Venus–Jupiter × universal day | hot | System 9 × 2 overlap | RM180 | +110,060 | +61,144% | 1/10 | −73% | 4,750 |
| 4 | Ayana × lunar leap month | hot+100 | System 9 × 2 disjoint | RM180 | +110,020 | +61,122% | 1/10 | −55% | 1,649 |
| 5 | Paksha × Venus rashi | cold | System 9 × 2 overlap | RM180 | +25,220 | +14,011% | 1/10 | −88% | 24,979 |
| 6 | Rahu rashi × aspect Mercury–Saturn | cold | System 9 × 2 disjoint | RM180 | +12,685 | +7,047% | 4/10 | −82% | 16,639 |
| 7 | Sun rashi × tropical Sun sign | pos | System 9 × 2 disjoint | RM180 | +12,600 | +7,000% | 3/10 | −79% | 10,806 |
| 8 | Nakshatra pada × ayana | cold | System 9 × 2 disjoint | RM180 | +12,580 | +6,989% | 3/10 | −70% | 3,375 |
| 9 | Saturn combust × plum trigrams | cold | System 9 × 2 overlap | RM180 | +12,560 | +6,978% | 1/10 | −80% | 11,064 |
| 10 | Day pillar × aspect Jupiter–Saturn | pos | System 9 × 2 overlap | RM180 | +12,560 | +6,978% | 3/10 | −76% | 6,819 |
| 11 | Paksha × mansion 28 | hot | System 9 × 2 disjoint | RM180 | +12,560 | +6,978% | 3/10 | −86% | 23,952 |
| 12 | Day element × day-vs-year branch | pos | System 9 × 2 disjoint | RM180 | +12,560 | +6,978% | 3/10 | −67% | 2,568 |
| 13 | Tropical Sun sign × draw in daylight | pos | System 9 × 2 disjoint | RM180 | +12,560 | +6,978% | 2/10 | −70% | 3,595 |
| 14 | Saturn combust × plum trigrams | cold | 10 tickets | RM100 | +6,620 | +6,620% | 1/10 | −84% | 17,220 |
| 15 | Aspect Jupiter–Saturn × plum trigrams | cold | 10 tickets | RM100 | +6,455 | +6,455% | 2/10 | −85% | 19,582 |
| 16 | Day of month × plum trigrams | pos | 10 tickets | RM100 | +6,440 | +6,440% | 1/10 | −80% | 10,718 |
| 17 | Mercury nakshatra × aspect Sun–Venus | cold | System 10 × 1 | RM450 | +20,010 | +4,447% | 3/10 | −79% | 10,203 |
| 18 | Day pillar × aspect Jupiter–Saturn | pos | System 10 × 1 | RM450 | +19,960 | +4,436% | 3/10 | −33% | 1,236 |
| 19 | Mercury nakshatra × Venus combust | cold | System 10 × 1 | RM450 | +19,960 | +4,436% | 2/10 | −81% | 13,207 |
| 20 | Mercury nakshatra (single) | cold | System 10 × 1 | RM450 | +19,910 | +4,424% | 2/10 | −81% | 13,370 |

- **One big prize per lead:** each margin comes from a single large prize, usually on one draw. These were the Grand prize on 26 Sep (#1–2), a 7 + bonus worth RM100,000 (#3–4), and a 7-number RM6,000 hit (#14–16, and inside the ~RM12.5k System 9 results). On the other draws these leads mostly lost their stake.
- **Not leads beforehand:** most ranked in the thousands or tens of thousands on the earlier draws. The best of them, Day pillar × aspect Jupiter–Saturn (pos), was 1,236th and still lost 33%.
- **Shifted calendars match them:** calendars that don't match the real sky produced winners of the same size on the same 10 draws, up to +RM121,430.

My recommendation is not to play any of these as a system. If you want one for fun, Paksha × Venus rashi (cold) is the one that made the most money on recent draws, but it is a reminder of luck, not an edge.

The full table, all 80 rows, is in `analysis/PROFIT_MARGIN.md`, pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Ok now how about the one that has the highest hit per day, tabulate them as well for me to see the profit

**Answer:**

"Hit per day" here means draws that paid any prize. I need per-draw wins for every lead, but only the top 20 by profit were saved, so I'm adding a hit-frequency ranking to the script and rerunning it.

**Answer:**

Now adding the hit-frequency tables to the report output.

**Answer:**

I'm rerunning all four formats so every lead gets a count of prize-winning draws over the last 10. The tables will show the leads that won on the most days, their profit, the earlier win rate, and how often random entries win. I'll report when it finishes.

**Answer:**

I've committed and pushed the updated script, which now ranks leads by how many draws won a prize. The rerun across all four formats is still going. Once it finishes I'll commit the new tables and show you the leads with the most winning days and their profit.

**Answer:**

Picking leads by how often they win a prize doesn't make money either. A random entry wins some prize on about 6–7% of draws, or about 0.7 of 10. The best leads won on 4–6 of the last 10 draws, but mostly small prizes, so most still lost money. Shifted calendars produced leads with just as many winning days (up to 5–6).

**10 tickets** (RM100 stake; most winning days was 4/10, by 22 leads; shifted calendars reached 5 and 6):

| # | Lead | Pattern | Winning days | Profit (RM) | Earlier win rate |
|---|---|---|---|---|---|
| 1 | KP Sun sub-lord × year yin-yang | pos | 4/10 | +235 | 6.4% |
| 2 | Hora lord × Mercury rashi | cold | 4/10 | +85 | 6.6% |
| 3 | Ayana × KP Moon star-lord | pos | 4/10 | +80 | 7.1% |
| 4 | Ayana × KP Moon star-lord | hot | 4/10 | +40 | 6.5% |
| 5 | Mars rashi × Mars retrograde | cold | 4/10 | +20 | 7.7% |
| 6 | Mercury retrograde × aspect Venus–Mars | cold | 4/10 | +20 | 8.2% |
| 7 | Mars rashi × aspects soft | cold | 4/10 | 0 | 6.3% |
| 8 | Venus retrograde × day officer | cold | 4/10 | −10 | 6.7% |

**System 10 × 1** (RM450 stake; most winning days was 4/10, by 26 leads; shifted calendars reached 5 and 5):

| # | Lead | Pattern | Winning days | Profit (RM) | Earlier win rate |
|---|---|---|---|---|---|
| 1 | KP Sun sub-lord × year yin-yang | hot | 4/10 | +540 | 5.9% |
| 2 | Jupiter retrograde × day branch | cold | 4/10 | +120 | 6.5% |
| 3 | Ayana × KP Moon star-lord | pos | 4/10 | +120 | 5.9% |
| 4 | Hora lord × KP Moon sub-lord | cold | 4/10 | +70 | 6.4% |
| 5 | Mercury retrograde × aspect Venus–Mars | cold | 4/10 | +70 | 7.7% |
| 6 | Karana × tropical Moon sign | hot | 4/10 | +20 | 6.0% |
| 7 | Moon navamsa × solar term | cold | 4/10 | +20 | 5.4% |
| 8 | Draw in daylight × aspect Mercury–Mars | cold | 4/10 | −100 | 6.9% |

**System 9 × 2 overlap** (RM180 stake; shifted calendars reached 4 and 6):

| # | Lead | Pattern | Winning days | Profit (RM) | Earlier win rate |
|---|---|---|---|---|---|
| 1 | Moon navamsa × solar term | cold | **5/10** | −60 | 5.7% |
| 2 | Ayana × KP Moon star-lord | pos | 4/10 | +300 | 7.4% |
| 3 | Month branch × draw in daylight | cold | 4/10 | +65 | 5.0% |
| 4 | Aspect Venus–Saturn × aspects soft | cold | 4/10 | +65 | 6.2% |
| 5 | Mars nakshatra × KP Sun star-lord | pos | 4/10 | +25 | 6.0% |
| 6 | Planets with Moon × ritu | hot | 4/10 | +25 | 7.2% |
| 7 | Mars rashi × aspect Mars–Jupiter | cold | 4/10 | +5 | 7.1% |

**System 9 × 2 disjoint** (RM180 stake; shifted calendars reached 5 and 5):

| # | Lead | Pattern | Winning days | Profit (RM) | Earlier win rate |
|---|---|---|---|---|---|
| 1 | Aspect Sun–Mercury × universal day | pos | **6/10** | −20 | 7.8% |
| 2 | Mercury rashi × aspect Moon–Mercury | cold | 5/10 | +280 | 7.0% |
| 3 | Aspect Sun–Mercury × universal day | hot | 5/10 | −40 | 7.4% |
| 4 | Mansion 28 × aspect Sun–Mercury | cold | 5/10 | −60 | 6.8% |
| 5 | Rahu rashi × aspect Mercury–Saturn | cold | 4/10 | **+12,685** | 8.1% |
| 6 | Mercury rashi × Saturn retrograde | cold | 4/10 | +260 | 8.0% |
| 7 | Mercury nakshatra × aspect Sun–Venus | cold | 4/10 | +240 | 7.7% |
| 8 | Jupiter retrograde × universal day | hot+100 | 4/10 | +240 | 6.5% |

- **Frequent wins are small wins:** most of these prizes are RM5–RM55 (4+bonus, 5, 5+bonus). That doesn't cover a RM10–RM45 stake, so the lead with the most winning days in each System 9 format still lost money.
- **The profit came from one bigger prize:**
  - Rahu rashi × aspect Mercury–Saturn made +RM12,685 from a single 7-number hit on 3 Oct.
  - KP Sun sub-lord × year yin-yang made +RM540 from a 6+bonus on the last draw.
- **Choosing by earlier win rate doesn't work:**
  - On the earlier draws, the best leads won on 9–11% of draws, against about 6–7% for random entries.
  - On the last 10 they averaged only 0.3–1.0 winning days and lost close to the whole stake: −RM97 (10 tickets), −RM425 (System 10), −RM148 (overlap), −RM154 (disjoint).
  - Shifted calendars did the same.
- **Ayana × KP Moon star-lord and KP Sun sub-lord × year yin-yang:** these are the only leads near the top in three formats each. But they were ranked in the thousands on the earlier draws and won only about 6–7% of the time there, which is chance level.

The full top-20 tables are in `analysis/PROFIT_*.md`, pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Oh no I think you made a mistake, system 10 is suppose to be only 1 ticket per race while system 9 is 2 tickets per race

**Answer:**

I checked the code and the saved results: the profit tables already use 1 System 10 ticket per draw and 2 System 9 tickets per draw, so there's no mistake to fix. The stakes in my tables look high because they are totals over all 10 draws, and I didn't say that clearly.

| Format | Tickets per draw | What one ticket covers | Cost per draw | Stake over the 10 draws |
|---|---|---|---|---|
| System 10 × 1 | **1** ticket: the lead's top 10 numbers | 45 combinations of 8 numbers | RM45 | RM450 |
| System 9 × 2 | **2** tickets: two 9-number sets (overlap or disjoint) | 9 combinations each | RM18 | RM180 |
| 10 ordinary tickets | 10 tickets of 8 numbers | 1 combination each | RM10 | RM100 |

- **RM45 is one ticket:** Magnum's official System Play 10 prize sheet prices one System 10 ticket at RM45, because it covers 45 combinations at RM1 each.
- **RM450 is ten draws:** it is 10 draws × RM45, not 10 tickets.
- **System 9 the same way:** each ticket is RM9, so two tickets are RM18 a draw and RM180 over the 10 draws.

So the System 10 results stand as reported. For example, KP Sun sub-lord × year yin-yang (hot) won on 4 of the 10 draws and made +RM540 on the RM450 total. Paksha × Venus rashi (cold) had all 8 numbers inside its single 10-number ticket on 26 Sep, which pays the Grand prize.

If you meant something else by a ticket, such as a System 10 ticket costing RM10, tell me the price you play at and I'll redo the profit tables with it.

---

**User:**

> The interesting part is the previous lead of mars rashi is not in both table?

**Answer:**

That's right. Mars rashi × month (cold) is in neither the profit table nor the winning-days table, because it caught mostly 3 and sometimes 4 main numbers, and those pay nothing.

| Format | Profit over the 10 draws | Winning days | Rank by earlier profit (of 26,224) |
|---|---|---|---|
| 10 ordinary tickets (RM100) | −RM80 | 1/10 | 19,811 |
| System 10 × 1 (RM450) | −RM400 | 1/10 | 16,484 |
| System 9 × 2 overlap (RM180) | −RM160 | 1/10 | 16,256 |
| System 9 × 2 disjoint (RM180) | −RM160 | 1/10 | 18,240 |

Earlier I ranked leads by total balls caught. On that measure it led with 34 in System 10, against 27.8 expected. The prize table needs at least 4 winning numbers + 1 bonus, or 5 winning numbers, in one 8-number combination.

Its System 10 ticket, draw by draw (main + bonus caught):

| Draw | 26 Sep | 27 Sep | 30 Sep | 3 Oct | 4 Oct | 7 Oct | 10 Oct | 11 Oct | 14 Oct | 17 Oct |
|---|---|---|---|---|---|---|---|---|---|---|
| Caught | 2+0 | 4+0 | 3+1 | 3+0 | 3+1 | 2+0 | 3+0 | 3+0 | 3+1 | 4+1 |
| Prize | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | RM50 |

- **The 4s pay nothing:** 4 main numbers with no bonus doesn't win, and 3 + 1 bonus doesn't either. Only the last draw, 4 + 1 bonus, paid: 10 combinations × RM5.
- **It rarely catches bonus balls:** only 3–4 over the 10 draws, against about 5.5 expected. Most low prizes depend on a bonus ball.
- **It never reached 5 main numbers:** that is where prizes start without a bonus.

So "catches more balls than average" and "makes money" are different things. In Magnum Life, money comes almost entirely from the rare 5+, 6+ or 7+ hits. A lead that steadily catches 3–4 numbers gets none of them.

---

**User:**

> Ok fine you have done the analysis for system 9 and 10, but you have not done the analysis for 10 tickets of the normal 8 numbers?

**Answer:**

I did run 10 ordinary 8-number tickets: each lead played 10 tickets of 8 numbers at RM1 each, RM10 per draw and RM100 over the 10 draws. It is the "10 tickets" format in both earlier tables, but it was mixed in with the System results, so here it is on its own. In short, picking a lead in advance lost almost the whole stake, which is worse than random tickets.

**Overview** (26,224 leads, hot/cold updated before every draw):

| | Result over the 10 draws |
|---|---|
| Random tickets, expected | −RM45 (55% returned); some prize on 6.6% of draws |
| Leads that ended in profit | 589 of 26,224 (shifted calendars: 340, 327) |
| #1 lead by earlier profit (Ritu × year yin-yang, hot), played on the 10 draws | −RM100 |
| Top 10 by earlier profit, average | −RM94 |
| Re-ranked by profit before every draw | −RM100 (kept Ritu × year yin-yang every draw) |
| Top 10 by earlier win rate, average | −RM97 (0.3 winning days) |

**Top 10 by profit on the last 10 draws (hindsight):**

| # | Lead | Pattern | Profit (RM) | Winning days | Rank earlier |
|---|---|---|---|---|---|
| 1 | Paksha × Venus rashi | cold | **+7,330,300** (Grand prize, 26 Sep) | 1/10 | 12,375 |
| 2 | Saturn combust × plum trigrams | cold | +6,620 | 1/10 | 17,220 |
| 3 | Aspect Jupiter–Saturn × plum trigrams | cold | +6,455 | 2/10 | 19,582 |
| 4 | Day of month × plum trigrams | pos | +6,440 | 1/10 | 10,715 |
| 5 | Day god × aspect Mars–Saturn | hot | +1,885 | 1/10 | 14,694 |
| 6 | Yoga × Moon phase | hot | +1,355 | 1/10 | 23,030 |
| 7 | KP Sun sub-lord × nine-star year | pos | +1,290 | 1/10 | 4,136 |
| 8 | Karana × aspect Mars–Saturn | hot | +940 | 1/10 | 4,059 |
| 9 | Karana × aspect Mars–Saturn | pos | +940 | 1/10 | 4,212 |
| 10 | Day pillar × draw in daylight | pos | +940 | 1/10 | 2,941 |

- **#2–4** each hit 7 numbers once, the RM6,000 prize.
- **#5–10** each hit one 6+bonus (RM600) or a few smaller prizes.

**Top 8 by winning days on the last 10 draws:**

| # | Lead | Pattern | Winning days | Profit (RM) |
|---|---|---|---|---|
| 1 | KP Sun sub-lord × year yin-yang | pos | 4/10 | +235 |
| 2 | Hora lord × Mercury rashi | cold | 4/10 | +85 |
| 3 | Ayana × KP Moon star-lord | pos | 4/10 | +80 |
| 4 | Ayana × KP Moon star-lord | hot | 4/10 | +40 |
| 5 | Mars rashi × Mars retrograde | cold | 4/10 | +20 |
| 6 | Mercury retrograde × aspect Venus–Mars | cold | 4/10 | +20 |
| 7 | Mars rashi × aspects soft | cold | 4/10 | 0 |
| 8 | Venus retrograde × day officer | cold | 4/10 | −10 |

On shifted calendars, the most winning days reached 5 and 6, more than the real calendar's best of 4.

**The earlier leads with 10 ordinary tickets:**

| Lead | Profit (RM) |
|---|---|
| Mars rashi × Venus combust (cold) | +145 |
| Moon rashi × Mars combust (pos) | +10 |
| Mars rashi × month (cold) | −80 |
| Venus nakshatra × KP Moon sub-lord (hot) | −95 |
| Mars rashi × tropical Sun sign (cold) | −100 |
| Mercury nakshatra × Venus rashi (hot) | −100 |

These come from `analysis/PROFIT_10_BONUS.md`, pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Ok now for all the system 10,9 and normal, rerank based on optimized number of stake and profit and the number of hits

**Answer:**

I'll combine all three formats into one ranking. For each lead in each format I'll score the profit margin (profit ÷ stake, which builds in the stake) and the number of winning days, then rank by the average of those two ranks. I'll also show which format suits each lead best, and test the same score chosen on the earlier draws. That needs every lead's per-draw results, not just the top 20, so I'm saving the full arrays and rerunning.

**Answer:**

While that runs, I'm writing the script that combines the three formats.

**Answer:**

The rerun is still going (10-ticket format first). I'll wait for it to finish, then run the combined ranking.

**Answer:**

I'm waiting for the four formats to finish rerunning. The combined ranking will then run on its own, and I'll show you the results once it's done.

**Answer:**

I've committed and pushed the scripts and the regenerated 10-ticket results to `claude/focused-franklin-ajsdm9`.

In the regenerated 10-ticket results, a few "rank earlier" positions moved slightly, for example 10,718 became 10,715. That is because leads with equal earlier profit are ordered in whatever order the parallel workers finish. The profit and win numbers are the same.

The rerun for the other three formats is still going, and the combined ranking will run straight after it.

**Answer:**

I've put all three formats into one ranking: every lead in every format is one row, 104,896 rows in total. Each row's score is the average of its rank by profit margin and its rank by winning draws, so lower is better. Margin is profit ÷ stake, so the stake is built into it. With hindsight, the best combination of stake, profit and hits on the last 10 draws is **Rahu rashi × aspect Mercury–Saturn (cold), played as System 9 × 2 disjoint**. Chosen in advance with the same score, though, every top pick lost money.

**Top 20 on the last 10 draws (hindsight):**

| # | Lead | Pattern | Format | Stake | Profit | Margin | Winning draws | Score |
|---|---|---|---|---|---|---|---|---|
| 1 | Rahu rashi × aspect Mercury–Saturn | cold | System 9 × 2 disjoint | RM180 | +12,685 | +7,047% | 4/10 | 6 |
| 2 | Sun rashi × tropical Sun sign | pos | System 9 × 2 disjoint | RM180 | +12,600 | +7,000% | 3/10 | 62 |
| 3 | Nakshatra pada × ayana | cold | System 9 × 2 disjoint | RM180 | +12,580 | +6,989% | 3/10 | 63 |
| 4 | Day pillar × aspect Jupiter–Saturn | pos | System 9 × 2 overlap | RM180 | +12,560 | +6,978% | 3/10 | 64 |
| 5 | Paksha × mansion 28 | hot | System 9 × 2 disjoint | RM180 | +12,560 | +6,978% | 3/10 | 64 |
| 6 | Day element × day-vs-year branch | pos | System 9 × 2 disjoint | RM180 | +12,560 | +6,978% | 3/10 | 64 |
| 7 | Mercury nakshatra × aspect Sun–Venus | cold | System 10 × 1 | RM450 | +20,010 | +4,447% | 3/10 | 72 |
| 8 | Day pillar × aspect Jupiter–Saturn | pos | System 10 × 1 | RM450 | +19,960 | +4,436% | 3/10 | 72 |
| 9 | Nakshatra lord × KP ascendant sub-lord | hot | System 9 × 2 disjoint | RM180 | +1,700 | +944% | 3/10 | 82 |
| 10 | Mercury nakshatra × plum trigrams | pos | 10 tickets | RM100 | +870 | +870% | 3/10 | 84 |
| 11 | Karana × aspect Mars–Saturn | hot | System 9 × 2 disjoint | RM180 | +1,340 | +744% | 3/10 | 92 |
| 12 | Moon rashi × Venus combust | pos | System 9 × 2 disjoint | RM180 | +1,340 | +744% | 3/10 | 92 |
| 13 | Mercury retrograde × KP Sun sub-lord | hot | System 9 × 2 disjoint | RM180 | +1,340 | +744% | 3/10 | 92 |
| 14 | Venus retrograde × day of month | hot | System 9 × 2 disjoint | RM180 | +1,340 | +744% | 3/10 | 92 |
| 15 | Mars rashi × nayin | hot | 10 tickets | RM100 | +700 | +700% | 3/10 | 152 |
| 16 | Jupiter retrograde × ritu | pos | 10 tickets | RM100 | +685 | +685% | 3/10 | 154 |
| 17 | Hora lord × Mercury rashi | cold | System 10 × 1 | RM450 | +2,475 | +550% | 3/10 | 160 |
| 18 | Mercury retrograde × KP Sun sub-lord | hot | System 10 × 1 | RM450 | +2,475 | +550% | 3/10 | 160 |
| 19 | KP ascendant sub-lord × aspect Mercury–Jupiter | cold | System 10 × 1 | RM450 | +2,475 | +550% | 3/10 | 160 |
| 20 | KP Sun sub-lord × year yin-yang | pos | 10 tickets | RM100 | +235 | +235% | 4/10 | 162 |

- **Big profits come from one big hit:**
  - #1–6 each had one 7-number hit (about +RM12,680 in System 9).
  - #7–8 had one 7-number hit in System 10 (+RM20,265).
  - #9–20 had one 6+bonus or 6-number hit.
  - Their other winning draws were RM2–RM55.
- **The jackpot lead drops out:** Paksha × Venus rashi won only on 1 of 10 draws, so it no longer reaches the top.
- **Best format:** System 9 × 2 disjoint fills most of the top. Among leads, 10 tickets was the best format by margin for the most (12,687), then System 9 disjoint (5,864), System 10 (4,759) and System 9 overlap (2,914).
- **Not much better than shifted calendars:** 319 rows were in profit with 3+ winning draws, against 188 and 224 on the shifted calendars.

**Chosen in advance with the same score:**
- **The top 10 on the earlier draws** were all System 9 × 2 disjoint leads, such as Year animal × draw in daylight (cold), with earlier margins of +530% to +550%. Those margins come from one Grand prize hit in the past.
- **On the last 10 draws** they lost RM152 on average out of RM180, with 0.7 winning draws.
- **Shifted calendars** lost RM172 and RM199 on the same test, about the same.
- **Random tickets** lose about RM81 on RM180.

Every leader in this ranking was a loser beforehand: earlier margins of −33% to −89%, against −45% for random tickets. If you want a format to play, System 9 × 2 disjoint gives the most chances at the 7-number prize for the stake. It still has the same 45% expected loss as every format, whatever lead feeds it.

The full table is in `analysis/PROFIT_COMBINED.md`, with a summary added to FINDINGS.md. Everything is pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Ok now let’s analyse on the lead that successfully predicted the grand win, how many leads manage to find the grand win for the 10 draws?

**Answer:**

Over the last 10 draws, only one lead out of 26,224 found the Grand prize: **Paksha × Venus rashi (cold), on 26 Sep 2026**. It won in two formats, and no other lead or format hit all 8 numbers on any of the 10 draws.

| Format | Leads with a Grand prize, last 10 draws | Shifted calendars | Expected by luck alone* |
|---|---|---|---|
| 10 ordinary tickets | **1** (Paksha × Venus rashi, 26 Sep) | 0, 0 | 0.09 |
| System 10 × 1 | **1** (same lead, same draw) | 0, 0 | 0.39 |
| System 9 × 2 overlap | 0 | 0, 0 | 0.15 |
| System 9 × 2 disjoint | 0 | 0, 0 | 0.16 |

\*Expected count if every lead were a random set of tickets, from 1 in 30.3 million per 8-number combination. Leads overlap a lot, so the real chance of at least one hit is a little lower.

**Was it a lead or luck?**

1. **No other lead came close that day.** On 26 Sep it was the only lead in 10 tickets or System 10 with even 7 numbers. On one shifted calendar, 4 leads got a 7-number prize on that same draw.
2. **It has no track record.** On the 1,002 earlier draws it never hit a Grand, ranked 12,375th on profit, and lost RM8,140 with 10 tickets (−81%).
3. **Grand hits happen about as often as luck predicts.** On the 1,002 earlier draws, leads hit the Grand at roughly the chance rate, and shifted calendars, which don't match the real sky, do the same:

| Format | Leads with ≥1 earlier Grand, real calendar | Shifted calendars | Expected by luck |
|---|---|---|---|
| 10 tickets | 6 | 7, 4 | ≈ 9 |
| System 10 × 1 | 38 | 31, 14 | ≈ 39 |
| System 9 × 2 overlap | 11 | 9, 9 | ≈ 15 |
| System 9 × 2 disjoint | 11 | 11, 5 | ≈ 16 |

4. **Past Grand winners didn't repeat.** The leads that hit a Grand earlier, such as Ritu × year yin-yang and Hora lord × Saturn nakshatra, lost almost their whole stake on the last 10 draws.

So with 26,224 leads, about one Grand somewhere among them every 100 draws or so is expected, which is close to what we saw. Paksha × Venus rashi was the one that happened to land in this window, and nothing in its history pointed to it beforehand.

---

**User:**

> Ok list out all the other leads that manage to hit high amount of numbers for higher prize like 7,6 numbers

**Answer:**

I'll recompute, for every lead, format and draw in the last 10, the best match in any of its 8-number combinations. Then I'll list every 7-number and 6-number hit, with the shifted calendars as a comparison.

**Answer:**

The script is running across all four formats. It lists every lead that caught 6, 7 or 8 winning numbers in one combination on the last 10 draws, with the prize paid and the shifted calendars for comparison. I'll show the results when it's done.

**Answer:**

The new script (`analysis/high_hits.py`) is committed and pushed. It's still running across the four formats; when it finishes I'll commit the results and list every lead that caught 6, 7 or 8 winning numbers in one combination.

**Answer:**

Here is every lead that caught 7 or 8 numbers in one combination over the last 10 draws, plus counts of 6-number hits. All of these leads ranked low on the earlier draws, so none were picked out in advance. One thing stands out: the real calendar produced noticeably more 6+ hits than the two shifted calendars.

**How many lead × draw hits, out of 26,224 leads:**

| Format | 8 (Grand) | 7 + bonus (2nd) | 7 (3rd) | 6 + bonus (4th) | 6 (5th) | Shifted calendars: 7+ / 6+ hits |
|---|---|---|---|---|---|---|
| 10 ordinary tickets | 1 | 0 | 3 | 35 | 263 | 6 / 165, 2 / 155 (real 4 / 302) |
| System 10 × 1 | 1 | 0 | 14 | 65 | 293 | 4 / 216, 3 / 257 (real 15 / 373) |
| System 9 × 2 overlap | 0 | 1 | 4 | 47 | 258 | 4 / 187, 2 / 176 (real 5 / 310) |
| System 9 × 2 disjoint | 0 | 1 | 13 | 80 | 281 | 8 / 293, 4 / 323 (real 14 / 375) |

**Every 7- and 8-number hit:**

| Format | Lead | Pattern | Draw | Best match | Payout that draw | Profit, 10 draws | Rank earlier |
|---|---|---|---|---|---|---|---|
| 10 tickets | Paksha × Venus rashi | cold | 26 Sep | **8 (Grand)** | RM7,330,400 | +7,330,300 | 12,376 |
| 10 tickets | Saturn combust × plum trigrams | cold | 3 Oct | 7 | RM6,720 | +6,620 | 17,220 |
| 10 tickets | Aspect Jupiter–Saturn × plum trigrams | cold | 3 Oct | 7 | RM6,540 | +6,455 | 19,582 |
| 10 tickets | Day of month × plum trigrams | pos | 7 Oct | 7 | RM6,540 | +6,440 | 10,720 |
| System 10 | Paksha × Venus rashi | cold | 26 Sep | **8 (Grand)** | RM7,398,800 | +7,398,350 | 8,135 |
| System 10 | Saturn nakshatra × aspect Moon–Jupiter | pos | 27 Sep | 7 | RM20,310 | +19,860 | 7,096 |
| System 10 | Moon rashi × Mars retrograde | pos | 30 Sep | 7 | RM20,310 | +19,860 | 21,342 |
| System 10 | Saturn combust × plum trigrams | cold | 3 Oct | 7 | RM20,310 | +19,910 | 15,960 |
| System 10 | Day pillar × aspect Jupiter–Saturn | pos | 3 Oct | 7 | RM20,310 | +19,960 | 1,236 |
| System 10 | Aspect Jupiter–Saturn × plum trigrams | cold | 3 Oct | 7 | RM20,310 | +19,960 | 18,173 |
| System 10 | Mercury nakshatra, alone and paired with: Mercury rashi, Venus combust, Jupiter combust, Saturn combust, ayana, lunar leap month, aspect Sun–Venus (8 leads) | cold | 4 Oct | 7 | RM20,310 each | ≈ +19,900 each | 202–15,295 |
| System 10 | Venus nakshatra × Part of Fortune rashi | cold | 10 Oct | 7 | RM20,310 | +19,860 | 21,243 |
| System 9 overlap | Aspect Venus–Jupiter × universal day | hot | 30 Sep | **7 + bonus** | RM110,240 | +110,060 | 4,750 |
| System 9 overlap | Paksha × Venus rashi | cold | 26 Sep | 7 | RM25,400 | +25,220 | 24,979 |
| System 9 overlap | Saturn combust × plum trigrams | cold | 3 Oct | 7 | RM12,740 | +12,560 | 11,064 |
| System 9 overlap | Moon rashi × Saturn retrograde | pos | 30 Sep | 7 | RM12,700 | +12,520 | 17,304 |
| System 9 overlap | Day pillar × aspect Jupiter–Saturn | pos | 3 Oct | 7 | RM12,700 | +12,560 | 6,819 |
| System 9 disjoint | Ayana × lunar leap month | hot+100 | 7 Oct | **7 + bonus** | RM110,200 | +110,020 | 1,649 |
| System 9 disjoint | Paksha × Venus rashi | cold | 26 Sep | 7 | RM12,700 | +12,520 | 8,921 |
| System 9 disjoint | Part of Fortune sign × aspect Sun–Mars | hot | 26 Sep | 7 | RM12,700 | +12,520 | 7,193 |
| System 9 disjoint | Rahu rashi × aspect Mercury–Saturn | cold | 3 Oct | 7 | RM12,700 | +12,685 | 16,644 |
| System 9 disjoint | Saturn combust × plum trigrams | cold | 3 Oct | 7 | RM12,700 | +12,540 | 16,653 |
| System 9 disjoint | Day pillar × aspect Jupiter–Saturn | pos | 3 Oct | 7 | RM12,700 | +12,540 | 17,182 |
| System 9 disjoint | Paksha × mansion 28 | hot | 4 Oct | 7 | RM12,700 | +12,560 | 23,949 |
| System 9 disjoint | Nakshatra pada × ayana | cold | 7 Oct | 7 | RM12,700 | +12,580 | 3,375 |
| System 9 disjoint | Day element × day-vs-year branch (hot and pos) | | 10 Oct | 7 | RM12,700 | ≈ +12,550 | 2,568 / 8,313 |
| System 9 disjoint | Sun rashi × tropical Sun sign | pos | 14 Oct | 7 | RM12,700 | +12,600 | 10,806 |
| System 9 disjoint | Sun nakshatra × aspect Mercury–Saturn | cold | 14 Oct | 7 | RM12,700 | +12,560 | 10,689 |
| System 9 disjoint | Tropical Sun sign × draw in daylight | pos | 14 Oct | 7 | RM12,700 | +12,560 | 3,596 |
| System 9 disjoint | Sun nakshatra × aspect Sun–Venus | cold | 17 Oct | 7 | RM12,700 | +12,540 | 18,962 |

- **Leads that hit in several formats:** Paksha × Venus rashi (cold) hit 7–8 in all four formats on 26 Sep. Saturn combust × plum trigrams and Day pillar × aspect Jupiter–Saturn hit 7 in three formats on 3 Oct.
- **Mercury nakshatra (cold), System 10, 4 Oct:** it gave the same 10 numbers, and so the same 7-hit, whether used alone or paired with 7 other parameters. That makes it one hit, not eight.
- **None were picked out in advance:** none of them had a 7+ hit on the earlier draws to make them stand out. Their earlier profit ranks run from 202 to 24,979, mostly in the thousands.

**The real calendar had more 6+ hits:**
- **The gap:** the real calendar had roughly 1.2–1.9 times as many 6+ hits as the two shifted calendars. For 10 tickets that is 302 against 165 and 155.
- **When:** the extra hits mostly fall on 30 Sep – 7 Oct; on 3 Oct, for example, 69 leads had 6+ against 4 and 11.
- **Why I'm not calling it a signal:** two shifted calendars over 10 draws is too few to say whether this is real or a quirk of those few draws. Many leads also share the same tickets, so one good pick on a draw shows up many times. Earlier tests with more shifted calendars and the full history found nothing.

To settle it, I can count 6+ hits for all leads over the whole history, against 10–20 shifted calendars. If the real calendar consistently produces more 6+ hits, that would be the first real sign of a pattern in all this work. Do you want me to run it?

The full list, including every 6-number hit, is in `analysis/HIGH_HITS.md`, pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Yes run it with 20 shifted calendars

**Answer:**

I'll count 6-, 7- and 8-number hits for every lead across the whole history, on the real calendar and on 20 shifted calendars, for all four formats in one pass. First I'm timing a sample to estimate the run length.

**Answer:**

A sample of 400 lead groups on 4 calendars took about 7 seconds, so the full run (26,224 leads × 21 calendars × all draws) should take about 10 minutes. Starting it now.

**Answer:**

The test is running on the real calendar and 20 shifted calendars, across all 26,224 leads, all four formats and the whole history. It should take about 10 minutes, and I'll report when it finishes.

**Answer:**

I've committed and pushed the test script, `analysis/high_hits_null.py`. I also deleted the two output files left over from the quick timing sample, so the only results committed will be from the full run.

The full run is still going, on the real calendar plus 20 shifted ones. When it finishes I'll commit the results and report whether the real calendar gives more 6-, 7- and 8-number hits than chance.

**Answer:**

Over the whole history, the real calendar gives slightly more 6- and 7-number hits than the 20 shifted calendars, in every format. The effect is small and only borderline significant, so it's a hint worth noting, not proof of a pattern, and nowhere near enough to make Magnum Life profitable.

**Whole history, about 1,000 draws × 26,224 leads, counting lead × draw hits:**

| Format | 6+ hits: real vs shifted mean | Rank of 21 | 7+ hits: real vs shifted mean | Rank of 21 | 8 (Grand): real vs shifted mean | Rank of 21 |
|---|---|---|---|---|---|---|
| 10 tickets | 49,063 vs 47,001 (+4%) | 2 | 1,261 vs 1,096 (+15%) | 3 | 7 vs 6 | 6 |
| System 10 × 1 | 59,366 vs 57,685 (+3%) | 2 | 2,402 vs 2,225 (+8%) | 4 | **39 vs 25** (shifted max 38) | **1** |
| System 9 × 2 overlap | 47,749 vs 46,217 (+3%) | 2 | 1,487 vs 1,352 (+10%) | 3 | 11 vs 12 | 8 |
| System 9 × 2 disjoint | 51,320 vs 50,776 (+1%) | 6 | 1,658 vs 1,428 (+16%) | 3 | 11 vs 13 | 7 |

**Last 10 draws only:** the real calendar ranks 4th–5th of 21 on 6+ hits (302 against 235 for 10 tickets). That is within the shifted range of 163–364, so the 1.9× gap I saw earlier against only two shifted calendars was mostly a matter of those two being low.

**Why this is a hint, not proof:**
- **It is really one test, not twelve.** The four formats reuse the same leads and the same rankings. The real calendar coming 2nd–3rd of 21 corresponds to roughly a 5–10% chance of being luck. That is borderline, and the analysis has run a great many tests along the way.
- **The System 10 Grand count is clumpy.** Grand hits cluster: one draw whose 8 numbers sit in the top 10 of many related leads counts many times over. With a few dozen hits, one such draw can produce the gap.
- **It's spread across all leads, not in particular ones.** Every attempt to choose a lead in advance has failed, by profit, win rate, balls caught and the combined score. Nobody can bet on "26,224 leads at once".
- **It doesn't change the money.** About 4% more 6s and 10–15% more 7s barely moves the return. Random tickets return about 55% of the stake, and the Grand prize is most of that. You would still lose roughly 40% or more.

**What would make it convincing:** the same tilt showing up on draws that haven't happened yet. I can freeze this test now and re-run it on the next 20–30 draws. If the real calendar again lands near the top of the 21 on 6+ and 7+ hits, that would be real evidence. I can also check the Grand count draw by draw, to see whether it is one lucky draw.

Results are in `analysis/HIGH_HITS_NULL.md`, with a summary added to FINDINGS.md. Everything is pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Ok fine from this new analysis tell me the lead that perform the best give me 10

**Answer:**

The 20-calendar test only kept totals across all leads, so I'll recount 6+ and 7+ hits per lead. Each lead is then compared against itself on the 20 shifted calendars. The top 10 are picked on the earlier draws only and checked on the last 10, with the same pick made on each shifted calendar as the baseline.

**Answer:**

It's running (about 6–7 minutes). I'll give you the top 10 leads, how each did on the last 10 draws in every format, and the shifted-calendar baseline.

**Answer:**

I've committed and pushed the new per-lead ranking script (`analysis/lead_high_hits.py`). The run is still going; when it finishes I'll commit the results and give you the top 10 leads.

**Answer:**

Here are the 10 best leads from the new analysis, chosen on the earlier draws only. **On the last 10 draws, none of them hit 6 or more numbers in any format**, and they lost about 90% of the stake.

I ranked each lead by how many more 6+ hits it got on the real calendar than on 20 shifted calendars. Hits are summed over the four formats, so one good draw can count up to 4 times.

| # | Lead | Pattern | Earlier 6+ hits (same lead, shifted avg) | Score (z) | Earlier 7+ hits | Last 10: 6+ hits | Last 10 profit (RM): 10 tkts / Sys 10 / Sys 9 overlap / Sys 9 disjoint |
|---|---|---|---|---|---|---|---|
| 1 | Aspect Sun–Mars × hard aspects | hot | 33 (5.9) | +8.9 | 1 | 0 | −85 / −350 / −160 / −180 |
| 2 | Aspect Sun–Venus × aspect Sun–Jupiter | hot+100 | 23 (5.8) | +7.1 | 0 | 0 | −100 / −450 / −180 / −180 |
| 3 | Mars retrograde × planets with Moon | pos | 30 (7.8) | +6.7 | 0 | 0 | −100 / −450 / −160 / −180 |
| 4 | KP Moon sub-lord × day pillar | cold | 17 (4.8) | +6.7 | 2 | 0 | −80 / −350 / −140 / −140 |
| 5 | KP Sun number × day stem | hot | 14 (3.5) | +6.6 | 1 | 0 | −100 / −450 / −180 / −160 |
| 6 | Jupiter rashi × nine-star day | hot | 30 (6.8) | +6.3 | 0 | 0 | −90 / −450 / −180 / −180 |
| 7 | Part of Fortune rashi × aspect Venus–Jupiter | cold | 26 (6.2) | +6.2 | **7** | 0 | −95 / −400 / −180 / −180 |
| 8 | Tithi × Saturn combust | cold | 26 (7.6) | +6.1 | 0 | 0 | −35 / −130 / −55 / −55 |
| 9 | KP Sun number × day branch | hot | 12 (3.4) | +5.9 | 3 | 0 | −100 / −450 / −180 / −160 |
| 10 | Planets with Moon (on its own) | pos | 24 (6.1) | +5.8 | 0 | 0 | −100 / −450 / −180 / −160 |

**What this shows:**
- **The 10 draws were a quiet stretch for them.** An average lead gets about 0.05 hits of 6+ in 10 draws, so 10 leads would expect about 0.5 together. Getting 0 is a little unlucky, not a clear failure.
- **The same pick made on the shifted calendars also got almost nothing:** mostly 0, at most 4 hits.
- **Ten draws is far too short to test these leads.** At their earlier rate, even the best lead would expect only about 0.3 hits of 6+ in 10 draws.
- **The high scores are partly a counting effect.** Each lead's shifted-calendar results are mostly 0–2 hits with little spread, so a lead with one or two strong runs on the real calendar gets a very high z. With 26,224 leads tested, scores of +6 to +9 at the top are expected by luck.

Part of Fortune rashi × aspect Venus–Jupiter (cold) is the most interesting one to follow: it had 7 hits of 7 numbers on the earlier draws, far more than any other lead here.

If you want to test them properly, I can freeze this list now and log their tickets for the next 30–50 draws. That's roughly the time needed for 6+ hits to show up often enough to tell skill from luck.

The table is in `analysis/LEAD_HIGH_HITS.md`, pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Part of Fortune rashi × aspect Venus–Jupiter (cold) is the most interesting one to follow: it had 7 hits of 7 numbers on the earlier draws, far more than any other lead here. Check this out

**Answer:**

I'll look at this lead in detail. For each format I'll list every draw where it caught 6 or 7 numbers, with dates and tickets. I'll compare it with the same lead on the 20 shifted calendars, work out its profit under the real prize rules, and check how many of the 26,224 leads would reach 7 such hits by luck.

**Answer:**

I'm rerunning the per-lead counts so the "how unusual is 7 hits" check covers all 26,224 leads. The detailed breakdown of Part of Fortune rashi × aspect Venus–Jupiter (cold) runs straight after. I'll report when both finish.

**Answer:**

The two updated scripts are committed and pushed: the new single-lead detail report and the per-lead hit counts. Both jobs are still running in the background; when they finish I'll commit the results and report on Part of Fortune rashi × aspect Venus–Jupiter (cold).

**Answer:**

I checked it, and it is less special than it looked. The "7 hits of 7 numbers" was really **2 lucky draws**, each counted once per format. About 15 leads reach that count on the real calendar, and a similar number do on the shifted calendars.

**The two draws:**

| Draw | Earlier draws in its cell | Winning numbers (+ bonus) | Best match: 10 tickets / Sys 10 / Sys 9 overlap / Sys 9 disjoint | Payout (RM) per format |
|---|---|---|---|---|
| 3 Feb 2024 | 52 | 3 6 9 11 14 18 20 36 (+24 31) | 7 / 7 / 7 / 7 | 6,720 / 20,310 / 12,740 / 12,700 |
| 17 Jul 2024 | 57 | 1 14 16 17 19 22 25 27 (+11 35) | 6 / 7 / 7 / 7 | 460 / 20,310 / 12,700 / 12,700 |

- **Two different cells:** the two draws fell in different Part of Fortune rashi / aspect Venus–Jupiter combinations, so the lead's success doesn't come from one recurring sky pattern.
- **One draw counted up to four times:** adding them up across formats (1 + 2 + 2 + 2) is what produced "7".

**Its record by format:**

| Format | 6+ hits earlier | 7+ hits earlier | Profit earlier (RM) | Return earlier | Last 10 draws |
|---|---|---|---|---|---|
| 10 tickets | 7 | 1 | −440 | 96% | no 6+, −95 |
| System 10 × 1 | 7 | 2 | +6,090 | 114% | no 6+, −400 |
| System 9 × 2 overlap | 7 | 2 | **+13,889** | **177%** | no 6+, −180 |
| System 9 × 2 disjoint | 5 | 2 | +12,484 | 169% | no 6+, −180 |

Random entries return about 55% of the stake. Its earlier profit in the System formats comes almost entirely from those two 7-number draws. On the last 10 draws it caught no 6+ and lost money in every format.

**Is it unusual?**
- **Against its own shifted calendars:** the same lead averages about 0.1 hits of 7 numbers per format, so 2 looks rare for this one lead.
- **Against all 26,224 leads:**
  - 15 leads reach 7 or more such hits on the real calendar. The 20 shifted calendars give 3–22 leads each, typically about 9.
  - The best lead on the real calendar has 8, while the shifted calendars' best is 8–13.
- **So:** a lead with 2 lucky draws is exactly what you expect to find when searching this many. Its real-calendar result is in line with the shifted calendars.

If you want to keep following it anyway, the 10 numbers it played for the latest draw (17 Oct, System 10) were **1 4 9 11 12 13 18 30 32 34**. I can work out its numbers for the next Magnum Life draw and log them, so we can see whether it adds another 7-number hit. Treat it as a fun watch, not a bet.

The report is in `analysis/LEAD_DETAIL_POF_RASHI_ASPECT_VENUS_JUPITER_COLD.md`, pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Based on all this leads which one needs to be observed and some what came out to be rare and have high amount of profit

**Answer:**

The one most worth watching is **Mercury nakshatra × Saturn combust (cold), played as System 10**. It is the only lead that made a big profit both on the earlier draws and on the last 10. Below it are the rare big-hit leads and the frequent small winners. None has yet beaten chance on draws it hadn't seen, so treat this as a list to observe, not to bet on.

**1. Top pick: Mercury nakshatra × Saturn combust (cold)**

| | Earlier draws (2020–Sep 2026) | Last 10 draws |
|---|---|---|
| System 10 × 1 | **+RM87,135, 293% return** (ranked 202 of 26,224) | **+RM19,910** (7 numbers on 4 Oct) |
| System 9 × 2 overlap / disjoint | 89% / 90% return | +RM260 / +RM180 (6 numbers on 4 Oct) |
| 10 tickets | 81% return | +RM270 |

- **What it means:** random entries return about 55%, so it did better than random in every format, before and during the test window.
- **The catch:** the 293% comes from a single 7 + bonus on 4 Dec 2022 (RM121,730). That draw came from a cell with only 9 earlier draws, a thin basis for the ranking. Its two big hits fell in different cells.
- **How rare it is:** about 623 leads have as many 7-number hits on the real calendar. The shifted calendars have 367–661, so it's normal for a search this size.
- **Latest numbers:** its System 10 set for the 17 Oct draw was **7 8 10 14 20 22 27 28 31 36**.

**2. Rare big hits in the last 10 draws**

| Lead | Pattern | Big hit | Best format | Earlier return (rank) |
|---|---|---|---|---|
| Paksha × Venus rashi | cold | **All 8 (Grand)**, 26 Sep | 10 tickets / System 10 | 19–23% (8,135–12,375) |
| Ayana × lunar leap month | hot+100 | **7 + bonus, RM110,200**, 7 Oct | System 9 × 2 disjoint | 45% (1,649) |
| Aspect Venus–Jupiter × universal day | hot | **7 + bonus, RM110,240**, 30 Sep | System 9 × 2 overlap | 27% (4,750) |
| Day pillar × aspect Jupiter–Saturn | pos | 7 numbers in three formats, 3 Oct; +RM19,960 System 10 | System 10 | **67% (1,236)**, the best earlier record of this group |
| Saturn combust × plum trigrams | cold | 7 numbers in all four formats, 3 Oct; +RM19,910 System 10 | System 10 | 16–20% (11,000+) |

**3. Rare earlier, quiet now:** Part of Fortune rashi × aspect Venus–Jupiter (cold) had two 7-number draws in 2024 and returned 177% in System 9 overlap. It caught no 6+ in the last 10 draws.

**4. Frequent small winners:** KP Sun sub-lord × year yin-yang (hot/pos) and Ayana × KP Moon star-lord (pos). Each won on 4 of the 10 draws and stayed slightly profitable (+RM80 to +RM540), but only from small prizes.

**Not recommended:** Mars rashi × month (cold) catches many numbers, but mostly 3–4 main numbers. Under the real prize table it lost 80–89% of the stake.

**Next step:** freeze this list and log each lead's numbers before every new Magnum Life draw. For a fair verdict, run it for 30–50 draws, and the System 10 leads need longer still. If you want that, I can work out the next draw's numbers for the top picks.

The list is in `analysis/WATCHLIST.md`, with the full report in `analysis/LEAD_DETAIL_MERCURY_NAKSHATRA_SATURN_COMBUST_COLD.md`. Both are pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Ok now let’s get back to the sports toto loto, it has its own bonus number, check the prize structure and also previously all the parameter single and pair that was tested is there to predict only 6 numbers (1 set) now I want it to have 10 sets and check and see how they perform for hot, cold, llm, etc

**Answer:**

Star Toto 6/50 is the only one of the three games with a bonus ball, and the data already includes it. Next I'm confirming the Power and Supreme Toto prize tables against a second source.

**Answer:**

The Toto run is going for all three games (26,224 astrological leads plus about 20 non-parameter methods each, 10 sets of 6 per draw). The longer histories make it heavier than Magnum Life, so it may take 20–30 minutes. I'll report when it's done.

**Answer:**

I've committed and pushed the Toto script (`analysis/toto_profit.py`). The run is still going in the background, and I'll commit the results and report when it finishes.

**Answer:**

I re-ran the three Sports Toto games with the official prize tables and 10 sets of 6 numbers per draw. Across all 26,224 astrological leads and every non-parameter method, nothing chosen in advance made money; every earlier pick lost roughly its whole stake.

The 10-set ticket structure had already been tested on balls caught. What's new here is scoring with real prize money, including Star Toto's bonus ball and Supreme Toto's RM2 bet.

**Prize tables**

| Game (price per set) | 6 | 5 + bonus | 5 | 4 + bonus | 4 | 3 + bonus | 3 |
|---|---|---|---|---|---|---|---|
| Star 6/50 (RM1, 1 bonus ball) | Jackpot 1, min RM1,188,888 | Jackpot 2, min RM100,000 | RM2,008 | RM788 | RM28 | RM18 | RM8 |
| Power 6/55 (RM1, no bonus) | Jackpot, min RM3,000,000 | – | RM3,300 | – | RM40 | – | RM3 |
| Supreme 6/58 (RM2, no bonus) | Jackpot, min RM8,888,888 | – | RM6,888 | – | RM80 | – | RM8 |

With jackpots at their minimum, random sets return about 35% of the stake in Star Toto and about 20% in Power and Supreme. Jackpots are shared if several people win, and that is ignored here.

**Last 10 draws, 10 sets per draw**

| Game (stake) | Random, expected | Best lead in hindsight | Shifted calendars' best | #1 by earlier profit | Top 10 by earlier profit | Best non-astrology method |
|---|---|---|---|---|---|---|
| Star 6/50 (RM100) | −RM65 | +RM8,100: Hora lord × Mars retrograde (cold), 5 numbers on 7 Oct | +8,100 / +8,116 | −RM100 | −RM97 | −RM28 (replay previous draw) |
| Power 6/55 (RM100) | −RM80 | **+RM3,023,083: Masa × day god (hot), all 6 on 27 Sep** | +3,023,080 / +3,016,566 | −RM100 | −RM82 | −RM70 (embedding neural) |
| Supreme 6/58 (RM200) | −RM160 | +RM27,856: Nakshatra × nayin (hot+100), 5 numbers on 11 Oct | +7,192 / +7,264 | −RM200 | −RM146 | −RM160 (analogy similar) |

**Power Toto jackpots:**
- **Two leads hit all 6 numbers:** Masa × day god (hot) on 27 Sep and tropical Sun sign × aspect Moon–Saturn (hot+100) on 11 Oct. Both were ranked 15,000th–20,000th on the earlier draws, with earlier returns of 5–6%.
- **Shifted calendars hit it too:** the same leads on the shifted calendars, which don't match the real sky, got 6 and 1 jackpot hits in the same 10 draws.
- **Earlier draws:** the real calendar had 8 jackpot hits against 15 and 25 on the shifted ones.

**5-number hits:** the real calendar had more on the last 10 draws.

| Game | Real calendar | Shifted calendars |
|---|---|---|
| Star | 28 | 11, 25 |
| Power | 146 | 101, 77 |
| Supreme | 22 | 2, 5 |

In each game they mostly come from one draw: 7 Oct for Star, 11 Oct for Power and Supreme. Many related leads land on the same numbers that day; in Supreme, for example, Nakshatra, Nakshatra pada and KP Moon number paired with day pillar or nayin all hit together. So it's one lucky draw counted many times, not many independent hits.

**Hot, cold, LLM and the other methods:**
- **None made money in any game:** hot and cold look-backs, the hot+cold mix, hot/cold + astrology, analogy, the embedding/LLM-style models, selected parameters and the baselines.
- **Best results:** "replay previous draw" in Star Toto (−RM28 of RM100) and the neural embedding model in Power Toto (−RM70).
- **The baseline:** the random baseline lost about the same.

**Past jackpot winners don't repeat:** the leads with the best earlier profit had returns of +11,000% to +21,000%, each from one past jackpot. All of them lost the full stake, or nearly, on the last 10 draws.

So Toto behaves like Magnum Life: big wins happen, but only to leads that look ordinary beforehand, and shifted calendars produce them just as often. If you want, I can add the Power Toto jackpot leads and the Supreme 11 Oct cluster to the watchlist and track them on the next draws.

Sources:
- [4Dmoon – SportsToto prize structure](https://www.4dmoon.com/sportstoto-prize-structure)
- [4dlatest – Prize structure for Sportstoto games](https://4dlatest.org/prize-structure-sportstoto)
- [Free Malaysia Today – Sports Toto introduces new Star Toto 6/50](https://www.freemalaysiatoday.com/category/nation/2017/10/17/sports-toto-introduces-new-star-toto-650)

The full tables are in `analysis/TOTO_PROFIT.md`, with a summary added to FINDINGS.md. Everything is pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> What happened to the astrological sign single and pairs in this case? Did you do the same analysis like you did for magnum live in terms of the astrological parameter?

**Answer:**

Yes, the Toto analysis covered the same astrological singles and pairs as Magnum Life. The 26,224 "leads" are exactly those, and every named lead in my Toto tables (Hora lord × Mars retrograde, Masa × day god, Nakshatra × nayin and so on) is one of them.

**What the 26,224 leads are, in both games:**
- 114 single parameters, Vedic, Chinese and Western: rashi, nakshatra, tithi, karana, yoga, combustion, retrogrades, aspects, KP lords, Part of Fortune, pillars, nayin, nine-star and others;
- all 6,441 pairs of them;
- plain hot/cold over all draws with no astrology, as a baseline;
- each of those × 4 patterns: hot, cold, position and hot+100.

Each lead builds its numbers before every draw, using only earlier draws that fell in the same astrological cell. Toto plays 10 sets of 6 numbers a draw; Magnum Life used 8-number tickets and System 9/10.

**What was done for both games, and what was Magnum-only so far:**

| Analysis | Magnum Life | Toto |
|---|---|---|
| All singles and pairs × hot/cold/pos/hot+100, official prizes | ✅ | ✅ |
| Profit, best lead in hindsight, shifted calendars | ✅ | ✅ |
| Most winning draws | ✅ | ✅ |
| Top 10 by earlier profit / win rate, played on the last 10 | ✅ | ✅ |
| Every 5/6-number (Toto) or 6/7/8-number (Magnum) hit listed | ✅ | ✅ |
| Non-astrology methods (hot/cold look-backs, LLM/embedding, analogy …) | ✅ | ✅ |
| Re-ranked by profit before every draw | ✅ | ❌ |
| Combined ranking by stake, profit and winning draws | ✅ | ❌ |
| Real calendar vs 20 shifted calendars over the whole history (high-hit test) | ✅ | ❌ |
| Per-lead hits against its own shifted calendars, top 10 + detail reports | ✅ | ❌ |
| System play (System 9 / 10) | ✅ | ❌ (Toto has System 7–12 too) |

**What I would expect from the missing pieces:** the earlier jackpot counts already point the same way.

| Game | Jackpot-level hits on the earlier draws, real calendar | Shifted calendars |
|---|---|---|
| Star | 18 | 15, 18 |
| Power | 8 | 15, 25 |
| Supreme | 13 | 15, 13 |

The real calendar is no better than the shifted ones here. The extra 5-number hits on the last 10 draws come mostly from one draw per game.

If you want Toto to match the Magnum analysis exactly, I can run the five missing pieces for Star, Power and Supreme:
- re-ranked before each draw;
- the combined ranking;
- the 20-shifted-calendar test over the whole history;
- per-lead top 10 with detail reports;
- System play, with the official Toto System 7–12 prize tables.

Do you want me to go ahead?

---

**User:**

> Yes go ahead and run all of them for Toto, I need to see how astrological signs acts here compared to that of magnum live

**Answer:**

I'll run all five missing pieces for Toto in one pass per game: every lead × 4 formats × the real calendar plus 20 shifted calendars over the whole history. First I'm checking how Sports Toto system play is priced and paid.

**Answer:**

All five analyses are now running for Star, Power and Supreme Toto. They cover four formats: 10 sets, System 7 × 2 overlap, System 7 × 2 disjoint and System 8 × 1. Each one runs on the real calendar and 20 shifted calendars over the whole history, and it should take about 1–1.5 hours. When it finishes I'll put the Toto results side by side with Magnum Life.

**Answer:**

The full Toto analysis script (`analysis/toto_full.py`) is committed and pushed to `claude/focused-franklin-ajsdm9`. The run itself is still going in the background; when it finishes I'll commit the results and report.

**Answer:**

The 20-calendar test shows a clear difference between the games. I'm reading the other outputs before writing it up.

**Answer:**

The parameter breakdown points to a real difference between the games. I'll launch a decisive 100-calendar check for Star Toto in the background while I write up.

**Answer:**

All five Toto analyses have finished. Toto behaves like Magnum Life where it matters: no lead or format makes money when chosen in advance. One Toto game, Star Toto 6/50, shows the strongest astrological tilt found so far, while Power and Supreme show none.

**1. Profit, re-ranking before every draw, and the combined ranking: no edge in any game**

| Game, format (stake over 10 draws) | #1 by earlier profit | Top 10 by earlier profit | Re-ranked before every draw | 20 shifted calendars (median) |
|---|---|---|---|---|
| Star, 10 sets (RM100) | −100 | −97 | −100 | −100 / −88 / −100 |
| Star, System 8 × 1 (RM280) | −280 | −250 | −280 | −280 / −250 / −280 |
| Power, 10 sets (RM100) | −100 | −82 | −100 | −100 / −92 / −100 |
| Power, System 8 × 1 (RM280) | −250 | −259 | −250 | −265 / −268 / −265 |
| Supreme, 10 sets (RM200) | −200 | −146 | −200 | −200 / −190 / −200 |
| Supreme, System 8 × 1 (RM560) | −480 | −504 | −480 | −560 / −532 / −560 |

The System 7 × 2 formats look the same. With the combined score (margin + winning draws), the top 10 chosen beforehand averaged −RM109 in Star, −RM122 in Power and −RM193 in Supreme. The shifted-calendar medians were −116, −122 and −230. As in Magnum Life, the leaders by earlier profit are past jackpot winners, and they then lose.

**2. Whole-history test of 5- and 6-number hits, real calendar vs 20 shifted calendars**

| Game | Real calendar's rank of 21 for 5+ hits (four formats) | Rank for 6-number hits | All leads together, z |
|---|---|---|---|
| **Star Toto 6/50** | **1, 1, 1, 1** (+11–16% more than shifted) | 6–9 (normal) | **+3.7** |
| Power Toto 6/55 | 10–16 (normal) | 14–21 (low) | −0.7 |
| Supreme Toto 6/58 | 6–17 (normal) | 1–20 (mixed) | −0.4 |
| Magnum Life, for comparison (6+ / 7+) | 2–6 / 3–4 | – | +1.4 |

**3. Which astrological parameters carry the excess**

| | Star Toto (5+) | Magnum Life (6+) |
|---|---|---|
| Most excess | solar term (+4.8), lagna nakshatra (+4.8), adhika masa (+3.6), aspect Venus–Saturn, Mercury and Venus retrograde, KP Sun / ascendant star lords, ritu | Moon navamsa (+3.7), year yin-yang (+3.6), nakshatra pada (+3.4), aspect Moon–Venus, nine-star year / month |
| Least excess | day-based ones: day vs year branch, day of month, day officer, day stem, day pillar | karana, day branch, tropical Sun sign |

- **No shared winner:** no parameter is strong in all four games. For example, aspect Moon–Venus is +3.1 in Magnum Life but only +0.6 in Star Toto.
- **Star Toto:** the excess comes from slow, seasonal and planetary-period parameters, not from day-of-week ones.
- **Power and Supreme:** their strongest parameters (hora lord +4.5 in Power, KP Sun number +4.0 in Supreme) sit inside totals that are no better than chance.

**4. Per-lead top 10 by 5+ hits against their own shifted calendars:** the top 10 got 0 hits of 5+ on the last 10 draws in Star and Supreme, and 1 in Power. Ten average leads would expect about 0.04–0.2, so 10 draws can't tell them apart from any other leads. The top leads in each game are as common on the shifted calendars as on the real one:

| Game | Top lead | Earlier 5+ hits | Leads with that many, real calendar | Shifted calendars |
|---|---|---|---|---|
| Star | Saturn retrograde × nayin (hot) | 10 | 3 | 0–6 |
| Power | Year pillar × Part of Fortune sign (pos) | 11 | 2 | 0–3 |
| Supreme | Nakshatra × tropical Sun sign (hot+100) | 12 | 1 | 0–2 |

**How astrology acts in Toto compared with Magnum Life:**
- **Shared:** in every game and format, nothing chosen in advance makes money, and big wins go to leads that look ordinary beforehand.
- **Star Toto is the exception:** across all leads together it gets about 13% more 5-number hits on the real calendar than on any of the 20 shifted ones, driven by seasonal and planetary-period parameters. Magnum Life has a weaker version of the same tilt.
- **Power and Supreme show nothing:** these are the two games with the longest histories, back to 2009/2010.
- **No forward evidence:** the extra 5-number hits didn't continue into the last 10 Star Toto draws (28 against a shifted mean of 29). A 13% tilt on 5-number hits also adds only about 1–2% to the return, which with jackpots at their minimum is about 35% in Star Toto, so it is far from profitable.

Ranking 1st of 21 only means the chance of luck is under about 5%. To pin that down, a 100-calendar test for Star Toto is now running (about 35 minutes). It also splits the history into halves to see whether the tilt is steady or comes from one period. I'll report the result when it finishes.

Results are in `analysis/TOTO_SYSTEM_PROFIT.md`, `TOTO_COMBINED.md`, `TOTO_HIGH_HITS_NULL.md`, `TOTO_LEAD_HIGH_HITS.md` and `PARAM_EXCESS.md`, with a summary added to FINDINGS.md. Everything is pushed to `claude/focused-franklin-ajsdm9`.

**Answer:**

With 100 shifted calendars, Star Toto's astrological tilt is weaker than the 20-calendar test made it look. It is borderline at best, and it doesn't hold steady over time.

**5-number hits across all leads: real calendar vs 100 shifted calendars**

| Format | Whole history | First half | Second half | Last 10 draws |
|---|---|---|---|---|
| 10 sets | rank 9/101, p = 0.08 | p = 0.40 | p = 0.03 | p = 0.39 |
| System 7 × 2 overlap | rank 7/101, p = 0.06 | p = 0.22 | p = 0.02 | p = 0.40 |
| System 7 × 2 disjoint | rank 8/101, p = 0.07 | p = 0.40 | p = 0.05 | p = 0.32 |
| System 8 × 1 | rank 3/101, p = 0.02 | p = 0.20 | p = 0.04 | p = 0.59 |

*p* is the share of shifted calendars that did at least as well as the real one.

- **Not as unusual as it looked:** with 20 shifted calendars the real one ranked 1st every time. With 100, the real calendar ranks 3rd–9th. A few shifted calendars do better: the best reach 3,590 hits in 10 sets against the real 3,356. So the earlier z of +3.7 overstated it; the realistic chance of luck is about 2–8%.
- **It comes and goes:**
  - First half of the history, roughly 2018–2022: no excess, p = 0.20–0.40.
  - Second half, roughly 2022–Sep 2026: an excess, p = 0.02–0.05.
  - Last 10 draws: nothing (28 hits against a shifted average of 28 in 10 sets).

  An effect that switches on and off like this looks more like noise than a stable pattern.
- **A long search makes it weaker still:** this analysis tested four games, several formats and two hit levels, and searched thousands of leads before that. Finding one game with p ≈ 0.02–0.08 is roughly what chance alone would produce.

**Final comparison: Magnum Life vs Toto**

| | Magnum Life | Star Toto | Power Toto | Supreme Toto |
|---|---|---|---|---|
| Real calendar's tilt on high hits (whole history) | slight (6+ / 7+ rank 2–6 of 21) | borderline (5+ p ≈ 0.02–0.08 of 100), second half only | none | none |
| Parameters carrying it | Moon navamsa, year yin-yang, nakshatra pada | solar term, lagna nakshatra, adhika masa, retrogrades | – | – |
| Same parameters across games? | no | no | – | – |
| Any lead or method profitable when chosen in advance? | no | no | no | no |
| Big wins on the last 10 draws | Grand by an ordinary lead (rank 12,375) | 5-number hits only | 2 jackpots by ordinary leads (rank 15–20k) | 5-number cluster on one draw |

Astrology behaves the same in all four games. It never picks winners in advance, and the occasional tilt in hit counts is small and switches on and off. It also points to different parameters in each game, which is the opposite of what a real astrological influence would do.

The only fair way to settle Star Toto's second-half tilt is to watch future draws. I could freeze the current list and re-test it after the next 50–100 Star Toto draws.

The 100-calendar results are in `analysis/TOTO_NULL100_TOTO50.md`, with FINDINGS.md updated. Everything is pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Ok now so far list out all the leads separated by each lotto which needs to be observed

**Answer:**

I'll pull the Toto candidates from the saved results so the watchlist covers all four games on the same footing.

**Answer:**

Here is the watchlist for each game. None of these leads has beaten chance on draws it hadn't already seen, so treat the list as leads to observe, not to bet on. ★ marks the leads with the strongest case: a big win on the last 10 draws and a good record before them.

## Magnum Life 8/36

| | Lead | Pattern | Last 10 draws | Best format | Earlier record |
|---|---|---|---|---|---|
| ★ | Mercury nakshatra × Saturn combust | cold | 7 numbers on 4 Oct (+RM19,910) | System 10 | rank 202, **return 293%** (one 7 + bonus in 2022) |
| ★ | Day pillar × aspect Jupiter–Saturn | pos | 7 numbers on 3 Oct in 3 formats | System 10 (+RM19,960) | rank 1,236, return 67% |
| | Paksha × Venus rashi | cold | **All 8 (Grand) on 26 Sep** | 10 tickets / System 10 | rank 12,375, return 19% |
| | Ayana × lunar leap month | hot+100 | 7 + bonus (RM110,200) on 7 Oct | System 9 × 2 disjoint | rank 1,649, return 45% |
| | Aspect Venus–Jupiter × universal day | hot | 7 + bonus (RM110,240) on 30 Sep | System 9 × 2 overlap | rank 4,750, return 27% |
| | Saturn combust × plum trigrams | cold | 7 numbers in all 4 formats on 3 Oct | System 10 | rank 11,000+, return 16–20% |
| | Part of Fortune rashi × aspect Venus–Jupiter | cold | quiet | System 9 × 2 overlap | two 7-number draws in 2024, return 177% |
| | KP Sun sub-lord × year yin-yang | hot / pos | won on 4 of 10 draws | System 10 (+RM540) | rank ~5,000–11,000 |
| | Ayana × KP Moon star-lord | pos | won on 4 of 10 draws | System 9 × 2 overlap (+RM300) | rank ~2,300–9,000 |

## Star Toto 6/50

This is the one game where all leads together beat the shifted calendars on 5-number hits (p ≈ 0.02–0.08, second half of the history only). The tilt is carried by solar term, lagna nakshatra, adhika masa, retrogrades and KP star lords.

| | Lead | Pattern | Last 10 draws | Best format | Earlier record |
|---|---|---|---|---|---|
| ★ | Hour stem (19h) × tropical Sun sign | pos / hot | **5 + bonus, Jackpot 2 (RM100,000)** | System 8 × 1 (+RM111,936) | rank 720, return 55% |
| ★ | Hora lord × Mars retrograde | cold | 5 numbers on 7 Oct | 10 sets (+RM8,100) | rank 843, return 56% |
| ★ | Hora lord × adhika masa | cold | 5 numbers on 7 Oct | 10 sets (+RM6,100) | rank 1,101, return 55% |
| | Rahu nakshatra × KP ascendant sub-lord | hot | 4 + bonus, 3 winning draws | System 8 × 1 (+RM6,404) | rank 1,098, return 48% |
| | Sun rashi × planets with Moon | cold | won on 4 of 10 draws | System 8 × 1 (+RM6,544) | rank 6,236, return 28% |
| | Lagna rashi × day officer | cold | 5 numbers, won on 4 of 10 draws | System 7 × 2 disjoint (+RM4,112) | return 20–23% |
| | Saturn retrograde × nayin | hot | no 5+ | — | most 5+ hits against its own shifted calendars (10 vs 0.2) |
| | Karana × masa | cold | about break-even | System 8 × 1 | 9 hits of 5+, vs 0.4 on its shifted calendars |

## Power Toto 6/55

No calendar effect over the whole history.

| | Lead | Pattern | Last 10 draws | Best format | Earlier record |
|---|---|---|---|---|---|
| ★ | Lunar month × tropical Sun sign | hot+100 | **Jackpot** (System 8) | System 8 × 1 (+RM3.04m) | rank 2,142, return 24% (best of the jackpot leads) |
| ★ | Tropical Sun sign × aspect Moon–Saturn | hot+100 | **Jackpot on 11 Oct** | 10 sets / System 8 | rank 3,293, return 23% |
| | Masa × day god | hot | **Jackpot on 27 Sep**, every format | all (+RM3.02m) | rank 20,004, return 5% |
| | Masa × adhika masa | hot+100 | Jackpot (System play) | System 7 / 8 | rank 16,700+, return 5% |
| | Month branch × aspect Venus–Jupiter | hot+100 | Jackpot (System 8) | System 8 × 1 | rank 16,282, return 6% |
| | Lagna rashi × Saturn retrograde | hot+100 | profit in 3 formats (+RM6,672) | System 7 × 2 overlap | 10 hits of 5+ against its own shifted calendars (z +9.6) |
| | KP Sun star-lord × month pillar | hot+100 | won on 4 of 10 draws | 10 sets (+RM139) | win rate 3.1% |

## Supreme Toto 6/58

No calendar effect for 5-number hits over the whole history.

| | Lead | Pattern | Last 10 draws | Best format | Earlier record |
|---|---|---|---|---|---|
| ★ | Moon rashi × hard aspects | cold | 5 numbers, 2 winning draws | System 8 × 1 (+RM21,464) | **rank 106, return 44%**, the best record in Supreme |
| ★ | KP Sun star-lord × day stem | hot | 5 numbers, 2 winning draws | System 7 × 2 disjoint (+RM14,168) | rank 1,473, return 30% |
| | Nakshatra × nayin (and its cluster) | hot+100 | 5 numbers on 11 Oct | 10 sets (+RM27,856) | rank 8,000–26,000, return 4–7% |
| | KP Moon number × nayin element | hot+100 | 5 numbers, 3 winning draws | System 7 × 2 overlap (+RM14,024) | top of the combined ranking |
| | Nakshatra × tropical Sun sign | hot+100 | no 5+ | — | most 5+ hits against its own shifted calendars (12, z +11.3) |

The nakshatra × nayin cluster covers Nakshatra, Nakshatra pada and KP Moon number, each paired with nayin or day pillar. They all picked the same numbers on 11 Oct, so they count as one hit.

**What would make this a fair test:**
- **Freeze the list now:** no changes later, since that would be hindsight again.
- **Log each lead's numbers before every draw:** Magnum Life and Star Toto have about 3 draws a week.
- **Re-check after 50–100 draws per game:** only a lead that keeps winning bigger prizes, more often than random tickets and the shifted calendars, would count as real.

I can set up that logging, working out every watched lead's numbers for the next draw of each game, if you'd like.

Everything is in `analysis/WATCHLIST.md`, now covering all four games, pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Ok now update the result for today and tell me how the leads perform. You can also use 4dmoon.com for the latest result

**Answer:**

The 17 Oct results are on 4dmoon.com. The 18 Oct page is still empty, so today's draw hasn't been published yet. I'm checking our data against 17 Oct.

**Answer:**

Our data already matches 4dmoon for 17 Oct. Today's draw (Sun 18 Oct) was due at about 7 pm Malaysia time; it's now about 8:20 pm there, so I'm checking again.

---

**User:**

> [Request interrupted by user]

---

**User:**

> Ok now update the result for today and tell me how the leads perform. You can also use 4dmoon.com for the latest result. All the loto results are already out in that website

**Answer:**

4dmoon's past-results page doesn't have 18 Oct yet. The homepage shows today's numbers through live JavaScript, so I'll render it in a browser to read them.

---

**User:**

> [Request interrupted by user]

---

**User:**

> Ok now update the result for today and tell me how the leads perform. You can also use 4dmoon.com for the latest result. All the loto results are already out in that website. Just search www.4dmoon.com that’s the latest result which is 18 Oct

**Answer:**

I have the Magnum Life main numbers for 18 Oct. Running it again to get the bonus numbers and the three Toto games.

**Answer:**

The second run split the numbers into single digits, so I'm asking once more for them as text, to remove any ambiguity.

**Answer:**

Across the 33 watched lead-and-format bets on today's draws, only one paid anything: Ayana × lunar leap month (hot+100) in Magnum Life won RM230 for a +RM212 profit. Every other lead missed, and no lead in any of the three Toto games won a prize.

This is the first draw after the watchlist was frozen. Each lead's numbers use only draws up to 17 Oct, so this is a genuine forward test. I added today's results to the data, taking them from 4dmoon.com.

**Today's results, Sunday 18 Oct 2026:**

| Game | Winning numbers | Bonus |
|---|---|---|
| Magnum Life | 09 10 19 20 21 22 33 35 | 06 18 |
| Star Toto 6/50 | 09 10 15 17 32 45 | 29 |
| Power Toto 6/55 | 10 18 25 31 46 47 | – |
| Supreme Toto 6/58 | 10 13 17 44 46 54 | – |

**Magnum Life:**

| Lead | Format | Best match | Payout | Profit |
|---|---|---|---|---|
| **Ayana × lunar leap month (hot+100)** | System 9 × 2 disjoint | **5 + 2 bonus** | **RM230** | **+RM212** |
| Saturn combust × plum trigrams (cold) | System 10 | 4 | 0 | −45 |
| Mercury nakshatra × Saturn combust (cold) ★ | System 10 / 10 tickets | 3 | 0 | −45 / −10 |
| Paksha × Venus rashi (cold), the Grand winner | 10 tickets / System 10 | 3 + 1 bonus | 0 | −10 / −45 |
| Mars rashi × month (cold) | System 10 | 3 | 0 | −45 |
| Aspect Venus–Jupiter × universal day (hot) | System 9 × 2 overlap | 3 | 0 | −18 |
| KP Sun sub-lord × year yin-yang (hot) | System 10 | 2 + 2 bonus | 0 | −45 |
| Day pillar × aspect Jupiter–Saturn (pos) ★ | System 10 | 1 + 1 bonus | 0 | −45 |
| Part of Fortune rashi × aspect Venus–Jupiter (cold) | System 9 × 2 overlap | 1 + 1 bonus | 0 | −18 |
| Ayana × KP Moon star-lord (pos) | System 9 × 2 overlap | 1 + 1 bonus | 0 | −18 |

- **The one winner:** Ayana × lunar leap month's second set was 06 09 12 18 19 21 27 33 35. That set holds 5 winning numbers and both bonus balls, which pays several 6th and 8th prizes. This is the same lead that won 7 + bonus (RM110,200) on 7 Oct.
- **Close but unpaid:** Saturn combust × plum trigrams had 4 winning numbers in its System 10 but no bonus ball, so it paid nothing.

**Star Toto 6/50:** no prizes, with at most 2 numbers or 2 + bonus; total −RM156. Lagna rashi × day officer was closest with 2 + bonus, and Hour stem (19h) × tropical Sun sign, the Jackpot 2 lead, caught only 1.

**Power Toto 6/55:** no prizes, at most 2 numbers; total −RM156. The two leads that had hit the jackpot caught 2 (Tropical Sun sign × aspect Moon–Saturn) and 1 (Masa × day god).

**Supreme Toto 6/58:** no prizes, at most 2 numbers (Nakshatra × nayin); total −RM152. Moon rashi × hard aspects ★ caught 0.

**Running total after 1 draw:**

| Game | Staked | Won | Profit |
|---|---|---|---|
| Magnum Life | RM362 | RM230 | −RM132 |
| Star Toto | RM156 | 0 | −RM156 |
| Power Toto | RM156 | 0 | −RM156 |
| Supreme Toto | RM152 | 0 | −RM152 |

That is ordinary for a single draw: random entries lose about 45–80% of the stake on average. One draw says nothing yet about whether these leads are real.

To keep the test running, send me "update results" after each draw (Wed, Sat, Sun and occasional Tuesdays). I'll fetch the numbers from 4dmoon.com, score every lead again and extend the running totals.

Sources:
- [4dmoon.com – latest results (18 Oct 2026)](https://www.4dmoon.com/)
- [4dmoon.com – past results 17 Oct 2026](https://www.4dmoon.com/past-results/2026-10-17)

The draw-by-draw scores and running totals are in `analysis/WATCH_LOG.md`, with every bet in `analysis/watch_log.csv`. Everything is pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> For all the toto loto, list out the leads and each their performance for today

**Answer:**

None of the 21 Toto lead-and-format bets won a prize today (18 Oct), so every one lost its full stake. The best match in any single set was 2 numbers (2 + bonus in Star), and you need 3 numbers for the smallest prize.

**Star Toto 6/50: winning numbers 09 10 15 17 32 45, bonus 29**

| Lead | Pattern | Format (stake) | Numbers played | Winning numbers caught | Best in one set | Profit |
|---|---|---|---|---|---|---|
| Lagna rashi × day officer | cold | System 7 × 2 disjoint (RM14) | 06 09 10 13 29 47 50 / 02 05 20 26 28 31 39 | 09, 10 + bonus 29 | **2 + bonus** | −RM14 |
| Sun rashi × planets with Moon | cold | System 8 (RM28) | 05 07 09 10 13 27 33 34 | 09, 10 | 2 | −RM28 |
| Saturn retrograde × nayin | hot | 10 sets (RM10) | built around 03 08 12 15 23 32 | 15, 32 | 2 | −RM10 |
| Karana × masa | cold | System 8 (RM28) | 05 06 15 21 29 31 37 48 | 15 + bonus 29 | 1 + bonus | −RM28 |
| Hour stem (19h) × tropical Sun sign | pos | System 8 (RM28) | 08 09 19 35 36 38 43 50 | 09 | 1 | −RM28 |
| Hora lord × Mars retrograde | cold | 10 sets (RM10) | built around 10 13 33 40 47 50 | 10 | 1 | −RM10 |
| Hora lord × adhika masa | cold | 10 sets (RM10) | built around 10 13 33 40 47 50 | 10 | 1 | −RM10 |
| Rahu nakshatra × KP ascendant sub-lord | hot | System 8 (RM28) | 03 11 12 15 16 21 22 35 | 15 | 1 | −RM28 |

Star total: RM156 staked, nothing won.

**Power Toto 6/55: winning numbers 10 18 25 31 46 47**

| Lead | Pattern | Format (stake) | Numbers played | Winning numbers caught | Best in one set | Profit |
|---|---|---|---|---|---|---|
| Tropical Sun sign × aspect Moon–Saturn | hot+100 | 10 sets (RM10) | built around 11 14 26 28 31 54 | 31, 46 | 2 | −RM10 |
| Tropical Sun sign × aspect Moon–Saturn | hot+100 | System 8 (RM28) | 04 11 14 26 28 31 46 54 | 31, 46 | 2 | −RM28 |
| Lunar month × tropical Sun sign | hot+100 | System 8 (RM28) | 11 14 26 28 31 37 46 54 | 31, 46 | 2 | −RM28 |
| Masa × day god | hot | 10 sets (RM10) | built around 01 11 31 37 41 54 | 31 | 1 | −RM10 |
| Masa × adhika masa | hot+100 | System 8 (RM28) | 01 11 14 26 28 31 37 54 | 31 | 1 | −RM28 |
| Month branch × aspect Venus–Jupiter | hot+100 | System 8 (RM28) | 04 11 14 26 28 31 37 54 | 31 | 1 | −RM28 |
| Lagna rashi × Saturn retrograde | hot+100 | System 7 × 2 overlap (RM14) | 14 28 32 33 47 48 52 / 13 28 33 48 49 52 55 | 47 | 1 | −RM14 |
| KP Sun star-lord × month pillar | hot+100 | 10 sets (RM10) | built around 07 11 26 28 31 44 | 31 | 1 | −RM10 |

Power total: RM156 staked, nothing won. Most Power leads shared the same core numbers (11 14 26 28 31 54). They caught 31, and some caught 46, but missed the rest.

**Supreme Toto 6/58: winning numbers 10 13 17 44 46 54**

| Lead | Pattern | Format (stake) | Numbers played | Winning numbers caught | Best in one set | Profit |
|---|---|---|---|---|---|---|
| Nakshatra × nayin | hot+100 | 10 sets (RM20) | built around 17 26 27 43 50 54 | 17, 54 | 2 | −RM20 |
| KP Sun star-lord × day stem | hot | System 7 × 2 disjoint (RM28) | 13 16 19 33 50 53 58 / 14 18 23 32 38 42 44 | 13, 44 (in different sets) | 1 | −RM28 |
| KP Moon number × nayin element | hot+100 | System 7 × 2 overlap (RM28) | 08 10 15 34 48 53 58 / 08 12 15 16 40 48 53 | 10 | 1 | −RM28 |
| Moon rashi × hard aspects | cold | System 8 (RM56) | 09 21 29 30 33 34 42 49 | none | 0 | −RM56 |
| Nakshatra × tropical Sun sign | hot+100 | 10 sets (RM20) | built around 15 27 34 38 41 55 | none | 0 | −RM20 |

Supreme total: RM152 staked, nothing won.

All 21 bets missed, which is normal for one draw. A set of 6 numbers wins something only about 1–2% of the time, so even 10 random sets usually come up empty. One draw is far too few to judge any lead.

The full number sets for every lead are in `analysis/watch_log.csv`, with the summary in `analysis/WATCH_LOG.md`.

---

**User:**

> From what I saw for lotto there is not cold+100? Why didn’t does analysis for all the single and pair parameter was not tested? While for Magnum live hot+100 and cold+100 was not tested?

**Answer:**

You're right that there's no cold+100, but that's true for every game. Both Magnum Life and the three Toto games tested the same four patterns on every single parameter and every pair. hot+100 *was* tested in Magnum Life. For example, Ayana × lunar leap month (hot+100), today's only winner, is a Magnum Life lead.

**The four patterns used everywhere:**

| Pattern | How each lead ranks the numbers, using only earlier draws |
|---|---|
| hot | most drawn in that astrological cell (draws with the same parameter value or pair) |
| cold | least drawn in that cell |
| pos | most often drawn in each ticket position within that cell |
| hot+100 | hot in the cell **plus** hot over the last 100 draws of all draws (cell and recent trend both hot) |

Every one of the 26,224 leads in every game is an astrological single or pair crossed with one of these four patterns: 114 singles, 6,441 pairs and the no-astrology baseline, each × 4. So all singles and pairs were tested in Toto and in Magnum Life alike. The only difference between the games is the ticket format (8 numbers vs 6, System 9/10 vs System 7/8).

**Why there's no cold+100:** when I built the patterns I added only one blend with the recent trend, hot+100, and never added the mirror image. There was no reason to leave it out; the set simply wasn't complete. The natural variants would be:

| Missing pattern | Meaning |
|---|---|
| cold+100 | cold in the cell **and** cold over the last 100 draws |
| hot cell + cold 100 | hot in the cell, but overdue recently |
| cold cell + hot 100 | cold in the cell, but hot recently |

That gives 7 patterns instead of 4, about 46,000 leads per game instead of 26,224.

**What it would take:** add these three patterns and rerun the main analyses for all four games. That means the profit tables, System play, re-ranking before every draw, the combined ranking and the 20-shifted-calendar test. On this machine that's roughly 2–3 hours. I'd then report whether any cold+100 or mixed lead stands out, add any good ones to the watchlist, and include them when scoring future draws.

One caution: adding 75% more leads also adds 75% more chances of lucky hindsight winners. Any new lead would face the same tests as before (earlier draws vs the last 10, shifted calendars) before going on the watchlist.

Do you want me to go ahead with all three new patterns for all four games?

---

**User:**

> Yes go ahead for all toto loto and also the magnum live. And test for last 10 draws to see how they perform, remember to always update the history for each draw before testing the next. And once that is all done, try for the latest result from today. And tell me which new leads arrive for magnum live, and all other sports toto

**Answer:**

I'll add the three new patterns (cold+100, hot-cell + cold-100, cold-cell + hot-100) and rerun every analysis on all four games with 7 patterns. That covers 45,892 leads per game: profit in four formats, re-ranking before each draw, the combined ranking, 20 shifted calendars and per-lead tests. The history is cut at 17 Oct so the last 10 draws (26 Sep–17 Oct) are tested walk-forward, then today's 18 Oct draw is scored separately as a true forward test. Writing one pipeline that handles Magnum Life and Toto together.

**Answer:**

The run may take longer than the 2-hour limit on background jobs, so I'm relaunching it as a detached process that can't be cut off.

**Answer:**

While the main run works, I'm preparing the next step. One script scores all 45,892 leads on today's draw (18 Oct), and the watchlist scorer gets the three new patterns.

**Answer:**

Progress so far:

- **Main run:** the 7-pattern analysis is running detached on all four games. History is cut at 17 Oct, so the last 10 draws (26 Sep–17 Oct) are tested walk-forward, with the history updated before each draw.
- **Scripts ready:** the next-step scripts are committed and pushed to `claude/focused-franklin-ajsdm9`. `lead_today.py` scores all 45,892 leads on today's 18 Oct draw, and `watch_score.py` now handles the new patterns.

When the main run finishes I'll score today's draw and report which new leads appear for Magnum Life and each Toto game.

**Answer:**

Done in about 70 minutes. Starting today's 18 Oct scoring of all leads in the background while I read the results.

**Answer:**

While today's scoring runs, I'm adding the most notable new-pattern leads to the watchlist scorer so they get scored on 18 Oct as well.

**Answer:**

I've added 16 new-pattern leads to the scorer (5 for Magnum Life, 5 for Star Toto, 2 for Power Toto and 4 for Supreme Toto), so they'll be scored on 18 Oct alongside the existing watchlist. The scoring of all 45,892 leads on today's draw is still running; once it finishes I'll put together the report for Magnum Life and each Toto game.

**Answer:**

I've committed and pushed the 7-pattern results (history up to 17 Oct) and the updated watchlist scorer to `claude/focused-franklin-ajsdm9`. The scoring of all leads on today's 18 Oct draw is still running; when it finishes I'll report the new leads for Magnum Life and each Toto game and how they did today.

**Answer:**

I re-ran every analysis with 7 patterns for Magnum Life and all three Toto games. Each game now has 45,892 leads: every single parameter and pair × hot, cold, pos, hot+100, cold+100, hot-cell + cold-100, and cold-cell + hot-100. History was cut at 17 Oct, so the last 10 draws (26 Sep–17 Oct) were tested walk-forward, with the history updated before each draw. Today's 18 Oct draw was then scored as a separate forward test.

**The three new patterns:** the clearest result is that leads chosen in advance still lose about the whole stake, in every game and format, with the new patterns included.

**Each pattern on its own:** this compares high hits (7+ in Magnum Life, 5+ in Toto) over the whole history, real calendar vs 20 shifted calendars. Each cell shows the rank of 21 and the z-score.

| Pattern | Magnum Life | Star Toto | Power Toto | Supreme Toto |
|---|---|---|---|---|
| hot | 8, +0.4 | **1, +4.2** | 10, +0.2 | 21, −2.0 |
| cold | 3, +1.3 | 7, +0.3 | 16, −0.7 | 3, +0.9 |
| pos | 8, +0.7 | **1, +2.7** | 12, 0.0 | 16, −0.7 |
| hot+100 | 5, +1.1 | 13, −0.5 | 18, −0.8 | 2, +1.9 |
| **cold+100 (new)** | 16, −0.7 | 7, +0.7 | 15, −0.8 | 2, +1.6 |
| **hot-cell + cold-100 (new)** | **1, +2.2** | 6, +0.6 | 16, −0.9 | 19, −1.3 |
| **cold-cell + hot-100 (new)** | 11, −0.3 | **1, +2.3** | 3, +1.4 | 8, 0.0 |

No pattern is strong in more than one or two games. The best new one is hot-cell + cold-100 in Magnum Life (rank 1 of 21, z +2.2), but the same pattern ranks 19th in Supreme. Shifted calendars produce strong-looking patterns about as often.

**Chosen in advance and played on the last 10 draws (top 10 by earlier profit, average):**

| Game, format | Real calendar | Shifted calendars (median) |
|---|---|---|
| Magnum Life System 10 (stake RM450) | −RM304 | −RM385 |
| Star Toto System 7 × 2 disjoint (RM140) | **+RM318** | −RM119 |
| Power Toto 10 sets (RM100) | −RM83 | −RM92 |
| Supreme Toto System 7 × 2 overlap (RM280) | −RM243 | −RM270 |

The only positive average is Star Toto System 7 disjoint, and it comes from one lead: Day of month × aspect Venus–Jupiter (hot-cell + cold-100), which caught 5 numbers for +RM4,016. Everything else lost about the stake, same as the shifted calendars.

## New leads that appear

**Magnum Life**

| Lead | Pattern | Why it stands out | Today (18 Oct) |
|---|---|---|---|
| **Mercury rashi × KP ascendant sub-lord** | cold+100 | earlier return **286%** (System 10, rank 994); profit in three formats on the last 10 (+RM4,580 System 10) | 1 number, −RM45 |
| Mars retrograde × Moon phase | hot-cell + cold-100 | won on 4 of the last 10 draws | 1, −RM18 |
| Mercury rashi × day branch | cold+100 | won on 4 of the last 10 draws | 1, −RM18 |
| Month stem × KP ruling planets | hot-cell + cold-100 | won on 4 of the last 10 draws | 1, −RM18 |
| Aspect Moon–Mars × aspect Mercury–Mars | cold+100 | most 7+ hits against its own shifted calendars (z +8.8) | 1, −RM45 |

**Star Toto 6/50**

| Lead | Pattern | Why it stands out | Today |
|---|---|---|---|
| Hora lord × Mars combust | cold-cell + hot-100 | 5 numbers on 7 Oct (+RM8,100) | **3 numbers, RM8 prize**, −RM2 |
| Saturn retrograde × aspect Mercury–Jupiter | cold-cell + hot-100 | earlier return 55% (rank 1,172), +RM4,048 | 2, −RM14 |
| Aspect Sun–Mars × aspect Moon–Venus | hot-cell + cold-100 | earlier return 45%, +RM4,078 | 1, −RM14 |
| Day of month × aspect Venus–Jupiter | hot-cell + cold-100 | top by earlier profit, and +RM4,016 on the last 10 | bonus only, −RM14 |
| Mars combust × aspect Moon–Mercury | hot-cell + cold-100 | most 5+ hits against its own shifted calendars (z +11.9) | 1, −RM10 |

**Power Toto 6/55**

| Lead | Pattern | Why it stands out | Today |
|---|---|---|---|
| Mercury nakshatra × soft aspects | cold-cell + hot-100 | 5 numbers, +RM6,672 | 1, −RM14 |
| Mars combust × aspect Jupiter–Saturn | cold-cell + hot-100 | 9 hits of 5+ against its own shifted calendars (z +8.6) | 1, −RM10 |

**Supreme Toto 6/58**

| Lead | Pattern | Why it stands out | Today |
|---|---|---|---|
| Saturn rashi × KP ascendant star-lord | cold+100 | 5 numbers, +RM13,928; earlier return 29% | 1, −RM28 |
| KP ascendant star-lord × year pillar | hot-cell + cold-100 | #1 by earlier profit; −RM8 on the last 10 | 1, −RM28 |
| Lagna rashi × lunar day | hot-cell + cold-100 | 5 numbers, +RM21,384 | 2, −RM56 |
| Sun nakshatra × lunar month | cold-cell + hot-100 | 5 numbers, +RM13,928 | 0, −RM28 |

## Today's draw for all 45,892 leads

| Game | Leads that won any prize | Best result today |
|---|---|---|
| Magnum Life | 8.6–9.6% | **7 + bonus (RM121,730)** in System 10, mostly **cold-cell + hot-100** leads |
| Star Toto | 2.5–3.6% | 5 numbers: KP ascendant star-lord × aspect Moon–Mars (cold), RM6,524 in System 8 |
| Power Toto | 2.3–3.3% | 5 numbers in System 7, e.g. Mercury rashi × day-vs-year branch (hot-cell + cold-100), RM6,812 |
| Supreme Toto | 1.8–3.6% | 5 numbers: **Jupiter nakshatra × aspect Moon–Mercury (hot-cell + cold-100)**, in all four formats, RM21,944 in System 8 |

**Magnum Life:**
- **The biggest winners were new-pattern leads.** Six cold-cell + hot-100 leads hit 7 + bonus in System 10: Nakshatra alone and paired with nakshatra lord, KP Moon star-lord, lunar leap month, Saturn nakshatra × aspect Moon–Venus, and weekday × aspect Venus–Jupiter.
- **System 9 disjoint winners:** two more new-pattern leads hit 7 + bonus (RM110,200), plus Mars rashi × month branch (hot+100).
- **Likely one shared pick:** most of these are the Nakshatra family landing on the same numbers, and none was on the list chosen before the draw.
- **The pre-chosen leads won almost nothing:** the best was Mars nakshatra × aspect Sun–Jupiter (cold+100) with 4 + bonus in System 9 disjoint (+RM2).

**On the watchlist today:**
- **Ayana × lunar leap month (hot+100)** is still the only profitable watched lead (+RM212).
- **Hora lord × Mars combust** (cold-cell + hot-100, Star Toto) won the smallest prize, RM8.
- All other watched leads, old and new, lost their stake.

**Conclusion:** the new patterns behave like the old ones. They produce many hindsight winners (they dominated today's biggest Magnum Life hits), but the ones chosen beforehand don't win more than chance. I've added the 16 new-pattern leads above to the watchlist, and they'll be scored on every future draw alongside the original leads. Send me "update results" after the next draw.

Results are in `analysis/LEADS7_*.md` and `analysis/LEADS7_TODAY_2026-10-18.md`, with the watchlist in `analysis/WATCHLIST.md` and the running log in `analysis/WATCH_LOG.md`. Everything is pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Ok don’t forget to update results. Anyways for the best result today, check and see how it performed for the previous days for each and every of those leads

**Answer:**

I'll look up each of today's biggest winners from all four games in the 7-pattern results. For each one I'll show how it did on the last 10 draws, its profit, win rate and high hits over the earlier history, and the same lead on the shifted calendars.

**Answer:**

None of today's biggest winners had a good record before 18 Oct. All of them lost money on the previous 10 draws, and almost all had earlier returns below what random tickets get. I checked each of the 15 biggest payouts in every game.

**What "before today" means:** history up to 17 Oct, with numbers built only from earlier draws. "Earlier" covers about 1,000 draws for Magnum Life and Star, and about 2,100 for Power and Supreme. Random entries return about 55% (Magnum Life), 35% (Star) and 20% (Power and Supreme).

## Magnum Life: today 7 + bonus (RM110,200–121,730) and 7 (RM20,310)

| Lead | Pattern | Format | Earlier rank / return | Earlier 7+ hits | Last 10 draws: profit, best per draw |
|---|---|---|---|---|---|
| Nakshatra (and × nakshatra lord, × KP Moon star-lord) | cold-cell + hot-100 | System 10 | 12,604–14,085 / 25–26% | 0 | −450, at most 3 + bonus |
| Nakshatra × lunar leap month | cold-cell + hot-100 | System 10 | 26,663 / 19% | 0 | −450, at most 3 + bonus |
| Saturn nakshatra × aspect Moon–Venus | cold-cell + hot-100 | System 10 | 15,196 / 24% | 0 | −450, at most 3 + bonus |
| Weekday × aspect Venus–Jupiter | cold-cell + hot-100 | System 10 | 15,537 / 24% | 0 | −400, at most 4 + bonus |
| **Mercury combust × soft aspects** | cold-cell + hot-100 | System 9 disjoint | **1,157 / 94%** | **1** | −180, at most 3 + bonus |
| Aspect Sun–Moon × aspect Sun–Venus | cold-cell + hot-100 | System 9 disjoint | 37,362 / 16% | 0 | −180, at most 4 |
| Mars rashi × month branch | hot+100 | System 9 disjoint | 33,295 / 17% | 0 | −140, at most 4 + bonus |
| 6 leads with 7 numbers (Venus combust, Venus retrograde, tropical Moon sign …) | cold-cell + hot-100 | System 10 | 17,405–30,069 / 18–23% | 0 | −350 to −450 |

## Star Toto 6/50: today 5 numbers (RM4,156–6,524) and 4 + bonus

| Lead | Pattern | Format | Earlier rank / return | Earlier 5+ hits | Last 10: profit, best per draw |
|---|---|---|---|---|---|
| KP ascendant star-lord × aspect Moon–Mars | cold | System 8 / System 7 × 2 | 21,485–23,808 / 18–19% | 0 | −108 to −280, at most 3 |
| Hour stem (19h) × universal day | cold | System 7 disjoint | 26,325 / 17% | 0 | −108, at most 3 |
| Moon navamsa × Moon phase | hot / pos | System 7 overlap / 8 | 9,358–18,303 / 22–29% | 0 | −78 to −280 |
| Mercury nakshatra × aspect Moon–Mercury | hot+100 | System 7 / 8 | 23,136–39,975 / 14–19% | 0 | −108 to −200, at most 3 |
| 6 more 4 + bonus / 4 winners | various | various | 10,036–35,186 / 15–28% | 0 | all lost |

## Power Toto 6/55: today 5 numbers (RM6,800–6,812) and 4

| Lead | Pattern | Format | Earlier rank / return | Earlier 5+ hits | Last 10: profit, best per draw |
|---|---|---|---|---|---|
| Mercury rashi × day-vs-year branch | hot-cell + cold-100 | System 7 overlap | 7,491 / 8% | 0 | −140, at most 2 |
| Year yin-yang × plum trigrams | hot-cell + cold-100 | System 7 disjoint | 42,712 / 5% | 0 | −140, at most 2 |
| Weekday × Moon phase | cold+100 | System 7 disjoint | 43,959 / 4% | 0 | −140, at most 2 |
| Paksha × KP ascendant sub-lord | hot | System 7 disjoint | 33,287 / 5% | 0 | −140, at most 2 |
| **Nakshatra lord × day stem** | cold | System 8 | **600 / 28%** | 1 | −280, at most 2 |
| 10 more 4-number winners | various | System 8 | 4,116–42,042 / 4–23% | 0–1 | −280 each |

## Supreme Toto 6/58: today 5 numbers (RM7,176–21,944) and 4

| Lead | Pattern | Format | Earlier rank / return | Earlier 5+ hits | Last 10: profit, best per draw |
|---|---|---|---|---|---|
| **Jupiter nakshatra × aspect Moon–Mercury** (5 numbers in all 4 formats) | hot-cell + cold-100 | all four | 6,798–17,422 / 7–8% | 0 | −200 to −560, at most 2 |
| 10 leads with 4 numbers (year animal, KP Sun star-lord, lagna, Rahu/Saturn rashi …) | various | System 8 | 7,641–40,577 / 5–8% | 0 | −480 to −560 |

**What this means:**
- **No warning signs beforehand:** today's winners were ordinary or weak leads. Most ranked in the 10,000s–40,000s of 45,892. Almost none had a single high hit before, while the same lead on the shifted calendars averages about 0.1–0.3. Over the last 10 draws they mostly caught 0–3 numbers and lost their stake.
- **Only two had a decent earlier record:**
  - Mercury combust × soft aspects (cold-cell + hot-100, Magnum Life System 9 disjoint): rank 1,157, return 94%, with one earlier 7-number hit.
  - Nakshatra lord × day stem (cold, Power Toto System 8): rank 600, return 28%.
- **The big Magnum Life win is one hit counted several times:** the Nakshatra family (Nakshatra alone and its pairs) picked the same 10 numbers.

Big wins land on leads that looked unremarkable the day before. That's why the only fair test is to keep scoring the frozen watchlist on future draws. I'll add the two leads with a decent earlier record to the watch log too.

**Results updates:** I've scheduled myself to run the update on **Wednesday 21 Oct at 9:30 pm Malaysia time**, after the 7 pm draws. I'll fetch the results from 4dmoon.com, including any Tuesday 20 Oct special draw, add them to the history and score every watchlist lead. You'll get the running totals.

The full table, with every lead's draw-by-draw record for the last 10 draws, is in `analysis/WINNERS_HISTORY_2026-10-18.md`, pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Mercury combust × soft aspects (cold-cell + hot-100, Magnum Life System 9 disjoint): rank 1,157, return 94%, with one earlier 7-number hit. This got 2 hits of 7+?

**Answer:**

Yes: two hits of 7+ in that format, one earlier and today's. I'm pulling the exact draws and how it did in the other formats.

**Answer:**

Yes. In **System 9 × 2 disjoint**, Mercury combust × soft aspects (cold-cell + hot-100) now has **two hits of 7+**: one earlier and one today. In the other three formats it has only the earlier one.

| Draw | Set that hit | Winning numbers (+ bonus) | Match | Payout |
|---|---|---|---|---|
| **29 Jan 2025** | Set 1: 06 12 14 16 22 27 30 34 35 | 06 11 12 14 16 22 27 35 (+ 04 13) | 7 | RM12,700 |
| **18 Oct 2026** (today) | Set 2: 03 09 10 18 19 20 21 33 35 | 09 10 19 20 21 22 33 35 (+ 06 18) | 7 + bonus | RM110,200 |

The two hits came from different sets. In January 2025 it was the top 9 numbers (set 1); today it was ranks 10–18 (set 2), which is exactly what the disjoint structure covers.

**Its record in each format:**

| Format | 7+ hits | 6+ draws before today | Profit before the last 10 (return) | Last 10 draws | Today |
|---|---|---|---|---|---|
| 10 tickets (RM10) | 1 (29 Jan 2025) | 2 | −RM2,100 (79%) | −RM85 | −RM10 |
| System 10 × 1 (RM45) | 1 (29 Jan 2025) | 3 | −RM15,425 (66%) | −RM400 | −RM45 |
| System 9 × 2 overlap (RM18) | 1 (29 Jan 2025) | 4 | −RM1,061 (94%) | −RM160 | −RM18 |
| **System 9 × 2 disjoint (RM18)** | **2 (29 Jan 2025, 18 Oct 2026)** | 3 | −RM1,121 (94%) | −RM180 | **+RM110,182** |

Random entries return about 55%, so its 94% before today was well above average, though still a loss. With today's 7 + bonus, it is now hugely in profit in System 9 disjoint. Over roughly 1,000 draws it staked about RM18,200 and won about RM127,000.

**How rare is it?**
- **One earlier 7+ hit is common:** 2,787 leads had at least one in System 9 disjoint before today. The shifted calendars, which don't match the real sky, average about 2,633.
- **Two before today is common too:** 89 leads had that, against about 86 on the shifted calendars.
- **So it looked ordinary beforehand:** being one of thousands of leads with a single 7+ hit was not unusual. Hitting 7 + bonus today on top of that is what makes it stand out, but plenty of leads score one big hit by chance.

This lead wasn't on the watchlist before today's draw, so today's win counts as hindsight, not a prediction. The fair test is from now on. I'll add it to the watchlist in System 9 × 2 disjoint, so it gets scored on every future draw from 21 Oct.

---

**User:**

> Check the other Toto winners for repeat high hits too

**Answer:**

I'll go through every big Toto winner from today (15 per game) and list every draw in its whole history where it caught 5 or more numbers. I'll also add Mercury combust × soft aspects to the watchlist, as I said I would.

**Answer:**

Only one of today's Toto winners has a repeat high hit: **Hour stem (19h) × universal day (cold), Star Toto System 7 × 2 disjoint**. It caught 5 numbers on 29 Jun 2019 and again today. Every other Toto lead that caught 5 today had never done it before.

For each of today's 15 biggest winners per game, I checked every draw since draw 100 of each history (mid-2018 for Star, early 2010 for Power and Supreme). The search counted draws where the same lead and format caught 5+ numbers in one combination. It found no 6-number (jackpot) hits at all.

## Star Toto 6/50

| Lead | Pattern | Format | Today | Draws with 5+ in its history |
|---|---|---|---|---|
| **Hour stem (19h) × universal day** | cold | System 7 × 2 disjoint | 5 (RM4,156) | **2: 29 Jun 2019 (5, RM4,156) and 18 Oct 2026** |
| KP ascendant star-lord × aspect Moon–Mars | cold | System 8 / System 7 overlap / System 7 disjoint | 5 (RM6,524 / RM4,156 / RM4,156) | 1: today only, in each format |
| Mercury nakshatra × aspect Moon–Mercury | hot+100 | System 8, System 7 overlap and disjoint | 4 + bonus | 1: 2 Jan 2019 (5, RM6,524 in System 8) |
| KP Sun sub-lord × aspect Sun–Moon | cold-cell + hot-100 | System 7 × 2 disjoint | 4 + bonus | 1: 2 Jun 2018 (5, RM4,156) |
| Day vs year branch × aspect Moon–Saturn, Moon navamsa × Moon phase, Hora lord × day element, Aspect Sun–Mars × nine-star day / × aspect Venus–Mars, Aspect Sun–Moon × aspect Mercury–Saturn | various | various | 4 + bonus or 4 | none |

## Power Toto 6/55

| Lead | Pattern | Format | Today | Draws with 5+ in its history |
|---|---|---|---|---|
| Mercury rashi × day-vs-year branch | hot-cell + cold-100 | System 7 overlap | 5 (RM6,812) | 1: today only |
| Year yin-yang × plum trigrams | hot-cell + cold-100 | System 7 disjoint | 5 (RM6,800) | 1: today only |
| Weekday × Moon phase | cold+100 | System 7 disjoint | 5 (RM6,800) | 1: today only |
| Paksha × KP ascendant sub-lord | hot | System 7 disjoint | 5 (RM6,800) | 1: today only |
| **Hora lord × day-vs-year branch** | cold | System 8 | 4 | 1: **3 Aug 2025 (5, RM10,530)** |
| **Nakshatra lord × day stem** | cold | System 8 | 4 | 1: **24 Jul 2024 (5, RM10,530)** |
| 8 other System 8 leads with 4 numbers (nine-star day × plum trigrams, yoga pairs, nakshatra lord pairs …) | various | System 8 | 4 | none |

## Supreme Toto 6/58

| Lead | Pattern | Format | Today | Draws with 5+ in its history |
|---|---|---|---|---|
| Jupiter nakshatra × aspect Moon–Mercury | hot-cell + cold-100 | all four formats | 5 (RM7,176–21,944) | 1: today only, in each format |
| 10 System 8 leads with 4 numbers (year animal pairs, KP Sun star-lord × aspect Sun–Moon, lagna pairs, Rahu/Saturn rashi …) | various | System 8 | 4 | none |

**What this shows:**
- **Only one real repeater:** Hour stem (19h) × universal day, with two 5-number hits more than 7 years apart. In Magnum Life, Mercury combust × soft aspects also has two 7+ hits, in January 2025 and today.
- **Most of today's 5-hitters were first-timers:** that includes Supreme's Jupiter nakshatra × aspect Moon–Mercury, which hit 5 in all four formats today but never before in about 2,700 draws.
- **Repeats are expected anyway:** about 2,000–3,000 leads per game catch 5 at least once over the history, so some will happen to do it twice. Two hits in 1,400 draws, years apart, is consistent with luck.

I've also added Mercury combust × soft aspects to the watchlist. Wednesday's update will score it along with the rest.

The table is in `analysis/REPEAT_HITS_2026-10-18.md`, pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Would like to know how the historical data is calculated? Is it based on all the previous historical data from the last pair of the event or only 1 round of the recent pair of the event?

**Answer:**

I'll check this against the code and work through a real example from today's winners.

**Answer:**

It uses **all previous occurrences** of the same astrological condition, from the start of the data up to the day before the draw. It is not just the most recent occurrence.

**How a lead builds its numbers for a draw:**

1. **Find the draw's "cell".** Look up the parameter values on the draw date. For a pair lead, both values must match. For example, on 18 Oct for Mercury combust × soft aspects, the cell is "Mercury not combust **and** 3 soft aspects".
2. **Collect every earlier draw in the same cell.** That means every past draw in the history (since April 2018 for Magnum Life) that had exactly the same values, however long ago, and none from the draw date or later.
3. **Count how often each number came up in those draws**, compared with how often it should have by chance.
4. **Rank the numbers by the pattern:**
   - **hot:** the numbers drawn most often in that cell.
   - **cold:** the numbers drawn least often in that cell.
   - **pos:** the numbers most often drawn in each ticket position in that cell.
   - **…+100 patterns:** these combine the cell count with how hot or cold each number has been over the last 100 draws of the whole game, all days, not just that cell.
5. **Build the tickets or System sets** from the top-ranked numbers.

Every past draw in the cell counts equally. A matching draw from 2018 has the same weight as one from last month; there's no fading.

**Real examples from the 18 Oct Magnum Life draw** (1,346 earlier draws in total):

| Lead | Cell on 18 Oct | Earlier draws in that cell | Spread across | First – last |
|---|---|---|---|---|
| Mercury combust × soft aspects | Mercury not combust, 3 soft aspects | 165 | 115 separate periods | May 2018 – Sep 2026 |
| Nakshatra | Uttara Ashadha | 54 | 53 separate periods | May 2018 – Jul 2026 |
| Hour stem (19h) × universal day | Bing, day 2 | 26 | 26 separate periods | May 2018 – Aug 2026 |

So "Nakshatra (cold-cell + hot-100)" on 18 Oct used all 54 earlier Uttara Ashadha draws since 2018, not just the last Uttara Ashadha day in July. It took the numbers least drawn on those days and weighted them by how hot each number was over the last 100 draws.

**Walk-forward:** each draw's numbers use only the draws before it, and the cell history grows by one draw every time a new draw falls in that cell. That's the "update history before each draw" rule. The same applies in the tests: the 26 Sep draw used history to 21 Sep, the 27 Sep draw used history to 26 Sep, and so on.

**Using only the most recent occurrence instead:** that would be a different method, and I haven't tested it. Possible versions include:
- **Last round only:** use only the most recent run of matching days. For a slow parameter like a retrograde period that might be a few dozen draws; for a nakshatra it's a single day.
- **Last N occurrences:** for example, only the 5 or 10 most recent draws in the cell.
- **Weighted:** use all occurrences, but weight recent ones more heavily.

A few draws per cell is very little data, since each draw shows only 8 of 36 numbers (or 6 of 50–58), so these versions would be noisier. It's still a reasonable question to test.

If you want, I can add "last occurrence only" and "last 5 / last 10 occurrences" as new patterns. They'd go through the same tests: the last 10 draws walk-forward, shifted calendars, and then the next real draws.

---

**User:**

> Using only the most recent occurrence instead: that would be a different method, and I haven't tested it. Possible versions include:
> 
> 	•	Last round only: use only the most recent run of matching days. For a slow parameter like a retrograde period that might be a few dozen draws; for a nakshatra it's a single day.
> 	•	Last N occurrences: for example, only the 5 or 10 most recent draws in the cell.
> 	•	Weighted: use all occurrences, but weight recent ones more heavily. Do analysis for all this and see if new leads perform better than the existing ones, make sure you do all the analysis like we did before and don’t miss any

**Answer:**

I'll add the three history windows as new variants of every lead and run the complete analysis set for each one, then compare them with the current "all occurrences" method:

- **Last round:** only the most recent unbroken run of matching draws.
- **Last 5 and last 10:** only the 5 or 10 most recent draws in the cell.
- **Weighted:** all occurrences, with weight halving every 10 occurrences back.

Each window gets all 7 patterns in all four games, and every analysis we ran before. Starting with the code.

**Answer:**

All four history windows match a brute-force check exactly; the weighted one differs only by rounding. Confirming the default still reproduces the earlier results, then launching the four runs.

**Answer:**

The four new history windows are now running for all four games, each through the full set of analyses. That covers all 7 patterns, profit in four formats, re-ranking before every draw, the combined score, 20 shifted calendars, and per-lead high hits. They're queued one after another and should take about 5 hours.

After that, a follow-up step runs on its own for each window: it scores today's 18 Oct draw for all leads, looks up the biggest winners' history and repeat hits, and builds a side-by-side comparison with the current method.

The code changes are committed and pushed. I'll report as soon as everything has finished, including whether the new leads beat the existing ones. Your scheduled results update on Wednesday 21 Oct still stands.

**Answer:**

The analysis is still running in the background; the 2-hour limit only stopped my progress watcher. The first window (last round) is almost finished, with three windows and the follow-up steps still to go, about 3.5–4 hours. I've restarted the watcher and will report the full comparison when it finishes.

**Answer:**

I've committed and pushed the partial results file for the first history window (last round) to `claude/focused-franklin-ajsdm9`. That window's run hasn't finished yet, and the other three windows and the follow-up steps are still to come, about 3.5–4 hours in all. I'll commit again and report the full comparison when they're done.

**Answer:**

My progress watcher hit its 2-hour limit and stopped. The analysis itself is still running; I've restarted the watcher.

Progress so far:
- **Last round:** finished for all four games.
- **Last 5:** nearly done.
- **Last 10 and weighted:** still to run, about 2.5 hours in total.
- **After that:** the 18 Oct scoring, winners' history and repeat-hit checks for each window run automatically, then the side-by-side comparison.

I've committed and pushed the completed results to `claude/focused-franklin-ajsdm9`. I'll report the full comparison once everything finishes.

**Answer:**

My progress watcher hit its 2-hour limit again, but the analysis is still running and I've restarted the watcher. The completed results so far are committed and pushed to `claude/focused-franklin-ajsdm9`.

| Window | Status |
|---|---|
| Last round | done |
| Last 5 | done |
| Last 10 | on its final game (Supreme) |
| Weighted | still to run, about 70 minutes |

After that, the 18 Oct scoring, winners' history, repeat-hit checks and the side-by-side comparison run automatically, about another hour. I'll report the full results when they're done.

**Answer:**

Three of the four history windows are finished: last round, last 5 and last 10. The weighted window is running now and should be done around 19:20 UTC. After that, the 18 Oct scoring, winners' history, repeat-hit checks and the comparison run on their own, which takes roughly another hour.

My progress check timed out again, so I restarted it. The analysis itself kept running. Finished results are committed and pushed to `claude/focused-franklin-ajsdm9`. I'll report the full comparison when everything is done.

**Answer:**

I ran every analysis again for each of the four history windows: all 7 patterns, all four games and all four formats, the 20 shifted calendars, per-lead tests, the 18 Oct forward draw, the winners' history and repeat hits. None of the new windows performs better than the current method of counting all earlier draws in the cell.

**The windows:**
- **All:** every earlier draw in the cell (the current method).
- **Last round:** only the most recent unbroken run of draws in the cell.
- **Last 5 / last 10:** only the 5 or 10 most recent draws in the cell.
- **Weighted:** all earlier draws, with each draw's weight halving every 10 occurrences back.

## 1. Choosing leads in advance and playing the last 10 draws

Profit on the last 10 draws, best format per game. Shifted-calendar medians are in brackets.

| Window | Magnum Life System 9 overlap, top 10 by earlier profit | Star Toto 10 sets, top 10 | Power Toto System 8, top 10 | Supreme Toto System 8, top 10 | Combined-score top 10 (Magnum / Star / Power / Supreme) |
|---|---|---|---|---|---|
| all | −162 (−152) | −96 (−87) | −271 (−265) | −520 (−540) | −154 / −116 / −124 / −249 |
| last round | **−87** (−160) | −87 (−79) | −271 (−272) | −560 (−540) | −263 / −74 / −107 / −202 |
| last 5 | −145 (−150) | −96 (−78) | −274 (−266) | −528 (−544) | −162 / −118 / −128 / −250 |
| last 10 | −146 (−154) | **+122** (−82) | −242 (−265) | −560 (−536) | −174 / −85 / −104 / −241 |
| weighted | −154 (−150) | −64 (−82) | −230 (−259) | −520 (−544) | −168 / **+36** / −109 / −243 |

- **Choosing in advance still loses:** in every window, the leads chosen beforehand lose about their whole stake, much like the shifted calendars.
- **The positive results come from one lead each:**
  - **Magnum last round:** re-ranking before every draw (not in the table) made +RM360 in 10 tickets and +RM220 in System 9 overlap. Both come from one lead, **Day element × aspect Moon–Jupiter (hot, last round)**. It was #1 by earlier profit because of one past Grand prize, and its only win in the last 10 was a single 6 + bonus on 27 Sep.
  - **Star last 10:** +RM122 for the top 10 in 10 sets, from one lead's hit.
  - **Star weighted:** +RM36 for the combined-score top 10, also from one lead's hit.

## 2. Real calendar vs 20 shifted calendars over the whole history

Each cell shows the real calendar's rank out of 21 for high hits (7+ in Magnum Life, 5+ in Toto), across the four formats; 1 means the real calendar did best.

| Window | Magnum Life | Star Toto | Power Toto | Supreme Toto |
|---|---|---|---|---|
| **all** | 3–8 | **1, 1, 1, 1** | 9–16 | 2–16 |
| last round | 15–19 | 2–12 | 7–14 | 3–16 |
| last 5 | 7–21 | 9–17 | 20–21 | 16–21 |
| last 10 | 10–21 | 5–18 | 12–20 | 10–15 |
| weighted | 8–16 | 4–20 | 2–16 | 1–13 |

The only tilt we found earlier was Star Toto's extra 5-number hits on the real calendar. It shows up only with all earlier draws and disappears with the shorter windows. Short windows are also degenerate: with only one or a few earlier draws, many leads end up picking the same numbers. On 18 Oct in Supreme Toto, 2,955 last-round leads all won the same RM272.

## 3. Today's forward draw (18 Oct): the biggest winners in each window

| Window | Biggest win | Lead | Earlier record |
|---|---|---|---|
| last 5 | **Star 5 + bonus, Jackpot 2 (RM112,216)** | Karana × aspect Venus–Mars (hot), System 8 | rank 33,653, return 15% |
| weighted | Magnum 7 + bonus (RM110,200) | Month branch × aspect Jupiter–Saturn (hot+100), System 9 disjoint | rank 39,309, return 15% |
| last round | Power 5 numbers (RM10,143), many leads with the same numbers | Moon navamsa / yoga / Part of Fortune rashi pairs (hot-cell + cold-100), 10 sets | ranks in the tens of thousands |
| last 10 | Power 5 numbers (RM10,530) | Day branch × Part of Fortune rashi (hot), System 8 | rank 11,968, return 7% |
| weighted | Power 5 numbers in all 4 formats | Month branch × soft aspects (cold) | rank 18,687–32,314, return 5–6% |

As before, today's big wins went to leads that looked weak beforehand.

## 4. Repeat high hits among today's winners

| Window | Lead | Game, format | High hits |
|---|---|---|---|
| **last 10** | **Nayin element × plum trigrams (pos)** | Star Toto, System 7 × 2 overlap | **5 numbers on 4 Jan 2020, 6 Apr 2025 and 18 Oct 2026** |
| weighted | Sun rashi × nayin element (cold-cell + hot-100) | Magnum Life, System 9 overlap | 7 numbers on 21 Dec 2024 and 18 Oct 2026 |
| last 10 | Jupiter rashi × nine-star day (cold) | Power Toto, System 8 | 5 numbers in 2013 and 2016 (not today) |

## Verdict

None of the new history windows beats counting all earlier draws. They don't pick better leads in advance, they don't make the real calendar stand out more against the shifted ones, and they remove the one tilt we had found (Star Toto 5-number hits). The forward results are the same story: big wins land on leads with poor earlier records.

**Added to the watchlist from the new windows, scored from 21 Oct:**

| Game | Lead (pattern @ window) | Why | Format |
|---|---|---|---|
| Star Toto | **Nayin element × plum trigrams (pos @ last 10)** | three 5-number hits over 6 years | System 7 × 2 overlap |
| Magnum Life | Sun rashi × nayin element (cold-cell + hot-100 @ weighted) | two 7-number hits | System 9 × 2 overlap |
| Magnum Life | Day element × aspect Moon–Jupiter (hot @ last round) | #1 by earlier profit, the only re-ranked pick with profit on the last 10 | System 9 overlap, 10 tickets |
| Star Toto | Karana × aspect Venus–Mars (hot @ last 5) | Jackpot 2 today (hindsight) | System 8 × 1 |
| Power Toto | Month branch × soft aspects (cold @ weighted) | 5 numbers in all four formats today (hindsight) | System 8 × 1 |

The results update is still set for Wednesday 21 Oct, 9:30 pm Malaysia time. It will fetch the new draws from 4dmoon.com and score every watchlist lead: the original ones, the new-pattern ones and these window leads.

The side-by-side comparison is in `analysis/WINDOWS_COMPARE.md`, with per-window details in `analysis/LEADS7_<WINDOW>_*.md`, `WINNERS_HISTORY_<WINDOW>_2026-10-18.md` and `REPEAT_HITS_<WINDOW>_2026-10-18.md`. FINDINGS.md and WATCHLIST.md are updated, and everything is pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> List out all the leads to be observed and how they became to be observed

**Answer:**

I'll take the list straight from the watchlist scorer, which holds every lead that gets scored on each new draw, and pair each lead with the reason it was added.

**Answer:**

There are **52 leads** on the watchlist: 18 for Magnum Life, 15 for Star Toto, 10 for Power Toto and 9 for Supreme Toto. Each one was added at one of four stages, and every one is scored automatically on each new draw.

**The four stages:**

| Stage | When | How leads were chosen |
|---|---|---|
| **A** – original analysis | after the 17 Oct draw | all single and pair parameters × 4 patterns (hot, cold, pos, hot+100), official prizes, tested on the last 10 draws (26 Sep–17 Oct) |
| **B** – 7 patterns | after 17 Oct | the 3 new patterns added (cold+100, hot-cell + cold-100, cold-cell + hot-100), same tests |
| **C** – history windows | after 17 Oct | only the last round / last 5 / last 10 / weighted earlier draws of each cell, same tests |
| **D** – 18 Oct hindsight | after 18 Oct | big winners of 18 Oct with a repeat high hit or a striking win; picked after the result, so only future draws count for them |

"Earlier" means the history before the last 10 draws. Random entries return about 55% of the stake in Magnum Life, 35% in Star Toto and 20% in Power and Supreme.

## Magnum Life 8/36 (18 leads)

| # | Lead | Pattern | Format | Stage | Why it is watched |
|---|---|---|---|---|---|
| 1 | Mercury nakshatra × Saturn combust | cold | System 10, 10 tickets | A | Profitable before **and** during the last 10: earlier return 293% (one 7 + bonus in Dec 2022), then 7 numbers on 4 Oct (+RM19,910) |
| 2 | Day pillar × aspect Jupiter–Saturn | pos | System 10 | A | 7 numbers on 3 Oct in three formats; best earlier record of the big hitters (rank 1,236, return 67%) |
| 3 | Paksha × Venus rashi | cold | 10 tickets, System 10 | A | **Grand prize (all 8) on 26 Sep**; weak beforehand (rank 12,375) |
| 4 | Ayana × lunar leap month | hot+100 | System 9 × 2 disjoint | A | 7 + bonus (RM110,200) on 7 Oct; then 5 + 2 bonus on 18 Oct (+RM212), the only watched lead in profit so far |
| 5 | Aspect Venus–Jupiter × universal day | hot | System 9 × 2 overlap | A | 7 + bonus (RM110,240) on 30 Sep |
| 6 | Saturn combust × plum trigrams | cold | System 10 | A | 7 numbers in all four formats on 3 Oct |
| 7 | Part of Fortune rashi × aspect Venus–Jupiter | cold | System 9 × 2 overlap | A | Two 7-number draws in 2024, earlier return 177%; quiet in the last 10 |
| 8 | KP Sun sub-lord × year yin-yang | hot | System 10 | A | Won on 4 of the last 10 draws (+RM540) |
| 9 | Ayana × KP Moon star-lord | pos | System 9 × 2 overlap | A | Won on 4 of the last 10 draws (+RM300) |
| 10 | Mars rashi × month | cold | System 10 | A | Most persistent ball-catcher (kept as a reference, though it loses money) |
| 11 | Mercury rashi × KP ascendant sub-lord | cold+100 | System 10, System 9 overlap | B | Earlier return 286% (rank 994) and profit in three formats on the last 10 |
| 12 | Mars retrograde × Moon phase | hot-cell + cold-100 | System 9 × 2 disjoint | B | Won on 4 of the last 10 draws (+RM1,465) |
| 13 | Mercury rashi × day branch | cold+100 | System 9 × 2 overlap | B | Won on 4 of the last 10 draws (+RM1,400) |
| 14 | Month stem × KP ruling planets | hot-cell + cold-100 | System 9 × 2 disjoint | B | Won on 4 of the last 10 draws (+RM1,380) |
| 15 | Aspect Moon–Mars × aspect Mercury–Mars | cold+100 | System 10 | B | Most 7+ hits against its own shifted calendars (z +8.8) |
| 16 | Day element × aspect Moon–Jupiter | hot @ last round | System 9 overlap, 10 tickets | C | #1 by earlier profit in three formats; the only pick re-ranked before each draw that made a profit on the last 10 (+RM360) |
| 17 | Mercury combust × soft aspects | cold-cell + hot-100 | System 9 × 2 disjoint | D | **Two 7+ hits**: 7 on 29 Jan 2025, then 7 + bonus (RM110,200) on 18 Oct; earlier return 94% |
| 18 | Sun rashi × nayin element | cold-cell + hot-100 @ weighted | System 9 × 2 overlap | D | Two 7-number hits: 21 Dec 2024 and 18 Oct 2026 |

## Star Toto 6/50 (15 leads)

| # | Lead | Pattern | Format | Stage | Why it is watched |
|---|---|---|---|---|---|
| 1 | Hour stem (19h) × tropical Sun sign | pos | System 8 | A | **5 + bonus (Jackpot 2, RM100,000)** on the last 10; earlier rank 720, return 55% |
| 2 | Hora lord × Mars retrograde | cold | 10 sets | A | 5 numbers on 7 Oct; earlier rank 843, return 56% |
| 3 | Hora lord × adhika masa | cold | 10 sets | A | 5 numbers on 7 Oct; earlier rank 1,101, return 55% |
| 4 | Rahu nakshatra × KP ascendant sub-lord | hot | System 8 | A | 4 + bonus, 3 winning draws; earlier rank 1,098 |
| 5 | Sun rashi × planets with Moon | cold | System 8 | A | Won on 4 of the last 10 draws (+RM6,544) |
| 6 | Lagna rashi × day officer | cold | System 7 × 2 disjoint | A | 5 numbers, won on 4 of the last 10 |
| 7 | Saturn retrograde × nayin | hot | 10 sets | A | Most 5+ hits against its own shifted calendars (10 vs 0.2) |
| 8 | Karana × masa | cold | System 8 | A | 9 hits of 5+ against its own shifted calendars; about break-even on the last 10 |
| 9 | Hora lord × Mars combust | cold-cell + hot-100 | 10 sets, System 7 overlap | B | 5 numbers on 7 Oct (+RM8,100); 3 numbers on 18 Oct (RM8 prize) |
| 10 | Saturn retrograde × aspect Mercury–Jupiter | cold-cell + hot-100 | System 7 × 2 disjoint | B | Earlier return 55% (rank 1,172), +RM4,048 on the last 10 |
| 11 | Aspect Sun–Mars × aspect Moon–Venus | hot-cell + cold-100 | System 7 × 2 disjoint | B | Earlier return 45%, +RM4,078 on the last 10 |
| 12 | Day of month × aspect Venus–Jupiter | hot-cell + cold-100 | System 7 × 2 disjoint | B | Top by earlier profit **and** +RM4,016 on the last 10 |
| 13 | Mars combust × aspect Moon–Mercury | hot-cell + cold-100 | 10 sets | B | Most 5+ hits against its own shifted calendars (12, z +11.9) |
| 14 | **Nayin element × plum trigrams** | pos @ last 10 | System 7 × 2 overlap | C/D | **Three 5-number hits**: 4 Jan 2020, 6 Apr 2025, 18 Oct 2026 |
| 15 | Karana × aspect Venus–Mars | hot @ last 5 | System 8 | D | 5 + bonus (Jackpot 2, RM112,216) on 18 Oct; weak beforehand (rank 33,653) |

## Power Toto 6/55 (10 leads)

| # | Lead | Pattern | Format | Stage | Why it is watched |
|---|---|---|---|---|---|
| 1 | Lunar month × tropical Sun sign | hot+100 | System 8 | A | **Jackpot** on the last 10; best earlier record of the jackpot leads (rank 2,142) |
| 2 | Tropical Sun sign × aspect Moon–Saturn | hot+100 | 10 sets, System 8 | A | **Jackpot on 11 Oct** |
| 3 | Masa × day god | hot | 10 sets | A | **Jackpot on 27 Sep**; weak beforehand (rank 20,004) |
| 4 | Masa × adhika masa | hot+100 | System 8 | A | Jackpot in System play |
| 5 | Month branch × aspect Venus–Jupiter | hot+100 | System 8 | A | Jackpot in System 8 |
| 6 | Lagna rashi × Saturn retrograde | hot+100 | System 7 × 2 overlap | A | Profit in three formats; 10 hits of 5+ against its own shifted calendars (z +9.6) |
| 7 | KP Sun star-lord × month pillar | hot+100 | 10 sets | A | Won on 4 of the last 10 draws |
| 8 | Mercury nakshatra × soft aspects | cold-cell + hot-100 | System 7 × 2 disjoint | B | 5 numbers, +RM6,672 on the last 10 |
| 9 | Mars combust × aspect Jupiter–Saturn | cold-cell + hot-100 | 10 sets | B | 9 hits of 5+ against its own shifted calendars (z +8.6) |
| 10 | Month branch × soft aspects | cold @ weighted | System 8 | D | 5 numbers in all four formats on 18 Oct; weak beforehand |

## Supreme Toto 6/58 (9 leads)

| # | Lead | Pattern | Format | Stage | Why it is watched |
|---|---|---|---|---|---|
| 1 | Moon rashi × hard aspects | cold | System 8 | A | 5 numbers, +RM21,464; **best earlier record in Supreme** (rank 106, return 44%) |
| 2 | KP Sun star-lord × day stem | hot | System 7 × 2 disjoint | A | 5 numbers, +RM14,168; earlier rank 1,473, return 30% |
| 3 | Nakshatra × nayin | hot+100 | 10 sets | A | 5 numbers on 11 Oct (+RM27,856), with its related leads (Nakshatra / KP Moon number paired with nayin / day pillar) |
| 4 | KP Moon number × nayin element | hot+100 | System 7 × 2 overlap | A | Top of the combined ranking (5 numbers, 3 winning draws) |
| 5 | Nakshatra × tropical Sun sign | hot+100 | 10 sets | A | Most 5+ hits against its own shifted calendars (12, z +11.3) |
| 6 | Saturn rashi × KP ascendant star-lord | cold+100 | System 7 × 2 disjoint | B | 5 numbers, +RM13,928; earlier return 29% |
| 7 | KP ascendant star-lord × year pillar | hot-cell + cold-100 | System 7 × 2 overlap | B | #1 by earlier profit; almost break-even on the last 10 (−RM8) |
| 8 | Lagna rashi × lunar day | hot-cell + cold-100 | System 8 | B | 5 numbers, +RM21,384 |
| 9 | Sun nakshatra × lunar month | cold-cell + hot-100 | System 7 × 2 overlap | B | 5 numbers, +RM13,928 |

**Performance so far:**
- **Stages A and B:** scored on 18 Oct. Only Ayana × lunar leap month (+RM212) made a profit, and Hora lord × Mars combust won RM8. Every other lead lost its stake.
- **Stages C and D:** these leads start counting from Wednesday 21 Oct.

**Caveat:** every lead on this list was found by looking back over tens of thousands of candidates, and the shifted calendars produce leads like these just as often. Only their results on future draws will show whether any of them is more than luck.

The scheduled update runs on Wednesday 21 Oct at 9:30 pm Malaysia time. It fetches the new results from 4dmoon.com and scores all 52 leads. The list and its reasons are in `analysis/WATCHLIST.md`, and the draw-by-draw scores are in `analysis/WATCH_LOG.md`.

---

**User:**

> Check if d9 navamsa plays a role single or as pair, redo all the analysis that we have already done specifically on this family.

**Answer:**

I'll start by checking which navamsa (D9) parameters the data already has, and whether the others can be computed.

**Answer:**

Only Moon navamsa exists so far. I'll look at how it's computed so I can build the full D9 family the same way.

**Answer:**

I've built the full D9 (navamsa) family and started rerunning every analysis on it. There are 13 parameters:

- the navamsa sign of the Moon, Sun, Mars, Mercury, Venus, Jupiter, Saturn, Rahu and Lagna;
- the D9 lord of the Moon and of the Lagna;
- Moon vargottama (same sign in D1 and D9), and the number of vargottama bodies.

These cover every draw date. The pipeline recomputes the existing Moon navamsa values exactly and reproduces the earlier Moon navamsa lead results.

For each of the four games, the run covers all 1,560 singles and pairs involving a D9 parameter, × 7 patterns, which is 10,920 leads. For each of the five history windows (all, last round, last 5, last 10, weighted) it repeats:

- profit in the four formats;
- re-ranking before every draw;
- the combined score;
- 20 shifted calendars over the whole history;
- per-lead high hits;
- the 18 Oct forward draw;
- the winners' history and repeat hits.

A final D9 report then compares the family against all leads and tests each D9 parameter on its own.

It should take about 3 hours. The code and the new D9 data are committed and pushed to `claude/focused-franklin-ajsdm9`, and I'll report when it's done. The Wednesday 21 Oct results update is still scheduled and will include any good D9 leads.

**Answer:**

The first window finished in 28 minutes with no errors. Four more to go, about 2 hours.

**Answer:**

The D9 runs are now on the last-round window, about 2 hours to go.

**Answer:**

I've committed and pushed the D9 results for the first history window ("all") to `claude/focused-franklin-ajsdm9`. The other four windows are still running, about 2 hours in total.

**Answer:**

The container restarted, which stopped both my progress watcher and the D9 run itself. I'm checking what survived before resuming.

**Answer:**

A container restart cut off the last D9 window ("weighted") partway through Supreme Toto. The other four windows had already finished, and their results are committed and pushed. I've restarted the weighted window, followed by the comparison and the D9 report. It should take about 35 minutes, and I'll report the full D9 results then.

**Answer:**

I reran every analysis on the full D9 family for all four games and all five history windows. D9 shows a small, uneven tilt: a little stronger than the average parameter in some games and weaker in others. It does not pick winners in advance any better than the other parameters do.

**What I built:** 13 D9 parameters, computed for every draw date at the 7 pm draw time:
- the navamsa sign of the Moon, Sun, Mars, Mercury, Venus, Jupiter, Saturn, Rahu and Lagna;
- the D9 lord of the Moon and of the Lagna;
- Moon vargottama, and the number of bodies that are vargottama.

That gives 1,560 singles and pairs × 7 patterns = **10,920 D9 leads per game**. I checked them against the earlier analyses: the existing Moon navamsa values matched exactly, and so did its earlier lead results.

## 1. Does the D9 family stand out against the shifted calendars?

This counts high hits (7+ in Magnum Life, 5+ in Toto) over the whole history. Rank is out of 21 calendars, where 1 means the real calendar did best.

| Game | D9 family rank, all earlier draws (z) | All leads rank (z) | Best D9 window |
|---|---|---|---|
| Magnum Life | 4 (+1.1) | 5 (+0.9) | **last round: 1st (z +3.0)**, while all leads rank 18th |
| Star Toto | 4 (+1.3) | **1 (+4.4)** | – (other windows 11th–19th) |
| Power Toto | **3 (+1.0)** | 12 (−0.6) | – (other windows 16th–20th) |
| Supreme Toto | 15 (−0.6) | 15 (−0.2) | last round 4th (+1.1) |

- **A mild edge in some games:** D9 is slightly better than average in Magnum Life and Power Toto.
- **Weaker in Star Toto:** the real calendar's 5-number tilt there comes from other parameters, not D9.
- **No standout in Supreme Toto.**
- **The one strong result is narrow:** Magnum Life with the last-round history (z +3.0). Short windows like last round tend to make many leads pick the same numbers, which can inflate a score like this.

## 2. Which D9 parameters carry it

I scored every D9 parameter in every game and window, 260 values in all. By chance about 3 would pass |z| > 2.5; **8 did, 6 of them positive**:

| Parameter | Where | z |
|---|---|---|
| **Lagna navamsa lord** | Magnum Life, last round | **+5.3** |
| Moon navamsa lord | Magnum Life, last round | +3.7 |
| **Lagna navamsa lord** | Power Toto, all earlier draws | **+3.2** |
| **Lagna navamsa** | Magnum Life, all earlier draws | **+3.1** |
| Sun navamsa | Magnum Life, last round | +2.9 |
| Sun navamsa | Supreme Toto, last 10 | +2.6 |
| Venus navamsa | Star Toto, weighted | −2.7 |
| Rahu navamsa | Power Toto, last 10 | −2.9 |

- **The Lagna-based D9 factors stand out most often:** Lagna navamsa and its lord appear in two games.
- **Not consistent:** none of them is strong in all games or all windows. In Star Toto, for example, Lagna navamsa is negative (−1.4).
- **Likely a seasonal effect:** at a fixed 7 pm draw time, the Lagna's navamsa moves with the date through the year. That makes it partly seasonal, like solar term, which also showed up in Star Toto earlier.

## 3. Choosing D9 leads in advance

Profit on the last 10 draws, using all earlier draws. Shifted-calendar medians are in brackets.

| Game | D9: top 10 by earlier profit (best format) | All leads, same | D9: combined-score top 10 | All leads |
|---|---|---|---|---|
| Magnum Life | **−RM86 (−155)**, System 9 disjoint | −RM88 (−87) | −RM126 (−171) | −RM154 (−158) |
| Star Toto | −RM96 (−88) | +RM318 (−119) | −RM120 (−111) | −RM116 (−116) |
| Power Toto | −RM96 (−92) | −RM83 (−92) | −RM119 (−125) | −RM124 (−124) |
| Supreme Toto | −RM184 (−192) | −RM186 (−194) | −RM238 (−252) | −RM249 (−236) |

D9 leads chosen in advance still lose about the whole stake. Magnum Life is the only game where they did a bit better than the shifted calendars.

## 4. Today's forward draw (18 Oct)

A slightly larger share of D9 leads won some prize than all leads did:

| Game | D9 leads winning a prize | All leads |
|---|---|---|
| Magnum Life | 9.1–10.9% | 8.6–9.6% |
| Power Toto | 3.1–3.7% | 2.3–3.3% |

Their wins were mostly small, though: the D9 family's best payout was smaller than the best across all leads. One draw is far too little to read anything into this.

**Repeat high hits among D9 leads:**
- **Moon sign (tropical) × Sun navamsa** (cold-cell + hot-100), Magnum Life System 9 disjoint: 7 + bonus (RM110,200) on 27 Apr 2025, then 7 numbers today.
- **Aspect Venus–Jupiter × Sun navamsa** (cold-cell + hot-100), Magnum Life System 10: 7 numbers on 15 Sep 2024 and today.
- **Rahu navamsa × vargottama count** (hot), Power Toto System 8: 5 numbers in 2014 and 2023.

## Verdict

D9 doesn't predict better than the other parameters. The Lagna-based D9 factors (Lagna navamsa and its lord) are the most interesting part. They appear in two games, but they aren't consistent across games and windows, and they may simply track the season. They're worth watching, not betting on.

**Added to the watchlist, scored from 21 Oct:**

| Game | Lead | Pattern | Format | Why |
|---|---|---|---|---|
| Magnum Life | Moon sign (tropical) × Sun navamsa | cold-cell + hot-100 | System 9 disjoint | 7 + bonus in 2025, 7 today |
| Magnum Life | Aspect Venus–Jupiter × Sun navamsa | cold-cell + hot-100 | System 10 | 7 in 2024, 7 today |
| Magnum Life | Day element × Lagna navamsa lord | pos | 10 tickets | top of the D9 combined ranking (+RM1,505 on the last 10) |
| Magnum Life | Lagna navamsa lord × vargottama count | hot-cell + cold-100 | System 9 disjoint | top D9 lead by earlier profit in 3 formats |
| Star Toto | Aspect Mars–Saturn × Mars navamsa | cold+100 | System 7 disjoint | won on 4 of the last 10 (+RM4,112) |
| Power Toto | Year stem × Lagna navamsa lord | cold | 10 sets | most 5+ hits against its own shifted calendars (z +11.8) |
| Power Toto | Lagna nakshatra × Rahu navamsa | hot+100 | 10 sets | won on 3 of the last 10 (+RM13,346) |
| Supreme Toto | Plum trigrams × Saturn navamsa | hot-cell + cold-100 | 10 sets | most 5+ hits against its own shifted calendars (z +9.7) |

That brings the watchlist to 60 leads.

A container restart interrupted the last history window partway through; I reran it, so all five windows are complete.

The 21 Oct results update is still set to run at 9:30 pm Malaysia time and will score all 60 leads. The full results are in `analysis/D9_REPORT.md` and `analysis/WINDOWS_COMPARE_D9.md`, with per-window details in `analysis/LEADS7_*_D9_*.md`. Everything is pushed to `claude/focused-franklin-ajsdm9`.

---

**User:**

> Check how the other D does then

**Answer:**

The other divisional charts are the 14 Parashari vargas besides D1 and D9: D2, D3, D4, D7, D10, D12, D16, D20, D24, D27, D30, D40, D45 and D60. I'll build each one the same way as D9: 12 parameters per chart (the sign of the 9 bodies including Lagna, the Lagna and Moon lords, and a vargottama count). Then I'll run the full analysis on each family, then a cross-chart report and one forward check.

Running 14 families × 5 history windows would take about 30 hours. So I'll first run all 14 with all earlier draws (about 7 hours, resumable), then run the windows only for the charts that stand out.

**Answer:**

Varga families work end to end, and the watchlist scorer still reproduces the known tickets. Writing the cross-chart report next.

**Answer:**

The divisional-chart test (D2 to D60) has only just started, so I have no results to report yet. D2 began at 05:16 UTC. Each chart takes about 28 minutes and there are 14 of them, so the whole set should be done in roughly 6½–7 hours.

For each chart I score its 12 parameters on their own and in pairs, with all 7 patterns. The parameters are the sign of each of the 9 bodies including Lagna, the Moon's and Lagna's sign lords, and how many bodies sit in the same sign as in the main chart. Each chart then goes through the same analysis as D9:
- **20-calendar test:** high hits over the whole history, real calendar against 20 shifted calendars.
- **Per-parameter check:** how much each parameter beats its own shifted calendars.
- **Picked in advance:** profit on the last 10 draws from leads chosen beforehand (top 10, re-ranked each draw, and combined score).
- **18 Oct draw:** what each chart's leads won.
- **Earlier record:** the best 18 Oct winners checked against their earlier history and repeat high hits.

Each finished chart is committed and pushed automatically. At the end I'll write `analysis/VARGAS_REPORT.md`, which puts every chart side by side with D9 and with all leads.

Once the report is written I'll tell you which charts and parameters stand out, if any. For those I'll run the other history windows (last round, last 5, last 10, weighted) and add their leads to the watchlist. The results update for Wednesday 21 Oct is still scheduled for 21:30 Malaysia time.

**Answer:**

D2 finished in about 17 minutes. That's faster than the others will be, because every D2 body can only be in one of two signs. D3 is running now. I'll report once all 14 charts and the comparison report are done.

**Answer:**

The chart runs are still going: D2 is done and D3 is in progress. I'm watching for the rest and will report once all 14 charts and the comparison report are finished.

**Answer:**

The finished D3 results file is now committed and pushed. The other D3 steps (the 18 Oct scoring and the winners checks) are still running. The run script commits and pushes each chart's files as it finishes, so the rest of the 14 charts will follow on their own.

I'll report how each divisional chart performs once all of them and the side-by-side report are done.

**Answer:**

D3 finished at 05:51 UTC. That's 2 of 14 charts done, at about 17 minutes each, so the rest should take roughly 3½ hours. I'll report once the side-by-side report is done.

**Answer:**

D4 finished at 06:09 UTC, so 3 of the 14 charts are done. The remaining 11 should take about 3 more hours.

**Answer:**

The divisional-chart runs are still in progress. D2, D3 and D4 are done, and D7 to D60 are still to come. I'll be notified when the whole set finishes, or straight away if a run fails. Then I'll report how each chart compares with D9 and with all leads.

**Answer:**

The D7 results file that triggered the stop hook is now committed and pushed, so the branch is clean again.

The chart runs are still going: D2, D3 and D4 are done, and D7 is part-way through. I'll report how each chart compares with D9 and with all leads once the full set and the comparison report are finished.

**Answer:**

The divisional-chart runs are still going: 10 of the 14 charts are done (D2 through D27). D30 started at 08:17 UTC, and D40, D45 and D60 follow, so about 75 more minutes.

My earlier wait hit its time limit and was stopped, but the runs themselves were unaffected. I've set a new one. Once all four charts and the comparison report are done, I'll report how each chart does against D9 and against all leads.

**Answer:**

In the report, pass names truncated to base+D9 for the d9 family.

**Answer:**

All 14 divisional charts have finished and the comparison report is written. I'm now choosing which of their leads to add to the watchlist.

**Answer:**

Singles work as plain names. Adding the varga leads to the watchlist and testing them on 18 Oct.

**Answer:**

I tested the other 14 divisional charts (D2, D3, D4, D7, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60) the same way as D9. Overall they don't help: none beats the general leads, though D24 is mildly suggestive.

Each chart has 12 parameters: the sign of the 9 bodies including Lagna in that chart, the Moon's and Lagna's sign lords, and how many bodies sit in the same sign as in the main chart. Taken singly and in pairs with 7 patterns, that is 11,130 leads per chart and game. Each went through the 20-shifted-calendar test, the per-parameter check, choices made before the last 10 draws, and the 18 Oct draw.

**Each chart's leads together** (high hits over the whole history; rank of the real calendar among 21, 1 = most; z in brackets):

| Chart | Magnum Life | Star | Power | Supreme |
|---|---|---|---|---|
| all leads | 5 (+0.9) | 1 (+4.4) | 12 (−0.6) | 15 (−0.2) |
| D9 | 4 (+1.1) | 4 (+1.3) | 3 (+1.0) | 15 (−0.6) |
| **D24** | **1 (+1.9)** | **2 (+1.8)** | **1 (+2.1)** | 11 (+0.4) |
| D7 | 9 | 3 | 11 | **1 (+2.4)** |
| D10 | 4 | 3 (+1.9) | 18 | 2 (+1.5) |
| D30 | 5 | 6 | 4 | 2 (+1.6) |
| D27 | 3 | 12 | 3 (+1.5) | 17 |
| others | mixed and middling, as chance would put them | | | |

- **D24 is the only chart that does well in three games**, ranking 1st, 2nd and 1st in Magnum Life, Star and Power. With 15 charts tested, about one in 20 such tests would show this by chance, so it is suggestive, not proof. It is weak in Supreme.
- **No chart carries the Star Toto tilt.** That tilt still comes from the ordinary leads.
- **The strongest single parameters are all slow bodies:**
  - Saturn in D10: Star, z +7.3.
  - Rahu in D27: Magnum Life, z +6.1.
  - Jupiter in D7: Magnum Life, z +5.5.

  Saturn holds a D10 sign for about six weeks at a time, so it marks stretches of time rather than individual draws. It may be picking up a lucky period rather than a real link.
- **Chosen in advance, these leads still lose about the stake, like all the others.** Three exceptions on the last 10 draws, compared with the median of the shifted calendars:
  - D10 Star, top 10 on System 8: +RM43 against −RM222.
  - D7 and D16 Magnum Life on System 9 × 2 overlap: −RM24 and −RM12, against about −RM150.
  - D12 Star, combined top 10: +RM301 against −RM112.
- **Jackpots in hindsight show up in every chart.** These include Star 6-number hits with Jupiter in D10 or Mercury in D12, and Power 6-number hits with D10 or D30 parameters. In every case the lead ranked hundreds to thousands down beforehand, the same pattern seen in every other family.
- **On 18 Oct** the share of these leads winning a prize was about the same as for all leads.

**Added to the watchlist (69 leads now):** for each chart and parameter that stood out, the best lead before 26 Sep that contains it. All lost or broke even on 18 Oct.
- Magnum Life:
  - moon_phase × lagna_d24
  - aspect_mars_jupiter × rahu_d27
  - day_vs_year_branch × jupiter_d7
- Star:
  - samvatsara × vargottama_d24_count
  - rahu_rashi × vargottama_d10_count
- Power:
  - saturn_d24 (single)
  - pof_sign × moon_d27_lord
- Supreme:
  - venus_retrograde × venus_d30
  - kp_sun_number × lagna_d7

The full tables are in `analysis/VARGAS_REPORT.md`, and `FINDINGS.md` and `WATCHLIST.md` are updated. Everything is committed and pushed.

The other history windows (last round, last 5, last 10, weighted) haven't been run on the charts yet; D24 is the best candidate, at about 1½ hours per window.

The results update for Wednesday 21 Oct is still set for 21:30 Malaysia time and will score all 69 watchlist leads.

---

**User:**

> Ok now list out all the leads and rank them from the best to worse and tell me why they are in the rank

**Answer:**

Writing a scorecard script that replays all 69 watchlist leads over the whole history, on the real calendar and on 20 shifted calendars. Tightening the ranking measures now.

**Answer:**

Ranking is computed; now writing a short reason for each lead and committing.

**Answer:**

I ranked all 69 watchlist leads, 75 entries in total because 6 leads are watched in two formats. Each was replayed over the whole history, using only draws before each draw, with the official prizes. Each lead was then compared with itself on 20 shifted calendars, where the astrology dates are moved so they no longer line up with the draws.

**How the score works.** Each entry is ranked three ways, and the final rank is the average:
1. **Return:** how much more it paid on the real calendar than on its own shifted ones.
2. **High hits:** how many more 7+ (Magnum Life) or 5+ (Toto) hits it got than on the shifted calendars.
3. **Steadiness:** whether that edge shows up in both the first and the second half of the history, or only in one stretch.

Every lead was picked because of a good past record, so a high rank means a strong record, not proof. The only real test is future draws.

## Tier 1: repeated high hits spread over years, ahead of chance in both halves

| # | Game | Lead (pattern, format) | Why |
|---|---|---|---|
| 1 | Star | day_of_month × aspect_venus_jupiter (hot/cold100, System 7 × 2 disjoint) | 5 in 2021, all 6 in 2022, 5 on 26 Sep. Strong in both halves |
| 2 | Power | sun_sign_tropical × aspect_moon_saturn (hot+100, System 8) | 5 in 2017, all 6 on 11 Oct (the 6 is why it was picked) |
| 3 | Power | year_stem × lagna_navamsa_lord (cold, 10 sets) | Three 5-number hits (2017, 2018, 2022), all before it was chosen. The cleanest record: no jackpot, 72% return vs 5% shifted |
| 4 | Star | nayin_element × plum_trigrams (pos@last10, System 7 × 2 overlap) | 5 in 2020, 2025 and on 18 Oct |
| 5 | Magnum | aspect_mars_jupiter × rahu_d27 (hot/cold100, 10 tickets) | 7 in 2023, all 8 in 2025 |
| 6 | Supreme | moon_rashi × aspects_hard (cold, System 8) | 5 in 2018, 2020 and on 27 Sep |
| 7 | Supreme | plum_trigrams × saturn_navamsa (hot/cold100, 10 sets) | 5 in 2014, 2015 and 2025 |
| 8 | Magnum | mercury_nakshatra × saturn_combust (cold, System 10) | 7 in 2022 and on 4 Oct; 335% return |
| 9 | Power | lunar_month × sun_sign_tropical (hot+100, System 8) | 5 in 2023, all 6 on 11 Oct |
| 10 | Magnum | pof_rashi × aspect_venus_jupiter (cold, System 9 × 2 overlap) | Two 7s in 2024 |

## Tier 2: two high hits, or one jackpot plus an edge in both halves (11–30)

| # | Game | Lead | Pattern, format |
|---|---|---|---|
| 11 | Supreme | nakshatra × sun_sign_tropical | hot+100, 10 sets |
| 12 | Supreme | kp_asc_star_lord × year_pillar | hot/cold100, System 7 × 2 overlap |
| 13 | Power | pof_sign × moon_d27_lord | hot+100, 10 sets |
| 14 | Power | lagna_rashi × saturn_retrograde | hot+100, System 7 × 2 overlap |
| 15 | Magnum | day_pillar × aspect_jupiter_saturn | pos, System 10 |
| 16 | Power | sun_sign_tropical × aspect_moon_saturn | hot+100, 10 sets |
| 17 | Power | mars_combust × aspect_jupiter_saturn | cold/hot100, 10 sets |
| 18 | Magnum | day_element × aspect_moon_jupiter | hot@last_round, 10 tickets |
| 19 | Star | saturn_retrograde × nayin | hot, 10 sets |
| 20 | Magnum | aspect_moon_mars × aspect_mercury_mars | cold+100, System 10 |
| 21 | Magnum | ayana × lunar_leap_month | hot+100, System 9 × 2 disjoint |
| 22 | Power | saturn_d24 | hot+100, 10 sets |
| 23 | Magnum | moon_phase × lagna_d24 | hot/cold100, 10 tickets |
| 24 | Star | saturn_retrograde × aspect_mercury_jupiter | cold/hot100, System 7 × 2 disjoint |
| 25 | Magnum | aspect_venus_jupiter × sun_navamsa | cold/hot100, System 10 |
| 26 | Magnum | day_element × aspect_moon_jupiter | hot@last_round, System 9 × 2 overlap |
| 27 | Magnum | moon_sign_tropical × sun_navamsa | cold/hot100, System 9 × 2 disjoint |
| 28 | Supreme | saturn_rashi × kp_asc_star_lord | cold+100, System 7 × 2 disjoint |
| 29 | Magnum | mercury_combust × aspects_soft | cold/hot100, System 9 × 2 disjoint |
| 30 | Magnum | paksha × venus_rashi | cold, 10 tickets |

The rankings rest on 1–3 big hits each. Several (13, 22, 23, 30) owe almost all their return to a single jackpot draw, and 18, 23 and 26–30 show an edge in only one half of the history.

## Tier 3: one earlier big hit, mostly in one stretch (31–52)

| # | Game | Lead | Note |
|---|---|---|---|
| 31 | Star | mars_combust × aspect_moon_mercury | |
| 32 | Supreme | venus_retrograde × venus_d30 | |
| 33 | Magnum | lagna_navamsa_lord × vargottama_count | |
| 34 | Magnum | day_vs_year_branch × jupiter_d7 | |
| 35 | Star | aspect_sun_mars × aspect_moon_venus | |
| 36 | Magnum | aspect_venus_jupiter × universal_day | |
| 37 | Star | rahu_rashi × vargottama_d10_count | |
| 38 | Star | samvatsara × vargottama_d24_count | |
| 39 | Supreme | kp_sun_star_lord × day_stem | |
| 40 | Supreme | kp_sun_number × lagna_d7 | |
| 41 | Star | rahu_nakshatra × kp_asc_sub_lord | |
| 42 | Magnum | sun_rashi × nayin_element | |
| 43 | Star | hour_stem_19h × sun_sign_tropical | |
| 44 | Power | masa × day_god | |
| 45 | Magnum | paksha × venus_rashi | System 10 format |
| 46 | Star | karana × masa | |
| 47 | Star | hora_lord × mars_combust | |
| 48 | Magnum | mercury_nakshatra × saturn_combust | 10 tickets format |
| 49 | Star | hora_lord × mars_retrograde | |
| 50 | Magnum | mercury_rashi × kp_asc_sub_lord | |
| 51 | Power | masa × adhika_masa | |
| 52 | Power | mercury_nakshatra × aspects_soft | |

- **Same Grand draw:** 33 and 34 share one Grand-winning draw on 21 Jan 2026.
- **One big hit only:** 44 and 51 have nothing beyond the jackpot draw they were picked for.

## Tier 4: only hits are in the draws they were picked on, or none at all (53–75)

| # | Game | Lead | High hits |
|---|---|---|---|
| 53 | Magnum | ayana × kp_moon_star_lord | none |
| 54 | Star | lagna_rashi × day_officer | |
| 55 | Magnum | mercury_rashi × kp_asc_sub_lord | none |
| 56 | Star | hora_lord × adhika_masa | |
| 57 | Power | month_branch × aspect_venus_jupiter | |
| 58 | Supreme | nakshatra × nayin | |
| 59 | Star | hora_lord × mars_combust | |
| 60 | Power | lagna_nakshatra × rahu_navamsa | |
| 61 | Star | sun_rashi × planets_with_moon | |
| 62 | Star | karana × aspect_venus_mars | |
| 63 | Magnum | saturn_combust × plum_trigrams | |
| 64 | Magnum | mars_retrograde × moon_phase | none |
| 65 | Star | aspect_mars_saturn × mars_navamsa | |
| 66 | Supreme | lagna_rashi × lunar_day | |
| 67 | Magnum | mercury_rashi × day_branch | none |
| 68 | Magnum | day_element × lagna_navamsa_lord | none |
| 69 | Power | month_branch × aspects_soft | |
| 70 | Supreme | sun_nakshatra × lunar_month | |
| 71 | Magnum | kp_sun_sub_lord × year_yinyang | none |
| 72 | Supreme | kp_moon_number × nayin_element | |
| 73 | Magnum | mars_rashi × month | none |
| 74 | Magnum | month_stem × kp_ruling_planets | none |
| 75 | Power | kp_sun_star_lord × month_pillar | none |

- **Picked for a recent hit:** they were added for a hit in the last 10 draws or on 18 Oct, and have no earlier high hits. That includes the 18 Oct winners: karana × aspect_venus_mars, which won RM112k, and month_branch × aspects_soft.
- **Leads with no high hits at all** (53, 55, 64, 67, 68, 71, 73, 74, 75) were picked for frequent small wins, and over the whole history they barely beat or fall below their shifted calendars. Of these, 71, 73, 74 and 75 are effectively no better than chance.

## Overall

- **Most trustworthy:** #3 Power year_stem × lagna_navamsa_lord and #7 Supreme plum_trigrams × saturn_navamsa. Each has three high hits spread over several years, all before they were chosen, and no jackpot inflating the return.
- **Big returns come from one draw:** the very high returns (5,000% to 72,000%) almost always come from one jackpot draw, and one draw can't show a lead works.
- **Low numbers for the shifted calendars:** their typical return (about 20% for Magnum Life) sits below the 55% random average because a typical calendar wins no jackpot.

The full table, each lead's reasons and every high-hit date are in `analysis/WATCH_RANK.md` (built by `analysis/watch_rank.py`); both are committed and pushed. The real test starts with Wednesday's results update, which will score every lead on the 21 Oct draw.

---

**User:**

> For today’s, prediction for all the leads, rank from best to worse and tell me the numbers

**Answer:**

Checking 4dmoon for any draw since 18 Oct (e.g. a Tuesday special) before building today's numbers.

**Answer:**

4dmoon still shows 18 Oct as the latest result for all four games, so the history is current. Generating today's numbers.

**Answer:**

Here are the numbers for today's draw (Wed 21 Oct) from all 69 watchlist leads, ranked best to worst using the ranking from my last message. That's 75 entries, because 6 leads are played in two formats.

4dmoon still shows 18 Oct as the latest draw for every game, so the numbers use all draws up to 18 Oct plus today's astrological values.

**How to read the numbers:**
- **System 7 / 8 / 9 / 10:** the full set of numbers to play. "× 2" means two systems, separated by "/".
- **10 tickets (Magnum Life) and 10 sets (Toto):** the "core" numbers go on every ticket. The rest of each ticket is filled from the "rotate" numbers: 3 of 6 per ticket. The exact 10 tickets are in `analysis/PREDICT_2026-10-21.md`.

| # | Game | Lead (pattern) | Format | Numbers |
|---|---|---|---|---|
| 1 | Star | day_of_month × aspect_venus_jupiter (hot/cold100) | System 7 × 2 disjoint | 04 07 13 23 24 29 30 / 32 33 34 41 42 44 50 |
| 2 | Power | sun_sign_tropical × aspect_moon_saturn (hot+100) | System 8 | 04 11 14 26 28 31 46 54 |
| 3 | Power | year_stem × lagna_navamsa_lord (cold) | 10 sets | core 25 35 36 + rotate 01 02 07 27 49 53 |
| 4 | Star | nayin_element × plum_trigrams (pos@last10) | System 7 × 2 overlap | 14 19 23 26 32 34 42 / 14 17 19 23 32 45 49 |
| 5 | Magnum | aspect_mars_jupiter × rahu_d27 (hot/cold100) | 10 tickets | core 06 17 29 31 32 + rotate 02 07 11 14 24 26 |
| 6 | Supreme | moon_rashi × aspects_hard (cold) | System 8 | 04 19 23 33 34 51 52 55 |
| 7 | Supreme | plum_trigrams × saturn_navamsa (hot/cold100) | 10 sets | core 22 23 57 + rotate 09 18 25 30 37 39 |
| 8 | Magnum | mercury_nakshatra × saturn_combust (cold) | System 10 | 07 10 14 20 22 27 28 30 31 36 |
| 9 | Power | lunar_month × sun_sign_tropical (hot+100) | System 8 | 11 14 26 28 30 31 37 46 |
| 10 | Magnum | pof_rashi × aspect_venus_jupiter (cold) | System 9 × 2 overlap | 03 19 22 23 24 27 33 34 36 / 06 15 19 22 23 24 26 33 34 |
| 11 | Supreme | nakshatra × sun_sign_tropical (hot+100) | 10 sets | core 16 34 42 + rotate 10 40 41 48 54 55 |
| 12 | Supreme | kp_asc_star_lord × year_pillar (hot/cold100) | System 7 × 2 overlap | 04 12 14 39 40 46 51 / 05 12 29 36 39 46 51 |
| 13 | Power | pof_sign × moon_d27_lord (hot+100) | 10 sets | core 13 26 47 + rotate 19 22 28 34 50 52 |
| 14 | Power | lagna_rashi × saturn_retrograde (hot+100) | System 7 × 2 overlap | 14 28 32 33 47 48 52 / 13 15 28 33 47 49 52 |
| 15 | Magnum | day_pillar × aspect_jupiter_saturn (pos) | System 10 | 02 05 06 11 13 15 18 19 25 29 |
| 16 | Power | sun_sign_tropical × aspect_moon_saturn (hot+100) | 10 sets | core 11 26 28 + rotate 04 14 20 31 46 54 |
| 17 | Power | mars_combust × aspect_jupiter_saturn (cold/hot100) | 10 sets | core 26 47 51 + rotate 13 19 28 32 48 52 |
| 18 | Magnum | day_element × aspect_moon_jupiter (hot@last_round) | 10 tickets | core 01 11 13 24 30 + rotate 09 12 27 29 31 36 |
| 19 | Star | saturn_retrograde × nayin (hot) | 10 sets | core 16 18 24 + rotate 19 20 25 29 35 39 |
| 20 | Magnum | aspect_moon_mars × aspect_mercury_mars (cold+100) | System 10 | 04 13 14 17 20 24 26 31 32 36 |
| 21 | Magnum | ayana × lunar_leap_month (hot+100) | System 9 × 2 disjoint | 02 03 10 15 16 23 25 28 30 / 06 09 12 18 19 21 27 33 35 |
| 22 | Power | saturn_d24 (hot+100) | 10 sets | core 28 47 50 + rotate 11 15 26 37 44 52 |
| 23 | Magnum | moon_phase × lagna_d24 (hot/cold100) | 10 tickets | core 24 26 29 31 32 + rotate 07 11 13 17 18 21 |
| 24 | Star | saturn_retrograde × aspect_mercury_jupiter (cold/hot100) | System 7 × 2 disjoint | 01 02 05 21 28 31 38 / 06 08 09 12 30 42 49 |
| 25 | Magnum | aspect_venus_jupiter × sun_navamsa (cold/hot100) | System 10 | 03 09 14 15 19 20 24 28 30 35 |
| 26 | Magnum | day_element × aspect_moon_jupiter (hot@last_round) | System 9 × 2 overlap | 01 09 11 12 13 24 27 30 36 / 01 04 09 11 13 24 29 30 31 |
| 27 | Magnum | moon_sign_tropical × sun_navamsa (cold/hot100) | System 9 × 2 disjoint | 08 09 14 19 21 28 30 35 36 / 01 03 06 10 15 22 24 25 27 |
| 28 | Supreme | saturn_rashi × kp_asc_star_lord (cold+100) | System 7 × 2 disjoint | 04 09 20 23 28 37 56 / 02 11 13 18 32 39 47 |
| 29 | Magnum | mercury_combust × aspects_soft (cold/hot100) | System 9 × 2 disjoint | 03 04 08 09 13 14 23 25 36 / 10 18 19 20 21 28 30 33 35 |
| 30 | Magnum | paksha × venus_rashi (cold) | 10 tickets | core 05 07 14 29 32 + rotate 01 12 18 20 24 34 |
| 31 | Star | mars_combust × aspect_moon_mercury (hot/cold100) | 10 sets | core 23 34 42 + rotate 31 39 44 45 47 49 |
| 32 | Supreme | venus_retrograde × venus_d30 (cold/hot100) | System 7 × 2 disjoint | 03 11 15 16 19 34 42 / 08 18 27 31 43 48 54 |
| 33 | Magnum | lagna_navamsa_lord × vargottama_count (hot/cold100) | System 9 × 2 disjoint | 04 06 07 14 22 24 26 29 34 / 02 03 05 11 13 30 32 35 36 |
| 34 | Magnum | day_vs_year_branch × jupiter_d7 (hot/cold100) | System 9 × 2 overlap | 02 05 11 12 13 21 26 29 31 / 02 11 12 14 17 21 23 26 31 |
| 35 | Star | aspect_sun_mars × aspect_moon_venus (hot/cold100) | System 7 × 2 disjoint | 13 32 36 39 40 44 47 / 12 14 16 18 20 30 35 |
| 36 | Magnum | aspect_venus_jupiter × universal_day (hot) | System 9 × 2 overlap | 02 08 12 15 19 23 25 29 31 / 02 07 08 14 15 23 25 28 29 |
| 37 | Star | rahu_rashi × vargottama_d10_count (pos) | System 8 | 03 06 08 09 12 26 39 50 |
| 38 | Star | samvatsara × vargottama_d24_count (cold) | 10 sets | core 13 27 29 + rotate 18 24 34 38 39 44 |
| 39 | Supreme | kp_sun_star_lord × day_stem (hot) | System 7 × 2 disjoint | 08 09 27 36 40 44 50 / 04 05 31 39 47 52 55 |
| 40 | Supreme | kp_sun_number × lagna_d7 (pos) | System 8 | 08 19 20 26 46 48 53 56 |
| 41 | Star | rahu_nakshatra × kp_asc_sub_lord (hot) | System 8 | 08 09 17 19 28 34 45 47 |
| 42 | Magnum | sun_rashi × nayin_element (cold/hot100@decay10) | System 9 × 2 overlap | 09 10 15 19 20 25 28 30 33 / 09 10 13 16 19 25 28 30 35 |
| 43 | Star | hour_stem_19h × sun_sign_tropical (pos) | System 8 | 14 19 25 32 33 35 42 45 |
| 44 | Power | masa × day_god (hot) | 10 sets | core 15 17 40 + rotate 09 20 23 32 37 46 |
| 45 | Magnum | paksha × venus_rashi (cold) | System 10 | 05 07 12 14 18 20 24 29 32 34 |
| 46 | Star | karana × masa (cold) | System 8 | 02 07 18 20 22 29 33 42 |
| 47 | Star | hora_lord × mars_combust (cold/hot100) | 10 sets | core 09 10 31 + rotate 05 17 20 22 35 48 |
| 48 | Magnum | mercury_nakshatra × saturn_combust (cold) | 10 tickets | core 07 20 22 27 28 + rotate 08 10 14 30 31 36 |
| 49 | Star | hora_lord × mars_retrograde (cold) | 10 sets | core 09 10 22 + rotate 05 07 14 20 34 40 |
| 50 | Magnum | mercury_rashi × kp_asc_sub_lord (cold+100) | System 10 | 05 06 07 08 11 12 17 26 31 34 |
| 51 | Power | masa × adhika_masa (hot+100) | System 8 | 11 14 26 28 31 37 46 54 |
| 52 | Power | mercury_nakshatra × aspects_soft (cold/hot100) | System 7 × 2 disjoint | 11 13 26 28 44 47 52 / 14 21 23 32 35 38 50 |
| 53 | Magnum | ayana × kp_moon_star_lord (pos) | System 9 × 2 overlap | 06 12 16 23 25 27 28 29 34 / 06 09 12 16 21 23 27 28 32 |
| 54 | Star | lagna_rashi × day_officer (cold) | System 7 × 2 disjoint | 08 14 16 27 30 46 47 / 03 04 09 21 31 34 49 |
| 55 | Magnum | mercury_rashi × kp_asc_sub_lord (cold+100) | System 9 × 2 overlap | 05 06 07 08 11 12 17 26 31 / 05 07 08 12 20 26 31 32 34 |
| 56 | Star | hora_lord × adhika_masa (cold) | 10 sets | core 09 10 14 + rotate 05 07 22 24 32 40 |
| 57 | Power | month_branch × aspect_venus_jupiter (hot+100) | System 8 | 04 11 14 26 28 31 37 46 |
| 58 | Supreme | nakshatra × nayin (hot+100) | 10 sets | core 05 19 43 + rotate 07 15 16 17 34 36 |
| 59 | Star | hora_lord × mars_combust (cold/hot100) | System 7 × 2 overlap | 05 09 10 17 22 31 35 / 05 09 10 20 24 31 48 |
| 60 | Power | lagna_nakshatra × rahu_navamsa (hot+100) | 10 sets | core 18 33 47 + rotate 14 26 31 36 37 52 |
| 61 | Star | sun_rashi × planets_with_moon (cold) | System 8 | 10 14 18 28 37 40 41 45 |
| 62 | Star | karana × aspect_venus_mars (hot@last5) | System 8 | 05 07 23 25 28 31 36 40 |
| 63 | Magnum | saturn_combust × plum_trigrams (cold) | System 10 | 04 06 08 11 13 14 15 24 26 34 |
| 64 | Magnum | mars_retrograde × moon_phase (hot/cold100) | System 9 × 2 disjoint | 02 05 07 08 11 26 29 31 34 / 01 06 12 14 17 23 25 32 36 |
| 65 | Star | aspect_mars_saturn × mars_navamsa (cold+100) | System 7 × 2 disjoint | 11 24 26 29 36 41 44 / 01 02 07 19 25 46 50 |
| 66 | Supreme | lagna_rashi × lunar_day (hot/cold100) | System 8 | 04 12 13 23 28 29 39 44 |
| 67 | Magnum | mercury_rashi × day_branch (cold+100) | System 9 × 2 overlap | 02 04 06 07 11 13 17 26 31 / 04 05 06 11 17 24 26 31 32 |
| 68 | Magnum | day_element × lagna_navamsa_lord (pos) | 10 tickets | core 09 10 21 22 25 + rotate 15 16 27 30 32 35 |
| 69 | Power | month_branch × aspects_soft (cold@decay10) | System 8 | 04 06 17 26 27 35 36 44 |
| 70 | Supreme | sun_nakshatra × lunar_month (cold/hot100) | System 7 × 2 overlap | 03 05 15 16 19 34 42 / 01 03 15 18 21 34 42 |
| 71 | Magnum | kp_sun_sub_lord × year_yinyang (hot) | System 10 | 06 07 15 17 19 24 25 27 31 35 |
| 72 | Supreme | kp_moon_number × nayin_element (hot+100) | System 7 × 2 overlap | 15 16 17 19 34 42 48 / 03 15 16 19 34 53 54 |
| 73 | Magnum | mars_rashi × month (cold) | System 10 | 01 04 07 12 13 17 23 29 31 32 |
| 74 | Magnum | month_stem × kp_ruling_planets (hot/cold100) | System 9 × 2 disjoint | 06 15 17 22 23 26 29 31 33 / 04 07 10 11 12 24 25 32 34 |
| 75 | Power | kp_sun_star_lord × month_pillar (hot+100) | 10 sets | core 11 28 31 + rotate 07 26 32 44 46 52 |

**Numbers that come up across many leads today:**
- **Power:** 11, 14, 26, 28, 31, 46 and 47 appear in most of the leads.
- **Magnum Life:** 24, 29 and 31 come up often.
- **Supreme:** 34 and 42 come up often.
- **Star:** the leads disagree; there is no clear shared group.

**Cost:** playing every entry would cost about RM1,687: Magnum Life RM717, Star RM326, Power RM248, Supreme RM396. None of these leads has yet beaten chance on draws it hadn't seen, so this is a test, not an expected profit.

Tonight's scheduled update (21:30 Malaysia time) will fetch the results and score every entry above with the same numbers. Full ticket lists are in `analysis/PREDICT_2026-10-21.md` and `analysis/predict_2026-10-21.csv`; everything is committed and pushed.

---

**User:**

> Ok based on all those leads what are the common numbers for Power, Magnum Life and Supreme, Star assuming that I’m buying. 5 tickets for each of them

**Answer:**

Here are 5 tickets per game for today, built from the numbers all the leads agree on most.

**How they were picked:**
- **Points per lead:** each lead counts once and gives points to its top 12 numbers, most to its first choice.
- **Weighting:** leads higher in the ranking count for more.
- **Ticket layout:** the strongest numbers go on all 5 tickets (6 for Magnum Life, 4 for Toto). Each ticket then gets 2 different numbers from the next ten, so 5 tickets cover 14 numbers in Toto and 16 in Magnum Life.

The number in brackets is how many leads pick that number.

### Magnum Life (8 numbers per ticket, 25 leads, RM5)
On every ticket: **14 19 24 28 29 31**
1. 14 19 24 **26 30** 28 29 31 → 14 19 24 26 28 29 30 31
2. 07 13 14 19 24 28 29 31
3. 11 14 19 24 28 29 31 32
4. 14 15 19 24 28 29 31 36
5. 06 14 19 23 24 28 29 31

The strongest agreement is on 24 (11), 29 (12), 14 (10), 31 (12) and 26 (11). Number 07 is also picked by 12 leads, but mostly lower down their lists.

### Star Toto (6 numbers, 18 leads, RM5)
On every ticket: **09 14 23 24**
1. 09 14 19 23 24 29
2. 09 13 14 23 24 34
3. 09 14 23 24 39 42
4. 07 09 14 23 24 44
5. 09 14 23 24 32 40

The leads agree least here: no number appears in more than 6 of 18 leads.

### Power Toto (6 numbers, 14 leads, RM5)
On every ticket: **11 26 28 47**
1. 11 14 26 28 47 52
2. 11 26 28 31 46 47
3. 11 13 26 28 37 47
4. 11 26 28 32 47 50
5. 01 04 11 26 28 47

This is the strongest consensus of the four games: 26 is in 11 of 14 leads and 28 in 10.

### Supreme Toto (6 numbers, 12 leads, RM10)
On every ticket: **04 23 34 39**
1. 04 16 19 23 34 39
2. 04 23 34 39 40 51
3. 04 09 23 34 39 42
4. 04 15 23 34 39 46
5. 04 23 34 37 39 55

Numbers 34 and 19 are each in 6 of 12 leads.

All 20 tickets cost RM25 in total. Mixing many leads doesn't add an edge that none of them showed on their own: each ticket has the same odds as any other 6 or 8 numbers. Treat it as a test.

The tickets are saved in `analysis/CONSENSUS_2026-10-21.md` and pushed. Tonight's 21:30 update will score them along with every lead.

---

**User:**

> Ok now check the latest result for today in google and tell me how they perform today and also for the last 3 days

**Answer:**

Results are in and the scoring ran. Checking the numbers match what I gave you this morning, then summarising.

**Answer:**

Today was a bad night: across all four games the leads returned RM105 on RM1,687, and none of your 20 consensus tickets won anything. The draw numbers run straight on from 18 Oct, so there was no Tuesday special draw.

Today's results (from 4dnow.app):

| Game | Result |
|---|---|
| Magnum Life | 03 16 18 26 29 32 35 36, bonus 10, 24 |
| Star Toto | 08 10 25 35 41 49, bonus 36 |
| Power Toto | 08 17 25 27 47 54 |
| Supreme Toto | 23 32 49 50 51 52 |

## Today (21 Oct)

Today is the only fair test: I gave you the numbers before the draw, and no lead was picked because of this draw.

**All 75 leads together:**
- Only 2 won a prize:
  - #23 Magnum Life moon_phase × lagna_d24, 10 tickets: 4 numbers plus a bonus ball, RM25.
  - #6 Supreme moon_rashi × aspects_hard, System 8: 3 numbers, RM80.
- No Star or Power lead won anything.
- Total: RM1,687 staked, RM105 back.

**Your 20 consensus tickets: RM0.**
- **Magnum Life:** at best 2 numbers plus bonus 24. That's 29 plus 26, 32 or 36, and Magnum Life pays nothing below 4 + bonus.
- **Star:** nothing matched.
- **Power:** 47 on all 5 tickets, 1 number each.
- **Supreme:** 23 on every ticket and 51 on one, so at most 2 numbers.

## The 3 draws before today

Each date uses numbers built only from the draws before it, so these are the tickets you would have got that morning. But many leads were added to the watchlist *because* of these draws, especially the 18 Oct winners, so these figures are flattered by hindsight.

| Draw | Stake (all 75) | Paid back | Main wins | Consensus tickets |
|---|---|---|---|---|
| Wed 14 Oct | RM1,687 | RM13,750 | Star saturn_retrograde × aspect_mercury_jupiter 5 numbers RM4,156; Magnum Life mercury_rashi × kp_asc_sub_lord 6 + 2 bonus RM4,930 | RM0 (best: Magnum Life 3 + 2 bonus) |
| Sat 17 Oct | RM1,687 | RM37,246 | Supreme lagna_rashi × lunar_day 5 numbers RM21,944; Supreme saturn_rashi × kp_asc_star_lord 5 numbers RM14,176 | RM0 (best: Magnum Life 3 numbers) |
| Sun 18 Oct | RM1,687 | RM283,102 | Star karana × aspect_venus_mars 5 + bonus RM112,216; Magnum Life mercury_combust × aspects_soft 7 + bonus RM110,200 | RM0 (best: Star 2 numbers) |
| **Wed 21 Oct** | RM1,687 | **RM105** | see above | **RM0** |

## What this shows

- **Hindsight decided the earlier wins.** On 14, 17 and 18 Oct the leads won big largely because they were chosen after seeing those draws. Most of the big 18 Oct wins came from leads ranked low (#25 to #69) that were added because of that draw.
- **The top-ranked leads didn't deliver either.** The ten ranked highest won almost nothing on any of the four days.
- **Consensus tickets haven't paid yet.** Across all 4 draws they won nothing. Blending the leads makes the tickets steady but not luckier.

One clean draw is far too few to judge on. I'll keep scoring each new draw without changing the list; that is the only honest way to find out whether any lead holds up.

The results are added to the data, and the per-ticket scores are in `analysis/CONSENSUS_SCORED.md` and `analysis/WATCH_LOG.md`, all pushed. Tonight's 21:30 scheduled update will find today's results already in and just re-score them.

---

**User:**

> No I mean create a table to see how each of those 75 leads perform for the last 3 days until today

**Answer:**

Here is how each of the 75 leads did on the last 3 draws and today: 14 Oct (Wed), 17 Oct (Sat), 18 Oct (Sun) and 21 Oct (Wed, today). Leads are in rank order. Each cell shows the best match, then the profit after the stake. For example, "5+1B / +4,142" means 5 numbers plus a bonus ball, ahead by RM4,142 that draw. B = bonus ball.

| # | Game | Lead (pattern) | Format | Stake | 14 Oct | 17 Oct | 18 Oct | 21 Oct | Total |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Star | day_of_month × aspect_venus_jupiter (hot/cold100) | Sys 7 × 2 disj | 14 | 1 / −14 | 1 / −14 | 0+1B / −14 | 1 / −14 | **−56** |
| 2 | Power | sun_sign_tropical × aspect_moon_saturn (hot+100) | Sys 8 | 28 | 1 / −28 | 0 / −28 | 2 / −28 | 1 / −28 | **−112** |
| 3 | Power | year_stem × lagna_navamsa_lord (cold) | 10 sets | 10 | 1 / −10 | 1 / −10 | 2 / −10 | 2 / −10 | **−40** |
| 4 | Star | nayin_element × plum_trigrams (pos@last10) | Sys 7 × 2 ovl | 14 | 1+1B / −14 | 1 / −14 | **5 / +4,174** | 1 / −14 | **+4,132** |
| 5 | Magnum | aspect_mars_jupiter × rahu_d27 (hot/cold100) | 10 tickets | 10 | 4+1B / −5 | 1+1B / −10 | 0+1B / −10 | 3+1B / −10 | **−35** |
| 6 | Supreme | moon_rashi × aspects_hard (cold) | Sys 8 | 56 | 1 / −56 | 0 / −56 | 0 / −56 | 3 / +24 | **−144** |
| 7 | Supreme | plum_trigrams × saturn_navamsa (hot/cold100) | 10 sets | 20 | 2 / −20 | 2 / −20 | 0 / −20 | 1 / −20 | **−80** |
| 8 | Magnum | mercury_nakshatra × saturn_combust (cold) | Sys 10 | 45 | 1+2B / −45 | 4+1B / +5 | 3 / −45 | 1+1B / −45 | **−130** |
| 9 | Power | lunar_month × sun_sign_tropical (hot+100) | Sys 8 | 28 | 2 / −28 | 0 / −28 | 2 / −28 | 0 / −28 | **−112** |
| 10 | Magnum | pof_rashi × aspect_venus_jupiter (cold) | Sys 9 × 2 ovl | 18 | 3+1B / −18 | 2 / −18 | 1+1B / −18 | 2+1B / −18 | **−72** |
| 11 | Supreme | nakshatra × sun_sign_tropical (hot+100) | 10 sets | 20 | 0 / −20 | 0 / −20 | 0 / −20 | 0 / −20 | **−80** |
| 12 | Supreme | kp_asc_star_lord × year_pillar (hot/cold100) | Sys 7 × 2 ovl | 28 | 1 / −28 | 1 / −28 | 1 / −28 | 1 / −28 | **−112** |
| 13 | Power | pof_sign × moon_d27_lord (hot+100) | 10 sets | 10 | 2 / −10 | 0 / −10 | 1 / −10 | 1 / −10 | **−40** |
| 14 | Power | lagna_rashi × saturn_retrograde (hot+100) | Sys 7 × 2 ovl | 14 | 2 / −14 | 0 / −14 | 1 / −14 | 1 / −14 | **−56** |
| 15 | Magnum | day_pillar × aspect_jupiter_saturn (pos) | Sys 10 | 45 | 4+1B / +5 | 4+1B / +5 | 1+1B / −45 | 2 / −45 | **−80** |
| 16 | Power | sun_sign_tropical × aspect_moon_saturn (hot+100) | 10 sets | 10 | 1 / −10 | 0 / −10 | 2 / −10 | 1 / −10 | **−40** |
| 17 | Power | mars_combust × aspect_jupiter_saturn (cold/hot100) | 10 sets | 10 | 1 / −10 | 2 / −10 | 1 / −10 | 1 / −10 | **−40** |
| 18 | Magnum | day_element × aspect_moon_jupiter (hot@last_round) | 10 tickets | 10 | 0+2B / −10 | 1 / −10 | 2 / −10 | 2+1B / −10 | **−40** |
| 19 | Star | saturn_retrograde × nayin (hot) | 10 sets | 10 | 0 / −10 | 1 / −10 | 2 / −10 | 2 / −10 | **−40** |
| 20 | Magnum | aspect_moon_mars × aspect_mercury_mars (cold+100) | Sys 10 | 45 | 4+2B / +55 | 4 / −45 | 1 / −45 | 3+1B / −45 | **−80** |
| 21 | Magnum | ayana × lunar_leap_month (hot+100) | Sys 9 × 2 disj | 18 | 3 / −18 | 1+2B / −18 | 5+2B / +212 | 2+1B / −18 | **+158** |
| 22 | Power | saturn_d24 (hot+100) | 10 sets | 10 | 1 / −10 | 1 / −10 | 1 / −10 | 1 / −10 | **−40** |
| 23 | Magnum | moon_phase × lagna_d24 (hot/cold100) | 10 tickets | 10 | 3+1B / −10 | 2 / −10 | 1+1B / −10 | 4+1B / +15 | **−15** |
| 24 | Star | saturn_retrograde × aspect_mercury_jupiter (cold/hot100) | Sys 7 × 2 disj | 14 | **5 / +4,142** | 0+1B / −14 | 2 / −14 | 2 / −14 | **+4,100** |
| 25 | Magnum | aspect_venus_jupiter × sun_navamsa (cold/hot100) | Sys 10 | 45 | 3 / −45 | 0 / −45 | **7 / +20,265** | 2+1B / −45 | **+20,130** |
| 26 | Magnum | day_element × aspect_moon_jupiter (hot@last_round) | Sys 9 × 2 ovl | 18 | 0+2B / −18 | 1 / −18 | 3 / −18 | 1+1B / −18 | **−72** |
| 27 | Magnum | moon_sign_tropical × sun_navamsa (cold/hot100) | Sys 9 × 2 disj | 18 | 2 / −18 | 2+2B / −18 | **7 / +12,682** | 2 / −18 | **+12,628** |
| 28 | Supreme | saturn_rashi × kp_asc_star_lord (cold+100) | Sys 7 × 2 disj | 28 | 2 / −28 | **5 / +14,148** | 1 / −28 | 1 / −28 | **+14,064** |
| 29 | Magnum | mercury_combust × aspects_soft (cold/hot100) | Sys 9 × 2 disj | 18 | 3 / −18 | 2 / −18 | **7+1B / +110,182** | 2+1B / −18 | **+110,128** |
| 30 | Magnum | paksha × venus_rashi (cold) | 10 tickets | 10 | 3+1B / −10 | 3+1B / −10 | 3+1B / −10 | 3+1B / −10 | **−40** |
| 31 | Star | mars_combust × aspect_moon_mercury (hot/cold100) | 10 sets | 10 | 1 / −10 | 2 / −10 | 1 / −10 | 1 / −10 | **−40** |
| 32 | Supreme | venus_retrograde × venus_d30 (cold/hot100) | Sys 7 × 2 disj | 28 | 1 / −28 | 1 / −28 | 1 / −28 | 0 / −28 | **−112** |
| 33 | Magnum | lagna_navamsa_lord × vargottama_count (hot/cold100) | Sys 9 × 2 disj | 18 | 5 / +22 | 4 / −18 | 4+1B / +2 | 4 / −18 | **−12** |
| 34 | Magnum | day_vs_year_branch × jupiter_d7 (hot/cold100) | Sys 9 × 2 ovl | 18 | 3+1B / −18 | 2+1B / −18 | 0+2B / −18 | 2 / −18 | **−72** |
| 35 | Star | aspect_sun_mars × aspect_moon_venus (hot/cold100) | Sys 7 × 2 disj | 14 | 1 / −14 | 1 / −14 | 1 / −14 | 1 / −14 | **−56** |
| 36 | Magnum | aspect_venus_jupiter × universal_day (hot) | Sys 9 × 2 ovl | 18 | 2 / −18 | 3+1B / −18 | 3 / −18 | 1 / −18 | **−72** |
| 37 | Star | rahu_rashi × vargottama_d10_count (pos) | Sys 8 | 28 | 2 / −28 | 2 / −28 | 2 / −28 | 1 / −28 | **−112** |
| 38 | Star | samvatsara × vargottama_d24_count (cold) | 10 sets | 10 | 1 / −10 | 2 / −10 | 0+1B / −10 | 0 / −10 | **−40** |
| 39 | Supreme | kp_sun_star_lord × day_stem (hot) | Sys 7 × 2 disj | 28 | 2 / −28 | 4 / +244 | 1 / −28 | 1 / −28 | **+160** |
| 40 | Supreme | kp_sun_number × lagna_d7 (pos) | Sys 8 | 56 | 2 / −56 | 1 / −56 | 1 / −56 | 0 / −56 | **−224** |
| 41 | Star | rahu_nakshatra × kp_asc_sub_lord (hot) | Sys 8 | 28 | 2 / −28 | 0+1B / −28 | 1 / −28 | 1 / −28 | **−112** |
| 42 | Magnum | sun_rashi × nayin_element (cold/hot100@decay10) | Sys 9 × 2 ovl | 18 | 1 / −18 | 2+1B / −18 | **7 / +12,682** | 2+1B / −18 | **+12,628** |
| 43 | Star | hour_stem_19h × sun_sign_tropical (pos) | Sys 8 | 28 | 2 / −28 | 2+1B / −28 | 1 / −28 | 2 / −28 | **−112** |
| 44 | Power | masa × day_god (hot) | 10 sets | 10 | 1 / −10 | 0 / −10 | 1 / −10 | 1 / −10 | **−40** |
| 45 | Magnum | paksha × venus_rashi (cold) | Sys 10 | 45 | 3+1B / −45 | 3+1B / −45 | 3+1B / −45 | 3+1B / −45 | **−180** |
| 46 | Star | karana × masa (cold) | Sys 8 | 28 | 0 / −28 | 1 / −28 | 1+1B / −28 | 0 / −28 | **−112** |
| 47 | Star | hora_lord × mars_combust (cold/hot100) | 10 sets | 10 | 1 / −10 | 0 / −10 | 3 / −2 | 2 / −10 | **−32** |
| 48 | Magnum | mercury_nakshatra × saturn_combust (cold) | 10 tickets | 10 | 2+2B / −10 | 4+1B / 0 | 3 / −10 | 1+1B / −10 | **−30** |
| 49 | Star | hora_lord × mars_retrograde (cold) | 10 sets | 10 | 2 / −10 | 1 / −10 | 1 / −10 | 1 / −10 | **−40** |
| 50 | Magnum | mercury_rashi × kp_asc_sub_lord (cold+100) | Sys 10 | 45 | **6+2B / +4,885** | 4 / −45 | 1 / −45 | 1 / −45 | **+4,750** |
| 51 | Power | masa × adhika_masa (hot+100) | Sys 8 | 28 | 2 / −28 | 0 / −28 | 1 / −28 | 1 / −28 | **−112** |
| 52 | Power | mercury_nakshatra × aspects_soft (cold/hot100) | Sys 7 × 2 disj | 14 | 1 / −14 | 1 / −14 | 1 / −14 | 1 / −14 | **−56** |
| 53 | Magnum | ayana × kp_moon_star_lord (pos) | Sys 9 × 2 ovl | 18 | 2 / −18 | 2+1B / −18 | 1+1B / −18 | 2 / −18 | **−72** |
| 54 | Star | lagna_rashi × day_officer (cold) | Sys 7 × 2 disj | 14 | 1 / −14 | 3 / +18 | 2+1B / −14 | 1 / −14 | **−24** |
| 55 | Magnum | mercury_rashi × kp_asc_sub_lord (cold+100) | Sys 9 × 2 ovl | 18 | **6+2B / +2,782** | 4 / −18 | 1 / −18 | 2 / −18 | **+2,728** |
| 56 | Star | hora_lord × adhika_masa (cold) | 10 sets | 10 | 0 / −10 | 1 / −10 | 1 / −10 | 1 / −10 | **−40** |
| 57 | Power | month_branch × aspect_venus_jupiter (hot+100) | Sys 8 | 28 | 2 / −28 | 0 / −28 | 1 / −28 | 0 / −28 | **−112** |
| 58 | Supreme | nakshatra × nayin (hot+100) | 10 sets | 20 | 1 / −20 | 0 / −20 | 2 / −20 | 0 / −20 | **−80** |
| 59 | Star | hora_lord × mars_combust (cold/hot100) | Sys 7 × 2 ovl | 14 | 1 / −14 | 0 / −14 | 2 / −14 | 2 / −14 | **−56** |
| 60 | Power | lagna_nakshatra × rahu_navamsa (hot+100) | 10 sets | 10 | 3 / −7 | 0 / −10 | 0 / −10 | 1 / −10 | **−37** |
| 61 | Star | sun_rashi × planets_with_moon (cold) | Sys 8 | 28 | 2 / −28 | 1 / −28 | 2 / −28 | 2 / −28 | **−112** |
| 62 | Star | karana × aspect_venus_mars (hot@last5) | Sys 8 | 28 | 1 / −28 | 2 / −28 | **5+1B / +112,188** | 1+1B / −28 | **+112,104** |
| 63 | Magnum | saturn_combust × plum_trigrams (cold) | Sys 10 | 45 | 0+2B / −45 | 2 / −45 | 4 / −45 | 1+1B / −45 | **−180** |
| 64 | Magnum | mars_retrograde × moon_phase (hot/cold100) | Sys 9 × 2 disj | 18 | 5+1B / +107 | 4+1B / +2 | 1 / −18 | 2 / −18 | **+73** |
| 65 | Star | aspect_mars_saturn × mars_navamsa (cold+100) | Sys 7 × 2 disj | 14 | 1 / −14 | 3 / +18 | 2 / −14 | 1+1B / −14 | **−24** |
| 66 | Supreme | lagna_rashi × lunar_day (hot/cold100) | Sys 8 | 56 | 1 / −56 | **5 / +21,888** | 2 / −56 | 1 / −56 | **+21,720** |
| 67 | Magnum | mercury_rashi × day_branch (cold+100) | Sys 9 × 2 ovl | 18 | 4+1B / +2 | 2 / −18 | 1 / −18 | 2+1B / −18 | **−52** |
| 68 | Magnum | day_element × lagna_navamsa_lord (pos) | 10 tickets | 10 | 0+2B / −10 | 2 / −10 | 2 / −10 | 3+1B / −10 | **−40** |
| 69 | Power | month_branch × aspects_soft (cold@decay10) | Sys 8 | 28 | 0 / −28 | 1 / −28 | **5 / +10,502** | 2 / −28 | **+10,418** |
| 70 | Supreme | sun_nakshatra × lunar_month (cold/hot100) | Sys 7 × 2 ovl | 28 | 1 / −28 | 0 / −28 | 0 / −28 | 0 / −28 | **−112** |
| 71 | Magnum | kp_sun_sub_lord × year_yinyang (hot) | Sys 10 | 45 | 3 / −45 | 5+2B / +525 | 2+2B / −45 | 1+1B / −45 | **+390** |
| 72 | Supreme | kp_moon_number × nayin_element (hot+100) | Sys 7 × 2 ovl | 28 | 3 / +4 | 1 / −28 | 1 / −28 | 0 / −28 | **−80** |
| 73 | Magnum | mars_rashi × month (cold) | Sys 10 | 45 | 3+1B / −45 | 4+1B / +5 | 3 / −45 | 2 / −45 | **−130** |
| 74 | Magnum | month_stem × kp_ruling_planets (hot/cold100) | Sys 9 × 2 disj | 18 | **6+1B / +1,462** | 5 / +22 | 1 / −18 | 2 / −18 | **+1,448** |
| 75 | Power | kp_sun_star_lord × month_pillar (hot+100) | 10 sets | 10 | 3 / −1 | 0 / −10 | 1 / −10 | 0 / −10 | **−31** |
| | | **All 75** | | **1,687** | **+12,063** | **+35,559** | **+281,415** | **−1,582** | **+327,455** |

**What the table shows:**
- **Only today is a fair test.** Today the 75 leads together lost RM1,582: just #6 (+RM24) and #23 (+RM15) made a profit.
- **The big profits on 14–18 Oct are hindsight.** Most of those leads were added to the watchlist because they won on those very draws. Examples are #29, #62 and #69 on 18 Oct, and #28 and #66 on 17 Oct. Their profits mostly show how they were chosen, not that they predicted anything.
- **The top-ranked leads (#1–#20) lost on almost every draw.** The only exceptions are small RM5–55 wins for #15 and #20, plus one 5-number Star hit for #4 on 18 Oct.
- **No lead won twice in the four draws.** The only one to win on more than one draw was #64, with small prizes on 14 and 17 Oct (+RM73 in total).
- **Some leads barely change.** #30 and #45 (paksha × venus_rashi) got exactly 3 + bonus every draw, because their numbers hardly move from draw to draw.

The table is saved in `analysis/WATCH_TABLE_2026-10-21.md` and pushed. Each new draw will be added as I keep scoring.

**Answer:**

The scheduled 21:30 results update has run; 4dmoon wasn't needed because today's results were already in from 4dnow.app this evening. The watchlist scoring ran on them, and I've now also scored all 45,892 leads on today's draw. Everything is committed and pushed.

**Watchlist today (21 Oct), all 75 entries:** RM1,687 staked, RM105 back. Only two made a profit:
- #6 Supreme moon_rashi × aspects_hard, System 8: 3 numbers, RM80.
- #23 Magnum Life moon_phase × lagna_d24, 10 tickets: 4 numbers plus a bonus ball, RM25.

None of the 20 consensus tickets won.

**Running totals for 14, 17, 18 and 21 Oct**, as in the per-lead table:

| Draw | Watchlist profit |
|---|---|
| 14 Oct | +RM12,063 |
| 17 Oct | +RM35,559 |
| 18 Oct | +RM281,415 |
| 21 Oct | **−RM1,582** |
| Total | +RM327,455 |

The earlier three draws are flattered by hindsight, because many leads were added after winning on those very draws. Today is the only draw where every lead was fixed beforehand, and the watchlist lost almost the whole stake on it.

**Best of all 45,892 leads today (in hindsight):**

| Game | Best lead | Pattern, format | Result | Leads with a prize |
|---|---|---|---|---|
| Magnum Life | aspect_sun_moon × aspect_mars_saturn | pos, System 10 | 7 numbers, RM20,310 | about 7% |
| Star | sun_sign_tropical × aspect_mercury_jupiter | pos, System 7 × 2 overlap | 5 numbers, RM8,312 | about 5–6% |
| Power | rahu_rashi × moon_phase | hot, System 7 × 2 disjoint | 5 numbers, RM6,800 (the only 5+ hit) | about 2–3% |
| Supreme | saturn_retrograde × universal_day | cold, 10 sets | 5 numbers, RM28,032 | about 5–6% |

None of today's top winners was on the watchlist, which repeats the pattern so far: the big winners come from leads nobody would have picked in advance.

The per-lead table is in `analysis/WATCH_TABLE_2026-10-21.md`, today's scores in `analysis/WATCH_LOG.md`, and the all-leads scoring in `analysis/LEADS7_TODAY_2026-10-21.md`.

There is no further update scheduled. I'll score the next draw (Sat 24 Oct) when you ask, or I can schedule it.

---

**User:**

> Just wondering if you have done da liu ren astrological parameters as well?

**Answer:**

No, I haven't tested any Da Liu Ren parameters yet. The Chinese side so far covers:

- the year, month, day and 19:00 hour pillars (stems and branches);
- nayin;
- the 12 day officers;
- the day god;
- the year, month and day Nine Stars;
- the Plum Blossom trigrams;
- the solar terms.

Nothing builds the Liu Ren chart itself.

**What I'd add as a Da Liu Ren family:**
- **Monthly General (月将):** set by the Sun's position, it changes at each major solar term.
- **Heavenly plate:** the Monthly General placed over the hour branch. The draw is always at 19:00, the Xu (戌) hour.
- **Four Lessons (四课):** the upper branch of each lesson.
- **Three Transmissions (三传):** the initial, middle and final branch.
- **The method that produced the transmissions:** 贼克, 比用, 涉害, 遥克, 昂星, 别责, 八专, 伏吟 or 返吟.
- **Noble Person (贵人) and the Twelve Heavenly Generals:** where the Noble Person sits (the evening rule applies at 19:00), and which general sits on the initial transmission.
- **Key combinations:** for example, whether the initial transmission clashes with or combines with the day branch.

That is about 12–15 parameters, tested exactly like D9 and the other divisional charts:
- singly and in pairs with all the other parameters, using all 7 patterns;
- against 20 shifted calendars;
- choosing leads before the last 10 draws, then testing on those 10;
- then on the latest draws.

**One limitation:** because the draw is always at 19:00, the hour never changes. The whole chart then depends only on the Monthly General and the day pillar, so there are at most 12 × 60 = 720 possible charts. The tests already include the day pillar, so part of what Liu Ren captures has been tested indirectly.

Liu Ren's real contribution is grouping those 720 charts in a new way: transmissions, method and generals. That grouping hasn't been tested.

Building and checking the chart takes about an hour. The full analysis run is about 20 minutes, then the reports. Do you want me to go ahead?

---

**User:**

> Tai Yi Shen Shu,Mei Hua Yi Shu ok and what about this 2?

**Answer:**

Mei Hua is only partly covered, and Tai Yi Shen Shu hasn't been done at all.

**Mei Hua Yi Shu (梅花易数): only the main hexagram so far**
- One parameter is tested, `plum_trigrams`: the upper and lower trigram for each draw, using the standard time method.
  - Upper trigram = (year branch + lunar month + lunar day) mod 8.
  - Lower trigram = the same sum plus the hour branch, mod 8. The hour is always Xu (戌) at 19:00.
- It already appears in three watchlist leads:
  - #4 Star nayin_element × plum_trigrams;
  - #7 Supreme plum_trigrams × saturn_navamsa;
  - #63 Magnum Life saturn_combust × plum_trigrams.
- Missing so far, which is where Mei Hua does its actual reading:
  - **Moving line (动爻):** the same sum plus the hour, mod 6.
  - **Changed hexagram (变卦):** the hexagram after the moving line flips.
  - **Mutual hexagram (互卦):** made from lines 2–4 and 3–5.
  - **Ti and Yong (体用):** which trigram is the body and which is the use, set by the moving line.
  - **Ti–Yong element relation:** whether the use trigram supports, drains, controls, is controlled by, or matches the body (生, 泄, 克, 被克, 比和). This is the core of the judgement.
  - **Elements of each trigram,** and whether they are strong for the season.

**Tai Yi Shen Shu (太乙神数): not done at all**
- I would use the daily chart (日计), counting days elapsed since a set starting point (积日).
- The daily chart gives:
  - **Tai Yi's palace:** one of 8 palaces, never the centre.
  - **Wen Chang (文昌), Shi Ji (始击) and Ji Shen (计神):** their positions.
  - **Host and guest calculations (主算 and 客算):** two actual numbers, roughly 1 to 40, that change from day to day.
  - **The host and guest generals and their deputies (主客大将/参将).**
  - **Pattern flags:** for example, the calculation being balanced or not, and conditions like 掩, 迫, 囚 and 击.
- The host and guest calculations are interesting here, because they are numbers that could be tested directly as lottery-number rules, not just as categories.
- One caveat: Tai Yi schools disagree on the starting point and some rules. I would use the 太乙统宗 standard rules and flag that I haven't checked them against a printed almanac, as with the Nine Star calendar.

**Same limitation as Da Liu Ren:** the draw is always at 19:00, so none of these charts uses a changing hour. Everything depends only on the date: the solar term, the lunar date and the day count. The new parameters are new groupings of the dates, not new information. Grouping the dates differently is exactly what can show up in the tests.

**What I'd suggest:** build all three as one Chinese divination family, about 30–35 parameters:
- Da Liu Ren: the 12–15 parameters from my last message.
- Mei Hua: the 6 or 7 missing pieces above.
- Tai Yi: about 10 parameters, plus the host and guest calculations as number rules.

The family would then go through the same full test as D9 and the divisional charts:
- singly and in pairs, with all 7 patterns;
- against 20 shifted calendars;
- choosing leads before the last 10 draws, then testing on those 10;
- then on the latest draws.

Building and checking the three charts takes a few hours, and the analysis run another couple of hours. Shall I go ahead with all three, or start with one?

---

**User:**

> OK please do the analysis for all 3 types of chinese astrology da liu ren, Tai Yi Shen Shu,Mei Hua Yi Shu for single and pair and repeat for all types such as cold, hot, etc

**Answer:**

Two open-source packages exist for these charts (kinliuren for Da Liu Ren, kintaiyi for Tai Yi). Reading their code before deciding whether to use them.

**Answer:**

Both packages are plain calculation code (no file or network access). kintaiyi implements the 太乙统宗 daily chart directly, which is better than writing my own from memory. Installing them.

**Answer:**

The calculations check out on hand-worked examples. Today's chart is 返吟 (the Monthly General 辰 sits opposite the hour 戌, as expected). Building the table for all 2,978 dates (~10 min).

**Answer:**

The table is built (35 parameters). Hooking the three families into the analysis pipeline.

**Answer:**

Pipeline works: 13,062 Da Liu Ren leads, 8,820 Mei Hua leads and 16,170 Tai Yi leads (each system alone and paired with every other parameter, × 7 patterns). Launching the full runs now (~1 hour).

**Answer:**

While those run, writing the comparison report for the three systems (same layout as the divisional-chart report, plus the 21 Oct draw).

**Answer:**

The three charts are built and checked, and the full analysis is running in the background. Da Liu Ren started at 03:18 UTC; Mei Hua and Tai Yi follow. I'll report when they finish, in about an hour, or sooner if anything fails.

**What I built** (`analysis/chinese_div.py`, values for every draw date in `data/astro_params_chinese_div.csv`):
- **Da Liu Ren, 12 parameters:**
  - the Monthly General;
  - the upper branches of the first and third lessons;
  - the initial, middle and final transmissions;
  - the method that produced them (賊尅, 比用, 涉害, 遙尅, 昴星, 別責, 八專, 伏吟, 返吟) and its named case;
  - the general on the initial transmission;
  - the initial transmission's relation to the day stem;
  - where the Noble sits;
  - whether the initial transmission is void.
- **Mei Hua Yi Shu, 8 new parameters** (the main hexagram was already tested):
  - the moving line;
  - the changed and mutual hexagrams;
  - which trigram is the body (Ti) and which the use (Yong);
  - the Ti–Yong element relation;
  - the body's seasonal strength;
  - the changed use trigram's relation to the body.
- **Tai Yi Shen Shu, 15 parameters** (daily chart, 太乙統宗 school):
  - the 局 number;
  - Tai Yi's palace, plus 天乙 and 地乙;
  - Wen Chang, Shi Ji and Ji Shen;
  - the host, guest and set calculations;
  - the host and guest generals;
  - the ruling door;
  - whether the five generals go out;
  - the host–guest relation.

**Where the calculations come from:** the Da Liu Ren and Tai Yi charts come from two open-source packages, kinliuren and kintaiyi. I read their code before using them; it is plain calculation with no file or network access. They agree with our existing almanac on the day pillars, for example 戊辰 for 21 Oct. A worked example from the Da Liu Ren package's own documentation (丁未 day) and a Mei Hua case I worked by hand both come out right. I added the Mei Hua parts myself.

**A Mei Hua limitation:** because the draw is always at 19:00, the lower trigram is always the upper trigram plus 3. So there are only 8 possible main hexagrams, 24 changed hexagrams and 8 mutual hexagrams. Mei Hua therefore has much less variety here than usual.

**What the run does, for each system:**
- every parameter alone and paired with all others, including pairs across the three systems, × 7 patterns (hot, cold, pos, hot+100, cold+100, hot/cold100, cold/hot100);
- against 20 shifted calendars;
- choosing leads before the last 10 draws, then testing on those 10;
- then on 18 Oct and on 21 Oct (the clean forward draw);
- the earlier record and repeat high hits of each day's biggest winners.

The results will be compared with D9 and with all leads in `analysis/CHINESE_DIV_REPORT.md`.

**Answer:**

The new Chinese chart code, the chart values for every draw date, and the pipeline changes are now committed and pushed, so the branch is clean. I've also told git to ignore the run's error logs.

The Da Liu Ren run is still going, with Mei Hua and Tai Yi after it. I'll report the results once all three finish, in about an hour.

**Answer:**

All three runs finished. Writing up findings and the watchlist entries.

**Answer:**

All three Chinese systems are now tested, and none of them predicts the draws. Mei Hua Yi Shu shows the most promise, Tai Yi Shen Shu is middling, and Da Liu Ren does worst.

**How the test was run.** Each system's parameters were tried alone, in pairs within the system, across the three systems, and paired with every earlier parameter. Each combination was run with all 7 patterns (hot, cold, pos, hot+100, cold+100, hot/cold100, cold/hot100):
- Da Liu Ren: 13,062 leads
- Mei Hua: 8,820 leads
- Tai Yi: 16,170 leads

**Each system's leads together.** The table counts their high hits (7+ in Magnum Life, 5+ in Toto) and ranks the real calendar against 20 shifted ones, 1 = most; z in brackets:

| System | Magnum Life | Star | Power | Supreme |
|---|---|---|---|---|
| all leads | 5 (+0.9) | 1 (+4.4) | 12 (−0.6) | 15 (−0.2) |
| **Mei Hua Yi Shu** | 11 (+0.2) | **2 (+1.3)** | **1 (+2.0)** | **4 (+1.3)** |
| Tai Yi Shen Shu | 14 (−0.3) | 4 (+1.2) | 3 (+1.2) | 19 (−1.0) |
| Da Liu Ren | 10 (+0.1) | 18 (−1.0) | 17 (−0.8) | **21 (−1.9)**, last |
| D9, for comparison | 4 | 4 | 3 | 15 |

- **Mei Hua is the best of the three.** It is in the top 4 in all three Toto games, about as good as D24 was. The strongest single parameters are:
  - the changed hexagram in Power (z +4.0);
  - the body trigram's seasonal strength in Star (+3.6);
  - the body trigram in Supreme (+3.4).

  Two cautions apply:
  - with the draw always at 19:00, Mei Hua has only 8 possible main hexagrams;
  - it follows a cycle of lunar dates, so like the slow planets it may just be marking stretches of time.
- **Tai Yi is middling:** good in Star and Power, poor in Supreme and Magnum Life. Its best parameter is the host calculation in Star (+2.7).
- **Da Liu Ren is the weakest** of everything tested so far: below chance in all three Toto games and last of 21 in Supreme.

**Leads chosen before the last 10 draws, played on them:** all three systems lost about the stake, the same as every other lead. The only small edges were Mei Hua and Tai Yi in Power: −RM79 and −RM81 against about −RM92 on the shifted calendars.

**On 18 and 21 Oct:** about the same share of their leads won a prize as all leads. The biggest winners on 21 Oct (Magnum Life 6 + bonus RM2,775, Star 5 numbers RM8,312) were again leads that ranked low beforehand.

**Added to the watchlist:** 8 leads, the best earlier lead built on each system's strongest parameter, plus the two with the most repeated hits. That brings the watchlist to 83 entries. All 8 lost on both 18 and 21 Oct:
- Magnum Life:
  - saturn_combust × dlr_zhi_upper
  - mh_changed_vs_ti × ty_wenchang
- Star:
  - aspect_mercury_venus × mh_ti_season
  - lunar_month × ty_host_calc
- Power:
  - lagna_navamsa_lord × mh_changed
  - dlr_noble_earth × ty_door
- Supreme:
  - year_yinyang × mh_ti
  - saturn_navamsa × mh_mutual

**Sources for the charts:** the Da Liu Ren and Tai Yi charts come from the open-source kinliuren and kintaiyi packages. I read their code first, and they agree with our almanac on the day pillars. Tai Yi follows the 太乙統宗 school; other schools would differ slightly.

Everything is committed and pushed. The full tables are in `analysis/CHINESE_DIV_REPORT.md`, and `FINDINGS.md` and `WATCHLIST.md` are updated.

---

**User:**

> list out the leads from those new leads and show me how they perform from the last 3 races

**Answer:**

The 8 new Chinese-system leads won only once in the last 3 draws (17, 18 and 21 Oct): RM80 back on RM414 staked, a loss of RM334.

Each cell shows the best match on that draw (B = bonus ball), then the profit in RM after the stake.

| # | Game | Lead (pattern) | System | Format | Stake | 17 Oct | 18 Oct | 21 Oct | Total |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Magnum Life | saturn_combust × dlr_zhi_upper (cold+100) | Da Liu Ren | 10 tickets | 10 | 2+1B / −10 | 2 / −10 | 2+1B / −10 | **−30** |
| 2 | Magnum Life | mh_changed_vs_ti × ty_wenchang (cold+100) | Mei Hua × Tai Yi | System 9 × 2 overlap | 18 | 3 / −18 | 1+1B / −18 | 3+1B / −18 | **−54** |
| 3 | Star | aspect_mercury_venus × mh_ti_season (hot) | Mei Hua | 10 sets | 10 | 1 / −10 | 1 / −10 | 0 / −10 | **−30** |
| 4 | Star | lunar_month × ty_host_calc (hot) | Tai Yi | System 8 | 28 | **3 / +52** | 1 / −28 | 2 / −28 | **−4** |
| 5 | Power | lagna_navamsa_lord × mh_changed (cold) | Mei Hua | 10 sets | 10 | 0 / −10 | 1 / −10 | 0 / −10 | **−30** |
| 6 | Power | dlr_noble_earth × ty_door (hot+100) | Da Liu Ren × Tai Yi | 10 sets | 10 | 0 / −10 | 0 / −10 | 0 / −10 | **−30** |
| 7 | Supreme | year_yinyang × mh_ti (cold) | Mei Hua | System 7 × 2 disjoint | 28 | 1 / −28 | 1 / −28 | 0 / −28 | **−84** |
| 8 | Supreme | saturn_navamsa × mh_mutual (hot/cold100) | Mei Hua | 10 sets | 20 | 2 / −20 | 0 / −20 | 1 / −20 | **−60** |
| | | **All 8** | | | **138 per draw** | **−54** | **−138** | **−138** | **−334** |

**What stands out:**
- **Only one win:** #4 (Star, Tai Yi host calculation) caught 3 numbers on 17 Oct, winning RM80 on a RM28 stake.
- **The best match anywhere was 3 numbers (plus bonus):** the Magnum Life leads stayed at 1–3 numbers plus bonus, and the Toto leads at 0–2 apart from #4's 3.
- **The two repeated-hit picks did worst:**
  - #6 Power dlr_noble_earth × ty_door matched no numbers on any draw.
  - #8 Supreme saturn_navamsa × mh_mutual matched at most 2.

  These two were added because they had 10 earlier 5-number hits each, far more than their shifted calendars gave.
- **17 Oct is not a clean test:** it fell inside the window used to choose these leads. Only 18 and 21 Oct are truly unseen, and every lead lost on both.

Two or three draws is far too few to judge any lead. These 8 will keep being scored with the rest of the watchlist on each new draw. The 17 Oct scores are added to `analysis/WATCH_LOG.md` and pushed.

---

**User:**

> "1 Karana × Day pillar
> 2 KP Moon number × Year element
> 3 Tithi × Sun nakshatra
> 4 KP Ascendant number × Year pillar
> 5 Mercury nakshatra × Venus rashi
> 6 Jupiter nakshatra × Mercury combust
> 7 S2 Mars triple
> 7 S1 Mars triple
> 8 Mercury navamsa × Venus rashi" check how this leads performs and if they are better

**Answer:**

These are the ranked 4D leads from the 4DPrediction project. Finding their exact definitions there before testing them.

**Answer:**

The 4D results are in. Now testing the same parameter combinations on Magnum Life and the three Toto games, to compare them with the lotto watchlist.

**Answer:**

These are your ranked leads from the 4D project. I checked how they did on the last 3 draws (17, 18 and 21 Oct) in 4D, and then tried the same astrology pairs on Magnum Life and Toto.

## 1. In 4D, the last 3 draws

Each lead plays 16 numbers × 3 operators, RM48 per draw, RM144 over the 3 draws. The picks are rebuilt before each draw from earlier results only.

| # | Lead | Straight wins | i-Box matches (approx. value) | Straight return on RM144 |
|---|---|---|---|---|
| 1 | Karana × Day pillar, S1, i-Box | 0 | 10 (~RM114) | RM0 |
| 2 | KP Moon number × Year element, 2+9 | 1: 4974 Da Ma Cai Consolation, 18 Oct, RM60 | 7 (~RM53) | RM60 |
| 3 | Tithi × Sun nakshatra, 2+9 | 1: 2533 Magnum Special, 17 Oct, RM180 | 3 (~RM28) | RM180 |
| 4 | KP Asc number × Year pillar, 5+6, i-Box | 1: 5304 Toto Consolation, 18 Oct, RM60 | 7 (~RM43) | RM60 (no picks on 17 and 21 Oct, RM48 staked) |
| 5 | Mercury nakshatra × Venus rashi, S1 | **1: 6537 Magnum 2nd prize, 21 Oct, RM1,000** | 5 (~RM77) | **RM1,000** |
| 6 | Jupiter nakshatra × Mercury combust, S2, i-Box | 0 | 5, including **8450 Magnum 1st** as i-Box on 21 Oct (~RM134) | RM0 |
| 7 | S2 Mars triple | 1: 8426 Toto Consolation, 17 Oct, RM60 | 8 (~RM101) | RM60 |
| 7 | S1 Mars triple | 0 | 3, including 8450 Magnum 1st as i-Box (~RM114) | RM0 |
| 8 | Mercury navamsa × Venus rashi, S2 | 0 | 2 (~RM18) | RM0 |

- **Best:** #5 Mercury nakshatra × Venus rashi, with the Magnum 2nd prize on 21 Oct. That one hit returned about 7 times its 3-day stake.
- **Close behind:** #6 and the S1 Mars triple. Both caught the Magnum 1st prize (8450) as an i-Box arrangement, worth about RM104–109 as i-Box.
- **Overall:** about RM1,360 straight on RM1,200 staked. Almost all of it is the single RM1,000 hit; without it, about RM360.

## 2. The same leads on Magnum Life and Toto

I used each lead's exact parameters and history version: (a) all earlier same-value days, or (b) only the previous same-value day. Each was tried in all 7 patterns and all 4 formats, 896 combinations in total. Each was replayed over the whole history and compared with 20 shifted calendars.

These pairs were chosen on 4D, never on lotto, so this is a clean test. They **do not carry over**:
- Only 0.7% of the 896 combinations beat their shifted calendars clearly (z above 2). Chance alone gives about 2.3%. Their typical z is −0.1, which is pure chance.
- In the pattern that matches each 4D method (S1 → hot, S2 → cold), most got **no** high hits over the whole history (7+ Magnum Life, 5+ Toto). The few with one hit were no better than their shifted calendars.
- On the last 3 draws, nearly every combination lost its stake. In the cheapest formats, the only wins were small:
  - #6 Supreme: 3 numbers on 21 Oct, +RM20 after the stake.
  - #6 Power: 3 numbers on 17 Oct, RM6 back on RM10.
  - #5 Magnum Life: 4 numbers plus a bonus on 21 Oct, broke even.
- The one striking result is the Mars triple in Power, hot+100, 10 sets: 2 high hits against 0.1 expected, ahead in both halves of the history. But it is 1 combination out of 896 and wasn't the pattern its 4D method uses, so it could easily be luck.

## Are they better?

- **In 4D, partly.** #5 (Mercury nakshatra × Venus rashi) had a real win, the Magnum 2nd prize, and it is the lead with the strongest long-run record there. But 3 draws can't separate it from luck: its long-run edge was only about ×1.13. In the 4D project, the most consistent lead was #1 (Karana × Day pillar), and it got only i-Box near-misses.
- **In lotto, no.** They do worse than the lotto watchlist's own leads. Those were selected on lotto, so their records naturally look better (typical z +1.9). The 4D pairs, being untuned to lotto, sit at chance.

The full lotto table is in `analysis/LEADS4D_LOTTO.md`, made by the new script `analysis/leads4d_lotto.py`; both are pushed to the mlive branch. I ran the 4D scoring from the 4D project's existing branch and didn't change anything there.

---

**User:**

> * The one striking result is the Mars triple in Power, hot+100, 10 sets: 2 high hits against 0.1 expected, ahead in both halves of the history. But it is 1 combination out of 896 and wasn’t the pattern its 4D method uses, so it could easily be luck. what about this show me how it performed in the last 5 races

**Answer:**

That Mars triple lead in Power Toto (Mars nakshatra × Mars rashi × Mercury combust, hot+100, 10 sets) did poorly on the last 5 draws. It won once, on 11 Oct, and then matched nothing at all on the last three. Each draw's numbers were built only from the draws before it.

| Draw | Numbers drawn | Lead's top 8 numbers | Best match (10 sets) | Profit (RM10 stake) |
|---|---|---|---|---|
| Sun 11 Oct | 11 14 26 28 31 54 | **11** 15 **26** **28** 32 34 44 50 | 3 numbers | **+20** |
| Wed 14 Oct | 28 31 32 36 46 49 | 11 15 26 **28** **32** 34 44 50 | 2 | −10 |
| Sat 17 Oct | 01 07 19 21 43 47 | 11 23 26 35 37 44 52 53 | 0 | −10 |
| Sun 18 Oct | 10 18 25 31 46 47 | 11 21 23 26 35 37 52 53 | 0 | −10 |
| Wed 21 Oct | 08 17 25 27 47 54 | 11 21 23 26 35 37 52 53 | 0 | −10 |
| **5 draws** | | | **one win (3 numbers)** | **−20** (RM30 back on RM50) |

The other formats tell the same story: only the 11 Oct draw paid anything (3 numbers each time).

| Format | Stake per draw | 11 Oct | 5 draws |
|---|---|---|---|
| System 7 × 2 overlap | RM14 | +RM10 | −RM46 |
| System 7 × 2 disjoint | RM14 | −RM2 | −RM58 |
| System 8 | RM28 | +RM2 | −RM110 |

**Why it stood out, and why that's weak:**
- Over the whole history it caught 5 numbers twice: on 24 Feb 2019 and on 12 Sep 2026. Its shifted calendars averaged 0.1 such hits, and that small expected count is what produces the big z score. With only two hits, one more or one fewer would change the picture completely.
- The two hits came from different groups of days, each with a different Mars sign, nakshatra and combust state. Nothing about this particular group of days has hit twice.
- Mars has been in Ashlesha (Karka) since 17 Oct, and that group has 74 earlier draws behind it, none of them a 5-number hit. That is when the lead went to 0 numbers.
- It was 1 of 896 combinations I tried, and the 4D method it comes from uses a different pattern. One combination out of that many looking this good is about what luck produces.

So the last 5 draws give no support to it being a real lead. I can add it to the watchlist so it keeps being scored on each new draw, but nothing so far suggests it will do better than chance.

---

**User:**

> OK now if you noticed, each of the parameter pairs that you have chosen as the lead, i would like to know within those parameters, which of them are top? for example rashixnakshatra-> thulaxswathi performs well it it is worthy to be observed? things like that, which means does will not be able to predict races at any other time except for that combo. Please do analysis on this matter for the chosen leads only with the same condition eg hot/cold to the selected leads

**Answer:**

Across all leads, cells that did well early did no better later (correlation −0.02). Calibrating the "expected by chance" counts with a shuffle test, since small cells skew the simple estimate.

**Answer:**

I took every lead on the watchlist, kept its pattern and format exactly as watched, and split its whole history by the actual values on each draw: its "cells", for example Mercury in Swati × Venus in Tula. For each cell I counted the draws, the winning draws, the high hits (7+ in Magnum Life, 5+ in Toto) and the return. Then I asked two questions.

**1. Are there more standout cells than luck would produce?**

No. Across the 83 entries there are 3,750 cells with at least 8 draws. 157 of them win clearly more often than their lead overall (z above 2). To see what chance gives, I shuffled each lead's wins randomly across its draws, which cuts any link to the cell. That produces 154 such cells on average. So the standouts are what randomness produces anyway.

**2. Does a cell that did well earlier keep doing well?**

This is the real test of "it only predicts in that combo". I ranked the cells on the first half of the history and checked them on the second half.
- The correlation between a cell's first-half and second-half results is **−0.02**, which is zero.
- The 121 cells that were clearly good in the first half averaged **−0.10** in the second half, slightly *below* their lead. With the wins shuffled the figure is +0.02, so real cells did no better than random ones.
- Only 16 cells were good in both halves, where independent chance would give about 22.

So no combination inside any lead keeps winning more than the lead does as a whole.

**The cells that look best, and why they don't hold up**

| Lead (as watched) | Cell | Record | Caveat |
|---|---|---|---|
| #7 Supreme plum_trigrams × saturn_navamsa | trigrams 3-6 × Saturn navamsa Kanya | 20 draws, 4 wins, **two 5-number hits (2015, 2025)**, good in both halves | Seen once among 3,750 cells. Saturn is now in Vrischika navamsa, and this combination doesn't occur again in the chart data, which runs to Feb 2027. |
| #3 Power year_stem × lagna_navamsa_lord | Yi year × Lagna navamsa lord Jupiter | 59 draws, 8 wins, good in both halves | Small prizes only, no high hit; Yi years are 2015 and 2025 |
| #15 Magnum Life day_pillar × aspect_jupiter_saturn | Yi You day / Ji Wei day × no aspect | 11–12 draws, 3 wins each | Too few draws |
| #29 Magnum Life mercury_combust × aspects_soft | Mercury not combust × 4 soft aspects | 46 draws, 7 wins | Small edge, small prizes |

Your example type, Mercury nakshatra × Saturn combust (#8 on the watchlist), has these best cells:
- Swati (Saturn not combust): 41 draws, 5 wins, one 7-number hit.
- Purva Ashadha: 40 draws, 5–6 wins.
- Shravana: 29 draws, 4 wins.

All three are close to the lead's normal rate. For 24 Oct, Mercury is in Vishakha, a cell with 38 earlier draws and only 2–3 small wins.

**Cells some leads are in for Saturday's draw (24 Oct)**
- **#30 and #45 Magnum Life paksha × venus_rashi:** Shukla × Venus in Tula. This is the same cell that gave the Grand prize on 26 Sep, but that is its only high hit in 42 draws.
- **#24 Star saturn_retrograde × aspect_mercury_jupiter:** retrograde × square. It had 5 numbers on 14 Oct, with 3 wins in 21 draws.
- **#14 Power lagna_rashi × saturn_retrograde:** Mesha × retrograde, 5 wins in 41 draws (z +2.7), all small prizes.
- **Power dlr_noble_earth × ty_door:** 酉 × 杜, 3 wins in 16 draws (z +3.0), all small prizes.

Based on the persistence test, none of these deserves more weight.

**The answer to your question:** if a lead only worked in one particular combination, that combination would keep standing out over time. It doesn't. The cells that look good are the ones that happened to win in the past, and they don't stay ahead. I wouldn't follow any single combination on its own.

The full table, every entry's best 3 cells plus its cell for Saturday, is in `analysis/LEAD_CELLS.md` (made by `analysis/lead_cells.py`). Both are committed and pushed.

---

**User:**

> just like karanax day pillar which is consistent in 4d, do you have any that is as consistent as it is?

**Answer:**

Karana × Day pillar earned that label in 4D by being picked on the early years and then beating chance in 14 of the following 15 years. I'll run the same test on the lotto leads: pick on the early years, count the later years above chance, and check against shifted calendars.

**Answer:**

Each lead takes a fraction of a second, so all 45,892 leads × 4 games × 11 calendars should take about 40 minutes. Starting it.

**Answer:**

I've started a consistency test across all 45,892 lotto leads in each of the 4 games. It should take about 40 minutes, and I'll report when it finishes. It copies how Karana × Day pillar was judged in 4D:

- **Chosen in advance:**
  - For each pattern, the top 5 leads are picked on the early years only (to 2021 for Magnum Life and Star, to 2016 for Power and Supreme).
  - I then count how many later years each one beats chance: 5 later years for Magnum Life and Star, 10 for Power and Supreme.
- **Measured per draw:** how many drawn numbers land in the lead's top 8 (Magnum Life) or top 6 (Toto). Chance gives an exact expected count, so "above chance" in a year is precise.
- **Checked against luck:**
  - The whole procedure is repeated on 10 shifted calendars, where the dates no longer line up with the draws.
  - I also run a version with no astrology at all, like the 4D check that found "the same picks without a parameter got 6 of 15".
- **Hindsight check:** the most consistent lead over the later years, compared with what the shifted calendars produce.

The script and results will be `analysis/consistency.py` and `analysis/CONSISTENCY.md`.

**Answer:**

I've committed and pushed the new test script (`analysis/consistency.py`), so the branch is clean again.

The test is still running in the background. When it finishes I'll send the results and push `CONSISTENCY.md` with them.

---

**User:**

> OK now i want you to redo all the analysis "OK now if you noticed, each of the parameter pairs that you have chosen as the lead, i would like to know within those parameters, which of them are top? for example rashixnakshatra-> thulaxswathi performs well it it is worthy to be observed? things like that, which means does will not be able to predict races at any other time except for that combo. Please do analysis on this matter for the chosen leads only with the same condition eg hot/cold to the selected leads" for this but rather than the current lead that we have, try for every combination of parameters

**Answer:**

I'll run the cell analysis on every lead rather than just the watchlist: all 114 parameters alone and in pairs, × 7 patterns, which is 45,892 leads per game, split into every value combination.

To keep a run over millions of cells fast, each draw is scored by how many drawn numbers land in the lead's top ticket (8 numbers for Magnum Life, 6 for Toto). Chance gives an exact expected count. Then come the same two tests as before:
- Are there more standout cells than chance?
- Do cells that were good early stay good later?

I'll also check both against shifted calendars.

**Answer:**

A test chunk works (about 120 cells per lead, roughly 5 million per game). Launching the full run alongside the consistency test.

**Answer:**

I've started the value-combination ("cell") analysis on every lead: all 114 parameters alone and in pairs, × 7 patterns, which is 45,892 leads per game and about 5 million cells each. It is running in the background alongside the consistency test.

The method is the same as for the watchlist cells, with one change: each draw is scored by how many drawn numbers land in the lead's top ticket (8 numbers for Magnum Life, 6 for Toto), because chance gives an exact expected count. Across all cells the run answers:
- **More standouts than chance?** How many cells beat chance clearly, compared with the 2.3% luck alone would give.
- **Do good cells stay good?** Whether cells that were good in the first half of the history stay good in the second half.
- **Luck check:** the same counts on 3 shifted calendars, where the dates no longer line up with the draws.
- **Strongest cells:** the cells good in both halves, for example a rashi × nakshatra value pair like your Tula × Swati.
- **This Saturday:** which of those good cells are active for the draw on 24 Oct.

Both runs should finish within the hour. When they do I'll report the consistency results and the cell results together, and push `analysis/CONSISTENCY.md` and `analysis/CELLS_ALL.md`. The script is already committed and pushed.

**Answer:**

The cell run crashed on its first attempt. It picked up the extra D9, divisional-chart and Chinese parameters, which have no stored values to label the cells with. I've limited it to the 114 base parameters, the same set as all the full runs, and restarted it.

The consistency test is unaffected: Magnum Life is done and the other three games are still running. I'll report both when they finish.

**Answer:**

I've committed and pushed the fix to the cell analysis (it now uses only the 114 base parameters), so the branch is clean again.

Both runs are still going in the background. The consistency test has finished Magnum Life and is working through Star, Power and Supreme. The cell analysis has restarted from the beginning. I'll report the results of both together once they finish.

**Answer:**

The container restarted and stopped both runs, the consistency test and the cell analysis, before either saved any results. I've started both again from the beginning, and they're running in the background.

They should finish in about an hour. I'll report the results of both together when they do.

**Answer:**

Both runs finished. Neither finds anything as consistent as Karana × Day pillar in 4D: no single lead, and no particular combination inside a lead, does better than chance once compared with the shifted calendars.

Both tests score each draw by how many drawn numbers land in the lead's top ticket (8 numbers for Magnum Life, 6 for Toto). That gives an exact chance level per draw.

## 1. Is any lotto lead as consistent as Karana × Day pillar?

I copied the 4D procedure:
- **Picking:** the top 5 leads of each pattern were chosen on the early years only (to 2021 for Magnum Life and Star, to 2016 for Power and Supreme).
- **Counting:** I counted how many later years each one beat chance.
- **Luck check:** the whole procedure was repeated on 10 shifted calendars, where the dates no longer line up with the draws.

| Game | Later years | Chosen leads: average years above chance (shifted) | Best chosen lead (shifted best) | Forward ratio (shifted) |
|---|---|---|---|---|
| Magnum Life | 5 | 2.2 (2.3) | 4 of 5 (4) | ×0.994 (×0.996) |
| Star | 5 | 2.4 (2.4) | 4 of 5 (5) | ×0.997 (×0.998) |
| Power | 10 | 4.7 (4.6) | 7 of 10 (8) | ×0.997 (×0.991) |
| Supreme | 10 | 5.1 (4.9) | 8 of 10 (8) | ×1.002 (×0.999) |

The leads picked in advance do no better than leads picked from shifted calendars. Nothing comes close to Karana's 14 of 15 years, where none of the 50 shifted calendars got 14. The best chosen leads were:
- **Supreme:** day_of_month × aspect_venus_mars (cold/hot100), 8 of 10 years, ×1.075. Shifted calendars produce 8 of 10 just as often.
- **Power:** lagna_nakshatra × aspect_venus_jupiter (cold+100), 7 of 10 years.
- **Star:** lagna_rashi × lunar_month (pos), 4 of 5 years, ×1.077.

**In hindsight** there are leads that beat chance every single year, for example:
- **Power:** jupiter_nakshatra × mars_retrograde (cold), 10 of 10 years, ×1.11.
- **Supreme:** kp_sun_star_lord × day_officer (hot), 10 of 10 years, ×1.10.

But such leads are as common on shifted calendars as on the real one:

| Game | Leads above chance every later year: real | Shifted calendars |
|---|---|---|
| Power | 12 | 4–22 |
| Supreme | 16 | 18–52 |
| Magnum Life | 1,045 | 948–1,329 |
| Star | 1,219 | 823–1,058 |

Out of 45,892 leads, luck alone produces leads like these. Star is the one slightly higher than its shifted range, which matches the small Star tilt found earlier.

## 2. Inside every lead: do particular combinations predict (like Tula × Swati)?

I split all 45,892 leads per game into their value combinations: about 1.5 million cells in Magnum Life and Star, and 2.9 million in Power and Supreme. Each was checked in the first half of the history and then in the second half.

| | Magnum Life | Star | Power | Supreme |
|---|---|---|---|---|
| Correlation of first half vs second half (0 = no carry-over) | −0.004 | +0.002 | −0.002 | −0.007 |
| Cells good in the first half: average in the second half (0 = luck) | −0.001 | −0.001 | −0.027 | −0.034 |
| ...share still above chance (50% = luck) | 48% | 49% | 48% | 47% |
| Cells good in both halves: real vs if the halves were independent | 602 vs 602 | 1,027 vs 978 | 1,496 vs 1,478 | 1,470 vs 1,572 |

Across about 9 million combinations, being good earlier says nothing about later. The numbers of cells that look good in both halves match independent chance almost exactly, and they match the shifted calendars too.

The strongest-looking ones are:
- Power: Mars in Vrischika × lunar mansion Nu (cold), 19 draws, good in both halves.
- Supreme: Garaja karana × Mercury–Jupiter opposition (hot+100), 12 draws.

These are what you get when you look through millions of small groups. Most have only 8–20 draws.

For Saturday's draw (24 Oct), 10–17 leads per game sit in a cell that was good in both halves, out of about 35,000–40,000 leads with an active cell. That is the number chance predicts.

## Overall

In these lotto games there is no lead, and no combination within a lead, that is consistent in the way Karana × Day pillar was in 4D. Every apparent pattern appears just as often when the astrology is scrambled against the dates. Even Karana's own edge in 4D was small, worth about 67% back instead of 64%.

Full tables are in `analysis/CONSISTENCY.md` and `analysis/CELLS_ALL.md`, made by `analysis/consistency.py` and `analysis/cells_all.py`. All are committed and pushed.

---

**User:**

> so based on this analysis what are the leads worth it of observing on future rounds?

**Answer:**

None of the lotto leads has shown a real edge, so nothing is worth betting on. If you want to keep testing, the useful approach is a short list frozen now and judged only on future draws. A lead belongs on it only if it was picked before the years it was tested on, kept roughly level with or above chance afterwards, and isn't explained by one lucky jackpot.

**Lotto short list**

| Game | Lead (pattern, format) | Why it's on the list |
|---|---|---|
| Star | lagna_rashi × lunar_month (pos) | Picked on data to 2021, then above chance in 4 of 5 later years, with the best forward ratio of any lead picked in advance (×1.077). Star is also the only game where astrology leads as a group beat the shifted calendars. |
| Supreme | day_of_month × aspect_venus_mars (cold/hot100) | Picked on data to 2016, then above chance in 8 of 10 later years (×1.075), the most of any lead picked in advance. |
| Power | karana × aspect_mercury_jupiter (hot/cold100) | Picked on data to 2016, then ×1.054 over the next 10 years (6 of 10 above chance). |
| Power | year_stem × lagna_navamsa_lord (cold, 10 sets) | The cleanest watchlist record: three 5-number hits in 2017, 2018 and 2022, all before it was chosen, with no jackpot inflating it. |
| Supreme | plum_trigrams × saturn_navamsa (hot/cold100, 10 sets) | Three 5-number hits spread over 2014–2025, before it was chosen. Its best value combination can't recur until Saturn returns to Kanya navamsa, which is beyond Feb 2027. |
| Magnum Life | rahu_nakshatra × aspect_moon_venus (cold/hot100) | The best Magnum Life lead picked in advance (×1.024), though only 3 of 5 years above chance. Magnum Life has nothing stronger. |

**Worth watching as groups, not single leads:**
- **Mei Hua Yi Shu leads in Toto.** They placed 2nd, 1st and 4th of 21 in Star, Power and Supreme, the best of the systems tested, comparable to D24.
- **D24 leads.** They placed 1st, 2nd and 1st in Magnum Life, Star and Power.

**In 4D** (the other project):
- **Karana × Day pillar** is still the most consistent lead found anywhere, though its edge is small.
- **Mercury nakshatra × Venus rashi** has the strongest long-run 4D record and won the Magnum 2nd prize on 21 Oct.

**What I'd stop watching:**
- **Most of the 83 watchlist entries,** especially the ones added because of a recent big win: the 18 Oct winners, the 17 Oct Supreme 5-number hits and the Grand prize lead. Every test since shows these were luck.
- **The Mars triple in Power.**
- **The 4D pairs played on lotto.**
- **Individual value combinations.** No cell keeps its advantage over time, so no "Tula × Swati"-type rule is worth following.

**How to judge the short list fairly:**
- Score each of the six on every draw from now on, without changing the list.
- Judge it after a fixed number of draws, about 50 (roughly 4 months of Toto). The test is whether its hits beat the exact chance level by more than luck allows. A few draws can't tell skill from luck either way.
- Expect at best a small gain. The strongest forward ratios are about ×1.05–1.08 more matched numbers. That still returns well under the stake, because the games pay out only about 20–55%.

I can set this up as a separate frozen short list, scored automatically alongside the current watchlist after each draw. Would you like me to?

---

**User:**

> add all this into the leads to be observed we will see how they perform

**Answer:**

Short list added to the watchlist. Scheduling the results update after Saturday's draw, as with the previous ones.

**Answer:**

I've added the short list to the leads to be observed, frozen as of today so it can't be changed after the fact. Four leads are new to the watchlist, and two were already on it:

| Game | Lead (pattern) | Formats scored |
|---|---|---|
| Star | lagna_rashi × lunar_month (pos), **new** | 10 sets, System 8 |
| Supreme | day_of_month × aspect_venus_mars (cold/hot100), **new** | 10 sets, System 8 |
| Power | karana × aspect_mercury_jupiter (hot/cold100), **new** | 10 sets, System 8 |
| Magnum Life | rahu_nakshatra × aspect_moon_venus (cold/hot100), **new** | 10 tickets, System 10 |
| Power | year_stem × lagna_navamsa_lord (cold), already watched | 10 sets |
| Supreme | plum_trigrams × saturn_navamsa (hot/cold100), already watched | 10 sets |

The Mei Hua and D24 groups stay on as observed groups through their existing watchlist entries. The two 4D leads (Karana × Day pillar and Mercury nakshatra × Venus rashi) are tracked in the 4D project.

**How they'll be judged, starting Saturday 24 Oct:**
- **Main test:** after every draw I count how many drawn numbers land in each lead's top ticket (8 numbers for Magnum Life, 6 for Toto). I compare that with the exact chance level and show a running ratio and z-score in a new "Short list" section of `analysis/WATCH_LOG.md`.
- **Prizes:** these are logged too.
- **When to decide:** after about 50 draws, roughly 4 months of Toto. Until then, a z-score between −2 and +2 is still just luck.

I've also set a scheduled task for **Saturday 24 Oct at 21:30 Malaysia time**. It will fetch that night's results, score the short list and the rest of the watchlist, push everything, and report back to you.

The list and its reasons are in `analysis/WATCHLIST.md` under "Short list (frozen 2026-10-22)". Everything is committed and pushed.

---

**User:**

> ok from all this new leads added show me how they perform in the last 5 draws

**Answer:**

Over the last 5 draws (11, 14, 17, 18 and 21 Oct), none of the six short-list leads won a prize, in any format. Measured by how many drawn numbers landed in each lead's top ticket, they were close to chance, as expected for so few draws.

**Prizes and best match per draw** (cheapest format; each cell is best match / profit in RM; B = bonus ball):

| Game | Lead (pattern) | Format, stake | 11 Oct | 14 Oct | 17 Oct | 18 Oct | 21 Oct | Total |
|---|---|---|---|---|---|---|---|---|
| Star | lagna_rashi × lunar_month (pos) | 10 sets, RM10 | 1 / −10 | 0 / −10 | 1 / −10 | 1 / −10 | 1 / −10 | **−50** |
| Supreme | day_of_month × aspect_venus_mars (cold/hot100) | 10 sets, RM20 | 2 / −20 | 2 / −20 | 0 / −20 | 0 / −20 | 0 / −20 | **−100** |
| Power | karana × aspect_mercury_jupiter (hot/cold100) | 10 sets, RM10 | 1 / −10 | 1 / −10 | 1 / −10 | 2 / −10 | 0 / −10 | **−50** |
| Power | year_stem × lagna_navamsa_lord (cold) | 10 sets, RM10 | 0 / −10 | 1 / −10 | 1 / −10 | 2 / −10 | 2 / −10 | **−50** |
| Supreme | plum_trigrams × saturn_navamsa (hot/cold100) | 10 sets, RM20 | 0 / −20 | 2 / −20 | 2 / −20 | 0 / −20 | 1 / −20 | **−100** |
| Magnum Life | rahu_nakshatra × aspect_moon_venus (cold/hot100) | 10 tickets, RM10 | 2+1B / −10 | 3 / −10 | 2 / −10 | 3 / −10 | 2 / −10 | **−50** |

The second formats did the same: Star System 8 lost RM140, Supreme System 8 RM280, Power System 8 RM140 and Magnum Life System 10 RM225. The best match anywhere was 3 numbers plus a bonus ball (Magnum Life System 10 on 18 Oct), which isn't enough for a prize.

**Top-ticket hits against chance (5 draws)** — the measure the short list will be judged on:

| Lead | Hits per draw | Total | Chance | Ratio |
|---|---|---|---|---|
| Star lagna_rashi × lunar_month | 1, 0, 1, 1, 1 | 4 | 3.6 | ×1.11 |
| Supreme day_of_month × aspect_venus_mars | 1, 1, 0, 0, 0 | 2 | 3.1 | ×0.64 |
| Power karana × aspect_mercury_jupiter | 1, 0, 1, 1, 0 | 3 | 3.3 | ×0.92 |
| Power year_stem × lagna_navamsa_lord | 0, 1, 1, 2, 2 | 6 | 3.3 | ×1.83 |
| Supreme plum_trigrams × saturn_navamsa | 0, 2, 1, 0, 1 | 4 | 3.1 | ×1.29 |
| Magnum Life rahu_nakshatra × aspect_moon_venus | 2, 3, 1, 3, 1 | 10 | 8.9 | ×1.12 |

Four of the six were slightly above chance; year_stem × lagna_navamsa_lord in Power did best, with 2 numbers in each of the last two draws. With only 5 draws, though, swings this size are ordinary luck. These draws also fall inside the data the leads were picked on, so they aren't a real test.

The real test starts Saturday (24 Oct). The scheduled task will score all six then and keep a running count in `analysis/WATCH_LOG.md`, with a fair verdict possible after about 50 draws.

---

**User:**

> so now rank all the leads that we have so far against the test that they have not trained before

**Answer:**

I ranked all 81 watchlist leads using only draws their choice never looked at. Each draw is scored by how many drawn numbers fall in the lead's top ticket (8 numbers for Magnum Life, 6 for Toto). Chance gives an exact expected count, so each lead gets a ratio and a z-score; a z between −2 and +2 is within luck.

**The basic problem: almost no lead has much unseen data.**
- **75 leads** were picked using data up to 17 or 18 Oct, so only 1 or 2 draws (18 and/or 21 Oct) are truly unseen for them.
- **4 short-list leads** have years of unseen draws: picked on data to 2016 or 2021, then tested on the years after.
- **The two other short-list leads** (year_stem × lagna_navamsa_lord and plum_trigrams × saturn_navamsa) come from the D9 run, so they have only 21 Oct unseen.

## Ranking

| # | Game | Lead (pattern) | Unseen draws | Hits / chance | z | Profit on those draws (RM) |
|---|---|---|---|---|---|---|
| 1 | Supreme | day_of_month × aspect_venus_mars (cold/hot100) | 1,580 (2017–2026) | 1,054 / 981, ×1.07 | **+2.6** | −29,240 on 31,600 (10 sets) |
| 2 | Star | lagna_rashi × lunar_month (pos) | 805 (2022–2026) | 624 / 580, ×1.08 | **+2.1** | −5,322 on 8,050 |
| 3 | Power | karana × aspect_mercury_jupiter (hot/cold100) | 1,581 (2017–2026) | 1,091 / 1,035, ×1.05 | +1.9 | −15,128 on 15,810 |
| 4 | Power | year_stem × lagna_navamsa_lord (cold) | 1 | 2 / 0.7 | +1.8 | −10 |
| 5 | Supreme | moon_rashi × aspects_hard (cold) | 2 | 3 / 1.2 | +1.7 | −32 on 112 |
| 6–9 | Star | sun_rashi × planets_with_moon, lagna_rashi × day_officer, saturn_retrograde × nayin, lunar_month × ty_host_calc | 2 | 3 / 1.4 | +1.5 | all lost the stake |
| 10 | Magnum Life | rahu_nakshatra × aspect_moon_venus (cold/hot100) | 805 (2022–2026) | 1,466 / 1,431, ×1.02 | +1.2 | −6,485 on 8,050 |
| 11–60 | mixed | 50 leads | 1–2 | close to chance | −0.7 to +1.0 | nearly all lost the stake |
| 61–81 | mixed | including mercury_combust × aspects_soft and day_of_month × aspect_venus_jupiter | 1–2 | below chance | −0.7 to −1.7 | all lost the stake |

The full table of all 81 is in `analysis/RANK_OOS.md`.

## What it means

**Top three: the only real evidence.** These short-list leads were tested on 5–10 unseen years, and they caught 5–8% more numbers than chance.

They still need two caveats:
- **They were picked for this result.** I put them on the short list because they were the best of 35 pre-picked leads per game on those unseen years. Among 35 leads, luck alone gives the best one a z of about +2, so z of +1.9 to +2.6 is only at the edge of luck.
- **They still lost money.** Even at ×1.07, the 10 sets returned only about 7–34% of the stake. Catching a few more numbers rarely turns into prizes.

**Ranks 4 to 81: no information yet.** One or two draws can't separate a good lead from a bad one. The order there is luck.

Two examples of how little 1–2 draws show:
- mercury_combust × aspects_soft won RM110,000 on 18 Oct. That draw was the reason it was added, so it can't count, and on 21 Oct it caught only 1 number.
- #1 on the old watchlist ranking, day_of_month × aspect_venus_jupiter, caught 0 numbers in both unseen draws.

## Bottom line

Only the top three have enough unseen data to judge, and even they are borderline. Everything else has to be judged on future draws.

The scheduled update after Saturday's draw adds one more unseen draw for every lead. I can rerun this ranking after each draw so it builds up over time. A fair judgement of the 1–2-draw leads needs about 50 draws, roughly 4 months of Toto.

This ranking is pushed as `analysis/RANK_OOS.md`, made by `analysis/rank_oos.py`.

---

**User:**

> i feel like unseen draws are unfair, try to rerun the analysis so that the unseen draws are fairrer

**Answer:**

Fairer is possible: give every lead the same kind of unseen test, with lots of unseen draws, by re-choosing leads before each year using only earlier data. I'll set it up as a rolling, year-by-year test.

**Answer:**

I agree the last ranking wasn't fair. Most leads had only 1–2 unseen draws, while the short-list leads got years. I've set up a fairer test and it is running now, roughly 30–40 minutes. In this test every lead goes through exactly the same unseen test, with years of unseen draws instead of one or two.

**How it works:**
1. **Pick before each year:** before each year in the history, every lead (all 45,892 per game, plus every watchlist lead) is judged only on the draws before that year.
2. **Choose the top 1%:** the top 1% of leads in each game are chosen for that year, as if you had picked them on 31 Dec.
3. **Score blind:** that year is then scored blind, counting how many drawn numbers land in each lead's top ticket (8 for Magnum Life, 6 for Toto) against exact chance.
4. **Repeat every year:** this runs for every year after the first two, from 2012 for Power and Supreme and 2020 for Magnum Life and Star. Thousands of unseen lead-draws per game are pooled.

**What it will show:**
- **Does picking on past records work at all?** If it does, the leads chosen each year should beat chance the following year. I compare that against 3 shifted calendars, where the dates no longer line up with the draws, and against using no astrology at all.
- **A fair score for each watchlist lead:**
  - which years its earlier record would have got it chosen;
  - how it did in those blind years only;
  - leads that were never good enough beforehand show "never". That says something too: they only look good in hindsight.

When it finishes I'll send the ranking and push `analysis/FAIR_OOS.md`. The script (`analysis/fair_oos.py`) is already pushed.

**Answer:**

The fair test is done. Picking leads by their past record doesn't work, and only 7 of the 81 watchlist leads would ever have been chosen in advance.

**How it works.** Before each year, I ranked every lead using only the draws before that year. The top 1% in each game (about 460 leads) counted as "chosen" for that year. That year was then scored blind: how many drawn numbers landed in each lead's top ticket (8 for Magnum Life, 6 for Toto), against exact chance. This repeats for every year: 2020–2026 for Magnum Life and Star, 2012–2026 for Power and Supreme. Every lead, watchlist or not, got exactly the same test.

## 1. Does choosing leads by their past record work?

No. The leads chosen each year did slightly *worse* than chance the following year, as badly as on shifted calendars where the dates no longer line up with the draws:

| Game | Chosen leads, next year | Shifted calendars | No astrology (best pattern) |
|---|---|---|---|
| Magnum Life | ×0.997 | ×0.996–0.998 | ×1.020 |
| Star | ×0.991 | ×0.987–0.991 | ×0.997 |
| Power | ×0.989 | ×0.985–0.992 | ×1.008 |
| Supreme | ×1.000 | ×0.999–1.001 | ×1.000 |

The leads that looked best before a year fell back the next year, and that drop was the same with real dates as with scrambled ones. In every game, the plain no-astrology pick did at least as well as the astrology leads.

## 2. The watchlist on the same test

Only **7 of the 81 watchlist leads** ever made the top 1% before a year. The other 74 never had a good enough record beforehand, so their good results only show up in hindsight.

The 7 that qualified, scored only on the years they would have been chosen:

| # | Game | Lead (pattern) | Years chosen beforehand | Blind draws | Blind ratio | Blind z |
|---|---|---|---|---|---|---|
| 1 | Magnum Life | **mars_rashi × month (cold)** | 2022–2026 | 805 | ×1.073 | **+3.5** |
| 2 | Supreme | **day_of_month × aspect_venus_mars (cold/hot100)** | 2015–2026 | 1,937 | ×1.082 | **+3.1** |
| 3 | Star | lagna_rashi × lunar_month (pos) | 2022–2026 | 805 | ×1.077 | +2.1 |
| 4 | Power | karana × aspect_mercury_jupiter (hot/cold100) | 2015, 2017–2026 | 1,759 | ×1.050 | +1.9 |
| 5 | Magnum Life | rahu_nakshatra × aspect_moon_venus (cold/hot100) | 2021–2026 | 931 | ×1.036 | +1.9 |
| 6 | Power | masa × adhika_masa (hot+100) | 2013–2020 | 1,364 | ×1.011 | +0.4 |
| 7 | Star | rahu_nakshatra × kp_asc_sub_lord (hot) | 2021 | 126 | ×0.970 | −0.3 |

Leads that never qualified include the 18 Oct RM110k winner (mercury_combust × aspects_soft), the Grand prize lead (paksha × venus_rashi), the 17 Oct Supreme 5-number hits, and the two leads with the cleanest records, year_stem × lagna_navamsa_lord and plum_trigrams × saturn_navamsa.

## 3. Are the top two real or luck?

About 1,600–2,600 leads per game qualified at some point, so a few strong blind records are expected by chance. I compared the best of them against 2 shifted calendars:
- **Magnum Life:** the best blind record in the whole game is mars_rashi × month (+3.5). The shifted calendars' best were +2.8 and +3.2, so it is slightly above luck, but only against 2 comparisons.
- **Star:** the best was +3.9, and the shifted calendars reached +3.5 and +3.8. That is luck-sized.
- **Supreme:** +3.1, against +3.0 and +2.9 on the shifted calendars. Also luck-sized.
- **Power:** +2.8, against +3.5 and +2.5. Also luck-sized.

## What this means

- **Picking leads on their past record doesn't predict the future.** That is the main fair result, and it holds in all four games.
- **Two leads are worth keeping a close eye on.** They passed the fair test better than the rest:
  - **Magnum Life mars_rashi × month (cold):** it qualified before every year from 2022 and caught 7% more numbers than chance in those blind years. It was on the watchlist as a "steady ball-catcher" but wasn't on the short list. I'd add it.
  - **Supreme day_of_month × aspect_venus_mars (cold/hot100):** it qualified before 12 straight years and stayed ×1.08 blind. It is already on the short list.

  Even for these two, catching 7–8% more numbers hasn't turned into profit; earlier tests showed the 10-set format returning less than the stake.
- **The other short-list leads** (lagna_rashi × lunar_month, karana × aspect_mercury_jupiter, rahu_nakshatra × aspect_moon_venus) are positive but within luck.

The results are in `analysis/FAIR_OOS.md`, made by `analysis/fair_oos.py` and `analysis/fair_oos_pool.py`, all pushed. Should I add mars_rashi × month (cold) to the frozen short list before Saturday's draw?

---

**User:**

> how does all 7 performed in the last 10 draws?

**Answer:**

Over the last 10 draws (30 Sep to 21 Oct), two of the seven won money, and mars_rashi × month caught the most numbers relative to chance. But most of these leads were picked while looking at these same 10 draws, so this isn't a fair test.

**Numbers caught in each lead's top ticket** (8 numbers for Magnum Life, 6 for Toto):

| Lead (pattern) | 30 Sep | 3 Oct | 4 Oct | 7 Oct | 10 Oct | 11 Oct | 14 Oct | 17 Oct | 18 Oct | 21 Oct | Total vs chance |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Magnum Life mars_rashi × month (cold)** | 2 | 2 | 3 | 2 | 3 | 3 | 2 | 4 | 2 | 2 | **25 vs 17.8 (×1.40)** |
| Supreme day_of_month × aspect_venus_mars (cold/hot100) | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 8 vs 6.2 (×1.29) |
| Star lagna_rashi × lunar_month (pos) | 2 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 7 vs 7.2 (×0.97) |
| Power karana × aspect_mercury_jupiter (hot/cold100) | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 7 vs 6.5 (×1.07) |
| Magnum Life rahu_nakshatra × aspect_moon_venus (cold/hot100) | 0 | 2 | 2 | 1 | 3 | 2 | 3 | 1 | 3 | 1 | 18 vs 17.8 (×1.01) |
| Power masa × adhika_masa (hot+100) | 1 | 0 | 0 | 1 | 1 | **5** | 2 | 0 | 1 | 1 | 12 vs 6.5 (×1.85) |
| Star rahu_nakshatra × kp_asc_sub_lord (hot) | 0 | 0 | 2 | 4 | 3 | 1 | 2 | 0 | 0 | 0 | 12 vs 7.2 (×1.67) |

**Money over the 10 draws:**

| Lead | Format | Stake | Paid back | Best match |
|---|---|---|---|---|
| mars_rashi × month | System 10 | RM450 | RM50 | 4 numbers (17 Oct) |
| day_of_month × aspect_venus_mars | 10 sets / System 8 | RM200 / RM560 | RM0 | 2 numbers |
| lagna_rashi × lunar_month | 10 sets / System 8 | RM100 / RM280 | RM0 | 2 numbers |
| karana × aspect_mercury_jupiter | 10 sets / System 8 | RM100 / RM280 | RM0 | 2 numbers |
| rahu_nakshatra × aspect_moon_venus | 10 tickets / System 10 | RM100 / RM450 | RM0 | 3 numbers |
| **masa × adhika_masa** | System 8 | RM280 | **RM3,040,200** | **all 6, Power jackpot (11 Oct)** |
| rahu_nakshatra × kp_asc_sub_lord | System 8 | RM280 | RM6,684 | 5 numbers (7 Oct) |

- **mars_rashi × month**, the strongest lead in the fair test, caught more numbers than chance in 7 of the 10 draws, 25 against 17.8 expected. That fits its blind record, although its System 10 ticket returned only RM50 of RM450.
- **The two prize winners won big** — the Power jackpot (masa × adhika_masa) and a 5-number Star hit (rahu_nakshatra × kp_asc_sub_lord). Both are on the watchlist *because* of those wins, so the wins can't count as evidence. In the fair yearly test both were weak: ×1.01 and ×0.97 in the years they'd have been chosen.
- **The other short-list leads** were close to chance, and none of them won a prize.

**Why this isn't a fair test:** these 10 draws were the test window used to pick most of the watchlist, and the fair yearly test covered them too. The first truly fair draw for all seven is Saturday 24 Oct. The scheduled update will score them from then on.

Do you want me to add mars_rashi × month (cold) to the frozen short list before Saturday?

---

**User:**

> what are other analysis which is plausible to be tested but we have not tested them yet? you can check the 4d repo to see if there are things that we can analyse

**Answer:**

Looking at both repos, most of what the 4D project tested has a lotto equivalent already. These are the plausible ideas not yet tested on Magnum Life and the Toto games, starting with the most worthwhile.

**Worth testing (astrology we haven't covered)**

| # | Idea | What it tests | From 4D? | Effort |
|---|---|---|---|---|
| 1 | **Tai Yi and Mei Hua as direct number rules** | The Tai Yi host, guest and set calculations are actual numbers (1–40) each day, and Mei Hua hexagrams give numbers too. Play those numbers directly instead of as categories. I mentioned this earlier but didn't run it. | yes (4D's "direct number test") | small |
| 2 | **Exact planetary positions** | Use exact longitudes, angles between planets and how far through each sign, instead of sign or nakshatra categories. Catches effects that cut across sign boundaries. | yes (`continuous_astro.py`) | medium |
| 3 | **Muhurta and timing factors at 19:00** | Rahu Kalam, Yamaganda, Gulika and Choghadiya at draw time; void-of-course Moon; out-of-bounds Moon; how close an eclipse or a planet changing direction is. These are classic "lucky time" factors that aren't in our 114 parameters. | no | small–medium |
| 4 | **Triples of parameters** | Three parameters together, like the 4D Mars triple. Lotto has only singles and pairs. There are about 240,000 triples per game, so the shifted-calendar check is essential. | yes (`s12_combos.py`) | large |
| 5 | **Transits to a "lottery birth chart"** | Planets today against the chart of each game's first draw (Magnum Life Apr 2018, Star Oct 2017, Power Oct 2009, Supreme Mar 2010). This is how astrologers usually time events. | no | medium |
| 6 | **Same-date repeats each year** | Do numbers come back around the same calendar date, or the same Chinese lunar date, in other years? | yes (`seasonal_astro.py`) | small |
| 7 | **Ticket shape by astrology** | Does the sum of the numbers, the odd/even split, high/low, or consecutive pairs change with the Moon phase, sign and so on? We only checked shape overall, not by astrology. If it held, it could filter tickets. | partly | small |

**Without astrology (to compare against)**

| # | Idea | What it tests | From 4D? | Effort |
|---|---|---|---|---|
| 8 | **Machine or ball bias by period** | The only real effect 4D ever found was a Magnum digit bias in 2019–2025. Our lotto fairness check looked at whole years; this would look for shorter stretches where some numbers came up too often. | yes (`magnum_bias.py`) | small |
| 9 | **Learning models** | Let a machine-learning model (gradient boosting, nearest-similar-days, a small neural net, combinations) work out each number's chance from all astrology values at once. Our "similar days", embedding and analogy models were simpler versions. | yes (`ml_model.py`) | medium |
| 10 | **Regime-change and number-timing models** | Detect when the number mix changes, predict from recent draws, and model how long since each number was last drawn. | yes (`new_models.py`) | medium |
| 11 | **4D results to lotto** | Do the same evening's 4D first prize digits, or earlier 4D results, point to Magnum Life or Toto numbers? The draws are run by the same operators. | no | small |

**Not worth testing:**
- **Cold-number and 1024-type single picks:** 4D already showed these were hindsight picks.
- **"Search single draw":** this only shows how easily a formula can be found to fit any one draw.
- **Ticket covering designs:** they change how winnings are spread across tickets, not the odds.

**My suggestion:** start with 1, 3 and 8. They are quick and new, and 8 is the only kind of effect that has ever proved real. Then 2 and 6, with 4 last because it's the biggest and the most prone to luck. Every test will use the fair yearly check from the last round, so the results stay comparable.

Which ones should I run?

---

**User:**

> lets test all the astrological analysis from 1 to 7

**Answer:**

I'll start by building the new parameters (muhurta timing, exact positions and transits to each game's first-draw chart), then write one shared test engine so every idea gets the same fair test.

**Answer:**

The new parameters are built: 14 muhurta, 45 exact-position and 13 transit parameters for every draw date. Now writing the shared test engine.

**Answer:**

While those run, I'm writing the scripts for the other three ideas: number rules, same-date repeats and ticket shape.

**Answer:**

#1 is done: every Tai Yi and Mei Hua number rule is at chance. Next, same-date repeats (#6).

**Answer:**

Fixed a bug in the shared test engine, which was crashing on the shifted calendars, and restarted those runs. The same-date test is still running. Now writing the ticket-shape test (#7).

**Answer:**

All seven tests are written and committed. The first one has finished, and the rest are running in the background.

**#1 Tai Yi and Mei Hua numbers played directly: no effect.**
- The tested rules were the Tai Yi host, guest and set calculations, generals, palace and 局, and the Mei Hua trigrams, moving line, hexagram and casting sum.
- **Each number alone:** no rule's number was drawn more often than chance in any game. The best single result was z +2.0 (Mei Hua casting sum in Star), and luck alone gave a best of +1.6 to +2.4 when the dates were scrambled.
- **The number ± 1:** no better; the best was +1.9.
- **All the day's rule numbers together as one ticket:** ×0.96 to ×1.00 of chance.

**Still running:**
- **#2 exact positions, #3 muhurta timing, #5 transits to each game's first-draw chart:** a few minutes each.
- **#4 triples of parameters:** about 6 hours, since it covers 240,000 combinations per game. It saves as it goes, so a container restart won't lose finished parts.
- **#6 same-date repeats:** partway through.
- **#7 ticket shape by astrology:** just restarted after I installed a missing statistics library.

**Early sign from #6 (partial):**
- Magnum Life shows nothing.
- Star Toto, with the same Chinese lunar date ±3 days and hot numbers, gives z +2.4. That beats all 50 "other date" comparisons. This was the first Star row out of several still running, so treat it as unconfirmed until the full table is in.

I'll report all seven together when they finish. The faster six should be done within the hour; triples will take longer.

**Answer:**

Six of the seven are done (triples still running). One result stands out, Star Toto with the same Chinese lunar date ±7 days (z +3.4). Checking it harder before reporting.

**Answer:**

Star has 2 draws with exactly the same 6 numbers, where chance expects 0.1. That suggests a data problem, so I'm checking the dates.

**Answer:**

Six of the seven are finished. Five show nothing beyond luck. The sixth, same-date repeats, found the most consistent pattern of the whole project in Star Toto. It isn't astrology, and it doesn't make money. The seventh, triples, is about halfway: Magnum Life and Star are done, and Power and Supreme need about 3 more hours.

| # | Test | Result |
|---|---|---|
| 1 | Tai Yi and Mei Hua numbers played directly | Chance. Best z +2.0, inside the luck range of +1.4 to +2.4. All of a day's rule numbers together scored ×0.96 to ×1.00. |
| 2 | Exact positions (longitudes in 10° steps, angles between planets in 15° steps; 42,042 leads per game) | Chance. Strong leads, the best lead and the best blind record are all within the shifted-calendar range. Leads chosen each year scored ×0.987 to ×0.999 the following year. |
| 3 | Muhurta at 19:00 (Rahu Kalam, choghadiya, void-of-course Moon, out-of-bounds Moon, eclipse season, planets near a station, panchaka) | Chance in all 4 games. Chosen leads scored ×0.990 to ×0.998 the next year. |
| 5 | Transits to each game's first-draw chart (houses, aspects, solar and lunar returns) | Chance. Magnum Life's best blind lead (+3.5) is only just above the shifted calendars' best (+3.4). |
| 7 | Draw shape by astrology (sum, odd/even, high/low, consecutive numbers) | Chance. Nothing beyond what the shifted calendars show, and predicting the shape from astrology gains nothing. |
| 6 | Same-date repeats | Nothing in Magnum Life, Power or Supreme. **Star Toto: a real-looking pattern** (below). |
| 4 | Triples of parameters (240,000 per game) | Still running; I'll report when it finishes. |

## The one notable result: Star Toto and the Chinese lunar date

The rule: for each draw, take the numbers drawn most often within a few days of **the same Chinese lunar date in earlier years**, and play the top 6. It doesn't use any planets, only the lunar calendar.

- **Every window works:** it beats chance at every window from ±3 to ±15 days (z +2.0 to +3.8, best at ±5 days).
- **The real date stands out:** I re-ran the same rule centred on 120 other dates spread around the year. The real lunar date ranks 1st to 5th of 120 every time.
- **Both halves:** it is above chance in the first and second half of the history.
- **Every year:** with ±7 days, it is above chance in **all 9 years 2018–2026** (×1.03 to ×1.30). That is as consistent as Karana × Day pillar in 4D.
- **Star only:** Magnum Life, Power and Supreme show nothing.

**Caveats:**
- **Window chosen after looking:** the first scan tried 32 versions (4 games × 2 calendars × 2 windows × hot or cold), and I picked the window widths after seeing it. So it's the strongest pattern found, but not proven.
- **No money in it:** the extra numbers are mostly 2 matches becoming 3. As a single 6-number ticket it returned **22–35% of the stake**, against about 35% for random picks.
- **Two repeated draws:** Star's history has two draws with exactly the same 6 numbers (7 Nov 2017 = 7 May 2022, and 21 Jan 2024 = 3 Jun 2026), where about 0.1 is expected. They don't fall on matching lunar dates, so they don't cause this pattern. They could be data errors worth checking against the official results.
- **Fits an earlier oddity:** Star was already the one game where astrology leads as a group beat the shifted calendars. Something tied to the calendar in Star's results may explain both, but I can't tell what.

**My suggestion:** add the **Star lunar-date rule (±7 days, hot, top 6)** to the frozen short list. Judged from Saturday on, it's the most deserving candidate so far.

Results are in `analysis/FINDINGS.md`, `analysis/SEASONAL.md`, `analysis/SEASONAL_CHECK.md`, `analysis/NUMBER_RULES_CN.md`, `analysis/SHAPE_ASTRO.md` and `analysis/FAMILY_FAIR_*.md`, all pushed. Should I add the lunar-date rule to the short list?

---

**User:**

> Star lunar-date rule (±7 days, hot, top 6) how did this perform in the last 10 draws?

**Answer:**

The Star lunar-date rule did poorly over the last 10 draws (30 Sep to 21 Oct). It matched 4 numbers in total, where chance expects 7.2, and won nothing. Each ticket used only draws before it.

| Draw | Lunar date | Ticket (top 6) | Drawn (+ bonus) | Matched |
|---|---|---|---|---|
| 30 Sep | 8/20 | **08** 13 24 33 43 50 | **08** 26 28 34 35 47 +40 | 1 |
| 3 Oct | 8/23 | 08 09 24 26 27 34 | 12 14 20 22 30 35 +37 | 0 |
| 4 Oct | 8/24 | 02 09 24 26 32 34 | 16 17 25 28 30 49 +42 | 0 |
| 7 Oct | 8/27 | 08 09 24 27 34 43 | 12 15 16 21 30 37 +38 | 0 |
| 10 Oct | 9/1 | 07 11 15 23 34 43 | 09 17 19 20 46 47 +33 | 0 |
| 11 Oct | 9/2 | 07 15 23 27 30 43 | 04 09 19 40 45 47 +05 | 0 |
| 14 Oct | 9/5 | 15 23 **27** 30 38 43 | 01 08 10 12 **27** 49 +33 | 1 |
| 17 Oct | 9/8 | **23** 28 **35** 39 43 50 | 22 **23** **35** 40 41 47 +21 | 2 |
| 18 Oct | 9/9 | 01 23 27 28 35 50 | 09 10 15 17 32 45 +29 | 0 |
| 21 Oct | 9/12 | 23 27 28 29 47 50 | 08 10 25 35 41 49 +36 | 0 |
| **Total** | | | | **4 vs 7.2 expected (×0.56), RM0 on RM10** |

These 10 draws are part of 2026, which counted toward its 9-of-9 good years, so they aren't a fresh test. Even its best year was only ×1.30, so a ×0.56 stretch of 10 draws is ordinary bad luck rather than proof that the pattern has stopped. Still, it shows how weak a ×1.10 edge is from draw to draw.

It would need many more draws to judge. Should I add it to the frozen short list so it's scored from Saturday on? Separately, the triples test is still running and I'll report it when it finishes.

---

**User:**

> ok rather than choosing only 1 ticket try for 10 tickets

**Answer:**

The 10-ticket version returned more than its stake over the whole history. Checking where that comes from and whether other dates do as well.

**Answer:**

With 10 tickets per draw, the Star lunar-date rule still won nothing in the last 10 draws: its best ticket matched 2 numbers, so it lost all RM100. Over the whole history (2018–2026), though, it is the only rule tested so far that returned more than its stake. That rests on three lucky draws, so it is not something to rely on.

The 10 tickets are made the same way as the other 10-set tests: the top 3 numbers go on every ticket, and the other 3 numbers on each ticket rotate among the next 6.

**Last 10 draws (30 Sep to 21 Oct)**

| Draw | Core (all tickets) | Rotating | Drawn | Best ticket | Prize |
|---|---|---|---|---|---|
| 30 Sep | **08** 13 43 | 09 24 **26** 33 42 50 | **08 26** 28 34 35 47 | 2 | 0 |
| 3 Oct | 08 26 34 | 09 24 27 **30** 33 43 | 12 14 20 22 **30** 35 | 1 | 0 |
| 4 Oct | 02 09 34 | 08 15 24 26 32 43 | 16 17 25 28 30 49 | 0 | 0 |
| 7 Oct | 08 09 43 | **15** 24 26 27 34 42 | 12 **15** 16 21 30 37 | 1 | 0 |
| 10 Oct | 15 23 43 | 05 07 08 11 34 38 | 09 17 19 20 46 47 | 0 | 0 |
| 11 Oct | 23 27 43 | 07 15 30 36 38 50 | 04 09 19 40 45 47 | 0 | 0 |
| 14 Oct | 23 **27** 43 | 07 15 28 30 38 50 | 01 08 10 12 **27** 49 | 1 | 0 |
| 17 Oct | **23** 28 **35** | 01 15 27 39 43 50 | 22 **23 35** 40 41 47 | 2 | 0 |
| 18 Oct | 23 28 35 | 01 04 27 43 46 50 | 09 10 15 17 32 45 | 0 | 0 |
| 21 Oct | 23 29 47 | 04 27 28 **35** 38 50 | 08 10 25 **35** 41 49 | 1 | 0 |
| **Total** | | | | **best 2** | **RM0 on RM100** |

**Whole history (1,262 draws, RM10 each)**
- **Return:** RM1.16 back per RM1, about RM2,000 profit over 8 years. Random 10-set tickets return about RM0.35.
- **Where it comes from:** almost all of it is **three draws with 5 numbers matched** (8 Feb 2022, 17 Jul 2024, 6 Apr 2025), each paying RM2,008.
- **By year:** 2018 ×0.46, 2019 ×0.72, 2020 ×0.19, 2021 ×0.30, **2022 ×1.46**, 2023 ×0.17, **2024 ×4.13**, **2025 ×1.58**, 2026 ×0.27. It was profitable in only 3 of 9 years, all because of those three draws.

**Is it luck?** I ran the same rule centred on 59 other dates around the year instead of the real lunar date.
- **Return:** their typical return is RM0.22 per RM1. Only 2 of the 59 matched or beat the real date, one of them through a jackpot.
- **5-number draws:** they average 0.25 such draws and never more than 2, so the real date's 3 is unusual.

Together with the steady extra numbers caught every year, this is the strongest pattern found anywhere in this project.

**Caveats:**
- **Chosen after looking:** I picked the ±7-day window after the first scan of 32 variants.
- **Three draws:** the profit comes from just three lucky draws. Without them it returns about RM0.2–0.7 per RM1, like random play.
- **Recent results are poor:** 2026 so far is ×0.27, and the last 10 draws returned nothing.

**My view:** this is the best candidate for watching, not for betting. I suggest adding it to the frozen short list as **Star lunar-date ±7, hot, 10 sets**, scored from Saturday. Fifty or more new draws would show whether the extra numbers keep coming. Even then, the profit depends on occasional 5-number hits.

Should I add it? The triples test is still running, and I'll report it when it finishes.

---

**User:**

> ok fine lets try to optimize the number of tickets for consistent wins please check and tehn tell me the result for the last 10 draws

**Answer:**

No number of tickets makes the Star lunar-date rule win consistently. I compared 11 plans from 1 to 28 tickets, and even the best one wins a prize in only about 1 draw in 13. In the last 10 draws, every plan won nothing.

**Why consistent wins aren't possible here:** Star Toto pays nothing below 3 matching numbers. Each ticket matches 3 or more in only about 1 draw in 50, so even 20–28 tickets per draw win in fewer than 1 draw in 10.

**Plans compared, 2018–2026 (1,262 draws)**

Each plan is built from the rule's ranking of numbers, best first. "Same plan, other dates" is the same plan using 59 other dates around the year instead of the lunar date.

| Plan | Tickets per draw | Draws with any prize | Same plan, other dates | Return per RM1 | Other dates | Worst year |
|---|---|---|---|---|---|---|
| Top 6 (1 ticket) | 1 | 3.3% | 1.8% | 0.35 | 0.19 | 0.12 |
| **Top 5 + 1 of next 2** | 2 | 4.5% | 2.6% | **1.12** | 0.19 | 0.15 |
| Top 5 + 1 of next 3 | 3 | 5.3% | 3.3% | 0.86 | 0.19 | 0.20 |
| Top 4 + 2 of next 4 | 6 | 6.2% | 4.2% | 0.83 | 0.20 | 0.13 |
| System 7 (top 7) | 7 | 5.0% | 2.9% | 0.75 | 0.19 | 0.17 |
| **10 sets (standard)** | 10 | **7.8%** | 5.5% | **1.16** | 0.22 | 0.17 |
| Top 3 + 3 of next 6 | 20 | 8.5% | 6.3% | 0.83 | 0.21 | 0.17 |
| System 8 (top 8) | 28 | 6.3% | 4.5% | 0.62 | 0.22 | 0.15 |

- **The lunar date helps in every plan.** It wins prizes about 1.5 times as often as the same plan on other dates (for example 7.8% against 5.5%).
- **The returns above RM1 all come from the same three 5-number draws** (2022, 2024, 2025). Every plan's worst year returned only RM0.12–0.20 per RM1.
- **The best two plans:**
  - 10 sets (RM10 per draw): the most frequent wins for the cost and the highest return.
  - Top 5 + 1 of the next 2 (2 tickets, RM2 per draw): almost the same return for a fifth of the cost.
- **More tickets don't help.** At 20–28 tickets the extra numbers dilute the rule's top picks, so the return falls.

**Last 10 draws (30 Sep to 21 Oct): no prize in any plan.**
- The best match on any ticket was 2 numbers, on 30 Sep and 17 Oct.
- The cost of that losing streak was RM20 for the 2-ticket plan, RM100 for 10 sets and RM280 for System 8.

**My recommendation:**
- Don't buy more tickets to chase consistent wins; it doesn't work with this game's prize structure.
- If you follow the rule, the **2-ticket plan** (RM2 per draw) captures nearly all of its long-run value at the lowest cost.
- **10 sets** wins a little more often but costs five times as much.

Either way, expect long runs with no prize, like the last 10 draws, and treat it as an experiment. Its profit so far rests on just three lucky draws.

The full table, including the last-10 results for every plan, is in `analysis/LUNAR_TICKETS.md` (made by `analysis/lunar_tickets.py`), pushed. The triples test is still running, and I'll report it when it finishes.

---

**User:**

> for the star lunar date rule, you checked only for the hot number? what about the others? and also from the previous astrological test from 1 to 7 did you do all types of analysis or only focus on the hot?

**Answer:**

You're right to ask. Here's what each test covered:

- **Star lunar-date rule:** only hot and cold. Cold showed nothing (×0.99 at ±7 days). The other five patterns weren't tried: pos, hot+100, cold+100, hot/cold100 and cold/hot100.
- **#2 exact positions, #3 muhurta, #4 triples and #5 transits:** all 7 patterns. The test engine scores every pattern for every lead.
- **#1 number rules:** patterns don't apply, because the numbers come straight from the date.
- **#7 ticket shape:** patterns don't apply either; it predicts the shape, not the numbers.
- **#6 same-date repeats:** hot and cold only, in all 4 games.

So the gap is #6. I'll rerun it now with all 7 patterns, in all 4 games, for both solar and lunar dates, at windows of 3, 5, 7 and 10 days, each checked against 59 other dates.

**Answer:**

I reran the same-date test (#6) with all 7 patterns, both calendars, all 4 games and windows of ±3, ±5, ±7 and ±10 days. Star's lunar-date effect shows up in three patterns, not just hot, so it isn't a quirk of one scoring method. Nothing similar appears in the other three games.

**Star Toto, lunar date.** Each cell is the z against chance, with the real date's rank among 60 dates in brackets (1 = best):

| ± days | hot | cold | pos | hot+100 | cold+100 | hot/cold100 | cold/hot100 |
|---|---|---|---|---|---|---|---|
| 3 | **+2.9 (1)** | −0.5 (44) | **+2.5 (1)** | +1.7 (1) | −0.2 (32) | **+2.4 (1)** | +0.9 (8) |
| 5 | **+2.7 (3)** | −0.4 (39) | **+3.1 (1)** | **+2.4 (1)** | −1.2 (55) | **+3.0 (2)** | +0.5 (20) |
| 7 | **+3.1 (2)** | −0.6 (44) | **+2.8 (1)** | +0.4 (12) | −2.2 (58) | **+2.1 (4)** | −0.4 (43) |
| 10 | **+2.4 (2)** | −1.0 (53) | **+2.7 (1)** | −0.8 (47) | −2.5 (60) | **+2.7 (3)** | +0.0 (32) |

- **Three patterns agree:** hot, pos and hot/cold100 rank 1st–4th of 60 dates at every window. All three favour numbers that came up often around the same lunar date in earlier years.
- **The cold patterns come out as mirror images:** cold and cold+100 sit at or below chance, sometimes ranking last. That is exactly what you'd see if the "hot" side is real.
- **The solar calendar date is weaker:** Star scores +1.0 to +2.2 at ranks 1–19, so the lunar date is what matters.
- **Elsewhere, nothing:**
  - Magnum Life's best is +1.9.
  - Power has one rank-1 cell at only +1.1.
  - Supreme's best is +1.9.

  These are scattered single hits, the number you'd expect from 168 tries per game.

**What each test covered:**

| Test | Patterns | Note |
|---|---|---|
| 2 exact positions, 3 muhurta, 4 triples, 5 transits | **All 7** | |
| 1 Tai Yi / Mei Hua numbers | Not applicable | The numbers come straight from the date. |
| 7 ticket shape | Not applicable | It predicts shape, not numbers. |
| 6 same-date repeats | First hot and cold only, **now all 7** | Covered above. |

**The other difference from the earlier analyses:** these new tests scored each lead by the numbers caught in its top ticket against chance. They didn't score prizes in every ticket format (10 sets, System 7 × 2, System 8 and so on), as the original pipeline did. Hits against chance is the more sensitive measure, and the prize returns for the Star rule were checked separately (shown last time). I can also run the families through the full prize pipeline if you want.

**On the Star lunar rule:**
- **pos and hot/cold100** are as strong as hot and slightly more stable across window widths. They are reasonable alternatives to the plain hot version.
- **They still need a forward test:** with the window and pattern picked after looking, only future draws can show whether any of them is real.

I can add all three (hot, pos and hot/cold100, ±7 days, 2-ticket and 10-set plans) to the frozen short list so they're scored from Saturday.

The table for all four games is in `analysis/SEASONAL7.md` (from `analysis/seasonal7.py`), pushed. Triples are about three-quarters done, and I'll report them when they finish.

---

**User:**

> ok tell me how star lunar scores for all those in past 10 draws

**Answer:**

Over the last 10 Star draws (30 Sep to 21 Oct), the three patterns that look best over the long run (hot, pos and hot/cold100) all did slightly worse than chance. The cold patterns, which sit at the bottom over the long run, did best. Chance is 7.2 numbers in each pattern's top 6 over the 10 draws.

**Top-6 numbers caught, per draw (±7 days)**

| Pattern | 30 Sep | 3 Oct | 4 Oct | 7 Oct | 10 Oct | 11 Oct | 14 Oct | 17 Oct | 18 Oct | 21 Oct | Total (chance 7.2) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hot | 2 | 0 | 0 | 1 | 0 | 0 | 1 | 2 | 0 | 0 | 6 |
| pos | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 2 | 0 | 0 | 5 |
| hot/cold100 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 2 | 0 | 1 | 7 |
| hot+100 | 2 | 0 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 1 | 7 |
| cold | 1 | 1 | 0 | 1 | 2 | 3 | 0 | 1 | 2 | 0 | **11** |
| cold+100 | 1 | 1 | 0 | 0 | 1 | 3 | 0 | 2 | 1 | 1 | **10** |
| cold/hot100 | 0 | 0 | 1 | 2 | 2 | 1 | 0 | 1 | 1 | 1 | 9 |

The hot count here (6) differs slightly from the 4 I showed last time. This version starts scoring from the 100th draw and handles ties the same way as the other pattern tests, which changes a few tickets.

**Totals for every window and pattern** (top-6 numbers caught / 2-ticket plan prize on RM20 / 10-set prize on RM100):

| Pattern | ±3 days | ±5 days | ±7 days | ±10 days |
|---|---|---|---|---|
| hot | 6 / RM26 / RM42 | 4 / 0 / RM18 | 6 / 0 / 0 | 4 / 0 / RM16 |
| pos | 6 / RM8 / RM40 | 5 / RM8 / RM16 | 5 / 0 / 0 | 5 / 0 / 0 |
| hot/cold100 | 6 / 0 / RM26 | 6 / 0 / 0 | 7 / 0 / RM8 | 5 / 0 / 0 |
| hot+100 | 7 / RM16 / RM32 | 7 / 0 / RM24 | 7 / 0 / 0 | 9 / 0 / 0 |
| cold | 10 / 0 / RM8 | **11** / RM8 / RM68 | **11 / RM24 / RM104** | 9 / 0 / 0 |
| cold+100 | 7 / RM8 / RM40 | **11** / RM8 / RM32 | 10 / RM8 / RM40 | 8 / 0 / RM8 |
| cold/hot100 | 8 / 0 / 0 | 8 / 0 / 0 | 9 / 0 / 0 | 6 / 0 / 0 |

- **Best results:** cold at ±7 days broke even, with RM104 back on RM100 for the 10 sets and RM24 on RM20 for the 2 tickets. Hot at ±3 days was the only hot version to profit on 2 tickets (RM26 on RM20).
- **No big wins:** no combination caught more than 3 numbers on any ticket, so every prize was RM8–18. Nothing came close to the 5-number hits that drove the long-run profit.
- **Is the rule failing?** Ten draws is too few to tell. A swing from 6 to 11 numbers caught between patterns is normal at this sample size. Over 1,262 draws the order is reversed: hot, pos and hot/cold100 beat 98% of other dates, while cold ranks near the bottom.

This is still a pattern to watch, not to bet on. I'd score hot, pos and hot/cold100 at ±7 days, plus cold for comparison, on every draw from Saturday. That way we'll see whether the long-run order or the recent one holds. Want me to add them to the frozen short list?

---

**User:**

> ok do more analysis into this for 10 sets not only for the last 10 draws but more and try to optimize the number of tickets to take for the day variations

**Answer:**

I'll do a full grid for the Star lunar rule:
- **Grid:** all 7 patterns × day windows ±3, ±5, ±7, ±10 and ±14 × 8 ticket plans from 1 to 28 tickets.
- **Periods:** the last 10, 50, 100, 200 and 500 draws, the whole history, and each year.
- **Fair test of the "best setup":** choose it before each year using only earlier years, then play that year blind.
- **Luck check:** the same choosing procedure run on 20 other dates around the year.

**Answer:**

I tested every combination: 7 patterns × 5 day windows (±3, 5, 7, 10, 14) × 8 ticket plans from 1 to 28 tickets. That's 280 setups, scored with the official Star prizes over the last 10, 50, 100, 200 and 500 draws, the whole history, and each year. **No combination gives consistent wins or a reliable profit.** The lunar date does help a little in every plan, but not enough to cover the stake.

## 1. "Best" setups are made by one or two lucky draws

Ranked by whole-history return, the top of the list is misleading:
- **Cold ±3, 10 sets** shows RM8.57 per RM1. Almost all of that comes from one jackpot in 2021, when that year returned RM82.77 per RM1. Every other year returned only RM0.12–1.07.
- **Hot ±7, 10 sets** (the setup from before) shows RM1.16, but its recent returns are poor:

| Period | Last 10 | Last 50 | Last 100 | Last 200 | Last 500 | All |
|---|---|---|---|---|---|---|
| Return per RM1 | 0.00 | 0.18 | 0.24 | 0.28 | 2.15 | 1.16 |

All of its profit came from 2022, 2024 and 2025. Random tickets return about RM0.35 per RM1 long-run, or about RM0.20 without big prizes.

## 2. The lunar date helps in every ticket plan, but only slightly

Median across all patterns and windows, whole history:

| Plan | Tickets per draw | Return: lunar date | Other dates | Draws with a prize: lunar | Other dates |
|---|---|---|---|---|---|
| top 6 | 1 | 0.21 | 0.16 | 1.9% | 1.6% |
| top 5 + 1 of next 2 | 2 | 0.22 | 0.17 | 2.8% | 2.3% |
| top 5 + 1 of next 3 | 3 | 0.23 | 0.17 | 3.6% | 3.0% |
| **top 4 + 2 of next 4** | **6** | **0.30** | 0.17 | 4.6% | 3.8% |
| System 7 | 7 | 0.24 | 0.17 | 3.2% | 2.7% |
| 10 sets | 10 | 0.27 | 0.19 | 5.9% | 5.0% |
| top 3 + 3 of next 6 | 20 | 0.26 | 0.19 | 6.7% | 5.8% |
| System 8 | 28 | 0.29 | 0.20 | 4.9% | 4.0% |

In every plan the real lunar date wins a prize slightly more often (about 1 extra winning draw per 100) and returns more than other dates. But even the best plan **wins a prize in only about 1 draw in 15–20**, so consistent wins aren't possible with Star's prize table.

## 3. The fair test: choose the best setup before each year, then play it

| Choice made each year on earlier years only | Fair return 2020–2026 | Other dates (median) | Other dates at or above |
|---|---|---|---|
| Any setup (pattern, window, plan) | **0.26** | 0.16 | 4 of 19 |
| top 6 (1 ticket) | 0.24 | 0.19 | 5 of 19 |
| top 5 + 1 of next 2 (2 tickets) | 0.28 | 0.16 | 3 of 19 |
| top 5 + 1 of next 3 (3 tickets) | 0.28 | 0.17 | 3 of 19 |
| top 4 + 2 of next 4 (6 tickets) | 0.31 | 0.17 | 4 of 19 |
| System 7 (7 tickets) | 0.22 | 0.16 | 6 of 19 |
| 10 sets | 0.28 | 0.19 | 7 of 19 |
| top 3 + 3 of next 6 (20 tickets) | 0.28 | 0.19 | 3 of 19 |
| System 8 (28 tickets) | 0.45 | 0.17 | 1 of 19 |

- **The rule beats other dates fairly but stays below the stake.** Played blind, it returned RM0.22–0.45 per RM1, better than other dates in most plans. You would still have lost more than half your money.
- **The "best" setup keeps changing.** Picked on past years it switched between cold ±3, hot ±10 and hot/cold100 ±7. That instability is a sign of chasing luck.
- **System 8's 0.45 is one lucky year.** It comes from a single 5-number hit in 2025.

## What to take from this

- **How many tickets:**
  - **6 tickets (top 4 + 2 of the next 4)** gives the best fair return for the cost at RM6 per draw.
  - **2 tickets (top 5 + 1 of the next 2)** is nearly as good for RM2 per draw.
  - More tickets don't raise the win rate enough to pay for themselves.
- **Which day window and pattern:** ±7 days with hot or hot/cold100 is the most stable, though it has been weak over the last 2 years.
- **Overall:** the lunar date is a genuine but small tilt. It adds about 1 extra winning draw per 100 and lifts returns from about RM0.17 to RM0.25–0.30 per RM1, still a loss of roughly 70% over time. Only rare 5-number hits ever made it profitable.

If you want to keep following it, the **6-ticket hot/cold100 ±7** plan is the most reasonable to watch. I can add it to the frozen short list and score it from Saturday.

The full tables are in `analysis/LUNAR_OPT.md` (from `analysis/lunar_opt.py`), pushed. The triples test is almost finished, and I'll report it when it completes.

**Answer:**

Good, ignored. Re-arming the wait for the last game.

**Answer:**

The triples test (#4) hasn't finished yet. Magnum Life, Star and Power are done; Supreme, the last game, is still running. My earlier wait timed out, but the test itself kept running, so nothing was lost. I've set a new wait and will report the triples results with the other six as soon as Supreme finishes.

**Answer:**

The last test (#4, triples of parameters) has finished, and it found nothing beyond chance. That completes all seven astrology tests.

**How it was tested:** every combination of three of the 114 base parameters (240,464 triples) × 7 patterns gives 1.68 million leads per game. Each was scored by how many drawn numbers land in its top ticket against chance, then compared with 2 shifted calendars and put through the fair yearly test.

| Game | Best lead, whole history (z): real (shifted) | Best record when chosen beforehand: real (shifted) | Triples chosen before each year, next year |
|---|---|---|---|
| Magnum Life | +5.0 (+4.6, +5.1) | +4.2 (+4.1, +4.4) | ×0.999 |
| Star | +4.5 (+4.7, +5.0) | +4.2 (+4.2, +4.6) | ×0.990 |
| Power | +4.2 (+5.0, +5.2) | +3.6 (+3.8, +4.2) | ×0.992 |
| Supreme | +4.8 (+5.0, +4.5) | +4.4 (+4.5, +3.8) | ×0.998 |

- **The best triples are no stronger than what scrambled calendars produce.** Out of 1.7 million leads, scores of z +4 to +5 appear by luck alone.
- **Choosing triples on their past record predicts nothing.** Triples picked before each year caught slightly *fewer* numbers than chance the next year, the same as pairs.
- **The third parameter adds nothing in Magnum Life.** Almost all of its top triples are **mars_rashi × month (cold)** plus some third parameter. That pair already led the fair yearly test, so the triples are just borrowing its record.

**All seven tests:**

| # | Test | Result |
|---|---|---|
| 1 | Tai Yi and Mei Hua numbers played directly | Chance |
| 2 | Exact planetary positions and angles | Chance |
| 3 | Muhurta at 19:00 (Rahu Kalam, choghadiya, void Moon, eclipses, stations) | Chance |
| 4 | Triples of parameters | Chance |
| 5 | Transits to each game's first-draw chart | Chance |
| 6 | Same-date repeats | Chance, except **Star Toto with the Chinese lunar date**: a small, steady edge, but it still loses about 70% of stakes over time |
| 7 | Draw shape by astrology | Chance |

So after everything tested, only two things are worth watching on future draws:
- the Star lunar-date rule (6-ticket hot/cold100 ±7 is the most reasonable version);
- mars_rashi × month (cold) for Magnum Life.

Neither has shown it can make money. I can add both to the frozen short list so the scheduled update scores them from Saturday.

Full tables are in `analysis/FAMILY_FAIR_TRIPLES.md` and `analysis/FINDINGS.md` is updated; both are pushed.

---

**User:**

> List out all the leads of today

---

**User:**

> [Request interrupted by user]

---

**User:**

> List out all the leads that needs to be observed and rank them

**Answer:**

This ranking uses only the fair evidence: how each lead did in years when it would have been picked in advance using earlier data, then scored blind. Hindsight wins don't count. None of these has made money on unseen draws, so they are for observing, not betting.

## Tier 1: strongest evidence (passed the fair yearly test)

| Rank | Game | Lead (pattern) | Evidence | Status |
|---|---|---|---|---|
| 1 | Magnum Life | **mars_rashi × month (cold)** | Picked in advance every year 2022–2026; ×1.073 more numbers than chance on 805 blind draws (z +3.5), the best blind record in Magnum Life, slightly above the shifted calendars (+2.8, +3.2). Its triples also topped the triples test. | On watchlist, **not yet on short list** |
| 2 | Supreme | **day_of_month × aspect_venus_mars (cold/hot100)** | Picked in advance 12 years running (2015–2026); ×1.082 on 1,937 blind draws (z +3.1) | Short list |
| 3 | Star | **Lunar-date rule, hot/cold100 ±7 days, 6 tickets** | Real lunar date ranks 1–4 of 60 dates in 3 patterns; above chance every year 2018–2026; fair return RM0.31 per RM1 vs 0.17 on other dates | **Not yet on short list** |
| 4 | Star | **lagna_rashi × lunar_month (pos)** | Picked in advance 2022–2026; ×1.077 blind (z +2.1) | Short list |

## Tier 2: positive but within luck

| Rank | Game | Lead (pattern) | Evidence | Status |
|---|---|---|---|---|
| 5 | Power | karana × aspect_mercury_jupiter (hot/cold100) | Picked in advance in 11 years; ×1.050 blind (z +1.9) | Short list |
| 6 | Magnum Life | rahu_nakshatra × aspect_moon_venus (cold/hot100) | Picked in advance 2021–2026; ×1.036 blind (z +1.9) | Short list |
| 7 | Star | Lunar-date rule, hot ±7 days (2 tickets or 10 sets) | Same effect as #3; profitable over the whole history only through three 5-number draws; poor last 2 years | Not yet on short list |
| 8 | Star | Lunar-date rule, pos ±7 days | Same effect, slightly weaker | Not yet on short list |

## Tier 3: watch, but expect nothing

| Rank | Game | Lead (pattern) | Why it's still here |
|---|---|---|---|
| 9 | Power | year_stem × lagna_navamsa_lord (cold) | Three 5-number hits before it was chosen, but never qualified in the fair test |
| 10 | Supreme | plum_trigrams × saturn_navamsa (hot/cold100) | Three 5-number hits before it was chosen; never qualified; its best value combination can't recur before Feb 2027 |
| 11 | Power | masa × adhika_masa (hot+100) | Won the Power jackpot on 11 Oct, but its blind record was ×1.011 (chance) |
| 12 | Toto | Mei Hua Yi Shu leads (as a group) | Best Chinese system (ranked 2nd, 1st and 4th of 21 in Star, Power and Supreme), but no single lead stands out |
| 13 | Magnum Life, Star, Power | D24 leads (as a group) | Ranked 1st, 2nd and 1st as a family; no single lead stands out |

**In 4D** (the other project, tracked there):
- **Karana × Day pillar (S1, i-Box):** the most consistent 4D lead, above chance 14 of 15 years, but a small edge.
- **Mercury nakshatra × Venus rashi (S1, Straight):** won the Magnum 2nd prize on 21 Oct.

**Everything else on the 83-entry watchlist** never qualified in the fair test, so its good results are hindsight only. That includes the 18 Oct RM110k winner, the Grand prize lead and the 17 Oct Supreme hits. They are still scored each draw, but I'd ignore them.

**Two decisions for you:**
1. Should I add #1 (mars_rashi × month) and #3 (Star lunar-date hot/cold100 ±7, 6 tickets) to the frozen short list before Saturday's draw? They currently have the best evidence but aren't on it.
2. Should I drop Tier 3 and the rest of the watchlist from the report, so each update shows only Tiers 1–2?

---

**User:**

> 1. Yes add that
> 2. No include all the tiers
> 
> Ok now, from all the leads, try to check if a combination of each other will produce a better lead

**Answer:**

I'll add a lunar-date "lead" type to the scorer, add both to the short list, then test combinations.

**Answer:**

Both are added and score correctly. Now the combination test.

**Answer:**

Both leads are now on the frozen short list, and every tier stays in the reports.
- **mars_rashi × month (cold):** Magnum Life, System 10.
- **Star lunar-date rule (hot/cold100, ±7 days):** played as 6 tickets and as 10 sets.

I checked both score correctly on the 21 Oct draw. Saturday's update will be their first scored draw.

**Combining leads doesn't produce a better lead.** For every game I merged each pair and triple of that game's observed leads into one ticket, by adding up how highly each lead ranks every number. I scored the results the same way as the fair test (numbers caught in the top ticket, against chance) and checked them against 5 shifted calendars.

| Game | Best single lead, forward years | Best combination, forward years | Verdict |
|---|---|---|---|
| Magnum Life | mars_rashi × month: ×1.073 (z +3.5) | + rahu_nakshatra × aspect_moon_venus: ×1.026 (+1.3) | **Combining weakens it** |
| Star | lunar-date hot/cold100: ×1.090 (+2.4) | + lagna_rashi × lunar_month: ×1.078 (+2.1) | Weaker |
| Power | karana × aspect_mercury_jupiter: ×1.054 (+1.9) | + masa × adhika_masa: ×1.032 (+1.1) | Weaker; the 3-way blend falls to chance (×0.995) |
| Supreme | day_of_month × aspect_venus_mars: ×1.075 (+2.6) | + plum_trigrams × saturn_navamsa: ×1.076 (+2.6) | No change |

Forward years are 2022 onwards for Magnum Life and Star, and 2017 onwards for Power and Supreme.

- **The strong lead gets diluted.** Each game's best lead does better alone. Blending in a weaker lead pulls its numbers down the ranking.
- **Leads don't add up.** If the leads were catching different real effects, combining them should strengthen the signal. It doesn't, which suggests each lead's small edge is its own and largely luck.
- **Shifted calendars sit around chance** (median z −0.9 to +0.9), so the single leads' edges are bigger than what scrambled dates produce. The combinations add nothing on top.
- **Prize returns didn't improve either.** The Star lunar rules alone returned RM1.31–1.67 per RM1 on 10 sets over 2022–2026. That comes from the same two or three 5-number draws, and in combination it drops to RM0.42–0.53.

**So the short list stays as single leads:**

| Rank | Game | Lead |
|---|---|---|
| 1 | Magnum Life | mars_rashi × month (cold) |
| 2 | Supreme | day_of_month × aspect_venus_mars (cold/hot100) |
| 3 | Star | lunar-date rule (hot/cold100 ±7) |
| 4 | Star | lagna_rashi × lunar_month (pos) |
| 5 | Power | karana × aspect_mercury_jupiter (hot/cold100) |
| 6 | Magnum Life | rahu_nakshatra × aspect_moon_venus (cold/hot100) |

Tiers 2–3 and the rest of the watchlist will still be scored and reported after each draw.

The results are in `analysis/COMBINE_LEADS.md`, made by `analysis/combine_leads.py`, and pushed. The update after Saturday's draw is scheduled for 24 Oct at 21:30 Malaysia time.

---

**User:**

> ok im wondering if shadbala or ashtakavarga matrix are used in your analysis?

**Answer:**

No. Neither Shadbala nor Ashtakavarga has been used anywhere, in the lotto work or the 4D project. I searched the code of both and neither appears.

**What we do use that's related:**
- **Dignity-like flags:** retrograde and combust status for each planet.
- **Vargottama counts** from D9 and the other divisional charts (part of Shadbala's positional strength).
- **Hora lord**, which relates to Shadbala's time-based strength.
- **Aspect counts** (soft and hard), a rough stand-in for aspect strength.

None of these combines into a planet's overall strength the way Shadbala does, and nothing scores the signs the way Ashtakavarga does.

**What they would add:**
- **Shadbala:** the six-fold strength of each of the 7 planets, made up of:
  - positional strength (exaltation, own sign, friendly signs and divisional dignity);
  - directional strength (by house from the Lagna);
  - time-based strength (day or night, paksha, hora, weekday, year, month);
  - motional strength (speed and retrogression);
  - natural strength;
  - aspectual strength.

  Testable as each planet's strength in bands, which planet is strongest, and whether the strongest planet is a benefic.
- **Ashtakavarga:** each planet's bindu score (0–8) in the sign it occupies, plus the total (Sarvashtakavarga) score of the sign of the Moon, the Lagna and each transiting planet. That is the classic way to judge whether a transit is favourable.

**How I'd test them:** add about 25–30 parameters for the draw time and run them through the same fair test as the last seven ideas:
- alone and paired with the 114 base parameters, × all 7 patterns;
- against 5 shifted calendars;
- with leads chosen before each year, then scored that year blind.

One limitation: Ashtakavarga and parts of Shadbala depend on the Lagna and planet signs, which we already test individually. If they show anything, it will be because they combine those signs in a new way.

Effort: building and checking the two calculations against textbook rules takes about 1–2 hours, plus about 30 minutes of testing. Should I go ahead?

---

**User:**

> yes sure

**Answer:**

I'll implement both from the classical tables, checking that the Ashtakavarga totals come out right (Sun 48, Moon 49, Mars 39, Mercury 54, Jupiter 56, Venus 52, Saturn 39, total 337). Then I'll run them through the same fair test.

**Answer:**

Both are built and tested. In three of the four games they show nothing. In Star Toto they show a small group effect that has to be checked against the earlier Star result before it can be trusted.

**What I built** (`analysis/strength.py`, 21 parameters for every draw date):
- **Ashtakavarga** (Parashari benefic-place tables): each planet's own bindus in the sign it occupies, and the Sarvashtakavarga bindus of the Moon's, Lagna's and Sun's signs. The tables are checked: the totals come out exactly as in the texts (Sun 48, Moon 49, Mars 39, Mercury 54, Jupiter 56, Venus 52, Saturn 39, total 337).
- **Shadbala, simplified** (from: exaltation, sign dignity by natural friendship, directional strength, paksha, retrogression, natural strength): each planet's total in five bands, the strongest and weakest planet, and benefics minus malefics.
  - Left out: aspect strength (Drik), most of the time-based strength (Kala), and speed-based motional strength (Chesta; only retrogression counts). So it is an approximation, not full classical Shadbala.

**Fair test:** each parameter alone and paired with the 114 base parameters, × 7 patterns, is 18,375 leads per game, compared with 5 shifted calendars:

| Game | Leads with z > 2: real (shifted) | Chosen before each year, next year: real (shifted) | Best blind z: real (shifted) |
|---|---|---|---|
| Magnum Life | 295 (317–441) | ×1.000 (×0.995–1.000) | +3.1 (+2.5 to +3.2) |
| **Star** | **513 (204–369)** | **×1.007, z +3.2 (all 5 shifted below ×1.000)** | +3.8 (+2.7 to +3.9) |
| Power | 185 (162–281) | ×0.994 (×0.988–0.996) | +3.3 (+2.6 to +3.3) |
| Supreme | 340 (305–590) | ×1.000 (×0.997–1.009) | +2.8 (+2.8 to +3.8) |

**Magnum Life, Power and Supreme are at chance.** Everything sits inside the shifted-calendar range.

**Star is above chance as a group:**
- It has more strong leads than any shifted calendar.
- Leads picked before each year kept a small edge the next year. This is the first family where that happened, and every shifted calendar fell below chance.

The strongest leads mostly involve the **Moon's strength (sb_moon)** and use the cold pattern:
- moon_phase × sb_moon (cold): blind z +3.8.
- draw_in_daylight × sb_mercury (cold): blind z +3.4.

**Read this with care.** Star is the game that has stood out every time: astrology leads as a group beat the shifted calendars, and the lunar-date rule worked there. The Moon's Shadbala here is mostly driven by paksha (the Moon's phase), which follows the lunar calendar. So this is very likely the **same Star lunar-cycle effect showing up again**, not a separate Shadbala effect. The best single leads are no stronger than the best shifted ones, and the edge is tiny (×1.007).

**So Shadbala and Ashtakavarga add nothing new.** The one signal points back to the Star lunar pattern already on the short list. I'd add **moon_phase × sb_moon (cold)** to the watchlist as a Star check alongside it, not to the short list.

Should I add it? Results are in `analysis/FAMILY_FAIR_STRENGTH.md`, and everything is committed and pushed.

---

**User:**

> no no add that to short list

**Answer:**

Done. **moon_phase × sb_moon (cold)** is now on the frozen short list for Star Toto, scored as 10 sets and as a System 8. A test score on the 21 Oct draw works.

The scoring script couldn't read the Shadbala and muhurta parameters before, so I extended it to load them. That means these newer parameter families can now be watched too.

**The short list, in rank order:**

| Rank | Game | Lead (pattern) | Formats |
|---|---|---|---|
| 1 | Magnum Life | mars_rashi × month (cold) | System 10 |
| 2 | Supreme | day_of_month × aspect_venus_mars (cold/hot100) | 10 sets, System 8 |
| 3 | Star | lunar-date rule, hot/cold100 ±7 days | 6 tickets, 10 sets |
| 4 | Star | lagna_rashi × lunar_month (pos) | 10 sets, System 8 |
| 5 | Star | **moon_phase × sb_moon (cold)**, new | 10 sets, System 8 |
| 6 | Power | karana × aspect_mercury_jupiter (hot/cold100) | 10 sets, System 8 |
| 7 | Magnum Life | rahu_nakshatra × aspect_moon_venus (cold/hot100) | 10 tickets, System 10 |
| 8 | Power | year_stem × lagna_navamsa_lord (cold) | 10 sets |
| 9 | Supreme | plum_trigrams × saturn_navamsa (hot/cold100) | 10 sets |

Tiers 2–3 and the rest of the watchlist will still be scored and reported, as you asked.

All are judged from Saturday 24 Oct, with no changes allowed. After each draw, the scheduled update (21:30 Malaysia time) scores them and adds the running numbers-caught-vs-chance count to the report. Everything is committed and pushed.

---

**User:**

> Make sure the conversation that we have from the start till now in this session is being pushed into GitHub

