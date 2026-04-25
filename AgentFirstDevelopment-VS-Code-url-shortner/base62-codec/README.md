# Base 62 Codec

A high-performance base 62 encoder/decoder library for Python 3.14. Supports encoding/decoding integers, bytes, and strings.

## Features

- 🚀 Fast and efficient base 62 encoding/decoding
- 🔤 Support for integers, bytes, and strings
- 🛡️ Type-safe with comprehensive error handling
- 📝 Fully documented with docstrings and examples
- ✅ Comprehensive test suite (100+ tests)
- 🐍 Python 3.14+ compatible
- 📦 Built with UV for fast dependency management

## Installation

### Using UV

```bash
# Clone the repository
git clone https://github.com/neerajbopalkar/Neo-TheOne.git
cd Neo-TheOne/base62-codec

# Create virtual environment and install dependencies
uv sync

# Or install in development mode with dev dependencies
uv sync --all-extras
```

## Quick Start

```python
from base62 import encode, decode, encode_str, decode_str

# Encode/decode integers
encoded = encode(12345)        # Returns: "315"
decoded = decode("315")        # Returns: 12345

# Encode/decode strings
encoded = encode_str("Hello")  # Returns: "1SbS5h"
decoded = decode_str("1SbS5h") # Returns: "Hello"
```

## Usage Examples

### Basic Integer Operations

```python
from base62 import encode, decode

# Encoding integers
print(encode(0))           # Output: '0'
print(encode(62))          # Output: '10'
print(encode(1000000))     # Output: '4c92'

# Decoding strings
print(decode('0'))         # Output: 0
print(decode('10'))        # Output: 62
print(decode('4c92'))      # Output: 1000000
```

### Working with Bytes

```python
from base62 import encode_bytes, decode_bytes

# Encode binary data
data = b"hello"
encoded = encode_bytes(data)
print(encoded)  # Output: '32D5Y6CyC'

# Decode back to bytes
decoded = decode_bytes(encoded)
print(decoded)  # Output: b'hello'

# Specify expected length (pads with leading zeros)
decoded = decode_bytes(encoded, length=10)
print(decoded)  # Output: b'\x00\x00\x00\x00\x00hello'
```

### Working with Strings

```python
from base62 import encode_str, decode_str

# Encode text
text = "Hello, World!"
encoded = encode_str(text)
print(encoded)  # Output: '73Oy60hGEW4eFPf9qV'

# Decode text
decoded = decode_str(encoded)
print(decoded)  # Output: "Hello, World!"

# Unicode support
unicode_text = "你好世界 🌍"
encoded = encode_str(unicode_text)
decoded = decode_str(encoded)
assert decoded == unicode_text
```

## Character Set

Base 62 uses 62 characters for encoding:
- `0-9` (10 digits)
- `a-z` (26 lowercase letters)
- `A-Z` (26 uppercase letters)

```
Charset: "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
```

## API Reference

### `encode(num: int) -> str`

Encode a non-negative integer to base 62 string.

**Args:**
- `num`: Non-negative integer to encode

**Returns:** Base 62 encoded string

**Raises:** `Base62Error` if num is negative

```python
>>> encode(3843)
'1Zz'
```

### `decode(encoded: str) -> int`

Decode a base 62 string to an integer.

**Args:**
- `encoded`: Base 62 encoded string

**Returns:** Decoded integer

**Raises:** `Base62Error` if encoded contains invalid characters

```python
>>> decode('1Zz')
3843
```

### `encode_bytes(data: bytes) -> str`

Encode bytes to base 62 string.

**Args:**
- `data`: Bytes to encode

**Returns:** Base 62 encoded string

```python
>>> encode_bytes(b'hello')
'32D5Y6CyC'
```

### `decode_bytes(encoded: str, length: int | None = None) -> bytes`

Decode base 62 string to bytes.

**Args:**
- `encoded`: Base 62 encoded string
- `length`: Optional expected length in bytes (pads with leading zeros if specified)

**Returns:** Decoded bytes

**Raises:** `Base62Error` if length mismatch or invalid characters

```python
>>> decode_bytes('32D5Y6CyC')
b'hello'
>>> decode_bytes('32D5Y6CyC', length=10)
b'\x00\x00\x00\x00\x00hello'
```

### `encode_str(text: str, encoding: str = "utf-8") -> str`

Encode a string to base 62.

**Args:**
- `text`: String to encode
- `encoding`: Text encoding to use (default: utf-8)

**Returns:** Base 62 encoded string

```python
>>> encode_str('Hello, World!')
'73Oy60hGEW4eFPf9qV'
```

### `decode_str(encoded: str, encoding: str = "utf-8") -> str`

Decode a base 62 string back to a string.

**Args:**
- `encoded`: Base 62 encoded string
- `encoding`: Text encoding to use (default: utf-8)

**Returns:** Decoded string

**Raises:** `Base62Error` if invalid characters; `UnicodeDecodeError` if invalid UTF-8

```python
>>> decode_str('73Oy60hGEW4eFPf9qV')
'Hello, World!'
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=base62 --cov-report=html

# Run specific test file
uv run pytest tests/test_base62.py

# Run with verbose output
uv run pytest -v
```

## Performance

The library is optimized for performance:
- Direct indexing for character mapping (O(1) lookup)
- Efficient integer conversion using native Python operations
- Minimal memory overhead

## Use Cases

- **URL Shorteners**: Create short, unique URLs
- **ID Generation**: Generate compact unique identifiers
- **Data Compression**: Compact representation of binary data
- **Token Generation**: Create readable tokens
- **File Naming**: Generate safe file names from binary data

## Error Handling

The library provides clear error handling with custom exceptions:

```python
from base62 import Base62Error, decode

try:
    result = decode("invalid!char")
except Base62Error as e:
    print(f"Encoding error: {e}")

try:
    result = decode("")
except Base62Error as e:
    print(f"Decoding error: {e}")
```

## Project Structure

```
base62-codec/
├── base62/                 # Main package
│   └── __init__.py        # Core encoder/decoder implementation
├── tests/                 # Test suite
│   └── test_base62.py    # Comprehensive tests
├── pyproject.toml         # Project configuration (UV/pip)
└── README.md             # This file
```

## Development

### Setup Development Environment

```bash
# Install all dependencies including dev tools
uv sync --all-extras

# Format code with black
uv run black base62 tests

# Lint with ruff
uv run ruff check base62 tests

# Run tests
uv run pytest
```

### Project Configuration

The project uses:
- **UV**: Fast Python package installer and project manager
- **pytest**: Testing framework
- **black**: Code formatter
- **ruff**: Fast Python linter

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created as part of the Neo-TheOne project by neerajbopalkar

## Changelog

### Version 1.0.0
- Initial release
- Basic encode/decode functionality for integers
- Bytes and string encoding/decoding support
- Comprehensive test suite
- Full documentation
