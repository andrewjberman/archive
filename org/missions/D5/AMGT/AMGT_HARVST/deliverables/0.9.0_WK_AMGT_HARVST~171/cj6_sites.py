"""cj6_sites.py -- AMGT_HARVST HVST-cj-6 step 1a (read only). Audits every app/harvest_*.py module for the sites where a
prefix or a key is built from a caller's security_key, and classes each site:

  PARTITION  a 'security_key=<key>/' partition built from the caller's key (the class this cell changes)
  COLUMN     a comparison with a security_key column value in a parquet filter or a row compare (named, not changed)
  OTHER      any other prefix, route or path built from the caller's key (named, not changed)

A line is a site when it builds a prefix or a key from the caller's key (a format string, a + concatenation, a quote,
or a call of a key helper) or compares a security_key column. Constants with a security_key= partition are listed as
CONST lines. Reads files only; writes cj6_sites.out.

Usage, from the worktree root:  python -u <this file>
"""

import glob
import os
import re
import sys

ROOT = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "cj6_sites.out")
APP = os.path.join(ROOT, "infra", "aws", "ec2", "opal-gateway", "app")

BUILD = re.compile(
    r"%\s*\(?(key|k|security_key|spelled)\b"
    r"|\+\s*(key|k|security_key)\b"
    r"|quote\(security_key"
    r"|str\(security_key\)"
    r"|_segment\(|_kind_ref\(|_groups\(|_series_name\("
    r"|\(\"security_key\""
)
CONST = re.compile(r"^[A-Z_]+ = ")
DEF = re.compile(r"^def (\w+)\(")


def classify(text):
    if "security_key=" in text:
        return "PARTITION"
    if '("security_key"' in text:
        return "COLUMN"
    return "OTHER"


def main():
    lines = []

    def out(text):
        safe = text.encode("ascii", "backslashreplace").decode("ascii")
        print(safe, flush=True)
        lines.append(safe)

    modules = sorted(glob.glob(os.path.join(APP, "harvest_*.py")))
    out("CJ6-SITES modules=%d" % len(modules))
    counts = {"PARTITION": 0, "COLUMN": 0, "OTHER": 0}
    for path in modules:
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        with open(path, "r", encoding="utf-8") as fh:
            src = fh.read().splitlines()
        fn = "module"
        for number, text in enumerate(src, start=1):
            m = DEF.match(text)
            if m:
                fn = m.group(1)
                continue
            if CONST.match(text):
                if "security_key=" in text:
                    out("CONST file=%s line=%d %s" % (rel, number, text.strip()[:150]))
                continue
            if text.lstrip().startswith(("#", '"""')):
                continue
            if not BUILD.search(text):
                continue
            cls = classify(text)
            counts[cls] += 1
            out("SITE file=%s line=%d fn=%s class=%s %s" % (rel, number, fn, cls, text.strip()[:170]))
    out("DENOMINATOR sites=%d PARTITION=%d COLUMN=%d OTHER=%d modules=%d"
        % (sum(counts.values()), counts["PARTITION"], counts["COLUMN"], counts["OTHER"], len(modules)))

    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        for line in lines:
            fh.write(line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
