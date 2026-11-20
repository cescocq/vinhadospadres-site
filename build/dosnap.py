import json,math
from snap import G,ring,proj,runs,kx,ky
P=ring(G['parish'])[:]
orig=json.dumps(G['parish'])
h=open('s63/history.html').read(); assert h.count(orig)==1, 'fmt'
def pt(R,i,t): a,b=R[i],R[i+1]; return [round(a[0]+(b[0]-a[0])*t,6),round(a[1]+(b[1]-a[1])*t,6)]
jobs=[]
for k in ['park','doc']:
    R=ring(G[k])
    for a,b in runs(P,R,300):
        if b-a<1: continue
        jobs.append((a,b,k))
jobs.sort(reverse=True)
for a,b,k in jobs:
    R=ring(G[k]); m=len(R)-1  # closed ring, last==first
    _,ia,ta=proj(P[a],R); _,ib,tb=proj(P[b],R)
    sa=ia+ta; sb=ib+tb
    fwd=(sb-sa)%m; bwd=(sa-sb)%m
    seg=[pt(R,ia,ta)]
    if fwd<=bwd:
        i=ia+1
        while True:
            ii=i%m
            if (i-sa)%m>=fwd or ((ii==ib+1)%m==0 and False): pass
            if ((i - sa) % m) >= fwd: break
            seg.append(R[ii]); i+=1
    else:
        i=ia if ta>0 else ia-1
        while True:
            ii=i%m
            if ((sa - i) % m) >= bwd: break
            seg.append(R[ii]); i-=1
    seg.append(pt(R,ib,tb))
    print(k,a,b,'->',len(seg),'fwd' if fwd<=bwd else 'bwd')
    P[a:b+1]=seg
P[-1]=P[0]
G['parish']['coordinates'][0]=P
h=h.replace(orig,json.dumps(G['parish']))
open('s63/history.html','w').write(h)
