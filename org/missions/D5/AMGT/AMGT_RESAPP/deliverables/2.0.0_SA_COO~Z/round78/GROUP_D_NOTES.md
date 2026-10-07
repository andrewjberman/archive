# AMGT_RESAPP round 78 -- GROUP D: the issuer's own four cells (bb-16, bb-17, bb-20, bb-21)

Drafted by `2.0.0_SA_COO~Z`, 2026-10-07 ~15:3xZ. Each check was written as a file and run at the base by this seat; the outputs
are quoted under each cell. The seat order (bb-18, the redeploy) and the walk (bb-19) are written by hand as order files.

---

## D1 -- `AMGT-bb-16` -- THE SEEKING ALPHA LAST-READ READER OVER THE COLLECTOR'S JOB RECORDS (row AMGT_RESAPP-Z-S367)

### 1. MEASURED AT THE BASE
- `FRESHNESS_COLUMN_READERS_READ_20261007.md` (@b824708cf4) and row Z-S367 (@450b5c1d99): the freshness reader takes a name's
  Seeking Alpha date from four per-security tables that hold 3 partitions (BABA, BA, COST), all 2026-09-11; the collector writes
  elsewhere. 3 false stale rows and 92 false "not collected" cells: 95 of 95 wrong.
- The contract file is `lib/research/freshness/seeking_alpha_job_record.schema.json` (@25ebedb3a3). No object exists under the
  record's address yet: the collector's half is AMGT_HARVST's cell.

### 2. THE ACT (worker face text)

The freshness page's "Seeking Alpha last read" is wrong for every covered company: it reads tables the collector stopped writing
in September. The collector will write one small record per finished job. Build the reader of those records. It is a pure
module: it reads no store. Another cell connects it to the page.

Read `lib/research/freshness/seeking_alpha_job_record.schema.json` first. It is the ONE contract, shared with the team that
writes the records. Do not edit it.

Create `lib/research/freshness/collector_record.py` (standard library only) exporting:

`REQUIRED_FIELDS`: a tuple equal to the schema's `required` list.

`parse_record(obj)` returns a clean dict of the record's fields, or `None` when `obj` does not match the contract.
1. It matches when every required field is present, `schema_version` is 1, `security_key` is text ending `_Equity`,
   `finished_at` is text shaped `YYYY-MM-DDTHH:MM:SSZ`, `status` is non-empty text, `stored` is a whole number of 0 or more
   (a true/false value is not a number), and `newest_article_stored_at` is either `None` or text of the same time shape.
2. Extra keys are allowed and are dropped from the returned dict, except `run_id`, which is kept when it is text.

`partition_for(security_key)` returns the folder name the records of that company sit under.
3. Use `lib.research.identity.crosswalk.security_key_partition`, the same function the freshness view already uses, so a name
   with a slash in it (`BP/_LN_Equity`) gets the slash-safe folder (`security_key=BP-SLASH-_LN_Equity`).

`seeking_alpha_state(records, pilot_stamp=None)` returns
`{"state", "last_read", "newest_job_finished_at", "newest_job_status", "stored_by_newest_job", "records", "rejected", "sentence"}`.
`records` is a list of objects as read from the store (dicts); `pilot_stamp` is the September pilot object's stamp when the
caller has one.
4. Run every object through `parse_record`. `records` is the count that parsed, `rejected` the count that did not.
5. The newest job is the parsed record with the greatest `finished_at`: its end time, status and stored count fill
   `newest_job_finished_at`, `newest_job_status`, `stored_by_newest_job`.
6. `last_read` is the greatest `newest_article_stored_at` across the parsed records, ignoring `None`.
7. `state` is `"read"` when `last_read` is set. `sentence`: "Seeking Alpha last read <date>." with the date as YYYY-MM-DD.
8. `state` is `"checked"` when one or more records parsed and none holds an article time. `sentence`: "Seeking Alpha was
   checked on <date of the newest job> and no article is held for this company." `last_read` stays `None`.
9. `state` is `"no_record"` when no record parsed. `sentence`: "No Seeking Alpha collection record is held for this company
   yet." `last_read` stays `None`.
10. **`pilot_stamp` never becomes a date and never changes the state.** It is accepted so the caller can hand it in; the
    function ignores it. The words "not collected" appear in no sentence this function returns: an empty folder is not
    evidence that nothing was collected.
