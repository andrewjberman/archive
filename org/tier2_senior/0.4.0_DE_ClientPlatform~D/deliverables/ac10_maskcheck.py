"""ADVI_PERFRP TO-R1-DE / AC10(c) -- masked pixel comparison of the protected tabs.

COO ruling @f696acb8f8 pins AC10(c) to a MASKED PIXEL comparison and BANS md5/byte
comparison of screenshots. The ban is empirical, not stylistic: two captures of an
UNCHANGED tree differ in bytes (98,490 vs 98,491) and in md5, so a byte test
false-positives on every run. Pixels are stable outside one animated element.

Two modes:

  derive   <dir> <tag> <n>          re-derive the mask from n captures of an
                                    UNCHANGED tree, comparing ALL pairs (not
                                    each-vs-first: a first-capture artefact would
                                    otherwise define the mask). Prints the union
                                    bbox and per-pair spread.

  compare  <pre.png> <post.png> <tag>   the acceptance assertion. Exit 0 only if
                                    dimensions match exactly AND zero pixels
                                    differ outside that tab's mask.

MASK IS PER TAB. Do NOT union across tabs -- the two boxes sit at different y
(the Distribution page is 250px taller) and their union would mask ~2,064
provably deterministic pixels, i.e. a blind spot a real regression could hide in.

Measured basis (n=5 per tab, 10/10 pairs each, one box, portal @d43b88c5):
  advisors      1440x1003   variance bbox (105, 904, 113, 912)    max 60px
  distribution  1440x1253   variance bbox (105,1154, 113,1162)    max 60px
Both are the pulsing green "Black Diamond Connected" status dot in the DATA
SOURCE panel -- identified by cropping and looking, not inferred from position.
0 of 10 pairs were pixel-identical on either tab: masking is REQUIRED, not
optional. Cross-machine stability is UNPROVEN -- re-run `derive` on your own box
before trusting `compare`.
"""
from __future__ import annotations

import os
import sys
from itertools import combinations

try:
    from PIL import Image, ImageChops
except ImportError:
    print("ERROR: Pillow is required (import PIL failed). Not falling back to a "
          "byte compare -- that is the banned test.")
    sys.exit(3)

# Per-tab mask: (x0, y0, x1, y1), half-open in the PIL bbox sense.
MASKS = {
    "advisors": (105, 904, 113, 912),
    "distribution": (105, 1154, 113, 1162),
}

# Capture files are commonly tagged with the short form. An unknown tag must
# FAIL LOUD, never resolve to None -- found during exercise: `derive ... adv 5`
# printed "declared mask: None", skipped the bounding verdict entirely, and still
# returned 0. A control that cannot find its mask must not report success.
ALIASES = {"adv": "advisors", "dist": "distribution"}


def resolve_tag(tag):
    """Canonical tag, or None if unknown. Callers MUST fail loud on None."""
    if tag in MASKS:
        return tag
    return ALIASES.get(tag)


def load(path):
    return Image.open(path).convert("RGB")


def diff_outside_mask(img_a, img_b, mask):
    """Count differing pixels, ignoring the mask box. Returns (count, bbox)."""
    diff = ImageChops.difference(img_a, img_b)
    if mask:
        # Zero the mask region so it cannot contribute to the count or the bbox.
        black = Image.new("RGB", (mask[2] - mask[0], mask[3] - mask[1]), (0, 0, 0))
        diff.paste(black, (mask[0], mask[1]))
    count = sum(diff.convert("L").histogram()[1:])
    return count, diff.getbbox()


