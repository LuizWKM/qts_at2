import pytest
from fastapi.testclient import TestClient

from app.main import app, books


@pytest.fixture
def client():
    original_books = books.copy()
    with TestClient(app) as test_client:
        yield test_client
    books.clear()
    books.update(original_books)
