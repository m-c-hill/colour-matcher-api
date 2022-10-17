import math
from nis import match
from typing import Tuple
import requests
import numpy as np
from urllib.request import urlopen
from PIL import Image

from .schemas import Colour

COMPRESSION_SIZE = 100

# TODO: documnetation

palette = [
    {"name": "salmon", "rgb": (250, 128, 114)},
    {"name": "chartreuse", "rgb": (127, 255, 0)},
    {"name": "aqua", "rgb": (255, 255, 0)},
]  # TODO: load in palette from db


def is_url_image(url: str) -> bool:
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.head(url)
    return r.headers["content-type"] in image_formats


def match_colour(url: str) -> bool:
    pixel_cache = {}
    colour_count = {}

    image = Image.open(urlopen(url))
    if image.mode != "RGB":
        image = image.convert("RGB")

    image = compress_image(image)
    image_arr = np.array(image)

    min_diff = math.inf  # TODO: doesn't seem right... think about eqn
    for row in image_arr:
        for pixel in row:
            rgb_pixel = tuple(pixel)

            if rgb_pixel in pixel_cache:
                colour_name = pixel_cache[rgb_pixel]["matched_colour"]
                colour_count[colour_name] += 1
                continue

            for colour in palette:
                rgb_palette = colour["rgb"]
                diff = get_redmean_colour_difference(rgb_pixel, rgb_palette)
                min_diff = min(min_diff, diff)
                pixel_cache[rgb_pixel] = {
                    "matched_colour": colour["name"],
                    "diff": diff,
                }
                colour_count[colour["name"]] = 1

    # TODO: add an upper bound to min diff to return null result if no colour matches correctly

    matched_colour = max(colour_count, key=colour_count.get)
    return {"url": url, "matched_colour": matched_colour, "diff": min_diff}


def compress_image(image: Image) -> Image:
    if image.height <= COMPRESSION_SIZE:
        return image

    height = COMPRESSION_SIZE
    width = int(COMPRESSION_SIZE / image.height * image.width)

    return image.resize((height, width))


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
