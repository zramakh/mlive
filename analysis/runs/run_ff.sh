cd /home/user/mlive; export OMP_NUM_THREADS=1
for f in muhurta transit continuous; do
  [ -f analysis/FAMILY_FAIR_${f^^}.md ] || python3 analysis/family_fair.py $f --shifts 5 > /dev/null 2>>ff_$f.err || echo "FAILED $f"
  echo "=== $f done $(date -u)"
done
[ -f analysis/FAMILY_FAIR_TRIPLES.md ] || python3 analysis/family_fair.py triples --shifts 2 > /dev/null 2>>ff_triples.err || echo "FAILED triples"
echo "=== triples done $(date -u)"
echo FFDONE
