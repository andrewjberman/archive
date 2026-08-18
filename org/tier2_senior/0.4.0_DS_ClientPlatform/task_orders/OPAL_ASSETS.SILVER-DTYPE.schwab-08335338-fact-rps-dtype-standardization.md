# TO OPAL_ASSETS.SILVER-DTYPE — `schwab/08335338/silver/fact_rps` is ALL object/string dtype: silver is NOT DOING ITS ONE JOB (Rule 17)

<task_order id="OPAL_ASSETS.SILVER-DTYPE" project="OPAL_ASSETS">
<issued_to>0.4.0_DS_ClientPlatform (schwab silver converter lane: `data/assets/scripts/silver/schwab_conversion.py` + `schwab_schemas.py`; owned-paths `data/**` = ANY; DS authorship)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T13:50Z</issued>
<dated>2026-08-20 — DATED + OWNED. Sequenced BEHIND ADVI_BDPLAT_RESTORE.TO-1 (today) and MDPF_PROVENANCE.T-B (08-19) at the same DS seat. Not tonight; does not gate the restore (DS coerces at gold meanwhile — the correct consumer posture until this lands).</dated>
<status>staged -- DATED 2026-08-20, owner named</status>
<priority>P3 — a silver-job defect: every consumer of this silver is coercing dtypes it should not have to</priority>
<authority>CTO disposition 134609Z (owner + shape ruled). Surfaced by 0.4.0_DS_ClientPlatform 134424Z: `opal-data-assets/schwab/08335338/silver/fact_rps` carries EVERY column as object/string dtype incl. quantities/prices (94,637 x 63 on 08-17). Rule 17: silver = dedup + dtype standardization ONLY — dtype standardization IS silver's one job.</authority>
</task_order>

## The job — Rule 17 exactly, nothing more
Standardize dtypes at silver per the `fact_rps` contract: quantities/prices/market values NUMERIC,
dates DATE, ids STRING. **NO field slimming, NO fillna/dropna, NO business-row filter, NO dropped bronze
columns** (Rule 17's forbidden list — anything needing judgment about field relevance or null meaning is
gold's). Bronze stays raw (17a). Check the sibling `08242234` (MDPF) silver for the same defect and state
whether it applies there — **but touch NOTHING under `08242234` in this TO** (two-buckets law; if it has
the same defect that is its own TO under its own owner).

## `<data_reprocess_scope>` — MANDATORY (CTO Auto-Rule 4)
A dtype-only change on FUTURE writes leaves every historical partition object-typed, so consumers coercing
at gold must keep coercing until reprocessed. State ONE of: (a) re-conversion of the affected
`fact_rps` partitions (count printed / total) with mtime verification + a downstream freshness read on
B_00's next scheduled run; or (b) an explicit NO-REPROCESS block with reasoning and the named consumers
that therefore keep coercing (at minimum B_00.canonical_holdings post-ADVI_BDPLAT_RESTORE). Silence on
this = non-conforming.

## Acceptance
- SD-1: `schwab_schemas.py`/`schwab_conversion.py` emit `fact_rps` with the contract dtypes; a live
  post-change partition read shows numeric quantities/prices/MVs, date dates, string ids (dtypes printed).
- SD-2: column set byte-identical before/after (63 of 63; no slimming — Rule 17).
- SD-3: row count identical on a re-converted overlap partition; a value-tie to the cent on the numeric
  columns vs the pre-change object strings cast at read (the standardization changed TYPES, not values).
- SD-4: `<data_reprocess_scope>` stated + executed-or-explicitly-declined; consumers named.
- SD-5: `08242234` sibling assessed, untouched, finding stated.

<proof_of_spec>
  <expected_criteria>SD-1,SD-2,SD-3,SD-4,SD-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/OPAL_ASSETS.SILVER-DTYPE_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
Positional-id validation, check the rc. Deploy via `safe-deploy` (shared repo home `data/assets/scripts/silver` = S3-membership guard: key-exists = update). `comp-pipescript io schwab_conversion --pipeline assets` before write.

## reporting
COO (cc CTO). Surprise channel: one line, no action.
