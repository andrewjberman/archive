#!/usr/bin/env python3
"""NFRA_CSE.P2 -- the algebra-primitive -> compiler COVERAGE SWEEP (the COMPUNIFY-wire, live).

AC1's "adding a primitive = a version-bump + a coverage-sweep (which compilers must now handle it)",
made a runnable gate. REUSES COMPUNIFY's proven comp_coverage_check DISCIPLINE (tri-state
PASS/FAIL/UNVERIFIABLE, never-false-clean, rule-registry+dispatcher) in a CSE-SIDE instrument --
NOT COMPUNIFY's ledger (that is comp-tools-one-home; THIS is algebra-primitive->compiler coverage, a
distinct concern -- CTO Q3 ruling). Registered as a producer in graph_contracts (0.5.0 constraint #6).

THE SWEEP: every structural algebra primitive (Entity / Relationship / EdgeKind) must be EMITTED by
>=1 registered compiler. A primitive no compiler emits = a coverage-GAP (fail-closed) -- a
MOTIF/PROMOTE candidate for a new recognizer, tracked, never a silent skip (LAW 1). This is the loop
that grows the algebra DELIBERATELY: a version-bump adds a primitive -> the sweep flags it un-emitted
until a compiler ships a recognizer for it -> then it clears.

LIVE SELF-DEMONSTRATION (schema 0.2): the CTO-ratified 0.2 EdgeKind bump {passthrough, rename,
recompute_guarded} is the first kind'd-edge capability -- NO compiler emits a kind yet (COMPILERKIT #2's
FLOWS_TO-with-kind is pending). So this sweep FLAGS EdgeKind as an open coverage-gap RIGHT NOW, and
CLEARS when #2's FLOWS_TO ships. The version-governance closing its own loop, runnably.

Compiler registry (P2): DERIVED from the grounded estate mappings (derive_runner.NODE_TYPE_LAYER
layer->compiler + cse_schema.CLOUDNODE_TYPE_TO_ENTITY / CLOUDEDGE_TO_RELATIONSHIP) -- NOT a
hand-maintained list (a hand-list DRIFTS -- the exact failure this sweep exists to catch, CTO Q2).
DURABLE FORM (flagged to COMPILERKIT 0.8.0~D): each Recognizer's SDK base carries `emits: [primitives]`
-> the registry becomes SDK-DERIVED (auto-current). This module structures for that migration:
compiler_emits() is the single seam a future SDK-declared source replaces.

Author: 0.4.0_DS_ClientPlatform~B   TO: NFRA_CSE.P2   Date: 2026-07-07
Status: DRAFT (CTO arch-gate PASS on the design; for CVO exercise-cert -- flags 0.2 EdgeKind gap,
clears on #2 FLOWS_TO). Canonical home on land = org/modules/graph/ (exec-lane; COO SoD-lands).
"""
from __future__ import annotations

import os
import sys

# Import the canonical algebra (0.2) + the grounded reconciliation mappings. Path-robust so this
# draft runs from the DS deliverables lane; a plain sibling import at the canonical home.
_GRAPH_MOD = os.path.join(os.path.dirname(__file__), "..", "..", "..", "modules", "graph")
if os.path.isdir(_GRAPH_MOD):
    sys.path.insert(0, os.path.abspath(_GRAPH_MOD))
import cse_schema as CSE  # noqa: E402

PASS, FAIL, UNVERIFIABLE = 0, 1, 2

# Register into the existing graph_contracts registry (0.5.0 constraint #6), not a new one.
PRODUCER_ID = f"nfra_cse_coverage_sweep@{CSE.SCHEMA_VERSION}"


# ===========================================================================
# THE COMPILER REGISTRY -- compiler-DECLARED, DERIVED from grounded estate mappings (not a hand-list).
#   layer -> compiler (grounded: derive_runner.NODE_TYPE_LAYER). aws/pipeline = the code/infra
#   compiler #1; portal = the TSX compiler #2; ms = the MS extractor. Each compiler's emitted
#   ENTITIES = the algebra entities its layer's node_types map to (via CLOUDNODE_TYPE_TO_ENTITY);
#   its RELATIONSHIPS from CLOUDEDGE_TO_RELATIONSHIP (edge producers). SEAM for the SDK migration:
#   replace compiler_emits() with the SDK-declared `Recognizer.emits` source; nothing else changes.
# ===========================================================================
_LAYER_TO_COMPILER = {
    "aws": "code-infra-compiler#1",
    "pipeline": "code-infra-compiler#1",
    "portal": "tsx-compiler#2",
    "ms": "ms-extractor#3",
}

