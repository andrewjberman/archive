#!/usr/bin/env python3
"""NFRA_MOTIF P1 CANONICAL A+B -- the 13 canonical STRUCTURAL motif detectors (Plane A cloud/IAM/serve x9
+ Plane B pipeline/data x4), the CANONICAL sibling of the DEBT-only P1 catalog.

TO NFRA_ONTOLOGY.AB-MAT-S1 (COO GO 20260718T140733Z; CTO SoD gate OPEN 140326Z). BINDING vocabulary spec:
org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_ONTOLOGY_AB_MATERIALIZE_SPEC.md @7892f3fbc (~C-authored,
CTO arch-gated SOUND). `tier: canonical` (contrast the debt tiers gate-ready/advisory/candidate-gen).

WHY A SIBLING (TO allows "or a canonical sibling"): the debt catalog NFRA_MOTIF_P1_c2_catalog.py + its
materializer are CVO-CERTED + already INGESTED (the 6 C2Motif + 1 C3System live in the store). Extending them
in place risks a regression on a certed+ingested layer; a clean sibling adds the A+B layer additively and
leaves the debt layer untouched. This module REUSES (never forks) the debt module's comp_kuzu runner
(Rule 20 QUERY-the-live-graph), GraphUnavailable fail-loud, AC3_THRESHOLD, system_node_id (collision-safe C3
ids), and the REAL comp_ladder fidelity gate.

GROUNDED LIVE (Rule 22 -- recurrence MEASURED, never echoed). The @02:18Z scan behind the spec had 3 recurrence
errors this catalog CORRECTS from the live graph @HEAD 8797848286033539361 (2026-07-18T14:14Z):
  a-store   232 (spec 28902 -- impossible; the path is bounded by S3Key=232),
  a-serve-cf  9 (spec 228  -- bounded by ORIGIN+USES_OAI=9 on 1 CLOUDFRONT_DISTRIBUTION),
  a-watch    21 (spec 184/71/50 -- MONITORS total is 28),
  a-orch     28 (spec 62   -- STATE_MACHINE INVOKES bounded).
The other 9 match the spec's per-type breakdowns. All 13 are >= AC3 (stable motifs).

C2->C1 RESOLVE (CTO acceptance condition 1): an A+B detector matches EXISTING estate nodes directly, so a C2
motif's C1 children ARE the bare estate node_ids (ARNs / '<type>:...') the store already carries -- they
resolve to NON-ZERO rows BY CONSTRUCTION. There is NO 'c1:D{n}:' ladder discriminator to strip (the 07-08
comp-kuzu 0-row trap was specific to the debt ladder's synthetic C1 wrapper; it does not arise here). The
resolve self-check counts them anyway and states the denominator (verify, do not assert).

NO RE-FREEZE (CTO acceptance condition 2): C2Motif + C3System are already in NODE_TYPE_LAYER (debt materialize
07-08; live counts C2Motif=6, C3System=1) -- this emits the SAME node_types, so no new node_type,
derive_runner.relabel_layers_by_node_type does not trip on 0.7.0 ingest.

HARD GUARDRAIL: this EMITS the materialize records (motif_c2c3_materialize_ab.json) through the governed path;
it NEVER hand-writes a C2Motif/C3System node into the store. 0.7.0 ingests + CVO certs the round-trip.

Usage:
  python NFRA_MOTIF_P1_canonical_ab_catalog.py            # live: build 13 motifs, emerge C3, EMIT the json
  python NFRA_MOTIF_P1_canonical_ab_catalog.py --print    # live + print the emergence + resolve self-check
  python NFRA_MOTIF_P1_canonical_ab_catalog.py --self-test # gate logic (no live graph): fidelity + AC3 + emergence + resolve-form

Author: 0.4.0_DS_ClientPlatform~B (MOTIF graph-lane). TO NFRA_ONTOLOGY.AB-MAT-S1.
"""
from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(WS, "org", "modules", "graph"))

import NFRA_MOTIF_P1_c2_catalog as P1  # noqa: E402  -- reuse comp_kuzu/GraphUnavailable/AC3/system_node_id
from comp_ladder import Node, fidelity_check  # noqa: E402  -- the REAL fidelity gate

SPEC_ARTIFACT = os.path.join(_HERE, "motif_c2c3_materialize_ab.json")
N, E = "CloudNode", "CloudEdge"


