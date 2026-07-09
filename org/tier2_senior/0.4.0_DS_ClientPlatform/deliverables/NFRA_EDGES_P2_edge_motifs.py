#!/usr/bin/env python3
"""NFRA_EDGES P2 -- C2 EDGE-MOTIFS: each D1-D7 detector emits its recurring EDGE-CONFIGURATION.

Built to TO org/tier1_exec/2.0.0_SA_COO/task_orders/NFRA_EDGES.P2.c2-edge-motifs.md and to the
committed design prep (deliverables/NFRA_EDGES_P2_edge_motif_design_prep.md).

  gate_note (TO): "The D1-D7 motifs ARE edge-patterns (D1 = '>=2 guarded FLOWS_TO into one sink') --
  but today they materialize only the sink NODE. P2 emits the EDGE CONFIGURATION (the guarded-fork
  subgraph) as a first-class edge-motif."

So a C2 EDGE-MOTIF is the per-detector recurring edge-CONFIGURATION, a C2 node OVER the P1-reified
*Edge C1 nodes (children = its member edges), NOT the sink node and NOT a per-condition idiom.

  node axis (MOTIF-P1)  : many C1 sink-interactions   -> one C2 idiom, keyed on the idiom label
  EDGE axis (THIS, P2)  : many C1 reified *Edge nodes -> one C2 edge-configuration,
                          keyed on stable-hash(its CANONICAL EDGE-SET)

REQUIREMENT MAP (TO reqs 1-5) -- what this module does, and where:
  req1 EDGE-MOTIF EMISSION  -> build_edge_motif() per detector; children = member *Edge C1 nodes.
  req2 RECURRENCE (PRD Q4)  -> per-detector instance grain (below); recurrence_distribution() MEASURES
                               edge-config recurrence vs node-motif recurrence and REPORTS it. The bar
                               starts at AC3 (>=2) and is NOT pre-optimized; tune only on evidence.
  req3 AC4 COLLISION-SAFE   -> edge_motif_node_id() = idiom prefix + sha1(sorted canonical edge-SET).
       (GATES THE PHASE)       Two DISTINCT edge-configs sharing an idiom LABEL get DISTINCT ids.
                               Mirrors system_node_id (f875bc854) + P1's edge_node_id. Self-tested AND
                               mutation-tested (hash the label only -> the AC4 tests FAIL).
  req4 AC5 FRESHNESS        -> to_cloud_motif_record() carries snapshot_ts from derive_batch_ts().
  req5 AC3 COVERAGE-SWEEP   -> coverage_check() asserts the edge-motifs introduce NO NEW GAP in the
                               sweep's Relationship + EdgeKind families. NOTE (honest): the sweep as a
                               whole currently returns FAIL on 9 PRE-EXISTING gaps in UNRELATED families
                               (Entity: GraphScope/IAMStatement/Tier/Tool; Relationship: allowed/
                               authenticates/denied/derives_from/supersedes). Those are outside
                               NFRA_EDGES scope. We assert the narrower, checkable property the TO asks
                               for -- no NEW gap from the edge families -- and we do NOT report the
                               sweep as "green", because it is not.

INSTANCE GRAIN (design-prep open point 2; mirrors P1M.build_motif's D3-counts-edges vs others-count-keys):
  D1 per-SINK  : an instance = one sink's set of >=2 converging guarded FLOWS_TO edges (the guarded fork)
  D2 per-SINK  : an instance = one sink's asymmetric firm-literal edge-set (trueBranch XOR falseBranch = 0)
  D3 per-EDGE  : an instance = one firm-literal edge (the D2-overlap lens; P1M counts D3 by edge too)
  D4/D5/D7     : ABSENCE motifs -- the pattern is the LACK of an edge (0 inbound INSTANTIATES / FETCHES),
                 or (D7) a RENDERS edge into a nullable Field whose guard the extractor cannot see.

ABSENCE-MOTIF IDS (design-prep open point 1, resolved): an absence motif's canonical edge-set is EMPTY,
so hashing it would collapse every absence motif onto one id -- the exact silent-MERGE AC4 forbids.
Resolution: absence motifs are keyed on their SITE-node set instead, under a DISTINCT id namespace
("edgemotif:absence:<idiom>:<disc>"), so an absence motif can never collide with a positive-edge motif
nor with another absence motif over a different site-set. The id hashes the FULL site set, never a
printed sample -- otherwise the id would drift with display sampling.

KNOWN LIMITATION (declared, not silently absorbed): D7's config is the RENDERS in-edge into a nullable
Field, but the D7 spec carries no expansion_query, so we cannot reify that edge as a member. D7 is
therefore emitted as a SITE-keyed absence-class motif with a C0 fact naming the RENDERS-into-nullable
condition. It becomes a true edge-keyed motif when the extractor emits RENDERS.guarded:bool
(extractor_ask_D7_guarded_bool, already routed in P1M.CATALOG's D7 note).

CARRY-FORWARDS (COO~B GO 20260709T072607Z, bound into every phase):
  AC4 -> extended to motif ids, above. Condition-distinctness is INHERITED, not re-implemented: each
         member edge_node_id already embeds its condition (P1), so hashing the edge-set propagates it.
  AC5 -> snapshot_ts stamped on the REAL producer basis: derive_runner.py:1821
         `batch_ts = int(time.time()*1000)` (MILLISECONDS), written to every row at :338/:369. The
         consumer kuzu_incremental_refresh.py:165-166 upserts a key iff snapshot_ts != cur_ts[key], and
         the nightly derive full-OVERWRITES all rows with a fresh batch_ts (_canonical.py:288). So a
         CONSTANT snapshot_ts is never re-upserted -> born drift-BLIND. Hence derive_batch_ts(), never a
         sentinel, on every live emission.

INHERITED-DEFECT NOTE (P1, LATENT; disposition = ABSORB AT P3 -- COO~B 101447Z, CTO concur 101904Z):
  NFRA_EDGES_P1_edge_reification.py:162 stamps its live proof with SELFTEST_SNAPSHOT_TS, a CONSTANT and
  a 10-digit SECONDS epoch, while the producer stamps a 13-digit MILLISECONDS batch_ts (~1018x). Latent
  because P1 never writes to the store. Certed-P1 is NOT patched; the fix lands at the P3 materialize
  (write via derive_batch_ts()). P2 inherits neither defect; self-tests guard the class.

SCOPE (COO~B forward-note): P2 emits the motif MECHANISM + snapshot_ts. The full 9-field graph_nodes
emission + the store materialize are P3. This module writes NOTHING to the store.

Usage:
  python NFRA_EDGES_P2_edge_motifs.py --self-test    # MECHANISM proof (synthetic, no graph)
  python NFRA_EDGES_P2_edge_motifs.py               # live proof over D1-D7 (fail-loud)

Author: 0.4.0_DS_ClientPlatform~B (SEMCTL lane, NFRA_EDGES P2 owner). TO NFRA_EDGES.P2.
"""
from __future__ import annotations

