# NEVER-WIDEN -- COO HALF: every silver `research-report` row is re-appended with a `fund_relation` (`HVST-cg-2`, round 92, workstream SILVER-REWRITE)

**Signer:** `2.0.0_SA_COO~W1`, drafted 2026-10-18 ~00:1xZ UTC. **Authority:** the CTO's round-91 analysis (`ledger/ROUND_ANALYSIS.round91.md` @9bdb466396, msg 7773) item 1 ("first a no-write census over 94 names printing the count per relation, then the silver rebuild under its own never-widen pair") and his rulings on `D1-S46` (msg 7771), on the two classification gaps (msg 7782) and on the word `adding` (msg 7784, with its guard); `HVST-cg-1` (merged `ad116e0037`); `HVST-cg-5` (merged `a9aecdd593`).

## THE MEASUREMENT (the CTO asked for the counts to be pasted here; every number below was read by the issuer at `a9aecdd593`)

- **Census (`cg2_census_at_a9aecdd593.out`, sha256 `69568d499eda8e7412c6629b...`, a no-write read of 5 silver parts, 6 requests, 133,462 bytes; the issuer's own re-run, identical to the worker's `cg5_census.out`):** `CENSUS-FUND-RELATION rows=355 reports=353 securities=94 holding=121 candidate=14 initiate=2 interest=2 template=1 unclassified=0 none=213`. The seven counts sum to 353. The 2 rows not counted are the two misfiled KMB reports, excluded as the gateway excludes them.
- **The CTO's named proof, equal:** `PROOF-NAMES ADBE_US_Equity=candidate SNPS_US_Equity=candidate MNST_US_Equity=candidate ML_FP_Equity=template CLX_US_Equity=candidate UNH_US_Equity=holding`.
- **The guard on `adding` (msg 7784):** exactly two rows match, both `CPA_US_Equity` (`RECOMMEDATION: Consider adding 50-100bps in IDVZ taking it to 150-200b`), a held position; none names a new position.
- **Rows moved by `HVST-cg-5` against `HVST-cg-1`:** 4 (`ORA_FP` x2 `unclassified` to `holding`, `CPA` x2 `none` to `holding`); no other row moved.
- **The dry run (`cg2_dryrun_at_a9aecdd593.out`, nothing put):** `REBUILD-PLAN rows=353 skipped_unchanged=0 new_parts=3 dates=3 puts_recorded=3 puts_performed=0 gets=12 bytes=266924`; the three parts it would write, one per date partition: `date=2026-09-23` 121 rows, `date=2026-09-24` 148 rows, `date=2026-09-25` 84 rows.

## THE ACT, in the order's words

