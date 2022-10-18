import pytest

def test_colour_matcher_url_success(client, image_url_valid_teal):
    response = client.post(
        "/v1/images/match-colour",
        json={"url": image_url_valid_teal},
    )
    assert response.status_code == 200
    assert response.json() == {
        "url": image_url_valid_teal,
        "matched_colour": "tropical_rain_forest"
    }


@pytest.mark.skip(reason="Not yet implemented")
def test_colour_matcher_url_no_match(client):
    grey_url = (
        "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-grey.png"
    )
    response = client.post(
        "/v1/images/match-colour",
        json={"url": grey_url},
    )
    assert response.status_code == 200
    assert response.json() == {
        "url": grey_url,
        "matched_colour": None
    }


def test_colour_matcher_url_invalid_url(client, invalid_url_no_image_content):
    response = client.post(
        "/v1/images/match-colour",
        json={"url": invalid_url_no_image_content},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "URL contains no valid image content."}
