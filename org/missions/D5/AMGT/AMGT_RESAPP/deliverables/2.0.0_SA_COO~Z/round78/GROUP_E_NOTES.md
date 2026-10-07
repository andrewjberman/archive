# AMGT_RESAPP round 78 -- GROUP E: one drafted cell (bb-7, redrafted to the CTO's ruling)

Drafted for `2.0.0_SA_COO~Z` on 2026-10-07, about 14:50Z to 15:10Z. Nothing is committed, no existing file was edited
other than `round78/checks/r78_bb7.py` (overwritten on instruction: it belonged to the refused draft), no store was
written, no vendor was called, no `--write-pool` was run.

**The ruling served.** `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULINGS_AMGT_RESAPP_ROUND78_CALLS_AT_THE_CUT_20261007.md`,
"bb-7, name search": "Not the copied file. The pool carries each record's legal name at its next mint, under a re-mint
pair like today's, and name search reads the pool."

**The base.** The shared tree on `CLOUD`; HEAD read `25ebedb3a3` when the reads began and `6defce97e6` at the last
dry-run. `lib/research/identity/` and `lib/research/api/` were clean in the shared tree. Python 3.14.7.

**Files.**
- check: `round78/checks/r78_bb7.py` (passes `bash .tools/commit-gate.sh`: "pre-commit gate clean for 1 of 1 file(s)").
- the literal base output: `round78/reads/bb7_E_base_output.txt` (a new file; `reads/bb7_base_output.txt` is the refused
  draft's and was left as it is).

**The finding that shapes the cell: this project's own stored objects already name 243 of 243, and the collector's file
is not needed at all.** The 158 names the collector's file marks "pool name as read" were read from this project's own
`universe/v1/` object. They are still stored there.

---

## E1 -- `AMGT-bb-7` -- the stored name list carries each record's legal name, and name search reads it

### 1. MEASURED AT THE BASE

Every count below was read in this session from `s3://opal-data-harvest` (boto3, read only) and the shared tree.

**The served object.** `crosswalk/v1/2026-10-07.json` is the newest of 7 keys: 243 records, 243 keyed, 243 distinct
keys, 0 unresolved. 175 records carry 11 fields; 68 carry a twelfth, `identity`.

**Where a name for each of the 243 can come from, by stored source.**

| source | what it is | names of 243 |
|---|---|---|
| A. the record's `source_row.folder` | the research folder name ("Lenovo 992 HK"); not a legal name | 96 |
| B. the record's `identity.name` | Bloomberg `NAME` from the record's own registration pull | 68 |
| A or B (what name search reads today) | | 100 |
| `lib/research/identity/registrations.json` | 72 rows; 68 carry `identity.name`; 0 carry any other name field | 68 (the same 68 keys as B) |
| identity bronze `NAME` | 68 objects in 68 partitions, 68 with `NAME` | 68 (the same 68 keys as B) |
| `universe/v1/2026-10-06.json` `name` | the newest universe object; 302 entries, 242 keyed, 101 keyed with a name | 101 (96 are the folder name again; 5 are holdings names) |
| C. `universe/v1/*.json` `name` on an entry whose `source` is "holding", all 3 retained objects, newest wins | the holdings line's own company name ("Apple Inc") | 163 (138 only in `2026-09-16.json`, 5 in `2026-10-06.json`, 20 also in B) |
| the collector's file (AMGT_HARVST) | a tracked repo file under that project's deliverables, last commit `bd663da39d` 2026-10-05; not a stored object | 234 |

**Which combination reaches the most.**
- A or B or C: **243 of 243**, 0 nameless. No file of another project is read.
- A legal name proper (B, then C; the folder name is not one): **211 of 243**: 68 from B, 138 from
  `universe/v1/2026-09-16.json`, 5 from `universe/v1/2026-10-06.json`. The other 32 have a research folder name and no
  legal name stored anywhere; all 32 are found by name search today through the folder. They are: 2317_TT, 9433_JP,
  ASML_NA, BABA_US, BA_US, BBSE3_BZ, BP/_LN, COST_US, ENEL_IM, HAL_US, HD_US, HSBA_LN, ICICIBC_IN, IMB_LN, INTU_US, KMB_US,
  KPN_NA, NG/_LN, NOVN_SW, NU_US, PBR_US, RKT_LN, RMS_FP, ROG_SW, RWE_GR, SAP_GY, SSE_LN, ST_SP, ULVR_LN, VLO_US,
  WALMEX*_MM, ZURN_SW (each `_Equity`).
- The collector's file adds nothing over A, B and C: its 234 are all in the pool, and C names 5 it lacks (BE, DG, ED,
  GEV, MRNA) plus B names 4 it lacks (6861_JP, ABNB_US, CAT_US, CSL_AU).

