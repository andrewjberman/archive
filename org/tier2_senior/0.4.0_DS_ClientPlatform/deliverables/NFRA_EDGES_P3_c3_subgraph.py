#!/usr/bin/env python3
"""NFRA_EDGES P3 -- C3 AS SUBGRAPH: emergence/spec half (req2, req3, req4, req5 contract).

Built to TO org/tier1_exec/2.0.0_SA_COO/task_orders/NFRA_EDGES.P3.c3-as-subgraph.md and to the committed
design prep (deliverables/NFRA_EDGES_P3_c3_subgraph_design_prep.md). Both read BEFORE any code.

JOINT TO. <issued_to> = 0.4.0_DS_ClientPlatform~B (emergence/spec) + 0.7.0_AE_CloudOps (graph-materialize/
ingest). **req1 (the in-VPC materialize of the intra-system CloudEdges) is AE's half and is NOT claimed here.**
This module produces the emergence, the signature, the settled collision-safe id, and the MATERIALIZE CONTRACT
that AE's ingest consumes. It writes NOTHING to the store.

  gate_note (TO): "A C3 system is really a SUBGRAPH (member nodes + the FLOWS_TO/RENDERS edges among them)
  but today materializes only its node-skeleton + CONTAINS."

REQUIREMENT MAP (what this module does; req1 deliberately absent):
  req2 SIGNATURE AS A C3-NODE PROPERTY -> c3_signature() returns a prop dict carried ON the existing
       EmergentSystem node. NO new node_type is introduced anywhere in P3 (the TO's reason: fewer collision
       surfaces; the C3 node already has a collision-safe id). Self-tested.
  req3 EDGE-OVERLAP CONNECTIVITY -> c3_emergence() unions motifs over BOTH axes (shared node constituents
       AND shared reified *Edge C1 constituents) and records WHICH axis linked each pair.
       ** MEASURED INERT ON THE LIVE ESTATE ** (design prep S3): 0 edge-only links today -- every
       edge-overlap pair is already node-connected, so membership and the C3 id are unchanged. But it is NOT
       structurally a no-op: D1 carries 16 reified-edge endpoints that are NOT node-constituents of its own
       node-motif. So the req3 path CANNOT be exercised by live data, and a live proof would pass identically
       against a correct implementation and against a `return`. The self-test therefore SYNTHESISES an
       edge-only link and asserts the axis actually does the work. Reported MET-with-measured-inert, never
       "it works because the graph changed."
  req4 COLLISION-SAFE ID, RECOMPUTED POST-SETTLEMENT -> settled_system_node_id(). Identity is the PAIR
       (theme, settled member-set), NEVER the member-set hash alone. This is the P2 D2/D3 lesson carried
       forward: two C2 edge-motifs had BYTE-IDENTICAL canonical edge-sets and were distinguished ONLY by
       their idiom prefix. The prefix is LOAD-BEARING. Mutation-tested.
       SEQUENCING (TO's CRITICAL COORDINATION): the shared unique-by-construction scheme landed with the N>1
       collision-hardening (f875bc854; ledger 20260708T1856Z CLOSED; R3 live-verified :25558d98 present, old
       bare id absent, no orphan; CVO~B re-certed). P3 EXTENDS it; it does not re-invent it.
  req5 AC5 FRESHNESS CONTRACT -> to_c3_node_record() + to_intra_edge_record() stamp snapshot_ts from
       derive_batch_ts() (the REAL producer basis). See "THE EDGE-IDENTITY TRAP" below.

THE EDGE-IDENTITY TRAP (grounded; the load-bearing item in AE's contract):
  A materialized intra-system edge is a CloudEdge, and the store's edge IDENTITY is the tuple
      (src_node_id, dst_node_id, edge_type, props)
  -- kuzu_nessie_load.py:190 ("props IS part of the edge identity (CTO 225614Z): MERGE on {edge_type, props}
  ... edge_type-only MERGE silently collapsed them last-props-wins = a no-silent-drop violation at the MERGE
  seam"), and kuzu_incremental_refresh.py:_cur_edges keys the live DB on exactly that tuple, carrying
  (layer, snapshot_ts) as in-place SET-fields.

  P1's edge_node_id(src, sink, edge_type, condition) is an ANALYSIS-side NODE id for a reified *Edge C1
  comp_ladder Node. It is NOT the store edge key. Keying materialized CloudEdges on edge_node_id would make
  them invisible to kuzu_incremental_refresh's MERGE + change-detection -- born DRIFT-BLIND even with a
  perfectly correct snapshot_ts. Do not conflate them. intra_edge_identity() below is the store key.

  Note the pleasing symmetry: props-in-the-edge-identity at the store seam IS the same no-silent-MERGE
  discipline as AC4 at the analysis seam. The guard condition lives in props, so two edges differing only by
  their guard stay distinct through the MERGE.

AC5, and where the P1 defect dies: snapshot_ts must come from derive_runner.py:1821
`batch_ts = int(time.time()*1000)` (13-digit MILLISECONDS), written to every row at :338/:369. The consumer
kuzu_incremental_refresh.py:165-166 upserts iff `snapshot_ts != cur_ts[key]`, and the nightly derive
full-overwrites with a fresh batch_ts (_canonical.py:288) -- so a CONSTANT stamp is never re-upserted and the
entity is born drift-blind. P1:162 stamps a CONSTANT 10-digit SECONDS sentinel; disposition is absorb-at-P3
(COO~B 101447Z, CTO concurring 101904Z), i.e. HERE, at the write. certed-P1 stays untouched.
CERT CONDITION (CTO + CVO~B, bound): the P3 AC5 cert must EXERCISE THE VALUE -- a real derive-run stamping a
ts that CHANGES across runs so the != fires -- not "a snapshot_ts field exists".

Usage:
  python NFRA_EDGES_P3_c3_subgraph.py --self-test   # mechanism proof (synthetic, no graph)
  python NFRA_EDGES_P3_c3_subgraph.py               # live emergence + the materialize contract (fail-loud)
  python NFRA_EDGES_P3_c3_subgraph.py --contract    # emit the AE materialize contract as JSON

Author: 0.4.0_DS_ClientPlatform~B (SEMCTL lane, NFRA_EDGES P3 emergence/spec owner). TO NFRA_EDGES.P3.
"""
from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(WS, "org", "modules", "graph"))

