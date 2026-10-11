"""AMGT_CORPUS round 46, CRPS-av-4 leg p -- the pixel comparison of two walker output directories (the CTO half's condition 2). Issuer's file.
READ-ONLY over local screenshots (gitignored; client and page content is never committed or pasted: this prints names and counts only).

  python av4_pixel_compare.py <dir A> <dir B>          dirs are tmp/ui-walk/<stamp>/ (each holds shots/NNN-<step>.png)

Pairs the shots of A and B by step name (the file name without its leading `NNN-`), compares each pair pixel for pixel (Pillow
ImageChops.difference over RGB; a size difference is a difference), and prints per shot `EQUAL` or `DIFFERENT <changed pixels> bbox <box>`,
then `pixels equal <e> of <n> paired; only in A <a>; only in B <b>`. Exit 0 only when every pair is equal and nothing is unpaired.
"""
import os
import re
import sys

from PIL import Image, ImageChops


def shots(d):
    out = {}
    root = os.path.join(d, "shots")
    for name in sorted(os.listdir(root)):
        if name.lower().endswith(".png"):
            out[re.sub(r"^\d+-", "", name)] = os.path.join(root, name)
    return out


def main(argv):
    a, b = shots(argv[0]), shots(argv[1])
    equal = 0
    paired = 0
    for step in sorted(set(a) & set(b)):
        paired += 1
        ia, ib = Image.open(a[step]).convert("RGB"), Image.open(b[step]).convert("RGB")
        if ia.size != ib.size:
            print("DIFFERENT %s size %s vs %s" % (step, ia.size, ib.size))
            continue
        diff = ImageChops.difference(ia, ib)
        box = diff.getbbox()
        if box is None:
            equal += 1
            print("EQUAL %s" % step)
        else:
            changed = sum(1 for px in diff.getdata() if px != (0, 0, 0))
            print("DIFFERENT %s changed_pixels %d bbox %s" % (step, changed, box))
    only_a, only_b = sorted(set(a) - set(b)), sorted(set(b) - set(a))
    print("pixels equal %d of %d paired; only in A %d; only in B %d" % (equal, paired, len(only_a), len(only_b)))
    for s in only_a[:6]:
        print("  only in A: %s" % s)
    for s in only_b[:6]:
        print("  only in B: %s" % s)
    return 0 if (paired and equal == paired and not only_a and not only_b) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
