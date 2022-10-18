import math
from typing import List, Tuple
from urllib.request import urlopen

import numpy as np
import requests
from nptyping import NDArray
from PIL import Image

from .schemas import Colour

COMPRESSION_SIZE = 40
PIXEL_DOMINANCE_THRESHOLD = 30


def is_url_image(url: str) -> bool:
    """
    Check if URL contains valid image content.
    """
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.head(url)
    return r.headers["content-type"] in image_formats


def load_image(url: str) -> NDArray:
    """
    Load an image from a URL and convert into an array of rows containing
    pixels with RGB colour values.
    """
    image = Image.open(urlopen(url))

    if image.mode != "RGB":
        image = image.convert("RGB")
    image = compress_image(image)

    return np.array(image)


def compress_image(image: Image) -> Image:
    """
    Compress an image based on a defined compression size.
    """
    if image.height <= COMPRESSION_SIZE:
        return image
    height = COMPRESSION_SIZE
    width = int((COMPRESSION_SIZE / image.height) * image.width)
    return image.resize((width, height))


def get_redmean_colour_difference(colour1: Tuple[int], colour2: Tuple[int]) -> float:
    """
    Calculate the colour difference between two colours using their RGB values
    and the the redmean equation.
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


def match_image_with_colour(url: str, palette: List[Colour]) -> dict:
    """
    Match an image with a colour from a palette of predefined colours.
    """
    pixel_cache = {}
    colour_count = {}

    image_array = load_image(url)

    for row in image_array:
        for pixel in row:
            rgb_pixel = tuple(pixel)
            if rgb_pixel in pixel_cache:
                matched_colour = pixel_cache[rgb_pixel]
                colour_count[matched_colour] += 1
                continue

            closest_colour = match_pixel_with_colour(rgb_pixel, palette)
            pixel_cache[rgb_pixel] = closest_colour
            colour_count[closest_colour] = colour_count.get(closest_colour, 0) + 1

    pixel_count = len(image_array) * len(image_array[0])
    matched_colour = check_matched_colour_dominant(colour_count, pixel_count)
    return {"url": url, "matched_colour": matched_colour}


def match_pixel_with_colour(pixel: Tuple[int], palette: List[Colour]) -> str:
    """
    Match a pixel (RGB tuple) with a colour from a palette of predefined
    colours.
    """
    min_diff = math.inf
    for colour in palette:
        rgb_palette = (colour.r, colour.g, colour.b)
        diff = get_redmean_colour_difference(pixel, rgb_palette)
        if diff < min_diff:
            min_diff = diff
            closest_colour = colour.name
    return closest_colour


def check_matched_colour_dominant(colour_count: dict, pixel_count: int) -> str:
    """
    Check the most frequent colour match exceeds the minimum threshold to be
    considered the matching colour.
    """
    dominant_pixel_percentage = (max(colour_count.values()) * 100) / pixel_count

    if dominant_pixel_percentage >= PIXEL_DOMINANCE_THRESHOLD:
        return max(colour_count, key=colour_count.get)
    return "NO-MATCH-FOUND"
