# POST_APPLY -- Family A (rows 1 and 2, Black Diamond), NFRA_IAMROLES202609.TO-IAM-w-2 PHASE B

**Cell:** IAM-w-2 (round 6, outcome FWD-4; round-5 analysis item E2)
**Executed by:** `0.7.0_AE_CloudOps~IR` -- **owner of record:** `0.7.0_AE_CloudOps~Z` (ruling @fa8ec0e726)
**Authority:** GO `2.0.0_SA_COO~ZI` msg 33097, RESUME msg 33162. Both never-widen halves SIGNED as files:
COO @`1ad6f36ca2`, CTO @`dadc1ec69a`. Order of acts per A4-r6 @`7af7a24e9f` / A5-r6 @`f37fb5892d`;
`-target` scope per A2-r6.
**The gate that held this cell, and what cleared it:** row `Z-S34`. Andrew answered item 4 of
@`5e10dd2dc5` verbatim **`YES, the exception, "for now".`** `1.0.0_SA_CTO~Z` landed R20 entries
**NFRA-IAMROLES-R20-01/02** in `org/standards/NAMING_LEGACY_READS.json` @`bd2cacee69`, authority
@`727ce5eefa` register **X17**, **cutoff 2026-12-31** -- the cutoff carrying his qualifier.
**Measured:** 2026-10-11, worktree `C:/tmp/iam-w1b`, branch `wk-iamroles-r6-w2-b2` @`869c01686c`,
Terraform v1.15.8, provider `hashicorp/aws v5.100.0`.

---

## 1. THE REQUIRED LINE

```
POST-APPLY-PLAN: infra/aws/terraform/bd-pipeline: 0 to add, 0 to change, 0 to destroy
```

That is the TARGETED re-plan, which is what AC2 asks for. Terraform renders a clean plan as a sentence
rather than a count, so its verbatim output is quoted here beside the canonical line:

```
$ terraform -chdir=infra/aws/terraform/bd-pipeline plan ... \
    -target=aws_iam_role.bd_merge_daily_lambda_role -target=aws_iam_role.bd_pipeline_task_role
No changes. Your infrastructure matches the configuration.
```

## 2. THE UNTARGETED MODULE PLAN, RECORDED BESIDE IT

```
UNTARGETED-MODULE-PLAN: infra/aws/terraform/bd-pipeline: No changes. Your infrastructure matches the configuration.
```

Fully absorbed, no residue. PHASE A's negative control read "No changes" **before** the act (once step
1a's `can()` guard made the module plannable at all), and the untargeted plan reads "No changes" after
it, so the whole delta -- 2 imports plus 2 `tags_all` changes -- is accounted for.

## 3. THE PLAN THAT WAS APPLIED, GRADED BEFORE THE APPLY

Saved with `-out`; the apply ran that file, so the applied plan IS the graded plan. Graded from
`terraform show -json` per `resource_change`, because the summary `2 to import, 0 to add, 2 to change,
0 to destroy` is **exactly what a trust-policy rewrite would also print** -- which is this cell's named
stop condition for row 2.

| graded property | measured |
|---|---|
| `resource_changes` total | 2 |
| non-no-op | 2 |
| the addresses | `aws_iam_role.bd_merge_daily_lambda_role`, `aws_iam_role.bd_pipeline_task_role` |
| actions / import ids | both `['update']`, importing `bd-merge-daily-lambda-role` / `bd-pipeline-task-role` |
| attributes that differ, per role | **1 each** (`tags_all`) |
| `tags_all`, per role | `{}` -> `Environment=Production, ManagedBy=Terraform, Project=OpalPortal, System=BDPipeline` |
| exact match to the 4 keys the pair signs | **True** for both, key count 4 |
| `assume_role_policy` / `inline_policy` / `managed_policy_arns` / `description` | unchanged on both |
| destroys | 0 |
| non-no-op addresses that are NOT one of the two adopted roles | **`[]`** |

**STOP CONDITION, PRINTED RATHER THAN SUMMARISED.** Row 2's trust in the plan, `before == after`:

