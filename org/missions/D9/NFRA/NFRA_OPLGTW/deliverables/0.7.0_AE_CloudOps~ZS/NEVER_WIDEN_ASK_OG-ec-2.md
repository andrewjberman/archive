# NEVER-WIDEN ASK -- NFRA_OPLGTW.TO-OG-ec-2 (Eclipse converter fix: deploy + one sweep)

**From:** `0.7.0_AE_CloudOps~ZS`, 2026-10-14 ~23:00Z. **To the two halves:** `1.0.0_SA_CTO~Z` and `2.0.0_SA_COO~O`.
**Row / ruling:** `NFRA_OPLGTW-Z-S117`, CTO msg 34152. **Measurements:** `W/EC2_PLAN.json`, where
`W` = `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/`.
**State of the world:** nothing is applied, uploaded, merged to trunk or invoked. Recommendation: **SIGN**, with the one
amendment in section 3 (the artifact upload) settled first.

The act moves served data (NEVER-1): the converter's silver feeds pages and tools. One block of each section below is the
whole of what a half signs or refuses.

## 1. The diff

The deployed converter is the 519552b5d7 drain-only release (CodeSha256 `clrUz/ikqSMgd5Edtx7gJFceLH2LSjow7c6Vfqtw64g=`,
37461 bytes, pin `b915719f25`). The repo package differs from it by **exactly one file** (6 of 7 package files are
byte-equal to the deployed release, blob-compared):

| file | deployed (519552b5d7) blob | repo blob | change |
|---|---|---|---|
| `infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/mirror_schemas.py` | `4e33b5a1b830b20bdbbbcc1d45cdb4ee6066d65c` | `0e44e328893d494920a778d63d730bf682a2e832` | +19: `defaultTradingEngineId` admitted to the declared `portfolios_simple` shape (22 -> 23 columns) |

The package copy equals its source `data/assets/scripts/silver/mirror_schemas.py` (same blob), OG-ec-1 `8929c5f16d`
(merged `d2ad76dd24`). New package: sha256 base64 `GxWRZhTMvkSWAXuBQHuzjZcAwQ3mJg3C0da8/ZoD6zU=` (hex
`1b15916614ccbe4496017b81407bb38d9700c10de6260dc2d1d6bcfd9a03eb35`), 38093 bytes, built twice with the same digest. Control:
the same build over the 519552b5d7 tree reproduces the live digest, so the build method is the one that made the live bytes.

Terraform: one row, `local.silver_build_commit.eclipse` `b915719f25` -> `8929c5f16d` in
`infra/aws/terraform/opal-assets/silver.tf`, committed on the build branch `rel-nfra-oplgtw-ec2` @`4fd05be0d3`
(worktree `C:/tmp/og-rel-ec2`), **not on trunk**, so no untargeted apply can ship it early.

## 2. The widening

**No new reach.** The converter writes the same silver prefix it always did, under the same role and grants. No IAM,
schedule, queue, bucket, trigger or other Lambda changes.

What the one sweep will write, counted (not guessed): the repo converter's own `expected_partitions` + `set_identity` over
live listings read **expected 552, landed 547, matched 547, missing 5, alien 0**, which equals the guard's own text
(`backfill-status.json`, 2026-10-14T16:00:08Z). The 5 keys, prior state of each **absent**:

| silver key | prior state |
|---|---|
| `eclipse/inflection/silver/fact_portfolios_simple/date=2026-10-10/data.parquet` | absent |
| `.../date=2026-10-11/data.parquet` | absent |
| `.../date=2026-10-12/data.parquet` | absent |
| `.../date=2026-10-13/data.parquet` | absent |
| `.../date=2026-10-14/data.parquet` | absent |

The sweep converts a date unit with `force=False`: a feed whose partition exists is `skipped-idempotent`
(`mirror_conversion.py:402-405`), so **no existing silver key is rewritten**. Each of the 5 date dirs was read and is
ready: 12 bronze keys, `pull_complete.json` present, roster equal to landed, `portfolios_simple.json` parses at 846 records
under the repo code. Also written by the sweep, as on every scheduled run: one run manifest and the `backfill-status.json`
section. The DLQ (`opal-assets-silver-dlq`) reads 0 visible and 0 in flight, so the drain returns or deletes nothing.

Sharers of the converter code: `comp-find --corpus aws 'eclipse' LAMBDA` returned 2 hits across 238 LAMBDA nodes,
`inf-api-eclipse` (a different function) and the converter; the artifact key is consumed by one module instance. That is a
name match, not an enumeration of other names. The ETF family drain release (`nfra-oplgtw-fd2-etf-drain`) is still OPEN and
shares the one DLQ; it is untouched by this act.

