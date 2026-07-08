#!/usr/bin/env python3
"""NFRA_PROMOTE-P2 / GOV-B R4 -- the PROPOSED 5th-producer CSE emission contract (PROMOTE / MATERIALIZER).

STATUS: CTO-ARCH-GATED (2026-07-08, GO -- CTO exercised the self-test 10/10 himself); routing CVO re-sign
-> COO SoD-land @0.4. A governed migration, NOT yet a landed change. Authored by 0.8.0_AE_CloudComp~D (the
GOV-B producer). The path is the SAME governed one as the 0.3 Entity.TYPE/SYMBOL bump. This module does NOT
mutate cse_schema.py; it proposes the migration + proves the contract shape validates through the REAL
cse_schema.validate under a SANDBOXED in-memory enum extension.

CONSUMER NOTE (CTO arch-gate): the LOW confidence (0.2) on a MATERIALIZED/DEMOTED CSE is the SUBJECT's
TYPE-confidence (untyped-Concept per S3.5) -- NOT the promotion EVENT's certainty. The promotion DEFINITELY
happened; that is carried by the event EXISTING + the verb + the commission_id, not the confidence field.
FEDOBS directive-effectiveness consumers must NOT discount the event because the band is LOW (LOW = "a
recognizer has no governed algebra-type", NOT "maybe it didn't promote"). An event-certainty-vs-type-
confidence split (a separate field) is a future refinement; within the current S3.5 rule, Concept->LOW is right.

WHY (CTO arch-gate 4d0886493, R4): the promotion MATERIALIZED/DEMOTED transition is itself an observation
(invariant #5) -- it should feed FEDOBS directive-effectiveness (before/after the promotion) as a first-class,
schema-validated CSE, alongside the git/graph_head/agent/deploy four (DS~B's NFRA_CSE_P3_emission_contracts.py).
The GOV-B loop CLOSED using the lifecycle/trail-record CSE (interim, non-gating -- see comp_promote_materializer
._emit_lifecycle_cse); this PROMOTE producer contract makes the transition a first-class CSE producer.

THE GOVERNED MIGRATION (what CTO ratifies + COO SoD-lands into org/modules/graph/cse_schema.py):
  ProducerKind: add ONE enum member ->   PROMOTE = "promote"
  (_PRODUCER_VALUES = frozenset(p.value for p in ProducerKind) derives it automatically -- no other edit.)
  VERSION: cse_schema @0.3 -> 0.4 (DS~B-confirmed 2026-07-08 as version-owner; CTO arch-gate GO). A MINOR,
  single additive/back-compat enum member -- goes SOLO (DS~B has no queued SCHEMA_VERSION change), no parallel
  bump. The SCHEMA_VERSION bump is the governance marker.

THE CONTRACT (P3 pattern): a MATERIALIZED/DEMOTED CSE emitted by the promote-materializer when a ratified
recognizer is hot-loaded LIVE (materialize -> verb CREATE) or hot-deregistered (demote -> verb DELETE).
  subject : the promoted RECOGNIZER. It is Concept(untyped)+LOW -- a recognizer has NO typed cloud Entity in
            the algebra (there is no Entity.RECOGNIZER), so Concept is the HONEST subject (LAW 1); low
            confidence per the S3.5 Concept rule (a promotion is CERTAIN, but its subject's algebra-TYPE is
            genuinely untyped -- we never smuggle a typed claim). This is the honest-degrade target used
            exactly as intended -- mirrors the agent(redacted-M365) producer's Concept+low case in P3.
  provenance : DECOMPRESSES to the git-versioned manifest entry (source=manifest, locus=recognizer_id,
               evidence=commission_id + coupling_ratio warrant) -- LAW 2 fidelity.

Usage:
  python NFRA_PROMOTE_P2_GOVB_R4_promote_emission_contract.py            # self-test (validates under sandbox)
  python NFRA_PROMOTE_P2_GOVB_R4_promote_emission_contract.py --spec      # human-readable contract + migration
"""
from __future__ import annotations

import os
import sys

# The canonical algebra + validator (path-robust; the canonical home is org/modules/graph).
_GRAPH_MOD = os.path.join(os.path.dirname(__file__), "..", "..", "..", "modules", "graph")
if os.path.isdir(_GRAPH_MOD):
    sys.path.insert(0, os.path.abspath(_GRAPH_MOD))
