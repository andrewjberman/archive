"""HVST-f-1 AC2: for every form with added hits, up to 10 added hits with their surrounding words. Read-only."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402


def main():
    securities, articles, rows = C.compute()
    hit_rows = [r for r in rows if r["hits"]]
    print("== HVST-f-1 AC2: added-hit sample for the text read ==")
    print("seed=%d; per form: all hits if <=%d, else %d drawn by random.Random('<seed>|<class>|<form>|<security_key>'), "
          "shown in article/offset order; forms with added hits=%d of %d generated; articles=%d" % (
              C.SEED, C.SAMPLE_N, C.SAMPLE_N, len(hit_rows), len(rows), len(articles)))
    print("match is marked [[like this]]; block = title or `block i` of the served text_blocks; offset = character offset in that text")
    total = 0
    for r in sorted(hit_rows, key=lambda r: (C.CLASSES.index(r["class"]), r["form"], r["security_key"])):
        s = C.sample(r)
        total += len(s)
        print()
        print("--- %s | form=%r | %s (%s) | sample %d of %d added hits (added pairs=%d) | %s" % (
            r["class"].split(" ")[0], r["form"], r["security_key"], r["company"], len(s), len(r["hits"]),
            r["pairs"], ";".join(r["flags"]) or "no flag"))
        for h in s:
            print("  article=%s | headline=%s | %s | offset=%d | %s" % (
                h["article_key"], h["headline"][:90], h["where"], h["offset"], h["context"].replace("\n", " ")))
    print()
    print("forms sampled=%d; hits shown=%d" % (len(hit_rows), total))


if __name__ == "__main__":
    main()
