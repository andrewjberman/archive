# EG-s-7 -- the remediation ladder, rungs 0-2 unattended, and the one invoke grant

**TO:** `ETFS_GUARDRAIL.TO-EG-s-7` · **Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` · **Worktree HEAD:** `62cc386d94` (branch `wk-ETFS_GUARDRAIL-1`) · **Verb:** wire.

## Module built

- `data/etfs/scripts/coverage/remediate.py` -- `remediate_month(partner, month, classes, *, invoke=None, s3=None, dry_run=False) -> dict`; CLI `--partner`, `--month`, `--dry-run`.
- `data/etfs/scripts/coverage/tests/test_remediate.py` -- six arms, ZERO AWS calls (stub `invoke` + stub `s3`).
- IAM edit: `infra/aws/terraform/etfs-reports/iam.tf`, one new Sid `InvokeProducersForRemediation`.

## 1. S7-AC1 -- the six-arm battery

**Invocation:**
```
python -m pytest data/etfs/scripts/coverage/tests/test_remediate.py -q
```
**Output (rc=0):**
```
6 passed in 0.07s
```
Arms: (a) C day -> exactly one invoke `{"date": d}`, stub reports slice present -> resolved; (b) B day -> invoke NEVER called, in `expected_empty`; (c) D day -> invoke raises the producer's "no ... partition" `RuntimeError` shape -> `unresolved`/class D, exactly one invoke, no retry; (d) UNKNOWN day, no probe mode -> rung 1 once, then rung 2 re-check attempted; (e) never calls `put_object` (asserted on the stub, across a mixed C/D/B/UNKNOWN month); (f) `dry_run=True` -> zero invokes, zero S3 reads, full plan returned.

## 2. S7-AC2 -- no HTTP client, no S3 write, by bytes

**Invocation:**
```
python -c "import re; s=open('data/etfs/scripts/coverage/remediate.py').read(); print('HTTP_CLIENT_IMPORTS=%d PUT_OBJECT_CALLS=%d' % (len(re.findall(r'^\s*(?:import|from)\s+(?:requests|urllib|http)\b', s, re.M)), len(re.findall(r'put_object\(', s))))"
```
**Output (rc=0):**
```
HTTP_CLIENT_IMPORTS=0 PUT_OBJECT_CALLS=0
```

## 3. S7-AC3 -- live dry-run, cottonwood August 2026

**Invocation:**
```
python data/etfs/scripts/coverage/remediate.py --partner cottonwood --month 2026-08 --dry-run
```
**Output (rc=0):**
```
LADDER: partner=cottonwood month=2026-08 holes=0 rung0=0 rung1=0 rung2=0 unresolved=0 dry_run=True
```
`holes=0` is the expected state after the 09-01 repair (matches `EG-s-4`'s own live read). No invoke made (dry-run) and none would have been planned.

## 4. S7-AC4 -- commit gate clean

**Invocation:**
```
bash .tools/commit-gate.sh data/etfs/scripts/coverage/remediate.py data/etfs/scripts/coverage/tests/test_remediate.py
```
**Output (rc=0):**
```
OK: pre-commit gate clean for 2 of 2 file(s)
```

## 5. S7-AC5 -- the Terraform plan (FAIL by output -- honest, and a row)

**Tool substitution recorded (filed `ETFS_GUARDRAIL-W1-S6`, INERT):** the criterion's own invocation names `.tools/terraform.exe`, which does not exist in this fresh worktree (`.gitignore` + `.tools/safe-apply.sh` both document it as per-device and gitignored; the sibling exists in the main workspace tree but worktrees do not inherit untracked files). Substituted the PATH-resolved `terraform` (v1.14.5) -- the same fallback `safe-apply.sh` already implements by design.

**Invocation:**
```
terraform -chdir=infra/aws/terraform/etfs-reports init -input=false
terraform -chdir=infra/aws/terraform/etfs-reports plan -no-color -input=false -lock=false
```
**Output (init rc=0; plan rc=1, i.e. terraform's "diff present" exit code):**
```
  # aws_iam_role_policy.reporter will be updated in-place
  ~ resource "aws_iam_role_policy" "reporter" {
      ...
                  + {
                      + Action   = ["lambda:InvokeFunction"]
                      + Effect   = "Allow"
                      + Resource = [
                          + "arn:aws:lambda:us-east-1:313476888478:function:cot-etf-ownership-daily",
                          + "arn:aws:lambda:us-east-1:313476888478:function:bd-49f-etf-ownership-daily",
                          + "arn:aws:lambda:us-east-1:313476888478:function:inf-etf-ownership-daily",
                        ]
                      + Sid      = "InvokeProducersForRemediation"
                    },
    }

  # aws_instance.reporter will be updated in-place
  ~ resource "aws_instance" "reporter" {
      ~ user_data = "e47b615c4b7a16df31146d6834cb30ef1693c80f" -> "434774b5a5facfeb4931f837e1b93edc13bbec35"
    }

