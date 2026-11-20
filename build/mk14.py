import sys; sys.path.insert(0,'/home/claude/vdp'); from icons import icon
S='/mnt/attach/outputs/37_site/'
h=open(S+'wines.html').read(); head=h[:h.find('</head>')]
L=['walnut','crunchy','elderberry','dried herbs','apricot','peach','apple','plum','yellow plum','mint','pear','tropical','dried fruit','citrus','red cherry','dark fruit','forest fruit','red fruit','fruit-driven','blueberry','almond','mineral','granite mineral','long finish']
g=lambda c:''.join(f'<figure class="ti">{icon(t,c)}<figcaption>{t}</figcaption></figure>' for t in L)
css='''<style>body{background:#E6DED0}.pg{max-width:1240px;margin:0 auto;padding:40px;font-family:var(--serif);color:#231F20}h1{font-size:36px;margin:0 0 4px}h2{font-size:24px;margin:30px 0 12px}
.grid{display:flex;flex-wrap:wrap;gap:18px 10px}.ti{margin:0;width:100px;text-align:center}.ti svg{width:64px;height:64px;display:block;margin:0 auto}.ti figcaption{font-size:13px;margin-top:6px}</style>'''
open('/home/claude/vdp/v14.html','w').write(head+css+f'</head><body><div class="pg"><h1>redrawn symbols</h1><h2>whites</h2><div class="grid">{g("#275FAC")}</div><h2>reds</h2><div class="grid">{g("#C76653")}</div></div></body></html>')
