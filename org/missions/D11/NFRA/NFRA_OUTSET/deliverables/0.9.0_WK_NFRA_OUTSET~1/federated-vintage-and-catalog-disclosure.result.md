# NFRA_OUTSET.TO-OS-s-4 -- RESULT: every `comp-heat federated` answer carries the catalogs joined and each one's BUILD time

**Assignee:** `0.9.0_WK_NFRA_OUTSET~1` (L7 worker subagent of `2.0.0_SA_COO`, spine v3)
**Branch:** `wk-OUTSET-1` (linked worktree `C:\tmp\wk-OUTSET-1`) · **Base:** CLOUD `b630052d6a`
**Cell:** `OS-s-4` · **outcome_ref:** FWD-2 · **verb:** fix · **depends_on:** `OS-s-1`

---

## 1. WHAT WAS MEASURED FIRST

`comp-heat federated` at `b630052d6a` printed a budget disclosure, a refusal-or-result, and nothing
about WHAT it had read. The cell's own words: *"`federated` runs rc 0 in 86 s over a 374-file
histogram with NO vintage line and NO catalog list."*

Two facts about the invocation this order names, both established before any edit:

1. **`--budget 120` never reaches the live plane.** `comp-heat`'s own
   `FEDERATED_LIVE_FLOOR_S` is 200 s (`_trino_fed.py`: "~3-4 min/call"), so 120 < 200 fires the
   refuse-before-dispatch guard. The criterion's invocation therefore had to be satisfied WITHOUT
   dispatching a Trino query -- **and it should be**: an artifact's build time is a property of the
   artifact, not of whether this process got as far as querying it. The vintage block runs on BOTH
   paths, which is also the only way a bounded caller ever sees it.
2. **The catalogs are two, and they are not equally reachable.** `_trino_fed.py:20-23` declares
   `iceberg.globgrph.graph_nodes` (Nessie-backed) and `code_heat.globgrph.code_heat` (Glue over
   parquet).

## 2. WHAT CHANGED

**`org/modules/heatmap/federated_vintage.py`** (new engine module, ~300 lines)

- `tables_in_sql()` -- the table list is **derived from the SQL about to run**, not recited from a
  constant. A `--sql` caller joins whatever it joins; a vintage block reciting the DEFAULT query's
  catalogs beside a custom query's answer would be a well-formed lie.
- `CATALOG_REGISTRY` -- a declared registry with per-catalog resolution kind. **An unregistered
  catalog is answered `absent` with that reason and its location is never guessed.**
- `resolve_location()` -- returns the location AND `how` it was resolved, because a live
  `glue:GetTable` read and a directory-naming convention do not deserve the same trust and the
  output must not present them as if they did.
- `_artifact_build_time()` / `_probe_prefix()` -- `max(s3 LastModified)` over the resolved prefix,
  **returned only when the listing COMPLETED**.
- `render_vintage()` -- the `VINTAGE:` block, one line per table, each carrying `claim=measured` or
  `claim=absent` plus its instrument or its reason, and a final line printing the query clock
  explicitly labelled as **not** a vintage.

**`.tools/comp-heat`** -- `_federated_sqls()` resolves the SQL once and feeds BOTH the vintage block
and the dispatch, so the catalogs disclosed are provably the catalogs joined rather than a second
list that could drift from the first. `_print_federated_vintage()` is called on the refuse path and
on the dispatch path.

**`.tools/tests/test_os4_federated_vintage.py`** -- new, 9 arms, 9/9 PASS.

### 2.1 THE TRAP THIS DESIGN EXISTS TO AVOID, and it was live on this estate

The obvious implementation reads the catalog's own metadata for a timestamp. On this estate that
returns a **plausible, well-formed, sixteen-day-wrong answer**:

| carrier | value | what it actually times |
|---|---|---|
| `glue get-table globgrph.code_heat` -> `UpdateTime` | **2026-06-29T20:34:47Z** | when the CATALOG ROW last changed |
| `s3` `max(LastModified)` under that table's own `StorageDescriptor.Location` | **2026-07-16T03:40:46Z** | when the DATA last landed |

