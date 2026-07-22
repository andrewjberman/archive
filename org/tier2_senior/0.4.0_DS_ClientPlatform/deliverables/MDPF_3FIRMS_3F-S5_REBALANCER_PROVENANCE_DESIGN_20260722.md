# 3F-S5 — Rebalancer-family provenance columns: DESIGN (routed to CTO gate; nothing implemented)

**Agent:** 0.4.0_DS_ClientPlatform · **TO:** `MDPF_3FIRMS.3F-S5` @`1b9db36b3` · **Repo vintage:**
`61365878d` (converters unmodified by this commit — design only).
**Status: DESIGN-AND-ROUTE. No converter change lands before CTO's word (his 211330Z gate).**

## 1. Empirical current state (auto-rule 7; all read this session 21:0x–21:2xZ)

**The rebalancer family = FOUR tables** (converter header + live partitions):

| Table | Partition read | Rows × cols | Provenance columns |
|---|---|---|---|
| `fact_model_roster` | date=2026-07-22 | 60 × 15 | **NONE** |
| `fact_model_definition` | date=2026-07-22 | 554 × 11 | **NONE** |
| `fact_model_blend` | date=2026-07-22 | 29 × 9 | **NONE** |
| `fact_model_assignment` | date=2026-07-22 | 911 × 21 | **NONE** |

Reference shapes (the families that DO carry provenance, empirical):
- **Mirror family** (`fact_holdings` @07-20, `fact_assets` @07-22, `fact_portfolios_full` @07-21):
  `_source_file:string, _source_as_of:string, _source:string, _feed:string, _schema_version:string`
- **Schwab family** (`fact_rps_s2` @07-21):
  `_source_file, _source_as_of, _master_observed, _section, _schema_version`
  (`_master_observed`/`_section` are Schwab H1-identity mechanics — not applicable here)

## 2. Proposed column set — MATCH THE MIRROR FAMILY EXACTLY (zero deviation)

Append to all four tables, trailing the vendor columns (mirror convention):

| Column | Type | Value (OBSERVED at conversion, never synthesized) |
|---|---|---|
| `_source_file` | string | The bronze object key that yielded THIS ROW — per-row, since rebalancer partitions are multi-object: roster/assignment rows ← their `page_*.json`; definition/blend rows ← their `{GUID}.json` |
| `_source_as_of` | string | The bronze partition date (= assignment/pull date; the endpoint is live-state, so pull-date IS the as-of) |
| `_source` | string | `blackdiamond` (constant) |
| `_feed` | string | `rebalancer_models` \| `rebalancer_model_detail` \| `rebalancer_accounts` |
| `_schema_version` | string | `1.0` |

Rationale for the mirror match: `rebalancer_conversion.py` is a declared sibling of
`mirror_conversion.py` (its own header, `:3`), rides the same `silver_registry.silver_key` grammar,
and lives in the same converter deployment family. No deviation is proposed, so none needs justifying.

## 3. ⚠ THE DEDUP INTERACTION — the one mechanical subtlety (state it or ship a silent row-count change)

Today `dedup_exact` (`rebalancer_conversion.py:171`) is **whole-row** dedup over the concatenated
multi-page frame. A per-row `_source_file` makes two vendor-identical rows from DIFFERENT pages no
longer exact duplicates — **naive whole-row dedup after this change would stop collapsing them and
row counts could silently grow.**

**Design requirement: dedup runs on VENDOR COLUMNS ONLY (sidecar excluded), conflict semantics
unchanged.** Precedent: the SmartX family already dedups on all-columns-except-`_ingested_at`
(`silver.py:271-272`), which the 3F-S2 Rule-17 audit adjudicated compliant — the key excludes only
OUR OWN metadata, never vendor data. Phase-3 must include a row-count parity check (new converter on
a fixture == old converter row count) in addition to the ETag control.

## 4. The Rule-17 argument — both ways, explicitly (CTO rules; "useful" is not an argument)

**PERMITTED, because provenance is the conversion act's own observation (my recommendation):**
1. Adding these columns is **none of Rule 17's prohibited operations** — nothing slimmed, no
   fillna/dropna, no row filtered, no bronze column dropped, no vendor value altered.
2. Rule 17 bans **judgment about field relevance or null meaning**. Provenance requires zero
   judgment about the vendor's data: `_source_file` is the key the converter is ALREADY holding
   when it parses the object; `_feed`/`_source`/`_source_as_of` are facts of the conversion event
   itself. It is metadata OF silver's one job, in the same class as the parquet conversion.
3. The estate has already ruled this class three times: the mirror family, the schwab family, and
   SmartX `_ingested_at` all carry conversion-act metadata through silver — **the rebalancer
   family's ZERO-column state is the anomaly (S4 divergence D4), not the norm.**
4. The `_`-prefix namespace keeps ours-vs-vendor mechanically distinguishable; the dedup key
   (§3) keeps vendor semantics untouched.

**REFUSED, the honest case (each-layer-does-one-job spine):**
1. It IS a schema change to a landed silver surface; silver stops being "the vendor table and
   nothing else."
2. Admissibility creep: `is_opal` (a derived business LABEL) already rides these tables under a PRD
   ruling — each addition individually defensible, jointly a drift vector. If CTO refuses, the
   boundary would be: conversion-act metadata lives only in the per-partition manifest/meta layer,
   not in-table — the cost being that a ROW still cannot answer "which bronze object produced me"
   (the exact D4 defect), only a partition can.

