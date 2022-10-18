import pytest

# ==================
#  Fixtures
# ==================


@pytest.fixture(scope="session")
def invalid_url_no_dominant_colour() -> str:
    return "https://media.pitchfork.com/photos/5929b2fe9d034d5c69bf4c59/1:1/w_600/7055fb4d.jpg"


# ==================
#  Tests
# ==================


def test_colour_matcher_url_success(client, image_url_valid_teal):
    response = client.post(
        "/v1/images/match-colour",
        json={"url": image_url_valid_teal},
    )
    assert response.status_code == 200
    assert response.json() == {
        "url": image_url_valid_teal,
        "matched_colour": "skobeloff",
    }


def test_colour_matcher_url_no_match(client, invalid_url_no_dominant_colour):
    response = client.post(
        "/v1/images/match-colour",
        json={"url": invalid_url_no_dominant_colour},
    )
    assert response.status_code == 200
    assert response.json() == {
        "url": invalid_url_no_dominant_colour,
        "matched_colour": "NO-MATCH-FOUND",
    }


def test_colour_matcher_url_invalid_url(client, invalid_url_no_image_content):
    response = client.post(
        "/v1/images/match-colour",
        json={"url": invalid_url_no_image_content},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "URL contains no valid image content."}
