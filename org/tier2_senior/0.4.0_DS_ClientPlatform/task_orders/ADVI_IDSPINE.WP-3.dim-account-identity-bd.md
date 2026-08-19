# TO ADVI_IDSPINE.WP-3 — gold `dim_account_identity_bd`, the fam superset (LAPTOP)

<task_order id="ADVI_IDSPINE.WP-3" project="ADVI_IDSPINE">
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T20:45Z</issued>
<dated>on WP-1</dated>
<status>staged -- GATED ON WP-1</status>
<priority>P1 -- this is the table that makes new accounts stop being invisible</priority>
<authority>SPEC_IDENTITY_SPINE_FAM_RESOLUTION_20260819.md §2 Layer 1 + §4 WP-3. Placement: LAPTOP (Rule 13 DS lane).</authority>
</task_order>

## Objective
Gold `dim_account_identity_bd` at **ACCOUNT grain** — the fam superset, refreshed daily: Relationship
ID (z-key), relationship name/SEC type, client name, registration type (36 values), account type
(15), roles x splits (Architect / Consultant / Implementor / LocalOps / Additional), open/closed,
inception.

Home: `opal-data-49financial/gold/advi/dimensions/` (the ruled home), **parquet + manifests**.

## GRAIN DISCIPLINE IS AN ACCEPTANCE CRITERION, NOT A STYLE NOTE
Rule 24: this table is **ACCOUNT grain and only account grain.** The spine is three tables at three
declared grains (group / account x group / account) — **we ADD tables, we do not overload one.** A
group-grain or membership-grain column appearing here is a schema defect, not a convenience.

## PROVENANCE PER ROW — the point of the whole spine
Every identity attribute block carries **`identity_source`** (`bd-allocation` | `fam-carried` |
`fam-live` | `bd-householding`) **+ `source_as_of`**, so a consumer can always see **which layer
answered.** This is what lets the carried fam data be used honestly instead of silently.

## CONFLICT LAW — ONE SOURCE OF RECORD PER FIELD; DISAGREEMENTS SURFACE, NEVER MERGE SILENTLY
- **Holder name:** BD Client Name is display SoR **where BD covers**; fam `col_5` is SoR **on the
  tail** (92.1% token agreement measured). **Disagreements beyond formatting land in a small
  RECONCILIATION LISTING — not a guess, not a silent pick.**
- **PII law carried:** fam `col_6` is TIN-shaped — **grouping-only, hashed anchor emitted** (a01's
  existing law). BD's z-keys are synthetic and safe.

## Acceptance criteria
- **WP3-1 FIELD CENSUS vs the 92-column header** — denominator printed, every column accounted for.
- **WP3-2 ROLES + SPLITS SUM TO 100% OR DECLARE** — a non-summing row is declared explicitly, never
  normalized away.
- **WP3-3 PROVENANCE COLUMNS PRESENT** (`identity_source` + `source_as_of`) and populated on every row.
- **WP3-4 CONFLICT LISTING EMITTED** for holder-name disagreements beyond formatting.
- **WP3-5 GRAIN ASSERTED:** account grain, one row per account, demonstrated not claimed.
- **WP3-6 proof instance VALID rc=0 positional: ids WP3-1..WP3-6.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>WP3-1,WP3-2,WP3-3,WP3-4,WP3-5,WP3-6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ADVI_IDSPINE.WP-3_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- Do not delete or stop consuming fam — **dormancy is never a deletion warrant and the carry is ruled.**
- No new triggers, no monitors. 49F-scoped only.

## Reporting
COO at landed, cc CRO~A. Session log w/ Compiler Tools section.