11. No sentence uses: identity, unresolved, security key, crosswalk, dossier, landed, model block, estate, stage, input
    ledger, bronze.
12. The function does not change its arguments.

Plant tests in `lib/research/freshness/tests/test_collector_record.py`: one case per rule 1 clause, rules 5 to 10, and the two
examples inside the schema file.

You do NOT edit `lib/research/api/scoped_amgt.py`, `lib/research/freshness/build_view.py` or the schema file. Your report
names the hookup: where the served freshness reader would list the records (one listing of the records' prefix, grouped by
folder) and call `seeking_alpha_state`, and which served fields it would replace.

### 3. THE CRITERIA
- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb16.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: a record with a stored article reads as read and is dated by its newest article; two records give the greatest article time and the greatest end time; records with no article read as checked with no date; no record reads no_record and never not collected; an object off the contract is counted and not used; the pilot stamp is not a date; C1-C6 PASS; R78 BB16 AC1 SERVED: YES; and exit=0
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb16.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: the module's required fields equal the schema's; both schema examples parse (2 of 2); a slash name's folder is the slash-safe one; S1-S3 PASS; R78 BB16 AC2 SERVED: YES; and exit=0

### 4. THE BASE DRY-RUN
```
AC1: FAIL C0 lib.research.freshness.collector_record imports cannot import name 'collector_record' ...  R78 BB16 AC1 SERVED: NO  exit=1  -> FAIL as expected (build)
AC2: FAIL C0 lib.research.freshness.collector_record imports cannot import name 'collector_record' ...  R78 BB16 AC2 SERVED: NO  exit=1  -> FAIL as expected (build)
```

### 5. `<paths>`
```
lib/research/freshness/collector_record.py
lib/research/freshness/tests/test_collector_record.py
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and class
`LOCAL`; `worker-light`.

### 7. Edges
None inbound. Outbound: its hookup is NOT in this round's adapter cell. The CTO ruled it deploys only when the collector's
records are present for the reached names (rulings file @f97be3fd6f, C2).

### 8. Not measured, and questions for the issuer
None beyond the column read.

---

## D2 -- `AMGT-bb-17` -- THE ADAPTER CELL: EVERY HOOKUP OF THE ROUND IN `scoped_amgt.py`

### 1. MEASURED AT THE BASE
`r78_bb17.py --crit AC1 --where local` at the base: H1 to H5 FAIL (no hookup is made) and H6 FAILS with 2 wrong rows of 60 read
(`2317_TT_Equity` peer `688910` and `PBR_US_Equity` peer `268236`, each served "USD" from a United States record behind a foreign
price). AC2 (the round-77 served shape on the tree) PASSES.

### 2. THE ACT (worker face text)

Six cells of this round each built a new module and named a hookup. You make every hookup. You are the ONLY writer of
`lib/research/api/scoped_amgt.py` this round. Each module is already merged into your worktree's base: read each module and
its tests before you call it. Each hookup below gives the function, the place by line number as measured at the cut, and the
effect; line numbers may have moved by a few lines, so find the named function.

1. **The coverage marker** (`lib/research/api/coverage_marker.py`, `marker(security_key, covered_keys)`). Where the overlay
   bundle and the thesis bundle are assembled (near `:3467` and `:3629`), add the key `research_coverage` holding the marker for
   the requested company, with `covered_keys` from `covered_security_keys()` as the adapter already reads it. A company outside
   the covered set then says so in ONE place.
2. **The country** (`lib/research/api/country_name.py`, `with_plain_country(header_figures)`). In `read_security_overlay`
   (near `:3472`) and `read_thesis_bundle` (near `:3632`), serve `"header_figures": country_name.with_plain_country(header_figures)`
   AFTER the figure checks have been computed from the stored list, so no check result moves.
3. **The one statement of inputs** (`lib/research/api/inputs_statement.py`, `statement(input_provenance, thesis)`). In
   `read_thesis_bundle`, after `passage_coverage` is set (near `:3700`), set
   `bundle["input_provenance"] = inputs_statement.statement(_overlay_input_provenance(resolved_key), bundle)`. On the overlay
   (near `:3495`) serve the SAME statement under the same key; the overlay does not hold the thesis parts, so pass `None` for
   `thesis` there ONLY if reading the thesis would add a store read to the overlay's first paint, and say in your report which
   you did and what it costs. Do not remove the `/ledger` route or the overlay's `provenance` block.
4. **The officer rank** (`lib/research/management/officer_rank.py`, `rank_officers(officers)`). At the top of
   `_serve_management_document` (near `:4553`), the one place every served roster passes:
   `officers = officer_rank.rank_officers(officers)`. Same rows, reordered; every count on the block is unchanged.
5. **The source names** (`lib/research/api/source_names.py`). `read_feed`: pass `items` through `with_publisher_names` and add a
   `source_name` beside `source` (near `:5316` and `:5346`). `_overlay_provenance`: a `source_name` on each of its three entries
   (near `:3290`). `_compose_ledger_provenance`: a `source_name` on the News class and on a Filings class that has a source
   (near `:6015` and `:6026`). Each is ADDED beside the raw text; the raw `source` values do not change.
6. **The peer price's own listing** (`lib/research/peers/price_listing.py`, `record_for_price(member, resolve)`). In
   `_with_price_currency` (near `:2371`), the record asked for a row's currency becomes
   `price_listing.record_for_price(m, _resolve_held_form)["record_key"]` in place of `price_currency.member_record_key(m)`. A row
   whose answer carries a `reason` is served `price_currency_reason` equal to that reason and NO `price_currency`.

NOT in this cell, and not to be wired by you: the segment table (`segment_table.py`), the segment period labels
(`segment_period.py`), the Seeking Alpha record reader (`collector_record.py`), the slash-safe officers reader (it needs no
hookup) and the Peers V reason (it needs none). Their serving waits on rulings outside this cell.

Run `lib/research/api/tests/` before your commit and report its last line.

### 3. THE CRITERIA
- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb17.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: a covered name reads covered and a pool name outside coverage says so once; the country reads in plain case with the stored text beside it; the thesis carries one statement of inputs with one filings row before the pack row; a chief-executive row leads every sampled roster that holds one; every provenance entry carries a source name key; no sampled peer row is served a United States record's currency behind a foreign price; H1-H6 PASS; R78 BB17 AC1 SERVED: YES; and exit=0
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb17.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: the round-77 served shape still reads YES on the tree; B1 PASS; R78 BB17 AC2 SERVED: YES; and exit=0

### 4. THE BASE DRY-RUN
```
AC1: H1-H5 FAIL; FAIL H6 ... rows read 60, wrong 2 [('2317_TT_Equity', '688910', 'TSM_US_Equity', 'USD'), ('PBR_US_Equity', '268236', ...)]
     R78 BB17 AC1 SERVED: NO   exit=1   -> FAIL as expected (build)
