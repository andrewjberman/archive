## B1 -- `AMGT-cc-3` -- THE STORE READER OF THE SEEKING ALPHA COLLECTOR'S JOB RECORDS, ONE LISTING PER SNAPSHOT REFRESH (ROW Z-S367, RULING R1)

### 1. MEASURED AT THE BASE

Base `44fe98b15e` (CLOUD), 2026-10-08T10:06Z to 10:2xZ. Store reads only (`s3://opal-data-harvest`, boto3, list and GET); nothing written.

**FIRST AND PLAINLY: the records do NOT exist for most covered names. 23 of 95 covered names hold a record; 72 hold none.**
Under CTO ruling C2 ("bb-16 deploys only with the collector's records present for the reached names") serving is a CTO call; see
"THE CONDITION" at the end of this section and question Q1 in section 8.

**The prefix, from the builder, never typed.** `lib.research.harvest.store.address_of('seeking-alpha', 'state', 'job_record', store.entity_partition('security_key', 'BA_US_Equity'), object_name='X.json')`
printed `s3://opal-data-harvest/seeking-alpha/harvest/state/job_record/security_key=BA_US_Equity/X.json`; `store.table_prefix(...)`
printed `seeking-alpha/harvest/state/job_record/`. `lib.opal_naming.address('seeking-alpha', <harvest scope>, 'state', 'job_record', 'date=1970-01-01')`
with its last segment cut prints the same bucket and prefix WITHOUT importing `store` (which imports `pyarrow` at its top, line 27).

**One paginated listing of that prefix (10:06Z):**

| measure | value |
|---|---|
| objects | 105 (25,525 bytes in all; the largest object is 259 bytes); 106 at 10:2xZ, so records are still arriving |
| distinct `security_key=` folders | 104 (103 hold one object, 1 holds two: AAPL_US_Equity, not covered); 0 keys of any other shape |
| oldest / newest object stamp | `20261005T014906Z` / `20261008T094721Z` |
| stamps by day | 10-05: 10; 10-06: 9; 10-07: 57; 10-08: 29 |
| written (LastModified) | 2026-10-07T15:54:14Z to 2026-10-08T09:47:23Z (76 on 10-07, 29 on 10-08) |
| parsed by `collector_record.parse_record` | 105 of 105; rejected 0 |
| body `security_key` whose folder differs from the folder it sits in | 0 of 105 |
| covered names (`covered_security_keys()`) | 95, all distinct |
| covered names with one or more records | **23 of 95** (23 records; the most any covered name holds is 1) |
| folders that are not a covered name | 81 of 104 |

**`seeking_alpha_state` per covered name (95):** `read` 11, `checked` 12, `no_record` 72.
- `read` (11), with the date: 992_HK 2026-09-22; ASML_NA, BABA_US 2026-10-06; AMD_US, BA_US, BP/_LN, COST_US, GOOGL_US 2026-10-07;
  HAL_US, HD_US, HSBA_LN 2026-10-08.
- `checked` (12): 2317_TT, 9433_JP, BBSE3_BZ, BZLFY_US, CPA_US, ENEL_IM, ICICIBC_IN, IDXX_US, IMB_LN, INTU_US, ISRG_US, KMB_US.
- Newest job's status over the 23: `new_articles` 10, `no_acceptable_new_articles` 13.
- **The three pilot names:** BABA_US_Equity `read`, last read `2026-10-06T23:15:47Z`; BA_US_Equity `read`, `2026-10-07T01:33:47Z`;
  COST_US_Equity `read`, `2026-10-07T11:27:36Z`. None reads 2026-09-11.
- The two covered slash names: `BP/_LN_Equity` `read` (found under `security_key=BP-SLASH-_LN_Equity`); `NG/_LN_Equity` `no_record`.

**Whether the collector runs on a schedule: NO.**
- `lib/opal_data_harvest/config.json` line 15: `"recurring_schedule_enabled": false`; `seeking_alpha_job_record.enabled` reads true.
- `org/missions/D5/AMGT/AMGT_HARVST/task-orders/AMGT_HARVST.TO-HVST-bl-1.covered-securities-with-no-collection-job.md` line 20: "The
  collector ... has only ever run as a per-security backfill: one job for one security per source", and its close: Seeking Alpha
  has a job for 115 of 242 securities.
