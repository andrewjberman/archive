# SMARTX ATOM-LEG PRE-FIRE EXPECTATION REPORT
## fact_allocation_positions + fact_allocation_valuation (run partition 2026-07-15)

**Filed by:** 0.4.0_DS_ClientPlatform, 2026-07-15 ~14:5xZ. **For:** 0.5.0_AE_OpalETL's first hardened
atom conversion run. **Rides to:** CTO family review. **Pattern:** 0.6.2 pre-fire expectation report
(the run is measured against THIS, filed BEFORE it, not against its own output -- a false premise
answered ON returns as corroboration; ask for the artifact, not the number).

### Grounding / provenance (state what each number is OF)
- **Denominator:** live `ListObjectsV2` recursive census of `s3://opal-data-assets/smartx/` @ 2026-07-15
  ~14:4xZ -- 26,382 total smartx keys; the atom slice enumerated below.
- **Schema contract:** `POSITIONS_SCHEMA` / `VALUATION_SCHEMA` @ `infra/aws/lambda/smartx_assets_pull/silver.py:120/134`
  (working tree ~14:5xZ, HEAD d6e748a53; the CTO shape-gate-PASS-073707Z pinned contract -- "expect THOSE").
- **Row rules:** `parse_allocation_holdings` @ `silver.py:72` (one object -> positions rows + exactly 1 valuation row).
- **Payload shape + positions magnitude:** 200-object live `boto3 get_object` sample of the 20260715 holdings
  atom (2.1% coverage; 2,313 sampled positions).

---

### THE ATOM -- one bronze object, two silver row-sets (not two feeds)
- Bronze key grammar: `smartx/allocation/{allocation_id}/bronze/holdings/{YYYYMMDD}/holdings.json` -- ONE
  object per allocation per day.
- `parse_allocation_holdings(object)` -> `(positions_rows, ONE valuation_row)`. The two legs are two
  projections of a single payload in one pass, so they share a coupling invariant (below), and a
  streaming converter fans them off one row-source (the delta-6 fan-out pattern, if/when it grows heavy).

