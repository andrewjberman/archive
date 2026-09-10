#!/usr/bin/env python3
"""i1_settle.py -- NFRA_CLDGRPH CG-s-41, criterion I1-AC1.

SETTLE THE INFERRED LINK BEFORE ANY LINE CHANGES: which warehouse row does the
incremental updater's upsert DESTROY, and on WHAT key does it match it?

Row W3-S19 labelled this INFERRED in its own words and said Trino/Athena would
settle it. This settles it WITHOUT Trino. The graph_nodes Iceberg table's own
metadata pointer is published to S3 by the writer itself (lambda_function.py
:548-564, MARKER_KEY 'warehouse/_branch_head.main.json', built in its own words
"so dev-box readers (which cannot reach Nessie REST) learn HEAD from an S3
object"), and an S3 get-object is a READ. So the warehouse ROWS are readable
from this laptop via pyiceberg's StaticTable over the marker's own
metadata_location, at the writer's own vintage.

READS ONLY. No S3 write, no ecs run-task, no CodeBuild, no image act, no
terraform apply, no act whose effect is an SNS publish (the egress hold).

THREE ARMS ON THREE DIFFERENT PLANES, so a wrong answer cannot pass all three
(Rule 22 DISCRIMINATION; arms A and B share no instrument and no substrate):

  A. WAREHOUSE PLANE  -- pyiceberg over the Iceberg data files in S3.
     What rows exist NOW, keyed how, written by whom (the `source` column).
  B. AWS CONTROL PLANE -- s3 get-bucket-policy via boto3.
     Which buckets actually HAVE a live policy, so a missing policy ROW can be
     told apart from a bucket that never had one. This is the arm that makes
     DESTROYED different from NEVER-EXISTED.
  C. FILTER REPLAY -- the writer's own predicate, re-implemented from source
     (lambda_function.py:391-405) and evaluated over arm A's real rows, so the
     destroyed row and the matching LIMB are read off a measurement.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

T0 = time.time()


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout.strip()


MARKER_BUCKET = "opal-313476888478-globgrph"
MARKER_KEY = "warehouse/_branch_head.main.json"

print("=" * 78)
print("i1_settle.py -- CG-s-41 / I1-AC1 -- SETTLE THE INFERRED LINK")
print("=" * 78)
print("TREE_READ cwd              = %s" % os.getcwd())
print("TREE_READ repo_toplevel    = %s" % _git("rev-parse", "--show-toplevel"))
print("TREE_READ branch           = %s" % _git("rev-parse", "--abbrev-ref", "HEAD"))
print("TREE_READ head             = %s" % _git("rev-parse", "HEAD"))
print("ENVIRONMENT of the baseline: NONE STORED. This script carries no stored")
print("  baseline at all; every number below is read LIVE in this run from AWS")
print("  us-east-1 account 313476888478, at the vintage the marker names.")
print("HARNESS GRAIN: the ROW in globgrph.graph_nodes -- not a served projection")
print("  of it, not a count of it, the rows themselves.")
print()

# ---------------------------------------------------------------------------
# ARM A -- THE WAREHOUSE PLANE
# ---------------------------------------------------------------------------
print("-- ARM A: WAREHOUSE PLANE (pyiceberg StaticTable over S3 data files) --")
try:
    import boto3
    import pyiceberg
    from pyiceberg.table import StaticTable
except Exception as exc:
    print("ERROR: instrument import failed: %s: %s" % (type(exc).__name__, exc))
    print()
    print("== SETTLE VERDICT (ordered for the accept) ==")
    print("SETTLED=BLOCKED")
    print("INSTRUMENT printed: pyiceberg StaticTable + boto3 -- IMPORT FAILED")
    print("INSTRUMENTS_TRIED=1 of 1")
    print("WHAT_EACH_COULD_NOT_SEE printed: pyiceberg/boto3 unimportable in this")
    print("  interpreter, so no warehouse row was readable by any instrument here.")
    sys.exit(0)

s3 = boto3.client("s3")
marker = json.loads(s3.get_object(Bucket=MARKER_BUCKET, Key=MARKER_KEY)["Body"].read())
tm = marker["table_metadata"]["graph_nodes"]
meta_loc = tm["metadata_location"]

print("MARKER  s3://%s/%s" % (MARKER_BUCKET, MARKER_KEY))
print("  writer_id        = %s" % marker.get("writer_id"))
print("  committed_at_iso = %s   <- THE VINTAGE OF EVERY ARM-A NUMBER"
      % marker.get("committed_at_iso"))
print("  nessie_commit    = %s" % marker.get("nessie_commit_hash"))
print("  graph_nodes.snapshot_id     = %s" % tm.get("snapshot_id"))
print("  graph_nodes.last_write_iso  = %s" % tm.get("last_write_iso"))
print("  metadata_location = %s" % meta_loc)

tbl = StaticTable.from_metadata(meta_loc)
snap = tbl.current_snapshot()
print("  pyiceberg %s loaded the table; current_snapshot_id = %s"
      % (pyiceberg.__version__, snap.snapshot_id))
same = (int(snap.snapshot_id) == int(tm["snapshot_id"]))
print("  SNAPSHOT_AGREES_WITH_MARKER = %s  (the table I read IS the one the"
      " writer stamped)" % ("true" if same else "FALSE"))

cols = ("node_id", "arn", "node_type", "name", "source", "snapshot_ts")
rows = tbl.scan(selected_fields=cols).to_arrow().to_pylist()
N = len(rows)
print()
print("DENOMINATOR: %d rows scanned in globgrph.graph_nodes -- the WHOLE table."
      % N)
print("  EXCLUDED FROM THIS DENOMINATOR: nothing. No filter, no pushdown, no")
print("  limit, no partition scope. 6 of the table's 9 columns were projected")
print("  (props and layer and drift_class are not read); every ROW is present.")

buckets = [r for r in rows if r["node_type"] == "S3_BUCKET"]
policies = [r for r in rows if r["node_type"] == "S3_BUCKET_POLICY"]
incr = [r for r in rows if r["source"] == "incremental"]
print("  S3_BUCKET rows        = %d" % len(buckets))
print("  S3_BUCKET_POLICY rows = %d" % len(policies))
print("  rows with source='incremental' (the Lambda's own mark) = %d" % len(incr))

print()
print("THE KEY SHAPE OF EACH CLASS, read off the rows (not off the docstring):")
b_arn_is_full = sum(1 for r in buckets if str(r["arn"]).startswith("arn:aws:s3:::"))
b_id_is_bare = sum(1 for r in buckets if r["node_id"] == str(r["arn"]).split(":::")[-1])
print("  S3_BUCKET        : arn column is a FULL s3 ARN in %d of %d;"
      " node_id is the BARE NAME in %d of %d"
      % (b_arn_is_full, len(buckets), b_id_is_bare, len(buckets)))
p_arn_is_bare = sum(1 for r in policies if r["arn"] == r["node_id"]
                    and not str(r["arn"]).startswith("arn:"))
print("  S3_BUCKET_POLICY : arn column CARRIES THE BARE BUCKET NAME and equals"
      " node_id in %d of %d" % (p_arn_is_bare, len(policies)))
print("  -> the two classes therefore contend for ONE string in ONE column")
print("     (node_id), and the policy also puts that string in `arn`.")

print()
print("EVERY row with source='incremental' (the whole set, no head, no sample):")
for r in sorted(incr, key=lambda x: x["snapshot_ts"]):
    print("  node_id=%-34s type=%-16s arn=%-40s snapshot_ts=%s"
          % (repr(r["node_id"]), r["node_type"], repr(r["arn"]), r["snapshot_ts"]))
incr_bucket_names = sorted({r["node_id"] for r in incr if r["node_type"] == "S3_BUCKET"})
policy_names = {r["node_id"] for r in policies}
bucket_names = sorted({r["node_id"] for r in buckets})

# ---------------------------------------------------------------------------
# ARM B -- THE AWS CONTROL PLANE
# ---------------------------------------------------------------------------
print()
print("-- ARM B: AWS CONTROL PLANE (s3 get-bucket-policy, boto3, us-east-1) --")
print("WHY THIS ARM EXISTS: a bucket with no policy ROW may simply have no")
print("  policy. Only a LIVE policy with NO row is a destroyed row. This arm is")
print("  a different plane, a different service and a different instrument from")
print("  arm A -- confirming arm A with arm A would be repetition, not")
print("  corroboration.")


def live_policy(name: str):
    cli = boto3.client("s3")
    try:
        cli.get_bucket_policy(Bucket=name)
        return "PRESENT"
    except Exception as exc:
        code = getattr(exc, "response", {}).get("Error", {}).get("Code", type(exc).__name__)
        if code in ("NoSuchBucketPolicy",):
            return "ABSENT"
        return "UNREADABLE:%s" % code


with ThreadPoolExecutor(max_workers=10) as pool:
    live = dict(zip(bucket_names, pool.map(live_policy, bucket_names)))

print("DENOMINATOR: %d of %d S3_BUCKET node_ids probed on the live control"
      " plane -- ALL of them, none excluded." % (len(live), len(bucket_names)))
n_present = sum(1 for v in live.values() if v == "PRESENT")
n_absent = sum(1 for v in live.values() if v == "ABSENT")
n_unread = len(live) - n_present - n_absent
print("  live policy PRESENT=%d  ABSENT=%d  UNREADABLE=%d" % (n_present, n_absent, n_unread))
if n_present and n_absent:
    print("  DISCRIMINATION CONTROL: the probe returned BOTH values over this")
    print("  population, so it is not a constant -- a PRESENT is informative.")
else:
    print("  WARN: the probe returned ONE value over the whole population; it")
    print("  cannot discriminate here and arm B is not load-bearing.")

print()
print("THE CROSS-TAB (live policy) x (policy ROW) x (touched by the Lambda),")
print("over all %d buckets -- every cell, nothing suppressed:" % len(bucket_names))
cells = {}
for b in bucket_names:
    cell = (live[b], "ROW" if b in policy_names else "NOROW",
            "INCR" if b in incr_bucket_names else "UNTOUCHED")
    cells.setdefault(cell, []).append(b)
for cell in sorted(cells):
    print("  live=%-9s row=%-5s lambda=%-9s  n=%d" % (cell[0], cell[1], cell[2], len(cells[cell])))
    for b in sorted(cells[cell]):
        print("        %s" % b)

destroyed = sorted(cells.get(("PRESENT", "NOROW", "INCR"), []))
false_pos = sorted(cells.get(("PRESENT", "NOROW", "UNTOUCHED"), []))
print()
print("  DESTROYED CELL (live policy PRESENT, policy ROW absent, bucket TOUCHED")
print("  by the incremental updater): n=%d -> %s" % (len(destroyed), destroyed))
print("  THE FALSIFIER FOR THE ATTRIBUTION (live policy PRESENT, row absent,")
print("  bucket NOT touched by the Lambda): n=%d -> %s" % (len(false_pos), false_pos))
print("  A non-empty falsifier cell would mean something OTHER than the Lambda")
print("  also removes policy rows, and the attribution would not hold.")

# ---------------------------------------------------------------------------
# ARM C -- FILTER REPLAY
# ---------------------------------------------------------------------------
print()
print("-- ARM C: FILTER REPLAY (the writer's own predicate over arm A's rows) --")
print("SOURCE OF THE PREDICATE, quoted from the file this cell fixes:")
print("  lambda_function.py:436  up_arns = [(n.get('arn') or n.get('id')) for n in nodes]")
print("  lambda_function.py:437  up_ids  = [n.get('id','') for n in nodes]")
print("  lambda_function.py:443  combined_filter = _match_filter(up_arns+del_arns, up_ids+del_ids)")
print("  lambda_function.py:399-404  In('arn', arns)  OR  In('node_id', ids)")
print("  lambda_function.py:501  table.overwrite(pa_table, overwrite_filter=combined_filter)")
print("  pyiceberg overwrite = DELETE every row matching the filter, THEN append")
print("  the upsert rows. So every row the filter matches and the batch does not")
print("  re-append is DESTROYED.")
print()


def replay_current_filter(node, population):
    """Exactly _match_filter's semantics for a batch of ONE node."""
    arns = [x for x in [(node.get("arn") or node.get("id"))] if x]
    ids = [x for x in [node.get("id", "")] if x]
    hits = []
    for r in population:
        on = []
        if r["arn"] in arns:
            on.append("arn")
        if r["node_id"] in ids:
            on.append("node_id")
        if on:
            hits.append((r, on))
    return hits


