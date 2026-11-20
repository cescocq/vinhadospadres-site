import asyncio,sys
sys.path.insert(0,'/home/claude/vdp'); from tlib import route
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-gl=swiftshader','--enable-unsafe-swiftshader']); logs=[]
        for w,h,n in [(1440,950,'d'),(1280,800,'l'),(390,844,'p')]:
            d=await b.new_page(viewport={'width':w,'height':h}); d.on('pageerror',lambda e:logs.append(str(e))); await d.route('**/*',route)
            await d.goto('file:///home/claude/vdp/s63/index.html#climate=2022'); await d.wait_for_timeout(9000)
            await d.screenshot(path=f'shots/3d_{n}.png'); await d.close()
        print(logs); await b.close()
asyncio.run(main())
