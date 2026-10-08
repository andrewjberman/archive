## D1 -- `AMGT-cc-6` -- THE ADAPTER CELL: EVERY HOOKUP OF THE ROUND, AND THE ONLY WRITER OF THE ADAPTER FILE

### 1. MEASURED AT THE BASE

Drafted for `2.0.0_SA_COO~Z`, 2026-10-08 10:3xZ to 10:5xZ, by a drafting subagent of that seat. Shared tree, branch `CLOUD`,
HEAD `d6ea0eff2f` at the dry-runs and `e26aa28d30` at the last read (other seats were committing). No product file was created
or edited; nothing is committed. Store reads were list and GET only; the deployed function was read by GET-shaped invokes only.

**The file the hookups go into did not move under the three sibling drafts.** `lib/research/api/scoped_amgt.py` is blob
`afe19b30ce43` (7,181 lines, last commit `59f820cf17`) at every HEAD read today, the blob GROUP_C names. Each line number the
siblings state was read at that blob:

| sibling claim | read today | verdict |
|---|---|---|
| A2: `read_thesis_bundle` at `:3629`; `resolved_key` `:3648`; `header_figures` `:3650`; `fiscal_year_figures` `:3659` | the same | CONFIRMED |
| A2: `bundle["segment_breakdown"] = read_segment_breakdown(resolved_key or security_key)` at `:3739`; the function-scope import of `section_coverage` at `:3741`; the statement of inputs at `:3746`; `_pool_client` at `:2155` | the same | CONFIRMED |
| A2: `inputs_statement.py:33` says "the segment table" for the filing-text breakdown | `out.append("the segment table")`, line 33 | CONFIRMED |
| C: sibling imports at `:127` to `:137`; `dossier_read` set at `:3655`; `"dossier_fields": _dossier_fields(dossier_read),` at `:3692` | the same | CONFIRMED |
| C: `_read_dossier_document` at `:4992`; unresolved name `:4998`; no notes `:5004`; failed read `:5006` ("dossier read failed: ...") | the same | CONFIRMED |
| C: `_plain_no_block_reasons` at `:1142` | the same; it runs only on the answer for a covered name with no stored company record (`:1127`) | CONFIRMED |
| B: `read_coverage_freshness` at `:5787`; the Seeking Alpha listing at `:5802`; `per_vendor` at `:5805` with its Seeking Alpha entry at `:5807`; `covered_keys` at `:5816` to `:5824`; the per-input copy at `:5846` to `:5849`; `last_refreshed` at `:5853` to `:5856` | the same | CONFIRMED |
| B: `_seeking_alpha_bronze_stamps` at `:5670`; `_freshness_complete` at `:5912`; `serve_coverage_freshness` at `:5923`; `refresh_freshness_snapshot` at `:5951`; `PAGE_ROW_FIELDS` at `page_body.py:10` | the same | CONFIRMED |
| B: the page's read path calls `read_coverage_freshness` only on its fallback | true for the route (`:7023` to `:7040`) | CONFIRMED, with one ADDITION below |

**Four things the sibling drafts did not say, each read at the base:**

1. **A second reader of the retired read record.** `lib/research/api/top_band.py:34` maps the input `seekingalpha` to the
   read record named `seeking_alpha_bronze`, to tell "the store did not answer" from "nothing read" in the statement of inputs
   on `/overlay` (`scoped_amgt.py:3535`) and `/thesis` (`:3746`). GROUP_B retires that record. With the map left as it is, a
   failed read of the collection records would be served on those two routes as "never read". One token moves (hookup 6).
2. **`serve_coverage_freshness` has a second caller.** `_overlay_input_provenance` (`:3369`, call at `:3377`) reads the same
   view on EVERY `/overlay` and `/thesis`. So the Seeking Alpha row of the statement of inputs on those two routes copies the
   freshness row: its `last_run` and `outcome` MOVE when the snapshot is re-written (section 8, "existing values that move").
   And a view with an unfinished read is never held (`:5946`): once the stored snapshot is more than 24 hours old, every
   `/overlay` and `/thesis` builds the whole view again. One build took **9.9 seconds** on this box.
3. **Tests that assert the retired source.** `lib/research/api/tests/test_freshness_harvest_stamps.py` lines 89 to 91 and
   `lib/research/api/tests/test_freshness_covered.py` lines 33 and 41 assert a Seeking Alpha stamp read from the four pilot
   tables' key names, and line 91 asserts the retired denominator. `lib/research/freshness/tests/test_page_body.py` line 23
   asserts each page row's keys equal `PAGE_ROW_FIELDS`, on rows with no `seeking_alpha`.
   `lib/research/api/tests/test_inputs_statement.py` line 38 asserts the phrase "the segment table". All four must be amended
   by this cell or AC3 fails.
4. **Run locally, the page reads the DEPLOYED function's stored snapshot,** not the tree (`/freshness?view=page` through the
   handler on this box answered from `s3://opal-data-harvest/amgt/harvest/state/freshness_snapshot/current/snapshot.json`,
   made 2026-10-08T07:23Z). A local check of the Seeking Alpha column therefore sets the stored snapshot aside in memory;
   `r79_cc6.py` does, and writes nothing.

