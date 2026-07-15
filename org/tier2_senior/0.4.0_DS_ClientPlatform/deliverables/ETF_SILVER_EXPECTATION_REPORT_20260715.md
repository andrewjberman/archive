# ETF SILVER FAMILY EXPECTATION REPORT -- PINNED ON FIRST-MONOLITH LANDED BYTES

**Filed:** 0.4.0_DS_ClientPlatform, 2026-07-15 ~18:4xZ. **Status: PINNED** (the build gate for
the etf converter; the part-1/D1 discipline -- this report precedes converter code).
**Basis partition:** the 2026-07-15 FIRST monolith ETF bronze (manual fire, Andrew-direct
"NOW" via COO relay 182117Z; landed 18:28Z; 0.5.0 landing-verified 183304Z).

## 0. Rulings binding this report
- Family design @ e8ecfab0a (CTO PASS-AS-DESIGN 154119Z) + 0.5.0's msn-strike amendment
  (CTO amendment cite 182228Z): the family is **THREE fact tables** -- fact_netassets_page,
  fact_holdings, fact_dailynav. fact_quotes/fact_funds STRUCK (ANDREW-DIRECT ~18:2xZ:
  MSN EXCLUDED, issuer route only). Q3 + msn sparsity law MOOT.
- Q1 (CTO 154119Z): BOTH-STORE -- captured string byte-faithful + standardized f64 alongside;
  **parse MISS = NULL, the ROW SURVIVES** (bronze stays re-derivable).
- Q2 (CTO 154119Z): per-fund silver scope trees + **CONSERVATION AC: sum(per-fund rows) ==
  delivered CSV data rows, denominator read from the file itself, pinned per conversion**
  (holdings AND dailynav).
- Contract (OPAL_ASSETS_V2_LAMBDA_CONTRACT.md): etf = ONE family / one lambda
  (opal-assets-silver-etf), per-vendor typed boundaries RAISING named (cell-1). Rules 6-8
  fill on THESE landed keys (sec 6 below); rule 9 msn -> STRUCK.
- Chunking-arch (@ ffdf766be vintage): ETF is the LIGHT class -- sec-1's tell (materialization
  blowup) is absent at 462KB/253KB/14KB/543B; whole-read; the streaming primitive is not
  needed; sec-6 EC2 branch n/a.
- Rule 17 scope, exactly: dedup = exact-dup over ALL vendor columns; dtype = explicit declared
  map; nothing else. Rule 17a: this family READS bronze, never writes it.

## 1. Landed partition (listing-based: ListObjectsV2 key+ETag+Size, 18:3xZ)
```
"9b70c957eae90ce9ae84ce760e0591b2"  trueshares/DIVZ/bronze/netassets/20260715/divz.html            462,322 B
"cfdb53a2dac62a0acfc928fc090d9e15"  trueshares/IDVZ/bronze/netassets/20260715/idvz.html            252,697 B
"55620e68ee20db7ba77bb612bd31b11e"  pathfinder/filepoint/bronze/holdings/20260715/ETF_Holdings.csv  14,305 B
"b6d8677d0db16cfc386f42d022e7170f"  pathfinder/filepoint/bronze/dailynav/20260715/DailyNAV.csv         543 B
msn/**  : 0 keys (tier never fired -- tiers=[filepoint,trueshares], degraded=[]; 0.5.0 183304Z)
```
Local md5 == ETag all four (single-part, AES256 monolith) -- measurement ran on byte-identical
copies. **ETag volatility law (0.5.0 183304Z): the 22:00Z scheduled fire REWRITES these same
keys -- every pin below is a CONTENT-SCHEMA pin, never an ETag pin.** Denominator of every
measurement below: these 4 objects, whole-read, measured 2026-07-15 18:3xZ by
`measure_etf_bronze.py` (independent; ties 0.5.0's harness at every overlap: 108 rows,
85/23 split, 4/4 captures, headers exact -- two instruments agree).

## 2. fact_netassets_page  (trueshares/{DIVZ,IDVZ}/silver/fact_netassets_page/date=YYYY-MM-DD/data.parquet)
Vendor artifact = raw issuer HTML (utf-8 strict-clean, both funds). The table is the PARSE
PRODUCT of the producer's own patterns (TS_PATTERNS + TS_ASOF_RE + ticker regex, copied
at-vintage from the C4 producer).