**The collector's names ARE this project's universe names.** Of the collector's 234 `company` values, 158 carry the
evidence "pool name as read", 69 are a research folder name cleaned by a rule, 2 are a pool name with its ticker removed
and 5 are the collector's own pilot names. For the 138 pool records that have no folder and no registered name, the
universe holdings name equals the collector's value on 137 of 138 (the one difference: `BP_US_Equity`, "BP PLC" in the
universe, "BP" in the collector's file).

**Why the newest universe object lost them.** `universe/v1/2026-09-16.json` names 191 of its 191 keyed entries;
`universe/v1/2026-10-06.json` names 101 of 242. `lib/research/identity/build_universe.py:796-799` writes
`"name": folder` for any name that is already a pool record, and a record made from a holdings line has no folder, so
its name is written as null from then on. The name survives only in the older object. This cell moves it into the pool
record, which is its one home after the mint.

**The builder and its schema.**
- `lib/research/identity/crosswalk.py build_crosswalk()` builds every record; no record field carries a legal name. The
  only name on a record is `identity.name` (68 records).
- `lib/research/identity/crosswalk.schema.json` sets `additionalProperties: false` on a record and on `denominators`.
  **The schema file must change**, or `write_pool` refuses the mint (`_validate_document_against_schema`).
- The pool has two mint routes and both must hand the names in, or the next mint by the other route drops them:
  `crosswalk.main` (the re-mint route) and `add_security._build_document` (the add-a-company route, which minted today's
  object for `ABNB`).
- The schema file is named by 13 files repo-wide; the non-test code among them is `crosswalk.py` alone.

**Name search.** `lib/research/api/name_search.py _stored_names()` reads `source_row.folder` then `identity.name`.
On an in-memory build of today's inputs: "apple" answers `none`, "microsoft" answers `none`, "airbnb" lists
`ABNB_US_Equity` "AIRBNB INC-CLASS A".

**An in-memory build equals the served object today.** `build_crosswalk("2026-10-07", ...)` over the registrations
file, `universe/v1/2026-10-06.json`, the research folders and the served object as `served`: 243 keys built, 243 served,
0 only on either side; 0 record fields differ on 243 of 243; of the top-level fields only
`research_universe.read_at` differs.

**Simulated in memory (no file edited).** With `legal_name` added by the rule below and name search reading it:
"apple" lists `AAPL_US_Equity` "Apple Inc"; "microsoft" lists `MSFT_US_Equity` "Microsoft Corp"; "airbnb" and "lenovo"
answer as today; "coca" lists 3 companies; 375 stored names typed whole (96 folder, 68 registered, 211 legal) list their
own record 375 of 375; 243 of 243 keys still answer `exact`; 0 legal names typed whole answer `exact`. The serialised
document grows from 748,500 bytes to 782,664 with a short evidence text; the act's full evidence sentences add more.

### 2. THE ACT (worker face text)

Typing a company name into the search lists nothing for 143 of the 243 companies we hold, because their stored record
carries no name: "apple" and "microsoft" both answer "no company we cover matches". The names exist. This project's own
stored universe objects (`s3://opal-data-harvest/universe/v1/<date>.json`) carry the company name of every holding, and
68 records carry the name their own registration stored. Make the builder of the stored name list put a legal name on
every record, state where it came from, and make the search read it.

You do NOT write the stored name list. The issuer mints it after your cell drains. Your proof is a build in memory.

**File 1: `lib/research/identity/crosswalk.py`.**

1. Add `universe_names(universe, universe_source, client=None)`. It returns a dict of company key to
   `{"value": <name>, "source": <where it was read>}`, or `None`.
   - `universe` is `None`: return `None` (the question is not asked).
   - `universe_source` starts with `s3://`: list every object under `universe/v1/` in `POOL_BUCKET` whose key matches
     `universe/v1/<YYYY-MM-DD>.json`, read each one, oldest first, and take every entry of `names` whose `source` is
     `"holding"`, whose `security_key` is set and whose `name` is a non-empty string. A newer object's name replaces an
     older one's. `value` is the name with outer whitespace removed and nothing else changed; `source` is
     `s3://opal-data-harvest/<that object's key>`. The object already in hand as `universe` need not be fetched again.
   - any other `universe_source` (a pinned local file, as the tests use): take the same entries from the one document
     `universe` and read nothing from the store; `source` is `universe_source`.
   - a failure to list or read the store RAISES. It is never answered with an empty dict.
   - keep the result in a module-level dict keyed by `universe_source`, so several builds in one run read once.
