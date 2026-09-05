#!/usr/bin/env python
# NFRA_CLDGRPH.TO-CG-D-9 limb (i) section 3 helper -- the derive-runner log-stream census.
# Author: 0.9.0_WK_NFRA_CLDGRPH~1. Pure read; writes nothing.
# This is the POSITIVE CONTROL for "exactly one derive ran in the window": it lists every
# derive stream with its event span, so a one is provably a one and a zero provably a zero.
# It replaces a shell loop that spawned two python processes PER ROW (16 spawns on this box) and
# that fed the aws shim's trailing CR into a digit guard -- which skipped every row and printed
# NOTHING. A control that reads as silence is a dead arm, not a pass.
import datetime
import os
import sys


def iso(ms):
    return datetime.datetime.fromtimestamp(
        int(ms) / 1000, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


want = os.environ.get("DERIVE_TASK", "")
rows = 0
for line in sys.stdin:
    parts = line.rstrip().split("\t")
    if len(parts) < 3:
        continue
    name, first_ms, last_ms = parts[0], parts[1], parts[2]
    if not (first_ms.isdigit() and last_ms.isdigit()):
        continue          # --max-items appends a pagination-token row with no timestamps
    fi, li = iso(first_ms), iso(last_ms)
    inw = "IN_WINDOW" if ("2026-09-04T21" <= fi < "2026-09-05T06") else "OUT"
    mine = "  <== the task CloudTrail names" if want and name.endswith(want) else ""
    print("  %s  %s  %s -> %s%s" % (inw, name, fi, li, mine))
    rows += 1
print("  DERIVE_STREAMS_LISTED=%d (positive control: a zero here would be a DEAD ARM,"
      " not a clean night)" % rows)
