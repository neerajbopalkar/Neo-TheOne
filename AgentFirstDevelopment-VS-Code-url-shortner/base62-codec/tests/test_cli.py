"""Tests for the CLI module."""

import pytest
import subprocess
import sys
import os
from pathlib import Path


# Get the base62-codec directory
BASE_DIR = Path(__file__).parent.parent


def run_cli(*args):
    """Helper function to run the CLI."""
    cmd = [sys.executable, str(BASE_DIR / "cli.py")] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(BASE_DIR))
    return result


class TestEncodeIntegerCLI:
    """Test CLI integer encoding."""

    def test_encode_integer_basic(self):
        """Test encoding a basic integer via CLI."""
        result = run_cli("encode", "--int", "12345")
        assert result.returncode == 0
        assert result.stdout.strip() == "3d7"

    def test_encode_integer_zero(self):
        """Test encoding zero via CLI."""
        result = run_cli("encode", "--int", "0")
        assert result.returncode == 0
        assert result.stdout.strip() == "0"

    def test_encode_integer_large(self):
        """Test encoding a large integer via CLI."""
        result = run_cli("encode", "--int", "999999999")
        assert result.returncode == 0
        assert result.stdout.strip() == "15FTGf"

    def test_encode_integer_negative_error(self):
        """Test encoding negative integer produces error."""
        result = run_cli("encode", "--int", "-100")
        assert result.returncode != 0
        assert "Error:" in result.stderr


class TestEncodeTextCLI:
    """Test CLI text encoding."""

    def test_encode_text_basic(self):
        """Test encoding basic text via CLI."""
        result = run_cli("encode", "--text", "hello")
        assert result.returncode == 0
        assert result.stdout.strip() == "7TqlfhZ"

    def test_encode_text_with_spaces(self):
        """Test encoding text with spaces."""
        result = run_cli("encode", "--text", "Hello World")
        assert result.returncode == 0
        assert len(result.stdout.strip()) > 0

    def test_encode_text_empty(self):
        """Test encoding empty text."""
        result = run_cli("encode", "--text", "")
        assert result.returncode == 0
        assert result.stdout.strip() == "0"

    def test_encode_text_unicode(self):
        """Test encoding unicode text."""
        result = run_cli("encode", "--text", "你好")
        assert result.returncode == 0
        assert len(result.stdout.strip()) > 0


class TestEncodeBytesCLI:
    """Test CLI bytes encoding."""

    def test_encode_bytes_hex_input(self):
        """Test encoding bytes from hex input."""
        result = run_cli("encode", "--bytes", "48656c6c6f", "--hex")
        assert result.returncode == 0
        assert result.stdout.strip() == "5tp3p3V"

    def test_encode_bytes_text_input(self):
        """Test encoding bytes from text input."""
        result = run_cli("encode", "--bytes", "hello")
        assert result.returncode == 0
        assert result.stdout.strip() == "7TqlfhZ"

    def test_encode_bytes_invalid_hex_error(self):
        """Test encoding invalid hex produces error."""
        result = run_cli("encode", "--bytes", "ZZZZ", "--hex")
        assert result.returncode != 0
        assert "Invalid hex string" in result.stderr


class TestDecodeIntegerCLI:
    """Test CLI integer decoding."""

    def test_decode_to_integer_basic(self):
        """Test decoding to integer via CLI."""
        result = run_cli("decode", "--string", "3d7")
        assert result.returncode == 0
        assert result.stdout.strip() == "12345"

    def test_decode_to_integer_zero(self):
        """Test decoding zero."""
        result = run_cli("decode", "--string", "0")
        assert result.returncode == 0
        assert result.stdout.strip() == "0"

    def test_decode_to_integer_large(self):
        """Test decoding large number."""
        result = run_cli("decode", "--string", "15FTGf")
        assert result.returncode == 0
        assert result.stdout.strip() == "999999999"

    def test_decode_invalid_character_error(self):
        """Test decoding invalid character produces error."""
        result = run_cli("decode", "--string", "!!!invalid!!!")
        assert result.returncode != 0
        assert "Invalid character" in result.stderr


