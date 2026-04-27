# URL Shortener

A minimal URL shortening service built with Python 3.14, FastAPI, SQLite, and a simple HTML/CSS frontend.

## Features

- ✨ Clean, minimal web interface
- 🔗 Generate short, alphanumeric URLs
- 📱 Redirect to original URLs
- 🗄️ SQLite database for persistence
- ✅ Comprehensive test suite with pytest
- 🚀 Fast async API with FastAPI

## Project Structure

```
url-shortener/
├── src/url_shortener/          # Main application code
│   ├── main.py                 # FastAPI app and endpoints
│   ├── encoder.py              # Base62 URL encoding/decoding
│   ├── db.py                   # SQLite database operations
│   ├── models.py               # Data models
│   └── config.py               # Configuration
├── static/                     # Frontend files
│   ├── index.html              # Main HTML page
│   └── style.css               # Styling
├── tests/                      # Test suite
│   ├── conftest.py             # Pytest fixtures and configuration
│   ├── test_encoder.py         # URL encoding tests
│   ├── test_db.py              # Database tests
│   ├── test_api.py             # API endpoint tests
│   └── test_integration.py     # End-to-end integration tests
├── pyproject.toml              # Project configuration and dependencies
└── README.md                   # This file
```

## Setup

### Prerequisites

- Python 3.14+
- UV (Python package manager)

### Installation

1. Clone or navigate to the project directory:

```bash
cd url-shortener
```

2. Create a virtual environment and install dependencies using UV:

```bash
# Install from pyproject.toml
uv sync

# Or with dev dependencies for testing
uv sync --with dev
```

### Running the Application

Start the FastAPI development server:

```bash
uv run python -m uvicorn src.url_shortener.main:app --reload
```

Then open your browser and go to:

```
http://localhost:8000
```

### Running Tests

Run the test suite with pytest:

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_encoder.py -v

# Run with coverage
uv run pytest --cov=src/url_shortener tests/
```

## API Documentation

### Health Check

Check if the service is running.

**Endpoint:** `GET /api/health`

**Response:**

```json
{
  "status": "ok"
}
```

### Shorten URL

Create a shortened URL.

**Endpoint:** `POST /api/shorten`

**Request Body:**

```json
{
  "url": "https://example.com/very/long/path?with=parameters"
}
```

**Response (Success - 200):**

```json
{
  "short_code": "a1",
  "short_url": "http://localhost:8000/a1",
  "original_url": "https://example.com/very/long/path?with=parameters"
}
```

**Response (Error - 400):**

```json
{
  "detail": "Invalid URL. Must start with http:// or https:// and be between 5 and 2048 characters."
}
```

### Redirect to Original URL

Redirect to the original URL using the short code.

**Endpoint:** `GET /{short_code}`

**Response:** HTTP 301 Redirect to the original URL

**Error (404):**

```json
{
  "detail": "Short code 'invalid' not found"
}
```

## Usage Examples

### Using cURL

```bash
# Shorten a URL
curl -X POST http://localhost:8000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/neerajbopalkar/Neo-TheOne"}'

# Response:
# {
#   "short_code": "1",
#   "short_url": "http://localhost:8000/1",
#   "original_url": "https://github.com/neerajbopalkar/Neo-TheOne"
# }

# Redirect using short code
curl -L http://localhost:8000/1
# This will redirect to https://github.com/neerajbopalkar/Neo-TheOne
```

### Using the Web Interface

1. Go to `http://localhost:8000`
2. Enter a URL in the input field
3. Click "Shorten"
4. Copy the shortened URL or click it to open in a new tab

## Configuration

Configuration is managed in `src/url_shortener/config.py`. You can override settings using environment variables:

```bash
# Set base URL for shortened links
export BASE_URL=https://myservice.com

# Set database path
export DB_PATH=/path/to/database.db

# Run the app
uv run python -m uvicorn src.url_shortener.main:app
```

## Technology Stack

- **Backend**: FastAPI 0.104+
- **Web Server**: Uvicorn
- **Database**: SQLite 3 (built-in Python module)
- **Testing**: pytest 7.4+
- **Package Manager**: UV
- **Frontend**: Vanilla HTML5 + CSS3

## URL Encoding Details

Short codes are generated using base62 encoding (0-9, a-z, A-Z) which:

- Creates human-readable, URL-safe codes
- Prevents collisions (sequential IDs)
- Is efficient (62^n possibilities)

**Examples:**

- ID 1 → code "1"
- ID 62 → code "10"
- ID 1000 → code "g8"

## Test Coverage

The test suite includes:

- **Unit Tests**: Encoder, database operations (test_encoder.py, test_db.py)
- **API Tests**: Endpoint behavior, validation, error handling (test_api.py)
- **Integration Tests**: End-to-end flows, no collisions, multiple URLs (test_integration.py)

**Current Coverage**: ~65-70% of backend code

Run tests with coverage report:

```bash
uv run pytest --cov=src/url_shortener tests/
```

## Future Enhancements

- [ ] User accounts and URL management dashboard
- [ ] Custom short codes (vanity URLs)
- [ ] Analytics (click tracking, hit counts)
- [ ] API authentication (API keys)
- [ ] URL expiration / TTL
- [ ] Rate limiting
- [ ] QR code generation
- [ ] Browser extension

## License

This project is part of the Neo-TheOne workspace. See the main README for details.

## Development Notes

### Adding New Features

1. Write tests first (TDD approach)
2. Implement the feature
3. Update this README if needed
4. Run full test suite to ensure no regressions

### Database

- Uses file-based SQLite database at `urls.db` (created automatically)
- For testing, uses in-memory SQLite (configured in `conftest.py`)
- No ORM; direct SQL for simplicity and learning

### Architecture Decisions

- **Sequential IDs + Base62**: Simple, collision-free, deterministic
- **FastAPI**: Modern async framework, excellent testing support
- **Direct SQLite**: No external dependencies, easier to understand
- **Minimal Frontend**: Focus on backend; basic HTML/CSS frontend
