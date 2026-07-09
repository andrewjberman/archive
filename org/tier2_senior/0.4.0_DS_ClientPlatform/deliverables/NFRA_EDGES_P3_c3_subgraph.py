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


_PROJECTED_PROP_KEYS = ("condition", "kind")


def _norm_kind(edge_kind: str) -> str:
    """Normalize a live props `kind` onto the governed EdgeKind vocabulary. Delegates to P1's map, which is
    the ONE source ({recompute/guarded -> recompute_guarded, passthrough, rename, "" -> passthrough}). An
    ad-hoc slash->underscore rewrite would silently mis-handle any future kind."""
    return P1E._EDGEKIND_NORMALIZE.get(edge_kind, edge_kind or "passthrough")


def project_edge_props(props_json: str) -> str:
    """Project a LIVE estate edge's props into the C3-subgraph CANONICAL form: {condition, kind}, with kind
    normalized onto the governed EdgeKind vocabulary. Deterministic (sorted keys) and IDEMPOTENT.

    WHY THIS EXISTS (0.7.0_AE caught it pre-build; the third consumer-catch, and it is a defect in the (a)
    check I had already had gated). A live estate FLOWS_TO edge and my contract edge are NOT comparable raw:
        LIVE     layer="aws"     props = {condition, dstField, kind:"recompute/guarded", rename, resolution,
                                          srcField, via}      -- 7 keys, kind with a SLASH
        CONTRACT layer="semctl"  props = {condition, kind:"recompute_guarded"}  -- 2 keys, kind with an
                                          UNDERSCORE (the governed EdgeKind value)
    Comparing them on (src,dst,edge_type,props) NEVER matches, so every live edge reads as
    missing_from_contract and the coverage-check FAILS LOUD spuriously on every derive. A check that cries
    wolf on every run is as useless as one that never fires -- the same proxy failure, mirrored.

    So BOTH sides are projected before comparison. kind normalization uses P1E._EDGEKIND_NORMALIZE (the one
    governed map: recompute/guarded -> recompute_guarded, passthrough, rename, "" -> passthrough) -- NOT an
    ad-hoc slash->underscore rewrite, which would silently mis-handle any future kind.
    """
    try:
        p = json.loads(props_json or "{}")
    except (json.JSONDecodeError, TypeError):
        p = {}
    if not isinstance(p, dict):
        p = {}
    return json.dumps({"condition": p.get("condition") or "",
                       "kind": _norm_kind(p.get("kind") or "")}, sort_keys=True)


def subgraph_coverage_check(contract_edges: list, live_edges: list) -> tuple:
    """SET-COMPLETENESS check (COO~B scope-ruling 111120Z, option (a)) -- run at DERIVE time by the ingest.

    THE HOLE THIS CLOSES: ingest_c2c3_motif_producer (derive_runner.py:1320-1360) replays a FROZEN spec list
    with NO live discovery. Its endpoint resolution makes DELETIONS loud (edges_unresolved > 0), but a NEWLY
    APPEARED qualifying estate edge is simply absent from the list and is SILENTLY never materialized. So a
    C3 subgraph can be perfectly per-entity fresh (every snapshot_ts != firing) and permanently INCOMPLETE.

    AC5's snapshot_ts is a per-ENTITY freshness contract; it is a PROXY for the property we actually want,
    which is set-COMPLETENESS. This check asserts the property directly.

    Returns (ok, missing_from_contract, absent_from_live):
      missing_from_contract -- live qualifying edges NOT in the frozen contract. THE SILENT HALF. ok is False
                               iff this is non-empty: the ingest must FAIL LOUD, never quietly under-materialize.
      absent_from_live      -- contract edges no longer live. Already surfaced as edges_unresolved; reported
                               here too so the ingest never has to infer it.

    Edges are compared on the STORE identity tuple (src, dst, edge_type, props) -- the same key
    kuzu_nessie_load MERGEs on. Comparing on anything else would make the check itself a proxy.
    """
    def key(e):
        # BOTH sides projected. project_edge_props is idempotent, so an already-canonical contract record is
        # unchanged while a RAW live estate row (7 props keys, slash-kind) is normalized into comparable form.
        return intra_edge_identity(e["src"], e["dst"], e["edge_type"], project_edge_props(e["props"]))

    contract_keys = {key(e) for e in contract_edges}
    live_keys = {key(e) for e in live_edges}
    missing_from_contract = sorted(live_keys - contract_keys)
    absent_from_live = sorted(contract_keys - live_keys)
    return (len(missing_from_contract) == 0), missing_from_contract, absent_from_live


