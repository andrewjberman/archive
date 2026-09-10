#!/usr/bin/env bash
# F4-AC4 -- THE SERVED GRAPH ANSWERS FOR THE STITCH TYPES, with the stitch vintage on
# the VINTAGE line and the pointer advanced. TO-CG-F-4 step 3.
#
# EVERY NUMBER IS READ THROUGH THE THIN CLIENT a human would use -- `bash .tools/comp-kuzu`
# in a subprocess -- so the VINTAGE line parsed here is the literal line the CLI prints on
# stderr, not a reconstruction from the service's JSON. The pointer is read from S3.
#
# TWO THINGS THE CRITERION'S OWN TEXT GETS WRONG, both measured and both printed:
#  * it calls the pre-fold answer "0 of 3"; it was 1 of 3, because API_ROUTE is a
#    derive-produced type and always has been (row W2-S47). SERVED_STITCH_TYPES is
#    therefore NOT the discriminator -- GOLD_SCRIPT is, and it is printed on its own line.
#  * it expects the stitch vintage from _provenance.format_provenance_header; no serve path
#    calls that. The vintage rides projection_worker's age_line, which IS the first half of
#    the CLI's VINTAGE line (row W2-S46, accepted by the issuer 20:1xZ).
#
# The stitch-v1 stamp is counted on `n.props`, not `n.vocabulary`: the property is not a
# fixed column -- _props_and_guard lands every non-fixed node key in the additive props
# JSON -- and the live service refuses the column form with "Binder exception: Cannot find
# property vocabulary for n." (row W2-S51). The refusal is EXERCISED below, not asserted.
#
# ONE ENVIRONMENT TRAP, fixed rather than worked around: a bare `bash` from a Python
# subprocess on this box resolves to the WSL stub, which answers nothing and leaves the
# reader looking like a graph with no rows. The bash actually executing this script is
# exported and used, so the subprocess runs the SAME interpreter as the caller.
#
# Run from the repository root.
set -u
BASH_BIN="$(command -v bash)"
export BASH_BIN

python - <<'PY'
import datetime
import json
import os
import re
import subprocess

import boto3

BASH = os.environ.get("BASH_BIN") or "bash"

BUCKET = "opal-313476888478-globgrph"
POINTER_BEFORE = "projection/2026-09-09T20:04:09.034708+00:00/"
Q_TYPES = ("MATCH (n:CloudNode) WHERE n.node_type IN ['GOLD_SCRIPT','S3_DATA_KEY','API_ROUTE'] "
           "RETURN n.node_type AS t, count(*) AS c ORDER BY t")
Q_STAMP = "MATCH (n:CloudNode) WHERE n.props CONTAINS 'stitch-v1' RETURN count(*) AS c"
Q_COLUMN = "MATCH (n:CloudNode) WHERE n.vocabulary = 'stitch-v1' RETURN count(*) AS c"

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def kuzu(q):
    """Run the thin client exactly as a reader would. Returns (rows, vintage_line)."""
    p = subprocess.run([BASH, ".tools/comp-kuzu", "--json", q],
                       capture_output=True, text=True)
    line = ""
    for ln in (p.stderr or "").splitlines():
        if ln.startswith("VINTAGE:"):
            line = ln.strip()
    try:
        rows = json.loads(p.stdout)
    except Exception:  # noqa: BLE001
        rows = None
    return rows, line, (p.stderr or "").strip()


rows, vline, err = kuzu(Q_TYPES)
counts = {r["t"]: r["c"] for r in (rows or [])}
non_zero = sum(1 for t in ("GOLD_SCRIPT", "S3_DATA_KEY", "API_ROUTE") if counts.get(t, 0) > 0)

stamp_rows, _, _ = kuzu(Q_STAMP)
stamped = (stamp_rows or [{}])[0].get("c", 0) if stamp_rows else 0
col_rows, _, col_err = kuzu(Q_COLUMN)

s3 = boto3.client("s3", region_name="us-east-1")
ptr = json.loads(s3.get_object(Bucket=BUCKET, Key="projection/current.json")["Body"].read())
prefix_now = ptr.get("artifact_prefix")
advanced = prefix_now != POINTER_BEFORE

m = re.search(r"Stitch source: (\S+) built (\S+?)\.", vline)
has_stitch = bool(m)
stitch_producer = m.group(1) if m else None
stitch_built_at = m.group(2) if m else None

print("F4-AC4 -- THE SERVED GRAPH ANSWERS FOR THE STITCH TYPES")
print("  live read at: %s   (through %s .tools/comp-kuzu, the reader's own path)" % (now, BASH))
print()
print("SERVED_STITCH_TYPES=%d of 3 non-zero" % non_zero)
for t in ("API_ROUTE", "GOLD_SCRIPT", "S3_DATA_KEY"):
    print("%s=%d" % (t, counts.get(t, 0)))
print("STITCH_V1_STAMPED=%d" % stamped)
if has_stitch:
    print("VINTAGE_HAS_STITCH=true stitch_built_at=%s stitch_producer=%s"
          % (stitch_built_at, stitch_producer))
else:
    print("VINTAGE_HAS_STITCH=false stitch_built_at=(absent)")
print("POINTER_ADVANCED=%s" % ("true" if advanced else "false"))
print()
print("  -- the VINTAGE line, verbatim, as the CLI printed it --")
print("     %s" % (vline or "(no VINTAGE line)"))
print()
print("  -- the pointer --")
print("     before this order's derive : %s" % POINTER_BEFORE)
print("     now                        : %s" % prefix_now)
print("     manifest_sha256            : %s" % ptr.get("manifest_sha256"))
print()
print("  -- the CONTROLS --")
print("     PRE-FOLD, measured before the image act: API_ROUTE=86, GOLD_SCRIPT=0,")
print("     S3_DATA_KEY=0 -> 1 of 3 non-zero. So SERVED_STITCH_TYPES was ALREADY")
print("     satisfied by an unfolded graph (row W2-S47); GOLD_SCRIPT is the limb that")
print("     discriminates, and API_ROUTE is the positive control on a type the")
print("     projection already carried.")
print("     THE STAMP IS ON props, NOT ON A COLUMN, and the refusal is exercised here:")
print("       %s" % Q_COLUMN)
print("       -> %s" % (("rows=%s" % col_rows) if col_rows is not None
                        else col_err.splitlines()[0] if col_err else "(no answer)"))
print("       so STITCH_V1_STAMPED above is counted on n.props CONTAINS 'stitch-v1'")
print("       (row W2-S51). A count taken on the column form would be a crash, not a 0.")
print()
print("  DENOMINATOR: 3 of 3 node types the criterion names, in ONE statement against the "
      "served graph; 1 of 1 pointer read from S3; 3 of 3 thin-client calls (types, stamp, "
      "and the column-form control); the VINTAGE line is 1 of 1, parsed from the CLI's own "
      "stderr.")
PY
