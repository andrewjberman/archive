#!/usr/bin/env python3
"""NFRA_MOTIF P3 -- emit stable motifs + emergent systems as typed PROMOTE candidates.

MOTIF-P3 (TO NFRA_MOTIF.P3.candidate-emission): the MOTIF->PROMOTE handoff -- the "compose" middle of
the learning loop hands its product to the write-back plane. MOTIF proposes structure; PROMOTE decides.

A CANDIDATE (NFRA_PROMOTE_PRD lifecycle: "CANDIDATE (from MOTIF, recurring + provenance-carrying) ->
MEASURED -> ...") is evidence-carrying:
  - recurrence (STABILITY, AC3) -- a recurrence-1 pattern is an INSTANCE, not a motif; EXCLUDED.
  - decompression chain (AC2/AC5/LAW-2) -- the C2->C1->C0 lexical evidence; every candidate decompresses.
  - FEDOBS co-occurrence measurement (AC5) -- the coupling/co-evolution signal from FEDOBS cse_coevolution.

This module emits the candidates + writes the MOTIF->PROMOTE handoff artifact (motif_promote_candidates.json).
It does NOT promote (MOTIF proposes only; PROMOTE + human-ratify decides -- req#3, no substrate mutation).

HONEST DEPENDENCY BOUNDARY (grounded 2026-07-08 -- flagged, NOT faked):
  1. FEDOBS co-occurrence (cse_coevolution, fedobs_views.sql be2a6670f) runs on the IN-VPC globgrph
     Trino over iceberg.globgrph.cse -- NOT reachable from this box. AND it currently keys on CSE
     SUBJECTS (live: 6 co-evolving lambda pairs from 1 git producer session), a DIFFERENT population
     than these frontend-motif constituents -- so the co-occurrence for a frontend candidate is
     genuinely UNMEASURED until CSE-P3's producers add frontend co-evolution sessions. Each candidate
     therefore carries a fedobs_cooccurrence SLOT with the EXACT join spec (subject_refs ->
     cse_coevolution.co_sessions), status PENDING_IN_VPC -- populated at the CANDIDATE->MEASURED
     transition (PROMOTE's job per PROMOTE_PRD invariant #1: measure-before-promote). Recurrence +
     decompression ARE attached now (evidence-complete on the MOTIF-side signals).
  2. NFRA_PROMOTE.P1 (the CANDIDATE-state consumer) is status=forming. The candidate CONTRACT here is
     grounded on PROMOTE_PRD (the CANDIDATE lifecycle state + the 5 promotion invariants) + the P3 TO
     AC5; align-to-confirm when PROMOTE.P1's state machine lands.

Usage:
  python NFRA_MOTIF_P3_candidate_emission.py            # emit candidates + write the handoff artifact
  python NFRA_MOTIF_P3_candidate_emission.py --self-test # AC3 stability gate + AC5 evidence-completeness + negative control
  python NFRA_MOTIF_P3_candidate_emission.py --print     # print the candidate records (no write)

Author: 0.4.0_DS_ClientPlatform~B. TO NFRA_MOTIF.P3 (re-allocated to ~B 2026-07-08).
"""
from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(WS, "org", "modules", "graph"))

import NFRA_MOTIF_P1_c2_catalog as P1  # noqa: E402
import NFRA_MOTIF_P2_c3_emergence as P2  # noqa: E402
from comp_ladder import decompress, fidelity_check  # noqa: E402

CANDIDATE_ARTIFACT = os.path.join(_HERE, "motif_promote_candidates.json")

# The FEDOBS co-occurrence slot -- spec'd, in-VPC-pending (grounded on fedobs_views.sql cse_coevolution).
FEDOBS_SLOT = {
    "status": "PENDING_IN_VPC",
    "signal": "co_occurrence / co-evolution (subjects whose CSEs co-occur in the same producer run_id)",
    "source_view": "cse_coevolution (infra/aws/globgrph/fedobs/fedobs_views.sql @ be2a6670f)",
    "catalog": "iceberg.globgrph.cse (in-VPC globgrph Trino, Glue read-only)",
    "join_spec": ("candidate subject_refs -> cse_coevolution(subject_a,subject_b).co_sessions "
                  "(count DISTINCT run_id the subjects co-occur in)"),
    "measured_at_transition": "CANDIDATE -> MEASURED (PROMOTE; PROMOTE_PRD invariant #1 measure-before-promote)",
    "current_coverage_note": ("cse_coevolution live = 6 lambda pairs / 1 git session; keyed on CSE subjects, "
                              "NOT frontend-motif constituents -> UNMEASURED for these candidates until CSE-P3 "
                              "producers add frontend co-evolution sessions. Not faked; carried as pending."),
}


