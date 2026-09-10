#!/usr/bin/env python3
"""
run_gate.py -- the TRADING-DAY GATE around the composer (cell RP-s-16, manifest row S3, outcome FWD-1)

Wraps `compose_edition.py` (RP-s-15's composer -- unedited, not touched by this cell) with the ONE
frontier CLAUDE.md NEVER#4 and this project's own round-1 law (`SCHEDULE.md`, cell RP-s-3) name:
`lib/trading_calendar.py`, resolved from a DERIVED repo root (`git rev-parse --show-toplevel`),
never a hardcoded literal and never a bare basename (SCHEDULE.md sec.2's basename trap -- five
files share that name; this script imports the package path `lib.trading_calendar`, which only
resolves to the canonical source, never to one of the three vendored Lambda-deploy copies).
NEVER a weekday check (`date.weekday() < 5`). NEVER a calendar-day subtraction.

WHAT THIS DOES: reads a gating date (today, UTC, unless `--date` overrides it for the
demonstration `RUN_AND_DELIVERY.md` sec.2 records), asks the canonical frontier's
`is_trading_day()`, and ONLY IF that returns True runs the composer (subprocess: the exact
`python compose_edition.py` a human would run by hand) to produce a real edition. On a
non-trading day it does NOT run the composer, prints why, and exits 0 -- no fallback to "run
anyway, it's a weekday."

WHAT THIS DOES NOT DO, BY WRITE SURFACE AND BY THE STANDING MORATORIUM: mint, edit or touch any
SNS topic, CloudWatch alarm, subscription or EventBridge rule. The recurring TRIGGER (what
invokes this script every trading morning, before Andrew's morning) and the DESTINATION EGRESS
(what carries the resulting `EDITION_SPECIMEN.md` to Andrew) are both infra/scheduler artifacts
outside `org/missions/D12/NFRA/NFRA_REPORT/deliverables/` -- outside this cell's paths -- and are
named, not built, in `RUN_AND_DELIVERY.md` sections 3-4, the same declared limit round 1's
`SCHEDULE.md` sec.6 stated for itself ("does not build a new scheduler, EventBridge rule, or cron
expression -- this is a LAW cell, not a wiring cell").
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _toplevel() -> str:
    """Resolve the repo root by git, from THIS file's own directory -- never a hardcoded
    literal, never the caller's cwd. Per CLAUDE.md LD-0405: workspace root is obtained via
    `git rev-parse --show-toplevel`, never written as a device-specific literal path."""
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=HERE, capture_output=True, text=True, timeout=15,
    )
    if out.returncode != 0 or not out.stdout.strip():
        raise RuntimeError(
            "cannot resolve repo root via git rev-parse --show-toplevel: rc=%s stderr=%r"
            % (out.returncode, out.stderr)
        )
    return out.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--date", default=None,
        help="ISO date (YYYY-MM-DD) to gate on. DEMONSTRATION/TEST HOOK ONLY -- a real "
             "trading-morning trigger calls this with no --date and gates on today (UTC).",
    )
    args = ap.parse_args()

    toplevel = _toplevel()
    if toplevel not in sys.path:
        sys.path.insert(0, toplevel)
    from lib.trading_calendar import is_trading_day, calendar_source  # the ONE frontier, resolved

    today = args.date or dt.datetime.utcnow().strftime("%Y-%m-%d")
    frontier = os.path.join(toplevel, "lib", "trading_calendar.py")

    print("OK: frontier = %s" % frontier)
    print("OK: calendar_source = %s" % calendar_source())
    print("OK: gating date = %s" % today)

    if not is_trading_day(today):
        print(
            "SKIP: %s is not an NYSE trading day (lib/trading_calendar.is_trading_day) -- the "
            "composer is NOT run and NO edition is produced or delivered today. This is the "
            "exact case that a weekday-only check got wrong on 2026-09-07 (Labor Day, a Monday)."
            % today
        )
        return 0

    composer = os.path.join(HERE, "compose_edition.py")
    print("OK: %s IS an NYSE trading day -- running the composer for real." % today)
    result = subprocess.run(
        [sys.executable, composer], cwd=HERE, capture_output=True, text=True,
    )
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
