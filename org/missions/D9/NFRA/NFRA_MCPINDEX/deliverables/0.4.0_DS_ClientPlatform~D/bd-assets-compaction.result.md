# NFRA_MCPINDEX.TO-MX-s-6 -- the bd_assets compaction (step 1 of 2)

**Lane:** `0.4.0_DS_ClientPlatform~D` · **Issuer:** `2.0.0_SA_COO~O` · **Order:** `@3e972dac5d` ·
**Risk class:** WORLD · **Written:** 2026-09-27T03:0xZ

**Headline: step 1 is done, deployed and verified against the served artifact -- but the fix the order
names in words would have destroyed the file it was meant to repair, so it was cut differently and the
difference is proven, not argued. Step 2 is blocked, and not on what the order expected.**

---

## 1. THE DEFECT, RE-MEASURED FROM THIS LANE

Row `NFRA_MCPINDEX-Z-S15` (`0.7.0_AE_CloudOps~I`) is correct on every limb. Confirmed independently here
rather than inherited:

- `.tools/aws ssm get-document --name opal-bd-asset-dim-download` -- its only converter line is
  `python3 convert_assets_to_silver.py --latest`. No `--backfill` anywhere in the document.
- The gate at the single call site read `if args.backfill and not args.no_compacted:`, so on the scheduled
  path the compaction branch was never entered.
- The bytes I patched are sha256 `0b99836672853e23ec6f0d8d72f9dc396d3fe58e7d15481e04d57cde48df187e` --
  the same sha Z-S15 recorded for BOTH the repo file and the deployed
  `s3://opal-data-bd/code/silver/convert_assets_to_silver.py`. No drift between what I read and what runs.

## 2. WHY THE LITERAL FIX WAS REFUSED, AND WHAT WAS CUT INSTEAD

The order says "fix the condition in the converter". Taken literally that is
`if not args.no_compacted: write_compacted(df)`. **That would have been a data-destroying fix.**

Under `--latest`, `df` is ONE forwardfill export. `write_compacted` REPLACES the key. Measured on the live
object before touching anything -- `silver/bd_assets.parquet` = **3,449,107 rows / 31 columns / 4 row groups
/ 69,441,673 bytes** (read through 65,536 bytes of ranged GETs, not a 69 MB download). So the one-line
widening would have replaced 3.4M consolidated rows with a single day's export, on the very file
`build_bd_assets_dim.py` reads -- turning a frozen input into a nearly empty one. It would also have made
the order's own AC1 go GREEN while doing it, because AC1 only reads LastModified.

What was cut instead, split on mode:

| mode | compaction | why |
|---|---|---|
| `--backfill` | REPLACES (unchanged) | that run's frame IS the whole consolidated set |
| `--latest`, `--file` | MERGES | the frame is one export, so it is folded in |

The merge streams: read the existing file row group by row group, drop the `transaction_id`s this run
re-issues, append this run's rows. It applies the same "later export wins" rule `dedup()` already applies
in-frame. It streams because peak memory is then ONE row group (largest 63.2 MB uncompressed) rather than
the 172.3 MB whole -- **the runner is a t3.medium with 4 GiB** (`i-0e6f6dc014fdcf1cd`, per Z-S17).

`_align_to_schema` casts each run onto the compacted file's own arrow schema, so the schema the bridge reads
cannot drift. A column the schema lacks is dropped LOUDLY; a column the export lacks is filled null. A new
BD export column would otherwise vanish without a word.

## 3. EVIDENCE -- THE TEST, WITH BOTH NEGATIVE CONTROLS ACTUALLY RUN

`data/black_diamond/tests/test_convert_assets_compaction.py` -- **7 passed**, no network (boto3.client is
stubbed before the module is imported, so the suite needs no credentials).

A test that is green on both sides of a change proves nothing, so both controls were run:

- **At base bytes `0b99836672`: 5 of 7 FAIL.** The 2 that pass are the regression guards
  (`--no-compacted` still skips, `--backfill` still replaces), which is the correct verdict at base.
- **With the naive one-line widening PLANTED:** `test_latest_writes_the_compacted_file` goes **GREEN** and
  `test_latest_retains_rows_it_did_not_re_issue` **FAILS** -- *"rows absent from this export were dropped"*.
  The mutant that satisfies the order's literal ask is caught by the test that matters.

