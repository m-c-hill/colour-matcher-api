import pytest
from fastapi.testclient import TestClient

from api import create_app


@pytest.fixture(scope="session")
def client():
    app = create_app()
    yield TestClient(app)
