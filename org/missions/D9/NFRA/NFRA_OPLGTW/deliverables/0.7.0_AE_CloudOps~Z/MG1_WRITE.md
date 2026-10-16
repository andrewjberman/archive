# OG-mg-1 Phase B -- the two writes and the read-back (0.7.0_AE_CloudOps~Z, 2026-10-16)

GO: msg 34954 (`2.0.0_SA_COO~O`), all three halves signed at ask sha256 `757f5146afee` (COO `020264306c`, CTO `c92d6c7c07`, CVO `5c4025b899`). Ledger
`nfra-oplgtw-r30-grant-writes` opened and committed (entry AND sentinel) before any write. No tid, oid, email or scope value appears here: pk hashes, roles, keys,
counts and revisions only (C7).

## C2 -- the re-read at the GO (`mg1_phaseb_reread.py`, 2026-10-16 ~11:19Z)

| check | read | want |
|---|---|---|
| Andrew (pk_hash `a18b74486b`) POLICY# items | 0 | 0 |
| Bloomberg (pk_hash `3c1d2597c9`) POLICY# items | 0 | 0 |
| Alyssa (pk_hash `2c61471b14`) profile | active / restricted / revision 4 / grant revision 4 | same |
| host `MASTER_ADMIN_EMAILS` | exactly 1 alias, sha10 `7b1bca22c9`, domain `opalinvest.com` | exactly 1 |
| R1 / R2 candidate email sha10 | `7b1bca22c9` / `f39c9b2025` | the Phase A values |
| denominator | POLICY# 17 of 1715 items scanned, one consistent page | -- |

RESULT: CLEAR. Alyssa's complete item set (9 items, all attributes, canonical JSON) hashed `b93cd3cbf990` before the writes.

## The two activates (`mg1_activate.py`, one `activate` each, under `opal-gateway-access-admin`, `--approver "Andrew Berman"`)

The `--source-authorization` string names CTO ruling msg 32383, decomposition R3-T.31, PRD v2.3 item 1, CTO ruling msg 33850, the ask sha and its three halves, and
the GO msg 34954. The module printed prepare()'s diff to the off-repo store X only.

| record | order | line printed by the module | exit |
|---|---|---|---|
| R1 (Andrew's principal) | first | `ACTIVATED profile_revision=1 grant_revision=1` | 0 |
| R2 (the Bloomberg principal) | second, after R1's line was read | `ACTIVATED profile_revision=1 grant_revision=1` | 0 |

No `REFUSED`, no stale base, no retry. Each ran as one `operator_transact` (profile, grant revision, operator_audit, one email_deny put).

## C5 -- the read-back (`mg1_readback.py` -> `MG1_READBACK.json`, 2026-10-16T11:23:57Z, strongly consistent, fully paginated, 1723 items)

| role | pk_hash | profile | grant in force | scope |
|---|---|---|---|---|
| andrew | `a18b74486b` | active, restricted, revision 1 | revision 1, active | 7 keys, `dates.calendar_months` 13, operations describe / download_filtered / list / query |
| bbg | `3c1d2597c9` | active, restricted, revision 1 | revision 1, active | identical |
| alyssa | `2c61471b14` | active, restricted, revision 4 | revision 4, active | untouched |

- R2 scope equals R1 scope: **true**, zero differing keys (whole-object equality of the stored scopes).
- R1 against Alyssa's revision-4 scope: changed top-level keys **none**; the window is 13 months in both (her scope was already at 13).
- Alyssa unchanged: her 9 items hash `b93cd3cbf990`, equal to the hash before the writes.
- Counts, before to after: POLICY# items 17 to 25 (+8 = 2 profiles, 2 grants, 2 operator_audit, 2 email_deny); profiles 4 to 6; grants 4 to 6; audit 8 to 10; email_deny 1 to 3.
- C6: exactly one email_deny per record (the deny count rose by exactly 2).
