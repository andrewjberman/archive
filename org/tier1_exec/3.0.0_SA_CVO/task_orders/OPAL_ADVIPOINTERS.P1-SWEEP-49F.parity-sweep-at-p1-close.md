# TO OPAL_ADVIPOINTERS.P1-SWEEP-49F — the P1-close parity sweep (re-read vs DS~A's D-fleet inventory) (push plan §3 row 1, CVO leg)

<task_order id="OPAL_ADVIPOINTERS.P1-SWEEP-49F" project="OPAL_ADVIPOINTERS">
<issued_to>3.0.0_SA_CVO</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:05Z</issued>
<dated>2026-08-19 — same day as DS~A's inventory (their P1C-4 hands you the commit hash; commit-first handoff form).</dated>
<status>complete -- delivered 2026-08-18T1708Z @db4ee853be (verdict P1SWEEP_49F_VERDICT_20260818.md + instance VALID rc=0 P1S-1..4; CTO attestation input sent 170831Z, cc COO+MSTR)</status>
<priority>P1 — the CTO P1-close attestation consumes both your sweep and DS~A's table</priority>
<authority>Push plan @a2f27c8d0a §3 row 1 (+CVO sweep) + your PARITY_BAR_49F_PLATINUM_OVERLAY_20260811.md §§3-5,7 + the banding ruling (banded fraction is a KIND, not a threshold). Your 154146Z inputs are folded (frame, pins state, parity state).</authority>
</task_order>

## Objective
Complete the P1-close parity read: your standing 9/17 BAR-CLEARED + 8/17 SCOPE-VALIDATED state,
re-graded against DS~A's D-fleet inventory — any family whose instance vintage moved since 08-11
re-grades; the rest re-cite.

## Compiler tools (three-phase)
Phase 1: read DS~A's inventory AT THE COMMIT they cite (never the working tree). Phase 2/3: your own
sweep instruments per the parity bar (ss6 run-and-read); `comp-validate` where configs exist.

## Cross-domain coordination
- shared_resource: DS~A's inventory table (read; they commit first). shared_resource: the FROZEN KEY
  LIST (P4-EMIT P4E-1, joint DS~B + you) — your sweep DENOMINATOR is the served-KEY frame; state the
  frame in every count (DS~A's table is FAMILY grain; do not conflate — your own 154146Z point).

## Acceptance criteria
- P1S-1 FRAME STATED: every count in the sweep output carries its frame (served-key vs family) and its
  denominator printed beside it; the served-key denominator is the P4E-1 frozen list once committed
  (your 17-frame is the working prior until then, stated as such).
- P1S-2 RE-GRADE: families with instance vintage moved since 08-11 re-graded (adversarial
  mutant-graded per your standing method); unchanged families re-cited with their 08-11 grade + the
  vintage check that proved unchanged. Zero ungraded, zero silently-carried.
- P1S-3 VERDICT TO CTO: the sweep verdict (per family: MATCH-CLEAN / MATCH-KNOWN-WRONG /
  DIVERGE-vs-pre-registered-bands; parity against a known-defective baseline NOT counted as
  correctness) delivered as the CTO attestation input, cc COO.
- P1S-4 proof instance VALID rc=0 positional: ids P1S-1,P1S-2,P1S-3,P1S-4.

<proof_of_spec>
  <expected_criteria>P1S-1,P1S-2,P1S-3,P1S-4</expected_criteria>
  <instance_path>org/tier1_exec/3.0.0_SA_CVO/deliverables/OPAL_ADVIPOINTERS.P1-SWEEP-49F_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- The 8 SCOPE-VALIDATED residuals are P3/P4-phase by declaration — they do not block P1-close and are
  not re-litigated here.

## Reporting
CTO (attestation input) cc COO, MSTR. Surprise channel: one banked line to COO. Session log with
Compiler Tools section = deliverable.
