# TO ADVI_49F.c02-ENUMERATOR — the P14 vehicle enumerates its date set from the calendar ∩ input presence, never an output table; and the c02 mirror-pull vehicle is retired from the host (cell C02-g-9)

<task_order id="ADVI_49F.c02-ENUMERATOR" project="ADVI_49F">
<issued_to>0.7.0_AE_CloudOps~L</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-30T09:5xZ</issued>
<decomp_ref>org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md -- <owned_cells>C02-g-9</owned_cells></decomp_ref>
<proof_of_spec>
  <expected_criteria>E-1,E-2,E-3,E-4,E-5</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps~L/deliverables/ADVI_49F.c02-ENUMERATOR.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form: python .tools/proof-of-spec-check.py <instance>.json E-1,E-2,E-3,E-4,E-5 ; print the checker's commit-ish beside the verdict -->
</proof_of_spec>
<status>pending -- GO on delivery of this face (C02-g-7 CLOSED at the grader 87083 and the issuer; the two items routed at condition (6) and at the g-6 close are unblocked). E-1/E-2 are code + arms at the seat; E-3 the DS-independent deploy of an AE-owned vehicle script read on the running artifact; E-4 the host-object retirement after a reference census. No dated run, no re-derivation, nothing served moves. The 12:50Z fire read (M-4, DS~N's) is unrelated and unchanged.</status>
<priority>P2 -- no served output depends on it today; it removes the mechanism that made a five-trading-day hole invisible to the instrument built to fill it, and a standing one-table rewrite capability with no live cell.</priority>
<authority>C02-g-7 B-1 (AE~L 86087; DS~N 86155): the P14 enumerator derives from flow_ledger, which carried the hole; CTO 86096 condition (6) "routed as an ITEM at the P14 script's owner, not fixed in this cell"; the register item @d1ea47add2; the g-6 close's mirror-pull removal item. Rule 13: an AE-owned vehicle script under the AE lane. D2 drive-pair scope. Not to 4.0.0_SA_CRO.</authority>
</task_order>

## READ THIS FIRST -- the decomp cell is the specification

**`org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md`, cell `C02-g-9`.** The state, the five criteria, the do-nots. **This face does not restate it.** Where the two differ, the cell governs.

## The one-paragraph version

The P14 re-derivation campaign enumerated its dates from `flow_ledger` CommonPrefixes -- an OUTPUT table -- so a date with no outputs was never a candidate, and five never-produced trading days stayed invisible to every re-run (534 not 539 was an enumeration property, C02-g-7 B-1). Derive the set from `dim_calendar`'s trading days INTERSECT a per-date input-presence census (B-2's instrument), print the three denominators and every exclusion with its reason, prove it with three arms from three truths (the stored set reproduced; a masked-output date STILL enumerated -- the arm the old code fails; an inputs-absent date EXCLUDED), deploy it to the host `_code/` set and read it on the running artifact against the index blob, and fire NOTHING. Then retire `_code/c02_reemit_mirror_pull.py` from the host after a zero-reference census with a positive control, prior VersionId retained.

## Acceptance criteria -- E-1 through E-5, verbatim from cell `C02-g-9`

<criterion id="E-1" cell_refs="C02-g-9"/> **THE ENUMERATOR at source**: calendar trading days ∩ input presence, never an output table; three denominators printed; every excluded calendar day named with its reason.
<criterion id="E-2" cell_refs="C02-g-9"/> **THE ARMS**: (i) a DRY run at HEAD reproduces the stored set 540 of 540 (0 missing / 0 extra); (ii) a synthetic masked-output date is STILL enumerated (the mutation restoring the flow_ledger read fails this arm); (iii) an inputs-absent date is EXCLUDED and printed UNBACKFILLABLE-INPUTS-ABSENT; commit-gate clean; `safe-commit -F`.
<criterion id="E-3" cell_refs="C02-g-9"/> **THE DEPLOY read on the running artifact**: host `_code/A00_ATTESTATION_REDERIVATION.py` ETag == the committed INDEX blob's LF md5, VersionId printed; deploy ledger opened and closed on the read; no campaign fired.
<criterion id="E-4" cell_refs="C02-g-9"/> **THE MIRROR-PULL VEHICLE RETIRED**: a reference census (entrypoint + P14 vehicle: 0 hits, positive control on a referenced module) BEFORE the delete; `_code/c02_reemit_mirror_pull.py` deleted from the host with its prior VersionId retained and printed; the repo copy untouched.
<criterion id="E-5" cell_refs="C02-g-9"/> proof VALID rc=0 positional E-1..E-5, checker vintage printed; graded by `3.0.0_SA_CVO`.

## Do NOT

- ⛔ **Do not fire a re-derivation, a backfill, or any dated run** under this cell -- a campaign is its own never-widen act with its own cell.
- ⛔ **Do not touch the chain entrypoint or a06** (C02-g-8's) or any DS-lane stage.
- ⛔ **Do not `cp` from the worktree** for the deploy digest -- the index blob is the identity (22a; five instances 08-30).
- ⛔ Nothing to `4.0.0_SA_CRO`.

## Reporting

E-1 + E-2 as one message (the three arms printed, the mutation's failure quoted) to the issuer + CTO; E-3 + E-4 as one message (the running-artifact read; the census + the delete with the VersionId) to the issuer + CTO + CVO; the proof at the close. Surprise channel: one line to `3.0.0_SA_CVO` cc issuer.