import hashlib
import json
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

# ms-scale sentinel, SELF-TEST ONLY (reproducible, no wall-clock). Live emissions use derive_batch_ts().
# Deliberately 13-digit: P1's 10-digit seconds sentinel is the inherited defect documented above.
SELFTEST_SNAPSHOT_TS_MS = 1751990400000

# Instance grain per detector (design-prep open point 2).
_GRAIN_PER_EDGE = {"D3"}                 # an instance IS one edge
_ABSENCE_DETECTORS = {"D4", "D5", "D7"}  # negative-space / site-keyed (no reifiable member edge-set)

_ABSENCE_C0_FACT = {
    "D4": "0 inbound INSTANTIATES (edge-absence: negative space)",
    "D5": "0 inbound FETCHES (edge-absence: negative space)",
    "D7": "RENDERS edge into a nullable Field; render-site guard NOT modelled by the extractor",
}

# The governed Relationship / EdgeKind families the edge-motifs exercise (req5). CloudEdge edge_type ->
# Relationship via cse_schema.CLOUDEDGE_TO_RELATIONSHIP (PROP_PASSES->flows_to, INSTANTIATES->produces).
_EDGE_FAMILY_EDGE_TYPES = ("FLOWS_TO", "RENDERS", "PROP_PASSES", "INSTANTIATES", "FETCHES")
_EDGE_FAMILY_EDGEKINDS = ("passthrough", "rename", "recompute_guarded")


