import json,math
kx=math.cos(math.radians(39.3))*111320; ky=110540
def proj(p,R):
    best=(1e18,0,0)
    for i in range(len(R)-1):
        a,b=R[i],R[i+1]; px,py=(p[0]-a[0])*kx,(p[1]-a[1])*ky; bx,by=(b[0]-a[0])*kx,(b[1]-a[1])*ky
        L=bx*bx+by*by; t=max(0,min(1,(px*bx+py*by)/L)) if L else 0
        d=math.hypot(px-t*bx,py-t*by)
        if d<best[0]: best=(d,i,t)
    return best
def rings(g):
    if g['type']=='Polygon': return [g['coordinates']]
    return g['coordinates']
