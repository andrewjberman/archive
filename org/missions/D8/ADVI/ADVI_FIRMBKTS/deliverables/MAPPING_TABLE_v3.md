# ADVI_FIRMBKTS round 3 -- MAPPING_TABLE_v3 (FB-f-2, the table repair under the grain ruling)

Supersedes `mapping_v2.json`. Machine table: `mapping_v3.json` (this folder). The census is `census.json`, listed_at 2026-10-09T20:36:32Z, never edited. Live listings are read-only list_objects_v2 calls (all pages) for every class this repair touched; they are dated per regrid below (2026-10-11T06:56:05Z to 2026-10-11T06:59:50Z). Keys are never printed here: classes, prefixes, tails and counts only.

## Denominators

- Census: 444 classes; 238,861 objects (bd 216 classes, 131,391 objects; inf 174, 99,668; cot 54, 7,802).
- Live total: 35,973 objects across the 9 listings this repair took (the 5 interleaved inf classes, cot bronze/, bd gold/clients/, gold/timeseries/ and logs/). The census is not re-listed in full; no other class was touched.

## Dispositions (rows)

| disposition | rows | note |
|---|---:|---|
| MOVE | 349 | includes 4 kind-marker rows (state) and the class-grain gold/clients/ row |
| HOME | 2916 | per-date children of the bronze and silver re-grids, opal-data-assets |
| RETIRE | 93 | 7 zero-byte placeholders (rule a, live HEAD size 0 on all) and the probe/ output (RB) |
| DECISION | 2 | FWD-7 and FWD-8 only, unchanged |
| FAULT | 84 | owner 1.0.0_SA_CTO~DELL1 on every row |
| total | 3444 | |

FAULT before: 89
FAULT after: 84

FAULT after does not exceed FAULT before. Removed from FAULT (10 rows, by key): bd gold/clients/; bd gold/cohorts/; bd gold/filters/; bd gold/nna/; bd gold/snapshots/; bd gold/summary/; cot bronze/; inf bronze/orion-api/; inf gold/eclipse/; inf silver/eclipse/. Added to FAULT (5 rows, by key): inf bronze/eclipse/_history/; inf bronze/eclipse/_meta/; inf bronze/orion-api/backfill_results/; inf bronze/orion-api/latest/; inf gold/eclipse/_meta/. The two groups are shown in full in the change list below; the net is -5.

## What changed, rule by rule

**(a) zero-byte folder placeholders: RETIRE.** 7 placeholder rows, each `placeholder_key` equal to its class prefix: bd gold/clients/, gold/timeseries/, gold/cohorts/, gold/filters/, gold/nna/, gold/snapshots/, gold/summary/. Live HEAD returns size 0 for all 7 (check arm T1). gold/clients/ is placed AT its class prefix with `exclude_keys: [gold/clients/]` (its 2948 data objects, one per client file, are not enumerated; one MOVE row). The other six keep their re-grids and their children.

**(b) completion markers: `kind: marker` at class grain with `marker_match` literal tails.** Placed: cot bronze/ (`_BRONZE_COMPLETE.json`, 113 objects, no data) under `state/bronze_complete` (cot-bronze-complete); inf bronze/orion-api/ (`_BRONZE_COMPLETE.json`, `_BRONZE_COMPLETE_qa.json`) under `state/bronze_complete`; inf gold/eclipse/ (`gold_complete.json`) under `state/gold_complete`; inf silver/eclipse/ (`silver_complete.json`) under `state/silver_complete`. Not placed: inf bronze/eclipse/ and bronze/eclipse_qa/ `pull_complete.json` markers, which share state keys for shared dates (66 keys): FAULT rows, owner 1.0.0_SA_CTO~DELL1 (round-2 rule 1e). Every `marker_match` tail is literal; the largest matched object is under 4 KiB in every class, so no finding row is needed. The inflection and silver families are not named by the ruling (surprise row ADVI_FIRMBKTS-D1-W12-S5).

**(c) interleaved classes re-gridded per date partition, no child cap.** Five classes (round-2 FAULT). Each keeps its marker row (b); its data is re-gridded into one child per date partition (the directory names that carry a date); a partition with only marker objects has no data child. Non-date objects are FAULT children, or RETIRE (probe output, RB). The per-class identity is `marker_objects + data_objects == listed_objects`, and the children sum to the same total (asserted in the build).

| class | markers | date children | data objects | non-date remainder | census | live | diff |
|---|---:|---:|---:|---|---:|---:|---:|
| inf bronze/eclipse/ | 134 | 134 | 1,664 | _history/ FAULT 55; _meta/ FAULT 1 | 1,785 | 1,798 | +13 |
| inf bronze/eclipse_qa/ | 67 | 67 | 804 | none | 858 | 871 | +13 |
| inf bronze/orion-api/ | 1776 | 2473 | 15,394 | backfill_results/ FAULT 1; latest/ FAULT 2; probe/ RETIRE 2 | 17,151 | 17,170 | +19 |
| inf gold/eclipse/ | 132 | 132 | 397 | _meta/ FAULT 1 | 525 | 529 | +4 |
| inf silver/eclipse/ | 132 | 132 | 528 | none | 655 | 660 | +5 |

