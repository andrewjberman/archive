# Never-widen sign-off packet -- r37 Lambda leg: irpt-status packages the two PDF-route fixes (commentary route binds by logical id; Overview route resolves the retained Opal PDF), at pin 474f174e89

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~Y2`, 2026-10-20. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane). **Ledger:** `irpt-status-r37-20261020`.
**Authority:** CTO msgs 11508 and 11512 (fix the commentary route and, where `opal_artifact` suffices, the Overview route, in one irpt-status code release under a pair) and msg 11516 (Andrew is at the desk: this packet is the critical path). Grounding: runs 7b and 7c stopped at the route read (rows S231, S233, W345-S1). **Scope:** ONE Lambda code release (`irpt-status`). No IAM, route, queue, table, secret, schema or resident host moves. No vendor call. The role's read of the Opal report family was applied earlier (ledger `irpt-status-opal-report-read-20261020`, CLOSED).

## 1. What ships

Pin `474f174e89407c62cec422870cb63cb47eff2e43` (trunk, box/dell2; carries AR-y-470 `d6fcee63650`, drained `d8497f8adc5`, and AR-y-472 `9caa35f08a6`, drained `06cb0e999d7`). `owned_report.py` is packaged from the source dir `infra/aws/lambda/investor-reporting/ops` (function map `infra/aws/lambda/ci/function-map/irpt-status.json`); NO map edit. Built twice, byte-identical, by worker `0.9.0_WK_IRPT_ANLREQ~348` (record `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~348/r51/R37_BUILD.json`); the issuer re-ran `live_diff.py` against the issuer's own fresh record of the live zip (`LIVE_IRPT_STATUS_MEMBERS_20261020.json`, downloaded by `aws lambda get-function` Code.Location and hashed member by member): `LIVE-DIFF-OK moved=1 added=0 removed=0 same=48 mover=owned_report.py has_commentary_fix=yes has_overview_fallback=yes`, and `--selftest` `CONTROL-FIRES`; the issuer hashed the stage zip itself.

| function | zip sha256 | CodeSha256 | bytes | members | changed vs the live package |
|---|---|---|---|---|---|
| `irpt-status` | `078474759a814617259902ce8811e9dc5b7fc0d6cca263598547e508245f1321` | `B4R0dZqBRhclmQLOiBHp3Ft/wNbMomNZhUflCCRfEyE=` | 369411 | 49 | 1 |

| member | live sha256 (12) | built sha256 (12) | attribution |
|---|---|---|---|
| `owned_report.py` | see the live record | `0efb3b154f01` (equals the blob at `06cb0e999d7`) | 2 commits since the live build: `d6fcee63650` (AR-y-470: `commentary_pdf` binds by logical id and signs the retained PDF's own sha256 instead of comparing it with the draft's), `9caa35f08a6` (AR-y-472: `pdf` resolves the retained Opal Overview PDF through the artifact binding when `release.protected_pdf_ref` is absent, bound to the report's own `opal_artifact.sha256`; the vendor path unchanged) |

The live package: CodeSha256 `274dl2bCd2VC3OcX4Uqc4AMbWep65B97F1+CVNoKfMc=`, 49 members, handler `status_installed.lambda_handler`, python3.12, LastModified 2026-10-17T16:41:08Z, 368788 bytes, zip sha256 `dbbe1d9766c27765...` (the r36s build). The other 48 members are identical to it.

## 2. Blast radius (read from the code at the pin)

| what the status Lambda answers for | BEFORE | AFTER |
|---|---|---|
| `GET analysis/requests/{id}/commentary-pdf` | refuses `COMMENTARY_PDF_BINDING` for every request (the PDF's sha is compared with the draft's, never equal) | answers a signed link for the retained commentary PDF of the viewer's own request, signed with the PDF's own sha256; the logical-id binding and the repository's owner, tenant and retention checks still apply; wrong family, zero length or non-hex sha still refuse |
| `GET analysis/requests/{id}/pdf` for an Opal report | refuses `ANALYSIS_PDF_NOT_RETAINED` for every real Opal report (the producer writes no `protected_pdf_ref`) | answers a signed link for the retained Overview PDF, bound to the report's own `opal_artifact.sha256`; a differing sha refuses `ANALYSIS_PDF_BINDING` |
| `pdf` for a vendor report or a report that carries `protected_pdf_ref` | as today | the SAME (that branch is untouched; the existing tests of it pass) |
| the status envelope, every other route, role, table, key | as today | as today |

**Who gains:** the viewers who may already read a request's report through these routes, after the route's existing re-authorization (`_materialize` before, `_final` after the artifact read). No new principal class, no new route. The role's read of the Opal report family was granted earlier; this release makes the routes use it. **Writers counted:** none; both methods read only. The status role's grants are NOT changed.

## 3. Apply protocol, in this order

0. Both halves at HEAD naming this file's blob. Open the ledger; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming `irpt-status`, its role or its key `investor-reporting/irpt-status.zip` is a STOP). Apply outside the weekday 11:30Z-14:15Z band; never alongside another IB2 act.
1. **R0, before-reads.** `get-function irpt-status` CodeSha256 equals `274dl2bCd2VC3OcX4Uqc4AMbWep65B97F1+CVNoKfMc=`; the key's whole version listing (never a paged length query): record the CURRENT latest VersionId, download that object and hash it: it must equal the CodeSha256 (this is the rollback source); the credential-less refusal envelope (status, body sha256); one retained READY report read (status, body sha256) as the synthetic internal viewer of TO-EXERCISE-R28b if one can be minted, else say NOT MADE. Any other live state: STOP (someone released; the issuer rebuilds).
2. **MEMBER DIFF.** `python infra/aws/lambda/ci/release-census.py irpt-status --pin 474f174e89407c62cec422870cb63cb47eff2e43` (read its `--help`): `changed_members=1` (`owned_report.py`), denominator 49. Any other member: STOP.
3. **U, build and upload.** A throwaway worktree OUTSIDE the product tree, DETACHED at the pin; `git show 474f174e89407c62cec422870cb63cb47eff2e43:infra/aws/lambda/ci/build-and-upload.sh | grep -c BUILD_ONLY` at least 1; `MSYS_NO_PATHCONV` UNSET (print that); a private TMPDIR; `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-status`: the printed CodeSha256 must equal `B4R0dZqBRhclmQLOiBHp3Ft/wNbMomNZhUflCCRfEyE=` (any other: ABORT before any upload); `git status --porcelain` shows nothing; then the same build WITHOUT `BUILD_ONLY` (one new object version, the new LATEST); read the object back (its sha256 equals the zip sha256 in section 1).
4. **C, scoped plan.** Root `infra/aws/terraform/investor-reporting/ops`, `-target=module.irpt_status.aws_lambda_function.this`: `Plan: 0 to add, 1 to change, 0 to destroy`, the changed attributes `last_modified`, `s3_object_version`, `source_code_hash` only. Anything else: STOP, nothing applied (after the upload: the rollback of section 4). **A, apply** with `.tools/safe-apply.sh` on the saved plan; never `aws lambda update-function-code`.
5. **V, after-reads.** G1 CodeSha256 equals `B4R0dZqBRhclmQLOiBHp3Ft/wNbMomNZhUflCCRfEyE=`. G2 the live object against the R0 download, member by member: exactly `owned_report.py` differs, nothing added or removed (print the list; denominator 49 of 49). G3 the credential-less refusal envelope equals R0's. G4 the READY report read of R0 again returns the same status and a byte-identical body (if R0 made one). G5 a commentary-route or Overview-route read for a synthetic request that holds a retained artifact: made only if such a request exists at R0 (the earlier runs' rows were deleted at their cleanup, so it is expected NOT MADE: the live proof of this release is run 7d, which follows it); record `S5 NOT MADE <why>` if so. G6 `release-census.py irpt-status` against the live zip prints `changed_members=0`.
6. **Record and close** the ledger; update the function map's deploy fields in the applier's worktree as the r36s order did; report once.

## 4. Rollback, per key

Copy the previous S3 VersionId (recorded at R0) onto the key, the scoped plan, `safe-apply`, read `274dl2bCd2VC3OcX4Uqc4AMbWep65B97F1+CVNoKfMc=` back. Nothing else moves, so nothing else is rolled back. The routes then refuse as today.

## 5. Not claimed

- That a real request's reports open end to end: run 7d is that proof, after the apply. A second defect behind these two (for example the signer refusing the Opal family) would be a new row.
- That the retained Overview artifact of a real request carries the logical id the route derives (`<request_id>-overview-<sha256>`, read from the producer at `opal_producer.py:686`; not measured live).
- That the live zip is unchanged since the issuer's read of 2026-10-20 ~20:2xZ (R0 proves it).
- That the two sibling test files that changed on trunk after the pin (`reports/tests/test_compare_ports.py`, `test_resident_installed.py`) matter: they are not package members.

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-20, on this packet's bytes at the commit that carries it. The write set: one Lambda code object (one S3 object version) and its function configuration. The blast radius is section 2; the rollback is section 4.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
