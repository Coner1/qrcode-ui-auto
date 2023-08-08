from pydantic import BaseModel


class GetQrcode(BaseModel):
    content: str