**The served state today, through the handler** (local and deployed agree):
- `/thesis` for AMD_US_Equity, 8766_JP_Equity, HD_US_Equity, ASML_NA_Equity: HTTP 200; no `segment_table` key; no
  `dossier_sections` key.
- `/freshness?view=page`: 95 rows; no row carries `seeking_alpha`; 3 rows carry a Seeking Alpha stamp, all the pilot's
  (`BABA_US_Equity` `20260911T040221Z`, `BA_US_Equity` `20260911T040304Z`, `COST_US_Equity` `20260911T040346Z`), and all 3
  are flagged stale on it; the other 92 read `NEVER`.
- `/freshness` (default body): 302 rows, 95 covered; 5 top-level keys, 13 denominators, 6 read records, 10 keys per row.
- Names the check pins: 10 of 95 covered names hold no stored segment folder (BABA_US, BA_US, COST_US, HAL_US, HD_US, INTU_US,
  KMB_US, NU_US, SAP_GY, VLO_US; 85 folders listed); 42 of 95 covered names hold research notes with none of the five sections
  (AMD_US_Equity is one of them).
- Both test folders together: `1 failed, 860 passed` (828 and 32). The one failure is
  `lib/research/api/tests/test_harvest_prefixes.py::test_ii_registry_hash_matches`.

### 2. THE ACT (worker face text)

Three cells of this round each built a new module and named a hookup. You make every hookup. You are the ONLY writer of
`lib/research/api/scoped_amgt.py` this round. The three modules are already merged into your worktree's base: read each one
and its tests, whole, before you call it:
`lib/research/api/segment_served.py`, `lib/research/api/dossier_sections.py`, `lib/research/freshness/collector_read.py`.
Each hookup below names the function to find, the place by line number AS MEASURED AT THE CUT, the exact call, and the effect.
Line numbers may have moved by a few lines: find the named function and the quoted line, never the number alone.

1. **The Bloomberg segment table on the thesis route.** In `read_thesis_bundle` (defined at `:3629`), find the line
   `bundle["segment_breakdown"] = read_segment_breakdown(resolved_key or security_key)` (`:3739`). Directly after it, and
   before the line `from lib.research.filings import section_coverage`, add these two lines, the import INSIDE the function:

       from lib.research.api import segment_served
       bundle["segment_table"] = segment_served.serve_segment_table(resolved_key or security_key, fiscal_year_figures, header_figures, client=_pool_client())

   `fiscal_year_figures` (`:3659`) and `header_figures` (`:3650`) are the names already in the function. Pass that
   `header_figures`, the stored list, not the plain-country copy the bundle serves. Effect: ONE new key, `segment_table`,
   beside `segment_breakdown`. Do not change `segment_breakdown` or anything that reads it.

2. **The five research-note sections on the thesis route.**
   (a) Beside the imports at `:134` to `:137`, add: `from lib.research.api import dossier_sections`
   (b) In `read_thesis_bundle`, inside the `bundle = {` literal, directly after the line
   `"dossier_fields": _dossier_fields(dossier_read),` (`:3692`), add this one line:

       "dossier_sections": dossier_sections.dossier_sections(dossier_read[0], read_failed=dossier_read[0] is None and str(dossier_read[1] or "").startswith("dossier read failed")),

   `dossier_read` is the pair already set at `:3655`. Make NO second read of the notes. Give no variable the name
   `dossier_sections`. Effect: ONE new key, `dossier_sections`, a list of five.

