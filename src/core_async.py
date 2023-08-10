import asyncio
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


# class Task:
#     task_id: str
#     content: str


class Instance:
    def __init__(self, headless=True):
        self.isStarted = False
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.page_limit = 1
        # self.task_queue = queue.Queue(maxsize=1000)
        self.lock = asyncio.Lock()

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
            await page.goto("http://localhost:3000")
            await page.wait_for_timeout(100)
            # Error Correction = L
            await page.locator(
                "#__nuxt > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > fieldset > label:nth-child(1) > input[type=radio]") \
                .click()

            # Boost ECC = Checked
            await page.locator(
                "#__nuxt > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > label > div > input[type=checkbox]") \
                .click()

            # Mask Pattern = 7
            await page.locator(
                "#__nuxt > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(2) > label:nth-child(2) > fieldset > label:nth-child(9) > input[type=radio]") \
                .click()

            # pixel style = Heart
            await page.locator(
                "#__nuxt > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(2) > label:nth-child(5) > fieldset > label:nth-child(2) > input[type=radio]") \
                .click()
            # Maker pixel
            await page.locator(
                "#__nuxt > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(2) > label:nth-child(7) > fieldset:nth-child(2) > label:nth-child(2) > input[type=radio]") \
                .click()
            # Maker shape
            await page.locator(
                "#__nuxt > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(2) > label:nth-child(8) > fieldset > label:nth-child(6) > input[type=radio]") \
                .click()
            # Maker inner
            await page.locator(
                "#__nuxt > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(2) > label:nth-child(9) > fieldset:nth-child(2) > label:nth-child(3) > input[type=radio]") \
                .click()

            # Margin = 6
            await page.locator(
                "#__nuxt > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(2) > div:nth-child(11) > div:nth-child(3) > input[type=number]") \
                .fill("7")
            # safe space = Extreme
            await page.locator(
                "#__nuxt > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(2) > label:nth-child(13) > fieldset > label:nth-child(4) > input[type=radio]") \
                .click()
            # Render type = all
            await page.locator(
                "#__nuxt > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(2) > label:nth-child(14) > fieldset > label:nth-child(1) > input[type=radio]") \
                .click()

            # clear seed input
            await page.locator(
                "#__nuxt > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(2) > label:nth-child(15) > input[type=number]") \
                .fill("")
            # background color = #888888
            await page.locator(
                "#__nuxt > div > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(2) > div:nth-child(16) > button:nth-child(4)") \
                .click()

            self.page = page
        except BaseException as e:
            logger.info(e)

    # async def submit_task(self, task: Task):
    #     self.task_queue.put(task)

    async def generate(self, content: str) -> str:
        async with self.lock:
            page = self.page
            if page is None:
                return ""

            textarea = page.locator("#__nuxt textarea")
            await textarea.fill(content)
            await page.wait_for_timeout(500)
            # screenshot_bytes = page.screenshot(path="output/example.png")
            # logger.info(base64.b64encode(screenshot_bytes).decode())
            # logger.info(base64.b64encode(screenshot_bytes))
            base64str = await page.locator("#__nuxt canvas").evaluate("canvas => canvas.toDataURL()")
            # logger.info(page.locator("#__nuxt canvas").count())
            # logger.info(page.locator("#__nuxt canvas").evaluate("canvas => canvas.toDataURL()"))
            # page.locator("#__nuxt canvas").screenshot(path="output/example1.png")
            # logger.info(page.locator("#__nuxt canvas")
            # logger.debug('this is a debug message')
            await textarea.clear()
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
