#!/usr/bin/env python3
"""NFRA_CSE.P2 req#2 (EXTENSION) -- FULL-GRAPH AC4 structural round-trip parity.

Extends the single-recognizer round-trip (NFRA_CSE_P2_ac4_lambda_writes_s3.py, the LAMBDA-WRITES_S3
slice, 12/12) to the WHOLE live CloudNode/CloudEdge graph. The round-trip, at estate scale:

    live graph  --recognize-->  fail-closed-validated CSE (GRAPH_HEAD producer)  --materialize-->  C1
                                                                                          |
                                            structural-diff vs the SAME live graph  <-----+

Parity PASS = the CSE algebra + LAW-2 mandatory-provenance REPRODUCE the current graph, node-for-node
and edge-for-edge (modulo NAMED coverage-gaps, which are legitimate MOTIF/PROMOTE candidates, never a
silent skip -- LAW 1). This is AC4: "CSE-to-C1 reproduces the live CloudNode/CloudEdge graph."

THE THESIS THIS PROVES AT ESTATE SCALE (comp_ladder's core claim, over 19.9k nodes / 34.9k edges):
the algebra is a LOSSY compression (many concrete edge_types -> one governed Relationship:
READS_S3 + READS_FIELD + READS_SECRET all -> READS; and many node_types -> one Entity), but the
MANDATORY provenance (LAW 2) makes the CSE representation LOSSLESS -- every concrete node_type /
edge_type decompresses back OUT of provenance.evidence, so re-materializing reconstructs the concrete
graph EXACTLY. A representation that DROPPED provenance (an embedding / latent vector) could not
round-trip -- which is precisely WHY the contract makes provenance mandatory + fail-closed. So this
module is not a tautology: its teeth are that every one of ~55k live nodes/edges must produce a CSE
that (a) classifies into the CLOSED algebra (fail-closed on any gap), (b) PASSES the full validator
(off-enum reject, provenance-evidence mandatory, confidence float, AC6 marker_head, S3.6 fidelity),
and (c) decompresses back to its exact concrete (nid, node_type) / (src, edge_type, dst). Any node or
edge the algebra CANNOT carry losslessly falls out as missing_in_reconstructed -- a real AC4 finding.

GROUNDING (Rule 22): the "reality" side is the LIVE graph pulled via kuzu_cli.py --json (the canonical
auto-refreshing surface -- query, never rebuild; CLAUDE.md Rule 20/21). Both the node-export and the
edge-export are read from ONE frozen vintage (snapshot-id consistency-guarded), and that snapshot-id
is pinned as head.marker_head on every emitted CSE (AC6 / one-marker-commit) -- so the round-trip
tests the MATERIALIZER's fidelity, not freshness. UNIFY-NOT-BUILD: all mapping + the validator come
from cse_schema (the CVO-certed P1 contract); nothing here re-authors algebra.

CTO ruling lineage (1.0.0_SA_CTO 130926Z on the 122951Z Q1-grounded RAVC): reality-to-reality, no
translation layer -- ARN-native LAMBDA nids + already-live edge_types. The single-recognizer slice
proved the discipline on 6 edges (+ the bd-client-detail EXTRA_IN_LIVE catch); this generalizes it to
the full graph. Design RAVC'd CTO 121122Z (TO req#6).

Author: 0.4.0_DS_ClientPlatform~B   TO: NFRA_CSE.P2 req#2   Date: 2026-07-07
Status: DRAFT (recognizer + materializer + live full-graph diff; --self-test deterministic/offline).
For CVO exercise-cert -> COO SoD-land canonical (org/modules/graph/, exec-lane), mirroring the P1/
coverage-sweep path. Pairs with 0.5.0_AE_OpalETL: the same CSE shape their C0 store-writer emits.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

# UNIFY-NOT-BUILD: the canonical algebra + fail-closed validator (P1, CVO-certed). Path-robust so this
# draft runs from the DS deliverables lane; a plain sibling import at the canonical home.
_GRAPH_MOD = os.path.join(os.path.dirname(__file__), "..", "..", "..", "modules", "graph")
if os.path.isdir(_GRAPH_MOD):
    sys.path.insert(0, os.path.abspath(_GRAPH_MOD))
import cse_schema as CSE  # noqa: E402

WS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
KUZU_CLI = os.path.join(WS, "infra", "aws", "globgrph", "kuzu_cli.py")
COMP_KUZU = os.path.join(WS, ".tools", "comp-kuzu")


class LivePullError(Exception):
    """A live graph export FAILED. Raised LOUD (never a silent partial/stale round-trip) -- the same
    honest-missing-never-silent-default discipline the P1 --live pull enforces."""


# ===========================================================================
# LIVE EXPORT -- the CANONICAL comp-kuzu surface (CLAUDE.md Rule 20/21: query, never rebuild; it
# auto-refreshes to Nessie HEAD on the marker-oracle). RAIL-PREFERRED path = the `bash .tools/comp-kuzu`
# wrapper; ROBUST fallback = kuzu_cli.py (comp-kuzu's own 3-line-wrapped implementation) invoked via
# sys.executable -- the SAME try-wrapper-then-cli pattern the canonical P1 module (cse_schema._pull_
# live_types) uses, because a bare `bash` on this Windows box can resolve to WSL bash and 500 on
# execvpe. Both hit the identical persisted Kuzu DB with identical auto-refresh + provenance header;
# kuzu_cli.py prints JSON to stdout (line 81) + the provenance header (snapshot-id) to stderr (line 53),
# the wrapper prepends a provenance preamble on stdout -- so we slice JSON from the first '[' and scan
# BOTH streams for the marker (robust across either path). (Manifest advisory C_adhoc_reimplementation
# on the inline Cypher is satisfied by routing through comp-kuzu first; the strings ARE the canonical
# CloudNode/CloudEdge query, the AC4 ground-truth, not an ad-hoc reimplementation of a comp-tool.)
# ===========================================================================
_NODE_Q = "MATCH (n:CloudNode) RETURN n.node_id AS nid, n.node_type AS nt"
_EDGE_Q = ("MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) "
           "RETURN a.node_id AS s, a.node_type AS snt, e.edge_type AS et, b.node_id AS d, b.node_type AS dnt")
_ALL_EDGE_COUNT_Q = "MATCH ()-[e:CloudEdge]->() RETURN count(e) AS c"
_SNAP_RE = re.compile(r"nodes snapshot-id:\s*(\S+)")


def _kuzu_json(query: str, timeout: int = 300) -> tuple:
    """Query the canonical comp-kuzu surface; return (rows, provenance_text). Tries the rail-preferred
    `bash comp-kuzu` wrapper first, falls back to kuzu_cli.py direct (Windows-spawn robust)."""
    cmds = []
    if os.path.isfile(COMP_KUZU):
        cmds.append(["bash", COMP_KUZU, "--json", query])
    cmds.append([sys.executable, KUZU_CLI, "--json", query])
    last = None
    for cmd in cmds:
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=WS, timeout=timeout)
        except Exception as ex:  # noqa: BLE001 -- try the next transport (e.g. WSL-bash execvpe)
            last = f"{cmd[0]} invocation failed: {ex}"
            continue
        i = proc.stdout.find("[")
        if proc.returncode == 0 and i >= 0:
            try:
                rows = json.loads(proc.stdout[i:])
            except Exception as ex:  # noqa: BLE001
                last = f"json parse failed via {cmd[0]}: {ex}"
                continue
            return rows, (proc.stdout[:i] + "\n" + proc.stderr)   # scan BOTH for the marker
        last = f"{cmd[0]} rc={proc.returncode}: {(proc.stderr or proc.stdout)[-500:]!r}"
    raise LivePullError(f"comp-kuzu/kuzu_cli export failed (all transports): {last}")


def _marker_from(provenance_text: str) -> str:
    m = _SNAP_RE.search(provenance_text or "")
    return m.group(1) if m else ""


def export_graph() -> tuple:
    """Pull the full live CloudNode/CloudEdge graph + the AC6 marker. Returns
    (nodes[(nid,nt)], edges[(s,snt,et,d,dnt)], marker, all_cloudedge_count). Fail-closed."""
    nrows, nprov = _kuzu_json(_NODE_Q)
    marker = _marker_from(nprov)
    if not marker:
        raise LivePullError("no 'nodes snapshot-id' in kuzu provenance header -- refusing an unpinned "
                            "AC6 marker_head (honest-missing, never a fabricated marker)")
    erows, eprov = _kuzu_json(_EDGE_Q)
    emarker = _marker_from(eprov)
    if emarker and emarker != marker:
        raise LivePullError(f"vintage skew: node export snapshot {marker} != edge export snapshot "
                            f"{emarker} -- refusing an inconsistent round-trip (surface refreshed mid-run)")
    crows, _ = _kuzu_json(_ALL_EDGE_COUNT_Q)
    all_edge_count = int(crows[0]["c"]) if crows else None
    nodes = [(r.get("nid"), r.get("nt")) for r in nrows]
    edges = [(r.get("s"), r.get("snt"), r.get("et"), r.get("d"), r.get("dnt")) for r in erows]
    return nodes, edges, marker, all_edge_count


# ===========================================================================
# RECOGNIZE (live node/edge -> fail-closed-validated CSE) + MATERIALIZE (CSE -> concrete node/edge).
# Reconstruction reads ONLY the CSE's own fields (subject.ref, edges[].target.ref, provenance.evidence)
# -- no side-channel -- so a node/edge round-trips iff its CSE actually carries enough to rebuild it.
# The concrete type lives in provenance.evidence: THAT is the lossless decompression the algebra's
# many-to-one compression relies on (LAW 2). It is mandatory + validated, so it cannot be silently
# dropped.
# ===========================================================================
_NODE_EV_RE = re.compile(r"node_type=(\S+)")
_EDGE_EV_RE = re.compile(r"edge_type=([^;]+);")


def _mk_cse(*, subject: CSE.EntityRef, edges: list, marker: str, evidence: str, locus: str,
            recognizer: str, artifact_class: str, confidence: float = 1.0) -> CSE.CSE:
    return CSE.CSE(
        event_id=f"gh:{artifact_class}:{locus}",
        schema_version=CSE.SCHEMA_VERSION,
        producer={"kind": CSE.ProducerKind.GRAPH_HEAD.value, "ref": marker},
        compiler={"id": "ac4_fullgraph_roundtrip", "artifact_class": artifact_class,
                  "version": CSE.SCHEMA_VERSION},
        transformation={"verb": CSE.Transformation.CREATE.value, "subject": subject, "edges": edges},
        provenance=CSE.Provenance(source=f"kuzu_nessie_db@{marker}", locus=locus,
                                  recognizer=recognizer, evidence=evidence),
        execution_meta={"timestamp": "", "actor": "ac4_fullgraph_parity", "run_id": marker},
        head={"marker_head": marker},
        qualifiers={CSE.Qualifier.CONFIDENCE.value: confidence},
    )


def _conf_for(ent, concept_conf: float) -> float:
    """node_type -> Entity is a deterministic TOTAL lexical map (not inferred) => HIGH (1.0) confidence,
    the HONEST value for a graph-derived node. EXCEPT Entity.CONCEPT, whose S3.5 rule requires low: this
    is the KNOWN algebra collision the full-graph round-trip surfaces (TypeDecl/symbol nodes are
    lexically-CERTAIN yet map to the honest-degrade Entity). `concept_conf` lets the diagnostic mode
    isolate the mechanism; production honest value stays 1.0 (which correctly REJECTS -> the finding)."""
    return concept_conf if ent == CSE.Entity.CONCEPT else 1.0


def recognize_node(nid, nt, marker: str, concept_conf: float = 1.0) -> tuple:
    """(cse, None) on success; (None, gap) on a coverage-gap / validation failure."""
    ent = CSE.map_cloudnode(nid, nt)
    if ent is None:
        return None, ("node", str(nid), str(nt), "no Entity mapping (node_type + nid-prefix both unmapped)")
    cse = _mk_cse(subject=CSE.EntityRef(ent.value, str(nid)), edges=[], marker=marker,
                  evidence=f"node_type={nt}", locus=str(nid),
                  recognizer="cloudnode_graph_recognizer", artifact_class="cloudnode",
                  confidence=_conf_for(ent, concept_conf))
    ok, errs = CSE.validate(cse)
    if not ok:
        return None, ("node", str(nid), str(nt), "CSE validation FAIL: " + "; ".join(errs))
    return cse, None


def materialize_node(cse: CSE.CSE) -> tuple:
    nid = cse.transformation["subject"].ref
    m = _NODE_EV_RE.search(cse.provenance.evidence)
    return (str(nid), m.group(1) if m else None)


def recognize_edge(s, snt, et, d, dnt, marker: str, concept_conf: float = 1.0) -> tuple:
    src_ent = CSE.map_cloudnode(s, snt)
    dst_ent = CSE.map_cloudnode(d, dnt)
    rel = CSE.map_cloudedge(et, dnt)   # 0.5: the sanctioned edge resolver -- target-typed for OWNED_BY
    #                                    (custody->OWNS via MS_USER / containment-inverse->CONTAINS via S3_BUCKET),
    #                                    matching the graph-head emitter. Was a flat CLOUDEDGE_TO_RELATIONSHIP.get(et)
    #                                    which mis-classified the 232 S3Key OWNED_BY edges. dnt = dst node_type.
    reasons = []
    if src_ent is None:
        reasons.append(f"src node unmapped (node_type={snt})")
    if dst_ent is None:
        reasons.append(f"dst node unmapped (node_type={dnt})")
    if rel is None:
        reasons.append(f"edge_type {et!r} unmapped")
    if reasons:
        return None, ("edge", (str(s), str(et), str(d)), str(et), "; ".join(reasons))
    cse = _mk_cse(
        subject=CSE.EntityRef(src_ent.value, str(s)),
        edges=[CSE.RelationshipDelta(rel.value, CSE.EntityRef(dst_ent.value, str(d)))],
        marker=marker, evidence=f"edge_type={et}; {s} -> {d}", locus=f"{s}->{d}",
        recognizer="cloudedge_graph_recognizer", artifact_class="cloudedge",
        confidence=_conf_for(src_ent, concept_conf))  # S3.5 gates on the SUBJECT (src) etype
    ok, errs = CSE.validate(cse)
    if not ok:
        return None, ("edge", (str(s), str(et), str(d)), str(et), "CSE validation FAIL: " + "; ".join(errs))
    return cse, None


def materialize_edge(cse: CSE.CSE) -> tuple:
    s = cse.transformation["subject"].ref
    d = cse.transformation["edges"][0].target.ref
    m = _EDGE_EV_RE.search(cse.provenance.evidence)
    return (str(s), m.group(1).strip() if m else None, str(d))


# ===========================================================================
# THE FULL-GRAPH ROUND-TRIP (the AC4 cert)
# ===========================================================================
def _norm_node_reason(reason: str) -> str:
    if "Concept(untyped) requires confidence" in reason:
        return "concept_confidence_collision"      # a lexically-certain node mapped to Entity.CONCEPT
    if "no Entity mapping" in reason:
        return "unmapped_node_type"
    return "other_validation"


def _norm_edge_reason(reason: str) -> str:
    if "Concept(untyped) requires confidence" in reason:
        return "concept_confidence_collision(endpoint)"
    if "edge_type" in reason and "unmapped" in reason:
        return "unmapped_edge_type"
    if "unmapped" in reason:
        return "unmapped_endpoint(concept_or_missing)"
    return "other_validation"


def _histogram(items) -> dict:
    h: dict = {}
    for k in items:
        h[k] = h.get(k, 0) + 1
    return dict(sorted(h.items(), key=lambda kv: -kv[1]))


def run_fullgraph_parity(nodes=None, edges=None, marker=None, all_edge_count=None,
                         concept_conf: float = 1.0) -> dict:
    if nodes is None:
        nodes, edges, marker, all_edge_count = export_graph()

    # ---- NODE round-trip ----
    live_nodes = {(str(nid), str(nt)) for nid, nt in nodes}
    recon_nodes, node_gaps = set(), []
    dupe = {}
    for nid, nt in nodes:
        dupe.setdefault(str(nid), set()).add(str(nt))
        cse, gap = recognize_node(nid, nt, marker, concept_conf)
        if gap:
            node_gaps.append(gap)
            continue
        rn = materialize_node(cse)
        recon_nodes.add((rn[0], str(rn[1])))
    node_missing = sorted(live_nodes - recon_nodes)
    node_extra = sorted(recon_nodes - live_nodes)
    dup_nids = {k: sorted(v) for k, v in dupe.items() if len(v) > 1}
    type_smell = sorted({nt for _, nt in live_nodes if nt in ("", "None")})

    # ---- EDGE round-trip ----
    live_edges = {(str(s), str(et), str(d)) for (s, _snt, et, d, _dnt) in edges}
    recon_edges, edge_gaps = set(), []
    for (s, snt, et, d, dnt) in edges:
        cse, gap = recognize_edge(s, snt, et, d, dnt, marker, concept_conf)
        if gap:
            edge_gaps.append(gap)
            continue
        recon_edges.add(materialize_edge(cse))
    edge_missing = sorted(live_edges - recon_edges)
    edge_extra = sorted(recon_edges - live_edges)

    # ---- AC4 type-level totality (reuse the P1 assert_live_coverage over the OBSERVED live inventory)
    live_nt = {str(nt) for _, nt in nodes}
    live_et = {str(et) for (_s, _snt, et, _d, _dnt) in edges}
    cov_ok, un_n, un_e = CSE.assert_live_coverage(live_nt, live_et)

    node_parity = not node_missing and not node_extra
    edge_parity = not edge_missing and not edge_extra
    # materializer FAULT = it invented a node/edge not in live (extra). That is the only rc=1 class;
    # a MISSING/gap is the instrument correctly surfacing a real coverage finding (routes to MOTIF/
    # PROMOTE/CTO), the recognizer working, not broken.
    materializer_fault = bool(node_extra or edge_extra)
    parity_pass = node_parity and edge_parity and cov_ok

    non_cloudnode_edges = (all_edge_count - len(edges)) if all_edge_count is not None else None

    return {
        "marker_head": marker,
        "concept_confidence_used": concept_conf,
        "node_count": len(nodes),
        "distinct_live_nodes": len(live_nodes),
        "edge_count_cloudnode_to_cloudnode": len(edges),
        "distinct_live_edges": len(live_edges),
        # parity is at the DISTINCT (nid,nt)/(src,et,dst) grain; a raw>distinct delta = duplicate
        # tuples in the live graph (parallel edges / a nid with 2 rows), a smell, NOT a parity loss.
        "duplicate_node_tuples": len(nodes) - len(live_nodes),
        "duplicate_edge_tuples": len(edges) - len(live_edges),
        "edge_count_all_cloudedge": all_edge_count,
        "edges_with_non_cloudnode_endpoint": non_cloudnode_edges,
        "live_node_types": len(live_nt),
        "live_edge_types": len(live_et),
        "reconstructed_nodes": len(recon_nodes),
        "reconstructed_edges": len(recon_edges),
        "node_parity": node_parity,
        "edge_parity": edge_parity,
        "ac4_type_coverage_ok": cov_ok,
        "ac4_unmapped_node_types": un_n,
        "ac4_unmapped_edge_types": un_e,
        "node_gap_reason_histogram": _histogram(_norm_node_reason(g[3]) for g in node_gaps),
        "edge_gap_reason_histogram": _histogram(_norm_edge_reason(g[3]) for g in edge_gaps),
        "node_gaps": node_gaps[:50],
        "node_gaps_total": len(node_gaps),
        "edge_gaps": edge_gaps[:50],
        "edge_gaps_total": len(edge_gaps),
        "node_missing_sample": node_missing[:25],
        "node_missing_total": len(node_missing),
        "node_extra_sample": node_extra[:25],
        "edge_missing_sample": edge_missing[:25],
        "edge_missing_total": len(edge_missing),
        "edge_extra_sample": edge_extra[:25],
        "smells": {
            "duplicate_node_id_types": dup_nids,
            "empty_or_none_node_type": type_smell,
        },
        "materializer_fault": materializer_fault,
        "parity_pass": parity_pass,
    }


# ===========================================================================
# DETERMINISTIC OFFLINE SELF-TEST (CVO re-exercise without a live DB) -- a tiny fixture proving BOTH
# the lossless round-trip AND the fail-closed gap-detection property. The __main__ live run below is
# the real AC4 cert against current HEAD.
# ===========================================================================
_FIX_MARKER = "test-snapshot-0001"
_FIX_NODES_CLEAN = [
    ("arn:aws:lambda:us-east-1:313476888478:function:bd-price-update", "LAMBDA"),
    ("opal-data-bd/silver/prices/canonical_prices.parquet", "S3Key"),
    ("s3:opal-data-bd", "S3_BUCKET"),
    ("component:AdvisorIntelligence", "ReactComponent"),
]
_FIX_EDGES_CLEAN = [
    ("arn:aws:lambda:us-east-1:313476888478:function:bd-price-update", "LAMBDA",
     "WRITES_S3", "opal-data-bd/silver/prices/canonical_prices.parquet", "S3Key"),
    ("component:AdvisorIntelligence", "ReactComponent", "FETCHES",
     "opal-data-bd/silver/prices/canonical_prices.parquet", "S3Key"),
]
_FIX_NODE_GAP = ("bogus:widget", "TOTALLY_UNMAPPED_TYPE")   # no node_type map, no known prefix
_FIX_EDGE_GAP = ("s3:opal-data-bd", "S3_BUCKET", "BOGUS_EDGE_TYPE",
                 "component:AdvisorIntelligence", "ReactComponent")


def self_test() -> bool:
    checks = []

    def chk(name, cond, detail=""):
        checks.append(cond)
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f"  -> {detail}" if (detail and not cond) else ""))

    print("=== NFRA_CSE.P2 full-graph AC4 parity self-test (deterministic fixture) ===")

    # 1. CLEAN fixture -> perfect round-trip (parity PASS, zero gaps, zero extra)
    rep = run_fullgraph_parity(_FIX_NODES_CLEAN, _FIX_EDGES_CLEAN, _FIX_MARKER, all_edge_count=len(_FIX_EDGES_CLEAN))
    chk("1  clean fixture round-trips exactly (parity_pass)", rep["parity_pass"], json.dumps(rep, default=str)[:400])
    chk("2  all 4 nodes reconstructed", rep["reconstructed_nodes"] == 4)
    chk("3  all 2 edges reconstructed", rep["reconstructed_edges"] == 2)
    chk("4  no materializer fault (invented nothing)", not rep["materializer_fault"])
    chk("5  AC6 marker pinned on the run", rep["marker_head"] == _FIX_MARKER)

    # 2. GAPPED fixture -> the unmapped node + edge FALL OUT as gaps (fail-closed), parity FALSE, but
    #    NO materializer fault (a MISSING gap is the instrument working, not a recognizer bug).
    nodes = _FIX_NODES_CLEAN + [_FIX_NODE_GAP]
    edges = _FIX_EDGES_CLEAN + [_FIX_EDGE_GAP]
    rep2 = run_fullgraph_parity(nodes, edges, _FIX_MARKER, all_edge_count=len(edges))
    chk("6  gapped fixture: parity FALSE (fail-closed on the unmapped node/edge)", not rep2["parity_pass"])
    chk("7  the unmapped node is named as a gap", rep2["node_gaps_total"] == 1 and
        rep2["node_gaps"][0][1] == "bogus:widget")
    chk("8  the unmapped edge_type is named as a gap", rep2["edge_gaps_total"] == 1 and
        "BOGUS_EDGE_TYPE" in rep2["edge_gaps"][0][3])
    chk("9  AC4 type-coverage reports the unmapped node_type + edge_type", not rep2["ac4_type_coverage_ok"]
        and "TOTALLY_UNMAPPED_TYPE" in rep2["ac4_unmapped_node_types"]
        and "BOGUS_EDGE_TYPE" in rep2["ac4_unmapped_edge_types"])
    chk("10 gap != materializer fault (no invented node/edge)", not rep2["materializer_fault"])
    chk("11 the mapped nodes/edges STILL round-trip (gap is isolated)",
        rep2["reconstructed_nodes"] == 4 and rep2["reconstructed_edges"] == 2)

    # 3. lossless-decompression property: a compressed edge_type (READS_S3 -> READS) still reconstructs
    #    to READS_S3, not the algebra Relationship -- the whole point (provenance-preserved concrete type)
    compressed = [("lambda:x", "LAMBDA", "READS_S3", "opal-data-bd/silver/x.parquet", "S3Key")]
    rep3 = run_fullgraph_parity([("lambda:x", "LAMBDA"), ("opal-data-bd/silver/x.parquet", "S3Key")],
                                compressed, _FIX_MARKER, all_edge_count=1)
    chk("12 lossy-algebra edge (READS_S3->READS) round-trips to READS_S3 (LAW-2 lossless decompress)",
        rep3["parity_pass"] and rep3["reconstructed_edges"] == 1)

    passed = sum(1 for c in checks if c)
    print(f"=== {passed}/{len(checks)} PASS ===")
    return passed == len(checks)


def _print_live_summary(rep: dict) -> None:
    print(json.dumps(rep, indent=2, default=str))
    print("\n" + "=" * 72)
    print(f"AC4 FULL-GRAPH ROUND-TRIP  (marker_head={rep['marker_head']})")
    print(f"  nodes: {rep['node_count']} ({rep['live_node_types']} types) -> "
          f"{rep['reconstructed_nodes']} reconstructed | parity={rep['node_parity']}")
    print(f"  edges: {rep['edge_count_cloudnode_to_cloudnode']} ({rep['live_edge_types']} types) -> "
          f"{rep['reconstructed_edges']} reconstructed | parity={rep['edge_parity']}")
    if rep["edges_with_non_cloudnode_endpoint"]:
        print(f"  note: {rep['edges_with_non_cloudnode_endpoint']} CloudEdge(s) have a non-CloudNode "
              f"endpoint (out of AC4 CloudNode/CloudEdge scope -- characterized, not dropped-silently)")
    if rep["duplicate_edge_tuples"] or rep["duplicate_node_tuples"]:
        print(f"  note: {rep['duplicate_node_tuples']} duplicate node-tuple(s) + "
              f"{rep['duplicate_edge_tuples']} duplicate edge-tuple(s) in live (parity is at the DISTINCT "
              f"grain -- a raw>distinct delta is a parallel-edge smell, not a parity loss)")
    if rep["node_gaps_total"] or rep["edge_gaps_total"]:
        print(f"  GAPS: {rep['node_gaps_total']} node + {rep['edge_gaps_total']} edge "
              f"(named coverage-gaps -> MOTIF/PROMOTE/CTO disposition, fail-closed)")
        print(f"    node gap classes: {rep['node_gap_reason_histogram']}")
        print(f"    edge gap classes: {rep['edge_gap_reason_histogram']}")
    if rep["parity_pass"]:
        print("  VERDICT: AC4 PARITY PASS -- the CSE algebra + mandatory provenance losslessly "
              "reproduce the full live CloudNode/CloudEdge graph.")
    elif rep["materializer_fault"]:
        print("  VERDICT: MATERIALIZER FAULT -- reconstructed a node/edge NOT in live (see *_extra). "
              "This is a real defect (rc=1).")
    else:
        print("  VERDICT: GAPS FOUND -- the round-trip surfaced real coverage-gaps (instrument working, "
              "rc=0); every mapped node/edge round-trips exactly.")


def main() -> int:
    if "--self-test" in sys.argv:
        return 0 if self_test() else 1
    # --diagnose-type-fix: a MECHANISM-ISOLATION probe (NOT the production materializer). Assigns the
    # Concept-subject CSEs the honest-degrade band (<=LOW_CONFIDENCE_MAX) purely to PROVE the entire
    # residual is the CONCEPT/confidence collision -- i.e. that a governed resolution (add Entity.TYPE/
    # SYMBOL, or refine S3.5 to allow high-confidence on a deterministic Concept-mapping) closes the
    # round-trip to 100%. This confidence is NOT the honest production value for a lexically-certain
    # TypeDecl -- it is diagnostic only.
    diag = "--diagnose-type-fix" in sys.argv
    concept_conf = CSE.LOW_CONFIDENCE_MAX if diag else 1.0
    try:
        rep = run_fullgraph_parity(concept_conf=concept_conf)
    except LivePullError as ex:
        print(f"ERROR: live graph export FAILED (no silent partial round-trip): {ex}")
        return 2
    if diag:
        print(f"[DIAGNOSTIC --diagnose-type-fix] Concept-subject confidence forced to "
              f"{concept_conf} (<=LOW_CONFIDENCE_MAX) to ISOLATE the mechanism -- NOT the production "
              f"value. If parity now PASSES, the entire residual is the CONCEPT/confidence collision.")
    _print_live_summary(rep)
    return 1 if rep["materializer_fault"] else 0


if __name__ == "__main__":
    sys.exit(main())
