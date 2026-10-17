# Malaysian lottery draw history

Historical draw results scraped from [lotto-8.com](https://www.lotto-8.com/Malaysia/) on 2026-10-17 using the TinyFish fetch tool. Every available page of each game's "Past Draw Results" list was collected.

| File | Game | Draws | First draw | Last draw | Columns |
| --- | --- | --- | --- | --- | --- |
| `star_toto_6_50.csv` | STAR TOTO 6/50 | 1,437 | 2017-10-21 | 2026-10-17 | `n1`–`n6`, `bonus` |
| `power_toto_6_55.csv` | POWER TOTO 6/55 | 2,855 | 2009-10-31 | 2026-10-17 | `n1`–`n6` |
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

## Quirks in the source data

These are kept as published:

- **Missing draw.** POWER TOTO 6/55 has no row for 2023-04-05, although the other Sports Toto games drew on that day.
- **Unsorted numbers.** The POWER TOTO 6/55 draw on 2017-01-01 is listed as `04, 09, 08, 44, 46, 50`, out of ascending order.
- **Repeated results.** Magnum Life shows identical results on consecutive dates three times: 2025-02-22/23, 2025-03-26/29 and 2025-04-26/27. These look like publishing errors on lotto-8.com. Check them against the official Magnum results before relying on them.
- **Extra draws.** Magnum Life has two Tuesday special draws, on 2018-06-19 and 2018-08-14, that have no Sports Toto equivalent.
