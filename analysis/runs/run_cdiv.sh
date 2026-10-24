cd /home/user/mlive; export OMP_NUM_THREADS=1
for f in dlr mh ty; do
  echo "=== $f start $(date -u)"
  [ -f analysis/leads7_${f}_results.json ] && [ -f analysis/profit_arrays/leads7_${f}_toto58.npz ] || python3 analysis/lead_full.py --until 2026-10-17 --family $f > /dev/null 2>$f.err || echo "FAILED full $f"
  for d in 2026-10-18 2026-10-21; do
    [ -f analysis/leads7_${f}_today_$d.json ] || python3 analysis/lead_today.py $d --family $f > /dev/null 2>>$f.err || echo "FAILED today $f $d"
    python3 analysis/winners_history.py $d --family $f > /dev/null 2>>$f.err || echo "FAILED winners $f $d"
    python3 analysis/repeat_hits.py $d --family $f > /dev/null 2>>$f.err || echo "FAILED repeat $f $d"
  done
  echo "=== $f end $(date -u)"
  git add -A analysis data > /dev/null 2>&1; git commit -qm "Chinese divination family $f: results" > /dev/null 2>&1; git push -q origin claude/focused-franklin-ajsdm9 > /dev/null 2>&1
done
echo CDIVDONE