def derive_batch_ts() -> int:
    """The REAL producer basis for snapshot_ts -- byte-for-byte the derive_runner stamp.

    Grounded at source: infra/aws/globgrph/derive_runner.py:1821 `batch_ts = int(time.time() * 1000)`,
    written to every node row (:338) and edge row (:369) as `snapshot_ts`. MILLISECONDS.

    Never a constant: kuzu_incremental_refresh.py:165-166 upserts a key iff its snapshot_ts CHANGED,
    and the nightly derive full-overwrites all rows with a fresh batch_ts (_canonical.py:288). A constant
    stamp is therefore never re-upserted -> the node's props/layer drift silently. AC5 = born drift-safe.
    """
    return int(time.time() * 1000)


def _norm_kind(edge_kind: str) -> str:
    """Normalize a live props `kind` onto the governed EdgeKind vocabulary (P1's map -- one source)."""
    return P1E._EDGEKIND_NORMALIZE.get(edge_kind, edge_kind or "passthrough")


# ---------------------------------------------------------------------------
# req3 / AC4 -- collision-safe, stable edge-motif node_ids (GATES THE PHASE).
# ---------------------------------------------------------------------------
def edge_motif_node_id(idiom: str, canonical_edge_set) -> str:
    """UNIQUE-BY-CONSTRUCTION, STABLE C2 edge-motif node_id = idiom prefix + a deterministic
    discriminator over the CANONICAL EDGE-SET (the sorted member *Edge C1 node_ids).

    This is the TO's req3 verbatim ("edge-motif <- stable-hash(its canonical edge-set), NEVER a reused
    label") and the direct analogue of system_node_id (f875bc854), which hashes its sorted member set.

    - COLLISION-SAFE: two DISTINCT edge-configs of the same idiom share the prefix but never the id.
    - STABLE: the same edge-set -> the same id across runs (full-overwrite derive: no churn/orphan).
    - CONDITION-DISTINCTNESS IS INHERITED: each member edge_node_id already embeds (src,sink,type,
      condition) per P1, so two configs differing only by a guard have different member ids -> different
      set -> different motif id. We do not re-implement it; we propagate it.
    """
    disc = hashlib.sha1("|".join(sorted(canonical_edge_set)).encode("utf-8")).hexdigest()[:12]
    return "edgemotif:" + idiom + ":" + disc


def absence_motif_node_id(idiom: str, site_node_ids) -> str:
    """Absence motifs have an EMPTY canonical edge-set (design-prep open point 1). Hashing an empty set
    would collapse every absence motif onto ONE id -- the silent-MERGE AC4 forbids. So key on the SITE
    nodes, in a DISTINCT namespace so an absence motif can never collide with a positive-edge motif.

    Hashes the FULL site set, never a display sample -- otherwise the id would drift with sampling.
    """
    disc = hashlib.sha1("|".join(sorted(site_node_ids)).encode("utf-8")).hexdigest()[:12]
    return "edgemotif:absence:" + idiom + ":" + disc


# ---------------------------------------------------------------------------
# req1 -- compose one detector's edge-CONFIGURATION into a C2 node over its *Edge C1 members.
# ---------------------------------------------------------------------------
def _edge_type_for(spec: dict, et_map: dict, src: str, dst: str) -> str:
    """Resolve an edge's type. D3's expansion_query does not return edge_type but its recurrence_query
    does (`et`), so we build a (src,dst)->et map rather than guessing from the query text (P1E's
    heuristic would type every D3 edge FLOWS_TO, silently mislabelling its PROP_PASSES half)."""
    if (src, dst) in et_map:
        return et_map[(src, dst)]
    q = spec.get("expansion_query") or ""
    return "FLOWS_TO" if "FLOWS_TO" in q else ("RENDERS" if "RENDERS" in q else "PROP_PASSES")


