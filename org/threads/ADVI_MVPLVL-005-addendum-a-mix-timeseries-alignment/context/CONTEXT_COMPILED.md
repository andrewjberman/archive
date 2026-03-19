# Thread Context (embedding-compressed)

Budget: 30,000 chars | Chunks: 58 of 318 | Score range: 0.038 - 0.582

---


## Source: `agents\0.4.2_RD_AdvisorIntelligence_commits.txt`


[score=0.444]

b331d3e6 feat(org): 0.4.0_DE_ClientPlatform — continuous view Max window clients fix task order
c08effac feat(org): 0.4.0_DE_ClientPlatform wave 2 — pod inventory + RD task orders
42f99352 logs: 0.4.2_RD_AdvisorIntelligence distribution nomenclature fix session log
2f8de475 docs(org): add xtick fix addendum for 0.4.2_RD_AdvisorIntelligence
4e046836 logs: 0.4.2_RD_AdvisorIntelligence xtick spacing fix session log



## Source: `agents\0.6.0_AE_PartnerETL_README.md`


[score=0.495]

# Agent 0.6.0_AE_PartnerETL — AWS Engineer

| Field | Value |
|-------|-------|
| **Agent ID** | 0.6.0_AE_PartnerETL |
| **Role** | AWS Engineer |
| **Title** | Partner ETL/Pipelines Engineer |
| **Tier** | 2 (Senior — Shared Services) |
| **Reports To** | 1.0.0_SA_CTO, 2.0.0_SA_COO |

---

## Pipeline Owned

| Pipeline | Terraform Module | Current Tag | S3 Backend |
|----------|-----------------|-------------|------------|
| BD (49 Financial) | `infra/aws/terraform/bd-pipeline/` | bd-v2.14.0 | ✅ |



[score=0.453]

| `infra/aws/ec2/EC2_MANIFEST.json` | Before touching any EC2 service — source of truth |

---

## Lambda Deployment Sequence

**Never skip or reorder steps.**

