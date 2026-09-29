"""HVST-f-1 AC4 (JUDGMENT, PRESENTED NOT GRADED): AC2's sample grouped by form for the CVO's text read.
Question for 3.0.0_SA_CVO~Z at L9: per form, how many sampled hits are the company? No verdict is recorded here."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402


def main():
    _sec, _arts, rows = C.compute()
    print("status=UNVERIFIABLE-BY-INSTRUMENT (graded by 3.0.0_SA_CVO~Z at L9; this script records NO verdict)")
    print("QUESTION per form: how many of the sampled hits below are the company?")
    by_form = {}
    for r in rows:
        if r["hits"]:
            by_form.setdefault((C.CLASSES.index(r["class"]), r["form"]), []).append(r)
    for (ci, form), rs in sorted(by_form.items()):
        print()
        print("##### FORM %r (%s) -- owner(s): %s" % (form, C.CLASSES[ci].split(" ")[0],
              "; ".join("%s (%s)" % (r["security_key"], r["company"]) for r in rs)))
        for r in rs:
            s = C.sample(r)
            print("  [%s] sample %d of %d added hits; flags: %s" % (
                r["security_key"], len(s), len(r["hits"]), ";".join(r["flags"]) or "none"))
            for i, h in enumerate(s, 1):
                print("   %2d. %s | %s | %s" % (i, h["headline"][:70], h["where"], h["context"].replace("\n", " ")))
            print("   sampled hits that are the company: ____ of %d   (CVO to fill at L9)" % len(s))


if __name__ == "__main__":
    main()