**(d) collisions.** 34 entries in `collisions[]`: 34 merge, 0 split. The five new entries are the per-date children of one class each (`merge`, overlap 0 measured: each partition writes its own date keys). The round-1 collision entries are carried unchanged. A shared table with a measured overlap above 0 between two classes is not merged or split by a worker: the two eclipse bronze marker groups are FAULT (round-2 rule 1e).

**(e) denominators.** Every re-grid carries `census_objects`, `listed_objects`, `difference`, `children_objects` (equal to `listed_objects`) and `listed_at`. Two inherited re-grids had child rows that did not sum to their listing (bd logs/ by 30, bd gold/timeseries/ by 3): their child counts are re-derived from the same live listings, so the rows now sum to the listing (surprise row ADVI_FIRMBKTS-D1-W12-S9).

## Judgments the ruling does not spell out

- Non-date objects of the five interleaved classes (inf: bronze/eclipse/_history/, _meta/; gold/eclipse/_meta/; orion-api latest/ and backfill_results/) are FAULT children: the ruling re-grids date partitions only.
- bronze/orion-api/probe/ (2 objects) is RETIRE under RB (probe output, no destination).
- bronze/eclipse_qa/ is re-gridded and homed under bronze/** (table eclipse_qa), not retired under RB's QA reading (surprise row ADVI_FIRMBKTS-D1-W12-S6).
- performance_dim_SKIP.json (1,142 objects of 110 bytes in orion-api partitions) is data, not a marker (surprise row ADVI_FIRMBKTS-D1-W12-S7).
- bd gold/timeseries/ root-level JSON objects (11) are one FAULT row at the class prefix, not 11 rows.
- The ten forwardfill _complete/ groups (bd 4, cot 6) are completion markers by name but stay FAULT under rule 1e, because their keys collide with each other and no state family is named (surprise row ADVI_FIRMBKTS-D1-W12-S11).

## Re-grids (census, live, difference)

| bucket | parent | census | live | difference | markers | data | children | listed_at | rule |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| bd | backfill_v2/ | 292 | 292 | +0 | - | - | 2 | 2026-10-11T06:29:53Z | prefix |
| bd | bronze/ | 212 | 215 | +3 | - | - | 3 | 2026-10-11T06:29:53Z | prefix |
| bd | forwardfill_v2/allocations/ | 146 | 148 | +2 | - | - | 2 | 2026-10-11T06:29:53Z | prefix |
| bd | forwardfill_v2/realized/ | 245 | 249 | +4 | - | - | 2 | 2026-10-11T06:29:53Z | prefix |
| bd | forwardfill_v2/transactions/ | 306 | 310 | +4 | - | - | 2 | 2026-10-11T06:29:53Z | prefix |
| bd | forwardfill_v2/unrealized/ | 89 | 91 | +2 | - | - | 2 | 2026-10-11T06:29:53Z | prefix |
| bd | gold/cohorts/ | 2 | 2 | +0 | - | - | 1 | 2026-10-11T06:29:53Z | prefix |
| bd | gold/filters/ | 2 | 2 | +0 | - | - | 1 | 2026-10-11T06:29:53Z | prefix |
| bd | gold/nna/ | 4 | 4 | +0 | - | - | 3 | 2026-10-11T06:29:53Z | prefix |
| bd | gold/snapshots/ | 7 | 7 | +0 | - | - | 6 | 2026-10-11T06:29:53Z | prefix |
| bd | gold/summary/ | 2 | 2 | +0 | - | - | 1 | 2026-10-11T06:29:53Z | prefix |
| bd | gold/timeseries/ | 2,640 | 2,644 | +4 | - | - | 8 | 2026-10-11T06:56:10Z | prefix |
| bd | logs/ | 9,107 | 9,239 | +132 | - | - | 2 | 2026-10-11T06:59:50Z | prefix |
| bd | scripts/ | 154 | 154 | +0 | - | - | 2 | 2026-10-11T06:29:53Z | prefix |
| bd | silver/transactions_enriched/ | 519 | 519 | +0 | - | - | 2 | 2026-10-11T06:29:53Z | prefix |
| cot | forwardfill_v2/account_attributes/ | 82 | 84 | +2 | - | - | 2 | 2026-10-11T06:30:42Z | prefix |
| cot | forwardfill_v2/allocations/ | 199 | 201 | +2 | - | - | 2 | 2026-10-11T06:30:42Z | prefix |
| cot | forwardfill_v2/holdings/ | 168 | 170 | +2 | - | - | 2 | 2026-10-11T06:30:42Z | prefix |
| cot | forwardfill_v2/realized/ | 204 | 206 | +2 | - | - | 2 | 2026-10-11T06:30:42Z | prefix |
| cot | forwardfill_v2/transactions/ | 207 | 209 | +2 | - | - | 3 | 2026-10-11T06:30:42Z | prefix |
| cot | forwardfill_v2/unrealized/ | 199 | 201 | +2 | - | - | 2 | 2026-10-11T06:30:42Z | prefix |
| cot | silver/ | 803 | 809 | +6 | - | - | 17 | 2026-10-11T06:30:42Z | prefix |
| inf | bronze/eclipse/ | 1,785 | 1,798 | +13 | 134 | 1,664 | 136 | 2026-10-11T06:56:05Z | per-date |
| inf | bronze/eclipse_qa/ | 858 | 871 | +13 | 67 | 804 | 67 | 2026-10-11T06:56:05Z | per-date |
| inf | bronze/orion-api/ | 17,151 | 17,170 | +19 | 1776 | 15,394 | 2476 | 2026-10-11T06:56:06Z | per-date |
| inf | gold/eclipse/ | 525 | 529 | +4 | 132 | 397 | 133 | 2026-10-11T06:56:09Z | per-date |
| inf | gold/timeseries/ | 2 | 2 | +0 | - | - | 2 | 2026-10-11T06:30:24Z | prefix |
| inf | platinum/clients/ | 4,199 | 4,202 | +3 | - | - | 2 | 2026-10-11T06:30:24Z | prefix |
| inf | silver/eclipse/ | 655 | 660 | +5 | 132 | 528 | 132 | 2026-10-11T06:56:09Z | per-date |

## FAULT remaining, grouped by reason, owner 1.0.0_SA_CTO~DELL1

| reason | rows |
|---|---:|
| 1e destination-key overlap with another class's destination (round-2 collision rule) | 40 |
| market-price silver: vendor not derivable from the key and not the feed vendor | 12 |
| no repair rule places it | 7 |
| non-date folder or object of a re-gridded class (no date partition; no rule places it) | 5 |
| silver/bronze root file with no data directory; no rule places it | 4 |
| round-1 rule finds no home for the object shape (RG4, RH3, RH2 as cited) | 3 |
| Lambda deployment artifacts: R16 not applied; home not ruled | 3 |
| leading-slash key (1b places no leading-slash key) | 3 |
| runtime telemetry whose reader is unnamed | 2 |
| completion markers sharing state keys with the other eclipse bronze class (1e; CTO rules split or merge) | 2 |
| code: scripts are not data; no tier holds them | 1 |
| a live credential (FWD-8 class) | 1 |
| root-level JSON objects of gold/timeseries/ (no rule places them) | 1 |

Owners: 1.0.0_SA_CTO~DELL1 (84).

Folder-level FAULT prefixes (file-level rows are counted, not named):

- 46 folder-level rows: bd backfill_v2/; bd bronze/; bd canonical/silver/dim_account/; bd canonical/silver/fact_position/; bd forwardfill_v2/allocations/_complete/; bd forwardfill_v2/realized/_complete/; bd forwardfill_v2/transactions/_complete/; bd forwardfill_v2/unrealized/_complete/; bd gold/advisors/; bd gold/config/; bd gold/consolidated/; bd gold/timeseries/; bd lambda-deploy/; bd lambda-layers/; bd lambda-packages/; bd schwab/silver/rps/; bd scripts/; bd silver/prices/; bd smartx/jwt/; cot forwardfill_v2/account_attributes/_complete/; cot forwardfill_v2/allocations/_complete/; cot forwardfill_v2/holdings/_complete/; cot forwardfill_v2/realized/_complete/; cot forwardfill_v2/transactions/_complete/; cot forwardfill_v2/transactions/_dryrun/; cot forwardfill_v2/unrealized/_complete/; cot gold/positions_cube/; cot gold/timeseries/positions_cube/; cot silver/; cot silver/prices/; inf /advisors/; inf /clients/; inf /firm/; inf bronze/eclipse/; inf bronze/eclipse/_history/; inf bronze/eclipse/_meta/; inf bronze/eclipse_qa/; inf bronze/orion-api/backfill_results/; inf bronze/orion-api/latest/; inf gold/canonical/; inf gold/classification/; inf gold/dimensions/_aor_exercise/aor_attribution_comparison/; inf gold/dimensions/aor_ledger/events/; inf gold/eclipse/_meta/; inf silver/prices/; inf telemetry/inf-gold-layer-runner/history/.
- 38 file-level rows (one object key each, not named here).

## New collision entries

- inf advi inflection/gold/eclipse: gold/eclipse/, verdict merge, overlap 0.
- inf eclipse inflection/bronze/eclipse: bronze/eclipse/, verdict merge, overlap 0.
- inf eclipse inflection/bronze/eclipse_qa: bronze/eclipse_qa/, verdict merge, overlap 0.
- inf eclipse inflection/silver/eclipse: silver/eclipse/, verdict merge, overlap 0.
- inf orion inflection/bronze/orion-api: bronze/orion-api/, verdict merge, overlap 0.

Build: `.scratch/build_v3.py` (not committed). Every address is `lib/opal_naming.py address()` output; the class-grain rows carry the tokens `{partition}` and `{object}`, which are patterns and not keys.