**MEASURED (2026-07-15 bytes):** capture census 4/4 BOTH funds.
DIVZ: nav "38.02", market_price "38.06", net_assets "278695788", shares_outstanding "7330000".
IDVZ: nav "34.47", market_price "34.64", net_assets "181982790", shares_outstanding "5280000".
As-of ALL FOUR labels, both funds: "Jul 14, 2026" (T-1 -- trading-calendar-correct, NEVER#1).
Ticker regex -> DIVZ / IDVZ. **UNIT PIN: net_assets raw string is FULL DOLLARS** -- the
`data-format="compact"` attribute is a CSS render hint, NOT a unit statement; no scaling at
silver, ever.

**DECLARED schema (17 parse-product cols + 5 provenance riders = 22):**
- `ticker` string (page-observed; the key scope stays the addressing claim)
- per field F in {nav, market_price, net_assets, shares_outstanding}:
  `{F}_raw` string (byte-faithful capture) + `{F}` float64 (standardized)
- per field: `{F}_as_of_raw` string (e.g. "Jul 14, 2026") + `{F}_as_of` date32
- riders: `_source_file, _source_as_of, _source, _feed, _schema_version`

**Boundary semantics (the HTML branch's typed boundary):**
- regex MISS -> NULL in raw + std, ROW SURVIVES (Q1's ruled AC); capture census printed +
  manifested per conversion (4/4 expected; <4/4 is LOUD, never a refusal).
- captured-but-unparseable (a capture that float()/strptime() rejects, e.g. "38.02.1" --
  structurally possible, `[\d.]+` admits multiple dots) -> **RAISE naming field+value**
  (the mirror numeric-as-text law: refusing to guess; NULLing a *captured* value would be
  silent judgment). MISS=NULL vs CAPTURED-BAD=RAISE is the line, stated here so it is
  reviewable, not discovered.
- Grain: 1 row / fund / run-day => exactly 1 row per partition. Dedup trivially preserved.
- AC-6 parity semantics (no tabular vendor header exists): output_cols == 17 declared + 5
  riders, checked per conversion; the REAL content control is the capture census.

## 3. fact_holdings  (pathfinder/{PFDE,PFOE}/silver/fact_holdings/date=YYYY-MM-DD/data.parquet)
**MEASURED:** header == the 13 declared cols EXACTLY (Date, Account, StockTicker, CUSIP,
SecurityName, Shares, Price, MarketValue, Weightings, NetAssets, SharesOutstanding,
CreationUnits, MoneyMarketFlag). No BOM, CRLF, 108 data rows, 0 ragged, 0 blank-dropped.
Account census {PFDE: 85, PFOE: 23}; **conservation 85+23 == 108 re-derived independently.**
Value forms: Date "07/15/2026" (MM/DD/YYYY, single value file-wide); Weightings carries `%`
("0.00%".."0.26%"...); numerics plain, no thousands-commas ("12251.00000000", "156199693.00");
MoneyMarketFlag census {"": 104, "Y": 4} -- the ONLY column with empty cells; CreationUnits
{"379.000000000000", "559.000000000000"}.

**DECLARED schema (13 vendor cols + 2 additive std + 5 riders = 20):**
- vendor 13, names verbatim; dtypes: `Shares, Price, MarketValue, NetAssets,
  SharesOutstanding, CreationUnits` -> float64 IN PLACE (mechanical parse-or-RAISE, the
  mirror `_numeric_or_raise` law); `Date, Account, StockTicker, CUSIP, SecurityName,
  Weightings, MoneyMarketFlag` -> string byte-faithful.
- additive: `date_std` date32 (from Date, %m/%d/%Y) + `weightings_pct` float64 (Weightings
  with `%` stripped -- both-store because the vendor rendering is non-trivially parsed;
  value stays in percent units: "0.26%" -> 0.26).
- `MoneyMarketFlag` STAYS STRING ("" and "Y" as delivered): ""->False would be null-meaning
  judgment (Rule 17); the legacy `is_cash` bool is gold-tier interpretation.
- riders: the 5.

**Per-fund split (Q2):** on the vendor's own `Account` column; DECLARED fund set
{PFDE, PFOE}; an Account value outside the set RAISES naming it (the split never discards
silently -- a new fund is a reviewed edit to etf_schemas.py). Conservation AC pinned per
conversion in the manifest: rows(PFDE)+rows(PFOE) == file data rows.

## 4. fact_dailynav  (pathfinder/{PFDE,PFOE}/silver/fact_dailynav/date=YYYY-MM-DD/data.parquet)
**MEASURED:** header == the 14 declared cols EXACTLY. No BOM, CRLF, 2 data rows (PFDE, PFOE --
1 row/fund), 0 ragged. Percent columns are BARE DECIMALS (no `%`): "0.6853", "-0.5365",
"0.0437", "0.2512". Rate Date "07/14/2026" -- **trails holdings' Date by one day: the
producer's own documented shape (DailyNAV is NAV-struck post-close), EXPECTED, not a
finding.** Cross-vintage note pinned for gold: holdings(07/15) PFDE NetAssets 156,199,693.00
/ shares 5,590,000 vs dailynav(07/14) 148,934,659.88 / 5,330,000 -- creation-unit activity
between vintages; silver preserves BOTH; adjudication is gold's job (design sec-3).

**DECLARED schema (14 vendor cols + 1 additive std + 5 riders = 20):**
- vendor 14, names verbatim (spaces preserved); dtypes: `Net Assets, Shares Outstanding,
  NAV, NAV Change Dollars, NAV Change Percentage, Market Price, Market Price Change Dollars,
  Market Price Change Percentage, Premium/Discount Percentage, Median 30 Day Spread
  Percentage` -> float64 IN PLACE (bare decimals, measured); `Fund Name, Fund Ticker, CUSIP,
  Rate Date` -> string byte-faithful.
- additive: `rate_date_std` date32 (design table-3's own line, verbatim: "Rate Date stays
  vendor-rendered string + a standardized date col alongside").
- riders: the 5.
**Per-fund split:** on `Fund Ticker`, same declared set, same raise-on-unknown, same
conservation AC (1+1 == 2 on this partition).

## 5. Family-wide converter cells (bound here, exercised in the suite)
- Partition identity = the BRONZE KEY's {YYYYMMDD} (delivery day), never an in-file date --
  in-file vintages are DATA (the mixed-vintage law above).
- Silver key derivation via silver_registry.silver_key; table-name map (design-ruled names):
  trueshares/netassets -> **fact_netassets_page** (not fact_netassets -- the _page suffix is
  the design's own name for the page-parse product), pathfinder/holdings -> fact_holdings,
  pathfinder/dailynav -> fact_dailynav.
- SET-IDENTITY fan: ONE filepoint bronze object -> TWO expected silver partitions
  (PFDE + PFOE); expected_partitions encodes the 1->2 fan. A fund absent from a delivered
  file = a 0-row SHELL partition for that fund (conservation still ties; shell=true in the
  manifest -- the mirror BD-shell precedent), never an unnamed hole.
- Idempotence: skip-if-landed on ALL of a unit's expected keys; force rewrites. **The 22:00Z
  same-key REWRITE means the event path will re-fire on these keys tonight: re-conversion of
  an already-converted partition is the designed idempotent path (skip), and force exists
  for a ruled re-land.**
- Belt-2 classes: 35-byte `grammar.probe` keys pre-exist under these prefixes -> `probe`,
  never converted; `.parquet` under bronze -> `coerced_parquet` (17a class); a stray msn/*
  key post-strike -> named class + FINDING (producer-side strike is 0.5.0's lane).
- Write path: whole-read -> explicit pyarrow schema -> write + read-back verify (the mirror
  write_partition law); manifests run-id-keyed to {source}/{scope}/meta/conversions/;
  sweep = the single backfill-status writer; DLQ drain sweep-only.
- Deploy stays GATED: converters go live after parity 3/3 + the cutover order completes
  (design STATUS line -- nothing here compresses the parity window). Hand-run conversions on
  landed monolith bronze are legal meanwhile (new territory, no consumer).

## 6. Contract rules 6-9 fill (grounded on the landed keys in sec-1)
| rule | prefix | suffix | grounding |
|---|---|---|---|
| 6 | `trueshares/DIVZ/bronze/` | `.html` | landed key sec-1 line 1 |
| 7 | `trueshares/IDVZ/bronze/` | `.html` | landed key sec-1 line 2 |
| 8 | `pathfinder/filepoint/bronze/` | `.csv` | landed keys sec-1 lines 3-4 (ONE rule covers both feeds; feed disambiguation is the key path, converter-side) |
| 9 | `msn/` | **STRUCK** | ANDREW-DIRECT ~18:2xZ (COO relay 182117Z); msn/ carries 0 keys (measured) |

Prediction-vs-landed: the 182428Z pre-fire prediction (from producer source) CONFIRMED
verbatim by 0.5.0 (183304Z) and by my own listing -- two instruments, zero deltas.

## 7. Cross-instrument agreement census (0.5.0 harness vs measure_etf_bronze.py)
holdings rows 108==108; split 85/23==85/23; dailynav rows 2==2 + header exact both; TS
captures 4/4==4/4 both funds; as_of "Jul 14 2026" both; msn 0==0. **Zero disagreements.**
