"""AMGT_RESAPP round 125 (AMGT-cg-4): did the redeploy move ONLY the census kinds' state words in the printed rich export?

  python r125_rich_kind_check.py <before_dir> <after_dir> [KEY ...]     (dirs hold <key>.md from r114_pack_capture_compare.py capture-rich)

Offline. For each name: take the BEFORE text, rewrite every line of the census kinds K1 to K6, K8 and K9 by replacing its state word (`ABSENT` or `REFUSED`, the first on the line)
with `Not available` (the expected AFTER), collapse all whitespace in the expected text and in the AFTER text, and compare. YES for a name when they are equal (the ONLY difference
between the two captures is the census kinds' word); NO otherwise, with the first differing 80 characters of each side. MOVED = the number of lines rewritten (the words the act moved
on that export). Prints one line per name and `RICH KIND CHECK: YES|NO (<n> of <m> names; <s> lines moved in total)`. Grades nothing by itself: a market-data move between two
captures reads NO and is the issuer's to explain.
At the base (before the redeploy) the AFTER capture still holds the old words, so a before/after pair taken then reads NO wherever a kind line exists: the criterion fails at the base.
"""
import os
import re
import sys

NAMES = ["RIO_LN_Equity", "ICT_PM_Equity", "GOOGL_US_Equity", "ICICIBC_IN_Equity", "HD_US_Equity", "BA_US_Equity", "KMB_US_Equity", "TSM_US_Equity"]
KINDS = [
    re.compile(r"^Posture: (ABSENT) -- "),
    re.compile(r"^(ABSENT) -- no call was made: "),
    re.compile(r"^y/y growth rows: (ABSENT) -- "),
    re.compile(r"^[0-9E, ]+: (ABSENT) -- the block carries fiscal years "),
    re.compile(r"^Description: (ABSENT) -- "),
    re.compile(r"^Exec Management: (ABSENT) \("),
    re.compile(r"^[A-Z0-9_]+: (REFUSED) -- "),
    re.compile(r"^(ABSENT) -- no peer set supplied to this export"),
]
EXT = "md"


def _read(d, key):
    with open(os.path.join(d, key + "." + EXT), encoding="utf-8") as f:
        return f.read()


def _expected(text):
    out, moved = [], 0
    for ln in text.split("\n"):
        for rx in KINDS:
            m = rx.match(ln)
            if m:
                ln = ln[:m.start(1)] + "Not available" + ln[m.end(1):]
                moved += 1
                break
        out.append(ln)
    return "\n".join(out), moved


def _norm(text):
    return re.sub(r"\s+", " ", text).strip()


def main(argv):
    args = list(argv[1:])
    if len(args) < 2:
        print(__doc__)
        return 2
    before, after = args[0], args[1]
    keys = args[2:] or NAMES
    ok, total = 0, 0
    for key in keys:
        exp, moved = _expected(_read(before, key))
        total += moved
        ne, na = _norm(exp), _norm(_read(after, key))
        if ne == na:
            ok += 1
            print("%s: YES | MOVED %d" % (key, moved))
        else:
            i = next((n for n, (x, y) in enumerate(zip(ne, na)) if x != y), min(len(ne), len(na)))
            print("%s: NO | MOVED %d | first difference at %d: expected %r after %r" % (key, moved, i, ne[i:i + 80], na[i:i + 80]))
    print("RICH KIND CHECK: %s (%d of %d names; %d lines moved in total)" % ("YES" if ok == len(keys) else "NO", ok, len(keys), total))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
