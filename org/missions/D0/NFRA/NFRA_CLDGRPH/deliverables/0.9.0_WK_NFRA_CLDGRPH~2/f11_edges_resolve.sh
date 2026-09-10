#!/usr/bin/env bash
# F11-AC3 -- 100% OF THE BOUNDARY EDGES RESOLVE ON THE SERVED GRAPH AND THE NODE COUNT
# RECONCILES. TO-CG-F-11 step 5.
#
# TWO PLANES, NAMED, BECAUSE THEY ANSWER DIFFERENT HALVES:
#  * THE DENOMINATOR is the PRODUCER's own count for the day -- stitch_stats.derives_from /
#    stitch_stats.stored_in in the artifact the fold ingested (s3://.../stitch/stitch_graph.json,
#    whose sha256 is checked against the marker here, the same guard the fold applies).
#  * THE NUMERATOR is read from the SERVED graph through `bash .tools/comp-kuzu`. An edge can
#    only exist in the store if BOTH its endpoints do, so an edge counted there IS a resolved
#    edge -- and any edge whose ends did not resolve is missing from the numerator, which is
#    exactly what this criterion is asking.
# Reading both from the same plane would prove nothing: the producer cannot tell you what the
# projection kept, and the projection cannot tell you what the producer emitted.
#
# The reconciliation (admitted = merged + created, lost 0) is the producer's own accounting,
# read from that same artifact's meta.stitch_unify -- not from the local run and not from a log.
#
# A bare `bash` from a Python subprocess on this box is the WSL stub (row W2-S54); the executing
# bash is exported and used.
#
# Run from the repository root.
set -u
BASH_BIN="$(command -v bash)"
export BASH_BIN

python - <<'PY'
import datetime
import hashlib
import json
import os
import subprocess

import boto3

BASH = os.environ.get("BASH_BIN") or "bash"
BUCKET = "opal-313476888478-globgrph"
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def kuzu(q):
    p = subprocess.run([BASH, ".tools/comp-kuzu", "--json", q], capture_output=True, text=True)
    try:
        return json.loads(p.stdout), (p.stderr or "").strip()
    except Exception:  # noqa: BLE001
        return None, (p.stderr or "").strip()


s3 = boto3.client("s3", region_name="us-east-1")
marker = json.loads(s3.get_object(Bucket=BUCKET, Key="stitch/stitch_marker.json")["Body"].read())
raw = s3.get_object(Bucket=BUCKET, Key="stitch/stitch_graph.json")["Body"].read()
art_sha = hashlib.sha256(raw).hexdigest()
art = json.loads(raw)
meta = art.get("meta", {})
stats = meta.get("stitch_stats", {})
uni = meta.get("stitch_unify", {})

produced_derives = int(stats.get("derives_from", 0))
produced_stored = int(stats.get("stored_in", 0))

rows, _ = kuzu("MATCH ()-[e:CloudEdge]->() RETURN DISTINCT e.edge_type AS t, count(*) AS c ORDER BY t")
served_edges = {r["t"]: r["c"] for r in (rows or [])}


def served(*names):
    return sum(served_edges.get(n, 0) for n in names)


served_derives = served("derives_from", "DERIVES_FROM")
served_stored = served("stored_in", "STORED_IN")

admitted = int(uni.get("admitted", 0))
merged = int(uni.get("merged", 0))
created = int(uni.get("created", 0))
lost = int(uni.get("lost", 0))

print("F11-AC3 -- THE BOUNDARY EDGES RESOLVE AND THE NODE COUNT RECONCILES")
print("  live read at: %s   (served side through %s .tools/comp-kuzu)" % (now, BASH))
print()
print("DERIVES_FROM_RESOLVED=%d of %d" % (served_derives, produced_derives))
print("STORED_IN_RESOLVED=%d of %d" % (served_stored, produced_stored))
print("RECONCILED admitted=%d merged+created=%d lost=%d" % (admitted, merged + created, lost))
print()
print("  -- the artifact this is measured against --")
print("     key            : s3://%s/stitch/stitch_graph.json" % BUCKET)
print("     sha256         : %s" % art_sha)
print("     marker sha256  : %s" % marker.get("artifact_sha256"))
print("     SHA MATCHES MARKER: %s   (the fold's own first guard, re-run here)"
      % (art_sha == marker.get("artifact_sha256")))
print("     producer       : %s   built_at %s   git_sha %s"
      % (marker.get("producer"), marker.get("built_at"), marker.get("git_sha")))
print("     producer node/edge totals: %s / %s"
      % (marker.get("total_nodes"), marker.get("total_edges")))
print()
print("  -- the producer's unification accounting, verbatim from meta.stitch_unify --")
print("     %s" % json.dumps({k: uni.get(k) for k in
                              ("admitted", "merged", "created", "lost", "edges_rewritten",
                               "idmap_size", "retyped_prior_cycle", "collapsed_copies")},
                             sort_keys=True))
print("     per_type: %s" % json.dumps(uni.get("per_type", {}), sort_keys=True))
print()
print("  -- every stitch edge family, served side, printed UNSCOPED --")
for t in sorted(served_edges):
    print("     %-24s %d" % (t, served_edges[t]))
print()
print("  -- the CONTROL --")
print("     the two numerators come from the SERVED store and the two denominators from the")
print("     PRODUCER's artifact; a fold that dropped an edge for an unresolved endpoint would")
print("     show as a numerator BELOW its denominator, and a projection that never ran would")
print("     show the previous day's numbers against today's artifact sha.")
print()
print("  DENOMINATOR: 2 of 2 boundary edge families the criterion names; %d distinct edge_type "
      "value(s) in the served graph read unscoped beside them; 1 of 1 artifact, identified by "
      "sha256 against the marker the fold checks." % len(served_edges))
PY
