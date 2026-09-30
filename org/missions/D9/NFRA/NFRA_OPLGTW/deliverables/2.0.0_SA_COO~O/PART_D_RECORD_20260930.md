# Part D record -- the switchover sitting's principal read (call 3), 2026-09-30

**By:** `2.0.0_SA_COO~O`. **Sheet:** `CALL3_PART_D_SHEET_20260930.md` @79c4956122. **Scope:** `1.0.0_SA_CTO~O` msg
27304 (call 3 = Part D only). **Why this source:** row `NFRA_OPLGTW-Z-S20` (the owner header carries `sub` but no
`oid` or `tid`).

## What was read

| item | principal | role in OG-t-2 |
|---|---|---|
| Tenant ID | the Opal tenant | the `<tid>` of every pair |
| Object ID | `andrew@opalinvest.com` | `ADMIN_PRINCIPAL` (`MASTER_ADMIN_PRINCIPALS`) |
| Object ID | `alyssa@opalinvest.com` | `WRITE_CAPABLE_PRINCIPALS`, 1 of 2 |
| Object ID | `opalbloomberg@opalinvest.com` | `WRITE_CAPABLE_PRINCIPALS`, 2 of 2 |

- **Source:** Andrew, from the Entra admin center, pasted into the `2.0.0_SA_COO~O` terminal at 2026-09-30 20:54:51Z
  (three values) and 20:57:35Z (Alyssa).
- **Shape:** 4 of 4 are GUIDs, and all 4 are distinct.
- **Corroboration from a second plane:** the tenant ID's and Alyssa's object ID's first 8 characters equal her existing
  grant's key (`6810043e/ad037ea5`, recorded in
  `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260930_14xxZ_AGREED_LAPTOP_PUSH_AND_ALYSSA_SCHWAB_GRANT.md`).
  The other two object IDs have no second plane at this read.
- **No roster widens:** the same three people hold these roles in today's email rosters (`deploy-to-ec2.sh:197`).

## Where the values are (never in this repository)

`%LOCALAPPDATA%\opal\og-principals\part_d_20260930.json` on site Z: 451 bytes, sha256
`536797163dc6cca208a59a1e6c69e4c32cdddff6ccffc7bf070e7d48ed561e4c`. OG-t-2's hand-off message carries the pairs and
cites this record. Remove the file when OG-t-2 closes.