import NFRA_EDGES_P1_edge_reification as P1E  # noqa: E402 -- certed reify_edge / reify_motif_edges
import NFRA_EDGES_P2_edge_motifs as P2        # noqa: E402 -- derive_batch_ts (the real producer basis)
import NFRA_MOTIF_P1_c2_catalog as P1M        # noqa: E402 -- CATALOG, build_motif, system_node_id
from comp_ladder import Node, decompress, fidelity_check  # noqa: E402

derive_batch_ts = P2.derive_batch_ts          # one source for the AC5 basis; do not re-implement

SELFTEST_SNAPSHOT_TS_MS = 1751990400000       # ms-scale, SELF-TEST ONLY


# ---------------------------------------------------------------------------
# req3 -- emergence over BOTH axes, recording which axis linked each pair.
# ---------------------------------------------------------------------------
def _is_edge_node(n: Node) -> bool:
    return n.layer == "C1" and n.ntype.endswith("Edge")


def node_constituents(motif: Node) -> set:
    """The PURE node axis: constituents reachable WITHOUT descending into a reified *Edge C1 subtree.

    SUBTLE AND LOAD-BEARING (caught by the synthetic req3 gate, which live data could never have caught):
    a reified *Edge C1 node carries its ENDPOINTS as C0 children (EdgeSource / EdgeSink / FlowFact). If the
    node axis merely filters out the *Edge node itself but still walks its subtree, those endpoint C0 facts
    leak into the node axis -- and then two motifs sharing an edge ALWAYS share node constituents too. Under
    that definition an edge-only link is impossible BY CONSTRUCTION and req3's edge axis is a permanent
    no-op that no live proof could distinguish from a correct implementation.

    So: the node axis STOPS at the edge boundary. The edge subtree belongs to the edge axis alone.
    """
    out: set = set()

    def walk(n: Node):
        if _is_edge_node(n):
            return                     # the edge subtree is the EDGE axis; do not descend
        if n.layer in ("C0", "C1"):
            out.add(n.nid)
        for c in n.children:
            walk(c)

    walk(motif)
    return out