```bash
# 1. Write/modify Lambda source
#    infra/aws/lambda/bd-pipeline/{function-name}/lambda_function.py

# 2. Write/update Terraform
#    infra/aws/terraform/bd-pipeline/lambdas.tf (+ iam.tf, layers.tf, eventbridge.tf as needed)

# 3. Build zip and upload to S3
./infra/aws/terraform/bd-pipeline/build-and-upload.sh

# 4. Update source map BEFORE committing
#    infra/aws/lambda/ci/lambda-source-map.json



[score=0.434]

| Core document | `org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/pipeline_inventory.xml` |
| Session logs | `org/tier2_senior/0.6.0_AE_PartnerETL/logs/YYYY-MM-DD/` |
| Task orders | `org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/` |

---

## Mandatory Reading Before Any Work

> CLAUDE.md has the rules. These docs have the depth — layer creation gates, import steps, rollback procedures, EC2 parity tools, source map requirements. Read the relevant doc before starting, not after hitting a problem.



[score=0.427]

| Resource | Path |
|----------|------|
| Lambda source | `infra/aws/lambda/bd-pipeline/` |
| Terraform module | `infra/aws/terraform/bd-pipeline/` |
| Gold layer scripts | `data/black_diamond/scripts/gold/` |
| EC2 runner source | `infra/aws/ec2/bd-gold-layer-runner/` |
| EC2 detail generator | `infra/aws/ec2/bd-gold-detail-generator/` |
| Historical prices EC2 | `infra/aws/ec2/historical-prices/` |
| Source map | `infra/aws/lambda/ci/lambda-source-map.json` |
| EC2 manifest | `infra/aws/ec2/EC2_MANIFEST.json` |
| Layer manifests | `infra/aws/lambda/layers/` |



[score=0.357]

> Tag is authoritative from `infra/aws/terraform/bd-pipeline/CHANGELOG.json`. Cross-check before assuming MEMORY.md is current.

---

## Key Paths



## Source: `agents\0.6.0_AE_PartnerETL_logs\adhc_gldec2_05d_date_fix_deploy.md`


[score=0.582]

| Step | Action | Result |
|------|--------|--------|
| 1 | Commit 05d fix + task order + log amendment | `8805f31b` fix(bd-pipeline): 05d date mismatch |
| 2 | deploy-to-ec2.sh | 05d uploaded to s3://opal-data-bd/code/gold/ (16 scripts total) |
| 3 | EC2_MANIFEST.json updated | Deploy recorded |
| 4 | Verify data_date alignment | client_performance max=2026-03-11, silver/allocations/2026-03-11.parquet exists |
| 5 | Task order marked complete | ADHC_GLDEC2.001 status=complete |

## Verification

S3 gold script count after deploy: **16 scripts** (same count, 05d replaced in-place).



[score=0.509]

| File | Change | Committed |
|------|--------|-----------|
| `data/black_diamond/scripts/gold/05d_write_aua_certification.py` | data_date fix + LIABILITY_TYPES narrowed | Yes -- `8805f31b` |
| `org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/ADHC_GLDEC2.001.05d-date-fix-redeploy.md` | New task order, marked complete | Yes -- `8805f31b` |
| `org/tier2_senior/0.6.0_AE_PartnerETL/logs/2026-03-11/advi_pscfix_a1_aua_certification_deploy.md` | Amendment documenting both bugs | Yes -- `8805f31b` |
| `infra/aws/ec2/EC2_MANIFEST.json` | Deploy recorded | Pending |

---

## Blockers

None.

---



[score=0.508]

Expected result: `gold/aua_certification/2026-03-12.json` will be written on the 2026-03-13 nightly run (with data_date = 2026-03-12, matching silver/allocations/2026-03-12.parquet).

---

## Next Steps

1. **Verify after next nightly run** -- check that `gold/aua_certification/` is no longer empty:
   ```bash
   aws s3 ls s3://opal-data-bd/gold/aua_certification/
   ```
2. **Verify publisher consumed certification** -- check `gold/summary/header_metrics.json` for `display_aua` matching `certified_aua` (not gold_aua)



[score=0.496]

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

05d is deployed to S3 with both fixes. Next nightly EC2 run will:
1. Run 05 (client_performance) -- produces gold/client_performance.parquet with max date T-1
2. Run 05c (validation) -- validates gold vs silver
3. Run 05d (certification) -- derives data_date from client_performance, finds silver allocation, writes `gold/aua_certification/{data_date}.json`
4. Publisher reads certification JSON and overrides total_aua in all outputs



[score=0.494]

**Bug 1 (date mismatch -- CRITICAL):**
05d used `datetime.date.today()` -> `2026-03-12` (calendar date T). Silver allocations
are named for data date T-1 (`2026-03-11.parquet`). 05d checked for
`silver/allocations/2026-03-12.parquet` which never exists at run time. Hit SKIP every
night since deployment on 2026-03-11. `gold/aua_certification/` was empty -- publisher
always fell back to uncertified gold totals.

Fix: derive `data_date = max(date)` from `gold/client_performance.parquet`, use that
for both silver lookup and gold filtering. This is the actual data date (T-1).



[score=0.494]

data_date alignment confirmed:
- `gold/client_performance.parquet` max date: `2026-03-11`
- `silver/allocations/2026-03-11.parquet`: exists (uploaded 2026-03-12 17:51 UTC)
- Next nightly run: 05d will look for `silver/allocations/{max_date}.parquet` instead of `silver/allocations/{today}.parquet`

## Root Cause Summary (from CTO investigation)



[score=0.453]

# ADHC_GLDEC2 -- 05d Date Fix Deploy -- 0.6.0_AE_PartnerETL

**Date:** 2026-03-12

## Objective

Deploy the fixed `05d_write_aua_certification.py` to EC2. Two bugs were found by
1.0.0_SA_CTO during an AUA investigation: (1) date mismatch causing 05d to SKIP
every nightly run, (2) LIABILITY_TYPES over-excluding insurance accounts.

---

## Deployment Sequence



## Source: `agents\0.6.0_AE_PartnerETL_logs\advi_49fnv3_008_gold_silver_validation.md`


[score=0.558]

| 6 | Fix: use account_id explicitly for silver-gold join | `a4cbbf87` fix(bd-pipeline): 05c use account_id for silver-gold join |
| 7 | Redeploy to EC2 | 16 gold scripts re-synced |
| 8 | EC2_MANIFEST.json updated | Manifest commit `dca49ecf` |
| 9 | Re-run backfill | 33 dates validated, 3 ERROR (early schema mismatch) |
| 10 | Root cause investigation | Missing accounts + price divergence documented |
| 11 | Mark task order complete | ADVI_49FNV3.008 status=complete |



[score=0.534]

| Step | Action | Result |
|------|--------|--------|
| 1 | Write 05c_validate_aua_vs_silver.py | Script created with PASS/WARN/FAIL thresholds, --backfill and --date CLI support |
| 2 | Commit source | `4fd699f4` feat(bd-pipeline): add 05c_validate_aua_vs_silver.py |
| 3 | safe-ec2-deploy.sh bd-gold-layer-runner | 16 gold scripts in s3://opal-data-bd/code/gold/ |
| 4 | EC2_MANIFEST.json updated | Manifest commit `968d0cbb` |
| 5 | Backfill run (local, --backfill) | Bug found: account_number/account_id mismatch in join |



[score=0.524]

| File | Change | Committed |
|------|--------|-----------|
| `data/black_diamond/scripts/gold/05c_validate_aua_vs_silver.py` | New validation script | Yes -- `4fd699f4`, fixed `a4cbbf87` |
| `data/black_diamond/scripts/gold/run_gold_layer.sh` | Added 00 to incremental run | Yes -- `ada01ed1` |
| `infra/aws/ec2/EC2_MANIFEST.json` | Deploy recorded (x3) | Yes -- `968d0cbb`, `dca49ecf`, `2d12ff54` |
| `org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/ADVI_49FNV3.008.gold-silver-aua-validation.md` | status=complete | Yes -- `2bcc43e0` |

---

## Blockers

None.

---

## Current State



[score=0.520]

Spot-check 2026-03-09 (matches DE baseline exactly):
```json
{
  "gold_aua": 1604917844.0,
  "silver_aua": 1599225406.73,
  "gap_abs": 5692437.26,
  "gap_pct": 0.003559,
  "accounts_missing_from_gold": 83,
  "accounts_missing_mv": 14797305.67,
  "price_divergence_estimate": 20489742.93,
  "status": "FAIL"
}
```

Pipeline wiring: `run_gold_layer.sh` already had `if [ -f 05c ]` guard from PSCFIX A1 deploy.
05c runs after 05_build_client_performance.py, before 05d_write_aua_certification.py.

---

## Root Cause Analysis



[score=0.505]

# ADVI_49FNV3.008 -- Gold-Silver AUA Validation Pipeline -- 0.6.0_AE_PartnerETL

**Date:** 2026-03-12
**Start Time:** 15:35
**End Time:** 16:40

## Objective

Create and deploy `05c_validate_aua_vs_silver.py` -- a daily gold-vs-silver AUA
cross-check with PASS/WARN/FAIL thresholds, account-level gap decomposition, and
liability type breakdown. Backfill all existing silver dates. Investigate root causes
of the gold-silver divergence (missing accounts + price divergence).

---

## Deployment Sequence



[score=0.473]

| 12 | Add 00_build_accounts_dimension to incremental run | `ada01ed1` feat(bd-pipeline): add 00_build_accounts_dimension to incremental run |
| 13 | Deploy updated runner to EC2 | run_gold_layer.sh re-synced to S3 |
| 14 | EC2_MANIFEST.json updated | Manifest commit `2d12ff54` |

## Verification

S3 validation files: **33 JSONs** in `gold/validation/`



[score=0.463]

**Status:** COMPLETE
**Active branch:** `CLOUD`

`05c_validate_aua_vs_silver.py` is live in S3 (`s3://opal-data-bd/code/gold/`, 16 scripts total).
Wired in `run_gold_layer.sh` both modes (incremental + full) via `if [ -f ... ]` guard.
33 backfill validation JSONs written to `gold/validation/`. All dates show FAIL status due to
83+ missing accounts exceeding the 50-account WARN threshold. The aggregate gap for the most
recent date (2026-03-09) is +0.36% ($5.7M), decomposing into -$14.8M missing accounts and
+$20.5M canonical price divergence.



