#!/usr/bin/env python3
import argparse
import binascii
import json
import os
import pathlib
import sys


ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_SETTINGS_PATH = ROOT_DIR / "scripts" / "hex_settings.json"
DEFAULT_SETTINGS = {
    "dev": {
        "dry_run": False,
        "verbose": False,
        "allow_overwrite": False,
        "default_uppercase": False,
        "default_xor_key": "",
        "access_token": "CHANGE_ME",
    }
}


def read_bytes(path: pathlib.Path) -> bytes:
    return path.read_bytes()


def write_bytes(path: pathlib.Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def load_settings(path: pathlib.Path) -> dict:
    if not path.exists():
        return json.loads(json.dumps(DEFAULT_SETTINGS))
    raw = path.read_text(encoding="utf-8")
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("settings file must contain a JSON object")

    merged = json.loads(json.dumps(DEFAULT_SETTINGS))
    for key, value in parsed.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key].update(value)
        else:
            merged[key] = value
    return merged


def save_settings(path: pathlib.Path, settings: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(settings, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_output_path(output_path: pathlib.Path, allow_overwrite: bool) -> None:
    if output_path.exists() and not allow_overwrite:
        raise ValueError(
            f"output exists: {output_path}. Use --force or set dev.allow_overwrite=true in settings"
        )


def log_enabled(verbose: bool, message: str) -> None:
    if verbose:
        print(message)


def check_dev_access(settings: dict, provided_token: str | None, allow_read: bool) -> None:
    dev = settings.get("dev", {}) if isinstance(settings.get("dev", {}), dict) else {}
    expected = str(dev.get("access_token", "")).strip()
    if not expected:
        return
    if expected == "CHANGE_ME":
        raise ValueError(
            "dev access token not initialized. Set a real token with settings-write dev.access_token \"<token>\""
        )
    if provided_token != expected:
        target = "read" if allow_read else "write"
        raise ValueError(
            f"dev settings {target} denied. Provide --token or HEX_OPS_TOKEN with the configured access token"
        )


def encode_file(
    input_path: pathlib.Path,
    output_path: pathlib.Path,
    uppercase: bool,
    allow_overwrite: bool,
    dry_run: bool,
    verbose: bool,
) -> None:
    source = read_bytes(input_path)
    hex_text = binascii.hexlify(source).decode("ascii")
    if uppercase:
        hex_text = hex_text.upper()
    validate_output_path(output_path, allow_overwrite)
    if dry_run:
        log_enabled(verbose, f"[dry-run] encode {input_path} -> {output_path}")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(hex_text, encoding="utf-8")
    log_enabled(verbose, f"encoded {input_path} -> {output_path}")


def decode_file(
    input_path: pathlib.Path,
    output_path: pathlib.Path,
    allow_overwrite: bool,
    dry_run: bool,
    verbose: bool,
) -> None:
    raw = input_path.read_text(encoding="utf-8")
    compact = "".join(raw.split())
    try:
        decoded = bytes.fromhex(compact)
    except ValueError as error:
        raise ValueError(f"invalid hex input in {input_path}: {error}") from error
    validate_output_path(output_path, allow_overwrite)
    if dry_run:
        log_enabled(verbose, f"[dry-run] decode {input_path} -> {output_path}")
        return
    write_bytes(output_path, decoded)
    log_enabled(verbose, f"decoded {input_path} -> {output_path}")


def xor_file(
    input_path: pathlib.Path,
    output_path: pathlib.Path,
    key_hex: str,
    allow_overwrite: bool,
    dry_run: bool,
    verbose: bool,
) -> None:
    source = read_bytes(input_path)
    key_compact = "".join(key_hex.split())
    try:
        key_bytes = bytes.fromhex(key_compact)
    except ValueError as error:
        raise ValueError(f"invalid key hex: {error}") from error
    if not key_bytes:
        raise ValueError("key cannot be empty")

    result = bytes(value ^ key_bytes[index % len(key_bytes)] for index, value in enumerate(source))
    validate_output_path(output_path, allow_overwrite)
    if dry_run:
        log_enabled(verbose, f"[dry-run] xor {input_path} -> {output_path}")
        return
    write_bytes(output_path, result)
    log_enabled(verbose, f"xor complete {input_path} -> {output_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Hex operations utility for files")
    parser.add_argument(
        "--settings",
        type=pathlib.Path,
        default=DEFAULT_SETTINGS_PATH,
        help=f"settings JSON path (default: {DEFAULT_SETTINGS_PATH})",
    )
    parser.add_argument("--verbose", action="store_true", help="enable verbose output")
    parser.add_argument("--dry-run", action="store_true", help="show actions without writing files")
    parser.add_argument("--force", action="store_true", help="allow overwriting existing output files")
    parser.add_argument("--token", help="access token for dev settings read/write")
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
    xor_parser.add_argument("key", nargs="?", help="hex key, for example deadbeef")

    settings_read_parser = subparsers.add_parser("settings-read", help="print current settings JSON")
    settings_read_parser.add_argument("--json", action="store_true", help="print compact JSON")
    settings_read_parser.add_argument("--token", dest="token_local", help="access token")

    settings_write_parser = subparsers.add_parser("settings-write", help="write one settings value")
    settings_write_parser.add_argument("key", help="dot key path, for example dev.verbose")
    settings_write_parser.add_argument("value", help="JSON value, for example true or \"beef\"")
    settings_write_parser.add_argument("--token", dest="token_local", help="access token")

    args = parser.parse_args()

    try:
        settings = load_settings(args.settings)
        dev = settings.get("dev", {}) if isinstance(settings.get("dev", {}), dict) else {}
        provided_token = args.token or getattr(args, "token_local", None) or os.environ.get("HEX_OPS_TOKEN")
        verbose = bool(args.verbose or dev.get("verbose", False))
        dry_run = bool(args.dry_run or dev.get("dry_run", False))
        allow_overwrite = bool(args.force or dev.get("allow_overwrite", False))

        if args.command == "encode":
            uppercase = bool(args.uppercase or dev.get("default_uppercase", False))
            encode_file(args.input, args.output, uppercase, allow_overwrite, dry_run, verbose)
        elif args.command == "decode":
            decode_file(args.input, args.output, allow_overwrite, dry_run, verbose)
        elif args.command == "xor":
            key = args.key if args.key is not None else str(dev.get("default_xor_key", ""))
            xor_file(args.input, args.output, key, allow_overwrite, dry_run, verbose)
        elif args.command == "settings-read":
            check_dev_access(settings, provided_token, allow_read=True)
            if args.json:
                print(json.dumps(settings, separators=(",", ":")))
            else:
                print(json.dumps(settings, indent=2, sort_keys=True))
        elif args.command == "settings-write":
            value = json.loads(args.value)
            keys = args.key.split(".")
            if not all(keys):
                raise ValueError("invalid key path")

            expected = str(dev.get("access_token", "")).strip()
            allow_bootstrap = expected == "CHANGE_ME" and args.key == "dev.access_token"
            if not allow_bootstrap:
                check_dev_access(settings, provided_token, allow_read=False)

            target = settings
            for segment in keys[:-1]:
                child = target.get(segment)
                if not isinstance(child, dict):
                    child = {}
                    target[segment] = child
                target = child
            target[keys[-1]] = value
            save_settings(args.settings, settings)
            log_enabled(verbose or True, f"saved {args.key} in {args.settings}")
        else:
            parser.print_help()
            return 1
    except (OSError, ValueError) as error:
        print(f"hex_ops error: {error}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
