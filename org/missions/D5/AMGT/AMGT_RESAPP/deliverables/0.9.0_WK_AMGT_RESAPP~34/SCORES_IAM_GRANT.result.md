# SCORES_IAM_GRANT -- result

**Worker:** `0.9.0_WK_AMGT_RESAPP~34`. **Act:** add exactly one entry, `"scores/v1/"`, to
`local.scoped_amgt_pool_prefixes` in `infra/aws/terraform/harvest/scoped-amgt-api.tf`, closing the
never-widen co-sign at `org/missions/D5/AMGT/AMGT_RESAPP/ledger/NEVER_WIDEN_ROUND13_SCORES_PREFIX_GRANT_{CTO,COO}_HALF.md`.
Branch `wk-amgt-13-scores-iam`, starting HEAD `8db1cd0a76`.

## 1. Ledger

Opened `org/critical_paths/change_management/20260918T0141Z_amgt-scores-v1-iam-grant-20260918_deploy_completion.md`
(slug `amgt-scores-v1-iam-grant-20260918`, window 2.0h) BEFORE the live act, 2 legs (L1 activation,
L2 verify). Both legs CLOSED with proof (below) and the ledger CLOSED before commit; sentinel
`org/critical_paths/.open_deploys/amgt-scores-v1-iam-grant-20260918.json` removed and committed
alongside the record, never left staged.

## 2. Pre-act measured state (rollback document)

`iam:GetRolePolicy` on `opal-amgt-scoped-api-role` / `opal-amgt-scoped-api-grants`, read fresh at the
act:

- `s3:GetObject` (`ReadThePoolPrefixesTheAdapterReads`): **12 entries**, `scores/v1/*` absent.
- `s3:ListBucket` StringLike (`ListOnlyThePoolPrefixesTheAdapterReads`): **12 entries**, `scores/v1/*`
  absent.
- Both lists matched exactly the CTO half's described pre-act state (publication-links/v1/,
  publications/v1/, universe/v1/, crosswalk/v1/, filings/v1/, drafting/v1/, peers/v1/, management/v1/,
  posture/v1/, derived/model_block/, packs/, raw/).

