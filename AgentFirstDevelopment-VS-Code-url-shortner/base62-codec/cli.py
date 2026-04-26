#!/usr/bin/env python3
"""Command-line interface for base62 encoder/decoder."""

import argparse
import sys
from base62 import encode, decode, encode_bytes, decode_bytes, encode_str, decode_str, Base62Error


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Base 62 encoder/decoder utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Encode an integer
  %(prog)s encode --int 12345
  
  # Decode a base62 string
  %(prog)s decode --string 3D7
  
  # Encode text
  %(prog)s encode --text "Hello, World!"
  
  # Decode text
  %(prog)s decode --text 1zoJoYqbdF4XG7aAmx
  
  # Encode binary data from hex
  %(prog)s encode --bytes "48656c6c6f" --hex
  
  # Decode to binary data (output as hex)
  %(prog)s decode --string 32D5Y6CyC --bytes --hex
        """,
    )

    subparsers = parser.add_subparsers(dest="operation", help="Operation to perform")

    # Encode subcommand
    encode_parser = subparsers.add_parser("encode", help="Encode data to base62")
    encode_group = encode_parser.add_mutually_exclusive_group(required=True)
    encode_group.add_argument(
        "--int",
        type=int,
        metavar="NUM",
        help="Integer to encode",
    )
    encode_group.add_argument(
        "--text",
        type=str,
        metavar="TEXT",
        help="Text to encode",
    )
    encode_group.add_argument(
        "--bytes",
        type=str,
        metavar="DATA",
        help="Hex string or binary data to encode",
    )
    encode_parser.add_argument(
        "--encoding",
        default="utf-8",
        metavar="ENC",
        help="Text encoding (default: utf-8)",
    )
    encode_parser.add_argument(
        "--hex",
        action="store_true",
        help="Input/output hex format for bytes",
    )

    # Decode subcommand
    decode_parser = subparsers.add_parser("decode", help="Decode data from base62")
    decode_group = decode_parser.add_mutually_exclusive_group(required=True)
    decode_group.add_argument(
        "--string",
        type=str,
        metavar="STR",
        help="Base62 string to decode",
    )
    decode_parser.add_argument(
        "--bytes",
        action="store_true",
        help="Output as bytes instead of integer",
    )
    decode_parser.add_argument(
        "--text",
        action="store_true",
        help="Output as text instead of integer",
    )
    decode_parser.add_argument(
        "--encoding",
        default="utf-8",
        metavar="ENC",
        help="Text encoding (default: utf-8)",
    )
    decode_parser.add_argument(
        "--hex",
        action="store_true",
        help="Output bytes as hex",
    )

    args = parser.parse_args()

    if not args.operation:
        parser.print_help()
        sys.exit(1)

    try:
        if args.operation == "encode":
            handle_encode(args)
        elif args.operation == "decode":
            handle_decode(args)
    except Base62Error as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_encode(args):
    """Handle encode operation."""
    if args.int is not None:
        result = encode(args.int)
        print(result)
    elif args.text is not None:
        result = encode_str(args.text, encoding=args.encoding)
        print(result)
    elif args.bytes is not None:
        # Handle hex input if --hex flag is set
        if args.hex:
            try:
                data = bytes.fromhex(args.bytes)
            except ValueError as e:
                raise Base62Error(f"Invalid hex string: {e}")
        else:
            # Treat as UTF-8 encoded text
            data = args.bytes.encode(args.encoding)
        
        result = encode_bytes(data)
        print(result)


def handle_decode(args):
    """Handle decode operation."""
    base62_str = args.string
    
    if args.text:
        # Decode to text
        try:
            result = decode_str(base62_str, encoding=args.encoding)
            print(result)
        except UnicodeDecodeError:
            raise Base62Error(f"Cannot decode as {args.encoding}. Decoded bytes are not valid {args.encoding}.")
    elif args.bytes:
        # Decode to bytes
        decoded_bytes = decode_bytes(base62_str)
        if args.hex:
            # Output as hex
            print(decoded_bytes.hex())
        else:
            # Output as UTF-8 text (if possible)
            try:
                print(decoded_bytes.decode(args.encoding))
            except UnicodeDecodeError:
                print(f"Cannot decode bytes as {args.encoding}. Use --hex for hex output.")
                sys.exit(1)
    else:
        # Decode to integer (default)
        result = decode(base62_str)
        print(result)


if __name__ == "__main__":
    main()
