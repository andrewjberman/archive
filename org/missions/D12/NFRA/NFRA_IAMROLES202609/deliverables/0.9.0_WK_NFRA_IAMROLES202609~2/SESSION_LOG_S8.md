# Session log -- 0.9.0_WK_NFRA_IAMROLES202609~2 -- NFRA_IAMROLES202609.TO-IAM-s-8

Worktree: `/c/tmp/wk-iamroles-2` (branch `wk-NFRA_IAMROLES202609-2`). Worker identity: L7, subagent
of `2.0.0_SA_COO~ZI`, no standing session-log surface -- this file is the record for THIS cell,
separate from `SESSION_LOG.md` (this worktree's earlier IAM-s-4 record from the same serial's prior
task order, which is not touched here).

## What was built

`preflight-blast-radius.py` -- a read-only predictor: `--role <name> --remove <action>`. It composes
five existing instruments rather than re-deriving any of their logic:

1. **Live policy enumeration** (boto3 `iam:Get*`/`iam:List*`, read-only): every inline AND attached
   managed policy on the role, live, because the repo's Terraform does not carry every grant --
   discovered mid-cell that `opal-data-refresh-lambda-policy` (the ONLY source granting
   `s3:PutObject` on 3 of the 6 examined resource patterns) has no `aws_iam_role_policy`/
   `aws_iam_policy` Terraform resource checked into this repo at all (confirmed pre-existing/
   out-of-band per `main.tf`'s own comment). A repo-only read would have under-counted the blast
   radius by half.
2. **IAM-s-1's `comp-iam-usage reach-check`** -- one live `simulate-principal-policy` call per
   resource (Rule-22a limit (b): never batched), plus a separate positive and negative control.
3. **IAM-s-1's `comp-iam-usage permission-cold`** -- the historical-usage plane, which reports
   `s3:PutObject` as `unobservable` (S3 has no action-level Access Advisor tracking) and that BLIND
   status is surfaced rather than read as "safe."
4. **IAM-s-4's `condition-axis-reader.py`**, shelled out to directly against every local `.tf` file
   this script can resolve a matching statement to (via `comp-find`, not a re-derived grep). The
   managed policy's statement, having no local file, is reported as a named gap and its
   Condition-key presence read manually off the live document instead, explicitly labelled as
   bypassing the reader.
5. **`comp-blast`**, run against every Lambda function (per the committed `lambda-source-map.json`)
   assuming the role, downstream direction -- both to name the wider code-dependency blast radius
   and to CROSS-CHECK the live-fetched policy names against a second, independent instrument (the
   served cloud graph), which corroborated all three granting policy names.
6. **`comp-iam`** (the DESIRED-plane Terraform-vs-source cross-reference), queried specifically to
   NAME where it is blind: it has no role entry for `opal-data-refresh-lambda-role` at all, and
   every one of `opal-data-refresh-api`'s 55 tracked call-site operations (including both real
   `s3:PutObject` call sites, confirmed by direct code reading of
   `infra/aws/lambda/data_refresh/lambda_function.py` lines 373 and 528) reads `role not mapped`.

## Two implementation bugs caught before delivery

- **Extensionless bash-script shims cannot be exec'd by a native-Windows Python's `subprocess.run`
  without `shell=True`** -- `comp-iam-usage`/`comp-blast`/`comp-iam` all failed `WinError 2` when
  called as bare argv[0]. Fixed by routing every tool call through `bash -c "<quoted argv>"`
  (non-login: PATH is already inherited from the parent environment carrying the `~/bin`
  forwarders; a login shell was tried first and works too, but adds unneeded profile-load noise).
- **This device's native Python defaults file reads to cp1252, not UTF-8** -- reading
  `lambda-source-map.json` without an explicit `encoding="utf-8"` raised `UnicodeDecodeError` on a
  non-ASCII byte. Fixed by opening it with `encoding="utf-8"` explicitly.
- (Caught mid-investigation, outside the deliverable itself, and worth recording so it is not
  re-discovered the hard way next time: a Python string literal beginning `/c/...` is NOT
  understood by this device's native-Windows Python as `C:\...` -- MSYS/bash rewrites `/c/...`
  command-LINE ARGUMENTS to `C:/...` before exec, but a hardcoded path string INSIDE a script's own
  source never passes through that rewrite, so `io.open("/c/tmp/.../file")` silently resolves
  against the current drive's literal `c` subfolder and raises FileNotFoundError against a file
  that plainly exists per `ls`. Every absolute-path use inside this deliverable's own script instead
  derives its root via `git rev-parse --show-toplevel` and joins with `os.path.join`, never a
  hand-written `/c/...` literal.)

## Controls run

- **Mutant**: a scratch copy (`.scratch/mutant_probe.py`, never committed) had `derive_probe_arn`
  overridden (as the LAST definition of that name at module scope, so it wins) to always return a
  nonexistent, ungranted bucket ARN regardless of the real resource pattern. Run against the same
  role/action: all 6 reach-check calls returned `implicitDeny`, and the PREDICTION collapsed to "No
  probed resource pattern currently evaluates ALLOWED" -- FIRED-AS-EXPECTED. The unmutated
  deliverable, run immediately after, reproduced the real 6-of-6 `allowed` prediction verbatim.
- **Determinism**: two full invocations against the same live role/action, several minutes apart;
  `diff` on stdout with the timestamp line excluded produced no output -- STABLE. comp-blast's node
  counts (1015, 1044) were also identical run-to-run (graph did not rebuild between runs).

## Scope held

Every AWS call made by this script and by this session is read-only: `iam:Get*`, `iam:List*`, and
the read-only `simulate-principal-policy` evaluation call reached through
`.tools/comp-iam-usage reach-check`. No mutating IAM call and no infrastructure-as-code application
of any kind occurred. The three `iam.tf` files granted as read surfaces
(`infra/aws/terraform/{estate-report,mdpf-pipeline,inf-pipeline}/iam.tf`) were consulted only to
confirm the candidate role/action pair named in the task order's own AC1 invocation was a real one
worth exercising against; none was modified. `org/critical_paths/change_management/` and
`org/critical_paths/.open_deploys/` were not used -- no world-changing act became necessary to
answer FWD-5 at the bar this cell was given (CHECK, not APPLY), so NEVER-2's sequence was never
entered. No alert/alarm/monitor/schedule/notification was created (G-21).

## Deliverables

- `preflight-blast-radius.py` -- the predictor (AC1).
- `BLAST_RADIUS.md` -- the FWD-5 exhibit document (AC2/AC3/AC4), carrying the verbatim exercised
  transcript.
- `NFRA_IAMROLES202609.TO-IAM-s-8.pre-flight-blast-radius-exercised.proof_of_spec.json` -- this
  cell's proof-of-spec instance.
- This file.

No surprise row was filed. Every path named in `<paths>` existed and was sufficient; no premise of
the task order failed; the tool ran cleanly to a real prediction on the first fully-fixed attempt.
The managed policy having no local Terraform custody, and comp-iam's complete non-tracking of this
role, are both squarely responsive to what AC1 itself asked for ("naming any service on which the
prediction is BLIND") -- they are the deliverable's content, not a deviation from the task order.
