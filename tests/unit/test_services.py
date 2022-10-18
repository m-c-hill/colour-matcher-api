from typing import Tuple
from urllib.request import urlopen

import pytest
from PIL import Image

from core import services

# =============
#  Fixtures
# =============


@pytest.fixture(scope="session")
def colour_crimson() -> Tuple[int]:
    return (220, 20, 60)


@pytest.fixture(scope="session")
def colour_salmon() -> Tuple[int]:
    return (250, 128, 114)


# =============
#  Tests
# =============


def test_match_image_with_colour(image_url_valid):
    result = services.match_image_with_colour(image_url_valid)

    assert result["url"] == image_url_valid
    assert result["matched_colour"] == "teal"
    assert result["diff"] == pytest.approx(120.4, 0.1)


def test_match_pixel_with_colour():
    pass


def test_is_url_image_returns_true(image_url_valid):
    assert services.is_url_image(image_url_valid)


def test_is_url_image_returns_false(image_url_invalid):
    assert not services.is_url_image(image_url_invalid)


def test_compress_image():
    image_url = "https://media.pitchfork.com/photos/5929a0fb13d197565213850b/1:1/w_600/7e252f9a.jpg"
    image = Image.open(urlopen(image_url))
    initial_height = image.height
    initial_width = image.width
    expected_height = 100
    expected_width = (100 / initial_height) * initial_width

    compressed = services.compress_image(image)

    assert compressed.height == expected_height
    assert compressed.width == expected_width


def test_get_redmean_colour_difference(colour_crimson, colour_salmon):
    diff = services.get_redmean_colour_difference(colour_crimson, colour_salmon)
    assert diff == pytest.approx(235.25, 0.01)


def test_load_image():
    url = "https://media.pitchfork.com/photos/5929a0fb13d197565213850b/1:1/w_600/7e252f9a.jpg"
    services.load_image(url)
    # Mock to reduce compression to 10?
