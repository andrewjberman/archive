# Design-Scope Brief: 49F Tax SMA Black Diamond Table (tax-pt2)

**For:** 1.0.0_SA_CTO (to stand up a dedicated project) · **From:** 0.2.0_DT_PortfolioAnalytics
**Date:** 2026-07-17 · **archetype:** SCRIBE (scoping)
**Companion doc (the IAM/entitlement half):** `deliverables/TAXSMA_PT2_SCOPED_TABLE_IAM_ASSESSMENT_20260717.md`
**Grounded on:** Manav's manual BD run (HAR `bd3.bdreporting.com`), the 2026-07-16 Yang call, Andrew-direct
design notes 2026-07-17, and the OPAL_CONSOLIDATION Taxonomy Standard @cc1cd96dd.

---

## 1. Objective

A dedicated Black Diamond ingestion (bronze) + a **per-account, denormalized, anonymized silver parquet
table** in `s3://opal-data-assets`, keyed off **account number**, carrying everything the Tax SMA quarterly
report needs. Alyssa runs a `/tax-pt2` skill that goes **over the MCP gateway** to that one table, keys off
an account number, and gets all report data for that account in a **single lookup with NO joins**.

**Settled by Andrew (not open):**
- **Source = Black Diamond, pulled directly** (BD is the defensive net-of-fees authority). *NOT* Schwab-derive.
  (Note for the record: Schwab HAS this data too; BD is the defensive choice, Schwab-derive is a parked
  secondary — see `memory/project_taxsma_schwab_has_fee_data_bd_is_defensive_not_necessary.md`. Do not
  re-litigate "Schwab can't provide it.")
- **Pattern = the Cottonwood BD bronze-ingestion pattern, scoped for the 49 Financial property** -- same
  resources, 49F-scoped: BD session cookie -> REST endpoint pull -> bronze -> silver-merge.
- **No backfill, no chunking lambda.** Forward-only; per-account pulls are small (the chunking strategy in
  `data/assets/docs/SCHWAB_AUTO_PULL_DESIGN.md` / BD datamining sweeps is NOT needed here).

## 2. Field spec + endpoint map (from the HAR -- Chiles Q2 04-08..06-30, reconciles to the cent)

BD account bridge in the HAR: BD `accountId 22596361` / `externalId z0822596361` -> Schwab `27265115`
(masked `XXXX5115`). **Alyssa keys off the Schwab account number**, so the table must bridge BD->Schwab
(the existing `blackdiamond/49f/silver/dim_account_xref` does exactly this -- a dependency, not new work).

| Report class (Yang) | BD REST endpoint | Fields to carry |
|---|---|---|
| Performance, net of all fees | `portfolioreporting/api/performance/performancePeriod` | per window: beginningMarketValue, endingMarketValue, netGains, netAdditions, **fees**, income, timeWeightedReturns.return (TWR), moneyWeightedReturns.return (MWR), benchmarks[].return/difference |
| Cap gains (tax) | `portfolioreporting/api/costBasis` | realizedShortTerm(Gain/Loss), realizedLongTerm(Gain/Loss), unrealizedShortTerm(Gain/Loss), unrealizedLongTerm(Gain/Loss), realizedTotal, unrealizedTotal, marketValue, accrual, cost basis |
| Positioning (top-10 holdings) | `portfolioreporting/api/allocation` (+ holdings levels) | ticker/cusip, weight, marketValue -- top 10 by portfolio weight |
| Sectors | `portfolioreporting/api/allocation` | sector -> weight |

**Period windows** the report needs (per Yang): the reporting quarter (e.g. Q2 = 04-08..06-30), QTD, YTD,
1Y, 3Y, Since-Inception. The `performancePeriod` response already returns a `dateRangePoints[]` array of
windows in one call -- so one pull per account yields all windows.
**Identity/dim fields:** schwab_account_number (key), client name is **DROPPED** (anonymization), strategy,
trade-start date (INPUT, never BD funding-inception -- BD anchors SI at funding; e.g. Chiles funded 03-16,
first trade 04-08), reporting_quarter, benchmark id(s).

## 3. Pipeline architecture (conforming to the monolith grammar + taxonomy standard)

Monolith grammar (law): `s3://opal-data-assets/{source}/{scope}/{layer}/{type|feed}/{date}`,
`{source}=blackdiamond`, `{scope}=49f`.

