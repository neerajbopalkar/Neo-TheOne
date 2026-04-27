"""Data models for URL Shortener."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class URLRecord:
    """Represents a shortened URL record in the database."""

    id: int
    original_url: str
    short_code: str
    created_at: datetime

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "original_url": self.original_url,
            "short_code": self.short_code,
            "created_at": self.created_at.isoformat(),
        }
