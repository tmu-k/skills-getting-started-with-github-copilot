from fastapi.testclient import TestClient
from src.app import app, activities
import copy
import pytest


@pytest.fixture(autouse=True)
def client():
    """Provide a TestClient and reset activities state for each test."""
    # Arrange: snapshot the original activities
    original = copy.deepcopy(activities)

    # Act: yield the client to the test
    client = TestClient(app)
    yield client

    # Assert / teardown: restore activities to original state
    activities.clear()
    activities.update(original)
