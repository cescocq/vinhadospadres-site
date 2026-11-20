import json,sys,math
sys.path.insert(0,'/home/claude/vdp'); from esnap_lib import *
SRC='/home/claude/vdp/estate_v64.js'; F='/home/claude/vdp/s65/data/estate.js'
s=open(SRC).read(); pre=s[:s.find('{')]; D=json.loads(s[s.find('{'):s.rfind(';')])
V=D['vdp']
def P(v): return ((v[0])*kx,(v[1])*ky)
def area(R): return sum(P(R[i])[0]*P(R[i+1])[1]-P(R[i+1])[0]*P(R[i])[1] for i in range(len(R)-1))/2
def dist(a,b): return math.hypot((a[0]-b[0])*kx,(a[1]-b[1])*ky)
def snap(A,B,thr):
    A=[list(v) for v in A[:-1]]
    # 1. insert B vertices that lie near A edges, ordered along each edge
    RA=A+[A[0]]; ins={}
    for v in B[:-1]:
        d,i,t=proj(v,RA)
        if d<thr and min(dist(v,RA[i]),dist(v,RA[i+1]))>0.3: ins.setdefault(i,[]).append((t,list(v)))
    NA=[]
    for i,v in enumerate(A):
        NA.append(v)
        for t,w in sorted(ins.get(i,[])): NA.append(w)
    A=NA
    # 2. move A vertices onto B
    RB=B; n=0
    for k,v in enumerate(A):
        d,i,t=proj(v,RB)
        if d<thr and d>0.01:
            a,b=RB[i],RB[i+1]; A[k]=[a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t]; n+=1
    # 3. dedupe
    out=[]
    for v in A:
        if not out or dist(v,out[-1])>0.05: out.append(v)
    if dist(out[0],out[-1])<0.05: out.pop()
    out=[[round(x,8),round(y,8)] for x,y in out]
    return out+[out[0]],n
def segs_cross(R):
    c=0;m=len(R)-1
    def ccw(a,b,c): return (c[1]-a[1])*(b[0]-a[0])-(b[1]-a[1])*(c[0]-a[0])
    for i in range(m):
        for j in range(i+2,m):
            if i==0 and j==m-1: continue
            a,b,c2,d=R[i],R[i+1],R[j],R[j+1]
            if (ccw(a,b,c2)*ccw(a,b,d)<0) and (ccw(c2,d,a)*ccw(c2,d,b)<0): c+=1
    return c
THR=float(sys.argv[1]) if len(sys.argv)>1 else 8
props=V['properties']; tg=[]
for p in props:
    R=p['geom']['coordinates'][0]; a0=area(R)
    for q in tg:
        R2,n=snap(R,q,THR)
        if segs_cross(R2)<=segs_cross(R): R=R2
        else: print('     skipP',n)
    p['geom']['coordinates'][0]=R; tg.append(R)
    print('P',p['id'],round(a0),round(area(R)),'x',segs_cross(R))
for pc in V['parcels']:
    polys=rings(pc['geom'])
    for poly in polys:
        R=poly[0]; a0=area(R)
        for q in tg:
            R2,n=snap(R,q,THR*0.6)
            if segs_cross(R2)<=segs_cross(R): R=R2
            else: print('     skip',n)
        poly[0]=R
        print('  ',pc['id'],round(a0),round(area(R)),'x',segs_cross(R))
    for poly in polys: tg.append(poly[0])
open(F,'w').write(pre+json.dumps(D,separators=(',',':'),ensure_ascii=False)+';\n')
