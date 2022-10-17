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
    closest_colour: Union[ColourNamed, None] = None
    true_colour: Colour


if __name__ == "__main__":
    breakpoint()
    x = 1
