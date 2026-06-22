import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module

@pytest.fixture
def client():
    # Arrange: snapshot activities state so tests are isolated
    backup = copy.deepcopy(app_module.activities)
    client = TestClient(app_module.app)
    try:
        yield client
    finally:
        # Restore original state after each test
        app_module.activities.clear()
        app_module.activities.update(backup)
