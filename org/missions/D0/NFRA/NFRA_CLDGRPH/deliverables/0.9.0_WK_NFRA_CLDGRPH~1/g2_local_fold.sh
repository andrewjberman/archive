#!/usr/bin/env bash
# NFRA_CLDGRPH TO-CG-G-2 / G2-AC2 (default) and G2-AC3 (--reconcile).
#
# A LOCAL FOLD OVER THE REAL SNAPSHOT. IT IS NOT A SERVED READ AND MUST NOT BE REPORTED AS
# ONE. Nothing here runs a producer in the cloud, starts an ECS task or a CodeBuild, builds
# or pushes an image, applies Terraform, or writes a single byte to S3. Every S3 call below
# is a GET or a HEAD.
#
# WHAT IT DOES, and each step names which plane it exercises:
#   1. GET the real AWS snapshot (the derive graph as last night's derive archived it) and
#      the real stitch artifact + marker.
#   2. PRODUCER PLANE: call the patched derive_stitch._index_aws on those real bytes and
#      show the bucket index now yields the CANONICAL endpoint; call the patched
#      derive_runner.stitch_served_from and let it emit SERVED_FROM itself.
#   3. FOLD PLANE: call the real derive_runner.fold_stitch_document on the real artifact --
#      which was produced by the OLD, un-updated producer, so its STORED_IN targets are
#      bucket NAMES. That is deliberate: it is the evidence that the fold repairs a
#      producer that has not moved yet, which is what "it fixes every producer feeding it"
#      has to mean. Then call derive_runner.normalize_edge_endpoints.
#   4. JOIN PLANE: re-implement kuzu_nessie_load's key rule (:204) and its endpoint match
#      (:249-253) locally and read WHAT EACH EDGE LANDS ON, before and after.
#
# Run from the repository root.
set -u

python - "$@" <<'PY'
import datetime
import hashlib
import io
import json
import sys
import tarfile
from pathlib import Path

