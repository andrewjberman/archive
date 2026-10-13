# IRPT_DASHBD round 87, workstream B -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-13 ~13:0xZ)

**One cell, WORLD:** `DB-b-165`, order `IRPT_DASHBD.TO-DB-b-165.thresholds-file-swap-apply-dell2` (issued @9d20875242 to `0.7.0_AE_CloudOps~IB2`), status `complete`, round-close `verdict=MAY-CLOSE` (`round-close-check --project IRPT_DASHBD --round 87`: orders=1, judgment=0).
Under the signed pair: packet sha256 `2ed4e840ef5624707a144d5c79f8bf2d96cde67e929a790e908e01ec080cd662`, COO half @7c9ad9d0f0, CTO half @c5e183273f.

## What was applied (the applier's report, msg 6923, and what this seat re-measured)

| item | applier's report | re-read by this seat (13:0xZ) |
|---|---|---|
| criterion `DB87-1-AC1` | PASS | PASS, re-run by this seat on the record (`THRESHOLDS_SWAP_APPLY_RECORD.json`); the proof instance validates (`proof-of-spec-check` VALID) |
| live function | CodeSha256 `J6M/92MhjYM/0kKoYRQwR0ah68DizcvnkVSE6o24udg=`, 3008 MB, applied 12:39:43Z | `get-function-configuration`: the same CodeSha256, MemorySize 3008, Timeout 900, Active, Successful, LastModified 2026-10-13T12:39:43Z |
| artifact | S3 version `UcKN2ttQzhg5B3jn3POSxVBGg15TqpON` | `list-object-versions`: that version IsLatest (223,320 B, 2026-10-13T12:36:19Z); `head-object` `content-sha256` equals the live CodeSha256; the prior version `8ELUDq_d2wRKI0kSXEuLXFm6iqgsiAyZ` (the REFRESH 4 build, the rollback target) is kept |
| member diff | exactly the one thresholds path (19 members against 19) | recorded as `['data/assets/scripts/gold/irpt_reporting/MEASURED_THRESHOLDS_R1.json']`, which the checker requires; the diff itself was the applier's read (this seat did not re-download the zip) |
| source map | re-pinned (commit c23fb94306, LOCAL) | `git show HEAD:infra/aws/lambda/ci/lambda-source-map.json` lines 6091-6094: the thresholds entry reads pin `aaeb1866ff...`, sha256 `69e0a889a7e6...` |
| plan and re-plan | 0/1/0; re-plan No changes | recorded (`plan` {0,1,0}, `replan_no_changes` true); the plan output itself is the applier's, not re-run |
| dry run | 348.1 s of 765, 1,221 MB of 2,556.8, 0 objects written (positive control 13) | the REPORT line for RequestId `022c46f0-bccc-4a6a-a955-023c06f67659` read from CloudWatch by this seat: Duration 348133.23 ms, Max Memory Used 1221 MB of 3008. 0 objects written and the control are the applier's reads |
| rollback | none | none recorded; the checker requires none |
| ledger | L1-L6 closed, L7 open for the issuer | entry `20261013T1228Z_irpt-dashbd-thresholds-swap-20261013_deploy_completion.md` Status OPEN, sentinel present: it stays OPEN until L7 |

## Open

- **Ledger leg L7 (mine): the first scheduled fire after this release**, next 2026-10-14 11:41Z. Read with `checks/l5/l5b_read.py` @88d74f1a63 (`--fire-window-start 2026-10-14T11:30:00Z --expect-codesha-prefix J6M/92Mh`), whose controls were
  run on synthetic manifests. **The leg's text asks for `threshold_claims_source stated`; the returns manifest carries no such key (measured on the date=2026-10-12 manifest), so the leg is read on the five claim words
  (`measured`, `measured`, `held`, `held`, `inferred`) and the proof says so.** Until then the ledger stays open (window 48 h; the fire is inside it).
- **Applier's odd line:** `crossbox-deploy-check` returned rc=124 (a WARN, a timeout) during its run. Not read by this seat; the applier recorded it.
- **Push state:** the applier's commits (map c23fb94306, close 7fc8c1834c) were LOCAL on box/dell2 at its report (origin 6742fc12d1, its read); this seat's drain-end is LOCAL.

## Not re-measured by this seat

The plan output and the applier's census of 45 worktrees; the zip member comparison; the 0-objects-written listing and its control; the kit comparison (the pair's, not this order's).

-- 2.0.0_SA_COO~D2
