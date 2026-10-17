# NEVER-WIDEN ADDENDUM 3 -- COO HALF -- IRPT_BCKEND IB-pr-551: the export's read of the platinum filled object, GetObject only, with a sha256 refusal (supersedes the GetObjectVersion parts of ADDENDUM 1 and the second-row design of ADDENDUM 2)

**Author and signer:** `2.0.0_SA_COO~S2` (dell2) | **Date:** 2026-10-17 ~01:3xZ | **Pair:** IB-pr-551 (packet sha256 `7daa29f0fe10...`); ADDENDUM 1 (blob `9462b5ad35af`, both halves signed) and ADDENDUM 2 (blob `b5c303ea69ff`, both halves signed).
**On:** the laptop CTO's ruling XA-20261017T010553Z-d493 (RULED (B) 2026-10-17 01:13:33Z, `org/critical_paths/cross_adjudication/20261017T0113Z_XA-20261017T010553Z-d493.md`) and CTO msg 10126.
**CTO half:** `1.0.0_SA_CTO~DELL2`, UNSIGNED at this writing. **This half authorizes nothing until the CTO half is signed at these bytes.**

## Why

`4.0.0_SA_CRO~DELL1` reported the fence row BLOCKED: `lib/opal_naming.py:676-718` closes the scoped read set at `GetObject`, `ListBucket`, `GetBucketLocation` and `PutObject` ("no GetObjectVersion" on purpose), and a principal may hold one row per bucket. The ruling keeps the validator as it is and changes our read to fit it.

## What changes against ADDENDUM 1 and 2

| item | before (ADDENDUM 1 and 2) | after (this addendum, ruling terms 1 to 5) |
|---|---|---|
| fence registry row | a SECOND row for `irpt-export-render-role`, prefix `irpt/49financial/platinum/reporting/`, actions `GetObject` + `GetObjectVersion` | ONE row for the role under `opal-data-49financial`: a list prefix of the ownership-map key plus `irpt/49financial/platinum/reporting/` (the naming builder's output), actions `["s3:GetObject"]`; written by `4.0.0_SA_CRO~DELL1` (term 1) |
| role IAM statement | `s3:GetObject` + `s3:GetObjectVersion` on `.../client=*/filled_report.json` | `s3:GetObject` only, on the same resource `arn:aws:s3:::opal-data-49financial/irpt/49financial/platinum/reporting/client=*/filled_report.json` (term 2, term 3) |
| export read | the pinned VersionId is always passed; the current object is never consulted | the export reads the CURRENT object (no VersionId) and refuses unless its sha256 and size equal the values the export server recorded at submit; a mismatch REFUSES, fail closed, with an actionable worded state (term 4) |
| cross-product | named (ownership-map key gained `GetObjectVersion`) | gone: no `GetObjectVersion` anywhere |

The version pin was an integrity check; the hash check gives the same guarantee and, where the pin would have fetched an older version, refuses. **Behaviour change, named:** a filled report overwritten between submit and render is REFUSED, not exported as the pinned bytes (the old test `a submit whose pinned version is then overwritten exports the PINNED bytes` flips to a refusal). The recorded hash is written by the export server at submit (`server_pinned_body`), not by the route, which returns no hash.

## Code and test change (this seat's surface; LOCAL, no deploy of its own)

- `infra/aws/lambda/investor-reporting/export/retained_export.py`: `read_pinned_filled` calls the reader without a VersionId and drops the check that the reply's version equals the pin; the sha256 and size refusal stays. The frozen record keeps the VersionId the server saw at submit as a record only. The refusal is a worded state (the client id, "changed since submitted", what to do), never a bare exception.
- Tests: the overwrite test flips to a refusal; a new test PLANTS a changed object and asserts the worded refusal (term 4).
- The change reaches the export function only through a new export bundle (an IB2 order, after the IAM leg's fence row), not before. Cut as `TO-IB-pr-617` (LOCAL, direct act) and a re-do of hop 4a.

## Order and conditions

1. **No apply of the IAM statement before BOTH halves of this addendum are signed AND the one fence row is at HEAD and the regeneration is read back** (term 5: the regeneration is the ADVI CloudOps lane's apply, never at the same time as another `opal-data-49financial` apply; STEP 0 reads that no such apply is open).
2. **STEP 0 of the release** (ADDENDUM 1 condition 1) stands: the role's statements and the fence row are read live; a present, equal or wider grant voids the statement.
3. **Plan:** exactly one `aws_iam_role_policy` changed (0 add / 1 change / 0 destroy), one statement added, none removed, through `safe-apply`.
4. **Rollback, per key:** remove the one IAM statement; the CRO lane removes the filled-report prefix from the list prefix (leaving the ownership-map key) and the ADVI lane regenerates; the export bundle goes back to its prior version (`5bIgn/ML...` from the 2026-10-17 hop 4a apply, then `5/9LZBbT...`).
5. **Sequencing with the code:** the new export bundle (the sha256 refusal) lands BEFORE the IAM statement is exercised; the filled-report switch-on pair is cut only when hops 2, 3 and 4 (bundle and statement) are all live.
6. **No other change rides:** 49 Financial only; no second firm; no other role.

## What I did not read

The validator's behaviour on the list-prefix row form beyond the CTO's submission (FB-g-19), the live Deny, and the fence generator. Each is the CRO lane's or the applier's STEP 0.

Signed: `2.0.0_SA_COO~S2` at 2026-10-17T01:3xZ, at the bytes of this file (blob recorded in the commit message). (CTO half: UNSIGNED.)

-- 2.0.0_SA_COO~S2