# Which compiler emits which live edge_types (grounded assignment; the durable form is SDK-declared).
# Code/infra #1 emits the aws/data edges; TSX #2 the portal render/fetch/flow edges; MS #3 the ms edges.
_EDGE_TO_COMPILER = {
    # tsx-compiler#2 (portal render/data-flow)
    "RENDERS": "tsx-compiler#2", "FETCHES": "tsx-compiler#2", "SERVED_FROM": "tsx-compiler#2",
    "FLOWS_TO": "tsx-compiler#2", "PROP_PASSES": "tsx-compiler#2", "ROUTES_TO": "tsx-compiler#2",
    "HAS_PROP": "tsx-compiler#2", "HAS_FIELD": "tsx-compiler#2", "HAS_TYPE": "tsx-compiler#2",
    "HAS_PROPS_TYPE": "tsx-compiler#2", "REFERENCES_TYPE": "tsx-compiler#2", "IS_ENDPOINT": "tsx-compiler#2",
    "READS_FIELD": "tsx-compiler#2", "READS_URL": "tsx-compiler#2", "INSTANTIATES": "tsx-compiler#2",
    "ALIAS_TO": "tsx-compiler#2", "HAS_KEY": "tsx-compiler#2", "DECLARES": "tsx-compiler#2",
    "SHARES_SOURCE": "tsx-compiler#2",
    # ms-extractor#3
    "OWNED_BY": "ms-extractor#3", "MEMBER_OF": "ms-extractor#3", "HAS_ACCESS": "ms-extractor#3",
    "SHARED_WITH": "ms-extractor#3",
    # code-infra-compiler#1 (aws/data/code) -- everything else live
    "CALLS": "code-infra-compiler#1", "READS": "code-infra-compiler#1", "WRITES": "code-infra-compiler#1",
    "IMPORTS": "code-infra-compiler#1", "READS_S3": "code-infra-compiler#1", "WRITES_S3": "code-infra-compiler#1",
    "READS_SECRET": "code-infra-compiler#1", "LOGS_TO": "code-infra-compiler#1", "TRIGGERS": "code-infra-compiler#1",
    "NOTIFIES": "code-infra-compiler#1", "INVOKES": "code-infra-compiler#1", "PUBLISHES_TO": "code-infra-compiler#1",
    "SUBSCRIBES": "code-infra-compiler#1", "RUNS": "code-infra-compiler#1", "CONTAINS": "code-infra-compiler#1",
    "CONTAINS_DRILLDOWN": "code-infra-compiler#1", "CLUSTERS": "code-infra-compiler#1",
    "HAS_POLICY": "code-infra-compiler#1", "HAS_PROFILE": "code-infra-compiler#1", "HAS_ROUTE": "code-infra-compiler#1",
    "ASSUMES": "code-infra-compiler#1", "CAN_ASSUME": "code-infra-compiler#1", "GRANTS": "code-infra-compiler#1",
    "ENCRYPTS_WITH": "code-infra-compiler#1", "USES_OAC": "code-infra-compiler#1", "USES_OAI": "code-infra-compiler#1",
    "USES_SG": "code-infra-compiler#1", "IN_VPC": "code-infra-compiler#1", "MONITORS": "code-infra-compiler#1",
    "ORIGIN": "code-infra-compiler#1", "PROJECTS_TO": "code-infra-compiler#1", "DEAD_LETTERS_TO": "code-infra-compiler#1",
    "EMITS_TO": "code-infra-compiler#1",
}


def _load_node_type_layer() -> dict:
    """Grounded layer source: derive_runner.NODE_TYPE_LAYER (node_type -> layer). Best-effort;
    UNVERIFIABLE (loud) if unreadable -- never a silent empty registry."""
    gg = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "infra", "aws", "globgrph")
    gg = os.path.abspath(gg)
    if os.path.isdir(gg) and gg not in sys.path:
        sys.path.insert(0, gg)
    try:
        from derive_runner import NODE_TYPE_LAYER  # noqa: E402
        return dict(NODE_TYPE_LAYER)
    except Exception as ex:  # noqa: BLE001
        raise RuntimeError(f"could not load NODE_TYPE_LAYER (grounded layer source): {ex}")