**If refused, the alternative** is a meta-layer manifest keyed per partition (already partially
exists via the converter's manifest writes) — closes the partition-level question, leaves the
row-level question open. Stated for completeness; recommendation stands with PERMITTED.

## 5. Forward-only migration plan (the defining constraint)

- **Bronze:** untouched, by construction — the converter never writes bronze (17a; header `:18`).
- **Landed silver:** NEVER rewritten. **Pre-change baseline captured THIS SESSION (21:2xZ, s3api
  head-object) — the Phase-3 negative control compares against exactly these:**

| Partition | ETag | Bytes |
|---|---|---|
| fact_model_roster date=2026-07-21 | `2f957e9be29b7d29798632862e6fe2c6` | 13,442 |
| fact_model_roster date=2026-07-22 | `2f957e9be29b7d29798632862e6fe2c6` | 13,442 |
| fact_model_definition date=2026-07-21 | `fe432c358e05421ce2d358898ed19a44` | 16,433 |
| fact_model_definition date=2026-07-22 | `85b2b38730eeb9c5d8fddc9caeb43315` | 16,334 |
| fact_model_blend date=2026-07-21 | `e2458ba306a314a24053fcc09cd54edd` | 7,647 |
| fact_model_blend date=2026-07-22 | `e2458ba306a314a24053fcc09cd54edd` | 7,647 |
| fact_model_assignment date=2026-07-21 | `fa1f8e8f859a3282e98c750b17bf5c4a` | 47,414 |
| fact_model_assignment date=2026-07-22 | `fa1f8e8f859a3282e98c750b17bf5c4a` | 47,414 |

  (Side observation, corroborates 0.6.2's B6 liveness read: roster/blend/assignment are
  byte-identical across 07-21/07-22 — a stable book; only `fact_model_definition` moved.)
- **Cutover:** the first partition date produced by the changed converter — **published as an
  explicit `provenance_contract_start: YYYY-MM-DD` line in this design's implementation amendment
  AND in the converter header** the moment CTO's GO fixes the deploy date. Never implicit.
- **Absence semantics (the S5 design requirement):** a rebalancer partition WITHOUT `_`-columns =
  **PREDATES-CONTRACT** (honest, expected for every date < cutover). It must never be read as
  "provenance unknown/failed." Consumers get this rule from the S4 contract doc (D4 row updated at
  implementation) + the cutover constant. Same class as 0.6.2's `_complete/`-sentinels-from-06-23
  finding and CONTROLS_OVER_CARE III-c.
- **Reprocess scope: NONE.** Synthesizing provenance for rows whose provenance was never observed
  fabricates the exact metadata the columns exist to guarantee.

## 6. Affected code + tables (deliverable b)

| Artifact | Delta |
|---|---|
| `data/assets/scripts/silver/rebalancer_schemas.py` | +5 sidecar names appended to ROSTER/DEFINITION/BLEND/ASSIGNMENT_COLUMNS + the 4 pyarrow schemas; `assert_declared_shape` continues to enforce exact shape |
| `data/assets/scripts/silver/rebalancer_conversion.py` | parsers stamp the 5 fields per row (each already knows its bronze key + feed + date); `dedup_exact` → vendor-columns-only key (§3) |
| `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/{rebalancer_conversion,rebalancer_schemas}.py` | the DEPLOYED twin — lands via the normal artifact-swap TF cycle, **0.7.0's infra half** (he has this noted-not-started; coordinated) |
| Tables | all four, +5 trailing string columns, from cutover date forward |

## 7. Consumer enumeration (denominator stated; comp-blast structurally blind here — S4 finding (c), PRD v1.14 authorizes the text-sweep substitute)

Instrument: repo-wide `comp-grep` over the four table names, `.py` scope, tests/`__pycache__`
excluded, THIS session. **Denominator: every tracked `.py` in the workspace incl. the portal
submodule path space; hits = 7 files, of which consumers:**

1. **Writer:** `rebalancer_conversion.py` (repo) + its deployed lambda twin — the change site.
2. **Reader (only gold consumer):** `build_dim_model_portfolio.py:348-350` — reads roster, blend,
   assignment by NAME with per-column access (S4 §3 map) → **+5 trailing columns cannot break it**;
   its whole-row output is its own gold frame, not a passthrough.
3. **`fact_model_definition`: zero readers today** (CRO's composition work read BRONZE
   `rebalancer_model_detail`, not this table).
4. **Upcoming (mine):** 3F-G8/G3 read assignment/roster/blend — sequencing below.
5. **NOT consumers:** `mirror_conversion.py:781` (comment reference); `WSE_COTMDL.json` (record).

**3F-B6 non-disturbance (0.6.2):** his liveness signal reads BRONZE `rebalancer_model_detail/` —
this design writes only silver; bronze is untouched by construction. **No interaction.** (Confirmed
against the converter: no bronze write path exists.)

## 8. Sequencing (per COO 211524Z)

Implementation lands **after 3F-G8's build is landed and verified** (G8 reads three of the four
tables; a schema change mid-build is the two-edits-one-function class) — or earlier ONLY if CTO
explicitly sequences it ahead. G8's gate is now B5 alone, so G8 likely executes tomorrow on the
03:30Z landing; S5 implementation slots behind it. 0.7.0 coordinates the lambda-twin deploy in the
same window.

## 9. What CTO is asked to rule (the gate)

1. The Rule-17 question (§4) — permitted / refused / permitted-with-conditions.
2. The column set (§2) — mirror-exact, zero deviation.
3. The dedup-key change (§3) — vendor-columns-only, smartx-precedent.
4. The sequencing (§8) — post-G8 default.
