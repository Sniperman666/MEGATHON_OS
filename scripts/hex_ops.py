#!/usr/bin/env python3
import argparse
import binascii
import pathlib
import sys


def read_bytes(path: pathlib.Path) -> bytes:
    return path.read_bytes()


def write_bytes(path: pathlib.Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def encode_file(input_path: pathlib.Path, output_path: pathlib.Path, uppercase: bool) -> None:
    source = read_bytes(input_path)
    hex_text = binascii.hexlify(source).decode("ascii")
    if uppercase:
        hex_text = hex_text.upper()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(hex_text, encoding="utf-8")


def decode_file(input_path: pathlib.Path, output_path: pathlib.Path) -> None:
    raw = input_path.read_text(encoding="utf-8")
    compact = "".join(raw.split())
    try:
        decoded = bytes.fromhex(compact)
    except ValueError as error:
        raise ValueError(f"invalid hex input in {input_path}: {error}") from error
    write_bytes(output_path, decoded)


def xor_file(input_path: pathlib.Path, output_path: pathlib.Path, key_hex: str) -> None:
    source = read_bytes(input_path)
    key_compact = "".join(key_hex.split())
    try:
        key_bytes = bytes.fromhex(key_compact)
    except ValueError as error:
        raise ValueError(f"invalid key hex: {error}") from error
    if not key_bytes:
        raise ValueError("key cannot be empty")

    result = bytes(value ^ key_bytes[index % len(key_bytes)] for index, value in enumerate(source))
    write_bytes(output_path, result)


def main() -> int:
    parser = argparse.ArgumentParser(description="Hex operations utility for files")
    subparsers = parser.add_subparsers(dest="command", required=True)

    encode_parser = subparsers.add_parser("encode", help="convert binary file to hex text")
    encode_parser.add_argument("input", type=pathlib.Path)
    encode_parser.add_argument("output", type=pathlib.Path)
    encode_parser.add_argument("--uppercase", action="store_true", help="emit uppercase hex")

    decode_parser = subparsers.add_parser("decode", help="convert hex text file to binary")
    decode_parser.add_argument("input", type=pathlib.Path)
    decode_parser.add_argument("output", type=pathlib.Path)

    xor_parser = subparsers.add_parser("xor", help="XOR file bytes with repeating hex key")
    xor_parser.add_argument("input", type=pathlib.Path)
    xor_parser.add_argument("output", type=pathlib.Path)
    xor_parser.add_argument("key", help="hex key, for example deadbeef")

    args = parser.parse_args()

    try:
        if args.command == "encode":
            encode_file(args.input, args.output, args.uppercase)
        elif args.command == "decode":
            decode_file(args.input, args.output)
        elif args.command == "xor":
            xor_file(args.input, args.output, args.key)
        else:
            parser.print_help()
            return 1
    except (OSError, ValueError) as error:
        print(f"hex_ops error: {error}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
