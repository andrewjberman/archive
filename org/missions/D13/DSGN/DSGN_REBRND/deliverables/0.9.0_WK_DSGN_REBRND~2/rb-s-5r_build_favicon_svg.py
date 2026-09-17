"""rb-s-5r_build_favicon_svg.py -- DSGN_REBRND.TO-RB-s-5 Amendment 1, the favicon SVG.

Builds <portal>/public/favicon.svg: a #5F3BE3 circle filling a 100x100 box, with the white
mark's three paths centred on it at 60% of the diameter. The paths are COPIED BYTE-FOR-BYTE
from <portal>/public/logos/opal-icon-white.svg (never retyped) and the script proves it by
reading its own output back. Nothing is fetched from any network location.

Usage: python rb-s-5r_build_favicon_svg.py <portal root>
"""

import re
import sys
from pathlib import Path

DIAMETER = 100.0
MARK_FRACTION = 0.60
ACCENT = "#5F3BE3"


def main():
    portal = Path(sys.argv[1])
    src_path = portal / "public/logos/opal-icon-white.svg"
    src = src_path.read_text(encoding="utf-8")
    vb = re.search(r'viewBox="([^"]+)"', src).group(1).split()
    w, h = float(vb[2]), float(vb[3])
    ds = re.findall(r'<path[^>]*\sd="([^"]+)"', src)
    if len(ds) != 3:
        print("ERROR: expected 3 paths in", src_path, "found", len(ds))
        sys.exit(1)
    s = DIAMETER * MARK_FRACTION / max(w, h)
    tx = (DIAMETER - w * s) / 2
    ty = (DIAMETER - h * s) / 2
    paths = "".join(f'<path d="{d}"/>' for d in ds)
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><title>Opal</title>'
        f'<circle cx="50" cy="50" r="50" fill="{ACCENT}"/>'
        f'<g transform="translate({tx:.4f} {ty:.4f}) scale({s:.7f})" fill="#FFFFFF">{paths}</g></svg>\n'
    )
    out = portal / "public/favicon.svg"
    out.write_bytes(svg.encode("utf-8"))

    back = out.read_bytes().decode("utf-8")
    out_ds = re.findall(r'<path d="([^"]+)"', back)
    print("SOURCE:", src_path.as_posix(), f"({len(src.encode('utf-8'))} B), viewBox {w} x {h}")
    print("SRC-PATHS:", len(ds), "OUT-PATHS:", len(out_ds))
    print("PATHS-BYTE-EQUAL:", out_ds == ds)
    print(f"MARK-BOX: {w * s:.3f} x {h * s:.3f} of {DIAMETER:.0f} (fraction of diameter {max(w, h) * s / DIAMETER:.2f}); "
          f"offset {tx:.4f}, {ty:.4f}")
    print("OUT:", out.as_posix(), f"({len(back.encode('utf-8'))} B)", "accent=" + str(ACCENT.lower() in back.lower()),
          "white=" + str("#ffffff" in back.lower()))
    sys.exit(0 if out_ds == ds else 1)


if __name__ == "__main__":
    main()
