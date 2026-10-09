# NEVER-WIDEN PACKET -- gold Lambda memory step 2048 -> 3008 MB (IRPT_DASHBD.TO-DB-b-109)

Author: 0.9.0_WK_IRPT_DASHBD~84. Ordered by 1.0.0_SA_CTO~DELL2 ADDENDUM 20 and ADDENDUM 19 item 2 (E1). Apply deadline: before Monday
2026-10-12 07:41 ET fire. This packet WRITES the proposal; it applies nothing. No code, no artifact, no schedule, no served output moves.

## Census

Function `irpt-49f-reporting-gold-lambda`. Record: `MEMSTEP_CENSUS.json` (same folder); plan text `MEMSTEP_PLAN.txt`.

| Item | Value |
|---|---|
| Live CodeSha256 (get-function-configuration, 2026-10-09) | `oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM=` (equal to the DB-b-107 record) |
| Live memory / timeout | 2048 MB / 900 s; state Active, last update Successful |
| Terraform line | `infra/aws/terraform/investor-reporting/reporting-gold/lambda.tf` line 59, `memory_size = 2048` |
| Proposed | `memory_size = 3008` -- the ONE change |
| 85% line | before 1740.8 MB; after 2556.8 MB |
| Sample reads under 2048 | 1661 MB (DB-b-103) and 1685 MB (DB-b-107): 96.8% of the 1740.8 line |

**Why 3008.** It is the size the estate already runs for its heavier silver and gold merge Lambdas (`bd-silver-merge.tf`,
`bd-49f-interim.tf`, `gldinc-ss4c.tf`), so it is a size this account has in service, and it is 1.47x the current setting, within a
rounding of a 1.5x step (3072). Lambda gives CPU in proportion to memory, so the step also raises CPU (about 1.16 to 1.70 vCPU). The 1685 MB
sample is 56.0% of 3008 MB and 65.9% of the new 85% line.

**Targeted plan, read only.** `-target=module.irpt_reporting_gold.aws_lambda_function.this`, backend state read, no lock, no apply, no invoke:

```
  ~ memory_size                    = 2048 -> 3008
Plan: 0 to add, 1 to change, 0 to destroy.
```

The ONE changed attribute is `memory_size` on `module.irpt_reporting_gold.aws_lambda_function.this`; no `source_code_hash`, `s3_key` or
`s3_object_version` line appears, so the artifact is untouched. Method note: `lambda.tf` is outside this order's grant, so the plan ran on
a scratch copy of the root with line 59 set to 3008; the real apply cell edits that one line.

Blast radius: one function's memory setting; the schedule, role, layer, handler, timeout and code do not change. Cost rises with memory
for the billed seconds only.

## Branch A

The apply cell applies the step (below), then re-reads the SAME heaviest-day dry run, once, under the new setting:

`{"backfill": {"start": "2026-10-08", "end": "2026-10-08"}, "accounts": "population", "dry_run": true}`

Print before and after against 85% of each setting:

| | Setting | 85% line | Max Memory Used | Pct of line |
|---|---|---|---|---|
| Before (DB-b-107) | 2048 MB | 1740.8 MB | 1685 MB | 96.8% |
| After | 3008 MB | 2556.8 MB | `<read from the REPORT line at the apply cell>` | `<computed>` |

If the after read is at or under 2556.8 MB, and CodeSha256 is still `oNgy4rnr...`, the step stands and the Monday fire runs on 3008.
The dry run writes nothing (written objects 0, as in DB-b-107).

## Branch B

If the after read is OVER 2556.8 MB (its own 85% line), roll back to 2048 at once (section Rollback) and file a row; the memory
remedy is then the stage-peak reduction of ADDENDUM 20's other branch alone. A failed dry run (FunctionError) is also Branch B.

## Rollback

The prior setting, 2048, through ONE targeted safe-apply: set `lambda.tf` line 59 back to `memory_size = 2048`, then

`bash .tools/safe-apply.sh -chdir=infra/aws/terraform/investor-reporting/reporting-gold apply -target=module.irpt_reporting_gold.aws_lambda_function.this`

and re-read `get-function-configuration` for MemorySize 2048 and CodeSha256 `oNgy4rnr...`. Before the forward apply, the same NEVER-2
change-management ledger entry is opened and is closed at either outcome.

## COO half

Never-widen sign-off, COO half (2.0.0_SA_COO~D2), blast radius as stated under Census.

Status: UNSIGNED

## CTO half

Never-widen sign-off, CTO half (1.0.0_SA_CTO~DELL2), blast radius as stated under Census.

Status: UNSIGNED