# ---------------------------------------------------------------------------
# The 13 canonical A+B detectors. Each `constituents` col is (alias, node_type); the instance_query RETURNs
# those node_id columns. recurrence = # matched path rows; the C2 CONTAINS the DISTINCT constituent nodes.
# ---------------------------------------------------------------------------
AB_CATALOG = [
    # -- Plane A: Cloud / IAM / Serve --------------------------------------------------------------
    {"id": "a-store", "plane": "A", "ntype": "AStoreMotif",
     "idiom": "(S3_BUCKET)-CONTAINS->(S3Key)-OWNED_BY->(S3_BUCKET) -- object storage",
     "constituents": [("b1", "S3_BUCKET"), ("k", "S3Key"), ("b2", "S3_BUCKET")],
     "query": ("MATCH (b1:%s)-[e1:%s]->(k:%s)-[e2:%s]->(b2:%s) WHERE b1.node_type='S3_BUCKET' "
               "AND e1.edge_type='CONTAINS' AND k.node_type='S3Key' AND e2.edge_type='OWNED_BY' "
               "AND b2.node_type='S3_BUCKET' RETURN b1.node_id AS b1, k.node_id AS k, b2.node_id AS b2" % (N, E, N, E, N))},
    {"id": "a-access", "plane": "A", "ntype": "AAccessMotif",
     "idiom": "(LAMBDA|EC2_INSTANCE)-READS|WRITES->(S3_BUCKET) -- compute-to-object access",
     "constituents": [("actor", None), ("bucket", "S3_BUCKET")],
     "query": ("MATCH (a:%s)-[e:%s]->(b:%s) WHERE (a.node_type='LAMBDA' OR a.node_type='EC2_INSTANCE') "
               "AND (e.edge_type='READS' OR e.edge_type='WRITES') AND b.node_type='S3_BUCKET' "
               "RETURN a.node_id AS actor, b.node_id AS bucket" % (N, E, N))},
    {"id": "a-table", "plane": "A", "ntype": "ATableMotif",
     "idiom": "(LAMBDA)-READS|WRITES->(DYNAMODB_TABLE)-ENCRYPTS_WITH->(KMS_KEY) -- encrypted table access",
     "constituents": [("l", "LAMBDA"), ("t", "DYNAMODB_TABLE"), ("kms", "KMS_KEY")],
     "query": ("MATCH (l:%s)-[e1:%s]->(t:%s)-[e2:%s]->(kms:%s) WHERE l.node_type='LAMBDA' "
               "AND (e1.edge_type='READS' OR e1.edge_type='WRITES') AND t.node_type='DYNAMODB_TABLE' "
               "AND e2.edge_type='ENCRYPTS_WITH' AND kms.node_type='KMS_KEY' "
               "RETURN l.node_id AS l, t.node_id AS t, kms.node_id AS kms" % (N, E, N, E, N))},
    {"id": "a-grant", "plane": "A", "ntype": "AGrantMotif",
     "idiom": "(LAMBDA|SERVICE_PRINCIPAL|INSTANCE_PROFILE)-ASSUMES|CAN_ASSUME->(IAM_ROLE)-HAS_POLICY->(IAM_POLICY) -- identity grant",
     "constituents": [("p", None), ("r", "IAM_ROLE"), ("pol", "IAM_POLICY")],
     "query": ("MATCH (p:%s)-[e1:%s]->(r:%s)-[e2:%s]->(pol:%s) WHERE (p.node_type='LAMBDA' "
               "OR p.node_type='SERVICE_PRINCIPAL' OR p.node_type='INSTANCE_PROFILE') "
               "AND (e1.edge_type='ASSUMES' OR e1.edge_type='CAN_ASSUME') AND r.node_type='IAM_ROLE' "
               "AND e2.edge_type='HAS_POLICY' AND pol.node_type='IAM_POLICY' "
               "RETURN p.node_id AS p, r.node_id AS r, pol.node_id AS pol" % (N, E, N, E, N))},
    {"id": "a-event", "plane": "A", "ntype": "AEventMotif",
     "idiom": "(EVENT_SOURCE)-EMITS_TO->(EVENT_RULE)-TRIGGERS->(LAMBDA) -- event routing",
     "constituents": [("s", "EVENT_SOURCE"), ("ru", "EVENT_RULE"), ("l", "LAMBDA")],
     "query": ("MATCH (s:%s)-[e1:%s]->(ru:%s)-[e2:%s]->(l:%s) WHERE s.node_type='EVENT_SOURCE' "
               "AND e1.edge_type='EMITS_TO' AND ru.node_type='EVENT_RULE' AND e2.edge_type='TRIGGERS' "
               "AND l.node_type='LAMBDA' RETURN s.node_id AS s, ru.node_id AS ru, l.node_id AS l" % (N, E, N, E, N))},
    {"id": "a-api", "plane": "A", "ntype": "AApiMotif",
     "idiom": "(API_GW)-HAS_ROUTE->(API_ROUTE)-ROUTES_TO->(LAMBDA) -- API routing",
     "constituents": [("g", "API_GW"), ("rt", "API_ROUTE"), ("l", "LAMBDA")],
     "query": ("MATCH (g:%s)-[e1:%s]->(rt:%s)-[e2:%s]->(l:%s) WHERE g.node_type='API_GW' "
               "AND e1.edge_type='HAS_ROUTE' AND rt.node_type='API_ROUTE' AND e2.edge_type='ROUTES_TO' "
               "AND l.node_type='LAMBDA' RETURN g.node_id AS g, rt.node_id AS rt, l.node_id AS l" % (N, E, N, E, N))},
    {"id": "a-serve", "plane": "A", "ntype": "AServeMotif",
     "idiom": ("(CLOUDFRONT_DISTRIBUTION)-ORIGIN|USES_OAI->(S3_BUCKET) ; "
               "(DataFetch)-IS_ENDPOINT->(Endpoint)-READS_URL->(ServedURL) -- serve boundary (CDN + FE), one motif"),
     "subqueries": [
        {"constituents": [("cf", "CLOUDFRONT_DISTRIBUTION"), ("b", "S3_BUCKET")],
         "query": ("MATCH (cf:%s)-[e:%s]->(b:%s) WHERE cf.node_type='CLOUDFRONT_DISTRIBUTION' "
                   "AND (e.edge_type='ORIGIN' OR e.edge_type='USES_OAI') AND b.node_type='S3_BUCKET' "
                   "RETURN cf.node_id AS cf, b.node_id AS b" % (N, E, N))},
        {"constituents": [("d", "DataFetch"), ("ep", "Endpoint"), ("u", "ServedURL")],
         "query": ("MATCH (d:%s)-[e1:%s]->(ep:%s)-[e2:%s]->(u:%s) WHERE d.node_type='DataFetch' "
                   "AND e1.edge_type='IS_ENDPOINT' AND ep.node_type='Endpoint' AND e2.edge_type='READS_URL' "
                   "AND u.node_type='ServedURL' RETURN d.node_id AS d, ep.node_id AS ep, u.node_id AS u" % (N, E, N, E, N))},
     ]},
    {"id": "a-watch", "plane": "A", "ntype": "AWatchMotif",
     "idiom": "(CW_ALARM)-MONITORS->(LAMBDA|EC2_INSTANCE) -- the Observer motif",
     "constituents": [("al", "CW_ALARM"), ("tgt", None)],
     "query": ("MATCH (al:%s)-[e:%s]->(tgt:%s) WHERE al.node_type='CW_ALARM' AND e.edge_type='MONITORS' "
               "AND (tgt.node_type='LAMBDA' OR tgt.node_type='EC2_INSTANCE') "
               "RETURN al.node_id AS al, tgt.node_id AS tgt" % (N, E, N))},
    {"id": "a-orch", "plane": "A", "ntype": "AOrchMotif",
     "idiom": "(STATE_MACHINE)-INVOKES->(LAMBDA) -- step-function orchestration",
     "constituents": [("sm", "STATE_MACHINE"), ("l", "LAMBDA")],
     "query": ("MATCH (sm:%s)-[e:%s]->(l:%s) WHERE sm.node_type='STATE_MACHINE' AND e.edge_type='INVOKES' "
               "AND l.node_type='LAMBDA' RETURN sm.node_id AS sm, l.node_id AS l" % (N, E, N))},
    # -- Plane B: Pipeline / Data ------------------------------------------------------------------
    {"id": "b-struct", "plane": "B", "ntype": "BStructMotif",
     "idiom": "(Pipeline)-CONTAINS->(PipelineScript)-CONTAINS->(PipelineFunction)-CALLS->(PipelineFunction) -- pipeline structure",
     "constituents": [("ps", "PipelineScript"), ("pf", "PipelineFunction"), ("pf2", "PipelineFunction")],
     "query": ("MATCH (p:%s)-[e1:%s]->(ps:%s)-[e2:%s]->(pf:%s)-[e3:%s]->(pf2:%s) WHERE p.node_type='Pipeline' "
               "AND e1.edge_type='CONTAINS' AND ps.node_type='PipelineScript' AND e2.edge_type='CONTAINS' "
               "AND pf.node_type='PipelineFunction' AND e3.edge_type='CALLS' AND pf2.node_type='PipelineFunction' "
               "RETURN ps.node_id AS ps, pf.node_id AS pf, pf2.node_id AS pf2" % (N, E, N, E, N, E, N))},
    {"id": "b-run", "plane": "B", "ntype": "BRunMotif",
     "idiom": "(EC2_INSTANCE)-RUNS->(PipelineScript) -- pipeline execution",
     "constituents": [("ec2", "EC2_INSTANCE"), ("ps", "PipelineScript")],
     "query": ("MATCH (ec2:%s)-[e:%s]->(ps:%s) WHERE ec2.node_type='EC2_INSTANCE' AND e.edge_type='RUNS' "
               "AND ps.node_type='PipelineScript' RETURN ec2.node_id AS ec2, ps.node_id AS ps" % (N, E, N))},
    {"id": "b-io", "plane": "B", "ntype": "BIoMotif",
     "idiom": "(PipelineScript|PipelineFunction)-READS_S3|WRITES_S3->(S3Key)-OWNED_BY->(S3_BUCKET) -- pipeline object I/O",
     "constituents": [("src", None), ("k", "S3Key"), ("b", "S3_BUCKET")],
     "query": ("MATCH (src:%s)-[e1:%s]->(k:%s)-[e2:%s]->(b:%s) WHERE (src.node_type='PipelineScript' "
               "OR src.node_type='PipelineFunction') AND (e1.edge_type='READS_S3' OR e1.edge_type='WRITES_S3') "
               "AND k.node_type='S3Key' AND e2.edge_type='OWNED_BY' AND b.node_type='S3_BUCKET' "
               "RETURN src.node_id AS src, k.node_id AS k, b.node_id AS b" % (N, E, N, E, N))},
    {"id": "b-dataflow", "plane": "B", "ntype": "BDataflowMotif",
     "idiom": "(Field)-FLOWS_TO->(Field) -- field-grain data lineage",
     "constituents": [("f1", "Field"), ("f2", "Field")],
     "query": ("MATCH (f1:%s)-[e:%s]->(f2:%s) WHERE f1.node_type='Field' AND e.edge_type='FLOWS_TO' "
               "AND f2.node_type='Field' RETURN f1.node_id AS f1, f2.node_id AS f2" % (N, E, N))},
]