import cse_schema as CSE  # noqa: E402
from cse_schema import CSE as CSEvent, EntityRef, Provenance  # noqa: E402

# The PROPOSED producer-kind value (NOT yet in cse_schema.ProducerKind -- that is the governed migration).
PROPOSED_PRODUCER_KIND = "promote"

# The exact governed migration for CTO ratify + COO SoD-land (author = ~D; NOT applied here).
PROPOSED_MIGRATION = {
    "file": "org/modules/graph/cse_schema.py",
    "change": "add one ProducerKind member: PROMOTE = \"promote\" (after GRAPH_HEAD)",
    "derived": "_PRODUCER_VALUES = frozenset(p.value for p in ProducerKind) picks it up automatically",
    "version": "cse_schema @0.3 -> 0.4 (DS~B-confirmed 2026-07-08, version-owner): a MINOR bump, single additive/back-compat enum member; goes solo (no batched change)",
    "version_history_line": "extend the SCHEMA_VERSION comment at cse_schema.py:42: "
                            "'0.3->0.4 (CTO-ratified <date>): +ProducerKind.PROMOTE (governed 5th-producer "
                            "emission-contract, back-compat additive)' -- keeps the version lineage self-documenting",
    "governed_by": "CTO arch-gate GO (2026-07-08) -> CVO re-sign -> COO SoD-land (same path as the 0.3 TYPE/SYMBOL bump)",
    "back_compat": "additive enum member -- no existing CSE invalidated; a new producer only widens the accepted set",
}


# ---------------------------------------------------------------------------
# THE 5TH PRODUCER EMISSION CONTRACT (P3 pattern -- the spec as structured data).
# ---------------------------------------------------------------------------
def contract_promote() -> dict:
    """promote-materializer -> the MATERIALIZED/DEMOTED recognizer transition -> promote CSE."""
    return {
        "producer_kind": PROPOSED_PRODUCER_KIND,   # PROPOSED ProducerKind.PROMOTE
        "ref": "the ratifier commission_id (the CTO promotion-ratify that authorized the live-load)",
        "compiler": {"id": "promote-materializer", "artifact_class": "promoted_recognizer",
                     "version": CSE.SCHEMA_VERSION},
        "recognizer": "comp_promote_materializer (materialize_live -> CREATE / demote_live -> DELETE)",
        "subject_rule": "the promoted RECOGNIZER. Concept(untyped)+LOW -- no Entity.RECOGNIZER exists, so "
                        "Concept is the honest subject (LAW 1); low confidence per the Concept S3.5 rule "
                        "(the promotion is certain, its algebra-TYPE is genuinely untyped -- never a smuggled "
                        "type). verb = create on materialize (hot-register live), delete on demote (deregister).",
        "provenance_map": {"source": "the git-versioned promote_recognizer_manifest.json entry",
                           "locus": "the recognizer_id",
                           "evidence": "commission_id + coupling_ratio warrant (decompresses to the manifest entry)"},
        "consumer_note": "the LOW confidence (0.2) is the SUBJECT's TYPE-confidence (untyped-Concept, S3.5), "
                         "NOT the promotion EVENT's certainty. The promotion DEFINITELY happened -- carried by "
                         "the event EXISTING + the verb + the commission_id, not the confidence field. FEDOBS "
                         "directive-effectiveness consumers must NOT discount the event for a LOW band (LOW = "
                         "'a recognizer has no governed algebra-type', NOT 'maybe it didn't promote'). "
                         "[CTO arch-gate note 2026-07-08]",
        "example": example_materialized,
        "example_demote": example_demoted,
    }


