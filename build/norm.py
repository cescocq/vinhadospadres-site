import json,asyncio,sys
sys.path.insert(0,'/home/claude/vdp'); from glyphs import G
from playwright.async_api import async_playwright
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(); d=await b.new_page()
        html='<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="-20 -20 140 140" style="color:#000">'+''.join(f'<g id="g_{k}" fill="currentColor">{v}</g>' for k,v in G.items())+'</svg>'
        await d.set_content(html)
        bb=await d.evaluate("Object.fromEntries([...document.querySelectorAll('g')].map(g=>{const b=g.getBBox();return [g.id.slice(2),[b.x,b.y,b.width,b.height]]}))")
        await b.close(); return bb
bb=asyncio.run(m())
T={}
for k,(x,y,w,h) in bb.items():
    pad=2.5; x-=pad;y-=pad;w+=2*pad;h+=2*pad   # allow for stroke widths
    s=21/max(w,h); T[k]=f'translate({20-s*(x+w/2):.3f} {20-s*(y+h/2):.3f}) scale({s:.4f})'
json.dump(T,open('norm.json','w'),indent=0); print(len(T))
