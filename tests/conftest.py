import socket
import subprocess
import sys
import time

import pytest
from fastapi.testclient import TestClient

from app.main import app, books


def _api_is_running() -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        connection.settimeout(0.2)
        return connection.connect_ex(("127.0.0.1", 3000)) == 0


@pytest.fixture(scope="session", autouse=True)
def api_server():
    if _api_is_running():
        yield
        return

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "3000",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(50):
            if _api_is_running():
                break
            time.sleep(0.1)
        else:
            raise RuntimeError("Não foi possível iniciar a API para os testes E2E.")
        yield
    finally:
        process.terminate()
        process.wait(timeout=5)


@pytest.fixture
def client():
    original_books = books.copy()
    with TestClient(app) as test_client:
        yield test_client
    books.clear()
    books.update(original_books)