[score=0.432]

### (a) Missing Accounts: Stale accounts_dimension (18 persistent + growing onboarding gap)

**Finding:** `gold/accounts_dimension_latest.parquet` has `data_as_of_date = 2026-03-02` and
`account_open_date` max = 2026-02-26. Script `00_build_accounts_dimension.py` only runs in
**full mode** (monthly, 1st of month). Between full runs, new BD accounts accumulate in silver
allocations but don't appear in gold.

**Backfill trend (missing account count over time):**



[score=0.430]

**Fix applied:** Added `00_build_accounts_dimension.py` to the incremental (daily) run in
`run_gold_layer.sh` (`ada01ed1`). There was no good reason to exclude it -- the script reads
account metadata from transactions + allocations and is idempotent. New accounts will now be
picked up same-day instead of waiting for the monthly full run. The 83 missing accounts should
drop to near-zero after the next nightly run (the ~18 persistent ones from pre-2026 should
also get picked up since the script reads all transaction history + enriches from latest
silver allocations).



[score=0.429]

| Decision | Rationale |
|----------|-----------|
| Use `account_id` (not `account_number`) for silver-gold join | Both datasets have `account_id` (z-prefixed internal BD ID). Silver also has `account_number` (numeric external ID) but gold doesn't -- using it caused false 6300+ "missing" accounts |
| 05c runs via `|| true` (not `run_script()`) | Same pattern as 05d -- `run_script()` passes `--upload` flag, non-blocking requirement means 05c should never halt the pipeline |



[score=0.038]

