# AMGT_RESAPP round 79 -- GROUP A: the segment table is SERVED (cc-1, cc-2) -- round-78 analysis R1, enrichment item 1, FWD-1

Drafted for `2.0.0_SA_COO~Z`, 2026-10-08 ~10:2xZ, by a drafting subagent of that seat. Each check was written as a file, passed
`bash .tools/commit-gate.sh`, and was run at the base (HEAD `c92e860791`; the three product files it reads last changed at
`59f820cf17`); the outputs are quoted under each cell. Each build criterion was also run once against an in-memory stub held
outside the repo, to show the check can read YES: those results are in section 4 of each cell. No product file was created or
edited. Neither cell edits `lib/research/api/scoped_amgt.py`: the hookup is the round's adapter cell's and is written out in
A2 section 8.

---

## A1 -- `AMGT-cc-1` -- THE SEGMENTS READER FINDS A STORED TABLE HOWEVER MANY LATER PULLS SIT ABOVE IT

### 1. MEASURED AT THE BASE
- One read of the whole stored set, 2026-10-08 ~10:0xZ, bucket `opal-data-harvest`, prefix
  `bloomberg/harvest/bronze/segments/`: **85 folders, 88 objects**, 0 keys of any other shape. Objects per folder: 1 in 84
  folders, 4 in 1 (`AMD_US_Equity`). Deepest folder: 4.
- Bodies it takes to reach the newest object that carries a segment list, newest first: 1 for 79 names, 2 for 1 name (AMD),
  and 5 names have no object that carries one (`8306_JP_Equity`, `939_HK_Equity`, `KOFUBL_MM_Equity`, `UBSG_SW_Equity`,
  `WALMEX*_MM_Equity`; one object each). 85 = 79 + 1 + 5.
- AMD's four objects, newest first: a pull of other fields with no segment list and no errors (362 bytes), a table (2,622
  bytes), a table (3,122 bytes), a pull of refused fields (458 bytes).
- The reader as built (`lib/research/api/segment_table.py`, `MAX_READ = 5`) reads the five newest bodies EVERY time and then
  chooses: it read 1 body on 84 names and **4 on AMD, where 2 are needed**. It serves revenue rows on 76 names and the sentence
  "Bloomberg's stored table for this name has no revenue by business line." on 9 (4 of the 9 carry operating income lines
  only: `8316_JP_Equity`, `BNP_FP_Equity`, `HSBA_LN_Equity`, `ISP_IM_Equity`).
- The blind spot, planted: a table under six newer error-free objects with no segment list reads status `none` and the
  no-revenue sentence, with the newest object as its source (check AC1 P1 at the base). No stored folder reaches it today.
- One body read from this box (n = 88): median 77 ms, 90th percentile 109 ms, longest 146 ms. Object size: smallest 103
  bytes, median 2,131, largest 74,988.
- The limit proposed, **20**, is five times today's deepest folder. Its worst case is a name whose 20 newest objects carry no
  table: 20 bodies, about 1.5 seconds from this box, on every request for that name. Today no name is near it.

### 2. THE ACT (worker face text)

A company's stored Bloomberg segment table sits in one folder, one object per pull. The reader built last round looks at the
five newest objects only. Five later pulls of other fields would hide a stored table, and the reader would then say the table
"has no revenue by business line", which is false: it stopped looking. Change the reader so that it finds the table however
many later pulls sit above it, reads no body it does not need, and says in plain words when it stopped with objects unread.

Edit `lib/research/api/segment_table.py` and its tests `lib/research/api/tests/test_segment_table.py`. Read both whole first.
The function's name, its arguments, the nine keys it returns and every sentence it serves today stay as they are.

1. `MAX_READ` becomes `20`. It is the most object BODIES one call may read. The folder is still listed once, whole, and its
   `.json` keys sorted newest first, exactly as now.
2. Walk the sorted keys newest first and read ONE body at a time. After each body, decide before reading the next:
   - if the object carries a table (the existing `_carries_table` rule: no `PG_REVENUE` field error, and it holds `PG_REVENUE`
     or `PG_OPERATING_INCOME`), it is the chosen object: STOP, read nothing more;
   - otherwise, if it is the first object seen that the existing `_usable` rule accepts, remember it as the fallback;
   - a body whose `response` is not a dictionary counts as one body read and is passed over, as now.
