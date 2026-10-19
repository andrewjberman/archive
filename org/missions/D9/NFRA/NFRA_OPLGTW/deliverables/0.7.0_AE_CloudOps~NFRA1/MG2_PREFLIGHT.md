# OG-mg-2 Phase A -- preflight record (comp-iam, operator identity, approver)

Applier: `0.7.0_AE_CloudOps~NFRA1`. Read at 2026-10-19T18:18:50Z. Counts, roles, keys and hashes only; no tid, oid, e-mail or account id is written here.

## Operator identity and comp-iam (re-simulated in Phase A)

- `sts:AssumeRole` into `opal-gateway-access-admin`: ASSUMED (the session ran `prepare()` under it; it wrote nothing).
- `simulate_principal_policy` on that role against `gateway-access-state-table`, with the `dynamodb:LeadingKeys` context `POLICY#*`: `dynamodb:PutItem` allowed, `dynamodb:UpdateItem` allowed (the writes `activate()` makes). Neither is implicitDeny.
- Strong reads of the store ran under the CALLING principal (a fully paginated `Scan`, 3 pages, 2074 items, 25 `POLICY#` items). The operator role holds no `Scan`: it writes only.

## Roles resolved

Both roles resolved in-process by the profile's e-mail prefix to EXACTLY ONE active `principal_profile` each (`andrew` pk_hash `a18b74486b`, `alyssa` pk_hash `2c61471b14`). The Bloomberg principal and every other profile are not touched.

## Approver and source authorization

Approver: `Andrew Berman` (the activation's `--approver`). Source record: `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261019_172xZ_ALYSSA_3PM_SCHWAB_TEST_SENDS_YES_ROSTER_AS_OPEN_CALLS_SCHWAB_FULL_ACCOUNTS.md` (commit 65a05f6658), relayed by `1.0.0_SA_CTO~Z` msg 36025 (a), (b). Andrew's word, verbatim, item 4:

> Schwab should automatically cover the full accounts, that should be easy enough to do because the premise should be that the tool is simply hitting what is being refreshed in AWS every single day, there shouldnt be a persisted list or anything of the sort because theres no need, it just needs to be redirected to the correct bucket

The order's open point stands for the halves: whether that word reaches Alyssa's grant (the CTO relays it for both).

## A finding the order does not mention (also in the ask, section 3)

`activate()` also puts one `email_deny` record per plan e-mail (row W3-S22). Measured now: Andrew's `email_deny` record DOES NOT EXIST (it was removed by the audited reversal, OG-ap-30); Alyssa's EXISTS. So activating Andrew's candidate would re-create it.
