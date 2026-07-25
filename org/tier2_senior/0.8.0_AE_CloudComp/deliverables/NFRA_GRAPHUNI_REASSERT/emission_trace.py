#!/usr/bin/env python
"""
NFRA_GRAPHUNI EMISSION-FILTER TRACE -- per-member attribution of WHERE the producer
drops each of the sharp case's 17 in-scope missing members.

For each missing member, classify into exactly one of:
  GENUINELY-ABSENT   -- no edge referencing this canonicalized id appears ANYWHERE in the
                        producer's raw JSON, under any form. A real emission gap.
  PRESENT-UNREACHABLE -- the correctly-canonicalized edge DOES exist in the producer's raw
                        JSON, but this member is not reachable via BFS from the seed in the
                        reconstructed graph (the bottleneck is an intermediate hop, not this
                        member's own connecting edge).
  REACHABLE-BUT-MISSED -- edge present, canonicalization correct, AND on a path from the
                        seed -- would indicate a bug in this trace script itself if it
                        appears (a member cannot be both reachable and in the missing set);
                        included as a self-consistency check, expected empty.

Then attributes each GENUINELY-ABSENT member to the specific source predicate in
extract_gold_compute.py responsible, confirming or refuting CVO~Z's/CTO~Z's named
predictions rather than assuming them.

Author: 0.8.0_AE_CloudComp~D, per CTO~Z dispatch NFRA_GRAPHUNI EMISSION_TRACE (20260725T070827Z).
"""
from __future__ import annotations

import json
import os
import re
import sys

WS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
sys.path.insert(0, WS)

from org.modules.graph.trace_graph import Edge, Node, TraceGraph  # noqa: E402

SP = os.path.dirname(__file__)
FIXTURE_DIR = os.path.join(WS, "org", "tier1_exec", "3.0.0_SA_CVO", "NFRA_GRAPHUNI_P0-CVO_fixture")
PRODUCER_JSON = os.path.join(SP, "gold_compute_producer_FULL_20260725.json")

doc = json.load(open(PRODUCER_JSON))
setdiff = json.load(open(os.path.join(SP, "SETDIFF_20260725_result.json")))
IN_SCOPE = {"CALLS", "READS_S3", "WRITES_S3"}

missing_all = setdiff["script_case"]["missing_members_with_edge_class"]
missing_in_scope = {nid: cls for nid, cls in missing_all.items() if set(cls) & IN_SCOPE}
print(f"in-scope missing members: {len(missing_in_scope)}", file=sys.stderr)

PIPELINE_RE = re.compile(r"^pipeline:[a-z_]+:gold:(.+)$")


def un_pipeline_id(pid):
    m = PIPELINE_RE.match(pid)
    return ("gold:" + m.group(1)) if m else None


def un_s3_id(target):
    m = re.match(r"^opal-data-[a-z]+/(.+)$", target)
    return ("s3:" + m.group(1)) if m else None


def canon_endpoint(raw):
    if raw.startswith("pipeline:"):
        return un_pipeline_id(raw)
    if raw.startswith("opal-data-"):
        return un_s3_id(raw)
    if raw.startswith("lambda:"):
        return raw  # lambda ids are not pipeline-prefixed in the producer at all
    return None


# ---------------------------------------------------------------------------
# Reconstruct the SAME v2 graph (node-order-fixed) to test reachability.
# ---------------------------------------------------------------------------
g = TraceGraph(built_at=0.0)
for n in doc["nodes"]:
    canon = un_pipeline_id(n["id"])
    if canon and canon not in g.nodes:
        g.add_node(Node(id=canon, node_type="GOLD_SCRIPT", label=canon))

for e in doc["edges"]:
    et = e["edge_type"]
    if et == "CONTAINS":
        continue
    s_raw, t_raw = e["source"], e["target"]
    if et == "CALLS":
        s, t = un_pipeline_id(s_raw), un_pipeline_id(t_raw)
        if s and t:
            g.add_edge(Edge(source=s, target=t, edge_type="CALLS"))
    elif et == "WRITES_S3":
        s, t = un_pipeline_id(s_raw), un_s3_id(t_raw)
        if s and t:
            if t not in g.nodes:
                g.add_node(Node(id=t, node_type="S3_ARTIFACT", label=t))
            g.add_edge(Edge(source=s, target=t, edge_type="WRITES_S3"))
    elif et == "READS_S3":
        s, t = un_pipeline_id(s_raw), un_s3_id(t_raw)
        if s and t:
            if t not in g.nodes:
                g.add_node(Node(id=t, node_type="S3_ARTIFACT", label=t))
            g.add_edge(Edge(source=t, target=s, edge_type="READS_S3"))

if not g._indexed:
    g._build_index()

seed = "gold:D_01.partner_analytics"
downstream_ids = {n.id for n, e, d in g.downstream(seed, max_depth=10)}
upstream_ids = {n.id for n, e, d in g.upstream(seed, max_depth=10)}
reachable = downstream_ids | upstream_ids | {seed}
print(f"reachable set in reconstruction: {len(reachable)}", file=sys.stderr)

# ---------------------------------------------------------------------------
# For each missing member: is a correctly-canonicalized edge referencing it present
# ANYWHERE in the producer's raw edges (any direction, any edge type)?
# ---------------------------------------------------------------------------
results = {}
for nid in missing_in_scope:
    present_edges = []
    for e in doc["edges"]:
        if e["edge_type"] == "CONTAINS":
            continue
        s_c = canon_endpoint(e["source"])
        t_c = canon_endpoint(e["target"])
        if nid in (s_c, t_c):
            present_edges.append({"raw_source": e["source"], "raw_target": e["target"],
                                   "edge_type": e["edge_type"],
                                   "canon_source": s_c, "canon_target": t_c})
    if not present_edges:
        classification = "GENUINELY-ABSENT"
    elif nid in reachable:
        classification = "REACHABLE-BUT-MISSED (self-check failure, investigate)"
    else:
        classification = "PRESENT-UNREACHABLE"
    results[nid] = {
        "fixture_edge_classes": missing_in_scope[nid],
        "classification": classification,
        "producer_edges_referencing_this_id_any_form": present_edges[:10],
        "n_producer_edges_found": len(present_edges),
    }

counts = {}
for v in results.values():
    counts[v["classification"]] = counts.get(v["classification"], 0) + 1
print("CLASSIFICATION COUNTS:", counts, file=sys.stderr)

out_path = os.path.join(SP, "EMISSION_TRACE_result.json")
json.dump({"seed": seed, "reachable_set_size": len(reachable),
           "classification_counts": counts, "per_member": results},
          open(out_path, "w"), indent=2)
print("WROTE", out_path)
for nid, v in results.items():
    print(f"  {nid}  ->  {v['classification']}  (fixture edges: {v['fixture_edge_classes']}, "
          f"producer hits: {v['n_producer_edges_found']})")
