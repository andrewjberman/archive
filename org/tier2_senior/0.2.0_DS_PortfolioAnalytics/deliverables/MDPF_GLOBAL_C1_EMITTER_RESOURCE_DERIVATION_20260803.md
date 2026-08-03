# MDPF_GLOBAL.C1 — Emitter Legacy-Row Re-Source Derivation + Spec

**Author:** 0.2.0_DS_PortfolioAnalytics · 2026-08-03 ~23:00Z · **TO:** MDPF_GLOBAL.C1 @21ed7ad2d4 (CTO ruling 221736Z: re-source is the default and the presumption)
**Cites @ 440d16e018** (emitter `lambda_function.py` + `channel_sources.py`, deployed 07-28 config per the TO). **Implementer:** 0.7.0_AE_CloudOps (Lambda change + deploy). **Read-only production; scratch derivations only.**

## Verdict up front

**Every legacy row RE-DERIVES. The droppable branch is EMPTY — no droppable ask goes to CTO.** The emitter's entire remaining base-read value dependence reduces to ONE quantity (ETF total net assets per ticker), whose authoritative source the emitter's own package already reads for a sibling row family. Parity: **12/12 exact matches** (3 sample dates × 4 tickers, to the cent, keyed by each partition's own stamped as-of).

## 1. Denominator — the emitter's row universe

| Row family | Builder | Count | Re-source status TODAY |
|---|---|---|---|
| Base cohorts | `build_rows` `:579` | 14 (COHORTS `:69-98`) | **10/14 already overridden** by `apply_channel_resource` `:1272+`: `49f_schwab_custody`, the 7 `_RESOURCE_MODEL_KEYS` model cohorts (`:1217-1224`), `49f_smartx_platform` (5-core), `inflection_models` |
| Appended channel rows | `apply_channel_resource` | 3 (`inflection_orion_custody`, `cottonwood_bd_holdings`, `cottonwood_bd_models`) | already canonical (`channel_sources.py` contracts) |
| Global row | same | 1 (`_global__aua_total`, fee-basis, `legs_present`) | already canonical |
| Totals | `build_total_rows` `:1029` | 2 (`TOTAL_ROW_IDS` `:1025`) | `_total__partner_aua` **already re-sourced** (AC7 regime move: contributors re-summed, partial-sum REFUSAL, `legacy_carried_total` side-field) |
| Ownership rows | `build_ownership_rows` `:754` | per ETF×partner | `held` values ALREADY read `opal-data-etfs` directly (`:764-767`) — runner-independent |

**THE LEGACY NON-RE-SOURCED SET — 3 row families, ONE shared quantity (`etf_total_net_assets` per DIVZ/IDVZ/PFOE/PFDE):**

1. **4 `etf_fund` cohort rows** (`etf_divz/idvz/pfoe/pfde`): value = `body.etf_decomposition[t].etf_total_net_assets`, as_of = `body.source_vintage.by_feeder.etf_net_assets[t]` (`:612-637`).
2. **`ownership_pct` denominators** on ownership rows: `_etf_totals(body)` (`:760`, `:801-804`) — the ONLY body-dependence in that family.
3. **`_total__etf_fund`**: sum over the 4 etf_fund rows (already carries the partial-sum refusal precedent).

Residual body reads: `generated_at` provenance stamps (cosmetic) + the handler's `:1517-1520` `except → body=None` (the DECLARED deep-history channel-rows-only branch).

## 2. Provenance chain + per-row classification

**The chain (source-confirmed):** `s3://opal-data-etfs/silver/netassets_daily.parquet` (ETFS_NETAST consolidated daily series; `net_assets_reported` = the issuer-reported authoritative total; `data_as_of` = issuer valuation date) → WS-D2 feeder (`build_mdpf_wsd2_etf_netassets_feeder.py` docstring: "a near-direct column map", latest row per ticker) → `opal-data-mdpf/mdpf/feeds/etf_net_assets/{date}.parquet` → `mdpf_aggregate_aua.py` → runner partition `etf_decomposition[]`. **The runner leg is a pure two-hop pass-through of one source object.**

| Row | Classification | Evidence |
|---|---|---|
| `etf_fund` ×4 | **RE-DERIVES** — read `netassets_daily.parquet` directly: per ticker, latest row `data_as_of <= accept-window`, value `net_assets_reported`, as_of `data_as_of` | **12/12 EXACT** across partitions 07-29/07-30/07-31 × 4 tickers, keyed by the partition's stamped as_of (e.g. DIVZ 07-31-partition $302,251,812 @07-29 == source row @07-29 to the cent) |
| ownership `held` | already canonical (no change) | `:764-767` reads `opal-data-etfs` daily partner artifacts |
| ownership `pct` | **RE-DERIVES** — same netassets read supplies the denominator (one read, two uses) | arithmetic on the 12/12-proven quantity |
| `_total__etf_fund` | **RE-DERIVES** — sum of the re-sourced 4; keep the existing refusal + mirror the partner_aua AC7 move (`legacy_carried_total` side-field, `contributors`, `legs_present`) | `:1025` + the AC7 precedent block |
| UNKNOWN rows | **NONE** | — |

**Bonus the re-source buys immediately:** the direct source is FRESHER than the dead runner plane today (PFDE/PFOE carry `data_as_of` 2026-08-03; the frozen runner partition serves 07-30-as-of values) — re-sourcing heals the exact staleness the runner's death causes. **(CTO on accepting C1, 232958Z, for the T5 record: "the retirement stops being a cost we absorb and becomes a fix.")**

## 3. The re-source spec (implementable by AE alone)

1. **New `channel_sources.etf_net_assets(run_date, tdb)`**: read `s3://opal-data-etfs/silver/netassets_daily.parquet` (single consolidated object — an object-read, not a partition listing); per ticker: latest row `data_as_of <= run_date` within the roster-declared cadence window (+1 td slip, the WO-4c discipline); emit `{value: net_assets_reported, as_of: data_as_of, derivation, source_field: "<key>[ticker].net_assets_reported@<data_as_of>", provenance: "measured", feed_id, cadence_lag_td, declared_cadence}`; absent/out-of-window → `{absent_reason}` sentinel (labeled absence, `_override` semantics `:1236+`). **Roster rider:** add an `etfs_netassets` feed entry to `partner_roster.json` (the cadence authority) — observed cadence: PFDE/PFOE ~T-0/T-1; DIVZ/IDVZ issuer-lagged 2–4 td (measured in the parity table) — declare per-ticker-family, do NOT demand same-day.
2. **Override the 4 cohorts** in `apply_channel_resource` via `_override(_mapped_row(cid), ...)` exactly like the other channels; `_etf_totals` consumed by ownership pct reads the same derivations (one fetch per invocation).
3. **`_total__etf_fund`** moves to the re-sourced regime mirroring `_total__partner_aua`'s AC7 block (sum own re-sourced additive contributors; `legacy_carried_total` preserved as the supersession delta; the existing partial-sum refusal stays).
4. **After this, ZERO value-bearing base reads remain** — the runner partition read becomes vestigial for the daily path.

## 4. The `:992` silent-aging rider (binding; closes with C1)

`_latest_key() = max(keys)` with no age bound (`:989-993`) — live today: serving the 07-31 partition since the runner died. Spec for the AE implementation:

1. **The daily path derives its run_date from the EVENT** (scheduled-fire date / explicit `run_date`), NEVER from `max(keys)` — a dead producer can then never silently re-serve yesterday's identity. `_latest_key()` survives ONLY for explicit walk/backfill invocations (event-flagged), where "latest" is the asked question.
2. **Post-re-source, `body=None` is the NORMAL daily mode** (no value depends on it): the `:1517-1520` branch becomes the declared mode, not a swallow — rows are wholly `as_of_basis=channel_source_partition_date`.
3. **Transition period only** (if any read remains): a partition whose run_date lags the event date beyond a declared window emits `partition_lag_td` + `status=degraded` IN the invocation result + on the row stamps (per-stage observable per the CANON-PROVEN law, per-stage-rc marker-blind per COO amendment #2). **No alarm/SNS/monitor** — moratorium respected; the state is in-band.

## 5. Folded supplement (COO 22:51:41Z) — the cottonwood s2 question

**s2 is DECLARATION-ONLY in the emitter; no emitted value is disclaimer-derived — and the negative is
now SOUND, not text-local** (the CTO's 225800Z discriminating check answered, case (a)):

- **The token census** (all 7 files): cottonwood `bd_holdings_s2`/`bd_allocations_s2` appear only in
  the vendored `partner_roster.json` declarations (`:291-311`) + two comments (`channel_sources.py:440,:511`).
- **The generic-consumption check** (what a token grep cannot see): roster feed entries ARE consumed
  generically at exactly ONE site — `_feed_by_prefix()` (`channel_sources.py:133-161`) — and it builds
  a `{prefix → cadence-metadata}` LOOKUP MAP performing ZERO reads. The resolution direction everywhere
  is LITERAL-PREFIX → roster-metadata (`accept_date:174` `_feed_by_prefix().get(prefix)`; un-rostered
  prefix refuses loudly `:175-177`) — the roster GATES reads, it never ORIGINATES one.
- **Every read-primitive call site, package-wide, passes a literal constant:** `accept_date`/
  `available_dates`/`_read_partition` at `channel_sources.py:246,:253,:280,:284,:288,:291,:338,:347,
  :381,:397,:406,:446` (SCHWAB_RPS2/SMARTX_AUM/SMARTX_ROSTER/ORION_ASSETS/ECLIPSE_PORTFOLIOS/
  COT_HOLDINGS), `lambda_function.py:1283` (eclipse literal), `:1518,:1563` (the aggregate partition
  key), `walk_daily_aua.py:61-63` (the same four literals). **No call site names an s2 prefix, so the
  s2 rows sit in the lookup map structurally unqueried.**

The roster's mis-declaration is a roster-content defect (0.4.0_DS's finding, routes separately); the
fix should roster `fact_holdings` (the real table `cot_total` already reads), not repair the s2 rows.
Method note banked: the token grep alone was the vintage-is-not-content class one level up — the
consumption-site check is what converts a text-local negative into a sound one.