2. `build_crosswalk(...)` gains one keyword argument, `legal_names=None`.
   - `legal_names is None`: nothing changes. No record gains a field and no count is added; the document is the one
     built today, byte for byte.
   - `legal_names` is a dict (it may be empty): after the records are final (after the union with `served`, after the
     ENRICH rows, after the retirements), every record gains ONE field, `legal_name`, an object with exactly three keys:
     - the record's own `identity.name` is a non-empty string:
       `{"value": <that name, outer whitespace removed>, "status": "MEASURED", "evidence": "the record's own identity.name (the Bloomberg NAME of its registration pull)"}`;
     - otherwise `legal_names` holds the record's `security_key`:
       `{"value": <its value>, "status": "MEASURED", "evidence": "<its source> :: names[] entry with source 'holding', its name"}`;
     - otherwise: `{"value": null, "status": "ABSENT", "evidence": "no stored source carries a legal name for this record; its research folder name, where it has one, is source_row.folder"}`.
   - a record carried from `served` that already holds `legal_name` keeps it as it is; one that does not gains it by the
     same rule.
   - `denominators["with_legal_name"]` is the count of records whose `legal_name.value` is not null.
   - No other field of any record changes: not `provenance`, not `identity`, not `source_row`.
3. `main()`: read the names once, `legal_names = universe_names(universe, universe_source)`, and pass
   `legal_names=legal_names` to both `build_crosswalk` calls (the `--disclosure` one and the one `--dry-run` and
   `--write-pool` share).
4. Add one paragraph to the `build_crosswalk` docstring stating the argument, the order of the three sources and that
   `None` leaves the document as it was.

**File 2: `lib/research/identity/crosswalk.schema.json`.** Add two OPTIONAL properties and make nothing required:
- on a record, `legal_name`: an object, `additionalProperties: false`, required `value`, `status`, `evidence`;
  `value` is a string or null, `status` is one of `MEASURED`, `ABSENT`, `evidence` is a string of 1 or more characters;
- on `denominators`, `with_legal_name`: an integer, minimum 0.
Give each a `description` naming this cell (AMGT-bb-7). An object built before this cell must still pass.

**File 3: `lib/research/identity/add_security.py`.** In `_build_document`, pass
`legal_names=crosswalk.universe_names(universe, universe_source)` to `build_crosswalk`. Change nothing else there.

**File 4: `lib/research/api/name_search.py`.** `_stored_names(record)` gains a third name after the two it reads today:
the record's `legal_name.value`, when `legal_name` is an object and the value is a non-empty string, added only when it
is not already in the list (compare case-insensitively). Nothing else in the matching changes. The candidate's `name`
stays the first stored name, so a company with a folder name still shows under it, and a company with only a legal
name now shows that. Update the module docstring's "Name:" paragraph to say so.

**Tests.**
- New file `lib/research/identity/tests/test_crosswalk_legal_name.py`, on fixtures only (no store, no network), at least:
  a record with `identity.name` takes it; a record with none takes the map's name and names the map's source in
  `evidence`; a record with neither reads `value` null and `status` ABSENT; `identity.name` wins over the map;
  `legal_names=None` builds a document equal to the one built without the argument; a built document with legal names
  passes `_validate_document_against_schema`; `universe_names` on a pinned local document takes only entries whose
  `source` is "holding" and reads nothing from the store; `universe_names(None, None)` is `None`.
- In `lib/research/api/tests/test_name_search.py` add `test_a_legal_name_lists_its_company`: a record whose only name is
  `legal_name.value` "Apple Inc" lists under "apple" and "Apple" with the name "Apple Inc"; a record with a folder name
  and a legal name lists under either and shows the folder name; a record whose `legal_name.value` is null lists by its
  ticker's first word only. Keep the eight tests there passing.
- Every test file already under `lib/research/identity/tests/` must keep passing unchanged. If one fails because of your
  change, your change is wrong: the default document must not move.

