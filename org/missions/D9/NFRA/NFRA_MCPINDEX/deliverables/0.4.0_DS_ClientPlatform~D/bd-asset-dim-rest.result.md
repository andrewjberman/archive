# MX-s-9 RESULT -- the Black Diamond asset dimension by REST (49F)

OUTPUT_KEY=s3://opal-data-bd/blackdiamond/49financial/bronze/assets_dim_rest/2026-09-28/assets_dim_rest.parquet

**Seat:** `0.4.0_DS_ClientPlatform~D`  **Order:** NFRA_MCPINDEX MX-s-9 (issued `0c557f19da`)
**Module:** `data/black_diamond/scripts/bronze/pull_bd_asset_dim_rest.py`
**Ledger:** `EGRESS_LEDGER_MX-s-9.md`  **Discovery record:** `discovery_MX-s-9.json`

## 1. The pull

| measure | value |
|---|---|
| rows written | **12,132** |
| `asset_id` unique | **True** (0 nulls) |
| columns | 15 |
| as-of date | **09/25/2026** (Friday -- the last COMPLETED trading day; run fired 01:2x ET Monday, pre-market, so today's positions are not loaded. `prev_trading_day` resolved it; `expected_last_trading_day` returns today because today IS a trading day, which is the frontier question, not the settled-data question) |
| query | qt4 UnrealizedGainLoss (open-lot, holding grain), run 541482 |
| object LastModified | 2026-09-28T05:24:16Z (issuance was 2026-09-28T04:25:12Z) |

Dedup note: the export arrived at 12,132 rows and dedup removed **0**. That is not a missing step --
with dimensions selected and NO facts/measures, BD returns the DISTINCT dimension tuple set, so the
result is already asset-grain. The dedup stays in the module because that property is BD's behaviour,
not a contract, and a future selection that adds a measure would re-expand it to lot grain.

Fill, over a printed denominator of 12,132: `asset_class` 100%, `asset_segment` 100%, `symbol` 100%,
`asset_name` 99.1%, `cusip` 90.2%, `ticker` 70.0%.

## 2. Super-class outcome -- FOUND, not absent

**`asset_super_class` is dim id 7** (`Asset SuperClass`, `mappedColumn=assetSuperClass`, on its own
qt4 level). Measured by scanning **148** qt4 dimensions.

The ruling allowed for `absent` (the column is not in `field_dictionary.md`). It is NOT absent. The
pulled column is **100% non-null over 12,132 rows** and carries exactly the six values
`build_bd_assets_dim.py` already maps in `BD_TO_OPAL` / `COARSE_SUPER_CLASSES`:

| value | rows |
|---|---|
| Equities | 5,840 |
| To Be Classified | 2,930 |
| Fixed Income | 2,543 |
| Unclassified | 600 |
| DIVERSIFIER | 186 |
| Cash & Cash Equivalents | 33 |

Nothing is inferred. Every row carries `asset_super_class_claim=measured`, `source_claim=measured`
and `coverage_claim=held_on_pull_date`.

**The AssetDim template cannot serve this.** The persisted `AssetDimTXNs_OpalCapital_Daily` (id
440247) is queryType **Transactions (qt2)**. That is the measured reason the earlier qt2 read found
no route to `assetClass`/`segment`, and it confirms the ruling's (ii) without relying on it.

## 3. Step 1.1 -- is ALLOCATION already served by REST, as fees is?

**YES. Allocation does not need a REST rebuild; like fees, its downloader is a dead path to report.**

| artifact | evidence | verdict |
|---|---|---|
| fees | `s3://opal-data-bd/bronze/fees/` newest `Fees_OpalCapital_Daily_2026-09-11_to_2026-09-25.xlsx` | CURRENT (the ruling's own finding, re-measured) |
| allocation | `s3://opal-data-bd/silver/allocations/` last write 2026-09-27T00:14:56Z, `comp-freshness` PASS at 29.2h | CURRENT |

The daily bronze completion marker `s3://opal-data-bd/bronze/2026-09-27/_BRONZE_COMPLETE.json` records
`overall: success` with `allocations` as_of **2026-09-25** -- Friday, the T-1 trading-day frontier on a
Monday.

Two honest limits on that verdict:
- I did not take the marker's word for it: the marker is a producer self-report, so the verdict above
  rests on the SERVED artifact's own freshness, measured separately.
- I did not independently exercise the allocation TRANSPORT. The inference that it is REST-served is:
  the portal downloader path fails (row Z-S8), yet the artifact is current, so a non-portal path is
  serving it. That is sound but it is an inference, not an exercised call, and it is named as one.

**A zero worth naming:** `bronze/allocation*` matches **0 of 195** objects under
`s3://opal-data-bd/bronze/`. That zero is NOT absence of allocation data -- the bronze tables land
under `silver/allocations/`, and the `bronze/` prefix holds only fees (131), bi (3) and 61 per-date
completion markers. A census stopped at `bronze/` would have reported allocation missing.

## 4. Coverage -- the union MX-s-6 step 2 must do, with both counts

qt4 carries assets **HELD on the pull date**. An asset fully sold since 2026-04-14 is not on it, so the
dim rebuild unions this pull with the frozen dim, latest-wins per `asset_id`. Measured, not projected:

| set | unique `asset_id` |
|---|---|
| frozen dim `silver/bd_assets_dim.parquet` (2026-04-14) | 10,937 |
| this REST pull (2026-09-25) | 12,132 |
| **union, latest-wins** | **12,141** |
| in BOTH (the pull refreshes) | 10,928 |
| ONLY in the pull (new since the freeze) | 1,204 |
| ONLY in the frozen dim (sold / not held) | 9 |

The headline for MX-s-6 step 2: the union adds only **9** rows over the pull alone, and the pull brings
**1,204** assets the frozen dim never had. The frozen dim is now a 9-row tail, not a co-equal source --
but it is not droppable, because those 9 are real assets with transaction history.

## 5. The scheduling spec (NOT built here -- MX-s-9 builds no schedule)

- **Trigger:** daily, after `bd-49f-auto-login` has refreshed `blackdiamond/49f/session` and before the
  silver dim rebuild. It must be a real schedule, not success-of-upstream as the only trigger.
- **Invocation:** `python data/black_diamond/scripts/bronze/pull_bd_asset_dim_rest.py pull --super-dim-id 7`
  with `--as-of` defaulted to the last COMPLETED trading day via `lib/trading_calendar.prev_trading_day`,
  NOT `expected_last_trading_day` (see s.1) and never a hand-typed date.
- **Freshness entry:** any `comp-freshness` row for this artifact must declare
  `freshness_basis: trading-day-frontier`, or it false-alarms every Monday.
- **Preconditions:** the session mint must return `access_token`; on a stale session the module exits
  loud and does NOT attempt a login.
- **Idempotence:** the key is date-partitioned, so a re-run overwrites its own partition only.
- **Cost:** one bearer mint, one template GET, one run, N status polls, one export per day.

## 6. Departures and defects, stated

1. **Address (rule 30).** The KEY is `lib/opal_naming.py key()` output, never hand-typed. The BUCKET is
   `opal-data-bd`, which `infra/logic/registry/scopes.json` records as a **provisioned, routed bucket
   alias of `opal-data-49financial`** (graded ALIAS). The LGIC tier-home rule R4 would put FIRM bronze
   in the shared `opal-data-assets`; `address()` returns exactly that. I did not take it: the order and
   AC2 both name `opal-data-bd`, and that is where this firm's live bronze/silver plane sits. Rule 30's
   non-application covers it (existing pipelines reach conformance through their own migration, R19,
   never as a rider). Recorded as a departure rather than taken silently.

   The module does not hand-keep ANY of those names. Scope, vendor, firm short-code, session secret and
   routed bucket are all read from the registry at import (`lookup("49financial")`, then the scope row's
   `pipeline_trees[].vendor`, `short`, and the routed `bucket` alias). Positive control: the derived
   values reproduce exactly the four the live pull used. The naming gate refused 16 strings on the first
   version of this module and now grades **WARN 1** -- a `RAISE-EXISTING` on a `s3://%s/%s` format string
   the gate itself says "mints nothing" because it is already carried at HEAD in `.tools/estate-capture.py`.
2. **The order's two-call bound was exceeded by one** -- three vendor operations, not two, from a
   response-shape defect in my own parser. Ledgered in full rather than netted out.
3. **A citation in the order is mis-pinned** (the Andrew quote belongs to the ~20:1xZ refinement, not
   `@785fc4d71f`). Genuine quote, wrong pin; substance unaffected. Detail in the ledger.
4. **Schema wart, found and fixed before hand-off:** the first landed object carried BD's raw
   `Asset SuperClass` column beside a copy -- two columns, one fact, which lets a consumer join on the
   wrong one. The module now renames rather than copies. The served object was rewritten from the local
   copy (no extra vendor call) after asserting the two columns were identical; it now has 15 columns.
5. **The super-class column is named `asset_super_class`, the VENDOR's name -- not `asset_super_class_bd`.**
   Bronze does not pre-empt silver's schema: `build_bd_assets_dim.py` already renames
   `asset_super_class` -> `asset_super_class_bd` in its own dedup step, and its current input
   (`silver/bd_assets.parquet`) carries the vendor name too. So this object matches the convention the
   consuming builder already expects, and MX-s-6 step 2 needs no rename shim.

## 7. What this order did NOT do

49F only; cot untouched. Served gold untouched. The dim rebuild is **MX-s-6 step 2**, not this order --
this writes bronze and stops. No schedule built. No alert, monitor or freshness-checker built. No push.
