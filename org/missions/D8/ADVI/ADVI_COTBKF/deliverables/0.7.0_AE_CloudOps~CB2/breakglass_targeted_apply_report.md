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

---

# ADDENDUM 1 (2026-10-11 09:01Z-09:08Z) -- RE-RUN UNDER AMENDMENT 1: APPLIED. Both IAM objects now exist.

**The verdict of the report above is superseded for the act, not for the record.** The stop it describes was
correct and is the reason this run exists: the canon's owner fixed `lib/opal_naming.py` and ruled the policy
name (laptop `1.0.0_SA_CTO` @`e1267f773c`), round 63 changed that one line to `RestrictedPrefixGetPutList`
(drained @`ca2a79acf1`), and the issuer re-released on both halves re-signed (AMENDMENT 1 @`85ef389f44`).

## VERDICT: Branch A, APPLIED. `Apply complete! Resources: 2 added, 0 changed, 0 destroyed.`

`CB62bj1-AC1` **PASS**, `CB62bj1-AC2` **PASS**, `CB62bj1-AC3` PENDING-ADJUDICATION.

## A1. The three NEW hashes of step 0 -- all equal

| file | measured | pin |
|---|---|---|
| COO half @`c9afa6bf16` | `ca572dd7e82971260d5af158d13232998038cf48be88a449b3ff323ecda7e8b7` | **equal** |
| CTO half @`129d787f44` (re-signed; first signature marked void in the file) | `f55925118eeed0a800a7fcdd456d5a6f96065a1d69f3e339c4fbfb7be029efdc` | **equal** |
| `s3-lgic-firm-buckets.tf` | blob `1985337a9cef839688fe054acc667ed4d4397dc7` | **equal on BOTH reads** |

The `.tf` was read both ways AMENDMENT 1 names -- `git hash-object` and `git rev-parse HEAD:<path>` -- and the
worktree is clean. HEAD contains `85ef389f44` and `e1267f773c`. The face's earlier "blob at `8c6fc7652a`" is
superseded by this value, as the amendment states.

## A2. The targeted plan, and the amendment's new STOP

```
Plan: 2 to add, 0 to change, 0 to destroy.
  # aws_iam_role.restricted_breakglass will be created
  # aws_iam_role_policy.restricted_breakglass will be created

planned ROLE name:   'cloudops-cot-restricted-breakglass-role'   <- MATCH, read from the plan JSON
planned POLICY name: 'RestrictedPrefixGetPutList'                <- the ruled name
```

rc=0, 0 `Error` blocks. The role name was read out of the plan's **after-values**, not from the `.tf` source and
not assumed from the module -- the amendment added this STOP because the generated naming carriers are stale at
HEAD (row `D2-S103`) and no dell2 seat runs `generate`. Had it printed anything else, Branch B.

The plan body was re-verified against both halves: trust = **one** statement, Sid `ConsoleUserOnly`, principal
`arn:aws:iam::313476888478:user/Andrew_Berman_Console`, **no Condition**, path `/`, max session 3600; policy =
exactly **four** actions, **zero** deletes, Cottonwood-only resources.

## A3. The naming limb PASSED where it refused

```
[naming-plan-gate] NAMING CONFORMANT aws_iam_role.restricted_breakglass
    cloudops-cot-restricted-breakglass-role -> cloudops-cot-restricted-breakglass-role
[naming-plan-gate] NAMING-PLAN: PASS 2 graded
```

Zero `NAMING REFUSE` lines, where the round-62 run printed `NAMING-PLACE: REFUSE 1 / NAMING-PLAN: REFUSE 2
graded` and `safe-apply` returned 7. **Nothing was overridden** to achieve this: no `HALT_OVERRIDE`, no
`pipeline-override`, no edited literal, and no name typed in from the gate's suggestion. The change came from
the canon owner's fix, which is what AMENDMENT 1 required.

Checked at the source before applying, so the PASS was understood rather than merely welcomed:
`grade('RestrictedPrefixGetPutList','IAM_POLICY')` returns `('NO-SYSTEM-ASKED', ...)` -- **the intended**
**verdict**, not a residual problem: commit `e1267f773c`'s own subject reads *"an inline PascalCase IAM policy
reaches NO-SYSTEM-ASKED before R1.f (D2-S98)"*. The old name still raises `R1.f`.

## A4. The apply

