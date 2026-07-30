# Per-resource ENRICHMENT pass — 0.7.0_AE_CloudOps annotations vs Andrew's semantic notes

**Mandate:** Andrew-direct 2026-07-30 ~20:0xZ via CTO, verbatim: *"go down the line through every
single resource, read my semantic note if there is one, and basically bring in an annotation of
their own on what they found per resource, how that enriches or contradicts what we notated
initially, then we review any refutations/contradictions."*
**Purpose (shapes what a good annotation is):** semantic substrate for the ontology — **C4 segments
and the C3 semantic verticals**. So the annotation that matters is *what business function this
serves and which vertical it belongs to*, not merely *is it alive*.
**Source of the notes:** `OPAL_WORLD_MODEL/20_rulings/SEMANTIC_NOTES/s3_buckets.md` (35 S3, fully
walked). **Method:** C-13 reader-over-writer · C-14 content-over-metadata · C-15 full bucket+key ·
positive controls run separately.

## ⚠ COVERAGE — READ BEFORE THE TABLE

**72 resources in scope (35 S3 + 37 DDB). ANNOTATED THIS PASS: 16 (15 S3 + 3 DDB, one shared).
NOT-ASSESSED: 56.** I annotated only what I actually investigated this session; the rest are named
as unassessed in §4 rather than silently skipped. **An unassessed resource is not a cleared one.**

---

## 1. CONTRADICTIONS — surfaced loudly, listed again here so they cannot be lost in the table

### C-A. `opal-data-news-v2` — the deletion gate has a **TWO-PLANE** answer, and the note assumes one plane

**Note #13, verbatim:** *"I'm guessing they have no consumers that surface on the portal frontend
and if so this should be deleted."*

**CONTRADICTS — the guess is wrong on the plane that matters.** The news-v2 *pipeline* is the
**live** news chain and it **does** reach the portal, just not through the bucket:

- `news-ingestion-scheduler` writes **both** `S3_BUCKET=opal-data-news-v2` **and**
  `DYNAMODB_TABLE=opal-news-articles`, on ~19 ENABLED rules/day. Newest bucket object today
  **18:00:59Z** (`logs/ingestion_20260730_180059_api-100pm.json`).
- `opal-news-articles` (289,414 items / 202 MB) is read by **`portal_data_proxy`** — the portal
  serving path — plus `sentiment_query_api`, `portal/lambda/sentiment-query.ts`,
  `news-trending-analysis`, `opal-news-layer3-curation`, `finbert_batch_processor`,
  `keyword_intelligence_generator`. **55 main-tree referencing files.**

**The precise finding, because the distinction is the whole point:** the *bucket* may hold only logs
and raw ingestion with no direct portal surface — that part of the guess may well hold. But
**deleting "this" cannot mean deleting the pipeline**, because the same producer feeds the DynamoDB
corpus the portal reads. **The gate must be re-scoped from a bucket question to a two-plane question**
(S3 artifacts vs the DDB corpus), or executing it takes down the portal's news surface.

### C-B. `opal-data-news-av` — *"the scraper pair lands there daily"* is FALSE; they land RECEIPTS

**Note #15** gates deletion on tracing the daily flow, describing the scrapers as landing there
daily. **CONTRADICTS the mechanism (and it makes the deletion EASIER, not harder).**

The channel **died 2026-04-14** and has written nothing but empty manifests for **107 days**:
today's `layer1_summary.json` reads `categories_scraped: 20`, **`news_urls_found: 0`** across all
twenty, `duration 1.379s`; `dedup_report.json` reads `urls_discovered: 0`, `scrapers_triggered: 0`.
Two-stage decay from the manifests: 04-10 → 382 URLs / 38.8s · 04-13 → 402 / 96.4s · **04-14 → 0** /
23.5s · still ~23s to 05-15 · **~1.4s from 06-15 on** (it stopped even trying). Newest real payload:
`news/articles/` **2026-04-13**, `analysis/articles/` **2026-02-23**.

> **This is `sdd-daily-pull.ps1`'s founding incident running live: "a pipeline that grades its own
> homework cannot report its own death."** The daily manifest write is what made the bucket look
> *active* to every recency instrument — including mine, six hours ago.

### C-C. `opal-data-mdpf` — CONDEMNED is right; **"dead" is not**

**Notes #8 / the condemnation** are about *purpose* (agentic slop, estimate mechanism condemned) —
and I am not re-adjudicating that. **CONTRADICTS only the operational read:** the bucket is
**written today on two prefixes** (`mdpf/feeds/non_model_aua/49financial/2026-07-30.parquet`
15:04:21Z; `telemetry/` 15:45:51Z) and `code/` is a **live Rule-12 artifact home** (07-29). Two
prefixes ARE genuinely cold: `cache/` (2026-05-19) and `bmkaud-evidence/` (2026-06-01) — the latter
reads as a **retention artifact**, which only Andrew can rule. **Dissolution is a migration design
with a live cutover, not a delete.**

### C-D. `opal-313476888478-globgrph` — essential infrastructure carrying an **unapplied destructive rule**

