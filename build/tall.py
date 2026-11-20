import asyncio,sys
sys.path.insert(0,'/home/claude/vdp'); from tlib import route
from playwright.async_api import async_playwright
B='file:///home/claude/vdp/s63/'; O='/home/claude/vdp/shots/'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-gl=swiftshader','--enable-unsafe-swiftshader']); logs=[]
        d=await b.new_page(viewport={'width':1440,'height':950}); d.on('pageerror',lambda e:logs.append(('d',str(e)))); await d.route('**/*',route)
        await d.goto(B+'index.html'); await d.wait_for_timeout(6000); await d.screenshot(path=O+'w_est.png')
        await d.click('#wlgo'); await d.wait_for_timeout(300); await d.screenshot(path=O+'w_est2.png')
        await d.click('button[data-lang="pt"]'); await d.wait_for_timeout(400); await d.locator('#proofTag').screenshot(path=O+'w_pt.png')
        for f in ['wine-white-2022','wines','code','history','recognition','contact','compare']:
            await d.goto(B+f+'.html'); await d.wait_for_timeout(1200)
            await d.evaluate("window.scrollTo(0,document.body.scrollHeight)"); await d.wait_for_timeout(600); await d.screenshot(path=O+f'w_{f}.png')
        await d.goto(B+'wine-white-2022.html'); await d.wait_for_timeout(800); await d.locator('.two').screenshot(path=O+'w_aromas.png')
        m=await (await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)).new_page(); m.on('pageerror',lambda e:logs.append(('m',str(e)))); await m.route('**/*',route)
        await m.goto(B+'index.html'); await m.wait_for_timeout(6000); await m.screenshot(path=O+'w_est_p.png')
        await m.goto(B+'wine-red-2022.html'); await m.wait_for_timeout(800); await m.evaluate("window.scrollTo(0,document.body.scrollHeight)"); await m.wait_for_timeout(400); await m.screenshot(path=O+'w_wine_p.png')
        print(logs); await b.close()
asyncio.run(main())
