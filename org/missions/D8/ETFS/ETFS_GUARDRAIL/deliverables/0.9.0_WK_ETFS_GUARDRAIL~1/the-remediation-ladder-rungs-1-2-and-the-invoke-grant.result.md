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

## 5. S7-AC5 -- the TARGETED Terraform plan (RULING @`2baa6af162`; now PASS)

**RULING recorded (issuer `2.0.0_SA_COO~B` @`2baa6af162`, on rows `ETFS_GUARDRAIL-W1-S6`/`-S7`):** the pre-existing `aws_instance.reporter` `user_data` drift (documented benign/deferred by commit `1502fdd6f9`, 2026-07-08) is NOT this order's -- a `user_data` change on `aws_instance` applies through a provider-side STOP/START of the reporter instance, a confirm-with-Andrew act routed by the issuer, not this worker. This order plans and applies BY TARGET to `aws_iam_role_policy.reporter` only. The issuer also copied the estate's pinned `.tools/terraform.exe` (v1.9.8) into this worktree -- confirmed present, used for everything below (the earlier PATH v1.14.5 substitution from row `ETFS_GUARDRAIL-W1-S6` is RETIRED per the ruling: a newer CLI would re-pin the remote state's `terraform_version`).

**Full (untargeted) plan -- the honest state of the whole directory, quoted verbatim, BEFORE the apply:**
```
terraform -chdir=infra/aws/terraform/etfs-reports version -> Terraform v1.9.8
terraform -chdir=infra/aws/terraform/etfs-reports init -input=false   (rc=0, after rm -rf .terraform/ to clear the prior v1.14.5-initialized backend cache)
terraform -chdir=infra/aws/terraform/etfs-reports plan -no-color -input=false -lock=false

  # aws_iam_role_policy.reporter will be updated in-place
      + Sid = "InvokeProducersForRemediation" (Action lambda:InvokeFunction, 3 producer ARNs)

  # aws_instance.reporter will be updated in-place
      ~ user_data = "e47b615c4b7a16df31146d6834cb30ef1693c80f" -> "434774b5a5facfeb4931f837e1b93edc13bbec35"

Plan: 0 to add, 2 to change, 0 to destroy.
```
Reproduced byte-for-byte (modulo the terraform binary) as the FAIL reading recorded before the ruling -- confirming the drift is real, version-independent, and not an artifact of the earlier PATH substitution.

**Invocation (TARGETED, per the amended criterion):**
```
.tools/terraform.exe -chdir=infra/aws/terraform/etfs-reports plan -no-color -input=false -lock=false -target=aws_iam_role_policy.reporter
```
**Output (rc=0):**
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

Plan: 0 to add, 1 to change, 0 to destroy.

Warning: Resource targeting is in effect ...
```
**S7-AC5 verdict: PASS.** The targeted plan shows EXACTLY the reporter role policy, `0 to add, 1 to change, 0 to destroy`, matching `1 to change`.

## 6. S7-AC6 -- the ledger, the targeted apply, the APPLIED-plane read, the targeted 0-diff (PASS)

**Ledger:** opened before the apply -- `python .tools/deploy_ledger.py open --slug etfs-guardrail-eg-s-7-reporter-invoke-grant --title "EG-s-7: lambda:InvokeFunction on the three ETFS producers for etfs-reports-reporter-role (targeted: aws_iam_role_policy.reporter only)" --author 0.9.0_WK_ETFS_GUARDRAIL~1 --leg "iam|activation|etfs-reports-reporter-role|..."` -> `org/critical_paths/change_management/20260905T0239Z_etfs-guardrail-eg-s-7-reporter-invoke-grant_deploy_completion.md`. Entry + sentinel COMMITTED (`d1c4204aa1`) before the apply.

**Apply, BY TARGET:**
```
HALT_ACK=1 .tools/safe-apply.sh -chdir=infra/aws/terraform/etfs-reports apply -input=false -auto-approve -target=aws_iam_role_policy.reporter
```
**Output (rc=0):**
```
comp-tagauthz gate PASSED -- no plan resource overwrites an access-granting tag.
tombstone-gate CLEAN: no planned create matches a tombstoned resource.
Plan: 0 to add, 1 to change, 0 to destroy.
aws_iam_role_policy.reporter: Modifications complete after 1s
Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
```

**Invocation (the APPLIED-plane read):**
```
.tools/aws iam get-role-policy --role-name etfs-reports-reporter-role --policy-name etfs-reports-reporter --query "PolicyDocument.Statement[?Sid=='InvokeProducersForRemediation'].Action" --output text
```
**Output (rc=0):**
```
lambda:InvokeFunction
```
Full statement read (`--query "PolicyDocument.Statement[?Sid=='InvokeProducersForRemediation']" --output json`): `Action=["lambda:InvokeFunction"]`, `Effect="Allow"`, `Resource=` exactly the three producer ARNs, `Sid="InvokeProducersForRemediation"` -- matches the DESIRED text exactly.

**Targeted 0-diff (post-apply):**
```
.tools/terraform.exe -chdir=infra/aws/terraform/etfs-reports plan -no-color -input=false -lock=false -target=aws_iam_role_policy.reporter -detailed-exitcode
-> "No changes. Your infrastructure matches the configuration." rc=0
```
**Full (untargeted) plan, post-apply (the honest remaining state):**
```
Plan: 0 to add, 1 to change, 0 to destroy.
  # aws_instance.reporter will be updated in-place
      ~ user_data = "e47b615c4b7a16df31146d6834cb30ef1693c80f" -> "434774b5a5facfeb4931f837e1b93edc13bbec35"
```
Only the pre-existing, out-of-scope `aws_instance.reporter` drift remains -- the IAM change landed and dropped out of the diff entirely.

**Ledger close:**
```
python .tools/deploy_ledger.py close-leg --slug etfs-guardrail-eg-s-7-reporter-invoke-grant --leg-id iam --proof "get-role-policy ... -> lambda:InvokeFunction (applied BY TARGET; targeted 0-diff rc=0)"
-> OK: leg iam closed. Remaining open: NONE
python .tools/deploy_ledger.py close --slug etfs-guardrail-eg-s-7-reporter-invoke-grant
-> OK: CLOSED deploy ledger 'etfs-guardrail-eg-s-7-reporter-invoke-grant' -- all 1 legs proven; sentinel removed
```
**S7-AC6 verdict: PASS.**

## 7. S7-AC7 -- THE ANSWER (judgment; recorded, no verdict)

- **Rungs 0-2 are unattended and never fabricate:** `remediate_month` never calls `put_object` (S7-AC2's byte census: 0; test arm (e) asserts it on a stub across a mixed C/D/B/UNKNOWN month); a B day is a hard STOP before any invoke (test arm (b)); a D day's rung-1 invoke is caught exactly once with no retry (test arm (c)); `dry_run=True` makes zero invokes and zero S3 reads (test arm (f)).
- **The invoke grant names exactly three functions and no bucket, and is now APPLIED:** the `InvokeProducersForRemediation` Sid's `Resource` array is exactly `cot-etf-ownership-daily`, `bd-49f-etf-ownership-daily`, `inf-etf-ownership-daily`; no `s3:*` action, no bucket ARN, anywhere in the statement -- confirmed on the APPLIED plane by `get-role-policy` (section 6), not just the DESIRED text.
- **Rung 3 is a STOP left to `EG-sb-7`:** `remediate.py` carries no provider-call code path at all (S7-AC2: `HTTP_CLIENT_IMPORTS=0`) and its `unresolved` list is the ONLY output for a day nothing could recover -- the module returns, it does not ask.
- **The Inflection re-check is stated against the deployed producer's bucket:** `remediate.py`'s `_INFLECTION_DEPLOYED_UPSTREAM` constant names `opal-data-inf/gold/canonical/holdings_<date>.parquet` explicitly as "the DEPLOYED producer's own read, per EG-s-12," and is appended to any Inflection D-day's `reason` string -- so an Inflection D verdict never cites the repo's committed-but-unapplied `opal-data-assets/orion/inflection/silver/fact_positions` design as if it were live.
- **The 49F producer map follows `EG-s-11`'s confirmed answer:** `_PRODUCER_BY_PARTNER["49financial"] = "bd-49f-etf-ownership-daily"` (not `-canonical`), matching `EG-s-11`'s result document (`WRITER=bd-49f-etf-ownership-daily EVIDENCE=3`).
- **The pre-existing `aws_instance.reporter` drift was surfaced, not silently applied or silently ignored:** filed as `ETFS_GUARDRAIL-W1-S7`, ruled by the issuer as out-of-scope (a confirm-with-Andrew STOP/START act), and is now BY-TARGET-excluded from every plan/apply this order runs -- the full plan's remaining line (section 6) is the honest record that it is still there.

## 8. Ledger

`org/critical_paths/change_management/20260905T0239Z_etfs-guardrail-eg-s-7-reporter-invoke-grant_deploy_completion.md` -- OPENED before the targeted apply (commit `d1c4204aa1`), one leg (`iam|activation|etfs-reports-reporter-role`), CLOSED after the `get-role-policy` proof and the targeted 0-diff (this commit). Target stated in the ledger title and the leg's proof text.

## 9. Push state (measured at report)

```
git ls-remote origin refs/heads/CLOUD
```
