#!/usr/bin/env python3
"""
make_icns.py  --  Generate icon.icns for macOS from the SVG source icon.

Usage:
    python3 scripts/make_icns.py [path/to/source.svg]

If no SVG is supplied the script falls back to icon.ico (already built by
make_icon.py / svg_to_ico.py) and converts the largest frame to ICNS.

Requirements:
    pip install pillow playwright
    playwright install chromium   (only needed for SVG → PNG rendering)

Output:
    icon.icns  (next to this script's project root)
"""

from __future__ import annotations

import os
import sys
import struct
import tempfile
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# macOS iconset sizes (pt size, scale)  →  pixel size
ICNS_SIZES = [16, 32, 64, 128, 256, 512, 1024]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _render_svg_to_pngs(svg_path: str) -> dict[int, bytes]:
    """Render SVG at each ICNS pixel size using Playwright headless Chromium."""
    import base64
    from playwright.sync_api import sync_playwright

    with open(svg_path, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode()
    data_url = f"data:image/svg+xml;base64,{b64}"

    pngs: dict[int, bytes] = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        for size in ICNS_SIZES:
            page = browser.new_page(viewport={"width": size, "height": size})
            page.set_content(f"""<!DOCTYPE html>
<html><head>
<style>*{{margin:0;padding:0;background:transparent}}
img{{width:{size}px;height:{size}px;display:block}}</style>
</head><body>
<img src="{data_url}">
</body></html>""")
            page.wait_for_load_state("networkidle")
            pngs[size] = page.screenshot(
                clip={"x": 0, "y": 0, "width": size, "height": size},
                omit_background=True,
                type="png",
            )
        browser.close()
    return pngs


def _pngs_from_ico(ico_path: str) -> dict[int, bytes]:
    """Extract the largest available frame from an .ico and resize for ICNS."""
    from PIL import Image
    import io

    img = Image.open(ico_path)
    # Grab the largest size in the ico
    sizes = img.info.get("sizes", [(img.width, img.height)])
    largest = max(sizes, key=lambda s: s[0])
    img = img.resize(largest, Image.LANCZOS).convert("RGBA")

    pngs: dict[int, bytes] = {}
    for size in ICNS_SIZES:
        resized = img.resize((size, size), Image.LANCZOS)
        buf = io.BytesIO()
        resized.save(buf, format="PNG")
        pngs[size] = buf.getvalue()
    return pngs


def build_icns(pngs: dict[int, bytes], out_path: str):
    """
    Assemble an ICNS file from a dict of {pixel_size: png_bytes}.
    Uses macOS `iconutil` if available; otherwise falls back to pure-Python
    construction of the ICNS binary format.
    """
    # Try iconutil (macOS only)
    if sys.platform == "darwin" and _have_iconutil():
        _build_icns_via_iconutil(pngs, out_path)
    else:
        _build_icns_raw(pngs, out_path)
    print(f"  Written: {out_path}")


def _have_iconutil() -> bool:
    try:
        subprocess.run(["iconutil", "--version"], capture_output=True)
        return True
    except FileNotFoundError:
        return False


def _build_icns_via_iconutil(pngs: dict[int, bytes], out_path: str):
    """Build ICNS using macOS `iconutil` (highest quality path)."""
    with tempfile.TemporaryDirectory(suffix=".iconset") as iconset:
        for size, data in pngs.items():
            # Standard names expected by iconutil
            name = f"icon_{size}x{size}.png"
            Path(iconset, name).write_bytes(data)
            # @2x variant (retina) — same PNG at 2× the logical size
            if size // 2 in pngs:
                name2x = f"icon_{size//2}x{size//2}@2x.png"
                Path(iconset, name2x).write_bytes(data)
        subprocess.run(
            ["iconutil", "-c", "icns", iconset, "-o", out_path],
            check=True,
        )


# OSType codes for common PNG sizes in the ICNS format
_OSTYPE: dict[int, bytes] = {
    16:   b"icp4",
    32:   b"icp5",
    64:   b"icp6",
    128:  b"ic07",
    256:  b"ic08",
    512:  b"ic09",
    1024: b"ic10",
}


def _build_icns_raw(pngs: dict[int, bytes], out_path: str):
    """Pure-Python ICNS builder (works on all platforms, used on Windows/CI)."""
    chunks: list[bytes] = []
    for size in ICNS_SIZES:
        if size not in pngs or size not in _OSTYPE:
            continue
        data = pngs[size]
        ostype = _OSTYPE[size]
        # Each ICNS chunk: 4-byte OSType + 4-byte length (includes 8-byte header)
        length = 8 + len(data)
        chunks.append(ostype + struct.pack(">I", length) + data)

    body = b"".join(chunks)
    total_length = 8 + len(body)
    icns = b"icns" + struct.pack(">I", total_length) + body

    with open(out_path, "wb") as fh:
        fh.write(icns)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    svg_path = sys.argv[1] if len(sys.argv) > 1 else None
    out_path = str(PROJECT_ROOT / "icon.icns")

    print("=" * 50)
    print("  AlocasiaTrack  --  macOS icon builder")
    print("=" * 50)

    if svg_path and Path(svg_path).exists():
        print(f"  Source:  SVG  ({svg_path})")
        try:
            pngs = _render_svg_to_pngs(svg_path)
        except Exception as exc:
            print(f"  SVG render failed ({exc}), falling back to icon.ico")
            pngs = _pngs_from_ico(str(PROJECT_ROOT / "icon.ico"))
    else:
        ico_path = str(PROJECT_ROOT / "icon.ico")
        if not Path(ico_path).exists():
            print("  ERROR: icon.ico not found — run make_icon.py first.")
            sys.exit(1)
        print(f"  Source:  ICO  ({ico_path})")
        pngs = _pngs_from_ico(ico_path)

    print(f"  Sizes:   {sorted(pngs.keys())}")
    build_icns(pngs, out_path)
    print("  Done.")


if __name__ == "__main__":
    main()
