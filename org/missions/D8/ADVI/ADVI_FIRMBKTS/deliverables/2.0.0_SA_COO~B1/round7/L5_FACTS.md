# ADVI_FIRMBKTS round 7 -- L5 ground truth (2.0.0_SA_COO~B1, dell1, 2026-10-13 ~08:3xZ)

Claims: M = measured by this seat now, H = held (a cited record).

| # | fact | claim | source |
|---|---|---|---|
| 1 | The CVO (msg 4702, `REMEDIATION_v7.md` @db0c7f9805) graded FWD-1: correctness MET (150 of 150 equal the key), the agreement arm NOT met (D1-C-S45); the CTO ruled a second fresh reader, not a reinterpretation. | H | `ROUND_ANALYSIS.round6.md` section 1 |
| 2 | Round 6's reader (`~67`) answered the 150 of `round6/READING_KEY.json` at the list `80ff50f2f576`; a second worktree of the SAME commit holds the same list and ids (no earlier answers). | M | `round6/READER_COMMIT.txt` |
| 3 | `emit_chain_complete` (`gold_dispatch.sh` ~835-855) tests `aws events put-events ... 2>&1 \| grep -q '"FailedEntryCount": 0'`; the failure WARN carries no CLI text. The script names a region nowhere (`--region`, `AWS_DEFAULT_REGION`, `AWS_REGION`, `aws configure`: 0 matches). | M | native grep, 06:5xZ |
| 4 | The event bus is `arn:aws:events:us-east-1:313476888478:event-bus/default` (the region the rule and the generator live in); the runner has no region set (round 6 FB-i-2, inferred: the global CloudFront call succeeds 4 of 4 chains). | M/H | `events describe-event-bus` at the cut; `round6/R6_CLOSE.md` |
| 5 | The runner's manifest bars SSM commands on it (row D1-S44), so a runner-side measurement is the dispatcher's own chain log. | H | `D1-S44` |
| 6 | `exec-summary-generator`'s handler hard-codes `upload=True` (`lambda_function.py:442`); `process_advisor(..., upload=False)` exists; `S3_BUCKET = "opal-data-bd"` goes through `platinum_destination` (canonical home since 4b); `MAX_ADVISORS_PER_FIRE = 5_000`; no tests directory is tracked under the generator. | M | file reads |
| 7 | `opal-data-49financial` versioning is Enabled; the canonical `advi/49financial/platinum/advisors/<id>/exec_summary.json` keys exist (act 3's copy, e.g. 2026-10-11T04:02Z); 194 objects under the advisor prefix listing top level. | M | `get-bucket-versioning`, `list-object-versions` |
| 8 | The CTO ruled (ADDENDUM 1, msg 4707): a dry-run handler YES, before the fix, own pair, arms "0 objects written; non-dry behaviour unchanged"; the region ONE variable `EVENTS_REGION` on the put-events call only, NOT a global export; the diff must show every other call byte-unchanged. | H | `ROUND_ANALYSIS.round6.md` ADDENDUM 1 |

## Base dry-runs (each check a file under `round7/checks/`, `round6/checks/` or `round4/checks/`)

| order | criterion | base | reference patch |
|---|---|---|---|
| FB-j-1 | AC1 reader (`r6_fwd1.py reader`) | FAIL as expected (0 of 4; 4 of 4 on a full fixture; 3 of 4 with one extra file) | -- |
| FB-j-2 | AC1 `r7_emit_test.sh` | FAIL as expected (1 of 3: E2 passes as a control) | PASS (3 of 3 on a reference function) |
| FB-j-2 | AC2 `awsdiff` | FAIL as expected (no hunk) | PASS (a good patch); FAIL on a patch that also adds `--region` to another call |
| FB-j-3 | AC1 `emiterr` | FAIL as expected (record absent) | -- |
| FB-j-4 | AC1 `r7_region_test.sh` | FAIL as expected (1 of 3: R3 passes as a control) | PASS (3 of 3 on a reference function with the variable and `--region`; `r7_emit_test.sh` still 3 of 3 there) |
| FB-j-5 | AC1, AC2, AC3 | FAIL as expected (test file absent; no diff; nothing changed) | -- |
| FB-j-6 | AC1 `dryrun` | FAIL as expected (record absent) | -- |
| FB-j-7 | AC1 `firstchain` | FAIL as expected (record absent) | -- |

(The record graders `emiterr`, `dryrun` and `firstchain` are dry-run at base only, each reading ABSENT as FAIL; each is re-run on the actor's
real record at the drain.)
