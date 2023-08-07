import random
from datetime import datetime

from loguru import logger
from playwright.sync_api import Playwright, sync_playwright, TimeoutError


def run(pw: Playwright) -> None:
    browser = pw.chromium.launch(headless=False, channel='chrome')
    context = browser.new_context()
    try:
        page = context.new_page()
        page.goto("https://qrcode.antfu.me/#generator")
        page.wait_for_timeout(random.randrange(3000, 6000))

        # screenshot_bytes = page.screenshot(path="output/example.png")
        # print(base64.b64encode(screenshot_bytes).decode())
        # print(base64.b64encode(screenshot_bytes))
        logger.info(page.locator("#__nuxt canvas").count())
        print(page.locator("#__nuxt canvas").evaluate("canvas => canvas.toDataURL()"))
        # page.locator("#__nuxt canvas").screenshot(path="output/example1.png")
        # logger.info(page.locator("#__nuxt canvas")
        logger.debug('this is a debug message')

        page.wait_for_timeout(random.randrange(5000, 10000))
    finally:
        try:
            context.close()
        except BaseException as e:
            print(datetime.now(), e)
        try:
            browser.close()
        except BaseException as e:
            print(datetime.now(), e)


OUTPUT_DIRECTORY_PATH = "output"


def main():
    # start monitor
    # start_monitor()
    try:
        with sync_playwright() as playwright:
            run(playwright)
    except TimeoutError as e:
        print(datetime.now(), "wait timeout exception occurred")
        print(datetime.now(), e)
        error_flag = True
    except BaseException as e:
        print(datetime.now(), "Something else went wrong")
        print(datetime.now(), e)
        error_flag = True


main()
logger.info("all finished")
