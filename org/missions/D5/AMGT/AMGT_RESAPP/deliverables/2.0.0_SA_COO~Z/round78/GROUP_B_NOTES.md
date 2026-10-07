# AMGT_RESAPP round 78 -- GROUP B draft cells (bb-2, bb-8, bb-9, bb-10, bb-11)

Drafted for `2.0.0_SA_COO~Z`, 2026-10-07 ~14:35Z. Nothing here is committed, built or deployed.

**How every number below was read.** One read of the deployed function `opal-amgt-scoped-api`, GET-shaped direct
invokes as `round77/checks/r77_served_shape.py` makes them: `/security/<KEY>/overlay` and `/security/<KEY>/thesis` for
the 95 names of `covered_security_keys()` plus `MSFT_US_Equity` and `ABNB_US_Equity`. 194 invokes, 194 answered 200
(overlay 97 of 97, thesis 97 of 97), bodies saved and counted offline. Called "the deployed read" below. Three further
reads are named where used: the pool list (`crosswalk.load_crosswalk()`), the stored run records
(`s3://opal-data-harvest/packs/<key>/input_ledger.json`), and the Security Scanner universe files
(`s3://opal-data-portal-v2/json/security_scanner/latest/universes/<id>/universe_data.json`, the files the peer engine
reads). Line numbers in `lib/research/api/scoped_amgt.py` are at its last commit `8c0c6de8c5` (workspace HEAD
`cfa0bdc08c`; the file did not move during this session).

**Shape shared by all five cells.** One new stdlib-only module plus its test; no cell edits
`lib/research/api/scoped_amgt.py`; each names the hookup the adapter cell makes. All five check scripts pass
`bash .tools/commit-gate.sh`. Every BUILD criterion fails at the base (the module is absent) and every BOUND criterion
passes there. Each build check was also run once against a throwaway in-memory reference module (scratch, not in the
repo) and read YES on every clause, so no check is unpassable. The reference modules were 12 to 35 lines each.

The words a served sentence must not use (inlined in each ACT): identity, unresolved, security key, crosswalk,
dossier, landed, model block, estate, stage, input ledger, bronze.

---

## B1 -- `AMGT-bb-2` -- ONE STATEMENT OF INPUTS (ruling 4, FWD-12; row AMGT_RESAPP-Z-W286-S2)

### 1. THE SOURCE
- `org/missions/D5/AMGT/AMGT_RESAPP/ledger/ROUND_ANALYSIS.round77.md:37` -- "**One served statement per name, read by
  both places.** The Model tab's ledger reads the same served `input_provenance` the top block reads, or it is removed.
  Its Filings line states what the page actually used. Producer cell here; the page cell is DSGN_AMGTV1's".
- `org/tier1_exec/3.0.0_SA_CVO/deliverables/DSGN_AMGTV1_FWD20_CLAUSE_COUNT_AND_FWD27_REGRADE_20261007.md:56-58` --
  "The foot says "Filings: no source set up yet; has not run yet." The Exec tab of BA US and VLO US lists officers
  "from Item 10" of the 10-K, and the Thesis is drawn from the 10-K. A reader is told the filings both feed the page and
  have never run."

### 2. MEASURED AT THE BASE
Where the two statements are built:
- The top block: overlay field `input_provenance`, built by `_overlay_input_provenance` (`scoped_amgt.py:3332-3344`)
  through `top_band.input_provenance` (`lib/research/api/top_band.py:201-236`), served at `:3495`. Rows come from the
  name's /freshness row. It has no filings row.
- The Model tab's "Where each input came from": route `/security/<key>/ledger` (`:6940-6944`),
  `read_input_ledger_served` (`:6048-6061`) = the stored run record (`read_input_ledger`, `:5912-5991`, six classes
  from `lib/research/ledger/ledger.py:48-55`: market_data, filings, news, social, web, sa) composed with a third
  statement, the overlay's `provenance` (`_overlay_provenance`, `:3226-3295`). The page prints it at
  `portal/src/pages/SecurityAnalysis/tabs/ModelTab.tsx:696-752`; a class with no run prints "has not run yet" (`:748`)
  and a class with no source prints "no source set up yet" (`:686`).
- So the page is served THREE statements of inputs today, not two: `input_provenance`, `provenance`, and `/ledger`.

Counts (the deployed read, denominator 95 covered names):
- `input_provenance` served: 95 of 95. Row classes: `bloomberg, seekingalpha, serp, pack` on 95 of 95. A filings row:
  0 of 95. Outcomes: bloomberg "landed" 95; pack "landed" 95; serp "never read" 95; seekingalpha "never read" 92,
  "landed" 3.
- Overlay `provenance.inputs` filings row: present 95 of 95, `last_run` null on 95 of 95, reason "no filings run is
  recorded yet for this name" on 95 of 95.
- What `/thesis` actually takes from a filing: filing passages (`passage_coverage.sections`) 12 of 95; written
  sections with a filing behind them (`drafting_provenance.accession`) 12; segment rows with a filing source 10;
  officers marked `source: "filing"` 7; a driver chart with `source: "filing"` and points 1. Any of the five: **12 of
  95**. Forms: 10-K 7, 20-F 5.
- **The contradiction: 12 of 95.** All 12 names whose thesis cites a filing are told "no filings run is recorded". The
  other 83 are told the same and cite none, so for them the line is true. The 12 start: ASML NA, BABA US, BA US,
  COST US, HAL US, HD US, INTU US, KMB US.
- Stored run records (S3 read): present 95 of 95; classes with a run: market_data on 95, every other class on 0.
  The filings class has never had a run recorded for any covered name, because no filings writer records one
  (`ledger.py:50`, `"filings": {"source": None, "stage": None}`). The Filings line can never become true by waiting.

### 3. THE ACT (worker face text)

Today the page states where its inputs came from in more than one place and the statements disagree: one says
"Filings: has not run yet" on a name whose thesis quotes its 10-K. Build the ONE statement both places will read.

Create `lib/research/api/inputs_statement.py` (standard library only: it rides the deployed package with no build
edit) exporting ONE function:

`statement(input_provenance, thesis)` returns a list of rows.
- `input_provenance` is the list the overlay serves today: four dicts `{input, source, last_run, outcome, reason}`
  for `bloomberg`, `seekingalpha`, `serp`, `pack`.
- `thesis` is the `/thesis` body for the same name (a dict), or `None` when the caller could not read it.