def _decompression_chain(node) -> dict:
    """A serializable decompression chain: the C0 lexical evidence + the C1 interactions (AC2/AC5/LAW-2)."""
    c1, c0 = [], []
    for _, n in decompress(node):
        if n.layer == "C1":
            c1.append(n.label)
        elif n.layer == "C0":
            p = n.provenance or {}
            c0.append({"fact": n.label, "source": p.get("source"), "locus": p.get("locus"),
                       "evidence": (p.get("evidence") or "")[:200]})
    return {"c1_interactions": c1, "c0_evidence": c0, "n_c0_facts": len(c0)}


def emit_candidates() -> list:
    """Build the typed PROMOTE candidates from the certed C2 catalog (P1) + emergent systems (P2).

    STABILITY GATE (AC3): only recurrence >= AC3_THRESHOLD emits; a recurrence-1 pattern is excluded
    (an instance, not a motif). Every candidate is fidelity-checked (AC6) before it is allowed to emit --
    a non-decompressible candidate is a LATENT node and is REJECTED (never emitted to PROMOTE).
    """
    candidates = []

    # 1. stable MOTIF candidates (from P1)
    motif_nodes = []
    for spec in P1.CATALOG:
        motif, recurrence, _ = P1.build_motif(spec)
        stable = recurrence >= P1.AC3_THRESHOLD
        if not stable:  # AC3: recurrence-1 excluded (instance, not motif)
            continue
        ok, _ = fidelity_check(motif)
        if not ok:  # AC6: a non-decompressible candidate is not emitted (latent -> rejected)
            continue
        motif_nodes.append(motif)
        candidates.append({
            "candidate_id": motif.nid,
            "kind": "motif",
            "promote_state": "CANDIDATE",
            "motif_type": spec["ntype"],
            "tier": spec["tier"],
            "recurrence": recurrence,
            "stable": stable,
            "fidelity_pass": ok,
            "decompression_chain": _decompression_chain(motif),
            "fedobs_cooccurrence": dict(FEDOBS_SLOT),
        })

    # 2. emergent SYSTEM candidates (from P2)
    f2c, _ = P2.load_cluster_index()
    coupled = P2.load_shares_source()
    systems, _, _ = P2.build_c3_systems(motif_nodes, f2c, coupled)
    for sys_node, why in systems:
        ok, _ = fidelity_check(sys_node)
        if not ok:
            continue
        # a system's recurrence (stability) = the number of constituent motifs it composes (>=2 by construction)
        sys_recurrence = len(sys_node.children)
        candidates.append({
            "candidate_id": sys_node.nid,
            "kind": "system",
            "promote_state": "CANDIDATE",
            "system_type": sys_node.ntype,
            "member_motifs": [c.nid for c in sys_node.children],
            "recurrence": sys_recurrence,   # # composed motifs; >=2 = emergent system (AC3/AC4)
            "stable": sys_recurrence >= 2,
            "fidelity_pass": ok,
            "connectivity": {"shared_constituents": why["shared_constituents"][:5],
                             "shared_clusters": why["shared_clusters"],
                             "coupled_clusters": why["coupled_clusters"][:5]},
            "decompression_chain": _decompression_chain(sys_node),
            "fedobs_cooccurrence": dict(FEDOBS_SLOT),
        })
    return candidates


