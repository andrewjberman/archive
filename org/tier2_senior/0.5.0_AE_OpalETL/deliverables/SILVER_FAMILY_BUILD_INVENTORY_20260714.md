# SMARTX + ETF SILVER-FAMILY BUILD INVENTORY (draft, 2026-07-14 ~19:0xZ)
# Purpose: execute-only pickup for the post-verdict critical path (Andrew-direct parity
# objective, CTO relay 185839Z). Rides to CTO with tonight's conversion report.
# GROUNDING: live ListObjectsV2 census 19:0xZ (denominator 16,764 smartx keys — matches
# CTO's number) + silver.py at HEAD 0a5d7e609 + SMARTX_C5_DATA_SHAPE_PLAN_20260714.md §4.
#
# STATUS UPDATE 2026-07-15 ~15:1xZ: THE PLANNED FAMILY (sec A rows 1-5) IS 5/5 LIVE SILVER.
#   fact_allocation_account_map 7,141 rows @ date=2026-07-14 (first V2-8 conversion, 07-14 night)
#   fact_allocation_positions 107,309 rows @ date=2026-07-15 (DS pin-tied to the row, 2 instruments)
#   fact_allocation_valuation    9,540 rows @ date=2026-07-15 (1:1 hard AC exact)
#   fact_model_aum_daily         4,278 rows @ date=2026-07-15 (3 named empty-series-unfunded holes)
#   fact_model_allocation_roster 9,540 rows @ date=2026-07-15 (status split exact; cross-feed tied)
# Contract amended per CTO rulings a1/keep/(c) 145610Z; (c) discriminator live @ 7f76de167.
# Expectation reports: DS part-1 @ 43bbc0385 + part-1b @ 6663a320a (PINNED). Manifests in
# smartx/platform/meta/pulls/20260715/. OPEN: the 7-feed table-or-exemption wave (sec A rows
# 6-12; DS part-2 -> CTO rulings) + the to_frames dedup-semantics ruling (latent, at CTO) +
# ETF family (design filed @ 9efe4ae0e, schemas pin on tonight's landed bytes).

## A. SMARTX — live bronze census vs converter status

| bronze feed (live census) | objs | planned silver table (C5 §4) | converter at HEAD | status |
|---|---|---|---|---|
| allocation/{id}/bronze/holdings (ATOM) | 9,525 | allocation_positions | parse_allocation_holdings + POSITIONS_SCHEMA + to_frames | CODE EXISTS — needs fact_ rename per naming law + real (non-draft) conversion run |
| (same payload, valuation leg) | — | allocation_valuation | VALUATION_SCHEMA + to_frames | same as above |
| model/{rmid}/bronze/allocation_accounts (feed 9) | 7 | allocation_account_map | COMPLETE: fact_allocation_account_map, review-PASSED, first conversion TONIGHT | HEAD of family |
| model/{rmid}/bronze/model_aum | 11 | model_aum_daily | NONE | BUILD |
| model/{rmid}/bronze/model_allocations (feed 5) | 11 | model_allocation_roster | NONE | BUILD |
| account/{uuid}/bronze/allocations (sweep) | 7,066 | NOT IN PLAN | NONE | DESIGN: fact table or ruled exemption |
| account/{uuid}/bronze/detail (enrichment) | 91 | NOT IN PLAN | NONE | DESIGN: identity join input — table or exemption |
| model/{rmid}/bronze/holdings | 11 | NOT IN PLAN | NONE | DESIGN |
| model/{rmid}/bronze/performance | 11 | NOT IN PLAN | NONE | DESIGN |
| model/{rmid}/bronze/changerequests | 11 | NOT IN PLAN | NONE | DESIGN |
| platform/bronze/nonzerosleeve | 1 | NOT IN PLAN (post-plan landing; money-leg + 2nd identity carrier) | NONE | DESIGN |
| platform/bronze/access_roster | 1 | NOT IN PLAN | NONE | DESIGN: likely meta/exemption |
| meta/pulls manifests | 16 | n/a (meta) | n/a | exempt by construction |

