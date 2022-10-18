from typing import Union

from pydantic import BaseModel


class Colour(BaseModel):
    r: int
    g: int
    b: int


class ColourNamed(Colour):
    name: str


class URLSubmit(BaseModel):
    url: str


class ColourMatchResponse(BaseModel):
    url: str
    matched_colour: Union[str, None] = None


class ImageCreate(BaseModel):
    url: str
    matched_colour_id: int
