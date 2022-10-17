from pydantic import BaseModel


class URLSubmit(BaseModel):
    url: str
