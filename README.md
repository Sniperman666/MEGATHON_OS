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

## Deployment

Changes are published through the `gh-pages` branch deployment flow.