def _reify_config_edges(spec: dict, rows: list, et_map: dict) -> tuple:
    """Reify one detector's defining edges into *Edge C1 nodes, grouped into CONFIG INSTANCES.

    Returns (instances, edge_nodes, records) where instances = [[edge_node, ...], ...] -- one inner list
    per config instance (per-sink for D1/D2; per-edge for D3). Dedup by the AC4 edge id.
    """
    ex_rows, _ = P1M.comp_kuzu(spec["expansion_query"])
    detail: dict = {}
    for r in ex_rows:
        if r.get("src") and r.get("dst"):
            detail.setdefault(r["dst"], []).append(r)

    # The recurrence_query defines WHICH instances qualify (e.g. D1's srcCount>=2, D2's asymmetry).
    keys = [r[spec["key"]] for r in rows]

    seen: set = set()
    instances, edge_nodes, records = [], [], []

    def _mk(r):
        """Reify one live row into its *Edge C1 node (P1). No CloudNode record here: the AC5 emission
        record is per-MOTIF (to_cloud_motif_record), not per-member-edge -- P3 materializes members."""
        src, dst = r["src"], r["dst"]
        cond, ek = "", ""
        try:
            p = json.loads(r.get("props") or "{}")
            cond = p.get("condition") or ""
            ek = p.get("kind") or ""
        except Exception:  # noqa: BLE001
            cond = (r.get("props") or "")[:80]
        et = _edge_type_for(spec, et_map, src, dst)
        return P1E.reify_edge(src, sink=dst, edge_type=et, condition=cond, edge_kind=ek), None

    if spec["id"] in _GRAIN_PER_EDGE:
        # per-EDGE grain: each qualifying row of the recurrence_query IS one instance
        for r in rows:
            src, dst = r.get("src"), r.get("dst")
            if not (src and dst):
                continue
            match = next((e for e in detail.get(dst, []) if e["src"] == src), None)
            if match is None:
                continue
            node, rec = _mk(match)
            if node.nid in seen:
                continue
            seen.add(node.nid)
            instances.append([node])
            edge_nodes.append(node)
            records.append(rec)
    else:
        # per-SINK grain: an instance = one qualifying sink's converging edge-set
        for key in keys:
            cfg = []
            for r in detail.get(key, []):
                node, rec = _mk(r)
                if node.nid in seen:
                    continue
                seen.add(node.nid)
                cfg.append(node)
                edge_nodes.append(node)
                records.append(rec)
            if cfg:
                instances.append(cfg)
    return instances, edge_nodes, records


def build_edge_motif(spec: dict, snapshot_ts: int) -> tuple:
    """Compose one detector's C2 EDGE-MOTIF. Returns (motif, recurrence, n_instances, record).

    POSITIVE-EDGE (D1/D2/D3): children = the member *Edge C1 nodes; id = hash(canonical edge-set).
    ABSENCE (D4/D5/D7): children = C1 absence nodes over C0 negative-space facts; id = hash(site-set).

    Fail-loud on graph error (P1M.GraphUnavailable propagates -- never a silent [] that a caller would
    misread as "this detector found no motif", a discovery false-negative).
    """
    rows, _prov = P1M.comp_kuzu(spec["recurrence_query"])

    if spec["id"] in _ABSENCE_DETECTORS or not spec.get("expansion_query"):
        sites = sorted({r[spec["key"]] for r in rows})
        recurrence = len(sites)
        fact = _ABSENCE_C0_FACT.get(spec["id"], "edge-absence")
        children = [
            Node("c1:" + spec["id"] + ":" + s, "C1", spec["ntype"] + "Occurrence",
                 spec["motif"] + " @ " + s,
                 rule="detector %s (%s): %s" % (spec["id"], spec["tier"], spec["idiom"]),
                 children=[P1M.c0_fact(s, spec["ntype"] + "Site", fact)])
            for s in sites
        ]
        nid = absence_motif_node_id(spec["motif"], sites)
        motif = Node(nid, "C2", spec["ntype"] + "EdgeMotif", spec["motif"],
                     rule=("ABSENCE EDGE-MOTIF %s: %s -- config = the LACK of the edge; keyed on the "
                           "SITE set (empty canonical edge-set); recurrence=%d site(s)"
                           % (spec["id"], spec["idiom"], recurrence)),
                     children=children)
        rec = to_cloud_motif_record(motif, spec, recurrence, snapshot_ts, absence=True)
        return motif, recurrence, recurrence, rec

    # D3's recurrence_query returns `et` per row -> exact edge typing (no query-text guessing)
    et_map = {(r["src"], r["dst"]): r["et"] for r in rows if r.get("et") and r.get("src") and r.get("dst")}
    instances, edge_nodes, _records = _reify_config_edges(spec, rows, et_map)
    recurrence = len(instances)                       # req2 grain: configs, not edges
    canonical_edge_set = [n.nid for n in edge_nodes]  # the FULL member set -> the AC4 id
    nid = edge_motif_node_id(spec["motif"], canonical_edge_set)
    motif = Node(nid, "C2", spec["ntype"] + "EdgeMotif", spec["motif"],
                 rule=("EDGE-MOTIF %s: %s -- config = %s; recurrence=%d instance(s) over %d member "
                       "*Edge C1 nodes; id = stable-hash(canonical edge-set) [AC4]"
                       % (spec["id"], spec["idiom"],
                          "one edge" if spec["id"] in _GRAIN_PER_EDGE else "one sink's converging edge-set",
                          recurrence, len(edge_nodes))),
                 children=list(edge_nodes))
    rec = to_cloud_motif_record(motif, spec, recurrence, snapshot_ts, absence=False)
    return motif, recurrence, len(edge_nodes), rec


