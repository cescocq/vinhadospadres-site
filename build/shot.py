# usage: python3 shot.py page[#..] out.png [js-before-shot] [wait] [w] [h] [full]
import asyncio,sys
sys.path.insert(0,'/home/claude/vdp'); from tlib import route
from playwright.async_api import async_playwright
B='http://localhost:8766/'
async def m(jobs):
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-gl=swiftshader','--enable-unsafe-swiftshader']); logs=[]
        ctxs={}
        for j in jobs:
            page,out=j[0],j[1]; js=j[2] if len(j)>2 else ''; wait=int(j[3]) if len(j)>3 else 2500; w=int(j[4]) if len(j)>4 else 1440; hh=int(j[5]) if len(j)>5 else 950; full=len(j)>6 and j[6]=='full'
            k=(w,hh)
            if k not in ctxs:
                c=await b.new_context(viewport={'width':w,'height':hh},device_scale_factor=2 if w<500 else 1,is_mobile=w<500,has_touch=w<500)
                await c.add_init_script("try{localStorage.setItem('vdpAge','1');localStorage.setItem('vdpWelcome','1')}catch(e){}")
                ctxs[k]=c
            d=await ctxs[k].new_page(); d.on('pageerror',lambda e:logs.append((page,str(e)))); await d.route('**/*',route)
            await d.goto(B+page); await d.wait_for_timeout(wait)
            if js:
                for part in js.split('||'):
                    if part.startswith('wait:'): await d.wait_for_timeout(int(part[5:])); continue
                    await d.evaluate(part); await d.wait_for_timeout(700)
            await d.screenshot(path=out,full_page=full); await d.close()
        print('errors:',logs); await b.close()
import json
jobs=json.loads(sys.argv[1])
asyncio.run(m(jobs))
