import math
from typing import Tuple, List
from urllib.request import urlopen

import numpy as np
import requests
from PIL import Image

from .schemas import Colour

COMPRESSION_SIZE = 40

palette = [
    {"name": "salmon", "rgb": (250, 128, 114)},
    {"name": "chartreuse", "rgb": (127, 255, 0)},
    {"name": "aqua", "rgb": (255, 255, 0)},
]  # TODO: load in palette from db


def is_url_image(url: str) -> bool:
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.head(url)
    return r.headers["content-type"] in image_formats


def load_image(url: str) -> np.array:
    image = Image.open(urlopen(url))
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = compress_image(image)
    return np.array(image)


def match_image_with_colour(url: str, palette: List[Colour]) -> dict:
    pixel_cache = {}
    colour_count = {}

    image_array = load_image(url)

    for row in image_array:
        for pixel in row:
            # TODO: refactor to pixel function
            rgb_pixel = tuple(pixel)

            if rgb_pixel in pixel_cache:
                matched_colour = pixel_cache[rgb_pixel]
                colour_count[matched_colour] += 1
                continue

            min_diff = math.inf
            for colour in palette:
                rgb_palette = (colour.r, colour.b, colour.g)
                diff = get_redmean_colour_difference(rgb_pixel, rgb_palette)
                if diff < min_diff:
                    min_diff = diff
                    closest_colour = colour.name

            pixel_cache[rgb_pixel] = closest_colour
            colour_count[closest_colour] = 1

    # TODO: add an upper bound to min diff to return null result if no colour matches correctly
    # TODO: add mean colour diff?

    matched_colour = max(colour_count, key=colour_count.get)
    return {"url": url, "matched_colour": matched_colour}


def match_pixel_with_colour():
    pass  # Needed?


def compress_image(image: Image) -> Image:
    if image.height <= COMPRESSION_SIZE:
        return image

    height = COMPRESSION_SIZE
    width = int((COMPRESSION_SIZE / image.height) * image.width)

    return image.resize((width, height))


def get_redmean_colour_difference(colour1: Tuple[int], colour2: Tuple[int]) -> float:
    """
    Source: https://www.compuphase.com/cmetric.htm
    """
    r1, g1, b1 = colour1
    r2, g2, b2 = colour2

    redmean_factor = 0.5 * (r1 + r2)
    d_red = r1 - r2
    d_green = g1 - g2
    d_blue = b1 - b2

    return math.sqrt(
        (2 + redmean_factor / 256) * math.pow(d_red, 2)
        + 4 * math.pow(d_green, 2)
        + (2 + (255 - redmean_factor) / 256) * math.pow(d_blue, 2)
    )


# TODO: documnetation
