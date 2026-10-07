# AMGT_RESAPP round 78 -- GROUP A cell drafts (bb-1, bb-3, bb-4, bb-13)

Drafted for the issuer `2.0.0_SA_COO~Z`, 2026-10-07. Nothing here is built or committed. Every number below was measured
in this session unless a document is named. Base at the dry-run: `94b13244ed` (HEAD moved from `0c8ccd2a04` while this was
drafted; none of the files these cells name changed between the two).

Reads used, named once and cited by letter below:
- (R1) boto3 listing and get of every object under `s3://opal-data-harvest/bloomberg/harvest/bronze/segments/` (87 objects, 85 folders).
- (R2) the same for `.../bronze/exec_officers/` (93 objects, 91 folders), each newest object parsed on the first `",  "`.
- (R3) GET-shaped direct invokes of the deployed `opal-amgt-scoped-api`: `/freshness?view=page` (95 covered rows), then
  `/security/<key>/thesis` for each of the 95, block `management`.
- (R4) local Python at the base: `bloomberg_fallback`, `exec_roster_chain.run_chain`, `build_view`, `peers_v`, `table_class`.
- (R5) boto3 read of the newest object per name under `s3://opal-data-harvest/scores/v1/`.
- (R6) source read with the Read and Grep tools.

Each check was also run against a throwaway in-memory reference build (never written to the repo) to prove it CAN pass:
bb1 AC1 5 of 5 and AC2 5 of 5, bb3 AC1 3 of 3 and AC2 2 of 2, bb4 AC1 4 of 4, bb13 AC1 4 of 4. The slowest is bb1 AC1 at
about 22 seconds (the worker's limit is 120). All four scripts read `OK: pre-commit gate clean` from `.tools/commit-gate.sh`.

---

## A1 -- `AMGT-bb-1` THE SEGMENTS READER (ruling 3, FWD-1)

### 1. MEASURED AT THE BASE

| fact | value | read |
|---|---|---|
| folders / objects | 85 / 87. AMD US holds 3 (`113201Z`, `114801Z`, `115113Z`); every other name holds 1 | R1 |
| slash names | 2 folders: `BP-SLASH-_LN_Equity` (BP PLC, 4 revenue rows, 0 income rows), `NG-SLASH-_LN_Equity` (NATIONAL GRID PLC, 10 and 11) | R1 |
| body keys | `security`, `pulled_at`, `response` on 85 of 85 newest objects. `response` keys: `NAME` 85, `PG_REVENUE` 76, `PG_OPERATING_INCOME` 50. `__field_errors__` appears in 0 of the 85 newest objects | R1 |
| row keys | `Metric Name`, `Period 1 Value` .. `Period 5 Value`, `Product Geographic Hierarchy Level` on 1,882 of 1,882 rows (1,465 revenue, 417 income) | R1 |
| names with revenue rows | 76 of 85; rows per name min 1, median 8, max 255 (SAN FP) | R1 |
| names with NO revenue rows and no error | 9: `8306 JP`, `8316 JP`, `939 HK`, `BNP FP`, `HSBA LN`, `ISP IM`, `KOFUBL MM`, `UBSG SW`, `WALMEX* MM`. The key `PG_REVENUE` is absent from the response (not an empty list) | R1 |
| names with operating income | 50 of 85. Both tables: 46. Income and no revenue: 4 (`8316 JP`, `BNP FP`, `HSBA LN`, `ISP IM`). Neither: 5 | R1 |
| hierarchy levels | revenue: level 1 329 rows, 2 431, 3 349, 4 229, 5 127. Income: level 1 229, 2 98, 3 90. Always an integer | R1 |
| level-1 revenue rows per name | min 1, max 15; 8 of 76 names have exactly one; 2 names repeat a level-1 label (ICICIBC IN "general insurance", NOKIA FH "network infrastructure") | R1 |
| the missing-period marker | 2,564 of 9,410 value cells hold exactly `-2.4245362661989844e-14` (one distinct value), in 55 names. 0 nulls. 234 cells are an exact `0.0`, which is a different thing: AMD's "All Other" row holds both | R1 |
| rows with all five periods missing | 0. Revenue rows whose Period 1 is the marker: 444 of 1,465 (lines that no longer report) | R1 |
| indentation | 1,324 of 1,882 metric names start with non-breaking spaces: 3 (529 rows), 6 (439), 9 (229), 12 (127), that is 3 per level below the first. No ordinary leading space | R1 |
| other non-ASCII | 3 metric names, all TSM US (a micro sign in "0.15/0.18 um"-style labels). `roster.asciify` turns that into "0.15/0.18m", which changes the meaning | R1, R4 |
| fiscal period | NOT in the object. No key or text names a year for "Period 1"; the only date is `pulled_at` (2026-10-07T11:51:03Z to 11:52:24Z) | R1 |
| currency and units | NOT in the object. 0 matches for "crncy" or "currency" across the 85 newest objects | R1 |
| AMD's three objects | `113201Z` (458 B): `NAME` plus 3 refused fields, no table. `114801Z` (3,122 B): the table plus 4 refused fields. `115113Z` (2,622 B): the table, no refused field, 6 revenue rows. The newest is the good one today | R1 |
| income rows matched to revenue rows by name and level | 336 of 368 (level 1: 178 of 202); every income row matches in 29 of 46 names; 4 names repeat a (name, level) inside income | R1 |
| round-76 ruling 7 on this data | `table_class.segment_refusal` over each name's revenue rows (label as `segment`, empty `text`): refused 0 of 76, over all rows and over level-1 rows alone | R1, R4 |
| what serves segments today | `scoped_amgt.py:3696` sets `bundle["segment_breakdown"] = read_segment_breakdown(...)`, the filing's prose rows. Nothing reads the Bloomberg table | R6 |
| the freshness readers | `segments` is NOT in `build_view._BLOOMBERG_BRONZE_REQUESTS` (`build_view.py:73`) nor in `scoped_amgt._BLOOMBERG_BRONZE_REQUESTS` (`scoped_amgt.py:5435`): a segments pull does not move a name's Bloomberg date | R6 |

### 2. THE ACT (worker face text)

Build a reader of the stored Bloomberg segment table as a NEW module, `lib/research/api/segment_table.py`, exporting ONE function:

`read_segment_table(security_key, client=None)` returns a dict with exactly these keys:
`status` ("served" or "none"), `rows`, `operating_income_rows`, `periods`, `period_note`, `currency`, `currency_note`, `reason`, `source`.
A row is `{"segment": str, "level": int, "values": [five entries, each a float or None]}`.

1. **Where it reads.** One folder per name in bucket `opal-data-harvest`: `bloomberg/harvest/bronze/segments/` +
   `lib.research.harvest.store.entity_partition("security_key", security_key)` + `/`, objects named `<stamp>.json`. Build the
   folder ONLY through `entity_partition`: two stored names carry a slash and their folders are `security_key=BP-SLASH-_LN_Equity`
   and `security_key=NG-SLASH-_LN_Equity`. `security_key` arrives in the underscore form (`AMD_US_Equity`, `BP/_LN_Equity`).
   `client` is an S3 client; when None, build `boto3.client("s3", region_name="us-east-1")` inside the function. Use only
   `client.get_paginator("list_objects_v2").paginate(Bucket=..., Prefix=...)` and `client.get_object(Bucket=..., Key=...)`: the
   check and the adapter both pass a client that offers just those two.
2. **Which object.** Sort the folder's `.json` keys newest first (the stamp sorts as text). Take the first USABLE one, reading
   at most five. The body is `{"security", "pulled_at", "response"}`. An object is usable when `response["__field_errors__"]`
   has no entry for `PG_REVENUE` AND (the response carries `PG_REVENUE` or `PG_OPERATING_INCOME`, or it has no field errors
   at all). An object that holds only refused fields (a field probe) is skipped, even when it is the newest.
3. **Rows.** `response["PG_REVENUE"]` and `response["PG_OPERATING_INCOME"]` are lists of
   `{"Metric Name", "Period 1 Value" .. "Period 5 Value", "Product Geographic Hierarchy Level"}`. For each row:
   `segment` is the metric name with every non-breaking space (`chr(160)`) turned into a space, runs of space collapsed, ends
   stripped; change no other character. `level` is the hierarchy level as stored (1 is a top line; 2 to 5 are lines beneath
   it). `values` are periods 1 to 5 in order: None when the stored value is missing, is not a number, or is non-zero and
   smaller than 1e-9 in size (Bloomberg writes a missing period as about -2.4e-14); an exact 0.0 stays 0.0. Keep the stored
   row order. `rows` come from `PG_REVENUE`, `operating_income_rows` from `PG_OPERATING_INCOME`. Do NOT join the two tables by name.
4. **Periods and currency.** The stored object names neither a fiscal year nor a currency. Serve `periods` as
   `["Period 1", "Period 2", "Period 3", "Period 4", "Period 5"]`, `period_note` as one plain sentence saying these are
   Bloomberg's own period numbers and the stored table does not say which fiscal year each one is, `currency` as None, and
   `currency_note` as one plain sentence saying the stored table does not state its currency or its units. Never guess either.
5. **The share-capital and one-heading rule (round-76 ruling 7).** Before serving, hand
   `lib.research.filings.table_class.segment_refusal` the revenue rows as `[{"segment": <segment>, "text": ""}, ...]`. If it
   returns a sentence, serve `rows: []`, `operating_income_rows: []`, `status: "none"` and YOUR OWN reason, because that
   module's sentences say "the filing text kept here" and this table is not a filing: for
   `table_class.SEGMENT_CAPITAL_REASON` say the Bloomberg table lists share capital rather than business lines; for
   `table_class.SEGMENT_ONE_LABEL_REASON` say it repeats one heading rather than separate business lines. `table_class.py` is
   read, never edited. (On today's 76 stored tables it refuses none; your tests plant both cases.)
6. **Nothing to show, each with its own plain reason** (`status: "none"`, `rows: []`):
   no object in the folder ("No Bloomberg segment table has been stored for this name yet."); objects, none usable; a usable
   object with no revenue lines (9 stored names today; when it carries operating income lines, still serve those in
   `operating_income_rows`); no `security_key` given; a read that failed ("... could not be read just now"). The function
   NEVER raises: any exception becomes the read-failed reason.
7. **`source`** when an object was chosen: `{"vendor": "Bloomberg", "label": "Bloomberg product segments", "object": <the key
   read>, "pulled_at": <the body's pulled_at>, "company": <response NAME>}`; None when no object was chosen.
8. Every reason is in plain words. Do not use: identity, unresolved, security key, crosswalk, dossier, landed, model block,
   estate, stage, input ledger, bronze.

Plant tests in `lib/research/api/tests/test_segment_table.py` with a small fake client: a served table, the newer-probe case,
the marker and the true zero, the indent, both refusals, each of the five kinds of nothing, a slash name, a client that raises.

**You do NOT edit `lib/research/api/scoped_amgt.py`, `lib/research/filings/table_class.py` or `lib/research/harvest/store.py`.**
The hookup is the adapter cell's. Name it in your report: `segment_table.read_segment_table(key, client=_pool_client())`, called
where `/thesis` is assembled beside `read_segment_breakdown` (`scoped_amgt.py:3696`), served under a NEW key `segment_table`;
the filing-prose `segment_breakdown` stays as it is.

### 3. THE CRITERIA

- AC1: `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb1.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: AMD US serves clean revenue rows from the newest stored object that carries the table; BP/ LN serves rows; a stored name with no revenue lines and a never-stored name each read their own plain reason; every stored name reads as its newest usable object says (N of N); periods and currency are stated plainly with `currency` None; C1-C5 PASS; `R78 BB1 AC1 SERVED: YES`; and exit=0.
- AC2: same line with `--crit AC2`. Expect: a newer object of refused fields is not chosen; indent stripped, level kept, the marker None, a true zero kept; share-capital lines and one repeated heading refused with a reason that names no filing; a raising store reads a reason; a slash name is found; F1-F5 PASS; `R78 BB1 AC2 SERVED: YES`; and exit=0.
- AC3: same line with `--crit AC3`. Expect: every plant case in `test_segment_table.py` passes; `R78 BB1 AC3 SERVED: YES`; and exit=0.

### 4. THE BASE DRY-RUN (all three are BUILD checks; each FAILED as expected)

```
### AC1
FAIL C0 lib.research.api.segment_table imports cannot import name 'segment_table' from 'lib.research.api' (C:\Users\Opal Bloomberg\Desktop\ajb_workspace\lib\research\api\__init__.py)
R78 BB1 AC1 SERVED: NO
exit=1
### AC2
FAIL C0 lib.research.api.segment_table imports cannot import name 'segment_table' from 'lib.research.api' (C:\Users\Opal Bloomberg\Desktop\ajb_workspace\lib\research\api\__init__.py)
R78 BB1 AC2 SERVED: NO
exit=1
### AC3
FAIL C1 the plant test file exists lib/research/api/tests/test_segment_table.py
R78 BB1 AC3 SERVED: NO
exit=1
```

### 5. `<paths>`

```
lib/research/api/segment_table.py
lib/research/api/tests/test_segment_table.py
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~<n>/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```
Read-only neighbours named on the face, not in `<paths>`: `lib/research/harvest/store.py`, `lib/research/filings/table_class.py`.

### 6. Risk and worker class

`LOCAL` (a new module and its test; it reads the store and writes nothing). The served move is the adapter cell plus the
redeploy under its pair, as ruling 3 says. Worker class `worker` (the product module is likely over 100 lines).

### 7. Edges

None inbound. Outbound: the adapter cell (the `/thesis` hookup) and the redeploy drain after this cell.

### 8. Not measured, and questions for the issuer

1. **RULE NEEDED: period and currency.** Ruling 3 asks for "the period and the currency". The stored object carries neither.
   The draft serves Bloomberg's own period numbers with a plain note, and `currency` None with a plain note. Giving a fiscal
   year or a currency needs either a new Bloomberg field on a new pull (Andrew's word) or a join to another stored object.
   I did not measure whether any stored object states the table's currency or which year Period 1 is. AMD's Period 1 Data
   Center value (16,635) looks like a latest-year figure in millions of US dollars; that is a reading of one name, not a
   measurement.
2. **The 4 names with operating income and no revenue** (three banks and SMFG): the draft serves their income rows beside the
   "no revenue lines" reason. Ruling 3 says the 9 "read a plain reason"; rule whether income-only is shown or withheld.
3. **Which levels the page shows** is a page call (DSGN_AMGTV1). The reader serves every row with its level; 255 rows on SAN FP.
4. **Income is served as its own table**, not as a column: 32 of 368 income rows have no revenue row of the same name and level.
5. The share-capital rule is exercised only by planted rows (0 of 76 real tables trip it).
6. `segments` is in neither freshness reader's table list. Not chased; say if a segments pull should count as a Bloomberg read.
7. The module sits in `lib/research/api/` (beside `name_search.py`, already in the Lambda package) and imports
   `lib.research.harvest.store`, which imports pyarrow at the top; the build script packages pyarrow 16.1.0
   (`build-and-upload-scoped-amgt.sh:132`) and `bloomberg_fallback` already imports the same module in the function. I did not
   run the Lambda build's closure walk on a new file.

---

## A2 -- `AMGT-bb-3` THE OFFICER RANK (ruling 9)

### 1. MEASURED AT THE BASE

Ranks below are counted with the rule the cell states (rank 0 the company's chief executive, 1 its chief financial officer),
run as a scratch reference over the same data; the labelled table in `r78_bb3.py` is that rule's expected answers on 69 real titles.

| fact | value | read |
|---|---|---|
| stored Bloomberg lists | 91 folders, 93 objects (2 folders hold 2); 91 of 91 newest lists carry officers; 1,428 officer rows, 0 without a title | R2 |
| stored: a chief-executive row present | 88 of 91. NOT first in 15 (position 2 in 13, 3 in 1, 4 in 1). None in 3: `6861 JP` (one row, "President"), `939 HK` ("Chairman/Exec Dir", ...), `ICT PM` ("Chairman/President", ...). More than one in 5 (`2317 TT`, `ADBE US`, `HEI US`, `NFLX US`, `SPOT US`: co-chiefs or a handover) | R2 |
| stored: a CFO row present | 87 of 91 | R2 |
| stored: lists whose order the rank changes | 41 of 91 | R2 |
| served rosters | 93 of 95 covered names serve officers (the 2 that serve none are the slash names of bb-4). 84 are Bloomberg-sourced (82 through the request-time chain, 2 from a stored management object). 9 are not: 7 `roster_source: FILING` (BABA, BA, COST, HD, NU, SAP, VLO) and 2 with no source label (HAL, INTU) | R3 |
| served: chief executive not first | 17 of 93. Bloomberg-sourced 14 of 84. Not Bloomberg-sourced 3 of 9: BABA (position 2), HD (position 6), BA (position 7) | R3 |
| served: no chief-executive row | 2 of 93 (`939 HK`, `ICT PM`) | R3 |
| served: lists whose order the rank changes | 42 of 93 (39 Bloomberg-sourced, 3 not) | R3 |
| NKE US as stored and served | "Chairman", "President/CEO", ..., "Exec VP/CFO/Interim Controller" seventh | R2, R3 |
| Bloomberg title grammar | roles joined by `/`; `ROLE:UNIT` marks a unit or region ("CEO:North America", "Exec VP/CEO:Europe", "Chairman & CEO:BNP Paribas Fortis"); `:Group` is the whole company ("President/CEO:Group"); titles are cut at 50 characters (72 rows sit at exactly 50) | R2 |
| spellings met | 123 distinct titles (190 rows) contain "CEO" or "Chief Exec"; 38 distinct (94 rows) contain "CFO", "Chief Fin" or similar. Whole-company forms include "President/CEO/Executive Director", "Co-Chief Executive Officer", "Rotating Chief Executive Officer", "Interim CEO & Mng Dir", "Group CEO/Executive Director". Not the company's chief: "Regional Chief Executive", "Deputy CEO/Executive Director", "Head:Chief Executive Office Strategy & Sustainabil", "Deputy CFO", "CFO:EMEA" | R2 |
| filing title grammar | prose: "President and Chief Executive Officer, and a member of the Board", "Chair, and as our President and Chief Executive Officer", "Chairman of the Board, Chief Executive Officer and President"; a unit's chief reads "... Chief Executive Officer of Boeing Defense, Space & Security", "Chief Executive Officer, Alibaba E-commerce Business Group", "Brazil Chief Executive Officer", "Chief Growth Officer and US CEO"; and "Special Advisor to the CEO" | R3 |
| where one line covers every served roster | `scoped_amgt._serve_management_document` (`scoped_amgt.py:4553`, `officers = list(document.get("officers") or [])`) is the single serve path for a stored management object AND for the chain's roster. The served title field is `role` | R6 |

A first draft of the rule that excluded any title containing "Vice" misread "Executive Vice President and Chief Financial
Officer" on the filing rosters; the stated rule looks only at the word directly before the role.

### 2. THE ACT (worker face text)

Build the officer rank as a NEW module, `lib/research/management/officer_rank.py`, with two PURE functions (no store read, no
network, no import beyond `re`):

- `title_rank(title)` returns 0 for the company's chief executive, 1 for its chief financial officer, 2 for anyone else
  (including None, an empty title and a non-string).
- `rank_officers(officers, title_field="role")` returns a NEW list holding the SAME row objects: every rank-0 row, then every
  rank-1 row, then the rest, each group in the order given. It never drops, copies, edits or adds a row, never changes the
  input list, and ranking a ranked list changes nothing.

The rule reads the title text only. Titles come in two shapes: Bloomberg's ("President/CEO:Group/Rep Exec Officer", roles
joined by `/`, a unit after `:`) and a filing's prose ("Executive Vice President; President and Chief Executive Officer of
Boeing Defense, Space & Security").

1. Split the title on `/` and `;`. Judge each piece alone; the title has the rank of its best piece.
2. In a piece, text after a `:` names a unit. A piece with a `:` counts only when what follows is empty or is "Group",
   "Company" or "Corporation". Look for the role only in the text BEFORE the `:`.
3. A chief-executive mention is "CEO", "Co-CEO", "Chief Executive", "Chief Executive Officer", "Co-Chief Executive Officer"
   (any case, whole words). A chief-financial mention is "CFO", "Chief Financial Officer", "Chief Finance Officer", or
   "Chief Financial and <one word> Officer".
4. A mention counts only when what stands directly before it in the piece is nothing, a comma, or one of: and, &, Group,
   Global, Interim, Acting, Rotating, our. So "Deputy CEO", "Regional Chief Executive", "Brazil Chief Executive Officer",
   "US CEO", "Special Advisor to the CEO" and "Dpty CFO" do not count.
5. A mention does not count when it is followed by "of <a unit>" (but "of the Company", "of the Group" and "of the
   Corporation" are fine), or by a comma and then a unit's name. After a comma these openings are NOT a unit: and, a member,
   member, President, Chair..., Director, Founder, Co-Founder, Chief, Executive, Managing, Secretary, Treasurer.
6. Rank 0 wins over rank 1 when a title earns both.

Worked examples, all real titles. Rank 0: "Chairman/CEO", "President/CEO:Group", "Co-Chairman/Co-President/Co-CEO",
"Interim CEO & Mng Dir", "Vice Chairman/CEO", "Chairman of the Board, Chief Executive Officer and President", "President and
Chief Executive Officer, and a member of the Board". Rank 1: "Exec VP/CFO/Interim Controller", "Sr VP:Finance/CFO", "Senior
Managing Corporate Executive Offi/CFO:Group", "Executive Vice President and Chief Financial Officer". Rank 2: "Chairman",
"President", "Exec VP/CEO:Europe", "Chairman & CEO:BNP Paribas Fortis", "Head:Chief Executive Office Strategy & Sustainabil",
"Chief Executive Officer, Alibaba E-commerce Business Group", "CFO:EMEA", "Deputy CFO".

Plant tests in `lib/research/management/tests/test_officer_rank.py`: both title shapes, each exclusion, co-chiefs kept in
order, a roster with no chief executive left as given, the empty list, a missing title, `title_field="title"`.

**You do NOT edit `lib/research/api/scoped_amgt.py`, `lib/research/management/exec_roster_chain.py` or
`lib/research/management/bloomberg_fallback.py`.** The hookup is the adapter cell's. Name it in your report:
`officers = officer_rank.rank_officers(officers)` at the top of `scoped_amgt._serve_management_document`
(`scoped_amgt.py:4553`), the one place every served roster passes (a stored management object and the request-time
chain's filing or Bloomberg roster alike). It returns the same rows reordered, so every count on that block is unchanged.

### 3. THE CRITERIA

- AC1: `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb3.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: every labelled title reads its rank (69 of 69); a roster in Boeing's filing order comes back chief executive, chief financial officer, then as given; the function is stable and safe; C1-C3 PASS; `R78 BB3 AC1 SERVED: YES`; and exit=0.
- AC2: same line with `--crit AC2`. Expect: every stored Bloomberg officer list is ranked without losing or misordering a row (N of N); NKE US opens with "President/CEO" then its CFO; C1-C2 PASS; `R78 BB3 AC2 SERVED: YES`; and exit=0.
- AC3: same line with `--crit AC3`. Expect: every plant case in `test_officer_rank.py` passes; `R78 BB3 AC3 SERVED: YES`; and exit=0.

### 4. THE BASE DRY-RUN (all three are BUILD checks; each FAILED as expected)

```
### AC1
FAIL C0 lib.research.management.officer_rank imports cannot import name 'officer_rank' from 'lib.research.management' (C:\Users\Opal Bloomberg\Desktop\ajb_workspace\lib\research\management\__init__.py)
R78 BB3 AC1 SERVED: NO
exit=1
### AC2
FAIL C0 lib.research.management.officer_rank imports cannot import name 'officer_rank' from 'lib.research.management' (C:\Users\Opal Bloomberg\Desktop\ajb_workspace\lib\research\management\__init__.py)
R78 BB3 AC2 SERVED: NO
exit=1
### AC3
FAIL C1 the plant test file exists lib/research/management/tests/test_officer_rank.py
R78 BB3 AC3 SERVED: NO
exit=1
```

### 5. `<paths>`

```
lib/research/management/officer_rank.py
lib/research/management/tests/test_officer_rank.py
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~<n>/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and worker class

`LOCAL`. Worker class `worker-light` (a pure module of well under 100 product lines).

### 7. Edges

None inbound. It does not depend on bb-4. Outbound: the adapter cell's one-line hookup, then the redeploy.

### 8. Not measured, and questions for the issuer

1. **Three stored lists carry no chief-executive title** (`6861 JP` "President", `939 HK`, `ICT PM` "Chairman/President"). The
   rank leaves them as served. `exec_roster_chain._has_chief_executive` treats a bare "President" as the chief executive for
   `_JP_Equity` names; a pure title function has no name to key on, so the draft does not copy that rule. Rule whether it should.
2. **Co-chiefs and handovers** (5 stored lists): both rows rank 0, in the served order. ADBE US serves "Chair/CEO" then
   "President/CEO".
3. The rank is served as ORDER only. If the page must show which rows were moved, that is one more served field and an
   adapter-cell decision.
4. A UK "Finance Director" is not ranked as a chief financial officer: 0 rows of that title in the 91 stored lists.
5. AC2 reads the stored Bloomberg lists only (R2). The filing rosters are covered by the labelled titles and the Boeing
   roster in AC1, typed from R3; the check does not re-read the deployed function.
6. Two titles I left OUT of the labelled table because their reading is a judgment call: "CEO/Pres & CEO:Centroamerica"
   (rule: rank 0, the first piece is unscoped) and "Rep Exec Officer/Senior Managing Exec Officer/CFO:" (cut at 50
   characters, empty unit; rule: rank 1).

---

## A3 -- `AMGT-bb-4` THE SLASH-SAFE OFFICERS READER (row AMGT_RESAPP-Z-S365)

### 1. MEASURED AT THE BASE

| fact | value | read |
|---|---|---|
| `newest_key("BP/ LN Equity")`, `newest_key("NG/ LN Equity")` | None, None | R4 |
| control `newest_key("AMD US Equity")` | `.../exec_officers/security_key=AMD_US_Equity/20261007T113604Z.json` | R4 |
| the stored objects | `security_key=BP-SLASH-_LN_Equity/20261007T113610Z.json`, `security_key=NG-SLASH-_LN_Equity/20261007T113644Z.json` | R2 |
| the denominator | 91 stored folders; the reader finds the newest object of 89; not 2 (the two slash names) | R2, R4 |
| the chain | `run_chain("BP/_LN_Equity")` and `("NG/_LN_Equity")`: served None, Bloomberg leg "not tried" with `needs_new_pull` true. `run_chain("AMD_US_Equity")`: Bloomberg, 25 officers | R4 |
| the deployed page | both slash names serve no officers; the reason ends "no Bloomberg officer list is stored for this name, and getting one needs a new Bloomberg request" | R3 |
| callers of `bloomberg_fallback.security_key` | 2, both inside the file: `newest_key` (`:93`, the defect) and `pull_exec_officers` (`:187`). 0 outside it (Grep over every `*.py` in the repo for `bloomberg_fallback.security_key` and `bf.security_key`; `enrich.py:615` only names it in a docstring) | R6 |
| the WRITER is already safe | `pull_exec_officers` hands that text to `hbloom.bronze_write`, which applies `store.entity_partition` (`harvest/bloomberg.py:110`). `crosswalk.slash_safe_key` REFUSES a value that already holds the slash token (`crosswalk.py:221`), so changing what `security_key()` returns would break the writer on a slash name | R6 |
| callers of `StoredBloombergInput` | 2 product callers: `exec_roster_chain._bloomberg_leg` (`:186`) and `fwd7_plan.produce` (`:61`); both inherit the defect and both are repaired by the one repair. The pull driver's plan (`integrations/bloomberg/research/research_pulls.py:82`) counts `needs_new_pull` from the chain, which is why it still names 2 | R6 |
| other readers of the officers store, same rule? | `build_view.latest_bloomberg_bronze_stamp` (`build_view.py:133`) builds the folder with `crosswalk.security_key_partition`: SAFE, and it returns a stamp for both slash names (`20261007T130306Z`, `20261007T130817Z`). `scoped_amgt.py:5602-5613` lists the whole prefix once and decodes each folder with `crosswalk.security_key_from_slash_safe`: SAFE by source read (not exercised by me on the deployed function). `fwd7_plan.py`: no rule of its own. So raw-slash readers of this store: 1 of 4 | R4, R6 |
| an existing estate function that already lists the right folder | `hbloom.bronze_fetched("exec_officers", "BP/_LN_Equity", client=s3)` returns the stored object | R4 |

### 2. THE ACT (worker face text)

Repair ONE method in ONE existing file: `StoredBloombergInput.newest_key` in `lib/research/management/bloomberg_fallback.py`.
You are the only writer of that file this round.

Today it lists `bloomberg/harvest/bronze/exec_officers/security_key=<security with spaces turned to underscores>/`. The
writer stores a name through `lib.research.harvest.store.entity_partition`, which turns a slash into `-SLASH-`. So
`BP/ LN Equity` and `NG/ LN Equity` are stored under `security_key=BP-SLASH-_LN_Equity/` and
`security_key=NG-SLASH-_LN_Equity/` and are never read: `newest_key("BP/ LN Equity")` returns None.

1. Make `newest_key(security)` list the folder the writer writes: `BRONZE_PREFIX` +
   `store.entity_partition("security_key", security_key(security))` + `/`. The store module is already imported in this
   file's package as `hbloom.store`; `hbloom.bronze_fetched("exec_officers", security_key(security), client=...)` is the
   estate's own listing of that folder and may be used instead. Keep the return: the newest `.json` key, or None.
2. Do NOT change what `security_key()` returns (`"AMD US Equity"` gives `"AMD_US_Equity"`, `"BP/ LN Equity"` gives
   `"BP/_LN_Equity"`). `pull_exec_officers` hands that text to the writer, which makes it slash-safe once; a second
   encoding is refused by the store.
3. Change nothing else in the file: not `pull_exec_officers`, not the parse, not the status rule, not `reference_data`'s
   shape. Fix the stale line in the class docstring if you touch it.
4. Plant tests in a NEW file, `lib/research/management/tests/test_stored_officers_slash_key.py`, with a fake S3 client:
   an object stored under `security_key=BP-SLASH-_LN_Equity/` is found by `newest_key("BP/ LN Equity")` and read by
   `pull_exec_officers("BP/ LN Equity", blp=StoredBloombergInput(s3=fake))` with status OK; a plain name is found as before;
   the newest of two stamps wins; a name with nothing stored returns None.

**You do NOT edit `lib/research/api/scoped_amgt.py`, `lib/research/management/exec_roster_chain.py`,
`lib/research/management/fwd7_plan.py`, `lib/research/freshness/build_view.py` or `lib/research/harvest/*`.** No hookup is
needed: `exec_roster_chain` already calls `newest_key`. Say so in your report, and say that the page changes only with the
next redeploy of the function.

### 3. THE CRITERIA

- AC1: `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb4.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: `newest_key("BP/ LN Equity")` and `newest_key("NG/ LN Equity")` each return the newest object in that name's folder; the control `AMD US Equity` still does; every stored officer folder is read (N of N); the chain serves officers for both slash names and the control; C1-C4 PASS; `R78 BB4 AC1 SERVED: YES`; and exit=0.
- AC2: same line with `--crit AC2`. Expect: every plant case in `test_stored_officers_slash_key.py` passes; `R78 BB4 AC2 SERVED: YES`; and exit=0.
- AC3 (bound): same line with `--crit AC3`. Expect: `security_key()` returns `AMD_US_Equity` and `BP/_LN_Equity` as before; the three existing test files of this reader pass; C1-C2 PASS; `R78 BB4 AC3 SERVED: YES`; and exit=0.

### 4. THE BASE DRY-RUN

AC1 (BUILD) FAILED as expected, with its control clause C2 passing:
```
   newest_key('BP/ LN Equity') = None
   newest_key('NG/ LN Equity') = None
   newest_key('AMD US Equity') = bloomberg/harvest/bronze/exec_officers/security_key=AMD_US_Equity/20261007T113604Z.json
FAIL C1 the two slash names read their newest stored object 
PASS C2 the control name still reads its newest stored object 
   stored officer folders 91; read 89; not read ['BP/ LN Equity', 'NG/ LN Equity']
FAIL C3 every stored officer folder is read 89 of 91
   chain BP/_LN_Equity: served by None, 0 officer(s); Bloomberg leg 'not tried'
   chain NG/_LN_Equity: served by None, 0 officer(s); Bloomberg leg 'not tried'
   chain AMD_US_Equity: served by bloomberg, 25 officer(s); Bloomberg leg 'served officers'
FAIL C4 the chain serves officers for both slash names and for the control 
R78 BB4 AC1 SERVED: NO
exit=1
```
AC2 (BUILD) FAILED as expected:
```
FAIL C1 the plant test file exists lib/research/management/tests/test_stored_officers_slash_key.py
R78 BB4 AC2 SERVED: NO
exit=1
```
AC3 (BOUND) PASSED as expected:
```
PASS C1 security_key() returns what it returned before 'AMD_US_Equity' 'BP/_LN_Equity'
   24 passed in 1.65s
PASS C2 the existing tests of this reader pass rc=0
R78 BB4 AC3 SERVED: YES
exit=0
```
With the repair applied in memory, AC1 read 91 of 91 and the chain served BP/ LN 10 officers and NG/ LN 9.

### 5. `<paths>`

```
lib/research/management/bloomberg_fallback.py
lib/research/management/tests/test_stored_officers_slash_key.py
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~<n>/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and worker class

`LOCAL` (code and a test). The served move, 93 to 95 names with officers, is the redeploy's. Worker class `worker-light`
(the product change is a few lines).

### 7. Edges

None inbound. Outbound: the redeploy drains after it. After the redeploy the pull driver's `plan officers` should read
names 0 (it reads 2 today, per `BA22_OFFICERS_ACT_RECORD_20261007.md`); that read is the issuer's.

### 8. Not measured, and questions for the issuer

1. Whether readers of OTHER Bloomberg stores (refdata, histdata, bestdata, identity) apply a raw-slash rule: not swept. The
   row asks it; this cell covers the officers store only.
2. AC1 C4 passes for a slash name served by ANY leg. Today neither has a filing matched, so only the Bloomberg leg can serve it.
3. AC1 pins no stamp: it compares the reader with a fresh listing, so a later pull does not break it.
4. The existing fake S3 in `test_fwd7_stored_fallback.py` is not edited; AC3 runs it (24 tests across the three files pass at the base).

---

## A4 -- `AMGT-bb-13` PEERS V BELOW THREE PEERS (row AMGT_RESAPP-Z-S162 part 3)

### 1. MEASURED AT THE BASE

What Andrew's word asks, quoted from the documents:
- `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261007_054xZ_ALL_RECS_APPROVED_CTOZ_THREE_CARRIED_CARDS.md`:
  verbatim "all recs approved"; ruling 2 as recorded: "Peers V reads "not available", with its reason, when a company has
  fewer than 3 peers: (a)." and "Ruling 2 sets the threshold at 3 peers, as the card stated it."
- `ledger/CTO_ADJUDICATION_REMEDIATION_ROWS_ROUND76.md` ADDENDUM 2, card 2: "With fewer than 3 eligible peers, every Peers V
  measure reads ABSENT with `absent_reason` naming the count ("2 peers; 3 are needed"). It is never a value computed on 1
  or 2. Proof: a plant at 2 peers and one at 3." It "goes into cell ba-16 ... or its successor if ba-16 is terminal."
- CTO msg 30663 (the inbox file named in the brief): "(2) Peers V reads not-available with its reason below 3 peers.
  2.0.0_SA_COO~Z, that goes into ba-16 or its successor."

Did ba-16 do it? **No.** Its order says "What is NOT yours: what Peers V means where a peer set is short is at Andrew. Keep
the floors as they are." (`task-orders/AMGT_RESAPP.TO-AMGT-ba-16...md:35`), it is terminal (drained @de063a4209), and the
string "are needed" occurs 0 times in `lib/research/scores/peers_v.py` (R6). A cell is drafted.

| fact | value | read |
|---|---|---|
| "never a value computed on 1 or 2" | ALREADY TRUE through the older floors. Plants at 0, 1, 2, 3 and 5 peers: no score, no measure measured. A measure is first measured at 6 peers; the score is first served at 8 | R4 |
| the reason below 3 today | score: `suppressed: \|K\|=2 (need >= 8) or \|M\|=0 (need >= 3)`. Measures: `dropped: only 2 of 2 peers carry measure 1 (FCF / mkt cap), need >= 6` on four, `the scanner serves no figure for this measure (EBITDA / EV)` on two. None names the count as ruled; the first two are not plain words | R4 |
| at 3 peers today | the same shape with 3 in place of 2 | R4 |
| the floors | `MIN_PEERS_FOR_V` 8, `MIN_MEASURES_FOR_V` 3, `MIN_PEERS_PER_MEASURE` 6, with two `assert` lines naming them as Andrew's (2026-09-15), and `test_peers_v_mapping.py:133` pins all three | R6 |
| what is stored and served | 35 newest objects under `scores/v1/`, every one from the 2026-09-17 run (33 at `<key>/2026-09-17.json`, 2 flat-layout objects for the slash names). Peers V is not available on 35 of 35. Peer count 12 on 33, 0 on 2 (`9433 JP`, `ICICIBC IN`). All 210 measure reasons are the pre-ba-16 legacy sentence: the producer has not run since ba-16 landed | R5 |
| the adapter | `scoped_amgt.read_scores` serves the stored record as written, translating only two exact legacy sentences (`scoped_amgt.py:4691-4713`). A new sentence written by the producer is served unchanged | R6 |

### 2. THE ACT (worker face text)

Add the three-peer rule to Peers V. It lives inside `score_peers_v` in `lib/research/scores/peers_v.py`, so this cell edits
that one existing file (you are its only writer this round) and adds one new test file.

Andrew's word, 2026-10-07: with fewer than 3 peers, Peers V reads not available, with a reason naming the count; it is never
a value computed on 1 or 2 peers.

1. Add a constant `MIN_PEERS_TO_COMPARE = 3` and a function `short_peer_set_reason(count)` returning exactly
   `"0 peers; 3 are needed"`, `"1 peer; 3 are needed"`, `"2 peers; 3 are needed"` (the 3 comes from the constant).
2. In `score_peers_v`, right after the subject is removed from the peer set and `K` is counted: when `K` is below
   `MIN_PEERS_TO_COMPARE`, return at once with `V` None, `K`, `M` an empty list, `state` `classify.ABSENT_SOURCE`, `reason`
   and `absent_reason` both that sentence, and `measures` holding ALL SIX measure ids, each
   `classify.absent(classify.ABSENT_SOURCE, <that sentence>)`. No measure is computed and no other reason is given.
3. At 3 peers or more, change NOTHING: the same keys, values and sentences as today. The older floors stay exactly as they
   are (8 peers for the score, 3 measures, 6 peers per measure), and so do the two `assert` lines and every existing name
   (`MEASURE_NOT_COMPUTABLE_REASON`, `LEGACY_MEASURE_NOT_COMPUTABLE_REASON`, `SCANNER_FACTOR_MAP`, ...).
4. Add one line to the module docstring's GUARDS paragraph stating the rule and its date.
5. Plant tests in a NEW file, `lib/research/scores/tests/test_peers_v_short_set.py`: plants at 0, 1 and 2 peers (the
   sentence on the score and on all six measures; no value anywhere), a plant at 3 (the sentence is not used), a plant at 8
   (a score is served, equal to the score before your change), the subject listed among its own peers is not counted, and
   both row vocabularies.

**You do NOT edit `lib/research/api/scoped_amgt.py`, `lib/research/scores/run_scores.py`, `classify.py` or
`test_peers_v_mapping.py`.** No adapter hookup is needed: the adapter serves the stored record as written. Say in your
report that the page shows the new sentence only after the scores producer (`run_scores`) is run again, which is a store
write and the issuer's act, not yours.

### 3. THE CRITERIA

- AC1: `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb13.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: plants at 0, 1 and 2 peers read no score and the count sentence on the score and on all six measures; the sentence carries no status word or symbol; at 3 peers the sentence is not used; at 8 peers the score is -1.0823626487770477 as before; C1-C4 PASS; `R78 BB13 AC1 SERVED: YES`; and exit=0.
- AC2 (bound): same line with `--crit AC2`. Expect: the floors read (8, 3, 6); the two existing test files of this score pass; C1-C2 PASS; `R78 BB13 AC2 SERVED: YES`; and exit=0.
- AC3: same line with `--crit AC3`. Expect: every plant case in `test_peers_v_short_set.py` passes; `R78 BB13 AC3 SERVED: YES`; and exit=0.

### 4. THE BASE DRY-RUN

AC1 (BUILD) FAILED as expected, with its two control clauses passing (the measure-reason lists are shortened here to their
first entry; the full lines are what the script prints):
```
   plant at 0: score None; reason 'suppressed: |K|=0 (need >= 8) or |M|=0 (need >= 3)'; measure reasons ['dropped: only 0 of 0 peers carry measure 1 (FCF / mkt cap), need >= 6', ...]
   plant at 1: score None; reason 'suppressed: |K|=1 (need >= 8) or |M|=0 (need >= 3)'; measure reasons ['dropped: only 1 of 1 peers carry measure 1 (FCF / mkt cap), need >= 6', ...]
   plant at 2: score None; reason 'suppressed: |K|=2 (need >= 8) or |M|=0 (need >= 3)'; measure reasons ['dropped: only 2 of 2 peers carry measure 1 (FCF / mkt cap), need >= 6', ...]
FAIL C1 below 3 peers the score and all six measures read the count sentence 
FAIL C2 the count sentence carries no status word or symbol 
   plant at 3: score None; reason 'suppressed: |K|=3 (need >= 8) or |M|=0 (need >= 3)'
PASS C3 at 3 peers the count sentence is not used 
PASS C4 at 8 peers the score is the same as before -1.0823626487770477
R78 BB13 AC1 SERVED: NO
exit=1
```
AC2 (BOUND) PASSED as expected:
```
PASS C1 the ruled floors are unchanged (8, 3, 6)
   55 passed in 0.69s
PASS C2 the existing tests of this score pass rc=0
R78 BB13 AC2 SERVED: YES
exit=0
```
AC3 (BUILD) FAILED as expected:
```
FAIL C1 the plant test file exists lib/research/scores/tests/test_peers_v_short_set.py
R78 BB13 AC3 SERVED: NO
exit=1
```

### 5. `<paths>`

```
lib/research/scores/peers_v.py
lib/research/scores/tests/test_peers_v_short_set.py
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~<n>/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and worker class

`LOCAL`. Worker class `worker-light` (about 15 product lines).

### 7. Edges

None inbound, provided no other round-78 cell writes `lib/research/scores/peers_v.py`. Outbound: none in code. The served
sentence needs a producer run (issuer act).

### 8. Not measured, and questions for the issuer

1. **RULE NEEDED: what the 3 means beside the older floors.** Andrew's 2026-09-15 floors (6 peers per measure, 8 for the
   score) already keep every value off a set of 1 or 2, and off 3 to 7 as well. The draft reads the new word as a distinct,
   plain REASON below 3 and leaves 3 to 7 to the older floors, whose sentences still carry "|K|", "|M|", "suppressed" and
   "dropped". If the word instead LOWERS a floor to 3 (a value on 3 peers), that contradicts the two `assert` lines and is
   not what this cell builds. "A plant at 2 peers and one at 3" passes under the draft: 2 reads the count sentence, 3 does not.
2. **"Eligible" peers.** The addendum says "fewer than 3 eligible peers". The draft counts `K` as the code does: every peer
   after the subject is removed, including a peer read in the other vocabulary (which carries no value). A stricter count
   would need a ruling on what makes a peer eligible.
3. **The reasons for 3 to 7 peers are not plain words** and are not touched here. If they should be, that is a second cell or
   an added rule on this one, and `test_score_modules.py` reads some of those sentences.
4. **The stored scores are from 2026-09-17**, before ba-16: 35 of 35 read the legacy sentence. Neither ba-16's mapping nor this
   rule reaches a page until `run_scores` is run. I did not run it (a store write).
5. The singular "1 peer; 3 are needed" and "0 peers; 3 are needed" are my wording; the ruled quote covers only "2 peers; 3 are needed".
6. Today 2 stored names have 0 peers and none has 1 or 2, so the rule would change the sentence on 2 of 35 names.

---

## Files

- `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/GROUP_A_NOTES.md` (this file)
- `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb1.py`
- `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb3.py`
- `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb4.py`
- `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb13.py`

Nothing else in the repo was written. No commit, no stage, no deploy, no store write, no Bloomberg or other vendor call.