Rules:
1. Every row of `input_provenance` is returned unchanged, in the same order. Do not copy-edit them.
2. Add exactly ONE row with `input: "filings"`, placed immediately before the `pack` row (last when there is no
   `pack` row). Its keys: `input`, `source`, `last_run`, `outcome`, `reason`, `form`, `filing_date`, `used_for`.
   `source` is "company filings read for this name".
3. The page uses a filing when any of these five is true in `thesis`, and `used_for` lists the true ones in this
   order and these words:
   - `passage_coverage.sections` has one or more entries -> "the filing passages"
   - `drafting_provenance.accession` is set and `drafted_sections` is non-empty -> "the written sections"
   - `segment_breakdown.rows` is non-empty and `segment_breakdown.source.form` is set -> "the segment table"
   - `thesis_driver_chart.source == "filing"` with one or more `points` -> "the driver chart"
   - one or more of `management.officers` has `source == "filing"` -> "the officer list"
4. When one or more is true: `outcome: "landed"`; `form` and `filing_date` from the newest `filing_date` among
   `passage_coverage.source`, `drafting_provenance` and `segment_breakdown.source`; `last_run` equal to `filing_date`;
   `reason` one sentence naming the form, the date and the uses, for example "This page uses the 10-K filed 2026-01-30
   for the filing passages, the written sections and the officer list."
5. When none is true: `outcome: "never read"`, `last_run`, `form`, `filing_date` all `None`, `used_for: []`, `reason`
   "No company filing has been read for this name yet, so nothing on this page comes from one."
6. When `thesis` is `None`: `outcome: "failed"`, `reason` "What this page took from company filings could not be read
   just now." A failed read must never read as "never read".
7. `outcome` uses only the three values the other rows already use: "landed", "never read", "failed".
8. No sentence you write (`reason`, `source`, `used_for`) uses: identity, unresolved, security key, crosswalk,
   dossier, landed, model block, estate, stage, input ledger, bronze. (`"landed"` is allowed as the `outcome` value
   only; it is an existing code, not a sentence.)
9. The function reads no store, calls nothing and does not change its arguments.

Plant tests in `lib/research/api/tests/test_inputs_statement.py`: all five uses; one use; none; `thesis` None; no
`pack` row; arguments unchanged.

You do NOT edit `lib/research/api/scoped_amgt.py`, `lib/research/api/top_band.py` or any portal file. Your report
names the hookup below and anything about it you found different.

**The hookup the adapter cell makes (named, not built here):**
- `read_thesis_bundle`, after `passage_coverage` is set (`scoped_amgt.py:3700-3701`, before `return bundle` at
  `:3702`): `bundle["input_provenance"] = inputs_statement.statement(_overlay_input_provenance(resolved_key), bundle)`.
  The thesis body already holds all five parts, so this costs one cached freshness read and no new store read.
- `read_security_overlay`, `:3495`: the same statement under the same key `input_provenance`. The overlay does not
  hold the thesis parts, so the adapter supplies them (issuer question 1 below).
- The six-class ledger is replaced by this statement: the Model tab reads `input_provenance` (five rows) and stops
  calling `/ledger`. The `/ledger` route and the overlay's `provenance` block then have no reader on the page; whether
  they are removed or left unread is the adapter cell's and the page cell's, not this one's.

### 4. THE CRITERIA
- **AC1 (build)** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb2.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: the four rows come back unchanged with ONE filings row before the pack row; a page that uses a filing reads "landed" with its form, date and five uses; a page that uses none reads "never read"; unread parts read "failed"; no served sentence carries a system word; C1-C4 PASS; R78 BB2 AC1 SERVED: YES; and exit=0
- **AC2 (seam, the real neighbour)** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb2.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: on the real overlay and thesis of BA_US_Equity the filings row reads "landed" with a form and a date; on AMD_US_Equity it reads "never read"; the four existing rows are unchanged on both; C1-C3 PASS; R78 BB2 AC2 SERVED: YES; and exit=0
- **AC3 (bound)** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb2.py" --crit AC3 --where local; echo "exit=$?"`
  Expect: the existing four-row builder's tests still pass; R78 BB2 AC3 SERVED: YES; and exit=0

### 5. THE BASE DRY-RUN
```
AC1: FAIL C0 lib.research.api.inputs_statement imports cannot import name 'inputs_statement' from 'lib.research.api' (...\lib\research\api\__init__.py)
     R78 BB2 AC1 SERVED: NO
     exit=1                                   -> base: FAIL as expected (build)
AC2: FAIL C0 lib.research.api.inputs_statement imports cannot import name 'inputs_statement' from 'lib.research.api' (...)
     R78 BB2 AC2 SERVED: NO
     exit=1                                   -> base: FAIL as expected (build)
AC3:    32 passed in 0.97s
     PASS C1 the four-row builder's tests pass rc=0
     R78 BB2 AC3 SERVED: YES
     exit=0                                   -> base: PASS as expected (bound)
```
Positive control (reference module, real handler): BA US read `filings 'landed' '10-K' '2026-01-30'` with all five
uses; AMD US read `filings 'never read'`. AC2 runs the real handler locally four times (about a minute).

### 6. `<paths>`
```
lib/research/api/inputs_statement.py
lib/research/api/tests/test_inputs_statement.py
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```
(plus the worker's own `deliverables/0.9.0_WK_AMGT_RESAPP~<n>/` folder, as round 77 cut it)

### 7. Risk and class
`LOCAL`; `worker-light` (the reference module was 35 lines).

### 8. Edges
None to build. The adapter cell hooks it after this drains. The page cell is DSGN_AMGTV1's and follows the redeploy.

### 9. Not measured, and questions for the issuer
1. **Where is the one statement served?** On `/thesis` it is free. On `/overlay` the adapter must supply the thesis
   parts, which costs reads on the page's first paint (the CVO read first paint at 3,495 ms, per
   `ROUND_ANALYSIS.round77.md:61`). Options: (a) both routes, the overlay reading the thesis body through the served
   cache; (b) `/thesis` only, and the top block reads `/thesis`. I did not measure the added time of (a).
2. **Three statements, not two.** The overlay's `provenance` block (`:3492`) is a third statement and is the source of
   the false Filings line. Ruling 4 names two places. Does the adapter cell retire `provenance` and `/ledger`, or
   leave them served and unread?
3. **The filings row's date.** `last_run` on the other rows is a read time (`20261006T132334Z`); the filings row
   carries the filing's own date (`2026-01-30`), because no time of reading is stored for a filing. The row also
   carries `filing_date` so the page can label it. If a read time is wanted instead, it has to be stored first.
