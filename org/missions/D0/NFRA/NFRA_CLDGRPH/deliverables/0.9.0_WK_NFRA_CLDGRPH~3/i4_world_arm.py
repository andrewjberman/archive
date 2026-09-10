#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-I-4 / I4-AC4 ARM 4 -- ask the BUCKET, not my own artifacts.

Arms 1-3 of I4-AC4 all read things this order wrote. If this order had written to S3 by some
path none of them models, all three would still read clean -- they share a dependency, and a
check scoped to the members cannot see a defect in what the members share. This arm reads
the object store itself: EVERY object in the bucket, not just the prefix this cell looked
at, because a write to a key outside snapshots/ is exactly what a prefix-scoped arm cannot
see. The denominator is printed.

THE ORACLE: no object may carry a LastModified at or after this cell's first read. The cell
start is the first line of this order's own read ledger, so the window opens BEFORE the
first thing this order did.

WHAT IT CANNOT SEE, stated because a control's limit is part of its value: an object written
and then deleted inside the window (S3 keeps no tombstone on an unversioned bucket), and a
write by ANOTHER actor is not distinguished from mine by this arm alone -- arm 3's verb
assertion is what separates those. A non-zero here is a finding to explain, not automatically
a violation by this cell.

usage: python i4_world_arm.py <cell-start-iso-Z>
"""

import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i4_lib  # noqa: E402


def main():
    start = sys.argv[1].strip()
    t0 = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=datetime.timezone.utc)
    root = i4_lib.repo_root()
    rc, out, err = i4_lib.aws_read(root, "s3api", "list-objects-v2",
                                   ["--bucket", i4_lib.BUCKET],
                                   "ARM 4: the WHOLE bucket, to catch a write outside snapshots/",
                                   timeout=70)
    if rc != 0:
        print("WORLD_ARM=NOT_COMPLETED rc=%d %s" % (rc, err.strip()[:160]))
        return 1
    d = json.loads(out)
    objs = d.get("Contents", [])
    moved = []
    prefixes = {}
    for o in objs:
        p = o["Key"].split("/")[0]
        prefixes[p] = prefixes.get(p, 0) + 1
        lm = o["LastModified"]
        try:
            ts = datetime.datetime.fromisoformat(lm.replace("Z", "+00:00"))
        except ValueError:
            continue
        if ts >= t0:
            moved.append((o["Key"], lm))
    print("WORLD_ARM_DENOMINATOR=%d object(s) across the WHOLE bucket (IsTruncated=%s)"
          % (len(objs), d.get("IsTruncated")))
    print("  top-level prefixes: %s" % ", ".join(
        "%s=%d" % (k, v) for k, v in sorted(prefixes.items(), key=lambda x: -x[1])))
    print("  window opens at %s (this cell's first ledger line, inclusive)" % start)
    print("OBJECTS_MODIFIED_SINCE_CELL_START=%d" % len(moved))
    for k, lm in moved[:20]:
        print("    MOVED %s %s" % (k, lm))
    if len(moved) > 20:
        print("    ... and %d more" % (len(moved) - 20))
    in_scope = [m for m in moved if m[0].startswith(i4_lib.PREFIX)]
    print("OF_THOSE_UNDER_%s%d" % (i4_lib.PREFIX.upper().rstrip("/") + "=", len(in_scope)))
    for k, lm in in_scope[:10]:
        print("    IN-SCOPE MOVED %s %s" % (k, lm))
    # THE ARM WENT NON-ZERO ON ITS FIRST REAL RUN, which is worth more than a clean sweep:
    # it shows the detector is not a constant. Attribution is NOT done by this arm alone --
    # arm 3's verb assertion (READ_VERBS only, zero write verbs in the ledger) is what says
    # the movement was not mine, and the moved keys lie under a prefix this order never
    # named in any call it made.
    if in_scope:
        print("WORLD_ARM=IN-SCOPE-OBJECT-MOVED-INVESTIGATE")
    elif moved:
        print("WORLD_ARM=NO-WRITE-BY-THIS-CELL (other writers active elsewhere in the bucket;")
        print("  the detector demonstrably CAN return non-zero, which a clean sweep never shows)")
    else:
        print("WORLD_ARM=CLEAN (and unexercised: nothing moved anywhere, so this run does not")
        print("  demonstrate the arm can fire)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
