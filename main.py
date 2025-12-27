# https://www.redfin.com/zipcode/30310
# https://www.redfin.com/zipcode/30311
# https://www.redfin.com/zipcode/30314

#import playwright
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import asyncio
from playwright.async_api import Page
from collections.abc import Coroutine, Awaitable
from playwright.async_api import Locator
from playwright.async_api import BrowserContext

#import other stuff
import random
import time
import re
from colorama import Fore, Style, init
init(autoreset=True)

#Make a function to scroll to the bottom
async def auto_scroll(page: Page):
    print(Fore.RED + "->" + Fore.BLUE + "Scrolling to the bottom of page...")
    #Get the height of the page PRESENTLY
    page_height = await page.evaluate("document.body.scrollHeight")

    #run a while true loop to scroll to the very end
    while True:
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        #wait for the stuff to load
        await asyncio.sleep(random.uniform(2, 3))

        new_height = await page.evaluate("document.body.scrollHeight")
        if new_height == page_height: #this means that new stuff didn't load
            await asyncio.sleep(2)
            if new_height == await page.evaluate("document.body.scrollHeight"):
                break
        page_height = new_height

#make a function to create delayed_starts to functions
async def delayed_start(delay: float,
                        func: Coroutine):
    await asyncio.sleep(delay)
    return await func


#make a function to go to urls
async def reach_url(page: Page,
                    url: str):
    #go to the url
    await page.goto(url=url, wait_until="domcontentloaded")
    await page.wait_for_selector('div#results-display', timeout=0)
    print(Fore.RED + "->" + Fore.GREEN + f"Reached {url}")

#make a function to click stuff
async def elem_clicker(page: Page,
                       elem: Locator,
                       button = "left"):
    #first hover over the element
    await elem.hover()
    await asyncio.sleep(random.uniform(0.75, 1.5))

    #click the element
    if button == "middle":
        await elem.click(button="middle")
    else:
        await elem.click()

async def propertry_handler(page: Page,
                            elem_list: list):
    TABS = []
    print(Fore.BLUE + f"Found {len(elem_list)} elements to click.")
    #loop through the elem list and just keep on clicking them, do not switch to the new tab keep on the original tab
    #and then create another loop to loop through the tabs
    for elem in elem_list:
        #perform the click
        async with page.expect_popup() as popup_info:
            await elem_clicker(page=page, elem=elem)

        new_tab = await popup_info.value
        await new_tab.wait_for_load_state("domcontentloaded")
        TABS.append(new_tab)
    print(Fore.BLUE + TABS)




#create the main function
async def main():
    try:
        #with instance
        async with Stealth().use_async(async_playwright()) as p:
            try:
                #create a browser
                browser = await p.chromium.launch(
                    headless=False,
                    proxy={
                        "server": "socks5://127.0.0.1:9050"
                    },
                    args=[
                        "--disable-blink-features=AutomationControlled"
                    ]
                )

                #Get a list of user_agents
                ua = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.7322.14 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.7322.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.7200.58 Safari/537.36"
                ]

                #Create 3 contexts
                context1 = await browser.new_context(
                    storage_state='state1.json'
                )
                context2 = await browser.new_context(
                    storage_state='state2.json'
                )
                context3 = await browser.new_context(
                    storage_state='state3.json'
                )

                #create a page for each context
                page1 = await context1.new_page()
                page2 = await context2.new_page()
                page3 = await context3.new_page()

                #reach the desired pages
                t1 = reach_url(
                    page=page1,
                    url="https://www.redfin.com/zipcode/30310"
                )
                t2 = reach_url(
                    page=page2,
                    url="https://www.redfin.com/zipcode/30311"
                )
                t3 = reach_url(
                    page=page3,
                    url="https://www.redfin.com/zipcode/30314"
                )

                await asyncio.gather(
                    delayed_start(0, t1),
                    delayed_start(2.0, t2),
                    delayed_start(2.5, t3)
                )

                #scroll to the bottom for each context
                t1 = auto_scroll(page=page1)
                t2 = auto_scroll(page=page2)
                t3 = auto_scroll(page=page3)

                await asyncio.gather(
                    delayed_start(0, t1),
                    delayed_start(2.0, t2),
                    delayed_start(2.5, t3)
                )

                #handle all the property cards by opening their links in the new tab
                await propertry_handler(page=page1, elem_list=await page1.locator('div[id^="MapHomeCard"]').all())
                await propertry_handler(page=page2, elem_list=await page2.locator('div[id^="MapHomeCard"]').all())
                await propertry_handler(page=page3, elem_list=await page3.locator('div[id^="MapHomeCard"]').all())

                await asyncio.sleep(10)
            except:
                pass
            finally:
                #save the storage states
                await context1.storage_state(path='state1.json')
                await context2.storage_state(path='state2.json')
                await context3.storage_state(path='state3.json')

             
    except Exception as e:
        print(Fore.RED + f"Error in playwright: {e}")
    finally:
        pass
        



#run the main function
if __name__ == '__main__':
    asyncio.run(main())

