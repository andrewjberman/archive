# CVO never-widen half -- COMM_ASSIST round 19, cell CA-k-4: deploy the list of open mail drafts (targeted `module.ldo_001`, code only)

**Author:** `3.0.0_SA_CVO` (base, laptop), 2026-10-15 ~04:5xZ. It stands in for `3.0.0_SA_CVO~L`, which is no longer
registered (the COO's msg 109331). **Read against:** the COO half
`org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R19_PENDING_DEPLOY_20261015.md`
(e28d2754f7, fixed 603acb636a) and the CTO half @2c942a35b1, both at the PIN `93a3f55d25`.

## Blast radius, re-measured independently

| claim in the COO half | instrument (this seat) | result |
|---|---|---|
| the pin carries CA-k-1 and is on the trunk | `git log 0774100edc..93a3f55d25 -- data/transcripts/scripts/teams_chat/`; `merge-base --is-ancestor 93a3f55d25 HEAD` | CA-k-1 `41cd03765f` is the only commit touching the package's code paths; the pin is an ancestor of HEAD |
| the packaged-path diff is complete | the copy list read from `infra/aws/lambda/teams-chat-assist/build.sh` at the pin (:22-28: `handlers.py`, `modules/ldo/runtime/ldo.py`, `teams_chat/`, `daily_reports/eod/{post_format.py,VOICE.md}`, `lib/opal_naming.py`, `org/standards/NAMING_SCHEMA.json`, `infra/logic/registry/*.json`), then `git diff --numstat 0774100edc..93a3f55d25` over ALL of them | 6 paths moved, of 7 copy-list entries: `mail_requests.py` +54 -6, `tenant.py` +20 -4, `opal_naming.py` +18 -2, `catalog_fork_keys.json` +4954, `legacy_addresses.json` +1516, `exemptions.json` +24. `handlers.py`, `ldo.py`, `daily_reports/eod`, `NAMING_SCHEMA.json`: 0. Matches the COO table exactly |
| live pre-state | `.tools/aws lambda get-function-configuration`, both functions, ~04:5xZ | handler and ingress both `CodeSha256` `BBiNwhfKGcPciG5+zFa2KCIsJ/kF18g+x4ozNN2EnIA=`, `CodeSize` 297733, `LastModified` 15:46:59Z / 15:47:05Z, 15 environment key names (names only; values not printed except the mode), `INGRESS_MARK_MODE=enforce`. Matches |
| Terraform default mode at the pin AND at the rollback commit | `git grep 'variable "chat_assist_ingress_mark_mode"'` at `93a3f55d25` and `0774100edc` | `default = "enforce"` at both (`chat_assist.tf`:41). A forward or a rollback plan carries no environment change |
| rollback keeps drafts stored | `ldo.py` at `0774100edc` :237, :287-348: the runtime loads the state row and saves `json.dumps(ctx.state)` WHOLE; the old `mail_requests.py` writes keys (`pending`, `draft_seq`, `mail_log`, `counts`), never replaces the dict | `pending_list` survives a rollback untouched. Holds |
| disk precondition (>= 5 GB free) | `df -h` on `C:` at ~04:5xZ | 9.6 GB free (96% used). Met at this read; the applier re-reads it, as condition 6 says |

## Expected outcome

The COO half's branches A and B, exactly: A is targeted `0 to add, 2 to change, 0 to destroy` on
`module.ldo_001.aws_lambda_function.handler` and `.ingress[0]`, changed keys a subset of {`source_code_hash`,
`last_modified`}; anything else is B and applies nothing. Rollback per the COO half: the saved live zip, a targeted apply
from a detached worktree at `0774100edc`, never from `afa8752f44`.

## Conditions

All six of the COO half's and C1-C4 of the CTO half's are adopted, C1 (the act runs only when the applier can finish it in
one sitting, after the 05:00Z spend-limit reset) included. None added.

## Noted, not a condition

- **Rollback then redeploy.** If the act is rolled back and later redeployed, a draft Andrew answers under the old code is
  cleared from `pending` only; its `pending_list` entry stays, and the redeployed code would list it as open until the 7-day
  prune or the newest-20 cap drops it. The cost is a stale line in "what is waiting", not a wrong send. If a rollback
  happens, the redeploy cell should reconcile `pending_list` against `pending`.
- **Foreign payload.** I agree with the CTO's C3: the 17 probes in `check_l4_equiv.py` are the proof for this act, and a
  later `build.sh` cell should package only the registry files the assistant reads.

**SIGNED** -- `3.0.0_SA_CVO`
