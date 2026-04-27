"""FastAPI application for URL Shortener."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel

from .config import config
from .db import URLDatabase
from .encoder import decode_id, encode_id

# Initialize FastAPI app
app = FastAPI(title="URL Shortener", version="0.1.0")

# Initialize database
db = URLDatabase()

# Counter for generating sequential IDs for short codes
_url_counter = 0


class ShortenRequest(BaseModel):
    """Request model for shortening a URL."""

    url: str


class ShortenResponse(BaseModel):
    """Response model for shortened URL."""

    short_code: str
    short_url: str
    original_url: str


def _validate_url(url: str) -> bool:
    """
    Validate the provided URL.

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise
    """
    if not url:
        return False
    if len(url) < config.MIN_URL_LENGTH or len(url) > config.MAX_URL_LENGTH:
        return False
    if not (url.startswith("http://") or url.startswith("https://")):
        return False
    return True


def _get_next_id() -> int:
    """
    Get the next sequential ID for a new URL entry.

    This is a simple approach using an in-memory counter.
    For production, this could use database sequences or snowflake IDs.

    Returns:
        Next sequential ID
    """
    global _url_counter
    _url_counter += 1
    return _url_counter


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/api/shorten")
async def shorten_url(request: ShortenRequest):
    """
    Shorten a URL.

    Args:
        request: ShortenRequest with the URL to shorten

    Returns:
        ShortenResponse with the short code and URL

    Raises:
        HTTPException: If URL is invalid or shortening fails
    """
    # Validate the URL
    if not _validate_url(request.url):
        raise HTTPException(
            status_code=400,
            detail="Invalid URL. Must start with http:// or https:// and be between "
            f"{config.MIN_URL_LENGTH} and {config.MAX_URL_LENGTH} characters.",
        )

    # Get next sequential ID and encode it
    url_id = _get_next_id()
    short_code = encode_id(url_id)

    try:
        # Store in database
        db.create_url(request.url, short_code)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to shorten URL: {str(e)}"
        )

    short_url = f"{config.BASE_URL}/{short_code}"

    return ShortenResponse(
        short_code=short_code,
        short_url=short_url,
        original_url=request.url,
    )


@app.get("/{short_code}")
async def redirect_to_url(short_code: str):
    """
    Redirect to the original URL using the short code.

    Args:
        short_code: The short code to redirect from

    Returns:
        RedirectResponse to the original URL

    Raises:
        HTTPException: If short code not found
    """
    # Look up the URL
    record = db.get_url_by_code(short_code)

    if record is None:
        raise HTTPException(
            status_code=404, detail=f"Short code '{short_code}' not found"
        )

    # Redirect to the original URL
    return RedirectResponse(url=record.original_url, status_code=301)


# Serve static files (HTML, CSS, etc.)
static_dir = Path(__file__).parent.parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
async def root():
    """Serve the main HTML page."""
    return RedirectResponse(url="/static/index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
