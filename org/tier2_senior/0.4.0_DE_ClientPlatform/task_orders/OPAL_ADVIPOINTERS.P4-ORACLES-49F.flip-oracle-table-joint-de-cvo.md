# TO OPAL_ADVIPOINTERS.P4-ORACLES-49F — the P4_FLIP_ORACLES_49F table (CRO~A J4, ratified): DE + CVO joint-author, runnable by 08-21

<task_order id="OPAL_ADVIPOINTERS.P4-ORACLES-49F" project="OPAL_ADVIPOINTERS">
<issued_to>0.4.0_DE_ClientPlatform (primary author) + 3.0.0_SA_CVO (joint — oracle validity)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T17:10Z</issued>
<dated>2026-08-21 — runnable the day before the 08-22 flip; row references fold into P4R-3/P4X-4 at delivery (COO folds; criterion sets stay stable).</dated>
<status>staged -- GO paired; author when your 08-19/20 rows clear</status>
<priority>P2 — makes the 08-22 flip's acceptance mechanical per key instead of per-judgment</priority>
<authority>CRO~A TIGHTENING_ENUMERATION_SPEC @1dceb7d61d J4, RATIFIED by CTO (G-C, @CTO_GATE_AND_RULING_SET_20260818_1700Z.md); COO releases the hook per the CTO ruling. Frame: the frozen P4E-1 v2 list @5f1076e9c1 (20 members) is the row denominator.</authority>
</task_order>

## Objective
Author `P4_FLIP_ORACLES_49F` — one row per flip-relevant key on the frozen list: the RUNNABLE oracle
that proves the flipped read serves the platinum/advi twin correctly (route + shape + value anchor +
the loud-failure signature), per the ratified J4 section. DE authors the rows (they own the read
surface); CVO validates each oracle CAN FAIL (an oracle that passes on the legacy serve too is not an
oracle — the mutant discipline applies to the table itself).

## Cross-domain coordination
- shared_resource: the frozen key list @5f1076e9c1 — OPEN rows (18, 20) get no oracle until resolved;
  GATED rows get legacy-side oracles only. shared_resource: P4R-3/P4X-4 — COO folds row references at
  delivery; DT consumes the table in the 08-22 rendered read.

## Acceptance criteria
- OR-1 COVERAGE: one row per EMIT key on the frozen list (denominator printed); OPEN/GATED rows
  carried with their state, never silently absent.
- OR-2 RUNNABLE: each oracle is an executable invocation (script/command + expected), not prose; the
  table states where it runs (DEV vs deployed) per row.
  **R1 RIDER (CTO @9988b2dd66): every value-anchor leg's LEGACY-side expected derives from the
  04:00Z T-1 serve, never the 23:01Z preview emission.**
- OR-3 CAN-FAIL (CVO's half): each oracle exercised once against a state where it MUST fail (the
  legacy serve or a mutated fixture) — pass-on-both rows are rewritten, shown.
- OR-4 proof instance VALID rc=0 positional per author half: ids OR-1,OR-2,OR-3,OR-4 (DE fills
  OR-1/OR-2, CVO fills OR-3; one instance, two evidence owners, stated per row).

<proof_of_spec>
  <expected_criteria>OR-1,OR-2,OR-3,OR-4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/OPAL_ADVIPOINTERS.P4-ORACLES-49F_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- No new instrument where ui-smoke / paired-provenance-exercise / comp-routes legs already serve —
  the table COMPOSES existing instruments (build ladder rung 2).

## Reporting
COO (cc CTO, DT, MSTR) at table-runnable; COO folds references into P4R-3/P4X-4 then. Surprise
channel: one banked line to COO. Session log with Compiler Tools section = deliverable.
