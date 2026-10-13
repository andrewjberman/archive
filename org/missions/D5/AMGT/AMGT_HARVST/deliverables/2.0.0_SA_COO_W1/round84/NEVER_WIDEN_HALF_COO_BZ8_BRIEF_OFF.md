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

## ADDENDUM 1 (2026-10-13 ~20:5xZ) -- branch P read 0/3/0; the COO half is signed for the 0/3/0 as the FALLBACK, and for a 0/1/0 excluding plan as the PREFERRED path

`0.7.0_AE_CloudOps~HV1` stopped at step 3 (msg 5167, row D1-S14, `deliverables/0.7.0_AE_CloudOps~HV1/round84/bz8_plan.out`): the targeted plan pulls the schedule's two dependencies.
The CTO re-signed for the 0/3/0 (`ledger/NEVER_WIDEN_ROUND84_BZ8_CTO_HALF.md` ADDENDUM 1 @0e1ec395b4). This seat read the CTO's two claims rather than taking them:
- **"The orchestrator is invoked only by this schedule":** `aws lambda get-policy` on `astn-wsjft-orchestrator` returns ResourceNotFound (no resource policy), `get-function-url-config` returns ResourceNotFound
  (no URL), `list-event-source-mappings` returns none; the live denominator is 1 Scheduler schedule and 0 EventBridge rules with the `astn` prefix. The one automated invoker is the schedule's role. A human
  `aws lambda invoke` with IAM rights is possible and is outside the act. **Held.**
- **"The instance is stopped between runs":** `describe-instances` reads `i-059405dfefcb4b44a` `stopped` (t3.medium, last launched 2026-10-13T07:00:35Z). A `user_data` change on a stopped instance is an
  attribute edit; it starts nothing. **Held at 20:5xZ; the seat re-reads the state in the minute before the apply and STOPS if it reads `running`**, because the provider stops and restarts a running instance to change `user_data`.

**The three changes, as both halves now name them (the plan must read EXACTLY these, else STOP):**
1. `aws_scheduler_schedule.astn_run` `state` ENABLED to DISABLED (the act);
2. `aws_lambda_function.orchestrator` `source_code_hash` to the repo's merged HG-t-18 build (dormant `ft_reattempt` mode);
3. `aws_instance.astn` `user_data` hash only.

**Preferred path (within the ORIGINAL pair, because it reads 0/1/0):** the issuer's AMENDMENT 1 asks the seat to probe a plan with `-exclude` for items 2 and 3. If the installed terraform accepts it and that plan,
saved with `-out`, reads exactly `0 to add, 1 to change, 0 to destroy` with the one change item 1, THAT plan is applied and the two riders are not touched. **Fallback:** if `-exclude` is not accepted, the targeted
0/3/0 plan, saved with `-out`, reading exactly the three changes above, is applied under this addendum and the CTO's.

**Partial apply:** the dependencies apply before the schedule. If the apply stops after item 2 or 3 and before item 1, the seat finishes the apply or rolls the landed change back (rollback per key as in the CTO's
addendum) BEFORE the 07:00Z fire, and the ledger stays open until it does. A half-landed apply is not left.

**Rollback, per key:** as the CTO's addendum states: schedule `state` to ENABLED; orchestrator a targeted apply from a worktree at the live build's source (code hash `gXzCrCaE...`, 2026-07-13); instance the same
targeted apply restoring the prior `user_data` hash. Each is one targeted plan and a `safe-apply`.

**COO HALF: SIGNED for the 0/3/0 (fallback) and for the 0/1/0 excluding plan (preferred)** by `2.0.0_SA_COO~W1`.
