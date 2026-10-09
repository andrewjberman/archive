# irpt-ycharts-generate RELEASE 6b -- never-widen pair DRAFT (the custody-factory grant, plus IRPT_ANLREQ's ticket binding)

**Deployer:** `2.0.0_SA_COO~Y2`. **Applier:** `0.7.0_AE_CloudOps~DELL2`.

**Supersedes** release 6 (`NEVER_WIDEN_PAIR_RELEASE6_CUSTODY.md`, blob a3c54ba263; CTO half @96e03f8ba1), on the CTO's ruling, msg 2833:
- Release 6's signed `V6EiBNcJ...` predates IB-pr-390's `served.py` (74a62fb46c). Applying it would revert ALL-never-admits and the
  profile narrowing.
- IB-pr-390 (CTO half @b97ebb6b98) went live at 07:49Z as `ZA0QJ5Wt...`. It already carries release 6's custody CODE and the AWSSDKPandas
  layer, but NOT the custody-factory policy.

DRAFT: no half signed.

## 1. Pin and artifact

- **Pin:** box/dell2 `66207bce7d`, ON origin (fetched read).
- **Built** (BUILD_ONLY in a detached worktree at the pin, this seat): `tdpterTMfJlWXjnoAQCwil+wN/Jf8Q/yLjGxTk7yUkk=`. A HEAD build at
  `8efbba1e21` gives the same value.
- **Live now / ROLLBACK:** `ZA0QJ5Wt/7JcwmuzVfHOeNAdFk6th4H5IEeqQStDYm8=` (IB-pr-390), S3 version `8rOI5aDff8mlWQQ6YNVy7Is11Pfh8jcn`.
- **Layers live:** `irpt-common:5` + `AWSSDKPandas-Python312:16`, which is generate.tf's declared state, so no layer diff.

## 2. Gates, at the pin

| gate | reading |
|---|---|
| census against LIVE | `changed_members=3`: `acceptance.py`, `submission.py`, `contracts/AnalysisSubmissionRequest.schema.json`. All three are IRPT_ANLREQ `AR-y-11` (+ AMENDMENT 1), drained @3ad7526e06 and staged by `AR-y-21` @3895b80dae |
| `checks/r73/cochange_closure.py` | `split=0` (88 rows) |
| `checks/r71/symbol_closure.py` on the BUILT zip | `modules=66 pairs=299 missing=0`, PASS; build import-closure OK, 67 files |

## 3. What moves

| member or resource | carries | owner's confirmation |
|---|---|---|
| `submission.py`, `acceptance.py` | `ticket_id`, optional, admitted only with an `input_id` basis, persisted on the acceptance record; the queue message is unchanged | ~Y2 (own cell) |
| `contracts/AnalysisSubmissionRequest.schema.json` | optional `ticket_id`, pattern `^TCK-[0-9]{8}-[0-9a-f]{8}$`, v1 additive | ~Y2 (own cell) |
| `aws_iam_role_policy.generate_custody_factory` | ADDED, the same 3 statements and 11 ARNs as release 6's section 3, unchanged | release 6 CTO half @96e03f8ba1 printed them beside their owners' read sets |

Plan-only (this seat, at HEAD before the upload): **1 to add, 0 to change, 0 to destroy**, the policy only. After the applier uploads
`tdpterTM...`, the targeted plan also shows the function's `s3_object_version` + `source_code_hash`, and nothing else. Any other attribute
is a STOP.

**Widens:** one role gains 3 statements over 11 ARNs, as release 6 declared. One request field becomes optional.
**Does not move:** IB-pr-390's `served.py` (equal at the pin), every other member, the layers, every other function and policy.

## 4. After-reads (order fixed)

0. Live at start is `ZA0QJ5Wt...`; otherwise STOP.
1. The symbol closure on the UPLOADED zip (downloaded back by version) reads `missing=0`, or STOP before the apply.
2. After apply:
   - live == `tdpterTM...`;
   - the policy reads back with exactly the 11 ARNs;
   - re-plan 0;
   - import census `failed: {}`, which gates the rest.
3. **The custody path:** one cottonwood statement submission (no `input_id`) shows no `CUSTODY_FACTORY_REQUIRED`, no ImportError and
   no AccessDenied on the 11 ARNs. Quote the outcome line; list every `custody_reports` object version it writes.
4. **The prospect path holds:** one `input_id` submission reaches the prospect factory.
5. **The ticket binding (AR-y-11, live):** one `input_id` submission with a valid `ticket_id` is accepted, and its acceptance record
   carries the same `ticket_id`. One with a malformed `ticket_id` refuses `TICKET_REFERENCE`.
6. **Cleanup:** read 3's objects. Andrew's word is recorded @35fabf20c8 (row e6a4, the `read3_objects` list), deleted once graded.
   Reads 4 and 5 store prospect records; their keys are listed, and their S3 deletes wait on Andrew's word (section 5).

**Branch B:** any of 0-2, 4 or 5 fails, or read 3 raises CUSTODY_FACTORY_REQUIRED, ImportError or AccessDenied:
- re-promote `8rOI5aDf` the same session;
- remove the policy (a targeted revert apply);
- then cleanup, then a BLOCKING row.
Read the failing call's CloudWatch line before halting.

## 5. Owed before signing

- The CTO half.
- Andrew's word on the S3 deletes of reads 4 and 5 (their synthetic prospect objects, named by key and version in the after-reads file). It is
  NOT covered by @35fabf20c8, which names read 3's list only; the issuer queues it as an open call once the keys exist.
