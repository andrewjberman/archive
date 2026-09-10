#!/usr/bin/env python3
"""i1_arm.py -- NFRA_CLDGRPH CG-s-41, criterion I1-AC3.

THE OVERWRITE ARM, AND IT GOES RED FIRST.

A green that was always going to be green is not a test. So this arm builds the
collision on a fixture, runs the PRE-FIX predicate against it, and shows a row
being DESTROYED -- and only then runs the POST-FIX predicate against the same
fixture and shows zero destroyed.

WHAT THE FIXTURE IS, AND WHY IT CAN REPRESENT THE FAILURE (a fixture that cannot
represent the failure cannot score it):

  * A REAL ICEBERG TABLE, not a mock and not a list of dicts. pyiceberg's
    SqlCatalog over a local sqlite catalog and a local warehouse directory,
    carrying the SAME 9-column schema as the live globgrph.graph_nodes
    (node_id/arn/node_type required-flags included).
  * The REAL write verb: table.overwrite(pa_table, overwrite_filter=F), the same
    call lambda_function.py:501 makes. The delete-then-append semantics under
    test are pyiceberg's own, not my model of them.
  * The REAL pre-fix predicate, EXTRACTED FROM git HEAD rather than restated by
    me. If I retyped it I would be testing my memory of the bug.
  * The REAL post-fix predicate, IMPORTED FROM THE MODULE I edited.
  * REAL colliding keys, taken from the live table (i1_settle.py measured them):
    the S3_BUCKET/S3_BUCKET_POLICY pair AND the IAM_ROLE/LAMBDA pair, because a
    fix demonstrated on one pair is a fix demonstrated on one pair.

NEGATIVE CONTROL IN THE SAME RUN: two rows whose keys are genuinely distinct
must BOTH survive both arms. Without it, "nothing was destroyed" is also what a
predicate that matches nothing would print.

READS ONLY as far as the estate is concerned: everything here is local. No AWS
call, no S3 write, no Nessie commit, nothing deployed.
"""
from __future__ import annotations

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
LAMBDA_REL = "infra/aws/lambda/globgrph/incremental_updater/lambda_function.py"
# The warehouse is addressed RELATIVE to the repo root, and the process chdirs
# there. pyiceberg URI-parses this string: an absolute Windows path "C:\..."
# parses as scheme "c" (ValueError: Unrecognized filesystem type in URI: c), and
# a file:///C:/... URI is re-parsed by pyarrow's LocalFileSystem into /C:/...
# (WinError 123). A drive-less relative path has no scheme and resolves locally.
os.chdir(REPO)
WH_REL = ".scratch/i1_arm_wh"
WH = REPO / ".scratch" / "i1_arm_wh"
CAPTURE = HERE / "i1_arm_red_capture.txt"

