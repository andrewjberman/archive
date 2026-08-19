# TO ADVI_IDSPINE.WP-1 — silver `fact_bd_allocation` parse (LAPTOP; CHAIN HEAD, ungated)

<task_order id="ADVI_IDSPINE.WP-1" project="ADVI_IDSPINE">
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T20:45Z</issued>
<dated>startable NOW -- bronze lands today</dated>
<status>staged -- GO paired; UNGATED CHAIN HEAD of the identity spine</status>
<priority>P1 -- WP-2/WP-3 both gate on it, and WP-2 is already-cut work that currently has no upstream</priority>
<authority>SPEC_IDENTITY_SPINE_FAM_RESOLUTION_20260819.md §2 + §4 WP-1 (Andrew-commissioned at the CRO~A terminal ~2030Z, VERBATIM: "COO wants a game plan... draft a spec on how this could be done and issue to COO"). Placement: LAPTOP (49F/ADVI lane, Rule 13 DS).</authority>
</task_order>

## Objective
Parse the daily BD allocation export into silver `fact_bd_allocation`. **The export already lands
daily and survived the entire fam outage** — that durability is why the spec makes it the identity
plane's source of record.

## ⛔ RULE 17 IS THE WHOLE SCOPE: DEDUP + DTYPE STANDARDIZATION **ONLY**
**NEVER slim fields. NEVER fillna/dropna. NEVER apply a business-row filter. NEVER drop bronze
columns.** Anything requiring judgment about field relevance or null meaning is gold-tier business
logic and belongs in WP-2/WP-3, not here. The 92-column header comes through intact.

**Bronze stays raw and untouched** — the export lands as the vendor delivers it. Parquet is a
*silver* format; do not push it up into the ingest.

## Acceptance criteria
- **WP1-1 ROW/COL COUNTS TIE to the xlsx dimension reference** — both counts, both sides, printed.
- **WP1-2 RE-RUN IS IDEMPOTENT** — run it twice and show the second run changes nothing. An
  idempotency claim that was never re-run is an assertion.
- **WP1-3 DECIMAL DTYPES per the SILVER-DTYPE law** (the Travis-Decimal specimen is the pointer).
  Float-coerced money is the defect this criterion exists to catch.
- **WP1-4 NO FIELD LOSS:** the emitted column set is the bronze column set. Print both counts —
  equality is the criterion, not "looks complete."
- **WP1-5 proof instance VALID rc=0 positional: ids WP1-1..WP1-5.** MEASURED/RULED-class run rows
  only; INFERRED-class expected values are mechanically ineligible.

<proof_of_spec>
  <expected_criteria>WP1-1,WP1-2,WP1-3,WP1-4,WP1-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ADVI_IDSPINE.WP-1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- No new trigger machinery and no monitors — **P2's existing schedule floor covers the new runners**
  (the spec is explicit: zero new triggers). No vendor calls; this parses an export that already lands.
- 49F-scoped throughout. Never reference cot or bd firm planes (NEVER#2, gate + IAM enforced).

## Reporting
COO at landed, cc DS~B (WP-2/T2-DIMS gates on this) and CRO~A (spec author). Session log w/
Compiler Tools section = deliverable.
