# MEGATHON

Fork: ARCHITECTURE

Static documentation site for MEGATHON guidance pages.

## Overview

This repository contains prebuilt HTML pages and assets used for public docs and troubleshooting guides.

## Project Structure

- `index.html` is the landing page.
- `*.html` files at the repo root are standalone documentation pages.
- `assets/` contains shared images, styling, and supporting static content.

## Local Development

No build step is required for basic edits.

1. Start a local static server from the repository root:

   ```bash
   python3 -m http.server 8000
   ```

2. Open `http://localhost:8000` in your browser.
3. Edit HTML/assets and refresh to validate changes.

## Python Hex Operations

Hex operations are available through `scripts/hex_ops.py`.

- Encode binary file to hex text:
  ```bash
  npm run hex -- encode input.bin output.hex
  ```
- Decode hex text back to binary:
  ```bash
  npm run hex -- decode output.hex restored.bin
  ```
- Apply repeating XOR using a hex key:
  ```bash
  npm run hex -- xor input.bin output.bin deadbeef
  ```

### Dev Options

- `--dry-run` previews operations without writing files.
- `--verbose` prints operation logs.
- `--force` allows overwriting existing outputs.
- `--settings <path>` loads settings from a custom JSON file.

### Read and Write Settings

Settings are stored in `scripts/hex_settings.json`.

- Read settings:
  ```bash
  npm run hex:settings:read -- --token "<your-token>"
  ```
- Write settings:
  ```bash
  npm run hex:settings:write -- dev.verbose true --token "<your-token>"
  ```

To make access less trivial for beginners, settings read/write is token-gated:

1. First-time setup (no token needed only for this one key):
   ```bash
   npm run hex:settings:write -- dev.access_token "\"your-secret-token\""
   ```
2. Set other values only with the token.
2. Use `--token` or export `HEX_OPS_TOKEN` before read/write commands.

Validate Python bytecode compilation:

```bash
npm run py-compile
```

## Deployment

Changes are published through the `gh-pages` branch deployment flow.