print("REPLAY POPULATION: all %d rows. For each of the %d S3_BUCKET node_ids in"
      % (N, len(bucket_names)))
print("  the table, the batch-of-one filter the Lambda WOULD build on its next")
print("  CloudTrail event for that bucket is evaluated against every row.")
collisions = []
for b in bucket_names:
    row = next(r for r in buckets if r["node_id"] == b)
    node = {"id": row["node_id"], "arn": row["arn"], "type": "S3_BUCKET"}
    hits = replay_current_filter(node, rows)
    foreign = [(r, on) for (r, on) in hits if r["node_type"] != "S3_BUCKET"]
    if foreign:
        collisions.append((b, foreign))

print()
print("  DENOMINATOR: %d of %d buckets replayed (all of them)." % (len(bucket_names), len(bucket_names)))
print("  BUCKETS WHOSE NEXT UPSERT DESTROYS A FOREIGN-CLASS ROW: %d of %d"
      % (len(collisions), len(bucket_names)))
for b, foreign in collisions:
    for r, on in foreign:
        print("    upsert of S3_BUCKET %-34s DESTROYS node_id=%-34s"
              " node_type=%-18s matched_on=%s"
              % (repr(b), repr(r["node_id"]), r["node_type"], "+".join(on)))

print()
print("  THE REPLAY OVER EVERY CLASS THE UPDATER CAN EMIT -- I ran this because")
print("  my first negative control CHOSE LAMBDA as the uncontended class and the")
print("  instrument came back NON-ZERO. The control was right and my choice of")
print("  control was wrong, so here is the whole population instead of a pick:")
UPDATER_CLASSES = ["S3_BUCKET", "LAMBDA", "IAM_ROLE", "DYNAMODB_TABLE",
                   "SNS_TOPIC", "SQS_QUEUE"]
