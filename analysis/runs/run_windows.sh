cd /home/user/mlive
export OMP_NUM_THREADS=1
for w in last_round last5 last10 decay10; do
  echo "=== $w start $(date -u)"
  python3 analysis/lead_full.py --until 2026-10-17 --window $w 2>&1 | grep -v "Warn\|tasks,"
  echo "=== $w end $(date -u)"
done
echo ALLDONE
