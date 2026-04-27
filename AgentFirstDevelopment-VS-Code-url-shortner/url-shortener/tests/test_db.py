"""Tests for the database module."""

import sqlite3
from datetime import datetime

import pytest

import sys
from pathlib import Path

src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from url_shortener.db import URLDatabase


class TestURLDatabase:
    """Tests for the URLDatabase class."""

    def test_database_initialization(self, test_db):
        """Test that database initializes correctly."""
        assert test_db is not None
        # Database file should exist
        assert Path(test_db.db_path).exists()

    def test_create_url(self, test_db):
        """Test creating a URL record."""
        record = test_db.create_url("https://example.com", "abc123")

        assert record.id == 1
        assert record.original_url == "https://example.com"
        assert record.short_code == "abc123"
        assert isinstance(record.created_at, datetime)

    def test_get_url_by_code(self, test_db):
        """Test retrieving a URL by short code."""
        test_db.create_url("https://example.com", "test1")
        record = test_db.get_url_by_code("test1")

        assert record is not None
        assert record.original_url == "https://example.com"
        assert record.short_code == "test1"

    def test_get_url_by_code_not_found(self, test_db):
        """Test retrieving a non-existent short code."""
        record = test_db.get_url_by_code("nonexistent")
        assert record is None

    def test_get_url_by_id(self, test_db):
        """Test retrieving a URL by ID."""
        created = test_db.create_url("https://example.com", "test2")
        record = test_db.get_url_by_id(created.id)

        assert record is not None
        assert record.id == created.id
        assert record.original_url == "https://example.com"

    def test_get_url_by_id_not_found(self, test_db):
        """Test retrieving a non-existent ID."""
        record = test_db.get_url_by_id(9999)
        assert record is None

    def test_duplicate_short_code_raises_error(self, test_db):
        """Test that duplicate short codes raise an error."""
        test_db.create_url("https://example.com", "dup")

        with pytest.raises(sqlite3.IntegrityError):
            test_db.create_url("https://another.com", "dup")

    def test_delete_url(self, test_db):
        """Test deleting a URL."""
        test_db.create_url("https://example.com", "del1")

        # Verify it exists
        assert test_db.get_url_by_code("del1") is not None

        # Delete it
        deleted = test_db.delete_url("del1")
        assert deleted is True

        # Verify it's gone
        assert test_db.get_url_by_code("del1") is None

    def test_delete_url_not_found(self, test_db):
        """Test deleting a non-existent URL."""
        deleted = test_db.delete_url("nonexistent")
        assert deleted is False

    def test_multiple_urls(self, test_db):
        """Test storing and retrieving multiple URLs."""
        test_db.create_url("https://example1.com", "url1")
        test_db.create_url("https://example2.com", "url2")
        test_db.create_url("https://example3.com", "url3")

        assert test_db.get_url_by_code("url1").original_url == "https://example1.com"
        assert test_db.get_url_by_code("url2").original_url == "https://example2.com"
        assert test_db.get_url_by_code("url3").original_url == "https://example3.com"

    def test_clear_all(self, test_db):
        """Test clearing all records."""
        test_db.create_url("https://example1.com", "url1")
        test_db.create_url("https://example2.com", "url2")

        assert test_db.get_url_by_code("url1") is not None
        assert test_db.get_url_by_code("url2") is not None

        test_db.clear_all()

        assert test_db.get_url_by_code("url1") is None
        assert test_db.get_url_by_code("url2") is None

    def test_long_urls(self, test_db):
        """Test storing very long URLs."""
        long_url = "https://example.com/" + "a" * 1000
        record = test_db.create_url(long_url, "longurl")

        retrieved = test_db.get_url_by_code("longurl")
        assert retrieved.original_url == long_url

    def test_url_with_special_characters(self, test_db):
        """Test storing URLs with special characters."""
        url = "https://example.com/path?param=value&other=123#section"
        record = test_db.create_url(url, "special")

        retrieved = test_db.get_url_by_code("special")
        assert retrieved.original_url == url