- `org/missions/D5/AMGT/AMGT_RESAPP/ledger/ROUND_ANALYSIS.round78.md` R2: a one-pass backfill with no daily run; mechanism and cadence
  held by Andrew (2026-09-15).
- The writer: `lib/opal_data_harvest/job_record.py` (`build_record`, `address`, `write`, write-once), order
  `AMGT_HARVST.TO-HVST-bf-1.seeking-alpha-job-record.md` (one-time emit of 59, switch on @a4542de7f9), ledger
  `org/critical_paths/change_management/20261007T1551Z_harvst-sa-job-record-m-20261007_deploy_completion.md` (CLOSED), and
  `TO-HVST-bh-8` (a record's `finished_at` is the job's own end). A job that did not conclude writes no record.
- **Why 23 of 95:** all 95 covered names are on the collector's own list (95 of 95 in
  `deliverables/2.0.0_SA_COO_H/round64/securities.universe.r64.json`, 242 securities). The backfill is in progress and the
  folders run from digits to the letter K. Of the 72 with no record, 47 begin L to Z (not reached), and 25 begin with a digit or
  A to K (reached by the alphabet and holding no record: not traced per name whether the job did not conclude or was never run).

**What the page shows per state under the existing stale rule** (`lib/research/freshness/stale_rule.py` `annotate_row`, which reads
only `per_input.seekingalpha`; the page is `portal/src/pages/Freshness/Freshness.tsx` line 130 and `freshnessRows.ts` at portal
`origin/DEV` d1b21c97):

| state | what feeds the rule | rule's input state | the cell draws | flags stale |
|---|---|---|---|---|
| `read` | the date | `fresh` when 7 or fewer trading days old, else `stale` | the date `YYYY-MM-DD` | only when more than 7 trading days old |
| `checked` | no date | `not_collected` | **"Not collected"** | never |
| `no_record` | no date | `not_collected` | **"Not collected"** | never |
| `unreadable` (this cell's failure state) | no date | `not_collected` | **"Not collected"** | never |

Measured today (2026-10-08): `read` gives fresh 10, stale 1 (992_HK_Equity: newest article stored 2026-09-22, newest job
2026-10-07 `no_acceptable_new_articles`); `checked` 12 and `no_record` 72 all give `not_collected`.
**So with the page as it is, 84 of 95 cells would read "Not collected".** The schema's reader rules 3 and 4 forbid those words
for both states. The adapter cell alone cannot serve this column right: the page must draw the row's sentence (section 8, H5, Q2).

**The function's role cannot read the prefix as the terraform stands.** `infra/aws/terraform/harvest/scoped-amgt-api.tf` lines
176 to 198 grant `seeking-alpha/harvest/bronze/` and `seeking-alpha/harvest/silver/`; no entry covers
`seeking-alpha/harvest/state/`. Read from the file at HEAD; the live policy was not simulated (section 8, Q3).

**THE CONDITION under which this cell's output may be served (for the CTO to rule):** the module is safe to BUILD now. It may be
SERVED when (a) the role holds list and get on the builder's job-record prefix; (b) the page draws `checked`, `no_record` and
`unreadable` in their own words and not as "Not collected"; and (c) the CTO accepts 23 of 95 with a record (11 dates) as
"records present for the reached names", or the collector's backfill has reached the remaining 72.

### 2. THE ACT (worker face text)

The freshness page's "Seeking Alpha last read" column is wrong for every covered company. The collector now writes one small
JSON record per finished job, and a pure reader of those records already exists
(`lib/research/freshness/collector_record.py`: `parse_record`, `partition_for`, `seeking_alpha_state`). Nothing reads the
records from the store yet. Build that one store-reading module. Another cell connects it to the page; you connect nothing.

Read first, whole: `lib/research/freshness/collector_record.py`, `lib/research/freshness/seeking_alpha_job_record.schema.json`
(its `x-address` and `x-reader-rules`), and `lib/research/freshness/snapshot.py` (how this package asks the address builder).

Create `lib/research/freshness/collector_read.py`. Standard library only at the top of the file, plus
`from lib.research.freshness import collector_record`. Import `boto3` and `lib.opal_naming` INSIDE the functions that use them.
**Never import `lib.research.harvest.store` or `pyarrow`**: the deployed function does not carry `pyarrow`.

It exports exactly these names:

`READ_WIDTH = 16`, `MAX_RECORDS_PER_COMPANY = 5`,
`UNREADABLE_SENTENCE = "The Seeking Alpha collection record could not be read just now."`

`job_record_location()` returns `(bucket, prefix)`.
1. Call `lib.opal_naming.address("seeking-alpha", lib.opal_naming.lookup("harvest")["long"], "state", "job_record", "date=1970-01-01")`.
   It returns `s3://<bucket>/<key>`. The bucket is the text between `s3://` and the first `/`. The prefix is the key with its
   last segment cut, ending in `/`. Type no bucket name and no prefix anywhere in the module or its tests.

`compact_stamp(last_read)` returns text or `None`.
2. For text shaped `YYYY-MM-DDTHH:MM:SSZ` return `YYYYMMDDTHHMMSSZ` (`2026-10-07T01:32:41Z` gives `20261007T013241Z`).
   For `None` or anything else return `None`. It never raises.

`seeking_alpha_by_security(covered_keys, client=None)` returns a dict with exactly two keys, `"by_security"` and `"read"`.
It NEVER raises, whatever the store does.
3. `covered_keys` is a list of company keys such as `BA_US_Equity` or `BP/_LN_Equity`. Keep the first of any repeated key.
   `"by_security"` holds one entry for EVERY key given, and no other key.
4. `client` is a store client with `get_paginator("list_objects_v2").paginate(Bucket=..., Prefix=...)` and
   `get_object(Bucket=..., Key=...)`. When it is `None`, make `boto3.client("s3", region_name="us-east-1")` inside the function.
   Call no other method of the client. Never write, copy or delete.
5. **ONE listing per call.** Paginate the prefix from rule 1 once and read every page's `Contents`. Do not pass `Delimiter`.
   Count every listed object in `read["objects_listed"]`.
6. A listed key counts only when, after the prefix, it is exactly `<folder>/<name>` with the folder starting `security_key=`
   and the name ending `.json`. Any other key is counted in `read["ignored"]` and never fetched.
7. A company's folder is `collector_record.partition_for(<key>)`. Fetch bodies ONLY for folders of the keys given. An object in
   any other folder is never fetched.
8. For one company, sort its object keys from greatest to least and keep the first `MAX_RECORDS_PER_COMPANY`. When it held
   more, add the company's key to the list `read["capped"]`. (The object name is the job's end time, so the greatest names are
   the newest jobs; each record already carries the newest article time held up to that job.)
