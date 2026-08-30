# TO ADVI_49F.c02-BACKFILL — the five-date backfill: 2026-08-11..08-17, CAUSE READ FIRST, then the plan, then the emission (cell C02-g-7)

<task_order id="ADVI_49F.c02-BACKFILL" project="ADVI_49F">
<issued_to>0.7.0_AE_CloudOps~L</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-30T05:2xZ</issued>
<decomp_ref>org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md -- <owned_cells>C02-g-7</owned_cells> (B-2's input-presence read is supplied by 0.4.0_DS_ClientPlatform~N by message; the cause FIX, if any, is a separate item routed to its owner -- NOT in this TO)</decomp_ref>
<proof_of_spec>
  <expected_criteria>B-1,B-2,B-3,B-4,B-5,B-6</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps~L/deliverables/ADVI_49F.c02-BACKFILL.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form: python .tools/proof-of-spec-check.py <instance>.json B-1,B-2,B-3,B-4,B-5,B-6 ; print the checker's commit-ish beside the verdict -->
</proof_of_spec>
<status>pending -- GO on delivery of this face for B-1 + B-2 (READS ONLY); B-3 is the plan under never-widen (CTO+COO sign); B-4/B-5 write ONLY on the signed plan. The seat is LIVE; C02-g-6 is ACCEPTED on substance (CVO 85944) and formally closes on its proof instance -- this face does not start B-4 before that close.</status>
<priority>P1 -- the five missing days are the BDPARITY hole on every period cell that spans them, and 2026-08-18's all-refused state hangs on 08-17's absence; but a backfill onto an unread cause is a shadow of the outage, so B-1 gates everything.</priority>
<authority>C02-g-6 ACCEPTED (CVO 85944); the five-date outage measured at AE~L 84527 + the 539 - 5 + 1 = 535 reconciliation (84911, DS~N corroborated); the issuer's sequencing at 85915 (3); the CTO's never-widen at this cell's plan (85934); the register item recorded at `459f17d006`. D2 drive-pair scope. Not to 4.0.0_SA_CRO.</authority>
</task_order>

## READ THIS FIRST -- the decomp cell is the specification

**`org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md`, cell `C02-g-7`.** The state, the pre-registered first act, the six criteria and the never-widen clause. **This face does not restate it.** Where the two differ, the cell governs.

## The one-paragraph version

Five trading days (2026-08-11, 12, 13, 14, 17) have no stored `twr_daily` partition. FIRST read WHY (the scheduler / dispatch / SSM plane for those dates -- `bd-49f-runner-daily` DISABLED and the fees-session cron are the first two reads) and WHETHER the inputs exist (DS~N's bronze/silver presence read per date). THEN plan: dates with inputs, oldest-first (each date's D-1 must exist -- 08-11's is stored; 08-12..08-17 chain on each other), readers announced, shapes pre-registered, CTO+COO sign. THEN produce -- **AMENDED 05:4xZ on B-1 (86087): the c02 mirror-pull CANNOT run here (two staged inputs absent), so B-4 is a FORWARD PRODUCTION of five never-produced dates on the FULL chain (`advi-49f-chain-dispatch`, one date per send, oldest-first), writing NEW keys in every table the chain writes (18 per the plan)**, under the gate's seven pre-registered conditions (CTO 86096) carried in the cell; re-emit 2026-08-18 LAST as its own arm on the c02 mirror-pull (its upstream tables exist) and read it against the pre-registration -- a manufactured return there is a finding, not a repair.

## Acceptance criteria -- B-1 through B-6, verbatim from cell `C02-g-7`

<criterion id="B-1" cell_refs="C02-g-7"/> **THE CAUSE, READ** per date, instrument named; the fix routed to its owner, not made here.
<criterion id="B-2" cell_refs="C02-g-7"/> **INPUT PRESENCE** per date (DS~N's read quoted with its denominator); absent-input dates EXCLUDED and printed UNBACKFILLABLE-INPUTS-ABSENT.
<criterion id="B-3" cell_refs="C02-g-7"/> **THE PLAN** under a FRESH never-widen (the c02-only sign-offs do not cover a full-chain production): the five dates NAMED BY HAND as the vehicle input with the `dim_calendar`-minus-stored derivation printed beside as the equality check (never `flow_ledger`); the full-chain vehicle with the engine read on the running artifact; per producer a00..c02 the vintage that will run vs the vintage that produced the 08-10/08-18 neighbours (identical or the difference named -- DS~N supplies the census; **no write before this is stated**); readers of ALL 18 tables announced (85486 form); per-date expected shapes pre-registered; SEQUENTIAL oldest-first with the per-date D-1 gate; the three pre-existing 08-11 partitions (dim_boundary/dim_calendar/dim_security, 2026-08-19T01:13Z) named with their disposition per the gate's ruling on condition (1); CTO+COO sign.
<criterion id="B-4" cell_refs="C02-g-7"/> **PRODUCTION** oldest-first, one date per send, per-date artifact oracle (D-1 present and conformant before D runs; a refused D-1 stops the run), mutex limb (ii) re-read before every date, floor ENABLED and untouched, publisher DISABLED, ledger via the tool; every new `twr_daily` partition carries vintage 946b5c5a3c... + schema "1.2" + ruled statuses only.
<criterion id="B-5" cell_refs="C02-g-7"/> **ACCEPTANCE** (CVO 86105 as graded): (i) 0 new versions on the 535 existing `twr_daily` partitions (f862baac5a instrument); (ii) five new `twr_daily` partitions with the current stamps; (iii) 0 new versions on EVERY other table the chain writes, the 18-table list from the plan printed as the denominator, EXCEPT the five date partitions in each -- the three 08-11 overwrites (if admitted) on their OWN line with pre/post digests; (iv) domain census after per table (535 -> 540, +5 elsewhere); (v) 2026-08-18 re-emitted LAST and read AS PREDICTED; the instance names its DATE SOURCE.
<criterion id="B-6" cell_refs="C02-g-7"/> proof VALID rc=0 positional B-1..B-6, checker vintage printed; graded by `3.0.0_SA_CVO`.

## Do NOT

- ⛔ **Do not emit before B-1 and B-2 are read and B-3 is signed.**
- ⛔ **Do not write to any existing key in ANY table the chain writes** -- new keys only; the sole candidates for an exception are the three named 08-11 dim partitions, and only on the gate's explicit ruling; B-5's per-table zero-new-versions listing is the arm.
- ⛔ **Do not derive the date set from `flow_ledger` or any output table** -- the hand-named list is the input; `dim_calendar` minus stored is the check.
- ⛔ **Do not repair the scheduler / dispatch here** -- route the cause's fix to its owner.
- ⛔ **Do not route anything on this subject to `4.0.0_SA_CRO`.**

## What is owed back, and when

**Message 1 at B-1 + B-2** (the cause per date + the input presence per date) to the issuer, the CTO and the CVO. **Message 2 = the B-3 plan** to the issuer + the CTO for the never-widen halves. **Then per-date reports, completion + B-5, the proof instance.** Surprise channel: one line to `3.0.0_SA_CVO` cc issuer.
