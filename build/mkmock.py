import re,sys
sys.path.insert(0,'/home/claude/vdp'); from icons import icon; from glyphs import TERM
S='/mnt/attach/outputs/37_site/'
h=open(S+'wines.html').read(); head=h[:h.find('</head>')]
def terms(f):
    t=open(S+f).read(); out={}
    for m in re.finditer(r'<section class="sense"><h2>(nose|mouth)</h2>(.*?)</section>',t,re.S):
        out[m.group(1)]=re.findall(r'<figcaption>([^<]*)</figcaption>',m.group(2))
    return out
w22=terms('qdvdp-3m12m-2022-white.html'); r22=terms('qdvdp-3m12m-2022-red.html')
seen={}
for t,k in TERM.items(): seen.setdefault(k,[]).append(t)
sheet=lambda c:''.join(f'<figure class="ti">{icon(v[0],c)}<figcaption>{" / ".join(v)}</figcaption></figure>' for k,v in seen.items())
def sec(d,col,name):
    return f'<div class="wn" style="--ac:{col}"><h3>{name}</h3><div class="two">'+''.join(f'<section><h4>{s}</h4><div class="grid">'+''.join(f'<figure class="ti">{icon(t,col)}<figcaption>{t}</figcaption></figure>' for t in d[s])+'</div></section>' for s in ('nose','mouth'))+'</div></div>'
css='''<style>body{background:#E6DED0}.pg{max-width:1200px;margin:0 auto;padding:40px 40px 80px;font-family:var(--serif);color:#231F20}
h1{font-size:40px;margin:0 0 6px}h2{font-size:26px;margin:40px 0 4px}p.k{color:#6b625b;margin:0 0 16px}
.grid{display:flex;flex-wrap:wrap;gap:18px 12px}.ti{margin:0;width:96px;text-align:center}.ti svg{width:60px;height:60px;display:block;margin:0 auto}.ti figcaption{font-size:13px;line-height:1.15;margin-top:6px}
.wn{border-top:3px solid var(--ac);padding-top:12px;margin-top:26px}.wn h3{font-size:24px;margin:0 0 10px}.two{display:grid;grid-template-columns:1fr 1fr;gap:34px}.two h4{font-size:20px;margin:0 0 10px}</style>'''
body=f'''<body><div class="pg"><h1>aroma symbols · silhouettes</h1><p class="k">One colour per wine (tile blue for whites, terracotta for reds). Same circle for every symbol; every silhouette scaled to the same maximum size and centred.</p>
<h2>as they would appear on the wine pages</h2>{sec(w22,"#275FAC","Quinta da Vinha dos Padres 2022 white 3M12M")}{sec(r22,"#C76653","Quinta da Vinha dos Padres 2022 red 3M12M")}
<h2>full set · whites</h2><div class="grid">{sheet("#275FAC")}</div><h2>full set · reds</h2><div class="grid">{sheet("#C76653")}</div></div></body></html>'''
open('/home/claude/vdp/symbols_mock.html','w').write(head+css+'</head>'+body)
