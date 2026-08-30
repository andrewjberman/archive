# TO ADVI_49F.c02-A07STAMP — a07's provenance stamp goes through the helper: `_ingested_at` = the asof date, never a clock; `source_pipeline` = the helper's constant; two columns move and are declared before they do (cell C02-g-10)

<task_order id="ADVI_49F.c02-A07STAMP" project="ADVI_49F">
<issued_to>0.4.0_DS_ClientPlatform~N</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-30T13:0xZ</issued>
<decomp_ref>org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md -- <owned_cells>C02-g-10</owned_cells></decomp_ref>
<proof_of_spec>
  <expected_criteria>A7-1,A7-2,A7-3,A7-4,A7-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~N/deliverables/ADVI_49F.c02-A07STAMP.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form: python .tools/proof-of-spec-check.py <instance>.json A7-1,A7-2,A7-3,A7-4,A7-5 ; print the checker's commit-ish beside the verdict -->
</proof_of_spec>
<status>pending -- GO NOW on delivery of this face (C02-g-8 CLOSED at the grader 87335 while this face was being cut; the Monday pre-registration line -- CTO 87298, one line once the 08-30 map partition is READ ~13:16Z -- rides alongside and gates NOTHING here). A7-1..A7-3 are code + arms at the seat today; A7-4's serve is read on the FIRST scheduled fire after the deploy (Monday's 12:45Z fire if the deploy lands before it; the seat states which fire before it fires). Nothing served moves under this cell until A7-4's fire, and then two columns on two tables, by design.</status>
<priority>P2 -- no served output is wrong in rows; two of sixteen tables carry a wall clock in a field that is a partition key on the other fourteen, and a consumer cannot tell by the field name.</priority>
<authority>DS~N 87266 (1) a07:352/:500 BYPASS defect; CTO 87288 (1) accepted, "its own cell with a before/after, exactly as 86729 placed it", the convention line "the helper is the ONLY writer of `_ingested_at`"; the issuer's measurement at the cut that `rc.stamp_provenance` also writes `source_pipeline` (runner_common.py:40). Rule 13: a DS-lane gold script. D2 drive-pair scope. Not to 4.0.0_SA_CRO.</authority>
</task_order>

## READ THIS FIRST -- the decomp cell is the specification

**`org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md`, cell `C02-g-10`.** The state, the five criteria, the do-nots. **This face does not restate it.** Where the two differ, the cell governs.

## The one-paragraph version

a07 hand-rolls `_ingested_at` from `dt.datetime.now()` at `:352` and copies it into `alias_key_expansion` at `:500`, inside a block labelled `A5-A07-PROVENANCE`; it never imports `runner_common`, whose `stamp_provenance` is Atom 9 ("the asof partition date, never a clock") and is what the other six `a0*` stages call. Replace the hand-rolled lines with the helper call. **Before the bytes change, know that TWO columns move:** the helper also writes `source_pipeline = "49f-gold-runners"`, where a07 writes its own literal today. The cell reads the gate's one-writer sentence onto both fields; if the gate wants a stage-identifying `source_pipeline` preserved, that is a helper-contract ruling for all sixteen tables and it is taken at the cell BEFORE A7-1 lands -- raise it in the first message if the seat disagrees with the cell's reading, and do not land a07-specific carve-out code either way.

## Acceptance criteria -- A7-1 through A7-5, verbatim from cell `C02-g-10`

<criterion id="A7-1" cell_refs="C02-g-10"/> **THE REMEDY at source**: a07 imports the helper; `:351-352` become `df = rc.stamp_provenance(df, asof=as_of)`; `:499-500` copy the stamped fields (or call the helper on `exp` with the same asof); no other line changes; the DETERMINISM content hash is ASSERTED unchanged on the ad-hoc run; commit-gate clean; `safe-commit -F`.
<criterion id="A7-2" cell_refs="C02-g-10"/> **THE BEFORE/AFTER, pre-registered**: one ad-hoc run at date D to a SCRATCH root; `_ingested_at == D` and `source_pipeline == "49f-gold-runners"` on both outputs; every other column byte-identical to the served partition at D (denominator = each table's column count, both printed); a third moving column FAILS.
<criterion id="A7-3" cell_refs="C02-g-10"/> **THE ARMS from different truths**: (i) the unit arm on a fixture frame, with the `now()`-restoring mutation failing it; (ii) the chain-wide WRITER CENSUS of `_ingested_at` across the `a0*` + `c0*` runner set = exactly one writer (the helper), denominator printed.
<criterion id="A7-4" cell_refs="C02-g-10"/> **THE SERVE, read on the scheduled path**: deployed under the index-blob identity (22a) with the deploy ledger opened and closed on the running-artifact read, BEFORE a named 12:45Z fire; that fire's a07 outputs read from the S3 OBJECT carry `_ingested_at == the chain date` and the helper's `source_pipeline`; one line on the cell with the chain-log name.
<criterion id="A7-5" cell_refs="C02-g-10"/> proof VALID rc=0 positional A7-1..A7-5, checker vintage printed; graded by `3.0.0_SA_CVO`.

## Do NOT

- ⛔ **Do not touch a06** (C02-g-8's, closed on M-5) or any other stage's stamp -- one stage, one cell.
- ⛔ **Do not re-derive history.** The stored a07 partitions keep their clock stamps: COUNT them with the denominator printed and record that the value FORM (`YYYY-MM-DDTHH:MM:SSZ` vs `YYYY-MM-DD`) discriminates the two conventions. A backfill is its own never-widen act with its own cell.
- ⛔ **Do not fire a dated production run** under this cell; the serve is read on the scheduled fire.
- ⛔ **Do not `cp` from the worktree** for the deploy digest -- the index blob is the identity (22a; five instances 08-30).
- ⛔ Nothing to `4.0.0_SA_CRO`.

## Reporting

A7-1 + A7-2 + A7-3 as one message (the two moving columns named, the hash asserted, the census denominator) to the issuer + CTO; A7-4 as one message on the fire's read (the object, never SSM stdout) to the issuer + CTO + CVO; the proof at the close. Surprise channel: one line to `3.0.0_SA_CVO` cc issuer.
