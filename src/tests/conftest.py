from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from nauta.client import NautaClient
from nauta.database import clear_database


@pytest.fixture
def runner():
    """
    Fixture to provide a CliRunner instance for testing.
    """
    yield CliRunner()

    with patch("nauta.database.get_global_db_path", return_value="test.db"):
        clear_database()


@pytest.fixture
def client():
    return NautaClient("correo@nauta.com.cu", "password")
