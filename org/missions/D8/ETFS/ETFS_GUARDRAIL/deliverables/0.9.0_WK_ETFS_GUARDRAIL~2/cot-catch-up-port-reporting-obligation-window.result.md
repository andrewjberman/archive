# EG-s-1 result -- cot-etf-ownership-daily: the catch-up ported, reporting-obligation window, probe, deployed

**TO:** `ETFS_GUARDRAIL.TO-EG-s-1` | **Worker:** `0.9.0_WK_ETFS_GUARDRAIL~2` | **Source (edited, deployed):**
`infra/aws/lambda/cot-pipeline/cot-etf-ownership-daily/lambda_function.py` (was 177 lines, 0 catch-up hits, per THE CELL)

---

## 1. Acceptance criteria, verbatim with rc and denominator

### S1-AC1 -- the eight-arm battery is green

**Invocation:** `python -m pytest infra/aws/lambda/cot-pipeline/cot-etf-ownership-daily/test_catchup_window.py -q`

```
........                                                                 [100%]
8 passed in 2.07s
```
rc=0. Denominator: 8 of 8 arms passed (h, c, d, a, b, e, f, g). **PASS.**

**Instrument note (filed `ETFS_GUARDRAIL-W2-S4`):** the battery is written as real `def test_*`
functions, NOT the bare-script-with-module-level-`sys.exit()` shape inf-etf-ownership-daily's
`test_catchup_scan.py` uses (the shape EG-s-3's port contract otherwise described mirroring). A
module-level `sys.exit()` raised during pytest COLLECTION crashes pytest with an INTERNALERROR
(rc=3, "no tests ran") regardless of whether every arm's own check would have passed --
reproduced independently on a two-line repro module, and on this file's own first draft (same 8
arms, all internally passing per print output) before the rewrite. `expect="passed"` is only
reachable from real pytest items.

### S1-AC2 -- four properties of the bytes

**Invocation:** `python -c "s=open('infra/aws/lambda/cot-pipeline/cot-etf-ownership-daily/lambda_function.py').read(); print('DAYCOUNT_WINDOW=%s SHIPPED_SIGNAL=%s PROBE=%s ZERO_VS_MISSING=%s' % ('CATCHUP_WINDOW_DAYS' in s, 'etf_ownership.pdf' in s, '\"probe\"' in s, 'skipped-no-valued-source' in s))"`

```
DAYCOUNT_WINDOW=False SHIPPED_SIGNAL=True PROBE=True ZERO_VS_MISSING=True
```
rc=0. Denominator: 4 of 4 properties matched the expectation exactly. **PASS.**

### S1-AC3 -- NO fifth in-repo copy of the calendar; the layer carries it

**Invocation:** `python -c "import os; print('COMMITTED_CAL_COPY=%s' % os.path.exists('infra/aws/lambda/cot-pipeline/cot-etf-ownership-daily/trading_calendar.py'))"`

```
COMMITTED_CAL_COPY=False
```
rc=0. Denominator: 1 of 1 path checked, absent as required. **PASS.**

**Attached layer ARNs (`get-function-configuration --query Layers[].Arn`, post-apply):**
```json
[
  "arn:aws:lambda:us-east-1:313476888478:layer:pandas-pyarrow-requests-layer:1",
  "arn:aws:lambda:us-east-1:313476888478:layer:opal-trading-calendar-layer:1"
]
```
Both the pre-existing pandas/pyarrow layer and the newly-attached `opal-trading-calendar-layer:1`
are present -- 2 of 2 expected layers.

### S1-AC4 -- the commit gate is clean

**Invocation:** `bash .tools/commit-gate.sh infra/aws/lambda/cot-pipeline/cot-etf-ownership-daily/lambda_function.py infra/aws/lambda/cot-pipeline/cot-etf-ownership-daily/test_catchup_window.py`

```
All checks passed!
OK: no unguarded strict-utf8 log reads.
OK: pre-commit gate clean for 2 of 2 file(s)
```
rc=0. One non-blocking WARN (non-ASCII `U+26D4` at line 11 -- the pre-existing `FIRM SEPARATION`
warning symbol, carried verbatim from the source, not introduced by this port). Denominator: 2 of
2 files clean. **PASS.**

