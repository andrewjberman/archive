# SMARTX MODEL-FAMILY PRE-FIRE EXPECTATION REPORT (Part 1b)
## fact_model_aum_daily + fact_model_allocation_roster (run partition 2026-07-15)

**Filed by:** 0.4.0_DS_ClientPlatform, 2026-07-15 ~15:0xZ. **For:** 0.5.0_AE_OpalETL's model-table runs
(which wait on this). **Rides to:** CTO family review (rulings a1/keep/(c)-with-AC already landed
@ 7f76de167 -- this measures against that AMENDED contract). **Follows:** the atom report
(SMARTX_ATOM_EXPECTATION_REPORT_20260715.md @ 43bbc0385).

Both tables have a SMALL denominator (11 objects each), so unlike the atom's positions leg these
expectations are **PINNED, not sampled** -- I read ALL 11 of each live bronze object.

### Grounding / provenance
- **Denominator + rows:** live `boto3 get_object` over ALL 11 `model_aum` + ALL 11 `model_allocations`
  bronze objects for 20260715 (`s3://opal-data-assets/smartx/model/{rmid}/bronze/...`), read 2026-07-15 ~15:0xZ.
- **Schema contract:** `MODEL_AUM_SCHEMA` / `MODEL_ALLOCATION_ROSTER_SCHEMA` @ `silver.py:187/276`;
  parsers `parse_model_aum` @ `:199`. Amended-contract rulings @ 7f76de167.
- **Expected key shape (0.5.0-confirmed writer convention):** `smartx/platform/silver/{table}/date=2026-07-15/data.parquet`.

---

### TABLE 3 -- `fact_model_aum_daily` (MODEL_AUM_SCHEMA, 10 cols) -- PINNED
- **EXPECTED ROWS: EXACTLY 4,278** = `sum(len(data.performance))` over the 11 objects (read in full).
  - Per-model performance rows (8 non-empty): 1220, 484, 467, 462, 424, 424, 424, 373.
  - **This corrects the "~185 rows/model" inventory estimate** -- ground truth is 373-1220 per non-empty
    model (Sum 4,278), consistent with the `silver.py:200` code comment "~400-1200 per live model".
  - Each `run_date` partition carries the FULL-HISTORY series the vendor served that day (not a single
    day) -- so the table re-lands the whole history per partition, by design.
- **3 EMPTY-SERIES models -> 0 rows each, NAMED holes** (not silent): `rmid` prefixes `53ba340c`,
  `920c1026`, `e32a9399`. All THREE empty signals AGREE (`performance=[]` AND `totalAum=0.0` AND
  `enterprise=null`) -> a legitimate empty. **The (c) three-signal discriminator's RAISE mutant is the
  FUNDED-but-empty case** (`totalAum>0` with `performance=[]`) -- NONE observed this partition; if one
  appears, the converter must RAISE, not emit 0 rows silently.
- **Schema (10):** `rmid, run_date` (string); `enterprise_id, enterprise_name` (string); `total_aum`
  (float64); `day` (date32); `performance_ts` (int64); `performance_date_friendly` (string);
  `closing_equity` (float64); `_ingested_at` (string).
- **AMENDED CONTRACT (CTO ruling a1):** **NO `model_id` column** -- the payload `data` key union is
  `{enterprise, performance, totalAum}` (measured, 11/11), carrying NO model identity. `rmid` (from the
  filing key) IS the identity; `model_id` is a GOLD join. A permanently-null injected `model_id` would be
  a hypothesis, not data.
- **`total_aum` PRESERVED but mis-scaled** (grounded range this partition: 6,897,854 to 161,399,446,373 --
  five orders of magnitude) -- gold ignores it (D4 8.6). Silver preserves as delivered (Rule 17).
- **`day` is date32 STANDARDIZED from the vendor epoch, ADDITIVE:** both raw renderings (`performance_ts`
  int64 epoch, `performance_date_friendly` string) preserved alongside -- never lossy.