def live_coverage_check(contract_path: str = None) -> tuple:
    """THE (a) CHECK, AS AE ACTUALLY RUNS IT. One entrypoint, one builder, zero re-implementation.

    WHERE THIS RUNS -- and this CORRECTS my own earlier spec (`run_at: derive time, before materialize`),
    which was unimplementable on this substrate. Grounded: derive_runner imports kuzu NOWHERE; its ingest
    operates over the in-memory `graph` dict; the Kuzu DB only exists AFTER kuzu_nessie_load reads Iceberg
    post-Nessie-commit. The D1-D7 detectors are Cypher over CloudNode/CloudEdge, so they CANNOT execute at
    derive time. The check therefore belongs in AE's existing POST-DERIVE R3-VERIFY leg (the "comp-kuzu
    round-trip" leg of the deploy ledger), against the freshly-loaded canonical.

    CONSEQUENCE, stated honestly: the check DETECTS rather than PREVENTS. That is correct here and not a
    weakening -- a failed R3 leg fails the deploy, the never-half-land ledger stays OPEN, and the deploy rolls
    back. Set-incompleteness is a data-coverage defect, not a corruption; detect-and-roll-back is the right
    instrument, and it is the instrument the ledger already provides.

    WHY THIS ANSWERS "the recompute must BE build_motif, not a drifting re-impl" (AE + COO~B): it literally is.
    This function runs the SAME live detector queries through the SAME P1M/P1E code the analysis-side emission
    used. AE imports nothing into the derive image and re-implements nothing. AE's R3 leg is one call:
        python NFRA_EDGES_P3_c3_subgraph.py --coverage-check     # rc=0 clean, rc=1 FAIL LOUD

    Satisfies CTO's "LIVE ALL THE WAY DOWN": there is no frozen branch -- the constituents come from the live
    detector recompute, and the edges from the live expansion queries. Fail-loud on GraphUnavailable, never a
    silent [] (which would read as "nothing missing" -- a vacuous pass).
    """
    path = contract_path or os.path.join(_HERE, "NFRA_EDGES_P3_materialize_contract.json")
    with open(path, "r", encoding="utf-8") as fh:
        contract = json.load(fh)

    ts = derive_batch_ts()
    motifs, all_edges = [], {}
    for spec in P1M.CATALOG:                       # LIVE detector recompute -- no frozen branch
        motif, edges, _recs, rec = P1E.build_motif_with_edges(spec, ts)
        if rec < P1M.AC3_THRESHOLD:
            continue
        motifs.append(motif)
        all_edges[motif.nid] = edges

    components, _evidence, _edge_only = c3_emergence(motifs)
    live_records: list = []
    for comp in components:
        if len(comp) < 2:
            continue
        theme = "firm-conditional-display" if any("firm" in m.nid or "display" in m.nid for m in comp) \
            else "shared-sink-cluster"
        system = Node(settled_system_node_id(theme, [m.nid for m in comp]), "C3", "EmergentSystem", theme,
                      rule="coverage-check", children=list(comp))
        reified = [e for m in comp for e in all_edges.get(m.nid, [])]
        seen, uniq = set(), []
        for e in reified:
            if e.nid not in seen:
                seen.add(e.nid)
                uniq.append(e)
        intra, _boundary, _outside = intra_system_edges(system, uniq)
        live_records.extend(to_intra_edge_record(e, ts) for e in intra)

    return subgraph_coverage_check(contract.get("intra_system_edges", []), live_records)


