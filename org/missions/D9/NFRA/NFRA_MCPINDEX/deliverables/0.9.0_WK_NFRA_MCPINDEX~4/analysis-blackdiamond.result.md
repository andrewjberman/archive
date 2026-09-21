# NFRA_MCPINDEX.TO-MX-a-3 -- Black Diamond property analysis

Worker: `0.9.0_WK_NFRA_MCPINDEX~4`. Cell `MX-a-3` (S8, FWD-4). Read verb throughout: boto3
`s3:ListObjectsV2` (paginated), `s3:GetObject`, `s3:HeadObject` via `.tools/aws` shim identity
(account 313476888478, us-east-1) and direct boto3 in the probe (same credentials, READ-only calls
only -- no PutObject/DeleteObject issued anywhere in this cell). Full run log with per-criterion
denominators: `probes/mx_a_3.py` output, reproduced verbatim in the WORKER REPORT. This file is the
narrative; the probe is the executable evidence.

## Read scope

Bucket under analysis: `opal-data-bd` (LIVE, DESIRED-plane bucket the property's own scripts write --
`data/black_diamond/scripts/silver/merge-daily-incremental.py:53`, `S3_BUCKET = os.environ.get(
'BD_S3_BUCKET', 'opal-data-bd')`, env override not exercised in this cell). Read at
2026-09-21T05:2x-05:34Z (multiple live reads across the AC1-AC9 probe runs; each run's own UTC
timestamp is printed in its VERDICT block).

## AC1 -- live silver prefixes, count/bytes/newest partition

Nine canonical tables identified (below), plus a live EXCLUDED set (28 named non-canon entries under
`silver/`, 2,591 objects / 1,483,511,857 bytes) and the bucket's non-`silver/` top-level prefixes
(also excluded, named). Denominator: 8,022 objects live under `s3://opal-data-bd/silver/` at run
time (`ListObjectsV2`, paginated). See `probes/mx_a_3.py` AC1 output for the per-table
object-count/byte/newest-partition-date table.

## AC2 -- grain, freshness field, latest value (per table, sourced)

| table | grain source | freshness field | latest value (live) |
|---|---|---|---|
| transactions | merge-daily-incremental.py:403-522 | trade_date / partition filename date | 2026-09-20 |
| allocations | merge-daily-incremental.py:767-865 | as_of_date / partition filename date | 2026-09-18 |
| realized | merge-daily-incremental.py:962-1040 | trade_date / partition filename date | 2026-09-20 |
| unrealized | merge-daily-incremental.py:1133-1218 | partition filename date (as_of_date) | 2026-09-18 |
| fees | convert_fees_to_silver.py:1-80 | trade_date / partition filename date | 2026-09-17 |
| bd_assets_dim | build_bd_assets_dim.py:1-53,85-120 | built_at column / S3 LastModified | 2026-04-14 (STALE, ~5 months) |
| canonical_prices | bd_price_update.py (invoke_price_update docstring, merge-daily-incremental.py:675-708) | date column (max) | 2026-09-21 |
| historical_prices | fetch_historical_prices_yfinance.py | date column (max) | 2026-09-18 |
| interpolated_prices | build_interpolated_prices.py | date column (max) | 2026-09-18 |

