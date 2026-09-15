# fwd2-real-resource.result.md -- LGIC_ENFORCE.TO-EN-x-1 (0.9.0_WK_LGIC_ENFORCE~1)

Worktree `.worktrees/wk-lgic-enforce-1-1-x1`, branch `wk-lgic-enforce-1-1-x1`, base CLOUD @c6d652a6dc.
**Order stays OPEN: X1-AC3 is FAIL, blocked by row LGIC_ENFORCE-W1-S19.**

## What landed

- **Practice copy.** `git worktree add -b prac-lgic-enforce-x1 .worktrees/prac-lgic-enforce-x1 HEAD`. The scratch
  branch `prac-lgic-enforce-x1` holds one commit, `before` = 104f092d69, which adds
  `infra/aws/terraform/shared-infra/lgic-enforce-fwd2-resource.tf`. It declares `aws_sqs_queue.lgic_enforce_fwd2`,
  named by `module.opal_name_lgic_enforce_fwd2` (system `advi`, scope `49financial`, function `fwd2-exercise`, kind
  `queue`), which renders `advi-49f-fwd2-exercise-queue`. The branch was never pushed and is left in place. The practice
  copy was removed clean with `git worktree remove`.
- **Plan (read-only).** `init -lockfile=readonly -plugin-dir=<shared tree .terraform/providers>` against the real S3
  backend, with nothing downloaded; then `plan -lock=false -out` (rc 0) and `show -json` (rc 0), Terraform v1.9.8.
  `Plan: 7 to add, 0 to change, 0 to destroy.` The queue is one create; the other six are the fence probes (row W1-S20).
  Saved as `fwd2_plan.json` in this folder. **Nothing applied; safe-apply not run.**
- **`after` was not produced.** Changing `"short": "49f"` to `"f49"` in `scopes.json` is refused by
  `python lib/opal_naming.py validate` (rc 1): `REFUSED scopes.json[0].short: 'f49': NAMING_SCHEMA.json firm_forms gives '49f'`.
  `generate` refuses on the same cause (rc 1). The second pin, `org/standards/NAMING_SCHEMA.json:112-113`, is outside
  `<paths>`. The change was restored byte-for-byte (row W1-S19).
- **Record.** `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/EXERCISE_FWD2.md`: the prose, including why `advi`, and
  the json block, with `after: null`.

## Criteria (each run in the worktree, `timeout 120`, as written)

| id | verdict line | rc | status |
|---|---|---|---|
| X1-AC1 | `VERDICT: PASS-RESOURCE-IN-PLAN` (`RESOURCE: advi-49f-fwd2-exercise-queue`) | 0 | PASS |
| X1-AC2 | `VERDICT: PASS-SAME-ROW` (`FENCE PATTERNS: ['arn:aws:iam::313476888478:role/*-49f-*']  ROW: 49financial`) | 0 | PASS |
| X1-AC3 | `VERDICT: FAIL-NOT-BOTH` (`NEW SHORT FORM: f49  NAME LINES: 0  FENCE LINES: 0`) | 1 | FAIL |

## Rows filed

- LGIC_ENFORCE-W1-S19, BLOCKING, ARMED (disarm 2.0.0_SA_COO~G). The short form is pinned in `NAMING_SCHEMA.json`
  firm_forms, outside the grant, so step 2 cannot regenerate.
- LGIC_ENFORCE-W1-S20, OBSERVATION, ARMED (disarm 2.0.0_SA_COO~G). CLOUD @c6d652a6dc still declares the probe roles
  EN-f-2 removed from AWS, and every shared-infra plan from CLOUD creates 6 of them.
- LGIC_ENFORCE-W1-S21, OBSERVATION, ARMED (disarm 2.0.0_SA_COO~G). x1-moves-both's name-line and fence-line filters
  both match the fence-pattern line, so X1-AC3 cannot tell the resource name moving from the pattern moving.

## Not claimed

- The resource's name moving under the short-form change. It was never exercised, because no `after` exists.
- Any live state beyond the plan's own refresh: nothing was applied or read otherwise.
