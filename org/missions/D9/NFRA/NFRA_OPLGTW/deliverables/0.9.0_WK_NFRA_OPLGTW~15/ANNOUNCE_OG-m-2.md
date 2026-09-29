# ANNOUNCE -- OG-m-2 PHASE A (0.9.0_WK_NFRA_OPLGTW~15), no AWS write

**State: BUILT AND TESTED, NOT COMMITTED.** The naming gate refused the code commit (row `NFRA_OPLGTW-Z-W15-S2`, BLOCKING);
a second row `-Z-W15-S1` (BLOCKING, inert) names an IAM gap. Neither was overridden. The code, tests and .tf diff sit in
worktree `C:/tmp/wk-oplgtw-15` on branch `wk-NFRA_OPLGTW-15` (uncommitted), and are saved here as
`og-m-2_code_and_iam.patch` (lambda_function.py + advi_49f_floor.tf) and `test_advi_49f_gold_dispatch_remedy.py.txt`.

## Diff stat (base 14d3ce32a8)
```
 infra/aws/lambda/opal-assets/advi-49f-gold-dispatch/lambda_function.py | 130 ++++++++++++++++++---
 infra/aws/terraform/opal-assets/advi_49f_floor.tf                      |  16 +++
 infra/aws/lambda/opal-assets/tests/test_advi_49f_gold_dispatch_remedy.py (new, 143 lines)
```
`lambda-source-map.json` not touched in PHASE A (the build script rewrites it in PHASE B).

## The 6 tests (dr.AC1.sh: "pytest rc=0; named tests passed 6 of 6; failed/error lines 0 -- RESULT: PASS")
test_chain_log_ok_classifies_ok_once, test_chain_log_abort_classifies_abort, test_missing_chain_log_is_unknown_and_says_so,
test_incomplete_marker_does_not_dispatch, test_qualified_marker_dispatches_once, test_floor_event_reads_no_marker.

## Targeted plan (`terraform plan -target=module.advi_49f_gold_dispatch -target=aws_iam_role_policy.advi_49f_gold_dispatch`, `-lock=false`, after a local `init` in the worktree)
`Plan: 0 to add, 1 to change, 0 to destroy.` -- `aws_iam_role_policy.advi_49f_gold_dispatch` updated in place: two
statements added, `ReadTheChainLog` (s3:GetObject on `arn:aws:s3:::opal-data-49financial/gold/advi/_logs/chain_*`) and
`ReadTheAcceleratorMarker` (s3:GetObject on `arn:aws:s3:::opal-data-assets/schwab/08335338/meta/complete/*`); no
ListBucket; the module (function) unchanged until a new artifact version exists.

## Live re-read (2026-09-29 ~01:0xZ)
- Lambda `advi-49f-gold-dispatch` CodeSha256 `fEMCZ4usqXuIC1GhklcClwOn/O6vR+uV+xgbk+oj8lk=`, LastModified 2026-08-19T17:32:12.440Z.
- Artifact `opal-313476888478-lambda-artifacts` `opal-assets/advi-49f-gold-dispatch.zip`: latest VersionId `MLLnDY4WlZCx94GuUkxXyQWlYXR2c5kY` (2026-08-19T15:59:08Z), content-sha256 `fEMCZ4...` (unchanged from the order; one older version `ttb_Z9GuVaGo1dNz4wKt0p7LhHGm5Lgs`).

## One-deployer census (`git worktree list --porcelain`, then `ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/` per tree)
104 worktrees read. Sentinel names matching `advi-49f|opal-assets|49f`: 2 distinct, neither on the dispatcher --
`irpt-performance-49f-engine-20260924.json` (11 trees, author 2.0.0_SA_COO~P, OPEN, irpt performance adapter) and
`nfra-mcpindex-bd-exporter-49f-session-read.json` (3 trees, OPEN, bd-exporter role secret read). Neither names `advi-49f-gold-dispatch`
or the `opal-assets` root. Re-run at PHASE B.

## Design notes
- Log key from `ExecutionStartDateTime` truncated to the second; tried TS, TS-1, TS+1; any read error counts as absent.
- The gate runs for the event source `advi.49f.silver-accelerator` (a superset of "returns a marker key": an S3 event with no key also skips), after the document allowlist check and before any EC2/SSM call. The event key is `unquote_plus`-decoded before the read (S3 event keys are URL-encoded: `date%3D...`).
- A missing `versionId` in the event skips (fail closed).
- SSM stdout is printed only as a length line.

---
## UPDATE after rulings A1 (@45a2a598a4, branch B) and A2 (@e534f3d938)