9. Fetch each kept object with `get_object`, read its `Body`, decode UTF-8 and parse JSON. Use a
   `concurrent.futures.ThreadPoolExecutor` of `min(READ_WIDTH, <objects to fetch>)` workers when there is more than one.
   Fetch no object twice.
10. A body that is fetched but is not UTF-8 JSON becomes `None` in the company's list. A fetched object for which
    `collector_record.parse_record` returns `None` (that includes the `None` just named) has its store key added to the list
    `read["rejected"]`. It is still handed to `seeking_alpha_state`, which counts it and never uses it as a date.
11. The company's entry is `collector_record.seeking_alpha_state(<its list of objects>)`, called with NO `pilot_stamp`. A company
    with no folder gets `seeking_alpha_state([])`, which reads `no_record`. Do not change the dict that function returns.
12. **A fetch that raises.** Add that object's key to the list `read["bodies_failed"]`. The company it belongs to gets the
    UNREADABLE entry of rule 14, even if its other objects were fetched. Every other company is unaffected.
13. **A listing that raises, or the address builder raising.** Every company gets the UNREADABLE entry; nothing is fetched;
    `read["reason"]` says what failed in plain words with the error's type name.
14. The UNREADABLE entry is exactly: `state` `"unreadable"`, `last_read` `None`, `newest_job_finished_at` `None`,
    `newest_job_status` `None`, `stored_by_newest_job` `None`, `records` `0`, `rejected` `0`, `sentence` `UNREADABLE_SENTENCE`.
    It never carries a date.
15. `"read"` is a dict with exactly: `status` (`"served"` or `"read_failed"`), `read_completed` (true only when the listing
    finished AND no fetch raised), `store` (`s3://<bucket>`, or `None` if the builder raised), `prefix`, `objects_listed`,
    `ignored`, `folders` (distinct counted folders listed), `covered_names` (keys given after rule 3), `covered_with_folder`,
    `bodies_read` (objects fetched), `bodies_failed` (sorted list), `rejected` (sorted list), `capped` (list, in the order of
    the keys given), `reason` (`None` when `read_completed` is true).
