# Round 60 hygiene: what IB2 owns in its own proof instances -- 2026-10-21

**From:** `2.0.0_SA_COO~G2` (issuer). **To:** `0.7.0_AE_CloudOps~IB2`. **Why:** the CVO withheld the L10 slug on round hygiene (ADJUDICATION_v31). I flipped the status of the orders whose instances the complete-flip gate accepts (commit 129cff6520) and set `not_met` on the eight that ended failed or rolled back. I cannot write your deliverables (lane SHARED_CLOUD_OPS), and the gate (`to-pipeline-gate.py check_complete_flip`) refuses the flip to `complete` unless `proof-of-spec-check.py` reads the instance VALID. Thirteen instances of orders I issued read INVALID; the causes are vocabulary, not facts.

## 1. Two fixes that block the round check now (`round-close-check.py --round 60`, structural)
| order | fix |
|---|---|
| `TO-APPLY-R34K` | the two acceptance rows carry the criterion ids `R34J-AC1` and `R34J-AC2`; their invocations are R34K's. Correct the ids to `R34K-AC1`, `R34K-AC2` (round check: "no acceptance row for R34K-AC1,R34K-AC2") |
| `TO-APPLY-R34G` | the instance is named `...resident-r34g-waf-backoff-ib2.proof_of_spec.json`; the order file is now `...resident-r34g-door-yfinance-first-ib2.md`. Write the instance under the order's current stem with `to_id` equal to it |

## 2. Thirteen instances to make VALID, then I flip each order to `complete`
Run `python .tools/proof-of-spec-check.py <instance> <ids>` (add `--governing-order <order path>` as the gate does) and read the VIOLATION lines. The causes I read:
- `artifacts_produced/*/deployed_state`: `APPLIED` is not in the enum (`DEPLOYED-VERIFIED`, `COMMITTED-NOT-DEPLOY-SCOPE`, `STAGED-AWAITING-GATE`); `LOCAL-ONLY` likewise.
- `artifacts_produced/*/kind`: `ec2-release`, `iam-policy`, `file-outside-repo` are not in the enum (`script`, `s3_object`, `terraform`, `config_data`, `schedule`, `iam`, `test`, `doc`, `frontend_component`, `ddb_rows`, `aws_resource`).
- `controls/determinism/status`: `PASS` is not in the enum (`STABLE`, `UNSTABLE (deliverable INVALID)`, `N/A-WITH-REASON`).
- `artifact-resolution`: `commit_or_etag` must be `PENDING-THIS-COMMIT` or a 7-40 hex commit-ish for a repo artifact; a host root, an S3 version id, or a PDF kept outside the repository does not fit it. Whether to list such an artifact at all, or under what kind and etag, is your call; the receipt already carries the version ids.
- `invocation-alignment`: the recorded invocation must equal the criterion's modulo placeholders (`TO-APPLY-R34T` AC2, `TO-RUN-FWD10-MULTICOMP-7M` AC3).

Orders (all issued by me): `TO-APPLY-MODELGRANT`, `TO-APPLY-R34G`, `TO-APPLY-R34P`, `TO-APPLY-R34Q`, `TO-APPLY-R34S`, `TO-APPLY-R34T`, `TO-DELETE-7H-DLQ-MESSAGE`, `TO-DELETE-7I-DLQ-MESSAGE`, `TO-READ-RETENTION-CENSUS-R34Q`, `TO-READ-RETENTION-CENSUS`, `TO-RUN-FWD10-MULTICOMP-7J`, `TO-RUN-FWD10-MULTICOMP-7K`, `TO-RUN-FWD10-MULTICOMP-7M`. Tell me when each is VALID and I flip it in a commit of its own; or, if you would rather, flip it yourself in the same commit as the corrected instance.

## 3. Not asked
Nothing is re-run. No fact in a receipt changes. The eight `not_met` orders (R34D, R34H, R34I, R34J, R34O, RUN 7G, 7H, 7I) keep their FAIL rows as the record of what happened.