print("    (the 6 classes bounded_derive_node returns, lambda_function.py:265-327)")
zero_arms, nonzero_arms = [], []
for t_ in UPDATER_CLASSES:
    rs = [r for r in rows if r["node_type"] == t_]
    hit_types = set()
    n_coll = 0
    for r in rs:
        node = {"id": r["node_id"], "arn": r["arn"], "type": t_}
        foreign = [x for x in replay_current_filter(node, rows)
                   if x[0]["node_type"] != t_]
        if foreign:
            n_coll += 1
            hit_types.update(x[0]["node_type"] for x in foreign)
    (nonzero_arms if n_coll else zero_arms).append(t_)
    print("    %-16s rows=%-5d upserts that DESTROY a foreign-class row=%-4d"
          " destroyed classes=%s"
          % (t_, len(rs), n_coll, sorted(hit_types) if hit_types else "NONE"))
print("    NEGATIVE CONTROL=%s -- classes where the replay returns ZERO: %s."
      % ("FIRED" if zero_arms and nonzero_arms else "NOT_FIRED",
         ", ".join(zero_arms) if zero_arms else "none"))
print("    The replay is therefore NOT a constant: it returns 0 on %d of the 6"
      " classes and non-zero on %d. It discriminates."
      % (len(zero_arms), len(nonzero_arms)))