16. The module never reads `seeking-alpha/harvest/bronze/` or any other prefix. The September pilot objects are not its input.
17. No sentence it returns uses: not collected, identity, unresolved, security key, crosswalk, dossier, landed, model block,
    estate, stage, input ledger, bronze.

Plant tests in `lib/research/freshness/tests/test_collector_read.py` with a fake client of your own (a dict of key to bytes;
no network): one test per rule 2, 3, 5 to 14, and one that the module's source text contains neither `harvest.store` nor
`pyarrow`.

You do NOT edit `lib/research/api/scoped_amgt.py`, `lib/research/freshness/build_view.py`, `lib/research/freshness/page_body.py`,
`lib/research/freshness/stale_rule.py`, `lib/research/freshness/collector_record.py` or the schema file. You deploy nothing and
write nothing to any store. AC2 reads the real store with this device's own credentials (list and GET only). Your report names
anything the hookup cell must know that this order did not say.

### 3. THE CRITERIA
- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc3.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: on a fake store, two companies read with their newest article date, a no-article record reads checked, no folder reads no_record, a malformed object is counted and named, the slash name is found, a failed listing and a failed body read unreadable with no date, one listing per call, the cap holds; F0-F11 PASS; R79 CC3 AC1 SERVED: YES; and exit=0
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc3.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: on the real store the read finishes, 95 of 95 covered names have a state, each equals the check's own recount (90 or more compared, 0 differ), 23 or more hold a record and 11 or more read a date, no date is 2026-09-11; R1-R6 PASS; R79 CC3 AC2 SERVED: YES; and exit=0
- **AC3** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc3.py" --crit AC3 --where local; echo "exit=$?"`
  Expect: the freshness test folder passes and collector_record.py and the schema file hold the bytes of the cut; B1-B2 PASS; R79 CC3 AC3 SERVED: YES; and exit=0

### 4. THE BASE DRY-RUN

At `44fe98b15e`, 2026-10-08 ~10:2xZ. AC1 and AC2 FAIL because the module does not exist (the right reason); AC3 PASSES.

```
--- BASE AC1
FAIL F0 lib.research.freshness.collector_read imports ModuleNotFoundError: No module named 'lib.research.freshness.collector_read'
R79 CC3 AC1 SERVED: NO
exit=1
--- BASE AC2
FAIL F0 lib.research.freshness.collector_read imports ModuleNotFoundError: No module named 'lib.research.freshness.collector_read'
R79 CC3 AC2 SERVED: NO
exit=1
--- BASE AC3
PASS B1 the freshness test folder passes 32 passed in 0.21s
PASS B2 lib/research/freshness/collector_record.py holds the bytes of the cut blob 848e4f19a677 pinned 848e4f19a677
PASS B2 lib/research/freshness/seeking_alpha_job_record.schema.json holds the bytes of the cut blob 1040d31b7f27 pinned 1040d31b7f27
R79 CC3 AC3 SERVED: YES
exit=0
```

Reachability: the same check run from a scratch script OUTSIDE the repo against an in-memory stub of the module (no product
file was created; `git status --porcelain -- lib/` is empty after it):