PARITY GAP STATEMENT: 5 planned tables cover 3 bronze feed families (atom×2 legs + feed-9 map
+ model_aum + feed-5 roster = 5 tables over 5 feeds). SEVEN live bronze feeds have NO planned
silver shape. Full bronze/silver parity (Andrew's bar) needs each to get a fact_{type} table
OR a recorded exemption ruling. This list = the expectation-report skeleton for DS.

## B. Naming law (cell-6, CTO-settled 111700Z, shape-class rule)
Silver = fact_{type} COMPLETE tables; gold = dim_* projections; gold is the ONE parse-down
point. => planned names: fact_allocation_positions, fact_allocation_valuation,
fact_model_aum_daily, fact_model_allocation_roster, fact_allocation_account_map.
RULED (CTO 231703Z): LEAVE-AND-QUEUE — the 2 pre-naming-law DRAFT silver objects join Andrew's
NEXT deletion batch (2,269-orphan precedent; versioning makes the wait free). DRAFT-SUPERSEDED,
copy-paste-ready for the batch:
```
s3://opal-data-assets/smartx/platform/silver/allocation_positions/date=2026-07-14/data.parquet   # DRAFT-SUPERSEDED (pandas-inferred schema, pre-V2-8, non-fact_ key; ~3.05MB)
s3://opal-data-assets/smartx/platform/silver/allocation_valuation/date=2026-07-14/data.parquet   # DRAFT-SUPERSEDED (pandas-inferred schema, pre-V2-8, non-fact_ key; ~1.13MB)
```
(bronze-never-rewritten does NOT bind silver; key hygiene + the batched-deletion law do.)

## C. Rule-17 constraints already ruled (do not re-litigate)
- Dedup + dtype ONLY; every vendor column preserved (incl. vendor bugs: assetType uniformly
  'equity', industry 'Unknown' — classification is a GOLD join).
- NO basis computation in silver (five internally-consistent AUM bases; Andrew's canonical =
  longEquity+cash GROSS, revisable => basis applies in GOLD only).
- Explicit pyarrow schema per table (no pandas inference); ListObjectsV2 key+ETag+Size
  acceptance (HeadObject never the acceptance instrument).
- Silver lands at platform scope (firm-wide fact tables).

## D. ETF family (contingent on tonight's first bronze)
- Bronze keys per C4 landing map (d69efaad2, PRD v1.3.6): vendor-delivery-scope bronze under
  opal-data-assets/etfs/; msn fallback homed; filepoint CSV = one raw object carrying both
  funds (17a: never split at ingest).
- Silver: currently laptop-side parity artifacts (SILVER_ROOT=_cloudprobe/ quarantine on
  legacy bucket during the 3-day window). Family build = fact_{type} tables fed off monolith
  bronze, event-triggered, AFTER parity 3/3 + cutover order (parity -> SILVER_ROOT="" ->
  verify live write -> disable legacy). Do not compress the parity window.
- Tonight's verdicts determine day-2; family design can start alongside day-3.

## E. Trigger confirmation leg (Andrew's second clause)
"bronze scheduled ingestion triggers and associated silver event-based triggers ... confirmed"
=> for smartx: scheduled = smartx-assets-daily-pull (09:30 ET, live, exercised 13:30Z fire);
silver event triggers = opal-assets-v0.7.0 silver container (events+sweeps+DLQ, live 07-14
~09:5xZ; V2-8 deploy = artifact-swap-only). Confirmation = EXERCISE the path per 22a
(behavioral, not config-read) once converters land.

## F. Build order proposal (for CTO/DS, not self-adjudicated)
1. Tonight: fact_allocation_account_map first conversion (signed, gated behind 22:00Z).
2. First-thing: fact_allocation_positions + fact_allocation_valuation (converters exist;
   naming-law rename + pinned-schema hardening + real run over 9,525-object atom).
3. fact_model_aum_daily + fact_model_allocation_roster (small: 11 objs each, new parsers).
4. DESIGN wave with DS + CTO: the seven unplanned feeds — table-or-exemption ruling each.
5. ETF family per D, respecting the parity window.
6. Trigger-confirmation exercise (E) => report against Andrew's OPAL_RUNNERS gate.