# ---------------------------------------------------------------------------
# GROUNDED EXAMPLES -- the REAL recognizer:silent-display-fork promotion (MATERIALIZED under
# CTO-PROMOTE-20260708T1521Z-silent-display-fork; live_as_of load-marker 96317d3292cf2cd3).
# ---------------------------------------------------------------------------
def _promote_cse(*, verb: str, recognizer_id: str, commission_id: str, coupling_ratio: float,
                 marker: str) -> CSEvent:
    prov = Provenance(
        source="org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/promote_recognizer_manifest.json",
        locus=recognizer_id, recognizer="promote_materializer",
        evidence=f"commission={commission_id} coupling_ratio={coupling_ratio} (ratified warrant)")
    return CSEvent(
        event_id=f"{PROPOSED_PRODUCER_KIND}:{recognizer_id}:{verb}",
        schema_version=CSE.SCHEMA_VERSION,
        producer={"kind": PROPOSED_PRODUCER_KIND, "ref": commission_id},
        compiler={"id": "promote-materializer", "artifact_class": "promoted_recognizer",
                  "version": CSE.SCHEMA_VERSION},
        # Concept(untyped) subject -> LOW confidence (S3.5): a recognizer has no typed cloud Entity.
        transformation={"verb": verb, "subject": EntityRef(CSE.Entity.CONCEPT.value, recognizer_id),
                        "edges": []},
        provenance=prov,
        execution_meta={"timestamp": "2026-07-08T15:21Z", "actor": "comp_promote_materializer",
                        "run_id": commission_id},
        head={"marker_head": marker},
        qualifiers={CSE.Qualifier.CONFIDENCE.value: 0.2,
                    CSE.Qualifier.SCOPE.value: "compilerkit.recognizer.hot_register"})


def example_materialized() -> CSEvent:
    """MATERIALIZED: recognizer:silent-display-fork hot-registered LIVE (verb=create)."""
    return _promote_cse(verb=CSE.Transformation.CREATE.value, recognizer_id="recognizer:silent-display-fork",
                        commission_id="CTO-PROMOTE-20260708T1521Z-silent-display-fork",
                        coupling_ratio=0.18, marker="96317d3292cf2cd3")


def example_demoted() -> CSEvent:
    """DEMOTED: recognizer:silent-display-fork hot-deregistered (verb=delete -- the exact inverse)."""
    return _promote_cse(verb=CSE.Transformation.DELETE.value, recognizer_id="recognizer:silent-display-fork",
                        commission_id="CTO-PROMOTE-20260708T1521Z-silent-display-fork",
                        coupling_ratio=0.18, marker="96317d3292cf2cd3")


# ---------------------------------------------------------------------------
# SANDBOXED validation proof -- temporarily widen the module-global _PRODUCER_VALUES to include the PROPOSED
# "promote" kind, validate through the REAL cse_schema.validate, then RESTORE. Proves the contract lands
# clean once the governed enum member is added -- WITHOUT mutating cse_schema.py.
# ---------------------------------------------------------------------------
def _sandboxed_validate(cse: CSEvent) -> tuple:
    original = CSE._PRODUCER_VALUES
    try:
        CSE._PRODUCER_VALUES = frozenset(original | {PROPOSED_PRODUCER_KIND})
        return CSE.validate(cse)
    finally:
        CSE._PRODUCER_VALUES = original   # never leave the sandbox extension live


