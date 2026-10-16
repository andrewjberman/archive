# NEVER-WIDEN PACKET -- the Cottonwood reporting-publish function: the CODE UPDATE to publisher 0.4.0 (history_scope per account, its claim and basis) and the FULL REPUBLISH of the 939 Cottonwood series from the rewritten gold (IRPT_DASHBD round 149)

**Packet author:** 2.0.0_SA_COO~D2. **Date:** 2026-10-16 ~22:4xZ. **Applier:** `0.7.0_AE_CloudOps~IB2` (the one IRPT CloudOps lane, rule 34). **Halves:** the COO half and the CTO half, each bound to this file's sha256 (printed in each half). **Order:** `IRPT_DASHBD.TO-DB-b-315` (cut after both halves are signed).
**What this pair does, in one paragraph.** The Cottonwood landing rewrite is done and verified (`DB-b-308`, ten events, ledger closed): the gold now carries `history_scope` per account by the first-row rule. The published Cottonwood series are still the old ones: 939 series, all `PARTIAL_HISTORY`, built by publisher 0.3.0, no claim. This pair moves the function `irpt-cot-reporting-publish-lambda` to publisher 0.4.0 and republishes the 939 series (same 1,878 keys, new versions). **Served output moves**, and this packet names what moves and counts it before the write (section 4).

## 1. The acts (six, in order; each has its own stop)

**Act 1 -- build and upload the new bundle.** The applier builds `irpt-cot-reporting-publish-lambda` with `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-cot-reporting-publish-lambda` (source-map entry key; its `artifact_s3_key` `investor-reporting/irpt-cot-reporting-publish-lambda.zip` is read from the map, never typed). The build-only hash (section 2) is the base64 sha256 the real build must print, or STOP. The upload writes a NEW VERSION of the key (versioned; the current version `4wX9zhqX6x4x73i1vX1ADsXfv1LyDzRA`, 142,653 bytes, is the rollback target) and updates the entry's `artifact_sha256` only.

**Act 2 -- ONE `safe-apply` of `infra/aws/terraform/investor-reporting/reporting-publish-iso/`** (never a bare `terraform apply`, never `aws lambda update-function-code`). **The plan gate is exactly 0 to add, 1 to change, 0 to destroy:** `module.irpt_reporting_publish_iso.aws_lambda_function.this`, by CODE attributes only (the artifact version and the code hash move; memory 1,024, timeout 900, handler, runtime, role, layer, no reserved concurrency and no environment stay). Any other line STOPS. The daily schedule `irpt-cot-reporting-publish-daily` stays DISABLED and does not appear in the plan.

**Act 3 -- the PRE-WRITE READ and ONE synchronous DRY-RUN event `{}`.** (a) Before the dry run the applier runs this seat's read tool `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/reads/cot_publish_offline_diff.py` (`python -I`, from the worktree root; read-only; counts only) and records its printed counts as `pre_write`. **Expected exactly the section 3 figures** unless a landing has added a day since (then they move a little). **STOP before any write** if: any series flips FULL to PARTIAL_HISTORY; the flips to FULL exceed 150; any series changes `value`, `income` or `holdings_price_return` on a day both versions hold; the series with a changed `total_return_daily` on a common day exceed 800; or the tool reports a refused series. (b) The dry run `{}` (`RequestResponse`, `--cli-read-timeout 0`) reads and builds and writes nothing. **Expected:** `uploaded` false; `published` 939 and `refused` 40 (the first publish's counts; a different count is read, recorded, and STOPS only above the 10 percent refusal line); Max Memory Used at most 819 MB and duration at most 720 s. The dry run's `CodeSha256` read proves the new code is live.

**Act 4 -- ONE-ACCOUNT canary** `{"upload": true, "accounts": ["<one id>"]}`: the first account, sorted, whose new series reads `history_scope` FULL (so the canary shows the flip); the id is never recorded, only 12 hex of its sha256. Two objects at the SAME keys as before. **After-read:** the stored series validates against the bundled series contract; it carries `history_scope` `FULL`, `history_scope_claim` `inferred` and `history_scope_basis`; the manifest carries `publisher_version` `0.4.0`; the prior version of each of the two keys is still present.

**Act 5 -- the FULL republish** `{"upload": true}`: 939 series and 939 manifests overwritten with new versions at the same keys. `published` equals Act 3's; the prefix keeps 1,878 objects. **After-read (all 939):** every series carries `history_scope_claim`; the FULL count equals `pre_write` flips; no series changed `value`, `income` or `holdings_price_return` on a common day against its prior version; the prior version of every key is present; ten sampled series (by sorted position, as hash prefixes) pass the Act 4 checks.

**Act 6 -- the receipt** with the counts, memory and duration of Acts 3 to 5, the `pre_write` and after-read counts side by side, and the words "client-facing: the Returns-from sentence goes for the FULL series" and "the daily returns of the restated October days moved".

## 2. Pins

- Repository commit read by this seat: `cbf7ead020ffaed9f90b20afc6bc6ca73d8b1872` (branch `box/dell2`).
- `reporting-publish-cot/handler.py` blob `cf22aa388903`, sha256 `5acd0ac46523aba8dd512fd1f832018e51b94e69d3322aea693e219614eab174`; `reporting-publish/publisher.py` (publisher 0.4.0, packaged into this bundle) blob `3f43a0bb5ad7`, sha256 `e303c3072abd9ee7da2e33d3770fd4b0b2b6b1d21399ab7750b235965afef10f`.
- **Build-only hash** (BUILD_ONLY=1 at that commit, every gate run, nothing uploaded): base64 sha256 `vYNB1EBTU2qEIINxTnhYQBBBEHBYFId7lllrIJM3YRE=`, 144,186 bytes.
- The read tool `reads/cot_publish_offline_diff.py` and its record `reads/RD_COT_PUBLISH_OFFLINE_DIFF_20261016.json` are committed beside the packet.