```
--- STUB AC1
PASS F0 the module imports and loads neither the harvest store module nor pyarrow []
PASS F0b still neither after a call []
PASS F1 two companies with records read as read, dated by the greatest stored article time AAA read 2026-10-07T01:32:41Z; BBB read 2026-10-06T11:58:00Z; missing fields []
PASS F2 a company whose only record holds no article reads as checked, with no date checked Seeking Alpha was checked on 2026-10-07 and no article is held for this company.
PASS F3 a company with no folder reads no_record, never not collected no_record No Seeking Alpha collection record is held for this company yet.
PASS F4 a malformed object is counted, named and not used as a date EEE no_record rejected 1; FFF read 2026-10-06T05:59:00Z rejected 1; named 2
PASS F5 the slash name is found under its slash-safe folder read 2026-10-07T04:27:21Z
PASS F7 one listing per call, bodies fetched for covered folders only, no other client method touched listings 1; gets 13 of 13 wanted; uncovered fetched False; other calls []
PASS F11 a company over the cap has only its newest records fetched, and is named cap 5; GGG read 2026-10-07T00:00:00Z records 5; capped ['GGG_US_Equity']
PASS F9 the September pilot object under the old tables never becomes a date DDD None
PASS F6 a listing that raises does not raise out: every company reads unreadable, none has a date states ['unreadable']; read_completed False
PASS F8 a body that cannot be fetched makes that one company unreadable and leaves the others BBB unreadable; AAA read; read_completed False; failed 1
PASS F10 compact_stamp gives the stamp form the other columns use, and None for no date ('20261007T013241Z', None, None)
R79 CC3 AC1 SERVED: YES
stub exit=0
--- STUB AC2
PASS R1 the function returns on the real store without raising, and its read finished objects listed 106; bodies read 23; rejected 0; reason None
PASS R2 every covered name has a state: read, checked or no_record, a date only on read 95 of 95 covered; states {'no_record': 72, 'checked': 12, 'read': 11}
PASS R3 the module's bucket and prefix equal the builder's ('opal-data-harvest', 'seeking-alpha/harvest/state/job_record/') against ('opal-data-harvest', 'seeking-alpha/harvest/state/job_record/')
PASS R4 state and date equal this check's own recount on every name whose folder did not change compared 95 of 95 (folders that changed during the run: 0); differ 0 []; objects 106 then 106
PASS R5 the counts are at or above the floor measured at the cut with a record 23 (floor 23); read 11 (floor 11); checked 12; no_record 72
PASS R6 no date is the pilot's 2026-09-11; BABA, BA and COST read at or after the cut's dates pilot-dated []; [('BABA_US_Equity', 'read', '2026-10-06T23:15:47Z'), ('BA_US_Equity', 'read', '2026-10-07T01:33:47Z'), ('COST_US_Equity', 'read', '2026-10-07T11:27:36Z')]
R79 CC3 AC2 SERVED: YES
stub exit=0
```

`bash .tools/commit-gate.sh` on the check file: `OK: pre-commit gate clean for 1 of 1 file(s)`, exit 0. The check is ASCII with
LF endings (0 bytes above 127, 0 carriage returns).

### 5. `<paths>`

```
lib/research/freshness/collector_read.py
lib/research/freshness/tests/test_collector_read.py
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and class

- `<risk>`: LOCAL. One new module and its tests; no served file is edited, nothing is deployed, no store is written. AC2 reads
  `s3://opal-data-harvest` (list and GET) with the device's credentials. Egress class NONE: no vendor, SEC or model call.
- `<worker_class>`: `worker`. The reference stub is about 100 lines before its tests, at the light class's limit; the failure
  rules (12 to 14) want the fuller effort.
- The SERVED act is the adapter cell's and the deploy pair's, not this cell's (section 8).

### 7. Edges

- **The cap (rule 8) and why 5.** Measured: the 23 covered folders hold 23 objects, at most 1 each; the largest folder in the
  whole prefix holds 2; the largest body is 259 bytes. A record is written once per finished job and the collector has no daily
  run, so a folder grows by one per backfill pass. A record carries the newest article time held "from this job or any earlier
  one", so the newest record alone answers rule 2 when the writer is right; 5 gives margin against one out-of-order write and
  bounds a refresh at 95 x 5 = 475 fetches (16 at a time), against 23 today. A capped company is named in `read["capped"]`.
- **Records keep arriving** (105 objects at 10:06Z, 106 at 10:2xZ). AC2's tolerance: the check lists before and after the
  module's call and compares only names whose folder did not change; it needs 90 or more of 95 compared and 0 differing. Its
  floors (23 with a record, 11 read, the three pilot dates) can only rise, because a record is never overwritten or deleted. If
  a record IS deleted the floor fails, and that is a finding, not a flake.
- **R2 pins 95 covered names.** If the covered list changes size AC2 fails on its count: re-measure, do not edit the number blind.
- **A body whose `security_key` differs from its folder** is used as it parses (0 of 105 today). The module does not check it;
  the writer builds both from one value (`job_record.address`).
