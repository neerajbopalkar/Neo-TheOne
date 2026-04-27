"""Pytest configuration and fixtures for URL Shortener tests."""

import os
import sqlite3
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add src to path so imports work
import sys

src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from url_shortener.main import app
from url_shortener.db import URLDatabase
from url_shortener import config as config_module


@pytest.fixture
def temp_db():
    """Create a temporary SQLite database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    yield db_path

    # Cleanup with error handling for Windows file locking issues
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except (PermissionError, OSError):
            # On Windows, SQLite may still hold locks - allow cleanup to fail gracefully
            pass


@pytest.fixture
def test_db(temp_db):
    """Create a fresh URLDatabase instance with a temporary database."""
    db = URLDatabase(db_path=temp_db)
    yield db
    # Cleanup is handled by temp_db fixture


@pytest.fixture
def client(temp_db, monkeypatch):
    """Create a TestClient with a temporary database."""
    # Monkey-patch the config to use temp database
    monkeypatch.setattr(config_module.config, "DB_PATH", temp_db)

    # Reset the URL counter
    import url_shortener.main as main_module
    main_module._url_counter = 0

    # Re-initialize the database in the app
    main_module.db = URLDatabase(db_path=temp_db)

    yield TestClient(app)


@pytest.fixture(autouse=True)
def reset_url_counter(monkeypatch):
    """Reset the URL counter before each test."""
    import url_shortener.main as main_module
    main_module._url_counter = 0
    yield
