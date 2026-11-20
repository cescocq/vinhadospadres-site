import asyncio,sys
sys.path.insert(0,'/home/claude/vdp'); from tlib import route
from playwright.async_api import async_playwright
B='file:///home/claude/vdp/s63/'; O='/home/claude/vdp/shots/'
import os; os.makedirs(O,exist_ok=True)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-gl=swiftshader','--enable-unsafe-swiftshader']); logs=[]
        d=await b.new_page(viewport={'width':1440,'height':950}); d.on('pageerror',lambda e:logs.append(str(e))); await d.route('**/*',route)
        await d.goto(B+'index.html#vdp'); await d.wait_for_timeout(6000)
        await d.screenshot(path=O+'e_main.png')
        await d.click('#wopen'); await d.wait_for_timeout(500); await d.screenshot(path=O+'e_wines.png')
        await d.click('[data-yr="2022"]'); await d.wait_for_timeout(400); await d.screenshot(path=O+'e_wines2.png')
        await d.evaluate("openWineCard('w22')"); await d.wait_for_timeout(600); await d.screenshot(path=O+'e_card.png')
        await d.click('#wback'); await d.wait_for_timeout(300); await d.screenshot(path=O+'e_back.png')
        print(logs); await b.close()
asyncio.run(main())