def run_coverage_check() -> int:
    """AE's R3-verify leg. rc=0 clean; rc=1 FAIL LOUD (missing_from_contract > 0); rc=2 UNVERIFIABLE."""
    print("=" * 88)
    print("NFRA_EDGES P3 -- (a) SET-COMPLETENESS coverage-check (post-derive, live canonical)")
    print("=" * 88)
    try:
        ok, missing, absent = live_coverage_check()
    except P1M.GraphUnavailable as ex:
        print("  UNVERIFIABLE (graph): %s" % ex)
        print("  NOT a pass. A silent [] here would read as 'nothing missing' -- a vacuous GREEN.")
        return 2
    print("  c3_subgraph_edges_missing_from_contract = %d   (FAIL LOUD if > 0)" % len(missing))
    print("  contract_edges_absent_from_live          = %d   (reported; already loud as edges_unresolved)"
          % len(absent))
    for m in missing[:5]:
        print("    MISSING (live qualifying edge absent from the frozen contract): %s" % (m,))
    for a in absent[:5]:
        print("    absent-from-live: %s" % (a,))
    print("\n  COVERAGE: %s" % ("PASS -- the frozen contract covers the live selection" if ok
                                else "FAIL LOUD -- the frozen contract UNDER-COVERS the live estate"))
    return 0 if ok else 1


