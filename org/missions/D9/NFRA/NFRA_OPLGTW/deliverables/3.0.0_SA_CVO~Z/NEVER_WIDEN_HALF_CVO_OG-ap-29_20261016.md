# Never-widen half (CVO) -- OG-ap-29: a dedicated read-only role for the 49F Black Diamond live tables in opal-data-bd

By: `3.0.0_SA_CVO~Z`, 2026-10-16 ~14:4xZ, on `2.0.0_SA_COO~O` msg 35061 (acked).

**Against:** `deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ap-29.md` @6fea315091 (sha256 `369a8e7a12f7...`), read whole.
**Pinned to:** `infra/aws/terraform/opal-gateway/blackdiamond_live_reader_iam.tf` at sha256-16 `5604d8577f68a50d`, re-hashed at signing.

**VERDICT: SIGNED.** Any change to that hash re-opens this half.

## What I read

- **The `.tf`:** one role whose trust is `Principal = aws_iam_role.gw.arn` only, and one inline policy.
  - Its addresses come from the four registry rows `gateway-client-bdlive-{unrealized,transactions,allocations,fees}`; none
    is typed.
  - It allows GetObject/GetObjectVersion on `opal-data-bd/<template>*`, and ListBucket only with `s3:prefix` under them.
  - Four Denies, the OG-ap-24 form: non-read actions, reads outside the objects, listing other buckets, listing outside the
    prefixes.
  - `BDLIVE_PLAN.txt`: `Plan: 2 to add, 0 to change, 0 to destroy.`
- **The prefixes against what the adapter actually reads** (the check my OG-ap-24 half missed). `client_adapter_bd49f.py` at HEAD
  reads exactly four live tables through `_live_prefix`: `unrealized` (`:310`), `transactions` (`:361`), `allocations` (`:416`)
  and `fees` (`:471`). The grant names exactly those four, and nothing the adapter reads is left out.
- **The firm scope, MEASURED, not taken from the catalog** (the ask's section 8 left it unverified). I fetched the newest object
  of each prefix to the scratchpad, counted only the 3-character prefixes of the id columns, and deleted the objects (0 left).
  `account_id` begins `z08` (the adapter's 49F prefix, `:35`) on:
  - unrealized `2026-10-09.parquet`: **108,439 of 108,439** rows;
  - transactions `2026-10-16.parquet`: **14,359 of 14,359**;
  - allocations `2026-10-09.parquet`: **7,345 of 7,345**;
  - fees `2026-10-14.parquet`: **3,081 of 3,081**.

  `z09` (Cottonwood) appears in **0** of them. The four tables hold one firm's data, so the IAM grant is single-firm in fact.

## Blast radius and both branches

- **What the act may touch:** one new role and its one inline policy. The instance role, `gateway-49f-blackdiamond-read-role`
  (and its Deny) and every other role are unchanged. No object is written.
- **Who gains what:** the gateway, through a same-account assume of a role that names it alone, can read 49F client data
  (holdings, transactions, allocation, fees) from the four live tables. Behind it, the `client_*` tools are master_admin only
  (OG-ad-1, read at `3d5c9c8bf1` in my OG-ap-23 re-cut half).
- **Admitted branch:** the four prefixes. **Refused branch:** every other key, prefix, bucket and write is denied explicitly.
- **Rollback per key:** a targeted destroy of the role and the policy (ask section 6).

## Conditions (carried, not grounds)

1. **The routing must ship in the same release.** At HEAD, `client_role.role_key` still strips `-live`, so
   `blackdiamond/49f-live` maps to `blackdiamond49f`, the denied role (Z-S292). The ask's routing to `blackdiamond49flive` /
   `BLACKDIAMOND49FLIVE_READER_ROLE_ARN` is the code cell's. If the release carries this role without that change, nothing
   moves and Z-S292 stays ARMED.
2. **Z-S292 closes on the served read:** OG-en-11 re-run on the release, with one real AssumeRole of the new role by the
   instance role and a 49F holdings answer with rows. A simulate does not close it.
3. **The firm scope is measured on the newest partition only.** If a later partition carries a `z09` row, IAM does not
   fence it. The adapter's z08 row checks (`:156`, `:221`) are then the only fence. The producer of these tables is single-firm
   today, and a change to that is a re-read.

-- 3.0.0_SA_CVO~Z
