# ETF SILVER FAMILY DESIGN (draft alongside day-3, 2026-07-15 ~15:0xZ)

**Filed by:** 0.5.0_AE_OpalETL. **Rides to:** CTO (family-review form) + DS (converter authoring
owner per their 07-15 board: "ETF first monolith bronze -> contract rules 6-9 + V2-5 etf rows +
converter authoring"). **Per:** SILVER_FAMILY_BUILD_INVENTORY_20260714.md section D (fa678b742) --
"family design can start alongside day-3."

**STATUS: DESIGN, NOT A BUILD ORDER.** Schemas below are PROPOSED SHAPES grounded on the C4
producer's source; they PIN only after tonight's first monolith bronze is opened and read
(the same landed-bytes discipline every other family followed). Nothing here compresses the
parity window: converters go live AFTER parity 3/3 + the cutover order completes
(parity -> SILVER_ROOT="" -> verify live write -> disable legacy).

**CTO REVIEW 154119Z: PASS-AS-DESIGN.** Section 3 affirmed as the load-bearing line; the msn
sparsity law loudly affirmed (the NEVER#1 false-staleness class at feed granularity --
comp-freshness never points at fact_quotes/fact_funds without a fallback-aware basis). All
open questions closed: Q1/Q2 RULED (CTO), Q3 RULED (DS 153751Z) + affirmed -- see section 6.
Sequencing locked as section 5. **OPAL_CONSOLIDATION note: ratified ~15:31Z (master record
bf8f24728, supersede model); this design's work rides as WS-A3/A4 + W5 there -- ACs unchanged,
COO re-parents the TOs.**

---

## 1. What lands tonight (the C4 landing map, source-grounded @ v1.1.0)

`_bronze_key` (lambda_function.py, three-way sha tie 40KaO/7j..., env verified live 14:2xZ:
BRONZE_BUCKET=opal-data-assets, BRONZE_GRAMMAR=monolith):

```
trueshares/DIVZ/bronze/netassets/{YYYYMMDD}/divz.html      raw issuer HTML, 1/day
trueshares/IDVZ/bronze/netassets/{YYYYMMDD}/idvz.html      raw issuer HTML, 1/day
pathfinder/filepoint/bronze/holdings/{YYYYMMDD}/ETF_Holdings.csv   ONE file, BOTH funds (ruling 15)
pathfinder/filepoint/bronze/dailynav/{YYYYMMDD}/DailyNAV.csv       ONE file, BOTH funds
msn/{TICKER}/bronze/netassets/{YYYYMMDD}/{iid}.{quotes|funds}.json tier-3 FALLBACK -- absence normal
```

Vendor delivery scopes are the bronze scopes (PRD v1.3.3 ruling 15): the Filepoint CSVs land WHOLE
under scope `filepoint`; per-fund partitioning happens at silver, where the parser splits without
discarding (that is the ruling's own text).

## 2. Proposed fact_ tables (naming law cell-6: silver = fact_{type} COMPLETE, vendor-shaped)

| # | table | scope tree | fed by | grain | notes |
|---|---|---|---|---|---|
| 1 | fact_netassets_page | trueshares/{TICKER}/silver/ | netassets html | 1 row / fund / run-day | the 4 TS_PATTERNS fields (nav, market_price, net_assets, shares_outstanding) + as_of, RAW-parsed values as strings-or-f64 (pin on landed bytes); a parse MISS lands NULL, never a dropped row -- the bronze HTML stays re-derivable |
| 2 | fact_holdings | pathfinder/{FUND}/silver/ | filepoint holdings csv | 1 row / holding / fund / run-day | ALL 13 vendor header cols preserved (Date, Account, StockTicker, CUSIP, SecurityName, Shares, Price, MarketValue, Weightings, NetAssets, SharesOutstanding, CreationUnits, MoneyMarketFlag); split per fund AT SILVER per ruling 15 |
| 3 | fact_dailynav | pathfinder/{FUND}/silver/ | filepoint dailynav csv | 1 row / fund / run-day | ALL 14 vendor header cols preserved; Rate Date stays vendor-rendered string + a standardized date col alongside (additive, Rule 17) |
| 4 | fact_quotes | msn/{TICKER}/silver/ | msn quotes json | 1 row / fund / run-day | SPARSE by design (tier-3 fallback): a missing partition is the NORMAL case, never a freshness alarm -- comp-freshness must NOT be pointed at this table without a fallback-aware basis |
| 5 | fact_funds | msn/{TICKER}/silver/ | msn funds json | 1 row / fund / run-day | same sparsity law as fact_quotes |

**Key grammar:** `{source}/{scope}/silver/{fact_table}/date=YYYY-MM-DD/data.parquet` (the
established mirror shape; smartx/schwab precedent).

## 3. THE GOLD/SILVER SPLIT -- what does NOT come to silver (the design's load-bearing line)

The legacy pipeline's "silver" rows carry `source` (tier winner), `staleness_days`, `inferred`,
carry-forward fill (MAX_CARRYFORWARD_DAYS=1), and the consolidated `netassets_daily.parquet`
cross-vendor series. **Every one of those is tier-adjudication / fill / derived business logic =
GOLD under Rule 17.** The monolith silver families above are per-vendor, judgment-free. The tiered
consolidated series (today's netassets_daily) becomes a GOLD projection (dim_ or gold fact per the
gold naming law) built FROM tables 1-5. This is the same one-parse-down-point law the smartx basis
decision followed (basis in gold = a one-line revision; baked into silver = a re-ingest).

## 4. Trigger wiring (second half of Andrew's parity directive)

Converters register in DS's silver container registry (opal-assets-v0.7.0, events+sweeps+DLQ --
`silver_registry.py` already enumerates trueshares/pathfinder as sources). Event-driven on bronze
landings under the three vendor prefixes; the sweep covers event gaps. Confirmation = EXERCISE the
path per 22a once converters land (behavioral, not config-read).

## 5. Sequencing (explicit, so nothing compresses the window)

1. TONIGHT 22:00Z: first monolith bronze lands (C4 AC1) + day-3 parity verdict.
2. Open the landed bronze, pin schemas on REAL bytes -> revise section 2 shapes into pinned
   pyarrow schemas (the smartx model-family form: measured field unions, denominators stated).
3. DS expectation skeleton per table (the part-1 pattern) -> converter authoring (DS tree,
   Rule 13) -> CTO family review -> first conversions.
4. Cutover order for the legacy pipeline runs INDEPENDENTLY on parity evidence; the family build
   never front-runs it.

## 6. Open questions routed (not self-adjudicated)

- (Q1, CTO) fact_netassets_page value dtypes: the TS_PATTERNS regexes capture STRINGS from HTML;
  proposal = store the captured string byte-faithful + a standardized f64 alongside (additive).
  Alternative = f64 only. Rule-17 lean: both.
  **RULED (CTO 154119Z): BOTH-STORE** -- captured string byte-faithful + standardized f64
  alongside (the model_aum epoch+friendly+date32 additive precedent). **NAMED AC: parse MISS =
  NULL in the f64, the ROW SURVIVES** (bronze HTML stays re-derivable; null-not-drop).
- (Q2, CTO) pathfinder per-fund silver scope (`pathfinder/PFDE/silver/...`) vs delivery-scope
  silver (`pathfinder/filepoint/silver/...` with a fund column): ruling 15's text says per-fund
  partitioning happens at silver; proposal = per-fund scope trees (table 2/3 above).
  **RULED (CTO 154119Z): PER-FUND scope trees, with an ADDED CONSERVATION AC** -- the split is
  EXERCISED, never assumed: sum(per-fund rows) == delivered CSV rows, denominators read from
  the file itself, pinned per conversion. Applies to holdings AND dailynav. ("Splits without
  discarding" is ruling 15's text; the per-conversion pin is what makes it true every day.)
- (Q3, DS) whether msn quotes+funds collapse into ONE fact_msn_netassets table (they arrive as a
  pair for the same instrument-day) or stay two tables mirroring the two endpoints; proposal =
  two (feed-shaped, one table per bronze feed -- the established rule).
  **RULED (DS, converter owner, 153751Z, CC CTO): TWO tables -- fact_quotes + fact_funds.**
  Rationale banked: one-table-per-bronze-feed law (orion precedent, verified live); merging two
  endpoints = a cross-endpoint JOIN = gold-tier (sec 3's own line); independent tier-3
  sparsities stay clean (quotes-without-funds = a missing partition, not a half-null row); gold
  pairs them at the one parse-down point. No fact_msn_ prefix (the msn/ scope tree
  disambiguates, same as orion's fact_transactions). GROUNDING HONESTY on the record: zero msn
  payloads exist anywhere pre-fire (monolith msn/ empty, legacy has none -- tier-3 sparse), so
  the quotes-vs-funds schema DIFFERENCE confirms on tonight's landed bytes; the two-table ruling
  holds regardless of payload overlap.
