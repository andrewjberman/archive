# ADVI_COTBKF CB-bj-1 -- the break-glass role was NOT created: the apply was refused at the naming gate

**Seat:** `0.7.0_AE_CloudOps~CB2` | **Order:** `ADVI_COTBKF.TO-CB-bj-1` (issued @`bac3f66620`) | **Round:** 62,
cell `CB-bj-1`, **outcome_ref** FWD-7 | **Risk:** WORLD | **Date:** 2026-10-11, 07:58Z-08:12Z | **Box:** dell2

## VERDICT: STOPPED between Branch A and step 3. Nothing was created. Nothing is stranded.

The targeted plan was **Branch A and correct**. `safe-apply.sh` then exited 7 and **terraform was never invoked**,
because the naming plan limb refused the inline policy's name. `CB62bj1-AC1` and `CB62bj1-AC2` cannot be met as
written; `CB62bj1-AC3` stays PENDING-ADJUDICATION. Rows `ADVI_COTBKF-D2-S98` and `-D2-S99`.

## 1. The three hashes of step 0 -- all equal

| file | measured | pin |
|---|---|---|
| COO half `.../2.0.0_SA_COO~C2/NEVER_WIDEN_FWD7_..._COO_HALF.md` | `31df136096ccbbaadf000931bfe8974368b3aa3842d77566ceaf79a7e3cde3f2` | **equal** |
| CTO half `.../1.0.0_SA_CTO~DELL2/NEVER_WIDEN_FWD7_..._CTO_HALF.md` | `de8c29b8febda2252a49af5111044edf5aa09439176f8926e5a21aa9c27e4cb9` | **equal** |
| `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf` | blob `26aa1a2633a36213300708cbfa0f3ea8fae524e8` | **identical** at `8c6fc7652a` and at `HEAD` |

`HEAD` contains `9b8eb8c244`. The `.tf` is clean in the worktree. Both halves read in full before the act, and
`/cloud-ops` was loaded this session.

## 2. The targeted plan -- Branch A, exactly

```
Plan: 2 to add, 0 to change, 0 to destroy.
  # aws_iam_role.restricted_breakglass will be created
  # aws_iam_role_policy.restricted_breakglass will be created
```

rc=0, **0 `Error` blocks**, saved outside the repo at
`C:/dev/_cotbkf_private_evidence_20261009/r62/breakglass_targeted.tfplan`. No third address, no change, no destroy.

The plan body was read against both halves and matches: role `cloudops-cot-restricted-breakglass-role`, path `/`,
`max_session_duration` 3600; trust is **one** statement, Sid `ConsoleUserOnly`, `sts:AssumeRole`, Principal
`arn:aws:iam::313476888478:user/Andrew_Berman_Console`, no condition, no service, no wildcard; inline policy
`restricted-prefix-get-put-list` = `s3:GetObject` + `s3:GetObjectVersion` + `s3:PutObject` on
`arn:aws:s3:::opal-data-cottonwood/commonwealth/cottonwood/bronze/crm/*`, plus `s3:ListBucket` on the bucket under
a `StringLike` `s3:prefix` condition scoped to that prefix. **Four actions, no delete.**

**One discrepancy, recorded and not a Branch B.** The COO half's section 1 says the role has "no tags"; the plan
shows `tags_all` with four provider `default_tags` (`Environment=Production`, `ManagedBy=Terraform`,
`Project=OpalPortal`, `System=SharedInfra`). Tags are metadata, grant nothing, and are not a third address, a
change or a destroy — so Branch A stands. The half's blast-radius sentence is inexact on that one point.

**A side finding on row `D2-S92`:** this targeted plan returned rc=0 with **zero** AccessDenied errors, where
round 61's untargeted plan of the same root returned rc=1 with two. That is empirical confirmation of the CTO
half's narrowing — targeting excluded the portal bucket from the refresh.

## 3. Which branch ran: none of the three. The apply was refused by a gate.

```
safe-apply: BLOCKED by the naming plan limb (LGIC_ENFORCE DEC-6, ENFORCE mode, rc=1). Nothing was planned
further or applied.
```

