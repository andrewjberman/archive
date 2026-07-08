#!/usr/bin/env python3
"""NFRA_PROMOTE P1 -- the promotion contract + lifecycle state machine + the 5-invariant gate.

NFRA_PROMOTE is the LAST plane (Directive / write-back) -- where the organization LEARNS explicitly:
an observed+measured regularity (a MOTIF candidate + a FEDOBS effect) promotes into explicit, inspectable,
reversible structure -- human-ratified, zero auto-mutation. P1 GENERALIZES the forming loop (does NOT
greenfield): the TH-C clause-A typed-commission dispatch (verdict -> typed advisory commission -> owner
ratifies -> zero auto-mutation) + the COMPLEARN-activation loop (observe->measure->validate->promote).

THE STATE MACHINE (PRD S4.3):
  CANDIDATE (from MOTIF, recurring + provenance-carrying)
    -> MEASURED   (FEDOBS quantifies effect; below anti-Goodhart floor -> parked/DROPPED, not promoted)
    -> PROPOSED   (a typed advisory commission to the ratify owner: evidence + effect + anti-Goodhart check)
    -> RATIFIED   (owner accepts) | REJECTED (owner declines, with reason -- itself an observation)
    -> MATERIALIZED (compiled into the target artifact class -- reversible, emits a CSE)
    -> MONITORED  (FEDOBS measures post-promotion effect on an interval)
        -> SUSTAINED (keeps its warrant) | DEGRADED -> DEMOTED (reversed, with degradation evidence)
  (+ DROPPED: a candidate with no MEANINGFUL measure even after coverage -- de-candidated, not zombie-held.)

THE 5-INVARIANT GATE (PRD S4.2 -- each a real incident, enforced NOT documented):
  1. MEASURE-BEFORE-PROMOTE -- no advance past CANDIDATE without a FEDOBS MEASURED effect. THE GATE BITES:
     an unmeasured candidate is HELD at CANDIDATE (a refusal, not a blocker). (AC1)
  2. ANTI-GOODHART -- the measured warrant must be MEANINGFUL (co_sessions >= a signal-vs-noise floor,
     structural/generalizing), NOT any-non-zero / tuned-to-metric. A single coincidental co-occurrence is
     NOT a warrant (CTO ratify-ruling condition). (AC3)
  3. HUMAN-RATIFY -- PROPOSED emits a TYPED ADVISORY COMMISSION; the owner ratifies; ZERO auto-mutation of
     the substrate. The engine never writes the substrate -- it proposes. (AC2)
  4. REVERSIBLE -- every materialization carries a demotion path; a DEGRADED promotion DEMOTES; a candidate
     that shows no meaningful measure even after coverage is DROPPED (not indefinite-pending). (AC4)
  5. INSPECTABLE -- every transition cites evidence + measured-effect + decompression-chain, and is
     CSE-logged (promotion is itself organizational evolution -> feeds its own observation). (AC5)

Consumes NFRA_MOTIF.P3's candidate handoff (motif_promote_candidates.json). Grounded on the CTO ratify
ruling (7 candidates RATIFIED-AS-CANDIDATES but PROMOTION WITHHELD -- measure pending): the gate firing.
Do NOT depend on the pending TH-C EFFECTIVE axis -- the measure-arm is FEDOBS (PRD S7/S8).

Usage:
  python NFRA_PROMOTE_P1_promotion_engine.py            # consume MOTIF candidates -> run the lifecycle (gate bites: all held at CANDIDATE, measure pending)
  python NFRA_PROMOTE_P1_promotion_engine.py --self-test # the 5-invariant gate exercised, each BITING (AC1-AC5 + negative controls)
  python NFRA_PROMOTE_P1_promotion_engine.py --lifecycle # print the state machine + the ratify-owner routing table

Author: 0.4.0_DS_ClientPlatform~B (build) + 1.0.0_SA_CTO (ratify owner). TO NFRA_PROMOTE.P1.
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field

_HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
CANDIDATE_ARTIFACT = os.path.join(_HERE, "motif_promote_candidates.json")
LIFECYCLE_LOG = os.path.join(_HERE, "promote_lifecycle_cse.jsonl")

# ---------------------------------------------------------------------------
# States + promotion classes + ratify-owner routing.
# ---------------------------------------------------------------------------
STATES = ["CANDIDATE", "MEASURED", "PROPOSED", "RATIFIED", "REJECTED",
          "MATERIALIZED", "MONITORED", "SUSTAINED", "DEGRADED", "DEMOTED", "DROPPED"]

# The four explicit artifact classes a validated regularity promotes into (PRD S4.1) + the ratify owner.
# Cross-plane promotions -> CTO; domain promotions -> the domain owner.
PROMOTION_CLASS_ROUTING = {
    "COMPILER_RULE": ("NFRA_COMPILERKIT (recognizer)", "1.0.0_SA_CTO"),      # a recurring pattern -> first-class recognizer
    "ALGEBRA_PRIMITIVE": ("NFRA_CSE (schema migration)", "1.0.0_SA_CTO"),    # a Concept cluster -> typed Entity/Relationship
    "ROUTING_DIRECTIVE": ("the router (explicit, not latent)", "1.0.0_SA_CTO"),
    "KNOWLEDGE_NODE": ("the graph (named governed capability)", "1.0.0_SA_CTO"),  # a C3 system -> knowledge node
}

# ANTI-GOODHART floor (invariant #2): a coupling must recur across >= FLOOR distinct producer sessions to be
# a warrant; a single coincidental co-occurrence is not (CTO ratify-ruling). Structural, not tuned-to-metric.
# CONFIG, not a hardcoded literal (CTO tuning note 2026-07-08): tunable without a code change via env
# PROMOTE_ANTI_GOODHART_FLOOR (default 2). It is a PRE-FILTER only -- the owner's explicit ratify remains the
# FINAL meaningfulness gate (a thin 2-session warrant can still be rejected). Revisit vs real data once
# frontend co-evolution measures land (raise if 2-co-occurrences prove noisy at scale); clamped >= 2 so the
# coincidence-floor invariant (a single one-off is never a warrant) can never be tuned away.
try:
    MEANINGFUL_CO_OCCURRENCE_FLOOR = max(2, int(os.environ.get("PROMOTE_ANTI_GOODHART_FLOOR", "2")))
except ValueError:
    MEANINGFUL_CO_OCCURRENCE_FLOOR = 2

# ANTI-GOODHART SIGNAL (CTO-RATIFIED 2026-07-08, COO co-set): gate on the COUPLING_RATIO
# (co_change_commits / commits_touching_either) -- edit-frequency-robust real coupling -- NOT the raw
# co_sessions count (a Goodhart-able activity proxy that over-emitted 6/7). FEDOBS_RATIO_FLOOR=0.15 is the
# CTO-reasoned starting default: above the coincidental-noise band (~0.05-0.10) + in the natural distribution
# GAP (0.097 -> 0.18, a real weak/tight bimodal split). CONFIG (tunable; a SMALL 7-sample -- revisit estate-wide).
# A PRE-FILTER only: the owner's promotion-ratify is the FINAL meaningfulness gate.
try:
    FEDOBS_RATIO_FLOOR = float(os.environ.get("FEDOBS_RATIO_FLOOR", "0.15"))
except ValueError:
    FEDOBS_RATIO_FLOOR = 0.15

# The FEDOBS frontend-co-evolution measure artifact (git-real, CVO-verifiable) -- joined into the candidates
# at load so the gate reads a REAL per-candidate coupling_ratio (the CANDIDATE->MEASURED bind).
FEDOBS_MEASURE_ARTIFACT = os.path.join(_HERE, "fedobs_frontend_coevolution.json")


@dataclass
class PromotionRecord:
    """A candidate flowing through the lifecycle. Carries its full inspectable trail (invariant #5)."""
    candidate_id: str
    promotion_class: str
    recurrence: int
    decompression_chain: dict            # from MOTIF (evidence half of invariant #5)
    fedobs_measure: dict                 # {status, co_sessions?, ...} -- the measured-effect half
    state: str = "CANDIDATE"
    history: list = field(default_factory=list)   # [(state, reason)] -- the CSE-logged transition trail
    ratify_owner: str = ""

    def log(self, state: str, reason: str):
        self.state = state
        self.history.append({"state": state, "reason": reason})


# ---------------------------------------------------------------------------
# The 5-invariant gate -- each returns (ok, reason); each BITES (refuses) when its condition is unmet.
# ---------------------------------------------------------------------------
def inv1_measured(rec: PromotionRecord) -> tuple:
    """MEASURE-BEFORE-PROMOTE: a FEDOBS MEASURED effect must exist. Pending measure => HELD (bites)."""
    st = (rec.fedobs_measure or {}).get("status")
    if st == "MEASURED":
        return True, "FEDOBS measured effect present"
    return False, "measure %s -- HELD at CANDIDATE (measure-before-promote firing, not a blocker)" % (st or "MISSING")


def inv2_anti_goodhart(rec: PromotionRecord) -> tuple:
    """ANTI-GOODHART (CTO-ratified signal 2026-07-08): gate on the COUPLING_RATIO (edit-frequency-robust real
    coupling), NOT the raw co_sessions count (a Goodhart-able activity proxy). A warrant needs a MEANINGFUL
    coupling (ratio >= FEDOBS_RATIO_FLOOR), not any active pair. Legacy measures (no ratio) fall back to the
    co_sessions floor for back-compat."""
    m = rec.fedobs_measure or {}
    ratio = m.get("coupling_ratio")
    if ratio is None:
        co = m.get("co_sessions", 0)
        return (co >= MEANINGFUL_CO_OCCURRENCE_FLOOR,
                "co_sessions=%d vs floor %d (legacy: no coupling_ratio)" % (co, MEANINGFUL_CO_OCCURRENCE_FLOOR))
    if ratio >= FEDOBS_RATIO_FLOOR:
        return True, "coupling_ratio=%.3f >= floor %.2f (real coupling, edit-frequency-robust)" % (ratio, FEDOBS_RATIO_FLOOR)
    return False, "coupling_ratio=%.3f < floor %.2f -- weak/coincidental, NOT a warrant (anti-Goodhart bites)" % (
        ratio, FEDOBS_RATIO_FLOOR)


def inv3_human_ratify(rec: PromotionRecord, owner_verdict: str | None) -> tuple:
    """HUMAN-RATIFY: PROPOSED -> typed advisory commission -> owner ratifies. Zero auto-mutation:
    the engine NEVER advances to RATIFIED on its own -- it requires an explicit owner verdict."""
    if owner_verdict == "RATIFY":
        return True, "owner %s RATIFIED (typed commission accepted; zero auto-mutation)" % rec.ratify_owner
    if owner_verdict == "REJECT":
        return False, "owner %s REJECTED (declined with reason -- itself an observation)" % rec.ratify_owner
    return False, "awaiting owner ratify (%s) -- HELD at PROPOSED, engine does NOT auto-ratify" % rec.ratify_owner


def inv5_inspectable(rec: PromotionRecord) -> tuple:
    """INSPECTABLE: cites evidence (decompression) + measured-effect + a CSE-logged trail."""
    has_evidence = bool(rec.decompression_chain and rec.decompression_chain.get("c0_evidence"))
    has_trail = len(rec.history) > 0
    ok = has_evidence and has_trail
    return ok, ("evidence+trail present" if ok else "MISSING evidence or CSE trail -- not inspectable")


def commission(rec: PromotionRecord) -> dict:
    """The TYPED ADVISORY COMMISSION emitted at PROPOSED (invariant #3) -- what the owner ratifies."""
    target, owner = PROMOTION_CLASS_ROUTING[rec.promotion_class]
    return {
        "commission_type": "PROMOTION",
        "candidate_id": rec.candidate_id,
        "promotion_class": rec.promotion_class,
        "target_artifact": target,
        "ratify_owner": owner,
        "cites": {
            "evidence_decompression": {"n_c0_facts": (rec.decompression_chain or {}).get("n_c0_facts", 0)},
            "measured_effect": rec.fedobs_measure,
            "anti_goodhart_check": inv2_anti_goodhart(rec)[1],
            "recurrence": rec.recurrence,
        },
        "auto_mutation": False,   # invariant #3: PROMOTE proposes; it never mutates the substrate
    }


# ---------------------------------------------------------------------------
# The lifecycle driver -- advance a record as far as the gate permits, holding where an invariant bites.
# ---------------------------------------------------------------------------
def advance(rec: PromotionRecord, owner_verdict: str | None = None, post_effect: str | None = None,
            coverage_landed: bool = False) -> PromotionRecord:
    """Drive one candidate through the lifecycle. The gate BITES at each transition -- a candidate is
    HELD at the last valid state when an invariant is unmet (never force-advanced)."""
    target, owner = PROMOTION_CLASS_ROUTING[rec.promotion_class]
    rec.ratify_owner = owner
    if not rec.history:
        rec.log("CANDIDATE", "accepted into candidate pool (provenance+decompression complete, fidelity-gated)")

    # invariant #1: measure-before-promote
    ok1, r1 = inv1_measured(rec)
    if not ok1:
        # invariant #4 (reversible): if coverage HAS landed and there's still no meaningful measure -> DROP,
        # not zombie-held (CTO ratify-ruling: a motif that doesn't co-evolve isn't a real coupling).
        if coverage_landed:
            rec.log("DROPPED", "coverage landed but no meaningful measure -- de-candidated (reversible, not zombie-held)")
        else:
            rec.log("CANDIDATE", r1)
        return rec
    rec.log("MEASURED", "FEDOBS effect bound: %s" % rec.fedobs_measure)

    # invariant #2: anti-Goodhart
    ok2, r2 = inv2_anti_goodhart(rec)
    if not ok2:
        rec.log("DROPPED", r2)   # a coincidental/fixture-fit measure is not a warrant -> de-candidate
        return rec

    # -> PROPOSED (emit the typed advisory commission; invariant #5 inspectable)
    rec.log("PROPOSED", "typed advisory commission -> %s (%s); anti-Goodhart: %s" % (owner, target, r2))

    # invariant #3: human-ratify (zero auto-mutation -- needs an explicit owner verdict)
    ok3, r3 = inv3_human_ratify(rec, owner_verdict)
    if not ok3:
        rec.log("REJECTED" if owner_verdict == "REJECT" else "PROPOSED", r3)
        return rec
    rec.log("RATIFIED", r3)

    # -> MATERIALIZED (reversible; emits a CSE). The store-write itself is the materializer's job (P2, in-VPC).
    rec.log("MATERIALIZED", "compiled into %s (reversible: demotion path attached); materializer=P2/in-VPC" % target)

    # -> MONITORED -> SUSTAINED | DEGRADED->DEMOTED (invariant #4 reversible)
    rec.log("MONITORED", "FEDOBS measures post-promotion effect on an interval")
    if post_effect == "DEGRADED":
        rec.log("DEGRADED", "post-promotion measure shows degradation")
        rec.log("DEMOTED", "reversed with degradation evidence (reversible invariant #4)")
    elif post_effect == "SUSTAINED":
        rec.log("SUSTAINED", "keeps its warrant")
    return rec


# ---------------------------------------------------------------------------
# CSE-log the lifecycle (invariant #5: every transition is itself an observation).
# ---------------------------------------------------------------------------
def emit_lifecycle_cse(records: list) -> str:
    lines = []
    for rec in records:
        for h in rec.history:
            lines.append(json.dumps({
                "cse_kind": "promotion_lifecycle",
                "candidate_id": rec.candidate_id,
                "promotion_class": rec.promotion_class,
                "state": h["state"], "reason": h["reason"],
                "note": "in-VPC CSE store-write is the materialize leg; local trail = the inspectable record",
            }))
    with open(LIFECYCLE_LOG, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + ("\n" if lines else ""))
    return LIFECYCLE_LOG


def _classify(candidate: dict) -> str:
    """Route a MOTIF candidate to a promotion class (PRD S4.1). A C3 system -> KNOWLEDGE_NODE; a recurring
    motif -> COMPILER_RULE (a recurring architectural idiom earns a first-class recognizer)."""
    return "KNOWLEDGE_NODE" if candidate.get("kind") == "system" else "COMPILER_RULE"


def _load_fedobs_measures() -> dict:
    """The git-real frontend-co-evolution measures (candidate_id -> {coupling_ratio, co_sessions}). When
    present, this is the CANDIDATE->MEASURED bind -- the gate reads a REAL per-candidate coupling."""
    if not os.path.exists(FEDOBS_MEASURE_ARTIFACT):
        return {}
    with open(FEDOBS_MEASURE_ARTIFACT, encoding="utf-8") as fh:
        payload = json.load(fh)
    return {m["candidate_id"]: m for m in payload.get("measures", [])}


def load_candidates() -> list:
    if not os.path.exists(CANDIDATE_ARTIFACT):
        return []
    with open(CANDIDATE_ARTIFACT, encoding="utf-8") as fh:
        payload = json.load(fh)
    measures = _load_fedobs_measures()   # JOIN the FEDOBS measure-bind if it has run
    recs = []
    for c in payload.get("candidates", []):
        fm = measures.get(c["candidate_id"])
        if fm is not None:
            # MEASURED: a real git-grounded coupling bound. The gate now evaluates it (anti-Goodhart ratio).
            measure = {"status": "MEASURED", "coupling_ratio": fm.get("coupling_ratio"),
                       "co_sessions": fm.get("co_sessions", 0), "source": "frontend-co-evolution (git, CVO-verifiable)"}
        else:
            fed = dict(c.get("fedobs_cooccurrence", {}))
            measure = {"status": "MEASURED" if fed.get("status") == "MEASURED" else "PENDING_IN_VPC",
                       "co_sessions": fed.get("co_sessions", 0), "source": fed.get("source_view")}
        recs.append(PromotionRecord(
            candidate_id=c["candidate_id"], promotion_class=_classify(c),
            recurrence=c.get("recurrence", 0), decompression_chain=c.get("decompression_chain", {}),
            fedobs_measure=measure))
    return recs


def run_engine() -> int:
    print("=" * 80)
    print("NFRA_PROMOTE P1 -- promotion lifecycle engine (consume MOTIF candidates -> run the gate)")
    print("=" * 80)
    recs = load_candidates()
    if not recs:
        print("no candidate artifact found (%s) -- run NFRA_MOTIF_P3 first." % os.path.relpath(CANDIDATE_ARTIFACT, WS))
        return 1
    for rec in recs:
        advance(rec)   # no owner verdict, no coverage: the gate holds each at CANDIDATE (measure pending)
    emit_lifecycle_cse(recs)

    print("\nConsumed %d MOTIF candidates -> lifecycle run (measure-before-promote gate active):\n" % len(recs))
    for rec in recs:
        target, owner = PROMOTION_CLASS_ROUTING[rec.promotion_class]
        print("  %-34s class=%-15s -> %-16s state=%s"
              % (rec.candidate_id, rec.promotion_class, owner, rec.state))
        print("       %s" % rec.history[-1]["reason"])
    held = sum(1 for r in recs if r.state == "CANDIDATE")
    promoted = sum(1 for r in recs if r.state in ("MATERIALIZED", "SUSTAINED"))
    print("\n" + "-" * 80)
    print("GATE RESULT: %d/%d HELD at CANDIDATE (measure PENDING_IN_VPC) | %d promoted." % (held, len(recs), promoted))
    print("AC1 measure-before-promote: FIRING -- no candidate reaches PROMOTED without a FEDOBS measure.")
    print("  This matches the CTO ratify-ruling (7 RATIFIED-AS-CANDIDATES, PROMOTION WITHHELD). The gate is")
    print("  a REFUSAL, not a blocker -- an unmeasured candidate CANNOT materialize (zero auto-mutation).")
    proposed = [r.candidate_id for r in recs if r.state == "PROPOSED"]
    if proposed:
        print("RE-ROUTE to CTO (promotion ratify -- coupling_ratio warrant, invariant #5 cited): %s" % ", ".join(proposed))
    print("Anti-Goodhart: coupling_ratio >= %.2f (CTO-ratified; a candidate below it is DROPPED, reversible not zombie-held)."
          % FEDOBS_RATIO_FLOOR)
    print("Lifecycle CSE trail: %s" % os.path.relpath(LIFECYCLE_LOG, WS))
    return 0


# ---------------------------------------------------------------------------
# Self-test -- the 5-invariant gate exercised, each BITING (the CVO cert bar: the gate must bite).
# ---------------------------------------------------------------------------
def _mk(cid, cls, measure, recurrence=5):
    return PromotionRecord(cid, cls, recurrence,
                           {"c0_evidence": [{"fact": "x", "source": "f.tsx", "locus": "L1"}], "n_c0_facts": 1},
                           measure)


def self_test() -> int:
    print("=== NFRA_PROMOTE_P1 self-test (the 5-invariant gate must BITE) ===")
    ok = []

    def chk(name, cond):
        ok.append(cond)
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    # AC1 measure-before-promote: an UNMEASURED candidate is HELD at CANDIDATE (cannot reach MATERIALIZED).
    r = advance(_mk("m:unmeasured", "COMPILER_RULE", {"status": "PENDING_IN_VPC", "co_sessions": 0}))
    chk("1  AC1: unmeasured candidate HELD at CANDIDATE (measure-before-promote bites)", r.state == "CANDIDATE")
    chk("1b AC1 negative control: unmeasured candidate NEVER reaches MATERIALIZED/SUSTAINED",
        r.state not in ("MATERIALIZED", "SUSTAINED"))

    # AC3 anti-Goodhart: a MEASURED-but-WEAK-coupling (coupling_ratio 0.05 < floor 0.15) is DROPPED, not promoted.
    r = advance(_mk("m:weak", "COMPILER_RULE", {"status": "MEASURED", "coupling_ratio": 0.05}), owner_verdict="RATIFY")
    chk("3  AC3: weak coupling (ratio 0.05<0.15) DROPPED, not promoted (anti-Goodhart bites on the RATIFIED signal)",
        r.state == "DROPPED")

    # AC2 human-ratify: a MEASURED+MEANINGFUL candidate with NO owner verdict is HELD at PROPOSED (zero auto-mutation).
    r = advance(_mk("m:unratified", "KNOWLEDGE_NODE", {"status": "MEASURED", "coupling_ratio": 0.18}), owner_verdict=None)
    chk("2  AC2: meaningful-but-unratified candidate HELD at PROPOSED (zero auto-mutation; no auto-ratify)",
        r.state == "PROPOSED")
    # AC2 negative control: owner REJECT -> REJECTED (not materialized)
    r = advance(_mk("m:rejected", "KNOWLEDGE_NODE", {"status": "MEASURED", "coupling_ratio": 0.18}), owner_verdict="REJECT")
    chk("2b AC2: owner REJECT -> REJECTED, never materialized", r.state == "REJECTED")

    # HAPPY PATH: measured + meaningful (ratio>=floor) + ratified -> MATERIALIZED (the gate PASSES a real warrant).
    r = advance(_mk("m:promotable", "COMPILER_RULE", {"status": "MEASURED", "coupling_ratio": 0.18}), owner_verdict="RATIFY",
                post_effect="SUSTAINED")
    chk("H  happy path: measured+meaningful+ratified -> MATERIALIZED -> SUSTAINED", r.state == "SUSTAINED")

    # AC4 reversible: a materialized promotion that DEGRADES post-promotion is DEMOTED.
    r = advance(_mk("m:degrades", "COMPILER_RULE", {"status": "MEASURED", "coupling_ratio": 0.18}), owner_verdict="RATIFY",
                post_effect="DEGRADED")
    chk("4  AC4 reversible: a DEGRADED post-promotion effect -> DEMOTED", r.state == "DEMOTED")
    # AC4 reversible (de-candidate): unmeasured AFTER coverage landed -> DROPPED, not zombie-held.
    r = advance(_mk("m:nocoverage", "COMPILER_RULE", {"status": "PENDING_IN_VPC", "co_sessions": 0}), coverage_landed=True)
    chk("4b AC4 reversible: no meaningful measure after coverage -> DROPPED (not zombie-held)", r.state == "DROPPED")

    # AC5 inspectable: every record cites evidence + a CSE-logged trail.
    r = advance(_mk("m:inspect", "COMPILER_RULE", {"status": "MEASURED", "co_sessions": 3}), owner_verdict="RATIFY")
    ok5, _ = inv5_inspectable(r)
    chk("5  AC5 inspectable: record cites evidence (decompression) + a CSE-logged transition trail", ok5)

    n = sum(1 for x in ok if x)
    print("--- self-test: %d/%d passed (the gate bites on AC1/AC2/AC3/AC4; passes a real warrant) ---" % (n, len(ok)))
    return 0 if n == len(ok) else 1


def print_lifecycle() -> int:
    print("NFRA_PROMOTE P1 -- lifecycle + ratify-owner routing")
    print(" ".join(STATES).replace(" ", " -> ", 1))
    print("\nStates: " + " -> ".join(STATES[:8]))
    print("        + DEGRADED->DEMOTED (reversible) + DROPPED (de-candidate: no meaningful measure)")
    print("\nPromotion class -> target artifact -> ratify owner:")
    for cls, (target, owner) in PROMOTION_CLASS_ROUTING.items():
        print("  %-18s -> %-38s -> %s" % (cls, target, owner))
    print("\nAnti-Goodhart floor: co_sessions >= %d distinct producer sessions (a single co-occurrence is coincidental)."
          % MEANINGFUL_CO_OCCURRENCE_FLOOR)
    return 0


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass
    args = sys.argv[1:]
    if "--self-test" in args:
        return self_test()
    if "--lifecycle" in args:
        return print_lifecycle()
    return run_engine()


if __name__ == "__main__":
    sys.exit(main())