### DENOMINATOR (grounded on the live listing, NOT the fleet manifest)
| partition | live `holdings.json` objects | basis |
|---|---|---|
| 2026-07-14 | 9,525 | recursive listing (== 0.5.0's `guard_ok 9,525/9,525`) |
| **2026-07-15 (RUN TARGET)** | **9,540** | recursive listing @ 14:4xZ; **9,540 DISTINCT allocation-ids** (1 object each, no dup prefixes -- verified) |

**NOTE -- the +15 is fleet GROWTH, not an anomaly.** 20260715 has 15 MORE allocations than 20260714
(new onboards). **If the run is measured against 9,525, the +15 reads as a false discrepancy.** The
2026-07-15 denominator is **9,540**.

---

### TABLE 1 -- `fact_allocation_valuation` (VALUATION_SCHEMA, 15 cols) -- PINNED
- **EXPECTED ROWS: EXACTLY 9,540** (1 per object; the envelope emits for EVERY object, INCLUDING the
  ~19% with zero positions). **`distinct allocation_id == 9,540`, 1:1 with objects.** [both PINNED -- a
  miss is a real defect: partial landing, dropped envelope, or dedup over-collapse]
- **Expected key shape:** `smartx/platform/silver/fact_allocation_valuation/date=2026-07-15/...parquet`
  (`fact_` per naming law cell-6; scope=platform firm-wide; supersedes the pre-naming-law draft at
  `.../allocation_valuation/`). Exact filename + partition convention (`date=` dir vs flat `{date}`) is
  the writer's -- I assert the SHAPE, not the filename.
- **Schema (15):** `allocation_id, owner_id, as_of, run_date` (string); `equity, long_equity,
  short_equity, cash, accrued_dividends, accrued_fees, accrued_interest` (float64); `long_position_count,
  short_position_count, total_count` (int32); `_ingested_at` (string).
- **Component completeness:** all 10 money/count components present + non-null in **200/200** sampled
  objects. Schema is nullable; **Rule 17 = preserve any null that DOES appear, never fillna.** NO basis
  computed in silver (five internally-consistent AUM bases; canonical `longEquity+cash` GROSS applies in
  GOLD only).

### TABLE 2 -- `fact_allocation_positions` (POSITIONS_SCHEMA, 17 cols) -- MAGNITUDE + invariant
- **EXPECTED ROWS: `sum(len(data.positions))` over the 9,540 objects ~= 110,000** [MAGNITUDE, not pinned]
  - basis: 200-object sample, mean **11.6** positions/obj (median 13.5, range **0-29**). Extrapolation
    `11.6 x 9,540 ~= 110,330`. Coverage 2.1%; the EXACT count is the run's own sum -- **treat ~100k-120k
    as a sanity band, not a pin.** A count far outside it means an unrepresentative sample (re-widen) OR
    a real positions explosion/loss.
  - **~19% of objects have ZERO positions (38/200).** So **positions rows != objects**, and
    **">=1 position per allocation" is FALSE.** Empty-position objects contribute 0 positions rows but
    STILL 1 valuation row.
- **Expected key shape:** `smartx/platform/silver/fact_allocation_positions/date=2026-07-15/...parquet`.
- **Schema (17):** `allocation_id, owner_id, as_of, run_date` (string); `ticker, symbol_id,
  symbol_alias_id, company` (string); `asset_type, industry` (string, vendor bugs preserved); `quantity,
  price, multiplier, market_value, value` (float64); `last_seen_date` (string); `_ingested_at` (string).
- **COUPLING INVARIANT:** `distinct allocation_id` in positions == the ~81% non-empty objects (~7,700),
  a **STRICT SUBSET** of valuation's 9,540. positions.allocation_id \\subseteq valuation.allocation_id.
- **Vendor bugs (grounded in the 200-sample, 2,313 positions):**
  - `asset_type`: **uniformly `equity` (2313/2313)** -- the vendor types everything equity. Preserved
    byte-faithful; classification is a GOLD join (Rule 17).
  - `industry`: **~97% `Unknown / Not Available` (2243/2313)** + a real-value tail (Consumer 27,
    Financial 8, Energy 8, Technology 7, Industrial 6, ...). **NOT uniform** -- preserved exactly as
    delivered, nulls-and-all.

---

### RULE-17 / DTYPE EXPECTATIONS (silver = dedup + dtype ONLY)
- ids / dates / tickers stay **STRING, byte-faithful** (leading-zero-safe -- the gold/Schwab join edge;
  a zero lost at silver is a failed join later). No numeric coercion.
- counts `int32`, values `float64`, per the EXPLICIT pinned schema (never pandas-inferred).
- **dedup = exact-duplicate rows only** (all vendor cols). NO field slimming, NO fillna/dropna, NO
  business-row filter. **Empty-position objects are NOT dropped** -- the valuation envelope still emits.
  (Valuation dedup removes 0: every row carries a distinct `allocation_id`.)

### ACCEPTANCE INSTRUMENT (V2-8 / Rule 22a) -- how the run is judged against this
- Landing = `ListObjectsV2` key+ETag+Size. **HeadObject is NOT the acceptance instrument.**
- **BEHAVIORAL (22a):** row counts read from the LANDED parquet, never the converter's self-report.
- Two falsifiable run-time checks:
  1. **`valuation rows == 9,540` AND `distinct allocation_id == 9,540`.** [HARD -- a miss is a defect]
  2. **`positions rows == run's sum(len(positions))`; sanity `~100k-120k`; positions.allocation_id a
     STRICT SUBSET of valuation's.** [magnitude + invariant]

### OPEN (for 0.5.0 + CTO, not self-adjudicated)
- Exact silver key filename + partition convention -- the writer's; I assert the SHAPE above.
- The 2 pre-naming-law DRAFT objects at non-`fact_` keys (`allocation_{positions,valuation}/date=2026-07-14/`)
  -- delete vs leave is CTO's (key hygiene; bronze-never-rewritten does not bind silver).
- Part 1b (`fact_model_aum_daily` + `fact_model_allocation_roster`) and Part 2 (the 7-feed
  table-or-exemption skeleton) follow this file.
