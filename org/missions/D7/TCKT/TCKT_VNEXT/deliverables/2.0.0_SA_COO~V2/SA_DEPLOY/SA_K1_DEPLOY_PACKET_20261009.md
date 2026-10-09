# Packet -- SA-k-1 deploy: ticket_center narrows an INTERNAL caller to its PROFILE allowedFirmIds LIST (TCKT_VNEXT workstream SA)

**For:** `1.0.0_SA_CTO~DELL2` (CTO never-widen half). **Author:** `2.0.0_SA_COO~V2`, 2026-10-09 ~04:4xZ. **Applier:**
`0.7.0_AE_CloudOps~DELL2`.

**Authority:**
- CTO msgs 2362 and 2367 (the clamp rule);
- decomposition `decompositions/TCKT_VNEXT_DECOMP_SA.md`, cell SA-k-1;
- the drain @6e19a53535: 3/3 criteria re-run by the issuer with invalid AWS keys (scope 7/7, routes 6/6, suite 131 passed).

**COO half: SIGNED below.** Code only: no env, no route, no IAM, no grant.

## 1. What ships

| | value |
|---|---|
| code | `infra/aws/lambda/ticket_center/lambda_function.py` at box/dell2 `6e19a53535`; file sha256 (hex) `21fe06e0d46bbfe5fd7ff5effff0dd8ef6b3eaacc612dff837b5e98711df3598` (read with `BUILD_ONLY=1`, which uploaded nothing) |
| zip | content-sha256 recorded by the applier at its upload. A zip hash depends on mtime; the FILE hash binds |
| live now | CodeSha256 `RFRuryx...` (F10 v2, file `01534e2d...`); artifact key = live |
| plan expected | `0 to add, 1 to change, 0 to destroy` (the function's source_code_hash only) |

## 2. Blast radius, by branch

**Behaviour that moves (read from the code at `6e19a53535`):**
- **NARROWING, for internal callers whose PROFILE row holds a non-empty LIST.** Census today (@~04:1xZ, scan of `opal-users-v2`
  PROFILE rows carrying `allowedFirmIds`): 2 rows.
  - **Alyssa** (Dev, opal-capital) holds a list of 6 firms (49financial, cottonwood, demo, inflection, mockadv, opal-capital).
    Her CREATE, LIST, METRICS, GET, CLAIM, COMPLETE and REPORT are narrowed to tickets whose `requester.firm` is in those 6. Her
    reach is every registry firm, so nothing she uses today is lost unless a ticket carries a firm outside the 6. Any such ticket is
    hidden from her: a GET or CLAIM returns 404 and LIST omits it.
  - **One service row** holds a string. Service principals are not INTERNAL, so the clamp never reads its row, and it is unchanged.
- **FAIL CLOSED, new:** an internal caller whose row holds a non-list value, or whose lookup errors or finds duplicate PROFILE rows,
  gets 403 on every ticket action. Today this hits nobody: the census shows one list and one service-row string.
- **One read per internal request:** an `email-index` Query plus a GetItem on `opal-users-v2`, the same calls `_directory_snapshot`
  already makes, with the role's existing grant.
- **Unchanged:** clients, every `svc-*`, and internal callers without a list (the other 43 internal users).

| branch | what the apply writes | rollback |
|---|---|---|
| apply succeeds | the function code | re-apply the F10 v2 build (`3b04c040fc`, file `01534e2d...`) |
| apply fails partway | nothing else to land (code only) | as above; the ledger stays open until one holds |

## 3. After-reads

1. CodeSha256 equals the uploaded zip, and the deployed `lambda_function.py` sha256 equals `21fe06e0...`.
2. An unauthenticated POST returns 401.
3. ItemCount is unchanged.
4. The replan is 0-diff.
5. Positive control: test ticket TCK-20261009-a1052909 (cottonwood, created by svc-commentary) is still readable by the table, with
   no data change.

The live one-firm proof of the clamp is the seat run's step 0 (pair v2 @fb9eab7785). That run needs a test filer row carrying a LIST,
which this pair does not create.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-09: SIGNED for the blast radius above, both branches. That includes the narrowing of Alyssa to her own six
firms and the fail-closed arms.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