**Rules.**
1. You run NO `--write-pool`, on `crosswalk` or on `add_security`, and you make no store write, put, copy or delete of
   any kind. `--dry-run` and `--disclosure` are allowed. No deploy. No Bloomberg, vendor, SEC or model call.
2. The names come from this project's own stored objects only. You do NOT read, import or copy anything under
   `lib/research/harvest/`, `lib/opal_data_harvest/` or `org/missions/D5/AMGT/AMGT_HARVST/`, and you type no company
   name into code.
3. A name is stored as it was read. Nothing is cleaned, cut, re-cased or guessed; a folder name is never written into
   `legal_name`.
4. The search still never guesses: an exact stored form answers `exact` as today, and a typed company name is never
   answered as `exact`.
5. Any sentence the search serves stays in plain words. Do not use: identity, unresolved, security key, crosswalk,
   dossier, landed, model block, estate, stage, input ledger, bronze.
6. You do NOT edit `lib/research/identity/build_universe.py`, `lib/research/identity/registrations.json`,
   `lib/research/api/scoped_amgt.py` or anything under `infra/`.
7. ASCII only in every file you write.

Report: how many of the records of an in-memory build carry a legal name and from which source (the check prints it),
the keys that carry none, and what "apple", "microsoft" and "airbnb" answer on that build.

### 3. THE CRITERIA

- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb7.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: an in-memory build carries `legal_name` (value, status, evidence) on every record, each value equal to the check's own reading of the stores with its source stated, 200 or more named (211 of 243 on 2026-10-07) and the rest ABSENT, the count stated and the schema check passed, the new test file passing; C1-C4 PASS; `R78 BB7 AC1 SERVED: YES`; and exit=0.
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb7.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: on that in-memory build "apple" lists AAPL_US_Equity as "Apple Inc", "microsoft" lists MSFT_US_Equity as "Microsoft Corp" and "airbnb" lists ABNB_US_Equity, none as exact; every stored name typed whole lists its own record; `test_a_legal_name_lists_its_company` exists and its file passes; C1-C3 PASS; `R78 BB7 AC2 SERVED: YES`; and exit=0.
- **AC3** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb7.py" --crit AC3 --where local; echo "exit=$?"`
  Expect: (BOUND) the in-memory build holds exactly the served object's keys and every field of every record other than `legal_name` equals the served record's; no top-level field moves outside the listed ones; a build not handed names carries none; every stored key still answers exact; the two packages' tests pass; C1-C5 PASS; `R78 BB7 AC3 SERVED: YES`; and exit=0.

The fields AC3 lets move, and why (the check's `MOVING` list): `research_universe.read_at` (the build's clock);
`research_universe.folders`, `denominators.research_folders_live` and `coverage_vintage.snapshot_stale_against_live`
(counts of the live research directory at the moment of the build, not of the builder);
`denominators.with_legal_name` (the one added count).

### 4. THE BASE DRY-RUN

Run 2026-10-07 15:04Z at HEAD `6defce97e6`. Literal, each line cut at 420 characters and the five measure lines printed
once here (they repeat under every criterion); whole in `round78/reads/bb7_E_base_output.txt`. AC1 FAILED as expected
(build), AC2 FAILED as expected (build), AC3 PASSED as expected (bound).

