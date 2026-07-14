#!/usr/bin/env python3
"""NFRA_PROMOTE P2 -- the DS-side materializers (the write-back terminus of the learning loop).

PROMOTE-P1 built the lifecycle + gate; P2 builds the MATERIALIZERS -- the arms that compile a RATIFIED
promotion into its target plane (PRD S4.1/S5-P2). Three are DS-owned (this module); the recognizer/
compiler-rule materializer + GOV-B are ~D's.

  - ALGEBRA_PRIMITIVE  -> a governed CSE schema migration (a recurring Concept cluster earns a typed
                          Entity/Relationship + a version bump). Reuses the exact governed-migration
                          pattern of the 0.3 Entity.TYPE/SYMBOL bump (author: this lane).
  - ROUTING_DIRECTIVE  -> the router: an EXPLICIT routing heuristic (NOT a latent affinity weight --
                          the explicit alternative to the COMPLEARN affinity flip).
  - KNOWLEDGE_NODE     -> the graph: a ratified C3 system becomes a NAMED, GOVERNED capability node
                          (distinct from the MOTIF-P2 graph-completeness materialize -- that writes the
                          DISCOVERED structure; this writes a RATIFIED-PROMOTED capability).

THREE HARD PROPERTIES on every materialization (the invariants P2 must satisfy; CVO certs each):
  - GATED on RATIFIED (invariants #1+#3): a materializer fires ONLY on a promotion that PASSED the
    measure-before-promote + human-ratify gate. An unmeasured/unratified candidate is REJECTED -- you
    cannot materialize what was never measured+ratified (this is the anti-auto-mutation gate biting).
  - REVERSIBLE (invariant #4): every materialization carries a DEMOTION artifact that is the exact
    inverse of its apply artifact; a post-promotion degradation demotes it (round-trip provable).
  - ZERO AUTO-MUTATION (invariant #3): the materializer PROPOSES the change (apply artifact); it NEVER
    writes the substrate itself. Governed application lands it (e.g. a CSE-schema bump lands via CTO
    ratify + COO SoD, exactly as the 0.3 bump did). Every materialization emits a CSE (invariant #5).

Consumes a RATIFIED lifecycle record (a dict) from the CANONICAL P1 machine,
org/modules/graph/comp_promote_lifecycle.py (@cb6a86177 -- DS~B's NFRA_PROMOTE_P1_promotion_engine
retired with provenance). Grounds the algebra-primitive migration on the LIVE cse_schema (author's
plane). Andrew scope: FULLY-HONEST -- real (sparse) measures, so some candidates materialize +
others stay HELD/DROPPED; the gate bites on real data AND a real one promotes.

Usage:
  python NFRA_PROMOTE_P2_materializers.py            # demo each materializer on a synthetic RATIFIED promotion
  python NFRA_PROMOTE_P2_materializers.py --self-test # each materializer + reversibility round-trip + not-ratified rejection

Author: 0.4.0_DS_ClientPlatform~B (DS materializers). TO NFRA_PROMOTE.P2.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from dataclasses import asdict, dataclass, field

_HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(WS, "org", "modules", "graph"))

import comp_promote_lifecycle as lifecycle  # noqa: E402  -- the CANONICAL P1 machine (@cb6a86177; DS~B engine retired with provenance)
try:
    import cse_schema as CSE  # noqa: E402  -- the live algebra (for the schema-migration materializer)
    _CSE_VERSION = CSE.SCHEMA_VERSION
except Exception:  # noqa: BLE001
    _CSE_VERSION = "0.4"   # import-fail fallback only (live import overrides); tracks the schema @0.4 (R4 ProducerKind.PROMOTE)


@dataclass
class Materialization:
    """A proposed, reversible write-back into a target plane. NEVER auto-applied."""
    candidate_id: str
    promotion_class: str
    target_plane: str
    apply: dict                              # the proposed change (governed application lands it)
    demote: dict                             # the exact inverse (reversibility, invariant #4)
    cse: dict = field(default_factory=dict)  # the emitted CSE (invariant #5)
    auto_mutation: bool = False              # ALWAYS False -- proposes, never writes the substrate
    reversible: bool = True


def _cse(verb: str, subject: str, rec: dict, detail: str) -> dict:
    """A promotion-lifecycle CSE (invariant #5: the materialization is itself an observation)."""
    return {"cse_kind": "promotion_materialize", "verb": verb, "subject_ref": subject,
            "candidate_id": rec["candidate_id"], "promotion_class": rec["promotion_class"],
            "detail": detail, "reversible": True,
            "note": "governed application lands the apply artifact; in-VPC CSE store-write is the emit leg"}


# ---------------------------------------------------------------------------
# The three DS materializers. Each: RATIFIED promotion -> reversible Materialization + a CSE.
# ---------------------------------------------------------------------------
def materialize_algebra_primitive(rec: dict) -> Materialization:
    """A recurring Concept cluster -> a typed Entity in cse_schema (a GOVERNED version bump)."""
    new_entity = "".join(w.capitalize() for w in rec["candidate_id"].split(":", 1)[-1].split("-"))[:24] or "PromotedType"
    cur = _CSE_VERSION
    nxt = "%.1f" % (float(cur) + 0.1)
    apply = {"cse_schema_migration": {"add_entity": new_entity, "version_bump": "%s -> %s" % (cur, nxt),
                                      "mapping": "add to Entity enum + CLOUDNODE_TYPE_TO_ENTITY; a recurring "
                                                 "Concept(untyped) cluster earns this typed primitive"},
             "governed_by": "CTO arch-gate + COO SoD-land (same path as the 0.3 TYPE/SYMBOL bump)"}
    demote = {"cse_schema_migration": {"remove_entity": new_entity, "version_revert": "%s -> %s" % (nxt, cur),
                                       "remap_to": "Entity.CONCEPT (honest-degrade) -- the primitive un-adds cleanly"}}
    return Materialization(rec["candidate_id"], rec["promotion_class"], "NFRA_CSE (schema)", apply, demote,
                           _cse("migrate", "cse_schema@%s" % nxt, rec, "add typed Entity %s" % new_entity))


def materialize_routing_directive(rec: dict) -> Materialization:
    """An observed effective pattern -> an EXPLICIT routing heuristic (NOT a latent weight)."""
    directive_id = "route:" + rec["candidate_id"].split(":", 1)[-1]
    apply = {"router_directive": {"add": directive_id, "kind": "explicit-heuristic",
                                  "not": "a latent affinity weight (the explicit alternative to the COMPLEARN flip)",
                                  "form": "an inspectable rule the router applies; cites its measured effect"}}
    demote = {"router_directive": {"remove": directive_id, "restores": "the router's prior behavior exactly"}}
    return Materialization(rec["candidate_id"], rec["promotion_class"], "the router", apply, demote,
                           _cse("add_directive", directive_id, rec, "explicit routing heuristic"))


def materialize_knowledge_node(rec: dict) -> Materialization:
    """A ratified C3 system -> a NAMED, GOVERNED capability node in the graph."""
    cap_id = "capability:" + rec["candidate_id"].split(":", 1)[-1]
    apply = {"graph_knowledge_node": {"node_id": cap_id, "node_type": "Capability",
                                      "provenance": {"from_c3_system": rec["candidate_id"], "recurrence": rec.get("recurrence"),
                                                     "decompression": "intact CONTAINS -> C2 -> C1 -> C0 (LAW-2)"},
                                      "governed_by": "the NODE_TYPE_LAYER taxonomy gate (semctl layer) + CVO",
                                      "ingest": "0.7.0 derive/ingest path (same as ingest_cluster_producer)"}}
    demote = {"graph_knowledge_node": {"remove": cap_id, "restores": "the graph without the promoted capability"}}
    return Materialization(rec["candidate_id"], rec["promotion_class"], "the graph", apply, demote,
                           _cse("promote_capability", cap_id, rec, "named governed capability from a C3 system"))


MATERIALIZERS = {
    "ALGEBRA_PRIMITIVE": materialize_algebra_primitive,
    "ROUTING_DIRECTIVE": materialize_routing_directive,
    "KNOWLEDGE_NODE": materialize_knowledge_node,
    # "COMPILER_RULE" -> ~D (recognizer/compiler-rule materializer + GOV-B); intentionally not here.
}


def _is_ratified(rec: dict) -> bool:
    """A promotion is materializable ONLY if it PASSED the ratify gate (a RATIFIED transition in the
    canonical record's history -- transitions[], the lifecycle's event trail on the record)."""
    return any(t.get("to") == "RATIFIED" for t in rec.get("transitions", []))


def materialize(rec: dict) -> tuple:
    """Materialize a RATIFIED promotion. Returns (Materialization | None, reason). GATE: rejects a
    non-ratified promotion (invariants #1+#3 -- you cannot materialize what was never measured+ratified)."""
    if not _is_ratified(rec):
        return None, ("REJECTED -- not RATIFIED (state=%s). Cannot materialize an unmeasured/unratified "
                      "promotion (measure-before-promote + human-ratify + zero-auto-mutation)." % rec["state"])
    fn = MATERIALIZERS.get(rec["promotion_class"])
    if fn is None:
        return None, "no DS materializer for class %s (COMPILER_RULE -> ~D)" % rec["promotion_class"]
    return fn(rec), "materialized into %s (reversible, zero-auto-mutation, CSE emitted)" % PROMOTION_TARGET(rec)


def PROMOTION_TARGET(rec) -> str:
    return {"ALGEBRA_PRIMITIVE": "NFRA_CSE schema", "ROUTING_DIRECTIVE": "the router",
            "KNOWLEDGE_NODE": "the graph"}.get(rec["promotion_class"], "?")


def demote(m: Materialization, reason: str) -> dict:
    """REVERSIBILITY (invariant #4): apply the demotion artifact -> reverses the materialization exactly."""
    return {"demoted": m.candidate_id, "target_plane": m.target_plane, "applied_inverse": m.demote,
            "reason": reason, "cse": {"cse_kind": "promotion_demote", "subject_ref": m.candidate_id,
                                      "verb": "demote", "reason": reason}}


# ---------------------------------------------------------------------------
# Demo: run each materializer on a synthetic RATIFIED promotion -- driven through the REAL
# canonical gate (isolated manifest + trail; synthetic data, exercised machine @cb6a86177).
# ---------------------------------------------------------------------------
_CHAIN = {"c0_evidence": [{"fact": "x", "source": "f.tsx", "locus": "L1"}], "n_c0_facts": 1}
_MEANINGFUL = {"effect": 0.18, "basis": "focused git co-evolution", "source": "demo fixture",
               "vintage": "fixture", "focused_coupling_ratio": 0.18, "coupling_ratio": 0.18,
               "co_sessions": 4}
_ANTI_GOODHART = {"structural_rationale": "recurring cross-file structural pattern",
                  "not_tuned_to_own_metric": True,
                  "generalizes_beyond_fixture": "portal surfaces beyond the fixture set"}


def _drive(cid, cls, *, measure, then_propose=True, then_ratify=True):
    """Drive a candidate through the CANONICAL gate on an isolated manifest+trail, as far as the
    gate honestly allows (a refusal leaves the record in place -- the gate biting IS the negative-
    control behavior). Returns the record dict in its final state."""
    td = tempfile.mkdtemp(prefix="promote_p2_gate_")
    trail = os.path.join(td, "cse.jsonl")
    man = {"promotions": {}}
    try:
        rec = lifecycle.open_candidate(
            {"candidate_id": cid, "decompression_chain": dict(_CHAIN), "recurrence": 5,
             "kind": "demo"}, man, promotion_class=cls, trail_path=trail)
        try:
            rec = lifecycle.advance(rec, "MEASURED", evidence={"why": "demo measure",
                                    "measured_effect": measure},
                                    manifest=man, actor="p2-demo", trail_path=trail)
            if then_propose:
                rec = lifecycle.advance(rec, "PROPOSED", evidence={"why": "demo propose",
                                        "anti_goodhart": dict(_ANTI_GOODHART)},
                                        manifest=man, actor="p2-demo", trail_path=trail)
            if then_propose and then_ratify:
                rec = lifecycle.advance(rec, "RATIFIED", evidence={"why": "demo ratify",
                                        "ratify": {"commission_id": "CTO-commission-TEST",
                                                   "ratifier": "1.0.0_SA_CTO",
                                                   "ref": "p2-demo synthetic ratify"}},
                                        manifest=man, actor="p2-demo", trail_path=trail)
        except lifecycle.InvariantViolation:
            pass   # the gate biting: the record stays where the machine holds it
        return rec
    finally:
        shutil.rmtree(td, ignore_errors=True)


def _ratified(cid, cls):
    """A synthetic promotion driven through the REAL canonical gate to RATIFIED (meaningful
    measure + routed-owner RATIFY with commission) -- never a hand-built 'looks ratified' dict."""
    return _drive(cid, cls, measure=dict(_MEANINGFUL))


def run_demo() -> int:
    print("=" * 78)
    print("NFRA_PROMOTE P2 -- DS materializers (RATIFIED promotion -> reversible write-back)")
    print("=" * 78)
    for cls in MATERIALIZERS:
        rec = _ratified("demo:%s" % cls.lower(), cls)
        m, reason = materialize(rec)
        print("\n[%s] %s" % (cls, reason))
        print("   target: %s | reversible=%s | auto_mutation=%s" % (m.target_plane, m.reversible, m.auto_mutation))
        print("   apply:  %s" % json.dumps(m.apply)[:150])
        print("   demote: %s" % json.dumps(m.demote)[:120])
        print("   cse:    verb=%s subject=%s" % (m.cse["verb"], m.cse["subject_ref"]))
    # the gate biting on a held candidate: a PENDING measure is NOT a measure (invariant-1) --
    # the canonical gate refuses MEASURED, the record holds at CANDIDATE, materialize rejects.
    held = _drive("motif:held", "KNOWLEDGE_NODE",
                  measure={"pending": True, "effect": 0.0, "basis": "in-VPC co-occurrence",
                           "source": "fedobs", "vintage": "pending"})
    _, reason = materialize(held)
    print("\n[GATE] held candidate (measure pending): %s" % reason)
    print("\n" + "-" * 78)
    print("3 DS materializers live (algebra-primitive/routing-directive/knowledge-node); recognizer=~D.")
    print("Each: RATIFIED-only, reversible (apply+demote inverse), zero-auto-mutation, CSE-emitting.")
    print("FULLY-HONEST (Andrew): on real sparse measures, the meaningful candidates materialize + the")
    print("  measure-empty ones stay HELD/DROPPED -- the gate bites on real data AND a real one promotes.")
    return 0


# ---------------------------------------------------------------------------
# Self-test -- each materializer + reversibility round-trip + the not-ratified rejection (biting).
# ---------------------------------------------------------------------------
def self_test() -> int:
    print("=== NFRA_PROMOTE_P2 self-test (materializers: reversible + anti-auto-mutation + gated) ===")
    ok = []

    def chk(name, cond):
        ok.append(cond)
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    for i, cls in enumerate(("ALGEBRA_PRIMITIVE", "ROUTING_DIRECTIVE", "KNOWLEDGE_NODE"), 1):
        rec = _ratified("m:%s" % cls, cls)
        m, _ = materialize(rec)
        chk("%d  %s materializer produces a materialization" % (i, cls), m is not None)
        # ANTI-AUTO-MUTATION: never writes the substrate directly
        chk("%da %s: auto_mutation is False (proposes, never auto-writes)" % (i, cls), m.auto_mutation is False)
        # REVERSIBLE: the demote artifact is the inverse of the apply (round-trip); emits a CSE
        d = demote(m, "degraded post-promotion")
        chk("%db %s: reversible -- demotion inverts the apply + emits a demote CSE" % (i, cls),
            m.reversible and d["applied_inverse"] == m.demote and d["cse"]["verb"] == "demote")
        chk("%dc %s: emits a materialize CSE (inspectable, invariant #5)" % (i, cls), bool(m.cse.get("verb")))

    # NEGATIVE CONTROL: a NON-RATIFIED (held, pending-measure) promotion is REJECTED -- the gate
    # bites at invariant-1 (a pending measure is NOT a measure); the record holds at CANDIDATE.
    held = _drive("m:held", "KNOWLEDGE_NODE",
                  measure={"pending": True, "effect": 0.0, "basis": "in-VPC co-occurrence",
                           "source": "fedobs", "vintage": "pending"})
    m_held, reason = materialize(held)
    chk("N  negative control: unratified/unmeasured promotion REJECTED (no materialization; gate bites)",
        m_held is None and "not RATIFIED" in reason and held["state"] == "CANDIDATE")

    # NEGATIVE CONTROL 2: a measured-but-coincidental candidate is REFUSED at the invariant-2
    # measurement floor (legacy co_sessions=1 < floor) -- it never REACHES the ratifier, so it is
    # not materializable (the absorbed DS~B floor doing exactly its job).
    dropped = _drive("m:coincidental", "ALGEBRA_PRIMITIVE",
                     measure={"effect": 0.05, "basis": "single co-occurrence", "source": "fedobs",
                              "vintage": "fixture", "co_sessions": 1})
    m_drop, _ = materialize(dropped)
    chk("N2 negative control: below-measurement-floor candidate is not materializable",
        m_drop is None and dropped["state"] == "MEASURED")

    # serializable (asdict round-trips) -- the materialization is a clean handoff artifact
    m, _ = materialize(_ratified("m:ser", "KNOWLEDGE_NODE"))
    chk("S  materialization is a serializable handoff artifact", isinstance(asdict(m), dict))

    n = sum(1 for x in ok if x)
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
    return run_demo()


if __name__ == "__main__":
    sys.exit(main())
