from typing import List, Tuple
from urllib.request import urlopen

import pytest
from PIL import Image

from core import services
from core.models import Colour

# =============
#  Fixtures
# =============


@pytest.fixture(scope="session")
def colour_crimson() -> Tuple[int]:
    return (220, 20, 60)


@pytest.fixture(scope="session")
def colour_salmon() -> Tuple[int]:
    return (250, 128, 114)


@pytest.fixture(scope="session")
def palette() -> List[Colour]:
    return [
        Colour(name="teal", r=0, g=128, b=128),
        Colour(name="red", r=255, g=0, b=0),
        Colour(name="yellow", r=251, g=206, b=177),
    ]


# =============
#  Tests
# =============


def test_is_url_image_returns_true(image_url_valid_teal):
    assert services.is_url_image(image_url_valid_teal)


def test_is_url_image_returns_false(invalid_url_no_image_content):
    assert not services.is_url_image(invalid_url_no_image_content)


def test_get_redmean_colour_difference(colour_crimson, colour_salmon):
    diff = services.get_redmean_colour_difference(colour_crimson, colour_salmon)
    assert diff == pytest.approx(235.25, 0.01)


def test_match_image_with_colour(image_url_valid_teal, palette):
    result = services.match_image_with_colour(image_url_valid_teal, palette)
    assert result["url"] == image_url_valid_teal
    assert result["matched_colour"] == "teal"


def test_compress_image(image_url_valid_teal):
    image = Image.open(urlopen(image_url_valid_teal))
    initial_height = image.height
    initial_width = image.width
    expected_height = 40
    expected_width = (40 / initial_height) * initial_width
    compressed = services.compress_image(image)
    assert compressed.height == expected_height
    assert compressed.width == expected_width


def test_check_matched_colour_dominant_success():
    colour_count = {"green": 30, "red": 50, "blue": 20}
    matched_colour = services.check_matched_colour_dominant(colour_count, 100)
    assert matched_colour == "red"


def test_check_matched_colour_dominant_failure():
    colour_count = {"green": 25, "red": 25, "blue": 25, "yellow": 25}
    matched_colour = services.check_matched_colour_dominant(colour_count, 100)
    assert matched_colour == "NO-MATCH-FOUND"
