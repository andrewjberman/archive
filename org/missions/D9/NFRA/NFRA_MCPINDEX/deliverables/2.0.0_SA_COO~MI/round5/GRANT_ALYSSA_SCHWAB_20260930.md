# Alyssa's Schwab grant -- written 2026-09-30T19:15:29Z (2.0.0_SA_COO~MI, MX-r-6 A5/A6)

- **Authority:**
  - Andrew "agreed" @29bc46d827: ONE new Schwab grant to Alyssa, two masters, four datasets.
  - Andrew "recs approved, proceed" @2bd24e1ac6: all accounts under both masters; read-only list/describe/query, no
    download.
  - CVO H2: she is named before the write, and hers is the only grant.
- **Principal:** tid `6810043e-d171-4adc-9975-068b35e179da`, oid `ad037ea5-fee8-412e-9da9-15c6cf2a4fbc`,
  `alyssa@opalinvest.com`. It is the only grant written.
- **Writer:** `infra/aws/ec2/opal-gateway/ops/schwab_entitlement_admin.py activate`.
  - Run as `arn:aws:sts::313476888478:assumed-role/opal-gateway-access-admin/coo-mi-alyssa-grant`
    (`check_operator_identity` OK).
  - Contract: the release's `org/standards/NFRA_OPLGTW_CONTRACT.json` (wk-nfra_mcpindex-5-19), which lists
    `dim_transaction`.
- **Account source:** the union of distinct `account_id` in the newest `dim_balance` and `dim_position` partitions per
  master.
  - 08242234: date=2026-09-29. 08335338: date=2026-09-28.
  - All ids match the scope parser's account pattern.
  - Raw ids were held only in the session scratchpad and deleted after the write. They are never in the repo.

## Before (profile revision 1, grant revision 1 -- OA-g-3, 2026-09-27)

- masters [], datasets [], accounts {}, columns {};
- operations [query];
- dates rolling_complete_window;
- 10 portal_channels. A portal-only grant: no Schwab tool admitted.

## After (profile revision 2, grant revision 2, status active -- read back from gateway-access-state-table)

| Field | Value |
|---|---|
| masters | 2 (08242234, 08335338) |
| accounts | 7,477 and 7,559 (sha256 of the sorted ids, first 16 hex: b027fe468fcb2c65, 2e5384b6f55f1b1a -- equal to the candidate's) |
| datasets | dim_asset, dim_balance, dim_position, dim_transaction |
| columns | every contracted served column (dim_position 11, dim_balance 9, dim_asset 9, dim_transaction 15) |
| operations | describe, list, query (no download_filtered) |
| dates | rolling_complete_window |
| portal_channels | 10, unchanged |
| operator_audit | 2026-09-30T19:15:29Z, approver andrew@opalinvest.com |

**The scope diff printed by `prepare` before the write** added the masters, the 4 datasets, the accounts, all columns and
the list/describe operations. It removed nothing. Portal channels and dates were unchanged.

**Rollback:** `schwab_entitlement_admin.py revoke` (a tombstone), or re-activate the revision-1 portal-only scope.

**Next:** r6.J1, Alyssa's cold run as the non-author asker: one Schwab position question and one transaction question,
each for one master and one date, in a fresh session with only the MCP connected.