def compiler_emits() -> dict:
    """THE SEAM (SDK-migration point): compiler_id -> {entities:set, relationships:set, edge_kinds:set}.

    DERIVED (P2) from the grounded estate mappings. Durable form = each Recognizer's SDK `emits`
    declaration replaces this function body; callers (coverage_sweep) are unchanged.
    """
    ntl = _load_node_type_layer()
    emits: dict = {}

    def _ensure(cid):
        emits.setdefault(cid, {"entities": set(), "relationships": set(), "edge_kinds": set()})
        return emits[cid]

    # Entities: each node_type -> its layer -> its compiler; the entity it maps to = that compiler emits it.
    for nt, ent in CSE.CLOUDNODE_TYPE_TO_ENTITY.items():
        layer = ntl.get(nt)
        cid = _LAYER_TO_COMPILER.get(layer)
        if cid:
            _ensure(cid)["entities"].add(ent.value)
    # Relationships: each live edge_type -> its compiler -> the algebra relationship it maps to.
    for et, rel in CSE.CLOUDEDGE_TO_RELATIONSHIP.items():
        cid = _EDGE_TO_COMPILER.get(et)
        if cid:
            _ensure(cid)["relationships"].add(rel.value)
    # Entity.CONCEPT is the LAW-1 UNIVERSAL honest-degrade target -- EVERY recognizer emits it BY
    # CONSTRUCTION (Concept(untyped)+low whenever it cannot lexically type a node). It is emitted-by-
    # design, never a coverage-gap. Before the 0.3 bump this was MASKED because "TypeDecl"->CONCEPT made
    # a node_type map to it; the 0.3 TypeDecl->TYPE remap EXPOSED that the node_type-derivation alone
    # would wrongly flag CONCEPT un-emitted. Model the degrade-fallback explicitly (a synthetic emitter).
    _ensure("_honest_degrade")["entities"].add(CSE.Entity.CONCEPT.value)
    # Entity.SYMBOL (0.3): emitted by the LIVE ts-morph/extract_api SYMBOL extractor -- a REAL existing
    # producer for symbol:-> nodes (the very nodes the 0.3 round-trip re-typed out of CONCEPT), just not
    # yet SDK-refactored onto the COMPILERKIT framework. COO ruling 2026-07-08 (GOV-A I1): attribute
    # SYMBOL to its REAL emitter (not fabricated, not the node_type-derivation which can't see prefixes),
    # so the primitive clears green HONESTLY. TRACKED FOLLOW-ON (loud, additive, NOT a silent skip):
    # extract_api SYMBOL extractor -> COMPILERKIT SDK `emits:[SYMBOL]` refactor (0.8.0~D). TYPE is
    # covered via TypeDecl->tsx-compiler#2 (and ~D emitted 136 TYPE nodes) -- also not a gap.
    _ensure("extract_api-symbol-extractor(live, pre-SDK-refactor)")["entities"].add(CSE.Entity.SYMBOL.value)
    # Edge-kinds: NO compiler declares emitting a kind yet (schema 0.2 fresh; COMPILERKIT #2's
    # FLOWS_TO-with-kind pending) -> edge_kinds stay EMPTY -> the sweep flags EdgeKind as a live gap.
    # When #2 ships, add its declared kinds here (or the SDK `emits` carries them) -> the gap clears.
    return emits


# ===========================================================================
# THE COVERAGE SWEEP (tri-state, never-false-clean -- the comp_coverage_check discipline, CSE-side)
# ===========================================================================
_FAMILIES = {
    "Entity": ("entities", lambda: CSE._ENTITY_VALUES),
    "Relationship": ("relationships", lambda: CSE._REL_VALUES),
    "EdgeKind": ("edge_kinds", lambda: getattr(CSE, "_EDGEKIND_VALUES", frozenset())),
}


def coverage_sweep(emits: dict = None) -> tuple:
    """Assert every structural algebra primitive is emitted by >=1 registered compiler.

    Returns (exit_code, gaps, note). PASS = every primitive emitted; FAIL = >=1 primitive no compiler
    emits (a coverage-GAP, named -- a MOTIF/PROMOTE candidate); UNVERIFIABLE = registry unreadable
    (loud, never a silent clean). Fail-closed: a gap is a FAIL, not a skip (LAW 1).
    """
    try:
        emits = compiler_emits() if emits is None else emits
    except Exception as ex:  # noqa: BLE001
        return UNVERIFIABLE, [], f"UNVERIFIABLE: compiler registry unreadable: {ex}"
    if not emits:
        return UNVERIFIABLE, [], "UNVERIFIABLE: empty compiler registry (never a silent clean)"

    gaps = []
    for fam, (key, values_fn) in _FAMILIES.items():
        emitted = set()
        for cid, decl in emits.items():
            emitted |= set(decl.get(key, set()))
        for prim in sorted(values_fn()):
            if prim not in emitted:
                gaps.append(f"{fam}:{prim} -- emitted by ZERO compiler (coverage-GAP; a recognizer must "
                            f"emit it OR it is a MOTIF/PROMOTE candidate for a new recognizer)")
    code = FAIL if gaps else PASS
    note = ("PASS: every algebra primitive emitted by >=1 compiler" if code == PASS
            else f"FAIL: {len(gaps)} primitive(s) with ZERO emitting compiler (coverage-gap, fail-closed)")
    return code, gaps, note


