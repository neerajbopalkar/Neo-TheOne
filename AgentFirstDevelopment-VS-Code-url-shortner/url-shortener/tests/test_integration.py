"""Integration tests for the URL Shortener application."""

import pytest

import sys
from pathlib import Path

src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


class TestEndToEndFlow:
    """End-to-end integration tests."""

    def test_full_url_shortening_flow(self, client):
        """Test the complete flow: shorten a URL, then redirect to it."""
        original_url = "https://example.com/very/long/path?param=value"

        # Step 1: Create a shortened URL
        response = client.post("/api/shorten", json={"url": original_url})
        assert response.status_code == 200

        data = response.json()
        short_code = data["short_code"]
        short_url = data["short_url"]

        assert short_code
        assert short_url
        assert original_url in data["original_url"]

        # Step 2: Use the short code to redirect
        redirect_response = client.get(f"/{short_code}", follow_redirects=False)
        assert redirect_response.status_code == 301
        assert redirect_response.headers["location"] == original_url

    def test_multiple_urls_no_collisions(self, client):
        """Test that multiple shortened URLs don't collide."""
        urls = [
            "https://example.com/path1",
            "https://example.com/path2",
            "https://example.com/path3",
            "https://example.com/path4",
            "https://example.com/path5",
        ]

        short_codes = set()
        created_urls = {}

        # Create multiple shortened URLs
        for url in urls:
            response = client.post("/api/shorten", json={"url": url})
            assert response.status_code == 200

            data = response.json()
            short_code = data["short_code"]

            # Check for collisions
            assert short_code not in short_codes, f"Collision detected: {short_code}"
            short_codes.add(short_code)
            created_urls[short_code] = url

        # Verify each one redirects to the correct URL
        for short_code, expected_url in created_urls.items():
            response = client.get(f"/{short_code}", follow_redirects=False)
            assert response.status_code == 301
            assert response.headers["location"] == expected_url

    def test_same_url_creates_different_entries(self, client):
        """Test that shortening the same URL twice creates two entries."""
        url = "https://example.com/test"

        response1 = client.post("/api/shorten", json={"url": url})
        response2 = client.post("/api/shorten", json={"url": url})

        assert response1.status_code == 200
        assert response2.status_code == 200

        code1 = response1.json()["short_code"]
        code2 = response2.json()["short_code"]

        # They should have different short codes (not reusing existing entries)
        assert code1 != code2

        # Both should redirect to the same original URL
        redirect1 = client.get(f"/{code1}", follow_redirects=False)
        redirect2 = client.get(f"/{code2}", follow_redirects=False)

        assert redirect1.headers["location"] == url
        assert redirect2.headers["location"] == url

    def test_various_valid_urls(self, client):
        """Test shortening various valid URL formats."""
        test_urls = [
            "https://example.com",
            "https://example.com/",
            "https://subdomain.example.com/path",
            "https://example.com:8080/path",
            "http://localhost:3000/test",
            "https://example.com/path?key=value&key2=value2",
            "https://example.com/path#anchor",
            "https://user:pass@example.com/path",
            "https://example.com/path/with/multiple/segments",
        ]

        for url in test_urls:
            response = client.post("/api/shorten", json={"url": url})
            assert response.status_code == 200, f"Failed to shorten: {url}"

            data = response.json()
            short_code = data["short_code"]

            # Verify redirect works
            redirect_response = client.get(f"/{short_code}", follow_redirects=False)
            assert redirect_response.status_code == 301
            assert redirect_response.headers["location"] == url

    def test_health_check_always_works(self, client):
        """Test that health check is always available."""
        response = client.get("/api/health")
        assert response.status_code == 200

        # Shorten some URLs
        client.post("/api/shorten", json={"url": "https://example.com"})

        # Health check should still work
        response = client.get("/api/health")
        assert response.status_code == 200
