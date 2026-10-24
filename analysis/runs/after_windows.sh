S=${LOGDIR:-/tmp}
until grep -q ALLDONE $S/windows.log; do sleep 60; done
cd /home/user/mlive; export OMP_NUM_THREADS=1
for w in last_round last5 last10 decay10; do
  echo "=== today $w $(date -u)"; python3 analysis/lead_today.py 2026-10-18 --window $w 2>&1 | grep -v Warn | tail -2
  python3 analysis/winners_history.py 2026-10-18 --window $w > /dev/null 2>&1 && echo "winners $w ok"
  python3 analysis/repeat_hits.py 2026-10-18 --window $w > /dev/null 2>&1 && echo "repeat $w ok"
done
python3 analysis/windows_compare.py 2026-10-18 > /dev/null 2>&1 && echo "compare ok"
echo FOLLOWUPDONE