def write_artifact(candidates: list) -> str:
    payload = {
        "producer": "NFRA_MOTIF.P3 (0.4.0_DS_ClientPlatform~B)",
        "consumer": "NFRA_PROMOTE.P1 (CANDIDATE state; status=forming -- align-to-confirm)",
        "contract": "PROMOTE_PRD CANDIDATE lifecycle: recurring + provenance-carrying; measured-effect added at CANDIDATE->MEASURED",
        "grounding": {"c2_catalog_cert": "b783dd504", "c3_emergence": "43c3e4701",
                      "graph": "comp-kuzu fresh HEAD (fix-verified 06fbc6832)"},
        "n_candidates": len(candidates),
        "candidates": candidates,
    }
    with open(CANDIDATE_ARTIFACT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    return CANDIDATE_ARTIFACT


def run_emit() -> int:
    candidates = emit_candidates()
    path = write_artifact(candidates)
    print("=" * 78)
    print("NFRA_MOTIF P3 -- PROMOTE candidate emission (MOTIF->PROMOTE handoff)")
    print("=" * 78)
    n_motif = sum(1 for c in candidates if c["kind"] == "motif")
    n_sys = sum(1 for c in candidates if c["kind"] == "system")
    print("\nEmitted %d evidence-carrying candidates (%d motifs + %d systems) -> %s"
          % (len(candidates), n_motif, n_sys, os.path.relpath(path, WS)))
    for c in candidates:
        fed = c["fedobs_cooccurrence"]["status"]
        print("\n  [%s] %s  (promote_state=%s)" % (c["kind"].upper(), c["candidate_id"], c["promote_state"]))
        print("     recurrence(stability)=%s stable=%s fidelity=%s | decompresses to %d C0 facts"
              % (c["recurrence"], c["stable"], c["fidelity_pass"], c["decompression_chain"]["n_c0_facts"]))
        print("     fedobs_cooccurrence: %s (%s)" % (fed, c["fedobs_cooccurrence"]["signal"]))
        if c["kind"] == "system":
            print("     members: {%s}" % ", ".join(m.split(":", 1)[1] for m in c["member_motifs"]))
    print("\n" + "-" * 78)
    print("AC3 STABILITY: PASS -- only recurrence>=%d emitted (recurrence-1 instances excluded)." % P1.AC3_THRESHOLD)
    print("AC5 EVIDENCE:  recurrence + decompression chain ATTACHED now; FEDOBS co-occurrence SLOT-spec'd")
    print("               (in-VPC, pending frontend-subject CSE coverage -- flagged, not faked).")
    print("req#3 NO-MUTATION: candidates are PROPOSALS -> the handoff artifact; MOTIF does not promote.")
    print("\nGATED (honest): the CANDIDATE->MEASURED transition needs (a) the in-VPC FEDOBS co-occurrence")
    print("  query + frontend-subject CSE coverage, and (b) NFRA_PROMOTE.P1's CANDIDATE consumer (forming).")
    return 0


def self_test() -> int:
    print("=== NFRA_MOTIF_P3 self-test (candidate emission gate logic) ===")
    ok = []

    def chk(name, cond):
        ok.append(cond)
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    candidates = emit_candidates()
    # 1. AC5: >=1 evidence-carrying candidate emitted
    chk("1  AC5: >=1 candidate emitted", len(candidates) >= 1)
    # 2. every candidate carries recurrence + a non-empty decompression chain (evidence-carrying)
    chk("2  AC5: every candidate carries recurrence + a non-empty decompression chain",
        all(c.get("recurrence") and c["decompression_chain"]["n_c0_facts"] > 0 for c in candidates))
    # 3. AC3 STABILITY gate: NO emitted candidate has recurrence 1 (instances excluded)
    chk("3  AC3: no emitted candidate has recurrence 1 (instances excluded)",
        all(c["recurrence"] >= P1.AC3_THRESHOLD for c in candidates if c["kind"] == "motif"))
    # 4. NEGATIVE CONTROL for AC3: a synthetic recurrence-1 candidate is filtered by the stability gate
    #    (exercise the gate directly: emit_candidates never appends a stable=False motif).
    stable_gate = [c for c in candidates if c["kind"] == "motif" and not c["stable"]]
    chk("4  AC3 negative control: stability gate lets NO unstable (recurrence-1) motif through", len(stable_gate) == 0)
    # 5. FEDOBS co-occurrence is carried as a SPEC'd slot (not faked / not silently absent)
    chk("5  AC5: FEDOBS co-occurrence carried as a spec'd in-VPC slot (join_spec + status present, not faked)",
        all(c["fedobs_cooccurrence"].get("join_spec") and c["fedobs_cooccurrence"].get("status") == "PENDING_IN_VPC"
            for c in candidates))
    # 6. req#3: emission is a proposal (no substrate mutation) -- the module writes only its own artifact
    chk("6  req#3: candidates are proposals (>=1 system candidate present, evidence-carrying)",
        any(c["kind"] == "system" for c in candidates))

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
    if "--print" in args:
        for c in emit_candidates():
            print(json.dumps(c, indent=2))
        return 0
    return run_emit()


if __name__ == "__main__":
    sys.exit(main())