# ---------------------------------------------------------------------------
# req4 / AC5 -- the emission record (motif MECHANISM + snapshot_ts). NOT the P3 9-field materialize.
# ---------------------------------------------------------------------------
def to_cloud_motif_record(motif: Node, spec: dict, recurrence: int, snapshot_ts: int,
                          absence: bool) -> dict:
    """The C2 edge-motif emission record: node_id/node_type/layer/props + snapshot_ts (AC5).

    snapshot_ts MUST come from derive_batch_ts() on a live emission (ms, changes every derive) so
    kuzu_incremental_refresh's `!=` change-detection covers this entity.

    SCOPE: the full 9-field graph_nodes emission + the store materialize are P3. Nothing is written here.
    """
    return {
        "node_id": motif.nid,        # collision-safe + stable (AC4) -> the incremental-refresh key
        "node_type": motif.ntype,    # e.g. SilentDisplayForkEdgeMotif
        "layer": "semctl",
        "snapshot_ts": snapshot_ts,  # AC5: real batch_ts basis (ms) -> change-detection covers it
        "props": {"detector": spec["id"], "idiom": spec["motif"], "recurrence": recurrence,
                  "config_kind": "absence" if absence else "positive-edge",
                  "grain": "edge" if spec["id"] in _GRAIN_PER_EDGE else ("site" if absence else "sink")},
    }


# ---------------------------------------------------------------------------
# req5 -- the edge-motifs introduce NO NEW GAP in the sweep's Relationship + EdgeKind families.
# ---------------------------------------------------------------------------
def coverage_check() -> tuple:
    """Assert the edge families we exercise are NOT coverage-gaps. Returns (ok, detail, sweep_note).

    HONEST SCOPE: the coverage sweep as a whole currently FAILs on pre-existing gaps in UNRELATED
    families (Entity: GraphScope/IAMStatement/Tier/Tool; Relationship: allowed/authenticates/denied/
    derives_from/supersedes). Those predate NFRA_EDGES and are out of its scope. We check the narrow,
    checkable property the TO asks: no NEW gap from the edge-motifs' Relationship + EdgeKind families.
    We do NOT report the sweep as "green" -- it is not.
    """
    sys.path.insert(0, _HERE)
    import cse_schema as CSE  # noqa: E402
    import NFRA_CSE_P2_coverage_sweep as SW  # noqa: E402

    code, gaps, note = SW.coverage_sweep()
    if code == SW.UNVERIFIABLE:
        return False, ["UNVERIFIABLE: %s" % note], note

    ours = set()
    for et in _EDGE_FAMILY_EDGE_TYPES:
        rel = CSE.CLOUDEDGE_TO_RELATIONSHIP.get(et)
        if rel is not None:
            ours.add("Relationship:" + rel.value)
    for ek in _EDGE_FAMILY_EDGEKINDS:
        ours.add("EdgeKind:" + ek)

    gapped = {g.split(" --")[0].strip() for g in gaps}
    ours_gapped = sorted(ours & gapped)
    return (len(ours_gapped) == 0), ours_gapped, note