3. **The Seeking Alpha column, read from the collector's records.** All of this is in `read_coverage_freshness` (`:5787`).
   (a) Beside the import on the function's first line (`:5794`), add, INSIDE the function:
       `from lib.research.freshness import collector_read`
   (b) Delete the line `seeking_alpha_bronze_keys, seeking_alpha_bronze_record = _pool_keys(SEEKING_ALPHA_BRONZE_PREFIX)`
       (`:5802`) and, in the `per_vendor = {` literal, the line `"seekingalpha": _seeking_alpha_bronze_stamps(seeking_alpha_bronze_keys),`
       (`:5807`).
   (c) Directly after the line `covered_set = set(covered_keys)` (`:5824`), OUTSIDE every loop, add:

       seeking_alpha_read = collector_read.seeking_alpha_by_security(covered_keys, client=_pool_client())
       seeking_alpha_by_key = seeking_alpha_read["by_security"]
       seeking_alpha_stamps: Dict[str, str] = {}
       for covered_key, entry in seeking_alpha_by_key.items():
           stamp = collector_read.compact_stamp(entry.get("last_read")) if entry.get("state") == "read" else None
           if stamp:
               seeking_alpha_stamps[covered_key] = stamp
       per_vendor["seekingalpha"] = seeking_alpha_stamps
       seeking_alpha_states = {"read": 0, "checked": 0, "no_record": 0, "unreadable": 0}

       Call the reader by that dotted name, `collector_read.seeking_alpha_by_security`, exactly ONCE in the function. The
       stamp MUST be the compact form (`20261007T013241Z`): `last_refreshed` is a text `max` over stamps of that form.
   (d) In the row loop, after `security_key_value` is known, add:

       seeking_alpha_entry = seeking_alpha_by_key.get(security_key_value) if security_key_value in covered_set else None
       if seeking_alpha_entry is not None and seeking_alpha_entry.get("state") in seeking_alpha_states:
           seeking_alpha_states[seeking_alpha_entry["state"]] += 1

       and in the row dictionary (`rows.append({...})`, `:5863`), after the `"pack"` entry, add ONE key:

       "seeking_alpha": None if seeking_alpha_entry is None else {name: seeking_alpha_entry.get(name) for name in ("state", "sentence", "last_read", "newest_job_finished_at", "newest_job_status")},

       Change nothing else in the loop: the per-input copy and `last_refreshed` keep their code and now read the value of (c).
   (e) In the returned `"denominators"`: delete the `"seeking_alpha_bronze_objects_listed"` line (`:5891`) and add
       `"seeking_alpha_job_record_objects_listed": seeking_alpha_read["read"].get("objects_listed", 0),` and
       `"seeking_alpha_states": seeking_alpha_states,`
   (f) In the returned `"reads"`: delete the `"seeking_alpha_bronze"` line (`:5900`) and add
       `"seeking_alpha_job_record": seeking_alpha_read["read"],`
   (g) Leave `_seeking_alpha_bronze_stamps` (`:5670`), `_SEEKING_ALPHA_BRONZE_TABLES` and `SEEKING_ALPHA_BRONZE_PREFIX`
       where they are; they now have no caller in this file. Add one comment line above `_seeking_alpha_bronze_stamps` saying
       so and naming this cell. Deleting them is not this cell's.
   What this hookup must and must not do:
   - ONE listing of the records per build of the view. The view is built by the scheduled snapshot refresh
     (`refresh_freshness_snapshot`, `:5951`). The page's request (`serve_coverage_freshness`, `:5923`, and the route at
     `:7023`) reads the stored snapshot with one GET and lists nothing; do not add a call of the reader there, in the route,
     or anywhere outside `read_coverage_freshness`.
   - A failed read never writes a snapshot. You add NO code for that: `_freshness_complete` (`:5912`) already refuses a view
     whose `reads` holds a record with `read_completed` false, and (f) puts the reader's own record there. Do not edit
     `_freshness_complete`, `serve_coverage_freshness`, `refresh_freshness_snapshot`, `lib/research/freshness/snapshot.py` or
     `lib/research/freshness/stale_rule.py`.
   - The three states stay apart: a row whose state is `checked`, `no_record` or `unreadable` gets NO stamp (so it reads
     `NEVER` and is never flagged stale), and keeps its own `state` and `sentence` in `seeking_alpha`.

4. **The page view carries the new field.** In `lib/research/freshness/page_body.py` line 10, `PAGE_ROW_FIELDS` gains
   `"seeking_alpha"` as its LAST entry. Nothing else in that file changes.

5. **One phrase that would name the wrong block.** In `lib/research/api/inputs_statement.py` line 33, change
   `out.append("the segment table")` to `out.append("the segment breakdown")`. That line speaks of the breakdown read from
   the company filing (the key `segment_breakdown`); from this round `segment_table` is Bloomberg's table. Change that one
   string and nothing else in the file: the statement of inputs gains no row and no other word.

6. **The statement of inputs reads the new read record.** In `lib/research/api/top_band.py` line 34, in `INPUT_SOURCES`, the
   second item of the `"seekingalpha"` entry changes from `"seeking_alpha_bronze"` to `"seeking_alpha_job_record"`. The first
   item (the plain sentence) does not change.

7. **Tests** (in `lib/research/api/tests/` and `lib/research/freshness/tests/`):
   - `test_freshness_harvest_stamps.py`: rewrite `test_seekingalpha_reads_new_grammar_key_names_never_article_never_getobject`
     for the new source. Put collector records in the fake store under the address the module builds
     (`collector_read.job_record_location()`; type no bucket or prefix), make the two names covered (patch
     `covered_security_keys` the way `test_freshness_covered.py` does), and assert: the stamp is the compact form of the
     record's newest article time; the pilot-table key names no longer make a stamp; the new denominator equals the records
     listed. Keep the other two tests of the file as they are.
   - `test_freshness_covered.py`: the two tests that plant a pilot-table key (lines 29 to 41) plant a collector record instead
     and assert its compact stamp.
   - `test_page_body.py`: give the fixture's rows a `seeking_alpha` value so the key-set assertion at line 23 holds.
   - `test_inputs_statement.py` line 38: the expected phrase becomes `"the segment breakdown"`.
   - ADD plant tests, no network: (i) the thesis bundle carries `segment_table` and `dossier_sections` (patch the two module
     functions with recorders: each called once, with the arguments named above); (ii) the reader is called exactly once per
     `read_coverage_freshness`; (iii) a covered row of each of the four states carries `seeking_alpha` with the five keys, and
     only the `read` row carries a stamp; a row that is not covered carries `seeking_alpha` None; (iv) with the reader
     returning `read_completed` false, `_freshness_complete(view)` is false; (v) in `test_top_band_provenance.py`, a view whose
     `reads.seeking_alpha_job_record.read_completed` is false and whose row reads `NEVER` gives the outcome `failed`.