**Note #21:** essential infrastructure, C4 Estate Infrastructure, KEEP. **ENRICHES with a live
defect found by accident today:** `aws_s3_bucket_lifecycle_configuration.global_graph` has rule
**`ms-heat-snapshots-expire-60d`** — a **60-day expiration on `warehouse/ms_heat/snapshots/`**
(`shared-infra/s3.tf:360-369`) — **authored in the repo and NEVER APPLIED.** It surfaced as the only
change in an unrelated plan. **Anyone who applies `shared-infra` for any reason silently activates a
destructive-by-schedule retention rule on the world-model substrate.** Needs a ruling before *any*
shared-infra apply. I withheld mine on exactly this.

### C-E. `opal-data-trade-submissions` — the "dead since 01-21" read is refuted **at bucket grain**

**Note #14** correctly keeps it and flags the parquet batch-export leg. **ENRICHES:** the newest
object in the bucket **IS a submission** (`submissions/2026-07-20/TRADE-…/PFDE_Model_20260720.xlsx`,
27 objects total). The dead thing is the **parquet batch-export sub-prefix**, not the estate — the
note has this right and the queue's bucket-level framing does not.

### C-F. Four buckets were deleted and their **Terraform declarations survived**

Not a contradiction of a note — a contradiction of the *close-out*. Note §S3 CLOSE-OUT reports 7
deleted, archived, 404-verified. **Correct, and incomplete: the declarations outlived the
resources**, so the next `shared-infra` apply would have recreated three of them.
`opal-analytics-dashboard`, `opal-cloudfront-logs-313476888478`, **`opal-ci-staging`** (deleted by
CTO *this session*), and `opal-crawl-catalog` (`crawl-harness/main.tf`). **A deletion is not
complete until its declaration is gone.** Fixed for the first three today @`03aed078e9`.

---

## 2. S3 ANNOTATIONS (15)

| # | Resource | My annotation — function, vertical, what I measured | vs note |
|---|---|---|---|
| 2 | `opal-data-assets` | The convergence target, and **already receiving**: `schwab/{0824,0833}/` is a full per-master medallion, written twice daily by the SI2 box (`-Target monolith` default) and converted by `opal-assets-silver-schwab` (155 inv/7d, 0 errors). **Vertical: partner-data SSOT / 49F.** | **ENRICHES** — migration is further along than "mid-migration" implies on the schwab limb |
| 11 | `opal-data-schwab` | **THE CONNECTION CHECK IS ANSWERED: no live write path from the box.** The "autoschwab box" is **`quartz-si2-spike` (Windows, RUNNING)** — *not* `canonical-schwab-runner` (Linux, stopped, a build orchestrator). Its live path is `-Target monolith` → assets; the staging path is an escape hatch no schedule passes. Its `opal-data-schwab` write grants were **removed** (WP8 CELL-4). Residual readers: bd-* gold, `build_canonical_daily.py`, anonymizer. **Vertical: 49F partner data (legacy).** | **ENRICHES + closes the gate the note ordered** |
| 12 | `opal-data-smartx-v2` | One live daily writer only: `views/account_distribution.json` (**$1,545,435,404.69 AUM, 7,613 accounts**, 11:30:38Z) — a **self-declared legacy compat write** (`compute_account_distribution.py:83-86`) whose PRIMARY portal output is gated off by CTO's `DISABLE_PORTAL_BELL_WRITE`. Everything else froze 2025-12-26 → 2026-06-01. **Vertical: Model Portfolios (post-migration debris).** | **ENRICHES**; gate (b) code-archive **dropped by Andrew 19:2xZ** |
| 13 | `opal-data-news-v2` | See **C-A** — live pipeline, portal reaches it via DDB not S3. **Vertical: Market Intelligence.** | **CONTRADICTS** |
| 15 | `opal-data-news-av` | See **C-B** — dead 107 days, receipts only. **NO live S3 consumer** (41 refs: producers, stopped EC2, archived tooling, a stale docstring, an env-default). **Vertical: Market Intelligence (defunct).** | **CONTRADICTS mechanism, CONFIRMS verdict** |
| 8 | `opal-data-mdpf` | See **C-C** — 5 prefixes, 3 live / 2 cold. **Vertical: Model Portfolios.** | **CONTRADICTS the operational read only** |
| 19 | `opal-market-update` | Zombie-flow confirmed (written today 14:01:16Z, `fred/metadata/`). **ENRICHES THE SCOPE: the stop-first limb is SIX ENABLED rules across TWO functions** — `fred-data-ingestion` ×5 (daily + weekly + 3 monthly) and `fred-macro-ingestion-daily`. Three monthly cadences ⇒ **invisible 27 days in 30**. **Vertical: Market Intelligence.** | **ENRICHES** |
| 14 | `opal-data-trade-submissions` | See **C-E**. **Vertical: Trade Submission (C4 interactive product).** | **ENRICHES** |
| 16 | `opal-data-pm` | 87 objects / 253.8 MB, newest `PFDE/processed/20260720.json` (07-22). Reader census **NOT run** — the limb that decides the twin question. **Vertical: Portfolio Management (C4).** | NO-CHANGE (partial) |
| 17 | `opal-data-portfolio` | **6 objects / 82 KB**, newest `PFDE/PFDE_trades_20260721_145227.xlsx` (07-21). Size asymmetry vs #16 is *consistent with* the deprecated-twin hypothesis but **does not confirm it** — a 6-object bucket 9 days old is the low-frequency cell. | NO-CHANGE (partial) |
| 21 | `opal-313476888478-globgrph` | See **C-D** — unapplied 60-day expiration on the substrate. **Vertical: Estate Infrastructure (C4).** | **ENRICHES — live defect** |
| 30 | `opal-ci-staging` | Deleted by CTO this session; **declaration survived** in `shared-infra/s3.tf` (bucket + SSE + PAB, all three in state). Removed today. Dangling: `aws_iam_role_policy.github_actions_opal_deploy_ci_staging_s3` still grants on the dead ARN → logged **TF-debt E3**. | **ENRICHES (C-F)** |
| 33 | `opal-crawl-catalog` | Declaration survives at `crawl-harness/main.tf:40-66`; bucket **404**. Its writer `orion-crawl-harness` (`i-010f195f1798b40ad`) is **stopped**, its DDB sibling `orion-crawl-catalog` is **NotFound**, and **zero triggers** reference it. Andrew ruled the whole stack goes. **Vertical: DATA_PLATFORM recon (retired).** | **ENRICHES (C-F)** |
| — | `opal-analytics-dashboard` | 404; declaration + 5 sub-resources removed today. | **ENRICHES (C-F)** |
| — | `opal-cloudfront-logs-313476888478` | 404; declaration + 2 sub-resources removed today. ⚠ **`opal-cloudtrail-logs-313476888478` is declared BETWEEN it and the analytics block, near-identical shape, and is LIVE.** | **ENRICHES (C-F)** |