## 3. Live state and the measured blast radius (read-only by this seat; the applier re-reads)

- Function `irpt-cot-reporting-publish-lambda`: `CodeSha256` `GagDGBNGmPsmYaJR1B7qG/TvaPdQU3LiVAh6c+wt6jo=`, 1,024 MB, timeout 900 s, handler `handler.lambda_handler`, layer `irpt-performance-native-layer:1`, no environment, last modified 2026-10-16T08:55:10Z, role `irpt-cot-reporting-publish-execution-role`; schedule `irpt-cot-reporting-publish-daily` DISABLED (`cron(30 9 ? * MON-FRI *)`, America/New_York).
- Published now (read by this seat): 939 series, every one `history_scope` `PARTIAL_HISTORY`, no `history_scope_claim`, publisher 0.3.0.
- **The new publisher run in-process over the rewritten gold, compared with the published series (MEASURED, counts only, no write):** 939 series differ (all gain `history_scope_basis` and `history_scope_claim`); **102 flip PARTIAL_HISTORY to FULL, 0 flip the other way**; 826 gain a newer day (`as_of`, `date` and the day's `value`, `income`, `holdings_price_return`, `return_basis`, `day_quality` extend); **on days both versions hold, `total_return_daily` differs for 657 series and `external_flow` for 659** (the restated October days of the rewrite, accepted by the CTO, msg 9487); `value`, `income` and `holdings_price_return` differ for 0; 118 series change their drawdown episodes; 0 refused. Record: `reads/RD_COT_PUBLISH_OFFLINE_DIFF_20261016.json`.

## 4. What each act changes in the world; the client-facing sentences this pair moves (count read before the write)

Act 1 adds an artifact version. Act 2 replaces the function's code. Acts 3 reads; Acts 4 and 5 overwrite served objects. **What a viewer of the Cottonwood Performance tab sees move, by count:** (1) **102 series** drop the sentence "Returns from <date>." (their history is FULL, not partial), and the others keep it; (2) **657 series** show a restated daily return on past days, so period returns that include those days move; (3) **826 series** end a day later (the newest landed day). No series changes `value`. The 40 refused accounts stay unpublished. These counts are read again by the applier in Act 3 before any write (section 1) and compared with the figures above.

## 5. Writers of the changed properties, counted

The function's CODE has ONE writer (the Terraform root `reporting-publish-iso` through `safe-apply`). The published OBJECTS have ONE writing rule (`publisher.py`, entered by the function) and ZERO enabled schedules (the daily schedule is DISABLED; 0 EventBridge rules target the function; `RD_IRPT_REPORTING_WRITERS_COUNT_20261016.json` @867d91f704), so only the named manual events write: N = 1 rule, entered by Acts 4 and 5 only.

## 6. Both branches

**Branch A:** every act returns what it states. **Branch B (a plan line outside the gate, a build hash that differs, a pre-write read outside its STOP lines):** STOP before the next act; the prior artifact version and the prior object versions are the rollback. **Branch C (memory or time):** a peak above 819 MB or an event over 720 s STOPS, no resize inside this pair. **Branch D (a refusal count above 10 percent in the dry run):** STOP before any write. **Branch E (a repeated Act 5):** same keys, acceptable.

## 7. Rollback, per key

Function: point the entry back to artifact version `4wX9zhqX6x4x73i1vX1ADsXfv1LyDzRA` through the Terraform root (`safe-apply`), never `update-function-code`. Objects: the bucket is versioned; for each of the 1,878 keys the prior version is the rollback; re-running the old publisher (0.3.0) after the function rollback republishes the old series. No object is deleted.

## 8. Conditions

1. **Ledger first,** bound to this packet's sha256 (`deploy_ledger.py open --slug irpt-dashbd-cottonwood-publish-hop2-scope-republish-20261016`, the applier named, legs git, build, terraform, pre-write read and dry run, canary, republish, receipt); `.open_deploys/` read across every live worktree with the denominator printed.
2. **Live state re-read at the moment of each act**; a difference from section 3 is recorded before the act.
3. **No act inside a landing fire:** none between 12:05 and 12:45 UTC on a weekday (the Cottonwood landing schedule), so the gold does not gain a day between the pre-write read and the republish.
4. **Stop at once** on a `Task timed out`, an `AccessDenied`, a Max Memory Used above 819 MB, or a count outside the STOP lines. Counts and words only, never an account id.
5. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version, no schedule change, no environment variable, no event other than the three named (`{}`, the canary, `{"upload": true}`).**

## 9. Questions for the CTO's half

1. Accept the republish with the three client-facing movements counted in section 4 (102 / 657 / 826)? 2. Accept the STOP lines of Act 3 as the guard on the counts? 3. Is the Cottonwood daily schedule's enabling its own later word (this seat's answer: yes, not in this pair)?

## 10. Not established, and so not covered

A `terraform plan` of this root with the new bundle; the function's run of the new code over the real gold (the dry run is the first); the figures of section 3 if a landing adds a day first; the Cottonwood filled report (hop 2 is 49 Financial only); enabling the schedule; any delete.