## Decisions Made



## Source: `agents\0.6.0_AE_PartnerETL_logs\advi_pscfix_a1_aua_certification_deploy.md`


[score=0.538]

# ADVI_PSCFIX A1 — AUA Certification Script Deploy — 0.6.0_AE_PartnerETL

**Date:** 2026-03-11
**Start Time:** 22:45
**End Time:** 22:58

## Objective

Write and deploy `05d_write_aua_certification.py` into the BD EC2 gold runner per
task order ADVI_PSCFIX.A1. Script runs daily after 05c_validate_aua_vs_silver.py,
reads silver/allocations/{date}.parquet, excludes liability account types, and
writes `gold/aua_certification/{today}.json` — the certified_aua figure the
bd-portal-publisher Lambda uses to override total_aua fields.

---

## Deployment Sequence



[score=0.531]

`05d_write_aua_certification.py` is live in S3 (`s3://opal-data-bd/code/gold/`). EC2
will pick it up on the next gold pipeline boot. Script reads `silver/allocations/{date}.parquet`,
excludes 6 liability types (CreditCard, Mortgage, Loans, Insurance, TermLife, Annuity),
computes `certified_aua`, loads `gold/client_performance.parquet` for `gold_aua`, and
writes `gold/aua_certification/{date}.json`. Exits 0 on all paths. Wired in both
incremental and full modes after 05 (and after 05c when 05c is deployed). The publisher



[score=0.510]

**Fix:** Load `gold/client_performance.parquet` first, derive `data_date = max(date)`,
and use that for both the silver lookup and the gold filter. This is the actual data
date the pipeline processed, which matches the silver filename convention.

### Bug 2: LIABILITY_TYPES over-excluded Insurance/TermLife/Annuity



[score=0.509]

| Step | Action | Result |
|------|--------|--------|
| 1 | Read task order, PRD, EC2 runner structure | Context established |
| 2 | Write 05d_write_aua_certification.py | `data/black_diamond/scripts/gold/05d_write_aua_certification.py` created |
| 3 | Wire 05d into run_gold_layer.sh (both modes) | `data/black_diamond/scripts/gold/run_gold_layer.sh` modified |
| 4 | Commit source | `6223d2d9` feat(bd-pipeline): add 05d + wire into run_gold_layer.sh |
| 5 | safe-ec2-deploy.sh bd-gold-layer-runner | 15 gold scripts in s3://opal-data-bd/code/gold/ |



[score=0.506]

### Files modified

| File | Change |
|------|--------|
| `data/black_diamond/scripts/gold/05d_write_aua_certification.py` | data_date from client_performance max(date) instead of today(); LIABILITY_TYPES narrowed to 3 |

### Requires redeployment

05d must be re-uploaded to `s3://opal-data-bd/code/gold/` via `safe-ec2-deploy.sh`
before the next nightly run for the fix to take effect.



[score=0.502]

3. **Verify in next pipeline run** — after EC2 boots and incremental run completes:
   ```
   aws s3 ls s3://opal-data-bd/gold/aua_certification/
   aws s3 cp s3://opal-data-bd/gold/aua_certification/2026-03-11.json -
   ```
   Confirm certified_aua ~1.599B, gold_aua ~1.605B, gap_pct ~-0.36%.

**Files to touch next:**
- `data/black_diamond/scripts/gold/05c_validate_aua_vs_silver.py` — write per ADVI_49FNV3.008



[score=0.451]

05d used `datetime.date.today()` to determine the silver allocation filename. The EC2
gold pipeline runs on calendar date T, but silver allocations are named for the **data
date** T-1 (e.g. `2026-03-11.parquet` is uploaded on 2026-03-12). So 05d looked for
`silver/allocations/2026-03-12.parquet` which never exists at run time. Result:
`gold/aua_certification/` was empty — 05d hit SKIP on every single nightly run since
deployment. The publisher always fell back to uncertified gold totals.



[score=0.440]

**Do NOT:**
- Use `run_script()` for 05c/05d in the runner — those helpers pass `--upload` which these scripts don't accept
- Write scripts directly on EC2 — all changes go repo -> S3 -> EC2 pull

---

## Amendment — 1.0.0_SA_CTO (2026-03-12)

**Two bugs found in 05d_write_aua_certification.py during CTO AUA investigation.**

### Bug 1: Date mismatch — 05d always SKIPs (CRITICAL)



[score=0.439]

