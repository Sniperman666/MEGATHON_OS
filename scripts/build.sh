#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR/assets"

# Copy root static pages and common assets
cp "$ROOT_DIR"/*.html "$DIST_DIR"/
cp "$ROOT_DIR"/favicon.ico "$DIST_DIR"/
cp "$ROOT_DIR"/homepage.png "$DIST_DIR"/
cp "$ROOT_DIR"/README.md "$DIST_DIR"/
cp -R "$ROOT_DIR"/assets/. "$DIST_DIR"/assets/

# Lightweight integrity checks on build output
if grep -R -n -I -E 'README_SYNC_MARKER|readme-sync-footer|Synced baseline: README\.md' "$DIST_DIR" > /dev/null; then
  echo "Build failed: sync marker/footer traces found in dist output." >&2
  exit 1
fi

echo "Build complete: $DIST_DIR"
