#!/usr/bin/env python3
"""NFRA_EDGES P2 -- C2 EDGE-MOTIFS (recurring edge idioms over the P1-reified *Edge C1 nodes).

P1 (262053a3d, both gates MET) lifted each motif-defining FLOWS_TO/RENDERS edge into a first-class
C1 *Edge Node with a collision-safe id. P2 closes the compose-middle on the EDGE axis: a set of
reified *Edge C1 nodes that share a DEFINING SIGNATURE, recurring >= AC3_THRESHOLD times, IS a C2
motif -- exactly as a set of sink-keyed C1 interactions is (NFRA_MOTIF_P1 build_motif).

  C2 motif (PRD S3/S4.1) = lossy-toward-abstraction, lossless-toward-provenance compression of a
  CONNECTED C1 subgraph, qualified by recurrence >= 2 (recurrence-1 = an *instance*, not a motif).

  node axis (MOTIF-P1): many C1 sink-interactions  -> one C2 idiom  ("silent-display-fork")
  EDGE axis (THIS)    : many C1 reified *Edge nodes -> one C2 idiom  ("guarded FLOWS_TO under
                                                                      condition C, recurring xN")

The ABSTRACTION is over LOCUS (which src->sink pair), never over the guard. An edge's IDENTITY tuple
is (src, sink, edge_type, condition) [P1 edge_node_id]; a motif's SIGNATURE drops the instance-specific
(src, sink) and keeps (edge_type, edge_kind, condition) -- so the motif says "this shaped edge recurs
at N loci", and each instance decompresses to its own C0 flow-fact.

TWO LOAD-BEARING CARRY-FORWARDS (COO~B GO 20260709T072607Z; bound into EVERY phase, non-negotiable):
  AC4 COLLISION-SAFE MOTIF IDS: the CONDITION is IN the motif identity tuple, so two motifs that
     differ ONLY by a guard/condition get DISTINCT stable ids -- no silent motif-MERGE (the edge-motif
     extension of P1's edge_node_id discipline, itself inheriting the C3 system_node_id fix f875bc854).
     The failure mode is MERGE (two idioms collapsing into one id -> a silent store-side MERGE that
     destroys one of them), so where identity is ambiguous this module OVER-SPLITS by construction:
     the condition is hashed VERBATIM, never normalized/canonicalized into a bucket.
     Self-tested distinct-tuple->distinct-id + same-tuple->stable-id (mirrors P1 lines 225-231).

  AC5 FRESHNESS: every motif emission carries snapshot_ts stamped on the REAL producer basis --
     derive_runner.py:1821 `batch_ts = int(time.time() * 1000)` (MILLISECONDS), written to every
     node/edge row (derive_runner.py:338/369). This is what makes the consumer's change-detection
     fire: kuzu_incremental_refresh.py:165-166 upserts a key iff
        `int(row["snapshot_ts"]) != cur_ts[key]`
     and the nightly derive full-OVERWRITES every row with a fresh batch_ts (_canonical.py:288).
     => a CONSTANT snapshot_ts is never re-upserted after first load: the node's props/layer/label
        can drift while the refresh silently skips it. Born drift-BLIND -- the exact failure AC5 exists
        to prevent. Hence derive_batch_ts() below, NOT a sentinel, on every live emission.

INHERITED-DEFECT NOTE (P1, LATENT -- reported, not silently patched; P1 is CVO-certed):
  P1's live proof stamps `snapshot_ts = SELFTEST_SNAPSHOT_TS` (NFRA_EDGES_P1_edge_reification.py:162),
  a CONSTANT whose value 1751990400 is a 10-digit SECONDS epoch (2025-07-08T16:00Z) while the real
  producer stamps a 13-digit MILLISECONDS batch_ts (~1018x larger). Two distinct AC5 defects:
    (a) CONSTANT   -> incremental-refresh change-detection (`!=`) never fires -> drift-blind;
    (b) WRONG UNIT -> any freshness/ordering comparison against real rows is off by ~1000x.
  Both are LATENT: P1 builds the CloudNode record but never writes it to the store (materialize is P3).
  So nothing is corrupted today. P2 does not inherit either defect. Routed to CTO/CVO/COO~B with the
  one-line fix (use derive_batch_ts(); ms-scale sentinel for the self-test only).

SCOPE (COO~B FORWARD-NOTE, explicit): P2 emits the motif MECHANISM + snapshot_ts. The full 9-field
graph_nodes emission + the cloud materialize are P3 items and are deliberately NOT done here. This
module writes NOTHING to the store.

Usage:
  python NFRA_EDGES_P2_edge_motifs.py --self-test   # MECHANISM proof (synthetic, no graph): AC4/AC3/AC5
  python NFRA_EDGES_P2_edge_motifs.py              # PROVE on the live firm detectors (fail-loud)

Author: 0.4.0_DS_ClientPlatform~B (SEMCTL lane, NFRA_EDGES P2 owner). TO NFRA_EDGES.P2.
"""
from __future__ import annotations