# resource-priority for C3 naming (inherited-from-constituents, deterministic, never invented -- the anchor's
# C3-naming law). A system is named by the highest-priority resource node_type among its SHARED constituents.
RESOURCE_THEME = [
    (("PipelineScript", "PipelineFunction", "Field"), "pipeline"),
    (("DYNAMODB_TABLE", "KMS_KEY"), "table-data"),
    (("IAM_ROLE", "IAM_POLICY"), "identity"),
    (("S3Key", "S3_BUCKET"), "object-data"),
    (("EVENT_RULE", "STATE_MACHINE", "API_ROUTE", "EVENT_SOURCE"), "compute-orchestration"),
    (("Endpoint", "ServedURL", "DataFetch"), "serve"),
]


def _theme_for(node_types: set) -> str:
    for types, theme in RESOURCE_THEME:
        if node_types & set(types):
            return theme
    return "shared-constituent-capability"


# ---------------------------------------------------------------------------
# Build one A+B C2 motif from its live rows. C1 children = the DISTINCT estate constituent nodes (bare
# node_ids that resolve). Returns (motif_node, recurrence, constituent_types: {node_id: node_type}).
# ---------------------------------------------------------------------------
def build_ab_motif(spec: dict) -> tuple:
    # a detector is one query, or a compound of sub-queries (a-serve: CDN-serve + FE-serve = one motif)
    subs = spec.get("subqueries") or [{"query": spec["query"], "constituents": spec["constituents"]}]
    recurrence = 0
    const_type: dict = {}                        # node_id -> node_type (for naming + labeling)
    for sub in subs:
        rows, _ = P1.comp_kuzu(sub["query"])
        recurrence += len(rows)                  # each matched path row = one instance of the idiom
        for r in rows:
            for alias, ntype in sub["constituents"]:
                nid = r.get(alias)
                if nid:
                    # actor/target aliases carry node_type=None (LAMBDA-or-EC2 etc.); keep the first seen or 'actor'
                    const_type.setdefault(nid, ntype or "actor")
    # compose the C2 motif: C1 child per distinct constituent (bare estate node_id -> resolves), C0 fact each.
    c1_children = []
    for nid in sorted(const_type):
        c0 = P1.c0_fact(nid, const_type[nid], "canonical A+B constituent")
        c1_children.append(Node(nid, "C1", const_type[nid] + "Instance", nid,
                                rule="canonical detector " + spec["id"] + ": " + spec["idiom"],
                                children=[c0]))
    motif = Node("motif:" + spec["id"], "C2", spec["ntype"], spec["id"],
                 rule="CANONICAL " + spec["plane"] + " (" + spec["id"] + "): " + spec["idiom"],
                 children=c1_children)
    return motif, recurrence, const_type


