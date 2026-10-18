"""AMGT_RESAPP round 118 (AMGT-by-4): the issuer's citation check on a read-cell receipt.

  python r118_receipt_cites_check.py <receipt.md> [REQUIRED SECTION HEADING ...]

Reads the receipt (a markdown file) and, for every `path:line` or `path:line-line` citation it finds (a repo-relative path made of word, dot, dash,
slash and tilde characters and ending in a file suffix, a colon, and a line number or a range), checks that the file exists under the current
directory and that the line (or the range's end) does not exceed the file's line count. It also checks the five section headings of the by-4
receipt (`## Producer step`, `## The rule`, `## What carrying the fund currency would need`, `## What the page does`, `## Not verified`) unless
other headings are named on the command line. Prints one line per refused citation and a last line
`RECEIPT CITES: YES|NO (<ok> of <n> citations resolve, <s> of <m> sections present)`.

It verifies that a cited line EXISTS. It does NOT grade whether the cited line says what the receipt claims: the CTO reads the receipt.
Read-only; reads only the receipt and the files it cites.
"""
import os
import re
import sys

DEFAULT_SECTIONS = ["## Producer step", "## The rule", "## What carrying the fund currency would need", "## What the page does", "## Not verified"]
CITE = re.compile(r"(?<![\w./~-])((?:[\w.~-]+/)+[\w.~-]+\.(?:py|ts|tsx|js|cjs|mjs|json|md|sh|yaml|yml|tf|sql|txt)):(\d+)(?:-(\d+))?")


def _lines(path):
    with open(path, "rb") as f:
        return f.read().count(b"\n") + 1


def main(argv):
    receipt = argv[1]
    sections = argv[2:] or DEFAULT_SECTIONS
    text = open(receipt, encoding="utf-8").read()
    seen, ok, bad = set(), 0, []
    for m in CITE.finditer(text):
        path, a, b = m.group(1), int(m.group(2)), m.group(3)
        key = (path, a, b)
        if key in seen:
            continue
        seen.add(key)
        end = int(b) if b else a
        if not os.path.isfile(path):
            bad.append("%s:%s%s  -> no such file under %s" % (path, a, "-" + b if b else "", os.getcwd()))
        elif a < 1 or end < a or end > _lines(path):
            bad.append("%s:%s%s  -> line outside the file (%d lines)" % (path, a, "-" + b if b else "", _lines(path)))
        else:
            ok += 1
    present = [h for h in sections if re.search(r"^" + re.escape(h) + r"\s*$", text, re.M)]
    for b in bad:
        print("REFUSED " + b)
    for h in sections:
        if h not in present:
            print("MISSING SECTION " + h)
    n = len(seen)
    verdict = "YES" if n and ok == n and len(present) == len(sections) else "NO"
    print("RECEIPT CITES: %s (%d of %d citations resolve, %d of %d sections present)" % (verdict, ok, n, len(present), len(sections)))
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
