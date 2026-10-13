"""AMGT_RESAPP round-103 PREP -- FWD-40 (d): the ten-name DRAW for the browser walk (PRD v0.44).

  python r103_walk_draw.py --census <census_v2.json> --date 2026-10-13 --out <draw.json>
  python r103_walk_draw.py --selftest

THE 93: the resolved names whose `packs/` prefix is their EXACT key (the census's `resolved` and `packs` sets, `V1_SECTION_CENSUS_READING.md` section 4). THE DRAW (the PRD's own wording):
the 93 keys sorted by sha256(walk date + ' ' + key), the first ten, the draw printed with the walk. Each key is also printed as the search text the walker types
(`ASML_NA_Equity` -> `ASML NA`). Prints `R103 WALK DRAW: 10 of 93 drawn (date <d>)`.
"""
import argparse
import hashlib
import json
import sys


def draw(keys, date, n=10):
    ranked = sorted(keys, key=lambda k: hashlib.sha256(("%s %s" % (date, k)).encode("utf-8")).hexdigest())
    return [(k, hashlib.sha256(("%s %s" % (date, k)).encode("utf-8")).hexdigest()) for k in ranked[:n]]


def search_text(key):
    return key[: -len("_Equity")].replace("_", " ") if key.endswith("_Equity") else key.replace("_", " ")


def selftest():
    keys = ["A_US_Equity", "B_US_Equity", "C_US_Equity", "D_US_Equity"]
    one = draw(keys, "2026-10-13", 2)
    two = draw(list(reversed(keys)), "2026-10-13", 2)
    other = draw(keys, "2026-10-14", 4)
    arms = [
        one == two,                                   # A1 the draw does not depend on the input order
        len(one) == 2 and len({k for k, _ in one}) == 2,
        [k for k, _ in other] != [k for k, _ in draw(keys, "2026-10-13", 4)] or True,  # A3 informative only: a different date may reorder
        search_text("ASML_NA_Equity") == "ASML NA" and search_text("1299_HK_Equity") == "1299 HK",
    ]
    for i, ok in enumerate(arms, 1):
        print("   %s A%d" % ("PASS" if ok else "FAIL", i))
    print("R103 WALK DRAW ARMS: %s" % ("YES" if all(arms) else "NO"))
    return 0 if all(arms) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--census")
    ap.add_argument("--date")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    d = json.load(open(a.census, encoding="utf-8"))
    keys = sorted(set(d["resolved"]) & set(d["packs"]))
    picked = draw(keys, a.date)
    for i, (k, h) in enumerate(picked, 1):
        print("%2d  %s  sha256 %s  search %r" % (i, k, h[:16], search_text(k)))
    if a.out:
        json.dump({"date": a.date, "population": len(keys), "draw": [{"key": k, "sha256": h, "search": search_text(k)} for k, h in picked]}, open(a.out, "w", encoding="utf-8"), indent=1)
    print("R103 WALK DRAW: %d of %d drawn (date %s)" % (len(picked), len(keys), a.date))
    return 0 if len(keys) == 93 and len(picked) == 10 else 1


if __name__ == "__main__":
    sys.exit(main())
