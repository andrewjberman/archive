# OPAL_ASSETS V2-8 -- PRE-FIRE EXPECTATION REPORT (the swap-gate input)

**Author:** 0.6.2_AE_PartnerETL . 2026-07-14 ~16:5xZ . repo vintage `e9d1a6817` (CLOUD)
**Gate:** CTO 113326Z (shape: units, expected rows per type incl. fam/slm CS-path + rps_s2, verification
classes) + CTO 162512Z (the eclipse dtype-refusal class, priced in). B-compressed precedent (DS 101619Z).
**Converter state:** deployed artifact = V2-7 loud no-op stub (5f6308383 @ 09:50Z); source = the reviewed
CRS family (deltas 1-4, head c36710809; suite 152 passed + 7 skipped). Swap vehicle = 0.7.0's saved plan
(0/2/0); TF already pins py3.11 / 3008MB / 600s (`infra/aws/terraform/opal-assets/silver.tf:410`), source
map carries the same (`opal-assets-silver-schwab`).

**What this is:** the numbers the first real conversions MUST match. Anything else post-swap is a finding.
Every number below is MEASURED -- either committed evidence (cited) or this session's read-only exercises
(GetObject + ListObjectsV2 only; ZERO writes; not a gold run; no artifact produced). Two lanes are reported
separately throughout: **0824 = "SCHWAB-RPS basis" / 0833 = "BD-sourced 49F basis"
(`conversion_manifest.BASIS_LABEL`, key-tied by test). NO combined totals exist in this report.**

---

## 1. UNITS

**Partition unit:** one (master lane, type, business-date). Landing grammar
`schwab/{master}/silver/fact_{type}[_s{N}]/date=YYYY-MM-DD/data.parquet`; projections `dim_*` same grammar.

**Row units (grain), dictionary SS2a + measured bytes:**

| table | one row is | table | one row is |
|---|---|---|---|
| fact_acc | an ACCOUNT | fact_rld | a realized lot (DAILY file) |
| fact_rps | an account x asset POSITION | fact_rlu / fact_rly | a realized lot (cumulative / yearly) |
| fact_rps_s2 | an ACCOUNT (balance section D2) | fact_rlw | a realized lot (weekly; **0824-ONLY type**) |
| fact_trn | a TRANSACTION event (per-partition APPEND, row key REFUTED v1.2.1) | fact_rtu / fact_rty | a tax-lot detail row (cum. / yearly) |
| fact_sec | a SECURITY | fact_upn / fact_upt | a pending-position row (DP family) |
| fact_uln / fact_ult | an unrealized lot (latest / sibling window) | fact_fam / fact_slm | an account x person IDENTITY row (**0833-ONLY, CS channel**) |

**Numeric units (DTYPE LAW, schwab_schemas.py header):** value columns = `decimal128(P,S)` pinned from the
VENDOR's own sign + zero-padded fixed field width (the width IS the precision bound) -- dollar amounts and
share/quantity fields at the vendor's declared scale, never a measured-magnitude guess. Dates = `date32`
from YYYYMMDD bytes. EVERYTHING else -- ids, account numbers (padding is information), codes,
whole-number-looking unsigned fields -- is STRING ("string until measured", Rule 17).
**Columns out = vendor columns + 5 provenance** (`_source_file, _source_as_of, _master_observed, _section,
_schema_version`), always last, always string.

## 2. EXPECTED ROWS PER TYPE -- the exercised numbers (latest landed partitions)

**Method:** the committed conversion path itself -- `crs_reader.parse_crs` / `cs_reader.parse_cs` ->
`dedup` -> `schwab_schemas.typed_table` -> `schwab_projections.project` -- exercised IN MEMORY over the
exact latest bronze partition of every type, BOTH lanes (29 objects, run-time-enumerated per 13b), zero S3
writes. **Result: 29/29 files, ZERO errors, every pipe file T1-tied, dedup removed 0 rows, all 8
projections exact-parity.** These are the rows the first real conversions of these partitions must land.

### 0824 -- SCHWAB-RPS basis (lane reported alone; never summed with 0833)

