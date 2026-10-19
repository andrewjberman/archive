"""AMGT_RESAPP round 124 (AMGT-cf-4): did the redeploy move ONLY the words `ABSENT` -> `Not available` in the printed pack?

  python r124_pack_word_swap_check.py <before_dir> <after_dir> [--ext txt|md] [KEY ...]   (dirs hold <key>.txt from r114_pack_capture_compare.py capture (the PDF text),
                                                                                      or <key>.md from capture-rich (the rich export): --ext md)

Offline (reads two folders of text). For each name: collapse all whitespace in BEFORE and AFTER, read `Not available` back as `ABSENT` in both,
and compare. YES for a name when the two are equal (the only difference between the captures is the word); NO otherwise, with the first
differing 80 characters of each side. Also prints, per name, SWAPS = (the count of `ABSENT` in BEFORE) - (the count of `ABSENT` in AFTER), which is
the number of words the act moved on that pack (0 before the redeploy takes effect; a positive number after). Prints the denominator and
`PACK WORD SWAP: YES|NO (<n> of <m> names; <s> words moved in total)`. Grades nothing by itself: a market-data move between two captures reads NO
and is the issuer's to explain, exactly as the form check does.
"""
import os
import re
import sys

NAMES = ["RIO_LN_Equity", "ICT_PM_Equity", "GOOGL_US_Equity", "ICICIBC_IN_Equity", "HD_US_Equity", "BA_US_Equity", "KMB_US_Equity", "TSM_US_Equity"]
OLD, NEW = "ABSENT", "Not available"


EXT = "txt"


def _read(d, key):
    with open(os.path.join(d, key + "." + EXT), encoding="utf-8") as f:
        return f.read()


def _norm(text):
    return re.sub(r"\s+", " ", text.replace(NEW, OLD)).strip()


def main(argv):
    if len([a for a in argv[1:] if not a.startswith("--")]) < 2:
        print(__doc__)
        return 2
    global EXT
    args = list(argv[1:])
    if "--ext" in args:
        i = args.index("--ext")
        EXT = args[i + 1]
        del args[i:i + 2]
    before, after = args[0], args[1]
    keys = args[2:] or NAMES
    ok, moved = 0, 0
    for key in keys:
        b, a = _read(before, key), _read(after, key)
        swaps = len(re.findall(r"\bABSENT\b", b)) - len(re.findall(r"\bABSENT\b", a))
        moved += swaps
        nb, na = _norm(b), _norm(a)
        if nb == na:
            ok += 1
            print("%s: YES | SWAPS %d" % (key, swaps))
        else:
            i = next((n for n, (x, y) in enumerate(zip(nb, na)) if x != y), min(len(nb), len(na)))
            print("%s: NO | SWAPS %d | first difference at %d: before %r after %r" % (key, swaps, i, nb[i:i + 80], na[i:i + 80]))
    print("PACK WORD SWAP: %s (%d of %d names; %d words moved in total)" % ("YES" if ok == len(keys) else "NO", ok, len(keys), moved))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
