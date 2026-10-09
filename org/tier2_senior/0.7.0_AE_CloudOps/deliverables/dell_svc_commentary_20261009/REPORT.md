# NFRA_CTLPLN TO24 svc-commentary IAM apply

## Applied 2026-10-09T02:03:17Z

`NFRA_CTLPLN.TO-APPLY-24` added exactly `arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/ticketing/svc-commentary-pXsmuU` to `aws_iam_policy.dell_agent_platform_secrets[0]`. The saved IAM policy version was `v2`; the live default version after apply is `v3`.

The default-variable plan was exactly `0 to add, 1 to change, 0 to destroy`. It changed only the ordered address, added the one requested ARN, removed no ARN, and was otherwise structurally identical. `.tools/safe-apply.sh` completed the saved plan once with the same `0/1/0` count.

The live policy matches the saved plan. Exact-resource IAM simulations returned:

- dell1 on the svc-commentary ARN: `allowed`
- dell1 on `opal/ticketing/svc-commentary-other`: `implicitDeny`
- dell2 on the svc-commentary ARN: `allowed`
- dell2 on `opal/ticketing/svc-commentary-other`: `implicitDeny`

The routed `comp-iam-usage reach-check` accepts roles and returned `UNKNOWN` for these IAM users. The authoritative evidence therefore uses four separate `aws iam simulate-principal-policy` calls, one resource ARN per call. No secret value was read.

The untargeted default-variable replan returned exit `0` with no changes. The deployment ledger `org/critical_paths/change_management/20261009T0201Z_dell-svc-commentary-to24-laptop-20261009_deploy_completion.md` is closed and its sentinel is removed. Opening commit: `47284bfdee`. Evidence is in this directory, principally `plan-verdict.json`, `apply.txt`, `after-policy.json`, `live-simulations.json`, `live-verdict.json`, and `replan.txt`.
