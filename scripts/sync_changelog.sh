#!/usr/bin/env bash
# Sync root CHANGELOG.md to website/docs/changelog.md with Docusaurus frontmatter.
# Called automatically by website prebuild/prestart scripts.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT_DIR/CHANGELOG.md"
DEST="$ROOT_DIR/website/docs/changelog.md"

if [ ! -f "$SRC" ]; then
  echo "Error: $SRC not found" >&2
  exit 1
fi

{
  echo "---"
  echo "sidebar_position: 99"
  echo "---"
  echo ""
  cat "$SRC"
} > "$DEST"

echo "Synced CHANGELOG.md -> website/docs/changelog.md"