### S1-AC5 -- the plan changes the Lambda + the layer attachment + the one Sid, nothing else

**Invocation:** `.tools/terraform.exe -chdir=infra/aws/terraform/cot-pipeline plan -no-color -input=false -lock=false`

**Summary line:** `Plan: 0 to add, 2 to change, 0 to destroy.`

**Every resource named in the plan (denominator: 2 of 2 changed, 0 of 0 added/destroyed):**
1. `aws_iam_role_policy.cot_etf_ownership_daily_s3` (updated in-place) -- adds the ONE new
   statement `ReadShippedSignal` (`s3:GetObject` on `arn:aws:s3:::opal-data-etfs/platinum/reports/*/etf_ownership.pdf`).
2. `module.cot_etf_ownership_daily.aws_lambda_function.this` (updated in-place) -- `layers` gains
   `arn:aws:lambda:us-east-1:313476888478:layer:opal-trading-calendar-layer:1`; `s3_object_version`
   and `source_code_hash` change to the new upload (`21/NtBoTmMsBBSsfwNnA+UP+I3HIzDnZaoeL3lBShFk=`).

No other resource address appears in the plan. **PASS** (not a BLOCKING row -- the plan matches
the bound exactly).

### S1-AC6 -- 0-diff after the apply

Applied via `HALT_ACK=1 .tools/safe-apply.sh -chdir=infra/aws/terraform/cot-pipeline apply -input=false -auto-approve`
-> `Apply complete! Resources: 0 added, 2 changed, 0 destroyed.`

**Invocation:** `.tools/terraform.exe -chdir=infra/aws/terraform/cot-pipeline plan -no-color -input=false -lock=false -detailed-exitcode; echo rc=$?`

```
...
No changes. Your infrastructure matches the configuration.
rc=0
```
Denominator: 1 of 1 re-plan, 0-diff. **PASS.**

### S1-AC7 -- served CodeSha256 == built artifact_sha256

**Invocation:** `python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~2/cot_served_vs_built.py`

```
SERVED CodeSha256 (live get-function-configuration): 21/NtBoTmMsBBSsfwNnA+UP+I3HIzDnZaoeL3lBShFk=
BUILT  artifact_sha256 (lambda-source-map.json, written by build-and-upload.sh): 21/NtBoTmMsBBSsfwNnA+UP+I3HIzDnZaoeL3lBShFk=
VERDICT: MATCH
```
rc=0. Denominator: 1 hash pair compared, MATCH. **PASS.**

(The script reads the served hash via `boto3` directly rather than shelling out to the
`.tools/aws` bash shim from Python -- shelling a bash script from `subprocess.run` on this box
raises `FileNotFoundError` since it is not a native Windows executable, CLAUDE.md Rule 16's
class of trap; caught and fixed before recording this run, no surprise row needed for an
implementation detail resolved before any output was reported.)

### S1-AC8 -- the deployed probe answers for 2026-08-04, writes nothing

**Invocation:** `.tools/aws lambda invoke --function-name cot-etf-ownership-daily --payload "{\"date\":\"2026-08-04\",\"probe\":true}" .scratch/probe_out.json`
(the literal `/dev/stdout` target the TO names produced `[Errno 2] No such file or directory:
'/proc/.../fd/pipe:[...]'` under the CLI v1 shim on this box -- an MSYS pipe-target quirk, not a
payload-form problem; writing to a real file resolved it immediately, recorded per the TO's own
"record the exact form" allowance.)

```
{"status": "probe", "date": "2026-08-04", "partition": true, "priced": 10958, "output_exists": true}
```
Denominator: `"partition": true` matched (the expectation); `priced=10958`, `output_exists=true`
recorded. **PASS.** No write reachable on this path (proven at the unit level by arm (g), which
raises `AssertionError` if `put_object` is ever called and the deployed probe's own response
shape carries no write-confirming field).

### S1-AC9 -- judgment, RECORD; NO VERDICT

