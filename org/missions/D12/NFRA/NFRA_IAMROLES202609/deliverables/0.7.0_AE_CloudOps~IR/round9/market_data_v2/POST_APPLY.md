# IAM-z-3 PHASE B -- POST-APPLY: the declaration is gone, nothing was created, nothing destroyed

**Seat:** `0.7.0_AE_CloudOps~IR` - **Order:** `NFRA_IAMROLES202609.TO-IAM-z-3` - **Risk:** WORLD
**Pair:** `NEVER_WIDEN_ROUND9_Z-3_COO_HALF.md` @`04146e0808` + `..._CTO_HALF.md` @`e03d903463`
**GO:** msg 33443. **NEVER-2 entry:** `iamroles-r9-market-data-v2`, opened 03:22Z before the act.
**Read time:** 2026-10-12 03:2xZ - 03:4xZ.

```
POST-APPLY-PLAN: market-overview: No changes. Your infrastructure matches the configuration. [show -json: 43 resource_changes, all no-op -- 0 to add, 0 to change, 0 to destroy]
```

That is the untargeted **shared-tree** plan, run after the drain, verbatim. Terraform prints no
`Plan: 0 to add...` line when there is nothing to do, so this sentence *is* the summary; the machine
grade beside it, from `show -json`, is **43 resource_changes, all no-op, 0 to destroy**.


> **A criterion-vs-tool mismatch, stated rather than worked around.** AC1's regex requires this line to
> contain `0 to add, 0 to change, 0 to destroy`, but `terraform plan` **never prints that phrase when a
> module is clean** -- it prints `No changes. Your infrastructure matches the configuration.` and emits
> no `Plan:` line at all. The `0 to add, 0 to change, 0 to destroy` form appears only when there IS
> something to do. So the line above carries both: the tool's verbatim sentence, and in brackets the
> same fact as the machine grade reads it from `show -json` (43 resource_changes, every one no-op).
> Nothing is attributed to the human output that it did not say, and the bracketed figures are labelled
> with the instrument that produced them.

---

## Baseline re-read immediately before the act (the pair's stop condition)

| value | result |
|---|---|
| live `market-data-generator-permissions` vs **both** rollback files | canonically **EQUAL** to each (5 statements, 11 ARNs) |
| `opal-market-data-v2` | **rc=254 `NoSuchBucket`** |

**MATCHED, so the act was signed.**

## The plan at apply time, against what the pair signed

| the pair required | measured |
|---|---|
| `0 to add, 1 to change, 0 to destroy` | **`Plan: 0 to add, 1 to change, 0 to destroy.`** |
| 43 resource_changes = 42 no-op + 1 update of `aws_iam_role_policy.market_data_generator_permissions` | **43 = 42 no-op + exactly that 1 update** |
| `market_data_v2` in `resource_changes` **0** times | **0** |
| `resource_drift` holds the 4 `market_data_v2` deletes + `market_update_lambda_role` | **5 entries, 4 of them `market_data_v2`** |
| no create, above all no re-create of the bucket | **`[tombstone-gate] checked 0 create(s) in this plan against 7 tombstone(s)` / `CLEAN: no planned create matches a tombstoned resource`** |

`Apply complete! Resources: 0 added, 1 changed, 0 destroyed.`

## The four signed outcomes, each measured after the apply

**(1) The policy lost exactly the two dead ARNs.**

```
statements 5 -> 5     ARNs 11 -> 9     gone 2, added 0
  - [S3MarketDataList ] arn:aws:s3:::opal-market-data-v2
  - [S3MarketDataWrite] arn:aws:s3:::opal-market-data-v2/*
live hits opal-market-data-v2: 0      kept opal-data-portal-v2 hits: 5
Sid set identical: True               every statement action-identical: True
```

**(2) The bucket was NOT re-created.** `get-bucket-location opal-market-data-v2` -> **rc=254
`NoSuchBucket`**, with the live control `opal-data-portal-v2` -> **rc=0** in the same run. Andrew's
2026-07-30 deletion stands.

**(3) The four stale state entries were pruned: `state list` 55 -> 51**, with **0** `market_data_v2`
addresses remaining. This is the half of the act that only the untargeted apply could do, which is why
the signed shape was untargeted rather than `-target`.

**(4) The post-apply plan is clean**, and `resource_drift` fell from **5 entries to 1** -- the four
`market_data_v2` drifts are gone because the state rows they described are gone. The surviving drift
entry is `aws_iam_role.market_update_lambda_role`, whose `resource_change` is no-op; see section 4 of
the survey, and the note below.

## What the apply did NOT do

No create of any kind; no destroy; no API call about the four removed resources -- their removal was a
**state prune**, because the refresh had already found them absent and the configuration no longer
declared them. `aws_iam_role.market_data_generator` itself is untouched (its orphan status is row
Z-S43's, not this act's), and `market_update_lambda_role` was reconciled in **state only**: its
`resource_change` read no-op throughout, so the live role was never modified.

> **The near-miss recorded in the survey held.** `market_update_lambda_role` has lost
> `AmazonS3FullAccess` and `AmazonDynamoDBFullAccess` in the world while Terraform state still listed
> them. Because its declaration **omits** `inline_policy` and `managed_policy_arns` (THE OMISSION RULE),
> this untargeted apply reconciled the stored values to the live ones and did **not** re-attach the two
> full-access policies. Had the declaration named `managed_policy_arns`, an apply whose stated purpose
> is to remove a permission would silently have re-widened a production role, behind a summary line
> reading `0 to add, 1 to change, 0 to destroy`.

## The record

| | |
|---|---|
| code | `96c735a39c` (the two removals) |
| tombstone | `64fc0b7370` -- `declaration_removed` now cites `@96c735a39c`; **TF-debt A7 CLOSED** after being disowned by this seat in July as not-authorized, now authorised by the CTO's E3 ruling |
| drained | `2df4bd537b` (3 files; safe-merge rc=0, tree check 3 needed / 0 dropped / 0 foreign) |

**Two sparse-worktree gates fired first**, both instrument failures and both fail-closed, the same pair
as ACT 1 of z-1: `safe-apply`'s HALT-gate (`SERIAL RESOLVES TO NO KNOWN AGENT`, because the cone held no
agent home folder) and `crossbox-deploy-check` (absent `lib/devices.py`). Fixed by adding `lib` and
`org/tier2_senior/0.7.0_AE_CloudOps` to the cone. **A sparse worktree that will run an apply needs
`lib` and its own agent home folder in the cone** -- I hit this twice tonight and the second time was
avoidable.

**No consumer run exists to read.** `market-data-generator-lambda-role` has `RoleLastUsed` null and no
Lambda node in the served graph, so the cell's post-change run has no referent. The evidence is the
document compare, the bucket's continued absence, the state count and the clean plan.
