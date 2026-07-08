#!/usr/bin/env python3
"""MOTIF-P2 follow-on -- the C2/C3-in-graph MATERIALIZE SPEC (node + CONTAINS-edge records for 0.7.0).

MOTIF-P2 discovered the C3 systems read-only (43c3e4701, CVO-certed 7328e270d); the store-write of the
C2/C3 nodes + CONTAINS edges is the MATERIALIZE leg (in-VPC AE/derive-ingest, same path as 0.7.0's
ingest_cluster_producer wrote the 91 clusters). COO ruled it in-scope (graph-completeness, NOT
loop-close-gating -- PROMOTE consumes the candidate JSON directly). This module EMITS the proposed
node/edge records (motif_c2c3_materialize.json) for 0.7.0 to ingest; CVO certs the round-trip (+ it
exercises the comp-kuzu re-finalize-on-advance residual in one pass).

The materialize is a GRAPH-COMPLETENESS write, NOT a promotion -- these C2/C3 nodes are the DISCOVERED
structure made queryable in the graph; a PROMOTION (a motif -> a first-class recognizer) is the separate
PROMOTE-plane write-back, human-ratified + measure-gated. Keep them distinct.

CONVENTION (proposed -- 0.7.0/CVO confirm the exact node_type/edge_type the store expects):
  - C2 motif node:  node_id="motif:<idiom>",  node_type="C2Motif"
  - C3 system node: node_id="system:<name>",  node_type="C3System"
  - CONTAINS edges: C3System -CONTAINS-> C2Motif (C3->C2); C2Motif -CONTAINS-> <existing C1 instance node>
    (C2->C1) -- linking the NEW C2 node to the EXISTING graph nodes (out:/rc:/type:/endpoint: instances),
    so the decompression chain is intact IN the graph (a materialized motif still decompresses to C0).
  - Every node carries recurrence + the decompression footprint in props (LAW-2: no latent node in the store).

Usage: python MOTIF_c2c3_materialize_spec.py            # emit the spec -> motif_c2c3_materialize.json
       python MOTIF_c2c3_materialize_spec.py --print     # print a summary

Author: 0.4.0_DS_ClientPlatform~B. MOTIF-P2 follow-on (materialize hand-off to 0.7.0_AE).
"""
from __future__ import annotations

import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(WS, "org", "modules", "graph"))

import NFRA_MOTIF_P1_c2_catalog as P1  # noqa: E402
import NFRA_MOTIF_P2_c3_emergence as P2  # noqa: E402
from comp_ladder import decompress  # noqa: E402

SPEC_ARTIFACT = os.path.join(_HERE, "motif_c2c3_materialize.json")


def _c1_instances(motif) -> list:
    """The existing C1 instance node_ids a C2 motif CONTAINS (its decompression-chain C1 layer).
    Ladder-provenance form 'c1:D{n}:<type>:...' (D{n} = the TSGRAPH detector that surfaced it)."""
    return [n.nid for _, n in decompress(motif) if n.layer == "C1"]


# The decompression ladder emits C1 nids in the provenance form 'c1:D{n}:<type>:...'. The ESTATE graph
# (where 0.7.0 ingests) uses the BARE '<type>:...' canonical node_id -- comp-kuzu verified 2026-07-08
# (0.7.0 RAVC1): the c1:D{n}: form resolves to 0 store nodes; stripped, 30/30 distinct resolve. Strip the
# discriminator so the CONTAINS edge targets the REAL node; keep the detector(s) in props (lossless).
_C1_DISCRIM = re.compile(r"^c1:(D\d+):(.*)$")


def _canonical_c1(nid: str):
    """(canonical_estate_node_id, detector|None) -- strip the ladder 'c1:D{n}:' discriminator to the bare
    '<type>:...' estate node_id the store actually carries; return the detector for provenance."""
    m = _C1_DISCRIM.match(nid)
    return (m.group(2), m.group(1)) if m else (nid, None)


