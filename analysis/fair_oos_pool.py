#!/usr/bin/env python3
"""For fair_oos.py: every pool lead's blind z (its hits in the years its earlier record put it in the top 1%), real vs 2 shifted calendars."""
import sys, os, math, json
sys.argv=['x','--shifts','2']; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import fair_oos as f
from multiprocessing import Pool
res={}
for key in f.LABEL:
    f.setup(key); W=f.ls.W; k,n=W["k"],W["n"]; e,v=k*k/n, k*(k/n)*(1-k/n)*(n-k)/(n-1)
    ys,years,lo=f.G["ys"],f.G["years"],f.G["lo"]; ny=np.array([(years[lo:]==y).sum() for y in ys],float)
    tasks=[(sh,i,min(i+200,len(f.SETS))) for sh in range(3) for i in range(0,len(f.SETS),200)]
    Y=np.zeros((3,len(f.SETS),len(f.PATS),len(ys)),np.float32)
    with Pool(4) as pool:
        for sh,i0,o in pool.imap_unordered(f.chunk,tasks): Y[sh,i0:i0+len(o)]=o
    tt=list(range(2,len(ys))); out=[]
    for sh in range(3):
        F=Y[sh].reshape(-1,len(ys)); Z=f.zcum(F,ny,e,v)
        ch=np.zeros_like(F,bool)
        for t in tt: ch[:,t]=Z[:,t]>=np.quantile(Z[:,t],0.99)
        hh=(F*ch).sum(1); nn=(ch*ny).sum(1); m=nn>0
        bz=(hh[m]-nn[m]*e)/np.sqrt(nn[m]*v)
        ny_=ch.sum(1)[m]
        out.append(dict(leads=int(m.sum()), z3=int((bz>=3).sum()), z35=int((bz>=3.5).sum()), z2=int((bz>=2).sum()), max=float(bz.max()),
            multi=int((ny_>=3).sum()), multi_z3=int(((ny_>=3)&(bz>=3)).sum()), multi_z2=int(((ny_>=3)&(bz>=2)).sum())))
    res[key]=out; print(key,out,flush=True)
json.dump(res,open(''+os.path.join(f.A,'fair_oos_pool.json')+'','w'))
