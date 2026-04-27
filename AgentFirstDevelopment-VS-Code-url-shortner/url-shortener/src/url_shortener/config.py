"""Configuration module for URL Shortener."""

import os
from pathlib import Path


class Config:
    """Application configuration."""

    # Base URL for shortened links (used in frontend and API responses)
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

    # Database configuration
    DB_PATH = os.getenv("DB_PATH", str(Path(__file__).parent.parent.parent.parent / "urls.db"))

    # Max URL length to accept (reasonable limit)
    MAX_URL_LENGTH = 2048

    # Min URL length to accept
    MIN_URL_LENGTH = 5


config = Config()