- **The bound's pin is a blob id, not a diff against HEAD,** so a worker who edits `collector_record.py` and commits it still fails.
- AC1 clause F0 fails if the module (or anything it imports at its top) loads `pyarrow` or `lib.research.harvest.store`.
- `partition_for` raised for 0 of 95 covered keys (including `WALMEX*_MM_Equity` and the two slash names). The act gives no
  rule for a key it refuses; rule 13's "never raises" still binds, so a worker who meets one reports it.
- The fake store pages two keys at a time, so a module that reads only the first page fails F1.

### 8. Not measured, and questions for the issuer

**THE HOOKUP the adapter cell must make (the issuer's cell; this cell edits none of these files):**

- **H1. Where.** `lib/research/api/scoped_amgt.py`, function `read_coverage_freshness` (line 5787). It builds every freshness
  row. Today: line 5802 lists the whole `seeking-alpha/harvest/bronze/` prefix; line 5807 sets
  `per_vendor["seekingalpha"] = _seeking_alpha_bronze_stamps(...)` (function at line 5670, the four pilot tables); lines 5846
  to 5849 copy it into each row's `per_input["seekingalpha"]`; lines 5853 to 5856 fold it into `last_refreshed`.
- **H2. One call per snapshot refresh.** After `covered_keys` is known (lines 5816 to 5824), call ONCE, outside the row loop:
  `sa = collector_read.seeking_alpha_by_security(covered_keys, client=_pool_client())`. `per_vendor` is built at line 5805,
  before `covered_keys`, so the Seeking Alpha entry moves below line 5824. `read_coverage_freshness` runs inside
  `snapshot.write_freshness_snapshot` (the scheduled `refresh_freshness_snapshot`, line 5951), so this is one listing per
  refresh. The page's read path (`serve_coverage_freshness`, line 5923) reads the stored snapshot and lists nothing; it calls
  `read_coverage_freshness` only on its existing fallback, when no snapshot under 24 hours old can be read.
- **H3. Served fields replaced.**
  - `rows[].per_input.seekingalpha`: `collector_read.compact_stamp(state["last_read"])` when `state["state"] == "read"`,
    otherwise `NEVER`. It MUST be the compact form: `last_refreshed` is a string `max` over stamps shaped `YYYYMMDDTHHMMSSZ`,
    and a dashed time sorts below every compact stamp.
  - `rows[].last_refreshed`: unchanged code, now fed the value above (so the 2026-09-11 pilot stamp leaves it).
  - `denominators.seeking_alpha_bronze_objects_listed` and `reads.seeking_alpha_bronze`: retired with the listing at line 5802
    (`seeking_alpha_bronze_keys` has no other use in the function), replaced by `reads.seeking_alpha_job_record = sa["read"]`
    and `denominators.seeking_alpha_job_record_objects_listed`.
  - `_seeking_alpha_bronze_stamps` and `_SEEKING_ALPHA_BRONZE_TABLES` lose their only caller.
- **H4. Served fields added.** On every covered row, `rows[].seeking_alpha = {"state", "sentence", "last_read",
  "newest_job_finished_at", "newest_job_status"}` copied from the company's entry; `None` on a row that is not covered (the
  module is asked for covered keys only). And `denominators.seeking_alpha_states = {"read": n, "checked": n, "no_record": n,
  "unreadable": n}` over covered rows.
- **H5. The stale rule's inputs.** `stale_rule.annotate_row` reads `per_input.seekingalpha` only. With H3: `read` becomes
  `fresh` or `stale` on the article date; `checked`, `no_record` and `unreadable` become `not_collected` and never flag stale.
  That is right for the FLAG. It is wrong for the WORDS: the page draws "Not collected" for `not_collected`
  (`Freshness.tsx` line 130). For the page body to carry the sentence, `"seeking_alpha"` must join `PAGE_ROW_FIELDS`
  (`lib/research/freshness/page_body.py` line 10), and the page must draw `seeking_alpha.sentence` when `seeking_alpha.state`
  is not `read`. The second half is a portal cell.
- **H6. A failed read never reaches the snapshot.** `_freshness_complete` (line 5912) already refuses a view whose `reads`
  holds a record with `read_completed` false, so with H3 a failed listing leaves the older snapshot in place and `unreadable`
  is served only on the live fallback. No new code is needed for that, only the `reads` entry.