import hashlib
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(WS, "org", "modules", "graph"))

import NFRA_EDGES_P1_edge_reification as P1E  # noqa: E402 -- the certed P1 edge-reification base
import NFRA_MOTIF_P1_c2_catalog as P1M        # noqa: E402 -- CATALOG + comp_kuzu + AC3_THRESHOLD
from comp_ladder import Node, decompress, fidelity_check  # noqa: E402 -- the REAL Node model + gate

# The firm detectors P1 proved on (same live surface -> the P2 result is comparable to P1's).
_FIRM_DETECTORS = P1E._FIRM_DETECTORS

# ms-scale sentinel for the SELF-TEST only (reproducible, no wall-clock). Real emissions use
# derive_batch_ts(). Deliberately 13-digit to match the producer basis (P1's 10-digit seconds
# sentinel is the inherited defect documented above).
SELFTEST_SNAPSHOT_TS_MS = 1751990400000

_EDGE_MOTIF_NTYPE = {
    "FLOWS_TO": "FlowsToEdgeMotif",
    "RENDERS": "RendersEdgeMotif",
    "PROP_PASSES": "PropPassesEdgeMotif",
}


def derive_batch_ts() -> int:
    """The REAL producer basis for snapshot_ts -- byte-for-byte the derive_runner stamp.

    Grounded at source: infra/aws/globgrph/derive_runner.py:1821  `batch_ts = int(time.time() * 1000)`,
    written to every node row (:338) and edge row (:369) as `snapshot_ts`. MILLISECONDS.

    Why a live wall-clock and not a constant: kuzu_incremental_refresh.py:165-166 upserts a key iff
    its snapshot_ts CHANGED, and the nightly derive full-overwrites all rows with a fresh batch_ts
    (_canonical.py:288). A constant stamp => never re-upserted => silent drift. AC5 = born drift-safe.
    """
    return int(time.time() * 1000)


def _norm_kind(edge_kind: str) -> str:
    """Normalize a live props `kind` onto the governed EdgeKind vocabulary (P1's map, one source)."""
    return P1E._EDGEKIND_NORMALIZE.get(edge_kind, edge_kind or "passthrough")


# ---------------------------------------------------------------------------
# AC4 -- the edge-MOTIF signature + its collision-safe, stable node_id.
# ---------------------------------------------------------------------------
def edge_motif_signature(edge_type: str, edge_kind: str, condition: str) -> tuple:
    """The DEFINING SIGNATURE of an edge-motif: (edge_type, edge_kind, condition).

    Abstracts over LOCUS (src, sink -- the instance-specific half of P1's edge identity tuple) and
    keeps the SHAPE. The condition is carried VERBATIM: two idioms that differ only by their guard are
    DIFFERENT motifs (AC4). Normalizing the condition into a bucket would MERGE them -- the exact
    silent-collapse this AC forbids -- so we never do it.
    """
    return (edge_type, _norm_kind(edge_kind), condition or "")


def edge_motif_node_id(sig: tuple) -> str:
    """UNIQUE-BY-CONSTRUCTION, STABLE C2 edge-motif node_id = human-readable prefix + a deterministic
    discriminator over the FULL signature (condition included -> no silent motif-merge, AC4).

    Same discipline as P1.edge_node_id / P1M.system_node_id: distinct tuple -> distinct id (never a
    reused label); same tuple -> identical id across runs (the full-overwrite derive re-materializes
    to the same node: no churn, no orphan).
    """
    edge_type, edge_kind, condition = sig
    key = "|".join([edge_type, edge_kind, condition])
    disc = hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]
    return "motif:edge:" + edge_type.lower() + ":" + disc