Both measured live 2026-09-05; they disagree by 16.3 days. This module therefore uses Glue **only to
resolve a location** and never as a time source, and battery arm B is built on exactly that
disagreement so the distinction is enforced by a test rather than by a comment.

This is the same class as the sibling finding on `OS-s-8` (a consumer read `class` where the
producer emits `band`; a join keyed on `os.path.basename` matched 0 of 1774) -- neither raised, both
produced a confident well-formed zero. Two controls answer it directly:

- **Field names are proven against what the producer emits.** Every field read
  (`StorageDescriptor.Location`, `Contents[].LastModified`, `CommonPrefixes[].Prefix`) was read live
  and returned a non-empty value before being relied on.
- **The join is proven non-zero on a case known to exist.** The `<table>_<uuid>/` convention that
  locates a Nessie table is exercised in arm C against the REAL 11 child prefixes of the warehouse
  root: `graph_nodes` -> **1 of 11**, with a negative control (`no_such_table` -> 0 matches ->
  `absent` with the match count, never a guess). A match count that is not exactly 1 refuses.

### 2.2 A MAX OVER A TRUNCATED LISTING IS NOT A MAXIMUM

S3 lists lexicographically, not by time, so the newest object can be on any page. When the listing
does not complete inside the per-table ceiling the module returns `absent` with that reason and
**never the max-so-far** -- which would be a wrong answer shaped exactly like a right one. Arm D
asserts it: `build_time=None`, `claim=absent`, `scanned` strictly between 0 and the population.

## 3. ACCEPTANCE -- invocation, output verbatim, rc, denominator

### O4-AC1 -- PASS-by-output
`<invocation>` `.tools/comp-heat federated --budget 120` · `<expect>` `VINTAGE`

```
budget: 120 s (flag)
BUDGET REACHED: 120 s (flag); scanned 0 of UNKNOWN (enumeration itself hit budget) queries; results are a PREFIX, not the answer; resume: comp-heat federated --cursor START
comp-heat federated: refusing to dispatch to the LIVE Trino plane -- budget below the transport's own known floor (~200s; _trino_fed.py: '~3-4 min/call') (a live call cannot be bounded once started -- .tools/_trino_fed.py, OS-s-5)
VINTAGE: 2 catalog(s) joined (code_heat, iceberg), 2 table(s), 1 measured / 1 UNREAD -- the ARTIFACT's build time, never the query's clock
  iceberg.globgrph.graph_nodes  build_time=UNREAD  claim=absent
      reason: listing did not complete within this table's probe ceiling (9001 object(s) read under s3://opal-313476888478-globgrph/warehouse/globgrph/graph_nodes_4c6c23bd-fffa-427e-9cd9-7a9deaa3426d/); S3 lists lexicographically, not by time, so no max is claimed from a partial read
  code_heat.globgrph.code_heat  build_time=2026-07-16T03:40:46Z  claim=measured  age=51.1d
      instrument: max(s3 LastModified) over 2 of 2 object(s) under s3://opal-313476888478-globgrph/warehouse/code_heat/; located by glue:GetTable globgrph.code_heat -> s3://opal-313476888478-globgrph/warehouse/code_heat/
  the query clock (2026-09-05T05:46:12Z) is NOT a vintage and is printed here only so the two cannot be confused
```