The suite also pins: `--latest` reads only the newest export (a planted older export's row must not appear);
a re-issued `transaction_id` ends up present exactly once carrying the new values; the schema gap is filled
and dropped in both directions; and the first-mint path when no compacted file exists.

## 4. SCALE EXERCISE -- because the unit test speaks to logic, not to a t3.medium

The unit test runs on synthetic rows. The first real scheduled fire will run on 3.4M. So the merge was
exercised against the REAL compacted file and the newest REAL forwardfill export, with a stub that serves
both from local disk and captures `put_object` to a local file. **Nothing was written to S3.**

```
INPUT  compacted : rows=3,449,107  row_groups=4  bytes=69,441,673
INPUT  export    : AssetDimTXNs_OpalCapital_Daily_2026-06-18_to_2026-06-18.xlsx (26,082 rows -> 25,383 after dedup)
  kept=3,449,107   superseded by this run=0   appended=25,383
OUTPUT compacted : rows=3,474,490  row_groups=5  bytes=70,061,781   row delta +25,383
schema preserved : True
transaction_id   : 3,474,490 rows, 3,474,490 distinct, duplicates=0
wall time        : 7.0 s
arrow pool max   : 826 MB      process peak RSS : 919 MB
```

**919 MB peak against 4 GiB.** It fits, with room.

Two honest qualifications on that run:

1. **`superseded by this run=0`.** This export re-issued no id already in the frozen file, which is expected
   since the compacted file predates it. So the SUPERSESSION arm was exercised by the unit test, not by this
   real-data run. Named rather than left to look covered.
2. **Row groups accumulate one per incremental run** (4 -> 5 here). Over a year of daily fires that is
   roughly 365 small row groups. It is bounded and benign today, and the existing periodic `--backfill`
   rewrite is its remedy, but it is a property this change introduces and the issuer should know it exists.

## 5. THE DEPLOY, verified against the served artifact and not from rc=0

- Commit **`a2d25dd90b`** (2 files, 364 insertions) in linked worktree `ds-d-mcpindex-s6` per rule 14b;
  merged to CLOUD at **`74db08f005`** via `safe-merge.sh`; worktree and branch removed.
- `.tools/safe-deploy.sh` -- `DEPLOYED [bd]` + `VERIFY OK comp-pipescript`.
- **My own read of the served object**, because a producer's rc=0 is not evidence:
  deployed `s3://opal-data-bd/code/silver/convert_assets_to_silver.py` sha256
  `d78c31853ab6374b0950346b1e0163ad635754f1b212faa8df86d71001e91bfd`
  == the committed build input `git show HEAD:<path>` sha256 `d78c31853ab6...`
  != the pre-fix base `0b99836672...` (negative control).
  LastModified `2026-09-27T02:08:44+00:00`, 14,443 bytes.
- **PUSH STATE, measured at write time by `git ls-remote origin CLOUD`:** `a2d25dd90b` and `74db08f005` are
  **on origin** (origin/CLOUD reads `74db08f005` -- the integrator's push, not this lane's; standing no-push
  honored). The row commit `97351a613e` is **LOCAL**.

No NEVER-2 ledger entry: nothing half-landable. One script object replaced, its rollback is the prior
version of one key, and the deploy completed and was verified inside the session.

## 6. CRITERIA -- both FAIL, by design, and the reason is upstream

Run by their literal invocations from the workspace root:

| id | invocation | result |
|---|---|---|
| AC1 | `bash .../round2/checks/s4.AC2.sh` | `silver/bd_assets.parquet LastModified=2026-04-14T20:09:23+00:00 after issue=no` -- **FAIL**, exit=1 |
| AC2 | `bash .../round2/checks/s4.AC3.sh` | `silver/bd_assets_dim.parquet LastModified=2026-04-14T20:44:16+00:00 after issue=no` -- **FAIL**, exit=1 |

Both criteria measure step 2's outcome, and step 2 is explicitly gated by the order on MX-s-4's login fix
plus one converted run. **The proof-of-spec instance is therefore NOT written yet**; it is owed when step 2
lands, and writing one now with two FAILs would read as a completion claim.

**I deliberately did not fire an ad-hoc `--latest` run to turn AC1 green.** It would have worked -- and it
would have been the predicate, not the substance. The newest forwardfill export is 2026-06-18 (48 exports,
none after 2026-06-19), so such a run would rewrite the compacted file from JUNE data and satisfy a
LastModified test while the order's actual words are "one real scheduled or ad-hoc run has converted
**current dates**". Naming it so it is visibly rejected rather than silently unconsidered.

## 7. STEP 2 IS BLOCKED, AND NOT ON WHAT THE ORDER EXPECTED

The order sequences step 2 behind "MX-s-4's login fix lands". At `9736741fe6` `0.7.0_AE_CloudOps~I` filed
its MX-s-4 instance: **AC1 FAILS on a vendor blocker and that failure is the deliverable.** The Black
Diamond login times out on navigation to `bd3.bdreporting.com`; all three BD downloaders fail on the
identical error with the same boundary (last clean 2026-06-22, first failing 2026-06-23); MX-s-4 step 1's
own carve-out routes a vendor-side cause to Andrew.

Independently consistent with what I measured from the data side: **1,890 silver partitions, newest
`2026-06-18` written 2026-06-19**, and no forwardfill export after 2026-06-19.

**So step 2's precondition is now a sovereign call at Andrew, not an AE task in flight.** Nothing on this
lane can accelerate it, and no DS act substitutes for it. That is a condition, not a stall -- but it is a
different condition than the order assumed, which is why it leads this section.

## 8. ROWS FILED

- **`NFRA_MCPINDEX-Z-S18`** (`97351a613e`) -- OBSERVATION / INERT, disarm owner `2.0.0_SA_COO~O`.
  A log commit (`64b6b9d65a`, subject `log(COMP_LEARNS.session13)`, 275 files / 16,609 deletions) reverted
  the ADHC_DSFLOW.004 sweep: it stripped `from __future__ import annotations` from 98 files, and **60 are
  still missing it at `74db08f005`** (33 re-added, one of those being this lane's own commit; 5 no longer at
  HEAD). Of the 60, three carry PEP-604 unions in annotations. Filed INERT, not ARMED, because the runner's
  Python version was NOT measured and on 3.10+ the import is unnecessary. The row also records that my first
  classifier pass said four, the fourth being a `.sh` file `ast.parse` could not read.
  It was found because the gate blocked MY commit for exactly that line.

## 9. TWO MECHANISM FACTS, recorded rather than filed

Both are about running gates from a SPARSE linked worktree. Neither failed silently, which is why neither
is a row -- but both cost a cycle and the next seat should not re-derive them.

- **`.tools/halt-gate-check.sh` BLOCKED fail-closed, twice, and was right both times.** First for an
  unresolved principal (fixed by writing `org/mcp/sessions/<session-id>.serial`), then because it scans
  `$REPO_ROOT/org/tier*_*/*/` for the seat's home folder -- which a sparse cone excludes. Fix: add
  `org/tier2_senior/<serial-base>` to the cone. The gate refusing rather than guessing is the correct
  behavior and its message named the remedy.
- **The naming gate could not read `infra/logic/registry/systems.json` from the sparse worktree** and said
  so loudly in its WARN window. It graded nothing on this commit. This commit types no new S3 address or
  resource name, so nothing was owed to it -- but a sparse cone silently narrows what that gate can see, and
  under LGIC_ENFORCE that would matter.

## 10. WHAT I DID NOT DO

- **No served gold touched.** The `holdings_lots` correction is not mine and not now (order bound 3).
- **No bridge rebuild.** It is step 2, gated above.
- **No schedule created or changed.** The existing trigger is read-only here (order preflight).
- **No alarm, monitor or notification** (standing moratorium), including for the vendor outage.
- **No push** (order bound 2). The integrator's window carried the merge.
- **No sweep of the other 60 files** in row Z-S18 -- out of this order's `<paths>` and a cell of its own.

## 11. COMPILER TOOLS

| tool | use |
|---|---|
| `.tools/commit-gate.sh` | clean 2 of 2; caught the missing `__future__` import that became row Z-S18 |
| `.tools/safe-commit.sh` | `a2d25dd90b`, `97351a613e`, both under this lane's author line |
| `.tools/safe-merge.sh` | `74db08f005`, row gate clean on the merged index |
| `.tools/safe-deploy.sh` | 1 script deployed + comp-pipescript VERIFY OK |
| `.tools/surprise-row-gate.py` | 1 new row of 59 graded at commit (standalone run read HEAD's 58 and saw 0 -- it grades STAGED content) |
| `.tools/aws` (`ssm get-document`, `s3api head-object`, `list-objects-v2`, `s3 cp`) | schedule read, object vintages, the 1,890-partition census |
| `pyarrow.parquet` over a ranged-GET file object | compacted schema + row-group sizes for 65,536 bytes instead of 69 MB |