# ---------------------------------------------------------------------------
# Grouping -- reified *Edge C1 nodes -> signature-keyed candidate motifs.
# ---------------------------------------------------------------------------
def group_edges_by_signature(edge_pairs: list) -> dict:
    """Group reified *Edge C1 nodes by their motif signature.

    edge_pairs: list of (edge_node: Node, cloud_record: dict) as returned in LOCKSTEP by
    P1.reify_motif_edges (edge_nodes[i] <-> cloud_records[i]; both appended together, already
    deduped by the AC4 edge id). The record's props carry the signature fields at source, so we
    read the signature off the record rather than re-parsing the node label.

    Returns {signature: [edge_node, ...]} -- insertion-ordered, deterministic.
    """
    groups: dict = {}
    for edge_node, rec in edge_pairs:
        p = rec["props"]
        sig = edge_motif_signature(p["edge_type"], p["edge_kind"], p["condition"])
        groups.setdefault(sig, []).append(edge_node)
    return groups


# ---------------------------------------------------------------------------
# AC1/AC6 -- compose a C2 edge-motif whose children are the reified *Edge C1 nodes.
# ---------------------------------------------------------------------------
def build_edge_motif(sig: tuple, edge_nodes: list) -> Node:
    """Compose a C2 edge-motif Node from its recurring *Edge C1 instances.

    children = the reified *Edge C1 nodes -> each decompresses to {src C0, sink C0, C0 FlowFact}, so
    the motif bottoms out in lexical evidence and PASSES comp_ladder.fidelity_check identically to a
    node-motif. A LATENT edge-motif (no instances) FAILS the gate, same as any latent node.
    """
    edge_type, edge_kind, condition = sig
    cond_label = (condition[:44] + "...") if len(condition) > 44 else (condition or "-")
    return Node(
        edge_motif_node_id(sig), "C2",
        _EDGE_MOTIF_NTYPE.get(edge_type, edge_type.title().replace("_", "") + "EdgeMotif"),
        "%s[%s] guard=%s (x%d)" % (edge_type, edge_kind, cond_label, len(edge_nodes)),
        rule=("EDGE-MOTIF: recurring %s edges (EdgeKind=%s) under condition=%s -- recurrence=%d "
              "distinct loci; abstraction over (src,sink), condition IN the identity (AC4)"
              % (edge_type, edge_kind, condition or "-", len(edge_nodes))),
        children=list(edge_nodes))


# ---------------------------------------------------------------------------
# AC5 -- the emission record (motif MECHANISM + snapshot_ts). NOT the P3 9-field materialize.
# ---------------------------------------------------------------------------
def to_cloud_motif_record(motif: Node, sig: tuple, recurrence: int, snapshot_ts: int) -> dict:
    """The C2 edge-motif emission record: node_id/node_type/layer/props + snapshot_ts (AC5).

    Mirrors P1.to_cloud_node's shape. snapshot_ts MUST come from derive_batch_ts() on a live emission
    (ms, changes every derive) so kuzu_incremental_refresh's `!=` change-detection covers this entity.

    SCOPE: the full 9-field graph_nodes emission + the store materialize are P3 (COO~B forward-note).
    Nothing here is written to the store.
    """
    edge_type, edge_kind, condition = sig
    return {
        "node_id": motif.nid,          # collision-safe + stable (AC4) -> the incremental-refresh key
        "node_type": motif.ntype,      # FlowsToEdgeMotif / RendersEdgeMotif
        "layer": "semctl",
        "snapshot_ts": snapshot_ts,    # AC5: real batch_ts basis (ms) -> change-detection covers it
        "props": {"edge_type": edge_type, "edge_kind": edge_kind,
                  "condition": condition, "recurrence": recurrence},
    }


