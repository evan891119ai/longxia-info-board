#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp="${TMPDIR:-/tmp}/longxia-info-board-gh-pages"
rm -rf "$tmp"
mkdir -p "$tmp"
cp -a "$root/docs/." "$tmp/"
cd "$tmp"
git init -b gh-pages >/dev/null
git config user.name "Longxia"
git config user.email "281945066+evan891119ai@users.noreply.github.com"
git add .
git commit -m "Deploy site" >/dev/null
git remote add origin https://github.com/evan891119ai/longxia-info-board.git
git push -f origin gh-pages
