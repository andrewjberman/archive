# Packet -- AR-v-12 deploy: ticket_center names its package principal (`svc-irpt-packager`), firm-bound (IRPT_ANLREQ round 1, workstream TICKET)

**For:** `1.0.0_SA_CTO~DELL2` (CTO never-widen half). **Author:** `2.0.0_SA_COO~V2`, 2026-10-09 ~05:3xZ. **Applier:**
`0.7.0_AE_CloudOps~DELL2` (Andrew-direct ~05:0xZ: "have them do it").

**Authority:** decomposition `IRPT_ANLREQ_DECOMP_R1.md` @52e8fa4fe7, hop 8 and C-PACKAGER; drain @86454002bf. Worker `~12`'s criteria
were re-run by the issuer with invalid AWS keys: 6/6, and the suite at 137.

**COO half: SIGNED below.** Code only: no env, route, IAM or grant.

## 1. What ships

| | value |
|---|---|
| code | `infra/aws/lambda/ticket_center/lambda_function.py` at box/dell2 `86454002bf`; file sha256 (hex) `04f5727bebf83e7c19493f944bc1c8ed2f7a28404b5137d6cf2cb32b699f9a38` (`BUILD_ONLY=1`, nothing uploaded) |
| live now | CodeSha256 `ywAvsfx...` (SA-k-1, file `21fe06e0...`) |
| delta since live | ONLY AR-v-12: `package_principal` changes from `""` to `"svc-irpt-packager"`, and `package_ticket` gains the firm check against the packager's own PROFILE `allowedFirmIds` LIST (no row, empty, non-list or lookup error returns 403) |
| plan expected | `0 to add, 1 to change, 0 to destroy`: the function's source hash, with `s3_object_version` moving with it (the SA1 precedent) |

## 2. Blast radius (both branches)

- **Live behaviour after the apply is still "refuse every caller"** on `POST /tickets/{id}/package`, because:
  - (a) no `svc-irpt-packager` token exists (its mint is a later pair, with `~G2`'s packager AR-g-12);
  - (b) even with a token, no PROFILE row with a list exists for it, so the new check returns 403.
- Every other route and principal is unchanged (the delta is confined to `package_ticket` and one type-data value).
- **Rollback:** re-apply the SA-k-1 build (`6e19a53535`, file `21fe06e0...`).

## 3. After-reads

1. The deployed `lambda_function.py` is `04f5727b...`.
2. The env is unchanged (8 keys).
3. An unauthenticated POST is refused.
4. ItemCount is unchanged.
5. The replan is 0-diff.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-09, for the blast radius above, both branches.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