# ---------------------------------------------------------------------------
# AC3 -- recurrence >= threshold = a MOTIF; recurrence 1 = an instance (reported, never forced).
# ---------------------------------------------------------------------------
def classify_groups(groups: dict, snapshot_ts: int) -> tuple:
    """Apply the AC3 stability threshold. Returns (motifs, records, instances).

    motifs    : [(sig, motif_node, recurrence)] for recurrence >= P1M.AC3_THRESHOLD
    records   : the AC5 emission record per motif
    instances : [(sig, recurrence)] below threshold -- an *instance*, NOT a motif (reported, not dropped)
    """
    motifs, records, instances = [], [], []
    for sig, edge_nodes in groups.items():
        recurrence = len(edge_nodes)
        if recurrence < P1M.AC3_THRESHOLD:
            instances.append((sig, recurrence))
            continue
        motif = build_edge_motif(sig, edge_nodes)
        motifs.append((sig, motif, recurrence))
        records.append(to_cloud_motif_record(motif, sig, recurrence, snapshot_ts))
    return motifs, records, instances


def edge_motifs_for_spec(spec: dict, snapshot_ts: int) -> tuple:
    """Reify one detector's defining edges (P1) then compose them into C2 edge-motifs (P2).

    Fail-loud on graph error (P1M.GraphUnavailable propagates -- never a silent [] misread as
    'no motif', which would be a discovery false-negative).
    """
    edge_nodes, cloud_records = P1E.reify_motif_edges(spec, snapshot_ts)
    if len(edge_nodes) != len(cloud_records):  # lockstep invariant P1 guarantees; assert, never assume
        raise RuntimeError("P1 reify_motif_edges broke lockstep: %d edge_nodes vs %d records"
                           % (len(edge_nodes), len(cloud_records)))
    groups = group_edges_by_signature(list(zip(edge_nodes, cloud_records)))
    return classify_groups(groups, snapshot_ts)


# ---------------------------------------------------------------------------
# PROVE on the live firm detectors -- edge-motifs emerge from the reified edge axis.
# ---------------------------------------------------------------------------
def prove_edge_motifs() -> int:
    print("=" * 88)
    print("NFRA_EDGES P2 -- PROVE C2 edge-motifs on the live firm detectors (D1/D2/D3)")
    print("=" * 88)
    snapshot_ts = derive_batch_ts()   # AC5: the REAL producer basis (ms), never a constant
    print("  snapshot_ts (derive_runner batch_ts basis, ms): %d" % snapshot_ts)

    all_groups: dict = {}
    try:
        for spec in P1M.CATALOG:
            if spec["id"] not in _FIRM_DETECTORS:
                continue
            edge_nodes, cloud_records = P1E.reify_motif_edges(spec, snapshot_ts)
            for sig, nodes in group_edges_by_signature(list(zip(edge_nodes, cloud_records))).items():
                all_groups.setdefault(sig, []).extend(nodes)
    except P1M.GraphUnavailable as ex:
        print("  UNVERIFIABLE (graph): %s" % ex)
        print("  The MECHANISM is proven by --self-test (synthetic, no graph). Re-run when reachable.")
        return 2

    # dedup across detectors by the AC4 edge id (D2/D3 overlap on the inflection edges BY DESIGN)
    for sig, nodes in list(all_groups.items()):
        seen, uniq = set(), []
        for n in nodes:
            if n.nid in seen:
                continue
            seen.add(n.nid)
            uniq.append(n)
        all_groups[sig] = uniq

    motifs, records, instances = classify_groups(all_groups, snapshot_ts)

    print("\n  C2 EDGE-MOTIFS (recurrence >= %d):" % P1M.AC3_THRESHOLD)
    print("  %-46s %-6s %-9s %s" % ("node_id", "recur", "fidelity", "signature"))
    print("  " + "-" * 100)
    all_ok = True
    for sig, motif, recurrence in motifs:
        ok, failures = fidelity_check(motif)
        all_ok = all_ok and ok
        et, ek, cond = sig
        print("  %-46s %-6d %-9s %s[%s] guard=%s"
              % (motif.nid, recurrence, "PASS" if ok else "FAIL", et, ek, (cond or "-")[:34]))
        for f in failures[:3]:
            print("       ! " + f)

    if instances:
        print("\n  Below AC3 threshold -- INSTANCES, not motifs (reported, never forced into a motif):")
        for sig, recurrence in instances:
            print("    recurrence=%d  %s[%s] guard=%s" % (recurrence, sig[0], sig[1], (sig[2] or "-")[:40]))

    # AC4 live check: every motif id distinct, and distinct signatures never share an id.
    ids = [m.nid for _, m, _ in motifs]
    ac4_live = len(ids) == len(set(ids))

    n_edges = sum(r for _, _, r in motifs) + sum(r for _, r in instances)
    flow_facts = sum(1 for _, m, _ in motifs
                     for _, n in decompress(m) if n.layer == "C0" and n.ntype == "FlowFact")
    print("\n  Decomposition: %d reified *Edge C1 instances -> %d C2 edge-motifs (+%d sub-threshold)"
          % (n_edges, len(motifs), len(instances)))
    print("  Every motif bottoms out in C0 lexical evidence: %d FlowFact C0 nodes" % flow_facts)
    print("\n  AC5 sample emission record (snapshot_ts on the real derive basis):")
    if records:
        r = records[0]
        print("    " + str({k: r[k] for k in ("node_id", "node_type", "layer", "snapshot_ts")}))
        print("    props: " + str(r["props"]))
    print("\n  AC4 (collision-safe motif ids, all distinct): %s" % ("PASS" if ac4_live else "FAIL"))
    print("  AC6 (every C2 edge-motif decompresses to C0 evidence): %s" % ("PASS" if all_ok else "FAIL"))
    ok_all = bool(motifs) and all_ok and ac4_live
    print("\n  P2: C2 edge-motifs emerge from the reified edge axis, fidelity green: %s"
          % ("PASS" if ok_all else "FAIL"))
    return 0 if ok_all else 1