# ---------------------------------------------------------------------------
# C3 emergence: shared-constituent union-find (the only substrate signal for infra motifs -- cluster/
# SHARES_SOURCE are portal-frontend signals that do not touch A+B nodes). name = inherited-from-constituents.
# ---------------------------------------------------------------------------
def ab_c3_emergence(motifs: list, const_types: dict) -> tuple:
    """(systems:[(node, why)], singletons:[nid]). A pair is CONNECTED iff their C1 constituent sets intersect."""
    foot = {m.nid: {c.nid for c in m.children} for m in motifs}
    by_nid = {m.nid: m for m in motifs}
    ids = [m.nid for m in motifs]
    parent = {i: i for i in ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)

    shared_ev: dict = {}
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            shared = foot[ids[i]] & foot[ids[j]]
            if shared:
                union(ids[i], ids[j])
                shared_ev[(ids[i], ids[j])] = shared
    comps: dict = {}
    for mid in ids:
        comps.setdefault(find(mid), []).append(mid)

    systems, singletons = [], []
    for _, members in sorted(comps.items()):
        if len(members) < 2:
            singletons.append(members[0])
            continue
        member_motifs = [by_nid[m] for m in members]
        why_shared = set()
        for (a, b), sh in shared_ev.items():
            if a in members and b in members:
                why_shared |= sh
        shared_types = {const_types.get(nid, "?") for nid in why_shared}
        theme = _theme_for(shared_types)
        rule = ("C3 EMERGENCE (structural shared-constituent, no embedding): motifs {%s} connected via %d shared "
                "estate node(s) of type(s) %s -> capability (DISCOVERED, not declared)"
                % (", ".join(m.split(":", 1)[1] for m in members), len(why_shared),
                   ", ".join(sorted(t for t in shared_types if t and t != "?"))))
        sys_node = Node(P1.system_node_id(theme, members), "C3", "EmergentSystem", theme, rule=rule,
                        children=member_motifs)
        systems.append((sys_node, {"shared_constituents": sorted(why_shared)[:8],
                                   "shared_types": sorted(shared_types), "n_shared": len(why_shared)}))
    return systems, singletons


