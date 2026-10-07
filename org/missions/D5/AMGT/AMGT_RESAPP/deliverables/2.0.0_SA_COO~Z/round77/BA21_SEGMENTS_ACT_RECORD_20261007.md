# AMGT_RESAPP round 77 -- `AMGT-ba-21` ACT RECORD: the segments probe ran; BRANCH B; the pull did NOT run

`2.0.0_SA_COO~Z`, 2026-10-07 ~11:4xZ. Pair: COO half @68c7c203a1, CTO half @5907c4e544 (C1, C2).

## C1 -- the vehicle completed today (read before the probe, 11:30Z)

| read | value |
|---|---|
| `OPAL_BBGTML_daily_pull` | LastRunTime 2026-10-07 07:00:01 local, **LastTaskResult 0**, State Ready |
| its log `bbg_tplus1_20261007_070002.log` (last write 07:09 local) | PRECONDITION PASS (DAPI UP, an entitled session answered a real refdata request); PULL EXIT CODE 0; PUBLISH EXIT CODE 0; ETF LEG EXIT CODE 0; CONSTITUENTS LEG EXIT CODE 0; PRICE LEG EXIT CODE 0; RIVALFUNDS BLOOMBERG LEG EXIT CODE 90 (landed); RIVALFUNDS ENRICHMENT EXIT CODE 94 (landed) |
| `OPAL_BBGTML_freshness_check` (the 07:30 ET check) | LastRunTime 2026-10-07 07:30:01 local, LastTaskResult 0, State Ready at 07:30:33 local: finished, not running |

Branch (a): the vehicle completed and the check was over. The probe ran.

## The probe

`research_pulls.py run segments --probe "AMD US Equity"`, ONE `reference_data` call at 2026-10-07T11:32:01Z.
Driver line: `pulled 1 failed 0 calls 1 stopped None`, exit 0.

Landed as received: `s3://opal-data-harvest/bloomberg/harvest/bronze/segments/security_key=AMD_US_Equity/20261007T113201Z.json`,
458 B, VersionId `DfHqbZyXt1rt5KzVoGhwWuVWyTSnNBRh`, document-sha256 `f7129c78...`. Read back by this seat:

| field | result |
|---|---|
| `NAME` | `ADVANCED MICRO DEVICES` (the control: the request reached the security and a known field answered) |
| `SEGMENT_NAME` | `BAD_FLD` / `INVALID_FIELD`, code 9, "Field not valid" |
| `SEGMENT_REVENUE` | `BAD_FLD` / `INVALID_FIELD`, code 9, "Field not valid" |
| `GEOGRAPHIC_SEGMENT_NAME` | `BAD_FLD` / `INVALID_FIELD`, code 9, "Field not valid" |

## Verdict: BRANCH B -- no segment field is served by these names. Step 2 (the 85-name pull) did NOT run.

- What the refusal says (`integrations/bloomberg/READ_HERE.md` section 1 and 4): `INVALID_FIELD` means the mnemonic does not exist
  on the reference-data field surface. It is NOT an entitlement refusal and NOT "not applicable to this security": `NAME` answered
  on the same request. A different name may exist. The three names were proposed from a naming convention and were never read
  from a Bloomberg source (`research_pull_fields.json`), so this is the expected way for a guess to fail.
- It says nothing about whether Bloomberg HOLDS segment data, or about another surface (a bulk field, a historical request with
  overrides, BQL). READ_HERE section 4's rule: ask which surface refused before concluding what Bloomberg does not have.
- `research_pull_fields.json` is NOT edited: `probed` stays false, because no served segment field was found.
- Calls spent under this pair: 1 of at most 1 + 85. The pair is used up for the probe; a second probe with other field names is
  a NEW call and comes back to the CTO first (both halves say so).

## One instrument trap met on the way, no call spent

The first invocation ran under the shell's default interpreter (Python 3.14, which has no `blpapi`). The driver's `health()`
catches the import failure and returns false, so it stopped `TERMINAL_DOWN`, exit 5, `calls 0`, while the Terminal was up (the
vehicle had just completed against it). The same command under the vehicle's interpreter
(`...\Programs\Python\Python311\python.exe`, `blpapi 3.26.4.2`) made the call. A missing library and a signed-out Terminal read
identically in this driver. Surfaced as a row; the driver is not edited here.

