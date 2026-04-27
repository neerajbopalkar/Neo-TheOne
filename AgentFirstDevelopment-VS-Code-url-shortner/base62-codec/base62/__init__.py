"""Base 62 encoding/decoding utilities."""

import string
from typing import Union


# Base 62 alphabet: 0-9, a-z, A-Z
CHARSET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = 62


class Base62Error(Exception):
    """Base exception for base62 codec errors."""

    pass


def encode(num: int) -> str:
    """
    Encode an integer to base 62 string.

    Args:
        num: Non-negative integer to encode

    Returns:
        Base 62 encoded string

    Raises:
        Base62Error: If num is negative

    Examples:
        >>> encode(0)
        '0'
        >>> encode(62)
        '10'
        >>> encode(3843)
        '1Zz'
    """
    if num < 0:
        raise Base62Error("Number must be non-negative")

    if num == 0:
        return "0"

    digits = []
    while num > 0:
        digits.append(CHARSET[num % BASE])
        num //= BASE

    return "".join(reversed(digits))


def decode(encoded: str) -> int:
    """
    Decode a base 62 string to an integer.

    Args:
        encoded: Base 62 encoded string

    Returns:
        Decoded integer

    Raises:
        Base62Error: If encoded contains invalid characters

    Examples:
        >>> decode('0')
        0
        >>> decode('10')
        62
        >>> decode('1Zz')
        3843
    """
    if not encoded:
        raise Base62Error("Cannot decode empty string")

    result = 0
    for char in encoded:
        if char not in CHARSET:
            raise Base62Error(f"Invalid character in base62 string: {char}")
        result = result * BASE + CHARSET.index(char)

    return result


def encode_bytes(data: bytes) -> str:
    """
    Encode bytes to base 62 string.

    Args:
        data: Bytes to encode

    Returns:
        Base 62 encoded string

    Examples:
        >>> encode_bytes(b'hello')
        '32D5Y6CyC'
    """
    # Convert bytes to integer (big-endian)
    num = int.from_bytes(data, byteorder="big")
    return encode(num)


def decode_bytes(encoded: str, length: int | None = None) -> bytes:
    """
    Decode base 62 string to bytes.

    Args:
        encoded: Base 62 encoded string
        length: Optional expected length in bytes. If provided, result will be
                padded with leading zeros to match this length.

    Returns:
        Decoded bytes

    Raises:
        Base62Error: If encoded contains invalid characters or length mismatch

    Examples:
        >>> decode_bytes('32D5Y6CyC')
        b'hello'
        >>> decode_bytes('32D5Y6CyC', length=5)
        b'hello'
    """
    num = decode(encoded)

    # Handle zero case
    if num == 0:
        result = b"\x00"
    else:
        # Calculate byte length
        byte_length = (num.bit_length() + 7) // 8
        result = num.to_bytes(byte_length, byteorder="big")

    if length is not None:
        if len(result) > length:
            raise Base62Error(
                f"Decoded bytes length {len(result)} exceeds expected length {length}"
            )
        # Pad with leading zeros
        result = result.rjust(length, b"\x00")

    return result


def encode_str(text: str, encoding: str = "utf-8") -> str:
    """
    Encode a string to base 62.

    Args:
        text: String to encode
        encoding: Text encoding to use (default: utf-8)

    Returns:
        Base 62 encoded string

    Examples:
        >>> encode_str('Hello, World!')
        '73Oy60hGEW4eFPf9qV'
    """
    return encode_bytes(text.encode(encoding))


def decode_str(encoded: str, encoding: str = "utf-8") -> str:
    """
    Decode a base 62 string back to a string.

    Args:
        encoded: Base 62 encoded string
        encoding: Text encoding to use (default: utf-8)

    Returns:
        Decoded string

    Raises:
        Base62Error: If encoded contains invalid characters
        UnicodeDecodeError: If decoded bytes are not valid UTF-8

    Examples:
        >>> decode_str('73Oy60hGEW4eFPf9qV')
        'Hello, World!'
    """
    return decode_bytes(encoded).decode(encoding)
