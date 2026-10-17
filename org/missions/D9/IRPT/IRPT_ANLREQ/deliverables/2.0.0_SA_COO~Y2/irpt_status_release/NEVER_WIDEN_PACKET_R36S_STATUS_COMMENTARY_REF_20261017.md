# Never-widen sign-off packet -- r36 Lambda leg: irpt-status packages the acceptance module that carries get_commentary_ref, at pin ae2ab2072b

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~Y2`, 2026-10-17. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane).
**Authority:** CTO msg 10600 (release irpt-status so the commentary PDF of a ticket opens); `ops/owned_report.py:350-373` refuses COMMENTARY_PDF_NOT_RETAINED when the packaged acceptance lacks `get_commentary_ref`. **Ledger:** `irpt-status-r36s-20261017`.
**Scope:** ONE Lambda code release (`irpt-status`). No IAM, route, queue, table, secret, schema or resident host moves. No vendor call.

## 1. What ships

Pin `ae2ab2072bb2341e3590a86123e343d2e2e82387` (the map edit: `infra/aws/lambda/ci/function-map/irpt-status.json`, numstat 2 2; `acceptance.py` staged-from pin `361c44fa9d` -> `06557b66184a5b3093f52bd80d2e8ee0be682e8c`, sha256 `0c4acec625b7da70da82efccf58cc967e9e5bf53c32e955d67079b711701513d`). Merged to `box/dell2` at `1872163873`. Built twice, byte-identical, by worker `0.9.0_WK_IRPT_ANLREQ~291` (record `r50/R36S_BUILD.json`); the issuer re-ran `live_diff.py` against the issuer's own record of the live zip: `LIVE-DIFF-OK moved=1 added=0 removed=0 same=48`, and `--selftest` `CONTROL-FIRES`.

| function | zip sha256 | CodeSha256 | bytes | members | changed vs the live package |
|---|---|---|---|---|---|
| `irpt-status` | `dbbe1d9766c2776542dce717e14a9ce0031b59ea7ae41f7b175f8254da0a7cc7` | `274dl2bCd2VC3OcX4Uqc4AMbWep65B97F1+CVNoKfMc=` | 368788 | 49 | 1 |

| member | live sha256 (12) | built sha256 (12) | attribution |
|---|---|---|---|
| `acceptance.py` | `06425d4731b7` | `0c4acec625b7` | 3 commits between the old and new staged pin: `2f7cc7be42` (AR-y-37, `accept` records `acting_principal_id`), `74bbdbb322` (IB-pr-455, optional boolean `commentary_requested`), `06557b6618` (IB-pr-478, adds `get_commentary_ref`, the packager reads `commentary_ref` from the request item's sibling attribute) |

The live package: CodeSha256 `+TcZDWmwE7uv3sUwos2+jn1lbKyQikK+13nNBzD6q4A=`, 49 members, handler `status_installed.lambda_handler`, python3.12, LastModified 2026-10-16T06:12:33Z, 368309 bytes (record `LIVE_IRPT_STATUS_MEMBERS_20261017.json`). The other 48 members are identical to it.

## 2. Blast radius (read from the code at the pin)

| what the status route answers for | BEFORE | AFTER |
|---|---|---|
| the status envelope of any request | as today | the SAME (the status handler never calls `accept()`; the added `accept(acting_principal_id)` writer change and `commentary_requested` copy are inert here; imports of the module unchanged) |
| the commentary route (`ops/owned_report.py`, report-record path) for a request whose item carries a commentary ref | COMMENTARY_PDF_NOT_RETAINED (the packaged acceptance lacks `get_commentary_ref`) | the ref is read and the PDF link returns |
| a request with no commentary ref | COMMENTARY_PDF_NOT_RETAINED | the same refusal as the code gives for an absent ref |
| any other route, role, table, key | unchanged | unchanged |

**Who gains: no principal class.** The route's creator/assignee check (`lambda_function.py:1750-1753`) is untouched. **Writers counted.** `accept()` is the only writer in the module; callers at the pin are the issuing Lambda and the test file `ops/tests/test_owned_requests.py:57` (record `ACCEPT_CALLERS.txt`); the status Lambda calls none. The status role's grant on the requests table is NOT changed `[declared in source, the live role policy not read: the apply order's R0 prints it]`.

## 3. Apply protocol, in this order

0. Both halves at HEAD naming this file's blob. Open the ledger; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming `irpt-status`, its role or its key is a STOP). Apply outside the weekday 11:30Z-14:15Z band.
1. **R0, before-reads.** `get-function irpt-status` CodeSha256 equals `+TcZDWmwE7uv3sUwos2+jn1lbKyQikK+13nNBzD6q4A=`; the key's latest S3 VersionId, downloaded and hashed, equals it (record the VersionId: the rollback source; the r35l ledger then-latest was `vP3Bt0tM_n0qEa17Nf_VA0ZtXjwMt4GX`, R0 must record the CURRENT latest); the credential-less refusal envelope (status, body sha256); one retained READY report read (status, body sha256).
2. **U, build and upload.** Throwaway worktree detached at the pin, `BUILD_ONLY=1`: the printed CodeSha256 must equal the table (any other: ABORT, nothing uploaded); then the same build without `BUILD_ONLY` (one new object version); read back (sha256 equals the zip's). `MSYS_NO_PATHCONV` unset; a private TMPDIR.
3. **C, scoped plan.** Root `infra/aws/terraform/investor-reporting/ops`, `-target=module.irpt_status.aws_lambda_function.this`: `Plan: 0 to add, 1 to change, 0 to destroy`, attributes `last_modified`, `s3_object_version`, `source_code_hash` only. Anything else: STOP, nothing applied.
4. **A, apply** with `safe-apply` on the saved plan; never `aws lambda update-function-code`.
5. **V, after-reads.** G1 CodeSha256 equals the table; G2 live object vs the previous version differs in exactly `acceptance.py` (denominator 49); G3 the refusal envelope equals R0's; G4 the READY report read of R0 returns the same status and body; G5 the commentary route returns 200 with a body for one synthetic request that has a retained commentary ref (record the request id, status, body sha256); G6 `release-census.py` against the live zip prints `changed_members=0`.
6. **Map record and close** in the applier's worktree (`artifact_*` and `last_deployed_*` of the `irpt-status` entry); close the ledger.

## 4. Rollback, per key

Copy the previous S3 VersionId (recorded at R0) onto the key, the scoped plan, `safe-apply`, read `+TcZDWmwE7uv3sUwos2+jn1lbKyQikK+13nNBzD6q4A=` back. Nothing else moves, so nothing else is rolled back.

## 5. Not claimed

- That the live zip is unchanged since the issuer's read of 2026-10-17 (R0 proves it).
- That the status role cannot write the requests table (the code never calls the writer; the live policy is not read here).
- That `irpt-commentary-draft-store-lambda.json` is current: it still stages `acceptance.py` at pin `283f7e7700` (row W291-S2, a separate function, not moved here).
- That a real ticket's commentary PDF opens end to end (G5 is one synthetic request; Andrew's ticket read-back is separate).

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-17, on this packet's bytes at the commit that carries it. The write set: one Lambda code object (one S3 object version) and its function configuration. The blast radius is section 2; the rollback is section 4.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
