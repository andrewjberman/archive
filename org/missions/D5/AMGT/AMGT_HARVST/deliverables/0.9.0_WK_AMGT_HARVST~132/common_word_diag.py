"""AMGT_HARVST round 76, HVST-bt-1 AMENDMENT 1 -- a DIAGNOSTIC beside `common_word_scan.py`, not part of the rule. It takes the
five aliases the CVO grade and the measured file put nearest the line (Visa, Orange, Booking, Cadence, Monster) and splits LOWER
and CAP_MID by where the use stands (title / body), by its form (all caps / not), and whether a CAP_MID title use stands in a title
capitalised throughout (where case carries no information, HVST-bk-2), plus the number of ARTICLES with each kind of use. It
changes nothing and tunes nothing; it writes `common_word_diag.out`. Run: `PYTHONPATH=. python <this file>` from the worktree root.
"""
import collections
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *[".."] * 7))
sys.path.insert(0, ROOT)

from lib.research.harvest import publication_gold as pg  # noqa: E402
from common_word_scan import classify  # noqa: E402

ALIASES = ["Visa", "Orange", "Booking", "Cadence", "Monster"]
OUT = os.path.join(HERE, "common_word_diag.out")


def main():
    rx = {a: re.compile(r"(?<!\w)" + re.escape(a) + r"(?!\w)", re.I) for a in ALIASES}
    cnt = {a: collections.Counter() for a in ALIASES}
    arts = {a: collections.Counter() for a in ALIASES}
    scanned = 0
    for article in pg._iter_latest_articles():
        scanned += 1
        title = article.get("title") or ""
        tcap = pg._capitalised_throughout(title)
        seen = {a: set() for a in ALIASES}
        for where, text in [("title", title)] + [("body", b or "") for b in (article.get("text_blocks") or [])]:
            for a in ALIASES:
                for m in rx[a].finditer(text):
                    kind = classify(text, m)
                    if kind is None:
                        continue
                    if kind == "lower":
                        label = "LOWER_" + where
                    else:
                        label = "CAP_MID_%s_%s" % (where, "allcaps" if m.group(0).isupper() else "mixedcase")
                        if where == "title" and tcap:
                            label += "_inTitleCasedHeadline"
                    cnt[a][label] += 1
                    seen[a].add(kind)
        for a in ALIASES:
            for kind in seen[a]:
                arts[a][kind] += 1
    lines = ["articles scanned %d" % scanned]
    for a in ALIASES:
        lines.append("%s: ARTICLES with a LOWER use %d, with a CAP_MID use %d" % (a, arts[a]["lower"], arts[a]["cap_mid"]))
        for label, n in sorted(cnt[a].items()):
            lines.append("  %s %s %d" % (a, label, n))
    with io.open(OUT, "w", encoding="ascii", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
