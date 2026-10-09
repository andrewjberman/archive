# NFRA_CTLPLN TO25 st27 F1 shell window

## B2 opened 2026-10-09T02:37:46Z

COO~C GO 107651 and CTO consent 107649 authorize the st27 window for dell2 ledger `irpt-ycdgen-st27-20261009`. The saved IAM policy version was `v5`.

The targeted plan used `-target=aws_iam_policy.dell2_ssm` and `open_dell2_f1_shell_window=true`. It was exactly `0 to add, 1 to change, 0 to destroy` on the one ordered address. The plan allows `AWS-RunShellScript` only with F1 `i-0167fd745ad906a66` and keeps the named other privileged host `i-0643a5bee8a8feabf` in the explicit-deny set. `.tools/safe-apply.sh` completed the saved plan once with the same `0/1/0` count.

The live policy is default version `v6`, updated at 02:37:46Z, and matches the saved plan. Three separate exact-resource IAM simulations returned:

- `AWS-RunShellScript`: `allowed`
- F1 `i-0167fd745ad906a66`: `allowed`
- other host `i-0643a5bee8a8feabf`: `explicitDeny`

No SSM command was sent. The targeted open-state replan returned exit `0` with no changes.

Ledger `org/critical_paths/change_management/20261009T0235Z_f1-st27-window-laptop-20261009_deploy_completion.md` has B2 closed and C2 open. Opening commit: `33a166d716`. C2 must run on dell2 V1 or at 2026-10-09T06:00Z without waiting. It requires a plain exact `0/1/0` close, `DenyShellDocuments` explicit deny, an untargeted default-variable `0/0/0` plan, closure of the ledger, and deletion of the retained Terraform scratch directory.