```
"{\"Statement\":[{\"Action\":\"sts:AssumeRole\",\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"ecs-tasks.amazonaws.com\"}}],\"Version\":\"2012-10-17\"}"
```

Summary verbatim: `Plan: 2 to import, 0 to add, 2 to change, 0 to destroy.`

`safe-apply`'s gates: `comp-tagauthz` PASSED (over **0 candidate resources** -- an empty denominator,
recorded with it, and not what answers the KEY COLLISION; both halves say so); `tombstone-gate` CLEAN.
The `naming-apply-gate` emitted **WARNs on names in OTHER files** (`alarms.tf`,
`bd-49f-etf-ownership-daily.tf`) -- all pre-existing, none this cell's, none a REFUSE, and none touched.

> **The apply's own completion line was NOT read, and that is recorded rather than glossed.** My
> output filter was written for the previous cells and the `naming-apply-gate` WARNs above pushed
> `Apply complete!` out of the captured window, so I had `rc=0` and nothing else. **An rc is not an
> oracle** -- so the apply was confirmed from the world instead: section 4's live reads plus
> `terraform state list`, which now holds both addresses. That is a stronger confirmation than the line
> I missed, but the sequence is worth stating: I did not see the producer's own success line and did not
> treat its absence as either success or failure.

## 4. BRANCH A, READ FROM THE WORLD

Every value below is a live AWS read taken after the apply, not the apply's self-report.

| read | `bd-merge-daily-lambda-role` | `bd-pipeline-task-role` |
|---|---|---|
| `list-role-tags` | **exactly 4**: `Environment=Production`, `ManagedBy=Terraform`, `Project=OpalPortal`, `System=BDPipeline` | **the same 4** |
| `list-role-policies` | `['bd-merge-daily-policy']` -- unchanged | `['BDPipelineTaskPolicy']` -- unchanged |
| `list-attached-role-policies` | 0 -- unchanged | 0 -- unchanged |
| **STOP CONDITION -- trust principal** | `lambda.amazonaws.com` -- unchanged | **`ecs-tasks.amazonaws.com` -- unchanged** |
| `description` | `Role for BD Merge Daily Lambda` -- unchanged | **`None` -- still absent**, as the declaration intends |
| `terraform state list` | `aws_iam_role.bd_merge_daily_lambda_role` present | `aws_iam_role.bd_pipeline_task_role` present |

**THE OMISSION RULE HELD IN THE WORLD on both roles:** each still carries its one inline policy and zero
attached managed policies. **No permission moved.** Four tags were added to each role where both carried
none, and PHASE A's survey named all four before either half was signed.

## 5. ROLLBACK, AVAILABLE AND UNUSED

Per the COO half: `terraform state rm` of each address (state only, no AWS change), plus
`aws iam untag-role --tag-keys Environment ManagedBy Project System` on each, plus reverting the rename.
Not needed, not run. Nothing is stranded.

## 6. THE LEDGER, AND THE HOLD IT CAME BACK FROM

`iamroles-r6-family-a` opened BEFORE the apply @`ae27a5f5f8` (3 legs), **HELD-PRE-APPLY** @`47955fd728`
when the naming gate refused the step-5 commit, **RELEASED** @`b0fdae1419` once the R20 entries were at
HEAD, and closed after this record. One module, one entry.

> **Why the hold was released rather than closed NOT-APPLIED and re-opened:** the entry was opened before
> the act exactly as NEVER-2 requires, and nothing was ever applied under it. Closing it and minting a
> fresh one would have erased the fact that the act was authorised, prepared, and stopped at a named
> gate. The issuer's instruction allowed either, conditioned on the ~06:03Z window; the window had not
> lapsed, so the release is the faithful path.
>
> **And one thing recorded against myself:** the FIRST hold on this entry did not persist. I ran it in a
> worktree and my own `git checkout --` during an unrelated revert discarded the uncommitted write, so
> the drained record still read `OPEN`. That is the same trap I banked in September about
> `deploy_ledger.py` in a linked worktree -- hit a second time, in the same session, by a different
> discard path. The release above was committed in the same step as the mutation.

**PHASE B ends here, per the order's step 6.**