# ===========================================================================
# RUNNABLE SELF-TEST (CVO re-exercise) -- proves the sweep flags the live 0.2 EdgeKind gap + clears it.
# ===========================================================================
def _self_test() -> bool:
    ok = []

    def check(name, cond, detail=""):
        ok.append(cond)
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f"  -> {detail}" if (detail and not cond) else ""))

    print("=== NFRA_CSE.P2 coverage-sweep self-test (algebra-primitive -> compiler coverage) ===")
    code, gaps, note = coverage_sweep()
    print(f"  live sweep (schema {CSE.SCHEMA_VERSION}): {note}")

    # 1. the sweep runs tri-state (not UNVERIFIABLE -- the registry loaded)
    check("1  sweep loaded the grounded compiler registry (not UNVERIFIABLE)", code in (PASS, FAIL))
    # 2. the LIVE 0.2 EdgeKind gap is FLAGGED (the self-demonstration -- no compiler emits a kind yet)
    edgekind_gaps = [g for g in gaps if g.startswith("EdgeKind:")]
    check("2  flags the live 0.2 EdgeKind gap (self-demonstration: kinds un-emitted until #2 FLOWS_TO)",
          len(edgekind_gaps) >= 1, f"EdgeKind gaps found: {edgekind_gaps}")
    print(f"       (EdgeKind gaps: {[g.split(' -- ')[0] for g in edgekind_gaps]})")
    # 3. THE SWEEP IS FAIL-CLOSED + CORRECT: on the current estate it FINDS real coverage-gaps (the
    #    feature, not a bug). Characterize the EXPECTED gap set -- these are legitimate un-emitted
    #    primitives (org-level awaiting COMPILERKIT's org-artifact compilers + representation choices
    #    that tie to the live-graph grounding). The sweep correctly returns FAIL + NAMES them.
    #    Org-level entities no CODE compiler emits (Requirement/Tool/Tier/GraphScope) + IAMStatement
    #    (folded into IAM_POLICY, NOT a discrete node -- matches the AC4 grounding: no stmt: node live).
    #    0.3 RESOLUTION (COO ruling 2026-07-08): the version-bump's TYPE/SYMBOL both clear GREEN, not
    #    gaps -- TYPE covered (TypeDecl->tsx-compiler#2; ~D emitted 136 TYPE nodes), SYMBOL attributed to
    #    the LIVE extract_api SYMBOL extractor (a real emitter; SDK-refactor onto COMPILERKIT is a TRACKED
    #    follow-on, above), CONCEPT modeled always-emitted (honest-degrade). So the entity gaps return to
    #    the org-level set awaiting COMPILERKIT's org-artifact compilers -- the governance loop CLOSED
    #    honestly on a real bump (flagged -> real emitter found/attributed -> cleared, never fabricated).
    _EXPECTED_ENTITY_GAPS = {"Requirement", "Tool", "Tier", "GraphScope", "IAMStatement"}
    entity_gap_names = {g.split(" -- ")[0].split(":", 1)[1] for g in gaps if g.startswith("Entity:")}
    check("3  sweep flags the EXPECTED org-level/representation Entity gaps (fail-closed, correct)",
          entity_gap_names == _EXPECTED_ENTITY_GAPS,
          f"got {sorted(entity_gap_names)} expected {sorted(_EXPECTED_ENTITY_GAPS)}")
    # 4. Relationship gaps: org-level (derives_from/supersedes) + IAM-representation (denied/allowed/
    #    authenticates -- NOT live edge_types; deny is via HAS_POLICY -- matches the grounding).
    _EXPECTED_REL_GAPS = {"derives_from", "supersedes", "denied", "allowed", "authenticates"}
    rel_gap_names = {g.split(" -- ")[0].split(":", 1)[1] for g in gaps if g.startswith("Relationship:")}
    check("4  sweep flags the EXPECTED org-level/IAM-representation Relationship gaps (correct)",
          rel_gap_names == _EXPECTED_REL_GAPS,
          f"got {sorted(rel_gap_names)} expected {sorted(_EXPECTED_REL_GAPS)}")
    print(f"       (the {len(gaps)} live coverage-gaps are the SWEEP WORKING -- deliberate MOTIF/PROMOTE "
          f"candidates + COMPILERKIT org-artifact-compiler targets, fail-closed not silent)")
    # 5. the gap CLEARS when compiler #2 declares its FLOWS_TO kinds (simulate #2 shipping)
    sim = compiler_emits()
    sim["tsx-compiler#2"]["edge_kinds"] |= set(getattr(CSE, "_EDGEKIND_VALUES", frozenset()))
    code2, gaps2, _ = coverage_sweep(sim)
    check("5  EdgeKind gap CLEARS when #2 ships FLOWS_TO kinds (governance loop closes)",
          not [g for g in gaps2 if g.startswith("EdgeKind:")])

    passed = sum(1 for r in ok if r)
    print(f"=== {passed}/{len(ok)} PASS ===")
    return passed == len(ok)


if __name__ == "__main__":
    sys.exit(0 if _self_test() else 1)
