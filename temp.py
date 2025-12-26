from playwright.async_api import async_playwright
import asyncio


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print(type(page))

if __name__ == '__main__':
    asyncio.run(main())