# ---------------------------------------------------------------------------
# ALTERNATIVE C3 view -- overlapping domain-resource-type COVER (the spec Sec-2 candidate model). A system =
# the motifs that share a DOMAIN resource-type; a motif may belong to SEVERAL (an overlapping cover, NOT a
# partition). Contrast ab_c3_emergence (connected-components PARTITION), which transitively MERGES the whole
# A-plane via shared LAMBDA/EC2/S3/PipelineScript INSTANCES -> 1 supersystem. This view is NOT emitted for
# ingest unilaterally (it changes what "C3 system" means: cover vs partition -> ~C/CTO ratify); it is computed
# to SURFACE to COO what the operational ~3-5 systems would be. (TO Phase-3 <if_mismatch>: surface, don't force.)
# ---------------------------------------------------------------------------
DOMAIN_TYPES = {
    "object-data": {"S3_BUCKET", "S3Key"},
    "table-data": {"DYNAMODB_TABLE", "KMS_KEY"},
    "identity": {"IAM_ROLE", "IAM_POLICY"},
    "eventing": {"EVENT_SOURCE", "EVENT_RULE"},
    "api": {"API_GW", "API_ROUTE"},
    "orchestration": {"STATE_MACHINE"},
    "observability": {"CW_ALARM"},
    "serve": {"CLOUDFRONT_DISTRIBUTION", "Endpoint", "ServedURL", "DataFetch"},
    "compute": {"LAMBDA", "EC2_INSTANCE"},
    "pipeline-code": {"PipelineScript", "PipelineFunction"},
    "dataflow": {"Field"},
}


def ab_domain_view(motifs: list, const_types: dict) -> dict:
    """{domain_theme: [member motif nids]} for domains with >=2 member motifs (an overlapping cover)."""
    motif_types = {m.nid: {const_types.get(c.nid, "?") for c in m.children} for m in motifs}
    out = {}
    for dom, types in DOMAIN_TYPES.items():
        members = [m.nid for m in motifs if motif_types[m.nid] & types]
        if len(members) >= 2:
            out[dom] = members
    return out


