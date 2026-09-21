# NFRA_MCPINDEX.TO-MX-a-7 -- ETFs (TrueShares, Pathfinder) analysis result

`0.9.0_WK_NFRA_MCPINDEX~3` | cell `MX-a-7` | worktree branch `wk-nfra_mcpindex-1-3c` @ `1310311a9b9b00898073a1d65d9ff748432f03c7`
Measured 2026-09-21, run window ~09:00Z-10:00Z UTC. Instrument: `.tools/aws s3api` (account 313476888478, us-east-1,
READ verbs only, list-objects-v2 auto-paginates by default -- no `--no-paginate` used anywhere below, so every count
below is the TRUE total, never a page count), `py -3.12` + `pyarrow` 18.1.0 (direct parquet reads of the newest live
partition), `git`, `comp-find`/`comp-read`, direct file reads. All S3 evidence is LIVE at run time; all repository
citations print the bytes at the cited line/path (PRD Rule VII.5), at worktree HEAD
`1310311a9b9b00898073a1d65d9ff748432f03c7`.

Read: PRD `org/missions/D9/NFRA/NFRA_MCPINDEX/prd/NFRA_MCPINDEX_PRD.md@b7dc80e2cc` (ENDPOINT FWD-5, CONTRACTS
C1-C8, SURFACE MANIFEST S5); decomposition
`org/missions/D9/NFRA/NFRA_MCPINDEX/decompositions/NFRA_MCPINDEX_DECOMP.md@f506f63a8b` s.3 (`MX-a-7`/`MX-t-7` cells,
S8 acceptance, the `MX-a-7` and `MX-t-7` property-specific additions), s.6 (gates), s.8 (bounds), s.11 (findings);
the prior sibling cells' results `.../0.9.0_WK_NFRA_MCPINDEX~3/analysis-portal.result.md` and
`.../analysis-schwab.result.md` for pattern only, not inherited as fact for this property (the portal analysis
covers the SERVED `platinum/etfs` side of ETFs -- a different layer, MX-a-1's own grant -- this cell is the SILVER
side, per fund). ISSUER CONTEXT (this cell's own worker face) instructs: instance `firm` field is `FABRIC` (ruling
`1.0.0_SA_CTO` @`f1c469829c`, row `NFRA_MCPINDEX-W1-S2`); next row id `NFRA_MCPINDEX-W3-S2`; the research record's
`trueshares/*` and `pathfinder/*` silver leads are treated as leads to independently measure, not inherited as fact.

---

## COMMAND LOG (read verb, AC1/AC3/AC8/AC9/AC11)

All AWS reads below are `s3api list-objects-v2` (auto-paginating; every count below was cross-checked with a
`--query "length(Contents)"` / `sum(...)`/`max_by(...)` read against the same live listing, confirming no 1000-object
page truncation on any of these small prefixes) or `s3api get-object` (parquet byte reads, one partition per table).
No write verb was used anywhere in this cell. Downloaded parquet files sit in `.scratch/parquet/` (worker worktree,
not part of the grant, not committed).

```
.tools/aws s3api list-objects-v2 --bucket opal-data-assets --prefix "trueshares/" --delimiter "/"
.tools/aws s3api list-objects-v2 --bucket opal-data-assets --prefix "pathfinder/" --delimiter "/"
.tools/aws s3api list-objects-v2 --bucket opal-data-assets --prefix "{source}/{fund}/silver/{table}/" --query "[length(Contents), sum(...), max_by(...)]"   (x8: 2 sources x 2 funds x 2 tables)
.tools/aws s3api list-objects-v2 --bucket opal-data-assets --prefix "{source}/{fund}/silver/{table}/" --query "Contents[].Key"   (date-partition census, netassets_page vs dailynav, AC11)
.tools/aws s3api list-objects-v2 --bucket opal-data-assets --prefix "trueshares/DIVZ/bronze/holdings/"                          (AC9's bronze-vs-silver cross-check)
.tools/aws s3api list-objects-v2 --bucket opal-data-assets --prefix "msn/" --delimiter "/"                                       (AC8, the struck-tier census)
.tools/aws s3api get-object --bucket opal-data-assets --key "{source}/{fund}/silver/{table}/date=2026-09-20/data.parquet" <local>  (x6: newest partition per live combo, read via pyarrow)
```

---

## AC1 -- live prefixes, object count, total bytes, newest date, per table