3. Stop reading when `MAX_READ` bodies have been read, whether or not a table was found.
4. Choose:
   - a table was found: that object, and everything after the choice (the source block, the rows, the share-capital and
     one-heading refusals, the no-revenue case) runs exactly as it does today;
   - no table was found and EVERY object of the folder was read: the fallback if there is one (today's second pass: it reads
     the no-revenue sentence with that object as its source), else `REASON_NONE_USABLE`, both exactly as today;
   - no table was found and one or more objects were left unread: return `_result(reason=REASON_NOT_ALL_READ)`: status
     `none`, no rows, no source. This holds even when a fallback was seen. The no-revenue sentence is never served by a call
     that left objects unread.
5. Add the constant, with this exact text:
   `REASON_NOT_ALL_READ = "Bloomberg's %d newest stored pulls for this name hold no business-line table; the older ones were not looked at." % MAX_READ`
6. The function still never raises: any exception is the read-failed reason, as now. Correct the module's opening text to
   describe the walk and the limit.
7. No sentence uses: identity, unresolved, security key, crosswalk, dossier, landed, model block, estate, stage, input ledger,
   bronze.

In `lib/research/api/tests/test_segment_table.py`:
8. Keep all seventeen existing test functions, by name. ONE existing assertion changes, and only that one: in
   `test_nothing_objects_none_usable`, `assert len(store.reads) == 5` becomes `assert len(store.reads) == 7` (the folder holds
   seven objects, fewer than the limit, so all seven are read). Add `"REASON_NOT_ALL_READ"` to the names listed in
   `test_reasons_use_plain_words`.
9. Add plant tests: a table under six newer error-free objects with no segment list is served from the table's object; eight
   objects whose newest carries the table read exactly one body; `MAX_READ + 3` objects with no segment list above a table
   read `REASON_NOT_ALL_READ`, exactly `MAX_READ` bodies and no source; a garbled object OLDER than the table is never read
   and the table is served.

You do NOT edit `lib/research/api/scoped_amgt.py`, `lib/research/api/segment_period.py`,
`lib/research/filings/table_class.py` or `lib/research/harvest/store.py`. Criterion AC2 reads the real store (read only):
it writes nothing and neither do you. Run `lib/research/api/tests/` before your commit and report its last line. In your
report, give the bodies read on `AMD_US_Equity` before and after your change.

### 3. THE CRITERIA
- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc1.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: a table under six newer objects with no segment list is served from its own object; eight objects whose newest carries the table read one body; MAX_READ is 20; objects left unread are said to be unread and never called no revenue, with exactly MAX_READ bodies read; a folder read to its end keeps its round-78 answers; P1-P5 PASS; R79 CC1 AC1 SERVED: YES; and exit=0
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc1.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: AMD US serves its rows from the newest stored object that carries the table and reads no body past it; every stored name reads as its whole folder says and reads no body it does not need (N of N); S1-S2 PASS; R79 CC1 AC2 SERVED: YES; and exit=0
- **AC3** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc1.py" --crit AC3 --where local; echo "exit=$?"`
  Expect: the seventeen round-78 plant cases are all still in test_segment_table.py and the file passes; B1 PASS; R79 CC1 AC3 SERVED: YES; and exit=0