SELECTION_RULE = {
    "description": "Recompute the intra-system edge set from the LIVE graph, then run subgraph_coverage_check "
                   "against the frozen contract. FAIL LOUD on any live qualifying edge absent from the contract.",
    "predicate": "edge_type in {FLOWS_TO, RENDERS} AND both endpoints resolve to C0/C1 constituents of the "
                 "C3's member motifs (a one-endpoint-inside edge is a BOUNDARY edge: excluded + counted)",
    "compare_on": ["src", "dst", "edge_type", "props"],
    # THE PROXY-INPUT TRAP (0.7.0_AE asked exactly this at build-planning; CTO 112711Z named the risk).
    # The "inside" set MUST be recomputed from the LIVE detector queries. It must NOT be obtained by walking
    # the C3's materialized CONTAINS subtree: those CONTAINS rows are themselves materialized from the FROZEN
    # spec (derive_runner.py:1383 `for se in spec_edges`), so using them to define "inside" makes this
    # coverage-check inherit the very freeze it exists to detect. A new estate node that SHOULD be a
    # constituent would not be "inside", its edges would not qualify, missing_from_contract would be empty,
    # and the check would PASS SILENTLY on a proxy input -- a check that cannot fire on the case it exists for.
    "constituent_resolution": "RECOMPUTE live: run each member detector's recurrence + expansion queries "
                              "against the live graph and take the resulting C0/C1 constituent ids. Do NOT "
                              "walk the materialized CONTAINS subtree (it is frozen-spec-derived).",
    "constituent_resolution_MUST_NOT": "walk the C3's CONTAINS edges in the derive graph -- they are formed "
                                       "from the frozen motif_c2c3_materialize.json (derive_runner.py:1383), "
                                       "so the inside-set would be frozen and the coverage-check vacuous.",
    "faithfulness_exercise": "The self-test proves the check's LOGIC (it is fed live_edges directly). It does "
                             "NOT prove the derive-time recompute is FAITHFUL. Only a live derive-run that "
                             "injects a genuinely-new qualifying ESTATE edge proves that -- CVO~B's live "
                             "round-trip, a hard condition on the materialize deploy-gate (CTO 112711Z).",
    # THE PROJECTION (0.7.0_AE's third consumer-catch). A live estate edge and a contract edge are NOT raw-
    # comparable: live props carry 7 keys with a SLASH kind ("recompute/guarded") at layer "aws"; the contract
    # carries the canonical {condition, kind-underscore} at layer "semctl". Compared raw, EVERY live edge reads
    # as missing_from_contract -> the coverage-check FAILS LOUD spuriously on every derive. A check that cries
    # wolf every run is as useless as one that never fires.
    "projection": {
        "apply_to": "BOTH sides before comparison (project_edge_props; idempotent, so contract records pass "
                    "through unchanged)",
        "compare_props_keys": list(_PROJECTED_PROP_KEYS),
        "kind_normalization": "P1E._EDGEKIND_NORMALIZE -- the ONE governed map "
                              "{recompute/guarded -> recompute_guarded, passthrough, rename, '' -> passthrough}. "
                              "NOT an ad-hoc slash->underscore rewrite (that would silently mis-handle a future kind).",
        "dropped_live_keys": ["dstField", "rename", "resolution", "srcField", "via"],
        "guard_preserved": "condition stays in the compare-identity, so two edges differing only by their guard "
                           "remain DISTINCT after projection (test 25, and the test-20 discipline).",
        "layer_is_not_identity": "layer is a SET-field in kuzu_incremental_refresh._cur_edges "
                                 "{(src,dst,edge_type,props): (layer, snapshot_ts)}, NOT part of the identity "
                                 "tuple. So aws-vs-semctl does not distinguish edges; only props does.",
    },
    "OPEN_ARCH_QUESTION_materialize_identity": "0.7.0_AE Q3, escalated to CTO -- NOT decided here. The 21 "
                                               "intra-system edges ALREADY EXIST as live estate CloudEdges "
                                               "(layer=aws, full props). Materializing the PROJECTED form "
                                               "creates a SECOND CloudEdge per pair (different props => "
                                               "different identity). Materializing the RAW form would instead "
                                               "MATCH the estate edge's identity and re-layer it aws->semctl "
                                               "in place (layer is a SET-field), corrupting the estate layer "
                                               "and churning drift-vector-2 every derive. Neither is obviously "
                                               "right; it is a graph-topology decision with blast radius. "
                                               "AWAITING CTO. Do not materialize until ruled.",
    "fail_loud_when": "missing_from_contract > 0  (a NEW qualifying estate edge the frozen list would have "
                      "silently dropped)",
    "emit_counter": "c3_subgraph_edges_missing_from_contract  (belongs in the R3-verify beside edges_unresolved=0)",
    # CORRECTED (my own earlier spec said "derive time, before materialize" -- unimplementable on this
    # substrate). derive_runner imports kuzu NOWHERE; the ingest works over the in-memory graph dict; Kuzu only
    # exists after kuzu_nessie_load reads Iceberg post-commit. The D1-D7 detectors are Cypher over
    # CloudNode/CloudEdge, so they cannot execute at derive time.
    "run_at": "POST-DERIVE, in the existing R3-verify leg (the comp-kuzu round-trip), against the freshly "
              "loaded canonical -- NOT inside the derive ingest.",
    "executor": "python org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/NFRA_EDGES_P3_c3_subgraph.py "
                "--coverage-check   ->  rc=0 clean | rc=1 FAIL LOUD | rc=2 UNVERIFIABLE",
    "no_reimplementation": "AE imports nothing into the derive image and re-implements nothing. The entrypoint "
                           "runs the SAME live detector queries through the SAME P1M/P1E code as the "
                           "analysis-side emission -- one builder, so the recompute cannot drift into a "
                           "second proxy (AE + COO~B's same-source-of-truth condition).",
    "detects_not_prevents": "A failed check fails the R3 leg -> the deploy fails -> the never-half-land ledger "
                            "stays OPEN -> rollback. Set-incompleteness is a data-coverage defect, not a "
                            "corruption, so detect-and-roll-back is the right instrument and the ledger already "
                            "provides it.",
    "why": "ingest_c2c3_motif_producer replays a frozen list with no live discovery: deletions are loud, "
           "ADDITIONS are silent. AC5 covers per-entity freshness, not set-completeness.",
    "root_fix_routed": "COO~B -> CTO, estate-wide: derive the selection live at derive time and demote the "
                       "frozen contract to an R3 expected-value FIXTURE. The C2/C3 CONTAINS materialize has "
                       "this same hole today, so it is a pattern change, not a P3 bolt-on.",
}