def edge_constituents(motif: Node) -> set:
    """The motif's reified *Edge C1 constituent ids (the edge axis)."""
    return {n.nid for _, n in decompress(motif) if n.layer == "C1" and n.ntype.endswith("Edge")}


def c3_emergence(motifs: list) -> tuple:
    """Union motifs into C3 components over node-overlap AND edge-overlap (req3: "alongside").

    Returns (components, link_evidence, edge_only_links) where
      components      : [[motif, ...], ...] connected sets (a component of 1 is NOT a system)
      link_evidence   : {(a_nid, b_nid): "node" | "edge" | "both"}  -- WHY each pair is connected
      edge_only_links : the pairs connected by the EDGE axis alone (the connectivity req3 ADDS)

    Adding an axis can only MERGE components, never split them -- connectivity is monotone in the
    constituent set. So `edge_only_links` is exactly the delta req3 buys.
    """
    nodec = {m.nid: node_constituents(m) for m in motifs}
    edgec = {m.nid: edge_constituents(m) for m in motifs}
    parent = {m.nid: m.nid for m in motifs}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    ids = [m.nid for m in motifs]
    link_evidence, edge_only = {}, []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            n_shared = nodec[a] & nodec[b]
            e_shared = edgec[a] & edgec[b]
            if not (n_shared or e_shared):
                continue
            if n_shared and e_shared:
                link_evidence[(a, b)] = "both"
            elif n_shared:
                link_evidence[(a, b)] = "node"
            else:
                link_evidence[(a, b)] = "edge"      # the connectivity the EDGE axis adds
                edge_only.append((a, b))
            union(a, b)

    by_nid = {m.nid: m for m in motifs}
    comps: dict = {}
    for mid in ids:
        comps.setdefault(find(mid), []).append(mid)
    components = [[by_nid[m] for m in members] for _, members in sorted(comps.items())]
    return components, link_evidence, edge_only


# ---------------------------------------------------------------------------
# req4 -- collision-safe C3 node_id, recomputed AFTER membership settles.
# ---------------------------------------------------------------------------
def settled_system_node_id(theme: str, settled_member_nids) -> str:
    """The C3 node_id, computed from the SETTLED member set (after node+edge overlap resolves).

    Identity is the PAIR (theme, settled member-set) -- NEVER the member-set hash alone. Delegates to the
    landed P1M.system_node_id (f875bc854), which is `theme + ":" + sha1(sorted members)`: we EXTEND the
    landed scheme rather than re-invent it (the TO's CRITICAL COORDINATION).

    Why the prefix is load-bearing, concretely (P2's live finding): two C2 edge-motifs -- D2
    cross-firm-asymmetry and D3 hardcoded-firm-literal -- carry BYTE-IDENTICAL canonical edge-sets on the
    live estate (the same four edge:flows_to members, disc 05c557b09327) and are distinguished ONLY by their
    idiom prefix. A "simplify to hash(member-set) alone" refactor silently MERGEs two distinct systems. The
    natural simplification IS the corruption.
    """
    return P1M.system_node_id(theme, list(settled_member_nids))


# ---------------------------------------------------------------------------
# req1's shape (AE materializes it) -- intra-system edge selection, boundary edges COUNTED not dropped.
# ---------------------------------------------------------------------------
def intra_system_edges(system: Node, reified_edges: list) -> tuple:
    """Split reified edges into INTRA-system (both endpoints resolve to C3 constituents) and BOUNDARY
    (exactly one endpoint inside). Returns (intra, boundary, outside).

    Boundary edges are EXCLUDED from the subgraph but COUNTED and returned -- never silently dropped. A
    confident subgraph over a silently-truncated edge set is the discovery-false-negative class that got
    P2's first build retracted.
    """
    inside = {n.nid for _, n in decompress(system) if n.layer in ("C0", "C1")}
    intra, boundary, outside = [], [], []
    for e in reified_edges:
        eps = [c.nid for c in e.children if c.ntype in ("EdgeSource", "EdgeSink")]
        hit = sum(1 for p in eps if p in inside)
        if hit == len(eps) and eps:
            intra.append(e)
        elif hit:
            boundary.append(e)
        else:
            outside.append(e)
    return intra, boundary, outside