### 4. THE BASE DRY-RUN
```
AC1 (base, HEAD c92e860791):
FAIL P1 a table under six newer objects with no segment list is served status 'none' rows 0 source 20261107T000000Z.json bodies read 5 reason "Bloomberg's stored table for this name has no revenue by business line."
FAIL P2 the reader stops at the first object that carries a table bodies read 5
FAIL P3 MAX_READ is 20 MAX_READ 5
FAIL P4 objects left unread are said to be unread, never called no revenue bodies read 5 of 9; reason "Bloomberg's stored table for this name has no revenue by business line."
PASS P5 a folder read to its end keeps its round-78 answers no list: "Bloomberg's stored table for this name has no revenue by business line."; refused fields: "Bloomberg's stored segment data for this name holds no business-line table yet."
R79 CC1 AC1 SERVED: NO
exit=1      -> FAIL as expected (build: the five-object limit and the read-all-five walk)

AC2 (base):
FAIL S1 AMD serves its rows from the newest object that carries the table and reads no body past it source 20261007T115113Z.json; bodies read 4, needed 2, in the folder 4
   stored names 85; serving revenue rows 76; deepest folder 4 object(s); most bodies needed 2; MAX_READ 5; e.g. wrong ['AMD_US_Equity (rows 6, bodies read 4, needed 2)']
FAIL S2 every stored name reads as its whole folder says and reads no body it does not need 84 of 85
R79 CC1 AC2 SERVED: NO
exit=1      -> FAIL as expected (build: AMD is served the right table today, but four bodies are read where two are needed)

AC3 (base):
   17 passed in 0.58s
PASS B1 the seventeen round-78 plant cases are all still there and the file passes rc=0; round-78 cases present 17 of 17
R79 CC1 AC3 SERVED: YES
exit=0      -> PASS as expected (bound)

REACHABLE (the same check file, the reader's walk replaced in memory by a scratch stub outside the repo; no product file written;
clause names shortened to "..." here, details literal):
AC1 (stub):
PASS P1 ... status 'served' rows 2 source 20261101T000000Z.json bodies read 7 reason None
PASS P2 ... bodies read 1
PASS P3 MAX_READ is 20 MAX_READ 20
PASS P4 ... bodies read 20 of 24; reason "Bloomberg's 20 newest stored pulls for this name hold no business-line table; the older ones were not looked at."
PASS P5 ...
R79 CC1 AC1 SERVED: YES   exit=0
AC2 (stub):
PASS S1 ... source 20261007T115113Z.json; bodies read 2, needed 2, in the folder 4
   stored names 85; serving revenue rows 76; deepest folder 4 object(s); most bodies needed 2; MAX_READ 20; e.g. wrong []
PASS S2 ... 85 of 85
R79 CC1 AC2 SERVED: YES   exit=0
```

