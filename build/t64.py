import asyncio,sys
sys.path.insert(0,'/home/claude/vdp'); from tlib import route
from playwright.async_api import async_playwright
B='http://localhost:8765/'; O='/home/claude/vdp/shots/'
pages=sys.argv[1].split(',')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-gl=swiftshader','--enable-unsafe-swiftshader']); logs=[]
        d=await b.new_page(viewport={'width':1440,'height':950}); d.on('pageerror',lambda e:logs.append(str(e))); d.on('requestfailed',lambda r:logs.append('FAIL '+r.url[:90]) if 'localhost' in r.url else None); await d.route('**/*',route)
        for f in pages:
            await d.goto(B+f); await d.wait_for_timeout(5000); await d.screenshot(path=O+'s64_'+f.replace('.html','').replace('#','_')+'.png')
            fam=await d.evaluate("document.fonts.check('italic 20px \"Arno Pro\"')"); print(f,'font',fam)
        print(logs); await b.close()
asyncio.run(main())