Plan: 0 to add, 2 to change, 0 to destroy.
```

**Denominator:** 2 of 2 resources changed shown, only 1 of 2 (`aws_iam_role_policy.reporter`) is this order's own edit.

**S7-AC5 verdict: FAIL by output.** The expected pattern `1 to change` does not match `Plan: 0 to add, 2 to change, 0 to destroy.` `git status --short infra/aws/terraform/etfs-reports/` shows only `M iam.tf`; `git diff instance.tf` is 0 bytes -- this worker's edit did not cause the `aws_instance.reporter` diff. That diff is a pre-existing, already-DOCUMENTED drift: commit `1502fdd6f9` (2026-07-08, "NFRA_TERRAFORM-P2 BATCH A") names it explicitly -- *"residuals are BENIGN non-replace (astn/etfs pending SNS sub=TIER-C; crawl user_data in-place; ...) -> deferred to a TIER-B/C safe-apply batch"* -- a ~2-month-old committed-but-never-applied `user_data` edit on this same instance. Per this TO's own BOUNDS ("a plan touching anything but `aws_iam_role_policy.reporter` is NOT applied"), **no apply was attempted.** Filed `ETFS_GUARDRAIL-W1-S7` (BLOCKING/INERT).

## 6. S7-AC6 -- UNCOMPUTABLE-BY-CONSTRUCTION

The criterion's own text makes it conditional: *"read after `HALT_ACK=1 .tools/safe-apply.sh ... apply ...`, which you run only after AC5's plan read exactly one resource."* AC5's plan read TWO. No apply was run; no `get-role-policy` read was made against a grant that does not yet exist on the APPLIED plane; no deploy ledger entry was opened (opening one for an apply this worker does not execute would itself be a stray, unclosed entry -- worse than not opening one). This criterion rides the later run that follows once `ETFS_GUARDRAIL-W1-S7`'s pre-existing drift is dispositioned (by its own commit's plan: "a TIER-B/C safe-apply batch") and the plan reads exactly one resource.

## 7. S7-AC7 -- THE ANSWER (judgment; recorded, no verdict)

- **Rungs 0-2 are unattended and never fabricate:** `remediate_month` never calls `put_object` (S7-AC2's byte census: 0; test arm (e) asserts it on a stub across a mixed C/D/B/UNKNOWN month); a B day is a hard STOP before any invoke (test arm (b)); a D day's rung-1 invoke is caught exactly once with no retry (test arm (c)); `dry_run=True` makes zero invokes and zero S3 reads (test arm (f)).
- **The invoke grant names exactly three functions and no bucket:** the added `InvokeProducersForRemediation` Sid's `Resource` array is exactly `cot-etf-ownership-daily`, `bd-49f-etf-ownership-daily`, `inf-etf-ownership-daily` (three fully-qualified function ARNs); no `s3:*` action, no bucket ARN, anywhere in the added block (visible in the plan diff above, section 5). NOT YET APPLIED (S7-AC5/AC6).
- **Rung 3 is a STOP left to `EG-sb-7`:** `remediate.py` carries no provider-call code path at all (S7-AC2: `HTTP_CLIENT_IMPORTS=0`) and its `unresolved` list is the ONLY output for a day nothing could recover -- the module returns, it does not ask.
- **The Inflection re-check is stated against the deployed producer's bucket:** `remediate.py`'s `_INFLECTION_DEPLOYED_UPSTREAM` constant names `opal-data-inf/gold/canonical/holdings_<date>.parquet` explicitly as "the DEPLOYED producer's own read, per EG-s-12," and is appended to any Inflection D-day's `reason` string (both the invoke-raised path and the recheck-failed path) -- so an Inflection D verdict never cites the repo's committed-but-unapplied `opal-data-assets/orion/inflection/silver/fact_positions` design as if it were live.
- **The 49F producer map follows `EG-s-11`'s confirmed answer:** `_PRODUCER_BY_PARTNER["49financial"] = "bd-49f-etf-ownership-daily"` (not `-canonical`), matching `EG-s-11`'s result document (`WRITER=bd-49f-etf-ownership-daily EVIDENCE=3`).

## 8. Ledger

No `org/critical_paths/change_management/` entry was opened. S7-AC5 failed its own precondition for the apply; opening a ledger entry for a deploy that is not executed would itself be a stray, unclosed entry -- worse than not opening one. The ledger opens when a future worker/seat re-plans this stack with a clean 1-resource diff and actually applies.

## 9. Push state (measured at report)

```
git ls-remote origin refs/heads/CLOUD
-> b000632f27e2e7462a8b666f15054a601b0324d1
```