`safe-apply.sh` rc=**7**. The gate refusals, verbatim, as the REPORT clause requires:

```
[naming-plan-gate] NAMING CONFORMANT aws_iam_role.restricted_breakglass
    cloudops-cot-restricted-breakglass-role -> cloudops-cot-restricted-breakglass-role
  why: aws_iam_role.restricted_breakglass (ADDITION): CONFORMANT as IAM_ROLE

[naming-plan-gate] NAMING REFUSE aws_iam_role_policy.restricted_breakglass
    restricted-prefix-get-put-list -> cloudops-49f-restricted-breakglass-policy
  why: NEW name the canon places as FIX. Owed: use cloudops-49f-restricted-breakglass-policy. Build it with
  name() or edit the literal; nothing else is owed. [grade() said: aws_iam_role_policy.restricted_breakglass
  (ADDITION): RAISE as IAM_POLICY: a rule or registry defect, not a naming verdict: R1.f: 'restricted' is in
  no vocabulary; no registry row resolves it. DEC-6: refused like any refusal once enforcing]

[naming-plan-gate] NAMING-PLACE: REFUSE 1
[naming-plan-gate] NAMING-PLAN: REFUSE 2 graded
```

**Both seat gates passed**, so the naming limb is the sole stop:

```
safe-apply: [seat-gates] APPLY-WHO serial=0.7.0_AE_CloudOps~CB2 kind=CLOUDOPS root=shared-infra
            verdict=ADMITTED reason=a CLOUDOPS seat applies
safe-apply: [seat-gates] CROSSBOX-DEPLOY device=dell2 root=shared-infra open_call=clear overlap=clear
            upset=clear open_deploy=clear verdict=CLEAR
```

The `naming-apply-gate` stage before it emitted only WARNs (116 graded, 10 expressions deferred to plan) and by
its own text "never refuses". The refusal is the **plan-time** limb.

**Measured at the source, not inferred from the gate's message:**

| call | result |
|---|---|
| `opal_naming.grade('cloudops-cot-restricted-breakglass-role','IAM_ROLE')` | `('CONFORMANT', 'cloudops-cot-restricted-breakglass-role')` |
| `opal_naming.grade('restricted-prefix-get-put-list','IAM_POLICY')` | **raises** `RaiseDefect: R1.f: 'restricted' is in no vocabulary; no registry row resolves it` |

So `grade()` reaches **no verdict at all** for the policy. The gate's own text classes it "a rule or registry
defect, not a naming verdict", and DEC-6 converts that RAISE into a refusal while enforcing.

### This is a fourth state the face does not enumerate

