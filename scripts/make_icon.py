"""
Generate icon.ico for AlocasiaTrack.

Design: 'A'-shaped leaf  /stem/  'T'-shaped leaf on a dark-green rounded square.
"""

from PIL import Image, ImageDraw


def _frame(size: int) -> Image.Image:
    s = size
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # ── Background ────────────────────────────────────────────────────────
    pad = max(1, s // 20)
    d.rounded_rectangle(
        [pad, pad, s - pad - 1, s - pad - 1],
        radius=max(3, s // 5),
        fill=(24, 68, 32, 255),
    )

    leaf  = (118, 198, 84, 255)   # mid-green
    slash = (170, 230, 120, 255)  # lighter stem green
    t     = max(1, s // 17)       # stroke thickness

    def pt(rx, ry):
        return (int(rx * s), int(ry * s))

    # ── A-leaf ─────────────────────────────────────────────────────────────
    # Two legs converging to a point at top-centre; horizontal crossbar.
    apex  = pt(0.265, 0.105)
    bl    = pt(0.070, 0.875)
    br    = pt(0.435, 0.875)

    d.line([apex, bl], fill=leaf, width=t)
    d.line([apex, br], fill=leaf, width=t)

    # Crossbar at ~58 % height
    cb_frac = (0.58 - 0.105) / (0.875 - 0.105)
    cb_lx = 0.265 + (0.070 - 0.265) * cb_frac
    cb_rx = 0.265 + (0.435 - 0.265) * cb_frac
    d.line([pt(cb_lx, 0.58), pt(cb_rx, 0.58)], fill=leaf, width=t)

    # ── Stem / ─────────────────────────────────────────────────────────────
    d.line([pt(0.465, 0.875), pt(0.545, 0.125)], fill=slash, width=t)

    # ── T-leaf ─────────────────────────────────────────────────────────────
    # Horizontal bar at top; vertical stem centred.
    bar_y = 0.215
    cx    = 0.745
    d.line([pt(0.575, bar_y), pt(0.920, bar_y)], fill=leaf, width=t)
    d.line([pt(cx,   bar_y), pt(cx,   0.875)],   fill=leaf, width=t)

    return img


def main():
    import pathlib
    out = pathlib.Path(__file__).resolve().parent.parent / "icon.ico"
    # Draw each size explicitly for crisp results, then bundle via the
    # 'sizes' keyword which tells Pillow to include all of them in the ICO.
    sizes  = [16, 32, 48, 64, 128, 256]
    frames = [_frame(s) for s in sizes]
    # ICO plugin: pass the 256-px master; add the rest via append_images;
    # the 'sizes' list tells the encoder which entries to write.
    ico_sizes = [(s, s) for s in sizes]
    frames[-1].save(
        str(out),
        format="ICO",
        sizes=ico_sizes,
        append_images=frames[:-1],
    )
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
