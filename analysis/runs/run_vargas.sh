cd /home/user/mlive; export OMP_NUM_THREADS=1
for D in 2 3 4 7 10 12 16 20 24 27 30 40 45 60; do
  f=d$D
  if [ ! -f analysis/leads7_${f}_today_2026-10-18.json ]; then
    echo "=== $f start $(date -u)"
    [ -f analysis/leads7_${f}_results.json ] && [ -f analysis/profit_arrays/leads7_${f}_toto58.npz ] || python3 analysis/lead_full.py --until 2026-10-17 --family $f > /dev/null 2>&1 || echo "FAILED full $f"
    python3 analysis/lead_today.py 2026-10-18 --family $f > /dev/null 2>&1 || echo "FAILED today $f"
    python3 analysis/winners_history.py 2026-10-18 --family $f > /dev/null 2>&1 || echo "FAILED winners $f"
    python3 analysis/repeat_hits.py 2026-10-18 --family $f > /dev/null 2>&1 || echo "FAILED repeat $f"
    echo "=== $f end $(date -u)"
    git add -A analysis > /dev/null 2>&1; git commit -qm "Divisional chart $f: results" > /dev/null 2>&1; git push -q origin claude/focused-franklin-ajsdm9 > /dev/null 2>&1
  fi
done
python3 analysis/vargas_report.py > /dev/null 2>&1 || echo "FAILED report"
echo VARGASDONE
