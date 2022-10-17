def test_colour_matcher_url_success(client):
    teal_url = (
        "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-teal.png"
    )
    response = client.post(
        "/v1/images/match-colour",
        json={"url": teal_url},
    )
    assert response.status_code == 200
    assert response.json() == {
        "url": teal_url,
        "closest_colour": {"name": "teal", "r": 0, "g": 128, "b": 127},
        "true_colour": {"r": 0, "g": 128, "b": 127},
    }


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
        "closest_colour": None,
        "true_colour": {"r": 36, "g": 36, "b": 36},
    }


def test_colour_matcher_url_invalid_url(client):
    invalid_url = "https://www.harukimurakami.com/"
    response = client.post(
        "/v1/images/match-colour",
        json={"url": invalid_url},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "URL contains no valid png image."}