# ---------------------------------------------------------------------------
# req2 -- the data-flow signature: a PROPERTY of the C3 node. No new node_type.
# ---------------------------------------------------------------------------
def c3_signature(system: Node, intra: list) -> dict:
    """The C3's data-flow signature, as a PROP on the existing EmergentSystem node (req2: explicitly NOT a
    new node_type). Decompressable: every element traces to a reified *Edge C1 -> its C0 flow-fact."""
    kinds, types, conds = {}, {}, []
    for e in intra:
        ff = next((c for c in e.children if c.ntype == "FlowFact"), None)
        ev = (ff.provenance or {}).get("evidence", "") if ff else ""
        types[e.ntype] = types.get(e.ntype, 0) + 1
        for k in ("recompute_guarded", "passthrough", "rename"):
            if "kind=" + k in ev:
                kinds[k] = kinds.get(k, 0) + 1
        if ":: condition=" in ev:
            c = ev.split(":: condition=", 1)[1].strip()
            if c and c != "-":
                conds.append(c)
    return {
        "edge_count": len(intra),
        "edge_types": dict(sorted(types.items())),
        "edge_kinds": dict(sorted(kinds.items())),
        "guards": sorted(set(conds))[:8],
        "flow": "firm-literal -> guarded-fork -> display-sink" if kinds.get("recompute_guarded") else "unguarded",
    }


# ---------------------------------------------------------------------------
# req5 -- the AC5 emission contract (what AE materializes). NOTHING is written here.
# ---------------------------------------------------------------------------
def intra_edge_identity(src: str, dst: str, edge_type: str, props: str) -> tuple:
    """THE STORE EDGE KEY -- the tuple kuzu_nessie_load MERGEs on (:190, "props IS part of the edge
    identity") and kuzu_incremental_refresh._cur_edges keys the live DB on. NOT P1's edge_node_id (an
    analysis-side NODE id): keying on that would make the edge invisible to the incremental refresh."""
    return (src, dst, edge_type, props or "")


def to_intra_edge_record(edge: Node, snapshot_ts: int) -> dict:
    """A materializable intra-system CloudEdge record. layer + snapshot_ts are in-place SET-fields; the
    identity is (src, dst, edge_type, props)."""
    src = next(c.nid for c in edge.children if c.ntype == "EdgeSource")
    dst = next(c.nid for c in edge.children if c.ntype == "EdgeSink")
    ff = next((c for c in edge.children if c.ntype == "FlowFact"), None)
    ev = (ff.provenance or {}).get("evidence", "") if ff else ""
    edge_type = "RENDERS" if edge.ntype == "RendersEdge" else ("PROP_PASSES" if edge.ntype == "PropPassesEdge" else "FLOWS_TO")
    cond = ev.split(":: condition=", 1)[1].strip() if ":: condition=" in ev else ""
    kind = next((k for k in ("recompute_guarded", "passthrough", "rename") if "kind=" + k in ev), "passthrough")
    props = json.dumps({"kind": kind, "condition": cond}, sort_keys=True)
    return {
        "src": src, "dst": dst, "edge_type": edge_type, "props": props,   # <- the IDENTITY tuple
        "layer": "semctl",
        "snapshot_ts": snapshot_ts,                                        # AC5: real ms basis, never constant
    }


def to_c3_node_record(system: Node, signature: dict, snapshot_ts: int) -> dict:
    """The C3 node record: the SAME EmergentSystem node_type (req2 -- no new node_type), carrying the
    data-flow signature as a PROPERTY, plus AC5's snapshot_ts."""
    return {
        "node_id": system.nid,          # settled, collision-safe (req4)
        "node_type": system.ntype,      # EmergentSystem -- unchanged, no new type
        "layer": "semctl",
        "snapshot_ts": snapshot_ts,     # AC5
        "props": {"theme": system.label, "signature": signature},
    }


