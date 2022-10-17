def test_colour_matcher_url(client):
    response = client.post(
        "/v1/images/match-colour",
        json={
            "url": "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-black.png"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "url": "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-black.png"
    }
