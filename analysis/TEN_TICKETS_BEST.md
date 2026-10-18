# Best single-ticket matches, 10 tickets per draw, last 10 draws

From `ten_tickets_results.json`. *Best per draw* = sum over the 10 draws of the best ticket's matches. *Max* = most numbers any one ticket matched, with the chance that the same tickets reach it at least once on fair draws. Chances from 20,000 simulated fair draw sets.

| Rank | Game | Method | Best per draw, summed (expected) | Chance | Max in one ticket (chance) | 3+ tickets (expected; chance) | 4+ tickets (expected) |
|---|---|---|---|---|---|---|---|
| 1 | Power 6/55 | baseline: replay previous draw | 19 (11.67) | 0.5% | 3 (40.5%) | 4 (1.329; 10.9%) | 0 (0.06) |
| 2 | Power 6/55 | selected params last/greedy (moon_sign_tropical + jupiter_nakshatra) | 17 (10.33) | 1.1% | 3 (35.7%) | 9 (1.336; 3.4%) | 0 (0.06) |
| 3 | Magnum Life | cell lead #1: moon_rashi × mars_combust (pos, weakest z +1.68) | 31 (24.06) | 2.9% | 5 (22.4%) | 41 (23.649; 7.0%) | 13 (5.38) |
| 4 | Supreme 6/58 | hot+cold (4 hot (last 100) + 2 cold (last 200)) | 15 (9.86) | 4.2% | 2 (94.4%) | 0 (1.125; 100.0%) | 0 (0.05) |
| 5 | Magnum Life | analogy direct | 31 (25.17) | 4.7% | 6 (2.1%) | 41 (23.634; 7.7%) | 13 (5.40) |
| 6 | Supreme 6/58 | cell lead #1: jupiter_rashi × jupiter_retrograde (hot, weakest z +1.65) | 15 (10.57) | 6.6% | 3 (35.0%) | 3 (1.144; 13.7%) | 0 (0.05) |
| 7 | Magnum Life | cell lead #3: mars_rashi × venus_combust (cold, weakest z +1.51) | 30 (24.61) | 7.0% | 5 (23.2%) | 42 (23.505; 6.1%) | 22 (5.36) |
| 8 | Power 6/55 | cell lead #2: ayana × kp_moon_number (cold, weakest z +1.46) | 14 (10.08) | 9.7% | 3 (35.0%) | 1 (1.334; 35.2%) | 0 (0.06) |
| 9 | Power 6/55 | cell lead #1: year_yinyang × day_god (cold, weakest z +1.69) | 14 (10.35) | 11.5% | 2 (95.6%) | 0 (1.318; 100.0%) | 0 (0.06) |
| 10 | Magnum Life | hot/cold + astrology (venus_nakshatra × planets_with_moon) | 29 (24.63) | 11.8% | 4 (80.9%) | 33 (23.547; 20.0%) | 10 (5.37) |
| 11 | Magnum Life | embedding ppmi | 28 (23.79) | 13.3% | 5 (22.1%) | 29 (23.462; 30.3%) | 12 (5.40) |
| 12 | Power 6/55 | cell lead #3: moon_rashi × jupiter_retrograde (cold, weakest z +1.41) | 13 (9.69) | 13.8% | 3 (32.8%) | 1 (1.317; 33.1%) | 0 (0.06) |
| 13 | Power 6/55 | baseline: hot last 100 | 14 (10.77) | 14.4% | 3 (38.1%) | 7 (1.3; 6.2%) | 0 (0.07) |
| 14 | Supreme 6/58 | selected params last/greedy (hora_lord + karana + yellow_black_path…) | 13 (9.84) | 15.1% | 2 (94.1%) | 0 (1.152; 100.0%) | 0 (0.05) |
| 15 | Star 6/50 | hot+cold (3 hot (last 300) + 3 cold (last 200)) | 14 (11.17) | 18.9% | 3 (43.9%) | 4 (1.746; 18.0%) | 0 (0.08) |
| 16 | Star 6/50 | cold numbers (N=200) | 14 (11.25) | 20.0% | 3 (44.9%) | 3 (1.755; 23.9%) | 0 (0.09) |
| 17 | Magnum Life | cell lead #5: hora_lord × venus_rashi (pos, weakest z +1.36) | 27 (23.72) | 20.3% | 4 (78.4%) | 43 (23.481; 5.1%) | 17 (5.38) |
| 18 | Star 6/50 | analogy last | 14 (11.43) | 21.7% | 3 (44.1%) | 1 (1.738; 44.5%) | 0 (0.09) |
| 19 | Power 6/55 | cell lead #4: moon_navamsa × mansion_28 (cold, weakest z +1.37) | 13 (10.54) | 21.8% | 3 (35.6%) | 3 (1.341; 17.9%) | 0 (0.06) |
| 20 | Magnum Life | analogy map | 27 (23.97) | 22.1% | 6 (2.0%) | 36 (23.63; 14.2%) | 15 (5.36) |
| 21 | Magnum Life | analogy similar | 27 (24.3) | 25.6% | 5 (22.7%) | 30 (23.488; 28.0%) | 13 (5.36) |
| 22 | Star 6/50 | hot numbers (N=300) | 13 (10.8) | 25.9% | 2 (96.6%) | 0 (1.751; 100.0%) | 0 (0.09) |
| 23 | Supreme 6/58 | baseline: hot last 100 | 12 (9.86) | 26.1% | 2 (94.2%) | 0 (1.15; 100.0%) | 0 (0.05) |
| 24 | Supreme 6/58 | hot numbers (N=100) | 12 (9.89) | 26.2% | 2 (94.1%) | 0 (1.14; 100.0%) | 0 (0.05) |
| 25 | Supreme 6/58 | embedding ppmi | 12 (10.14) | 29.2% | 2 (94.7%) | 0 (1.142; 100.0%) | 0 (0.05) |
| 26 | Power 6/55 | analogy last | 12 (10.32) | 31.2% | 2 (95.4%) | 0 (1.343; 100.0%) | 0 (0.06) |
| 27 | Magnum Life | embedding neural+prev | 25 (22.88) | 31.6% | 4 (74.6%) | 21 (23.508; 58.5%) | 2 (5.33) |
| 28 | Magnum Life | analogy last | 26 (24.03) | 33.0% | 4 (80.2%) | 31 (23.48; 24.9%) | 14 (5.43) |
| 29 | Supreme 6/58 | analogy map | 11 (9.63) | 35.8% | 3 (32.1%) | 1 (1.123; 31.5%) | 0 (0.05) |
| 30 | Star 6/50 | cell lead #1: tithi × hour_stem_19h (pos, weakest z +1.61) | 12 (11.03) | 42.1% | 2 (97.0%) | 0 (1.79; 100.0%) | 0 (0.10) |
| 31 | Magnum Life | embedding neural | 23 (21.89) | 42.7% | 4 (70.2%) | 23 (23.513; 51.2%) | 3 (5.33) |
| 32 | Star 6/50 | hot/cold + astrology (mercury_combust × day_officer) | 12 (11.31) | 46.4% | 2 (97.6%) | 0 (1.772; 100.0%) | 0 (0.09) |
| 33 | Star 6/50 | baseline: replay previous draw | 13 (12.51) | 49.3% | 3 (48.5%) | 9 (1.754; 6.5%) | 0 (0.09) |
| 34 | Star 6/50 | embedding ppmi | 12 (11.52) | 49.5% | 3 (45.3%) | 3 (1.744; 24.6%) | 0 (0.09) |
| 35 | Power 6/55 | hot numbers (half-life 5) | 11 (10.58) | 50.1% | 3 (36.8%) | 1 (1.345; 36.8%) | 0 (0.06) |
| 36 | Power 6/55 | analogy direct | 10 (9.61) | 50.3% | 2 (93.2%) | 0 (1.339; 100.0%) | 0 (0.06) |
| 37 | Power 6/55 | selected params last/top_m (moon_sign_tropical + nine_star_year + day_branch…) | 11 (10.72) | 52.2% | 2 (95.9%) | 0 (1.366; 100.0%) | 0 (0.06) |
| 38 | Star 6/50 | selected params last/greedy (day_element + nakshatra + sun_sign_tropical) | 12 (11.77) | 53.4% | 2 (98.0%) | 0 (1.778; 100.0%) | 0 (0.10) |
| 39 | Magnum Life | baseline: replay previous draw | 25 (24.83) | 53.6% | 4 (81.8%) | 13 (23.574; 84.4%) | 2 (5.48) |
| 40 | Magnum Life | cold numbers (N=15) | 23 (22.87) | 53.7% | 4 (74.7%) | 19 (23.601; 65.7%) | 4 (5.34) |
| 41 | Supreme 6/58 | analogy similar | 10 (9.83) | 54.1% | 3 (31.7%) | 5 (1.161; 8.7%) | 0 (0.05) |
| 42 | Power 6/55 | embedding neural | 11 (10.92) | 55.2% | 3 (39.2%) | 10 (1.324; 3.4%) | 0 (0.06) |
| 43 | Star 6/50 | selected params direct/top_m (ritu) | 12 (12.06) | 57.5% | 3 (47.7%) | 2 (1.782; 32.4%) | 0 (0.09) |
| 44 | Star 6/50 | baseline: hot last 100 | 11 (11.11) | 58.0% | 3 (44.5%) | 3 (1.78; 25.1%) | 0 (0.09) |
| 45 | Star 6/50 | cell lead #5: saturn_nakshatra × nine_star_month (pos, weakest z +1.18) | 11 (11.29) | 60.7% | 3 (44.5%) | 2 (1.755; 31.9%) | 0 (0.10) |
| 46 | Star 6/50 | cell lead #3: nakshatra_lord × karana (hot, weakest z +1.27) | 11 (11.32) | 60.9% | 2 (97.4%) | 0 (1.745; 100.0%) | 0 (0.09) |
| 47 | Supreme 6/58 | baseline: random | 18 (18.08) | 61.0% | 3 (68.3%) | 1 (1.142; 68.1%) | 0 (0.05) |
| 48 | Magnum Life | baseline: random | 34 (34.22) | 61.6% | 4 (99.6%) | 22 (23.591; 68.2%) | 5 (5.39) |
| 49 | Magnum Life | selected params last/greedy (hora_lord + day_god + lunar_leap_month…) | 23 (23.84) | 65.2% | 3 (99.7%) | 26 (23.663; 40.8%) | 0 (5.41) |
| 50 | Power 6/55 | hot/cold + astrology (karana × adhika_masa) | 10 (10.7) | 67.1% | 2 (96.2%) | 0 (1.3; 100.0%) | 0 (0.06) |
| 51 | Power 6/55 | analogy map | 9 (9.72) | 67.3% | 2 (93.6%) | 0 (1.339; 100.0%) | 0 (0.07) |
| 52 | Power 6/55 | analogy similar | 9 (9.74) | 67.3% | 2 (93.9%) | 0 (1.317; 100.0%) | 0 (0.06) |
| 53 | Star 6/50 | selected params direct/greedy (ritu + jupiter_rashi + day_element) | 11 (11.8) | 68.0% | 3 (46.6%) | 1 (1.754; 46.5%) | 0 (0.09) |
| 54 | Magnum Life | selected params direct/greedy (jupiter_rashi + samvatsara) | 22 (23.22) | 69.0% | 4 (77.2%) | 31 (23.556; 25.0%) | 11 (5.35) |
| 55 | Star 6/50 | analogy direct | 10 (10.96) | 70.2% | 3 (42.9%) | 1 (1.77; 42.5%) | 0 (0.09) |
| 56 | Supreme 6/58 | cell lead #2: mars_rashi × year_element (hot, weakest z +1.38) | 10 (10.92) | 70.6% | 2 (96.4%) | 0 (1.163; 100.0%) | 0 (0.05) |
| 57 | Supreme 6/58 | analogy last | 9 (9.96) | 70.9% | 3 (32.2%) | 1 (1.118; 31.9%) | 0 (0.05) |
| 58 | Magnum Life | selected params direct/top_m (jupiter_rashi + lagna_nakshatra + mercury_combust) | 23 (24.56) | 73.4% | 4 (81.0%) | 27 (23.511; 37.1%) | 7 (5.37) |
| 59 | Magnum Life | cell lead #4: jupiter_rashi × planets_with_moon (pos, weakest z +1.39) | 22 (23.85) | 75.1% | 4 (79.3%) | 22 (23.43; 54.1%) | 5 (5.35) |
| 60 | Power 6/55 | embedding ppmi | 9 (10.38) | 76.2% | 2 (95.7%) | 0 (1.332; 100.0%) | 0 (0.06) |
| 61 | Star 6/50 | embedding neural | 9 (10.44) | 76.3% | 3 (39.6%) | 1 (1.764; 39.8%) | 0 (0.09) |
| 62 | Magnum Life | hot numbers (N=150) | 22 (24.02) | 76.8% | 4 (79.5%) | 21 (23.6; 58.6%) | 1 (5.38) |
| 63 | Supreme 6/58 | hot/cold + astrology (paksha × rahu_rashi) | 8 (9.43) | 76.9% | 2 (92.7%) | 0 (1.148; 100.0%) | 0 (0.05) |
| 64 | Supreme 6/58 | selected params last/top_m (hora_lord) | 9 (10.42) | 77.1% | 2 (95.1%) | 0 (1.126; 100.0%) | 0 (0.05) |
| 65 | Magnum Life | hot+cold (1 hot (last 50) + 7 cold (last 10)) | 21 (23.11) | 77.2% | 3 (99.5%) | 24 (23.59; 48.1%) | 0 (5.37) |
| 66 | Supreme 6/58 | selected params direct/greedy (kp_sun_star_lord + day_branch + month_stem…) | 8 (9.67) | 79.7% | 2 (93.5%) | 0 (1.16; 100.0%) | 0 (0.05) |
| 67 | Power 6/55 | cell lead #5: yoga × ritu (pos, weakest z +1.36) | 9 (10.7) | 79.8% | 2 (96.0%) | 0 (1.359; 100.0%) | 0 (0.07) |
| 68 | Magnum Life | selected params last/top_m (hora_lord + day_of_month + weekday…) | 21 (23.45) | 80.5% | 4 (77.9%) | 14 (23.733; 82.2%) | 2 (5.42) |
| 69 | Star 6/50 | baseline: random | 18 (19.56) | 85.2% | 3 (82.6%) | 1 (1.772; 83.0%) | 0 (0.09) |
| 70 | Star 6/50 | selected params last/top_m (day_element) | 9 (11.28) | 85.3% | 2 (97.4%) | 0 (1.794; 100.0%) | 0 (0.09) |
| 71 | Supreme 6/58 | cell lead #4: solar_term × month_pillar (pos, weakest z +1.34) | 7 (9.18) | 85.6% | 2 (92.0%) | 0 (1.141; 100.0%) | 0 (0.05) |
| 72 | Supreme 6/58 | cell lead #3: solar_term × month_stem (pos, weakest z +1.34) | 7 (9.17) | 85.7% | 2 (91.6%) | 0 (1.129; 100.0%) | 0 (0.05) |
| 73 | Power 6/55 | baseline: random | 17 (18.62) | 85.9% | 2 (100.0%) | 0 (1.322; 100.0%) | 0 (0.06) |
| 74 | Supreme 6/58 | cold numbers (N=200) | 6 (8.27) | 86.4% | 1 (100.0%) | 0 (1.148; 100.0%) | 0 (0.05) |
| 75 | Power 6/55 | embedding neural+prev | 8 (10.39) | 86.4% | 3 (37.7%) | 10 (1.369; 3.4%) | 0 (0.07) |
| 76 | Magnum Life | cell lead #2: yoga × mars_rashi (hot, weakest z +1.56) | 20 (23.37) | 87.2% | 3 (99.7%) | 9 (23.641; 92.8%) | 0 (5.42) |
| 77 | Power 6/55 | hot+cold (6 cold (last 50)) | 7 (9.53) | 87.9% | 2 (93.1%) | 0 (1.355; 100.0%) | 0 (0.06) |
| 78 | Supreme 6/58 | selected params direct/top_m (kp_sun_star_lord) | 8 (10.49) | 88.4% | 3 (34.6%) | 1 (1.126; 34.9%) | 0 (0.05) |
| 79 | Star 6/50 | cell lead #4: nakshatra × lagna_rashi (pos, weakest z +1.21) | 9 (11.76) | 89.6% | 2 (97.8%) | 0 (1.765; 100.0%) | 0 (0.10) |
| 80 | Star 6/50 | embedding neural+prev | 7 (9.82) | 89.8% | 2 (94.4%) | 0 (1.753; 100.0%) | 0 (0.09) |
| 81 | Magnum Life | baseline: hot last 100 | 20 (24.11) | 91.6% | 3 (99.7%) | 9 (23.634; 93.1%) | 0 (5.44) |
| 82 | Star 6/50 | analogy similar | 8 (11.12) | 91.8% | 3 (43.1%) | 1 (1.766; 43.7%) | 0 (0.09) |
| 83 | Star 6/50 | analogy map | 8 (11.14) | 91.9% | 3 (43.0%) | 1 (1.771; 43.5%) | 0 (0.09) |
| 84 | Supreme 6/58 | embedding neural+prev | 7 (10.23) | 92.8% | 2 (95.2%) | 0 (1.163; 100.0%) | 0 (0.05) |
| 85 | Supreme 6/58 | analogy direct | 6 (9.13) | 93.0% | 2 (91.6%) | 0 (1.137; 100.0%) | 0 (0.05) |
| 86 | Supreme 6/58 | cell lead #5: yoga × month_branch (hot, weakest z +1.34) | 7 (10.29) | 93.6% | 2 (95.0%) | 0 (1.15; 100.0%) | 0 (0.05) |
| 87 | Power 6/55 | cold numbers (half-life 20) | 8 (11.55) | 95.1% | 2 (97.5%) | 0 (1.298; 100.0%) | 0 (0.07) |
| 88 | Star 6/50 | cell lead #2: karana × jupiter_combust (pos, weakest z +1.35) | 7 (11.04) | 96.3% | 2 (96.9%) | 0 (1.755; 100.0%) | 0 (0.09) |
| 89 | Supreme 6/58 | embedding neural | 6 (10.2) | 97.2% | 2 (95.3%) | 0 (1.093; 100.0%) | 0 (0.05) |
| 90 | Supreme 6/58 | baseline: replay previous draw | 7 (11.45) | 98.2% | 1 (100.0%) | 0 (1.152; 100.0%) | 0 (0.05) |
| 91 | Power 6/55 | selected params direct/greedy (venus_nakshatra + nayin + kp_asc_star_lord…) | 4 (9.94) | 99.7% | 1 (100.0%) | 0 (1.324; 100.0%) | 0 (0.07) |
| 92 | Power 6/55 | selected params direct/top_m (venus_nakshatra + hour_stem_19h + day_officer) | 4 (10.56) | 99.9% | 2 (95.8%) | 0 (1.325; 100.0%) | 0 (0.06) |