**What must NOT change.**
- On `/overlay` and `/thesis`: every key served today keeps its name and its value. You ADD two keys on `/thesis`
  (`segment_table`, `dossier_sections`) and none on `/overlay`. The two exceptions are named and are the whole list: the one
  phrase of hookup 5, and the Seeking Alpha row of the statement of inputs, which copies the freshness row.
- The round-78 hookups (the coverage marker, the plain country, the one statement of inputs, the officer rank, the source
  names, the peer price listing): untouched. Criterion AC2 reads them.
- The default `/freshness` body: every other field keeps its name and meaning. The whole change is: two keys retired
  (`denominators.seeking_alpha_bronze_objects_listed`, `reads.seeking_alpha_bronze`), three added
  (`denominators.seeking_alpha_job_record_objects_listed`, `denominators.seeking_alpha_states`,
  `reads.seeking_alpha_job_record`), one key added per row (`seeking_alpha`), and the SOURCE of `per_input.seekingalpha`.
- No `.tf` file. The function's permission to read the collector's records is another cell's. You deploy nothing, write to no
  store, send no scheduled event, and call no vendor, web or model service.
- You do not edit the three sibling modules, `segment_table.py`, `segment_period.py`, `collector_record.py`,
  `lib/research/freshness/build_view.py` or `lib/research/corpus/dossier.py`.

Run both test folders before your commit and report the last line. Report also: the seconds one `/thesis` took before and
after on `AMD_US_Equity`; the state counts criterion AC1 prints; and anything the three modules did that this text did not
foresee (file a surprise row for it and keep working; do not bend a hookup to fit).

### 3. THE CRITERIA
- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc6.py" --crit AC1 --where local; echo "exit=$?"`
  Expect: the thesis serves the Bloomberg segment table for AMD US with its first column named fiscal year 2025 in USD, serves 8766 JP with its first column unnamed and a note, and reads a plain reason where no table is stored; it serves the five research-note sections for ASML NA in order and five absent entries with reasons for AMD US; every covered freshness row carries a Seeking Alpha state and sentence, no row that is not read carries a date or a stale flag, no date is 2026-09-11; the default freshness body keeps every other field; one build asks the record reader once, a page request answered from a snapshot asks it not at all, and a failed read writes no snapshot; H1-H4, H5a-H5d, K1 and L1-L3 PASS; R79 CC6 AC1 SERVED: YES; and exit=0
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc6.py" --crit AC2 --where local; echo "exit=$?"`
  Expect: the round-78 served shape still reads YES on the tree (its six clauses pass); B1 PASS; R79 CC6 AC2 SERVED: YES; and exit=0
- **AC3** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round79/checks/r79_cc6.py" --crit AC3 --where local; echo "exit=$?"`
  Expect: lib/research/api/tests/ and lib/research/freshness/tests/ show 860 or more passed, no error, and no failure other than the allowed test_harvest_prefixes.py::test_ii_registry_hash_matches, which the check prints; B1 PASS; R79 CC6 AC3 SERVED: YES; and exit=0

### 4. THE BASE DRY-RUN

`bash .tools/commit-gate.sh` on the check file: `OK: pre-commit gate clean for 1 of 1 file(s)`, exit 0. The check is ASCII
with LF endings (0 characters above 127, 0 carriage returns). At the base AC1 FAILS for the right reason (the keys are
absent and the reader is not called) and both bounds PASS. Literal, HEAD `d6ea0eff2f`, standard error not shown:

```
== BASE AC1 local ==
FAIL H1 the thesis serves the Bloomberg segment table with its first column named and its currency AMD_US_Equity http 200; segment_table ABSENT; status None; rows 0; first column None None; currency None units None
FAIL H2 a first column that ties to no year is served unnamed with its note, and no stored table reads a plain reason 8766_JP_Equity http 200 status None rows 0 first column None year None note None; HD_US_Equity http 200 status None reason None
FAIL H3 the thesis serves the five research-note sections in the fixed order, the first with its stored text ASML_NA_Equity http 200; dossier_sections ABSENT; fields []; first status None; text opens ''
FAIL H4 a name whose notes hold none of the five serves five absent entries, each with a plain reason AMD_US_Equity dossier_sections ABSENT; statuses []; first reason None
   lib.research.freshness.collector_read does not import: ImportError: cannot import name 'collector_read' from 'lib.research.freshness' (C:\Users/Opal Bloomberg/Desktop/ajb_workspace\lib\research\freshness\__init__.py)
   freshness page http 200; rows 95; view made 2026-10-08T10:49Z; answered from no stored snapshot (the view was worked out now) {"object": null, "reason": "this check set the stored snapshot aside to read the tree's own view; this view was worked out from the stores just now, so it may be slow"}
   Seeking Alpha states over 95 rows: {"null": 95}
FAIL H5a every covered row carries a Seeking Alpha state and its sentence 0 of 95 rows (covered names at the draft 95); sentences saying not collected 0
FAIL H5b every state is one of read, checked, no_record, unreadable off the list 95 [('1299_HK_Equity', None), ('2317_TT_Equity', None), ('8035_JP_Equity', None)]
FAIL H5c a row that is not read carries no date and is not flagged stale; a read row carries a compact stamp flagged stale 3 [('BABA_US_Equity', None), ('BA_US_Equity', None), ('COST_US_Equity', None)]; dated 3 [('BABA_US_Equity', None, '20260911T040221Z'), ('BA_US_Equity', None, '20260911T040304Z'), ('COST_US_Equity', None, '20260911T040346Z')]; read rows without the compact stamp of their date 0 []
FAIL H5d no served Seeking Alpha date is the pilot's 2026-09-11 rows dated 2026-09-11: 3 ['BABA_US_Equity', 'BA_US_Equity', 'COST_US_Equity']
FAIL K1 the default freshness body keeps every other field, carries the three added and not the two retired http 200; rows 302 (covered 95); fields lost []; row fields lost [], unexpected []; retired still served ['denominators.seeking_alpha_bronze_objects_listed', 'reads.seeking_alpha_bronze']; added not served ['denominators.seeking_alpha_job_record_objects_listed', 'denominators.seeking_alpha_states', 'reads.seeking_alpha_job_record']; state counts {}; rows not covered that carry the field 0; record read finished None, objects listed None
FAIL L1 one build of the view asks the record reader once calls after the first build 0; after the second request 0 (1 when the view was held, 2 when built again)
FAIL L2 a page request answered from a stored snapshot asks the record reader not at all http 200; calls before 0, after 0; answered from a snapshot True; rows 95
FAIL L3 a record read that fails writes no snapshot, and every covered row reads unreadable with no date raised None; written True; writes attempted 1; unreadable with no date 0 of 95 covered rows; said None
R79 CC6 AC1 SERVED: NO
exit=1      -> FAIL as expected (build: no hookup is made). L3's "writes attempted 1" is a write to the check's recording stand-in, not to the store.

== BASE AC2 local ==
   PASS H1 a covered name reads covered and a pool name outside coverage says so once AMD_US_Equity: 'covered'; MSFT_US_Equity: 'outside_coverage'
   PASS H2 the country reads in plain case with the stored text beside it value 'United States' stored 'UNITED STATES'
   PASS H3 the thesis carries one statement of inputs with one filings row before the pack row rows ['bloomberg', 'seekingalpha', 'serp', 'filings', 'pac
   PASS H4 a chief-executive row leads every sampled roster that holds one 6 of 6 rosters with such a row
   PASS H5 every provenance entry carries a plain source name key 3 of 3
   PASS H6 no sampled peer row is served a United States record's currency behind a foreign price rows read 60, wrong 0 []
PASS B1 the round-78 served shape still reads YES on the tree rc=0; clauses passing 6 of 6; R78 BB17 AC1 SERVED: YES
R79 CC6 AC2 SERVED: YES
exit=0      -> PASS as expected (bound; 54 seconds)

== BASE AC3 local ==
   1 failed, 860 passed, 297 warnings in 29.30s
   failures allowed, known at the draft and another cell's to repair: ['lib/research/api/tests/test_harvest_prefixes.py::test_ii_registry_hash_matches']
PASS B1 both test folders pass apart from the allowed failures rc=1; passed 860 (at the draft 860); failed ['lib/research/api/tests/test_harvest_prefixes.py::test_ii_registry_hash_matches']; of them not allowed []; errors []
R79 CC6 AC3 SERVED: YES
exit=0      -> PASS as expected (bound)

== BASE AC1 deployed (the line the redeploy's list carries; read-only invokes; H1-H4 and H5b-K1 read as in the local run) ==
FAIL H1 ... AMD_US_Equity http 200; segment_table ABSENT; ...
FAIL H2 ... FAIL H3 ... FAIL H4 ...
   freshness page http 200; rows 95; view made 2026-10-08T07:23Z; answered from the stored snapshot {"age_hours": 3.49, "generated_at": "2026-10-08T07:23Z", "object": "s3://opal-data-harvest/amgt/harvest/state/freshness_snapshot/current/snapshot.json"}
   Seeking Alpha states over 95 rows: {"null": 95}
FAIL H5a every covered row carries a Seeking Alpha state and its sentence 0 of 95 rows (covered names at the draft 95); sentences saying not collected 0
FAIL H5b every state is one of read, checked, no_record off the list 95 [('1299_HK_Equity', None), ('2317_TT_Equity', None), ('8035_JP_Equity', None)]
FAIL H5c ... FAIL H5d ... FAIL K1 ...
   L1-L3 (the wiring) are read on the tree only: run --where local
R79 CC6 AC1 SERVED: NO
exit=1      -> FAIL as expected (the deployed package holds no hookup)
```