## What is owed next (not under this pair)

The right mnemonics. That is a research question (Andrew's relaunch word routes research needs to the CRO): which Bloomberg
reference or bulk fields carry business-segment and geographic-segment revenue for an equity, read from a Bloomberg source and not
from a convention. With an answer in hand, a second one-name probe is asked of the CTO.
FWD-1 on AMD stays "SEGMENT PULL NOT YET RUN" for the round: the served reader of this bronze is uncut and has nothing to read.

---

# ADDENDUM 1 (~12:0xZ) -- the second probe read BRANCH A, and the pull RAN: 85 of 85 landed, 76 carry segment revenue

Everything above this line describes the first probe and stands as written. This addendum supersedes its "the pull did NOT run"
for the day: the CTO gave its word for ONE more probe (msgs 30847 and 30856), on candidates from
`org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/RESAPP_BA21_SEGMENT_MNEMONIC_CANDIDATES_20261007.md` @5be2c73b12 (all from recall,
none read from a Bloomberg source, as that file says).

## The second probe

ONE `reference_data` call on `AMD US Equity` at 2026-10-07T11:48:01Z, through the driver's own `run()` (same gates, same
as-received landing), with `NAME` and the CRO's ranks 1 to 7. Landed:
`.../bronze/segments/security_key=AMD_US_Equity/20261007T114801Z.json`, 3,122 B, VersionId `RI4LGdra.Z86cKzJt3YzCfdiQjMcNl0X`.

| field | result |
|---|---|
| `NAME` | `ADVANCED MICRO DEVICES` (control) |
| `PG_REVENUE` | **SERVED**, a bulk field: 6 rows, each `Metric Name` (Data Center, Client & Gaming, Embedded, ...), `Period 1 Value` to `Period 5 Value`, `Product Geographic Hierarchy Level` |
| `PG_OPERATING_INCOME` | **SERVED**, same shape, 6 rows |
| `BICS_REVENUE_%_LEVEL_ASSIGNED` | answered `100.0`; not a segment table, not pulled |
| `PG_BULK_FIELDS`, `PRODUCT_SEG_NAME`, `GEO_SEG_NAME`, `NUMBER_OF_BUSINESS_SEGMENTS` | each `BAD_FLD` / `INVALID_FIELD` |

