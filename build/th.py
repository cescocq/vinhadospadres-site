import asyncio,sys
sys.path.insert(0,'/home/claude/vdp'); from tlib import route
from playwright.async_api import async_playwright
f=sys.argv[1]; out=sys.argv[2]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); logs=[]
        d=await b.new_page(viewport={'width':1440,'height':950}); d.on('pageerror',lambda e:logs.append(str(e))); await d.route('**/*',route)
        await d.goto('file://'+f); await d.wait_for_timeout(1500)
        await d.evaluate("document.getElementById('c1795').scrollIntoView({block:'center'})"); await d.wait_for_timeout(5000)
        await d.screenshot(path=out); print(logs); await b.close()
asyncio.run(main())