AC2: PASS B1 the round-77 served shape still reads YES on the tree rc=0 R77 SERVED SHAPE: YES
     R78 BB17 AC2 SERVED: YES  exit=0   -> PASS as expected (bound)
```

### 5. `<paths>`
```
lib/research/api/scoped_amgt.py
lib/research/api/tests/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and class
`LOCAL` (it edits no `.tf` and no route list this round); `worker`.

### 7. Edges
After bb-2, bb-3, bb-8, bb-9, bb-10 and bb-11 drain. Before the redeploy (bb-18).

### 8. Not measured, and questions for the issuer
The cost of the statement on the overlay's first paint (hookup 3) is not timed; the worker reports it.

---

## D3 -- `AMGT-bb-20` -- THE LINE-ENDING CELL: NINE FILES RE-COMMITTED WITH LF ENDINGS (row AMGT_RESAPP-Z-S362, ruling 12 as amended)

### 1. MEASURED AT THE BASE
`git ls-files --eol`, 2026-10-07: 45 tracked files carry CR in the index under `eol=lf` (41 `.py`, 4 `.tf`), the count of row
Z-S362. 34 of the 41 `.py` fail `.tools/commit-gate.sh` as they stand; 7 of the 45 sit under `infra/aws/lambda/`. The CTO ruled
(rulings file @f97be3fd6f, C1): land the `.py` that pass the gate and the `.tf`, excluding ANY file under `infra/aws/lambda/`,
with no gate override. That is 9 files: `HYGIENE_LANDABLE_FILES_20261007.txt`.

### 2. THE ACT (worker face text)

Nine tracked files carry Windows line endings in git while their own attribute says they must carry Unix ones, so `git status`
calls them modified or clean depending on a cache, not on their content. Re-commit those nine with Unix line endings, and
change nothing else.

The nine are listed, one per line, in
`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/HYGIENE_LANDABLE_FILES_20261007.txt`. Read it; it is your
whole write set under `data/` and `infra/`.