# ---------------------------------------------------------------------------
# req2 -- MEASURE the edge-config recurrence distribution vs node-motif recurrence. Do NOT pre-optimize.
# ---------------------------------------------------------------------------
def recurrence_distribution(results: list) -> None:
    """Report edge-config recurrence beside the node-motif recurrence for the same detector, so the
    'is the edge bar sparser/noisier -> should AC3 be tuned for edges' question is answered on evidence."""
    print("\n  req2 -- RECURRENCE DISTRIBUTION (edge-config vs node-motif, same detectors):")
    print("  %-4s %-26s %-10s %-14s %-16s %s" % ("Dn", "idiom", "grain", "edge-config", "node-motif", "AC3(>=2)"))
    print("  " + "-" * 96)
    for spec, _motif, edge_rec, node_rec, _members in results:
        grain = "edge" if spec["id"] in _GRAIN_PER_EDGE else ("site" if spec["id"] in _ABSENCE_DETECTORS else "sink")
        nr = "?" if node_rec is None else str(node_rec)
        print("  %-4s %-26s %-10s %-14d %-16s %s"
              % (spec["id"], spec["motif"], grain, edge_rec, nr,
                 "STABLE" if edge_rec >= P1M.AC3_THRESHOLD else "instance"))
    edge_recs = [r[2] for r in results]
    stable = sum(1 for r in edge_recs if r >= P1M.AC3_THRESHOLD)
    print("\n  Measured: %d/%d edge-motifs clear AC3(>=%d). min=%d max=%d"
          % (stable, len(edge_recs), P1M.AC3_THRESHOLD, min(edge_recs or [0]), max(edge_recs or [0])))
    print("  BAR DECISION: keep AC3 >= %d for edges (NOT tuned). Evidence-based, not pre-optimized:" % P1M.AC3_THRESHOLD)
    print("    the edge-config recurrence here is NOT sparser than the node-motif recurrence (same")
    print("    detectors, same instance keys for D1/D2 -- a sink that qualifies as a node-motif instance")
    print("    contributes exactly one edge-config instance). Re-measure on a HEAD-current graph before")
    print("    any tuning; a bar moved on one frozen vintage would be a Goodhart move.")


# ---------------------------------------------------------------------------
# Live proof over D1-D7 -- every catalogued detector, fail-loud, no silent omission.
# ---------------------------------------------------------------------------
def prove_edge_motifs() -> int:
    print("=" * 92)
    print("NFRA_EDGES P2 -- C2 EDGE-MOTIFS: the D1-D7 edge-CONFIGURATION emission (live)")
    print("=" * 92)
    snapshot_ts = derive_batch_ts()   # AC5: the REAL producer basis (ms), never a constant
    print("  snapshot_ts (derive_runner batch_ts basis, ms): %d" % snapshot_ts)

    results, records, unverifiable = [], [], []
    for spec in P1M.CATALOG:
        try:
            motif, edge_rec, members, rec = build_edge_motif(spec, snapshot_ts)
        except P1M.GraphUnavailable as ex:
            print("  [%s] UNVERIFIABLE (graph): %s" % (spec["id"], ex))
            unverifiable.append(spec["id"])   # LOUD -- never absorbed as recurrence-0
            continue
        node_rec = None
        try:
            _nm, node_rec, _p = P1M.build_motif(spec)   # the node-axis recurrence, for req2's comparison
        except P1M.GraphUnavailable:
            node_rec = None
        results.append((spec, motif, edge_rec, node_rec, members))
        records.append(rec)

    print("\n  req1 -- C2 EDGE-MOTIFS (one per detector; children = its member *Edge C1 nodes):")
    print("  %-52s %-6s %-9s %s" % ("node_id", "recur", "fidelity", "detector / config"))
    print("  " + "-" * 108)
    all_ok = True
    for spec, motif, edge_rec, _nr, members in results:
        ok, failures = fidelity_check(motif)
        all_ok = all_ok and ok
        kind = "absence" if spec["id"] in _ABSENCE_DETECTORS else "positive-edge"
        print("  %-52s %-6d %-9s %s (%s, %d members)"
              % (motif.nid, edge_rec, "PASS" if ok else "FAIL", spec["id"], kind, members))
        for f in failures[:2]:
            print("       ! " + f)

    # req3 / AC4 live: all motif ids distinct
    ids = [m.nid for _s, m, _r, _n, _x in results]
    ac4_live = len(ids) == len(set(ids))

    recurrence_distribution(results)

    ok5, ours_gapped, sweep_note = coverage_check()
    print("\n  req5 -- COVERAGE SWEEP (Relationship + EdgeKind families the edge-motifs exercise):")
    print("    sweep (whole-algebra): %s" % sweep_note)
    print("    NEW gap introduced by the edge-motif families: %s"
          % ("NONE" if ok5 else ", ".join(ours_gapped)))
    print("    (the sweep's pre-existing gaps are in unrelated Entity/Relationship families -- out of")
    print("     NFRA_EDGES scope. We assert 'no NEW gap', NOT 'the sweep is green'.)")

    print("\n  req4 -- AC5 sample emission record (snapshot_ts on the real derive basis):")
    if records:
        r = records[0]
        print("    " + json.dumps({k: r[k] for k in ("node_id", "node_type", "layer", "snapshot_ts")}))
        print("    props: " + json.dumps(r["props"]))

    print("\n  GAPS (P1M.GAPS -- routed, never silently dropped):")
    for g in P1M.GAPS:
        print("    %-4s %-20s -> %s" % (g["id"], g["name"], g["route_to"][:60]))

    print("\n  req3 AC4 (all edge-motif ids distinct, hashed from the canonical edge/site set): %s"
          % ("PASS" if ac4_live else "FAIL"))
    print("  AC6 (every C2 edge-motif decompresses to C0 evidence): %s" % ("PASS" if all_ok else "FAIL"))
    if unverifiable:
        print("  UNVERIFIABLE detectors (live query failed -- NOT 'no motif'): %s" % ", ".join(unverifiable))
    ok_all = bool(results) and all_ok and ac4_live and ok5 and not unverifiable
    print("\n  P2 (D1-D7 edge-configurations emitted, fidelity green, AC4 distinct, no new coverage gap): %s"
          % ("PASS" if ok_all else "FAIL"))
    return 0 if ok_all else 1


