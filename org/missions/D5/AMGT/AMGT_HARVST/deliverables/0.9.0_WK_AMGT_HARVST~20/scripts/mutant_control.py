"""HVST-s-1 mutant control: the AC2 delta comparison must report a NON-ZERO delta against a
FABRICATED before-state, proving +0 is a measurement and not a constant. READ ONLY."""

import copy
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import snapshot_lib  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent


def delta(before, after, publisher):
    """The IDENTICAL arithmetic ac2.py runs."""
    return (after[publisher]["silver_listing_hit_rows"] - before[publisher]["silver_listing_hit_rows"],
            after[publisher]["bronze_news_listing_objects"] - before[publisher]["bronze_news_listing_objects"])


def main():
    before, _ = snapshot_lib.load(HERE / "before.pickle")
    after, _ = snapshot_lib.load(HERE / "after.pickle")
    real = delta(before, after, "sa")
    print("REAL   before sa silver=%d bronze=%d ; after sa silver=%d bronze=%d ; delta silver=%+d bronze=%+d"
          % (before["sa"]["silver_listing_hit_rows"], before["sa"]["bronze_news_listing_objects"],
             after["sa"]["silver_listing_hit_rows"], after["sa"]["bronze_news_listing_objects"],
             real[0], real[1]))

    mutant = copy.deepcopy(before)
    mutant["sa"]["silver_listing_hit_rows"] = 3
    mutant["sa"]["bronze_news_listing_objects"] = 1
    fired = delta(mutant, after, "sa")
    print("MUTANT before sa silver=3 bronze=1 (FABRICATED) ; same after-read ; delta silver=%+d bronze=%+d"
          % (fired[0], fired[1]))
    ok = fired != (0, 0) and real == (0, 0)
    print("MUTANT %s: the same delta code reports %+d/%+d against a fabricated before and %+d/%+d against the "
          "measured one." % ("FIRED AS EXPECTED" if ok else "DID NOT FIRE -- deliverable INVALID",
                             fired[0], fired[1], real[0], real[1]))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
