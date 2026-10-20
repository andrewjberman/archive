# NFRA_SCHWABBF -- Alongside box state-tier fence row and role re-point: never-widen pair, COO half

**Issuer:** `2.0.0_SA_COO~SA` (laptop), 2026-10-20 ~20:3xZ. **Halves:** COO = this file (SIGNED below); CTO = `org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_ALONGSIDE_STATE_FENCE_CTO_HALF.md` (OWED).
**Cell:** `AL-i-2` (order `task-orders/NFRA_SCHWABBF.TO-AL-i2.alongside-state-tier-iam-and-fence-row.md`). The pin is the merge of `AL-i-2` on `box/laptop`; this half is re-read at that pin before the apply, and the apply is a later CloudOps order (`TO-AL-r3`), not this file.
**Andrew-direct:** ~17:0xZ 2026-10-20, "a, yes. this needs to go through the same full bronze/silver process that the other masters go through" (PRD v1.0 C-TIERS); ~13:5xZ, "exact same setup and logic as already exists with the 49 schwab box".
**Precedent:** `~SB`'s `BF-h-5` (three scoped rows) and its pair `org/missions/D8/NFRA/NFRA_SCHWABBF/ledger/NEVER_WIDEN_BF5_STATE_FENCE_COO_HALF.md` + CTO half @4b0036c6cb.

## 1. The act and what it touches

Two changes, applied together by the NFRA CloudOps lane after the cell merges:
1. **Alongside root, update in place** (one `aws_iam_role_policy`): remove the two master-scope statements (`_ops`, `meta/pulls`) that no firm-form master uses any more; add `s3:PutObject` on `arn:aws:s3:::opal-data-cottonwood/schwab/cottonwood/state/{pulls,daily_pull}/date=*/<master>.*` for the four Cottonwood masters (8 resources). Net: the role loses two grants and gains one narrower one.
2. **The Cottonwood firm bucket's fence (shared-infra, `s3-lgic-firm-buckets.tf`, rendered from `infra/logic/registry/exemptions.json` by `modules/opal_name`):** ONE new scoped exemption row for the principal `arn:aws:iam::313476888478:role/schwab-alongside-si2-box-role`: `s3:PutObject` on the prefixes `schwab/cottonwood/state/pulls/` and `schwab/cottonwood/state/daily_pull/` only. The module renders a scoped row as three extra Denies (any other action, objects outside the prefixes, listings outside them), so the role is admitted for those two prefixes and nothing else in the bucket.

| what | widens? |
|---|---|
| the role's identity policy | narrows overall (two broader-scope statements out, one narrower in) |
| the bucket fence | widens by one principal, one action, two prefixes, for the one role whose job is writing these records; everything else in the bucket (the restricted CRM prefix and all other prefixes) keeps every existing Deny |
| anything else | no |

**Does not touch:** the 49F box and its role, the converter roles (`BF-h-5` covers them), the restricted `commonwealth/cottonwood/bronze/crm/` prefix and its breakglass Denies, any other bucket.

## 2. Writers of the property (counted at signing; N printed)

- Principals the Cottonwood bucket fence admits by exemption row today: read the file at the pin and print N (the issuer prints it in the CTO ask; at the cut the file carries the precedent rows, `opal-clientops-ews-role`-class rows for `opal-data-49financial`, and `BF-h-5`'s converter row for this bucket). This act adds 1.
- Writers of `schwab/cottonwood/state/{pulls,daily_pull}/` after the act: 1 (this role, per master by file name).
- Writers of the fence registry file `infra/logic/registry/exemptions.json`: the CRO's registry and cell orders by path; this act is one appended row by a worker under `AL-i-2`'s `<paths>`.

## 3. Expected outcome, read from the module's own rule (both branches)

The module (`infra/aws/terraform/modules/opal_name/main.tf`, ~140-300) keeps a scoped row inside `fence_exemption_arns` (so the base `DenyForeignFirmPrincipals` lets the role through) and renders three extra Denies on the role. Read at signing; the CloudOps plan re-confirms.
- **Branch A:** the shared-infra plan for the Cottonwood bucket policy shows ONLY the policy document changing (an in-place update of `aws_s3_bucket_policy` for `opal-data-cottonwood`), and the diff in the rendered JSON is exactly the added principal in the exemption list plus three extra Deny statements for that principal; no other bucket, no other principal. The Alongside root plan shows ONE in-place update of the inline role policy and nothing else. Proceed.
- **Branch B:** any other resource in either plan, any other bucket's policy, any change to an existing principal's statements, or a plan that deletes a statement. Do not apply; report to the COO.

## 4. Blast radius and rollback

- Blast radius: one bucket policy document (in place) and one inline role policy (in place). A mistake would at worst let the Alongside role write two run-record prefixes it should not, or refuse its own run-record writes (a WARN in the puller, not a data loss).
- **Rollback:** bucket policy: re-apply the previous policy document (the prior plan's "before" is saved by the CloudOps lane; the change is one principal and three Denies out). Role policy: re-apply the previous inline policy (the cell's previous commit). Both are in-place reversions; no data is touched. Versioning on the data keys is unaffected.

## 5. Conditions of this half

1. Apply only from the pinned worktree at the merge of `AL-i-2`, saved plans, `safe-apply`, no `-target` beyond the two roots named, no `-var`.
2. The shared-infra apply is coordinated with `2.0.0_SA_COO~SB`'s fence apply (`BF-h-5`, release R3a) so the two registry changes ride ONE plan if both are merged by then; if `~SB`'s apply has already run, this row is a second small apply and the plan must still read Branch A.
3. No rule is enabled and no pull runs beyond the first-day trace until this act is applied AND the Alongside role's puller upload (`AL-p-2`) is done (CTO condition 6).

## COO half -- SIGNED

`2.0.0_SA_COO~SA`, 2026-10-20, for the blast radius in section 1, both branches in section 3, the rollback in section 4 and conditions 1-3, on the merge of `AL-i-2` (the pin is named in `TO-AL-r3` when it is cut).

## CTO half -- OWED (`1.0.0_SA_CTO`)
