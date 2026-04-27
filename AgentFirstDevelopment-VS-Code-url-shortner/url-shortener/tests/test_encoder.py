"""Tests for the URL encoder module."""

import pytest

import sys
from pathlib import Path

src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from url_shortener.encoder import encode_id, decode_id


class TestEncodeId:
    """Tests for the encode_id function."""

    def test_encode_zero(self):
        """Test encoding the number 0."""
        assert encode_id(0) == "0"

    def test_encode_small_number(self):
        """Test encoding a small number."""
        assert encode_id(1) == "1"
        assert encode_id(9) == "9"

    def test_encode_base_boundary(self):
        """Test encoding at base62 boundaries."""
        assert encode_id(61) == "Z"  # Last single-char code (0-9=10, a-z=26, A-Z=26)
        assert encode_id(62) == "10"  # First two-char code

    def test_encode_larger_number(self):
        """Test encoding larger numbers."""
        result = encode_id(1000)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_encode_very_large_number(self):
        """Test encoding very large numbers."""
        result = encode_id(1000000)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_encode_negative_raises_error(self):
        """Test that negative numbers raise ValueError."""
        with pytest.raises(ValueError):
            encode_id(-1)


class TestDecodeId:
    """Tests for the decode_id function."""

    def test_decode_zero(self):
        """Test decoding '0'."""
        assert decode_id("0") == 0

    def test_decode_single_digit(self):
        """Test decoding single-digit codes."""
        assert decode_id("1") == 1
        assert decode_id("9") == 9

    def test_decode_base_boundary(self):
        """Test decoding at base62 boundaries."""
        assert decode_id("Z") == 61
        assert decode_id("10") == 62

    def test_decode_larger_code(self):
        """Test decoding larger codes."""
        result = decode_id("zzz")
        assert isinstance(result, int)
        assert result > 0

    def test_decode_invalid_character_raises_error(self):
        """Test that invalid characters raise ValueError."""
        with pytest.raises(ValueError):
            decode_id("!")

        with pytest.raises(ValueError):
            decode_id("@")

        with pytest.raises(ValueError):
            decode_id("_")


class TestEncodeDecode:
    """Tests for encoding and decoding round-trips."""

    @pytest.mark.parametrize(
        "num",
        [0, 1, 10, 61, 62, 100, 1000, 10000, 100000, 1000000],
    )
    def test_encode_decode_round_trip(self, num):
        """Test that encoding then decoding returns the original number."""
        encoded = encode_id(num)
        decoded = decode_id(encoded)
        assert decoded == num

    def test_consistent_encoding(self):
        """Test that the same number always produces the same encoding."""
        num = 12345
        encoded1 = encode_id(num)
        encoded2 = encode_id(num)
        assert encoded1 == encoded2

    def test_different_numbers_different_codes(self):
        """Test that different numbers produce different codes."""
        code1 = encode_id(1)
        code2 = encode_id(2)
        assert code1 != code2
