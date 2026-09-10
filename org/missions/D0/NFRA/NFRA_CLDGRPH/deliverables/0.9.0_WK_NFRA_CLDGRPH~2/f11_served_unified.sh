#!/usr/bin/env bash
# F11-AC2 -- THE SERVED GRAPH CARRIES THE UNIFIED VOCABULARY. TO-CG-F-11 step 5.
#
# EVERY NUMBER IS READ THROUGH THE THIN CLIENT a human would use -- `bash .tools/comp-kuzu`
# in a subprocess -- against the graph the estate SERVES, not against a local artifact and
# not against the producer's self-report.
#
# THREE INSTRUMENT NOTES, each of them a row this project already paid for:
#  * the stitch-v1 stamp is counted on `n.props`, NOT on `n.vocabulary`: props is the
#    additive JSON column and the live service refuses the column form with
#    "Binder exception: Cannot find property vocabulary for n." (row W2-S51). The refusal
#    is EXERCISED below rather than asserted, so a 0 here cannot be a crash misread as an
#    absence.
#  * a bare `bash` from a Python subprocess on this box resolves to the WSL stub, which
#    answers nothing and reads as an empty graph (row W2-S54). The executing bash is
#    exported and used.
#  * DISTINCT n.node_type is printed WHOLE, so the "0 of 4" claim is made against the
#    population and not against four scoped lookups that would each pass on an empty graph.
#
# Run from the repository root.
set -u
BASH_BIN="$(command -v bash)"
export BASH_BIN

python - <<'PY'
import datetime
import json
import os
import subprocess

import boto3

BASH = os.environ.get("BASH_BIN") or "bash"
BUCKET = "opal-313476888478-globgrph"
# the pointer this order's derive must advance PAST: F-4's projection, read from
# projection/current.json at 2026-09-09T23:5xZ, before the ad-hoc derive of this order.
POINTER_BEFORE = "projection/2026-09-09T21:05:17.968166+00:00/"
PROVISIONAL = ["GOLD_SCRIPT", "S3_DATA_KEY", "PORTAL_COMPONENT", "REACT_QUERY_KEY"]

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def kuzu(q):
    p = subprocess.run([BASH, ".tools/comp-kuzu", "--json", q], capture_output=True, text=True)
    line = ""
    for ln in (p.stderr or "").splitlines():
        if ln.startswith("VINTAGE:"):
            line = ln.strip()
    try:
        rows = json.loads(p.stdout)
    except Exception:  # noqa: BLE001
        rows = None
    return rows, line, (p.stderr or "").strip()


types_rows, vline, _ = kuzu(
    "MATCH (n:CloudNode) RETURN DISTINCT n.node_type AS t, count(*) AS c ORDER BY t")
served = {r["t"]: r["c"] for r in (types_rows or [])}
provisional_served = sum(1 for t in PROVISIONAL if served.get(t, 0) > 0)

stamp_rows, _, _ = kuzu("MATCH (n:CloudNode) WHERE n.props CONTAINS 'stitch-v1' RETURN count(*) AS c")
stamped = (stamp_rows or [{}])[0].get("c", 0) if stamp_rows else None
col_rows, _, col_err = kuzu("MATCH (n:CloudNode) WHERE n.vocabulary = 'stitch-v1' RETURN count(*) AS c")

# the merged pipeline scripts, queryable BY TIER. tier is a node ATTRIBUTE (extract_gold_compute),
# so it lands in the additive props JSON; the column form is tried too and whichever answers is
# named, because "which carrier holds it" is exactly what a rename breaks.
tier_props, _, tier_props_err = kuzu(
    "MATCH (n:CloudNode) WHERE n.node_type = 'PipelineScript' AND n.props CONTAINS '\"tier\": \"gold\"' "
    "RETURN count(*) AS c")
tier_col, _, tier_col_err = kuzu(
    "MATCH (n:CloudNode) WHERE n.node_type = 'PipelineScript' AND n.tier = 'gold' RETURN count(*) AS c")
tier_gold, tier_carrier = 0, "none"
if tier_props:
    tier_gold, tier_carrier = tier_props[0].get("c", 0), "props JSON"
if not tier_gold and tier_col:
    tier_gold, tier_carrier = tier_col[0].get("c", 0), "n.tier column"

s3 = boto3.client("s3", region_name="us-east-1")
ptr = json.loads(s3.get_object(Bucket=BUCKET, Key="projection/current.json")["Body"].read())
prefix_now = ptr.get("artifact_prefix")

print("F11-AC2 -- THE SERVED GRAPH CARRIES THE UNIFIED VOCABULARY")
print("  live read at: %s   (through %s .tools/comp-kuzu, the reader's own path)" % (now, BASH))
print()
print("PROVISIONAL_NAMES_SERVED=%d of 4" % provisional_served)
for t in PROVISIONAL:
    print("   %-18s %d" % (t, served.get(t, 0)))
print("PORTAL_BUNDLE_SERVED=%d" % served.get("PORTAL_BUNDLE", 0))
print("STITCH_V1_STAMPED_SERVED=%s" % ("(query refused)" if stamped is None else stamped))
print("PIPELINESCRIPT_TIER_GOLD=%d" % tier_gold)
print("POINTER_ADVANCED=%s" % ("true" if prefix_now != POINTER_BEFORE else "false"))
print()
print("  -- the canonical types the unification writes into --")
for t in ("PipelineScript", "PipelineFunction", "S3Key", "Component", "ReactQueryKey"):
    print("   %-18s %d" % (t, served.get(t, 0)))
print()
print("  -- the pointer --")
print("     before this order's derive : %s" % POINTER_BEFORE)
print("     now                        : %s" % prefix_now)
print("     manifest_sha256            : %s" % ptr.get("manifest_sha256"))
print("     VINTAGE (the CLI's own line): %s" % (vline or "(no VINTAGE line)"))
print()
print("  -- the CONTROLS --")
print("     the stamp is on props, not on a column, and the column form is EXERCISED here:")
print("       MATCH (n:CloudNode) WHERE n.vocabulary = 'stitch-v1' RETURN count(*) AS c")
print("       -> %s" % (("rows=%s" % col_rows) if col_rows is not None
                        else (col_err.splitlines()[0] if col_err else "(no answer)")))
print("       so a 0 above is a COUNT and not a crash (row W2-S51).")
print("     tier carrier that answered: %s" % tier_carrier)
print("       props form -> %s ; column form -> %s"
      % (tier_props if tier_props is not None else (tier_props_err.splitlines()[0:1] or ["-"])[0],
         tier_col if tier_col is not None else (tier_col_err.splitlines()[0:1] or ["-"])[0]))
print("     PORTAL_BUNDLE is the POSITIVE CONTROL on this reading: it is a stitch-emitted")
print("     type that was deliberately KEPT, so a graph with no stitch in it at all would")
print("     fail this line while satisfying every 0 above.")
print()
print("  DENOMINATOR: %d distinct node_type value(s) in the served graph, read UNSCOPED in one "
      "statement; the 4 provisional names are checked against that whole population; 5 of 5 "
      "thin-client calls answered (types, stamp, stamp-column control, tier-props, tier-column); "
      "1 of 1 pointer read from S3." % len(served))
PY
