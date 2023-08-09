from fastapi import FastAPI
from loguru import logger

from src import core_async

app = FastAPI()
# ins = core.Instance()
# ins.start()


ins = core_async.Instance(False)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/api/qrcode/get")
async def get_qrcode(content: str):
    logger.info(content)
    await ins.start()
    # i = core_async.get_instance(False)
    base64_str = await ins.generate(content)
    base64_str = core_async.remove_base64_img_prefix(base64_str)
    # core_async.save_image(urllib.parse.quote_plus(content + ".png"), base64.b64decode(base64_str))
    # await ins.close()s
    return base64_str