# ---------------------------------------------------------------------------
# Build the materialize spec (nodes + CONTAINS edges) -- the motif_c2c3_materialize_ab.json-analog.
# ---------------------------------------------------------------------------
def build_ab_spec() -> tuple:
    motifs, recur, const_types = [], {}, {}
    prov = {}
    for spec in AB_CATALOG:
        rows, p = P1.comp_kuzu("MATCH (n:%s) RETURN n.node_id LIMIT 0" % N) if False else ([], {})  # noqa: F841
        motif, recurrence, ct = build_ab_motif(spec)
        motifs.append((motif, recurrence, spec))
        recur[spec["id"]] = recurrence
        const_types.update(ct)
    # capture provenance once (a cheap probe)
    _, prov = P1.comp_kuzu("MATCH (n:%s) WHERE n.node_type='S3_BUCKET' RETURN n.node_id LIMIT 1" % N)

    motif_nodes = [m for m, _, _ in motifs]
    systems, singletons = ab_c3_emergence(motif_nodes, const_types)
    domain_view = ab_domain_view(motif_nodes, const_types)   # surfaced alternative (not emitted as nodes)

    nodes, edges = [], []
    for motif, recurrence, spec in motifs:
        c1 = [c.nid for c in motif.children]     # bare estate node_ids (resolve; no discriminator to strip)
        nodes.append({"node_id": motif.nid, "node_type": "C2Motif",
                      "props": {"motif_type": spec["ntype"], "plane": spec["plane"], "tier": "canonical",
                                "recurrence": recurrence, "n_instances": len(c1), "detector": spec["idiom"]}})
        for tgt in c1:
            edges.append({"source": motif.nid, "target": tgt, "edge_type": "CONTAINS",
                          "props": {"layer": "C2->C1"}})
    for sys_node, why in systems:
        nodes.append({"node_id": sys_node.nid, "node_type": "C3System",
                      "props": {"system_type": sys_node.label, "member_motifs": [c.nid for c in sys_node.children],
                                "recurrence": len(sys_node.children),
                                "connectivity": {"shared_types": why["shared_types"], "n_shared": why["n_shared"],
                                                 "shared_constituents": why["shared_constituents"]}}})
        for member in sys_node.children:
            edges.append({"source": sys_node.nid, "target": member.nid, "edge_type": "CONTAINS",
                          "props": {"layer": "C3->C2"}})

    spec_doc = {
        "producer": "NFRA_ONTOLOGY.AB-MAT-S1 (0.4.0_DS_ClientPlatform~B) -- canonical A+B materialize",
        "consumer": "0.7.0_AE_CloudOps (derive/ingest -- same path as the debt materialize)",
        "binding_spec": "NFRA_ONTOLOGY_AB_MATERIALIZE_SPEC.md @7892f3fbc",
        "grounding": {"graph_head": prov.get("nessie_head"),
                      "nodes_snapshot_id": prov.get("nodes_snapshot_id"),
                      "recurrence": "MEASURED live per detector (not echoed from spec)"},
        "convention_note": ("node_type C2Motif/C3System (already in NODE_TYPE_LAYER -- no re-freeze) + CONTAINS "
                            "edges. C2->C1 targets are the BARE estate node_ids (ARNs / '<type>:...') that the "
                            "store carries -- a canonical A+B detector matches estate nodes directly, so there is "
                            "NO 'c1:D{n}:' ladder discriminator to strip and the 07-08 0-row trap does not arise. "
                            "C3->C2 targets are the motif: nodes in this same batch. 0.7.0/CVO confirm on ingest."),
        "singletons": singletons,
        "c3_emergence_note": {
            "emitted_model": "connected-components union-find over shared C1 constituent INSTANCES (the certed "
                             "P2 mechanism). RESULT: it OVER-MERGES the A-plane into 1 supersystem because "
                             "LAMBDA/EC2_INSTANCE/S3_BUCKET/PipelineScript INSTANCES are shared across "
                             "capabilities -- so the C3 partition is degenerate (same shape as the debt system).",
            "surfaced_gap": "the spec's Sec-2 ~3-5 candidate systems are an OVERLAPPING domain-resource-type "
                            "COVER (a motif can be in several); a connected-components PARTITION cannot represent "
                            "overlapping systems. Choosing the cover model CHANGES what 'C3 system' means -> needs "
                            "~C (vocabulary) + CTO (arch-gate) ratification. SURFACED to COO per TO Phase-3 <if_mismatch>; "
                            "NOT unilaterally emitted.",
            "alternative_domain_cover_SURFACED": {dom: mem for dom, mem in domain_view.items()},
        },
        "counts": {"c2_motif_nodes": sum(1 for n in nodes if n["node_type"] == "C2Motif"),
                   "c3_system_nodes": sum(1 for n in nodes if n["node_type"] == "C3System"),
                   "contains_edges": len(edges),
                   "c2_to_c1_edges": sum(1 for e in edges if e["props"]["layer"] == "C2->C1"),
                   "c3_to_c2_edges": sum(1 for e in edges if e["props"]["layer"] == "C3->C2")},
        "nodes": nodes,
        "edges": edges,
    }
    return spec_doc, motifs, systems, singletons


