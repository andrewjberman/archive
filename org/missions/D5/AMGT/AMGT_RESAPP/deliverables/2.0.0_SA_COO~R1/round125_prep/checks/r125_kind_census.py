"""AMGT_RESAPP round 125 (cg-1, cg-3): which printed lines moved between two full-text captures, by KIND of the census table.

  python r125_kind_census.py compare <before.json> <after.json>     (captures from r124_full_text_census.py capture live|local)

Read-only. RICH (line-structured): a line only in BEFORE is REMOVED, only in AFTER is ADDED. A REMOVED/ADDED pair is EXPECTED when the added line equals the
removed line with its FIRST state word (`ABSENT` or `REFUSED`) replaced by `Not available`, and the removed line is one of the census kinds:
  K1  `Posture: ABSENT -- <reason>` (and with `. Nothing is rendered in its place.`)
  K2  `ABSENT -- no call was made: <reason>`
  K3  `y/y growth rows: ABSENT -- ...`
  K4  `<years>E: ABSENT -- the block carries fiscal years ...`
  K5  `Description: ABSENT -- <reason>`
  K6  `Exec Management: ABSENT (<words>).`
  K8  `<MNEMONIC>: REFUSED -- <reason>`
  K9  `ABSENT -- no peer set supplied to this export`
  K0  (round 124, already moved) `<column>: ABSENT -- ...` inside `## Peers`, `The chart: ABSENT...` -- counted under K0 if seen.
Every other moved line is OTHER: a row, and it stops the redeploy. PDF: the AFTER text must equal the BEFORE text byte for byte per name (the PDF prints no state word).
Prints the denominator, the counts per kind, the names, and `CENSUS: CLEAN|NOT CLEAN`. Grades nothing by itself.
"""
import collections
import json
import re
import sys

KINDS = [
    ("K1", re.compile(r"^Posture: (ABSENT) -- ")),
    ("K2", re.compile(r"^(ABSENT) -- no call was made: ")),
    ("K3", re.compile(r"^y/y growth rows: (ABSENT) -- ")),
    ("K4", re.compile(r"^[0-9E, ]+: (ABSENT) -- the block carries fiscal years ")),
    ("K5", re.compile(r"^Description: (ABSENT) -- ")),
    ("K6", re.compile(r"^Exec Management: (ABSENT) \(")),
    ("K8", re.compile(r"^[A-Z0-9_]+: (REFUSED) -- ")),
    ("K9", re.compile(r"^(ABSENT) -- no peer set supplied to this export")),
    ("K0", re.compile(r"^The chart: (ABSENT)")),
]


def _kind(old):
    for name, rx in KINDS:
        m = rx.match(old)
        if m:
            return name, m.start(1), m.end(1)
    return None


def compare(a, b):
    ja, jb = json.load(open(a, encoding="utf-8")), json.load(open(b, encoding="utf-8"))
    both = sorted(set(ja) & set(jb))
    skipped = [k for k in both if "error" in ja[k] or "error" in jb[k]]
    kinds, per_name, other, pdf_bad = collections.Counter(), collections.defaultdict(collections.Counter), [], []
    for k in both:
        if k in skipped:
            continue
        ra, rb = ja[k]["rich"].splitlines(), jb[k]["rich"].splitlines()
        sa, sb = set(ra), set(rb)
        only_a, only_b = [x for x in ra if x not in sb], [x for x in rb if x not in sa]
        used = set()
        for old in only_a:
            hit = _kind(old)
            new = old[:hit[1]] + "Not available" + old[hit[2]:] if hit else None
            if hit and new in only_b and new not in used:
                used.add(new)
                kinds[hit[0]] += 1
                per_name[hit[0]][k] += 1
            else:
                other.append((k, "REMOVED", old))
        for new in only_b:
            if new not in used:
                other.append((k, "ADDED", new))
        if ja[k]["pdf"] != jb[k]["pdf"]:
            pdf_bad.append(k)
    print("COMPARE: %d names in both captures, %d skipped (an error in a capture)" % (len(both), len(skipped)))
    for k in skipped:
        print("  SKIPPED %s" % k)
    total = sum(kinds.values())
    print("RICH MOVED LINES (expected pairs): %d" % total)
    for name in sorted(kinds):
        print("  %-3s %5d lines on %3d names" % (name, kinds[name], len(per_name[name])))
    print("RICH OTHER MOVED LINES (a row, stops the redeploy): %d" % len(other))
    for k, how, line in other[:40]:
        print("  OTHER %-24s %-7s %s" % (k, how, line[:150]))
    print("PDF: %d name(s) differ%s" % (len(pdf_bad), (": " + ", ".join(pdf_bad[:12])) if pdf_bad else " (byte-identical on every comparable name)"))
    print("CENSUS: %s" % ("CLEAN: only the census kinds moved, the PDF unchanged" if not other and not pdf_bad else "NOT CLEAN: read the OTHER / PDF lines above"))
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "compare":
        sys.exit(compare(sys.argv[2], sys.argv[3]))
    print(__doc__)
    sys.exit(2)
