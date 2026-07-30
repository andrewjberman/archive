# TF DEBT — RUNNING LIST (session tracker, append-only)

**Owner:** `0.7.0_AE_CloudOps` · **Opened:** 2026-07-30 · **Status:** LIVE, updated as the queue walk
continues.
**Andrew-direct, 2026-07-30 ~19:2xZ, verbatim:** *"if any of these things are persisted by terraform
as you note, there needs to be a scratchpad list where thats kept on file over the course of your
session so we can strategically fix the terraforms first and then get rid of the offending
resources."*

**Purpose:** one place that answers *"what Terraform must change before this resource can die?"* so
the TF repairs are batched and done FIRST, and the deletions follow. Rationale + traps + execution
order: `docs/briefs/terraform-fixes-before-decommission-20260730.md`.

**Legend —** `[ ]` open · `[x]` done (with evidence) · `[!]` blocked/needs a ruling.

---

## A. RESURRECTION HAZARDS — declared in TF, resource ALREADY deleted (fix regardless of any teardown)

- [ ] **A1** `opal-analytics-dashboard` — `infra/aws/terraform/shared-infra/s3.tf:89-97+` (bucket +
      versioning). Live: **404** (control `opal-data-assets` → 200). Q-12.
- [ ] **A2** `opal-cloudfront-logs-313476888478` — `shared-infra/s3.tf:37-57` (bucket + SSE + PAB).
      Live: **404**. Q-12.
- [ ] **A3** `opal-crawl-catalog` — `crawl-harness/main.tf:40-66` (bucket + PAB + versioning + SSE).
      Live: **404**. Q-22; found only by reading the declaration, not by name-grep.
- [ ] **A4** `orion-crawl-catalog` (DynamoDB) — already NotFound; verify no surviving declaration
      when A3's stack is destroyed.

> ⚠ **A1/A2 SANDWICH A LIVE RESOURCE:** `opal-cloudtrail-logs-313476888478` is declared at
> `shared-infra/s3.tf:63-83`, between them, near-identical block shape, **LIVE**. Remove by resource
> ADDRESS + named sub-resources. Never by line range or block pattern.

## B. STACKS TO DESTROY (authorized; ordering applies)

- [ ] **B1** `infra/aws/terraform/crawl-harness/` — **ENTIRE STACK.** Andrew-direct verbatim
      2026-07-30: *"I dont care about any of these crawl functions, all of it can go."* Manifest:
      instance + SG + 3 IAM roles/policies + instance profile + **4 SSM documents** +
      `dc2-test1-offpeak-harness` rule (applied, DISABLED) + target + A3. Plus **6 stale `tfplan.*`
      files** in that dir.
- [ ] **B2** `infra/aws/terraform/seeking-alpha/main.tf` — Q-15 chain. **D1 must precede.**
- [ ] **B3** `infra/aws/terraform/smartx-v2-bucket-lifecycle/main.tf:34` — a lifecycle stack whose
      entire subject is `opal-data-smartx-v2`; orphaned the moment the bucket dies. **C1 must precede.**

## C. CODE FIXES THAT MUST LAND BEFORE THE RESOURCE DIES (Lambda code = TF deploy, Rule 1)

- [ ] **C1** `infra/aws/lambda/smartx_ingestion_pipeline/compute_account_distribution.py:435-444` —
      drop the legacy compat write. Blocking: `smartx-account-distribution-daily` **ENABLED
      `cron(30 11)`** would fail daily once the bucket is gone.
      ⚠ **Do NOT touch `DISABLE_PORTAL_BELL_WRITE` (`:408-421`)** — live CTO guard (2026-07-23).
- [ ] **C2** `infra/aws/lambda/news_layer3_curation/lambda_function.py:52` — env-var DEFAULT
      `'opal-data-news-av'`. Inert today; lands on a deleted bucket if the var is ever unset.