1. **BRONZE (raw, byte-for-byte per Rule 17a):** the BD REST responses, one prefix per endpoint/feed:
   `blackdiamond/49f/bronze/reporting_performance/{date}/`, `.../reporting_costbasis/{date}/`,
   `.../reporting_allocation/{date}/`. Raw JSON as delivered (names included -- bronze is untouched).
   Producer: a 49F-scoped clone of the Cottonwood REST-consume pattern
   (`data/cot/scripts/bronze/cot_bronze_ingest.py` is the template; it already reads
   `blackdiamond/49f/session` + drives the REST chain), extended to hit the `portfolioreporting/api/*`
   endpoints above. Reuse the live 49F session/auth resources (`bd-49f-auto-login`,
   the `.bd.identity` cookie in `blackdiamond/49f/session`) -- do NOT stand up a second login box.
2. **SILVER (`fact_{type}` complete table, Rule 17 = dedup + dtype ONLY):** the standardized parse of the
   reporting responses, one row per (schwab_account, period-window): `blackdiamond/49f/silver/fact_taxsma_report/`
   (name TBD-by-taxonomy). Complete = every field pulled; NO slimming here.
3. **SERVE PROJECTION (the anonymized, few-fields table Alyssa reads):** the parse-down -- drop names,
   keep only the report fields, denormalize per account. **Taxonomy note (flag for your ruling):** the
   standard says *gold is the ONE parse-down point; gold `dim_*` = projections*. So the "very few fields /
   very anonymized" table is taxonomically a **gold `dim_taxsma_report`**, even though the design note
   called it "silver parquet." Recommend: serve projection = `blackdiamond/49f/gold/dim_taxsma_report/`
   (or a dedicated serve prefix), and the **scoped IAM points at exactly that one prefix**. If you rule the
   single anonymization-drop acceptable in silver, a silver-only shortcut collapses (2)+(3) -- your call;
   either way it must be **its own isolated prefix** so the per-employee IAM is a single-prefix grant.
4. **Trigger:** bronze-complete sentinel -> EventBridge -> silver-merge, mirroring the cot/bd49f chain.
   Cadence: refresh on the same daily rhythm as the existing 49F pull (cheap; keeps the table current so
   Alyssa's quarter-end run reads fresh data). Scheduler named per standard `{unit}-{function}-{cadence}`.

## 4. Consumption contract (the MCP read path)

- Alyssa's `/tax-pt2 {account}` skill -> MCP gateway -> reads the serve projection at its one prefix,
  keyed by schwab account number -> returns the account's full report record. No joins, no other bucket.
- The gateway reaches S3 by **assuming Alyssa's per-employee scoped IAM role** (see companion assessment):
  gateway AWS-surface entitlements file = `email -> scoped-IAM-role-ARN`; Alyssa's role = read-only on
  **only** the serve-projection prefix. This is the "AWS-specific entitlement layer" -- net-new; the gateway
  currently has ZERO opal-data-assets reach.

## 5. Explicitly OUT of scope

- No backfill; no chunking lambda; no historical reload (forward-only).
- No Schwab-derive path (parked secondary).
- No second BD login box (reuse 49F session).
- No client PII in the serve projection (anonymized; account-number key only).
- Cottonwood/`cot` firm data is untouched -- we replicate the PATTERN, never mirror the firm (bd<->cot
  separation gate + IAM stands).

## 6. Open decisions for the project

1. **Serve-layer naming/placement** (silver `fact_` vs gold `dim_` for the parse-down) -- section 3.3;
   my rec is gold `dim_taxsma_report`, isolated prefix, per the taxonomy standard.
2. **Endpoint mechanism** -- the HAR shows the `portfolioreporting/api/*` REST endpoints (browser/clientview
   session). Confirm these are pullable with the `.bd.identity` datamining session, or whether a
   clientview-session variant is needed (the cot pattern's REST chain is the reference to verify against).
3. **Account universe + roster** -- 3 live accounts now (Chiles 0027265115, Bump 0035940058, Macy
   0091939812), grows fast; the roster feed (`template_roster`) + `dim_account_xref` drive account
   discovery + the BD->Schwab bridge.
4. **Period-window set** to freeze (Q/QTD/YTD/1Y/3Y/SI) + trade-start-date input source (Yang's xlsx).

## 7. Definition of done

Bronze lands the raw BD reporting responses for all live 49F accounts daily; silver `fact_` carries the
complete standardized parse; the serve projection is a per-account, anonymized, few-field, account-number-keyed
table on its own isolated prefix; Alyssa's per-employee scoped IAM reads only that prefix through the MCP
gateway; `/tax-pt2 {account}` returns the full report record in one lookup; reconciles to the HAR targets
(Chiles Q2: BMV 1,061,234.71 / EMV 978,575.04 / netGains -87,061.19 / TWR -8.2053% / realizedShortTerm
-61,933.73 / unrealizedTotal 822,189.90).