# THE NODE-TYPE TRAP -- the exact twin of the edge-identity trap, and I walked into it (0.7.0_AE caught it
# pre-build, 111217Z). comp_ladder's Node.ntype is an ANALYSIS-side type name. The STORE's node_type is a
# different vocabulary, governed by derive_runner.NODE_TYPE_LAYER:
#   - the SERVED node system:firm-conditional-display:25558d98 carries node_type "C3System" (live-verified);
#   - NODE_TYPE_LAYER maps {"C2Motif": "semctl", "C3System": "semctl"} and has NO "EmergentSystem" entry;
#   - "EmergentSystem" appears NOWHERE in infra/aws/globgrph (0 matches / 63 files) -- it is not a store type;
#   - the precedent contract motif_c2c3_materialize.json uses "C3System" for this same node_id.
# Emitting node_type="EmergentSystem" would therefore (i) FAIL-CLOSE relabel_layers_by_node_type on an
# unmapped type (aborting the derive) and (ii) be a node_TYPE change on a served node -- a different animal
# from the node_ID stability we measured. req2 ("no new node_type") is satisfied by using the EXISTING STORE
# type, not by echoing the analysis ntype.
_ANALYSIS_TO_STORE_NODE_TYPE = {"EmergentSystem": "C3System"}


def store_node_type(analysis_ntype: str) -> str:
    """Map an analysis-side ntype onto the governed STORE node_type. FAIL LOUD on an unmapped type: an
    unmapped node_type reaches the derive and fail-closes relabel_layers_by_node_type, so it is far better
    to fail here, at contract-emission, than at 02:00Z inside the nightly."""
    try:
        return _ANALYSIS_TO_STORE_NODE_TYPE[analysis_ntype]
    except KeyError:
        raise RuntimeError(
            "analysis ntype %r has no governed STORE node_type. Do NOT emit it: derive_runner's "
            "NODE_TYPE_LAYER would fail-close on an unmapped type. Add the mapping (and the "
            "NODE_TYPE_LAYER entry, 0.7.0_AE's lane) deliberately." % analysis_ntype) from None