Branch A said "-> step 3"; step 3 was attempted and a mechanical gate refused it. It is **not Branch B** (the plan
was correct) and **not Branch C** (Branch C presupposes the role *created* and the policy refused by the
**applier's credentials**; here neither exists and the refuser is an apply-time gate). **Branch C's pre-authorised
targeted destroy was therefore NOT invoked — it has no subject.**

## 4. Nothing was created -- verified, not assumed

| read | result |
|---|---|
| `get-role cloudops-cot-restricted-breakglass-role` | `NoSuchEntity` |
| isolated positive control, same credentials | `arn:aws:iam::313476888478:role/demo-transform-runner-ec2-role` |
| `terraform state list` | **253** rows, **0** matching `breakglass` |
| positive control on the same state | **10** rows matching `lgic_firm` |

No rollback was needed or performed. The world is exactly as it was before the act.

## 5. Why the owed name must NOT simply be typed in

The gate says: *Owed: use `cloudops-49f-restricted-breakglass-policy`.* That name carries the **`49f`** firm token
on a policy whose only grants are on `opal-data-cottonwood`'s `commonwealth/cottonwood/bronze/crm/` prefix — while
the same gate graded the sibling **role** CONFORMANT as `cloudops-`**`cot`**`-`. Adopting it as printed would label
a Cottonwood-only break-glass grant after 49 Financial: a cross-firm mislabel on an IAM object.

Two further reasons not to hand-type a fix:

- **CLAUDE.md rule 30** makes a builder refusal *"a missing registry row to add (`infra/logic/registry/`), never a
  hand-typed workaround"*. That registry is not in this order's `<paths>` grant, and it is the LGIC canon's, whose
  owner is the laptop `1.0.0_SA_CTO` (CTO ruling @`27ba4d3769` item 4).
- Editing the `.tf` literal would change **the very blob both halves pinned** at `8c6fc7652a`, voiding the pair.

**Not established by this seat:** why the suggestion resolves to `49f` (`grade()` raises before returning, so the
suggestion is built on a path I did not trace), and whether the remedy is a vocabulary entry for `restricted`, a
registry row, or a different policy name built by `name()`. That is the canon owner's call, not mine.

## 6. The ledger entry

`org/critical_paths/change_management/20261011T0758Z_advi-cotbkf-r62-bj1-breakglass-role-targeted-apply-20261011_deploy_completion.md`

Opened **before the plan** (condition 1) after a `.open_deploys/` union across **43 of 43** live worktrees —
per-tree counts 17 to 29, 873 row-reads summed, **101 distinct** paths, **0** naming this act. **Closed
20261011T081xZ**, every leg dispositioned:

| leg | disposition |
|---|---|
| L1 | targeted plan — Branch A, proven |
| L2 | **NOT APPLIED / REFUSED-BEFORE-APPLY** — closed as refused, not as done |
| L3 | proof 1 — **UNREACHABLE BY CONSTRUCTION** (reads objects that were never created) |
| L4 | proof 2 — **UNREACHABLE BY CONSTRUCTION** (`shared_infra_plan_after.json` does not exist) |

`check --red` no longer lists it. **The entry's CLOSED status means every leg is dispositioned and nothing is
stranded — it does not mean the deploy happened.** A CLOSE DISPOSITION section at the foot of the entry says so in
those words, and carries the hold.

### The hold lives in the entry's text because the tool would not carry it

`deploy_ledger.py hold` refused both forms: `--pre-apply` because the plan leg already carries proof ("the act has
started"), and a normal `hold` because an open apply leg reads to it as *"a half-landed deploy ... stays RED"*.
Neither describes an act that planned, was refused at the gate, and created nothing — and "half-landed" is the
costly misreading, because it points at stranded infrastructure that does not exist. Filed as row
`ADVI_COTBKF-D2-S99`, with a suggested `REFUSED-BEFORE-APPLY` disposition offered as a shape, not a decision.

- **Named dependency:** an LGIC naming-canon resolution for `restricted`, so `grade()` returns a verdict instead of
  raising `R1.f`. Owner: laptop `1.0.0_SA_CTO`; routed via `2.0.0_SA_COO~C2`. Row `D2-S98`.
- **Re-read event:** an amendment to `TO-CB-bj-1` naming the resolved policy name and its commit. Re-read by
  re-running the targeted plan and confirming it is still Branch A **before** any apply.
- **A re-run is a NEW ledger entry.** This one is terminal.

## 7. Bounds honoured

No untargeted apply. No other address applied. No state verb. **The role was never assumed** (condition 5) — and
could not be, since it does not exist. The restricted prefix was neither read nor listed. No push. Plans and their
JSON live outside the repo. `<status>` was **not** flipped: the acceptance was not met.

## Evidence files (outside the repo)

`C:/dev/_cotbkf_private_evidence_20261009/r62/`

| file | what it is |
|---|---|
| `step2_targeted_plan.txt` | the Branch A plan, addresses and count line |
| `breakglass_targeted.tfplan` | the saved plan that was never applied |
| `step3_apply.txt` | 255 lines — the full gate output and the verbatim refusal |
| `base_init.txt` | `init` in the base checkout (aws v5.100.0) |
| `state_after_refusal.txt` | 253 state rows, the breakglass/lgic_firm denominators |
| `open_deploys_union_sorted.txt` | the 101-entry union across 43 worktrees |
