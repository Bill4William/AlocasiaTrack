#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# AlocasiaTrack  --  macOS build script
# Run from any directory; the script cd's to the project root automatically.
#
# Produces:
#   dist/AlocasiaTrack.app                        -- the application bundle
#   installer_output/AlocasiaTrackSetup_v1.0.0.dmg -- drag-to-install disk image
#
# Requirements:
#   Python 3.11+  (python.org build recommended — includes Tcl/Tk for tkinter)
#   pip3 install -r requirements.txt
#   pip3 install pyinstaller
#   Xcode Command Line Tools:  xcode-select --install
# ---------------------------------------------------------------------------
set -euo pipefail

cd "$(dirname "$0")/.."

echo "=================================================="
echo "  AlocasiaTrack Build Script (macOS)"
echo "=================================================="
echo

# ---- Python detection -------------------------------------------------------
PY=""
for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
        PY="$candidate"
        break
    fi
done

if [ -z "$PY" ]; then
    echo "ERROR: Python not found."
    echo "  Install from https://python.org  or:  brew install python"
    exit 1
fi

echo "Using Python: $($PY --version)"
echo

# ---- Step 1: Generate ICNS icon ---------------------------------------------
echo "[1/3] Generating macOS icon (icon.icns)..."
SVG_SOURCE="E:/AlocasiaTracker/AT_ICON.svg"
if [ -f "$SVG_SOURCE" ]; then
    "$PY" scripts/make_icns.py "$SVG_SOURCE"
else
    "$PY" scripts/make_icns.py
fi
echo

# ---- Step 2: PyInstaller ----------------------------------------------------
echo "[2/3] Bundling application with PyInstaller..."
"$PY" -m PyInstaller AlocasiaTrack.spec --clean --noconfirm
echo

# ---- Step 3: Create DMG -----------------------------------------------------
echo "[3/3] Creating disk image (.dmg)..."
mkdir -p installer_output

VERSION="1.0.0"
DMG_NAME="AlocasiaTrackSetup_v${VERSION}.dmg"
DMG_PATH="installer_output/${DMG_NAME}"

# Staging folder: .app + Applications symlink for drag-and-drop install
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

cp -r "dist/AlocasiaTrack.app" "$TMP_DIR/"
ln -s /Applications "$TMP_DIR/Applications"

# Build compressed read-only DMG
hdiutil create \
    -volname "AlocasiaTrack" \
    -srcfolder "$TMP_DIR" \
    -ov \
    -format UDZO \
    "$DMG_PATH"

echo
echo "=================================================="
echo "  SUCCESS"
echo "  App:       dist/AlocasiaTrack.app"
echo "  Installer: ${DMG_PATH}"
echo "=================================================="
