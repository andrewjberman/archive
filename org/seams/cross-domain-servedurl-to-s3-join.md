# SEAM: ts_semantic ServedURL node  ->  cloud-graph S3 bucket node   (scale: MESO)
**archetype:** VALIDATE
**seam-slug:** cross-domain-servedurl-to-s3-join (NFRA_TSGRAPH P4)
**run:** 0.7.0_AE_CloudOps 2026-06-18T00:20Z (Andrew-directed /seams on most-recent work)

## Seam definition
- **Side A (source):** the ts_semantic `ServedURL` node (e.g. `endpointurl:/api/general/benchmarks/model_portfolio_benchmarks.json`, `props.url` = the clean path) -- emitted by the DE's ts-morph producer.
- **Side B (sink):** the cloud-graph S3 bucket node (e.g. `arn:aws:s3:::opal-data-portal-v2`) -- from the AWS-side derive.
- **The boundary:** the `SERVED_FROM` edge formed by `stitch_served_from()` (infra/aws/globgrph/derive_runner.py, committed DORMANT e1899add6). Resolution = the ground-truthed `/api/general/{X}` -> `opal-data-portal-v2/json/{X}` rule; both-ends-verify = `head_object` (source) + bucket-name->live-node_id lookup (target); props carry `s3_key`/`bucket`/`resolution`.
- **Expected contract:** a ServedURL resolves to its backing S3 object, co-keyed on the cloud-graph's ACTUAL s3 node_id, forming a SERVED_FROM edge ONLY if both ends are real (object exists + node exists) else VISIBLE-unresolved -- closing the portal->cloud fine-lineage leg (gold-field -> ServedURL -> render). Recorded: NFRA_TSGRAPH.P4 TO (COO), CTO accept-review 001440Z, RAVC 001238Z.

## Axis verdicts
| Axis | Verdict | Evidence | Delta (if FAIL) |
|---|---|---|---|
| MECHANICAL  | **FAIL (pre-live-land)** | derive task role `derive_runner_s3` (item2a.tf:60-103) grants s3:GetObject on ONLY `opal-313476888478-globgrph` + `terraform-state`; `opal-data-portal-v2` is in NO globgrph IAM policy. The derive runs as `derive_runner_task` (item2a.tf:297). So `head_object(opal-data-portal-v2,...)` -> AccessDenied(403) -> caught by `except Exception` -> ALL 29 /api/general/* edges fall to object-miss. Live SERVED_FROM count = 0 (also currently 0 = dormant, comp-kuzu). | the seam carries 0 edges at the live-land (silent no-op via 403), NOT the believed 29. + the head_object except conflates 403(IAM)/404(absent) -> mislabels the cause. |
| DECLARATIVE | PASS (with parity caveat) | code matches its docstring + the RAVC (both-ends-verify, co-key on the actual arn-form node_id, 29/4/12 coverage). The "29 keyed" was honestly labeled SCRATCH/live-pending. | parity gap to record: the docstring/RAVC omit the IAM PRECONDITION (the derive role needs opal-data-portal-v2 read). The scratch ran head_object under DEV-BOX creds, not the derive role -> env-mismatch (dump-vs-derive class). |
| SEMANTIC    | PASS (conditional on MECHANICAL) | the resolved object is correct + independently cross-checked: model_portfolio_benchmarks -> json/benchmarks/model_portfolio_benchmarks.json (== DE ground-truth), head-object 19256B (== DE's exact byte count). bucket-grain edge + object-key-in-props = CTO-accepted v1. | none on content; the gold->object SINGLE-traversal precision (object-grain WRITES) is a CTO-tracked v1 gap (relies on pipescript externally). |

## Knowledge-parity delta
- **BELIEVED:** the P4 code is "built + scratch-validated + accepted," and the post-nightly live-land yields ~29 SERVED_FROM edges (the scratch coverage).
- **TRUE:** the live-land would yield **0** edges -- the derive task role cannot `head_object` opal-data-portal-v2 (AccessDenied), so every /api/general/* resolution falls to object-miss-unresolved. The scratch-test passed only because it exercised the DEV-BOX's creds, not the derive's task role (the env-mismatch / dump-vs-derive divergence class -- the SAME class as the D8 mismatches this project hardened against).
- **CORRECTED:** this seam record + RAVC to CTO/COO. The fix routes to my lane (the derive infra) BEFORE the post-nightly live-land.

## Verdict
**BROKEN@MECHANICAL** -- NOT viable for the post-nightly live-land as-is. The seam would silently carry zero edges (IAM AccessDenied masked as object-absent). High-value catch: found before the land, not after a silent-empty re-derive.

## Residual / unknowns + fix routing (my lane, pre-live-land)
1. **IAM grant (BLOCKING):** add `s3:GetObject` (+ `s3:ListBucket`/`GetBucketLocation`) on `arn:aws:s3:::opal-data-portal-v2` (+ the 4 positioning/sentiment exception buckets once their real origin is resolved) to `derive_runner_s3` (item2a.tf). NB: this is a NEW cross-domain read grant (globgrph derive -> a portal data-tier bucket) -- surface to CTO/COO before applying (it's the graph-platform reading a served-data bucket, not a firm-pipeline cross-ref, but it's an IAM expansion). Additive read perm = nightly-safe (no graph touch), can land tonight so it's ready for the post-nightly re-derive. comp-iam verify after.
2. **403/404 distinction (code):** in `stitch_served_from`, distinguish `head_object` AccessDenied(403) from NoSuchKey(404) so the coverage caveat is accurate -- an IAM-blocked URL must surface as `iam-denied` (a LOUD config error), NOT `object-absent` (which reads as a benign per-path exception). The [[reference_s3_headobject_403_forbidden_names_no_action]] class (HeadObject's bodyless 403 names no action -> ground on the error code, not a parsed action).
3. **Scratch-test lesson:** a binding scratch-test must exercise the ACTUAL runtime principal (the derive's task role), or at minimum flag the IAM precondition -- dev-box-creds != derive-role is an env-mismatch that can pass a scratch while the live path no-ops.
4. **Live binding verify (still owed):** the on-graph SERVED_FROM edges actually forming (post-IAM-fix, post-nightly re-derive, under the ledger) -- the LIVE mechanical confirmation, which only the real re-derive provides.

## Compiler Tools
| Tool | Axis | Result |
|---|---|---|
| `comp-kuzu MATCH SERVED_FROM count` | MECHANICAL | 0 edges live (confirms dormant) |
| `comp-kuzu` s3 node identity | (build) | node_id = `arn:aws:s3:::opal-data-portal-v2` (the arn-form co-key, NOT bucket-name) |
| grep `derive_runner_s3` policy (item2a.tf) | MECHANICAL | s3:GetObject scoped to globgrph + tf-state ONLY; opal-data-portal-v2 absent -> the IAM gap |
| `aws s3api head-object` (dev creds) | SEMANTIC | object exists 19256B == DE ground-truth (but dev-creds, not the derive role -> the env-mismatch) |
| comp-iam service (derive role) | MECHANICAL | TODO post-fix: verify the opal-data-portal-v2 grant before the live-land |