class TestDecodeTextCLI:
    """Test CLI text decoding."""

    def test_decode_to_text_basic(self):
        """Test decoding to text via CLI."""
        result = run_cli("decode", "--string", "7TqlfhZ", "--text")
        assert result.returncode == 0
        assert result.stdout.strip() == "hello"

    def test_decode_to_text_with_spaces(self):
        """Test decoding to text with spaces."""
        # First encode
        result_encode = run_cli("encode", "--text", "Hello World")
        assert result_encode.returncode == 0
        encoded = result_encode.stdout.strip()

        # Now decode it back
        result_decode = run_cli("decode", "--string", encoded, "--text")
        assert result_decode.returncode == 0
        assert result_decode.stdout.strip() == "Hello World"

    def test_decode_to_text_invalid_utf8_error(self):
        """Test decoding invalid UTF-8 produces error."""
        # First encode some raw bytes that are not valid UTF-8
        result_encode = run_cli("encode", "--bytes", "ff", "--hex")
        assert result_encode.returncode == 0
        encoded_bytes = result_encode.stdout.strip()

        # Try to decode as text (should fail for invalid UTF-8)
        result_decode = run_cli("decode", "--string", encoded_bytes, "--text")
        assert result_decode.returncode != 0
        assert "Cannot decode" in result_decode.stderr or "Error:" in result_decode.stderr


class TestDecodeBytesCLI:
    """Test CLI bytes decoding."""

    def test_decode_to_bytes_hex_output(self):
        """Test decoding to bytes with hex output."""
        result = run_cli("decode", "--string", "5tp3p3V", "--bytes", "--hex")
        assert result.returncode == 0
        assert result.stdout.strip() == "48656c6c6f"  # "hello" in hex

    def test_decode_to_bytes_text_output(self):
        """Test decoding to bytes as text."""
        result = run_cli("decode", "--string", "5tp3p3V", "--bytes")
        assert result.returncode == 0
        assert result.stdout.strip() == "Hello"


class TestRoundTripCLI:
    """Test CLI round-trip encoding/decoding."""

    def test_round_trip_integer(self):
        """Test round-trip encoding and decoding integers."""
        original = 543210

        # Encode
        result_encode = run_cli("encode", "--int", str(original))
        assert result_encode.returncode == 0
        encoded = result_encode.stdout.strip()

        # Decode
        result_decode = run_cli("decode", "--string", encoded)
        assert result_decode.returncode == 0
        assert int(result_decode.stdout.strip()) == original

    def test_round_trip_text(self):
        """Test round-trip encoding and decoding text."""
        original = "The quick brown fox"

        # Encode
        result_encode = run_cli("encode", "--text", original)
        assert result_encode.returncode == 0
        encoded = result_encode.stdout.strip()

        # Decode
        result_decode = run_cli("decode", "--string", encoded, "--text")
        assert result_decode.returncode == 0
        assert result_decode.stdout.strip() == original

    def test_round_trip_bytes_hex(self):
        """Test round-trip encoding and decoding bytes (hex format)."""
        original_hex = "deadbeefcafebabe"

        # Encode
        result_encode = run_cli("encode", "--bytes", original_hex, "--hex")
        assert result_encode.returncode == 0
        encoded = result_encode.stdout.strip()

        # Decode
        result_decode = run_cli("decode", "--string", encoded, "--bytes", "--hex")
        assert result_decode.returncode == 0
        assert result_decode.stdout.strip() == original_hex


class TestEncodingOptions:
    """Test CLI encoding options."""

    def test_custom_encoding_utf16(self):
        """Test custom text encoding (UTF-16)."""
        result_encode = run_cli("encode", "--text", "hello", "--encoding", "utf-16")
        assert result_encode.returncode == 0
        encoded = result_encode.stdout.strip()

        # Decode with same encoding
        result_decode = run_cli("decode", "--string", encoded, "--text", "--encoding", "utf-16")
        assert result_decode.returncode == 0
        assert result_decode.stdout.strip() == "hello"


class TestCLIHelp:
    """Test CLI help and error handling."""

    def test_help_command(self):
        """Test help command."""
        result = run_cli("--help")
        assert result.returncode == 0
        assert "Base 62 encoder/decoder" in result.stdout

    def test_encode_help(self):
        """Test encode help."""
        result = run_cli("encode", "--help")
        assert result.returncode == 0
        assert "Integer to encode" in result.stdout

    def test_decode_help(self):
        """Test decode help."""
        result = run_cli("decode", "--help")
        assert result.returncode == 0
        assert "Base62 string to decode" in result.stdout

    def test_no_operation_shows_help(self):
        """Test that no operation shows help."""
        result = run_cli()
        assert result.returncode == 1
        assert "Base 62 encoder/decoder" in result.stdout


class TestErrorHandling:
    """Test error handling."""

    def test_missing_required_argument(self):
        """Test missing required argument."""
        result = run_cli("encode")
        assert result.returncode != 0

    def test_invalid_int_argument(self):
        """Test invalid integer argument."""
        result = run_cli("encode", "--int", "not_a_number")
        assert result.returncode != 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