**Denominator: 8** (this property's 2 sources -- TrueShares, Pathfinder -- x 2 funds each x 2 silver tables each:
`trueshares/{DIVZ,IDVZ}/silver/{fact_netassets_page,fact_holdings}`,
`pathfinder/{PFDE,PFOE}/silver/{fact_holdings,fact_dailynav}`). Bucket `opal-data-assets`
(`data/assets/scripts/silver/silver_registry.py:46`, `ASSETS_BUCKET = "opal-data-assets"`, printed; also the
`MONOLITH` default in `data/assets/scripts/silver/etf_conversion.py:69`). Table names are the silver-registry's
own `_fact_table()` output (`fact_{feed}` -- `silver_registry.py:70-81`, printed): `netassets` -> feed name
`netassets_page` (the design's own ruled table name, `etf_schemas.py:63-64`), `holdings` -> `fact_holdings`
(both sources share the feed name), `dailynav` -> `fact_dailynav` (Pathfinder only).

**Top-level, MEASURED** (`s3api list-objects-v2 --prefix "trueshares/" --delimiter "/"`): exactly 2
`CommonPrefixes`, `trueshares/DIVZ/` and `trueshares/IDVZ/` -- matching `etf_schemas.py:56`'s
`TRUESHARES_SCOPES = ("DIVZ", "IDVZ")`. (`--prefix "pathfinder/" --delimiter "/"`): 3 `CommonPrefixes`,
`pathfinder/PFDE/`, `pathfinder/PFOE/` (the two silver fund trees, matching `etf_schemas.py:60`'s
`PATHFINDER_FUNDS = ("PFDE", "PFOE")`) and `pathfinder/filepoint/` (the vendor's BRONZE DELIVERY scope -- one
CSV per delivery, split into the two fund trees at silver, per the Q2 ruling quoted at AC2/AC4 below; excluded
from this property's silver-table set at AC8, it carries no `silver/` subtree of its own).

| source | fund | table | n objects | total bytes | newest object (LastModified) |
|---|---|---|---:|---:|---|
| trueshares | DIVZ | `fact_netassets_page` | 68 | 912,721 | `date=2026-09-20/data.parquet`, 2026-09-20T22:00:15Z |
| trueshares | IDVZ | `fact_netassets_page` | 68 | 912,716 | `date=2026-09-20/data.parquet`, 2026-09-20T22:00:15Z |
| trueshares | DIVZ | `fact_holdings` | **0** | **0** | -- (prefix carries no objects; see AC9) |
| trueshares | IDVZ | `fact_holdings` | **0** | **0** | -- (prefix carries no objects; see AC9) |
| pathfinder | PFDE | `fact_holdings` | 68 | 1,190,115 | `date=2026-09-20/data.parquet`, 2026-09-20T22:00:16Z |
| pathfinder | PFOE | `fact_holdings` | 68 | 915,939 | `date=2026-09-20/data.parquet`, 2026-09-20T22:00:16Z |
| pathfinder | PFDE | `fact_dailynav` | 66 | 839,850 | `date=2026-09-20/data.parquet`, 2026-09-20T22:00:16Z |
| pathfinder | PFOE | `fact_dailynav` | 66 | 839,850 | `date=2026-09-20/data.parquet`, 2026-09-20T22:00:16Z |

**Asymmetry, MEASURED, named rather than smoothed over -- two distinct gaps, different causes:**
1. **`fact_holdings` is EMPTY for BOTH TrueShares funds (0 of 0)** despite `trueshares/{DIVZ,IDVZ}/bronze/holdings/`
   carrying 28 live objects each (2026-08-24 through 2026-09-20, MEASURED) and a registered silver converter
   (`_convert_trueshares_holdings`, `etf_conversion.py:279-347`) that has NEVER RUN against them -- see AC9 and
   surprise row `NFRA_MCPINDEX-W3-S2`.
2. **`fact_dailynav` (Pathfinder) carries 66 dates against `fact_holdings`/`fact_netassets_page`'s 68** -- a
   2-date gap, MEASURED (date-partition set diff): the two missing dates are `2026-08-29` and `2026-08-30`, both
   WEEKEND dates (Saturday/Sunday, confirmed via `datetime.date.fromisoformat(...).strftime('%A')`). The filepoint
   `DailyNAV.csv` feed simply was not delivered those two calendar days, while the TrueShares netassets PAGE (a
   website scrape, not a vendor batch delivery) and the filepoint `ETF_Holdings.csv` feed both landed on every one
   of the 68 dates. Named, not chased further (out of this cell's writes) -- see AC11 for the per-question-class
   disposition this gap drives.

Newest partition for every one of the 6 live table/fund combos is `date=2026-09-20`, at this run's vintage. Read
verb: `s3api list-objects-v2`, printed above; no write verb.

`VERDICT: PASS-MXA7-AC1`

---

## AC2 -- grain, freshness field, latest value per table, source printed

**`fact_netassets_page` (TrueShares, DIVZ/IDVZ).** Grain: ONE row per fund (`ticker`) per partition date -- source
`data/assets/scripts/silver/etf_schemas.py:113-123` (`NETASSETS_PAGE_COLS`, printed): 17 declared columns, no
tabular vendor header (a page-parse product, not a CSV). **Freshness field: FOUR INDEPENDENT `*_as_of` columns**
(`nav_as_of`, `market_price_as_of`, `net_assets_as_of`, `shares_outstanding_as_of`), each captured from the
TrueShares page's own "As of:" label per metric (`etf_schemas.py:90-95`, `TS_ASOF_LABELS`/`TS_ASOF_RE`, printed)
-- there is NO single freshness field like Schwab's `business_date`; every metric carries its own as-of date, which
can in principle differ metric-to-metric (not observed to differ in this run's sample, but the schema does not
guarantee agreement).

**Latest value, MEASURED** (live parquet, `date=2026-09-20` partition, both funds): `nav_as_of` =
`market_price_as_of` = `net_assets_as_of` = `shares_outstanding_as_of` = `2026-09-18` for BOTH DIVZ and IDVZ --
**a 2-DAY LAG between the S3 partition date (2026-09-20, when the page was scraped) and the page's own declared
as-of date (2026-09-18)**, MEASURED and named (the vendor page itself reports data 2 days stale relative to the
scrape date; not chased further, out of this cell's writes). DIVZ: `nav=37.47`, `net_assets=303,124,247`,
`shares_outstanding=8,090,000`. IDVZ: `nav=33.80`, `net_assets=198,735,669`, `shares_outstanding=5,880,000`.

**`fact_holdings` (both sources, per-fund).** Grain: ONE row per (fund, security) per partition date -- source
`etf_schemas.py:127-175` (`HOLDINGS_VENDOR`/`TS_HOLDINGS_VENDOR` + additive dicts, printed): 13 Pathfinder vendor
columns + 2 additive (`date_std`, `weightings_pct`), 10 TrueShares vendor columns + 1 additive (`date_std`),
**declared SEPARATELY per source on purpose** (`etf_schemas.py:150-157`, printed: "the two issuers RENDER
DIFFERENTLY ... Weightings renders BARE ... against filepoint's '0.26%'"). Freshness field: `Date` (vendor string,
`MM/DD/YYYY`) / `date_std` (derived `date32`). **Latest value, MEASURED** (Pathfinder, live parquet,
`date=2026-09-20` partition): `Date` = `"09/21/2026"` for every row of BOTH PFDE (90 rows) and PFOE (24 rows) --
**the vendor's OWN `Date` field is ONE DAY AHEAD of the S3 partition key** (holdings reported as of the day
FOLLOWING delivery), a different asymmetry direction than `fact_netassets_page`'s 2-day-behind lag, MEASURED and
named. TrueShares' own `fact_holdings` freshness field is declared identically in code (`TS_HOLDINGS_ADDITIVE`,
`date_std`) but cannot be confirmed against live data at this run time (AC1: 0 objects).

**`fact_dailynav` (Pathfinder only, PFDE/PFOE).** Grain: ONE row per fund per partition date -- source
`etf_schemas.py:188-206` (`DAILYNAV_VENDOR`/`DAILYNAV_ADDITIVE`, printed): 14 vendor columns + 1 additive
(`rate_date_std`). Freshness field: `Rate Date` (vendor string) / `rate_date_std` (derived `date32`). **Latest
value, MEASURED** (live parquet, `date=2026-09-20`): `Rate Date` = `"09/18/2026"` for both PFDE and PFOE -- the
SAME 2-day-behind lag as `fact_netassets_page` (not the 1-day-ahead lag `fact_holdings` carries), MEASURED.
PFDE: `NAV=28.2903`, `Net Assets=169,458,710.36`. PFOE: `NAV=22.1103`, `Net Assets=86,230,359.18`.

`VERDICT: PASS-MXA7-AC2`

---

## AC3 -- firm/master scope rule per table, key-prefix segment named; tables whose scope cannot be read from the key

**Every table's fund scope IS in its key**, in the SAME position as the source segment shifts: for `trueshares/*`
keys, segment 1 = source (`trueshares`), **segment 2 = fund** (`DIVZ`/`IDVZ`); for `pathfinder/*` silver keys,
segment 1 = source (`pathfinder`), **segment 2 = fund** (`PFDE`/`PFOE`) -- this differs from `pathfinder`'s OWN
BRONZE keys, where segment 2 is the vendor delivery scope `filepoint` (the fan-out to two funds happens only at
silver, per the Q2 ruling, AC2/AC4). Scope rule, MEASURED (this run's live sample key):
`trueshares/DIVZ/silver/fact_netassets_page/date=2026-09-20/data.parquet` -- segment 2 (`DIVZ`) carries the fund
scope, confirmed against `etf_schemas.py:56,60`'s declared `TRUESHARES_SCOPES`/`PATHFINDER_FUNDS` tuples (printed,
AC1). Segment 4 (after `{source}/{fund}/silver/`) is the table name (`fact_netassets_page`, `fact_holdings`,
`fact_dailynav`). So a full key carries BOTH the fund scope and the table identity in its own path, with no
field-level lookup required, for every one of the 8 table/fund combos this cell measured (including the 2 empty
`fact_holdings` combos -- their PREFIX still carries the fund scope even with zero objects under it). This holds
identically for both sources, so this criterion's "table whose scope cannot be read from its key" clause names
**none** for this property (a measured, not an assumed, empty set -- the same finding `MX-a-2` reported for
Schwab).

`VERDICT: PASS-MXA7-AC3`

---

## AC4 -- never-sum rules, each with its reason

1. **Cross-fund.** `etf_schemas.py:56,60` (printed, AC1): `TRUESHARES_SCOPES = ("DIVZ", "IDVZ")`,
   `PATHFINDER_FUNDS = ("PFDE", "PFOE")` -- FOUR distinct SEC-registered ETFs, each its own legal entity with its
   own CUSIP/ticker, NAV, shares outstanding and holdings book. PRD C4: "Masters and firms are never summed
   across, in any phrasing" -- the same discipline applies here to funds, the entitlement-scope equivalent of a
   Schwab master. Reason: summing `net_assets`/`Net Assets`/`shares_outstanding` or holdings `MarketValue` across
   two funds (or across the two SOURCES, TrueShares + Pathfinder) conflates four unrelated funds' balance sheets
   into a number that describes none of them. `etf_positioning_gold.py:11` (printed, portal-side gold producer,
   read as corroboration only): "the four books (DIVZ/IDVZ/PFDE/PFOE)" -- the SAME four-fund framing appears at
   the gold tier this project's `MX-a-1` cell already analysed.
2. **Cross-date (point-in-time, non-additive).** `net_assets`, `nav`, `market_price`, `shares_outstanding`
   (`fact_netassets_page`) and `Net Assets`, `NAV`, `Market Price`, `Shares Outstanding` (`fact_dailynav`) are all
   SNAPSHOT figures carrying their own as-of date (AC2) -- summing a fund's `net_assets` across two dates
   double-counts a STOCK (a balance) as if it were a FLOW, the identical class of error Schwab's `dim_position`/
   `dim_balance` never-sum rule (AC4 #2, `MX-a-2`) names. No engine exists yet to enforce "one date per query" on
   a call path for this property (AC8 -- no read role or typed-query wiring exists today), so this is a
   PRODUCER-SIDE fact (the field's own definition, not yet a call-path guarantee) -- named as such rather than
   overstated as an enforced rule.
3. **Non-additive field (price, percent, ratio).** `nav`, `market_price` (per-share prices), `Weightings`/
   `weightings_pct` (percent-of-fund), `NAV Change Percentage`, `Market Price Change Percentage`,
   `Premium/Discount Percentage` (all percent/ratio fields, `fact_dailynav`) are never additive regardless of
   type -- summing a percent field across holdings or across dates produces a number with no defined meaning
   (the same reasoning class `MX-a-2`'s `datasets.json`-sourced rule used; no equivalent per-table contract file
   exists yet for this property since no `INT/` integration is built, so this rule is reasoned directly from the
   fields' own declared semantics, `etf_schemas.py:178-206`, printed at AC2, rather than read off a config file).
4. **Cross-feed double count (the same fact, measured by two different tables).** A fund's `NetAssets`/`Net
   Assets` figure is carried REDUNDANTLY in THREE places for Pathfinder funds: `fact_holdings`'s own `NetAssets`
   column (repeated on every holding row), `fact_dailynav`'s `Net Assets` column, and (once TrueShares'
   `fact_holdings` backfills) the same pattern for DIVZ/IDVZ against `fact_netassets_page`'s `net_assets`. These
   are THE SAME UNDERLYING QUANTITY measured by different feeds, never independent components of a larger total
   -- adding `fact_holdings`'s `NetAssets` value to `fact_dailynav`'s `Net Assets` value for the same fund/date
   double-counts the whole fund's net assets as if two different funds contributed to it. Reason: unlike Schwab's
   `dim_transaction` (AC4 #4 there, a true row-level aggregation hazard), this is a CROSS-TABLE identity hazard --
   the boundary is "never add two tables' representations of the same scalar fact", not "never aggregate rows
   without a filter".

`VERDICT: PASS-MXA7-AC4`

---

## AC5 -- common questions, numbered, table + fields, source stated

Source discipline: every question below is sourced from (a) the producer/registry code's own declared field set
and grain (`NETASSETS_PAGE_COLS`, `HOLDINGS_VENDOR`/`TS_HOLDINGS_VENDOR`, `DAILYNAV_VENDOR`), (b) the
decomposition's own `MX-t-7` cell title ("ETF tools per fund: holdings, net assets, daily NAV" --
`NFRA_MCPINDEX_DECOMP.md:418`, printed), or (c) this seat's reasoning from the datasets' own field shape. **None
is presented as measured user demand** -- this property has no beta usage yet (C8/S11 have not run, and no
`INT/` integration exists to route a real question through), and this cell does not claim otherwise.

| # | question | table(s) | fields | source |
|---|---|---|---|---|
| 1 | What are fund X's current holdings (securities, shares, market value, weight)? | `fact_holdings` | `StockTicker`/`Stock Ticker`, `CUSIP`, `SecurityName`/`Security Name`, `Shares`, `Price`, `MarketValue`/`Market Value`, `Weightings`/`weightings_pct`, `CreationUnits`, `MoneyMarketFlag` | (a) `HOLDINGS_VENDOR`/`TS_HOLDINGS_VENDOR`, `etf_schemas.py:127-175`; (b) `MX-t-7` names "holdings" |
| 2 | What is fund X's net assets (AUM) as of date Y? | `fact_netassets_page` (DIVZ/IDVZ) / `fact_dailynav` (PFDE/PFOE) | `net_assets`/`net_assets_as_of` / `Net Assets`, `Rate Date` | (a) `etf_schemas.py:113-123`, `:188-206`; (b) `MX-t-7` names "net assets" |
| 3 | What is fund X's NAV and market price as of date Y? | `fact_netassets_page` (DIVZ/IDVZ) / `fact_dailynav` (PFDE/PFOE) | `nav`/`nav_as_of`, `market_price`/`market_price_as_of` / `NAV`, `Market Price`, `Rate Date` | (a) same as #2; (b) `MX-t-7` names "daily NAV" |
| 4 | What is fund X's shares outstanding? | `fact_netassets_page` / `fact_dailynav` / `fact_holdings` (carried redundantly in all three) | `shares_outstanding` / `Shares Outstanding` / `SharesOutstanding` | (c) reasoning from the field shape (AC4 #4's redundancy finding) |
| 5 | How has fund X's NAV / market price changed since the prior business day (dollars, percent)? | `fact_dailynav` ONLY (PFDE/PFOE) | `NAV Change Dollars`, `NAV Change Percentage`, `Market Price Change Dollars`, `Market Price Change Percentage` | (a) `etf_schemas.py:188-206`; **NAMED ABSENT for DIVZ/IDVZ** -- `NETASSETS_PAGE_COLS` (`:113-123`, printed at AC2) carries no day-over-day change column at all |
| 6 | What is fund X's premium/discount to its NAV? | `fact_dailynav` ONLY (PFDE/PFOE) | `Premium/Discount Percentage` | (a) `etf_schemas.py:200`; **NAMED ABSENT for DIVZ/IDVZ** -- no equivalent field in `NETASSETS_PAGE_COLS` |
| 7 | What are fund X's top N holdings by weight? | `fact_holdings` (filtered by fund, sorted) | `StockTicker`/`CUSIP`, `Weightings`/`weightings_pct` | (c) reasoning from the grain (one row per security, weight-bearing field present) |
| 8 | Which fund(s) hold security Y (a cross-fund lookup by CUSIP or ticker)? | `fact_holdings`, across all 4 funds' own silver trees | `CUSIP`/`StockTicker`, fund (from the key's segment 2, AC3) | (c) reasoning, the same question class `MX-a-2`'s AC5 Q4 (Schwab) used |

`VERDICT: PASS-MXA7-AC5`

---

## AC6 -- question -> tool or typed query, with reason

**Assigned to a proposed purpose-built tool (Q1, Q2, Q3, Q4, Q5, Q6):** a single-fund, single-date lookup ("what
does fund X hold", "what is fund X's net assets/NAV", "how did fund X's NAV change") is this property's single
most common shape, and the decomposition's own downstream tool-building cell already frames the property this
way: `MX-t-7` (decomp s.3, printed at AC5) is "ETF tools per fund: holdings, net assets, daily NAV" -- three
named targets, all single-fund/single-date GETs. **Reason:** a fixed single-key GET (fund + date in, that fund's
row(s) for that date out) is cheap and needs no filter/group-by/aggregate generality, the same reasoning
`MX-a-2`'s AC6 used for Schwab's Q1/Q2 (positions/balances) and `MX-a-1`'s AC6 used for the portal's whole-object
reads.

- **Q1 (`fact_holdings`, per fund):** assigned to `pathfinder_get_holdings(fund, date)` for PFDE/PFOE. **NO TOOL
  proposed for the TrueShares side (DIVZ/IDVZ) at this run time** -- `fact_holdings` carries 0 live objects for
  both TrueShares funds (AC1/AC9); shipping a tool against an empty table would always return no data. Once the
  feed backfills (a repair, not this cell's writes -- surprise row `NFRA_MCPINDEX-W3-S2`), the natural name is
  `trueshares_get_holdings(fund, date)`, following the SAME `{system}_{function}` pattern as the two tools this
  cell does propose (AC7); this cell records the gap rather than proposing a tool that cannot answer today.
- **Q2, Q3, Q4, Q5, Q6 (`fact_netassets_page` / `fact_dailynav`):** assigned to `trueshares_get_snapshot(fund,
  date)` (DIVZ/IDVZ) and `pathfinder_get_snapshot(fund, date)` (PFDE/PFOE). **Reason for ONE snapshot tool per
  source, not three:** the underlying data is genuinely ONE ROW per fund per date in a SINGLE table for each
  source (`fact_netassets_page` for TrueShares, `fact_dailynav` for Pathfinder, AC2) -- `MX-t-7`'s title names
  three question CLASSES ("holdings, net assets, daily NAV"), not three physical tables; "net assets" and "daily
  NAV" collapse to the SAME single-key GET for this property, unlike Schwab where positions and balances are
  genuinely separate tables. Q5/Q6 (day-over-day change, premium/discount) are additional COLUMNS on the SAME
  Pathfinder row `pathfinder_get_snapshot` already returns -- no separate tool, and their ABSENCE for TrueShares
  is a field the tool's response simply omits (named at Q5/Q6, AC5), never fabricated.

**Assigned to the typed query (Q7, Q8):** every question that needs a filter, sort or cross-fund scan beyond the
single fund+date key is routed to the typed query rather than a new named tool. **Reason:**
- **Q7 (top-N holdings by weight):** the same `fact_holdings` table `pathfinder_get_holdings`/(future)
  `trueshares_get_holdings` already reads, but sorted/limited -- multiplying tools per sort combination is the
  same anti-pattern `MX-a-1`'s and `MX-a-2`'s AC6 both refused (Schwab Q3/Q4).
- **Q8 (cross-fund CUSIP/ticker lookup):** needs a scan across MULTIPLE funds' own silver trees (four separate
  key prefixes, AC3), which is a filter-driven, cross-scope shape the typed query's structured-object grammar
  (C6) is built for; a single-fund purpose-built tool cannot answer it without becoming a fan-out itself.

No question above is left to the typed query without the reason stated (JUDGMENT AC10 grades whether the
assignment is well-judged; this criterion is mechanical -- that every question HAS a stated assignment).

`VERDICT: PASS-MXA7-AC6`

---

## AC7 -- proposed tool names pass C3

C3 (PRD, printed): `{system}_{function}[_{qualifier}]`; `system` a key of `infra/logic/registry/systems.json`;
`function` a base-form verb; scope (fund) is an explicit ARGUMENT, never folded into the name. `systems.json`
MEASURED (this run, live read): 25 keys; `trueshares` and `pathfinder` are BOTH present, each `"class": "VENDOR"`
(printed verbatim in this cell's own read) -- the SAME system-key shape Schwab's tools use (`"class": "VENDOR"`
there too), and distinct from `"etfs"` (`"class": "PRODUCT"`), the system MX-a-1's portal-level
`etfs_get_positioning` tool already uses for the SERVED/gold layer -- no name collision is possible between the
two layers' tools since they use different system prefixes entirely.

**Proposed tool set (3 new tools, for Q1/Q2-Q6's purpose-built assignment, AC6):**

| tool name | serves | system in systems.json? | function (verb) | collides with an existing tool name? |
|---|---|---|---|---|
| `trueshares_get_snapshot(fund, date)` | Q2, Q3, Q4, Q5(absent-named), Q6(absent-named) | yes (VENDOR) | get | no -- no existing `trueshares_*` tool (comp-find, 0 hits under `INT/`) |
| `pathfinder_get_snapshot(fund, date)` | Q2, Q3, Q4, Q5, Q6 | yes (VENDOR) | get | no -- no existing `pathfinder_*` tool |
| `pathfinder_get_holdings(fund, date)` | Q1 | yes (VENDOR) | get | no |

Both `trueshares` and `pathfinder` are live `systems.json` keys, every proposed name's second segment is `get` (a
base-form verb), fund and date are explicit call ARGUMENTS never folded into the name -- matching `MX-t-7`'s own
acceptance bar ("every tool name passes `MX-n-1`'s validator at registration", decomp s.3, printed). `Q7`/`Q8`
carry NO proposed tool name (AC6) and are typed-query only, and no tool is proposed for TrueShares holdings today
(AC6/AC9), so this cell adds exactly 3 candidate names, all passing C3.

`VERDICT: PASS-MXA7-AC7`

---

## AC8 -- read fence as exact prefixes; exclusions named

**Proposed fence (bucket `opal-data-assets`):** **no existing read role or fence exists for this property today**
-- MEASURED: `comp-find --name '*reader_iam*' infra/aws/terraform/opal-gateway/` returns exactly 1 hit,
`schwab_reader_iam.tf`; no `trueshares_reader_iam.tf`, `pathfinder_reader_iam.tf` or `etfs_reader_iam.tf` exists.
This cell's preflight `comp-iam` summary ("silver only through assumed fenced roles; no firm-bucket grant") is
consistent with this measured absence. DESIRED and APPLIED are therefore BOTH ABSENT (unlike Schwab, which
already has 6 of 8 prefixes granted) -- there is nothing to compare a live IAM read against yet.

- `trueshares/DIVZ/silver/fact_netassets_page/*`, `trueshares/IDVZ/silver/fact_netassets_page/*` -- IN (the 2
  live, populated combos).
- `pathfinder/PFDE/silver/fact_holdings/*`, `pathfinder/PFOE/silver/fact_holdings/*`,
  `pathfinder/PFDE/silver/fact_dailynav/*`, `pathfinder/PFOE/silver/fact_dailynav/*` -- IN (the 4 live,
  populated Pathfinder combos).
- `trueshares/DIVZ/silver/fact_holdings/*`, `trueshares/IDVZ/silver/fact_holdings/*` -- **PROPOSED, though EMPTY
  today** (0 objects, AC1/AC9): `MX-t-7`'s own title names "holdings" as one of the three per-fund question
  classes for THIS property, so the fence is proposed now (the same discipline Schwab's `dim_transaction` fence
  prefix used -- proposed ahead of a tool, per bound 8's read-only-integration scope) so a future `MX-t-7` pass
  does not need a second PRD/fence amendment once the feed backfills; AC6/AC9 make explicit that NO TOOL ships
  against it today.

**EXCLUDED, each with its reason:**
- `trueshares/{DIVZ,IDVZ}/bronze/*`, `pathfinder/filepoint/bronze/*` -- EXCLUDED: bronze is pre-silver raw
  extraction (`silver_registry.py:8-9`, printed: "bronze is RAW and UNTOUCHED. This module NEVER writes under
  bronze/."), the same exclusion class `MX-a-2`'s AC8 used for Schwab's bronze tier.
- `trueshares/{DIVZ,IDVZ}/meta/*`, `pathfinder/{PFDE,PFOE,filepoint}/meta/*` -- EXCLUDED: pipeline bookkeeping
  (`backfill-status.json`, `meta/conversions/`, `meta/pulls/`) -- the same exclusion class `MX-a-1`'s
  `_manifests/` and `MX-a-2`'s `_ops/`; unlike Schwab, no existing role grants a `meta/complete/*`-shaped
  catalog-role prefix here, so nothing under `meta/` is proposed IN.
- `msn/*` (top-level, not fund-scoped) -- EXCLUDED and MEASURED EMPTY at this run time (`s3api list-objects-v2
  --prefix "msn/" --delimiter "/"`, live: zero `Contents`, zero `CommonPrefixes`) -- matching the design's own
  STRUCK-tier declaration (`etf_conversion.py:118-121`, printed: "STRUCK tier ... nothing under msn/ is ever
  converted; its existence post-strike is a producer-lane FINDING"). The live measurement corroborates the code
  comment rather than merely repeating it.
- `_quarantine/*` (top-level, bucket-wide, not fund-scoped) -- EXCLUDED: `silver_registry.py:49`
  (`QUARANTINE_PREFIX = "_quarantine/"`, printed), a loud unreadable-identity bin, "outside every {source}/ tree,
  scanned by nothing that serves" -- not a table of this property.

`VERDICT: PASS-MXA7-AC8`

---

## AC9 -- a property with no data says so and proposes no tool

**At PROPERTY grain**, MX-a-7 has live, non-empty data: 6 of the 8 table/fund combos (AC1) carry live objects
(68/68/68/68/66/66), so the property as a whole is NOT empty and this criterion is not triggered at that grain --
the same vacuous-pass shape `MX-a-2`'s AC9 reported for Schwab.

**At TABLE grain, ONE combo is genuinely empty and is named, not smoothed over:** `trueshares/{DIVZ,IDVZ}/silver/
fact_holdings/` carries **0 objects** at this run time (MEASURED, AC1), despite `trueshares/{DIVZ,IDVZ}/bronze/
holdings/` carrying 28 live bronze objects each since 2026-08-24 (MEASURED) and a registered silver converter for
exactly this feed (`_convert_trueshares_holdings`, `etf_conversion.py:279-347`) existing in code. **NO TOOL is
proposed for TrueShares `fact_holdings`** (AC6, Q1) -- this cell does not ship a purpose-built tool, and does not
route the question to the typed query either, against a table that returns zero rows for every date it would ever
be asked about; the question is instead marked as unanswerable for DIVZ/IDVZ today, with the gap named (AC11) and
a surprise row filed (`NFRA_MCPINDEX-W3-S2`) for the mismatch between this measured absence and the silver
tree's own `backfill-status.json` guard, which reports `"backfill_complete": true` / `"verdict": "PASS"` /
`"holes": []` while never counting this feed at all.

`VERDICT: PASS-MXA7-AC9`

---

## AC10 -- JUDGMENT

Graded by `3.0.0_SA_CVO` at L9. Record UNVERIFIABLE-BY-INSTRUMENT; status_reason: "graded by 3.0.0_SA_CVO at L9,
per this order's own text". No verdict recorded here.

---

## AC11 -- every question class answered per fund; a fund with no data for a date named

**Per-fund disposition, all 4 funds (DIVZ, IDVZ, PFDE, PFOE), against the 8 numbered question classes (AC5):**

| # | question class | DIVZ | IDVZ | PFDE | PFOE |
|---|---|---|---|---|---|
| 1 | holdings | **NO DATA for any date at this run time** (0 of 0 partitions, `fact_holdings` empty, AC1/AC9) | **NO DATA for any date** (same) | answered, 68 dates, newest `2026-09-20` | answered, 68 dates, newest `2026-09-20` |
| 2 | net assets | answered, 68 dates (`fact_netassets_page`), newest `2026-09-20` (as-of `2026-09-18`) | answered, 68 dates, newest `2026-09-20` (as-of `2026-09-18`) | answered, 66 dates (`fact_dailynav`) -- **NO DATA for `2026-08-29`, `2026-08-30`** | same as PFDE -- **NO DATA for `2026-08-29`, `2026-08-30`** |
| 3 | NAV / market price | answered, same 68 dates as #2 | answered, same 68 dates as #2 | answered, same 66 dates as #2 -- **NO DATA for `2026-08-29`, `2026-08-30`** | same as PFDE |
| 4 | shares outstanding | answered (`fact_netassets_page`) | answered | answered (`fact_dailynav`/`fact_holdings`) | answered |
| 5 | day-over-day NAV/price change | **FIELD DOES NOT EXIST for this source** (`NETASSETS_PAGE_COLS` carries no change column, AC5 Q5) | same as DIVZ | answered, 66 dates -- **NO DATA for `2026-08-29`, `2026-08-30`** | same as PFDE |
| 6 | premium/discount to NAV | **FIELD DOES NOT EXIST for this source** (AC5 Q6) | same as DIVZ | answered, 66 dates -- **NO DATA for `2026-08-29`, `2026-08-30`** | same as PFDE |
| 7 | top-N holdings by weight | **NO DATA** (depends on #1) | **NO DATA** (depends on #1) | answered (derived from `fact_holdings`) | answered |
| 8 | cross-fund CUSIP/ticker lookup | contributes NO rows for DIVZ/IDVZ (holdings empty) | (same) | contributes rows | contributes rows |

**The measured gap dates, named exactly as this criterion requires:** `fact_dailynav` (PFDE, PFOE) has no data for
`2026-08-29` and `2026-08-30` (both weekend dates, AC1) -- question classes #2, #3, #5, #6 for PFDE/PFOE are
answered for every OTHER date among the 66-68 measured, and explicitly say "no data" rather than a fabricated
zero for those two dates (C4: "no data for that date is never rendered as zero" -- this cell's own disposition
table follows that rule for its OWN measured facts, ahead of any tool existing to enforce it on a call path).
**TrueShares' holdings question classes (#1, #7, partially #8) have no data for ANY date at this run time** --
the strongest form of "a fund with no data for a date", named per-date-set (0 of 0) rather than glossed as
"in progress".

`VERDICT: PASS-MXA7-AC11`