- [ ] **C3** `data/canonical/schwab/build_canonical_daily.py:48, :141-146, :228` — reads the dead
      `opal-data-schwab/01_raw/`; **already silently resolves "latest" to the frozen 2026-07-15**.
      Under the 49F-deprecation ruling this is a **delete-candidate, not a repair-candidate** —
      confirm no other caller first.

## D. PRODUCERS TO STOP FIRST (ordering)

- [x] **D1** `seeking-alpha-news-daily` + `seeking-alpha-analysis-daily` — ~~ENABLED~~ **DISABLED
      2026-07-30 ~19:3xZ** under the Andrew-direct GO relayed by CTO (*"go ahead with the
      seeking-alpha teardown"*). **Evidence:** `describe-rule` → `State: DISABLED` on both, read back
      after the change; **positive control** `news-api-100pm` (untouched) still reads `ENABLED`, so
      the probe discriminates. The 107-day dead channel no longer fires. **Fully reversible**
      (`enable-rule`); nothing downstream removed.
- [ ] **D2** fred: **6 ENABLED rules / 2 functions** — `fred-data-ingestion` ×5 (`-daily` `cron(0 23)`,
      `-weekly`, `-monthly-early/mid/late`) + `fred-macro-ingestion-daily` `cron(30 23)`. Three are
      MONTHLY → invisible 27 days in 30.
- [ ] **D3** `smartx-account-distribution-daily` `cron(30 11)` — stop **after** C1.
- [ ] **D4** `dc2-test1-offpeak-harness` — applied, DISABLED; dies with B1.

## E. DANGLING IAM GRANTS (clean up AFTER deletion)

- [ ] **E1** `opal-data-news-av` grants — `news-pipeline/iam.tf` ·
      `shared-infra/lambda-execution-role.tf` · `market-overview/least-privilege-secrets.tf` ·
      `opal-assets/router_iam.tf` · `seeking-alpha/main.tf`.
      *(Note: the bucket itself is **NOT** `aws_s3_bucket`-declared anywhere — live-no-declared, so
      there is no bucket TF leg, only the stack + these grants.)*
- [ ] **E2** `opal-data-smartx-v2` grants — `shared-infra/opal-portal-lambda-role.tf` ·
      `shared-infra/iam_legacy.tf` · `opal-assets/router_iam.tf`.

## F. APPLIED AGAINST ITS OWN HOLD / STALE DECLARATIONS

- [!] **F1** `canonical-schwab-ec2/runner-trigger.tf:13-16` — carries a *"Do NOT apply until…"*
      banner and **is applied + ENABLED**, 0 fires/30d, no emitter anywhere. **Needs a ruling:** wire
      the emitter, or destroy rule + box + start-path IAM together.
- [ ] **F2** `infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1:557-561` — says
      `MonolithSchwabMetaPullsWrite` is "authored-not-applied"; **it has applied**, manifests land
      daily. Stale comment on a live grant.

## G. HYGIENE

- [ ] **G1** 6 stale `tfplan.*` artifacts in `infra/aws/terraform/crawl-harness/` (`tfplan.cat`,
      `.crawl`, `.ecltrim`, `.fork-c`, `.fork-c-iam`, `.forkb`) — remove with B1.

---

## NOT MINE — CTO's DynamoDB walk (tracked so the picture is whole; I have measured NONE of these)

- **Q-23** `opal-sessions` decommission — table + `opal-session-analytics` + 4 `/analytics/*` routes
  + portal ingest calls. Destructive step pending Andrew's GO at CTO's terminal.
- **Q-24** Terraform ALL globgrph resources (Andrew verbatim), incl. nessie catalog tables + the
  ECS→DDB derive gap.

## COVERAGE

**8 of 24 queue items walked** (Q-1, Q-2, Q-4 partial, Q-7 partial, Q-12, Q-13, Q-15, Q-16, Q-22).
**16 unwalked.** This list WILL grow — it is the running record; the brief is the reasoned snapshot.
