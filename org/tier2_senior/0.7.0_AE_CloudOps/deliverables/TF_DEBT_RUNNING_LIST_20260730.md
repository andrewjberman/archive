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

## ✅ AUTHORIZED PLAN OF RECORD (Andrew-direct 2026-07-30 ~19:4xZ via CTO, verbatim: *"yes im ok with these items from 0.7.0 you can approve them"*)

**Execution order is APPROVED. Everything below is authorized — no further GO is needed to start any
tranche. What IS required: take only what you can CLOSE, and if you hand off, hand off AT A SEAM.**

| Order | Tranche | Risk class | Ledger entry? |
|---|---|---|---|
| **1st** | **A1 + A2 + A3** (+ **B1** crawl-harness destroy — A3 is that stack's declaration leg, so sequencing them together is cleaner; + **G1** the 6 stale `tfplan.*`) | **PURE REPAIR — nothing dies** | no |
| 2nd | **T1** selective capture | additive, zero deletion | no |
| 3rd | **T2** 7 lambdas + DDB `seeking-alpha-article-urls` (bucket SURVIVES; **NOT** `opal-news-articles`) | inert compute (rules already disabled) | no |
| 4th | **T3** `news_layer3_curation:52` + deploy cycle — **MUST precede T4**, and stands on its own merit even if the bucket never dies | normal deploy | no |
| 5th | **T4** bucket + `seeking-alpha/main.tf` destroy + 2 EC2 + AMI-rotation keyword + **E1** grants | **IRREVERSIBLE** | **YES** — open at deploy-start, close at completion |

**T1 capture standard (adopted verbatim into the plan):** article payloads ONLY — `news/articles/`
through 2026-04-13, `analysis/articles/` through 2026-02-23. **SKIP** the 107 days of zero-manifests
and the debug/batches churn, **and say so in the report rather than capturing 82.8 MB to look
thorough.**

**Why these are the seams:** the right unit is the set of points where *stopping forever is still
coherent*. Each tranche leaves the estate consistent if it is the last thing that ever happens.

> ⚠ **THE ADJACENCY TRAP BINDS ON TRANCHE 1** — `opal-cloudtrail-logs-313476888478` is declared at
> `shared-infra/s3.tf:63-83`, **between A1 and A2**, near-identical block shape, and it is **LIVE**.
> **Remove by RESOURCE ADDRESS, never by line range or block pattern.**

**LANE FACT (CTO, structural — not a preference):** `infra/aws` is **AE-commit-only** and CTO's
session holds **denied destructive permissions** (a `delete-table` was refused twice on 2026-07-30).
**T2 and T4 require an AE seat regardless of who is supervising.**

**ROSTER CORRECTION (CTO, 2026-07-30):** RV-0058 (MSTR~Z) records the AE device-keyed-archive TO as
blocked because *"the 0.7.0 seat was killed at 1810Z."* That is a **stale-roster read of the
PREDECESSOR's kill** — this seat is live and is not a blocker on anything; that TO is **unparked**.

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

---

## A-SWEEP — ESTATE-WIDE RESURRECTION-HAZARD DETECTION (2026-07-30 ~20:3xZ, Andrew asked how to eliminate the CLASS)

**Denominator: 26 bucket names declared across 57 Terraform stacks vs 32 live buckets.**

**TWO REAL HAZARDS REMAIN** (both already-deleted buckets whose declarations survive):
- [ ] **A6** `opal-data-aaii-v2` — 404 live, still declared.
- [ ] **A7** `opal-market-data-v2` — 404 live, still declared.

Both appear in the S3 close-out's "7 DELETED this session" list, which is the same C-F pattern:
**the deletion was completed and verified; the declaration was not part of the delete.**

> 🚨 **THE SWEEP INSTRUMENT PRODUCED A FALSE POSITIVE ON THE MOST DANGEROUS BUCKET IN THE ESTATE.**
> `comm -23 declared live` reported **`opalinvest-portal`** as declared-but-absent. It is **LIVE** —
> HeadBucket returns 200, and it is present in BOTH files (`live.txt:32`, `declared.txt:26`). It is
> the **DEFAULT CloudFront behavior origin — the dashboard's front door** (note #35). Acting on that
> row would have removed the declaration for the live SPA shell.
> **Root cause: `comm` requires strict matching collation and silently mis-reports otherwise; the
> false positive landed on the LAST line of the live file.** Caught only by re-probing each candidate
> individually instead of trusting the set operation.
> **CONTROL: never act on a set-difference row without an individual live probe of that row.** The
> set operation is a CANDIDATE GENERATOR, never a verdict. Same class as the `grep -c` on an error
> message: the retrieval, not the pattern, is what needs the control.

**STILL UNSWEPT — the class is not S3-only.** The same declared-vs-live difference must be run for
DynamoDB tables, Lambda functions, EventBridge rules, SSM documents, and IAM roles. **A6/A7 are the
S3 slice only.**

## THE PROCEDURAL FIX — how the class stops being generated

**MEASURED TODAY: `terraform destroy` IS THE INSTRUMENT THAT MANUFACTURES THIS HAZARD.** On the
crawl-harness retirement, the moment the destroy completed, `terraform plan` read **20 TO ADD** — all
16 resources gone, all still declared, the stack primed to rebuild the entire estate including the
EC2 box on the next apply by anyone.

> **`terraform destroy` empties the STATE and leaves the SOURCE fully armed. It guarantees the
> window. The window is worst precisely because the resources are gone — so nobody is watching
> them — while the declaration is intact.**

**THE ZERO-WINDOW PROCEDURE (use this instead, for any retirement):**

1. **DELETE THE RESOURCE BLOCKS FROM THE `.tf` FIRST.**
2. `terraform plan` → reads **"N to destroy"** (terraform reconciles state against the reduced config).
3. `.tools/safe-apply.sh apply <plan>` (Rule 18).
4. **Source and state go clean in the SAME operation. There is no window at any point.**

This reaches an identical end state with **one leg instead of two**, and it is not a preference —
the two-leg path has an unavoidable armed interval and the one-leg path has none.

- [ ] **PROPOSED GATE (not built — proposing, not building):** a plan-time lint that fails any stack
      whose plan contains `to add` for an `aws_s3_bucket`/`aws_dynamodb_table` the estate has
      deliberately deleted. Andrew's standing moratorium bans alerts/monitors; a **GATE** is the
      sanctioned form (gates teach at violation time). **Needs Andrew's word before anyone builds it.**

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
