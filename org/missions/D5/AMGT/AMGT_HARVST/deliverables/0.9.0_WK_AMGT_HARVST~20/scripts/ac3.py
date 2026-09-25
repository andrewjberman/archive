"""HVST-s-1 AC3 -- publisher_coverage run PURE over the POST-RUN listing_hit rows. No write."""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import snapshot_lib  # noqa: E402
from lib.research.harvest.publication_gold import publisher_coverage  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
SECURITIES = pathlib.Path("org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~4/securities.json")


def main():
    counts, rows = snapshot_lib.load(HERE / "after.pickle")
    securities = json.loads(SECURITIES.read_text(encoding="utf-8"))
    print("AC3 -- publisher_coverage(listing_hit_rows, securities), PURE, no I/O inside the function")
    print("  listing_hit rows fed in: %d (every row of every publisher's silver, the AC2 AFTER snapshot)"
          % len(rows))
    print("  securities fed in: %d (denominator) from %s" % (len(securities), SECURITIES))
    print("  columns present on a listing_hit row: %s"
          % (sorted(rows[0].keys()) if rows else "NO ROWS AT ALL"))

    coverage = publisher_coverage(rows, securities)
    sa_hits = 0
    for security in securities:
        key = security.get("security_key")
        spans = coverage.get(key) or {}
        rendered = {pub: (str(span[0]), str(span[1])) for pub, span in sorted(spans.items())}
        sa_span = spans.get("sa")
        if sa_span is not None:
            sa_hits += 1
        print("  %-16s sa span = %s ; every publisher span = %s"
              % (key, ("(%s, %s)" % (sa_span[0], sa_span[1])) if sa_span else "NONE", rendered or "{}"))
    print("  sa spans %d of %d" % (sa_hits, len(securities)))

    covered_any = sum(1 for s in securities if (coverage.get(s.get("security_key")) or {}))
    print("  POSITIVE CONTROL on the same call: %d of %d securities yield a NON-EMPTY span map from some "
          "publisher, so a 0 for sa is a true zero and not a reader that sees nothing."
          % (covered_any, len(securities)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