| File | Change | Committed |
|------|--------|-----------|
| `data/black_diamond/scripts/gold/05d_write_aua_certification.py` | New script | Yes — `6223d2d9` |
| `data/black_diamond/scripts/gold/run_gold_layer.sh` | 05c guard + 05d wired in both modes | Yes — `6223d2d9` |
| `infra/aws/ec2/EC2_MANIFEST.json` | Deploy recorded by safe-ec2-deploy.sh | Yes — `9bce21bd` |
| `org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/ADVI_PSCFIX.A1.aua-certification-script.md` | status=complete | Yes (this commit) |

---

## Blockers

None.

---

## Current State



[score=0.434]

| 6 | EC2_MANIFEST.json updated | Manifest commit `9bce21bd` |
| 7 | Mark task order complete | ADVI_PSCFIX.A1.aua-certification-script.md status=complete |

## Verification

S3 gold script count after deploy: **15 scripts** (was 14 before 05d).

05d confirmed uploaded:
```
s3://opal-data-bd/code/gold/05d_write_aua_certification.py
```

run_gold_layer.sh confirmed uploaded:
```
s3://opal-data-bd/code/gold/run_gold_layer.sh
```

---

## Decisions Made



## Source: `agents\0.6.0_AE_PartnerETL_logs\advi_pscfix_a3_script09_cert_override.md`


[score=0.495]

2. **[0.6.0_AE_PartnerETL] Complete ADVI_49FNV3.008** — write 05c_validate_aua_vs_silver.py
   (still pending; wired in run_gold_layer.sh with file-existence guard).

3. **Verify on next pipeline run** — check quarterly donut total:
   ```bash
   aws s3 cp s3://opal-data-bd/gold/partner_analytics/header_metrics_quarterly.json - \
     | python -c "import sys,json; d=json.load(sys.stdin); print(d['views']['aua']['current']['donut']['total'])"
   ```



[score=0.451]

