#!/usr/bin/env python3
"""Star Toto lunar-date rule (±7 days, hot) as 10 sets: whole-history return and 5-number draws, real date vs 59 other dates (6-day steps)."""
import sys; sys.argv=['x']; import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np, datetime as dt, csv, common, ephemeris as eph, toto_profit as tp, lead_search10 as ls
from multiprocessing import Pool
g=common.load_game("toto50"); k,n=6,50
H=g["hit"][:,1:].astype(float); D=g["dates"]; days=[dt.date.fromisoformat(x) for x in D]; years=np.array([x.year for x in days])
pos=np.array([(eph.lunar_date(x)[0]-1)*30+eph.lunar_date(x)[1]-1 for x in days],float)
rows=list(csv.DictReader(open(common.DATA+"/star_toto_6_50.csv"))); bon=np.array([int(r["bonus"]) for r in rows])
T=tp.pay_table("toto50"); tie=np.random.default_rng(1).random((len(D),n))*1e-6; pats=ls.swap_patterns(6)
def run(off):
    pay=0; nd=0; hi=[]; hits=0
    for t in range(len(D)):
        c=(pos+off-pos[t]+180)%360-180; m=(np.abs(c)<=7)&(years<years[t])
        if m.sum()<3: continue
        rk=np.argsort(-(H[m].sum(0)+tie[t])); win=set(np.flatnonzero(H[t]).tolist()); nd+=1
        hits+=len(win&set(rk[:6].tolist()))
        best=0
        for p in pats:
            s=set(int(rk[q]) for q in p); mm=len(s&win); b=int(bon[t]-1 in s); pay+=T[mm,b]; best=max(best,mm)
        if best>=5: hi.append(D[t])
    return off, pay/(10*nd), hi, hits/(nd*0.72)
if __name__=="__main__":
    with Pool(4) as p: R=list(p.map(run, range(0,360,6)))
    r0=R[0]; print("real: return",round(r0[1],3),"5-hit draws",r0[2],"top-6 ratio",round(r0[3],3))
    others=[r[1] for r in R[1:]]; print("other dates: median return",round(np.median(others),3),"share >= real",np.mean(np.array(others)>=r0[1]), "max",round(max(others),3))
    print("5-hit draws at other dates: mean",np.mean([len(r[2]) for r in R[1:]]), "max", max(len(r[2]) for r in R[1:]))