def self_test() -> bool:
    checks = []

    def chk(name, cond, detail=""):
        checks.append(bool(cond))
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f"  -> {detail}" if (detail and not cond) else ""))

    print(f"=== NFRA_PROMOTE R4 PROMOTE emission-contract PROPOSAL (schema {CSE.SCHEMA_VERSION}, sandboxed) ===")

    # 0. HONEST current state: "promote" is NOT yet a governed kind -> a promote CSE is REJECTED today
    #    (proves the migration is genuinely needed, and that we did NOT smuggle the enum in).
    ok_now, _ = CSE.validate(example_materialized())
    chk("0  PRE-migration: a promote-kind CSE is REJECTED today (ProducerKind.PROMOTE not yet governed)",
        not ok_now)

    # 1. POST-migration (sandboxed): MATERIALIZED + DEMOTED both validate through the REAL validator.
    for nm, ex in (("MATERIALIZED", example_materialized()), ("DEMOTED", example_demoted())):
        ok, errs = _sandboxed_validate(ex)
        chk(f"1  {nm}: validates through cse_schema.validate under the proposed enum (sandbox)", ok, str(errs))
        fok, ff = CSE.cse_fidelity_ok(ex)
        chk(f"1b {nm}: decompresses to C0 evidence (fidelity, LAW 2 -- the manifest entry)", fok, str(ff))

    # 2. subject is Concept(untyped)+low (the honest-degrade target -- a recognizer has no typed Entity).
    m = example_materialized()
    chk("2  subject is Concept(untyped)+low (honest -- no Entity.RECOGNIZER; never a smuggled type)",
        m.transformation["subject"].etype == CSE.Entity.CONCEPT.value
        and CSE.confidence_band(m.qualifiers[CSE.Qualifier.CONFIDENCE.value]) == "low")

    # 3. NEGATIVE control: a promote CSE smuggling HIGH confidence on the Concept subject is REJECTED even
    #    under the sandbox (the migration widens the producer set -- it does NOT relax the Concept honesty rule).
    bad = example_materialized()
    bad.qualifiers[CSE.Qualifier.CONFIDENCE.value] = 0.95
    ok_bad, _ = _sandboxed_validate(bad)
    chk("3  NEGATIVE: high-confidence on a Concept(untyped) promote subject is REJECTED (Concept rule holds)",
        not ok_bad)

    # 4. the migration is a SINGLE additive enum member (minimal, back-compat) + the sandbox is restored.
    chk("4  migration is one additive enum member (PROMOTE='promote'); back-compat (no existing CSE invalidated)",
        PROPOSED_MIGRATION["change"].count("PROMOTE") == 1)
    chk("4b sandbox restored: _PRODUCER_VALUES does NOT leak the proposed kind after the proof",
        PROPOSED_PRODUCER_KIND not in CSE._PRODUCER_VALUES)

    # 5. verb discipline: materialize=create, demote=delete (the exact-inverse transition pair).
    chk("5  verb pair: materialize=create / demote=delete (reversible transition)",
        example_materialized().transformation["verb"] == CSE.Transformation.CREATE.value
        and example_demoted().transformation["verb"] == CSE.Transformation.DELETE.value)

    # 6. CTO arch-gate consumer note documented: LOW = subject TYPE-confidence, not event certainty.
    chk("6  contract documents the consumer note (LOW=type-confidence, NOT event-certainty; CTO arch-gate)",
        "NOT the promotion EVENT's certainty" in contract_promote()["consumer_note"])

    # 7. version pinned to the DS~B-confirmed 0.4 (version-owner) -- de-risks the SoD-land.
    chk("7  version pinned @0.3 -> 0.4 (DS~B-confirmed version-owner; solo sequential MINOR bump)",
        "0.4" in PROPOSED_MIGRATION["version"] and "version_history_line" in PROPOSED_MIGRATION)

    passed = sum(1 for c in checks if c)
    print(f"=== {passed}/{len(checks)} PASS (PROPOSAL -- routes CTO arch-gate -> CVO re-sign -> COO SoD-land) ===")
    return passed == len(checks)


def print_spec() -> None:
    c = contract_promote()
    print("# NFRA_PROMOTE R4 -- the PROPOSED 5th producer emission contract (PROMOTE / MATERIALIZER)\n")
    print("## producer: promote  (PROPOSED ProducerKind.PROMOTE)")
    print(f"   ref         : {c['ref']}")
    print(f"   compiler    : {c['compiler']['id']}  (artifact_class={c['compiler']['artifact_class']})")
    print(f"   recognizer  : {c['recognizer']}")
    print(f"   subject rule: {c['subject_rule']}")
    print(f"   provenance  : source={c['provenance_map']['source']}")
    print(f"                 locus={c['provenance_map']['locus']}  evidence={c['provenance_map']['evidence']}")
    print(f"   consumer    : {c['consumer_note']}")
    print("\n## THE GOVERNED MIGRATION (CTO ratifies -> COO SoD-lands):")
    for k, v in PROPOSED_MIGRATION.items():
        print(f"   {k:12s}: {v}")
    print("\n## STATUS: PROPOSAL. The GOV-B loop closed on the lifecycle/trail-record CSE (interim, non-gating).")
    print("   This makes PROMOTE a first-class schema-validated 5th CSE producer. Non-loop-close-blocking.")


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass
    if "--spec" in sys.argv[1:]:
        print_spec()
        return 0
    return 0 if self_test() else 1


if __name__ == "__main__":
    sys.exit(main())
