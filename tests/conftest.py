import os
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.config.settings import settings


@pytest.fixture(scope="session")
def client(tmp_path_factory):

    os.environ["VECTOR_DB_PATH"] = str(tmp_path_factory.mktemp("vector_store"))
    os.environ["DATA_DIR"] = str(tmp_path_factory.mktemp("data"))
    
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def test_env():

    os.environ["API_KEY"] = settings.API_KEY
    os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY
