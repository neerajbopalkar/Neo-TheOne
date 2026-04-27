#!/usr/bin/env python3
"""
Example usage of the base62 codec library.

This script demonstrates various ways to use the base62 encoder/decoder.
"""

from base62 import (
    encode,
    decode,
    encode_bytes,
    decode_bytes,
    encode_str,
    decode_str,
)


def example_integers():
    """Demonstrate integer encoding/decoding."""
    print("=" * 60)
    print("INTEGER ENCODING/DECODING")
    print("=" * 60)

    numbers = [0, 1, 10, 61, 62, 100, 3843, 1000000, 999999999]

    for num in numbers:
        encoded = encode(num)
        decoded = decode(encoded)
        print(f"{num:>12} → {encoded:>10} → {decoded:>12}")
        assert decoded == num, "Round trip failed!"

    print()


def example_bytes():
    """Demonstrate bytes encoding/decoding."""
    print("=" * 60)
    print("BYTES ENCODING/DECODING")
    print("=" * 60)

    byte_data = [
        b"hello",
        b"world",
        b"base62",
        b"The quick brown fox",
        b"\x00\x01\x02\x03",
    ]

    for data in byte_data:
        encoded = encode_bytes(data)
        decoded = decode_bytes(encoded)
        print(f"{str(data):30} → {encoded:20}")
        assert decoded == data, "Round trip failed!"

    print()


def example_strings():
    """Demonstrate string encoding/decoding."""
    print("=" * 60)
    print("STRING ENCODING/DECODING")
    print("=" * 60)

    strings = [
        "Hello, World!",
        "base62 codec",
        "123!@#$%^&*()",
        "你好世界",
        "🌍 Unicode test 🚀",
    ]

    for text in strings:
        encoded = encode_str(text)
        decoded = decode_str(encoded)
        print(f"{text:30} → {encoded:30}")
        assert decoded == text, "Round trip failed!"

    print()


def example_url_shortener():
    """Demonstrate URL shortener use case."""
    print("=" * 60)
    print("URL SHORTENER USE CASE")
    print("=" * 60)
    print("Generate short codes from numeric IDs:\n")

    base_url = "https://example.com/"
    ids = [1, 100, 10000, 1000000]

    for id_num in ids:
        short_code = encode(id_num)
        short_url = base_url + short_code
        print(f"ID {id_num:>10} → {short_url}")

    print()


def example_id_generation():
    """Demonstrate ID generation use case."""
    print("=" * 60)
    print("ID GENERATION USE CASE")
    print("=" * 60)
    print("Generate compact IDs from binary data:\n")

    # Simulate some binary data (e.g., from UUID or hash)
    binary_data = [
        b"\x00\x00\x00\x01",
        b"\xff\xfe\xfd\xfc",
        b"user_12345",
    ]

    for data in binary_data:
        compact_id = encode_bytes(data)
        print(f"Binary: {data!r:30} → ID: {compact_id}")

    print()


def example_error_handling():
    """Demonstrate error handling."""
    print("=" * 60)
    print("ERROR HANDLING")
    print("=" * 60)

    from base62 import Base62Error

    # Invalid character
    try:
        decode("invalid!char")
    except Base62Error as e:
        print(f"✓ Caught invalid character error: {e}")

    # Empty string
    try:
        decode("")
    except Base62Error as e:
        print(f"✓ Caught empty string error: {e}")

    # Negative number
    try:
        encode(-5)
    except Base62Error as e:
        print(f"✓ Caught negative number error: {e}")

    print()


def example_performance():
    """Demonstrate performance with large numbers."""
    print("=" * 60)
    print("PERFORMANCE TEST")
    print("=" * 60)

    large_numbers = [
        62**5,
        62**10,
        62**15,
        12345678901234567890,
    ]

    for num in large_numbers:
        encoded = encode(num)
        decoded = decode(encoded)
        print(f"Number: {num}")
        print(f"  Encoded ({len(encoded):2} chars): {encoded}")
        print(f"  Round trip: {'✓ OK' if decoded == num else '✗ FAIL'}")
        print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("BASE62 CODEC - USAGE EXAMPLES")
    print("=" * 60 + "\n")

    example_integers()
    example_bytes()
    example_strings()
    example_url_shortener()
    example_id_generation()
    example_error_handling()
    example_performance()

    print("=" * 60)
    print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()