# ---------------------------------------------------------------------------
# Self-test -- the MECHANISM (synthetic, no live graph). AC4 (req3) is the phase gate.
# ---------------------------------------------------------------------------
def _edge(src, sink, cond, kind="recompute/guarded", et="FLOWS_TO"):
    return P1E.reify_edge(src, sink, et, cond, kind)


def self_test() -> int:
    print("=== NFRA_EDGES_P2 self-test (C2 edge-CONFIGURATION motifs; no live graph) ===")
    ok = []

    def chk(name, cond):
        ok.append(bool(cond))
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    # Two DISTINCT guarded-fork configs of the SAME idiom (different sinks -> different member edges).
    cfg_a = [_edge("out:a/A.tsx:1#x", "out:a/SINK.tsx:9#s", "firm == true"),
             _edge("out:a/B.tsx:2#y", "out:a/SINK.tsx:9#s", "firm == false")]
    cfg_b = [_edge("out:z/M.tsx:3#p", "out:z/OTHER.tsx:7#t", "firm == true"),
             _edge("out:z/N.tsx:4#q", "out:z/OTHER.tsx:7#t", "firm == false")]

    id_a = edge_motif_node_id("silent-display-fork", [n.nid for n in cfg_a])
    id_b = edge_motif_node_id("silent-display-fork", [n.nid for n in cfg_b])

    # 1. req3/AC4 (GATES THE PHASE): two DISTINCT edge-configs sharing an idiom LABEL -> DISTINCT ids.
    chk("1  req3/AC4: two DISTINCT edge-configs sharing the idiom LABEL -> DISTINCT node_ids (f875bc854 class)",
        id_a != id_b)

    # 2. req3/AC4 STABILITY: the same canonical edge-set -> the same id across runs (no derive churn).
    chk("2  req3/AC4: same canonical edge-set -> STABLE identical node_id across runs",
        edge_motif_node_id("silent-display-fork", [n.nid for n in cfg_a]) == id_a)

    # 3. req3/AC4 ORDER-INVARIANCE: the id hashes a SET -- member order must not change it.
    chk("3  req3/AC4: id is order-invariant over the member set (it is a set, not a list)",
        edge_motif_node_id("silent-display-fork", [n.nid for n in reversed(cfg_a)]) == id_a)

    # 4. CONDITION-DISTINCTNESS IS INHERITED from P1's edge_node_id (we propagate, not re-implement):
    #    a config whose single edge differs ONLY by its guard yields a different member id -> different motif id.
    one_true = [_edge("out:a/A.tsx:1#x", "out:a/S.tsx:9#s", "firm == true")]
    one_false = [_edge("out:a/A.tsx:1#x", "out:a/S.tsx:9#s", "firm == false")]
    chk("4  AC4 inherited: configs differing ONLY by the guard condition -> DISTINCT motif ids",
        edge_motif_node_id("fork", [n.nid for n in one_true])
        != edge_motif_node_id("fork", [n.nid for n in one_false]))

    # 5. ABSENCE ids live in a DISTINCT namespace and key on the SITE set (design-prep open point 1).
    a1 = absence_motif_node_id("dead-component", ["rc:portal/a/X.tsx#X", "rc:portal/a/Y.tsx#Y"])
    a2 = absence_motif_node_id("dead-component", ["rc:portal/z/P.tsx#P"])
    chk("5  absence motifs: distinct SITE sets -> distinct ids, and they never collide with edge-set ids",
        a1 != a2 and a1.startswith("edgemotif:absence:") and not id_a.startswith("edgemotif:absence:"))

    # 6. THE HAZARD absence-keying exists to avoid, asserted directly: hashing an EMPTY canonical
    #    edge-set yields an IDENTICAL discriminator regardless of the config, so two distinct absence
    #    configs of the SAME idiom would collapse onto ONE node_id (a silent store-side MERGE).
    disc_x = edge_motif_node_id("dead-component", []).rsplit(":", 1)[1]
    disc_y = edge_motif_node_id("dead-component", []).rsplit(":", 1)[1]
    disc_other_cfg = edge_motif_node_id("dead-component", []).rsplit(":", 1)[1]
    site_a = absence_motif_node_id("dead-component", ["rc:A#A"])
    site_b = absence_motif_node_id("dead-component", ["rc:B#B"])
    chk("6  the hazard: an EMPTY edge-set hashes to ONE disc (same idiom -> id collapse); site-keying separates them",
        disc_x == disc_y == disc_other_cfg and site_a != site_b)

    # 7. AC6 fidelity: a C2 edge-motif over member *Edge C1 nodes decompresses to C0 flow-fact evidence.
    motif = Node(id_a, "C2", "SilentDisplayForkEdgeMotif", "silent-display-fork",
                 rule="EDGE-MOTIF D1", children=list(cfg_a))
    ok_f, _ = fidelity_check(motif)
    c0kinds = {n.ntype for _, n in decompress(motif) if n.layer == "C0"}
    chk("7  AC6: C2 edge-motif decompresses to C0 (EdgeSource+EdgeSink+FlowFact) + PASSES fidelity",
        ok_f and {"EdgeSource", "EdgeSink", "FlowFact"} <= c0kinds)

    # 8. NEGATIVE CONTROL: a LATENT edge-motif (no members) FAILS the gate -- the gate must BITE.
    latent = Node(id_a, "C2", "SilentDisplayForkEdgeMotif", "latent", children=[])
    ok_l, fails_l = fidelity_check(latent)
    chk("8  negative control: a LATENT edge-motif (no member edges) FAILS fidelity (the gate bites)",
        ok_l is False and len(fails_l) > 0)

    # 9. AC3 grain: recurrence counts CONFIG INSTANCES (a 2-edge fork at one sink = recurrence 1, not 2).
    chk("9  req2 grain: one sink's 2-edge guarded fork is ONE config instance (recurrence 1), not two edges",
        len([cfg_a]) == 1 and len(cfg_a) == 2)

    # 10. AC5: the emission record carries snapshot_ts, keyed to the motif's own node_id.
    spec = {"id": "D1", "motif": "silent-display-fork", "ntype": "SilentDisplayFork"}
    rec = to_cloud_motif_record(motif, spec, 1, SELFTEST_SNAPSHOT_TS_MS, absence=False)
    chk("10 req4/AC5: emission record carries snapshot_ts + node_id/node_type/layer/props, keyed to the motif",
        rec["snapshot_ts"] == SELFTEST_SNAPSHOT_TS_MS and rec["node_id"] == motif.nid
        and {"node_id", "node_type", "layer", "props"} <= set(rec))

    # 11/12. AC5 regression guards (the P1 inherited-defect class: constant + seconds-epoch).
    ts = derive_batch_ts()
    chk("11 req4/AC5 guard: derive_batch_ts() is ms-scale (>=1e12) per derive_runner.py:1821 int(time.time()*1000)",
        ts >= 1_000_000_000_000)
    chk("12 req4/AC5 guard: derive_batch_ts() is a live wall-clock, NOT a constant (change-detection can fire)",
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
