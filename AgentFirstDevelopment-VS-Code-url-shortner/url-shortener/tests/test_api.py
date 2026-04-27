"""Tests for the FastAPI endpoints."""

import pytest

import sys
from pathlib import Path

src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


class TestHealthCheck:
    """Tests for the health check endpoint."""

    def test_health_check_returns_ok(self, client):
        """Test that health check endpoint returns OK."""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestShortenEndpoint:
    """Tests for the POST /api/shorten endpoint."""

    def test_shorten_valid_url(self, client):
        """Test shortening a valid URL."""
        response = client.post(
            "/api/shorten",
            json={"url": "https://example.com/very/long/path"},
        )
        assert response.status_code == 200

        data = response.json()
        assert "short_code" in data
        assert "short_url" in data
        assert "original_url" in data
        assert data["original_url"] == "https://example.com/very/long/path"
        assert data["short_code"] != ""
        assert "localhost:8000" in data["short_url"]

    def test_shorten_multiple_urls(self, client):
        """Test shortening multiple URLs generates different codes."""
        response1 = client.post(
            "/api/shorten",
            json={"url": "https://example.com/path1"},
        )
        response2 = client.post(
            "/api/shorten",
            json={"url": "https://example.com/path2"},
        )

        assert response1.status_code == 200
        assert response2.status_code == 200

        code1 = response1.json()["short_code"]
        code2 = response2.json()["short_code"]
        assert code1 != code2

    def test_shorten_url_without_protocol_rejected(self, client):
        """Test that URLs without http/https protocol are rejected."""
        response = client.post(
            "/api/shorten",
            json={"url": "example.com"},
        )
        assert response.status_code == 400
        assert "http" in response.json()["detail"].lower()

    def test_shorten_empty_url_rejected(self, client):
        """Test that empty URLs are rejected."""
        response = client.post(
            "/api/shorten",
            json={"url": ""},
        )
        assert response.status_code == 400

    def test_shorten_too_long_url_rejected(self, client):
        """Test that overly long URLs are rejected."""
        long_url = "https://example.com/" + "a" * 3000
        response = client.post(
            "/api/shorten",
            json={"url": long_url},
        )
        assert response.status_code == 400

    def test_shorten_http_url(self, client):
        """Test shortening a URL with http (not https)."""
        response = client.post(
            "/api/shorten",
            json={"url": "http://example.com"},
        )
        assert response.status_code == 200
        assert response.json()["original_url"] == "http://example.com"

    def test_shorten_returns_correct_short_url_format(self, client):
        """Test that the short URL has the correct format."""
        response = client.post(
            "/api/shorten",
            json={"url": "https://example.com/test"},
        )

        data = response.json()
        short_url = data["short_url"]
        short_code = data["short_code"]

        assert short_code in short_url
        assert short_url.startswith("http://localhost:8000/")


class TestRedirectEndpoint:
    """Tests for the GET /{short_code} redirect endpoint."""

    def test_redirect_with_valid_short_code(self, client):
        """Test redirecting with a valid short code."""
        # First, create a shortened URL
        create_response = client.post(
            "/api/shorten",
            json={"url": "https://example.com/redirect-test"},
        )
        short_code = create_response.json()["short_code"]

        # Then, try to redirect using the short code
        response = client.get(f"/{short_code}", follow_redirects=False)

        assert response.status_code == 301
        assert response.headers["location"] == "https://example.com/redirect-test"

    def test_redirect_with_invalid_short_code_returns_404(self, client):
        """Test that an invalid short code returns 404."""
        response = client.get("/nonexistent", follow_redirects=False)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_multiple_redirects(self, client):
        """Test that multiple different short codes redirect correctly."""
        # Create multiple URLs
        urls = [
            "https://example1.com",
            "https://example2.com",
            "https://example3.com",
        ]

        short_codes = []
        for url in urls:
            response = client.post("/api/shorten", json={"url": url})
            short_codes.append(response.json()["short_code"])

        # Verify each one redirects correctly
        for short_code, original_url in zip(short_codes, urls):
            response = client.get(f"/{short_code}", follow_redirects=False)
            assert response.status_code == 301
            assert response.headers["location"] == original_url

    def test_redirect_preserves_query_parameters(self, client):
        """Test that redirecting to a URL with query parameters works."""
        url = "https://example.com/page?param1=value1&param2=value2"
        create_response = client.post("/api/shorten", json={"url": url})
        short_code = create_response.json()["short_code"]

        response = client.get(f"/{short_code}", follow_redirects=False)
        assert response.status_code == 301
        assert response.headers["location"] == url

    def test_redirect_preserves_anchors(self, client):
        """Test that redirecting to a URL with anchors works."""
        url = "https://example.com/page#section"
        create_response = client.post("/api/shorten", json={"url": url})
        short_code = create_response.json()["short_code"]

        response = client.get(f"/{short_code}", follow_redirects=False)
        assert response.status_code == 301
        assert response.headers["location"] == url


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_redirects_to_static_index(self, client):
        """Test that the root path redirects to the static HTML."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307  # Temporary redirect
        assert "/static/index.html" in response.headers["location"]
