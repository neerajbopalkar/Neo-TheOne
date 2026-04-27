# Setup and Installation Guide

## Prerequisites

- **Python 3.14** or higher
- **UV** - Fast Python package installer and project manager

## Installing UV

UV is the recommended way to manage this project. Install it globally:

### On Windows (using PowerShell)
```powershell
# Using pip (if Python is already installed)
pip install uv

# Or download from: https://github.com/astral-sh/uv/releases
```

### On macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For more installation methods, see the [UV documentation](https://github.com/astral-sh/uv).

## Project Setup

### 1. Navigate to the project directory
```bash
cd base62-codec
```

### 2. Install dependencies using UV

```bash
# Install the project in development mode
uv sync

# Or install with all development dependencies
uv sync --all-extras
```

This will:
- Create a virtual environment
- Install all dependencies specified in `pyproject.toml`
- Install the project in editable mode

### 3. Verify Installation

```bash
# Check Python version
uv run python --version

# Test the package import
uv run python -c "import base62; print('✓ base62 module imported successfully')"
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage report
uv run pytest --cov=base62 --cov-report=html

# Run specific test file
uv run pytest tests/test_base62.py -v

# Run specific test
uv run pytest tests/test_base62.py::TestBasicEncoding::test_encode_zero -v
```

After running coverage, open `htmlcov/index.html` to view the coverage report.

## Running Examples

```bash
# Run all examples
uv run python examples.py

# Or run interactively
uv run python
>>> from base62 import encode, decode
>>> encode(12345)
'315'
```

## Development Workflow

### Code Quality Tools

```bash
# Format code with black
uv run black base62 tests examples.py

# Lint with ruff
uv run ruff check base62 tests examples.py

# Fix linting issues automatically
uv run ruff check --fix base62 tests examples.py
```

### Common Development Tasks

```bash
# Run all checks (format, lint, test)
uv run black base62 tests examples.py && uv run ruff check --fix base62 tests && uv run pytest

# Interactive Python shell with project context
uv run python

# Install additional package (example)
uv pip install <package-name>
```

## Project Structure

```
base62-codec/
├── base62/
│   └── __init__.py          # Main module with encode/decode functions
├── tests/
│   ├── __init__.py
│   └── test_base62.py       # Comprehensive test suite (100+ tests)
├── examples.py              # Usage examples
├── pyproject.toml           # Project configuration
├── README.md                # User documentation
├── LICENSE                  # MIT License
├── .gitignore               # Git ignore rules
└── SETUP.md                 # This file
```

## Project Configuration (pyproject.toml)

Key configuration points:

```toml
[project]
requires-python = ">=3.14"

[tool.uv]
python-version = "3.14"

[project.optional-dependencies]
dev = ["pytest>=7.0", "pytest-cov>=4.0", "black>=23.0", "ruff>=0.1"]
```

## Troubleshooting

### Python 3.14 Not Found

If you get an error that Python 3.14 is not found:

```bash
# Install Python 3.14
uv python install 3.14

# Or list available Python versions
uv python list
```

### Permission Denied (macOS/Linux)

```bash
# Make sure UV is executable
chmod +x ~/.local/bin/uv
```

### Virtual Environment Issues

```bash
# Remove UV cache and sync fresh
uv sync --refresh

# Or completely recreate
rm -rf .venv
uv sync
```

### Import Errors

```bash
# Reinstall in editable mode
uv pip install -e .

# Or full reinstall
uv sync --refresh
```

## Next Steps

1. **Read the main README**: Check [README.md](README.md) for API reference
2. **Run examples**: Execute `uv run python examples.py` to see usage patterns
3. **Run tests**: Execute `uv run pytest` to verify everything works
4. **Explore the code**: Check `base62/__init__.py` for implementation details

## Additional Resources

- [UV Documentation](https://github.com/astral-sh/uv)
- [Python 3.14 Documentation](https://docs.python.org/3.14/)
- [pytest Documentation](https://docs.pytest.org/)
- [Base 62 Wikipedia](https://en.wikipedia.org/wiki/Base62)

## Support

For issues or questions, please open an issue on the GitHub repository.
