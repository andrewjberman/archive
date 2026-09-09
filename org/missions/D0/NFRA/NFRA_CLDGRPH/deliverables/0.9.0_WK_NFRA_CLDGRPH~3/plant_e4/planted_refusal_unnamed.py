#!/usr/bin/env python3
"""E4-AC2 NEGATIVE CONTROL -- a _stitch_freshness whose refusals name nothing.

Same function name, same two raise sites, same `%`-formatted and implicitly
concatenated strings as the real file, and NEITHER text carries the home token
or the cell id. Fed through the SAME reader as comp_debt.py. If the reader
scores this 2 of 2, the real 2 of 2 is a constant.

Never imported, never run.
"""
import os

STITCH_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kuzu_stitch_db")
STITCH_STALE_HOURS = 48.0


def freshness_assert():
    raise SystemExit("REFUSE: the served cloud graph is unreachable -- this is the "
                     "NESSIE surface's refusal and must be reported OUT-OF-SCOPE.")


def _stitch_freshness(allow_stale: bool):
    if not os.path.exists(STITCH_DB):
        raise SystemExit("REFUSE: kuzu_stitch_db not found at %s -- the REACHABILITY "
                         "stitch surface." % STITCH_DB)
    age_h = 999.0
    if not allow_stale:
        raise SystemExit("REFUSE: kuzu_stitch_db is STALE (age %.0fh > %.0fh) -- a "
                         "REACHABILITY sweep over a stale stitch phantoms orphans. "
                         "Re-run derive_stitch or pass --allow-stale."
                         % (age_h, STITCH_STALE_HOURS))
    return "current", age_h