### 5. `<paths>`
```
lib/research/api/segment_table.py
lib/research/api/tests/test_segment_table.py
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and class
`LOCAL` (a reader module and its tests; no deploy, no store write). `worker-light`: the change to the product file is under
40 lines.

### 7. Edges
None inbound. It does not wait on A2 and A2 does not wait on it: A2 calls the reader by name and works with either walk.
Outbound: the adapter cell and the redeploy; the deploy pair names `segment_table.py` among the files whose bytes change.

### 8. Not measured, and questions for the issuer
- **The limit of 20 is a drafting choice, the issuer's to change.** It is not derived from a pull cadence: how often a pull of
  other fields lands in these folders was not read (88 objects, all but AMD's from one pull day). The check reads the number
  as the constant `N_STATED = 20` at the top of `r79_cc1.py`; change both together.
- The cost of a body read from the deployed function was not timed; the figures in section 1 are from this box.
- One change of behaviour beyond the blind spot, stated so it is not a surprise: today a garbled object anywhere in the five
  newest makes the whole read fail; after this cell a garbled object OLDER than the table is never read, so the table is
  served. A garbled object NEWER than the table still reads the read-failed reason.
- Kept as built, not changed here: when the newest object that carries a table holds operating income lines only, the reader
  stops there and does not look for an older object with revenue lines. No stored folder has that shape today (the 4
  operating-income-only names hold one object each).
- AC2's S2 passes for 84 of 85 names at the base, so its build signal rests on ONE stored name (AMD). If AMD's folder were
  trimmed to its table before the worker runs, AC2 would pass at the base and only AC1 would carry the build.

---

## A2 -- `AMGT-cc-2` -- ONE SERVED SEGMENT TABLE WITH ITS PERIOD AND CURRENCY LABELS (FWD-1, CTO MSG 31077)

### 1. MEASURED AT THE BASE
- The two modules this cell stands on are merged and unserved: `lib/research/api/segment_table.py`
  (`read_segment_table(security_key, client=None)`) and `lib/research/api/segment_period.py`
  (`label_periods(period_sums, revenue_by_year, currency)`). No file `lib/research/api/segment_served.py` exists; the word
  `segment_table` appears in `scoped_amgt.py` only as an unrelated status string at `:4015`.
- One run over all 85 stored names, 2026-10-08 ~10:1xZ, of a scratch stub of this cell's function, fed the figures exactly as
  `read_thesis_bundle` holds them (`read_model_block`, then the fiscal-year list and the header list):
  - 76 names serve revenue rows; 9 read a plain reason (4 of the 9 carry operating income lines only). 0 names lack stored
    company figures.
  - Period 1 is labelled on **72** and unlabelled on **4** (`8766_JP_Equity`, `AMXB_MM_Equity`, `RIO_LN_Equity`,
    `SAN_FP_Equity`): the round-78 read's 72 and 4, reproduced through the adapter's own reads.
  - Columns labelled per served table, of 5: five on 63 names, four on 8, three on 2, two on 2, one on 1 (AMD). 76 = 63 + 13.
    Every one of the 76 has one or more labelled columns, so the currency is stated on 76 of 76, including the 4 whose
    Period 1 is unlabelled (their later columns tie).
  - Currency served: USD 38, EUR 14, GBP 7, BRL 3, JPY 3, CHF 2, MXN 2, TWD 2, CAD 1, CNY 1, INR 1, PHP 1, SGD 1 (sum 76).
    Stored unit of the tied revenue figure: `MILLIONS` on 76 of 76. No name repeats a fiscal year among its revenue figures.
  - AMD US: 6 rows (Data Center, Client & Gaming, Client, Gaming, Embedded, All Other); Period 1 sum of the level-1 rows
    34,639.0 = stored fiscal year 2025 revenue; Periods 2 to 5 (16,136; 11,817; 10,595; 3,940) tie to no stored year.
  - One call of the stub (one listing and the bodies) from this box: median 103 ms, longest 271 ms.
- In `read_thesis_bundle` (`scoped_amgt.py:3629`) the stored header list is `header_figures` (`:3650`) and the stored
  fiscal-year list is `fiscal_year_figures` (`:3659`); the filing-text breakdown is set at `:3739`. A revenue entry reads
  `{"scope": "fiscal_year_line_item", "fiscal_year": "2016", "mnemonic": "SALES_REV_TURN", "value": 4319.0, "unit": "MILLIONS", ...}`
  and the currency entry `{"scope": "header", "mnemonic": "EQY_FUND_CRNCY", "value": "USD", ...}`. A name with no stored
  company figures has an empty fiscal-year list and a header list of seven entries, none of them the currency.

### 2. THE ACT (worker face text)

We hold, for 76 companies, Bloomberg's table of revenue by business line. Two pieces were built last round and neither is
served: a reader of the stored table, and a function that names a column of the table with a fiscal year only where the
column adds up to the company's reported revenue. Build the ONE function that puts them together and returns the block the
`/thesis` route will serve under the key `segment_table`. Another cell connects it to the route.

Read first, whole: `lib/research/api/segment_table.py`, `lib/research/api/segment_period.py`, and their tests in
`lib/research/api/tests/`. Do not edit them.

Create `lib/research/api/segment_served.py` exporting ONE function:

`serve_segment_table(security_key, fiscal_year_figures, header_figures, client=None)`

- `security_key`: the company, underscore form (`AMD_US_Equity`, `BP/_LN_Equity`), or None.
- `fiscal_year_figures`: a list of stored figure entries (dictionaries with `scope`, `fiscal_year`, `mnemonic`, `value`,
  `unit`), possibly empty, possibly None.
- `header_figures`: a list of stored header entries (dictionaries with `mnemonic`, `value`), possibly empty, possibly None.
- `client`: a store client, handed on untouched.

It returns a dictionary with EXACTLY these ten keys:

| key | value |
|---|---|
| `status` | `"served"` when revenue rows are served, else `"none"` |
| `rows` | the reader's `rows`, unchanged: each `{"segment", "level", "values"}` with five values, a number or None |
| `operating_income_rows` | the reader's `operating_income_rows`, unchanged |
| `periods` | a list of five column entries (rule 5), or `[]` |
| `period_note` | one plain sentence about how the columns are named, or None |
| `currency` | the reporting currency code, stated only where a column ties (rule 6), else None |
| `units` | the units of the figures in lower case (for example `"millions"`), stated only where a column ties, else None |
| `currency_note` | one plain sentence about the currency and units, or None |
| `reason` | the reader's `reason`, unchanged (None when rows are served) |
| `source` | the reader's `source`, unchanged |

Each entry of `periods` has EXACTLY these five keys: `period` (1 to 5), `label` (`"Fiscal year 2025"` when the column is
named, else `"Period 3"` with its own number), `fiscal_year` (the stored year text such as `"2025"`, or None),
`top_level_sum` (the sum the column was tested with, or None), `note` (None when the column is named, else one plain
sentence saying why it is not).

Rules:
1. **The store is read only through the reader.** Import the module (`from lib.research.api import segment_period,
   segment_table`) and call `segment_table.read_segment_table(security_key, client=client)` exactly ONCE, by that dotted
   name, so a test can replace it. Import no store library and call no store method yourself.
2. **Nothing to show.** When the reader returns no `rows`: `status` is `"none"`, `rows` is `[]`, `operating_income_rows`,
   `reason`, `source`, `period_note` and `currency_note` are the reader's own values, `currency` and `units` are None.
   `periods` is `[]`, except when the reader returned operating income rows: then it is five entries, each
   `{"period": n, "label": "Period n", "fiscal_year": None, "top_level_sum": None, "note": None}`.
3. **The column sums.** For each column n from 1 to 5: take `row["values"][n - 1]` of every row of `rows` whose `level` is
   exactly 1, keep the values that are not None and are larger than 1e-6 in size, and add them. A column with no value kept
   has the sum None. Rows of level 2 and deeper are never added.
4. **The stored figures.** Revenue by year: from `fiscal_year_figures`, every entry that is a dictionary with `mnemonic`
   equal to `"SALES_REV_TURN"`, `scope` equal to `"fiscal_year_line_item"`, a `fiscal_year` that is not None and a `value`
   that is a number (a true/false value is not a number); the key is `str(fiscal_year)`, and the first entry seen for a year
   wins. Keep each year's `unit` beside it. Currency: the `value` of the first entry of `header_figures` that is a
   dictionary with `mnemonic` equal to `"EQY_FUND_CRNCY"` and a non-empty text value, stripped; None when there is none.
   Anything that is not a list, or an entry that is not a dictionary, is passed over without error.
5. **Naming the columns.** Call `segment_period.label_periods(sums, revenue_by_year, currency)` once. For each entry it
   returns, in order: `period` and `fiscal_year` as returned; `top_level_sum` is its `sum`; `label` is `"Fiscal year "` plus
   the year when it has one, else `"Period "` plus the number; `note` is None when it has a year, else the result's own
   top-level `reason` when that is not None (no reported revenue is held), else the entry's `reason`. Never name a column
   yourself and never carry a year from one column to the next: the function you call is the only thing that names one.
6. **Currency and units.** `currency` is the `currency` that call returned (it is None unless one or more columns tie).
   `units` is the stored `unit` of the revenue figure of the lowest-numbered named column, stripped and in lower case, or
   None when no column is named or that unit is not text.
7. **`period_note`**, one of four exact sentences:
   - no reported revenue was held (the call's top-level `reason` is not None): "We hold no reported revenue for this company
     to name these columns from, so they keep Bloomberg's own period numbers."
   - revenue held, no column named: "No column adds up to the company's reported revenue for any year we hold, so the
     columns keep Bloomberg's own period numbers."
   - all five named: "Each column is named with the fiscal year whose reported revenue its top-level rows add up to."
   - otherwise: "A column is named with a fiscal year where its top-level rows add up to the company's reported revenue for
     that year. The other columns keep Bloomberg's own period numbers."
8. **`currency_note`**, one of four:
   - no column named: the reader's `segment_table.CURRENCY_NOTE`;
   - named, currency and units both known: "Figures are in <units> of <currency>, the units and currency of the reported
     revenue these columns add up to." (for AMD: "Figures are in millions of USD, ...");
   - named, currency known, units not: "Figures are in <currency>, the currency of the reported revenue these columns add up
     to; the units are not stated.";
   - named, no currency held: "We hold no reporting currency for this company, so the currency of these figures is not
     stated."
9. **It never raises.** Wrap the whole body: on any exception return `status` `"none"`, `rows` `[]`,
   `operating_income_rows` `[]`, `periods` `[]`, `reason` equal to `segment_table.REASON_FAILED`, and None for the other
   five keys.
10. It does not change its arguments, and it does not change the dictionary the reader returned in a way that alters
    `rows`, `operating_income_rows` or `source`.
11. No sentence uses: identity, unresolved, security key, crosswalk, dossier, landed, model block, estate, stage, input
    ledger, bronze.

Plant tests in `lib/research/api/tests/test_segment_served.py`, with a small fake client like the one in
`test_segment_table.py`: one case per rule 2 to 9 (both halves of rule 2; each of the four sentences of rules 7 and 8), a
figures list holding entries of another mnemonic and another scope that must not be counted, arguments left unchanged, and
the reader replaced by a recorder to show it is called once with the client handed in.

You do NOT edit `lib/research/api/scoped_amgt.py`, `lib/research/api/segment_table.py`,
`lib/research/api/segment_period.py` or their tests. Criterion AC2 reads the real store (read only) and takes about a
minute. Run `lib/research/api/tests/` before your commit and report its last line. Your report states the hookup the adapter
cell must make: the call, its three arguments as they are named in `read_thesis_bundle`, and the served key.

### 3. THE CRITERIA
- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc2.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: a column that ties is labelled with its fiscal year with currency and units stated and the rows unchanged; a column that ties to no year and a column with no figure are unlabelled and each says why; with no figures the table is still served unlabelled; nothing to show reads a plain reason and never raises; every answer carries exactly the ten keys and every period entry its five; no served sentence uses a system word; the store is read only through read_segment_table, once; F1-F7 PASS; R79 CC2 AC1 SERVED: YES; and exit=0
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc2.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: AMD US serves its revenue rows with Period 1 labelled fiscal year 2025 in millions of USD; 8766 JP serves its rows with Period 1 unlabelled and a plain note; a name with no stored table and a stored name with no revenue lines each read their own plain reason; every stored name is served and its Period 1 is labelled exactly when its level-1 rows tie to a stored year (N of N); S1-S4 PASS; R79 CC2 AC2 SERVED: YES; and exit=0
- **AC3** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc2.py" --crit AC3 --where local; echo "exit=$?"`
  Expect: the plant tests of the reader, the period labels and the filing-text breakdown pass; B1 PASS; R79 CC2 AC3 SERVED: YES; and exit=0

