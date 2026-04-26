# Base62 CLI Examples

## Basic Usage

### Encode Integers

```bash
# Simple integers
python cli.py encode --int 0
python cli.py encode --int 100
python cli.py encode --int 12345
python cli.py encode --int 999999999

# Large numbers
python cli.py encode --int 68719476735  # 2^36 - 1
```

### Decode Base62 Strings

```bash
# Decode back to integers
python cli.py decode --string 0
python cli.py decode --string 2s
python cli.py decode --string 3d7
python cli.py decode --string 15FTGf

# Decode large numbers
python cli.py decode --string 2ZqUy
```

### Text Encoding

```bash
# Encode text to base62
python cli.py encode --text "hello"
python cli.py encode --text "Hello, World!"
python cli.py encode --text "Python 3.14"
python cli.py encode --text "Base62 Encoder/Decoder"

# Encode special characters
python cli.py encode --text "user@example.com"
python cli.py encode --text "path/to/file.txt"

# Encode multi-line text
python cli.py encode --text "Line 1
Line 2
Line 3"
```

### Text Decoding

```bash
# Decode base62 back to text
python cli.py decode --string 7TqlfhZ --text
python cli.py decode --string 1zoJoYqbdF4XG7aAmx --text
python cli.py decode --string 3d7YsXTTLhHeVU0h --text

# Decode to original text
python cli.py decode --string 37VH9kK1 --text
```

### Binary Data (Hex Format)

```bash
# Encode hex data
python cli.py encode --bytes "48656c6c6f" --hex  # "hello" in hex
python cli.py encode --bytes "deadbeef" --hex
python cli.py encode --bytes "cafebabe" --hex

# Encode binary as text
python cli.py encode --bytes "hello"
python cli.py encode --bytes "world"

# Decode to hex
python cli.py decode --string 5tp3p3V --bytes --hex
python cli.py decode --string 2c9w9CRJ --bytes --hex

# Decode to text
python cli.py decode --string 5tp3p3V --bytes
```

### Custom Text Encodings

```bash
# UTF-16 encoding
python cli.py encode --text "hello" --encoding utf-16
python cli.py decode --string <result> --text --encoding utf-16

# UTF-32 encoding
python cli.py encode --text "hello" --encoding utf-32
python cli.py decode --string <result> --text --encoding utf-32

# Latin-1 encoding
python cli.py encode --text "café" --encoding latin-1
python cli.py decode --string <result> --text --encoding latin-1
```

### Unicode Text

```bash
# Chinese characters
python cli.py encode --text "你好世界"
python cli.py decode --string <result> --text

# Emoji
python cli.py encode --text "🚀 Hello 🌍"
python cli.py decode --string <result> --text

# Mixed scripts
python cli.py encode --text "Hello مرحبا שלום"
python cli.py decode --string <result> --text
```

## Practical Use Cases

### URL Shortening Simulation

```bash
# Encode a URL (without the protocol)
python cli.py encode --text "github.com/neerajbopalkar/Neo-TheOne"

# Use the result as a short code
```

### Session Token Generation

```bash
# Encode timestamp + identifier
python cli.py encode --int 1682073600  # Unix timestamp
python cli.py encode --int 1682073600000  # Milliseconds
```

### Checksum/Hash Simulation

```bash
# Encode binary data from API response
python cli.py encode --bytes "d41d8cd98f00b204e9800998ecf8427e" --hex

# Create short reference
```

### File Naming

```bash
# Create unique file names from content
python cli.py encode --text "document_2026_04_26"
python cli.py encode --text "backup_database.sql"
```

### API Response Encoding

```bash
# Encode JSON response
python cli.py encode --text '{"user":"john","id":12345}'
```

## Piping and Chaining

### Encode and then Decode (Round-trip)

```bash
# On Windows PowerShell:
$encoded = $(python cli.py encode --int 54321)
python cli.py decode --string $encoded

# Encode text and decode it back
$encoded = $(python cli.py encode --text "Hello World")
python cli.py decode --string $encoded --text
```

### Batch Operations

```bash
# Create a batch of encodings
@("hello", "world", "base62", "encoder") | ForEach-Object {
    python cli.py encode --text $_
}

# Or decode multiple values
@("7TqlfhZ", "2VVsQXV", "37VH9kK1", "37VH3fGgG") | ForEach-Object {
    python cli.py decode --string $_ --text
}
```

## Help and Information

```bash
# General help
python cli.py --help

# Encode subcommand help
python cli.py encode --help

# Decode subcommand help
python cli.py decode --help
```

## Error Handling Examples

```bash
# Negative number (should fail)
python cli.py encode --int -100

# Invalid hex string (should fail)
python cli.py encode --bytes "ZZZZ" --hex

# Invalid base62 character (should fail)
python cli.py decode --string "!!!invalid!!!"

# Missing required argument (should fail)
python cli.py encode

# Decode invalid UTF-8 (should fail)
python cli.py decode --string <binary_encoded> --text
```

## Performance Testing

```bash
# Encode very large integer
python cli.py encode --int 18446744073709551615  # Max uint64

# Encode long text
python cli.py encode --text "The quick brown fox jumps over the lazy dog. " * 100

# Encode large binary data (1MB hex)
python cli.py encode --bytes ("00" * 1000000) --hex
```

## Real-World Examples

### Example 1: User ID Shortener

```bash
# User has ID 987654321
python cli.py encode --int 987654321
# Output: aD5xqp

# Later decode it back
python cli.py decode --string aD5xqp
# Output: 987654321
```

### Example 2: Database Record Reference

```bash
# Encode record timestamp
python cli.py encode --text "user:2026-04-26:12:30:45"

# Use as unique reference code
```

### Example 3: Hex Data Conversion

```bash
# Convert hex color code to base62
python cli.py encode --bytes "FF5733" --hex

# Share shorter code instead of hex
```

### Example 4: Unicode Slug Generation

```bash
# Create URL-safe slug from text
python cli.py encode --text "my-awesome-article"

# Use in URLs
```

## Quick Start Script

Save this as `test_cli.ps1` and run with `powershell -ExecutionPolicy Bypass -File test_cli.ps1`:

```powershell
# Test basic encoding/decoding
Write-Host "=== Encoding Integer ===" -ForegroundColor Green
python cli.py encode --int 12345

Write-Host "`n=== Decoding ===" -ForegroundColor Green
python cli.py decode --string 3d7

Write-Host "`n=== Encoding Text ===" -ForegroundColor Green
python cli.py encode --text "hello"

Write-Host "`n=== Decoding Text ===" -ForegroundColor Green
python cli.py decode --string 7TqlfhZ --text

Write-Host "`n=== Encoding Hex ===" -ForegroundColor Green
python cli.py encode --bytes "48656c6c6f" --hex

Write-Host "`n=== Round-trip Test ===" -ForegroundColor Green
$encoded = $(python cli.py encode --text "Round Trip Test")
Write-Host "Encoded: $encoded"
$decoded = $(python cli.py decode --string $encoded --text)
Write-Host "Decoded: $decoded"

Write-Host "`n=== All Tests Completed ===" -ForegroundColor Cyan
```

## Tips and Tricks

1. **URL-Safe Encoding**: Base62 is naturally URL-safe (no special characters)
2. **Bidirectional**: Always can convert back to original format
3. **Reversible**: Use `encode` then `decode` to verify roundtrips
4. **Custom Encoding**: Change text encoding for different character sets
5. **Hex Support**: Handle binary data by converting to/from hex format
