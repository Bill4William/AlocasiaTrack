"""
Convert an SVG file to a multi-size ICO using Playwright's Chromium renderer.
Usage: python scripts/svg_to_ico.py <input.svg> [output.ico]
"""
import sys
import os
from pathlib import Path
from PIL import Image
import io


def svg_to_ico(svg_path: str, ico_path: str):
    svg_path = Path(svg_path).resolve()
    ico_path = Path(ico_path).resolve()

    print(f"Rendering {svg_path.name} via Chromium...")

    from playwright.sync_api import sync_playwright

    sizes = [256, 128, 64, 48, 32, 16]
    frames = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 256, "height": 256})

        # Load SVG directly as a data URL so file:// path issues don't matter
        svg_content = svg_path.read_text(encoding="utf-8")
        import base64
        b64 = base64.b64encode(svg_content.encode()).decode()
        data_url = f"data:image/svg+xml;base64,{b64}"

        html = f"""<!DOCTYPE html>
<html>
<head>
<style>
  * {{ margin: 0; padding: 0; }}
  html, body {{ width: 256px; height: 256px; overflow: hidden; background: transparent; }}
  img {{ width: 256px; height: 256px; display: block; }}
</style>
</head>
<body><img src="{data_url}"></body>
</html>"""

        page.set_content(html)
        page.wait_for_load_state("networkidle")

        for size in sizes:
            page.set_viewport_size({"width": size, "height": size})
            page.evaluate(f"""
                document.querySelector('img').style.width = '{size}px';
                document.querySelector('img').style.height = '{size}px';
                document.body.style.width = '{size}px';
                document.body.style.height = '{size}px';
            """)
            png_bytes = page.screenshot(
                clip={"x": 0, "y": 0, "width": size, "height": size},
                omit_background=True,
            )
            img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
            frames.append(img)
            print(f"  {size}x{size} done")

        browser.close()

    # Save as multi-size ICO
    ico_path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        str(ico_path),
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=frames[1:],
    )

    # Verify
    with open(str(ico_path), "rb") as f:
        header = f.read(6)
    import struct
    _, _, count = struct.unpack("<HHH", header)
    print(f"\nSaved {ico_path}")
    print(f"ICO contains {count} size(s): {sizes[:count]}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/svg_to_ico.py <input.svg> [output.ico]")
        sys.exit(1)
    svg  = sys.argv[1]
    ico  = sys.argv[2] if len(sys.argv) > 2 else str(Path(svg).with_suffix(".ico"))
    svg_to_ico(svg, ico)