### 4. THE BASE DRY-RUN
```
AC1 (base, HEAD c92e860791):
FAIL C0 lib.research.api.segment_served imports cannot import name 'segment_served' from 'lib.research.api' (C:\Users\Opal Bloomberg\Desktop\ajb_workspace\lib\research\api\__init__.py)
R79 CC2 AC1 SERVED: NO
exit=1      -> FAIL as expected (build: the module does not exist)

AC2 (base):
FAIL C0 lib.research.api.segment_served imports cannot import name 'segment_served' from 'lib.research.api' (C:\Users\Opal Bloomberg\Desktop\ajb_workspace\lib\research\api\__init__.py)
R79 CC2 AC2 SERVED: NO
exit=1      -> FAIL as expected (build: the module does not exist)

AC3 (base):
   35 passed, 6 warnings in 0.32s
PASS B1 the plant tests of the reader, the period labels and the filing-text breakdown pass rc=0
R79 CC2 AC3 SERVED: YES
exit=0      -> PASS as expected (bound)

REACHABLE (the same check file, with a scratch stub outside the repo placed in memory under the module's name; no product file written;
the two period entries of F2 shortened with "..." here, the rest literal):
AC1 (stub):
PASS F1 a column that ties is labelled with its fiscal year; currency and units stated; rows unchanged P1 {'period': 1, 'label': 'Fiscal year 2025', 'fiscal_year': '2025', 'top_level_sum': 14.0, 'note': None}; currency 'EUR' units 'millions'
PASS F2 a column that ties to no year, and a column with no figure, are not labelled and each says why P3 {... 'top_level_sum': 10.0, 'note': "The rows of this column do not add up to the company's reported revenue for any year we hold, so the year is not stated."}; P5 {... 'top_level_sum': None, 'note': 'No top-level row carries a figure in this column.'}
PASS F3 with no figures the table is still served, no column labelled, no currency, no units period note "We hold no reported revenue for this company to name these columns from, so they keep Bloomberg's own period numbers."
PASS F4 nothing to show reads a plain reason and never raises raised None; reasons ['No Bloomberg segment table has been stored for this name yet.', 'The Bloomberg segment table for this name could not be read just now.']
PASS F5 every answer carries exactly the ten keys and every period entry its five answers 8, off-shape [] []
PASS F6 no served sentence uses a system word sentences read 50, words used []
PASS F7 the store is read only through read_segment_table, once, with the client handed in; arguments unchanged imports ['__future__', 'lib']; store calls in the source []; reader calls 1
R79 CC2 AC1 SERVED: YES   exit=0
AC2 (stub, 66 seconds):
PASS S1 AMD serves its revenue rows with Period 1 labelled fiscal year 2025 in millions of USD rows 6; P1 label 'Fiscal year 2025' sum 34639.0; currency 'USD' units 'millions'
PASS S2 a name whose Period 1 ties to no stored year serves its rows with Period 1 unlabelled and a plain note 8766_JP_Equity rows 6; P1 label 'Period 1' sum 8336718.0 note "The rows of this column do not add up to the company's reported revenue for any year we hold, so the year is not stated."
   never stored: 'No Bloomberg segment table has been stored for this name yet.'
   stored, no revenue lines: "Bloomberg's stored table for this name has no revenue by business line."
PASS S3 a name with no stored table and a stored name with no revenue lines each read their own plain reason
   stored names 85; serving revenue rows 76; Period 1 labelled 72; Period 1 unlabelled 4 ['8766_JP_Equity', 'AMXB_MM_Equity', 'RIO_LN_Equity', 'SAN_FP_Equity']; e.g. wrong []
PASS S4 every stored name is served, and its Period 1 is labelled exactly when its level-1 rows tie to a stored year 85 of 85
R79 CC2 AC2 SERVED: YES   exit=0
```

