"""Database module for URL Shortener using SQLite."""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from .config import config
from .models import URLRecord


class URLDatabase:
    """Manages SQLite database operations for storing shortened URLs."""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the database connection.

        Args:
            db_path: Path to SQLite database file. If None, uses config.DB_PATH
        """
        self.db_path = db_path or config.DB_PATH
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Create the database and table if they don't exist."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_url TEXT NOT NULL,
                    short_code TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_short_code ON urls(short_code)
                """
            )
            conn.commit()

    def create_url(self, original_url: str, short_code: str) -> URLRecord:
        """
        Store a shortened URL mapping in the database.

        Args:
            original_url: The full URL to store
            short_code: The generated short code

        Returns:
            URLRecord with the inserted data

        Raises:
            sqlite3.IntegrityError: If short_code already exists
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO urls (original_url, short_code)
                VALUES (?, ?)
                """,
                (original_url, short_code),
            )
            conn.commit()

            # Retrieve the inserted record
            row_id = cursor.lastrowid
            record = self.get_url_by_id(row_id)
            if record is None:
                raise RuntimeError("Failed to retrieve inserted record")
            return record

    def get_url_by_code(self, short_code: str) -> Optional[URLRecord]:
        """
        Retrieve the original URL by its short code.

        Args:
            short_code: The short code to look up

        Returns:
            URLRecord if found, None otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, original_url, short_code, created_at
                FROM urls
                WHERE short_code = ?
                """,
                (short_code,),
            )
            row = cursor.fetchone()

        if row is None:
            return None

        return URLRecord(
            id=row[0],
            original_url=row[1],
            short_code=row[2],
            created_at=datetime.fromisoformat(row[3]),
        )

    def get_url_by_id(self, url_id: int) -> Optional[URLRecord]:
        """
        Retrieve a URL record by its database ID.

        Args:
            url_id: The database ID

        Returns:
            URLRecord if found, None otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, original_url, short_code, created_at
                FROM urls
                WHERE id = ?
                """,
                (url_id,),
            )
            row = cursor.fetchone()

        if row is None:
            return None

        return URLRecord(
            id=row[0],
            original_url=row[1],
            short_code=row[2],
            created_at=datetime.fromisoformat(row[3]),
        )

    def delete_url(self, short_code: str) -> bool:
        """
        Delete a URL mapping by its short code.

        Args:
            short_code: The short code to delete

        Returns:
            True if a record was deleted, False if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM urls WHERE short_code = ?", (short_code,))
            conn.commit()
            return cursor.rowcount > 0

    def clear_all(self):
        """Clear all records from the database (for testing)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM urls")
            conn.commit()
