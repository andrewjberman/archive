#!/usr/bin/env python3
"""NFRA_EDGES P1 -- EDGE REIFICATION in the MOTIF ladder (lift FLOWS_TO/RENDERS into C1 *Edge nodes).

The SEMCTL C0->C3 ladder tracks NODES; the frontend MOTIF pipeline FLATTENS the motif-defining
FLOWS_TO/RENDERS edges into rule-TEXT (motif_c2c3_materialize.json = CONTAINS-only, sink-node C1
constituents) -> a C3 materializes as a node-SKELETON, not the SUBGRAPH it is. The algebra
(cse_schema Relationship+EdgeKind) + the reference comp_ladder (DeniedEdge/AllowedEdge, :125/136/144)
ALREADY reify edges co-equally; P1 brings the frontend MOTIF pipeline to the same bar. NO new store,
NO new fidelity gate -- reify into the EXISTING comp_ladder.Node model (edges are duals of nodes).

Hybrid (PRD Q1): P1 = the MECHANISM + the proof on firm-conditional-display. The eager intra-system
sweep is P3. Lazy (reify-on-decompress) is the default elsewhere.

TWO LOAD-BEARING ACs (CTO arch-gates hardest, CVO certs):
  AC4 COLLISION-SAFE IDS: every reified *Edge node_id is UNIQUE-BY-CONSTRUCTION = stable-hash(src, sink,
     edge_type, condition), NEVER a reused label -- inherits the C3 fix (f875bc854). A self-test GATES
     the phase: two DISTINCT edges sharing a label yield DISTINCT node_ids (else the store-side MERGE
     silently collapses them -- the exact corruption f875bc854 closed).
  AC5 FRESHNESS: every materialized *Edge entity conforms to the graph_nodes CloudNode schema
     (node_id/node_type/layer/props) + carries snapshot_ts (the batch_ts producer-stamp), so the
     incremental-kuzu-refresh + reconcile-oracle drift-safety (keys nodes on {node_id: snapshot_ts})
     COVERS it -- else born drift-blind.

Usage:
  python NFRA_EDGES_P1_edge_reification.py --self-test   # MECHANISM proof (synthetic, no live graph): AC4/AC1/AC5
  python NFRA_EDGES_P1_edge_reification.py                # PROVE on firm-conditional-display (live graph; fail-loud)

Author: 0.4.0_DS_ClientPlatform~B (SEMCTL lane, NFRA_EDGES P1 owner). TO NFRA_EDGES.P1.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(WS, "org", "modules", "graph"))

import NFRA_MOTIF_P1_c2_catalog as P1M  # noqa: E402 -- the certed C2 catalog + detectors + comp_kuzu
from comp_ladder import Node, decompress, fidelity_check  # noqa: E402 -- the REAL Node model + fidelity gate

# A deterministic snapshot_ts for the self-test (real materialize stamps the batch_ts at store time).
SELFTEST_SNAPSHOT_TS = 1751990400  # fixed sentinel -> reproducible self-test (no Date.now nondeterminism)

# The governed EdgeKind vocabulary (cse_schema _EDGEKIND_VALUES) -- normalize the live props "kind" onto it.
_EDGEKIND_NORMALIZE = {"recompute/guarded": "recompute_guarded", "recompute_guarded": "recompute_guarded",
                       "passthrough": "passthrough", "rename": "rename", "": "passthrough"}
_EDGE_NTYPE = {"FLOWS_TO": "FlowsToEdge", "RENDERS": "RendersEdge", "PROP_PASSES": "PropPassesEdge"}


# ---------------------------------------------------------------------------
# AC4 -- collision-safe, unique-by-construction *Edge node_id (inherits f875bc854).
# ---------------------------------------------------------------------------
def edge_node_id(src: str, sink: str, edge_type: str, condition: str) -> str:
    """UNIQUE-BY-CONSTRUCTION *Edge node_id: a stable hash of the DEFINING TUPLE (src, sink, edge_type,
    condition), NEVER a reused label. Two edges can share a type/label but never a node_id -> no silent
    store-side MERGE collapse (the same discipline as system_node_id, f875bc854). Deterministic + stable:
    same tuple -> same id across runs (so the full-overwrite derive does not churn/orphan)."""
    key = "|".join([src, sink, edge_type, condition or ""])
    disc = hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]
    return "edge:" + edge_type.lower() + ":" + disc


# ---------------------------------------------------------------------------
# AC1 -- reify one motif-defining edge into a C1 *Edge Node (children bottom out in C0).
# ---------------------------------------------------------------------------
def reify_edge(src: str, sink: str, edge_type: str, condition: str, edge_kind: str) -> Node:
    """Reify a motif-defining edge into a first-class C1 *Edge Node (comp_ladder.Node). children =
    {src C0, sink C0, a C0 flow-fact carrying EdgeKind + the guard condition}. Decompresses to C0 +
    passes fidelity_check IDENTICALLY to a node (a LATENT edge-node -- no children -- FAILS the gate)."""
    ek = _EDGEKIND_NORMALIZE.get(edge_kind, edge_kind or "passthrough")
    src_c0 = P1M.c0_fact(src, "EdgeSource", "flow source")
    sink_c0 = P1M.c0_fact(sink, "EdgeSink", "flow sink")
    # the C0 FLOW-FACT: the lexical evidence of the RELATIONSHIP itself (its source line + kind + condition)
    fsrc, floc, _ = P1M.parse_locus(src)
    flow_c0 = Node(
        "flowfact:" + edge_node_id(src, sink, edge_type, condition)[len("edge:"):], "C0", "FlowFact",
        "%s -%s-> %s" % (src.split(":", 1)[-1][:28], edge_type, sink.split(":", 1)[-1][:28]),
        provenance={"source": fsrc, "locus": floc,
                    "evidence": "%s -%s(kind=%s)-> %s :: condition=%s" % (src, edge_type, ek, sink, condition or "-")})
    return Node(
        edge_node_id(src, sink, edge_type, condition), "C1", _EDGE_NTYPE.get(edge_type, edge_type.title().replace("_", "") + "Edge"),
        "%s -%s-> %s" % (src.split(":", 1)[-1], edge_type, sink.split(":", 1)[-1]),
        rule="reify %s edge (EdgeKind=%s, condition=%s)" % (edge_type, ek, condition or "-"),
        children=[src_c0, sink_c0, flow_c0])


# ---------------------------------------------------------------------------
# AC5 -- the CloudNode materialization view (freshness-contract conforming).
# ---------------------------------------------------------------------------
def to_cloud_node(edge_node: Node, snapshot_ts: int, src: str, sink: str, edge_type: str,
                  condition: str, edge_kind: str) -> dict:
    """The graph_nodes CloudNode record for a reified *Edge node -- conforms to the 8-field derive
    schema (node_id/node_type/props) + carries snapshot_ts (the batch_ts producer-stamp). The
    incremental-kuzu-refresh keys nodes on {node_id: snapshot_ts} -> this reified edge is COVERED
    (AC5, not drift-blind). layer=semctl (the SEMCTL analysis layer, like C2Motif/C3System)."""
    ek = _EDGEKIND_NORMALIZE.get(edge_kind, edge_kind or "passthrough")
    return {
        "node_id": edge_node.nid,           # unique-by-construction (AC4) -> the incremental-refresh key
        "node_type": edge_node.ntype,       # FlowsToEdge / RendersEdge
        "layer": "semctl",
        "snapshot_ts": snapshot_ts,         # AC5: the batch_ts stamp -> change-detection covers this entity
        "props": {"src": src, "sink": sink, "edge_type": edge_type, "edge_kind": ek, "condition": condition or ""},
    }


# ---------------------------------------------------------------------------
# Live: reify a motif's defining edges from the detector's expansion query.
# ---------------------------------------------------------------------------
def reify_motif_edges(spec: dict, snapshot_ts: int) -> tuple:
    """Run the detector's expansion_query live + reify each FLOWS_TO/RENDERS edge into a C1 *Edge Node.
    Returns (edge_nodes, cloud_records). Fail-loud on graph error (P1M.comp_kuzu raises GraphUnavailable).
    Only positive-edge motifs (D1/D2/D3 -- an expansion_query) have defining edges to reify."""
    if not spec.get("expansion_query"):
        return [], []
    ex_rows, _ = P1M.comp_kuzu(spec["expansion_query"])
    edge_type = "FLOWS_TO" if "FLOWS_TO" in spec["expansion_query"] else (
        "RENDERS" if "RENDERS" in spec["expansion_query"] else "PROP_PASSES")
    edge_nodes, cloud_records, seen = [], [], set()
    for e in ex_rows:
        src, sink = e.get("src"), e.get("dst")
        if not (src and sink):
            continue
        cond, ek = "", ""
        try:
            p = json.loads(e.get("props") or "{}")
            cond = p.get("condition") or ""
            ek = p.get("kind") or ""
        except Exception:  # noqa: BLE001
            cond = (e.get("props") or "")[:80]
        en = reify_edge(src, sink, edge_type, cond, ek)
        if en.nid in seen:                  # dedup identical (src,sink,type,condition) edges by their AC4 id
            continue
        seen.add(en.nid)
        edge_nodes.append(en)
        cloud_records.append(to_cloud_node(en, snapshot_ts, src, sink, edge_type, cond, ek))
    return edge_nodes, cloud_records


def build_motif_with_edges(spec: dict, snapshot_ts: int) -> tuple:
    """Compose a C2 motif with BOTH axes: the existing sink-NODE C1 constituents (node axis) AND the
    reified *Edge C1 constituents (edge axis). Returns (motif, edge_nodes, cloud_records, recurrence)."""
    node_motif, recurrence, _ = P1M.build_motif(spec)
    edge_nodes, cloud_records = reify_motif_edges(spec, snapshot_ts)
    node_motif.children = list(node_motif.children) + edge_nodes   # the motif now decompresses to node + edge
    return node_motif, edge_nodes, cloud_records, recurrence


# ---------------------------------------------------------------------------
# PROVE on firm-conditional-display (live) -- the C3 system decompresses to node + edge constituents.
# ---------------------------------------------------------------------------
_FIRM_DETECTORS = ("D1", "D2", "D3")   # silent-display-fork + cross-firm-asymmetry + hardcoded-firm-literal


def prove_firm_conditional_display() -> int:
    print("=" * 84)
    print("NFRA_EDGES P1 -- PROVE edge-reification on firm-conditional-display (live graph)")
    print("=" * 84)
    snapshot_ts = SELFTEST_SNAPSHOT_TS
    members, all_edges, all_records = [], [], []
    try:
        for spec in P1M.CATALOG:
            if spec["id"] not in _FIRM_DETECTORS:
                continue
            motif, edge_nodes, records, _ = build_motif_with_edges(spec, snapshot_ts)
            members.append(motif)
            all_edges.extend(edge_nodes)
            all_records.extend(records)
    except P1M.GraphUnavailable as ex:
        print("  UNVERIFIABLE (graph): %s" % ex)
        print("  The MECHANISM is proven by --self-test (synthetic, no graph). Re-run this live proof when the graph is reachable.")
        return 2
    system = Node("system:firm-conditional-display", "C3", "EmergentSystem", "firm-conditional-display",
                  rule="C3 = {silent-display-fork, cross-firm-asymmetry, hardcoded-firm-literal} + reified edges",
                  children=members)
    node_c0 = [n for _, n in decompress(system) if n.layer == "C0" and n.ntype not in ("FlowFact",)]
    edge_nodes = [n for _, n in decompress(system) if n.layer == "C1" and n.ntype.endswith("Edge")]
    flow_facts = [n for _, n in decompress(system) if n.layer == "C0" and n.ntype == "FlowFact"]
    ok, failures = fidelity_check(system)
    print("\n  firm-conditional-display decompresses to:")
    print("    NODE constituents (sink C1 -> C0 facts): %d C0 node-facts" % len(node_c0))
    print("    EDGE constituents (reified *Edge C1):     %d edge-nodes -> %d C0 flow-facts" % (len(edge_nodes), len(flow_facts)))
    print("    fidelity_check(system): %s" % ("PASS" if ok else "FAIL"))
    for f in failures[:5]:
        print("       ! " + f)
    print("\n  sample reified edges (AC4 collision-safe ids):")
    for en in edge_nodes[:4]:
        print("    %s   [%s]" % (en.nid, en.label[:60]))
    print("\n  AC5 sample CloudNode record (snapshot_ts + CloudNode-conform):")
    if all_records:
        print("    " + json.dumps({k: all_records[0][k] for k in ("node_id", "node_type", "layer", "snapshot_ts")}))
    both = len(edge_nodes) > 0 and len(node_c0) > 0 and ok
    print("\n  AC1: decompresses to BOTH node AND edge constituents, fidelity green: %s" % ("PASS" if both else "FAIL"))
    return 0 if both else 1


# ---------------------------------------------------------------------------
# Self-test -- the MECHANISM (synthetic, no live graph): AC4 / AC1 / AC5 + node+edge decomposition.
# ---------------------------------------------------------------------------
def self_test() -> int:
    print("=== NFRA_EDGES_P1 self-test (edge-reification mechanism; no live graph) ===")
    ok = []

    def chk(name, cond):
        ok.append(cond)
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    # 1. AC1: a reified edge decompresses to its C0 flow-fact + src + sink; passes fidelity IDENTICALLY to a node.
    e = reify_edge("out:portal/a/A.tsx:1#x", "out:portal/a/B.tsx:2#y", "FLOWS_TO", "firm == true", "recompute/guarded")
    ok1, _ = fidelity_check(e)
    c0kinds = {n.ntype for _, n in decompress(e) if n.layer == "C0"}
    chk("1  AC1: reified *Edge decompresses to C0 (src+sink+FlowFact) + PASSES fidelity (dual of a node)",
        ok1 and {"EdgeSource", "EdgeSink", "FlowFact"} <= c0kinds)

    # 2. AC1 negative control: a LATENT edge-node (no children) FAILS fidelity, same as a latent node.
    latent = Node("edge:flows_to:deadbeef", "C1", "FlowsToEdge", "latent", children=[])
    ok2, fails2 = fidelity_check(latent)
    chk("2  AC1 negative control: a LATENT edge-node (no C0 path) FAILS fidelity (same gate as a node)",
        ok2 is False and len(fails2) > 0)

    # 3. AC4 (GATES THE PHASE): two DISTINCT edges sharing a label/type yield DISTINCT node_ids.
    id_a = edge_node_id("out:X#a", "out:Y#b", "FLOWS_TO", "firm==true")
    id_b = edge_node_id("out:P#c", "out:Q#d", "FLOWS_TO", "firm==false")   # different tuple, same edge_type
    chk("3  AC4: two DISTINCT FLOWS_TO edges -> DISTINCT node_ids (no reused-label collapse)", id_a != id_b)

    # 4. AC4 STABILITY: the same defining tuple -> the SAME node_id across runs (full-overwrite derive no churn).
    chk("4  AC4: same (src,sink,type,condition) -> STABLE identical node_id across runs",
        edge_node_id("out:X#a", "out:Y#b", "FLOWS_TO", "firm==true") == id_a)

    # 5. AC4: the id is unique-by-CONSTRUCTION, not a reused label -- a differing CONDITION alone -> different id.
    chk("5  AC4: condition is part of the identity (same src/sink/type, different condition -> different id)",
        edge_node_id("out:X#a", "out:Y#b", "FLOWS_TO", "firm==true") != edge_node_id("out:X#a", "out:Y#b", "FLOWS_TO", "firm==false"))

    # 6. AC5: the CloudNode record conforms (node_id/node_type/layer/props) + carries snapshot_ts (the refresh key).
    rec = to_cloud_node(e, SELFTEST_SNAPSHOT_TS, "out:portal/a/A.tsx:1#x", "out:portal/a/B.tsx:2#y",
                        "FLOWS_TO", "firm == true", "recompute/guarded")
    chk("6  AC5: CloudNode record carries snapshot_ts + node_id/node_type/layer/props (incremental-refresh covers it)",
        rec.get("snapshot_ts") == SELFTEST_SNAPSHOT_TS and {"node_id", "node_type", "layer", "props"} <= set(rec)
        and rec["node_id"] == e.nid)

    # 7. NODE+EDGE decomposition: a C2 motif carrying BOTH a sink-node C1 AND a reified *Edge C1 decompresses to both.
    sink_c0 = P1M.c0_fact("out:portal/a/B.tsx:2#y", "DisplaySink", "sink")
    node_c1 = Node("c1:D1:out:portal/a/B.tsx:2#y", "C1", "SilentDisplayForkInteraction", "fork", rule="D1", children=[sink_c0])
    motif = Node("motif:silent-display-fork", "C2", "SilentDisplayFork", "silent-display-fork", rule="ABSORB D1",
                 children=[node_c1, e])   # BOTH axes: a node C1 + a reified *Edge C1
    okm, _ = fidelity_check(motif)
    has_node = any(n.ntype == "SilentDisplayForkInteraction" for _, n in decompress(motif))
    has_edge = any(n.ntype == "FlowsToEdge" for _, n in decompress(motif))
    chk("7  a C2 motif decompresses to BOTH node AND edge constituents (fidelity green)", okm and has_node and has_edge)

    n = sum(1 for r in ok if r)
    print("--- self-test: %d/%d passed ---" % (n, len(ok)))
    return 0 if n == len(ok) else 1


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass
    if "--self-test" in sys.argv[1:]:
        return self_test()
    return prove_firm_conditional_display()


if __name__ == "__main__":
    sys.exit(main())
