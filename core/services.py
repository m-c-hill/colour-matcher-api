from typing import Tuple
from PIL import Image

from .schemas import Colour

COMPRESSION_SIZE = 100

palette = [
    {"name": "salmon", "rgb": (250, 128, 114)},
    {"name": "chartreuse", "rgb": (127, 255, 0)},
    {"name": "aqua", "rgb": (255, 255, 0)},
]  # TODO: load in palette from db


def is_url_image(url: str) -> bool:
    pass


def match_colour(url: str) -> bool:
    pass


def compress_image(image: Image) -> Image:
    pass


# ===============================================


def get_redmean_colour_difference(
    colour1: Tuple[float], colour2: Tuple[float]
) -> float:
    """
    Source: https://www.compuphase.com/cmetric.htm
    """
    pass


if __name__ == "__main__":
    match_colour(
        "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-teal.png"
    )
