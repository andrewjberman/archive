# ADHOC.unmanaged-lambdas-adoption — Seven-Row Verdict Table

**Agent:** 0.7.0_AE_CloudOps~E · **Date:** 2026-08-04 · **TO:** ADHOC.unmanaged-lambdas-adoption (COO, CTO framework 170852Z + rider 170951Z)
**Census closed against:** CTO~B RCG cycle-3 Rule-1 finding (460/460 TF files scanned — seven live registered Lambdas with no Terraform anywhere).
**Method:** per function — live primitives (get-function-configuration + get-policy + list-rule-names-by-target + list-event-source-mappings + get-function-url-config + IAM role reads), CloudWatch 30d Invocations/Errors + last-log-event, comp-debris band (30d window, 196 lambdas), role RoleLastUsed. Adoption per NFRA_TERRAFORM-P2 (import + TF-adopts-live); **nothing deleted in-TO**.

## NAME-STEM CONFLATION GUARD (CTO rider 170951Z, verbatim)

'finbert (10-file TREE)' = dead, ARCHIVE evidence at CRO (RCG record) vs 'finbert-batch-processor (LIVE fn, finbert_batch_processor/ 1-file tree)' = THIS TO's adoption-or-decommission subject. Independent artifacts; NEITHER disposition reads onto the other — a reader who saw the RCG deliverable must not inherit "finbert is dead" onto the live function, nor read a KEEP as contradicting CRO's ARCHIVE.

## Verdict table

| # | Function | Live state (grounded 2026-08-04) | Discriminator inputs | Verdict | Evidence |
|---|---|---|---|---|---|
| 1 | access-anomaly-scanner | Active, py3.11, 256MB/60s, role lambda-access-anomaly-scanner-role; trigger: EventBridge `access-anomaly-scanner-schedule` ENABLED cron(0 * * * ? *) | comp-debris **HOT** (dormant 1d); 983 inv/30d, **353 errors/30d**; last log 2026-08-04T22:00Z; RoleLastUsed 2026-08-04 | **ADOPT** — done | security-ops module @`d27e3f9f63`+`fd5e98909`; 8 resources imported; plan "No changes" (`security-ops/plan-zero-diff-proof.txt`); source-map verified by read. **Routed finding AAS-ERR below.** |
| 2 | opal-bd-transaction-consolidator | Active, py3.12, 3008MB/900s, role bd-processor-lambda-role (SHARED); resource policy allows s3://opal-data-bd invoke (Sid `s3-backfill-trigger`) but **opal-data-bd notification config does NOT reference it** — permission is DANGLING, wired consumers are bd-allocation-processor / bd-gold-trigger / bd-silver-merge only | comp-debris **STILLBORN-OR-GUARD**; 0 inv/30d; last log 2026-02-09T16:09Z (~6 months); role heat (2026-08-02) is NOT evidence — shared role, heat is other bd fns | **DECOMMISSION-CANDIDATE** (dossier only, routed) | Dossier D1 below |
| 3 | cost-anomaly-scanner | Active, py3.11, 256MB/120s, role lambda-cost-anomaly-scanner-role; trigger: EventBridge `cost-anomaly-scanner-schedule` ENABLED cron(0 */6 * * ? *) | comp-debris **HOT** (dormant 1d); 120 inv/30d, 0 errors; last log 2026-08-04T18:00Z | **ADOPT** — done | security-ops module, same commits/proof as row 1 |
| 4 | finbert-batch-processor | Active, py3.11, 256MB/900s, role opal-portal-lambda-role (shared, already TF-managed in shared-infra); triggers: TWO ENABLED EventBridge rules `finbert-scoring-post-ingestion` (11x/day) + `-45min` (3x/day) | comp-debris **HOT** (dormant 0d); 420 inv/30d, 0 errors; last log 2026-08-04T22:10Z; **CRO consult 222913Z: KEEP** ("ENABLED production schedules firing daily into the live news sentiment stack... current tooling by the estate's own law; the 'last deployed 2026-01-03' is deploy-staleness, not deadness") | **ADOPT** — done | news-pipeline/finbert-batch.tf @`d27e3f9f63`; 8 resources imported; targeted plan "No changes" (`news-pipeline/finbert-adoption-plan-proof.txt`) @`4fc1d37cf`; untagged provider alias protects the zero-diff gate against module default_tags |
| 5 | schwab-anonymizer | Active, py3.11, 512MB/900s, dedicated role; **ZERO triggers of any kind** (no resource policy, no EventBridge rule, no ESM, no fn URL) | comp-debris **STILLBORN-OR-GUARD** (created 2025-12-23, zero invocations in window); NO log events at all in /aws/lambda/schwab-anonymizer; RoleLastUsed 2025-12-11 (~8 months) | **DECOMMISSION-CANDIDATE** (dossier only, routed) | Dossier D2 below |
| 6 | security-sweep-comprehensive | Active, py3.11, 1024MB/300s, role security-sweep-dedicated-role (tagged 2026-02-17 iam-remediation, tags preserved verbatim in TF); trigger: EventBridge `security-sweep-comprehensive` ENABLED cron(0 12 * * ? *) | comp-debris **HOT** (dormant 1d); 30 inv/30d (daily), 0 errors; last log 2026-08-04T12:02Z | **ADOPT** — done | security-ops module, same commits/proof as row 1 |
| 7 | sentiment_query_api | Active, nodejs18.x, 512MB/900s, dedicated role; sole trigger: resource policy for API Gateway `cxm5b58nme` — **that REST API NO LONGER EXISTS** (get-rest-api → NotFoundException) | comp-debris **STILLBORN-OR-GUARD**; 0 inv/30d; last log 2025-12-23T23:24Z (~7.5 months); RoleLastUsed 2026-01-02; **CRO consult 222913Z: NOT-RESEARCH-CURRENT** ("research consumes scored sentiment via the pipeline artifacts, not via this query API... my evidence supports DECOMMISSION-CANDIDATE DOSSIER; I do not assert dead") — serving check (mine): the only wired consumer is a deleted API | **DECOMMISSION-CANDIDATE** (dossier only, routed) | Dossier D3 below |

