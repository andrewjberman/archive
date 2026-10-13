# NEVER-WIDEN -- COO HALF: disable the 3 AM WSJ/FT morning-brief schedule `astn-wsjft-3am-run`, `HVST-bz-8` (round 84, workstream BRIEFOFF)

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-13 ~20:4xZ. **Pairs with:** `1.0.0_SA_CTO~DELL1`'s half at `ledger/NEVER_WIDEN_ROUND84_BZ8_CTO_HALF.md` (owed).
**Authority for the act itself:** Andrew-direct ~20:0xZ call 7 (CTO msg 5131): "No let's turn that off we don't need that."

## THE ACT, in the order's words

Dell1, once, by `0.7.0_AE_CloudOps~HV1` in its own worktree:
1. Open a deploy-completion ledger entry (EDIT, APPLY, VERIFY legs).
2. Edit ONE attribute in `infra/aws/terraform/astn-pipeline/orchestrator.tf`: `aws_scheduler_schedule.astn_run` line 175, `state = "ENABLED"` to `"DISABLED"` (plus one comment line). No other line moves.
3. `terraform plan -target=aws_scheduler_schedule.astn_run -out=...` and READ it: exactly `0 to add, 1 to change, 0 to destroy`, the one change `state: "ENABLED" -> "DISABLED"`. Anything else is a STOP with no apply.
4. `.tools/safe-apply.sh -chdir=... apply <that saved plan>`. Never a CLI edit of the schedule.
5. Read back AC1 (State), AC2 (expression unchanged), AC3 (source agrees); close the ledger.

## BLAST RADIUS

- **Writers of the property N = 1.** `state` of the schedule `astn-wsjft-3am-run` is written by one Terraform resource, `aws_scheduler_schedule.astn_run` (`comp-find` over the module's four `.tf` files:
  1 hit for the scheduler resource). Live denominator: `aws scheduler list-schedules --name-prefix astn` returns 1 schedule, `aws events list-rules --name-prefix astn` returns 0. N = 1 rule read: the resource's own `state` attribute.
- **What it touches in the world:** the nightly 03:00 ET invocation of Lambda `astn-wsjft-orchestrator` with `{"mode":"run"}` stops. That run pulled WSJ and FT news through Bright Data, summarised it, and emailed the digest
  through SES to its recipient. After the act that email stops arriving. Nothing else consumes the schedule.
- **Not touched:** the schedule's expression, timezone, target and input (AC2 reads the expression); the Lambda and its code; IAM roles and policies; the bucket `opal-data-astn` and its contents; the SNS topic; SES; the EC2 instance;
  the `absence_check` mode (its own schedule was torn down earlier, commit 0ee89c9826); every other Terraform resource in the module (the plan is targeted and must read 0/1/0).
- **Served output moved:** one. The digest email for the 2026-10-14 03:00 ET run (and every run after) is not sent. That is the intended effect, ordered by Andrew.
- **Rollback, per key:** set `state` back to `"ENABLED"` in `orchestrator.tf`, plan targeted (0/1/0), `safe-apply` the saved plan. The next 03:00 ET fire runs. Nothing is deleted, so nothing is rebuilt. The schedule's last modification
  date (2026-06-25) is the "before" the AC2 and the plan's prior-state read pin.

## BOTH BRANCHES (the half is signed for BOTH or for neither)

- **Branch D (the schedule reads `ENABLED`, the targeted plan reads 0/1/0, the apply completes):** the schedule is `DISABLED`, the source agrees, the criteria hold.
- **Branch S (the schedule already reads `DISABLED` at the start):** no edit, no plan, no apply; AC1 and AC2 hold on the existing state, and AC3 is read on the source (if the source still says `"ENABLED"`, the
  seat edits ONLY the source line and commits it, because a source that disagrees with the world would re-enable the schedule at the next module apply; that one edit takes a targeted plan that must read `No changes`).
- **Branch P (the plan reads anything other than 0/1/0):** NO apply, one row, the question returns to the issuer.

## WHAT THIS HALF DOES NOT COVER
- Deleting the schedule, the Lambda, the bucket, the SNS topic or the instance; an untargeted `terraform apply`; a CLI-side edit (`aws scheduler update-schedule` or any other).
- Any change to the digest's content, its recipients or the dormant FT-reattempt code.
- Re-enabling it (a separate act on a separate word).

## VERDICT: SIGNED (COO). Not started until the CTO half is on file.
