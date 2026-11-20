import json,math,sys
G=json.load(open('G.json'))
kx=math.cos(math.radians(39.3))*111320; ky=110540
def ring(g): return g['coordinates'][0]
def proj(p,R):
    best=(1e18,0,0)
    for i in range(len(R)-1):
        a,b=R[i],R[i+1]; px,py=(p[0]-a[0])*kx,(p[1]-a[1])*ky; bx,by=(b[0]-a[0])*kx,(b[1]-a[1])*ky
        L=bx*bx+by*by; t=max(0,min(1,(px*bx+py*by)/L)) if L else 0
        d=math.hypot(px-t*bx,py-t*by)
        if d<best[0]: best=(d,i,t)
    return best
def runs(P,R,T):
    near=[proj(p,R)[0]<T for p in P]; n=len(P)
    out=[];i=0
    while i<n:
        if near[i]:
            j=i
            while j+1<n and near[j+1]: j+=1
            out.append((i,j)); i=j+1
        else: i+=1
    return out
if __name__=='__main__':
    P=ring(G['parish'])
    for k in ['park','doc']:
        R=ring(G[k])
        for T in (150,300,500):
            print(k,T,[(a,b) for a,b in runs(P,R,T) if b-a>=1])