| table | date | rows_out | cols_out | verification |
|---|---|---:|---:|---|
| fact_acc | 2026-07-13 | 7,073 | 95 | T1_RECONCILED |
| fact_rps | 2026-07-13 | 92,103 | 63 | T1_RECONCILED |
| fact_rps_s2 | 2026-07-13 | 7,074 | 39 | T1_RECONCILED |
| fact_trn | 2026-07-13 | 890 | 140 | T1_RECONCILED |
| fact_sec | 2026-07-13 | 2,056 | 74 | T1_RECONCILED |
| fact_uln | 2026-07-13 | 271,580 | 61 | T1_RECONCILED |
| fact_ult | 2026-07-13 | 194,605 | 61 | T1_RECONCILED |
| fact_upn | 2026-07-13 | 56,214 | 44 | T1_RECONCILED |
| fact_upt | 2026-07-13 | 35,787 | 44 | T1_RECONCILED |
| fact_rld | 2026-07-13 | 453 | 86 | T1_RECONCILED |
| fact_rlu | 2026-06-05 | 287,566 | 87 | T1_RECONCILED |
| fact_rlw | 2026-07-10 | 250,201 | 80 | T1_RECONCILED |
| fact_rly | 2026-06-30 | 234,639 | 87 | T1_RECONCILED |
| fact_rtu | 2026-06-05 | 114,209 | 75 | T1_RECONCILED |
| fact_rty | 2026-06-30 | 77,675 | 75 | T1_RECONCILED |
| dim_position | 2026-07-13 | 92,103 | 30 | = fact_rps rows (parity exercised) |
| dim_balance | 2026-07-13 | 7,074 | 39 | = fact_rps_s2 rows (parity exercised) |
| dim_transaction | 2026-07-13 | 890 | 44 | = fact_trn rows (parity exercised) |
| dim_asset | 2026-07-13 | 2,056 | 29 | = fact_sec rows (parity exercised) |

### 0833 -- BD-sourced 49F basis

| table | date | rows_out | cols_out | verification |
|---|---|---:|---:|---|
| fact_acc | 2026-07-13 | 7,146 | 95 | T1_RECONCILED |
| **fact_fam (CS)** | 2026-07-13 | **7,093** | 11 | **UNVERIFIED_BY_T1** |
| **fact_slm (CS)** | 2026-07-13 | **7,094** | 11 | **UNVERIFIED_BY_T1** |
| fact_rps | 2026-07-13 | 93,607 | 63 | T1_RECONCILED |
| **fact_rps_s2** | 2026-07-13 | **7,147** | 39 | T1_RECONCILED |
| fact_trn | 2026-07-13 | 930 | 140 | T1_RECONCILED |
| fact_sec | 2026-07-13 | 2,315 | 74 | T1_RECONCILED |
| fact_uln | 2026-07-13 | 273,680 | 61 | T1_RECONCILED |
| fact_ult | 2026-07-13 | 197,201 | 61 | T1_RECONCILED |
| fact_upn | 2026-07-13 | 56,629 | 44 | T1_RECONCILED |
| fact_upt | 2026-07-13 | 36,874 | 44 | T1_RECONCILED |
| fact_rld | 2026-07-13 | 453 | 86 | T1_RECONCILED |
| fact_rlu | 2026-06-05 | 289,336 | 87 | T1_RECONCILED |
| fact_rly | 2026-06-30 | 236,352 | 87 | T1_RECONCILED |
| fact_rtu | 2026-06-05 | 114,767 | 75 | T1_RECONCILED |
| fact_rty | 2026-06-30 | 78,846 | 75 | T1_RECONCILED |
| dim_position | 2026-07-13 | 93,607 | 30 | = fact_rps rows (parity exercised) |
| dim_balance | 2026-07-13 | 7,147 | 39 | = fact_rps_s2 rows (parity exercised) |
| dim_transaction | 2026-07-13 | 930 | 44 | = fact_trn rows (parity exercised) |
| dim_asset | 2026-07-13 | 2,315 | 29 | = fact_sec rows (parity exercised) |

