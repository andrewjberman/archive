# NFRA_CTLPLN.TO-APPLY-29 -- applied report

**archetype:** DEPLOY
**seat:** 0.7.0_AE_CloudOps~CTL | **issuer:** 2.0.0_SA_COO~C | **risk:** WORLD | **date:** 2026-10-09

## APPLIED TIME

`2026-10-09T12:21:00Z` (live `get-policy` UpdateDate on both policies; `safe-apply` returned 12:20:59Z).

## The act, in order

| step | evidence |
|---|---|
| trunk | `box/laptop` @`0e6e70363e`; `git merge-base --is-ancestor 97fb0b2abf HEAD` = CONTAINED |
| saved default version ids (step 1) | `cloudops-dell-agent-plan-reads-policy` **v2** (UpdateDate 2026-10-09T01:26:36Z); `cloudops-dell-agent-platform-secrets-policy` **v3** (2026-10-09T02:03:17Z) |
| plan (step 2, untargeted, default variables) | `Plan: 0 to add, 2 to change, 0 to destroy` on exactly `aws_iam_policy.dell_agent_plan_reads` and `aws_iam_policy.dell_agent_platform_secrets[0]`; 18 diff-marked lines, **0 removals** (`'-' lines: 0`) |
| what the plan added | plan reads: one statement `Sid=ReadSesConfigurationSetPlanReads`, `Action=ses:DescribeConfigurationSet`, `Resource=["*"]`. platform secrets: one element, `arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/investor-reporting/svc-custody-statement-9CmPmS` |
| NEVER-2 entry (step 3) | `org/critical_paths/change_management/20261009T1214Z_nfra-ctlpln-to29-dell-ses-custody-laptop-20261009_deploy_completion.md`, OPENED 12:14Z, 2 legs, rollback = re-apply at the merge's first parent `ee9dd2f594` |
| apply (step 4) | ONE `.tools/safe-apply.sh ... apply <saved plan>`; `Apply complete! Resources: 0 added, 2 changed, 0 destroyed` |
| new default versions | plan reads **v2 -> v3**; platform secrets **v3 -> v4**; both UpdateDate `2026-10-09T12:21:00Z` |
| re-plan (AC1) | `exit=0`, `No changes. Your infrastructure matches the configuration.` |

## Read-back, live simulation only -- 8 of 8 arms (step 5)

One `--resource-arns` per call (IAM trap 1); each allow arm run as its own invocation beside its deny.

| arm | cloudops-dell1-agent-user | cloudops-dell2-agent-user | expected |
|---|---|---|---|
| `ses:DescribeConfigurationSet` | allowed | allowed | allowed |
| `ses:DeleteConfigurationSet` | implicitDeny | implicitDeny | refused |
| `GetSecretValue` on `...svc-custody-statement-9CmPmS` | allowed | allowed | allowed |
| `GetSecretValue` on `...svc-custody-statement-other` | implicitDeny | implicitDeny | refused |

**Trap-3 control:** `aws accessanalyzer validate-policy` over `ses:DescribeConfigurationSet`,
`ses:DeleteConfigurationSet` and `secretsmanager:GetSecretValue` returned **zero** `ERROR` findings, so no
`implicitDeny` above is a mistyped action name.

**No secret value was read.** Zero `GetSecretValue` API calls were made by this seat; every secret-facing
call was `iam simulate-principal-policy`, which evaluates policy and returns no value.

## Gate output worth recording

`safe-apply`'s seat-gates limb printed `CROSSBOX-DEPLOY ... verdict=STOP` in **WARN** mode on two hits:

1. `OPEN-CALL org/devices/crossbox/XB-20261009T093642Z-9ec5.json` (OPEN, laptop -> dell1). **Read it:** it is an
   ORDER to `0.7.0_AE_CloudOps~CT1` to `safe-commit` surprise rows `NFRA_CTLPLN-CT1-S1/-S2` because dell1's
   box-sync is HELD. It carries no apply and no write to this root; the token match comes from its
   `body_path` investigation file.
2. `OPEN-DEPLOY` -- a self-hit on the entry this seat had opened 2 minutes earlier.

Concurrency check before proceeding: `git worktree list --porcelain` = **1** live worktree; a per-tree
`ls-tree` of `org/critical_paths/.open_deploys/` = **27** entries, of which **1** names
`nfra-ctlpln-identity` -- this seat's own. The decisive control is that the plan reproduced the issuer's
~11:0xZ measurement exactly (`0/2/0`, same two addresses), which no concurrent write to the root would have
left intact.

`naming-plan-gate`: PASS, 14 resource names graded. `tombstone-gate`: CLEAN, 0 creates. `tag-authz`: SKIPPED
(no provider `default_tags` block in this root). HALT-gate surfaced 3 routine messages from
`2.0.0_SA_COO~C` -- all three already read and acked, one of them the GO for this apply -- then `HALT_ACK=1`.
Per Rule 18 a HALTGT pass is cited by nobody and is not cited here.

## Compiler tools

- `comp-to NFRA_CTLPLN.TO-APPLY-29...` -- session TO_ID set.
- `comp-iam gaps` (AE minimum after the `iam.tf` change that arrived in @`97fb0b2abf`): 886 calls verdicted
  across 105 mapped roles; 38 missing / 302 deny-present / 1 coverage-unknown / 3 resource-mismatch across 34
  services. **Zero** rows name either graded policy. The 3 resource-mismatch rows sit in
  `etfs-reports-reporter`, `opal-gateway` (x2) -- a standing census owned elsewhere, not re-filed here.
  Necessary, not sufficient: it models `(action)`, never `(action, resource)`.
- `comp-find` was the rail's answer to one denied directory-scoped grep; the resolution used a named-file
  read and `terraform state show` instead.

## Scratch

`to29.tfplan`, `to29_plan.txt`, `to29_apply.txt`, `to29_replan.txt`, `actcheck.json` were written to the
session scratchpad and deleted at close.
