# Never-widen sign-off packet -- r37 Lambda leg: irpt-ycharts-generate (the upload door) takes the O1 owner-resolution change, at pin bd1894d789

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~Y2`, 2026-10-20. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane).
**Authority:** PRD IRPT_ANLREQ v0.24 O1 (an Opal staff user is never refused: C-FIRM); the earlier O1 hunk design `O1_OWNER_RESOLUTION_HUNK_FOR_P2_REVIEW_20261019.md` (typed exception, reviewed by `~P2`). **Ledger:** `irpt-ycdgen-o1-r37-20261020`.
**Scope:** ONE Lambda code release (`irpt-ycharts-generate`, the Analysis Request upload door). No IAM, route, queue, table, secret, schema or resident host moves. No vendor call. The other eight Lambdas that stage `_authz/served.py` do NOT move.

## 1. What ships

Pin `bd1894d789f5196bbc48dc00b081d10c9cc03610` (the map edit: `infra/aws/lambda/ci/function-map/irpt-ycharts-generate.json`, numstat 2 2; `_authz/served.py` staged-from pin `564e604838` -> `720e125d31469ed60b6e698812c7be731bd6d8e8`, sha256 `600a934c4b34da1e14ec8b7d4de4a3f69cc55c331257dd90abb525def9929fcd`). Merged to `box/dell2` at `1f7fb64f3c2`. The pin `720e125d31` is a scratch commit (`scratch/o1-served-pin`): HEAD with `served.py` held at the LIVE blob `30c0eb88ec38` plus ONLY the O1 hunks. The newer DASHBD change `a3058c274c` (the FORWARD_FUNCTION_ENV port) is NOT carried. Built twice, byte-identical, by worker `0.9.0_WK_IRPT_ANLREQ~314` (record `0.9.0_WK_IRPT_ANLREQ~314/r37/R37_BUILD.json`). The issuer re-measured the zip: sha256 and CodeSha256 below, 107 members, and `served.py` inside it hashes `600a934c4b34`, the pin's blob.

| function | zip sha256 | CodeSha256 | bytes | members | changed vs the live package |
|---|---|---|---|---|---|
| `irpt-ycharts-generate` | `51dc323cd354cf19e6fe7167b5874af1ca3ae609e692b14ca47db15569b0529c` | `UdwyPNNUzxnm/nFntYdK8co65gnmkrFMpH2xVWmwUpw=` | 639139 | 107 | 1 |

| member | live sha256 (12) | built sha256 (12) | attribution |
|---|---|---|---|
| `_authz/served.py` (packaged as `served.py`) | `30c0eb88ec38` | `600a934c4b34` | AR-y-415 (O1): +26 / -13 lines in `_create_owner`, `_advisor_owner`, one new class `AdvisorUnprovisioned` and its import |

The live package: CodeSha256 `kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE=`, 107 members, handler `generate_installed.lambda_handler`, python3.12 (record `LIVE_IRPT_YCDGEN_MEMBERS_20261020.json`). The worker's checker printed `R37-DIFF-OK moved=1 added=0 removed=0 same=106`, `R37-IDENTITY-OK builds_identical=yes import_served=ok import_generate_installed=ok`, `R37-MAP-OK numstat=2/2` (records `DIFF.txt`, `IDENTITY.txt`, `MAP.txt` beside the build record).

## 2. Blast radius (read from the code at the pin)

| the door answers an on-behalf upload for | BEFORE | AFTER |
|---|---|---|
| an Opal staff filer, no advisor named, whose profile LISTS the tenant | refused `NOT_AUTHORIZED` ("must name the firm advisor") | the owner is `access.prospect_owner()` (the filer's own); stored |
| an Opal staff filer, no advisor named, tenant not listed | `access.prospect_owner()` | the SAME |
| an advisor named and provisioned (partner profile and active user row at the firm) | the advisor's owner through `resolve_prospect_owner` | the SAME |
| an advisor named, NO partner profile at the firm, or user row absent / disabled / of another firm | refused | `access.prospect_owner()`; the typed email is dropped, never authority |
| an advisor named with a partner email or firm MISMATCH, or a user-row email mismatch | refused | refused (plain `ProspectOwnershipRefused`) |
| unreadable query, a firm that is not a registered client firm, profile reads raising, `prospect_owner()` unresolvable | refused | refused |
| any other route, role, table, key | unchanged | unchanged |

**Who gains: no principal class.** The staff-only reach is decided before this code (`uploads.py`'s rule on whether the filer may act for the firm is UNCHANGED); this change decides only WHOSE name the stored request carries. The owner still comes only from a verified identity (`prospect_owner()` or `resolve_prospect_owner`), never from a request value. **Writers counted.** `_create_owner` has one caller at the pin, the guard's on-behalf create path; `_advisor_owner` has one, `_create_owner`; `AdvisorUnprovisioned` subclasses the refusal, so any other catcher still fails closed. Tests: `_authz` 375 passed (the pinned `test_served_on_behalf_create.py` updated for the new rule, `test_create_owner_on_behalf.py` 9 new). `[declared in source and tests; the live profile rows are not read here]`

## 3. Apply protocol, in this order

0. Both halves at HEAD naming this file's blob. Open the ledger; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming `irpt-ycharts-generate`, its role or its key is a STOP). Apply outside the weekday 11:30Z-14:15Z band, outside 05:45Z-07:00Z on Tuesday 2026-10-20, and never alongside run 5 or TV2's TO-R20-REL2 or another IB2 act.
1. **R0, before-reads.** `get-function irpt-ycharts-generate` CodeSha256 equals `kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE=`; the key's latest S3 VersionId, downloaded and hashed, equals it (record the VersionId: the rollback source); the credential-less refusal envelope (status, body sha256).
2. **U, build and upload.** Throwaway worktree detached at the pin, `BUILD_ONLY=1`: the printed CodeSha256 must equal the table (any other: ABORT, nothing uploaded); then the same build without `BUILD_ONLY` (one new object version); read back (sha256 equals the zip's). `MSYS_NO_PATHCONV` unset; a private TMPDIR.
3. **C, scoped plan.** Root `infra/aws/terraform/investor-reporting/ycharts` (the module is declared at `generate.tf:377`; if the applier's R0 finds the root differs, STOP and say so), `-target=module.irpt_ycharts_generate.aws_lambda_function.this`: `Plan: 0 to add, 1 to change, 0 to destroy`, attributes `last_modified`, `s3_object_version`, `source_code_hash` only. Anything else: STOP, nothing applied.
4. **A, apply** with `safe-apply` on the saved plan; never `aws lambda update-function-code`.
5. **V, after-reads.** G1 CodeSha256 equals the table; G2 live object vs the previous version differs in exactly `served.py` (denominator 107); G3 the refusal envelope equals R0's; G4 `release-census.py` against the live zip prints `changed_members=0`. The behaviour proof is run 5 (staff upload with an unprovisioned advisor and with none), not this apply.
6. **Map record and close** in the applier's worktree (`artifact_*` and `last_deployed_*` of the `irpt-ycharts-generate` entry); close the ledger.

## 4. Order of release with the portal

This backend change is safe alone: a portal that still sends `advisor_email` gets the same answers, and a portal that stops sending it is only served after this lands. The portal half (row `ba68` and its PROD promote) ships in the SAME release as this one; this Lambda goes FIRST.

## 5. Rollback, per key

Copy the previous S3 VersionId (recorded at R0) onto the key, the scoped plan, `safe-apply`, read `kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE=` back. Nothing else moves, so nothing else is rolled back.

## 6. Not claimed

- That the live zip is unchanged since the issuer's read of 2026-10-20 (R0 proves it).
- That the six other function-map files that still name the old `served.py` sha are current (worker row `IRPT_ANLREQ-D2-W314-S1`, reported, not edited; those Lambdas are not moved here).
- That a real staff upload for an unprovisioned advisor succeeds end to end (run 5 proves it; this apply does not).
- That the typed advisor email is kept as attribution anywhere (it is dropped; a separate contract if wanted).

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-20, on this packet's bytes at the commit that carries it. The write set: one Lambda code object (one S3 object version) and its function configuration. The blast radius is section 2; the rollback is section 5.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
