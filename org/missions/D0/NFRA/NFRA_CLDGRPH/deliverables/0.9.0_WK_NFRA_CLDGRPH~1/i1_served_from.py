#!/usr/bin/env python3
"""i1_served_from.py -- NFRA_CLDGRPH CG-s-41, deliverable 5.

SERVED_FROM's 27 EDGES, SHOWN SAFE BY THE SAME ARM RATHER THAN BY ARGUMENT.

The cell states that SERVED_FROM is "still loaded on it": 27 edges, all 27 on the
same parent class, same collision, same Lambda path, untouched family. The
argument that the fix covers them is easy to make and worth nothing. This script
makes the demonstration instead:

  1. MEASURE the 27 live, from the warehouse -- which edges, on which endpoint
     string, resolving to which node, and whether that node is still alive.
  2. RESOLVE them with the SERVED loader's OWN key rule (graph_key, extracted by
     content from kuzu_nessie_load.py), not with a restatement of it. Two rules
     for one question is the defect that file's docstring exists to record.
  3. RUN THE SAME ARM i1_arm.py ran -- a real local Iceberg table, the real
     table.overwrite verb, the PRE-FIX predicate then the POST-FIX predicate --
     seeded with the REAL endpoint strings and the REAL node rows, and count how
     many of the 27 lose their endpoint in each arm.

RED FIRST here too: if the pre-fix arm does not orphan the 27, the fixture cannot
represent the failure and nothing below would score it.

READS ONLY on the estate side. Nothing is deployed, nothing is written to S3.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
import types
from pathlib import Path

T0 = time.time()
HERE = Path(__file__).resolve().parent
REPO = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True).stdout.strip())
os.chdir(REPO)
LAMBDA_REL = "infra/aws/lambda/globgrph/incremental_updater/lambda_function.py"
LOADER_REL = "infra/aws/globgrph/kuzu_nessie_load.py"
WH_REL = ".scratch/i1_sf_wh"
MARKER_BUCKET = "opal-313476888478-globgrph"
MARKER_KEY = "warehouse/_branch_head.main.json"

HEAD = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
print("=" * 78)
print("i1_served_from.py -- CG-s-41 -- SERVED_FROM's 27, DEMONSTRATED NOT ASSERTED")
print("=" * 78)
print("TREE_READ cwd    = %s" % os.getcwd())
print("TREE_READ branch = %s" % subprocess.run(
    ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip())
print("TREE_READ head   = %s" % HEAD)
print()

import boto3  # noqa: E402
# Imported HERE, after the header block, ON PURPOSE: the TREE_READ lines above
# must print before any third-party import can fail, so a missing pyiceberg is
# reported against a KNOWN tree rather than as a bare traceback. E402 waived
# per-line with the reason stated, not silenced file-wide.
import pyarrow as pa  # noqa: E402
from pyiceberg.catalog.sql import SqlCatalog  # noqa: E402
from pyiceberg.schema import Schema  # noqa: E402
from pyiceberg.table import StaticTable  # noqa: E402
from pyiceberg.types import LongType, NestedField, StringType  # noqa: E402

# ---------------------------------------------------------------------------
# 1. MEASURE THE 27 LIVE
# ---------------------------------------------------------------------------
print("-- 1. THE 27, MEASURED IN THE WAREHOUSE --")
s3 = boto3.client("s3")
marker = json.loads(s3.get_object(Bucket=MARKER_BUCKET, Key=MARKER_KEY)["Body"].read())
tmeta = marker["table_metadata"]
print("  VINTAGE: %s (the marker the writer itself stamped)" % marker["committed_at_iso"])
print("  graph_edges last_write = %s" % tmeta["graph_edges"]["last_write_iso"])
print("  graph_nodes last_write = %s" % tmeta["graph_nodes"]["last_write_iso"])

et = StaticTable.from_metadata(tmeta["graph_edges"]["metadata_location"])
nt = StaticTable.from_metadata(tmeta["graph_nodes"]["metadata_location"])
E = et.scan(selected_fields=("src_id", "dst_id", "edge_type")).to_arrow().to_pylist()
N = nt.scan(selected_fields=("node_id", "arn", "node_type")).to_arrow().to_pylist()
print("  DENOMINATOR: %d edge rows and %d node rows -- both tables entire, no"
      " filter, no limit." % (len(E), len(N)))

counts: dict = {}
for e in E:
    counts[e["edge_type"]] = counts.get(e["edge_type"], 0) + 1
SF = [e for e in E if e["edge_type"] == "SERVED_FROM"]
SI = [e for e in E if e["edge_type"] == "STORED_IN"]
print("  SERVED_FROM = %d      <- the family this deliverable is about" % len(SF))
print("  STORED_IN   = %d      <- the family round 8 measured losing 124" % len(SI))
print("  OWNED_BY    = %d    <- THE POSITIVE CONTROL the cell names. A family"
      % counts.get("OWNED_BY", 0))
print("                          this size reading non-zero is what tells a real")
print("                          zero apart from an empty read.")
if counts.get("OWNED_BY", 0) == 0 or not SF:
    print("  BLOCKED: the control family is empty or SERVED_FROM is absent; this")
    print("  read cannot be trusted and nothing below would score anything.")
    sys.exit(1)
print("  POSITIVE_CONTROL=FIRED (OWNED_BY=%d, non-zero)" % counts["OWNED_BY"])

# The served loader's OWN key rule, extracted by content.
loader_src = (REPO / LOADER_REL).read_text(encoding="utf-8")
m = re.search(r"^def graph_key\(.*?(?=\n(?:def |# ---))", loader_src, re.S | re.M)
if not m:
    raise SystemExit("ERROR: could not extract graph_key from %s" % LOADER_REL)
gk_ns: dict = {}
exec(compile(m.group(0), "<%s:graph_key>" % LOADER_REL, "exec"), gk_ns)
graph_key = gk_ns["graph_key"]
print()
print("  THE SERVED KEY RULE, extracted from %s (not restated):" % LOADER_REL)
print("    node key      = graph_key(arn) or graph_key(node_id)   [:217, 'S9: ONE key rule']")
print("    edge endpoint = graph_key(src_id) / graph_key(dst_id)  [:259-260]")


def served_index(node_rows):
    """key -> row, exactly as kuzu_nessie_load builds `best`."""
    idx = {}
    for r in node_rows:
        k = graph_key(r.get("arn")) or graph_key(r.get("node_id"))
        if k:
            idx[k] = r
    return idx


live_idx = served_index(N)
dsts: dict = {}
for e in SF:
    dsts[e["dst_id"]] = dsts.get(e["dst_id"], 0) + 1
print()
print("  WHERE THE 27 LAND (every distinct endpoint, not a sample):")
by_id: dict = {}
for r in N:
    by_id.setdefault(r["node_id"], set()).add(r["node_type"])
armed = 0
for d in sorted(dsts):
    landed = live_idx.get(graph_key(d))
    classes = sorted(by_id.get(d, []))
    print("    dst_id=%-28s n=%-3d -> resolves to node_type=%s"
          % (d, dsts[d], landed["node_type"] if landed else "NOTHING (dangling)"))
    print("      node_id %r is claimed by %d class(es): %s" % (d, len(classes), classes))
    if landed and landed["node_type"] == "S3_BUCKET_POLICY" and len(classes) > 1:
        armed += dsts[d]
        print("      STATUS: ARMED. The endpoint resolves to the POLICY row, and an")
        print("        S3_BUCKET upsert of the same name destroys that row.")
print("  SERVED_FROM edges ARMED by the collision = %d of %d" % (armed, len(SF)))

print()
print("  AND THE ALREADY-FIRED HALF, for contrast -- STORED_IN's endpoints:")
sd: dict = {}
for e in SI:
    sd[e["dst_id"]] = sd.get(e["dst_id"], 0) + 1
for d in sorted(sd, key=lambda k: -sd[k]):
    landed = live_idx.get(graph_key(d))
    print("    dst_id=%-28s n=%-3d -> node_type=%s ; classes at that node_id=%s"
          % (d, sd[d], landed["node_type"] if landed else "NOTHING",
             sorted(by_id.get(d, []))))
print("    -> read the node_type column above, not this sentence's expectation:")
print("       these endpoints now resolve to NOTHING. The POLICY row they used")
print("       to land on is destroyed, and the BUCKET row does NOT answer to the")
print("       bare name -- its served key is the full ARN. So they DANGLE. That")
print("       is 124 (opal-data-bd) + 11 (opal-data-inf) = the 135 STORED_IN")
print("       edges derive_runner.py:2308 names, plus 2 on opal-data-mdpf, which")
print("       has NO live bucket policy at all and therefore never had a policy")
print("       row to land on -- a different cause with the same appearance, and")
print("       the reason 137 is not 135.")
print("       SERVED_FROM is the SAME SHAPE ONE STEP EARLIER: its policy row is")
print("       still alive, so its 27 have not fallen yet.")

# ---------------------------------------------------------------------------
# 2. THE ARM
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("-- 2. THE SAME ARM, ON THE REAL 27 --")

old_src_file = subprocess.run(["git", "show", "%s:%s" % (HEAD, LAMBDA_REL)],
                              capture_output=True, text=True).stdout
mo = re.search(r"^def _match_filter\(.*?(?=\n(?:def |# ---))", old_src_file, re.S | re.M)
if not mo:
    raise SystemExit("ERROR: no pre-fix _match_filter at HEAD")
old_ns: dict = {"logger": types.SimpleNamespace(warning=lambda *a, **k: None)}
exec(compile(mo.group(0), "<HEAD:_match_filter>", "exec"), old_ns)
old_match_filter = old_ns["_match_filter"]

os.environ.setdefault("NESSIE_URI", "http://localhost:19120")
os.environ.setdefault("WAREHOUSE_URI", "s3://unused/warehouse")
sys.modules.setdefault("_provenance", types.ModuleType("_provenance"))
sys.modules["_provenance"].stamp_marker = lambda *a, **k: None
sys.path.insert(0, str(REPO / "infra/aws/lambda/globgrph/incremental_updater"))
import lambda_function as LF  # noqa: E402

print("  PRE-FIX predicate : extracted from git %s:%s" % (HEAD[:10], LAMBDA_REL))
print("  POST-FIX predicate: imported from the module on disk")

SCHEMA = Schema(
    NestedField(1, "node_id", StringType(), required=True),
    NestedField(2, "arn", StringType(), required=False),
    NestedField(3, "node_type", StringType(), required=True),
    NestedField(4, "name", StringType(), required=False),
    NestedField(5, "layer", StringType(), required=False),
    NestedField(6, "drift_class", StringType(), required=False),
    NestedField(7, "source", StringType(), required=False),
    NestedField(8, "snapshot_ts", LongType(), required=False),
    NestedField(9, "props", StringType(), required=False),
)
PA_SCHEMA = pa.schema([
    pa.field("node_id", pa.string(), nullable=False),
    pa.field("arn", pa.string(), nullable=True),
    pa.field("node_type", pa.string(), nullable=False),
    pa.field("name", pa.string(), nullable=True),
    pa.field("layer", pa.string(), nullable=True),
    pa.field("drift_class", pa.string(), nullable=True),
    pa.field("source", pa.string(), nullable=True),
    pa.field("snapshot_ts", pa.int64(), nullable=True),
    pa.field("props", pa.string(), nullable=True),
])

# THE SEED IS THE REAL THING: every node row in the live table whose node_id is
# an endpoint of one of the 27, plus the control rows for the OWNED_BY sample.
SF_ENDPOINTS = sorted({e["dst_id"] for e in SF} | {e["src_id"] for e in SF})
OWNED_SAMPLE = [e for e in E if e["edge_type"] == "OWNED_BY"][:200]
CTL_ENDPOINTS = sorted({e["dst_id"] for e in OWNED_SAMPLE} | {e["src_id"] for e in OWNED_SAMPLE})
WANTED = set(SF_ENDPOINTS) | set(CTL_ENDPOINTS)
seed_rows = [r for r in N
             if r["node_id"] in WANTED or graph_key(r["arn"]) in WANTED]
print()
print("  FIXTURE SEED: %d REAL node rows lifted from the live table -- every row"
      % len(seed_rows))
print("    whose node_id or arn is an endpoint of one of the %d SERVED_FROM edges"
      % len(SF))
print("    or of the %d OWNED_BY control edges. Denominator %d of %d live rows."
      % (len(OWNED_SAMPLE), len(seed_rows), len(N)))
print("  EDGES UNDER TEST: the %d real SERVED_FROM rows, endpoint strings verbatim."
      % len(SF))

if WH_REL and Path(WH_REL).exists():
    shutil.rmtree(WH_REL, ignore_errors=True)
Path(WH_REL).mkdir(parents=True, exist_ok=True)
catalog = SqlCatalog("sf", **{"uri": "sqlite:///%s/catalog.db" % WH_REL, "warehouse": WH_REL})
try:
    catalog.create_namespace("sf")
except Exception:
    pass


def to_pa(rows, ts):
    return pa.table({
        "node_id": [r["node_id"] for r in rows],
        "arn": [r.get("arn") or "" for r in rows],
        "node_type": [r["node_type"] for r in rows],
        "name": [r.get("name") or "" for r in rows],
        "layer": ["aws" for _ in rows],
        "drift_class": ["" for _ in rows],
        "source": [r.get("source") or "" for r in rows],
        "snapshot_ts": [ts for _ in rows],
        "props": ["" for _ in rows],
    }, schema=PA_SCHEMA)


# The upsert the Lambda makes on the next CloudTrail write to that bucket.
TARGET = sorted(dsts)[0]
UPSERT = {"id": TARGET, "arn": "arn:aws:s3:::%s" % TARGET, "type": "S3_BUCKET",
          "name": TARGET, "source": "incremental"}
print("  THE ACT UNDER TEST: one incremental upsert of S3_BUCKET %r -- the same"
      % TARGET)
print("    shape as the three that already fired (opal-data-bd, -cot, -inf).")


def orphan_count(node_rows, edges):
    idx = served_index(node_rows)
    lost = [e for e in edges
            if graph_key(e["dst_id"]) not in idx or graph_key(e["src_id"]) not in idx]
    return len(lost), lost


def run(label, build_filter):
    ident = ("sf", label)
    try:
        catalog.drop_table(ident)
    except Exception:
        pass
    t = catalog.create_table(ident, schema=SCHEMA)
    t.append(to_pa(seed_rows, 1000))
    before_rows = t.scan().to_arrow().to_pylist()
    b_lost, _ = orphan_count(before_rows, SF)
    b_ctl, _ = orphan_count(before_rows, OWNED_SAMPLE)
    f = build_filter(UPSERT)
    t.overwrite(to_pa([{"node_id": UPSERT["id"], "arn": UPSERT["arn"],
                        "node_type": UPSERT["type"], "name": UPSERT["name"],
                        "source": UPSERT["source"]}], 2000), overwrite_filter=f)
    after_rows = t.scan().to_arrow().to_pylist()
    a_lost, lost = orphan_count(after_rows, SF)
    a_ctl, _ = orphan_count(after_rows, OWNED_SAMPLE)
    return {"filter": str(f), "before_rows": len(before_rows), "after_rows": len(after_rows),
            "sf_orphaned_before": b_lost, "sf_orphaned_after": a_lost,
            "ctl_orphaned_before": b_ctl, "ctl_orphaned_after": a_ctl,
            "after": after_rows}


red = run("red", lambda u: old_match_filter([u["arn"] or u["id"]], [u["id"]]))
print()
print("  ARM 1 -- RED (pre-fix predicate)")
print("    filter: %s" % red["filter"])
print("    node rows %d -> %d" % (red["before_rows"], red["after_rows"]))
print("    SERVED_FROM edges with an unresolvable endpoint: %d before -> %d AFTER"
      % (red["sf_orphaned_before"], red["sf_orphaned_after"]))
SF_ORPHANED_BEFORE = red["sf_orphaned_after"]
print("    SERVED_FROM_ORPHANED_BEFORE_FIX=%d of %d" % (SF_ORPHANED_BEFORE, len(SF)))

green = run("green", lambda u: LF._match_filter([(u["arn"], u["id"], u["type"])]))
print()
print("  ARM 2 -- GREEN (post-fix predicate, same fixture, same act)")
print("    filter: %s" % green["filter"])
print("    node rows %d -> %d" % (green["before_rows"], green["after_rows"]))
print("    SERVED_FROM edges with an unresolvable endpoint: %d before -> %d AFTER"
      % (green["sf_orphaned_before"], green["sf_orphaned_after"]))
SF_ORPHANED_AFTER = green["sf_orphaned_after"]
print("    SERVED_FROM_ORPHANED_AFTER_FIX=%d of %d" % (SF_ORPHANED_AFTER, len(SF)))

print()
print("  NEGATIVE CONTROL -- the %d OWNED_BY edges in the same fixture, whose"
      % len(OWNED_SAMPLE))
print("    endpoints are on uncontended keys. They must be untouched by BOTH arms:")
print("    red   arm: %d orphaned before -> %d after"
      % (red["ctl_orphaned_before"], red["ctl_orphaned_after"]))
print("    green arm: %d orphaned before -> %d after"
      % (green["ctl_orphaned_before"], green["ctl_orphaned_after"]))
ctl_ok = (red["ctl_orphaned_after"] == red["ctl_orphaned_before"]
          and green["ctl_orphaned_after"] == green["ctl_orphaned_before"])
print("    CONTROL_UNMOVED=%s" % ("true" if ctl_ok else "false"))

policy_alive = any(r["node_id"] == TARGET and r["node_type"] == "S3_BUCKET_POLICY"
                   for r in green["after"])
policy_dead_red = not any(r["node_id"] == TARGET and r["node_type"] == "S3_BUCKET_POLICY"
                          for r in red["after"])

ok = (SF_ORPHANED_BEFORE == len(SF) and SF_ORPHANED_AFTER == 0
      and ctl_ok and policy_alive and policy_dead_red)

print()
print("=" * 78)
print("== SERVED_FROM VERDICT ==")
print("SERVED_FROM_EDGES=%d of %d measured live" % (len(SF), len(SF)))
print("BASELINE_RED_CAPTURED=%s" % ("true" if SF_ORPHANED_BEFORE > 0 else "false"))
print("SERVED_FROM_ORPHANED_BEFORE=%d" % SF_ORPHANED_BEFORE)
print("SERVED_FROM_ORPHANED_AFTER=%d" % SF_ORPHANED_AFTER)
print("PARENT_POLICY_ROW destroyed by the pre-fix arm = %s ; alive after the"
      " post-fix arm = %s" % (policy_dead_red, policy_alive))
print("NEGATIVE_CONTROL=%s (OWNED_BY sample unmoved in both arms)"
      % ("FIRED" if ctl_ok else "DID_NOT_FIRE"))
print("POSITIVE_CONTROL=FIRED (OWNED_BY=%d live, so a zero would have been"
      " visible as a zero)" % counts["OWNED_BY"])
print("SERVED_FROM_COVERED=%s" % ("YES" if ok else "NO"))
print()
print("COVERAGE, stated: this exercises ALL %d SERVED_FROM edges (not a sample)"
      % len(SF))
print("  against %d real node rows, through the real overwrite verb. It does NOT"
      % len(seed_rows))
print("  exercise the Kuzu loader itself, the projection service, or a deployed")
print("  Lambda. The key rule used to resolve endpoints is the loader's OWN,")
print("  extracted from its source, so the resolution is not a second rule.")
print("PROVENANCE: the live counts and both orphan counts are `measured`. That")
print("  the same mechanism covers both families is DEMONSTRATED here, not held.")
print("elapsed=%.1fs" % (time.time() - T0))
sys.exit(0 if ok else 1)