**Cross-checks that tie:** (a) parsed == attested on every pipe file (T1 inside `parse_crs`, hard-raise);
(b) rows_out == parsed on every table (dedup removed 0 on these partitions -- the dedup stays live for
genuine dupes); (c) the reader reproduces the committed two-vintage census EXACTLY on the shared
partitions (0833 acc 7,146 / rps 93,607 + s2 7,147 / sec 2,315 / trn 930 / fam 7,093 / slm 7,094 @
0270e70dc); (d) cols_out == vendor + 5 provenance everywhere (acc 90+5, trn 135+5, fam 6+5; dims 25/34/39/24 +5).
**Observations (recorded, not adjudicated):** 0824 acc 7,073 vs 0833 acc 7,146 -- close-but-different is
expected (D3: overlap SET 7,053); rld @ 07-13 = 453 rows in BOTH lanes (byte sizes differ, 49,154 vs
49,231; each ties its own T1 independently).
**Daily-band note:** future daily partitions drift by small day-over-day deltas off these anchors; a
first-fire row count in this band, T1-tied, is nominal. A count far outside the band that still T1-ties is
vendor-real (report, don't refuse).

## 3. VERIFICATION CLASSES (manifest vocabulary, cell-4 rider 1)

- **T1_RECONCILED** -- every pipe (CRS) table. Parsed rows tie the vendor's own T1 trailer attestation or
  the conversion refuses WHOLE (`CrsReconciliationError` lands nothing). Exercised this session: 27/27
  pipe files at the latest partitions, plus 46 more pipe parses across backlog vintages (SS5).
- **UNVERIFIED_BY_T1** -- fact_fam / fact_slm only (CS channel: headerless CSV, `CS{MMDDYY}`, NO trailer
  EXISTS). Structural width-control only; honestly weaker, never dressed as tied. The manifest carries the
  class so a reader of the manifest alone sees it.
- Never a PASS that silently checked nothing (`NO_CONFIG`-class outputs do not exist in this vocabulary).

## 4. THE BACKLOG (what the ratchet must retire) -- guard-baseline denominators

Live pre-deploy baseline (committed transcripts, ListObjectsV2 walks, 2026-07-14 ~11:2xZ), re-verified this
session (key recount ties: 0824 = 5,978 bronze keys, 0833 = 6,945):

| lane | bronze keys | shortfall entries (facts+projections) | named holes | surplus | collisions |
|---|---:|---:|---:|---:|---:|
| 0824 | 5,978 | 7,468 | 1,040 | 0 | 0 |
| 0833 | 6,945 | 8,436 | 1,039 | 0 | 0 |

**The arithmetic ties exactly** (checked, both lanes): shortfall = fact partitions (incl. fact_rps_s2 as
its own table, 506) + 4 projections x 506. 0833: 5,906 facts + 506 s2 + 2,024 dims = 8,436. 0824: 4,938 +
506 + 2,024 = 7,468. Named holes = tcf 754 + tcfx 183 + tnn 102/103 -- reader-variance types, UNCONVERTED-
not-absent, **never converted by this family and never silently absorbed; they stay named forever.**
**RLD day-law refusals in the backlog: ZERO -- enumerated, not assumed.** All 754 delivery dates in BOTH
lanes carry rld, so `assert_rld_covered` refuses no date (`rld_refused_dates: []` expected in every sweep
manifest).

## 5. THE DTYPE-REFUSAL CLASS, PRICED (CTO 162512Z) -- and the one refusal family it FOUND

**Structural answer:** the eclipse mechanism (a value column declared int off a single-vintage whole-value
measurement) CANNOT fire here -- `schwab_schemas.py` @ e9d1a6817 contains **ZERO integer declarations**
(grep `int64|int32|pa.int` = 0; 275 decimal128 columns). Ints were never derived from measured magnitudes:
the DTYPE LAW pins decimal128 precision from the VENDOR's own field width, and whole-looking numerics
without the sign+fixed-width signature stay STRING.

**Exercised answer (newest):** full typed path, 29/29 latest partitions, both lanes -- ZERO cast errors (SS2).

**Exercised answer (backlog vintages) -- this is where the priced prediction has real content.** The same
typed path was run over the OLDEST + MIDDLE partition of every type, both lanes (58 objects, incl. the
2023-07 deep history that predates the 20240708 stability control). Result: **46/58 convert clean**
(incl. acc/rps/trn/uln at the 2024-07-08 census control -- e.g. 0833 acc 4,075 / rps 57,927 + s2 4,075 /
trn 10,869 / uln 64,011, byte-identical to the committed census), **12 refuse -- ALL loud, ALL in the
realized-lot rl\* family, ZERO dtype/cast errors anywhere:**

1. **Vendor layout APPEND, measured to the day:** `schwab_order_id` + `versmrkr_7/8` appear in
   RLD/RLU/RLY on **2025-07-18 exactly** (binary-searched on rld, 10 probes; boundary re-probed identical
   on BOTH lanes; rlu/rly bracket-probed consistent; rlw's history starts 2025-09-05, post-boundary, all
   clean -- consistent with its 2/2 samples passing). Partitions BEFORE the boundary lack those columns;
   the pin (measured at newest-vintage only for these types) classifies them CORE; the vintage-aware drift
   law therefore refuses them: `SchemaDriftError` -> `action=failed`, lands NOTHING, named in the sweep
   manifest. **Exact expected refusal counts, identical both lanes: rld 506 + rlu 8 + rly 24 = 538 per
   lane.**
2. **One zero-row shell per lane:** `rld @ 2025-01-09` (525/513 bytes -- the national day of mourning,
   markets closed; trading-calendar-consistent). `parse_crs` refuses it as `CrsFormatError: no data rows`
   -> quarantine class. **1 per lane.**

**Expected steady-state after the full ratchet, BEFORE any pin extension: residual shortfall = 539 per
lane** (538 drift + 1 shell; rl\* types carry no projections, so no dim residue), holes stay 1,039/1,040,
surplus 0, collisions 0. **Retired by the ratchet: 8,436 - 539 = 7,897 (0833) and 7,468 - 539 = 6,929
(0824).**

**The remedy is already the module's own printed path** (measure the vintage -> reclassify
`schwab_order_id`/`versmrkr_*` as APPENDED with census date 2025-07-18 -> pre-boundary partitions NULL-fill
honestly per the ambiguity-window law). That is a delta-5 pin edit + DS contract touch; the shell wants its
own small ruling (0-row-shell law like the mirror family's, i.e. land an empty T1-attested partition, vs
stay-quarantined). **Both are named DECISIONS at your gate, not code I have changed. The swap does NOT wait
on them unless you say so: pre-boundary rl\* refusals are loud, idempotent, and retire cleanly on a later
pin extension; nothing lands wrong meanwhile.**