REACHABLE. The same check file, run in-process from a scratch script OUTSIDE the repo. The three sibling modules were placed
in memory under their names as stand-ins written from the sibling notes' section 2 alone, and the hookups of section 2 above
were made in memory by wrapping `read_thesis_bundle` and `read_coverage_freshness` and extending `PAGE_ROW_FIELDS`. No repo
file was written (`git status --porcelain -- lib/` is empty after it). Every clause passes. Literal:

```
== STUB AC1 local ==
PASS H1 the thesis serves the Bloomberg segment table with its first column named and its currency AMD_US_Equity http 200; segment_table present; status 'served'; rows 6; first column 'Fiscal year 2025' '2025'; currency 'USD' units 'millions'
PASS H2 a first column that ties to no year is served unnamed with its note, and no stored table reads a plain reason 8766_JP_Equity http 200 status 'served' rows 6 first column 'Period 1' year None note "The rows of this column do not add up to the company's reported revenue for any year we hold, so the year is not stated."; HD_US_Equity http 200 status 'none' reason 'No Bloomberg segment table has been stored for this name yet.'
PASS H3 the thesis serves the five research-note sections in the fixed order, the first with its stored text ASML_NA_Equity http 200; dossier_sections present (5); fields ['company_description', 'why_we_own', 'positives', 'negatives', 'special_items']; first status 'served'; text opens 'COMPANY DESCRIPTION:What started as a failing joint venture'
PASS H4 a name whose notes hold none of the five serves five absent entries, each with a plain reason AMD_US_Equity dossier_sections present (5); statuses ['absent', 'absent', 'absent', 'absent', 'absent']; first reason 'No research report we hold for this company has a "Company description" section.'
   freshness page http 200; rows 95; view made 2026-10-08T10:54Z; answered from no stored snapshot (the view was worked out now) {"object": null, "reason": "this check set the stored snapshot aside to read the tree's own view; this view was worked out from the stores just now, so it may be slow"}
   Seeking Alpha states over 95 rows: {"checked": 13, "no_record": 71, "read": 11}
PASS H5a every covered row carries a Seeking Alpha state and its sentence 95 of 95 rows (covered names at the draft 95); sentences saying not collected 0
PASS H5b every state is one of read, checked, no_record, unreadable off the list 0 []
PASS H5c a row that is not read carries no date and is not flagged stale; a read row carries a compact stamp flagged stale 0 []; dated 0 []; read rows without the compact stamp of their date 0 []
PASS H5d no served Seeking Alpha date is the pilot's 2026-09-11 rows dated 2026-09-11: 0 []
PASS K1 the default freshness body keeps every other field, carries the three added and not the two retired http 200; rows 302 (covered 95); fields lost []; row fields lost [], unexpected []; retired still served []; added not served []; state counts {"checked": 13, "no_record": 71, "read": 11, "unreadable": 0}; rows not covered that carry the field 0; record read finished True, objects listed 108
PASS L1 one build of the view asks the record reader once calls after the first build 1; after the second request 1 (1 when the view was held, 2 when built again)
PASS L2 a page request answered from a stored snapshot asks the record reader not at all http 200; calls before 1, after 1; answered from a snapshot True; rows 95
PASS L3 a record read that fails writes no snapshot, and every covered row reads unreadable with no date raised None; written False; writes attempted 0; unreadable with no date 95 of 95 covered rows; said 'a store read did not finish, so the snapshot was left as it was'
R79 CC6 AC1 SERVED: YES
stub exit=0
```

### 5. `<paths>`

```
lib/research/api/scoped_amgt.py
lib/research/api/inputs_statement.py
lib/research/api/top_band.py
lib/research/freshness/page_body.py
lib/research/api/tests/
lib/research/freshness/tests/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

### 6. Risk and class

- `<risk>`: LOCAL for this cell. It edits four product files and tests, no `.tf`, no route list; it deploys nothing, writes to
  no store and sends no scheduled event. AC1 reads `s3://opal-data-harvest` (list and GET) with the device's credentials and
  makes its one "write" against a recording stand-in in memory. Egress class NONE.
- The SERVED act is the redeploy's and its never-widen pair's, not this cell's. Section 8 holds the list for the pair.
- `<worker_class>`: `worker`. About 30 product lines in four files, but four existing test files to amend, five plant tests
  to add, and the round's only edit of the 7,181-line adapter.

### 7. Edges

- **Inbound.** Cut AFTER `AMGT-cc-2`, `AMGT-cc-3` and `AMGT-cc-4` drain: their three modules must be in this cell's base.
  `AMGT-cc-1` is not an edge (the segment reader is called by name and works with either walk).
