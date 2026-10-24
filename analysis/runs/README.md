# Batch runners

Shell scripts used to run the long jobs in this session (resumable: each skips work whose output exists). Run from the
repo root, e.g. `LOGDIR=/tmp bash analysis/runs/run_ff.sh`.

- `run_windows.sh`, `after_windows.sh` - lead_full.py for every history window, then the comparison reports
- `run_d9.sh`, `run_d9b.sh` - the D9 family through every window
- `run_vargas.sh` - the divisional charts D2-D60
- `run_cdiv.sh` - Da Liu Ren, Mei Hua Yi Shu, Tai Yi Shen Shu families
- `run_ff.sh` - family_fair.py for muhurta, transit, continuous and triples

Prediction and live scoring: `watch_predict.py DATE` (numbers for a coming draw), `consensus.py`, `watch_score.py DATES`
(score the watchlist and short list after a draw), `lead_today.py DATE`.