**rc=0.** Denominator: **2 of 2 catalogs joined are named; 1 of 2 tables measured, 1 of 2 UNREAD with
its reason.** 3 of 3 consecutive runs identical on every field that is not a clock (wall 4992 /
5732 / 5113 ms; the only run-to-run difference is the iceberg row's `scanned`, 9001 / 9001 / 10001,
which is the bounded probe's own progress and is printed as such).

**No Trino query was dispatched by this criterion** -- the refusal line is in the output above and
the battery asserts its presence rather than assuming it.

### O4-AC2 -- PASS-by-output
`<invocation>` `python .tools/tests/test_os4_federated_vintage.py` · `<expect>` `PASS`

```
[PASS] A-TABLES-DERIVED-FROM-THE-SQL-NOT-RECITED -- canonical SQL -> [('iceberg','globgrph','graph_nodes'), ('code_heat','globgrph','code_heat')] ; a DIFFERENT --sql -> [('hive','other','thing'), ('code_heat','globgrph','code_heat')] (2 of 2 statements parsed)
[PASS] B-GLUE-IS-A-LOCATION-SOURCE-NOT-A-TIME-SOURCE -- reported build_time=2026-07-16 03:40:46+00:00 (the ARTIFACT's); the catalog row's UpdateTime is 2026-06-29 20:34:47+00:00 and is NOT what was reported -- they disagree by 16.3 days
[PASS] C-CONVENTION-JOIN-NONZERO-ON-A-KNOWN-CASE-PLUS-ZERO-MATCH-CONTROL -- graph_nodes -> 1 of 11 child prefix(es) | NEGATIVE CONTROL no_such_table -> matched 0 directory(ies)
[PASS] D-TRUNCATED-LISTING-IS-UNREAD-NOT-A-PARTIAL-MAX -- scanned 22 of 400 object(s) then stopped; build_time=None claim=absent
[PASS] E-UNREGISTERED-CATALOG-IS-UNREAD-WITH-A-REASON -- catalog 'hive' is not in this tool's vintage registry (registered: code_heat, iceberg); no location is guessed
[PASS] F-SPENT-BUDGET-IS-UNREAD-NOT-A-DEFAULT -- 2 of 2 tables UNREAD with the budget reason; 0 fabricated timestamps
[PASS] G-RED-MUTANT-PRINTS-THE-QUERY-CLOCK-AND-IS-CAUGHT -- mutant build_time=2026-09-05 05:18:57+00:00 is within 0.0 s of the query clock instead of the artifact's 2026-07-16 03:40:46+00:00 (51.1 days apart)
[PASS] H-MUTATION-ANCHOR-UNIQUE
[PASS] I-LIVE-CLI-CARRIES-VINTAGE-AND-DID-NOT-DISPATCH -- rc=0 in 4.2s | stamp='2026-07-16T03:40:46Z' parsed=True age=51.1 d | not-the-query-clock=True | refusal present=True
OS4-FEDERATED-VINTAGE BATTERY: 9/9 PASS (denominator 9; 8 offline, 1 live-bounded, 0 Trino queries dispatched)
```

**rc=0. 9 of 9 arms PASS** (the battery prints its own denominator). Also under pytest: `1 passed in
4.61s`. Stable across 3 runs.

**The RED mutant the criterion names** is arm G: `_artifact_build_time()`'s return is replaced with
`_now_utc()` -- the QUERY CLOCK -- in a temporary copy of the engine **outside the repository**, and
the arm catches it by the only property that separates the two, the 51.1-day gap. Without it, arms B
and I would be vacuous.

**Cost discipline in the battery itself:** 8 of 9 arms run against a FAKE object plane and make no
AWS call at all; the single live arm runs at `--budget 120`, below the 200 s floor, so the live Trino
plane cannot be reached, and the arm asserts the refusal text so that is a checked property.

### O4-AC3 -- JUDGMENT (`judgment="true"`) -- RECORDED, NO VERDICT

The criterion: *record whether any joined catalog cannot report a build time, and what the answer
prints in that case (UNREAD with its reason, never a default).* `3.0.0_SA_CVO` grades this at L9.

**One of the two joined catalogs cannot report a build time in-band: `iceberg.globgrph.graph_nodes`.**

What the answer prints, verbatim:
```
  iceberg.globgrph.graph_nodes  build_time=UNREAD  claim=absent
      reason: listing did not complete within this table's probe ceiling (9001 object(s) read under s3://opal-313476888478-globgrph/warehouse/globgrph/graph_nodes_4c6c23bd-fffa-427e-9cd9-7a9deaa3426d/); S3 lists lexicographically, not by time, so no max is claimed from a partial read
```
`build_time=UNREAD`, `claim=absent`, and a reason naming the prefix, the count read, and why a
partial read cannot yield a max. No default, no fallback, no substituted clock.

**WHY it cannot, measured out-of-band rather than asserted.** Each alternative was checked and each
is closed from here:

| resolution path | result |
|---|---|
| Glue Data Catalog | **not present** -- `get_tables globgrph` -> `['code_heat','obs_findings','tool_activity']`; `get_databases` -> `['cloudtrail_forensics','default','globgrph','opal_mcp']`, no graph table in any |
| Iceberg `metadata/version-hint.text` | **404** |
| `warehouse/snap_ingest/last_append/` pointers | present for `code_heat_snap`, `fedobs_coevolution_snap`, `fedobs_coverage_snap`, `ms_heat_snap` -- **not for `graph_nodes`** |
| the Nessie pointer itself | **in-VPC only**, the same reachability wall as the Trino coordinator (`_trino_fed.py:10-14`) |
| the S3 object plane | **resolvable but not affordable in-band** -- see below |

The object plane CAN answer, and I measured it completely so the UNREAD is a cost decision rather
than a mystery: **183,447 objects / 184 pages / 36.55 s** for the table; **134,616 objects / 25.51 s**
for `metadata/` alone; **20,374 objects / 4.88 s** for the `*.metadata.json` shape -- one metadata
file per Iceberg commit, none expired. The completed listing dates the table at
**2026-09-05T02:11:10Z**, about three hours before this read.

**So the two sides of the join differ in age by roughly 51 days.** The `code_heat` side's freeze is
**`0.7.0_AE_CloudOps~W`'s measurement on `OS-s-7`**, cited and not re-derived: producer made
host-bound by a CTO revert on 2026-07-16, **0 of 142** live EventBridge rules fire it, Glue `Owner`
null. My tool independently re-reads the same object plane and prints `2026-07-16T03:40:46Z`, which
**agrees** with that measurement -- but through a different client (boto3 vs the `.tools/aws` CLI) on
the **same plane**, so it is corroboration on the client axis only and is **not** independent on the
plane axis. I state that rather than presenting agreement as if it were two instruments.

**What I do not claim.** That the join's answers are therefore wrong. I did not run the join --
`comp-heat` refuses to dispatch below 200 s and this order's invocation is 120 s -- so what a 51-day
skew does to a consumer's question is `OS-s-8`'s and `OS-s-10`'s to say, not this cell's.

Filed as `NFRA_OUTSET-W1-S14` (ARMED on the GROWTH, not on the current UNREAD: 20,374 unexpired
snapshot metadata files grow with every derive run, so this disclosure gets strictly more expensive
over time and the UNREAD widens rather than holding).

## 4. LIVE-PLANE DISCIPLINE

| what | held |
|---|---|
| Trino queries dispatched | **0** -- every invocation ran at `--budget 120`, below the tool's own 200 s floor, and the refusal line is asserted by the battery |
| budget raised to make something pass | **never** |
| AWS surfaces touched | `glue:GetTable`, `glue:GetTables`, `glue:GetDatabases`, `s3:ListBucket`, one `s3:HeadObject` -- **all read-only**; nothing written, nothing deleted |
| per-call cost of the new disclosure | ~4-5 s wall (one Glue read + a 2-object listing + one bounded 3 s probe) |
| reproducibility | a live read is not reproducible the way a git count is. Vintage stated: all live readings 2026-09-05 ~05:0x-05:5xZ. `code_heat`'s value was identical across 6 readings; the iceberg row's `scanned` varies run to run and is printed, not smoothed |

## 5. REGRESSION + GATES

| check | result |
|---|---|
| `python .tools/tests/test_os4_federated_vintage.py` | `9/9 PASS`, rc=0 (x3) |
| `python -m pytest -q .tools/tests/test_os4_federated_vintage.py` | `1 passed in 4.61s`, rc=0 |
| `python .tools/tests/test_os1_budget_battery.py` | `OS1-BUDGET BATTERY: 21/21 PASS`, rc=0 |
| `python .tools/tests/test_os2_path_grain.py` | `OS2-PATH-GRAIN BATTERY: 10/10 PASS`, rc=0 (see s.6) |
| `bash .tools/commit-gate.sh` on the 4 touched files | `OK: pre-commit gate clean for 4 of 4 file(s)`, rc=0 |

## 6. WORK DONE OUTSIDE THIS CELL, ON THE ISSUER'S INSTRUCTION -- `NFRA_OUTSET-W1-S12`

`2.0.0_SA_COO` instructed this worker, mid-round, to fix `OS-s-2`'s battery arm F **if** a later
order admitted it to that file; `TO-OS-s-4`'s `<paths>` grants `.tools/tests/`, so the condition is
met. **I reproduced the flake here before fixing it** (`9/10 PASS` rc=1 with `age-diff=1`, then
`10/10` rc=0 on the immediate re-run, no code change between).

**Cause:** the arm compares two SEPARATE `comp-heat` invocations seconds apart. A tracked file's age
is a commit timestamp and is stable between them; an **untracked** file's age is a live filesystem
mtime, so any write to the worktree between the passes moves it.

**Fixed without weakening.** The path SET is still compared exactly over every row (that is what a
scoping regression moves); band and age are now compared over the **git-sourced** rows; the
mtime-sourced rows are compared on membership with their count **printed as a stated exclusion**; a
`HEAD held / MOVED` reading brackets the arm; and **every difference now names its members** -- the
defect the issuer named was that the count came from `age_diff` while the printed list came from
`key_diff`, so a failure printed `age-diff=1 []` and named nothing.

**Falsifier RUN, not promised:** the battery re-run while a background loop touched an untracked file
inside the scoped corner every 0.3 s for the whole run -- the exact producing condition -- returned
`10/10 PASS` with `388 git-sourced (band+age compared) + 1 mtime-sourced (membership only) ...
key-diff=0 [] band-diff=0 [] age-diff(>0.01d)=0 [] ; HEAD held during the arm (b630052d6a)`. Not
vacuous: 388 of 389 rows are still compared on both axes and that count is printed.

## 7. AN ERROR OF MINE, RECORDED IN FULL -- `NFRA_OUTSET-W1-S13`

**I executed code from the main workspace and wrote a file there, believing I was in my worktree.**
In the Bash tool, `cd X && A & B; C` backgrounds the whole `cd X && A` list, so `B` and `C` run in
the session's default cwd. One falsifier invocation therefore ran the MAIN tree's **drained** copy of
`test_os2_path_grain.py` and wrote
`C:\Users\AndrewBerman\Desktop\ajb_workspace\.scratch\os2_falsifier.txt` (2146 B, 01:33).

**The tell was a stale string** -- the battery printed the PRE-EDIT detail format. That is the only
reason it was caught; a run whose output happened to look the same in both trees would have been
indistinguishable from a correct one, which is why the row is ARMED.

**Blast radius measured, not assumed:** exactly one file created (that `.scratch/` already existed at
01:23 with another seat's `wk3-d5/`, so nothing was clobbered); no mutant copies left behind
(`grep -c 'comp-heat-os'` -> 0, the battery's own `finally` having cleaned up); no git object, index
or tracked file in the main workspace touched; no commit made there. **I did not delete the stray
file** -- the main workspace is outside my grant and a second unauthorised act there is worse than a
stray scratch file. `2.0.0_SA_COO` owns that call; the exact path is in the row.

The falsifier was then re-run correctly from absolute paths with the background loop cd-ing itself,
and its conclusion is unchanged -- but the first reading of it was worthless.

## 8. DECLARED NON-APPLICATION

- **`.tools/_trino_fed.py` is not in this order's `<paths>`** and was not edited. The vintage lives
  in the wrapper + a new engine module, which is why the disclosure works on the refuse path (where
  the transport is never reached at all).
- **`comp-freshness` was considered and rejected on the build ladder** (rung 2, "the estate already
  has it"): it is a PASS/FAIL **gate** over declared BD/INF/COT gold-chain cadence entries, not a
  general artifact-vintage reader for a Trino catalog, and using it would drag a cadence-config
  declaration in for two tables that have none. Named rather than silently skipped.
- **No `--vintage-ceiling` flag was added.** The per-table ceiling derives from the caller's existing
  Rule T `remaining()`; a new flag would be a second budget carrier beside Rule T's.
- **Iceberg snapshot expiry is not this cell.** It is a producer-side act on `infra/` paths this
  order does not grant. Recorded in `W1-S14`.
- **No alarm, monitor, freshness-checker or SNS**; nothing deleted; no new dependency (boto3 is
  already the federated path's own).

## 9. PUSH STATE

**LOCAL.** Nothing pushed under this order. Measured with `git ls-remote` at report time -- the
reading and its vintage are in the WORKER REPORT.
