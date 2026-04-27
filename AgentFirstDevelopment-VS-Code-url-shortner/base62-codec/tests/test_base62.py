"""Tests for the base62 codec module."""

import pytest
from base62 import (
    encode,
    decode,
    encode_bytes,
    decode_bytes,
    encode_str,
    decode_str,
    Base62Error,
)


class TestBasicEncoding:
    """Test basic integer encoding."""

    def test_encode_zero(self):
        """Test encoding zero."""
        assert encode(0) == "0"

    def test_encode_single_digit(self):
        """Test encoding single digit numbers."""
        assert encode(1) == "1"
        assert encode(9) == "9"
        assert encode(10) == "a"
        assert encode(35) == "z"
        assert encode(36) == "A"
        assert encode(61) == "Z"

    def test_encode_base_value(self):
        """Test encoding exactly the base value."""
        assert encode(62) == "10"
        assert encode(124) == "20"

    def test_encode_large_numbers(self):
        """Test encoding large numbers."""
        assert encode(3843) == "1Zz"
        assert encode(1000000) == "4c92"
        assert encode(999999999) == "15FTGg"

    def test_encode_negative_raises_error(self):
        """Test that encoding negative numbers raises an error."""
        with pytest.raises(Base62Error):
            encode(-1)
        with pytest.raises(Base62Error):
            encode(-100)


class TestBasicDecoding:
    """Test basic string decoding."""

    def test_decode_zero(self):
        """Test decoding zero."""
        assert decode("0") == 0

    def test_decode_single_digit(self):
        """Test decoding single digit strings."""
        assert decode("1") == 1
        assert decode("9") == 9
        assert decode("a") == 10
        assert decode("z") == 35
        assert decode("A") == 36
        assert decode("Z") == 61

    def test_decode_base_value(self):
        """Test decoding base value."""
        assert decode("10") == 62
        assert decode("20") == 124

    def test_decode_large_strings(self):
        """Test decoding large base62 strings."""
        assert decode("1Zz") == 3843
        assert decode("4c92") == 1000000
        assert decode("15FTGg") == 999999999

    def test_decode_invalid_character_raises_error(self):
        """Test that invalid characters raise an error."""
        with pytest.raises(Base62Error):
            decode("!")
        with pytest.raises(Base62Error):
            decode("abc!")
        with pytest.raises(Base62Error):
            decode("_")

    def test_decode_empty_string_raises_error(self):
        """Test that empty string raises an error."""
        with pytest.raises(Base62Error):
            decode("")


class TestRoundTrip:
    """Test encode/decode round trips."""

    def test_round_trip_small_numbers(self):
        """Test round trip for small numbers."""
        for i in range(1000):
            encoded = encode(i)
            decoded = decode(encoded)
            assert decoded == i

    def test_round_trip_large_numbers(self):
        """Test round trip for large numbers."""
        test_numbers = [
            62,
            62**2,
            62**3,
            62**4,
            1000000,
            999999999,
            12345678901234567890,
        ]
        for num in test_numbers:
            encoded = encode(num)
            decoded = decode(encoded)
            assert decoded == num


class TestBytesEncoding:
    """Test bytes encoding/decoding."""

    def test_encode_bytes_simple(self):
        """Test encoding simple byte strings."""
        result = encode_bytes(b"hello")
        assert isinstance(result, str)
        assert all(c in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in result)

    def test_decode_bytes_round_trip(self):
        """Test round trip for bytes."""
        test_data = [
            b"hello",
            b"world",
            b"base62",
            b"",
            b"\x00",
            b"\x00\x00",
            b"\xff\xfe\xfd",
            b"The quick brown fox",
        ]
        for data in test_data:
            encoded = encode_bytes(data)
            decoded = decode_bytes(encoded)
            assert decoded == data

    def test_decode_bytes_with_length(self):
        """Test decoding bytes with specified length."""
        encoded = encode_bytes(b"hi")
        decoded = decode_bytes(encoded, length=5)
        assert decoded == b"\x00\x00\x00hi"

    def test_decode_bytes_length_mismatch(self):
        """Test that length mismatch raises error."""
        encoded = encode_bytes(b"hello world")  # 11 bytes
        with pytest.raises(Base62Error):
            decode_bytes(encoded, length=5)


class TestStringEncoding:
    """Test string encoding/decoding."""

    def test_encode_str_simple(self):
        """Test encoding simple strings."""
        result = encode_str("Hello, World!")
        assert isinstance(result, str)

    def test_decode_str_round_trip(self):
        """Test round trip for strings."""
        test_strings = [
            "Hello, World!",
            "base62 codec",
            "123!@#$%^&*()",
            "Unicode: 你好世界 🌍",
            "Empty next:\n",
            "",
            "a",
            " ",
        ]
        for text in test_strings:
            encoded = encode_str(text)
            decoded = decode_str(encoded)
            assert decoded == text

    def test_encode_decode_str_different_encodings(self):
        """Test with different string encodings."""
        text = "Hello, 世界"
        
        # UTF-8 (default)
        encoded_utf8 = encode_str(text, encoding="utf-8")
        decoded_utf8 = decode_str(encoded_utf8, encoding="utf-8")
        assert decoded_utf8 == text

    def test_decode_str_invalid_utf8_raises_error(self):
        """Test that invalid UTF-8 raises an error."""
        # Encode raw bytes that aren't valid UTF-8
        invalid_bytes = b"\xff\xfe"
        encoded = encode_bytes(invalid_bytes)
        
        with pytest.raises(UnicodeDecodeError):
            decode_str(encoded)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_zero_values(self):
        """Test handling of zero values."""
        assert encode(0) == "0"
        assert decode("0") == 0
        assert decode_bytes("0") == b""  # decode treats encoded 0 as empty after conversion

    def test_very_large_numbers(self):
        """Test with very large numbers."""
        large_num = 62**10
        encoded = encode(large_num)
        decoded = decode(encoded)
        assert decoded == large_num

    def test_all_charset_characters(self):
        """Test that all characters in charset are handled correctly."""
        charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, char in enumerate(charset):
            assert encode(i) == char
            assert decode(char) == i

    def test_bytes_with_null_bytes(self):
        """Test handling bytes with null characters."""
        data = b"\x00\x00\x01"
        encoded = encode_bytes(data)
        decoded = decode_bytes(encoded)
        assert decoded == data

    def test_long_string_encoding(self):
        """Test encoding very long strings."""
        long_string = "a" * 10000
        encoded = encode_str(long_string)
        decoded = decode_str(encoded)
        assert decoded == long_string


class TestConsistency:
    """Test consistency between different encoding methods."""

    def test_bytes_and_str_consistency(self):
        """Test that string encoding is consistent with bytes encoding."""
        text = "Hello, World!"
        
        # Method 1: encode_str
        encoded1 = encode_str(text)
        
        # Method 2: encode_bytes + text.encode()
        encoded2 = encode_bytes(text.encode("utf-8"))
        
        assert encoded1 == encoded2

    def test_different_representations_same_result(self):
        """Test that different input representations give same output."""
        num = 12345
        bytes_data = num.to_bytes(2, byteorder="big")
        
        encoded_int = encode(num)
        encoded_bytes = encode_bytes(bytes_data)
        
        # Both should decode to the same integer representation
        assert decode(encoded_int) == num
        assert decode(encoded_bytes) == num
