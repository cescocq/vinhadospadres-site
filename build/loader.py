import re
S='/home/claude/vdp/s64/'
svg=open('/home/claude/vdp/Loader.svg').read()
svg=svg[svg.find('<svg'):]
svg=re.sub(r'<defs>.*?</defs>','',svg,flags=re.S).replace('class="cls-1"','').replace('<svg id="Layer_1" data-name="Layer 1"','<svg aria-hidden="true"')
# animate each tile with a delay based on its x position
def anim(m):
    x=float(re.search(r'(?:M|x=")([\d.]+)',m.group(0)).group(1)); d=x/323.81*1.2
    tag=m.group(0)
    return tag.replace('<path ',f'<path style="animation-delay:{d:.2f}s" ').replace('<rect ',f'<rect style="animation-delay:{d:.2f}s" ')
svg=re.sub(r'<(path|rect)[^>]*/>',anim,svg)
CSS='''<style id="ldcss">#vdpLoad{position:fixed;inset:0;z-index:999;display:grid;place-items:center;background:#E6DED0;transition:opacity .5s}
#vdpLoad.out{opacity:0;pointer-events:none}#vdpLoad svg{width:min(260px,60vw);height:auto;fill:#C56552}
#vdpLoad path,#vdpLoad rect{animation:ldp 1.4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes ldp{0%,100%{opacity:.25;transform:scaleY(.7)}50%{opacity:1;transform:scaleY(1)}}
@media (prefers-reduced-motion:reduce){#vdpLoad path,#vdpLoad rect{animation:none}}</style>'''
HTML=f'<div id="vdpLoad" role="status" aria-label="Loading">{svg}</div>'
JS='''<script id="ldjs">(function(){const L=document.getElementById('vdpLoad');function done(){requestAnimationFrame(()=>requestAnimationFrame(()=>{L.classList.add('out');setTimeout(()=>L.remove(),600);}));}
if(document.readyState==='complete')done();else addEventListener('load',done);setTimeout(done,8000);})();</script>'''
for f in ['index.html','history.html']:
    h=open(S+f).read()
    if 'id="vdpLoad"' in h: continue
    h=h.replace('</head>',CSS+'</head>',1)
    h=re.sub(r'(<body[^>]*>)',r'\1'+HTML,h,1)
    i=h.rfind('</body>'); h=h[:i]+JS+h[i:]
    open(S+f,'w').write(h); print('loader',f)