- **H7. The grant comes first.** Add the builder's prefix `seeking-alpha/harvest/state/job_record/` to the role's read list
  (`infra/aws/terraform/harvest/scoped-amgt-api.tf`, the list at lines 176 to 198; both the list and get limbs), applied and
  re-read BEFORE the code leg, under its never-widen pair. Without it the listing is refused in the function, every name
  reads `unreadable`, no snapshot is written, and after 24 hours the page falls back to a slow live view.
- **H8. The deployed check, after the snapshot is re-written** (the scheduled event `{"amgt_scheduled_action":
  "refresh_freshness_snapshot"}`, then `GET /freshness`):
  - `snapshot.generated_at` is after the deploy; `reads.seeking_alpha_job_record.read_completed` is true and its
    `objects_listed` is 105 or more;
  - over rows with `covered` true (95): `seeking_alpha.state` counts sum to 95 with `read` 11 or more, `read` + `checked` 23 or
    more, `no_record` 72 or fewer, `unreadable` 0 (measured today: 11 / 12 / 72 / 0);
  - `per_input.seekingalpha` is a compact stamp exactly on the `read` rows and `NEVER` on the rest; no row's value begins
    `20260911`;
  - BABA_US_Equity, BA_US_Equity, COST_US_Equity read `20261006T231547Z`, `20261007T013347Z`, `20261007T112736Z` or later;
  - on `GET /freshness?view=page`: `rows[].inputs.seekingalpha.state` is `fresh` or `stale` on the `read` rows and
    `not_collected` on the rest; `rows[].seeking_alpha.sentence` is present on 95 of 95; "not collected" is in no sentence.

**Questions for the issuer (each a CTO call unless said):**

- **Q1. C2's condition.** 23 of 95 covered names hold a record. Served today the column would read 11 dates, 12 "checked, no
  article held" and 72 "no collection record is held yet", against 3 false dates and 92 false "Not collected" now. Is 23 of
  95 "records present for the reached names"? The collector's backfill is the only thing that moves the 72, and it is
  AMGT_HARVST's.
- **Q2. The page.** Without a page change 84 of 95 cells read "Not collected", which the contract's rules 3 and 4 forbid.
  Whose cell draws the sentence (DSGN_AMGTV1's amendment per R3, or a portal cell in this issuance)? Until it lands the column
  is truer in the data and unchanged in its words on 84 rows.
- **Q3. The grant.** H7 is read from the terraform at HEAD. The live policy was not simulated; one
  `simulate-principal-policy` on the role for `s3:ListBucket` (prefix condition) and `s3:GetObject` settles it.
- **Q4. A true stale flag that reads oddly.** 992_HK_Equity was checked on 2026-10-07 and found nothing acceptable; its newest
  stored article is 2026-09-22, so the rule flags it stale as "Seeking Alpha last read 2026-09-22". That follows reader rule 2.
  With no daily run, all 11 `read` names go stale about seven trading days after their date (the first around 2026-10-16).
  Whether the flag should key on the article date or on the job's end is an outcome question (FWD-7).
- **Q5. The second reader.** `lib/research/freshness/build_view.py` (the hand-run view) still reads the four pilot tables
  (line 81). A repair in the served reader alone leaves it wrong.

**Not measured:**
- The live IAM policy of the function's role (Q3), and whether `lib/opal_naming` resolves the `seeking-alpha` `state` address
  inside the deployed package (`snapshot.py` already calls the same builder there for source `amgt`; this source and tier were
  called only on this device).
- The function's timeout against a refresh with the added listing and up to 475 fetches; today the added work is one listing
  of about 106 keys and 23 fetches, and the retired listing of `seeking-alpha/harvest/bronze/` (14,951 article partitions at
  the round-78 read) is the larger of the two.
- Per name, why 25 covered names that begin with a digit or A to K hold no record (a job that did not conclude, or no job).
- Whether any of the 81 uncovered folders is another listing of a covered company (for example `AZN_US_Equity` beside covered
  `AZN_LN_Equity`, `IMBBY_US_Equity` beside `IMB_LN_Equity` which reads `checked`). If the collector files a company's articles
  under its US line, the covered line reads `checked` or `no_record` while articles are held. Not traced; it is the writer's
  key choice and may deserve a surprise row from the issuer.
- The page was read from portal `origin/DEV` at d1b21c97 by `git show`; it was not rendered.
- The worker's deliverables folder is not in section 5: the slot number is the issuer's, and the generator adds it.