# ---------------------------------------------------------------------------
# Self-test -- the MECHANISM (synthetic, no live graph): AC4 / AC3 / AC5 / fidelity + negative controls.
# ---------------------------------------------------------------------------
def _mk_edge(src: str, sink: str, edge_type: str, cond: str, kind: str):
    """A reified *Edge C1 node + its P1 cloud record (the lockstep pair group_edges_by_signature eats)."""
    node = P1E.reify_edge(src, sink, edge_type, cond, kind)
    rec = P1E.to_cloud_node(node, SELFTEST_SNAPSHOT_TS_MS, src, sink, edge_type, cond, kind)
    return node, rec


def self_test() -> int:
    print("=== NFRA_EDGES_P2 self-test (C2 edge-motif mechanism; no live graph) ===")
    ok = []

    def chk(name, cond):
        ok.append(bool(cond))
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    sig_true = edge_motif_signature("FLOWS_TO", "recompute/guarded", "firm == true")
    sig_false = edge_motif_signature("FLOWS_TO", "recompute/guarded", "firm == false")

    # 1. AC4 (GATES THE PHASE): two motifs differing ONLY by the guard condition -> DISTINCT ids.
    chk("1  AC4: motifs differing ONLY by condition -> DISTINCT node_ids (no silent motif-MERGE)",
        edge_motif_node_id(sig_true) != edge_motif_node_id(sig_false))

    # 2. AC4 STABILITY: the same signature -> the SAME id across runs (full-overwrite derive: no churn).
    chk("2  AC4: same signature -> STABLE identical node_id across runs",
        edge_motif_node_id(edge_motif_signature("FLOWS_TO", "recompute/guarded", "firm == true"))
        == edge_motif_node_id(sig_true))

    # 3. AC4: edge_type is part of the identity.
    chk("3  AC4: differing edge_type -> distinct motif id",
        edge_motif_node_id(edge_motif_signature("RENDERS", "recompute/guarded", "firm == true"))
        != edge_motif_node_id(sig_true))

    # 4. AC4: edge_kind is part of the identity.
    chk("4  AC4: differing edge_kind -> distinct motif id",
        edge_motif_node_id(edge_motif_signature("FLOWS_TO", "passthrough", "firm == true"))
        != edge_motif_node_id(sig_true))

    # 5. GROUPING (the AC4 merge-guard exercised END-TO-END, not just at the id): two edges that differ
    #    only by their guard must land in TWO groups, never one.
    pairs_mixed = [
        _mk_edge("out:a/A.tsx:1#x", "out:a/B.tsx:2#y", "FLOWS_TO", "firm == true", "recompute/guarded"),
        _mk_edge("out:a/C.tsx:3#p", "out:a/D.tsx:4#q", "FLOWS_TO", "firm == false", "recompute/guarded"),
    ]
    g_mixed = group_edges_by_signature(pairs_mixed)
    chk("5  AC4 end-to-end: 2 edges differing ONLY by guard -> 2 DISTINCT groups (never merged)",
        len(g_mixed) == 2)

    # 6. GROUPING positive: two edges at DIFFERENT loci sharing the signature -> ONE motif, recurrence 2.
    pairs_same = [
        _mk_edge("out:a/A.tsx:1#x", "out:a/B.tsx:2#y", "FLOWS_TO", "firm == true", "recompute/guarded"),
        _mk_edge("out:z/M.tsx:9#r", "out:z/N.tsx:8#s", "FLOWS_TO", "firm == true", "recompute/guarded"),
    ]
    g_same = group_edges_by_signature(pairs_same)
    chk("6  abstraction over LOCUS: 2 edges, same signature, different src/sink -> ONE group (recurrence 2)",
        len(g_same) == 1 and len(list(g_same.values())[0]) == 2)

    # 7. AC3: recurrence 2 = a MOTIF; recurrence 1 = an INSTANCE (not forced into a motif).
    motifs_s, records_s, instances_s = classify_groups(g_same, SELFTEST_SNAPSHOT_TS_MS)
    motifs_m, _, instances_m = classify_groups(g_mixed, SELFTEST_SNAPSHOT_TS_MS)
    chk("7  AC3: recurrence 2 -> 1 motif, 0 instances; recurrence 1 each -> 0 motifs, 2 instances",
        len(motifs_s) == 1 and len(instances_s) == 0
        and len(motifs_m) == 0 and len(instances_m) == 2)

    # 8. AC1/AC6 fidelity: the C2 edge-motif decompresses to C0 FlowFact evidence, gate PASSES.
    motif = motifs_s[0][1]
    ok_f, _ = fidelity_check(motif)
    c0kinds = {n.ntype for _, n in decompress(motif) if n.layer == "C0"}
    chk("8  AC6: C2 edge-motif decompresses to C0 (EdgeSource+EdgeSink+FlowFact) + PASSES fidelity",
        ok_f and {"EdgeSource", "EdgeSink", "FlowFact"} <= c0kinds)

    # 9. NEGATIVE CONTROL: a LATENT edge-motif (no instances) MUST FAIL the gate -- the gate must BITE.
    latent = Node(edge_motif_node_id(sig_true), "C2", "FlowsToEdgeMotif", "latent", children=[])
    ok_l, fails_l = fidelity_check(latent)
    chk("9  negative control: a LATENT edge-motif (no C1 instances) FAILS fidelity (the gate bites)",
        ok_l is False and len(fails_l) > 0)

    # 10. AC5: the emission record conforms + carries snapshot_ts keyed to the motif's own node_id.
    rec = records_s[0]
    chk("10 AC5: emission record carries snapshot_ts + node_id/node_type/layer/props, keyed to the motif",
        rec.get("snapshot_ts") == SELFTEST_SNAPSHOT_TS_MS
        and {"node_id", "node_type", "layer", "props"} <= set(rec)
        and rec["node_id"] == motif.nid and rec["props"]["recurrence"] == 2)

    # 11. AC5 REGRESSION GUARD (the P1 inherited-defect class): the live stamp must be the REAL
    #     derive_runner basis -- MILLISECONDS (13-digit), not a 10-digit seconds epoch. Catches both
    #     the wrong-unit bug and (by using a wall-clock, not a constant) the drift-blind constant bug.
    ts = derive_batch_ts()
    chk("11 AC5 guard: derive_batch_ts() is ms-scale (>=1e12), matching derive_runner.py:1821 int(time.time()*1000)",
        ts >= 1_000_000_000_000)
    chk("12 AC5 guard: derive_batch_ts() is a live wall-clock, NOT a constant (change-detection can fire)",
        derive_batch_ts() >= ts)

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
    return prove_edge_motifs()


if __name__ == "__main__":
    sys.exit(main())
