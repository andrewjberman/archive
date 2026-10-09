# IRPT_ANLREQ release 1 -- irpt-status + one API route -- never-widen pair DRAFT (the ticket binding read side, and the original-file reader)

**Deployer:** `2.0.0_SA_COO~Y2`. **Applier:** `0.7.0_AE_CloudOps~DELL2`.

**Source:** the CTO round-1 analysis, release 1 (msg 2770), and ADDENDUM 1 (@64e9e6157d). The cells are:
- `AR-y-11` (+ AMENDMENT 1), drained @3ad7526e06;
- `AR-y-21`, the staged rows, @3895b80dae and @3a6d021e4a;
- `AR-y-22`, the original-file reader, @75650bef27.

`irpt-ycharts-generate`'s half of this work rides release 6b (`TO-APPLY-Y77`).

DRAFT: no half signed.

## 1. Pin and artifact

- **Pin:** box/dell2 `3a6d021e4a`. LOCAL when drafted; it must be on origin before the apply.
- **Built** (BUILD_ONLY at HEAD = pin, this seat): `WTGCJPiSEWSack1XvAMRyTGSVLX84VSm+3eC3eSPgsQ=`. Import-closure OK, 38 files.
- **Live now / ROLLBACK:** `E7VKvhg3E9D5euWO+S649/iyAJ05xUmFPqHEAKDTFxA=`, LastModified 07:43:46Z. That is IB-pr-395's release of IB-pr-390's
  `served.py` on this host. The applier records the current S3 version at step 0 as the rollback source.

## 2. Gates at the pin

| gate | reading |
|---|---|
| census against LIVE (`release-census.py irpt-status --pin HEAD`) | `changed_members=5`: `acceptance.py`, `submission.py` (AR-y-11), `entry.py`, `owned_report.py`, `pdf_link.py` (AR-y-22). No other lane's member rides |
| `checks/r73/cochange_closure.py irpt-status` | `split=0` (42 rows) |
| `checks/r71/symbol_closure.py` on the BUILT zip | `modules=37 pairs=115 missing=0`, PASS |

## 3. Terraform, plan-only (this seat)

| root | target | reading |
|---|---|---|
| `investor-reporting/ops` | `module.irpt_status` | No changes before the upload. After the upload: the function's `s3_object_version` + `source_code_hash` only |
| `investor-reporting/api` | untargeted | `1 to add`: `aws_apigatewayv2_route.irpt["GET /api/scoped/investor-reporting/analysis/requests/{requestId}/original"]` (the carrier `docs/contracts/investor-reporting/v1/routes.json`, under the existing authorizer and integration). Nothing else |

**Widens:**
- one GET route, behind the existing authorizer;
- one reader, which signs a link to the caller's OWN request's original upload, re-authorized per request; another firm is refused;
- the signer admits exactly two more families (`ORIGINAL_HOLDINGS`, `ORIGINAL_CSV`), each bound to `reporting_destination`;
- one optional request field read back (`ticket_id`).

**Does not move:**
- IAM: the role's family list already holds both originals (`ops/iam.tf:85`);
- every other route and function;
- the PDF route, whose signer default family is unchanged.

## 4. After-reads (order fixed)

0. Live at start is `E7VKvhg3...`; otherwise STOP. Record the current S3 version as the rollback source.
1. The symbol closure on the UPLOADED zip (downloaded back by version) reads `missing=0`, or STOP before the apply.
2. After both applies:
   - live == `WTGCJPiS...`;
   - both re-plans read 0;
   - the route lists in `get-routes`;
   - an existing route (`GET .../analysis/requests`) for the test filer still answers 200.
3. **The original reader**, on ONE template-lane request owned by the test filer (6b's read 5 request, or one fresh template upload as Y75
   read 4):
   - the owner receives a signed link whose sha256 equals the retained original's;
   - a viewer at ANOTHER firm is refused;
   - a custody-lane request refuses `ANALYSIS_ORIGINAL_NOT_APPLICABLE`.
4. **The ticket binding, read side:** `GET .../analysis/requests/{id}?include=composition` for a ticketed request returns the composition with
   its `ticket_id`, and the response meets `OwnedAnalysisRequest`.
5. **The PDF route holds:** `analysis-request-pdf` for an existing READY request still signs, or still refuses by its same name if none is
   retained.
6. **Cleanup:** any record or object made only for read 3 is listed by key and version. Its S3 deletes wait on Andrew's word.

**Branch B:** any of 0-2 or 5 fails, or read 3 or 4 fails:
- re-promote the step-0 version the same session;
- remove the route (a targeted revert of the `routes.json` entry, then apply);
- then cleanup, then a BLOCKING row.
Read the failing call's CloudWatch line before halting.

## 5. Owed before signing

- The CTO half.
- Pin `3a6d021e4a` on origin.
