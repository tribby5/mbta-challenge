import pytest


# Don't need to have an api key set for testing
@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("MBTA_API_KEY", "test_key")