1. For each listed file, make the committed bytes equal the bytes at the base with every carriage return removed, and nothing
   else: `git add --renormalize -- <file>` does this for a file whose attribute says `eol=lf`. Check with `git ls-files --eol
   -- <file>` that it then reads `i/lf`.
2. Commit the nine in ONE commit through `.tools/safe-commit.sh` (the commit gate runs on the `.py` files; each of the six
   `.py` passed it at the cut).
3. **Touch no other file under `data/smartx/` or `infra/aws/`.** 36 more files have the same defect and are NOT yours: 34 fail
   the commit gate as they stand, and every file under `infra/aws/lambda/` is a function's source, whose package would change
   at its next deploy. If `git status` shows any of them modified after your commit, leave them and say so.
4. **Apply nothing.** No `terraform` command, no deploy, no upload. The three `.tf` files change only their line endings.
5. Print in your report: the nine files with `i/lf`, and the count still reading `i/crlf` under `eol=lf` in the whole
   repository (expected 36), from one `git ls-files --eol` pass.

### 3. THE CRITERIA
- **AC1** `cd "$(git rev-parse --show-toplevel)" && python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb20.py" --crit AC1; echo "exit=$?"`
  Expect: the list holds 9 files and none is a Lambda source; every listed file reads i/lf in the index (9 of 9); C0-C1 PASS; R78 BB20 AC1 SERVED: YES; and exit=0
- **AC2** `cd "$(git rev-parse --show-toplevel)" && python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb20.py" --crit AC2; echo "exit=$?"`
  Expect: with carriage returns removed, every listed file equals its bytes at the base (9 of 9); R78 BB20 AC2 SERVED: YES; and exit=0
- **AC3** `cd "$(git rev-parse --show-toplevel)" && python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb20.py" --crit AC3; echo "exit=$?"`
  Expect: nothing else under data/smartx or infra/aws changed since the base; R78 BB20 AC3 SERVED: YES; and exit=0

### 4. THE BASE DRY-RUN
```
AC1: FAIL C1 every listed file reads i/lf in the index 0 of 9   R78 BB20 AC1 SERVED: NO   exit=1  -> FAIL as expected (build)
AC2: PASS C1 with CR removed, every listed file equals its bytes at the base 9 of 9       exit=0  -> PASS as expected (bound)
AC3: PASS C1 nothing else under data/smartx or infra/aws changed since the base           exit=0  -> PASS as expected (bound)
```

