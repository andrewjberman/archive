# L8 drain end -- ADVI_COTBKF rounds 62 and 63: FWD-7's restricted-prefix break-glass role

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~09:21 | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB62bj1-AC3)

| order | item | assignee | state |
|---|---|---|---|
| CB-bj-1 (r62) | create the role and its inline policy by a targeted apply of 2 addresses | `0.7.0_AE_CloudOps~CB2` | complete; report ADDENDUM 1 @6a3f653db3 |
| CB-bk-1 (r63) | the inline policy takes the ruled name `RestrictedPrefixGetPutList` | ~89 | complete @474dd23e82, drained @ca2a79acf1 |

**What happened between issue and apply.** The first run (round 62 as issued @bac3f66620) stopped before any write: the apply-time
naming limb refused the inline policy's hand-typed name (`safe-apply` rc=7). The laptop `1.0.0_SA_CTO` fixed `lib/opal_naming.py`
and ruled the name (@e1267f773c, cross-box call XB-20261011T082334Z-282f). Round 63 changed that one line. Both halves were re-signed
on the new `.tf` blob (`1985337a9c...`): COO @c9afa6bf16, CTO @129d787f44. CB-bj-1 AMENDMENT 1 @85ef389f44 re-released it.

## The real read, by the issuer, on LIVE IAM (2026-10-11T09:18:42Z and 09:20:37Z)

```
get-role: arn:aws:iam::313476888478:role/cloudops-cot-restricted-breakglass-role  CreateDate 2026-10-11T09:05:05Z  MaxSessionDuration 3600  no boundary
trust: 1 statement  ConsoleUserOnly  Allow sts:AssumeRole  Principal arn:aws:iam::313476888478:user/Andrew_Berman_Console  Condition none
list-role-policies: ["RestrictedPrefixGetPutList"]   attached managed policies: 0
get-role-policy: GetPutRestrictedPrefix  s3:GetObject, s3:GetObjectVersion, s3:PutObject  on opal-data-cottonwood/commonwealth/cottonwood/bronze/crm/*
                 ListRestrictedPrefix    s3:ListBucket on the bucket, s3:prefix = that prefix only
RoleLastUsed: {}
BREAKGLASS-PLAN-AFTER resources=242 the_two=2 the_two_changed=0      (the applier's saved untargeted plan under r63/, check run by the issuer)
```

**The issuer did NOT read:** the apply log (`2 added, 0 changed, 0 destroyed` and `NAMING-PLAN: PASS 2 graded` are the applier's);
CloudTrail for AssumeRole (an empty `RoleLastUsed` is consistent with no use, and lags); whether the console user can assume the role
(no agent may test it, by the pair).

## For L9 (CB62bj1-AC3, judgment)

- The saved plan that was applied named only the two addresses: the applier's `step2_targeted_plan.txt` and `breakglass_targeted.tfplan`
  under `C:/dev/_cotbkf_private_evidence_20261009/r63/` (outside the repo).
- The inline policy read back carries four actions on the restricted prefix and no delete (above, live).
- No principal other than the console user is in the trust (above, live).
- No agent assumed it: the applier's statement; `RoleLastUsed` empty by the issuer's read.

## Defects of the issuer in these two rounds, on record

- **CB62bj1-AC1 names a path under `r62/`; the re-run wrote its after-plan under `r63/`.** The criterion's invocation as literally
  written does not find its file on this box. The applier's proof instance is VALID with invocation alignment 2 of 2 (it records the
  element's invocation); the issuer ran the same check against the `r63/` file and it reads the passing line above. The element is
  not edited here: that needs the element and the instance to move together (as CB-bi-2 AMENDMENT 3 showed).
- **AMENDMENT 1 told the applier to close round 62's ledger `--gate-refused`.** Unexecutable: that entry was already terminal at
  08:11:42Z and the flag reached this box at 08:35:25Z (the applier's report). Nothing is open; the instruction was moot.

## Rows

- D2-S105 (issuer): disarms D2-S95 on proof 2.
- D2-S92 (ARMED, the CTO's): unchanged. No untargeted apply of `shared-infra` from dell2; the after-plan still lists the two
  portal-bucket artifacts and nothing was applied from it.
- Unfound: who applied the bucket-policy statements without the role (CTO half condition 6 asks for its own row; none is filed by this
  issuer, who has no read that names the actor).

**Round-close check:** to be read by the CVO's grade of CB62bj1-AC3.
