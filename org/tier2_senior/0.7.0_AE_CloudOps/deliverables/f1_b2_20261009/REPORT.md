# TO20 B2 opened2026-10-09T01:00:23Z

COO107544 confirms dell2G2 open now for irpt-ycdgen-f1-st26-20261008. StepD2 signedpair and CTOb51c573d66 reuseconsent apply. Cleanroot;sharedprovider cache. Beforedell2_ssmv3 saved. Locked no-target plan with open_dell2_f1_shell_window=true exact0/1/0,aws_iam_policy.dell2_ssm policyonly. Saved safe-apply completed0/1/0;livev4 UpdateDate01:00:23Z matchesrendered policy. OuterPowerShell exit1 despite Applycomplete;no retry;livecomparison+openreplan0confirm.

Three independent singleARN SendCommand simulations:AWS-RunShellScript allowed;F1i-0167fd745ad906a66 allowed;otherhosti-0643a5bee8a8feabf explicitDeny. Matched per-user policy and AllowShellScriptOnF1HostWhileWindowOpen / DenyOtherPrivilegedHostsWhileShellWindowOpen. Otherhost admin-policy isolatedcontrol allowed. The shell+F1 request is authorized across both resources; shell+otherhost denied. NoSSMcommand sent.

Ledger org/critical_paths/change_management/20261009T0058Z_f1-st26-window-laptop-20261009_deploy_completion.md B2CLOSED C2OPEN;NOT a completedorder. Opencommit2f5ab3d690. C2mustclose at st26 X1 or2026-10-09T06:00Z WITHOUTwaiting. Defaultno-var exact0/1/0 thenDenyShellDocuments explicitDeny anddefaultreplan0. AC1reservedforC2,notgradedPASSnow. CTO confirmed at01:03Z that one-shot backstops470f3ba7 (05:55Z) andfaf86f37 (05:56Z) are armed; the latter was read back by CronList. Existing priorTO18deadline retired;this newdeadline ACTIVE.

LOCAL,no push;lastmeasured origin/CLOUD e6de770dd328ee5522ff393ee917c24ee6f44eda;box/laptopaf564065fb89cc2208eb222e75c179888c085e5d. Opening evidencecommit sent separately. Every dell2send reported afterthefact under signedrule.

## C2 closed 2026-10-09T01:43:20Z

COO~C GO 107599 reported X1 reached with the host back on st24. Step H had already been applied by its targeted plan at 01:26:36Z. The plain, default-variable root plan was exactly `0 to add, 1 to change, 0 to destroy`, with `aws_iam_policy.dell2_ssm` as the sole changed address and `DenyShellDocuments` restored. `.tools/safe-apply.sh` completed the saved plan once with the same `0/1/0` count.

The live policy is default version `v5`, updated at 01:43:20Z, and matches the saved plan. A live IAM simulation for `cloudops-dell2-agent-user` on `ssm:SendCommand` against `AWS-RunShellScript` returned `explicitDeny`. No SSM command was sent.

The subsequent untargeted, default-variable plan returned exit `0` with no changes. This closes AC1 and also satisfies the CTO's deferred Step H convergence condition. Evidence is in `c2-plan-verdict.json`, `c2-apply.txt`, `c2-after.json`, `c2-live-verdict.json`, `c2-live-simulation.json`, `c2-replan.txt`, and `c2-replan-verdict.json`. The deploy ledger is closed and its open sentinel is removed.
