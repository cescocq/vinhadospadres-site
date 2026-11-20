import asyncio,sys,os
sys.path.insert(0,'/home/claude/vdp'); from tlib import route
from playwright.async_api import async_playwright
B='http://localhost:8765/'; O='/home/claude/vdp/shots/v64/'; os.makedirs(O,exist_ok=True)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-gl=swiftshader','--enable-unsafe-swiftshader']); logs=[]
        ctx=await b.new_context(viewport={'width':1440,'height':950})
        d=await ctx.new_page(); d.on('pageerror',lambda e:logs.append((d.url[-30:],str(e)))); await d.route('**/*',route)
        await d.goto(B+'index.html'); await d.wait_for_timeout(5000); await d.screenshot(path=O+'gate.png')
        await d.click('#agY'); await d.wait_for_timeout(300)
        await d.click('button[data-lang="pt"]'); await d.wait_for_timeout(600); await d.screenshot(path=O+'index_pt_toggle.png')
        await d.click('#sitenav a[href="history.html"]'); await d.wait_for_timeout(5000); print('after nav click:',d.url)
        await d.screenshot(path=O+'history_pt.png')
        for f in ['code-pt','wines-pt','wine-red-2022-pt','compare-pt','recognition-pt','contact-pt','privacy','privacy-pt','404','index-pt']:
            await d.goto(B+f+'.html'); await d.wait_for_timeout(2500 if 'index' not in f else 6000); await d.screenshot(path=O+f+'.png',full_page=('index' not in f))
        # EN button on PT page goes to EN
        await d.goto(B+'wines-pt.html'); await d.wait_for_timeout(800)
        await d.locator('.seg button',has_text='EN').first.click(); await d.wait_for_timeout(1200); print('EN switch ->',d.url)
        m=await (await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)).new_page(); m.on('pageerror',lambda e:logs.append(('m',str(e)))); await m.route('**/*',route)
        await m.goto(B+'wine-white-2022-pt.html'); await m.wait_for_timeout(1500); await m.screenshot(path=O+'gate_p.png')
        await m.tap('#agY'); await m.wait_for_timeout(300); await m.screenshot(path=O+'wine_pt_p.png',full_page=True)
        print(logs); await b.close()
asyncio.run(main())
