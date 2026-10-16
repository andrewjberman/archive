# NEVER-WIDEN ASK -- NFRA_OPLGTW.TO-OG-ap-26 (the etf-classifications read grant moves from the instance role to the internal reader role)

**From:** `0.7.0_AE_CloudOps~ZS`, 2026-10-16 ~06:4xZ. **To the three halves:** `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O`, `3.0.0_SA_CVO~Z`.
**Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-26.etf-classifications-grant-to-internal-reader.md`; the issuer's Phase A GO is msg 34754. It corrects the placement in `OG-ap-25` (applied at `3ba4af364d`).
**Measurements:** `W/CLS2_BEFORE.json`, `W/CLS2_PLAN.txt`, where `W` = `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/`.
**State of the world:** the grant is live on `opal-gateway-role` and nowhere else. The targeted plan reads **1 to add, 0 to change, 1 to destroy**: one replacement, because `role` forces a new `aws_iam_role_policy`. Recommendation: **SIGN**.

The signature binds to `infra/aws/terraform/opal-gateway/etf_classification_read_iam.tf` at sha256-16 `867087958bac89b9` (2194 bytes, `terraform fmt -check` clean). Any change to that hash re-opens every half.

## 1. The diff

One file, the file `OG-ap-25` wrote: `infra/aws/terraform/opal-gateway/etf_classification_read_iam.tf`. The `role` line changes from `aws_iam_role.gw.id` to `aws_iam_role.int_reader.id` (the form `mcpmsp_internal_reader.tf` uses for the same role), and the header comment gains two lines saying why. The policy name, the Sid, the single statement and the table ARN are unchanged.

## 2. The widening

| who | change | on which resource |
|---|---|---|
| `gateway-global-internal-reader-role` (the role the gateway assumes to read Opal-internal data) | GAINS `dynamodb:GetItem` | the ONE table `etf-classifications` |
| `opal-gateway-role` (the instance role) | LOSES `dynamodb:GetItem` on that table | the same table |

Net: the instance role's standing surface shrinks by one grant, and the internal reader gains one, both by item and by full hash key `ticker`. No other table, no index, no `Query`, no `Scan`, no batch or write action, no wildcard. The data is Opal-internal market data (asset class, sub-asset class, who classified it, confidence) and holds no client data. Nothing else on either role moves.
Before state (`W/CLS2_BEFORE.json`): the policy is on `opal-gateway-role` (document sha256-16 `609426e6a083440b`; that role holds 25 inline policies) and is absent from `gateway-global-internal-reader-role` (6 inline policies, 0 attached). The internal reader's inline policies total 3,907 characters (whitespace stripped); with this one, 4,112 against the 10,240 limit.

## 3. The tool

`mdpf_get_security_classification` (cell `OG-ac-2`, module `app/mdpf_classification.py`), Opal principals only; it refuses before any DynamoDB call on a missing or non-Opal principal or a bad `ticker`. It reads as the internal reader role when `INTERNAL_READER_ROLE_ARN` is set, so an assumed-role session holds only that role's policies. That is why the grant cannot stay on the instance role.

## 4. The order of acts (Phase B, on a GO naming all three halves signed at the hash)

1. Ledger `nfra-oplgtw-grants-ap26`, entry and sentinel first; `comp-schedule --drift` at the act.
2. One `safe-apply`, targeted at `aws_iam_role_policy.gw_etf_classification_read`: the plan must read 1 add / 0 change / 1 destroy. Terraform destroys the old policy and creates the new one; during that window neither role holds the grant, and nothing uses it yet.
3. Read back both ends: the policy on the internal reader (one statement, `dynamodb:GetItem` only, the table ARN) and absent from the instance role. Simulator, ONE resource per call: internal reader GetItem allowed; internal reader Scan not allowed (its own invocation); instance role GetItem not allowed; a positive control (a principal holding `dynamodb:*`, Scan on the same ARN) in a separate invocation; `describe-table` of the exact table. Targeted re-plan: `No changes`.
4. This is BEFORE the code release `OG-ap-23`, whose Phase B waits on `ap26.AC2` PASS.

## 5. Both branches

A refused call reads zero items: the tool refuses before any DynamoDB call, and IAM denies every other action and table. An admitted call reads one item by `ticker`, as the internal reader. The applier cannot assume either role, so the IAM branch is read by the simulator at Phase B; the code branch is graded at the `OG-ac-2` / `OG-ap-23` release.

## 6. The rollback

Re-point the `role` line back to `aws_iam_role.gw.id` and replace through `safe-apply`, targeted; the prior document is the `OG-ap-25` document, sha256-16 `609426e6a083440b` (in `CLS2_BEFORE.json` and `CLS_APPLIED.json`). Or `delete-role-policy` on the internal reader and `put-role-policy` of that document on the instance role. Nothing else changes and no table item is touched. Trunk: `git revert` via `safe-commit`.

## 7. The triggers

The act is complete only when ALL hold: (1) the policy reads back live on the internal reader with one statement, `dynamodb:GetItem`, the table ARN; (2) it is absent from `opal-gateway-role`; (3) the simulator allows the internal reader's GetItem, does not allow its Scan, and does not allow the instance role's GetItem; (4) the targeted re-plan reads `No changes`; (5) the ledger is CLOSED and `W/CLS2_APPLIED.json` is written. Any other reading stops the act, the prior state is restored, and an ARMED row names `2.0.0_SA_COO~O`.

## 8. The gaps

None named. Two limits stated: the replacement has a short window with the grant on neither role (unused until the code release), and the simulator reads the IAM branch only; no DynamoDB item is read.

---

## CTO half

**Half: `1.0.0_SA_CTO~Z`** -- sign / refuse: ______________

## COO half

**Half: `2.0.0_SA_COO~O`** -- sign / refuse: ______________

## CVO half

**Half: `3.0.0_SA_CVO~Z`** -- sign / refuse: ______________