4. **Off-task, no row filed (the channel file is outside my write set):** `input_provenance` reads seekingalpha
   "never read" (`last_run` "NEVER") on 92 of 95 names and "landed" on 3, all three dated 2026-09-11. Round 77's
   analysis (`:10-12`) describes the same three as stale beside rows reading "All inputs current". A reader of the
   top block is told Seeking Alpha has never been read for 92 names. Whether that is true or a plane mismatch is the
   subject of row AMGT_HARVST-Z-S100 (commit `2a18cdc6d0`); I did not read it.
5. Not measured: the `/ledger` route on the deployed function (the brief limited deployed reads to overlay and
   thesis). Its content is stated from the code and the stored run records.

---

## B2 -- `AMGT-bb-8` -- EACH PEER PRICE WITH THE CURRENCY OF ITS OWN LISTING (FWD-8)

### 1. THE SOURCE
- `org/missions/D13/DSGN/DSGN_AMGTV1/ledger/CTO_COUNTERSIGN_COMPLETION_GRADES_ROUND46.md:31-35` -- "The failing limb
  is a Price column headed "currency not stated" holding 230,500 beside 356.62. A reader cannot compare it. Producer:
  each peer price is served with its currency, and the page prints it. "TSM US" beside 2,365 gets one read by the
  producer (which listing that price belongs to). ... a currency is read from a stored field, never inferred from the
  exchange code."
- `org/tier1_exec/3.0.0_SA_CVO/deliverables/DSGN_AMGTV1_ROUND46_COMPLETION_GRADE_20261007.md:43-46` -- "The Price
  column is headed "currency not stated" and holds 230,500, 172,100 and 1,495,000 beside 356.62 and 589.90. ... "TSM
  US" sits beside a price of 2,365. Whether that price belongs to the US listing is unread".
- Carried by `ROUND_ANALYSIS.round77.md:58`: "each peer price served with its currency".

### 2. MEASURED AT THE BASE
**Round 69 already built the field; it does not do what is asked.** `_with_price_currency`
(`scoped_amgt.py:2371-2400`, cell AMGT-at-3) with `lib/research/peers/price_currency.py` serves `price_currency` or a
plain `price_currency_reason` on every peer row. So I draft a cell, for two measured reasons:

- **Coverage (the deployed read).** Names with a peer set: 57 of 95. Peer rows: 676, every one with a price (676 of
  676). With `price_currency`: **25 of 676**. With the reason only: 651 of 676, all one reason ("... this peer is not
  matched to a company record that states its trading currency"). Neither: 0. The currency comes only from the row's
  own matched company record; 651 rows name no record (`identity.resolution` UNRESOLVED on 651).
- **Three of the 25 served currencies belong to a different listing.** The row matched by company name to a US
  listing while the price is the home-exchange price:
  - `688910` Taiwan Semiconductor, country Taiwan, price 2,365.0, served `USD` from `TSM_US_Equity` (2 rows: the
    tables of 2317 TT and GOOGL US);
  - `268236` Petroleo Brasileiro, country Brazil, price 47.31, served `USD` from `PBR_US_Equity` (1 row).
  This answers the CTO's "TSM US" read: the 2,365 is the Taiwan listing's price, and the page is served USD beside it.
  A wrong currency is worse than none. How the 25 were matched: company name 19, the pool list's own key 4, Japan
  exchange code 2. Of the 19 name matches, 3 pair a US-listing record with a non-US row; the other 16 pair a listing
  in the row's own country (Roche CHF, AstraZeneca GBp, RWE EUR and so on).

Where a currency could be read from stored data, with no vendor call:
- **The scanner file itself: nowhere.** Row fields over 5,264 rows of the six universe files: `ticker, name, mktVal,
  country, sector, industryGroup, universeWeight, divzWeight, price, values`. A field naming a currency: 0 of 10. The
  factor metadata file mentions "currency" 0 times. `cap_currency` is USD on 676 of 676 rows and is the market cap's
  currency, not the price's.
- **The pool list: no.** Its 243 records carry no currency field (0 of 243).
- **A US row's own company record: yes, partly.** 489 of the 651 rows are United States rows with a plain alphabetic
  ticker. Asking the pool list for `"<ticker> US"` (the engine's declared US rule, `lib/research/peers/universe.py:36-41`)
  resolves 164 of them; 50 of those 164 name a key with a stored company record (which states `CRNCY`), 48 of them
  covered names. So about 50 more rows can be served a currency from stored data.
- **What cannot be served from stored data:** about 600 of 676 rows (the 325 US rows the pool list does not hold, the
  114 it holds with no stored record, and 162 non-US rows). Samsung's 230,500 is one of them.

### 3. THE ACT (worker face text)

A peer row's price comes from the Security Scanner, which quotes each price in that listing's own trading currency
and stores no currency beside it. Today the page is served the currency of the peer's matched company record. That is
right when the record is the same listing as the price, and wrong when it is not: Taiwan Semiconductor's Taiwan price
of 2,365 is served with "USD" because the company matched to its US listing.

Create `lib/research/peers/price_listing.py` (standard library only) exporting ONE function:

`record_for_price(member, resolve)` returns `{"record_key": <key or None>, "basis": <word or None>, "reason": <sentence or None>}`.
- `member` is one peer row as served: it carries `ticker`, `country` (the scanner's country name, such as
  "United States" or "Taiwan"), and `identity`, a dict whose `security_key` is the company record the row was matched
  to, or `None`.
- `resolve` is a function the caller hands in: `resolve("MSFT US")` returns a record key or `None`. Do not import the
  pool list yourself.

Rules, in order:
1. **Own ticker.** The row has a record key and the row's `ticker` equals the key's first part (the text before the
   first underscore: `HD` for `HD_US_Equity`, `8306` for `8306_JP_Equity`). Return that key, `basis: "own_ticker"`.
2. **Refused: a US listing behind a foreign price.** The row has a record key that ends `_US_Equity`, its ticker is
   not the key's first part, and its `country` is not "United States". Return no key, no basis, and this reason:
   "This price is quoted on the company's home exchange. The company record we hold is its United States listing, so
   that record's currency is not used for this price."
3. **Name match, same country.** The row has any other record key. Return it, `basis: "name_match"`.
4. **US ticker.** The row has no record key, its `country` is "United States" and its `ticker` is letters only. Ask
   `resolve(ticker + " US")`. If it returns a key, return it with `basis: "us_ticker"`.
5. **Otherwise** return `{"record_key": None, "basis": None, "reason": None}`. For a row that is not a United States
   row with a letters-only ticker, do not call `resolve` at all.
6. Never work out a currency from a country, an exchange code or the market-cap currency. This function chooses a
   record or refuses one; the currency is read from that record by the caller.
7. The reason uses none of: identity, unresolved, security key, crosswalk, dossier, landed, model block, estate,
   stage, input ledger, bronze.

Plant tests in `lib/research/peers/tests/test_price_listing.py`: one case per rule, the `BRK.B` ticker (not letters
only: rule 5), and a `resolve` that raises (let it raise; the caller decides).

You do NOT edit `lib/research/api/scoped_amgt.py` or `lib/research/peers/price_currency.py`.

**The hookup the adapter cell makes:** in `_with_price_currency` (`scoped_amgt.py:2371-2400`), the record asked for a
row's currency becomes `price_listing.record_for_price(m, _resolve_held_form)["record_key"]` in place of
`price_currency.member_record_key(m)` (`:2382-2384`; `_resolve_held_form` is at `:2328-2333`). At `:2398`, a row whose
answer carries a `reason` is served `price_currency_reason` equal to that reason and no `price_currency`. The currency
itself is still read by `_record_trading_currency` (`:2357-2368`).

### 4. THE CRITERIA
- **AC1 (build)** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb8.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: HD keeps its own record; the Taiwan row matched to TSM_US_Equity is refused with a plain reason; Roche keeps its Swiss record; MSFT takes the record named for "MSFT US"; Samsung gets none and the list is not asked; C1-C5 PASS; R78 BB8 AC1 SERVED: YES; and exit=0
- **AC2 (seam, the real neighbour)** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb8.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: over the stored peer sets of 2317_TT_Equity, BA_US_Equity and VLO_US_Equity every row gets an answer, the row 688910 matched to TSM_US_Equity is refused, and no answer pairs a US-listing record with a row from another country; C1-C3 PASS; R78 BB8 AC2 SERVED: YES; and exit=0
- **AC3 (bound)** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb8.py" --crit AC3 --where local; echo "exit=$?"`
  Expect: the existing price-currency tests still pass; R78 BB8 AC3 SERVED: YES; and exit=0

### 5. THE BASE DRY-RUN
```
AC1: FAIL C0 lib.research.peers.price_listing imports cannot import name 'price_listing' from 'lib.research.peers' (...\lib\research\peers\__init__.py)
     R78 BB8 AC1 SERVED: NO
     exit=1                                   -> base: FAIL as expected (build)
AC2: FAIL C0 lib.research.peers.price_listing imports cannot import name 'price_listing' from 'lib.research.peers' (...)
     R78 BB8 AC2 SERVED: NO
     exit=1                                   -> base: FAIL as expected (build)
AC3:    9 passed in 0.50s
     PASS C1 the existing price-currency tests pass rc=0
     R78 BB8 AC3 SERVED: YES
     exit=0                                   -> base: PASS as expected (bound)
```
Positive control (reference module, real stored sets): `rows 36; by basis {None: 20, 'us_ticker': 16}; refused
[('688910', 'TSM_US_Equity')]; crossed []`.

### 6. `<paths>`
```
lib/research/peers/price_listing.py
lib/research/peers/tests/test_price_listing.py
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 7. Risk and class
`LOCAL`; `worker-light` (the reference function was 20 lines).

### 8. Edges
None to build. The adapter hookup is the served move.

### 9. Not measured, and questions for the issuer
1. **This cell does not make FWD-8 true.** After it and its hookup, about 75 of 676 rows carry a currency (22 kept
   + about 50 added) and 3 wrong ones are refused. About 600 rows still read a reason, because no stored field
   states the scanner price's currency. Closing FWD-8 needs one of: the Security Scanner's producer adds a currency
   to its universe rows (another project's file), or a vendor pull of `CRNCY` for the peer names (a vendor use, on
   Andrew's word). That call is the CTO's or Andrew's; it is not a cell I can draft from stored data.
2. **The three wrong currencies are served now** (2317 TT, GOOGL US and PBR US peer tables). I filed no row: the
   channel file is outside my write set. It wants one, `disarm_owner` `2.0.0_SA_COO~Z`.
3. Rule 2 catches a US listing behind a foreign price. A non-US depositary listing behind a home price (a London
   depositary receipt, say) would pass rule 3. I found none among the 19 name matches; I did not measure the class
   beyond those 19.
4. The "about 50" assumes each of the 50 stored records states `CRNCY`; I counted the records' folders under
   `derived/model_block/` (102 distinct), not the figure inside each.
5. The PBR row sits in PBR US's own peer table: the company's home listing is listed as its own comparable. Not this
   cell's; noted for the peer engine's self-exclusion rule.

---

## B3 -- `AMGT-bb-9` -- THE COUNTRY IN PLAIN CASE (FWD-27 ground 2)

### 1. THE SOURCE
- `org/tier1_exec/3.0.0_SA_CVO/deliverables/DSGN_AMGTV1_FWD20_CLAUSE_COUNT_AND_FWD27_REGRADE_20261007.md:52-53` -- "**A
  vendor string beside the page's own form.** The foot prints "Country: UNITED STATES" where the identity header
  prints "Industrials -- US"."
- `org/tier1_exec/3.0.0_SA_CVO/deliverables/DSGN_AMGTV1_ROUND49_FWD20_FWD27_REGRADE_20261007.md:63` -- "**Ground 2, the
  vendor string: STANDS.** "Country: UNITED STATES" on 2 of 2."
- `org/missions/D13/DSGN/DSGN_AMGTV1/ledger/CTO_COUNTERSIGN_COMPLETION_GRADES_ROUND46.md:153-154` -- ""Country: UNITED
  STATES" (served, producer)".

### 2. MEASURED AT THE BASE
- **The served field** is the header figure with `mnemonic: "COUNTRY_FULL_NAME"` in `header_figures`, on both
  `/overlay` and `/thesis`. The page prints its `value` as it is (`portal/src/pages/SecurityAnalysis/modelSheet.ts:171-177`:
  "`value` is exactly the served header figure's value", label "Country"). The figure is a stored Bloomberg text
  field passed through by `_header_figures` (`scoped_amgt.py:2545-2581`).
- **Counts (the deployed read, 95 names, same on both routes):** the figure is served on 95 of 95; distinct values 22;
  all capitals on **95 of 95**. Values: UNITED STATES 33, BRITAIN 12, FRANCE 7, JAPAN 5, SWITZERLAND 5, BRAZIL 4,
  MEXICO 4, CHINA 3, NETHERLANDS 3, CANADA 2, GERMANY 2, HONG KONG 2, ITALY 2, PHILIPPINES 2, TAIWAN 2, FINLAND 1,
  INDIA 1, PANAMA 1, SINGAPORE 1, SPAIN 1, SWEDEN 1, URUGUAY 1 (sum 95).
- **Round 77 does not do it:** 0 of 95 serve it in plain case.
- **The existing rule:** display names are re-cased by `_clean_display_name` / `_title_case_display_name`
  (`scoped_amgt.py:943-983`). It lives in the file this cell may not edit, and it carries company-name rules (share
  classes, legal forms, "CO/THE") that do not belong on a country. The rule to reuse is its principle: an
  all-capitals vendor text is served in title case, and a text that already carries a lower-case letter is served
  as it is.
- A second candidate source, measured and not recommended: the peers country map
  (`lib/research/peers/taxonomy.py:104-160`) gives a plain name for the two-letter code in `CNTRY_OF_DOMICILE`. It
  names 20 of the 22 served codes; it has no entry for PA and UY, and it reads "United Kingdom" where Bloomberg's
  text reads "BRITAIN". Re-casing the served text keeps Bloomberg's own word and covers 22 of 22.

### 3. THE ACT (worker face text)

The page prints "Country: UNITED STATES" because the country arrives from the data vendor in capitals and is passed
through. Serve it in plain case.

Create `lib/research/api/country_name.py` (standard library only) exporting TWO functions:

`plain_country(value)` returns the country text in plain case.
1. A value that is not text, is empty, or already carries a lower-case letter is returned unchanged.
2. Otherwise each run of letters becomes one word with a capital first letter and the rest lower case: "UNITED
   STATES" -> "United States", "HONG KONG" -> "Hong Kong", "BRITAIN" -> "Britain".
3. The words "of", "and" and "the" stay lower case unless they open the name: "ISLE OF MAN" -> "Isle of Man",
   "TRINIDAD AND TOBAGO" -> "Trinidad and Tobago".
4. Punctuation and spacing are kept; each side of a hyphen is its own word: "GUINEA-BISSAU" -> "Guinea-Bissau".
5. No country is renamed. "BRITAIN" stays "Britain"; do not turn it into another name.

`with_plain_country(header_figures)` returns a NEW list for the header figures of one company.
6. The entry whose `mnemonic` is `COUNTRY_FULL_NAME` and whose `value` is text is replaced by a COPY with `value`
   set to `plain_country(value)` and a new key `value_as_stored` holding the text as it was.
7. Every other entry is the same object, in the same position. The list handed in and its entries are not changed.
   A list with no such entry comes back as an equal new list.

The 22 values served today, all of which must come out right: BRAZIL, BRITAIN, CANADA, CHINA, FINLAND, FRANCE,
GERMANY, HONG KONG, INDIA, ITALY, JAPAN, MEXICO, NETHERLANDS, PANAMA, PHILIPPINES, SINGAPORE, SPAIN, SWEDEN,
SWITZERLAND, TAIWAN, UNITED STATES, URUGUAY.

Plant tests in `lib/research/api/tests/test_country_name.py`: the 22 values, the three shapes of rules 3 and 4, the
unchanged cases of rule 1, and rules 6 and 7.

You do NOT edit `lib/research/api/scoped_amgt.py`.

**The hookup the adapter cell makes:** where each bundle is assembled, AFTER the figure checks have been computed
from the stored list: `"header_figures": country_name.with_plain_country(header_figures)` in `read_security_overlay`
(`scoped_amgt.py:3472`) and in `read_thesis_bundle` (`:3632`). The checks at `:3447` and `:3628` keep reading the
stored list, so no check result moves.

### 4. THE CRITERIA
- **AC1 (build)** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb9.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: the 22 country values served today read in plain case (22 of 22); small words stay lower and hyphen parts are cased; a plain, empty or non-text value comes back unchanged; the country entry is a re-cased copy with the stored text kept and nothing else moves; C1-C4 PASS; R78 BB9 AC1 SERVED: YES; and exit=0
- **AC2 (seam, the real neighbour)** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb9.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: BA_US_Equity's stored record reads "United States" with "UNITED STATES" kept beside it, the entry count is unchanged and no other value moved; C1-C2 PASS; R78 BB9 AC2 SERVED: YES; and exit=0

### 5. THE BASE DRY-RUN
```
AC1: FAIL C0 lib.research.api.country_name imports cannot import name 'country_name' from 'lib.research.api' (...\lib\research\api\__init__.py)
     R78 BB9 AC1 SERVED: NO
     exit=1                                   -> base: FAIL as expected (build)
AC2: FAIL C0 lib.research.api.country_name imports cannot import name 'country_name' from 'lib.research.api' (...)
     R78 BB9 AC2 SERVED: NO
     exit=1                                   -> base: FAIL as expected (build)
```
Positive control (reference module, real record): `BA US: header entries 24 -> 24; stored country 'UNITED STATES';
served 'United States'; kept beside it 'UNITED STATES'; other values moved []`.

### 6. `<paths>`
```
lib/research/api/country_name.py
lib/research/api/tests/test_country_name.py
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 7. Risk and class
`LOCAL`; `worker-light` (the reference module was 22 lines).

### 8. Edges
None.

### 9. Not measured, and questions for the issuer
1. **`value` is rewritten, not a new field beside it.** The page prints `value`, and the CTO states DSGN_AMGTV1 cuts
   no page round until this deploys (`CTO_COUNTERSIGN_COMPLETION_GRADES_ROUND46.md:206-208`), so a new field would
   leave the page unchanged. The stored text travels as `value_as_stored`. If a rewritten `value` is not wanted,
   the alternative is a `display_value` field and a page cell.
2. **"BRITAIN" becomes "Britain"**, Bloomberg's word, beside an identity line reading "GB". If the firm wants "United
   Kingdom", that is a rename table, and rule 5 forbids it here; rule on it.
3. Other all-capitals text among the header figures (thesis, 95 names): `NAME` 95 of 95, `SHORT_NAME` 94,
   `LONG_COMP_NAME` 5. The page's foot lists four header facts (`modelSheet.ts:172-177`); `SHORT_NAME` is still in
   that list in the tree I read (portal `a3ab197f`), though the CTO records it removed on the round-47 candidate.
   This cell re-cases the country only.
4. Not measured: the print pack. `lib/research/print/render_pack.py:356` labels the same figure "Country"; whether
   it reads the served bundle or the stored record I did not read, so the pack may still print capitals.
5. The check runs no plant-test criterion; the test file is graded by the suite at the drain.

---

## B4 -- `AMGT-bb-10` -- ONE SERVED MARKER FOR A NAME OUTSIDE COVERAGE (row AMGT_RESAPP-Z-S364)

### 1. THE SOURCE
- `org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round47/ROUND47_CLOSE.md:43-44` -- "**No coverage
  marker is served** for a pool name outside coverage. The page infers it from the shape of the seven header figures.
  A served marker would let the page say "not covered" in its own words instead of repeating the producer's reason."
- `org/missions/D13/DSGN/DSGN_AMGTV1/ledger/CTO_COUNTERSIGN_COMPLETION_GRADES_ROUND46.md:126-127` -- "The rule is keyed
  on the served SHAPE, not on coverage, because no coverage marker is served. So it also fires for a covered name
  whose seven figures are all absent for one shared reason."
- Same file `:143-144` -- "**For the next AMGT_RESAPP enrichment list** (named by the close, accepted here): a plain
  served news-source name; a served coverage marker for a pool name outside coverage; the two lower-case served lines
  above."

### 2. MEASURED AT THE BASE
The deployed read, three overlays:

| | MSFT_US_Equity | ABNB_US_Equity | AMD_US_Equity (covered control) |
|---|---|---|---|
| status | 200 | 200 | 200 |
| header figures | 7, all null | 7, all null | 24, none null |
| "We hold no stored company data for this name yet." | on 7 of 7 | on 7 of 7 | on 0 |
| a field naming coverage | none | none | none |
| served name | Microsoft Corp | Airbnb Inc | Advanced Micro Devices Inc |
| news feed | SERVED, 35 items | NEVER_HELD, 0 | SERVED, 18 items |
| peer rows | 12 | 0 | 12 |
| `input_provenance` reason | "nothing has been read from this input ..." | "this name is not among the names the freshness view lists ..." | (landed) |

- **No marker is served.** Top-level overlay fields: MSFT 25, AMD 23; the two extra are `places_moved` and
  `places_moved_reason`. No field on either says whether the name is covered. `/thesis` likewise (its only field
  with "cover" in the name is `passage_coverage`, about filing sections).
- All three names read `identity_status: MEASURED` from the pool list, so nothing served tells them apart except
  the shape of the figures.
- **Denominators (pool-list read and `covered_security_keys()`):** pool records 243, each with its own key (243
  distinct); covered names 95, all 95 in the pool; **pool names outside coverage 148**.
- Two outside names say different things in the top block: MSFT is listed by the freshness view, ABNB is not. A
  marker lets the page say one thing for both.
- Round 77 does not do it: the marker is absent on 97 of 97 overlays read.

### 3. THE ACT (worker face text)

We serve a page for any company in our wider company list, but we cover (hold research and company figures for)
only some of them. For a company we do not cover, nothing served says so: the page shows seven header figures each
reading "We hold no stored company data for this name yet." Build the ONE marker that says it once.

Create `lib/research/api/coverage_marker.py` (standard library only) exporting ONE function:

`marker(security_key, covered_keys)` returns a dict with exactly these four keys: `status`, `covered`, `sentence`,
`covered_names`.
- `security_key` is the company's key as text, or `None`.
- `covered_keys` is the collection of keys we cover, or `None` when the caller could not read that list.

Rules:
1. `covered_keys` is `None`: `status: "not_known"`, `covered: None`, `covered_names: None`, `sentence` "We could not
   check just now whether we cover this company." A list that could not be read must never read as "not covered".
2. `security_key` is in `covered_keys`: `status: "covered"`, `covered: True`, `sentence: None`.
3. Anything else, including an empty or missing key: `status: "outside_coverage"`, `covered: False`, `sentence` "We
   do not cover this company yet, so we hold no company figures or research for it. Any news or comparable companies
   shown here come from our wider market data."
4. In rules 2 and 3 `covered_names` is the count of distinct keys in `covered_keys`.
5. The three statuses are the whole set; every input gets exactly one. Keys are compared exactly as given (no
   re-casing, no trimming).
6. No sentence uses: identity, unresolved, security key, crosswalk, dossier, landed, model block, estate, stage,
   input ledger, bronze.

Plant tests in `lib/research/api/tests/test_coverage_marker.py`: one per rule, a key with a slash (`BP/_LN_Equity`),
a list with a repeated key (counted once), a `set` and a `list` argument.

You do NOT edit `lib/research/api/scoped_amgt.py`.

**The hookup the adapter cell makes:** a new top-level field `research_coverage` on both bundles:
`"research_coverage": coverage_marker.marker(resolved_key, covered)` in `read_security_overlay` (the bundle at
`scoped_amgt.py:3467-3496`) and `read_thesis_bundle` (`:3629`). `covered` is `covered_security_keys()` read as
`_covered_key_known` reads it (`:1064-1081`), and `None` when that read raises.

### 4. THE CRITERIA
- **AC1 (build)** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb10.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: a covered name reads "covered" with no sentence; a name outside the list and an empty key read "outside_coverage" with one plain sentence; an unread list reads "not_known", never "outside_coverage"; every answer carries the four fields and no system word; C1-C4 PASS; R78 BB10 AC1 SERVED: YES; and exit=0
- **AC2 (seam, the real neighbour)** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb10.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: against the real covered list every covered name reads "covered" (N of N); MSFT_US_Equity and ABNB_US_Equity read "outside_coverage" with the sentence and AMD_US_Equity reads "covered"; the pool's names split into the two statuses with nothing left over; C1-C3 PASS; R78 BB10 AC2 SERVED: YES; and exit=0

### 5. THE BASE DRY-RUN
```
AC1: FAIL C0 lib.research.api.coverage_marker imports cannot import name 'coverage_marker' from 'lib.research.api' (...\lib\research\api\__init__.py)
     R78 BB10 AC1 SERVED: NO
     exit=1                                   -> base: FAIL as expected (build)
AC2: FAIL C0 lib.research.api.coverage_marker imports cannot import name 'coverage_marker' from 'lib.research.api' (...)
     R78 BB10 AC2 SERVED: NO
     exit=1                                   -> base: FAIL as expected (build)
```
Positive control (reference module, real lists): `every covered name reads covered 95 of 95`; `pool names 243; by
status {'covered': 95, 'outside_coverage': 148}; covered list 95`; `95 + 148 = 243`.

### 6. `<paths>`
```
lib/research/api/coverage_marker.py
lib/research/api/tests/test_coverage_marker.py
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 7. Risk and class
`LOCAL`; `worker-light` (the reference function was 12 lines).

### 8. Edges
None.

### 9. Not measured, and questions for the issuer
1. **The field name.** I draft `research_coverage`, not `coverage`: the function already serves a route `/coverage`
   (articles collected, `scoped_amgt.py:4004`) and a field `passage_coverage` (filing sections). A bare `coverage`
   field would be a third meaning.
2. **A second meaning of "covered" is already served.** `lib/research/coverage/covered_no_block.py` answers a name
   in the Security Scanner's S&P 500 list that is NOT in the pool (Deere) with `covered_no_block`, described as
   "covered, no block yet". Under this marker Deere reads `outside_coverage` (it is not one of the 95). Two served
   fields would then disagree about the word. Rule which one "covered" means; I recommend the 95, and that the
   Deere answer's wording is changed in the adapter cell.
3. **The CTO's routed finding** (`CTO_COUNTERSIGN_COMPLETION_GRADES_ROUND46.md:201-204`): "for a name outside coverage
   the chatter line says the name is not in the covered set, and never "no articles"". The marker gives the page
   what it needs to do that; if the line is to be served instead, it is a further act on the monthly chatter read,
   not in this cell.
4. Not measured: the overlays of the other 146 outside names. The 148 is a count of keys, not of pages read.
5. The sentence says "yet". ABNB was registered for a first pull (round 77, ba-23), so "yet" is true of it; for MSFT
   it is a hope. Drop the word if it promises too much.
6. The check runs no plant-test criterion; the test file is graded by the suite at the drain.

---

## B5 -- `AMGT-bb-11` -- A PLAIN SERVED NEWS-SOURCE NAME

### 1. THE SOURCE
- `org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round47/ROUND47_CLOSE.md:40-42` -- "**The news source
  is served with storage words:** `harvested news (the overlay feed, gold article_security_mention)`. The page now
  maps that exact string to "Articles we collect"; if the producer changes the string, the row falls back to "source
  not named". A plain served source name would remove the page-side mapping."
- `org/missions/D13/DSGN/DSGN_AMGTV1/ledger/CTO_COUNTERSIGN_COMPLETION_GRADES_ROUND46.md:129-130` -- "The news source
  string is mapped on the page to "Articles we collect", beside the existing Bloomberg and Seeking Alpha mappings; an
  unmapped source reads "source not named"."
- Same file `:143` -- "a plain served news-source name".

### 2. MEASURED AT THE BASE
The string the source names is the News class's `source` on the `/ledger` route, written at `scoped_amgt.py:6015`.
It is one of several places a source is served. The deployed read, 95 names:

| where | what is served | plain already? |
|---|---|---|
| top band items (`top_band.items[].publisher`) | 69 items on 57 of 95 names: Seeking Alpha 35, Barron's 14, Bloomberg 14, Wall Street Journal 4, Financial Times 2 | **YES, 69 of 69**, by `top_band.PUBLISHER_NAMES` (round 76, az-2); the code travels beside it as `publisher_code` |
| feed items (`feed.items[].publisher`) | 640 items: `sa` 222, `barrons` 202, `bbg` 164, `wsj` 43, `ft` 9 | **NO, 0 of 640**: a code only, 5 distinct codes, no name beside it |
| `feed.source` | "gold article_security_mention (the day view's own source)" on 95 of 95 | NO |
| `provenance.inputs[].source` | 3 strings, each on 95 of 95: "input ledger, class filings"; "the overlay feed's newest harvested article (fetched_at)"; "the input ledger's newest market_data run" | NO |
| `input_provenance[].source` | 4 strings, each on 95 of 95, e.g. "Bloomberg data pulls stored for this name" | YES |
| `/ledger` News class `source` | "harvested news (the overlay feed, gold article_security_mention)" (from the code; the route was not read on the deployed function) | NO |

- **So round 76 already does it for the top band, and I draft no cell for the band.** What is left is the feed's
  item codes and five storage-word source strings.
- **A plain-name map exists, but not where the brief looked.** `lib/research/lists/data/publishers.json` is a
  register of 2 web domains (seekingalpha.com, sap.com) with owner and review dates; it maps no code to a name. The
  code-to-name map is `top_band.PUBLISHER_NAMES` (`lib/research/api/top_band.py:23-29`), 5 codes, and it covers 5 of
  the 5 codes the feed serves. The page keeps its own copy (`portal/src/pages/SecurityAnalysis/components/publisherNames.ts`).

### 3. THE ACT (worker face text)

The page is served the names of its sources in the system's own words, such as "harvested news (the overlay feed,
gold article_security_mention)", and has to translate them itself. Serve a plain name beside each.

Create `lib/research/api/source_names.py` (standard library plus `lib.research.api.top_band`, which is itself
standard library only) exporting THREE functions:

`source_name(raw)` returns `{"name": <plain name or None>, "known": <True or False>}`.
1. It knows exactly these eight texts, compared exactly:
   - "harvested news (the overlay feed, gold article_security_mention)" -> "Articles we collect"
   - "gold article_security_mention (the day view's own source)" -> "Articles we collect"
   - "the overlay feed's newest harvested article (fetched_at)" -> "Articles we collect"
   - "input ledger, class filings" -> "Company filings"
   - "input ledger, class filings (a filings stage run recorded for this name)" -> "Company filings"
   - "the input ledger's newest market_data run" -> "Bloomberg"
   - "the Bloomberg pull the model block was computed from (raw_stamp_used)" -> "Bloomberg"
   - "model block and input ledger" -> "Bloomberg"
2. Any other value, including `None`, returns `{"name": None, "known": False}`. Never return the raw text as a name.

`publisher_name(code)` returns the publisher's name for a code, or `None`.
3. Read the names from `top_band.PUBLISHER_NAMES`; do not write a second table. An unknown code or a non-text value
   returns `None`. (Note the difference from the top band, which serves an unknown code as it is.)

`with_publisher_names(items)` returns a NEW list of news items.
4. Each item is a COPY carrying a new key `publisher_name` equal to `publisher_name(item["publisher"])`; `publisher`
   and every other key are unchanged. An item with an unknown or missing code gets `publisher_name: None`. The list
   handed in and its items are not changed.

5. No name you serve uses: identity, unresolved, security key, crosswalk, dossier, landed, model block, estate,
   stage, input ledger, bronze, gold, harvested, overlay, ledger.

Plant tests in `lib/research/api/tests/test_source_names.py`: the eight texts, an unknown text, `None`, the five
codes, an unknown code, and rule 4.

You do NOT edit `lib/research/api/scoped_amgt.py` or `lib/research/api/top_band.py`. The raw `source` texts stay as
they are: other readers and tests compare them.

**The hookup the adapter cell makes** (each adds a name BESIDE the raw text, never in place of it):
- `read_feed`: `items` through `source_names.with_publisher_names(items)` (items built at `scoped_amgt.py:5346-5357`)
  and a new `source_name` beside `source` (`:5316`).
- `_overlay_provenance`: a `source_name` on each of the three entries (`:3290-3295`).
- `_compose_ledger_provenance`: a `source_name` on the News class (`:6015`) and on a Filings class with a source
  (`:6026`).

### 4. THE CRITERIA
- **AC1 (build)** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb11.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: each of the eight source texts served today has a plain name (8 of 8); an unknown text is not passed off as a name; the five publisher codes are named and an unknown code is not; items are copied with the name beside the unchanged code; C1-C4 PASS; R78 BB11 AC1 SERVED: YES; and exit=0
- **AC2 (seam, the real neighbour)** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb11.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: the real feed of BA_US_Equity has its source text known and named "Articles we collect", and every item gets a publisher name (N of N); C1-C2 PASS; R78 BB11 AC2 SERVED: YES; and exit=0
- **AC3 (bound)** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb11.py" --crit AC3 --where local; echo "exit=$?"`
  Expect: each of the eight raw texts is still written in the producer's source (8 of 8); R78 BB11 AC3 SERVED: YES; and exit=0

### 5. THE BASE DRY-RUN
```
AC1: FAIL C0 lib.research.api.source_names imports cannot import name 'source_names' from 'lib.research.api' (...\lib\research\api\__init__.py)
     R78 BB11 AC1 SERVED: NO
     exit=1                                   -> base: FAIL as expected (build)
AC2: FAIL C0 lib.research.api.source_names imports cannot import name 'source_names' from 'lib.research.api' (...)
     R78 BB11 AC2 SERVED: NO
     exit=1                                   -> base: FAIL as expected (build)
AC3: PASS C1 every raw string the map names is still written in the producer 8 of 8; gone []
     R78 BB11 AC3 SERVED: YES
     exit=0                                   -> base: PASS as expected (bound)
```
Positive control (reference module, real feed): `BA US feed: status 'SERVED'; ... items 74; with a publisher name 74;
codes ['barrons', 'bbg', 'sa', 'wsj']`.

### 6. `<paths>`
```
lib/research/api/source_names.py
lib/research/api/tests/test_source_names.py
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 7. Risk and class
`LOCAL`; `worker-light` (the reference module was 25 lines).

### 8. Edges
No build edge. **A ruling edge with B1:** the one text the source sentence names is served only by `/ledger`. If the
B1 hookup retires `/ledger` and the overlay's `provenance` block from the page, six of the eight texts lose their
reader, and this cell shrinks to the feed (the item codes and `feed.source`). Rule B1's question 2 before cutting
this one, or cut it as drafted and accept that part of the map may serve nothing.

### 9. Not measured, and questions for the issuer
1. **Is this cell wanted at all once B1 lands?** See the edge above. The part that stands either way: 640 feed items
   served with a code and no name, across the 95.
2. The eight texts are an exact-match table of text written in another file. AC3 fails the day one of them is
   reworded, which is the point, but it also means a rewording in the adapter cell must update this table in the same
   round.
3. Not measured: whether the page prints `feed.source` or the `provenance` source strings anywhere today. I read the
   Model tab's ledger (`ModelTab.tsx:672-687`), which prints the `/ledger` source through its own three-entry map.
4. Not read on the deployed function: `/ledger` (outside the routes the brief allowed).

---

## CHECK SCRIPTS

```
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb2.py    AC1 build, AC2 seam, AC3 bound
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb8.py    AC1 build, AC2 seam, AC3 bound
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb9.py    AC1 build, AC2 seam
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb10.py   AC1 build, AC2 seam
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb11.py   AC1 build, AC2 seam, AC3 bound
```

One line per check for the issuance commit:
```
bb-2 AC1 base: FAIL as expected    bb-2 AC2 base: FAIL as expected    bb-2 AC3 base: PASS as expected
bb-8 AC1 base: FAIL as expected    bb-8 AC2 base: FAIL as expected    bb-8 AC3 base: PASS as expected
bb-9 AC1 base: FAIL as expected    bb-9 AC2 base: FAIL as expected
bb-10 AC1 base: FAIL as expected   bb-10 AC2 base: FAIL as expected
bb-11 AC1 base: FAIL as expected   bb-11 AC2 base: FAIL as expected   bb-11 AC3 base: PASS as expected
```

Every seam criterion (`AC2`) reads live stores from the worker's shell (S3, and for bb-2 the function's own handler
run locally). A worker with no AWS credentials in its shell fails them for that reason, not for its code.

## WHAT THE ADAPTER CELL INHERITS (all in `lib/research/api/scoped_amgt.py`)

| from | function | where | effect on the served body |
|---|---|---|---|
| bb-2 | `inputs_statement.statement` | `:3700-3702` (thesis), `:3495` (overlay) | `input_provenance` gains a filings row; thesis gains `input_provenance` |
| bb-8 | `price_listing.record_for_price` | `:2381-2385`, `:2398` | 3 wrong currencies become reasons; about 50 US rows gain a currency |
| bb-9 | `country_name.with_plain_country` | `:3472`, `:3632` | the country `value` in plain case, `value_as_stored` beside it |
| bb-10 | `coverage_marker.marker` | bundles at `:3467` and `:3629` | new field `research_coverage` |
| bb-11 | `source_names.*` | `:5316`, `:5346-5357`, `:3290-3295`, `:6015`, `:6026` | `publisher_name` and `source_name` beside the raw values |

bb-2, bb-9 and bb-10 all touch the two bundle assemblies; they are one adapter cell's edits, in one worktree.