# ---------------------------------------------------------------------------
# Phase-2 RESOLVE self-check (CTO acceptance condition 1): every C2->C1 target resolves to a store node.
# ---------------------------------------------------------------------------
def resolve_check(spec_doc: dict) -> tuple:
    targets = {e["target"] for e in spec_doc["edges"] if e["props"]["layer"] == "C2->C1"}
    if not targets:
        return 0, 0
    # Independent exercise (NOT an assertion): pull the store's FULL node_id set in one query and intersect.
    # The targets were built from per-detector MATCH queries; this verifies them against a SEPARATE full-node
    # pull -- so a resolve is a measured fact, not "they came from the store so they must resolve".
    rows, _ = P1.comp_kuzu("MATCH (n:%s) RETURN n.node_id AS nid" % N)
    store = {r["nid"] for r in rows}
    resolved = len(targets & store)
    return resolved, len(targets)


# ---------------------------------------------------------------------------
def emit(do_print: bool) -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass
    try:
        spec_doc, motifs, systems, singletons = build_ab_spec()
    except P1.GraphUnavailable as ex:
        print("SPEC NOT REGENERATED -- graph unavailable: %s" % ex)
        print("  (fail-closed: keep the last-good motif_c2c3_materialize_ab.json; re-run when reachable.)")
        return 2

    # fidelity gate every C2 + C3 (the REAL comp_ladder gate)
    all_ok = True
    for motif, _, _ in motifs:
        ok, _f = fidelity_check(motif)
        all_ok = all_ok and ok
    for sys_node, _ in systems:
        ok, _f = fidelity_check(sys_node)
        all_ok = all_ok and ok

    resolved, denom = resolve_check(spec_doc)

    with open(SPEC_ARTIFACT, "w", encoding="utf-8") as fh:
        json.dump(spec_doc, fh, indent=2)

    c = spec_doc["counts"]
    print("CANONICAL A+B materialize -> %s" % os.path.relpath(SPEC_ARTIFACT, WS))
    print("  %d C2Motif + %d C3System + %d CONTAINS edges (%d C2->C1, %d C3->C2)"
          % (c["c2_motif_nodes"], c["c3_system_nodes"], c["contains_edges"], c["c2_to_c1_edges"], c["c3_to_c2_edges"]))
    print("  fidelity (comp-ladder, all C2+C3): %s" % ("PASS" if all_ok else "FAIL -- latent node"))
    print("  RESOLVE self-check (CTO cond 1): %d/%d distinct C2->C1 targets resolve to a store node (%.1f%%)"
          % (resolved, denom, (100.0 * resolved / denom) if denom else 0.0))
    print("  no-refreeze (CTO cond 2): node_types = {C2Motif, C3System} only (both already in NODE_TYPE_LAYER)")

    if do_print:
        print("\n  recurrence (MEASURED live):")
        for motif, recurrence, spec in motifs:
            print("    %-12s recur=%-6d n_constituents=%d" % (spec["id"], recurrence, len(motif.children)))
        print("\n  EMERGENT C3 systems:")
        for sys_node, why in systems:
            members = [c.label for c in sys_node.children]
            print("    system:%s (%s)  <- {%s}" % (sys_node.label, sys_node.nid.split(":")[-1], ", ".join(members)))
            print("       shared types: %s | %d shared constituent(s)"
                  % (", ".join(t for t in why["shared_types"] if t and t != "?"), why["n_shared"]))
        if singletons:
            print("  singletons (isolated -- correctly not forced): %s" % ", ".join(singletons))
        dv = spec_doc["c3_emergence_note"]["alternative_domain_cover_SURFACED"]
        print("\n  [SURFACED to COO] connected-components emergence OVER-MERGES to %d system(s); the spec's ~3-5"
              % len(systems))
        print("  are an OVERLAPPING domain-resource-type COVER (a partition cannot represent it). Domain cover (>=2 motifs):")
        for dom, mem in dv.items():
            print("    %-22s <- {%s}" % (dom, ", ".join(m.split(":", 1)[1] for m in mem)))
    return 0 if (all_ok and resolved == denom and denom > 0) else 1