```
aws_iam_role.restricted_breakglass: Creation complete after 0s
    [id=cloudops-cot-restricted-breakglass-role]
aws_iam_role_policy.restricted_breakglass: Creation complete after 0s
    [id=cloudops-cot-restricted-breakglass-role:RestrictedPrefixGetPutList]
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

rc=0, 09:04:22Z-09:05:06Z. `safe-apply.sh` was handed **the saved plan file** from step 2, not a fresh plan.
**Branch C never arose** -- the policy did not fail -- so its pre-authorised destroy was neither needed nor used.

## A5. Proof 1, read from live IAM rather than the apply log

| read | result |
|---|---|
| `get-role` Arn | `arn:aws:iam::313476888478:role/cloudops-cot-restricted-breakglass-role` |
| `length(AssumeRolePolicyDocument.Statement)` | **1** |
| trust principals (AC2's exact invocation) | `arn:aws:iam::313476888478:user/Andrew_Berman_Console` -- that one ARN, nothing else |
| `get-role-policy --policy-name RestrictedPrefixGetPutList` | rc=0, served `PolicyName` = `RestrictedPrefixGetPutList` |
| actions | **4**: `s3:GetObject`, `s3:GetObjectVersion`, `s3:PutObject`, `s3:ListBucket` |
| delete actions | **0** |
| resources | Cottonwood only: the CRM prefix and the bucket, the latter under a `StringLike s3:prefix` condition |

The statement **count** was read separately, because a one-line principal output is exactly what would hide a
second statement. Before this act the same `get-role` returned `NoSuchEntity` beside an isolated positive
control that returned a real ARN -- so this instrument has a measured reading **both ways** on this exact name.

**Condition 5 honoured:** no `sts:AssumeRole` was called by this seat at any point, on either run. `get-role`
and `get-role-policy` read the role's metadata; they do not assume it.

## A6. Proof 2 -- a PLAN ONLY; nothing applied from it

```
BREAKGLASS-PLAN-AFTER resources=242 the_two=2 the_two_changed=0

  no-op  aws_iam_role.restricted_breakglass
  no-op  aws_iam_role_policy.restricted_breakglass
```

`the_two=2`, **not 0**, so this is not the failed read the criterion warns about. The untargeted plan itself is
rc=1 with exactly **2** `Error` blocks and `Plan: 2 to add, 0 to change, 1 to destroy`; its only non-no-op rows
besides the two are `aws_s3_bucket.opalinvest_portal` (create) and its SSE config (delete/create) -- **dell2's**
**known credential reading, row `D2-S92`**, the same portal-bucket false positive measured at round 61, which
condition 4 provides for and from which **nothing was applied**.

**Row `D2-S95`'s disarm is the issuer's on this proof** (condition 6), not this seat's. This line is its evidence.

## A7. The ledger, and one instruction that could not be executed

New entry `20261011T0901Z_advi-cotbkf-r63-bj1-...`, opened **before the plan** after a **46 of 46** worktree
`.open_deploys/` union (per-tree 17-29, 942 row-reads, **104 distinct** paths). All 4 legs closed with proof,
CLOSED.

The union surfaced **round 62's own entry**, which could have read as an open deploy needing action. Measured
instead of acted on, per NEVER-2: 5 of 46 trees carry a pre-close snapshot and 41 do not; the shared tree's HEAD
carries the open-deploy file **0** times, deleted at `bb3ab3a85a` (is-ancestor of HEAD, confirmed); the entry
reads `CLOSED ... 20261011T081142Z`. World-done -- not re-executed, not re-closed.

**AMENDMENT 1's instruction to close round 62 with `deploy_ledger close --gate-refused` is not executable, and
is reported rather than faked.** That entry was already terminal at **08:11:42Z**; `close` returns *"no open
deploy ledger for slug"*. The `--gate-refused` flag landed at **08:35:25Z** in commit `e1267f773c` -- 24 minutes
later, and added in response to this seat's row `D2-S99`. Its help text now asks for exactly what that row said
was missing: *"the gate's refusal line plus the nothing-created reads with a positive control"*. The substance
is already in round 62's entry: the refusal verbatim in L2's proof, the nothing-created reads with their
positive control, and a CLOSE DISPOSITION section. Only the verb could not be run.

## A8. Bounds honoured on this run

No untargeted apply. No other address applied. No state verb. The role was **never assumed**. The restricted
prefix was neither read nor listed. No push. Plans and their JSON outside the repo. `<status>` **flipped to
complete** -- the acceptance is met.

## A9. Evidence files for this run

`C:/dev/_cotbkf_private_evidence_20261009/r63/`

| file | what it is |
|---|---|
| `step2_targeted_plan.txt`, `step2_plan.json` | the Branch A plan and the printed role name |
| `breakglass_targeted.tfplan` | **the saved plan that was applied** |
| `step3_apply.txt` | the apply, naming PASS and the two creation lines |
| `proof1_policy.json` | `get-role-policy` on the served role |
| `step5_plan_after.txt`, `shared_infra_plan_after.json` | proof 2's untargeted plan |
| `open_deploys_union_sorted.txt` | the 104-entry union across 46 worktrees |
