import os

from loguru import logger
from playwright.async_api import async_playwright


# async def main():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch()
#         page = await browser.new_page()
#         await page.goto("http://playwright.dev")
#         print(await page.title())
#         await browser.close()


# asyncio.run(main())

def remove_base64_img_prefix(s: str) -> str:
    s = s.removeprefix("data:image/png;base64,")
    s = s.removeprefix("data:image/jpg;base64,")
    s = s.removeprefix("data:image/jpeg;base64,")
    return s


def save_image(name, b):
    if not os.path.exists("output"):
        os.makedirs("output")
        logger.info(f"Directory 'output' created successfully.")
    # Check if the file exists
    image_full_path = os.path.join(os.path.join("output", name))
    with open(image_full_path, "wb") as f:
        f.write(b)
        logger.info(f"image saved,path={image_full_path}")


class Instance:
    def __init__(self, headless=True):
        self.isStarted = False
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.page_limit = 1

    async def start(self) -> None:
        try:
            if not self.isStarted:
                p = await async_playwright().start()
                self.browser = await p.chromium.launch(headless=self.headless, channel='chrome')
                await self.add_one_page()
                self.isStarted = True
        except TimeoutError as e:
            logger.info("wait timeout exception occurred")
            logger.info(e)
        except BaseException as e:
            logger.info("Something else went wrong")
            logger.info(e)

    async def add_one_page(self):
        if self.page_limit >= 5:
            return
        try:
            page = await self.browser.new_page()
            await page.goto("https://qrcode.antfu.me/#generator")
            await page.wait_for_timeout(100)
            self.page = page
        except BaseException as e:
            logger.info(e)

    async def generate(self, text: str) -> str:
        page = self.page
        if page is None:
            return ""
        logger.info(await page.locator("#__nuxt textarea").count())
        await page.locator("#__nuxt textarea").type(text=text)
        await page.wait_for_timeout(1000)
        # screenshot_bytes = page.screenshot(path="output/example.png")
        # logger.info(base64.b64encode(screenshot_bytes).decode())
        # logger.info(base64.b64encode(screenshot_bytes))
        base64str = await page.locator("#__nuxt canvas").evaluate("canvas => canvas.toDataURL()")
        # logger.info(page.locator("#__nuxt canvas").count())
        # logger.info(page.locator("#__nuxt canvas").evaluate("canvas => canvas.toDataURL()"))
        # page.locator("#__nuxt canvas").screenshot(path="output/example1.png")
        # logger.info(page.locator("#__nuxt canvas")
        # logger.debug('this is a debug message')
        return base64str

    async def close(self):
        try:
            if self.page is not None:
                await self.page.close()
        except BaseException as e:
            logger.error(e)
        try:
            if self.context is not None:
                await self.context.close()
        except BaseException as e:
            logger.error(e)
        try:
            if self.playwright is not None:
                await self.playwright.close()
        except BaseException as e:
            logger.error(e)

#
# instance_global = Instance()
#
#
# async def get_instance(headless: bool) -> Instance:
#     """
#     :rtype: Instance
#     """
#     global instance_global
#     return instance_global
