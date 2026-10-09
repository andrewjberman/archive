# NFRA_CTLPLN Step H targeted apply

## Applied 2026-10-09T01:26:36Z

`NFRA_CTLPLN.TO-APPLY-22` was applied only to `aws_iam_policy.dell_agent_plan_reads` while the separate F1 shell window remained open. The saved IAM policy version was `v1`; the live default version after apply is `v2`.

The targeted plan was exactly `0 to add, 1 to change, 0 to destroy`. It added the single `ReadUiWalkerPassword` statement for `ssm:GetParameter` on `arn:aws:ssm:us-east-1:313476888478:parameter/opal/ui-walker/password`, removed nothing, and did not contain `aws_iam_policy.dell2_ssm`. `.tools/safe-apply.sh` completed with the same `0/1/0` count. No parameter value was read.

Live IAM simulations passed all six required arms:

- dell1 `ssm:GetParameter`: `allowed`
- dell1 `ssm:DeleteParameter`: `implicitDeny`
- dell2 `ssm:GetParameter`: `allowed`
- dell2 `ssm:DeleteParameter`: `implicitDeny`
- dell2 `ssm:SendCommand` on `AWS-RunShellScript`: `allowed`
- dell2 `ssm:SendCommand` on F1 `i-0167fd745ad906a66`: `allowed`

The targeted replan returned exit `0` with no changes. The deploy ledger `org/critical_paths/change_management/20261009T0125Z_dell-steph-laptop-20261009_deploy_completion.md` is closed and its sentinel is removed. Evidence is in this directory, principally `plan-verdict.json`, `apply.txt`, `after.json`, and `replan.txt`.

The CTO-required untargeted convergence read remains deferred until `TO-APPLY-20` leg C2 closes. Running it while C2 is open would include the shell-window closure, so it is outside this targeted order until that trigger occurs.