The window is the reporting obligation with a shipped-signal terminus (`_window_dates`,
`_report_shipped`); the port keeps the source's three skips (`_catchup_missing_dates`) and never
fabricates (upstream-absent is always skipped, `_partition_exists`); the ZERO-vs-MISSING contract
is untouched (`_process_date`'s `priced == 0` guard, byte-identical in shape to the pre-port
`lambda_handler` body). FWD-1's EXERCISED grade (a real missed day caught up without a person) is
the next scheduled fire (`cron(30 10 * * ? *)`) that names a recovered date in
`catchup_processed` -- this order does not manufacture that fire; it deploys the mechanism that
will produce it.

---

## 2. THE DEPLOY -- sequence, hashes, ledger

| step | invocation | result |
|---|---|---|
| commit source | `safe-commit.sh` (lambda_function.py, test_catchup_window.py, .tf edit, surprise row) | `42dd9e8c81` |
| build+upload | `bash infra/aws/lambda/ci/build-and-upload.sh cot-pipeline cot-etf-ownership-daily` | SHA256 `21/NtBoTmMsBBSsfwNnA+UP+I3HIzDnZaoeL3lBShFk=`, uploaded, write VERIFIED |
| commit artifact | `safe-commit.sh` (lambda-source-map.json) | `946507c4ae` |
| ledger open | `deploy_ledger.py open --slug etfs-guardrail-eg-s-1-cot-catchup-port ... --lambda cot-etf-ownership-daily` | 1 tf-lambda leg opened |
| commit ledger open | `safe-commit.sh` (.open_deploys sentinel + change_management entry) | `13ed1ab775` |
| terraform init | `.tools/terraform.exe -chdir=infra/aws/terraform/cot-pipeline init -input=false` | initialized (first run this worktree; `.tools/terraform.exe` is gitignored per-device and was copied from the main tree since a linked worktree does not inherit untracked files) |
| plan | see S1-AC5 | 0 add / 2 change / 0 destroy |
| apply | `HALT_ACK=1 .tools/safe-apply.sh -chdir=infra/aws/terraform/cot-pipeline apply -input=false -auto-approve` (first attempt refused rc=3 IDENTITY UNRESOLVED -- wrote the gitignored session serial file the gate's own banner prescribed, re-ran) | `Apply complete! Resources: 0 added, 2 changed, 0 destroyed.` |
| 0-diff | see S1-AC6 | `No changes.` |
| served vs built | see S1-AC7 | MATCH |
| probe | see S1-AC8 | `partition: true` |
| record deploy | `bash infra/aws/lambda/ci/record-terraform-deploy.sh cot-pipeline --function cot-etf-ownership-daily --author "0.9.0_WK_ETFS_GUARDRAIL~2 <...>"` | `ci: record deploy cot-pipeline @ 13ed1ab7 [skip ci]` -> `a8ef1ca328`; `last_deployed_commit` set to `42dd9e8c81` (the source commit, per the script's own corrected contract -- not HEAD, not the ledger commit) |
| close-leg | `deploy_ledger.py close-leg --slug ... --leg-id cot-etf-ownership-daily --proof "..."` | leg closed |
| close | `deploy_ledger.py close --slug etfs-guardrail-eg-s-1-cot-catchup-port` | `CLOSED ... all 1 legs proven; sentinel removed` |
| commit ledger close | `safe-commit.sh` | `091681fe45` |

**No leg left open; the change-management entry is CLOSED, not merely committed.**

---

## 3. Bounds honored

- No served `daily/cottonwood/*.json` object deleted; property 1's "deleted slice" is not
  exercised by this order (unit arms + probe only, per the BOUNDS).
- No dated non-probe invoke run (would write a slice) -- not exercised by this order.
- NEVER#1/NEVER#2: no read added on `blackdiamond/49f/` or any firm prefix other than
  `blackdiamond/cottonwood/`; the one new Sid reads only the aggregation bucket's own
  `platinum/reports/*/etf_ownership.pdf`.
- Terraform through `.tools/safe-apply.sh` only; `aws lambda update-function-code` never called;
  ledger opened before the apply, closed after; plan read before apply (S1-AC5); 0-diff after
  (S1-AC6); the artifact upload preceded the plan.

## 4. Push state (measured)

`git ls-remote origin refs/heads/CLOUD` -- see the WORKER REPORT for the value read at report
time (a push state read earlier in a long session is stale by the time it is quoted).