BRANCH A. Product (business) segments only: no override is passed, so the geographic split is not asked (the CTO's scope).

## C2 -- the fields-file edit and the name list, before the pull

`research_pull_fields.json`: segments now ask `NAME`, `PG_REVENUE`, `PG_OPERATING_INCOME`, `probed true`, with the refused names
recorded; its test pins that every field asked for is one a probe read SERVED (20 of 20 pass). Commit 588a7fc70e.
Name list: `PLAN_segments_20261007.txt`, 85 names, committed @bb38ea2d43. M = 85, under the bound of 90.

## The pull

`run segments --confirm-calls 85` at 11:50:07Z, vehicle State Ready. The driver recomputed the plan at exactly 85 or it would
have refused. `pulled 85 failed 0 calls 85 stopped None`, done 11:52:25Z. No CAPACITY stop.

**Calls spent under this pair: 2 probes + 85 = 87.** (The COO half pictured 1 + M; the second probe is the CTO's added word.)

## Read after, every one of the 85 landed objects opened

| outcome | names |
|---|---|
| `PG_REVENUE` rows served | **76** (rows per name: min 1, median 8, max 255) |
| `PG_REVENUE` absent from the response, NO field error | **9** |
| no object landed | 0 |
| `PG_OPERATING_INCOME` rows served / not served | 50 / 35 |

The 9 with no revenue rows and no error: `8306 JP`, `8316 JP`, `939 HK`, `BNP FP`, `HSBA LN`, `ISP IM`, `UBSG SW` (seven banks),
`KOFUBL MM` and `WALMEX* MM`. Four of them (`8316 JP`, `BNP FP`, `HSBA LN`, `ISP IM`) DO carry `PG_OPERATING_INCOME` rows. So for
these names the field exists and Bloomberg returned nothing under it: a bank's top line is not filed as "revenue" in this table.
That is a reading of the pattern, not a measurement of why; a different `PG_` measure for banks was not probed.

## What moved, and what did not

- New bronze keys only: 85 objects from the pull plus 2 probe objects, all under `bloomberg/harvest/bronze/segments/`
  (85 partitions; AMD holds 3 objects). Nothing served moved: the reader of this bronze is still uncut.
- **For whoever cuts that reader:** 2 of the 85 partitions are slash names written slash-safe (`BP-SLASH-_LN_Equity`,
  `NG-SLASH-_LN_Equity`). A reader that builds the prefix from the raw key will miss them, exactly as row `AMGT_RESAPP-Z-S365`
  found for the officers reader. Row shape to parse: a list of dicts keyed `Metric Name`, `Period N Value`,
  `Product Geographic Hierarchy Level`; some metric names carry leading non-breaking spaces as indentation; a missing period
  arrives as a value near zero (`-2.4e-14`), not as null. Which fiscal period "Period 1" is, is NOT in the response.
- FWD-1 on AMD stays "segment reader not built" for round 77; the data it needs is now stored.

---

# ADDENDUM 2 (~15:0xZ) -- the third AMD probe: Period 1 is the latest fiscal YEAR, in the reporting currency; the quarter fields do not label the table

The CTO's word for ONE more call (rulings file @f97be3fd6f, bb-1; GO msg 31058), on candidates from
`org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/RESAPP_BB1_PG_REVENUE_PERIOD_AND_CURRENCY_FIELDS_20261007.md` @44c6d20389 (from
recall). `bloomberg_health` read ok first. ONE `reference_data` call on `AMD US Equity` at 2026-10-07T14:58:56Z through the
driver's own `run()`; `pulled 1 failed 0 calls 1`. Landed as received:
`.../bronze/segments/security_key=AMD_US_Equity/20261007T145856Z.json`, 362 B, VersionId `GqgUu55gO_yFhOo0Z3jTJDIhYRvt7M2f`.

| field | served value |
|---|---|
| `NAME` | ADVANCED MICRO DEVICES (control) |
| `SALES_REV_TURN` | **34639.0** |
| `EQY_FUND_CRNCY` | USD |
| `EQY_FISCAL_YR_END` | 12/2025 |
| `PRIMARY_PERIODICITY` | Quarterly and Annual |
| `LATEST_PERIOD_END_DT_FULL_RECORD` | 2026-06-27 |
| `FISCAL_YEAR_PERIOD` | 2026 Q2 |
| `LATEST_ANNOUNCEMENT_DT` | 2026-08-04 |
| `CRNCY` | USD |

Nine of nine served; no field error.

**The comparison the CTO asked for.** The level-1 rows of the stored `PG_REVENUE` table (object `20261007T114801Z.json`), Period 1:
Data Center 16,635 + Client & Gaming 14,550 + Embedded 3,454 = **34,639** ("All Other" carries the missing-value marker). This
seat re-summed it from the stored object. `SALES_REV_TURN` returned **34,639.0**. They are equal.

**What that measures, and what it does not:**
- Period 1 of the bulk table is the company's latest ANNUAL period, in the units and currency of the fundamentals fields.
  `EQY_FISCAL_YR_END` 12/2025 names its year end and `EQY_FUND_CRNCY` USD names its currency. For AMD these are measured.
- `LATEST_PERIOD_END_DT_FULL_RECORD` (2026-06-27) and `FISCAL_YEAR_PERIOD` (2026 Q2) describe the latest QUARTER. They do NOT
  label the table. A reader that printed either beside Period 1 would print the wrong period.
- Periods 2 to 5 as "one fiscal year back each" is still an assumption; nothing in this call measures it.
- This is one name. The other 84 need the same three fields (`SALES_REV_TURN`, `EQY_FISCAL_YR_END`, `EQY_FUND_CRNCY`) to carry a
  period and a currency: 84 or 85 calls, a NEW Bloomberg pull, which is Andrew's word (the CTO's ruling says so). Not run.
- AMD now holds 4 objects under the segments table; 2 carry the table (11:48Z probe 2, 11:51Z the pull) and 2 are probes of other
  fields (11:32Z, 14:58Z). The newest object is NOT the table. The reader (cell bb-1) takes the newest object that carries the
  table, which its draft already states.

Calls on AMD under the segments word today: 3 probes and 1 in the pull. No further call follows from this one.