On dell1, by `0.7.0_AE_CloudOps~SC1`, from a worktree at commit `a9aecdd593` (or a later commit whose `lib/research/` tree is byte-identical to it, proven by an empty `git diff a9aecdd593 <commit> -- lib/research`): (0) BEFORE, read only: run the census and the dry run and print them; they must equal the measurement above, else STOP. (1) WRITE, the three date partitions in this order, each as a SEPARATE foreground command: `2026-09-25` (84 rows, the canary), then `2026-09-23` (121), then `2026-09-24` (148); each command builds the rows of that date exactly as the dry run does (the newest row per (`security_key`, `report_id`) by the gateway's rule, the two misfiled KMB rows excluded, `dict(row)` plus `fund_relation = fund_relation.classify(row["fund"], row["fund_evidence"])`) and calls `lib.research.harvest.store.silver_append("amgt", "research-report", rows, ("security_key", "report_id"), run_stamp, client=<the real client>)` with a fresh `run_stamp` (UTC `YYYYMMDDTHHMMSSZ`). (2) After each, READ THE PART BACK (below) before the next date starts.

## THE PROPERTY AND ITS WRITERS (printed, CLAUDE.md section 5)

The property moved is the `fund_relation` column of the silver `research-report` table (`amgt/harvest/silver/research-report/`). **N = 2 writers:** (1) `lib/research/corpus/typed.py::main` (line 699, `store.silver_append`), which builds every NEW row through `typed.record()`, now carrying the key (`HVST-cg-1`); (2) this act. Both rules are read: they are the same function, `fund_relation.classify(fund, fund_evidence)`, on the same two fields, so a row this act writes equals the row `record()` would write for that report. (`substrate.py` line 525 calls `silver_append` with a stub client inside a read-only proof; it is not a writer of the bucket.) No schedule or trigger runs `typed.main` against the bucket in this act's window (the seat confirms, step 0).

## WHAT THIS CHANGES IN THE WORLD (named)

- **Silver objects are ADDED; none is changed or deleted.** Three NEW parquet parts (`part-<run_stamp>.parquet`, one in each of `date=2026-09-23`, `date=2026-09-24`, `date=2026-09-25`) in `opal-data-harvest`, 353 rows in all. The silver writer never overwrites (`IfNoneMatch`); the old parts stay.
- **Which rows win:** each new row keeps its `fetched_at` (so its date partition) and gains `fund_relation` and a new `record_hash` (all 353 hashes change); `silver_latest` takes the newest `fetched_at` per key and, on a tie, the part with the later `run_stamp`; the gateway (`harvest_research.py::_research_reports`, lines 258-295) takes the part whose KEY sorts highest. The new parts win under both rules (a `run_stamp` of 2026-10-18 sorts after the old stamps of 2026-09-23 to 2026-09-26).
- **What changes in what is served: NOTHING, until `HVST-cg-3`.** The gateway builds each entry from the fixed tuple `REPORT_FIELDS` (`fund_relation` is not in the deployed tuple); `fund_form.gather_items` reads `row.get("fund")`; both read rows as dictionaries and name their keys, so an added key is invisible to them. The seat proves it: UNH and CPA, read served before and after through the gateway, are equal (`content_sha256`, `source_keys` equal; `research_reports[]` entries unchanged and without `fund_relation`). This is why the order is silver first, gateway second (CTO msg 7775): the field is never served empty.
- **Not touched:** gold (continuation, dossier, fund form), bronze, the gateway code and service (no restart), IAM, schedules, Terraform, any other table, the two misfiled KMB rows (not re-appended; the gateway excludes them).

## BOTH BRANCHES (the half is not signed unless it covers both)

- **Branch A (the part read back equals the plan):** the part has exactly the date's planned row count (84, 121 or 148); the column `fund_relation` is present; the set of (`security_key`, `report_id`) equals the planned set; every column other than `fund_relation` and `record_hash` equals the row it supersedes (the old row, read from its old part); `fund_relation` of every row equals `classify(fund, fund_evidence)`, and the per-relation counts of that date equal the census's for the same rows. The next date starts.
- **Branch B (the part differs in ANY of those):** STOP; start nothing else; record the exact difference. The part is already written (the writer cannot unwrite it): its repair is a still NEWER part from a corrected run (never an overwrite), decided by the issuer and the CTO; no key is deleted by the seat.
- **Either way:** `fund`, `fund_evidence` and `fund_absent_reason` of no row change; a mismatch in them is a STOP.

## CONDITIONS

- **C-1.** The code is the tree at `a9aecdd593` (the empty `lib/research` diff proof printed in `cg2_before.out`); the row set is what the dry run plans (353 rows, 3 dates); nothing is added or dropped by hand.
- **C-2.** A change-management ledger entry is open at the start and CLOSED and COMMITTED at the end (NEVER-2; `org/critical_paths/change_management/` and the sentinel `org/critical_paths/.open_deploys/harvst-cg2-silver-fund-relation-rewrite.json`), naming the bucket, the table prefix, the window and the manifest.
- **C-3.** Every put is recorded in `cg2_written.out` the moment it lands (key, VersionId, bytes, sha256, rows, UTC); the manifest IS the rollback list and is committed with the ledger close.
- **C-4.** The write principal is the one dell1's existing harvest tooling already holds; NO grant, key or policy is requested; an AccessDenied is a STOP.
- **C-5 (the CTO's rule for write runs, row `D1-S44`).** One date partition per command; EVERY command is FOREGROUND with `python -u` and its output appended to a log file; NO `nohup`, no detached or background process; after each date read the manifest and confirm the part is present before starting the next; a missing key, any error (an `IfNoneMatch` conflict, AccessDenied, a throttle) or silence is a STOP with the exact text; no retry loop.
- **C-6.** After the LAST date, the gateway's own rule (newest part key per (`security_key`, `report_id`)) is applied to the bucket: all 353 reports are served from the new parts, each carries `fund_relation`, and the counts equal the census line (`holding=121 candidate=14 initiate=2 interest=2 template=1 unclassified=0 none=213`); the six `PROOF-NAMES` equal.
- **C-7.** UNH and the CONTROL: `UNH_US_Equity` and `CPA_US_Equity` are read served through the gateway BEFORE the first write and AFTER the last, with `fields` `["fund_of_record","last_stated_position"]`; every returned field entry, `content_sha256`, `source_keys` and the `research_reports[]` entries equal.
- **C-8.** No Terminal, queue or Bloomberg use; no S3 delete by the seat; NO call of `etfs_compare_peers` on the gateway (site Z row `Z-S375`).
- **C-9 (site Z told first).** Before the first write the issuer asks `0.0.0_AB_MSTR~DELL1` to tell site Z the window, the table prefix and the three part dates, and that a site Z write to `amgt/harvest/silver/research-report/` in flight is a STOP; the issuer sends GO with site Z's answer.

## ROLLBACK (stated honestly)

The act is ADD-ONLY; the pre-act state returns when the three new keys are removed, which is an S3 delete: Andrew's act, not the seat's and not pre-approved here. Because the old parts are never overwritten, removing the new parts restores exactly the served state before the act (the old rows win again). The manifest lists every new key and VersionId. The 84-row canary partition bounds the first exposure. Because nothing served changes until `HVST-cg-3`, a bad part costs nothing in the world before the gateway release, and `HVST-cg-3` is not started until C-6 passes.

## WHAT THIS DOES NOT COVER

The gateway release (`HVST-cg-3`, its own pair); the `fund_form` rebuild (`HVST-cf-3`, `-5`, their own pairs); gold; the shared classifier of gold and silver (row `D1-S49`, round 93); any silver table other than `research-report`.

## VERDICT: SIGNED (COO). Not started until the CTO half is on file at these bytes.