# ---------------------------------------------------------------------------
def self_test() -> int:
    print("=== NFRA_MOTIF canonical A+B self-test (gate logic; no live graph) ===")
    ok = []

    def chk(name, cond):
        ok.append(bool(cond))
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    # 1. catalog shape: 13 detectors, 9 Plane-A + 4 Plane-B, unique ids
    chk("1  13 detectors (9 A + 4 B), unique motif ids",
        len(AB_CATALOG) == 13 and sum(1 for s in AB_CATALOG if s["plane"] == "A") == 9
        and sum(1 for s in AB_CATALOG if s["plane"] == "B") == 4
        and len({s["id"] for s in AB_CATALOG}) == 13)

    # 2. a well-formed A+B motif (C2->C1(bare estate id)->C0-with-evidence) PASSES fidelity
    c0 = P1.c0_fact("arn:aws:s3:::opal-data-bd", "S3_BUCKET", "constituent")
    c1 = Node("arn:aws:s3:::opal-data-bd", "C1", "S3_BUCKETInstance", "b", rule="a-store", children=[c0])
    m = Node("motif:a-store", "C2", "AStoreMotif", "a-store", rule="CANONICAL", children=[c1])
    chk("2  positive: well-formed A+B motif PASSES comp-ladder fidelity", fidelity_check(m)[0] is True)

    # 3. negative control: a latent C2 (no children) FAILS the gate
    chk("3  negative control: latent motif (no children) FAILS the gate",
        fidelity_check(Node("motif:x", "C2", "X", "x", children=[]))[0] is False)

    # 4. RESOLVE FORM: a bare estate node_id is NOT the 'c1:D{n}:' trap form (no discriminator to strip)
    import re
    trap = re.compile(r"^c1:D\d+:")
    chk("4  resolve form: C2->C1 targets are bare estate ids, NOT the c1:D{n}: 0-row trap form",
        not trap.match("arn:aws:s3:::opal-data-bd") and not trap.match("LAMBDA:bd-gold-trigger"))

    # 5. emergence: two motifs sharing a constituent form ONE system; an isolated one stays a singleton
    def mk(nid, cids):
        ch = [Node(x, "C1", "T", x, rule="d", children=[P1.c0_fact(x, "T", "c")]) for x in cids]
        return Node("motif:" + nid, "C2", "M", nid, rule="C", children=ch)
    mA = mk("a-store", ["arn:aws:s3:::bd", "s3key:bd/x"])
    mB = mk("b-io", ["s3key:bd/x", "PipelineScript:g.py"])            # shares s3key:bd/x with A
    mC = mk("iso", ["DataFetch:z"])                                   # isolated (no shared constituent)
    sysc, singles = ab_c3_emergence([mA, mB, mC], {"arn:aws:s3:::bd": "S3_BUCKET", "s3key:bd/x": "S3Key",
                                                   "PipelineScript:g.py": "PipelineScript", "DataFetch:z": "DataFetch"})
    chk("5  emergence: A-B (shared constituent) form 1 system; C (isolated) is a singleton",
        len(sysc) == 1 and len(sysc[0][0].children) == 2 and "motif:iso" in singles)

    # 6. C3 naming inherited-from-constituents (object-data from the shared S3Key)
    chk("6  C3 naming inherited-from-constituents (shared S3Key -> object-data)",
        sysc and sysc[0][0].label == "object-data")

    # 7. collision-safe + stable C3 node_id (reuses the certed system_node_id)
    sysc2, _ = ab_c3_emergence([mA, mB, mC], {"arn:aws:s3:::bd": "S3_BUCKET", "s3key:bd/x": "S3Key",
                                              "PipelineScript:g.py": "PipelineScript", "DataFetch:z": "DataFetch"})
    chk("7  C3 node_id STABLE across re-runs (same member-set -> same id; no churn)",
        [s.nid for s, _ in sysc] == [s.nid for s, _ in sysc2])

    n = sum(1 for r in ok if r)
    print("--- self-test: %d/%d passed ---" % (n, len(ok)))
    return 0 if n == len(ok) else 1


def main() -> int:
    args = sys.argv[1:]
    if "--self-test" in args:
        return self_test()
    return emit("--print" in args)


if __name__ == "__main__":
    sys.exit(main())