print("=" * 78)
print("i1_arm.py -- CG-s-41 / I1-AC3 -- THE OVERWRITE ARM, RED FIRST")
print("=" * 78)
print("TREE_READ cwd    = %s" % os.getcwd())
print("TREE_READ branch = %s" % subprocess.run(
    ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip())
HEAD = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
print("TREE_READ head   = %s" % HEAD)
print("ENVIRONMENT of the baseline: THIS RUN. The red baseline is not a stored")
print("  number from another machine or another night -- it is captured in this")
print("  process, on this fixture, seconds before the green arm runs on the same")
print("  fixture. Nothing is compared across environments.")
print("HARNESS GRAIN: the ROW in an Iceberg table, after a real overwrite call.")
print()

# Imported HERE, after the header block, ON PURPOSE: the TREE_READ lines above
# must print before any third-party import can fail, so a missing pyiceberg is
# reported against a KNOWN tree rather than as a bare traceback. E402 waived
# per-line with the reason stated, not silenced file-wide.
import pyarrow as pa  # noqa: E402
import pyiceberg  # noqa: E402
from pyiceberg.catalog.sql import SqlCatalog  # noqa: E402
from pyiceberg.schema import Schema  # noqa: E402
from pyiceberg.types import LongType, NestedField, StringType  # noqa: E402

# ---------------------------------------------------------------------------
# THE TWO PREDICATES UNDER TEST
# ---------------------------------------------------------------------------
print("-- THE TWO PREDICATES, BOTH OBTAINED BY CONTENT, NEITHER RETYPED --")


def extract_fn(source: str, name: str) -> str:
    m = re.search(r"^def %s\(.*?(?=\n(?:def |# ---))" % re.escape(name),
                  source, re.S | re.M)
    if not m:
        raise SystemExit("ERROR: could not extract %s" % name)
    return m.group(0)


old_src_file = subprocess.run(["git", "show", "%s:%s" % (HEAD, LAMBDA_REL)],
                              capture_output=True, text=True).stdout
if "def _match_filter" not in old_src_file:
    raise SystemExit("ERROR: git show returned no _match_filter -- refusing to "
                     "run a red arm against a file I could not read")
old_fn_src = extract_fn(old_src_file, "_match_filter")
old_ns: dict = {"logger": types.SimpleNamespace(warning=lambda *a, **k: None)}
exec(compile(old_fn_src, "<HEAD:_match_filter>", "exec"), old_ns)
old_match_filter = old_ns["_match_filter"]
print("  PRE-FIX  : _match_filter extracted from `git show %s:%s`" % (HEAD[:10], LAMBDA_REL))
print("             signature = %s"
      % re.search(r"def _match_filter\([^)]*\)", old_fn_src).group(0))

os.environ.setdefault("NESSIE_URI", "http://localhost:19120")
os.environ.setdefault("WAREHOUSE_URI", "s3://unused/warehouse")
sys.modules.setdefault("_provenance", types.ModuleType("_provenance"))
sys.modules["_provenance"].stamp_marker = lambda *a, **k: None
sys.path.insert(0, str(REPO / "infra/aws/lambda/globgrph/incremental_updater"))
import lambda_function as LF  # noqa: E402

new_match_filter = LF._match_filter
print("  POST-FIX : _match_filter IMPORTED from the module at %s" % LAMBDA_REL)
print("             signature = %s"
      % re.search(r"def _match_filter\([^)]*\)",
                  (REPO / LAMBDA_REL).read_text(encoding="utf-8")).group(0))
print("  (the two signatures DIFFER, which is the point: the key gained its class)")
print()

# ---------------------------------------------------------------------------
# THE FIXTURE
# ---------------------------------------------------------------------------
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

# Every seed row's shape is the shape i1_settle.py measured in the live table.
SEED = [
    # THE COLLIDING PAIR the cell is about: the policy's canonical key IS the
    # bucket name, so it sits on the bucket's node_id.
    dict(node_id="opal-data-bd", arn="arn:aws:s3:::opal-data-bd",
         node_type="S3_BUCKET", name="opal-data-bd", source="full-derive"),
    dict(node_id="opal-data-bd", arn="opal-data-bd",
         node_type="S3_BUCKET_POLICY", name="opal-data-bd", source="full-derive"),
    # A SECOND colliding pair, measured live (8 such pairs): a function and its
    # execution role legitimately share a name. Both carry full, DIFFERENT arns,
    # so only the node_id limb can collide them.
    dict(node_id="opal-cot-value-parity",
         arn="arn:aws:lambda:us-east-1:313476888478:function:opal-cot-value-parity",
         node_type="LAMBDA", name="opal-cot-value-parity", source="full-derive"),
    dict(node_id="opal-cot-value-parity",
         arn="arn:aws:iam::313476888478:role/opal-cot-value-parity",
         node_type="IAM_ROLE", name="opal-cot-value-parity", source="full-derive"),
    # THE NEGATIVE CONTROL: two rows with genuinely DISTINCT keys. Neither may
    # be touched by either arm. If these die, the predicate is over-matching and
    # every "0 destroyed" below would be meaningless.
    dict(node_id="opal-control-table", arn="arn:aws:dynamodb:us-east-1:313476888478:table/opal-control-table",
         node_type="DYNAMODB_TABLE", name="opal-control-table", source="full-derive"),
    dict(node_id="opal-control-topic", arn="arn:aws:sns:us-east-1:313476888478:opal-control-topic",
         node_type="SNS_TOPIC", name="opal-control-topic", source="full-derive"),
]


def to_pa(rows, ts):
    return pa.table({
        "node_id": [r["node_id"] for r in rows],
        "arn": [r.get("arn", "") for r in rows],
        "node_type": [r["node_type"] for r in rows],
        "name": [r.get("name", "") for r in rows],
        "layer": ["aws" for _ in rows],
        "drift_class": [r.get("drift_class", "") for r in rows],
        "source": [r.get("source", "") for r in rows],
        "snapshot_ts": [ts for _ in rows],
        "props": ["" for _ in rows],
    }, schema=PA_SCHEMA)


def fresh_table(cat, name):
    ident = ("arm", name)
    try:
        cat.drop_table(ident)
    except Exception:
        pass
    t = cat.create_table(ident, schema=SCHEMA)
    t.append(to_pa(SEED, 1000))
    return t


def dump(t):
    got = t.scan().to_arrow().to_pylist()
    return sorted([(r["node_id"], r["node_type"], r["arn"], r["snapshot_ts"]) for r in got])


if WH.exists():
    shutil.rmtree(WH, ignore_errors=True)
WH.mkdir(parents=True, exist_ok=True)
catalog = SqlCatalog("arm", **{
    "uri": "sqlite:///%s/catalog.db" % WH_REL,
    "warehouse": WH_REL,
})
try:
    catalog.create_namespace("arm")
except Exception:
    pass

print("-- THE FIXTURE --")
print("  pyiceberg %s, SqlCatalog(sqlite) + local warehouse %s" % (pyiceberg.__version__, WH))
print("  schema = the live graph_nodes 9-column schema (node_id/node_type required)")
print("  DENOMINATOR: %d seed rows -- 2 colliding pairs (4 rows) + 2 distinct-key"
      " control rows. Nothing else." % len(SEED))
for r in SEED:
    print("    node_id=%-24s type=%-18s arn=%s" % (r["node_id"], r["node_type"], r.get("arn")))

# The upsert the Lambda performs when CloudTrail reports a write to that bucket.
UPSERT_BUCKET = dict(id="opal-data-bd", arn="arn:aws:s3:::opal-data-bd",
                     type="S3_BUCKET", name="opal-data-bd", source="incremental")
UPSERT_LAMBDA = dict(id="opal-cot-value-parity",
                     arn="arn:aws:lambda:us-east-1:313476888478:function:opal-cot-value-parity",
                     type="LAMBDA", name="opal-cot-value-parity", source="incremental")
UPSERTS = [UPSERT_BUCKET, UPSERT_LAMBDA]


def run_arm(label, build_filter, capture_lines):
    """One arm: seed a fresh table, run the real overwrite, report what died."""
    results = []
    for up in UPSERTS:
        t = fresh_table(catalog, "%s_%s" % (label, up["type"].lower()))
        before = dump(t)
        f = build_filter([up])
        t.overwrite(to_pa([{"node_id": up["id"], "arn": up["arn"],
                            "node_type": up["type"], "name": up["name"],
                            "source": up["source"]}], 2000),
                    overwrite_filter=f)
        after = dump(t)
        gone = [r for r in before if r not in after
                and not (r[0] == up["id"] and r[1] == up["type"])]
        same_class_rows = [r for r in after if r[0] == up["id"] and r[1] == up["type"]]
        results.append({
            "upsert": up, "filter": str(f), "before": before, "after": after,
            "foreign_destroyed": gone, "own_rows_after": len(same_class_rows),
        })
        capture_lines.append("ARM=%s UPSERT=%s(%s)" % (label, up["id"], up["type"]))
        capture_lines.append("  FILTER: %s" % f)
        capture_lines.append("  BEFORE (%d rows):" % len(before))
        for r in before:
            capture_lines.append("    %s" % (r,))
        capture_lines.append("  AFTER  (%d rows):" % len(after))
        for r in after:
            capture_lines.append("    %s" % (r,))
        capture_lines.append("  FOREIGN-CLASS ROWS DESTROYED: %d" % len(gone))
        for r in gone:
            capture_lines.append("    DESTROYED %s" % (r,))
        capture_lines.append("")
    return results


# ---------------------------------------------------------------------------
# RED
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("-- ARM 1: RED. The PRE-FIX predicate, run BEFORE anything is claimed. --")
cap: list[str] = ["CG-s-41 i1_arm.py RED CAPTURE",
                  "captured_at_head=%s" % HEAD,
                  "predicate=_match_filter at git HEAD (pre-fix), extracted by content",
                  ""]


def old_builder(nodes):
    arns = [(n.get("arn") or n.get("id")) for n in nodes]
    ids = [n.get("id", "") for n in nodes]
    return old_match_filter(arns, ids)


red = run_arm("red", old_builder, cap)
DESTROYED_BEFORE = sum(len(r["foreign_destroyed"]) for r in red)
for r in red:
    print()
    print("  upsert %s (%s)" % (r["upsert"]["id"], r["upsert"]["type"]))
    print("    filter built by the PRE-FIX code: %s" % r["filter"])
    print("    rows before = %d, rows after = %d" % (len(r["before"]), len(r["after"])))
    for g in r["foreign_destroyed"]:
        print("    DESTROYED -> node_id=%-24s node_type=%-18s arn=%s" % (g[0], g[1], g[2]))
    print("    own-class rows remaining for this key = %d (must be 1: replaced, not duplicated)"
          % r["own_rows_after"])
print()
print("  DESTROYED_BEFORE=%d" % DESTROYED_BEFORE)
CAPTURE.write_text("\n".join(cap) + "\n", encoding="utf-8", newline="\n")
print("  RED CAPTURE WRITTEN: %s (%d bytes)" % (CAPTURE, CAPTURE.stat().st_size))
print("  BASELINE_RED_CAPTURED=%s" % ("true" if DESTROYED_BEFORE > 0 and CAPTURE.exists() else "false"))
if DESTROYED_BEFORE == 0:
    print("  ERROR: the red arm did not go red. The fixture cannot represent the")
    print("  failure, so nothing below could score it. Refusing to run green.")
    sys.exit(1)

# ---------------------------------------------------------------------------
# GREEN
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("-- ARM 2: GREEN. The POST-FIX predicate, same fixture, same overwrite. --")
cap2: list[str] = []


def new_builder(nodes):
    keys = [(n.get("arn") or "", n.get("id") or "", n.get("type") or "") for n in nodes]
    return new_match_filter(keys)


green = run_arm("green", new_builder, cap2)
DESTROYED_AFTER = sum(len(r["foreign_destroyed"]) for r in green)
dup = [r for r in green if r["own_rows_after"] != 1]
for r in green:
    print()
    print("  upsert %s (%s)" % (r["upsert"]["id"], r["upsert"]["type"]))
    print("    filter built by the POST-FIX code: %s" % r["filter"])
    print("    rows before = %d, rows after = %d" % (len(r["before"]), len(r["after"])))
    print("    foreign-class rows destroyed = %d" % len(r["foreign_destroyed"]))
    print("    own-class rows remaining for this key = %d %s"
          % (r["own_rows_after"],
             "(replaced, not duplicated -- the upsert still works)"
             if r["own_rows_after"] == 1 else "*** REGRESSION: not exactly 1 ***"))
print()
print("  DESTROYED_AFTER=%d" % DESTROYED_AFTER)
print("  UPSERT_STILL_REPLACES=%s (no duplicate rows introduced by the narrowing)"
      % ("true" if not dup else "FALSE"))

# ---------------------------------------------------------------------------
# THE NEGATIVE CONTROL
# ---------------------------------------------------------------------------
print()
print("-- NEGATIVE CONTROL: two rows with genuinely DISTINCT keys --")
CONTROL_KEYS = {("opal-control-table", "DYNAMODB_TABLE"),
                ("opal-control-topic", "SNS_TOPIC")}
ctl_ok = True
for label, arm in (("red", red), ("green", green)):
    for r in arm:
        survived = {(x[0], x[1]) for x in r["after"]} & CONTROL_KEYS
        print("  %-5s arm, upsert %-24s : control rows surviving = %d of %d %s"
              % (label, r["upsert"]["id"], len(survived), len(CONTROL_KEYS),
                 sorted(survived)))
        if len(survived) != len(CONTROL_KEYS):
            ctl_ok = False
print("  DISTINCT_KEYS_BOTH_SURVIVE=%s" % ("true" if ctl_ok else "false"))
print("  NEGATIVE_CONTROL=%s" % ("FIRED" if ctl_ok else "DID_NOT_FIRE"))
print("  (FIRED means: the control rows were present in the population, were")
print("   exposed to both predicates, and survived both. It is what separates")
print("   'the fix stopped the destruction' from 'the predicate matches nothing'.)")

# ---------------------------------------------------------------------------
# THE DELETE PATH, which shares the same filter
# ---------------------------------------------------------------------------
print()
print("-- THE DELETE PATH (same filter, opposite intent) --")
ct = {"detail": {"eventName": "DeleteBucket", "recipientAccountId": "313476888478",
                 "requestParameters": {"bucketName": "opal-data-bd"}}}
dk = LF.delete_keys_from_event(ct)
print("  delete_keys_from_event(DeleteBucket opal-data-bd) -> %s" % dk)
t = fresh_table(catalog, "del")
before = dump(t)
t.delete(delete_filter=new_match_filter([tuple(k) for k in dk]))
after = dump(t)
killed = [r for r in before if r not in after]
print("  rows removed = %d" % len(killed))
for r in killed:
    print("    removed node_id=%-24s node_type=%s" % (r[0], r[1]))
pol_alive = any(r[0] == "opal-data-bd" and r[1] == "S3_BUCKET_POLICY" for r in after)
print("  the BUCKET row is gone       : %s"
      % (not any(r[0] == "opal-data-bd" and r[1] == "S3_BUCKET" for r in after)))
print("  the POLICY row is UNTOUCHED  : %s" % pol_alive)
print("  (before the fix a DeleteBucket removed both, because the bare name")
print("   matched both. The policy is now stale until the nightly derive drops")
print("   it -- that is the named, accepted cost of the narrowing.)")

# ---------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------
overwrite_arm_pass = (DESTROYED_BEFORE > 0 and DESTROYED_AFTER == 0
                      and not dup and ctl_ok and pol_alive)
print()
print("=" * 78)
print("== ARM VERDICT (ordered for the accept) ==")
print("BASELINE_RED_CAPTURED=true")
print("OVERWRITE_ARM=%s" % ("PASS" if overwrite_arm_pass else "FAIL"))
print("DESTROYED_BEFORE=%d" % DESTROYED_BEFORE)
print("DESTROYED_AFTER=%d" % DESTROYED_AFTER)
print("DISTINCT_KEYS_BOTH_SURVIVE=%s" % ("true" if ctl_ok else "false"))
print("NEGATIVE_CONTROL=%s" % ("FIRED" if ctl_ok else "DID_NOT_FIRE"))
print()
print("COVERAGE of this arm, stated rather than implied: it exercises the two")
print("  colliding pairs it seeds (S3_BUCKET/S3_BUCKET_POLICY and")
print("  IAM_ROLE/LAMBDA) over %d fixture rows. It does NOT exercise the live"
      % len(SEED))
print("  27,685-row table, the Nessie catalog, the SQS handler or a deployed")
print("  Lambda -- nothing here is deployed and nothing here touched AWS.")
print("PROVENANCE: DESTROYED_BEFORE / DESTROYED_AFTER / the control results are")
print("  `measured` -- pyiceberg returned them in this run.")
print("elapsed=%.1fs" % (time.time() - T0))
sys.exit(0 if overwrite_arm_pass else 1)