def cmd_derive(directory, tag, count):
    canon = resolve_tag(tag)
    if canon is None:
        print("UNKNOWN TAG %r -- known: %s (aliases: %s). Refusing to derive "
              "against no mask." % (tag, sorted(MASKS), sorted(ALIASES)))
        return 2
    imgs = []
    for i in range(1, count + 1):
        path = os.path.join(directory, "%s_%d.png" % (tag, i))
        if not os.path.isfile(path):
            print("MISSING CAPTURE: %s" % path)
            return 2
        imgs.append(load(path))
    sizes = {im.size for im in imgs}
    print("=== derive %s : n=%d captures of an UNCHANGED tree ===" % (tag, count))
    print("  dimensions: %s  %s"
          % (sizes, "STABLE" if len(sizes) == 1 else "*** UNSTABLE -> pixel compare invalid ***"))
    if len(sizes) != 1:
        return 2
    width, height = imgs[0].size
    total = width * height
    union = None
    pairs = []
    for a, b in combinations(range(count), 2):
        raw = ImageChops.difference(imgs[a], imgs[b])
        bbox = raw.getbbox()
        nonzero = sum(raw.convert("L").histogram()[1:])
        pairs.append((a + 1, b + 1, nonzero, bbox))
        if bbox:
            union = bbox if union is None else (
                min(union[0], bbox[0]), min(union[1], bbox[1]),
                max(union[2], bbox[2]), max(union[3], bbox[3]))
    identical = sum(1 for p in pairs if p[2] == 0)
    print("  pairs compared: %d of %d possible" % (len(pairs), count * (count - 1) // 2))
    print("  pixel-identical pairs: %d/%d %s"
          % (identical, len(pairs),
             "(masking REQUIRED)" if identical == 0 else "(some pairs stable)"))
    print("  max differing pixels: %d of %d (%.5f%%)"
          % (max(p[2] for p in pairs), total, 100.0 * max(p[2] for p in pairs) / total))
    print("  UNION bbox of all variance: %s" % (union,))
    print("  declared mask for %s : %s" % (canon, MASKS[canon]))
    for first, second, nonzero, bbox in pairs:
        print("    pair %d-%d: %5d px  bbox=%s" % (first, second, nonzero, bbox))
    if union:
        mask = MASKS[canon]
        bounded = (union[0] >= mask[0] and union[1] >= mask[1]
                   and union[2] <= mask[2] and union[3] <= mask[3])
        print("  VERDICT: observed variance is %s the declared mask"
              % ("WITHIN" if bounded else "*** OUTSIDE *** -- re-derive before using compare;"))
        return 0 if bounded else 1
    return 0


def cmd_compare(pre_path, post_path, tag):
    canon = resolve_tag(tag)
    if canon is None:
        print("UNKNOWN TAG %r -- known: %s (aliases: %s). Refusing to compare "
              "against no mask." % (tag, sorted(MASKS), sorted(ALIASES)))
        return 2
    pre, post = load(pre_path), load(post_path)
    print("=== AC10(c) masked compare : %s ===" % canon)
    print("  pre : %s  %s" % (pre.size, pre_path))
    print("  post: %s  %s" % (post.size, post_path))
    if pre.size != post.size:
        print("  FAIL -- DIMENSIONS DIFFER. Not resizing; a size change is a real change.")
        return 1
    mask = MASKS[canon]
    count, bbox = diff_outside_mask(pre, post, mask)
    total = pre.size[0] * pre.size[1]
    print("  mask applied: %s (%d px)" % (mask, (mask[2] - mask[0]) * (mask[3] - mask[1])))
    print("  differing pixels OUTSIDE mask: %d of %d" % (count, total))
    print("  bbox of remaining difference : %s" % (bbox,))
    if count == 0:
        print("  PASS -- surface unchanged outside the declared mask.")
        print("  NOTE: this judges WHETHER something changed, never whether a change "
              "is correct, and it does not cover interaction states. The human READ stands.")
        return 0
    print("  FAIL -- the protected surface changed outside the mask.")
    return 1


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    if args[0] == "derive" and len(args) == 4:
        return cmd_derive(args[1], args[2], int(args[3]))
    if args[0] == "compare" and len(args) == 4:
        return cmd_compare(args[1], args[2], args[3])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
