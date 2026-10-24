cd /home/user/mlive; export OMP_NUM_THREADS=1
for w in all last_round last5 last10 decay10; do
  echo "=== $w start $(date -u)"
  python3 analysis/lead_full.py --until 2026-10-17 --window $w --family d9 > /dev/null 2>&1 || echo "FAILED full $w"
  python3 analysis/lead_today.py 2026-10-18 --window $w --family d9 > /dev/null 2>&1 || echo "FAILED today $w"
  python3 analysis/winners_history.py 2026-10-18 --window $w --family d9 > /dev/null 2>&1 || echo "FAILED winners $w"
  python3 analysis/repeat_hits.py 2026-10-18 --window $w --family d9 > /dev/null 2>&1 || echo "FAILED repeat $w"
  echo "=== $w end $(date -u)"
done
python3 analysis/windows_compare.py 2026-10-18 --family d9 > /dev/null 2>&1 || echo "FAILED compare"
python3 analysis/d9_report.py > /dev/null 2>&1 || echo "FAILED report"
echo D9DONE