**State: still BUILT AND TESTED, NOT COMMITTED.** Route (iii) reached; row `NFRA_OPLGTW-Z-W15-S3` (BLOCKING, INERT) carries the exact refusal.
- **A1 applied:** marker ARN `s3:GetObject` + `s3:GetObjectVersion`; chain-log ARN `s3:GetObject` alone; no ListBucket.
- **A2 route (i) failed:** `address('advi','49financial','gold','_logs','chain_')` gives `.../advi/49financial/gold/_logs/chain_`, not the existing `gold/advi/_logs/chain_`.
- **A2 route (ii) built:** `local.advi_49f_chain_log_prefix` read by the SSM upload target, the IAM ARN and a new env var `CHAIN_LOG_PREFIX` (plus `CHAIN_LOG_BUCKET`); no Python literal of either; unset env reads `UNKNOWN(chain_log=unconfigured)`. Tests set the env.
- **Route (iii):** `naming-gate.py --enforce` REFUSES `advi_49f_floor.tf:56 gold/advi/_logs/chain_` ("EXISTING and OUT-OF-PATTERN as S3Key in a surface remediations.json assigns to the live remediation ADVI_FIRMBKTS: REFUSE unless the diff removes it"), although the diff removes the same literal from the SSM cp line. Only other output: WARN on `advi.49f.silver-accelerator`.
- **Tests:** dr.AC1.sh `named tests passed 6 of 6; failed/error lines 0 -- RESULT: PASS`.
- **Targeted plan (`-lock=false`):** `Plan: 0 to add, 2 to change, 0 to destroy.` Changed: `aws_iam_role_policy.advi_49f_gold_dispatch` and `module.advi_49f_gold_dispatch.aws_lambda_function.this` (env `CHAIN_LOG_BUCKET`, `CHAIN_LOG_PREFIX` added). `aws_ssm_document` is not listed: unchanged (guard met).
- `og-m-2_code_and_iam.patch` and the `.py.txt` copy are refreshed to the current worktree state.

---
## UPDATE after A3 (SPLIT) and the CTO pin addendum -- this order is OG-m-2a; PHASE A COMPLETE, COMMITTED

**Code commit `c064389bab` (LOCAL, wk-NFRA_OPLGTW-15).** Naming gate on the diff: `NAMING-GATE: WARN 1 graded` (only the existing `advi.49f.silver-accelerator` hand-kept-carrier WARN); no refusal, no override.
- **Diff (2 tracked + 1 new):** `lambda_function.py` +44 (marker gate, `_marker_closure_status`, s3 client, `_trigger_identity` rider stays); `advi_49f_floor.tf` +9 (one statement `ReadTheAcceleratorMarker`: `s3:GetObject` + `s3:GetObjectVersion` on `arn:aws:s3:::opal-data-assets/schwab/08335338/meta/complete/*`, no ListBucket); new test file, 3 tests.
- **Reverted:** every classifier and chain-log change (no chain-log grant, literal, local or `CHAIN_LOG_*` env var); the stdout `_classify` is byte-for-byte the deployed shape.
- **Tests:** `test_incomplete_marker_does_not_dispatch`, `test_qualified_marker_dispatches_once`, `test_floor_event_reads_no_marker`. dr.AC1.sh: `named tests passed 3 of 3; failed/error lines 0 -- RESULT: PASS`.
- **Targeted plan (`-lock=false`):** `Plan: 0 to add, 1 to change, 0 to destroy.` Only `aws_iam_role_policy.advi_49f_gold_dispatch` is listed. The function's code change appears only after the new artifact version exists (the module reads the artifact's latest S3 version); no env var, no `aws_ssm_document` change.
- **Live re-read (now):** `CodeSha256` `fEMCZ4usqXuIC1GhklcClwOn/O6vR+uV+xgbk+oj8lk=` (2026-08-19T17:32:12.440Z); artifact latest VersionId `MLLnDY4WlZCx94GuUkxXyQWlYXR2c5kY`. Unchanged.

**2b frozen candidate:** `og-m-2b_candidate_frozen.patch`, sha256 `600a4b6da9e75c65472dfdf10532cd85218f291c2b0b14b79d232275ca5ffbfe` (11,683 bytes), byte-identical to `og-m-2_code_and_iam.patch` committed at 8340c65376 (same sha256) and to the CTO pin prefix `600a4b6da9e7...` (the CTO's file itself is not present in this worktree to compare in full). Not to be edited. `og-m-2b_input_test_full_6.py.txt` is the six-test file for 2b.
