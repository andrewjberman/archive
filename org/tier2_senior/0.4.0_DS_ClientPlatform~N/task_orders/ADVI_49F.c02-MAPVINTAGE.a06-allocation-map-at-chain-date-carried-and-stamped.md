# TO ADVI_49F.c02-MAPVINTAGE — a06 reads the NEWEST POPULATED allocation-map partition (header-only skipped) and STAMPS `map_date` + `map_carried` (cell C02-g-8; the filename's "at-chain-date-carried" is the first ruling's wording, WITHDRAWN at CTO 86490 — the body governs; title corrected 08:4xZ on 86765)

<task_order id="ADVI_49F.c02-MAPVINTAGE" project="ADVI_49F">
<issued_to>0.4.0_DS_ClientPlatform~N</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-30T08:1xZ</issued>
<decomp_ref>org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md -- <owned_cells>C02-g-8</owned_cells></decomp_ref>
<proof_of_spec>
  <expected_criteria>M-1,M-2,M-3,M-4,M-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~N/deliverables/ADVI_49F.c02-MAPVINTAGE.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form: python .tools/proof-of-spec-check.py <instance>.json M-1,M-2,M-3,M-4,M-5 ; print the checker's commit-ish beside the verdict -->
</proof_of_spec>
<status>M-1..M-3 DONE (DS~N 86765: fix @fec349cf79 deployed 08:42:34Z, served ETag == index blob, 4.0 h before the 12:45Z fire; M-4 after that fire; M-5 the re-drive GO 08:4xZ) -- was: pending -- GO on delivery of this face; M-1 (one read) first, then M-2/M-3 as fast as the DS gate allows: landing M-3 before ~12:40Z makes TODAY's 12:45Z fire the first exercise; otherwise Monday 2026-08-31 12:45Z is, and that fire is the one that matters (its abort would leave Tuesday's run with no D-1). The 12:45Z fire is NOT held (issuer 86469; CTO 86478 concurs).</status>
<priority>P1 -- a live scheduled-fire hazard with a ~4.5 h clock at cut; every C02-g-7 backfill date aborts identically until this lands; the crosswalk's emitted vintage is undeclared on every partition today.</priority>
<authority>AE~L's halt + census (86456: 13 of 46 map partitions empty, all weekend; a06 reads NEWEST regardless of D); the CTO's convention ruling (86478, adopted verbatim in the cell); the issuer's disarm + fire decision (86469); Rule 13 (DS commits + QA-deploys gold scripts). D2 drive-pair scope. Not to 4.0.0_SA_CRO.</authority>
</task_order>

## READ THIS FIRST -- the decomp cell is the specification

**`org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md`, cell `C02-g-8`.** The state, the ruled convention (i)-(v), the five criteria. **This face does not restate it.** Where the two differ, the cell governs.

## The one-paragraph version

`a06_dim_identity_crosswalk.py` reads the NEWEST `fact_allocation_account_map` partition regardless of the chain date; the map is header-only every Saturday and Sunday and lands after the 12:45Z fire, so Sunday's and Monday's fires abort at the (correct) :49 guard and every backfill date aborts the same way. M-1 is ANSWERED at cut (DS~N 86499: 08-23 Sun + 08-24 Mon both aborted @a06; the scope is SUNDAY AND MONDAY; the 08-29 backfill masked it). THEN implement the ruled convention at source (M-2) -- **as AMENDED by the CTO at 86490 (the 534 P14 crosswalks were built under NEWEST-map semantics; a date-matched read on five dates would island them):** a06 resolves the NEWEST POPULATED partition (header-only skipped); the guard at :49 refuses only when no populated partition exists at all; the crosswalk stamps `map_date` + `map_carried` (true when `map_date` != the chain date); a validator arm refuses a crosswalk with no `map_date`; unit arms reachable from four different truths. "The map at the chain's date" is QUEUED at the CTO as a series-wide re-derivation item, NOT this face. THEN deploy on the DS lane and READ IT ON THE RUNNING ARTIFACT (M-3: host `_code/` ETag == the INDEX blob's LF md5, never the worktree's). THEN read the first scheduled exercise from the S3 chain log (M-4). M-3 unblocks AE~L's re-drive of C02-g-7 (M-5).

## Acceptance criteria -- M-1 through M-5, verbatim from cell `C02-g-8`

<criterion id="M-1" cell_refs="C02-g-8"/> **THE FIRST READ -- ANSWERED AT CUT (DS~N 86499):** floor-form chain logs 12 of 560: 08-23 Sun AND 08-24 Mon both ABORT @a06 (Tue 08-25 OK, the negative control); 3 of 12 floor fires aborted; the 08-29 backfill wrote the missing 08-21 partitions and masked it. The instance quotes that census with its denominator; no further read.
<criterion id="M-2" cell_refs="C02-g-8"/> **THE CODE at source**: (i)-(v) implemented; four unit arms each reachable from a different truth (newest populated -> selected; newest header-only with an older populated -> the older selected, `map_carried=true`; no populated at all -> :49 refusal; no `map_date` on the emitted crosswalk -> refused); commit-gate clean; `safe-commit -F` on the DS lane.
<criterion id="M-3" cell_refs="C02-g-8"/> **THE DEPLOY read on the running artifact**: host `_code/a06_dim_identity_crosswalk.py` ETag == LF md5 of the committed INDEX blob, `_code/` VersionId printed; deploy ledger opened at the deploy, closed on this read.
<criterion id="M-4" cell_refs="C02-g-8"/> **THE FIRST SCHEDULED EXERCISE** read from the S3 chain log (never SSM stdout): a06's line with `map_date` + `map_carried`, the chain completing past a06; if M-3 missed today's fire, today's 12:50Z abort read is printed beside it as the pre-registered falsifier.
<criterion id="M-5" cell_refs="C02-g-8"/> C02-g-7's re-drive UNBLOCKED by M-3 (AE~L's act); proof VALID rc=0 positional M-1..M-5, checker vintage printed; graded by `3.0.0_SA_CVO`.

## Do NOT

- ⛔ **Do not touch the SmartX map** (upstream, another plane) and **do not hold the floor** (the fire is the falsifier; the issuer's act).
- ⛔ **Do not change a06's emitted schema** beyond the two stamped fields; **do not re-derive the 534 P14 crosswalks** here (a separate register item).
- ⛔ **Do not `cp` from the worktree** for the deploy reference -- the index blob is the identity (22a; four instances tonight).
- ⛔ **Do not route anything on this subject to `4.0.0_SA_CRO`.**

## What is owed back, and when

**M-1 as one line** to the issuer + CTO. **M-2 + M-3 together** (the commit hash, the deploy read) to the issuer, CTO, CVO and `0.7.0_AE_CloudOps~L` (whose re-drive waits on M-3) -- with the time against the 12:40Z mark stated. **M-4** after the fire. Proof instance at the close. Surprise channel: one line to `3.0.0_SA_CVO` cc issuer.