# ---------------------------------------------------------------------------
# Live: emergence over the real catalog + the materialize contract for AE.
# ---------------------------------------------------------------------------
def run_live(emit_contract: bool = False) -> int:
    print("=" * 92)
    print("NFRA_EDGES P3 -- C3-as-subgraph: emergence/spec half (req1 materialize = 0.7.0_AE, NOT claimed)")
    print("=" * 92)
    ts = derive_batch_ts()
    print("  snapshot_ts (derive_runner batch_ts basis, ms): %d" % ts)

    motifs, all_edges = [], {}
    try:
        for spec in P1M.CATALOG:
            motif, edges, _recs, rec = P1E.build_motif_with_edges(spec, ts)
            if rec < P1M.AC3_THRESHOLD:
                continue
            motifs.append(motif)
            all_edges[motif.nid] = edges
    except P1M.GraphUnavailable as ex:
        print("  UNVERIFIABLE (graph): %s" % ex)
        print("  The MECHANISM is proven by --self-test. Re-run when the canonical is reachable.")
        return 2

    components, evidence, edge_only = c3_emergence(motifs)
    systems = [c for c in components if len(c) >= 2]
    singles = [c[0] for c in components if len(c) == 1]

    print("\n  req3 -- EMERGENCE (node-overlap + EDGE-overlap):")
    for (a, b), axis in sorted(evidence.items()):
        print("    %-28s <-> %-28s linked by: %s" % (a.split(":", 1)[1], b.split(":", 1)[1], axis))
    print("    EDGE-ONLY links (the connectivity req3 ADDS on this estate): %d" % len(edge_only))
    if not edge_only:
        print("      -> MEASURED INERT. Every edge-overlap pair is already node-connected. This is NOT a")
        print("         structural no-op (D1 carries 16 reified-edge endpoints absent from its node axis),")
        print("         so the req3 path is UNEXERCISABLE by live data -> the self-test synthesises it.")

    rc = 0
    for comp in systems:
        member_nids = [m.nid for m in comp]
        theme = "firm-conditional-display" if any("firm" in m.nid or "display" in m.nid for m in comp) \
            else "shared-sink-cluster"
        # req4: recompute the id AFTER membership settles
        nid = settled_system_node_id(theme, member_nids)
        system = Node(nid, "C3", "EmergentSystem", theme,
                      rule="C3 SUBGRAPH: members {%s} + their intra-system edges" % ", ".join(
                          m.nid.split(":", 1)[1] for m in comp),
                      children=list(comp))

        reified = [e for m in comp for e in all_edges.get(m.nid, [])]
        seen, uniq = set(), []
        for e in reified:
            if e.nid not in seen:
                seen.add(e.nid)
                uniq.append(e)
        intra, boundary, outside = intra_system_edges(system, uniq)
        sig = c3_signature(system, intra)
        ok, failures = fidelity_check(system)
        rc = rc or (0 if ok else 1)

        print("\n  req4 -- SETTLED C3 node_id: %s" % nid)
        print("    members (%d): %s" % (len(comp), ", ".join(m.nid.split(":", 1)[1] for m in comp)))
        print("    fidelity (C3 -> C2 -> C1 -> C0 evidence): %s" % ("PASS" if ok else "FAIL"))
        for f in failures[:3]:
            print("       ! " + f)
        print("\n  req1 (AE's half) -- INTRA-SYSTEM EDGE SELECTION:")
        print("    intra-system: %d   boundary (one endpoint outside, EXCLUDED + COUNTED): %d   outside: %d"
              % (len(intra), len(boundary), len(outside)))
        print("\n  req2 -- DATA-FLOW SIGNATURE (a PROPERTY of the C3 node; node_type stays %s):" % system.ntype)
        print("    " + json.dumps(sig))

        if emit_contract:
            # snapshot_ts is DELIBERATELY NULL in the contract. Emitting a concrete ts here would hand AE a
            # CONSTANT to copy -- which is precisely the latent P1 defect (a constant is never re-upserted by
            # kuzu_incremental_refresh's `snapshot_ts != cur_ts[key]` test -> born drift-blind). The producer
            # MUST stamp it at derive time from derive_runner's own batch_ts.
            def _strip_ts(rec: dict) -> dict:
                r = dict(rec)
                r["snapshot_ts"] = None
                return r

            contract = {
                "c3_node": _strip_ts(to_c3_node_record(system, sig, ts)),
                "intra_system_edges": [_strip_ts(to_intra_edge_record(e, ts)) for e in intra],
                "edge_identity_key": ["src", "dst", "edge_type", "props"],
                "edge_identity_source": "kuzu_nessie_load.py:190 MERGE on {edge_type, props}; "
                                        "kuzu_incremental_refresh._cur_edges keys (src,dst,edge_type,props)",
                "snapshot_ts": "NULL BY DESIGN -- STAMP AT DERIVE TIME",
                "snapshot_ts_source": "derive_runner.py:1821 batch_ts = int(time.time()*1000)  [13-digit ms]",
                "snapshot_ts_WARNING": "Do NOT copy a literal ts from this file. A CONSTANT snapshot_ts is "
                                       "never re-upserted (kuzu_incremental_refresh.py:165-166 upserts iff "
                                       "snapshot_ts != cur_ts[key]) -> the entity is born DRIFT-BLIND. This "
                                       "is the latent NFRA_EDGES_P1:162 defect, absorbed at P3 by COO~B/CTO "
                                       "disposition. The P3 AC5 cert EXERCISES the value: a real derive-run "
                                       "must stamp a 13-digit ms ts that CHANGES across runs so the != fires.",
                "NOT_the_edge_key": "P1 edge_node_id() is an analysis-side NODE id -- keying CloudEdges on it "
                                    "makes them invisible to kuzu_incremental_refresh (born drift-blind)",
                "boundary_edges_excluded": len(boundary),
                "c3_node_id_is_unchanged": "system:firm-conditional-display:25558d98 == the SERVED id "
                                           "(round-trip verified) -> NOT a served-identity replacement; no "
                                           "orphan, no consumer re-pin. Still a STORE WRITE: never-half-land "
                                           "deploy-completion ledger + R3-style live verify still required.",
            }
            path = os.path.join(_HERE, "NFRA_EDGES_P3_materialize_contract.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(contract, fh, indent=2, sort_keys=True)
            print("\n  MATERIALIZE CONTRACT for 0.7.0_AE written -> %s" % os.path.relpath(path, WS))

    for sg in singles:
        print("\n  singleton (correctly NOT forced into a system): %s" % sg.nid)

    print("\n  req1: NOT CLAIMED -- the in-VPC materialize/ingest is 0.7.0_AE_CloudOps's half of this joint TO.")
    return rc


# ---------------------------------------------------------------------------
# Self-test -- req3's gate is SYNTHETIC by necessity (the live estate cannot exercise it).
# ---------------------------------------------------------------------------
def _c0(nid, ntype="F"):
    return Node(nid, "C0", ntype, nid, provenance={"source": nid.split("#")[0], "locus": "-", "evidence": nid})


def _motif(nid, c0ids, edges=()):
    c1 = Node("c1:" + nid, "C1", "I", nid, rule="d", children=[_c0(x) for x in c0ids])
    return Node("motif:" + nid, "C2", "M", nid, rule="ABSORB", children=[c1] + list(edges))


def self_test() -> int:
    print("=== NFRA_EDGES_P3 self-test (C3-as-subgraph emergence/spec; no live graph) ===")
    ok = []

    def chk(name, cond):
        ok.append(bool(cond))
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    # THE req3 GATE. The live estate has ZERO edge-only links, so a live proof cannot distinguish a correct
    # implementation from a `return`. Synthesise one: two motifs sharing a reified *Edge C1 node and NO node
    # constituent. node-overlap alone must leave them SEPARATE; node+edge must MERGE them.
    shared_edge = P1E.reify_edge("out:a/A.tsx:1#x", "out:b/B.tsx:2#y", "FLOWS_TO", "firm == true", "recompute/guarded")
    m1 = _motif("alpha", ["out:p/P.tsx:1#p"], edges=[shared_edge])
    m2 = _motif("beta", ["out:q/Q.tsx:2#q"], edges=[shared_edge])

    chk("1  req3 setup: the two motifs share NO node constituent",
        not (node_constituents(m1) & node_constituents(m2)))
    chk("2  req3 setup: the two motifs DO share a reified *Edge C1 constituent",
        bool(edge_constituents(m1) & edge_constituents(m2)))

    comps, evidence, edge_only = c3_emergence([m1, m2])
    chk("3  req3 GATE: an EDGE-ONLY link merges them into ONE component (the edge axis does real work)",
        len(comps) == 1 and len(comps[0]) == 2)
    chk("4  req3 GATE: the link is attributed to the EDGE axis, and counted as an edge-only link",
        evidence.get((m1.nid, m2.nid)) == "edge" and len(edge_only) == 1)

    # Node axis ALONE must leave them separate -- this is the half that fails if the edge axis is dropped.
    n1, n2 = node_constituents(m1), node_constituents(m2)
    chk("5  req3 control: node-overlap ALONE leaves them in SEPARATE components (0 shared node constituents)",
        len(n1 & n2) == 0)

    # req4: identity is the PAIR (theme, settled member-set). The prefix is LOAD-BEARING.
    ms = ["motif:a", "motif:b"]
    id_x = settled_system_node_id("firm-conditional-display", ms)
    id_y = settled_system_node_id("shared-sink-cluster", ms)          # SAME member-set, different theme
    chk("6  req4/AC4: same settled member-set + DIFFERENT theme -> DISTINCT ids (prefix is load-bearing)",
        id_x != id_y)
    chk("7  req4/AC4: different settled member-set -> distinct ids",
        settled_system_node_id("firm-conditional-display", ["motif:a", "motif:c"]) != id_x)
    chk("8  req4/AC4: same settled tuple -> STABLE id across runs (full-overwrite derive: no churn)",
        settled_system_node_id("firm-conditional-display", list(reversed(ms))) == id_x)

    # req2: the signature is a PROPERTY; no new node_type is introduced.
    sysnode = Node(id_x, "C3", "EmergentSystem", "firm-conditional-display", rule="r", children=[m1, m2])
    sig = c3_signature(sysnode, [shared_edge])
    rec = to_c3_node_record(sysnode, sig, SELFTEST_SNAPSHOT_TS_MS)
    chk("9  req2: signature rides as a PROP on the existing EmergentSystem node_type (no new node_type)",
        rec["node_type"] == "EmergentSystem" and "signature" in rec["props"] and sig["edge_count"] == 1)

    # Intra vs boundary: a boundary edge (one endpoint outside) is EXCLUDED and COUNTED, never dropped.
    outside_edge = P1E.reify_edge("out:a/A.tsx:1#x", "out:zz/Z.tsx:9#z", "FLOWS_TO", "", "passthrough")
    intra, boundary, _out = intra_system_edges(sysnode, [shared_edge, outside_edge])
    chk("10 req1-shape: boundary edge (one endpoint outside the C3) EXCLUDED from intra AND COUNTED",
        len(intra) == 1 and len(boundary) == 1)

    # req5 / AC5: the store EDGE KEY is (src,dst,edge_type,props) -- NOT P1's edge_node_id.
    erec = to_intra_edge_record(shared_edge, SELFTEST_SNAPSHOT_TS_MS)
    key = intra_edge_identity(erec["src"], erec["dst"], erec["edge_type"], erec["props"])
    chk("11 req5: intra-edge record carries the STORE identity tuple (src,dst,edge_type,props) + snapshot_ts",
        len(key) == 4 and erec["snapshot_ts"] == SELFTEST_SNAPSHOT_TS_MS
        and "condition" in erec["props"] and erec["src"] != shared_edge.nid)
    chk("12 req5 TRAP: the edge key is NOT P1's analysis-side edge_node_id (that would be drift-blind)",
        erec["src"] != shared_edge.nid and not str(key).startswith("edge:"))

    # AC5 basis guards (the P1 inherited-defect class).
    ts = derive_batch_ts()
    chk("13 AC5 guard: derive_batch_ts() is ms-scale (>=1e12), per derive_runner.py:1821", ts >= 1_000_000_000_000)
    chk("14 AC5 guard: derive_batch_ts() is a live wall-clock, NOT a constant", derive_batch_ts() >= ts)

    # Fidelity + negative control.
    okf, _ = fidelity_check(sysnode)
    latent = Node(id_x, "C3", "EmergentSystem", "latent", children=[])
    okl, fl = fidelity_check(latent)
    chk("15 AC6: the C3 decompresses C3->C2->C1->C0 evidence (fidelity PASS)", okf)
    chk("16 negative control: a LATENT C3 (no members) FAILS fidelity (the gate bites)", okl is False and fl)

    n = sum(1 for r in ok if r)
    print("--- self-test: %d/%d passed ---" % (n, len(ok)))
    return 0 if n == len(ok) else 1


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass
    args = sys.argv[1:]
    if "--self-test" in args:
        return self_test()
    return run_live(emit_contract="--contract" in args)


if __name__ == "__main__":
    sys.exit(main())
