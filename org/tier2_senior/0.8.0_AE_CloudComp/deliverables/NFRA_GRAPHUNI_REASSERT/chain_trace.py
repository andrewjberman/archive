#!/usr/bin/env python
"""
NFRA_GRAPHUNI CHAIN-TRACE -- for each PRESENT-UNREACHABLE member, walk the FIXTURE's own
shortest seed->member path and identify the FIRST hop (edge) absent from the producer's
reconstructed edge set. Scope: gold subset first (dominant, 47 of 60 across both
measured targets), positions_cube family as the named probe.

Path definition (explicit, since "the path" is otherwise ambiguous): the SHORTEST
BFS path in the FIXTURE's own pinned pre-delta graph from the seed to the member, in
whichever direction (downstream/upstream) actually discovers it -- reconstructed by
walking each node's first-discovery edge (BFS parent pointers) back to depth 0. This is
a well-defined, reproducible choice, not necessarily the ONLY path the fixture's
216-member radius implies, but it is A real path that exists in the fixture graph and
is sufficient to name a first broken hop.

Author: 0.8.0_AE_CloudComp~D, per CTO~Z dispatch NFRA_GRAPHUNI CHAIN-TRACE (20260725T071845Z).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

WS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
sys.path.insert(0, WS)

from org.modules.graph.trace_graph import Edge, Node, TraceGraph  # noqa: E402

SP = os.path.dirname(__file__)
FIXTURE_DIR = os.path.join(WS, "org", "tier1_exec", "3.0.0_SA_CVO", "NFRA_GRAPHUNI_P0-CVO_fixture")
PRODUCER_JSON = os.path.join(SP, "gold_compute_producer_FULL_20260725.json")
SEED = "gold:D_01.partner_analytics"

doc = json.load(open(PRODUCER_JSON))
PIPELINE_RE = re.compile(r"^pipeline:[a-z_]+:gold:(.+)$")


def un_pipeline_id(pid):
    m = PIPELINE_RE.match(pid)
    return ("gold:" + m.group(1)) if m else None


def un_s3_id(target):
    m = re.match(r"^opal-data-[a-z]+/(.+)$", target)
    return ("s3:" + m.group(1)) if m else None


# --- reconstruct v2 producer graph, keep a fast edge-membership set ---
prod_edges = set()  # (source, target, edge_type)
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
            prod_edges.add((s, t, "CALLS"))
    elif et == "WRITES_S3":
        s, t = un_pipeline_id(s_raw), un_s3_id(t_raw)
        if s and t:
            if t not in g.nodes:
                g.add_node(Node(id=t, node_type="S3_ARTIFACT", label=t))
            g.add_edge(Edge(source=s, target=t, edge_type="WRITES_S3"))
            prod_edges.add((s, t, "WRITES_S3"))
    elif et == "READS_S3":
        s, t = un_pipeline_id(s_raw), un_s3_id(t_raw)
        if s and t:
            if t not in g.nodes:
                g.add_node(Node(id=t, node_type="S3_ARTIFACT", label=t))
            g.add_edge(Edge(source=t, target=s, edge_type="READS_S3"))
            prod_edges.add((t, s, "READS_S3"))

m0 = g.find_node(SEED)
assert m0 and m0[0].id == SEED, "node-order fix regressed"

# --- load the FIXTURE's own pinned graph (the source of truth for "the path") ---
fixture_graph = TraceGraph.load(Path(os.path.join(FIXTURE_DIR, "graph.json.pinned_predelta")))
if not fixture_graph._indexed:
    fixture_graph._build_index()


def bfs_with_parents(tg, start, max_depth=10):
    """Like TraceGraph.downstream()/upstream() but also returns a parent map:
    node_id -> (predecessor_node_id, Edge, direction) for the first-discovery edge."""
    visited = {start}
    queue = [(start, 0)]
    down_parent = {}
    while queue:
        cur, depth = queue.pop(0)
        if depth >= max_depth:
            continue
        for e in tg._forward.get(cur, []):
            if e.target not in visited:
                visited.add(e.target)
                down_parent[e.target] = (cur, e, "downstream")
                queue.append((e.target, depth + 1))
    up_parent = {}
    visited2 = {start}
    queue2 = [(start, 0)]
    while queue2:
        cur, depth = queue2.pop(0)
        if depth >= max_depth:
            continue
        for e in tg._reverse.get(cur, []):
            if e.source not in visited2:
                visited2.add(e.source)
                up_parent[e.source] = (cur, e, "upstream")
                queue2.append((e.source, depth + 1))
    return down_parent, up_parent


down_parent, up_parent = bfs_with_parents(fixture_graph, SEED)


def path_to(member):
    """Reconstruct the shortest seed->member path (list of edges, seed-first order)."""
    if member in down_parent:
        parent = down_parent
        direction = "downstream"
    elif member in up_parent:
        parent = up_parent
        direction = "upstream"
    else:
        return None, None
    chain = []
    cur = member
    while cur != SEED:
        pred, edge, _ = parent[cur]
        chain.append(edge)
        cur = pred
    chain.reverse()
    return chain, direction


def hop_present_in_producer(edge):
    return (edge.source, edge.target, edge.edge_type) in prod_edges


# ---------------------------------------------------------------------------
# Scope: gold-subset PRESENT-UNREACHABLE members from the sharp case, starting with the
# positions_cube family probe named in the ruling.
# ---------------------------------------------------------------------------
emission_trace = json.load(open(os.path.join(SP, "EMISSION_TRACE_result.json")))
gold_present_unreachable = [nid for nid, v in emission_trace["per_member"].items()
                           if v["classification"] == "PRESENT-UNREACHABLE" and nid.startswith("gold:")]
print(f"gold PRESENT-UNREACHABLE members to trace: {len(gold_present_unreachable)}", file=sys.stderr)

results = {}
first_hops = {}
for member in gold_present_unreachable:
    chain, direction = path_to(member)
    if chain is None:
        results[member] = {"error": "not found in fixture graph BFS from seed (unexpected)"}
        continue
    first_absent = None
    for edge in chain:
        if not hop_present_in_producer(edge):
            first_absent = edge
            break
    results[member] = {
        "direction": direction,
        "path_length": len(chain),
        "full_path": [f"{e.source} --{e.edge_type}--> {e.target}" for e in chain],
        "first_absent_hop": (f"{first_absent.source} --{first_absent.edge_type}--> {first_absent.target}"
                            if first_absent else "ALL HOPS PRESENT (unexpected -- would mean reachable)"),
    }
    if first_absent:
        key = f"{first_absent.source} --{first_absent.edge_type}--> {first_absent.target}"
        first_hops[key] = first_hops.get(key, 0) + 1

print("=" * 70)
print("FIRST-ABSENT-HOP FREQUENCY (shared-hop test):")
for hop, count in sorted(first_hops.items(), key=lambda kv: -kv[1]):
    print(f"  {count}x  {hop}")

out_path = os.path.join(SP, "CHAIN_TRACE_result.json")
json.dump({"seed": SEED, "n_traced": len(gold_present_unreachable),
           "first_hop_frequency": first_hops, "per_member": results},
          open(out_path, "w"), indent=2)
print("WROTE", out_path)
