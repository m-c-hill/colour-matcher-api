import pytest
from api import create_app
from core.schemas import Colour
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def client() -> TestClient:
    app = create_app()
    yield TestClient(app)


@pytest.fixture(scope="session")
def image_url_valid_teal() -> str:
    return (
        "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-teal.png"
    )


@pytest.fixture(scope="session")
def invalid_url_no_image_content() -> str:
    return "https://www.harukimurakami.com/"
