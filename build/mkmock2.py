import sys; sys.path.insert(0,'/home/claude/vdp'); from icons import icon
S='/mnt/attach/outputs/37_site/'
h=open(S+'wines.html').read(); head=h[:h.find('</head>')]
FAM=[('fruit',['apricot','peach','dried fruit','yellow plum','plum','apple','baked apple','pear','tropical','citrus','red cherry','fruit-driven','dark fruit','forest fruit','red fruit','blueberry','elderberry','almond','walnut']),
('floral',['orange blossom','pollen']),
('herbal & wood',['wild herbs','dried herbs','savoury','mint','pennyroyal','hay','cedar','light oak']),
('spice & smoke',['white pepper','spice','aniseed','smoky']),
('earth & mineral',['earthy','clay','mineral','granite mineral','stony','chalk','chalky','chalky finish','saline']),
('structure & feel',['fresh','clean','dry','bone-dry','fine tannins','refined tannins','grainy','textured','long finish','elegant','ethereal','light','balanced','crunchy'])]
n=sum(len(t) for _,t in FAM); print(n)
def block(c): return ''.join(f'<h3>{f}</h3><div class="grid">'+''.join(f'<figure class="ti">{icon(t,c)}<figcaption>{t}</figcaption></figure>' for t in ts)+'</div>' for f,ts in FAM)
css='''<style>body{background:#E6DED0}.pg{max-width:1240px;margin:0 auto;padding:40px 40px 80px;font-family:var(--serif);color:#231F20}
h1{font-size:40px;margin:0 0 6px}h2{font-size:28px;margin:44px 0 0;padding-top:12px;border-top:3px solid var(--ac)}h3{font-size:19px;margin:22px 0 10px;color:#6b625b}p.k{color:#6b625b;margin:0 0 10px}
.grid{display:flex;flex-wrap:wrap;gap:18px 10px}.ti{margin:0;width:92px;text-align:center}.ti svg{width:58px;height:58px;display:block;margin:0 auto}.ti figcaption{font-size:13px;line-height:1.15;margin-top:6px}</style>'''
body=f'<body><div class="pg"><h1>aroma symbols · every term unique</h1><p class="k">{n} terms, {n} different symbols. Same circle, same maximum silhouette size, centred.</p><h2 style="--ac:#275FAC">whites · tile blue</h2>{block("#275FAC")}<h2 style="--ac:#C76653">reds · terracotta</h2>{block("#C76653")}</div></body></html>'
open('/home/claude/vdp/symbols_unique.html','w').write(head+css+'</head>'+body)