- **Outbound.** The redeploy follows this cell. The cell that grants the function list and get on the collector's records
  must be APPLIED before the redeploy's code leg (GROUP_B H7). Without the grant the scheduled refresh cannot finish its
  read, writes no snapshot, the stored snapshot ages past 24 hours, and from then on every `/freshness`, `/overlay` and
  `/thesis` request builds the whole view again (9.9 seconds on this box), because an unfinished view is never held.
- **AC1 `--where deployed` is not one of the three criteria; it is the line the redeploy's list carries.** Its H5 and K1 read
  NO until the scheduled event `{"amgt_scheduled_action": "refresh_freshness_snapshot"}` has run on the new code, because the
  page reads the stored snapshot. Order for the redeploy: deploy, the snapshot event, then the deployed line. H5 prints the
  snapshot's stamp. The check never sends the event.
- **Names the check pins, and what moves them.** `HD_US_Equity` holds no stored segment folder today (one of 10 covered
  names); a Bloomberg segments pull for it turns H2's second half to `served` and fails the clause for a reason that is not
  the worker's: swap `NO_TABLE_NAME` for another of the 10. `AMD_US_Equity` holds notes with none of the five sections (one of
  42); a re-mint by AMGT_CORPUS that gives it one fails H4: swap `NO_SECTIONS_NAME`. H5a pins 95 covered names, as GROUP_B's
  check does: re-measure if the covered list changes size, do not edit the number blind.
- **H5d refuses every Seeking Alpha date of 2026-09-11.** A collector record whose newest stored article is truly of that day
  would fail it. None reads so today (the oldest `read` date is 2026-09-22).