### 5. `<paths>`
```
lib/research/api/segment_served.py
lib/research/api/tests/test_segment_served.py
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and class
`LOCAL` (a new module and its tests; it reads the store through an existing reader and writes nothing). `worker`: about 110
product lines and a test file.

### 7. Edges
None inbound: it does not wait on A1 (it calls the reader by name; AC2 reads 85 of 85 with the reader as it stands, since no
stored folder is deeper than five). Outbound: the adapter cell is cut AFTER this cell drains and makes the one hookup of
section 8; the redeploy follows the adapter cell and its deploy pair names that hookup.

### 8. Not measured, and questions for the issuer
**THE HOOKUP the adapter cell must make (the only edit to `lib/research/api/scoped_amgt.py` this group needs):**
- Where: in `read_thesis_bundle` (`scoped_amgt.py:3629` at HEAD `c92e860791`), directly after the line
  `bundle["segment_breakdown"] = read_segment_breakdown(resolved_key or security_key)` (`:3739`) and before the statement of
  inputs is built (`:3746`).
- What, two lines:
  `from lib.research.api import segment_served` (inside the function, the way `section_coverage` is imported at `:3741`), then
  `bundle["segment_table"] = segment_served.serve_segment_table(resolved_key or security_key, fiscal_year_figures, header_figures, client=_pool_client())`
- Values already in hand there: `resolved_key` (`:3648`) and the asked-for `security_key`; `fiscal_year_figures` (`:3659`,
  `model["fiscal_year_figures"]`, the stored fiscal-year list); `header_figures` (`:3650`, the STORED header list, not the
  plain-country copy served at `:3673`; either holds the currency entry); `_pool_client` (`:2155`), the seam every other read
  of the bundle uses, which offers the two calls the reader makes.
- Served key: `segment_table`, NEW, beside `segment_breakdown`. The filing-text `segment_breakdown` stays as it is.
- What a deployed check should read on `/thesis` for AMD US to prove it: `segment_table.status == "served"`;
  `segment_table.rows` holds 6 rows, the first `{"segment": "Data Center", "level": 1}` with first value 16635.0;
  `segment_table.periods[0].fiscal_year == "2025"`, `.label == "Fiscal year 2025"`, `.top_level_sum == 34639.0`,
  `.note == null`; `segment_table.currency == "USD"`; `segment_table.units == "millions"`;
  `segment_table.source.object` ends `security_key=AMD_US_Equity/20261007T115113Z.json`. A deployed answer of
  `status "none"` with the reason "The Bloomberg segment table for this name could not be read just now." means the function
  could not read the folder (see the grant below), not that nothing is stored.

**Not measured:**
- **The deployed function's grant on the segments folder.** `infra/aws/terraform/harvest/scoped-amgt-api.tf:176` lists the
  prefix `bloomberg/harvest/bronze/` (DESIRED); the applied policy was not read. The reader swallows a denied read into its
  read-failed sentence, so only the deployed check above tells the two apart.
- **The deployed package's closure.** `segment_table.py` imports `lib.research.harvest.store` at its top, which imports
  `pyarrow` and `lib.opal_naming`. The build script says it already packages both for the timeline loaders; that a cold
  import of `segment_served` works inside the package was not exercised (the redeploy's import check answers it). The
  function-scope import above keeps that import off the cold start of every other route; its cost on the first `/thesis` was
  not timed.
- The added time on `/thesis`: one listing and one body per name from this box, median 103 ms; not timed from the function.
- The page. This group serves a key on the route. Nothing on the Security Analysis page draws `segment_table` yet, so FWD-1
  does not move on the walk until a page cell draws it. No page file was read.
- Whether the operating income table shares the revenue table's columns. The column names are computed from the revenue
  rows and are served once, for both tables; no operating income sum was tied to a stored figure.
- A tie by coincidence, the fiscal year's end date, and why the 4 names do not tie on Period 1: as left open in
  `round78/reads/SEGMENT_PERIOD_LABEL_READ.md`.
- CTO msg 31077 was read only as it is restated in `round78/GROUP_D_NOTES.md` cell D4 and the bb-21 order; the message body
  itself was not read.

**Questions and observations for the issuer:**
1. **`units` is a field this draft ADDS** beyond "period and currency labels". Without it AMD reads "34,639 USD". The unit is
   the stored unit of the tied revenue figure (`MILLIONS` on 76 of 76), stated only where a column ties, by the same
   reasoning as the currency. Strike rule 6's second sentence, the `units` key and check clauses F1/S1's units test if the
   CTO's ruling is read as currency only.
2. **The currency is stated for the whole table when ANY column ties** (the built `label_periods` rule). So the 4 names
   whose Period 1 is unlabelled still state a currency, from a later column. That is the built rule, not a new one.
3. **A revenue figure now carries its own `currency` field** (`"currency": "USD", "currency_basis": "reporting
   (EQY_FUND_CRNCY)"` on AMD), which the round-78 read said it did not. It equals the header currency on 76 of 76 tied
   names, so the header source ruled by the CTO and the row's own field agree today. This draft uses the header, as ruled.
4. **One phrase, two things.** `lib/research/api/inputs_statement.py:33` calls the filing-text breakdown "the segment table"
   in the served statement of inputs. Once a Bloomberg table is served under the key `segment_table`, that phrase names the
   other block. It is not this group's to change; it sits with the page findings of ruling R3.
5. An operating-income-only name (4 today) is served `status "none"` with its operating income rows and five unnamed
   columns. Whether the page draws those rows is the page cell's call.
6. A2's AC2 takes about 66 seconds from this box (85 names, three reads each). The order's timeout of 900 covers it.
