# NEVER-WIDEN ASK -- NFRA_OPLGTW.TO-OG-ap-25 (the gateway role reads the etf-classifications table by key)

**From:** `0.7.0_AE_CloudOps~ZS`, 2026-10-16 ~05:0xZ. **To the three halves:** `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O`, `3.0.0_SA_CVO~Z`.
**Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-25.etf-classifications-read-grant.md`; the issuer's Phase A GO is msg 34735.
**Spec and census:** `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~113/ETF_CLASS_SPEC.md` section Grant, and `ETF_CLASS_CENSUS.json`.
**Measurements:** `W/CLS_BEFORE.json`, `W/CLS_PLAN.txt`, where `W` = `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/`.
**State of the world:** nothing is applied. The targeted plan reads **1 to add, 0 to change, 0 to destroy** (one inline policy on `opal-gateway-role`).
Recommendation: **SIGN**.

The signature binds to `infra/aws/terraform/opal-gateway/etf_classification_read_iam.tf` at sha256-16 `c51c268d41b63e8f` (1973 bytes, `terraform fmt -check` clean).
Any change to that hash re-opens every half; it is not applied on a stale hash.

## 1. The diff

One new file, no existing file changes: `infra/aws/terraform/opal-gateway/etf_classification_read_iam.tf`. It holds one `opal_name` module call (the policy name,
`lib/opal_naming.py name("gateway","global","etf-classification-read","policy")` = `gateway-global-etf-classification-read-policy`), two data sources for the region and the
account (the ARN is built from them, as the sibling files do), and ONE `aws_iam_role_policy` on `aws_iam_role.gw`. No registry row is needed (the policy names no S3 prefix). The
`.terraform.lock.hcl` is unchanged by `terraform init`.
Before state (`W/CLS_BEFORE.json`): the table `etf-classifications` is ACTIVE in us-east-1, hash key `ticker`, no range key, no index, 11,362 items by the census count;
`opal-gateway-role` holds 24 inline policies and 1 attached; **0 of 24** policy documents name `etf-classifications` (each fetched and searched), so the grant is not a duplicate.

## 2. The widening

| who gains what | on which resource | for which firm |
|---|---|---|
| the gateway instance role may call `dynamodb:GetItem` | the ONE table `arn:aws:dynamodb:us-east-1:<account>:table/etf-classifications` | none: the rows are Opal-internal market data and hold no client data |

The statement: Effect Allow, Action `["dynamodb:GetItem"]`, Resource the table ARN, Sid `ReadEtfClassificationsByTicker`. It lets the gateway read ONE item at a time, by the full hash key
`ticker`, and nothing else: no other table, no index, no `Query`, no `Scan`, no `BatchGetItem`, no write or delete, no wildcard action or resource. Today the gateway role reads this table
with `implicitDeny` (the CRO's G4 spec).
What an Opal analyst learns through the tool: a security's `asset_class` and `sub_asset_class`, who classified it (`classified_by`: scheduled, model, legacy or seed), the model's
`classification_confidence` and `low_confidence`, and the descriptive columns the item carries (`name`, `sector`, `listing_country`, `instrument_kind`, `management_style`, `last_updated`).
The census read the attribute names from a 200-item sample, so a rarer attribute is not listed here; the grant is by item, not by attribute, so the gateway can read every attribute of an item it asks for.

## 3. The tool

`mdpf_get_security_classification` (cell `OG-ac-2`, module `app/mdpf_classification.py`) is the only user. It is for Opal principals only and refuses before any DynamoDB call on a missing
principal, a principal that is not an Opal user, a missing or non-string `ticker`, a `ticker` over 96 characters, or one holding whitespace or `/` (spec section Refused). No other tool,
page or person's login reads this table through this policy.

## 4. The order of acts (Phase B, on a GO naming all three halves signed at the hash)

1. Ledger `nfra-oplgtw-grants-ap25`, entry and sentinel first; `comp-schedule --drift` at the act, what it scanned recorded.
2. Apply the one policy through `safe-apply`, targeted at it, 1 add. Read it back: `get-role-policy` (one statement, `dynamodb:GetItem` only, the table ARN), then `simulate-principal-policy`, ONE resource per call:
   GetItem allowed; Scan not allowed (the negative control, run as its own invocation); a `*`-principal positive control beside any deny read; and an existence read of the table ARN (`describe-table`), because a simulated `allowed` proves the pattern and not the table.
3. Re-plan the target: `No changes`. Re-hash nothing else (no other policy is touched).
4. The grant is live BEFORE the code release that serves the tool (after `OG-ap-23`).

## 5. Both branches

A refused call reads zero items: the tool refuses before any DynamoDB call, and an unlisted action or table is denied by IAM. An admitted call reads exactly one item by `ticker`. The applier cannot
call the table as the gateway role, so the IAM branch is read at Phase B by the simulator (GetItem allowed, Scan not allowed); the code branch (zero calls on a refused argument, one on an admitted) is graded at `OG-ac-2`'s release.

## 6. The rollback

`delete-role-policy` for `gateway-global-etf-classification-read-policy` on `opal-gateway-role`, or `terraform destroy` targeted at `aws_iam_role_policy.gw_etf_classification_read`; this removes only what
this ask added. Nothing else on the role changes and no table item is touched. Trunk: `git revert` of the `.tf` commit via `safe-commit`.

## 7. The triggers

The act is complete only when ALL hold: (1) the policy reads back live with exactly one statement, `dynamodb:GetItem`, the table ARN; (2) the simulator allows GetItem and does not allow Scan; (3) the targeted re-plan reads `No changes`; (4) the ledger is CLOSED and
`W/CLS_APPLIED.json` is written. Any other reading stops the act and the policy is destroyed, with an ARMED row naming `2.0.0_SA_COO~O`.

## 8. The gaps

None named. Two limits stated: the census sampled 200 of 11,362 items for attribute names, and the item count in `CLS_BEFORE.json` (11,362) is `describe-table`'s estimate, which equals the census's paginated count; Phase A reads no item.

---

## CTO half

**Half: `1.0.0_SA_CTO~Z`** -- sign / refuse: ______________

## COO half

**Half: `2.0.0_SA_COO~O`** -- sign / refuse: ______________

## CVO half

**Half: `3.0.0_SA_CVO~Z`** -- sign / refuse: ______________
