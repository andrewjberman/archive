"""HVST-f-1 MUTANT CONTROL: the census must be able to see. Break the span reader (spans() returns nothing) and
the census of form 'T' for AT&T must fall from its real added-hit count to 0; with the real reader it must be > 0.
Read-only."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402


def total_added(securities, articles):
    sec = next(s for s in securities if s["security_key"] == "T_US_Equity")
    return sum((C.added_for(a, sec, "T") or {"added_count": 0})["added_count"] for a in articles)


def main():
    securities = C.load_securities()
    articles = C.load_articles()
    real = total_added(securities, articles)
    original = C.spans
    C.spans = lambda text, aliases: []
    try:
        mutant = total_added(securities, articles)
    finally:
        C.spans = original
    print("form 'T' added hits over %d articles: real reader=%d; mutant reader (spans() returns nothing)=%d" % (len(articles), real, mutant))
    print("MUTANT " + ("KILLED" if real > 0 and mutant == 0 else "SURVIVED"))


if __name__ == "__main__":
    main()