- **Local `unreadable` is accepted** (the issuer's rule): on a box that cannot list the records, H5a to H5d pass with every
  row `unreadable` and prove the shape only. The state counts are printed; a local run with `unreadable` above 0 is not
  evidence of the column. `--where deployed` does not accept it.
- **AC3's floor is 860 passed,** the count at this draft. The sibling cells add tests before this cell is cut, so the count
  can only be higher; the issuer may raise `PASSED_AT_THE_DRAFT` at the cut. If the sibling repair cell regenerates the stale
  hash first, the allowed failure simply stops failing and AC3 still passes.
- **Rows that are not covered** read `NEVER` for Seeking Alpha after this cell (the reader is asked for covered names only),
  where today a pilot-table key would give them a stamp. No such row holds one today (the 3 pilot stamps are all covered).
- AC1 local makes four thesis reads and two builds of the view (about a minute on this box, not timed to the second); AC2 took 54 seconds and AC3 about 30.

### 8. Not measured, and questions for the issuer

**FOR THE NEVER-WIDEN PAIR OF THE REDEPLOY (ruling R1: the pair lists the hookups by name).**

Hookups, by name:
1. `segment_served.serve_segment_table` called in `scoped_amgt.read_thesis_bundle`, served on `GET /security/<name>/thesis`
   under `segment_table` (cell `AMGT-cc-2`'s module; it reads through `segment_table.read_segment_table`, cell `AMGT-cc-1`).
2. `dossier_sections.dossier_sections` called in `scoped_amgt.read_thesis_bundle`, served on `/thesis` under
   `dossier_sections` (cell `AMGT-cc-4`'s module; no new store read).
3. `collector_read.seeking_alpha_by_security` and `collector_read.compact_stamp` called in
   `scoped_amgt.read_coverage_freshness`, served on `GET /freshness` and written into the stored snapshot by the scheduled
   `refresh_freshness_snapshot` (cell `AMGT-cc-3`'s module). It REPLACES the listing of `seeking-alpha/harvest/bronze/`.
4. `page_body.PAGE_ROW_FIELDS` gains `seeking_alpha`, served on `GET /freshness?view=page`.
5. `inputs_statement._uses`: the phrase "the segment table" becomes "the segment breakdown" on `/thesis`.
6. `top_band.INPUT_SOURCES["seekingalpha"]` reads the read record `seeking_alpha_job_record`, on `/overlay` and `/thesis`.

Files of the deployed package whose bytes change: `scoped_amgt.py`, `inputs_statement.py`, `top_band.py`,
`freshness/page_body.py` (this cell); `segment_served.py`, `dossier_sections.py`, `freshness/collector_read.py` (new);
`segment_table.py` (cc-1).

Served fields ADDED:
- `/thesis`: `segment_table` with `status`, `rows`, `operating_income_rows`, `periods` (each `period`, `label`,
  `fiscal_year`, `top_level_sum`, `note`), `period_note`, `currency`, `units`, `currency_note`, `reason`, `source`.
- `/thesis`: `dossier_sections`, five entries, each `field`, `heading`, `status`, `text`, `reason`, `citation`.
- `/freshness` (default body and the stored snapshot): `rows[].seeking_alpha` (None on a row that is not covered, else
  `state`, `sentence`, `last_read`, `newest_job_finished_at`, `newest_job_status`);
  `denominators.seeking_alpha_job_record_objects_listed`; `denominators.seeking_alpha_states` (`read`, `checked`,
  `no_record`, `unreadable`); `reads.seeking_alpha_job_record` (the reader's own record of 14 keys).
- `/freshness?view=page`: `rows[].seeking_alpha` (the same five keys).

Served fields RETIRED (default `/freshness` body only): `denominators.seeking_alpha_bronze_objects_listed`,
`reads.seeking_alpha_bronze`. No file under `portal/src` reads either (one search of that folder, 0 hits).

EXISTING served values that MOVE (the whole list; each moves only when the snapshot is re-written, except the phrase):
- `/freshness` and its page view: `rows[].per_input.seekingalpha` for the 3 pilot rows (BABA_US, BA_US, COST_US: from
  `20260911T04....Z` to the record's date) and for the other `read` rows (from `NEVER` to a compact stamp: 8 today);
  `rows[].last_refreshed` where that stamp is the row's greatest; and on the page view the rule's outputs that follow from
  it (`inputs.seekingalpha`, `stale_inputs`, `stale`, `keyed_date`, `stale_reason`). Today 3 rows are flagged stale on the
  pilot date; after, those 3 are not, and 992_HK_Equity is (GROUP_B Q4).
- `/overlay` and `/thesis`: the Seeking Alpha row of `input_provenance` (`last_run`, `outcome`, `reason`) for the same rows,
  because it copies the freshness row.
- `/thesis`: in the filings row of `input_provenance`, `used_for` and the `reason` sentence say "the segment breakdown"
  where they said "the segment table", for a name whose filing breakdown has rows.

**Questions for the issuer.**
- **Q1. `lib/research/api/top_band.py` is a path this draft ADDS to the list it was given** (hookup 6, one token). Strike
  hookup 6, the path and plant test (v) if the path may not widen. The cost of striking: on `/overlay` and `/thesis` a failed
  read of the collector's records is then served as "never read", with the sentence "nothing has been read from this input
  for this name yet", on the live fallback only.
- **Q2. The wording of hookup 5 is a drafting choice.** "the segment breakdown" matches the served key `segment_breakdown`
  and is the smallest edit: one string. It changes one existing served phrase on `/thesis`, named above. The alternative
  (leave it, and let R3's page amendment settle the words) leaves one phrase naming two blocks once `segment_table` is served.
- **Q3. A `checked` name still reads "never read" in the statement of inputs** on `/overlay` and `/thesis` ("nothing has been
  read from this input for this name yet"): the statement copies the stamp, and a checked name has none. Carrying the three
  states into that statement is a change to `top_band.input_provenance` and belongs with ruling R3's one statement of inputs;
  this cell does not do it. It deserves a surprise row from the issuer (the channel is outside my write set).
- **Q4. The page still draws "Not collected"** for the 84 rows that are not `read` until a page cell draws
  `seeking_alpha.sentence` (GROUP_B Q2). This cell serves the field; it changes no page.
- **Q5. The three functions and constants left without a caller** (hookup 3g) are left in place on purpose. Say if the cell
  should delete them; `lib/research/freshness/build_view.py` still reads the pilot tables either way (GROUP_B Q5).

**Not measured.**
- **The worker's hookups.** They do not exist; the modules do not exist. What ran is my stand-ins of the three modules and my
  in-memory wrappers, both written from the sibling notes. The stub run proves each clause of the check can read YES and that
  the names and shapes the three drafts state fit together through the handler. It proves nothing about the code the
  workers will write.
- **The deployed function's permission** on the collector's records and on the segments folder: read from the terraform file
  at HEAD only (lines 178 and 179 list the Seeking Alpha `bronze/` and `silver/` prefixes and no `state/` prefix); the live
  policy was not simulated.
- **The deployed package**: that `segment_served` (which loads `lib.research.harvest.store` and `pyarrow` on first use) and
  `collector_read` (which calls `lib.opal_naming`) import and resolve inside it. The redeploy's import check answers it.
- **Time.** The added time of one listing and one body on `/thesis`, and of one listing and up to 475 record reads in the
  scheduled refresh, from the function. On this box one whole build of the view took 9.9 seconds before the change; the
  retired listing of `seeking-alpha/harvest/bronze/` is the larger of the two listings.
- **The page.** Nothing was rendered; no file under `portal/` was read beyond one search for the two retired key names and
  the phrase.
- **Readers of the retired keys outside `lib/` and `portal/src`** (a notebook, a dashboard, another project's check): not
  searched. Inside `lib/`: `top_band.py:34` (hookup 6) and three test files (hookup 7), and no other.
- **A covered name listed twice in the universe file** would be counted twice in `seeking_alpha_states`, as it is in every
  other per-row count of the view. Not looked for; today the view holds 95 covered rows for 95 covered names.
- `AMGT-cc-1`'s walk was not in the tree, so H1 and H2 read the segment reader as it stands (five objects).
- The CTO's ruling on the Seeking Alpha column was read as the issuer quoted it; the message itself was not read.
- The worker's deliverables folder is not in section 5: the slot number is the issuer's, and the generator adds it.
