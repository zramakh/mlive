# mlive

Malaysian lottery draw history and an astrology-based prediction study.

- [`data/`](data/README.md): every STAR TOTO 6/50, POWER TOTO 6/55, SUPREME TOTO 6/58 and Magnum
  Life result available on lotto-8.com, with corrections checked against lottolyzer.com.
  `data/astro_params.csv` holds the 83 Vedic, KP and Chinese almanac parameters of every draw date.
- [`analysis/`](analysis/FINDINGS.md): fairness tests, conditional scans, numerology, and
  frozen, forward-tested astrology formulas. These follow the method of the
  [4DPrediction](https://github.com/zramakh/4DPrediction) repo. Summary in
  [FINDINGS.md](analysis/FINDINGS.md), full report in [REPORT.md](analysis/REPORT.md).

Python 3 with numpy. To get picks for a coming draw:

```sh
python3 analysis/astro_model.py predict --date 2026-10-21
```

No method here has beaten random picking on unseen draws; see the findings before using the picks.