**Finding (freshness):** `bd_assets_dim.parquet` -- the asset_id->cusip/classification bridge every
transaction/realized/unrealized row is enriched against at ingestion (`enrich_with_cusip()`,
merge-daily-incremental.py:292-334) -- was last built 2026-04-14 and is not rebuilt on any cadence
this cell found referenced in the silver scripts (no scheduler/Lambda trigger for
`build_bd_assets_dim.py` was located; `bd-daily-trigger` per README.md:322-338 only starts the BD
export/silver-merge/gold pipeline, not this dimension build). New assets landing after 2026-04-14 get
a null cusip join. DECLARED risk (from the code's own comment, not exercised): none observed broken,
just unrefreshed.

## AC3 -- firm/master scope rule

Read live from `infra/logic/registry/scopes.json`: firm `49financial`'s `pipeline_trees` names
`data/black_diamond/` as vendor `blackdiamond`, `separated_from: ["cottonwood"]`. Cottonwood carries
its OWN, separate Black-Diamond-flavored tree at `data/cot/` (`separated_from: ["49financial",
"inflection"]`) -- a different tree, a different firm's data, out of this cell's scope entirely.

**None of the nine live keys carry a firm-prefix segment** (the bucket `opal-data-bd` is not even
`scopes.json`'s registered canonical bucket for 49financial, which is `opal-data-49financial` --
see AC8). So every table in this property is the "scope cannot be read from its key" case named
in the criterion; the true scope (firm `49financial`, single tenant of this pipeline tree) is
recoverable only from the registry, never from the S3 key shape.

## AC4 -- never-sum rules (7, each with a cross-master/cross-firm/cross-date/non-additive reason)

See `probes/mx_a_3.py` AC4 output for the full text. Summary: (1) AUA never derived from summed
flows (non-additive/wrong-basis, README.md:10-27's own explicit warning); (2) snapshot fields never
summed across `as_of_date` (cross-date); (3) realized and unrealized never combined unlabeled
(non-additive, different basis); (4) transaction `market_value` never summed across daily partitions
without transaction_id dedup (cross-date, BD re-sends ids); (5) price fields never summed across
assets (non-additive); (6) Black Diamond (49financial) never summed with Cottonwood's separate BD
tree (cross-firm, scopes.json `separated_from`); (7) fee fields never summed across billing periods
without checking for overlap (cross-date).

## AC5/AC6 -- common questions (10), table/fields/source, and their tool-or-typed-query assignment

See `probes/mx_a_3.py` AC5/AC6 output for the full numbered list. Sources used: producer code (6),
portal page (README.md's documented `opal-data-portal-v2/json/advisor-intelligence/*` pages, 2 of the
10 also cite this), prior art (the README's own NNA Classification System section, 1), and reasoning
(2, including the meta freshness question). **None is presented as measured user demand** -- no
query log or usage telemetry exists for this pre-launch tool set, and the probe's own source lines
say so explicitly.

9 of 10 questions are assigned to the **typed query** (C6): each is a single-table filter, group-by,
point-lookup or aggregate with no cross-row state. **1 of 10** (NNA category breakdown) is assigned
to a **proposed tool**, `blackdiamond_classify_nna`, because the classification (NMNC / NMEC_NA /
NMEC_SA / OUTFLOW, README.md:384-412) needs per-client SEQUENTIAL state across the full transaction
history in chronological order -- a state machine C6's filters/group-bys/aggregates cannot express --
and the live `silver/transactions/` schema carries no `is_nna*`/`nna_category` columns (measured: 74
live columns, none named `is_nna*`); those fields exist only in the STALE, excluded
`bd_nna_daily.parquet` (last modified 2026-01-20).

## AC7 -- tool name validation against C3

`blackdiamond_classify_nna`: system token `blackdiamond` is a live key in
`infra/logic/registry/systems.json` (25 keys, VENDOR class); function token `classify` is a
base-form verb; the scope (`49financial`) is NOT folded into the name and is proposed as an explicit
call argument. Passes C3 as read (the validator does not exist yet per C3's own text; NAMING_SCHEMA
v1.12 does not grade MCP tool names, confirmed at the decomposition's falsifier 6).

## AC8 -- proposed read fence

Exact prefixes (9), all under `s3://opal-data-bd/silver/`:
`transactions/`, `allocations/`, `realized/`, `unrealized/`, `fees/`, `bd_assets_dim.parquet`,
`prices/canonical_prices.parquet`, `historical_prices.parquet`, `interpolated_prices.parquet`.

28 named exclusions within `silver/` (legacy monoliths frozen since Jan/Feb 2026, explicit backups,
control-plane manifests/sidecars, and the `silver/prices/{date}.parquet` gold-trigger artifact whose
rows are already upserted into `canonical_prices.parquet`) plus every non-`silver/` top-level prefix
in the bucket (see probe output for the full named list).

**Finding, not a fence line:** the Rule 30 builder resolves this property's canonical LGIC address to
`s3://opal-data-assets/blackdiamond/49financial/silver/<table>/date=...` -- a different bucket and key
shape than the live data. That address is UNOCCUPIED today; Black Diamond has not migrated to LGIC
canon (an R19 migration gap, not this analysis cell's to fix per Rule 30's own non-application
clause). The read fence above targets the LIVE location, per bound #13 (measure deployment facts,
never presume).

## AC9 -- data-presence antecedent

Black Diamond HAS live silver data (8,022 objects, 2,847,180,993 bytes under `silver/` at run time).
The criterion's antecedent ("no silver or served data") is false for this property, so its "says so,
proposes no tool" branch does not bind; 10 questions and 1 tool are proposed against real, live tables
instead, which is the correct behavior when data exists.

## AC10 (judgment, no probe, no verdict from this worker)

The 10-question list targets what a 49 Financial-facing Opal staff member (advisor/ops/compliance)
would plausibly ask about this book: AUA, flows, NNA, gains (realized/unrealized), pricing, advisor
attribution, fees, asset classification, and the property's own freshness. Each of the 9
typed-query assignments carries a stated reason (single-table, additive, no cross-row state); the
one tool assignment carries a stated reason (stateful classification, no queryable columns for it in
silver). No question is left unassigned or unreasoned. Left to `3.0.0_SA_CVO` at L9 per the order's
own instruction.

## Surprise filed

One row filed to the project's investigation channel: `opal-data-bd` (this property's live bucket)
also hosts substantial live data for two OTHER MX-a-k properties in this same project -- `schwab/`
(4,622 objects, ~12.1GB) and `smartx/` (2,967 objects, ~64.7MB) -- plus a `platinum/` served-tier
prefix (24,906 objects, ~5.5GB) and a `canonical/` tier (486 objects, ~1.98GB). Neither the PRD nor
the decomposition's S8 per-property notes name this shared-bucket fact, which is relevant to C7
isolation planning for `MX-a-2`/`MX-a-6`/`MX-i-1`..`MX-i-3`. This cell's own read fence (AC8) already
excludes all of it by name; filed for the cells that touch Schwab/SmartX and the grant-model
generator to have on record.
