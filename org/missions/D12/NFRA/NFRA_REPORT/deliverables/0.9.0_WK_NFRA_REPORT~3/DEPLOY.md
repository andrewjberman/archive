# DEPLOY.md -- NFRA_REPORT.TO-RP-s-23 (0.9.0_WK_NFRA_REPORT~3)

Wire the edition renderer into `opal-infrastructure-monitor` and deploy it on the Terraform path
(`infra-monitor.tf:7`: package -> S3 -> `source_code_hash` reads the object's metadata -> `safe-apply`).
No other path is used at any point in this record.

## 1. Source change (lambda_function.py)

`infra/aws/lambda/infrastructure_monitor/lambda_function.py`'s handler, at the (pre-change) line 267
`email_body = format_report(report)`, is rewired to:

```
rows, omissions = edition_rows.rows_from_report(report, _load_prior_report())

for r in rows:
    if r["family"] == "watch":
        delta, note = edition.compute_delta_watch(r["prev"], r["curr"])
    else:
        delta, note = edition.compute_delta(r["prev"], r["curr"])
    r["delta"] = delta
    r["rule_note"] = "(%s)" % note

needs_andrew, breach_rows, worse_rows = edition.compute_verdict(rows)
email_body = edition.render_markdown(rows, needs_andrew, breach_rows, worse_rows, start_time.isoformat())
```

`format_report` (the 439-line legacy renderer) stays DEFINED, unreferenced by the handler, for
`RP-s-24`. `send_email`, `archive_report`, `publish_status_feed` are unchanged. Two module-level
imports added: `import edition`, `import edition_rows`.

AC4, run against this worktree's source at HEAD:
```
HANDLER_CALLS_format_report=0 HANDLER_CALLS_render_markdown=1 format_report_STILL_DEFINED=1 DELTA_ATTACHED=2 COMPUTE_DELTA_CALLS=2
```
Matches the expectation (0 / >=1 / 1 / >=1 / >=2).

## 2. Package (the artifact is layer-shaped, function modules only)

4 files packaged, sorted, fixed-timestamp zip (PowerShell `System.IO.Compression.ZipFile`, same
technique as `infra/aws/lambda/ci/build-and-upload.sh`) -- NOT the vendored `anyio/`, `httpx/`,
`certifi/`, `pydantic`, etc. directories in the source folder, which belong to the
`anthropic_sdk_deps` layer (`infra-monitor.tf:53`) and are not shipped:

```
edition.py            15,492 bytes
edition_rows.py       26,984 bytes
lambda_function.py   121,582 bytes
openai_cost_tracker.py 18,376 bytes
```

Import-closure check (`infra/aws/lambda/ci/import-closure-check.py`, run standalone against exactly
these 4 files, independent of `lambda-source-map.json`'s `files[]` list -- see the SEPARATE finding
below):
```
OK: import-closure -- 4 packaged .py file(s), every top-level import satisfied by package/stdlib/runtime/layer.
```

Zip: 4 entries, 54,009 bytes total. `SHA256` (base64, Lambda's `source_code_hash` format):
`j7lljv8S5efk1KJz0Zh7+pV0+PIfcYbCOVJY2TE0/kE=`

## 3. S3 put (before any Terraform action)

```
aws s3 cp .../opal-infrastructure-monitor.zip \
  s3://opal-313476888478-lambda-artifacts/shared-infra/opal-infrastructure-monitor.zip \
  --metadata content-sha256=j7lljv8S5efk1KJz0Zh7+pV0+PIfcYbCOVJY2TE0/kE= \
  --region us-east-1
```
Upload VERIFIED via `head-object` (not trusted from the cp's own rc):
```
ContentLength: 54009   Metadata.content-sha256: j7lljv8S5efk1KJz0Zh7+pV0+PIfcYbCOVJY2TE0/kE=
```
Matches the local zip's byte size (54009) and computed SHA256 exactly.

## 4. Terraform plan (scoped) + safe-apply

Plan scoped to the one resource this cell may touch (`-target=aws_lambda_function.infra_monitor`):
```
Terraform will perform the following actions:
  # aws_lambda_function.infra_monitor will be updated in-place
  ~ resource "aws_lambda_function" "infra_monitor" {
        id                = "opal-infrastructure-monitor"
      ~ last_modified     = "2026-07-08T01:29:08.000+0000" -> (known after apply)
      ~ s3_object_version = "YneO.cB9qClMEkBUeljD7l2m9BsVfNGJ" -> "ptn6tOacqtLFMCAL9jRPA.8E4H9ZEqzE"
      ~ source_code_hash  = "r/bjjp5dJMcxw4NnzSNFsUCpYlWrH+sJsVJu+JiWxs8=" -> "j7lljv8S5efk1KJz0Zh7+pV0+PIfcYbCOVJY2TE0/kE="
        tags              = {}
        # (28 unchanged attributes hidden)
    }

Plan: 0 to add, 1 to change, 0 to destroy.
```
0 to add, 0 to destroy -- no alarm, topic, subscription, schedule or notification appears anywhere
in this plan. Only the Lambda function's code pointer changes.

Applied via `.tools/safe-apply.sh -chdir=infra/aws/terraform/shared-infra apply <planfile>` (never a
bare `terraform apply` at any point in this record):

- HALTGT checkpoint: BLOCKING on the first attempt (identity could not be resolved -- see
  `NFRA_REPORT-Z-W3-S1` in the investigations file for the full finding and the in-paths remedy
  applied, commit `0eb5081768`). After the remedy, the checkpoint correctly resolved this worker,
  correctly routed to scanning issuer `2.0.0_SA_COO~ZZ`'s inbox, and surfaced 173 pending ROUTINE
  (non-STOP-class) messages -- all automated `deploy_ledger.py` nudges/notices, manually confirmed
  (before relying on `HALT_ACK`) to carry zero `[STOP]`/`[HALT]`-subject entries at the scanned,
  unread, top level. Acknowledged with `HALT_ACK=1` (the documented, non-audited path for routine,
  non-STOP pending mail) and the checkpoint passed.
- `comp-tagauthz` pre-apply gate: `RESULT: none of the 0 candidate(s) carries a tag that ...
  default_tags ... would overwrite. safe-apply: comp-tagauthz gate PASSED.`
- tombstone gate: `CLEAN: no planned create matches a tombstoned resource.`
- Terraform: `aws_lambda_function.infra_monitor: Modifications complete after 6s`
- `Apply complete! Resources: 0 added, 1 changed, 0 destroyed.`

## 5. Before / after (AC1, read live, not assumed)

Pre-state (measured at the cut, matches the TO's own red-arm line exactly):
```
CodeSha256   r/bjjp5dJMcxw4NnzSNFsUCpYlWrH+sJsVJu+JiWxs8=
LastModified 2026-07-08T01:29:08.000+0000
CodeSize     40015
```
Post-state (measured live, this session, after the apply above):
```
CodeSha256   j7lljv8S5efk1KJz0Zh7+pV0+PIfcYbCOVJY2TE0/kE=
LastModified 2026-09-10T16:35:55.000+0000
CodeSize     54009
```
Both `CodeSha256` and `LastModified` differ from the pre-state. AC1 PASS.

## 6. AC2 / AC3 -- read from the DEPLOYED package, not the repo

AC2 (deployed zip downloaded from `Code.Location`, contents enumerated):
```
ENTRIES=4 PRESENT=3 of 3 MISSING=[]
```
PASS -- `edition.py`, `edition_rows.py` and `lambda_function.py` are all present in what AWS serves.

AC3 (same downloaded zip, every `.py` entry searched for the literal substring `ROW_FACTS`):
```
PY_ENTRIES=4 ROW_FACTS_CARRIERS=2 NAMES=['edition.py', 'edition_rows.py']
```
FAIL against the stated expectation of `ROW_FACTS_CARRIERS=0`. Filed as `NFRA_REPORT-Z-W3-S2`:
both carriers are docstring/comment/citation-string mentions of the specimen's data-structure name
(e.g. `edition.py`'s own module docstring states the specimen's fact list "do NOT travel here"; one
citation string is even rendered into the email's own REGION KEY to document where a quoted fact
traces to) -- neither file defines a `ROW_FACTS = [...]` literal (confirmed by a definition-scoped
search finding zero matches). The substantive bar (no embedded fact list ships) is met; the literal
criterion, as written, is not. Recorded honestly as FAIL, not rounded to PASS.

## 7. Change-management ledger

`org/critical_paths/change_management/infra-monitor-edition-wire-deploy-20260910.md` -- opened before
the first deploy act (the S3 put in section 3), closed in this same session/cell after the apply in
section 4 landed and was verified live in section 5. The live Lambda function moved cleanly from the
old code to the new code in one session; nothing was left half-landed.

## 8. What this record does NOT do

No alarm, topic, subscription, schedule or notification was created, modified or planned (section 4's
plan shows 0 add / 0 destroy, one resource updated in place). `infra-monitor.tf` itself is unmodified
by this cell -- the resource's `source_code_hash` / `s3_object_version` wiring already read from the
S3 object's metadata before this cell began; only the object's content changed. The EventBridge
trigger, the SES identity and the recipient list were not touched. `edition.py` and `edition_rows.py`
were not edited (RP-s-21 / RP-s-22's deliverables). `format_report` was not removed. Terraform was
never invoked directly -- every apply in this record went through the wrapper that runs the pre-apply
checkpoints first.