- Natural key `(rmid, day, run_date)`; a CONFLICTING duplicate (same key, different `closing_equity`)
  RAISEs (`MapShapeError`), an IDENTICAL duplicate collapses. Expect 0 conflicts.

### TABLE 4 -- `fact_model_allocation_roster` (MODEL_ALLOCATION_ROSTER_SCHEMA, 13 cols) -- PINNED
- **EXPECTED ROWS: EXACTLY 9,540** = `sum(len(data))` over the 11 objects (read in full), one row per
  allocation record, ALL statuses.
- **Status breakdown (grounded): `open` 7,125 / `close` 2,381 / `workingClose` 34** = 9,540 (matches the
  `silver.py:288` census exactly). ALL statuses kept -- no business-row filter (Rule 17).
- **Field presence -- 100% populated (9,540/9,540 each):** `model.id`, `model.name`, `advisor.crd`,
  `allocationId`, `openedDate.timestamp`, `value`. No nulls in these this partition.
- **Schema (13):** `model_id, model_name, rmid, allocation_id` (string); `advisor_id, advisor_name,
  advisor_crd` (string -- **`advisor_crd` BYTE-FAITHFUL, never numeric-coerced**: a leading zero lost at
  silver is a failed gold join); `value` (float64); `status` (string); `opened_ts` (int64),
  `opened_date_friendly` (string); `run_date, _ingested_at` (string).
  - `model_id`/`model_name` HERE come from `record.model.{id,name}` (delivered per record, present in all
    9,540) -- distinct from the AUM table where model identity is absent. `+2` preserved vendor fields
    (`model_name`, `opened_date_friendly`) beyond the ruling's list -- never-slim (Rule 17), flagged for
    your family review.

---

### CROSS-FEED CONSISTENCY INVARIANT (a firm-wide check the skeleton hands CTO)
Three INDEPENDENT smartx feeds each enumerate the SAME allocation fleet on 2026-07-15:
| feed | table | count |
|---|---|---|
| `allocation/{id}/bronze/holdings` (atom) | `fact_allocation_valuation` (1 envelope/allocation) | **9,540** |
| `model/{rmid}/bronze/model_allocations` | `fact_model_allocation_roster` (1 record/allocation) | **9,540** |
| (bronze object count, the atom denominator) | -- | **9,540** |
**These three MUST agree.** A divergence = a dropped allocation somewhere (a real defect, not growth).
Recommend wiring `distinct(fact_allocation_valuation.allocation_id) == distinct(fact_model_allocation_roster.allocation_id)`
as a cross-table gate (both should equal the 9,540 fleet).

### RULE-17 / DTYPE EXPECTATIONS
- ids/dates/crd stay STRING byte-faithful; counts int32 / epochs int64 / values float64 per the EXPLICIT
  pinned schemas (never pandas-inferred).
- dedup = exact-duplicate rows only; NO slimming, NO fillna/dropna. Empty-series models are NAMED holes
  (0 rows), not dropped-silently; the funded-but-empty case RAISEs.

### ACCEPTANCE INSTRUMENT (V2-8 / Rule 22a)
- Landing = `ListObjectsV2` key+ETag+Size; row counts read from the LANDED parquet (behavioral, not self-report).
- Falsifiable run-time checks:
  1. `fact_model_aum_daily rows == 4,278`; exactly 3 empty-series models (named); 0 funded-but-empty RAISEs;
     0 `(rmid,day,run_date)` conflicts.
  2. `fact_model_allocation_roster rows == 9,540`; status split 7,125/2,381/34; `model_id`/`advisor_crd`
     non-null 9,540/9,540.
  3. CROSS-FEED: roster distinct allocation_id == valuation distinct allocation_id == 9,540.

### OPEN (for 0.5.0 + CTO)
- The `+2` never-slim roster fields (`model_name`, `opened_date_friendly`) -- confirm they stay (Rule 17 says yes).
- Part 2 (the 7-feed table-or-exemption skeleton) follows -- it feeds YOUR rulings.
