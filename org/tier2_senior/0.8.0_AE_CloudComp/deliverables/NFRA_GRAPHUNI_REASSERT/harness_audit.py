#!/usr/bin/env python
"""
NFRA_GRAPHUNI HARNESS-AUDIT -- reconcile the producer's emitted edge set against the
v2 reconstruction's held edge set, printing the drop count BY REASON. Every dropped
edge must be accounted for by a named intended reason, or the harness is not fit to
measure the producer (CVO~Z's bar, CTO~Z's dispatch, 20260725T073908Z).

Positive control: s3:silver/prices/canonical_prices.parquet, expected writer count 18
(CVO~Z's independent count applying PIPELINE_RE + un_s3_id + the if-s-and-t guard
verbatim to the raw JSON -- zero guard-dropped, gold:INF_build_canonical_prices among
the 18 survivors). v2's own run reported 16 writers into this node -- this script finds
exactly where the missing >=2 go, line-level.

Author: 0.8.0_AE_CloudComp~D, per CTO~Z dispatch NFRA_GRAPHUNI HARNESS-AUDIT.
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
PRODUCER_JSON = os.path.join(SP, "gold_compute_producer_FULL_20260725.json")
doc = json.load(open(PRODUCER_JSON))

PIPELINE_RE = re.compile(r"^pipeline:[a-z_]+:gold:(.+)$")


def un_pipeline_id(pid):
    m = PIPELINE_RE.match(pid)
    return ("gold:" + m.group(1)) if m else None


def un_s3_id(target):
    m = re.match(r"^opal-data-[a-z]+/(.+)$", target)
    return ("s3:" + m.group(1)) if m else None


# ---------------------------------------------------------------------------
# Reproduce the v2 reconstruction EXACTLY, but instrumented: classify every raw edge's
# fate by reason before it either lands in the graph or gets dropped.
# ---------------------------------------------------------------------------
drop_reasons = {
    "CONTAINS-skip": 0,
    "unmapped-source (un_pipeline_id failed)": 0,
    "unmapped-target (un_s3_id/un_pipeline_id failed)": 0,
    "kept": 0,
}
drop_examples = {k: [] for k in drop_reasons}

g = TraceGraph(built_at=0.0)
node_pre_pop_order = []
for n in doc["nodes"]:
    canon = un_pipeline_id(n["id"])
    if canon and canon not in g.nodes:
        g.add_node(Node(id=canon, node_type="GOLD_SCRIPT", label=canon))
        node_pre_pop_order.append(canon)
pre_populated_ids = set(g.nodes.keys())
print(f"pre-populated nodes (from doc['nodes'], GOLD_SCRIPT only): {len(pre_populated_ids)}", file=sys.stderr)

edge_before_add = set()   # (source, target, edge_type) BEFORE calling add_edge
edge_dupe_count = 0

for e in doc["edges"]:
    et = e["edge_type"]
    if et == "CONTAINS":
        drop_reasons["CONTAINS-skip"] += 1
        continue
    s_raw, t_raw = e["source"], e["target"]
    if et == "CALLS":
        s, t = un_pipeline_id(s_raw), un_pipeline_id(t_raw)
        if not s:
            drop_reasons["unmapped-source (un_pipeline_id failed)"] += 1
            if len(drop_examples["unmapped-source (un_pipeline_id failed)"]) < 5:
                drop_examples["unmapped-source (un_pipeline_id failed)"].append(e)
            continue
        if not t:
            drop_reasons["unmapped-target (un_s3_id/un_pipeline_id failed)"] += 1
            if len(drop_examples["unmapped-target (un_s3_id/un_pipeline_id failed)"]) < 5:
                drop_examples["unmapped-target (un_s3_id/un_pipeline_id failed)"].append(e)
            continue
        key = (s, t, "CALLS")
        if key in edge_before_add:
            edge_dupe_count += 1
        edge_before_add.add(key)
        g.add_edge(Edge(source=s, target=t, edge_type="CALLS"))
        drop_reasons["kept"] += 1
    elif et == "WRITES_S3":
        s, t = un_pipeline_id(s_raw), un_s3_id(t_raw)
        if not s:
            drop_reasons["unmapped-source (un_pipeline_id failed)"] += 1
            if len(drop_examples["unmapped-source (un_pipeline_id failed)"]) < 5:
                drop_examples["unmapped-source (un_pipeline_id failed)"].append(e)
            continue
        if not t:
            drop_reasons["unmapped-target (un_s3_id/un_pipeline_id failed)"] += 1
            if len(drop_examples["unmapped-target (un_s3_id/un_pipeline_id failed)"]) < 5:
                drop_examples["unmapped-target (un_s3_id/un_pipeline_id failed)"].append(e)
            continue
        if t not in g.nodes:
            g.add_node(Node(id=t, node_type="S3_ARTIFACT", label=t))
        key = (s, t, "WRITES_S3")
        if key in edge_before_add:
            edge_dupe_count += 1
        edge_before_add.add(key)
        g.add_edge(Edge(source=s, target=t, edge_type="WRITES_S3"))
        drop_reasons["kept"] += 1
    elif et == "READS_S3":
        s, t = un_pipeline_id(s_raw), un_s3_id(t_raw)
        if not s:
            drop_reasons["unmapped-source (un_pipeline_id failed)"] += 1
            continue
        if not t:
            drop_reasons["unmapped-target (un_s3_id/un_pipeline_id failed)"] += 1
            continue
        if t not in g.nodes:
            g.add_node(Node(id=t, node_type="S3_ARTIFACT", label=t))
        key = (t, s, "READS_S3")  # polarity flip
        if key in edge_before_add:
            edge_dupe_count += 1
        edge_before_add.add(key)
        g.add_edge(Edge(source=t, target=s, edge_type="READS_S3"))
        drop_reasons["kept"] += 1

total_raw = len(doc["edges"])
total_accounted = sum(drop_reasons.values())
print("=" * 70, file=sys.stderr)
print(f"TOTAL RAW EDGES: {total_raw}  ACCOUNTED: {total_accounted}  "
      f"{'MATCH' if total_raw == total_accounted else 'MISMATCH -- UNACCOUNTED LOSS'}", file=sys.stderr)
print(f"DROP-COUNT BY REASON: {json.dumps({k: v for k, v in drop_reasons.items()}, indent=2)}", file=sys.stderr)
print(f"DUPLICATE (source,target,type) triples seen more than once before add_edge: {edge_dupe_count}",
      file=sys.stderr)

# ---------------------------------------------------------------------------
# POSITIVE CONTROL: s3:silver/prices/canonical_prices.parquet writer count.
# ---------------------------------------------------------------------------
target_key = "s3:silver/prices/canonical_prices.parquet"
if not g._indexed:
    g._build_index()
writers_in_graph = sorted({e.source for e in g._reverse.get(target_key, [])})
print("=" * 70, file=sys.stderr)
print(f"GRAPH writers into {target_key}: {len(writers_in_graph)}", file=sys.stderr)
for w in writers_in_graph:
    print(f"    {w}", file=sys.stderr)

raw_writers_expected = []
for e in doc["edges"]:
    if e["edge_type"] != "WRITES_S3":
        continue
    s, t = un_pipeline_id(e["source"]), un_s3_id(e["target"])
    if s and t == target_key:
        raw_writers_expected.append((e["source"], s))
print(f"RAW-JSON writers that SHOULD survive (un_pipeline_id + un_s3_id both succeed): "
      f"{len(raw_writers_expected)}", file=sys.stderr)

missing_from_graph = [s for (raw, s) in raw_writers_expected if s not in writers_in_graph]
print(f"MISSING FROM GRAPH despite surviving both transforms: {len(missing_from_graph)}", file=sys.stderr)
for m in missing_from_graph:
    print(f"    {m}", file=sys.stderr)
    # find its raw edge(s) and check node pre-population status
    raw_matches = [e for e in doc["edges"] if e["edge_type"] == "WRITES_S3"
                  and un_pipeline_id(e["source"]) == m and un_s3_id(e["target"]) == target_key]
    for rm in raw_matches:
        print(f"        raw edge: {rm}", file=sys.stderr)
        print(f"        source pre-populated as a node? {m in pre_populated_ids}", file=sys.stderr)
        print(f"        source in g.nodes at audit end? {m in g.nodes}", file=sys.stderr)
        print(f"        (s,t,type) was added to edge_before_add set? "
              f"{(m, target_key, 'WRITES_S3') in edge_before_add}", file=sys.stderr)

out_path = os.path.join(SP, "HARNESS_AUDIT_result.json")
json.dump({
    "total_raw_edges": total_raw, "total_accounted": total_accounted,
    "drop_reasons": drop_reasons, "drop_examples": drop_examples,
    "duplicate_triples": edge_dupe_count,
    "positive_control": {
        "target_key": target_key,
        "graph_writer_count": len(writers_in_graph),
        "graph_writers": writers_in_graph,
        "raw_expected_writer_count": len(raw_writers_expected),
        "missing_from_graph_despite_surviving_transforms": missing_from_graph,
    },
}, open(out_path, "w"), indent=2)
print("WROTE", out_path)
