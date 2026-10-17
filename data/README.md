# Malaysian lottery draw history

Historical draw results scraped from [lotto-8.com](https://www.lotto-8.com/Malaysia/) on 2026-10-17 using the TinyFish fetch tool. Every available page of each game's "Past Draw Results" list was collected.

| File | Game | Draws | First draw | Last draw | Columns |
| --- | --- | --- | --- | --- | --- |
| `star_toto_6_50.csv` | STAR TOTO 6/50 | 1,437 | 2017-10-21 | 2026-10-17 | `n1`–`n6`, `bonus` |
| `power_toto_6_55.csv` | POWER TOTO 6/55 | 2,856 | 2009-10-31 | 2026-10-17 | `n1`–`n6` |
| `supreme_toto_6_58.csv` | SUPREME TOTO 6/58 | 2,786 | 2010-03-20 | 2026-10-17 | `n1`–`n6` |
| `magnum_life.csv` | Magnum Life 8/36 | 1,346 | 2018-04-25 | 2026-10-17 | `n1`–`n8`, `bonus1`, `bonus2` |

Each CSV also has `draw_date` (ISO `YYYY-MM-DD`) and `day` (`WED`/`SAT`/`SUN`, or `TUE` for special draws). Rows are sorted from oldest to newest, and numbers are zero-padded as they appear on the site.

The site covers less history than the operators' full records: STAR TOTO 6/50 and Magnum Life only go back to 2017 and 2018.

## Source

| Game | URL | Pages |
| --- | --- | --- |
| STAR TOTO 6/50 | `https://www.lotto-8.com/Malaysia/listltoTOTO50.asp?indexpage=N&orderby=new` | 63 |
| POWER TOTO 6/55 | `https://www.lotto-8.com/Malaysia/listltoTOTO55.asp?indexpage=N&orderby=new` | 125 |
| SUPREME TOTO 6/58 | `https://www.lotto-8.com/Malaysia/listltoTOTO58.asp?indexpage=N&orderby=new` | 122 |
| Magnum Life | `https://www.lotto-8.com/Malaysia/listltoML8.asp?indexpage=N&orderby=new` | 59 |

The scraped tables are kept verbatim in `raw/`, one draw per line as `DD/MM/YY|main numbers|bonus numbers`.

## Rebuilding and validation

```sh
python3 scripts/build_csv.py
```

The script regenerates the CSVs from `raw/`. It fails if any row has an invalid date, a duplicate draw date, the wrong number count, a number out of range, or a repeated number within a draw. The row count for each game matches the site's pagination: 23 draws per page, with a shorter last page.

## Corrections verified against other sources

lotto-8.com had a few errors. Each one was checked against [lottolyzer.com](https://en.lottolyzer.com/history/malaysia/), which lists results with official draw numbers, and fixed in `raw/`:

| Game | Draw date | lotto-8.com | Corrected (lottolyzer) |
| --- | --- | --- | --- |
| POWER TOTO 6/55 | 2023-04-05 | missing | `04 29 32 39 41 48` (draw 5619) |
| POWER TOTO 6/55 | 2017-01-01 | `04 09 08 44 46 50` (unsorted) | `04 08 09 44 46 50` (draw 4529) |
| Magnum Life | 2025-02-23 | copy of 2025-02-22 | `02 05 10 11 17 18 34 35` + `08 29` (draw 168/25) |
| Magnum Life | 2025-03-29 | copy of 2025-03-26 | `02 12 23 24 27 33 34 35` + `01 08` (draw 182/25) |
| Magnum Life | 2025-04-27 | copy of 2025-04-26 | `06 09 10 13 16 19 25 34` + `07 31` (draw 195/25) |

In each Magnum Life case the earlier date's result is correct; lotto-8.com repeated it on the following draw.

Magnum Life also has two Tuesday special draws, on 2018-06-19 and 2018-08-14. These are genuine and have no Sports Toto equivalent.