```
### AC1 --where local
   served object crosswalk/v1/2026-10-07.json; records 243; in-memory build records 243; builder handed legal names: no (the builder offers none)
   records with a research folder name 96; with a registered name 68; with either 100 of 243
   retained universe objects 3 ['universe/v1/2026-09-15.json', 'universe/v1/2026-09-16.json', 'universe/v1/2026-10-06.json']; keys they name on a holding entry 163, of which in this build 163
   oracle legal names 211 of 243, by source {"identity.name": 68, "none": 32, "universe/v1/2026-09-16.json": 138, "universe/v1/2026-10-06.json": 5}
   no legal name stored anywhere: 32 ['ASML_NA_Equity', 'BABA_US_Equity', 'BBSE3_BZ_Equity', 'BP/_LN_Equity', 'BA_US_Equity', 'COST_US_Equity', 'ENEL_IM_Equity', 'HSBA_LN_Equity', 'HAL_US_Equity', 'RMS_FP_Equity', 'HD_US_Equity', '2317_TT_Equity', 'ICICIBC_IN_Equity', 'IMB_LN_Equity', 'INTU_US_Equity', '9433_JP_Equity', 'KMB_US_Equity', 'KPN_NA_Equity', 'NG/_LN_Equity', 'NOVN_SW_Equity', 'NU_US_Equity', 'PBR_US_Equit
   in-memory build: records with a non-empty legal_name.value 0 of 243
FAIL C1 every record carries legal_name with value, status, evidence 0 of 243
FAIL C2 every record's legal name equals the oracle's, with its source stated; 200 or more are named 0 of 243 agree; named 211; first disagreeing ['ASML_NA_Equity', 'ADBE_US_Equity', 'AI_FP_Equity', 'BABA_US_Equity', 'AMXB_MM_Equity', 'AZN_LN_Equity', 'BBSE3_BZ_Equity', 'BNP_FP_Equity']
FAIL C3 the named count is stated and the document passes the write-time schema check with_legal_name None against 211 named; schema: passes
FAIL C4 lib/research/identity/tests/test_crosswalk_legal_name.py exists and passes the file does not exist
R78 BB7 AC1 SERVED: NO
exit=1
### AC2 --where local
   'apple': status none candidates []
   'microsoft': status none candidates []
   'airbnb': status candidates candidates [('ABNB_US_Equity', 'AIRBNB INC-CLASS A')]
FAIL C1 apple, microsoft and airbnb list their companies by company name, never as exact 
FAIL C2 every stored name (folder, registered, legal), typed whole, lists its own record 100 of 243 records, 375 names typed, of 243 records in all; not listed ['2602335D_US_Equity', 'AAPL_US_Equity', 'ABBV_US_Equity', 'ABT_US_Equity', 'ADM_US_Equity', 'AEP_US_Equity', 'AIG_US_Equity', 'AIZ_US_Equity', 'AMAT_US_Equity', 'AMP_US_Equity', 'AMX_US_Equity', 'AMZN_US_Equity']
FAIL C3 the test file holds test_a_legal_name_lists_its_company and passes 8 passed in 1.41s
R78 BB7 AC2 SERVED: NO
exit=1
### AC3 --where local
PASS C1 the same keys, and every existing field of every record equals the served record's keys 243 built, 243 served, only built [], only served []; fields that moved {}
PASS C2 every top-level field equals the served object's, other than the listed moving ones moved outside the list []; listed ones that moved ['research_universe.read_at']
PASS C3 a build not handed legal names carries none 0 of 243 records carry legal_name
PASS C4 every stored key passes through as exact, and lenovo lists under its folder name 243 of 243 exact; lenovo [('992_HK_Equity', 'Lenovo 992 HK')]
PASS C5 the two packages' test files pass 233 passed, 47 warnings, 2 subtests passed in 6.94s
R78 BB7 AC3 SERVED: YES
exit=0
```

Reading the AC1 C3 line: the schema reads "passes" at the base because the base document has no new field; the clause
fails on the missing count and on the builder offering no names.

### 5. `<paths>`