ROOT = Path.cwd()
for _p in (str(ROOT), str(ROOT / "org" / "modules" / "graph"),
           str(ROOT / "infra" / "aws" / "globgrph")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import boto3
import derive_runner as DR
import derive_stitch as DS
from org.modules.graph.grain_sentinel import run_grain_sentinel

RECONCILE = "--reconcile" in sys.argv[1:]
BUCKET = "opal-313476888478-globgrph"
# CG-s-32's served denominators, from the drained TO-CG-G-1 instance. A STORED baseline
# from the SERVED plane, quoted here and never re-derived by this local run.
CENSUS_STORED_IN = 135
CENSUS_SERVED_FROM = 27
CENSUS_POLICY_NODES = 15
# The five canonical magnitudes the CVO signed at round 6.
MAGNITUDES = {"PipelineScript": 167, "PipelineFunction": 1217, "S3Key": 381,
              "Component": 201, "ReactQueryKey": 125}

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
s3 = boto3.client("s3", region_name="us-east-1")

snap_key = s3.get_object(Bucket=BUCKET, Key="snapshots/latest.txt")["Body"].read().decode().strip()
snap_raw = s3.get_object(Bucket=BUCKET, Key=snap_key)["Body"].read()
_tf = tarfile.open(fileobj=io.BytesIO(snap_raw))
graph = json.loads(_tf.extractfile(_tf.getmembers()[0]).read())

marker = json.loads(s3.get_object(Bucket=BUCKET,
                                  Key=DR.STITCH_MARKER_KEY)["Body"].read())
art_body = s3.get_object(Bucket=BUCKET, Key=DR.STITCH_ARTIFACT_KEY)["Body"].read()
art_sha = hashlib.sha256(art_body).hexdigest()
art = json.loads(art_body)
stitch_stats = (art.get("meta") or {}).get("stitch_stats") or {}
unify = (art.get("meta") or {}).get("stitch_unify") or {}


def served_key(n):
    """kuzu_nessie_load.py:204 -- graph_key(arn) or graph_key(node_id). The JOIN's rule."""
    return str(n.get("arn") or "").strip() or str(n.get("id") or "").strip()


def join(g):
    """kuzu_nessie_load's load, locally: key the nodes, then match endpoints RAW.

    MERGE-style dedup on (src, dst, edge_type, props) exactly as :253 does, so a family's
    count here is EDGES STORED and not MERGE attempts (the S8 lesson, kept).
    """
    best = {}
    for cdata in g.get("classes_data", {}).values():
        for n in cdata.get("nodes", []) or []:
            k = served_key(n)
            if k:
                best.setdefault(k, n)
    seen = set()
    landings = []
    skipped = 0
    for e in g.get("edges", []) or []:
        src = e.get("source", e.get("src", ""))
        dst = e.get("target", e.get("dst", ""))
        src = str((src or {}).get("id", "") if isinstance(src, dict) else (src or "")).strip()
        dst = str((dst or {}).get("id", "") if isinstance(dst, dict) else (dst or "")).strip()
        et = str(e.get("edge_type", ""))
        if src not in best or dst not in best:
            skipped += 1
            continue
        ident = (src, dst, et, str(e.get("props", "")))
        if ident in seen:
            continue
        seen.add(ident)
        landings.append({"edge_type": et, "src": src, "dst": dst,
                         "src_type": str(best[src].get("type", "")),
                         "dst_type": str(best[dst].get("type", ""))})
    return landings, skipped, len(best)


def by_target_type(landings, family):
    out = {}
    for x in landings:
        if x["edge_type"] == family:
            out[x["dst_type"]] = out.get(x["dst_type"], 0) + 1
    return dict(sorted(out.items()))


def keys_of(landings, family):
    return len({x["src"] for x in landings if x["edge_type"] == family})


print("G2-AC%s -- THE BUCKET IDENTITY MADE ONE, ON A LOCAL FOLD OVER THE REAL SNAPSHOT"
      % ("3 (--reconcile)" if RECONCILE else "2"))
print("  local run at: %s" % now)
print("INSTRUMENT: derive_runner.fold_stitch_document + normalize_edge_endpoints +"
      " stitch_served_from and derive_stitch._index_aws, called IN THIS PROCESS on bytes"
      " GET from S3; the join is kuzu_nessie_load.py:204/:249-253 re-implemented here.")
print("  THIS IS A LOCAL FOLD, NOT A SERVED READ. It says what the NEXT derive would put"
      " into Iceberg, not what the projection is serving now. The served re-take of"
      " F11-AC3 is a later cut, gated on the egress hold.")
print("COVERAGE: the whole snapshot (%d node class(es)) and the whole stitch artifact;"
      " no sampling, no LIMIT." % len(graph.get("classes_data", {})))
print("GRAIN: one EDGE per row, counted per family with its distinct SOURCE keys beside it;"
      " the landing is a node CLASS.")
print("ENVIRONMENT of the stored baselines: CG-s-32's served census (STORED_IN 135,"
      " SERVED_FROM 27, both 100%% onto S3_BUCKET_POLICY, %d shadow nodes) from the drained"
      " TO-CG-G-1 instance; the producer-side denominators from this artifact's own"
      " meta.stitch_stats. Neither is re-derived by this local run." % CENSUS_POLICY_NODES)
print("SNAPSHOT=%s" % snap_key)
print("ARTIFACT=s3://%s/%s sha256=%s marker_sha256=%s SHA_MATCHES_MARKER=%s"
      % (BUCKET, DR.STITCH_ARTIFACT_KEY, art_sha, marker.get("artifact_sha256"),
         art_sha == marker.get("artifact_sha256")))
print("")

# ---------------------------------------------------------------- the BEFORE landing
before_landings, before_skipped, before_keys = join(graph)
before_stored = by_target_type(before_landings, "STORED_IN")
before_served = by_target_type(before_landings, "SERVED_FROM")
before_derives = by_target_type(before_landings, "DERIVES_FROM")
print("  -- BEFORE: the snapshot exactly as last night's derive archived it --")
print("     STORED_IN    by target class: %s   keys=%d"
      % (before_stored or "(none)", keys_of(before_landings, "STORED_IN")))
print("     SERVED_FROM  by target class: %s   keys=%d"
      % (before_served or "(none)", keys_of(before_landings, "SERVED_FROM")))
print("     DERIVES_FROM by target class: %s   keys=%d"
      % (before_derives or "(none)", keys_of(before_landings, "DERIVES_FROM")))
print("")

# ---------------------------------------------------------------- the PRODUCER plane
lam_by_name, bkt_by_name, aws_keys = DS._index_aws(graph)
canonical_bkt = sum(1 for v in bkt_by_name.values() if str(v).startswith("arn:aws:s3:::"))
print("  -- PRODUCER PLANE: derive_stitch._index_aws on the real snapshot --")
print("     BUCKET_INDEX_CANONICAL=%d of %d bucket(s) now yield the arn (was 0 of %d: the"
      " index returned `nid or arn`, the short name)"
      % (canonical_bkt, len(bkt_by_name), len(bkt_by_name)))
print("     example: %s -> %s" % tuple(list(bkt_by_name.items())[0]) if bkt_by_name else "")
print("")

# Strip the three carry-forward families; the fold and the producer re-emit them below.
# derive_stitch does exactly this for STORED_IN, and for the same reason: an edge arriving
# in the snapshot is by construction a PREVIOUS cycle's output.
carried = {"STORED_IN": 0, "SERVED_FROM": 0, "DERIVES_FROM": 0}
kept_edges = []
for e in graph.get("edges", []) or []:
    et = str(e.get("edge_type", ""))
    if et in carried:
        carried[et] += 1
        continue
    kept_edges.append(e)
graph["edges"] = kept_edges
print("  -- carry-forward stripped before the re-fold (previous cycle's own output) --")
print("     %s" % json.dumps(carried, sort_keys=True))
print("")

# ---------------------------------------------------------------- the FOLD plane
vintage = DR.fold_stitch_document(graph, art_body, marker)
if vintage is None:
    print("BLOCKED: the fold refused the artifact (sha or parse). No numbers below.")
    sys.exit(1)

served_from_err = None
try:
    DR.stitch_served_from(graph)
except Exception as ex:  # noqa: BLE001
    served_from_err = "%s: %s" % (type(ex).__name__, ex)
    print("WARN: SERVED_FROM_LOCAL_EMIT_FAIL %s" % served_from_err)

norm = DR.normalize_edge_endpoints(graph)
print("")

# ---------------------------------------------------------------- the JOIN plane
after_landings, after_skipped, after_keys = join(graph)
after_stored = by_target_type(after_landings, "STORED_IN")
after_served = by_target_type(after_landings, "SERVED_FROM")
after_derives = by_target_type(after_landings, "DERIVES_FROM")

stored_total = sum(after_stored.values())
served_total = sum(after_served.values())
stored_on_bucket = after_stored.get("S3_BUCKET", 0)
served_on_bucket = after_served.get("S3_BUCKET", 0)
policy_hits = after_stored.get("S3_BUCKET_POLICY", 0) + after_served.get("S3_BUCKET_POLICY", 0)
derives_total = sum(after_derives.values())
produced_derives = int(stitch_stats.get("derives_from", 0) or 0)
produced_stored = int(stitch_stats.get("stored_in", 0) or 0)

print("  -- AFTER: what the next derive would commit --")
print("     STORED_IN    by target class: %s   keys=%d"
      % (after_stored or "(none)", keys_of(after_landings, "STORED_IN")))
print("     SERVED_FROM  by target class: %s   keys=%d"
      % (after_served or "(none)", keys_of(after_landings, "SERVED_FROM")))
print("     DERIVES_FROM by target class: %s   keys=%d"
      % (after_derives or "(none)", keys_of(after_landings, "DERIVES_FROM")))
print("")

if not RECONCILE:
    print("LOCAL_FOLD_STORED_IN_ON_S3_BUCKET=%d of %d resolved STORED_IN edge(s) in this "
          "local fold (CG-s-32's SERVED denominator was %d of 137 emitted, 100 percent of "
          "it on S3_BUCKET_POLICY; the producer emitted %d this cycle)"
          % (stored_on_bucket, stored_total, CENSUS_STORED_IN, produced_stored))
    print("LOCAL_FOLD_SERVED_FROM_ON_S3_BUCKET=%d of %d resolved SERVED_FROM edge(s) in this "
          "local fold (CG-s-32's SERVED denominator: %d, 100 percent of it on "
          "S3_BUCKET_POLICY)" % (served_on_bucket, served_total, CENSUS_SERVED_FROM))
    print("ON_S3_BUCKET_POLICY=%d across both families  (was %d + %d = %d before this "
          "change, by the census)"
          % (policy_hits, CENSUS_STORED_IN, CENSUS_SERVED_FROM,
             CENSUS_STORED_IN + CENSUS_SERVED_FROM))
    print("DERIVES_FROM_RESOLVED=%d of %d emitted by the producer this cycle "
          "(meta.stitch_stats.derives_from)" % (derives_total, produced_derives))
    print("")
    print("  -- the consequence a reader must not miss --")
    all_policy = sum(1 for x in after_landings
                     if x["dst_type"] == "S3_BUCKET_POLICY" or x["src_type"] == "S3_BUCKET_POLICY")
    print("     EDGES_TOUCHING_S3_BUCKET_POLICY_AFTER=%d of %d edge(s) in the local fold. "
          "The two families that landed there were its ONLY edges (CG-s-32: it appears as a "
          "target in SERVED_FROM and STORED_IN and nowhere else, and never as a source), so "
          "the class becomes an ISLAND. debtscan_canon_scorer.py:48/:144 declares "
          "ServedURL-[SERVED_FROM]->S3_BUCKET_POLICY as AUTH_CANON's live shape and WILL "
          "score differently; that scorer is NOT this order's to edit and the change is "
          "filed as a row." % (all_policy, len(after_landings)))
    print("     ENDPOINT_CANONICALIZE: %s"
          % json.dumps({k: norm[k] for k in ("aliases", "ambiguous_aliases",
                                             "endpoints_rewritten", "edges_touched",
                                             "resolvable_before", "resolvable_after")},
                       sort_keys=True))
    print("     by_edge_type: %s" % json.dumps(norm["by_edge_type"], sort_keys=True))
    print("")
    print("  DENOMINATOR: 3 of 3 edge families the criterion names, over %d resolved edge(s) "
          "in a local fold of 1 of 1 snapshot (%s) and 1 of 1 stitch artifact identified by "
          "sha256 against its own marker; %d endpoint(s) skipped as unresolved by the join "
          "(was %d before)." % (len(after_landings), snap_key, after_skipped, before_skipped))
    ok = (stored_on_bucket > 0 and served_on_bucket > 0 and policy_hits == 0
          and derives_total > 0)
    # Re-stated at the FOOT as well as the head: every number above came from THIS
    # snapshot, and a reader who scrolls to the verdict must not have to scroll back for
    # the vintage the verdict is about.
    print("SNAPSHOT=%s   ARTIFACT_SHA256=%s" % (snap_key, art_sha))
    print("LOCAL_FOLD_RESULT=%s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)

# ---------------------------------------------------------------- G2-AC3, --reconcile
admitted = int(unify.get("admitted", 0) or 0)
merged = int(unify.get("merged", 0) or 0)
created = int(unify.get("created", 0) or 0)
lost = int(unify.get("lost", 0) or 0)
print("RECONCILED admitted=%d merged+created=%d lost=%d" % (admitted, merged + created, lost))
print("  source: the PRODUCER's own accounting, meta.stitch_unify in the artifact whose "
      "sha256 matches its marker -- not this local run and not a log.")
print("  per_type: %s" % json.dumps(unify.get("per_type", {}), sort_keys=True))
print("")

all_nodes = [n for v in graph.get("classes_data", {}).values() for n in v.get("nodes", [])]
grain = run_grain_sentinel(all_nodes, DS._load_grain_baseline())
print(grain.render())
print("  source: org.modules.graph.grain_sentinel, the estate's OWN producer-side bar, run "
      "here on the LOCAL FOLD's %d node(s) against org/modules/graph/grain_baseline.json."
      % len(all_nodes))
print("")

counts = {}
for n in all_nodes:
    t = str(n.get("type", ""))
    if t in MAGNITUDES:
        counts[t] = counts.get(t, 0) + 1
unchanged = 0
print("  -- the five canonical magnitudes the CVO signed --")
for t in sorted(MAGNITUDES):
    got = counts.get(t, 0)
    same = got == MAGNITUDES[t]
    unchanged += 1 if same else 0
    print("     %-18s local_fold=%-6d signed=%-6d %s"
          % (t, got, MAGNITUDES[t], "UNCHANGED" if same else "MOVED -- a ROW before a fix"))
print("MAGNITUDES_UNCHANGED=%d of %d" % (unchanged, len(MAGNITUDES)))
print("")
print("  DENOMINATOR: 1 of 1 artifact reconciliation read from meta.stitch_unify; 1 of 1 "
      "grain-sentinel run over %d node(s); %d of %d signed magnitude(s) unchanged; the "
      "snapshot is %s." % (len(all_nodes), unchanged, len(MAGNITUDES), snap_key))
ok = (admitted == merged + created and lost == 0 and grain.passed
      and unchanged == len(MAGNITUDES))
print("RECONCILE_RESULT=%s" % ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
PY
