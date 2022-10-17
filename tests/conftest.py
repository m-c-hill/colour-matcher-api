import pytest
from fastapi.testclient import TestClient

from api import create_app
from core.schemas import Colour


@pytest.fixture(scope="session")
def client() -> TestClient:
    app = create_app()
    yield TestClient(app)


@pytest.fixture(scope="session")
def image_url_valid() -> str:
    return (
        "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-teal.png"
    )


@pytest.fixture(scope="session")
def image_url_invalid() -> str:
    return "https://www.harukimurakami.com/"
