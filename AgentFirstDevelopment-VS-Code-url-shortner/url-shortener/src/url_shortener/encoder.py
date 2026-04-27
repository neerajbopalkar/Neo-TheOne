"""URL encoding/decoding logic using base62."""


def encode_id(num: int) -> str:
    """
    Encode a numeric ID to a base62 string.

    Base62 uses 0-9, a-z, A-Z (62 characters total).
    This creates shorter, alphanumeric codes suitable for URLs.

    Args:
        num: Positive integer to encode

    Returns:
        Base62 encoded string
    """
    if num == 0:
        return "0"

    if num < 0:
        raise ValueError("Only non-negative integers can be encoded")

    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []

    while num > 0:
        result.append(alphabet[num % 62])
        num //= 62

    return "".join(reversed(result))


def decode_id(code: str) -> int:
    """
    Decode a base62 string back to its numeric ID.

    Args:
        code: Base62 encoded string

    Returns:
        Decoded numeric ID

    Raises:
        ValueError: If code contains invalid characters
    """
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = 0

    for char in code:
        if char not in alphabet:
            raise ValueError(f"Invalid character in code: {char}")
        result = result * 62 + alphabet.index(char)

    return result