**CRO consult answers cited (both research-adjacent functions):** message `20260804T222913Z_4.0.0_SA_CRO_CONSULT_ANSWER` — finbert-batch-processor KEEP (grounded on docs/briefs/TRIGGER_GRAPH_AND_RUNTIME_MAP.md rows 10/17/248); sentiment_query_api no-research-consumer, coldness decides (it decided: cold + consumer deleted).

## Adoption mechanics (rows 1, 3, 4, 6)

- **NEW module `infra/aws/terraform/security-ops/`** (state key `security-ops/tfstate`, tag `security-ops-v0.1.0`): the 3 security/monitoring fns + dedicated roles + inline policies transcribed verbatim from live + AWSLambdaBasicExecutionRole attachments + rules/targets/permissions + log groups (retention unset to match live). 24 resources imported; **plan: "No changes" — import-then-plan-ZERO-DIFF proven**, hence NO apply was ever pending (DELTA=0 by construction). Provider deliberately carries no default_tags — that is what makes true zero-diff adoption possible.
- **news-pipeline/finbert-batch.tf**: finbert-batch-processor + 2 rules + 2 targets + 2 permissions + log group via an **untagged provider alias** (module default_tags would have forced a tags_all update onto every imported resource, failing the zero-diff gate). 8 resources imported; **targeted plan: "No changes"**. Tag `news-pipeline-finbert-adopt-v1`.
- Code managed outside TF (placeholder + `ignore_changes=[filename, source_code_hash]`, house pattern per trade-pipeline/bd-pipeline).
- Source map: all 4 entries updated (pipeline + adoption note) and **verified by READ** (json parse + field print) — not trusted to any updater (per the record-terraform-deploy blindness specimen).
- comp-iam gaps after the iam.tf authoring: 17 estate gaps, **zero touching the adopted four** (their policies are verbatim-from-live under which they run clean).
- One correction the plan itself caught: security-sweep-dedicated-role carries live tags (Created/ManagedBy/Purpose) my first authoring omitted — transcribed rather than stripped.

