#!/usr/bin/env python
"""
NFRA_GRAPHUNI EMISSION-FILTER TRACE -- predict-then-measure control.

PREDICTION (written BEFORE running this script, per the dispatch's explicit order
requirement -- see GRAPHUNI_EMISSION_TRACE.md for the prediction text as committed):
held-out target s3:gold/timeseries/client_performance.parquet. Model built from the
sharp case: 13/17 (76%) PRESENT-UNREACHABLE, 4/17 (24%) GENUINELY-ABSENT (both lambda:
members + 2 s3: members). Prediction: the majority of this target's missing members
will classify PRESENT-UNREACHABLE; any GENUINELY-ABSENT members will skew toward
non-GOLD_SCRIPT node types (lambda:) rather than gold:/s3: members, since :94's
GOLD_SCRIPT-only slice is the one CONFIRMED predicate from the sharp-case trace.

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

HELD_OUT_TARGET = "s3:gold/timeseries/client_performance.parquet"

doc = json.load(open(PRODUCER_JSON))
fixture = json.load(open(os.path.join(FIXTURE_DIR, "fixture_layer_a.tool_answers.json")))
old = fixture["tool"]
IN_SCOPE = {"CALLS", "READS_S3", "WRITES_S3"}

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
        return raw
    return None


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

downstream_ids = {n.id for n, e, d in g.downstream(HELD_OUT_TARGET, max_depth=10)}
upstream_ids = {n.id for n, e, d in g.upstream(HELD_OUT_TARGET, max_depth=10)}
reachable = downstream_ids | upstream_ids | {HELD_OUT_TARGET}

old_ids = set(old["comp-blast"].get(HELD_OUT_TARGET, {}).get("radius_ids", []))
new_ids = reachable  # cmd_blast's actual radius computation for an s3: seed is downstream+upstream too
missing = sorted(old_ids - new_ids)

results = {}
for nid in missing:
    present_edges = []
    for e in doc["edges"]:
        if e["edge_type"] == "CONTAINS":
            continue
        s_c = canon_endpoint(e["source"])
        t_c = canon_endpoint(e["target"])
        if nid in (s_c, t_c):
            present_edges.append(e["edge_type"])
    classification = "GENUINELY-ABSENT" if not present_edges else (
        "REACHABLE-BUT-MISSED(bug)" if nid in reachable else "PRESENT-UNREACHABLE")
    results[nid] = {"classification": classification, "n_producer_edges_found": len(present_edges),
                    "node_type_prefix": nid.split(":", 1)[0]}

counts = {}
for v in results.values():
    counts[v["classification"]] = counts.get(v["classification"], 0) + 1

genuinely_absent_prefixes = [v["node_type_prefix"] for v in results.values()
                            if v["classification"] == "GENUINELY-ABSENT"]

print(f"HELD-OUT TARGET: {HELD_OUT_TARGET}", file=sys.stderr)
print(f"old_n={len(old_ids)} new_n={len(new_ids)} missing_n={len(missing)}", file=sys.stderr)
print(f"MEASURED CLASSIFICATION COUNTS: {counts}", file=sys.stderr)
print(f"genuinely-absent node-type prefixes: {genuinely_absent_prefixes}", file=sys.stderr)

out_path = os.path.join(SP, "EMISSION_TRACE_CONTROL_result.json")
json.dump({"held_out_target": HELD_OUT_TARGET, "old_n": len(old_ids), "new_n": len(new_ids),
           "missing_n": len(missing), "classification_counts": counts,
           "genuinely_absent_prefixes": genuinely_absent_prefixes, "per_member": results},
          open(out_path, "w"), indent=2)
print("WROTE", out_path)