### 5. `<paths>`
```
data/smartx/scripts/check_packages.py
data/smartx/scripts/lambda_smartx_query.py
infra/aws/connection_pool/__init__.py
infra/aws/ec2/smartx-exporter/smartx-workspace/scripts/check_packages.py
infra/aws/ec2/smartx-exporter/smartx-workspace/scripts/lambda_smartx_query.py
infra/aws/scripts/create_causality_v2_tables.py
infra/aws/terraform/nfra-agentbus-alyssa01/iam.tf
infra/aws/terraform/nfra-agentbus-alyssa01/main.tf
infra/aws/terraform/seeking-alpha/main.tf
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and class
`WORLD` by the path floor only (it names `.tf` files and applies nothing); `worker-light`.

### 7. Edges
None.

### 8. Not measured, and questions for the issuer
Whether the pre-push deploy gate treats a line-ending change to `data/smartx/scripts/*.py` as a script to upload was not
exercised; the issuer reads the push gate's output at the next push by `0.0.0_AB_MSTR~Z`.

---

## D4 -- `AMGT-bb-21` -- THE SEGMENT TABLE'S PERIOD AND CURRENCY, LABELLED ONLY WHERE THEY TIE TO STORED REVENUE (CTO ruling msg 31077)

### 1. MEASURED AT THE BASE
- The third AMD probe (`round77/BA21_SEGMENTS_ACT_RECORD_20261007.md` ADDENDUM 2): `SALES_REV_TURN` 34,639 equals the sum of
  Period 1's level-1 revenue rows; Period 1 is the fiscal year ended 12/2025 in USD.
- `reads/SEGMENT_PERIOD_LABEL_READ.md` (a read with no Bloomberg call, today): over the 76 names with revenue rows, Period 1's
  level-1 sum equals a stored fiscal year's revenue on **72**, does not on **4**, and no name lacks stored revenue (0). All 72
  matched the NEWEST stored year (62 on 2025, 10 on 2026). The next column back ties to the prior stored year on 71 of the 72;
  the one that does not is AMD (16,136 against 25,785, two of four level-1 rows present). The stored figures are in millions;
  the reporting currency is the stored `EQY_FUND_CRNCY` figure, present on 76 of 76.

### 2. THE ACT (worker face text)

The stored segment table of a company has five columns named only "Period 1" to "Period 5", and no currency. A careful reader
cannot tell which year a column is. For most companies the column can be named from figures we already hold: when the level-1
rows of a column add up to the company's stored revenue for a fiscal year, that column is that fiscal year. Build the function
that names a column ONLY where that tie holds. It is a pure module: it reads no store.

Create `lib/research/api/segment_period.py` (standard library only) exporting ONE function:

`label_periods(period_sums, revenue_by_year, currency)` returns `{"periods": [...], "currency": <text or None>, "reason": <text or None>}`.
- `period_sums` maps a column number (1 to 5) to the sum of that column's level-1 rows, or `None` when no level-1 row carries
  a value in that column.
- `revenue_by_year` maps a fiscal-year label as stored (text such as "2025") to the stored revenue for that year, in the same
  units as the table.
- `currency` is the company's stored reporting currency (text such as "USD"), or `None`.

Rules:
1. Work through the columns in number order. A column TIES to a year when its sum is a number, the year's revenue is a number
   above zero, and the two differ by 0.5 percent of the revenue or less.
2. When a column ties to more than one year, take the year whose revenue is closest. A year already given to an earlier column
   is not given again: one stored year names one column.
3. Each entry of `periods` is `{"period": <n>, "fiscal_year": <year text or None>, "sum": <the sum or None>, "reason": <text or None>}`,
   one per key of `period_sums`, in number order.
4. A column that ties carries its `fiscal_year` and `reason: None`.
5. A column with a sum that ties to no year carries `fiscal_year: None` and this reason: "The rows of this column do not add up
   to the company's reported revenue for any year we hold, so the year is not stated."
6. A column with no sum carries `fiscal_year: None` and this reason: "No top-level row carries a figure in this column."
7. **Never name a column from its neighbour.** A column that does not tie is not given the year before or after a column that
   does.
8. `currency` in the result is the `currency` handed in when one or more columns tie, and `None` otherwise: the currency is
   stated only when a tie shows the table is in the units of the stored figures.
9. When `revenue_by_year` is empty: every column is unlabelled, `currency` is `None`, and the top-level `reason` is "We hold no
   reported revenue for this company to name these columns from." Otherwise the top-level `reason` is `None`.
10. No sentence uses: identity, unresolved, security key, crosswalk, dossier, landed, model block, estate, stage, input ledger,
    bronze.
11. The function reads nothing, calls nothing and does not change its arguments.

Plant tests in `lib/research/api/tests/test_segment_period.py`: a tie, a near miss just outside 0.5 percent, a column with no
sum, the two-columns-one-year case of rule 2, an empty `revenue_by_year`, and a `None` currency with a tie.

You do NOT edit `lib/research/api/scoped_amgt.py` or `lib/research/api/segment_table.py`. Your report names the hookup: the
level-1 sums come from the segment table another cell builds (`segment_table.read_segment_table`), the revenue by year from the
company's stored fiscal-year figures (`SALES_REV_TURN`, scope `fiscal_year_line_item`) and the currency from the stored header
figure `EQY_FUND_CRNCY`; say exactly where each is already in hand when `/thesis` is assembled.

### 3. THE CRITERIA
- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb21.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: a column that ties is labelled with its fiscal year and the currency is stated; a column that ties to no stored year is not labelled and says why; a column with no sum is not labelled; with no stored revenue nothing is labelled; one stored year is given to one column only; no served sentence uses a system word; C1-C6 PASS; R78 BB21 AC1 SERVED: YES; and exit=0
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb21.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: AMD's Period 1, summed from the newest stored segment table that carries revenue rows and set against the stored revenue figures, reads fiscal year 2025 in USD; S1 PASS; R78 BB21 AC2 SERVED: YES; and exit=0

### 4. THE BASE DRY-RUN
```
AC1: FAIL C0 lib.research.api.segment_period imports ...   R78 BB21 AC1 SERVED: NO   exit=1  -> FAIL as expected (build)
AC2: FAIL C0 lib.research.api.segment_period imports ...   R78 BB21 AC2 SERVED: NO   exit=1  -> FAIL as expected (build)
```

### 5. `<paths>`
```
lib/research/api/segment_period.py
lib/research/api/tests/test_segment_period.py
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and class
`LOCAL`; `worker-light`.

### 7. Edges
None inbound. Outbound: with bb-1 it feeds the segment table's hookup, which is cut after the CTO reads this round's result.

### 8. Not measured, and questions for the issuer
The 4 names that do not tie (8766 JP, SAN FP, AMXB MM, RIO LN) read unlabelled in Period 1 under this rule; three of them have
no Period 1 figure at all.

---

## D5 -- `AMGT-bb-22` -- THE DIVERGENCE SCORE READS THE DISPERSION FIELDS BLOOMBERG SERVES (AMGT_CORPUS probe, msg 31085)

### 1. MEASURED AT THE BASE
- AMGT_CORPUS's probe, 2026-10-07 15:17Z, one name (BA US), evidence
  `org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/evidence/r40_ap10_probe_BA_20261007.txt` @e3579e3693: Bloomberg
  refuses `BEST_CPS_STANDARD_DEV`, `BEST_CPS_AVG`, `BEST_EPS_STANDARD_DEV`, `BEST_EPS_AVG` as invalid fields and returns
  `BEST_CPS_STDDEV`, `BEST_EPS_STDDEV`, `BEST_CPS_NUMEST`, `BEST_EPS_NUMEST`.
- `lib/research/scores/divergence.py:64-65` names the four refused fields; `run_scores.py:210,225` reads the two tuples, so it
  follows them. The refused names also sit in `lib/research/scores/tests/test_house_fcf.py` and
  `lib/research/api/tests/test_score_modules.py`.

### 2. THE ACT (worker face text)

The divergence score asks for six Bloomberg fields about how far analysts disagree. A probe today showed Bloomberg does not
have four of them under the names our code uses, so the score can never be fed. Change the code to the names Bloomberg serves.

In `lib/research/scores/divergence.py`:
1. `CFPS_FIELDS` becomes `("BEST_CPS_STDDEV", "BEST_CPS", "BEST_CPS_NUMEST")`.
2. `EPS_FIELDS` becomes `("BEST_EPS_STDDEV", "BEST_EPS", "BEST_EPS_NUMEST")`.
3. The order inside each tuple keeps its meaning: standard deviation, then the consensus mean, then the number of estimates.
   Every use in the module reads the tuples by position; change no arithmetic and no guard.
4. Correct the module's opening text where it names the old fields, and say there that the mean is the consensus estimate
   field itself (`BEST_CPS`, `BEST_EPS`).

In `lib/research/scores/tests/test_house_fcf.py` and `lib/research/api/tests/test_score_modules.py`: rename the same four keys
in the test rows. Change no expected number.

Do not edit `lib/research/scores/run_scores.py`: it reads the two tuples and follows them. Do not run it: a store write is the
issuer's act. If any other `.py` under `lib/research/scores/` carries one of the four old names, rename it there and say so.

### 3. THE CRITERIA
- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb22.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: the two field lists are the served names; no refused name remains in the score modules or the two test files; C1-C2 PASS; R78 BB22 AC1 SERVED: YES; and exit=0
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb22.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: the score tests pass; B1 PASS; R78 BB22 AC2 SERVED: YES; and exit=0

### 4. THE BASE DRY-RUN
```
AC1: FAIL C1 ... ('BEST_CPS_STANDARD_DEV', 'BEST_CPS_AVG', 'BEST_CPS_NUMEST') ...; FAIL C2 files read 10, with a refused name 3   exit=1  -> FAIL as expected (build)
AC2: PASS B1 the score tests pass rc=0 87 passed   exit=0  -> PASS as expected (bound)
```

### 5. `<paths>`
```
lib/research/scores/divergence.py
lib/research/scores/tests/test_house_fcf.py
lib/research/api/tests/test_score_modules.py
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and class
`LOCAL`; `worker-light`.

### 7. Edges
None. The pull of the four served fields is AMGT_CORPUS's amendment; the score is fed when both have landed and the scores
producer next runs.

### 8. Not measured, and questions for the issuer
That `BEST_CPS` / `BEST_EPS` as stored carry the same period override as the standard deviation pulled beside them is
AMGT_CORPUS's to state in its amendment; this cell renames and does not pull.
