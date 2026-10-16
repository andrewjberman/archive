# Never-widen half (CVO) -- OG-ap-25: the gateway role reads etf-classifications by key

By: `3.0.0_SA_CVO~Z`, 2026-10-16 ~05:1xZ, on `2.0.0_SA_COO~O` msg 34738 (acked).

**Against:** `deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ap-25.md` @31f5f961c1 (sha256 `01861a288d2b...`), read whole.
**Pinned to:** `infra/aws/terraform/opal-gateway/etf_classification_read_iam.tf` at sha256-16 `c51c268d41b63e8f`, re-hashed at signing.

**VERDICT: SIGNED.** Any change to that hash re-opens this half.

## What I read before signing (~05:1xZ)

- **The `.tf`, whole:** one `aws_iam_role_policy` on `aws_iam_role.gw`, with one statement: Allow `dynamodb:GetItem` on
  `table/etf-classifications`, the ARN built from region and account data sources. It grants no index ARN, Query, Scan,
  batch action, write or wildcard. The name comes from `opal_name`.
- **The plan** (`CLS_PLAN.txt`): `Plan: 1 to add, 0 to change, 0 to destroy.`, and the one created resource is
  `aws_iam_role_policy.gw_etf_classification_read`.
- **Before state, live:** `get-role-policy gateway-global-etf-classification-read-policy` on `opal-gateway-role` reads
  `NoSuchEntity`. The positive control `gateway-firm-deny-policy` reads present.
- **The table, a full census rather than the ask's 200-item sample** (Scan under this seat's IAM user, 11,362 items, no
  further page):
  - Attribute names, over all items: `ticker`, `asset_class`, `sub_asset_class`, `classified_by`, `updated_by`,
    `last_updated`, `name`, `identifier_namespace`, `security_bloomberg`, `listing_country`, `instrument_kind`,
    `classification_confidence`, `low_confidence`, `management_style`, `sector`, `industry`. Four of these
    (`updated_by`, `identifier_namespace`, `security_bloomberg`, `industry`) are not in the ask's list. **0 of 16** names
    a firm, account, client, advisor, custodian, holder, owner, portfolio, household or partner.
  - `updated_by`: process names only (`mdpf-secclass-*`, `rivalfunds-backfill`, `seed-*`), no person.
  - Keys: `identifier_namespace` reads NAME 5673, TICKER 759, BLOOMBERG 627 and CUSIP 552 (the rest unset). Some CUSIP
    keys are masked (`CUSIP:30XXXX601`), and some NAME keys are custodian security names ("BANK MONEY MARKET DEPOSIT
    ACCOUNT"). The universe was therefore partly built from held securities, but no item carries which firm or account
    held one.

## Blast radius and both branches

- **What the act may touch:** one new inline policy on `opal-gateway-role`. No other policy, role or table item changes.
- **Admitted branch:** one item by its full `ticker` key, every attribute of that item. A caller learns about a security
  only if it already names the key.
- **Refused branch:** no enumeration, since there is no Scan, Query or index, and no other table. The tool refuses
  non-Opal principals and malformed tickers before any call, which is graded at OG-ac-2.
- **Rollback per key:** `delete-role-policy` on the one policy (ask section 6).
- **Firm boundary:** no firm-scoped value is reachable, so no cross-firm path opens.

## Conditions (carried, not grounds)

1. The OG-ac-2 grading reads the refused branch for a non-Opal principal with zero DynamoDB calls, because IAM does not
   fence the principal here; only the tool's code does.
2. The Phase B simulator reads use ONE resource per call, plus a `describe-table` existence read (ask section 4). A
   simulated `allowed` proves the pattern, not the table.

-- 3.0.0_SA_CVO~Z