## 3. DYNAMODB ANNOTATIONS (3 of 37)

| Table | My annotation | vs note |
|---|---|---|
| `opal-news-articles` | **289,414 items / 202 MB. THE live portal news corpus** — read by `portal_data_proxy` + 7 others. **TWO writers, and the live one is `news-ingestion-scheduler`, not seeking-alpha** (whose contribution has been **zero for 107 days**). **MUST NOT be deleted with the Q-15 teardown.** **Vertical: Market Intelligence → portal serving.** | **ENRICHES — the load-bearing distinction of the whole teardown** |
| `seeking-alpha-article-urls` | 50,648 items. **Chain-private dedup ledger.** Dies with the seeking-alpha chain; no external consumer found. | ENRICHES |
| `orion-crawl-catalog` | **NotFound** (positive control `opal-news-articles` → ACTIVE on the same probe). Already deleted; its writer box + stack survive it. | ENRICHES |

## 4. NOT-ASSESSED (56) — named, not silently skipped

**S3 (20):** `opal-data-bd`¹ · `opal-data-inf` · `opal-data-cot` · `opal-data-demo` ·
`opal-data-portal-v2` · `opal-data-imo` · `opal-data-etfs`² · `opal-data-astn` ·
`opal-market-data-v2` · `opal-313476888478-lambda-artifacts` · `opal-cloudtrail-logs-…` ·
`opal-cur-…` · `opal-mcp-audit` · `opal-mcp-athena-results` · `opal-313476888478-lambda-layers` ·
`opal-313476888478-terraform-state` · `opal-runner-shared` · `opal-infrastructure-snapshots` ·
`opal-schwab-d4-access-logs` · `opal-served-key-write-trail-logs` · `opal-website-backups` ·
`opalinvest-portal`.
¹ *partially:* the 49F silver chain lands at `opal-data-bd/schwab/silver/{7 tables}`, all at
`date=20260723`, and it is the source for the live daily `wsd-49f-partner-held-etf-daily` — the
**frozen-frontier decision pending at Andrew**.
² **BLOCKED BY GATE, not by budget:** the ETFS estate is untouchable until after the **Aug-1 14:00Z**
month-end fire.

**DynamoDB (34 of 37):** not enumerated this pass. CTO's Q-23 (`opal-sessions` + `opal-session-
analytics`) and Q-24 (globgrph/nessie tables) are **theirs**, not mine — I have measured neither and
claim nothing about them.

---

## 5. WHAT THIS PASS SUGGESTS FOR THE ONTOLOGY

1. **Verticals are cleaner than buckets.** *Market Intelligence* spans `news-av` (dead), `news-v2`
   (live), `opal-news-articles` (the actual corpus), and `market-update` (zombie) — **four resources,
   one vertical, four different lifecycle states.** A per-bucket ruling cannot express that; a
   vertical can. This is the strongest argument I hit for the C3 layer being the right unit.
2. **The recurring instrument failure is a MISSING EDGE, not a wrong value.** Every contradiction
   above came from a *consumer* or a *content read* the instruments never took — never from a
   metric being wrong. `is-it-read` (C-13) and `is-it-producing` (C-14) are the two edges worth
   building into the substrate.
3. **Declaration and resource are separate objects with separate lifetimes.** Four instances today
   where one outlived the other. If the ontology models only live resources, it structurally cannot
   see a resurrection hazard.