Full pre-act document: `.scratch/pre_act_policy.json` (worktree-local, not committed -- the rollback
value is recorded here and in the ledger's L1 proof string).

## 3. The Terraform change

`infra/aws/terraform/harvest/scoped-amgt-api.tf`:
- Appended `"scores/v1/",` to `local.scoped_amgt_pool_prefixes` (after `"raw/",`), with a new comment
  block naming the co-sign, the mandatory trailing slash, and the `derived/model_block/` /
  `derived/model_block_fye/` analogy the CTO half cites.
- Corrected the stale comment: replaced the "14 top-level prefixes ... lib/, packs/, raw/ and
  social/" text (measured 2026-09-16) with the current measured state: **16** top-level prefixes
  (live `list-objects-v2 --delimiter /` sweep: crosswalk/, derived/, drafting/, filings/, identity/,
  lib/, management/, packs/, peers/, posture/, publication-links/, publications/, raw/, scores/,
  social/, universe/), 12 granted before this act, ungranted set **after** this act = `identity/`,
  `lib/`, `social/` (`social/` deliberately, collection is RESERVED and OFF). No hand-edit to either
  IAM statement -- both recompute from the one list entry via the existing `for` expressions.

## 4. A blocking environmental precondition, worked around and reverted (see surprise row)

The first targeted plan failed before ever evaluating the target: `chatter-axis-schedule.tf:124`
`filebase64sha256()` reads a gitignored, never-committed build artifact
(`infra/aws/terraform/harvest/.build/chatter-axis-producer.zip`) that this fresh worktree never had,
and `-target` does not prune that evaluation out of the graph. The `.tf` file's own comment documents
the precondition ("Run it BEFORE terraform init/plan"), so this is a known but easily-tripped
worktree-provisioning gap, not a defect in the source. Worked around with a disposable placeholder
zip at the same path (arbitrary bytes, confirmed gitignored via `git check-ignore -v`, never staged
or committed) purely so `filebase64sha256()` had a file to hash; the targeted plan then evaluated
cleanly and named only the co-signed resource. The placeholder was deleted after the apply completed
and never touched any tracked file. Filed as `AMGT_RESAPP-Z-W34-S1` (OBSERVATION, ARMED -- the next
worker in this shared root will hit the identical block from a fresh worktree).

## 5. Targeted plan (pre-apply)

```
terraform -chdir=infra/aws/terraform/harvest plan -target=aws_iam_role_policy.scoped_amgt_api_grants -no-color -input=false
...
  # aws_iam_role_policy.scoped_amgt_api_grants will be updated in-place
  ~ resource "aws_iam_role_policy" "scoped_amgt_api_grants" {
      ~ policy = jsonencode(... + "arn:aws:s3:::opal-data-harvest/scores/v1/*" ... + "scores/v1/*" ...)
    }
Plan: 0 to add, 1 to change, 0 to destroy.
```
Named ONLY `aws_iam_role_policy.scoped_amgt_api_grants`. Discriminator satisfied (CTO half s.7 / COO
half s.3).

## 6. Apply

`HALT_ACK=1 bash .tools/safe-apply.sh -chdir=infra/aws/terraform/harvest apply -target=aws_iam_role_policy.scoped_amgt_api_grants -auto-approve -no-color`.

The HALT-GATE surfaced **182 pending routine messages** (no `[STOP]`/`[HALT]` subject on any of
them -- all `RED:`/`WARN:`/`HELD-STALE:` deploy-ledger bot notices, 20-46 days old, addressed to
`0.7.0_AE_CloudOps` / `0.6.0_AE_PartnerETL` about unrelated projects: `cot-pair-tolerance-recal`,
`emitter-wo4a-totals-refusal`, `inf-bronze-ac5-legA-20260724`, `freshguard-leg4/5`,
`scty-premcp-p1-layer2-phase1`, and many `UNINDEXED open deploy-completion ledger` gate-bypass scan
lines -- none reference AMGT_RESAPP or scores/v1). Grepped the full captured output for `[STOP]`/
`[HALT]`: zero hits. This is the routine base-inbox HALT-GATE the task's own instructions
pre-authorized `HALT_ACK=1` for; re-ran with `HALT_ACK=1` (rc=0):

```
Plan: 0 to add, 1 to change, 0 to destroy.
aws_iam_role_policy.scoped_amgt_api_grants: Modifying...
aws_iam_role_policy.scoped_amgt_api_grants: Modifications complete after 0s
Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
```

## 7. Post-act measured state

`iam:GetRolePolicy`, read fresh post-act:

- `s3:GetObject`: **13 entries**. Added: `arn:aws:s3:::opal-data-harvest/scores/v1/*`. Other 12
  confirmed byte-identical (order + content) to the pre-act read by direct list comparison.
- `s3:ListBucket` StringLike: **13 entries**. Added: `scores/v1/*`. Other 12 byte-identical to
  pre-act.
- **Negative control**: `identity/`, `lib/`, `social/` searched against both post-act limbs --
  **zero hits in either limb**. The grant widened by exactly the one prefix.
- `CodeSha256` on `opal-amgt-scoped-api`: `0l7f4YGikexrP7INF7q8r5k11+0J0BBxpJ6sYqP8Uyo=` -- unchanged,
  matching the pre-act anchor exactly (confirmed via `get-function-configuration`). No code deploy.

## 8. Post-act served read (the pass/fail line for this act)

`aws lambda invoke --function-name opal-amgt-scoped-api` against
`GET /api/scoped/amgt/security/ASML_NA_Equity/thesis` (`x-firm-id: bd`): **StatusCode 200**.

`body.scores`:
- `scores_status`: **`SERVED`** (was `READ_FAILED` pre-act on every covered name per row
  `AMGT_RESAPP-Z-W27-S11`'s live evidence -- this is the state transition the co-sign exists to
  produce).
- `as_of`: `2026-09-17`.
- `robustness.state`: `ABSENT_SOURCE` (`n=1 of 6` measured, below the `n>=5` eligibility floor --
  the same fiscal-year-model-block field gap the CTO half's row `Z-S162`-class already documents;
  unrelated to this grant).
- `peers_v.state`: `ABSENT_SOURCE` (`|K|=12` / `|M|=0`, below the `>=3` peer floor -- the same
  scanner-factor-vocabulary gap row `Z-S164` documents; unrelated to this grant).
- `divergence.state`: `ABSENT_SOURCE` (FWD-20's house FCF forecast producer does not exist yet --
  unrelated to this grant).

**No `AccessDenied`, no `READ_FAILED`.** Per both signed halves' section 6: an honestly-ABSENT
result on all three fields, with a completed read, is this act **SUCCEEDING**, not partially
failing. This is the state observed. The rollback branch (a second `AccessDenied` on the same
prefix) did **not** occur, so no rollback was performed.

## 9. Bounds held

No write/delete/tag action added to either limb. No prefix but `scores/v1/` (with its mandatory
trailing slash) added. No code/route/env/layer/timeout/memory change (`CodeSha256` unchanged). No
change to the other 12 prefixes (byte-identical, confirmed programmatically). No vendor call, no
producer re-run. Applied via `.tools/safe-apply.sh` only, Terraform only. No non-ASCII introduced.
Not pushed.

## 10. Committed paths

- `infra/aws/terraform/harvest/scoped-amgt-api.tf` (the one list entry + the stale-comment fix)
- `org/critical_paths/change_management/20260918T0141Z_amgt-scores-v1-iam-grant-20260918_deploy_completion.md`
- `org/critical_paths/.open_deploys/amgt-scores-v1-iam-grant-20260918.json` (sentinel removal)
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` (row
  `AMGT_RESAPP-Z-W34-S1`)
- `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~34/SCORES_IAM_GRANT.result.md`
  (this file)

Both signed halves' own obligations (CTO half s.7-8, COO half's "THIS HALF'S OWN OBLIGATION AT
DRAIN") are satisfied by the measured values above; the COO half's own file is left untouched here
per this worker's `<paths>` grant (it does not include `org/missions/D5/AMGT/AMGT_RESAPP/ledger/`) --
the issuing COO appends its own drain record to that file per its stated obligation.

Push state: LOCAL on SITEZ, branch `wk-amgt-13-scores-iam`.