print()
print("  AND THE UNSCOPED READ, because a check scoped to S3_BUCKET cannot see a")
print("  defect in what the CLASSES SHARE (CLAUDE.md Rule 22). Over the WHOLE")
print("  table, which node_id strings does more than one node_type claim?")
by_id = {}
for r in rows:
    by_id.setdefault(r["node_id"], set()).add(r["node_type"])
multi = {k: v for k, v in by_id.items() if len(v) > 1}
print("    DENOMINATOR: %d distinct node_id strings over %d rows -- the whole"
      " table, nothing excluded." % (len(by_id), N))
print("    node_id strings claimed by MORE THAN ONE node_type = %d" % len(multi))
pair_counts = {}
for v in multi.values():
    pair_counts[tuple(sorted(v))] = pair_counts.get(tuple(sorted(v)), 0) + 1
for p in sorted(pair_counts, key=lambda k: -pair_counts[k]):
    reachable = any(c in UPDATER_CLASSES for c in p)
    print("      %-46s n=%-3d updater-reachable=%s"
          % (" + ".join(p), pair_counts[p], "YES" if reachable else "no"))
print("    -> THE COLLISION IS NOT ONE PAIR. The cell and derive_runner.py:2306-")
print("       2308 both say 'exactly one class' holds a short id as its key, and")
print("       that is TRUE OF THE CANONICAL KEY SPACE (arn-or-id). The DESTRUCTION")
print("       does not run in that space: _match_filter matches the RAW node_id")
print("       COLUMN, and in THAT space %d pairs collide. Filed as a row."
      % len(pair_counts))

