# NEVER-WIDEN ASK -- NFRA_MCPORTAL `MP-pd-7`, the grant-writer Lambda's code, deployed from source through Terraform (Act A only)

- **Asked by:** `0.7.0_AE_CloudOps~NFRA1`
- **Halves asked of:** `1.0.0_SA_CTO~Z` (CTO half) and `2.0.0_SA_COO~MP` (COO half)
- **Order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-pd-7.person-access-release.md` (AMENDMENT A2); GO: `.../deliverables/2.0.0_SA_COO~MP/pd/GO_MP-pd-7.md` (`LIVE_BASE` `13917ef993207bee6b8df0124eec5444da4d62cd`, `LAMBDA_COMMIT` `f3774ac1df8`, deadline 2026-10-21T05:30:00Z)
- **The act:** one `safe-apply` of one targeted plan on `aws_lambda_function.mcportal_grant_writer` (`mcportal-grant-writer-lambda`), in place. No gateway release, no IAM, no store write.
- **Measured:** `2026-10-20T19:56:24Z` (records `W/MP-pd-7_MEASURE.json`, `W/MP-pd-7_INVOKE_BEFORE.json`, `W/mp_pd7_measure.py`; `W` = `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~NFRA1/`)

## 1. BLAST RADIUS -- what this act may touch

ONE thing: the function's code package. The plan (targeted, `-lock=false`, no `-out`, nothing applied) reads **`Plan: 0 to add, 1 to change, 0 to destroy.`**; the one in-place update changes `source_code_hash` `894RI63/G4h019yxAGP7E+wQzrpZIfJoMaLhzpTTyck=` -> `RUGwtI9t8UKV8VpyCeArffZFwHeuUm4QhOIJU+nAJjg=` (and `last_modified`, known after apply) and nothing else.
- Read at the act, twice: `services.opal-gateway.deployed_commit` is `LIVE_BASE` at both reads (first read 13917ef993, second 13917ef993: stable and equal to the GO's: True). A different value at the act STOPS it.
- The package is built by the Lambda's own `build_package.py` through the Terraform `data "external"` and `archive_file` (no Terraform logic changes); the Lambda directory is byte-equal to `LAMBDA_COMMIT` (`git diff --quiet f3774ac1df8 HEAD -- <dir>` reads equal: True).

## 2. WHAT IT MAY NEVER TOUCH

The function's role and its policies, its environment, the owner-key variable and secret, the layer (version 1 stays), the changes table, the gateway (no release, no restart), the tool surface, the Lambda's memory, timeout or handler, and any other resource. The plan above shows none of them; any plan that shows more than the one resource STOPS the act.

## 3. CENSUS -- the package, measured

| | deployed now | the new package |
|---|---|---|
| CodeSha256 / source_code_hash | `894RI63/G4h019yxAGP7E+wQzrpZIfJoMaLhzpTTyck=` (LastModified 2026-10-11T20:32:52.000+0000) | `RUGwtI9t8UKV8VpyCeArffZFwHeuUm4QhOIJU+nAJjg=` |
| zip members | 11 | 65 |
| `lambda_function.py` holds `WIDEN-NO-CONFIRM` / `widening_signoff` | False / False | True / True |
| `lambda_function.py` holds `set_person_access` | False | true |

**Declared departure (1 of 2): the package GROWS from 11 to 65 members.** The closure is DERIVED by `build_package.py` (an `ast` walk of `app.access_state` and `ops.schwab_entitlement_admin`, every `import` including lazy ones) at the LIVE gateway release `13917ef993`, not at the release the deployed package was built from. Against the deployed zip: 54 members are new, 6 differ and 5 are equal. The differing members are:
  - `infra/aws/ec2/opal-gateway/app/access_state.py`
  - `infra/aws/ec2/opal-gateway/app/config.py`
  - `infra/aws/ec2/opal-gateway/app/data_entitlement.py`
  - `infra/aws/ec2/opal-gateway/app/graphql_plumbing/catalog_gate.py`
  - `lambda_function.py`
  - `org/standards/NFRA_OPLGTW_CONTRACT.json`

I probed the import side, because the layer holds only PyJWT and cryptography (boto3 is in the runtime): the new package's `lambda_function` imports and runs a no-header event with every top-level module outside {stdlib, boto3, botocore, jwt, cryptography} BLOCKED (the 64 `.py` members include modules that import `mcp`, `msal`, `httpx`, `pyarrow`, `starlette`, `pypdf` and `yaml`, but none is reached at import or on the handler's path; the deployed old package passes the same probe). This is a probe on this device, not the Lambda: the real proof is the post-apply invoke, and a failure of it is the rollback trigger in section 7.

## 4. THE BUILD COMPARISON

The new package's members, built twice from the same inputs, are recorded by short md5 in `W/MP-pd-7_MEASURE.json`'s source build and are compared after the apply with the deployed zip's members (the code zip downloaded from the presigned URL `get-function` returns, on Opal's own plane): the md5 of every member must equal the package built here (AC2).

## 5. ROLLBACK -- a declared departure (2 of 2), for both halves to accept or refuse

The order asks for a rollback "proven before the act by a rebuild compared by md5 per member against the deployed package, with a negative control". **That proof cannot be given as written.** The previous handler is `30d9b99758d` (its `lambda_function.py` equals the deployed one byte for byte). Rebuilt from that commit against the SAME live release (`13917ef993`) the package has 65 members: against the deployed zip 54 are new, 5 differ and 6 are equal. It is NOT the deployed package, because the closure is derived from the live release and the live release moved after the deployed package was built. The negative control reads as it should (the NEW package differs from the deployed one: True).
What the rollback therefore is: `safe-apply` of the old handler (`30d9b99758d`'s `lambda_function.py`) with the current closure: the previous BEHAVIOUR on the current closure, not the previous bytes. The deployed zip's own bytes are held (the download, sha256 prefix `f3de1123adff1b88`, 57638 bytes) in the scratch folder but cannot be re-applied through `safe-apply` without a Terraform change, which the order forbids. The rollback's time is measured as the build time plus the apply time of this act (the same two steps in the other direction); I record which and the seconds in the close report.
If either half wants the literal-bytes rollback instead, the act waits for a ruling on how (a Terraform change is outside this order).

## 6. THE READ-BACKS AND THE INVOKES

- **Before (measured now, 2026-10-20T20:04:11Z):** one no-header invoke of each action: `narrow` answers `REFUSED NO-OWNER-HEADER` (`record` PUT) and `set_person_access` answers `REFUSED NO-OWNER-HEADER` (`record` PUT). **Each refused invoke writes ONE append-only record to the writer's own changes table** (`record: PUT`): that is the function's existing behaviour for a refused outcome, not a store write of this act; the after-invokes write two more.
- **After the apply:** the same two no-header invokes must BOTH answer `REFUSED NO-OWNER-HEADER` (AC2); the function's code zip, downloaded, holds `WIDEN-NO-CONFIRM` and `widening_signoff` in `lambda_function.py`, and every member's md5 equals the package built here; `GW_LAMBDA_SHA256` (the function's `CodeSha256` after the act) goes in the close report on a line of its own.
- **Semantic change, named:** `set_person_access` becomes writable when a route reaches it, and a change that adds an entry to `tools_allow` or `channels_allow` needs the verified owner's `widening_confirm` exactly `true` (otherwise `WIDEN-NO-CONFIRM`; a confirmed widening writes `widening_signoff`). **Nothing reaches the action until the gateway mounts its route (not this order).** No `person_access` record is written by this act.

## 7. FAILURE BRANCHES, IN WORDS BOTH HALVES REPEAT

Roll back AT ONCE if the post-apply no-header invoke of any action stops answering `REFUSED NO-OWNER-HEADER`, or if the plan at the apply shows more than the one resource. Otherwise a miss in the deployed-bytes read alone is graded FAIL as measured, a row is opened, and the issuer (`2.0.0_SA_COO~MP`) decides. A refused half STOPS the act. If the act has not closed by 2026-10-21T05:30Z it does not start (or stops at a clean state): `OG-rl-17`'s window at 06:00Z takes precedence.

## 8. Gate lines

process-wide state this change touches: none in this repo's processes (one Lambda function's code package; no logger, signal, environment or global config of the gateway), read. I read `mcportal_grant_writer.tf`, `build_gw_stage.py`, `build_package.py`, the Lambda directory's history and the deployed package. No account number, ARN or token appears here.

## 9. The two halves (sign ONCE, on this ask's sha256)

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed on this ask's sha256 with the package growth (section 3) and the rollback departure (section 5) read.

### COO half (`2.0.0_SA_COO~MP`)

To be signed on this ask's sha256 with the plan (section 1), the invokes (section 6) and the failure branches (section 7) read.