## Routed finding AAS-ERR (not fixed in-TO; owner to be assigned by CTO)

access-anomaly-scanner is HOT but **36% of invocations error**: the scan works, the ALERT DISPATCH leg fails — hourly `Failed to dispatch alert: InvalidInstanceId ... SendCommand` against moltbot `i-0b784d4908e320fc4` (instance stopped or SSM-dark). **Access-anomaly alerts are currently being silently dropped.** Mechanism grounded on CloudWatch log read 2026-08-04 (two specimens, 22:00Z + 23:00Z). NOT an alarm-build request (moratorium respected) — this is an existing alert path, defective, surfaced as an owned finding. Same moltbot dependency exists in cost-anomaly-scanner's policy (same SSM target) — it shows 0 errors only because it presumably found nothing to alert on in-window; **the dispatch leg is untested-cold there, not proven-good**.

## Decommission dossiers (evidence only — routing to CTO; nothing deleted)

### D1 — opal-bd-transaction-consolidator
- Purpose (source read + Sid): S3-triggered consolidator for bd transactions, Sid `s3-backfill-trigger` — a backfill instrument.
- **The trigger is a dangling permission**: opal-data-bd's live notification configuration routes to bd-allocation-processor / bd-gold-trigger / bd-silver-merge only. Nothing can invoke this fn today except manual invoke.
- Cold: 0 inv/30d; last log 2026-02-09; comp-debris STILLBORN-OR-GUARD. Repo source exists (`infra/aws/lambda/bd_transaction_consolidator/`), source-map has a 2026-07-02 baseline sha (drift-reference only).
- **Caveat for the ruling:** shared role `bd-processor-lambda-role` is HOT (other bd fns) — any decommission must remove ONLY the fn + its dangling permission, never the role. comp-debris' own law: an abandoned half-build looks identical to a rare-event guard — a backfill tool may be kept-by-design. Recommend: CTO ruling with DS/bd-owner consulted.

### D2 — schwab-anonymizer
- **Zero triggers of any kind, zero log events ever retained, role unused since 2025-12-11.** Manual-invoke-only tool; no evidence it has ever run in the observable window.
- Repo source exists (`infra/aws/lambda/schwab-anonymizer/schwab_anonymizer.py`). Name suggests 49F Schwab PII anonymization — **guard-vs-stillborn genuinely undecidable from metrics** (a PII anonymizer can be a rare-event compliance instrument). Recommend: CTO ruling with the 49F/Schwab owner (AE base runs the /49-schwab-conv lane) consulted before any action.

### D3 — sentiment_query_api
- Sole wired consumer was API Gateway `cxm5b58nme` — **deleted** (NotFoundException). A Lambda whose only trigger points at a deleted API is unreachable by construction.
- Cold: 0 inv/30d; last log 2025-12-23; RoleLastUsed 2026-01-02; comp-debris STILLBORN-OR-GUARD.
- CRO (research seat, 222913Z): no current research consumer — research consumes scored sentiment via pipeline artifacts (DynamoDB/S3), not this API. CRO explicitly does not assert dead; the serving-side check above completes the picture.
- Strongest of the three candidates. 3.1MB nodejs bundle; repo source `infra/aws/lambda/sentiment_query_api/index.js`. Recommend: decommission ruling; if any future query API is wanted it would be rebuilt against the current serving stack, not this artifact.

## Ledger

Commits: `4c7e6d146` (TO pending) · `d27e3f9f63` (TF authoring + source map x4) · `fd5e98909` (security-ops zero-diff proof + role-tags correction) · `4fc1d37cf` (finbert zero-diff proof). Tags (local, integrator pushes per LD-0367): `security-ops-v0.1.0`, `news-pipeline-finbert-adopt-v1`. All commits lane-local on CLOUD, unpushed by design — **integrator (MSTR) push includes these + both tags (`git push --follow-tags`)**.