matched_on = sorted({on_ for _, f in collisions for _, on in f for on_ in on})
settled = bool(collisions) and bool(destroyed) and not false_pos and same

print()
print("=" * 78)
print("== SETTLE VERDICT (ordered for the accept) ==")
print("SETTLED=%s" % ("YES" if settled else "BLOCKED"))
print("INSTRUMENT printed: pyiceberg %s StaticTable.from_metadata over"
      " s3://%s/... (the metadata_location the WRITER itself stamped into"
      " %s), plus boto3 s3:GetBucketPolicy on the AWS control plane."
      % (pyiceberg.__version__, MARKER_BUCKET, MARKER_KEY))
print("INSTRUMENT COVERAGE printed: %d of %d rows of globgrph.graph_nodes"
      " (the entire table, no filter) at vintage %s; and %d of %d S3_BUCKET"
      " node_ids probed live. NOT COVERED: rows written after that vintage,"
      " and the graph_edges table (a different cell)."
      % (N, N, marker.get("committed_at_iso"), len(live), len(bucket_names)))
if settled:
    print("DESTROYED_ROW_KEY printed: the S3_BUCKET_POLICY row whose node_id IS"
          " THE BARE BUCKET NAME. Concretely, for the %d buckets still carrying"
          " a policy row today: %s" % (len(collisions),
                                       ", ".join("%s" % b for b, _ in collisions)))
    print("DESTROYED_ROW_KEY printed (already destroyed, arm B): %s -- these %d"
          " buckets have a LIVE bucket policy on the AWS control plane and NO"
          " S3_BUCKET_POLICY row in the warehouse, and they are exactly the"
          " buckets the incremental updater has written."
          % (", ".join(destroyed), len(destroyed)))
    print("MATCHED_ON printed: %s -- the `node_id` column limb of"
          " _match_filter's In('arn',...) OR In('node_id',...). The policy row's"
          " OWN canonical key IS the bare bucket name, so the bucket's upsert"
          " filter names it. The `arn` limb does NOT match (the bucket's arn is"
          " the full ARN); the destruction is entirely the node_id limb."
          % "+".join(matched_on))
else:
    print("INSTRUMENTS_TRIED=2 of 2")
    print("WHAT_EACH_COULD_NOT_SEE printed: arm A snapshot agreement=%s;"
          " replay collisions=%d; arm B destroyed cell=%d; falsifier cell=%d."
          % (same, len(collisions), len(destroyed), len(false_pos)))
print("PROVENANCE LABELS: every number above is `measured` (an instrument"
      " returned it in THIS run). Nothing here is `held` or `inferred`.")
print("elapsed=%.1fs" % (time.time() - T0))
