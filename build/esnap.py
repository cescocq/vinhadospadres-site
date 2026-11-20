import json,sys,math
sys.path.insert(0,'/home/claude/vdp'); from esnap_lib import *
F='/home/claude/vdp/s65/data/estate.js'
s=open(F).read(); pre=s[:s.find('{')]; D=json.loads(s[s.find('{'):s.rfind(';')])
V=D['vdp']
def pt(R,i,t): a,b=R[i],R[i+1]; return [round(a[0]+(b[0]-a[0])*t,7),round(a[1]+(b[1]-a[1])*t,7)]
def path_between(R,ia,ta,ib,tb):
    m=len(R)-1; sa=ia+ta; sb=ib+tb
    fwd=(sb-sa)%m; bwd=(sa-sb)%m
    seg=[pt(R,ia,ta)]
    if fwd<=bwd:
        k=ia+1
        while ((k-sa)%m)<fwd and ((k-sa)%m)>0: seg.append(R[k%m]); k+=1
    else:
        k=ia if ta>0 else ia-1
        while ((sa-k)%m)<bwd and ((sa-k)%m)>0: seg.append(R[k%m]); k-=1
    seg.append(pt(R,ib,tb)); return seg,min(fwd,bwd)
def snap_ring(P,T,thr):
    closed=P[0]==P[-1]; Q=P[:-1] if closed else P[:]
    n=len(Q); near=[proj(v,T)[0]<thr for v in Q]
    if all(near) or not any(near): 
        if all(near): return P,0
        return P,0
    # rotate so Q[0] is not near
    r=near.index(False); Q=Q[r:]+Q[:r]; near=near[r:]+near[:r]
    out=[];i=0;changed=0
    while i<n:
        if not near[i]: out.append(Q[i]); i+=1; continue
        j=i
        while j+1<n and near[j+1]: j+=1
        _,ia,ta=proj(Q[i],T); _,ib,tb=proj(Q[j],T)
        if i==j: out.append(pt(T,ia,ta))
        else:
            seg,span=path_between(T,ia,ta,ib,tb)
            # guard: target path should be about as long as the run (avoid wrapping the wrong way)
            def L(pp): return sum(math.hypot((pp[k+1][0]-pp[k][0])*kx,(pp[k+1][1]-pp[k][1])*ky) for k in range(len(pp)-1))
            if L(seg)>2.5*L(Q[i:j+1])+20: out.extend(pt(T,*proj(v,T)[1:]) for v in Q[i:j+1])
            else: out.extend(seg)
        changed+=j-i+1; i=j+1
    # dedupe consecutive duplicates
    o2=[out[0]]
    for v in out[1:]:
        if abs(v[0]-o2[-1][0])>1e-8 or abs(v[1]-o2[-1][1])>1e-8: o2.append(v)
    o2.append(o2[0]); return o2,changed
log=[]
props=V['properties']; done=[]
for p in props:
    R=p['geom']['coordinates'][0]
    for q in done:
        R,c=snap_ring(R,q['geom']['coordinates'][0],8.0)
        if c: log.append((p['id'],'->',q['id'],c))
    p['geom']['coordinates'][0]=R; done.append(p)
targets=[(p['id'],p['geom']['coordinates'][0]) for p in props]
for pc in V['parcels']:
    polys=rings(pc['geom'])
    for poly in polys:
        R=poly[0]
        for tid,T in targets:
            R,c=snap_ring(R,T,7.5)
            if c: log.append((pc['id'],'->',tid,c))
        poly[0]=R
    for poly in polys: targets.append((pc['id'],poly[0]))
for l in log: print(*l)
open(F,'w').write(pre+json.dumps(D,separators=(',',':'),ensure_ascii=False)+';\n')
