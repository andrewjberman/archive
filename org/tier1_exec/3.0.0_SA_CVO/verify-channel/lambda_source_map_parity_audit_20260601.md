# Lambda source-map parity audit + compile-vs-aging assessment — 2026-06-01T1737Z

**Author:** 3.0.0_SA_CVO · **Trigger:** Andrew-direct ("refresh source map + analyze tf modules + code for parity" → "source map should be COMPILED, not written and aging; explore the opal compilers, are they batch-run, how accurate/comprehensive vs current state").
**Method:** independent read of `infra/aws/lambda/ci/lambda-source-map.json` (utf-8), `infra/aws/terraform/**`, disk lambda dirs, git mtimes, + Explore-agent inventory of the comp-* suite + deploy scripts.

## VERDICT
The source-map is **structurally written-and-aging, NOT compiled** — confirmed empirically. There is **no categorical compile/batch mechanism**; comp-* compilers are ad-hoc, never batch-run. Symptoms below are the direct consequence. **Recommend building a categorical source-map COMPILER** (scope at end).

---

## 1. Is there a compiler? (Explore-agent inventory)
- **NO categorical source-map compiler exists.** The map is hand-registered per-Lambda (CLAUDE.md Rule 4; the map's own `_note`: *"Add new functions when created"*). Deploy scripts derive only the *value fields* of **already-listed** entries: `build-and-upload.sh` recomputes `artifact_sha256` from a source-zip; `record-terraform-deploy.sh` sets `last_deployed_commit/at` via `git log`. **Neither enumerates source dirs to derive the entry set.** The strongest "compile-from-state" behavior is `build-and-upload.sh`'s ADHC_DRIFTD.002 guard (errors if a source `.py` isn't in `files[]`) — demands a human update, not auto-regen.
- **comp-* tools (26) are ad-hoc, never batch-run.** No CI job / hook / cron / orchestrator runs the suite. Catalog (`org/modules/graph/comp-tools.yaml`) is explicitly situational. Only 2 single-tool gates wired: `comp-pipescript deployed` (DS gold gate) + `comp-freshness` (pre-dispatch). `comp-iam` only READS the source-map.
- `.tools/lambda-source-map.json.new/.clean/.tmp` = **stale Feb hand-edit artifacts, unreferenced by any script** (delete-candidates).
- CI `lambda-deploy.yml` does a read-only drift check (zip-sha vs live AWS `CodeSha256`, `::warning::`) at deploy-time — a partial drift signal, but not an always-on categorical compile.

## 2. Comprehensiveness gaps (source-map vs disk + TF)
Source-map: **169 entries in `functions`** (13 `source_dir=EXTERNAL` by-design) + **7 MISLOCATED top-level keys**. Disk: 138 `lambda_function.py` dirs (+ node/mjs + variant-handler python lambdas not counted).

- **STRUCTURAL DEFECT — 7 entries mislocated as top-level JSON keys OUTSIDE `functions`:** `bd-incrparity-trigger`, `inf-portal-publisher`, `inf-portal-advisor-publisher`, `inf-client-detail`, `inf-gold-trigger`, `inf-otp-relay`, `inf-bronze-trigger`. These are real lambdas (e.g. inf-client-detail is TF-backed `inf-pipeline/iam.tf` with a `lambda_function.py`) but **invisible to every tool that iterates `m['functions']`** (build-and-upload, record-terraform-deploy, comp-iam) → no sha-refresh, no deploy-provenance, no IAM-gap check. Also a schema mismatch (handler/runtime/pipeline/s3_bucket/s3_key vs the standard files/artifact_*/last_deployed_*).
- **Rule-4 gaps — disk lambdas with NO source-map entry:** `seeking-alpha-dedup-coordinator` (**TF-backed `seeking-alpha/main.tf` — definitive gap, CI-drift-blind on a deployed lambda**); `market_query`, `smartx_query`, `trending_image_generator`, `security-sweep-daily` (no literal TF-ref + git-stale Jan–Feb → likely dormant/manual, but absent from the map either way).
- **Broken `source_dir`:** entry `seeking-alpha-analysis-scraper` points its `source_dir` at the **absent** `seeking-alpha-article-scraper` (real dir is `…-analysis-scraper`).
- **Provenance gap:** **42/169** functions entries have no `last_deployed_at`.
- (Noise excluded honestly: `daily_agenda_generator/package`, `portal_data_proxy/_build_tmp` are vendored/build copies, not distinct lambdas. The A-side "22 source_dir-not-a-py-dir" are almost all legitimate node/mjs lambdas + non-`lambda_function.py` handlers + data-script dirs.)

## 3. Accuracy / aging (the "written and aging" symptom)
- **14/126 provenance-bearing entries STALE** — source git-commit POSTDATES `last_deployed_at`: all 8 `find-insure-*` (deploy 05-28 < src 06-01, today's in-flight work), `opal-portal-data-proxy` (04-29<05-28), `keyword-intelligence-generator`, `inf-portal-advisor-publisher`, `shared-advisor-router`, `opal-partners-data` (04-17<05-05), `ycharts-market-data-pull`. **Caveat:** some staleness is *expected in-flight* (code edited, redeploy pending) — it is NOT necessarily a defect. The point: **the map gives no always-on signal; you must run this exact analysis to know.** A compiled/drift-checked map flags it automatically.
- **SM↔TF linkage incomplete:** **49/169 no `tf_resource`, 40/169 no `tf_file`** (~30% unlinked). GOOD: 0 declared `tf_file`s are missing on disk. Reverse: 19/46 TF `aws_lambda_function` resources unmatched by any SM `tf_resource` — largely EXTERNAL/edge/node + `tf_resource`-field-absent (partly matching-granularity, partly real).

## 4. RECOMMENDATION — a categorical source-map compiler
A new compiler (natural fit as a comp-* tool, e.g. `comp-lambdamap`) that DERIVES the map from current state, run as a BATCH (CI job / pre-deploy gate):
1. **Enumerate** all lambda source dirs across `infra/aws/lambda/**` + `infra/aws/lambda-edge/**` + EXTERNAL-declared — handle `lambda_function.py`, `index.mjs/js`, and variant python handlers.
2. **Parse TF** (`aws_lambda_function`) → derive `tf_file`/`tf_resource` for every lambda; flag TF-without-source + source-without-TF.
3. **Recompute `artifact_sha256`** from current source on demand → diff vs recorded + live AWS `CodeSha256` → emit drift (extends the partial `lambda-deploy.yml` check to always-on).
4. **Normalize structure** — single schema, no top-level-key misplacement (fixes the 7 mislocated entries by construction).
5. **Batch-run** so the map is generated, never hand-aged; CI fails on uncompiled-drift.

This is an infra-tooling architecture proposal: **ws CTO** (PRD/design) + **AE** (source-map/deploy mechanism owner) build it; ties to the comp-* compiler thesis (**CL CTO**). CVO delivers this audit + recommendation; build is CTO/AE lane. Routed Andrew (direct) + CTO + AE, CC COO + MSTR.