| File | Change | Committed |
|------|--------|-----------|
| `data/black_diamond/scripts/gold/09_generate_partner_analytics.py` | Added `_load_aua_certification()` + cert load + current-period override | Yes — `f6fef305` |
| `infra/aws/ec2/EC2_MANIFEST.json` | Deploy recorded by safe-ec2-deploy.sh | Yes — `cc798d4d` |
| `org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/ADVI_PSCFIX.A3.script09-cert-override.md` | status=complete | Yes (this commit) |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD`



[score=0.432]

# ADVI_PSCFIX A3 — Script 09 Cert Override Deploy — 0.6.0_AE_PartnerETL

**Date:** 2026-03-11
**Start Time:** 23:45
**End Time:** 23:58

## Objective

Add `_load_aua_certification()` helper and current-period donut total override to
`09_generate_partner_analytics.py` per task order ADVI_PSCFIX.A3. When
`gold/aua_certification/{today}.json` exists, overrides `views.aua/geo/adv[current].donut.total`
with `certified_aua` in all three granularity JSONs (`header_metrics_quarterly/monthly/annual.json`).

---

## Deployment Sequence



## Source: `agents\0.6.0_AE_PartnerETL_logs\bd_pipeline_output_audit_onboarding.md`


[score=0.520]

### R1: bd-portal-advisor-publisher Audit

**File:** `infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py`

| Check | Result |
|-------|--------|
| OUTPUT_BUCKET default | `'opal-data-bd'` (line 35) |
| put_object calls | `Bucket=OUTPUT_BUCKET` exclusively |
| Output keys | `gold/advisors/{adv_id}/book.json`, `gold/implementor_leaderboard.json`, `gold/clients/{rel_id}.json` |
| opal-data-portal-v2 grep | ZERO MATCHES |

**Verdict:** CLEAN. Writes exclusively to `opal-data-bd/gold/`.

### R2: EC2 Gold Scripts Audit



[score=0.476]

| Step | Action | Result |
|------|--------|--------|
| 1 | Read recent logs (cache_control_ec2_gold_scripts, 5bed0dbf) | Context established |
| 2 | Grep OUTPUT_BUCKET + opal-data-portal-v2 in bd-portal-publisher | CLEAN -- zero portal-v2 matches |
| 3 | Grep OUTPUT_BUCKET + opal-data-portal-v2 in bd-portal-advisor-publisher | CLEAN |
| 4 | Grep S3_BUCKET across all active gold scripts (data/black_diamond/scripts/gold/*.py) | CLEAN -- all = opal-data-bd |
| 5 | Check EC2 user-data.sh (bd-gold-detail-generator) | Scripts from s3://opal-data-bd/scripts/gold_layer/ |



[score=0.455]

1. **[0.7.0_AE_CloudOps] Remove stale IAM permission** -- edit `infra/aws/terraform/bd-pipeline/iam.tf`
   line 375 to remove `arn:aws:s3:::opal-data-portal-v2/*` from the bd-pipeline Lambda role policy.
   Terraform apply, 0-diff confirm, tag bd-v{next}, push.

2. **[0.6.0_AE_PartnerETL] Verify s3://opal-data-bd/scripts/gold_layer/ contents** -- via AWS console,
   confirm which version of 11_generate_clients_tab.py lives at that prefix. If it references
   opal-data-portal-v2, replace with the current archive/11 version (which uses opal-data-bd).



[score=0.447]

| Script | S3_BUCKET | portal-v2 refs |
|--------|-----------|----------------|
| 00_build_accounts_dimension.py | opal-data-bd | NONE |
| 01_build_advisor_assignments_history.py | opal-data-bd | NONE |
| 02_build_positions_cube.py | opal-data-bd | NONE |
| 03_build_holdings_lots.py | opal-data-bd | NONE |
| 04_build_client_dimension.py | opal-data-bd | NONE |
| 05_build_client_performance.py | opal-data-bd | NONE |
| 05b_build_account_performance.py | opal-data-bd | NONE |
| 06_build_client_tax_liability.py | opal-data-bd | NONE |
| 07_build_nna_aua_by_geography.py | opal-data-bd | NONE |



## Source: `agents\0.6.0_AE_PartnerETL_logs\cache_control_ec2_gold_scripts.md`


[score=0.500]

| Step | Action | Result |
|------|--------|--------|
| 1 | Edit script 09 `write_s3()` at line 1616 | Added `CacheControl='public, max-age=300, s-maxage=3600'` |
| 2 | Edit script 10 `write_s3()` at line 911 | Same change |
| 3 | Upload 09 to `s3://opal-data-bd/code/gold/` | `aws s3 cp` — 71.3 KiB |
| 4 | Upload 10 to `s3://opal-data-bd/code/gold/` | `aws s3 cp` — 40.7 KiB |
| 5 | Commit | `5bed0dbf` feat(bd-gold): add Cache-Control to EC2 gold scripts 09 and 10 |
| 6 | Start EC2 `i-01003b035d2988dfb` | Gold pipeline ran with updated scripts |



[score=0.425]

```
gold/partner_analytics/header_metrics_quarterly.json: public, max-age=300, s-maxage=3600 | 2026-03-10 18:06:07 UTC
gold/partner_analytics/header_metrics_monthly.json:  public, max-age=300, s-maxage=3600 | 2026-03-10 18:06:25 UTC
gold/partner_analytics/header_metrics_annual.json:   public, max-age=300, s-maxage=3600 | 2026-03-10 18:06:43 UTC
gold/advisor_rolling_flows.json:                     public, max-age=300, s-maxage=3600 | 2026-03-10 18:07:28 UTC
```

---

## Decisions Made



## Source: `agents\0.6.0_AE_PartnerETL_logs\cache_control_publisher_deploy.md`


[score=0.486]

A follow-up task order to 0.6.0_AE_PartnerETL is needed to fix `09_generate_partner_analytics.py` and any other EC2 gold scripts that write directly to S3.

---

## Current State

> **Status:** COMPLETE (with gap documented above)
> **Active branch:** `CLOUD`



[score=0.472]

aws s3api head-object on gold/architect_leaderboard.json: public, max-age=300, s-maxage=3600  OK
aws s3api head-object on gold/clients_tab.json:          public, max-age=300, s-maxage=3600  OK
aws s3api head-object on gold/summary/header_metrics.json: public, max-age=300, s-maxage=3600  OK
```

## Deployment Tags

| Pipeline | Tag | Commit |
|----------|-----|--------|
| bd-pipeline | `bd-v2.17.2` | `0177c5e7` |

---

## Decisions Made



[score=0.443]

| 13 | Trigger publisher (write pipeline-complete.json) | Publisher ran at 17:15 UTC |
| 14 | Verify Cache-Control on S3 objects | `public, max-age=300, s-maxage=3600` confirmed |
| 15 | CloudFront invalidation | `IBBYOP4C74SMIF09VX049SQGKL` InProgress |

## Verification

```
aws s3api head-object --bucket opal-data-bd --key gold/timeseries_chart.json:
  LastModified: Tue, 10 Mar 2026 17:16:43 GMT
  CacheControl: public, max-age=300, s-maxage=3600  OK



[score=0.443]

1. **[Andrew] Verify in portal** — after CloudFront invalidation `IBBYOP4C74SMIF09VX049SQGKL` completes (~1-2 min), hard refresh the Advisor Intelligence page. The Network tab should show `Cache-Control: public, max-age=300, s-maxage=3600` in the response headers for `timeseries_chart.json`.
2. **[0.6.0_AE_PartnerETL] Fix EC2 gold script 09** — `09_generate_partner_analytics.py` writes to `gold/partner_analytics/` directly using boto3 without Cache-Control. Needs the same `CacheControl` parameter added to its `put_object` calls. Requires EC2 deployment protocol (repo -> S3 -> EC2 pulls).



[score=0.438]

| File | Change | Committed |
|------|--------|-----------|
| `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py` | Added `CacheControl=` param to `_save_json` put_object | Yes — `b9c483aa` |
| `infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py` | Same | Yes — `b9c483aa` |
| `infra/aws/lambda/ci/lambda-source-map.json` | Updated artifact_sha256 for both publishers; post-deploy fields | Yes — `b9c483aa`, `0177c5e7` |
| `org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/pipeline_inventory.xml` | Updated current_tag to bd-v2.17.2 | Yes — `0177c5e7` |



## Source: `agents\0.6.0_AE_PartnerETL_logs\drfr_ptmch_p3b_deploy.md`


[score=0.515]

| 18 | Fallback path performance finding | Timeout (300s) on gold/clients/ volume |
| 19 | pipeline_inventory.xml → bd-v2.18.2 | Updated |
| 20 | record-terraform-deploy + commit | `cf5117b0` |
| 21 | Tag bd-v2.18.2 + push | Pushed |

## Verification

```
aws lambda get-function --function-name bd-time-machine \
  --query "Configuration.{CodeSha256:CodeSha256,LastModified:LastModified}"

{
    "CodeSha256": "ECUBv/TTn8fmwdHNOH+HQ7f22ou3FBmjEBbU1x8/kX8=",
    "LastModified": "2026-03-10T22:40:48.000+0000"
}
```



[score=0.486]

| File | Change | Committed |
|------|--------|-----------|
| `infra/aws/lambda/bd-pipeline/bd-time-machine/lambda_function.py` | Bug fixes by COO at 233da228 (not this session) | Yes — `233da228` |
| `infra/aws/lambda/ci/lambda-source-map.json` | SHA256 updated for bd-time-machine | Yes — `dbff0093` |
| `infra/aws/terraform/bd-pipeline/iam.tf` | `s3:ListObjectVersions` → `s3:ListBucketVersions` | Yes — `2ab1e436` |
| `org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/pipeline_inventory.xml` | bd-v2.18.1 → bd-v2.18.2, last_deployed_commit updated | Yes — `97f49f4a` |



[score=0.450]

| Step | Action | Result |
|------|--------|--------|
| 1 | Verify bug fixes in working copy (4 criteria) | All confirmed in lambda_function.py |
| 2 | Build + upload bd-time-machine via PowerShell PS1 | SHA256: `ECUBv/TTn8fmwdHNOH+HQ7f22ou3FBmjEBbU1x8/kX8=` |
| 3 | Update source map + commit | `dbff0093` [skip ci] |
| 4 | terraform plan (bd-pipeline) | 0 add, 1 change, 0 destroy (code update) |
| 5 | terraform apply | 1 changed (bd-time-machine Lambda) |
| 6 | 0-diff plan | No changes |
| 7 | pipeline_inventory.xml → bd-v2.18.1 | Updated |
| 8 | record-terraform-deploy + commit | `8c794947` |



## Source: `agents\0.6.0_AE_PartnerETL_logs\gold_pipeline_staleness_investigation.md`


[score=0.564]

```
pipeline-complete.json: {"status":"success","mode":"incremental","timestamp":"2026-03-10T15:57:27Z","run_date":"2026-03-10"}
timeseries_chart.json: 29,703,340 bytes (2026-03-10 11:58:22)
client_performance.parquet: 74,145,300 bytes (2026-03-10 11:55:26)
advisor_rolling_flows.json: 111,644,942 bytes (2026-03-10 11:57:26)
Run log: s3://opal-data-bd/logs/gold-layer/gold_incremental_2026-03-10.log (21,069 bytes)
Publisher: Data as of 2026-03-06, AUA=$1,619,318,260, NNA_12M=$251,892,894
```

---

## Root Cause Analysis



[score=0.499]

| Step | Action | Result |
|------|--------|--------|
| 1 | Investigate S3 timestamps | `pipeline-complete.json` last written 2026-03-04, `timeseries_chart.json` 2026-03-06, `trigger-pending.json` 2026-03-09 |
| 2 | Check EC2 instance state | `i-01003b035d2988dfb` stopped, last launched 2026-03-09 21:51 UTC |
| 3 | Check EventBridge rules | `bd-gold-nightly-fallback` (Mon-Fri 23:00 UTC) and `bd-gold-layer-monthly-trigger` both ENABLED |
| 4 | Analyze bd-gold-trigger Lambda logs | EC2 started on 03-04, 03-05, 03-06, 03-09 but found "running" on subsequent triggers |



[score=0.487]

| 5 | Check silver layer freshness | Silver prices through 2026-03-08, transactions through 2026-03-06 -- upstream data is CURRENT |
| 6 | SSM diagnostic into EC2 | **ROOT CAUSE: systemd service `gold-layer-runner` is DISABLED** |
| 7 | Enable systemd service | `systemctl enable gold-layer-runner` via SSM |
| 8 | Start gold layer | `systemctl start gold-layer-runner` -- pipeline executed |
| 9 | Verify pipeline completion | `pipeline-complete.json` written 2026-03-10T15:57:27Z, run_date=2026-03-10, status=success |



[score=0.464]

# Gold Pipeline Staleness Investigation — 0.6.0_AE_PartnerETL

**Date:** 2026-03-10
**Task Order:** ADVI_49FNV3.004.gold-pipeline-staleness-investigation.md

## Objective

Investigate why `opal-data-bd/gold/timeseries_chart.json` had a last data date of 2026-03-02 despite the bronze/silver/gold pipeline being configured to run daily. Determine root cause and fix.

---

## Deployment Sequence



## Source: `agents\0.6.0_AE_PartnerETL_task_orders\infrastructure_inventory.md`


[score=0.487]

### Data Scripts (Bronze / Silver / Gold layers)
- `data/black_diamond/scripts/bronze/` -- raw data ingestion scripts
- `data/black_diamond/scripts/silver/` -- data cleaning and transformation scripts
- `data/black_diamond/scripts/gold/` -- 10 active gold scripts run sequentially (00 through 10)
  - Read each script to understand its role in the sequential pipeline

### EC2 Manifest
- `infra/aws/ec2/EC2_MANIFEST.json` -- BD gold layer runner service entry

### Deployment Tag
- bd-v2.14.0

## Deliverable XML Schema

Write your inventory using this structure:



## Source: `inline_notes.md`


[FORCED]

ALIGNMENT THREAD: DS + AE + RD must agree on the interface contract for Addendum A of ADVI_MVPLVL before task orders are written.

DS (0.4.0_DS_ClientPlatform) is the knowledge source -- built the classification pipeline and point-in-time composition endpoints. AE (0.6.0_AE_PartnerETL) owns the EC2 gold runner and will deploy the new gold script. RD (0.4.2_RD_AdvisorIntelligence) will wire Mix + Concentration timeseries charts into Books Tab L3/L4.

KEY FILES (use tools to read as needed):
- data/black_diamond/scripts/gold/05b_build_account_performance.py -- pattern for 06b (positions_cube x prices join, ThreadPoolExecutor)
- data/black_diamond/scripts/gold/06_build_client_tax_liability.py -- 06b goes after this
- infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py -- existing endpoints + where new ones go
- infra/aws/lambda/v2_portal/_shared/etf_classification.py -- _classify_holding pipeline
- portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx -- Books Tab L3/L4 drill
- docs/architecture/ADVI_MVPLVL_PRD.md -- full PRD (Addendum A starts at line 796)

GOLD ARTIFACTS (from PRD Addendum A2):
1. gold/client_mix_timeseries.parquet: (date, relationship_id, asset_class, market_value, pct) -- 5 classes: equity, fixed_income, structured_notes, cash, other
2. gold/client_concentration_timeseries.parquet: (date, relationship_id, asset_name, ticker, asset_class, market_value)

LAMBDA ENDPOINTS (from PRD A3):
- GET /api/scoped/partners/books/relationship/{id}/mix-timeseries?firmId=xxx -- returns wide-format {date, equity, fixed_income, ...} as pct
- GET /api/scoped/partners/books/relationship/{id}/concentration-timeseries?firmId=xxx -- returns top-N holdings per date

FRONTEND (from PRD A4):
- Stacked area chart for Mix timeseries at L3 (relationship) and L4 (account)
- Concentration chart linked to Mix: clicking asset class in Mix filters Concentration
- Same time window (1Y/3Y/Max) and granularity as AUA/NNA charts

DELIVERABLE: Agreed contract covering (1) gold artifact schema, (2) endpoint response shape, (3) chart data consumption pattern.




## Source: `refs\runall.sh-ec2-gold-runner-pipeline-order----06b-goes-after-06.sh`


[score=0.460]

#!/bin/bash
#
# Gold Layer Generation Pipeline
#
# Wrapper script that calls the optimized unified generator.
# Kept for backwards compatibility with EC2 user-data.
#
# Usage:
#   ./run_all.sh              # Dry run
#   ./run_all.sh --upload     # Production (upload to S3)
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================================================"
echo "GOLD LAYER PIPELINE (via unified generator)"
echo "Started: $(date -Iseconds)"
echo "======================================================================"

