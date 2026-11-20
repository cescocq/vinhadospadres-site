import json,sys,math
from shapely.geometry import Polygon,MultiPolygon,mapping,shape
from shapely.ops import snap,unary_union
from shapely.geometry.polygon import orient
SRC='/home/claude/vdp/estate_v64.js'; F='/home/claude/vdp/s65/data/estate.js'
s=open(SRC).read(); pre=s[:s.find('{')]; D=json.loads(s[s.find('{'):s.rfind(';')])
V=D['vdp']; lon0,lat0=-7.5,39.3
kx=math.cos(math.radians(lat0))*111320; ky=110540
def tom(g):
    def r(R): return [((x-lon0)*kx,(y-lat0)*ky) for x,y in R]
    if g['type']=='Polygon': return Polygon(r(g['coordinates'][0]),[r(h) for h in g['coordinates'][1:]])
    return MultiPolygon([Polygon(r(p[0]),[r(h) for h in p[1:]]) for p in g['coordinates']])
def tog(G,typ):
    def r(R): return [[round(x/kx+lon0,8),round(y/ky+lat0,8)] for x,y in R.coords]
    polys=[orient(p,-1) for p in (G.geoms if hasattr(G,'geoms') else [G]) if p.area>(2 if typ=='MultiPolygon' else 25)]
    polys.sort(key=lambda p:-p.area)
    if typ=='Polygon' or len(polys)==1:
        p=polys[0]; return {'type':'Polygon','coordinates':[r(p.exterior)]+[r(h) for h in p.interiors]}
    return {'type':'MultiPolygon','coordinates':[[r(p.exterior)]+[r(h) for h in p.interiors] for p in polys]}
TOL=float(sys.argv[1]) if len(sys.argv)>1 else 7
PT=float(sys.argv[2]) if len(sys.argv)>2 else 4
def clean(G): 
    G=G.buffer(0)
    return G
prev=[]; PM={}
for p in V['properties']:
    G=tom(p['geom']); a0=G.area
    if prev:
        U=unary_union(prev)
        G=clean(snap(G,U,TOL)); G=clean(G.difference(U))
        # close slivers: union then erode/dilate tiny
    prev.append(G); PM[p['id']]=G
    p['geom']=tog(G,'Polygon'); print('P',p['id'],round(a0),round(G.area))
prevP=[]
for pc in V['parcels']:
    G=tom(pc['geom']); a0=G.area; own=PM[pc['prop']]
    inside=G.intersection(own).area/G.area
    tg=unary_union([b.boundary for b in PM.values()])
    G2=clean(snap(G,tg,PT))
    if abs(G2.area-a0)/a0<0.08: G=G2
    else: print('    skip snap',round(G2.area))
    if inside>0.97: G=clean(G.intersection(own))
    for q in prevP:
        if G.intersection(q).area>1: G=clean(G.difference(q))
    prevP.append(G)
    pc['geom']=tog(G,pc['geom']['type']); print('  ',pc['id'],round(a0),round(G.area),'inside',round(inside,3),G.geom_type)
open(F,'w').write(pre+json.dumps(D,separators=(',',':'),ensure_ascii=False)+';\n')
F2=F; s=open(F2).read(); D=json.loads(s[s.find('{'):s.rfind(';')])
M={'Castelao':'Castelão','Fernao Pires':'Fernão Pires'}
for r in D['vdp']['records']: r['variety']=M.get(r['variety'],r['variety'])
open(F2,'w').write(pre+json.dumps(D,separators=(',',':'),ensure_ascii=False)+';\n')