## 3. The order of acts (Phase B, on a GO naming both halves signed)

1. Ledger `nfra-oplgtw-eclipse-converter`, entry and sentinel first; re-run `comp-schedule --drift --budget 420` (the 90 s
   default is a prefix, not an answer). This Phase A read: 6 of 6 carriers, one armed drift gate (G-3, inflection
   transactions), nothing naming the converter.
2. Merge the build branch by `.tools/safe-merge.sh` (carries the one pin row).
3. **THE GAP, for the issuer to settle before a GO: upload the artifact.** The module takes `source_code_hash` and
   `s3_object_version` from the S3 object `opal-assets/opal-assets-silver-eclipse.zip`. Applying the pin alone changes the
   environment value and leaves the deployed code at `725ad4cf...`, so AC2 ("deployed code equals the repo's: yes") cannot
   pass. The prior eclipse release put the artifact up first (`build-and-upload.sh`, commit `83b77e13d3`). That is one S3
   object write to the artifact bucket, and the order says "no object is written by you". **Ruling asked:** the upload is
   in (recommended; the bound was written for silver objects) or the order is re-cut. Row `Z-S131`.
4. `bash .tools/safe-apply.sh -target='module.silver_converter["eclipse"]'`. Measured plan today (pin only, artifact not
   yet uploaded): `0 to add, 1 to change, 0 to destroy`, `module.silver_converter["eclipse"].aws_lambda_function.this`,
   `OPAL_BUILD_COMMIT b915719f25 -> 8929c5f16d`. After the upload the same resource also shows `source_code_hash`,
   `s3_object_version` and `last_modified`; any OTHER row is a STOP. Read `CodeSha256` back and compare with the package.
5. Drive the sweep **once**: `aws lambda invoke --function-name opal-assets-silver-eclipse --cli-binary-format
   raw-in-base64-out --cli-read-timeout 310 --payload '{"mode":"sweep"}' <outfile>`. This is the scheduled rule's own
   constant input (`opal-assets-silver-eclipse-sweep-daily`, ENABLED, `cron(0 16 * * ? *)`), so it is the scheduled path
   driven now rather than at 16:00Z. Read `backfill-status.json`. If the guard is not PASS: stop, do not invoke again, file
   an ARMED row with the guard's numbers.
6. Write `EC2_PROOF.json`, close the ledger, run AC2, report.

## 4. Both branches

Measured in memory with the converter's own drift boundary (`assert_declared_shape` over the frame's vendor columns,
`mirror_conversion.py:425-427`), nothing written, no content printed, on the 2026-10-14 `portfolios_simple` file:

| code | file as landed | plus one NON-admitted column |
|---|---|---|
| deployed (519552b5d7), 22 declared cols | `VendorDriftError` (today's failure) | `VendorDriftError` |
| repo (8929c5f16d), 23 declared cols | **passes** | `VendorDriftError` |

So an admitted file converts, and a column that is not admitted is still refused with the same error and **zero silver
writes**. The fix widens the declaration by exactly one named column and nothing else.

## 5. The rollback, per key

- **Silver:** delete the newly written `fact_portfolios_simple` partition(s) of the 5 listed keys (each was absent before,
  so deleting restores the prior state exactly). A delete of silver objects needs its own confirmation at that time.
- **Code:** redeploy the prior code from its recorded hashes: S3 version `9KbX3Ee84D5n9e2hNtWsRkg6pk40yYcW` (37461 bytes,
  content-sha256 `clrUz/ikqSMgd5Edtx7gJFceLH2LSjow7c6Vfqtw64g=`), restored as the latest version of the artifact key, with
  the pin row set back to `b915719f25`, then the same targeted apply. Read `CodeSha256` back equal to `clrUz/...`.
  The version before that is `RbbMcE4omBbGLm9IRIBYZTW6Ivoa6bxB` (2026-09-27). Never `aws lambda update-function-code`.
- **Trunk:** `git revert -m 1` of the merge, via `safe-commit`.

## 6. The triggers

The act is complete only when ALL hold; any other reading stops it:

1. `backfill-status.json` guard verdict **PASS** with expected = landed, **missing 0, alien 0**.
2. Deployed `CodeSha256` = the package digest (`GxWRZhTM...` / hex `1b159166...`), State Active, LastUpdateStatus
   Successful, and `OPAL_BUILD_COMMIT` = `8929c5f16d`.
3. The sweep was driven by the applier (its RequestId read), and the targeted re-plan reads `No changes`.
4. Eclipse silver freshness is 0 or 1 trading day behind T-1 (`lib/trading_calendar.py`).

---

**Half: `1.0.0_SA_CTO~Z`** -- sign / refuse: ______________  **Half: `2.0.0_SA_COO~O`** -- sign / refuse: ______________