def to_c3_node_record(system: Node, signature: dict, snapshot_ts: int) -> dict:
    """The C3 node record: the existing STORE node_type (req2 -- no new node_type), carrying the data-flow
    signature as a PROPERTY, plus AC5's snapshot_ts.

    node_type is the STORE type (C3System), NOT system.ntype (the analysis-side "EmergentSystem"). See the
    node-type trap above. This is the same analysis-vs-store confusion as the edge-identity trap, one node up.
    """
    return {
        "node_id": system.nid,                      # settled, collision-safe (req4)
        "node_type": store_node_type(system.ntype),  # STORE type, governed by NODE_TYPE_LAYER
        "layer": "semctl",
        "snapshot_ts": snapshot_ts,                 # AC5
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
                # (C) IS THE ARCHITECTURE (CTO ruling 115438Z). The intra-system edges are NOT materialized:
                # semctl twins would feed back through the LAYER-BLIND D2/D3 detectors (4 of them carry the
                # inflection literal in `condition`) -> D3 recurrence 4->8 -> P2's edge-motif node_id changes
                # -> the AC4 stability invariant is broken by P3's own output. So the ONLY materialized entity
                # is the C3 node (its req2 signature prop + AC5 snapshot_ts). The 21 edges below are an
                # EXPECTED-VALUE FIXTURE for the R3 traversal-assertion and for the (a) coverage-check.
                "architecture": "(C) no-duplicate: the C3 carries its subgraph by REACHABILITY "
                                "(C3 -CONTAINS-> C2Motif -CONTAINS-> C1 constituents; the FLOWS_TO/RENDERS "
                                "estate edges among them already exist at layer=aws). CTO ruling 115438Z.",
                "materialize": ["c3_node"],
                "do_NOT_materialize": "intra_system_edges -- they already exist as live estate CloudEdges. "
                                      "Writing semctl twins is a SELF-REFERENTIAL FEEDBACK CORRUPTION: no "
                                      "detector filters layer, D2/D3 select on props CONTAINS "
                                      "'inflection_wealth_management', 4 of the 21 carry it -> they would be "
                                      "re-detected, D3 recurrence 4->8, P2's canonical edge-set and therefore "
                                      "its motif node_id CHANGE. (A) REJECTED. (B) MERGEs onto the estate edge "
                                      "and flaps its layer aws<->semctl every derive -- REJECTED.",
                "intra_system_edges_role": "EXPECTED-VALUE FIXTURE. Assert present + both-ends resolve + "
                                           "unresolved=0 + boundary=0 by LIVE traversal (AC-1). Compare against "
                                           "the live recompute for the (a) coverage-check. Never written.",
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
                # COO~B scope-ruling 111120Z option (a): the ingest MUST recompute the live selection at
                # derive time and FAIL LOUD on any live qualifying edge absent from this frozen list.
                "selection_rule": SELECTION_RULE,
                "coverage_check": {
                    "required": True,
                    "expected_edge_count": len(intra),
                    "run_at": "derive time, before materialize",
                    "fail_loud_when": "missing_from_contract > 0",
                    "note": "A frozen row-set is per-entity fresh (snapshot_ts) and can still be permanently "
                            "INCOMPLETE. AC5 covers the entity, this covers the SET. Deletions are already "
                            "loud (edges_unresolved); this closes the silent ADDITION half.",
                },
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
    chk("9  req2: signature rides as a PROP on the existing STORE node_type (no new node_type)",
        rec["node_type"] == "C3System" and "signature" in rec["props"] and sig["edge_count"] == 1)

    # THE NODE-TYPE TRAP (0.7.0_AE caught this pre-build): the emitted node_type must be the STORE type
    # (C3System, governed by NODE_TYPE_LAYER + carried by the served node), NOT comp_ladder's analysis-side
    # ntype ("EmergentSystem", which appears nowhere in infra/aws/globgrph and would FAIL-CLOSE the derive).
    chk("9a node-type TRAP: the record carries the STORE node_type, NOT the analysis-side ntype",
        rec["node_type"] == "C3System" and rec["node_type"] != sysnode.ntype)

    # and an UNMAPPED analysis ntype must FAIL LOUD at contract-emission, not reach the derive.
    try:
        store_node_type("SomeUngovernedType")
        raised = False
    except RuntimeError:
        raised = True
    chk("9b node-type TRAP: an UNMAPPED analysis ntype raises at emission (never reaches the derive's "
        "fail-close relabel)", raised)

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

    # ---- COO~B 111120Z option (a): the derive-time SET-COMPLETENESS check, AND ITS EXERCISE.
    # "Don't ship a coverage-check you haven't proven bites." A check that cannot fire is itself a proxy.
    e_contract = to_intra_edge_record(shared_edge, SELFTEST_SNAPSHOT_TS_MS)
    e_new_live = to_intra_edge_record(
        P1E.reify_edge("out:n/N.tsx:5#n", "out:m/M.tsx:6#m", "FLOWS_TO", "firm == true", "recompute/guarded"),
        SELFTEST_SNAPSHOT_TS_MS)

    ok_same, miss_same, _abs_same = subgraph_coverage_check([e_contract], [e_contract])
    chk("17 coverage-check PASSES when the frozen contract matches the live selection",
        ok_same is True and not miss_same)

    # THE SILENT HALF, exercised: a live qualifying edge that the frozen contract does not contain.
    ok_add, miss_add, _abs_add = subgraph_coverage_check([e_contract], [e_contract, e_new_live])
    chk("18 coverage-check GATE: a live qualifying edge ABSENT from the contract -> FAIL LOUD (the silent "
        "under-materialization the frozen-spec replay would never have reported)",
        ok_add is False and len(miss_add) == 1)

    # The already-loud half is still REPORTED, never inferred -- and it must NOT trip the fail-loud gate,
    # because a deletion already surfaces as edges_unresolved at the ingest.
    ok_del, miss_del, abs_del = subgraph_coverage_check([e_contract, e_new_live], [e_contract])
    chk("19 coverage-check: a contract edge no longer live is REPORTED as absent_from_live, and does NOT "
        "trip the fail-loud gate (deletions are already loud via edges_unresolved)",
        len(abs_del) == 1 and ok_del is True and not miss_del)

    # Non-vacuity: the gate must key on the STORE identity tuple. Two edges differing ONLY by their guard
    # condition (which lives in props) must be DISTINCT to the check -- else a swapped guard reads as covered.
    e_other_guard = to_intra_edge_record(
        P1E.reify_edge("out:a/A.tsx:1#x", "out:b/B.tsx:2#y", "FLOWS_TO", "firm == false", "recompute/guarded"),
        SELFTEST_SNAPSHOT_TS_MS)
    ok_guard, miss_guard, _ = subgraph_coverage_check([e_contract], [e_other_guard])
    chk("20 coverage-check keys on the STORE identity (props carries the guard): an edge differing ONLY by "
        "its condition is NOT considered covered", ok_guard is False and len(miss_guard) == 1)

    # ---- THE PROJECTION (0.7.0_AE's third consumer-catch). A RAW live estate edge carries 7 props keys and a
    # SLASH-form kind; the contract carries the canonical {condition, kind-underscore}. Without projecting both
    # sides, every live edge reads as missing_from_contract and (a) FAILS LOUD spuriously on every derive.
    raw_live = {
        "src": "out:a/A.tsx:1#x", "dst": "out:b/B.tsx:2#y", "edge_type": "FLOWS_TO",
        "props": json.dumps({"condition": "firm == true", "dstField": "y", "kind": "recompute/guarded",
                             "rename": False, "resolution": "getSymbol ...", "srcField": "X.p",
                             "via": "mapping a/A.tsx:1"}, sort_keys=True),
    }
    chk("21 PROJECTION: a RAW live estate edge (7 props keys, slash-kind) projects to the contract's canonical "
        "{condition,kind} form", project_edge_props(raw_live["props"]) == e_contract["props"])

    ok_proj, miss_proj, _ = subgraph_coverage_check([e_contract], [raw_live])
    chk("22 PROJECTION GATE: the SAME edge in raw-live form vs contract form must NOT read as missing "
        "(no spurious FAIL LOUD every derive)", ok_proj is True and not miss_proj)

    # Non-vacuity of the projection: comparing the RAW props un-projected WOULD have reported it missing.
    raw_key = intra_edge_identity(raw_live["src"], raw_live["dst"], raw_live["edge_type"], raw_live["props"])
    con_key = intra_edge_identity(e_contract["src"], e_contract["dst"], e_contract["edge_type"], e_contract["props"])
    chk("23 PROJECTION non-vacuity: un-projected raw props != contract props (so the projection is doing real "
        "work, not a no-op)", raw_key != con_key)

    # Idempotence: projecting an already-canonical contract record must not change it.
    chk("24 PROJECTION is idempotent (contract records pass through unchanged)",
        project_edge_props(e_contract["props"]) == e_contract["props"])

    # The projection must NOT collapse a guard difference (test-20 discipline, now through the projection).
    chk("25 PROJECTION preserves the guard: two edges differing only by condition stay DISTINCT after projection",
        project_edge_props(e_contract["props"]) != project_edge_props(e_other_guard["props"]))

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
    if "--coverage-check" in args:      # AE's R3-verify leg (post-derive, live canonical)
        return run_coverage_check()
    return run_live(emit_contract="--contract" in args)


if __name__ == "__main__":
    sys.exit(main())
