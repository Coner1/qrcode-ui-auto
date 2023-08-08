import random

from loguru import logger
from playwright.sync_api import TimeoutError, Page, sync_playwright


class Instance:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page: Page = None

        self.page_limit = 1

    def start(self) -> None:
        try:
            self.playwright = sync_playwright().start()
            # with sync_playwright() as playwright:
            #     run(playwright)
            self.browser = self.playwright.chromium.launch(headless=self.headless, channel='chrome')
            self.add_one_page()
        except TimeoutError as e:
            logger.info("wait timeout exception occurred")
            logger.info(e)
        except BaseException as e:
            logger.info("Something else went wrong")
            logger.info(e)

    def add_one_page(self):
        if self.page_limit >= 5:
            return
        try:
            # BrowserContext
            context = self.browser.new_context()
            page = context.new_page()
            page.goto("https://qrcode.antfu.me/#generator")
            page.wait_for_timeout(random.randrange(3000, 6000))
            self.context = context
            self.page = page
        except BaseException as e:
            logger.info(e)

    def generate(self, text: str) -> str:
        page = self.page
        if page is None:
            return ""
        logger.info(page.locator("#__nuxt textarea").count())
        page.locator("#__nuxt textarea").type(text=text)
        page.wait_for_timeout(10)
        # screenshot_bytes = page.screenshot(path="output/example.png")
        # logger.info(base64.b64encode(screenshot_bytes).decode())
        # logger.info(base64.b64encode(screenshot_bytes))
        base64str = page.locator("#__nuxt canvas").evaluate("canvas => canvas.toDataURL()")
        # logger.info(page.locator("#__nuxt canvas").count())
        # logger.info(page.locator("#__nuxt canvas").evaluate("canvas => canvas.toDataURL()"))
        # page.locator("#__nuxt canvas").screenshot(path="output/example1.png")
        # logger.info(page.locator("#__nuxt canvas")
        # logger.debug('this is a debug message')
        return base64str

    def close(self):
        try:
            if self.page is not None:
                self.page.close()
        except BaseException as e:
            logger.error(e)
        try:
            if self.context is not None:
                self.context.close()
        except BaseException as e:
            logger.info(e)
        try:
            self.playwright.close()
        except BaseException as e:
            logger.info(e)

# main()
# logger.info("all finished")
