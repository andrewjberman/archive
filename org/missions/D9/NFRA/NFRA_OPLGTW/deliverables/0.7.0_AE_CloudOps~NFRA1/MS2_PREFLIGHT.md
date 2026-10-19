# OG-ms-2 Phase A -- preflight record (comp-iam, operator identity, approver)

Applier: `0.7.0_AE_CloudOps~NFRA1`. Read at 2026-10-19T21:25:20Z. Counts, roles, keys and hashes only; no tid, oid, e-mail or account id is written here.

## Operator identity and comp-iam (re-simulated in Phase A)

- `sts:AssumeRole` into `opal-gateway-access-admin`: ASSUMED (the session ran `prepare()` under it; it wrote nothing).
- `simulate_principal_policy` on that role against `gateway-access-state-table`, with the `dynamodb:LeadingKeys` context `POLICY#*`: `dynamodb:PutItem` allowed, `dynamodb:UpdateItem` allowed. Neither is implicitDeny.
- Strong reads of the store ran under the CALLING principal (a fully paginated `Scan`, 3 pages, 2104 items, 27 `POLICY#` items, 6 profiles).

## Role resolved

`alyssa` resolved in-process by the profile's e-mail prefix to EXACTLY ONE active `principal_profile` (pk_hash `2c61471b14`, profile revision 6, grant revision 6). Andrew's grant (revision 1) and every other profile are not touched.

## Approver and source authorization

Approver: `Andrew Berman`. Source record: `org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20261019_195xZ_ALYSSA_SCHWAB_MASTER_0840_ADD_TO_ENTITLEMENTS.md`, relayed by `1.0.0_SA_CTO~Z` msg 36102 and sequenced by its ruling (B) msg 36104. Andrew's word, verbatim:

> we need to add 0840 to her search ability for schwab. she has the 0824 and 0833 accounts at schwab, the smartx and black diamond masters. she needs the 0840 master too added to her entitlements.

The record carries the mapping "0840" -> master `08403355` as INFERRED; Phase A confirms it against the bucket: `08403355` is the ONLY prefix beginning 0840 under `schwab/` (3 master prefixes in all).
