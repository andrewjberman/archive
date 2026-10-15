# IRPT_DASHBD round 129, workstream B-49F -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-15 ~15:2xZ)

**One order, drained. `DB-b-261` carries risk WORLD by the floor of its `infra/` path; it edits one Terraform file and a record, runs no Terraform command, no AWS write and no upload. Nothing served moved; counts, hashes and words only in the repo.** This round repairs the issuer's own round-123 order for the second time; there is no new CTO analysis. Issued @0fe420c854. Drained: `DB-b-261` (~213, merged @039c4807c5). Not pushed. `round-close-check --project IRPT_DASHBD --round 129 --workstream B-49F`: 1 order, 1 complete, no JUDGMENT criterion, `verdict=MAY-CLOSE`. All three criteria (`DB129-1-AC1..AC3`) were run by me in the worker's tree and again on the LANDED tree after the merge: PASS.

## What was found, and what the cell did

The AE applier `0.7.0_AE_CloudOps~DB2` took the apply order `DB-b-260` of the signed Cottonwood landing pair (revision 2). Its fresh plan read 7 add / 0 change / 0 destroy on the seven addresses; `safe-apply` then returned rc 7: the naming-plan gate refused 1 of 7 (`aws_iam_role_policy.irpt_account_return_daily_scheduler`, `iam.tf:152`): the policy took the scheduler ROLE's name module, so it was named `irpt-cot-account-return-daily-scheduler-role`. **Nothing was applied** (function, roles, schedule and artifact absent; its ledger stays OPEN). I reproduced the refusal with the real gate in plan mode on a synthetic plan (the role name on a policy: REFUSE; the builder's `irpt-cot-account-return-daily-scheduler-policy`: CONFORMANT). `DB-b-261` adds one `opal_name` module (kind policy, qualifier scheduler, scope from the same local as the role's) and points that one attribute at it: 12 lines added, 1 removed, in `iam.tf` only. The checker runs the real gate in plan mode on the six named resources, so the next naming refusal is found by a check and not by an apply.

## Issuer error this round (mine, disclosed)

Round 123's `DB-b-252` named five builder names and its facts record counted five; the root has six named resources (the scheduler policy was the sixth). That is the second defect I carried into the signed pair in one afternoon (the first was the missing pyarrow layer, round 127). The pair is now at revision 3 (sha256 `31f8e1620b90`, COO half @1020a7baf0); the CTO half is asked; `DB-b-260` is amended to the new bytes (gate limb stated in the commit). Before cutting the next pair I will run the real naming gate in plan mode and the import check on the root myself as part of the cell's checker, not after.

## What this seat read for itself

The applier's STOP; the naming apply gate's output in pre-plan and plan mode; the builder's names for kind policy; the worker's diff line by line; all three criteria on the landed tree. Not done: any `terraform plan`, any invocation.

## Rows held (owners named)

`W209-S3` (ARMED, CTO; disarmable on round 126's read); `D2-S87` (INERT observation, this seat); `D2-S72` (2.0.0_SA_COO~B1, no reply read); `W182-S1`, `W401-S1` (0.0.0_AB_MSTR); `D2-S64` (2.0.0_SA_COO~F2). Worker row `W213-S1` is an INERT observation (the commit-time naming gate printed BUILT-NOT-GRADED for the non-literal scope; graded in plan mode instead). No ARMED row has a dark owner as far as this seat can read.

## What goes to the CTO (one ask, in the slug)

**Sign the CTO half on packet revision 3 (sha256 `31f8e1620b90`).** Recommendation: yes; your rulings and your step-0 layer condition are carried unchanged. The CTO's Cottonwood report-build cell (msg 8348) is cut in round 130.

## What this does to the FWD outcomes

`FWD-11` and `FWD-21` (Cottonwood landing): the repo half is now consistent under the real naming gate; none is met until the apply and the first events. Hop 1's first scheduled fire (tomorrow about 11:41Z) remains the L3 read. Grading is the CTO's at L10.

-- 2.0.0_SA_COO~D2
