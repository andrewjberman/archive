# ANNOUNCE -- OG-m-3 PHASE A (0.9.0_WK_NFRA_OPLGTW~15), no AWS write

Code commit `4e14699746` (LOCAL, wk-NFRA_OPLGTW-15). Branch was already at CLOUD HEAD `bd0e06fe4c`: `40fcde8bf7` and `e4ec197609` are both ancestors of HEAD (`merge-base --is-ancestor` rc 0 each).

## Delta proof (frozen patch re-applied UNMODIFIED)
- Frozen patch sha256 `600a4b6da9e75c65472dfdf10532cd85218f291c2b0b14b79d232275ca5ffbfe` (read again just before applying). Target bytes built outside the repo: `git archive 8340c65376` of the two files, `git apply` of the patch in `.scratch/tgt` (both "Applied cleanly"). The archive came out CRLF, so the line endings were normalised to LF to match HEAD's stored form (index `i/lf`, `eol=lf`); no other edit. The test file is `og-m-2b_input_test_full_6.py.txt` copied over the test path, byte for byte.
- `git diff --ignore-cr-at-eol --stat HEAD` before the commit: `lambda_function.py` 97 lines (+77/-20 net of the test file), test file 43, `advi_49f_floor.tf` 22; 3 files changed, 133 insertions, 29 deletions.
- Hunks in `lambda_function.py`: docstring bullets (2), `from datetime import datetime, timedelta`, `CHAIN_LOG_BUCKET`/`CHAIN_LOG_PREFIX` (+2 comment lines), `_classify_log`, `_chain_log_keys`, the new `_classify(inv)` (replaces the stdout `_classify`), and the call site with its stdout-context print. **One hunk beyond the order's list:** the `ACCELERATOR_SOURCE` constant is moved up (deleted at its old line and added above the two new constants), value unchanged; it is part of the frozen bytes. The marker-gate code (`_marker_closure_status`, the SKIP branch) shows NO diff.
- Hunks in `advi_49f_floor.tf`: the local `advi_49f_chain_log_prefix` (+ 2 comment lines, line 56), `ReadTheChainLog` statement, the marker statement's comment text, the two env vars `CHAIN_LOG_BUCKET`/`CHAIN_LOG_PREFIX`, and the SSM document's `aws s3 cp` line (:313) reading the local.

## Reference count of `local.advi_49f_chain_log_prefix`: 3
:164 `ReadTheChainLog` Resource, :208 `CHAIN_LOG_PREFIX` env var, :313 the SSM `aws s3 cp` target. (The definition is :56.) No fourth.

## Naming gate (`naming-gate.py --enforce` on the diff, and again inside `safe-commit.sh`)
`NAMING-GATE: WARN 2 graded`, rc 0. `NAMING WAIVED-READ ... advi_49f_floor.tf:56 gold/advi/_logs/chain_` "WAIVED as an authorized LEGACY READ by OPLGTW-LEGACY-READ-01 (owner 1.0.0_SA_CTO~O, cutoff 2026-10-06 inclusive UTC) ... referenced 3 time(s) as reviewed". The other line is the old WARN on `advi.49f.silver-accelerator` (`lambda_function.py:69`). No override.

## Tests (dc.AC1.sh: "pytest rc=0; named tests passed 6 of 6; failed/error lines 0 -- RESULT: PASS")
test_chain_log_ok_classifies_ok_once, test_chain_log_abort_classifies_abort, test_missing_chain_log_is_unknown_and_says_so, test_incomplete_marker_does_not_dispatch, test_qualified_marker_dispatches_once, test_floor_event_reads_no_marker.

## Plan (bound 4: `plan -target=module.advi_49f_gold_dispatch -target=aws_iam_role_policy.advi_49f_gold_dispatch -target=aws_ssm_document.advi_49f_chain_dispatch`, `-lock=false`)
`Plan: 0 to add, 2 to change, 0 to destroy.` Listed: `aws_iam_role_policy.advi_49f_gold_dispatch` (adds `ReadTheChainLog`, `s3:GetObject` on `arn:aws:s3:::opal-data-49financial/gold/advi/_logs/chain_*`) and `module.advi_49f_gold_dispatch.aws_lambda_function.this` (env `CHAIN_LOG_BUCKET = opal-data-49financial`, `CHAIN_LOG_PREFIX = gold/advi/_logs/chain_`; its code changes only after the new artifact exists). `aws_ssm_document.advi_49f_chain_dispatch` is NOT listed: it renders unchanged (guard met).

## comp-iam (`comp-iam service advi-49f-gold-dispatch`, after the change)
`checked 7 calls across 7 statements; 4 unresolvable`; 3 GRANTED-BROAD (the same three as at the cut), the s3 reads now among the resolvable/unresolvable set; no new broad grant.

## Live reads (2026-09-29 ~02:5xZ)
`CodeSha256 KqlIoAJs98dXE1RoL9g0xBG0yQw9Mo3JiSFUaJO17qg=` (LastModified 2026-09-29T02:05:33Z). Artifact latest VersionId `3qOKR75Bkc4pDjaQxsSqy0h1.dYuTjqp` (2026-09-29T01:54:50Z), content-sha256 `KqlIoAJs...`. Both as the order states.

## One-deployer census (`git worktree list --porcelain`, `ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/` per tree)
111 trees read, 1,180 sentinel entries, 44 distinct sentinels. Name matches on `advi|dispatch|opal-assets|49f|oplgtw`: `advi-insure-gold-chain-membership` (OPEN, 49F `_code` bundle), `advi-insure-iam-insurance-silver-read` (OPEN, bd-exporter role), `irpt-holdings-principals-dispatch-m-20260925` (HELD, irpt holdings), `irpt-performance-49f-engine-20260924` (OPEN, irpt performance), `nfra-mcpindex-bd-exporter-49f-session-read` (OPEN, bd-exporter role), `nfra-oplgtw-og-r-1-first-release` (OPEN, 0.9.0_WK_NFRA_OPLGTW~2, opal-gateway EC2 asset). None names `advi-49f-gold-dispatch`, the `opal-assets` root or the dispatcher. `nfra-oplgtw-dispatch-classifier-remedy` is not listed (closed). Re-run at PHASE B.