## 6. EXPECTED POST-SWAP BEHAVIOR, IN ORDER

1. **At apply (0.7.0's saved 0/2/0):** no invocation -- the swap is an artifact/config motion; nothing
   fires without a bronze landing or a schedule.
2. **Zero-event window until the next landing:** ZERO conversions, ZERO manifests. Expected and healthy.
3. **Evening fires 21:45Z (0833) / 22:15Z (0824) -- the FIRST evening fires (schedules born 07-14, no
   precedent).** Two nominal branches: (a) vendor has not posted 07-14 files by then -> `downloaded=0,
   ok=true` run manifest, zero events (healthy skip; frontier logic); (b) files posted -> per-object S3
   events, one conversion each, ~9-10 pipe (+2 CS on 0833) partitions dated 2026-07-14, rows in the SS2
   band, T1-tied, per-lane EVENT manifests under `schwab/{master}/meta/conversions/{run_id}.json`. **No
   RLD batch-refusal on events by design** -- the day law binds in the sweep (`schwab_runtime.py:12-16`);
   the event path converts singles as they land. The stub-era landings of 07-13 partitions are ALREADY
   bronze; they convert via sweep, not via a re-fired event.
4. **Sweep 12:15Z 07-15 = ratchet run #1** (`cron(15 12 * * ? *)`, silver.tf:151): pre-verdict prints the
   full backlog (SS4 numbers); converts misses in sorted-key order, lane 0824 first
   (`DECLARED_SCHWAB_MASTERS` order). **`_sweep_lane` has NO per-run time bound -> EXPECT the 600s Lambda
   timeout to KILL run #1 mid-backlog.** That is the PREDICTED signature of a 12.9K-partition backlog
   meeting a 10-minute window, not a failure: every landed partition is durable + idempotent
   (`already_converted` skips on the next pass), and the killed run's manifest + backfill-status simply DO
   NOT land (they write post-loop). **A missing 07-15 sweep manifest = nominal.** Because 0824 sweeps
   first, 0833 may see zero sweep progress until 0824's lane drains.
5. **Throughput anchor + drain path:** largest single type measured 10.6s typed+parquet (rlu 289K x 82,
   silver.tf:410 note); most backlog partitions are small dailies. ESTIMATE (labeled as such): ~150-600
   conversions per 600s run -> the backlog does NOT drain on one natural sweep/day in useful time.
   **Recommendation at your discretion: after first-conversion signoff (AC-3), drive the ratchet with
   repeated `{"mode":"sweep"}` invocations** -- each is idempotent and monotonic; the guard's
   shortfall_pre/post pair in each completed manifest IS the ratchet meter. I do not fire these without
   your word.
6. **Verdict trajectory:** backfill-status `guard_verdict` = FAIL (honest full-lane shortfall) shrinking
   run over run -> steady-state FAIL at exactly 539/lane residual (SS5) until the delta-5 pin extension ->
   then PASS with holes named. The FAILs before that point are the guard being honest about work
   remaining, per design; only a shortfall that STOPS shrinking (with no timeout-kill explanation) or ANY
   surplus/collision > 0 is a real alarm.

## 7. FAILURE SIGNATURES (so nothing gets smoothed at 22:00Z)

| signature | meaning | lands data? |
|---|---|---|
| `CrsFormatError` -> `quarantined` + quarantine key | unreadable/unknown shape (incl. the 2025-01-09 shells) | nothing (quarantine marker only) |
| `CrsReconciliationError` -> `failed` + re-raise -> retry x2 -> DLQ | parsed != T1 attested (the silent-drop falsifier) | NOTHING |
| `SchemaDriftError` -> `failed` | unknown column / CORE-missing (incl. the 538/lane pre-boundary rl\*) | NOTHING |
| `ArrowInvalid` / cast raise -> `failed` | a vendor byte that does not fit its pinned type (0 observed in 87 exercised parses) | NOTHING |
| manifest `ok: false` + per-type verdicts | >=1 result not converted/idempotent, or projection parity broke | per-object |
| `scope_mismatch` finding on a result | H1 master != folder claim (the BYTES win, finding carried) | converts under OBSERVED master |
| event lambda death (unhandled) | async retry x2 -> DLQ; next sweep drains + reports it (cap 100/manifest) | visible in sweep manifest |

A refusal is never a partial landing: write-order is record -> manifest -> raise, and every write is
verified (`_put_table_verified` / `_write_parquet_verified`).

## 8. INSTRUMENTS + DENOMINATORS OF THIS REPORT (Rule 22/22a)

- **Enumerations:** ListObjectsV2 full walks, ContinuationToken drained; denominators printed at run time:
  30 latest-partition keys; 5,978 + 6,945 bronze keys (== the guard-baseline transcripts); 754 + 754 rld
  dates; 58 vintage-sample keys; 12 + 12 rlu, 36 + 36 rly date lists.
- **Exercised:** 87 bronze objects parsed through the committed path this session (29 newest + 58
  oldest/middle), ~650MB read, ZERO writes to any bucket. The positive control: the 20240708 census
  partitions re-produce the committed census numbers byte-for-byte.
- **Coverage statement:** every (lane, type) at newest vintage; oldest + middle vintage per (lane, type);
  boundary binary-search on rld with bracket probes on rlu/rly, both lanes. NOT exercised: the remaining
  ~1,300 middle partitions per lane (sampled, not swept -- the sweep itself is the full-population pass);
  the Lambda runtime environment (that is the swap's own first fire); IAM (exercised at container deploy).
- **Committed evidence this report folds:** guard transcripts + live baseline
  (`OPAL_ASSETS_V28_SET_IDENTITY_GUARD_MUTANT_TRANSCRIPTS_20260714.md`), two-vintage typed census
  (`OPAL_ASSETS_V28_TYPED_COLUMN_CENSUS_BOTH_VINTAGES_20260714.json` @ 0270e70dc), contract v1.2.2
  (e89f71c0e), dictionary (`docs/architecture/OPAL_RUNNERS_49F_SILVER_DATA_DICTIONARY.md`), the family
  commits 61130d39b / 10dcc8e81 / 26e5f51f7 / d87a9cec8 / c36710809.
- **Session transcripts committed alongside:** `OPAL_ASSETS_V28_PREFIRE_EXERCISE_TRANSCRIPTS_20260714/`
  (newest-partition results, vintage-sample results, boundary probes, shell census).

---

**Bottom line for the gate:** the family's numbers are pinned by exercise on the exact bytes it will meet;
the one refusal family on the backlog is measured to the day (2025-07-18), counted exactly (539/lane),
loud, idempotent, and retirable by the module's own documented remedy; the dtype class you asked me to
price cannot fire structurally and did not fire in 87 exercised parses. The swap is safe to sign on these
predictions; deviations from ANY number above are findings, and I will be watching the fires against this
table.
