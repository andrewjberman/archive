# NEVER-WIDEN, COO HALF -- hop 1 to the cloud: the 49 Financial reporting-gold function gains the `filled_report_values` stage (IRPT_DASHBD rounds 118 to 123, workstream B-49F): ONE Terraform apply, TWO in-place changes, ONE new gold prefix

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED. **Date:** 2026-10-15 ~11:0xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_HOP1_FILLED_REPORT_VALUES_STAGE.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_HOP1_FILLED_REPORT_VALUES_STAGE.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_HOP1_FILLED_REPORT_VALUES_STAGE.md`), sha256 `2f25b84dc85c1592801783ae23113e13c2686bad54b9fa6460ea6d353ac2635e`
(computed by this seat on the file; 13,116 bytes). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's three questions (section 7).
**Nothing is applied until both halves are SIGNED on this sha256.** Ordered by the CTO's rounds 120 to 123 rulings named in the packet.

## 1. What this half covers

ONE act: a Terraform apply of `infra/aws/terraform/investor-reporting/reporting-gold/` through `.tools/safe-apply.sh`, by the AE applier `0.7.0_AE_CloudOps~DB2`, after a bundle build of the function `irpt-49f-reporting-gold-lambda` through `infra/aws/lambda/ci/build-and-upload.sh`. The plan gate is exactly 0 add / 2 change / 0 destroy on `module.irpt_reporting_gold.aws_lambda_function.this` (memory 3008 to 8192 and the code hash) and `aws_iam_role_policy.irpt_reporting_gold` (four new statements and one extended write list). Anything else STOPS. Nothing else: no Cottonwood root, no schedule change, no other function, no gold object written by the apply itself.

## 2. What this seat measured and re-ran, and what it did not

- **Live state, read by this seat (read-only) at packet time:** the function (memory 3008, timeout 900, `CodeSha256` `J6M/92Mh...`, last modified 2026-10-13T12:39:43Z, equal to the source map's recorded deployed hash); the role policy (seven statements, by sid); the schedule (`cron(41 7 ? * MON-FRI *)` New York, ENABLED); the artifact bucket's versioning (`Enabled`).
- **The code and the Terraform, read line by line by this seat:** the handler diff of the split (`run_filled_day`, `owed_filled_days`, `invoke_next_day`, `filled_day_event`, `run`, `lambda_handler`); the Terraform diffs of the three grants, the invoke statement and the memory line. The criteria of rounds 121, 122 and 123 for these cells (the grants, the split, the stage memory, the memory edit) were RE-RUN by this seat in each worker's tree and, for rounds 121 and 122, again on the landed tree: PASS. The 120 tests of the handler's directory pass.
- **The numbers behind the memory ruling:** the 4,024.6 MB peak and the 154 s day are the worker's local measurements (workstation, one real day, 2026-10-13), checked by the checker's arithmetic; this seat did not repeat the 10-minute run.
- **NOT done by anyone:** a `terraform plan` of this change (no terraform binary on this seat's box); a live self-invoke; the Lambda's own memory and time at 8,192 MB.

## 3. Writers of the changed property, counted: N = 1 rule, 2 entry paths

The property is the content of the gold prefix `filled_report_values`. One rule writes it (`run_filled_day`), entered by the scheduled fire and by a `day` event. The new IAM write grant names that one prefix; the earlier five prefixes keep their one writer each and none of their rules changes.

## 4. Blast radius, and the limits this half signs under

- The apply changes no served value. After it, the first scheduled fire writes ONE new partition in a NEW prefix (no existing key is overwritten) and nothing pulls history; the earlier tables are written as on any day.
- **Honest limits, signed on:** the plan has never been run; the unqualified function ARN of the invoke grant may not match what a scheduled invocation reports (then the chain stops after the first day and nothing else is harmed); a failed invocation is retried by Lambda's async retry and re-runs the earlier stages (idempotent by design); the stage's real memory and time in the Lambda are unmeasured and the after-read records them.
- **Not covered:** a backfill of earlier days; any portal reader of the table; the Cottonwood landing; a change to the schedule.

## 5. Both branches

Branch A (the stage runs): the packet's section 3 and the after-read. Branch B (a read is denied, the invocation runs out of memory or time, or the self-invoke is refused): the packet's section 5; the earlier tables are written before the stage; the day is left unlanded and owed again at the next fire.

## 6. Conditions of this half

1. **Ledger first,** bound to the packet's sha256 (`irpt-dashbd-hop1-filled-report-values-20261015`; legs git, terraform, verify); `.open_deploys/` read across every live worktree with the denominator printed. 2. **Live state re-read at the moment of the apply** and equal to the packet's section 2, else STOP. 3. **The plan read first:** exactly 0/2/0 on the two addresses, else STOP; the bundle built from the pinned files and the three new members' pins and hashes written by the applier. 4. **Not within an hour before a scheduled fire, and not during another seat's open ledger entry on the root.** 5. **No `update-function-code`, no bare `terraform apply`, no manual write event without the CTO's word.** 6. **The applier is an AE seat the gates admit, not a worker.**

## 7. The three questions, from this seat (the CTO's half decides them)

1. **The unqualified ARN:** this seat recommends ACCEPT: the first fire is the first reading and the failure is bounded to the chain, not the tables.
2. **History:** ACCEPT one partition per fire and no backfill in this pair; the backfill is its own cell and pair.
3. **Async retry:** ACCEPT for this pair (the earlier stages are idempotent); setting `MaximumRetryAttempts` to 0 would be a third change and a different plan.

-- 2.0.0_SA_COO~D2