def build_spec() -> dict:
    # stable C2 motifs (from P1) + emergent C3 systems (from P2)
    motifs, prov = [], {}
    for spec in P1.CATALOG:
        motif, recurrence, p = P1.build_motif(spec)
        prov = p or prov
        if recurrence >= P1.AC3_THRESHOLD:
            motifs.append((motif, recurrence, spec))
    motif_nodes = [m for m, _, _ in motifs]
    f2c, _ = P2.load_cluster_index()
    coupled = P2.load_shares_source()
    systems, _, _ = P2.build_c3_systems(motif_nodes, f2c, coupled)

    nodes, edges = [], []

    # C2 motif nodes + their CONTAINS->C1 edges
    for motif, recurrence, spec in motifs:
        nodes.append({"node_id": motif.nid, "node_type": "C2Motif",
                      "props": {"motif_type": spec["ntype"], "catalog_class": spec["catalog_class"],
                                "tier": spec["tier"], "recurrence": recurrence,
                                "n_instances": len(_c1_instances(motif))}})
        # C2->C1 CONTAINS -> the EXISTING estate node (canonical '<type>:...'; discriminator stripped).
        # DEDUP the collapse-cases (same canonical node surfaced by >1 detector, e.g. the D2 n D3 overlap-lens),
        # merging the detector provenance so nothing is lost.
        by_target: dict = {}
        for inst in _c1_instances(motif):
            tgt, det = _canonical_c1(inst)
            slot = by_target.setdefault(tgt, set())
            if det:
                slot.add(det)
        for tgt, dets in by_target.items():
            props = {"layer": "C2->C1"}
            if dets:
                props["via_detectors"] = sorted(dets)
            edges.append({"source": motif.nid, "target": tgt, "edge_type": "CONTAINS", "props": props})

    # C3 system nodes + their CONTAINS->C2 edges
    for sys_node, why in systems:
        nodes.append({"node_id": sys_node.nid, "node_type": "C3System",
                      "props": {"system_type": sys_node.ntype,
                                "member_motifs": [c.nid for c in sys_node.children],
                                "recurrence": len(sys_node.children),
                                "connectivity": {"shared_constituents": why["shared_constituents"][:5],
                                                 "shared_clusters": why["shared_clusters"]}}})
        for member in sys_node.children:
            edges.append({"source": sys_node.nid, "target": member.nid, "edge_type": "CONTAINS",
                          "props": {"layer": "C3->C2"}})

    return {
        "producer": "MOTIF-P2 follow-on (0.4.0_DS_ClientPlatform~B)",
        "consumer": "0.7.0_AE_CloudOps (derive/ingest -- same path as ingest_cluster_producer)",
        "cert": "CVO round-trip (7328e270d discovery -> materialized round-trip)",
        "grounding": {"c2_catalog_cert": "b783dd504", "c3_emergence": "43c3e4701",
                      "graph": "comp-kuzu fresh HEAD (fix-verified 06fbc6832)",
                      "nodes_snapshot_hint": prov.get("nodes_snapshot_id")},
        "convention_note": ("node_type C2Motif/C3System + CONTAINS edges. C2->C1 targets are the CANONICAL "
                            "estate node_ids (bare '<type>:...'; the ladder 'c1:D{n}:' discriminator STRIPPED "
                            "so the edge resolves to the EXISTING store node -- comp-kuzu RAVC1 2026-07-08: "
                            "c1:D{n}: form=0 store rows, stripped=30/30 resolve). Detector provenance kept in "
                            "props.via_detectors (lossless). C3->C2 targets are the motif: nodes created in this "
                            "same batch. 0.7.0/CVO confirm the exact C2Motif/C3System node_type on ingest."),
        "taxonomy_prereq": {
            "gate": "C2Motif + C3System are NEW node_types -> derive_runner.relabel_layers_by_node_type FAILS CLOSED "
                    "(COND-2 durability) on any node_type not in NODE_TYPE_LAYER (derive_runner.py:~1497). Ingesting "
                    "WITHOUT adding them first re-freezes the derive (the exact ~24h freeze fixed today). MUST "
                    "pre-add + CVO count re-sign + CTO arch-gate BEFORE ingest (0.7.0 drives, like today's aws +3 dual-sign).",
            "recommended_layer": "a NEW 'semctl' (or 'motif') analysis/composition layer -- NOT portal/aws/pipeline. "
                                 "Rationale: C2Motif/C3System are the SEMCTL compression layers (C2/C3) ABOVE the C1 "
                                 "estate, discovered-architecture nodes, not infra. A distinct layer keeps the taxonomy "
                                 "honest (C0 facts / C1 estate / C2 motifs / C3 systems) + isolates them from estate blast-radius.",
        },
        "counts": {"c2_motif_nodes": sum(1 for n in nodes if n["node_type"] == "C2Motif"),
                   "c3_system_nodes": sum(1 for n in nodes if n["node_type"] == "C3System"),
                   "contains_edges": len(edges)},
        "nodes": nodes,
        "edges": edges,
    }


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass
    spec = build_spec()
    with open(SPEC_ARTIFACT, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, indent=2)
    c = spec["counts"]
    print("MOTIF C2/C3 materialize spec -> %s" % os.path.relpath(SPEC_ARTIFACT, WS))
    print("  %d C2Motif nodes + %d C3System nodes + %d CONTAINS edges"
          % (c["c2_motif_nodes"], c["c3_system_nodes"], c["contains_edges"]))
    print("  convention: %s" % spec["convention_note"])
    if "--print" in sys.argv[1:]:
        for n in spec["nodes"]:
            print("  NODE %-32s %s" % (n["node_id"], n["node_type"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