```
lib/research/identity/crosswalk.py
lib/research/identity/crosswalk.schema.json
lib/research/identity/add_security.py
lib/research/api/name_search.py
lib/research/identity/tests/test_crosswalk_legal_name.py
lib/research/api/tests/test_name_search.py
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/<worker serial>/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and class

LOCAL for the cell: it edits code and tests, builds in memory and writes no store. The served act is the issuer's mint
after the drain, under its own signed pair; that act is SERVED and is not this cell's.

Worker class: `worker`. The estimate is about 60 product lines in `crosswalk.py`, 3 in `add_security.py`, 6 in
`name_search.py` and about 25 schema lines, which is under the light class's 100, but the file is the builder of an
object three projects read and the default document must not move by a byte; the fuller class is the safer cut.

### 7. Edges

- **Before it: none.** No other drafted round-78 cell names `lib/research/identity/` or `name_search.py` in its paths
  (read: the path blocks of `GROUP_A_NOTES.md`, `GROUP_B_NOTES.md`, `GROUP_C_NOTES.md`; the one hit outside the refused
  bb-7 draft is a read-only test file in GROUP C). The refused draft's cell C3 in `GROUP_C_NOTES.md` must not be cut.
- **After it: the mint, then the redeploy.** The page shows nothing new until (1) the issuer mints
  `crosswalk/v1/<date>.json` from the drained code under a signed pair, and (2) the deployed function carries the new
  `name_search.py`. Either alone changes nothing a user sees: the new search on today's pool finds no `legal_name`; the
  old search on a new pool does not read it.
- **The mint's own diff is already written.** `r78_bb7.py --crit AC3` is the pair's read: after the drain it prints the
  fields that would move at a mint. Expected then: 243 keys, 0 existing record fields moved, `legal_name` added on 243,
  `with_legal_name` 211 added, `read_at` moved.
- **A same-day mint overwrites `crosswalk/v1/2026-10-07.json`.** That key holds 2 versions (read 15:0xZ): the current
  one `Y6Tisihmmlm1lCHOO61ci9b726FLXBAI`, 13:22:15Z, 748,500 B, and `1b0PNH1yqkGnLoyRbOHwEZTxBleOBxib`, 13:15:52Z,
  745,570 B. A third put on 2026-10-07 takes the current VersionId as its rollback target, re-read at the act; a mint
  on a later date writes a new key and leaves today's untouched.
- Drafts of other round-78 cells were being written in this folder at the same time (`checks/r78_bb16.py`,
  `r78_bb19.py` are untracked and not mine); their path blocks were not read. The issuer's cut checks the write sets.
- **AMGT_CORPUS and AMGT_HARVST read the pool.** The added field sits beside the fields they read
  (`source_row.folder`, `association_keys`, the keyed forms); none of those moves (AC3 C1). The pair should still tell
  `2.0.0_SA_COO~X` and `2.0.0_SA_COO~H` the time, as today's re-mint did.

### 8. Not measured, and questions for the issuer

- **Rule the 32.** 32 records have a research folder name and no legal name in any stored source of this project. The
  draft writes them ABSENT and leaves them findable by folder name, as today. The other reading of "each record's legal
  name" is a derived name (the folder with its ticker removed, as the collector does for 69). The draft refuses that:
  a derived name is not a legal name. A true legal name for the 32 is one Bloomberg `NAME` read each, which is Andrew's
  word.
- **Rule the precedence.** The draft takes the registration's Bloomberg `NAME` before the holdings name. 20 records
  have both. The Bloomberg names are upper case and cut by Bloomberg ("MITSUBISHI UFJ FINANCIAL GRO"); the holdings
  names are mixed case ("Apple Inc"). The search reads both either way; only the stored `legal_name.value` differs.
- **Names are stored as read.** 9 holdings names end in a slash tail ("Coca-Cola Co/The", "Marriott International
  Inc/MD"), 8 named values are exactly 30 characters long (possibly cut at the source), and 74 are upper case. The
  search shows them as stored. Cleaning them is a display question for a later cell, not a pool question.
- **138 names rest on one object dated 2026-09-16.** If `universe/v1/2026-09-16.json` were removed before the mint,
  those 138 would read ABSENT. After the mint the pool holds them, but a record the builder re-makes from its inputs is
  re-read from the universe objects each time, not from the served pool. The durable repair is one line in
  `lib/research/identity/build_universe.py:799` (`"name": folder` loses the holdings name of every record already in
  the pool), so each new universe object carries the names forward. That file is outside this cell; it is a candidate
  next cell, and a surprise row is the issuer's to file.
- NOT measured: the holdings object itself (`gold/holding/date=2026-10-02/holding.parquet`, named in the universe
  object's `holdings_source`). It is the origin of source C and may name more than the retained universe objects do. It
  was not opened: it is another plane, and source C already reaches 211.
- NOT measured: whether any reader outside `lib/research/` rejects a pool record with a field it does not know. The
  schema is named by no non-test code outside `crosswalk.py` (one search over `*.py`, `*.sh`, `*.json`, `*.ts`, `*.tf`,
  13 files, each hit's path read). Readers of the pool's records were listed in
  `round77/POOL_REBUILD_DIFF_READ_20261007.md`; that list was not re-run.
- NOT exercised: `add_security`'s hermetic tests against the new `_build_document` line. The draft's rule that a pinned
  local universe is read alone, and a `None` universe asks nothing, is written to keep them hermetic; the worker's run
  of AC3 C5 is the proof.
- NOT exercised: the deployed route. The cell's proof is local by instruction; "apple" on the deployed route is the
  redeploy cell's read after the mint.
- The check calls three private names of the builder (`_read_pool_latest`, `_research_folders_for_disclosure`,
  `_validate_document_against_schema`) and expects the new loader to be named `universe_names`. If the worker renames
  the loader, AC1 C3 fails; the act names it for that reason.
