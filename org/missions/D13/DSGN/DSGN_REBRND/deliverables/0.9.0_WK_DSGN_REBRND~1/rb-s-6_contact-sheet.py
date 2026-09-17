"""contact-sheet.py -- tile every keyboard-walk stop's clip into one PNG per route.

Usage: python contact-sheet.py <walk-json> <out.png>
Each tile is labelled: stop number, element, :focus-visible, and which ring (if any) painted.
"""
import json
import sys

from PIL import Image, ImageDraw

src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src, encoding="utf-8"))
tiles = []
for s in d["stops"]:
    if s.get("body") or not s.get("clip"):
        continue
    try:
        im = Image.open(s["clip"]).convert("RGB")
    except OSError:
        continue
    im.thumbnail((340, 150))
    label = "#%d %s %s | fv=%s ring=%s%s" % (s["i"], s["tag"], s["text"][:22], "Y" if s["fv"] else "N", s["ring"],
                                             "" if s["ring"] == "NONE" else ("-full" if s.get("full") else "-partial"))
    tiles.append((im, label))
for c in d.get("clicks", []):
    if c.get("none") or not c.get("shot"):
        continue
    try:
        im = Image.open(c["shot"]).convert("RGB")
    except OSError:
        continue
    im.thumbnail((340, 150))
    tiles.append((im, "MOUSE %s | fv=%s ring=%s" % (c["kind"], "Y" if c["fv"] else "N", c["ring"])))

cols, tw, th = 4, 356, 180
rows = max(1, (len(tiles) + cols - 1) // cols)
header = 34
sheet = Image.new("RGB", (cols * tw, header + rows * th), (255, 255, 255))
dr = ImageDraw.Draw(sheet)
env = d["env"]
dr.text((8, 8), "%s [%s] root-font %s | stops %d | shell-accent-fill %d | %s" % (
    d["route"], d["tag"], env["rootFont"], len([s for s in d["stops"] if not s.get("body")]),
    len(env["shellFill"]), "wrapped" if d["wrapped"] else "capped"), fill=(0, 0, 0))
for n, (im, label) in enumerate(tiles):
    x, y = (n % cols) * tw + 8, header + (n // cols) * th
    sheet.paste(im, (x, y + 16))
    dr.text((x, y + 2), label, fill=(0, 0, 0))
sheet.convert("P", palette=Image.ADAPTIVE, colors=256).save(out, optimize=True)
print("SHEET", out, "tiles", len(tiles), "size", sheet.size)
