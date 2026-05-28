# ADVI_INFMVP.F3 — Keyword instant-analysis popup (MKOV_DLYCLD async-precompute rollup) (pod 0.1)

**Project:** [ADVI_INFMVP](../../../projects/ADVI_INFMVP.json)
**PRD:** `docs/architecture/ADVI_INFMVP.md` v0.1 §3 F3 + `docs/architecture/MKOV_DLYCLD.md` (rolled up here) (commit 5f6018778)
**Pod:** 0.1.0_DS_MarketIntelligence (lead) + 0.7.0_AE_CloudOps (EventBridge/Lambda/TF) + RD/DE (consumer repoint)
**Lane:** pod 0.1 (DS lead for precompute logic; AE for schedule+cache infra; FE consumer = `portal/src/components/market-performance/TopicCloud.tsx`)
**Issued to:** 0.1.0_DS_MarketIntelligence
**Author:** 2.0.0_SA_COO 2026-05-28T~19:46Z (/drive — CTO NOVEL_PRD_READY handoff 19:45Z; MKOV_DLYCLD subsumed)
**Sizing:** Phase-0 investigation ~45-60min; Phase-1 build sized after Phase-0
**Authority anchor:** CTO PRD v0.1 5f6018778 + Andrew direct 2026-05-28 (keyword popup slow/not working; precompute it)

<status>in_progress</status>

## Phase-0 FINDINGS (DS 0.1 lead, 2026-05-28T~20:18Z) — precompute infra EXISTS; it's a bug, not a greenfield build

**Current path traced:** portal `KeywordSentimentModal.tsx` → `getKeywordIntelligence()` → `POST /v1/sentiment/keyword-intelligence` → `portal_data_proxy.get_keyword_intelligence` (cache-first: reads `opal-keyword-intelligence` DynamoDB keyed on `{keyword, generated_date=today-UTC}`; on MISS → live GPT + write-back). Precompute = `keyword-intelligence-generator` Lambda, **chain-invoked async by `news-trending-analysis`** (`news_trending_analysis:1590`) 2x/day after writing `keyword-sentiments.json`. Standalone EventBridge rule `keyword-intelligence-generator-daily` intentionally DISABLED (fallback). DynamoDB cache (not S3) is the artifact store.

**ROOT CAUSE (empirical):** generator calls **gpt-5.4 with legacy `max_tokens`** → 400 `use max_completion_tokens` on EVERY keyword. CloudWatch `/aws/lambda/keyword-intelligence-generator` 2026-05-28 = "0 written, 20 errors / 20 total". DynamoDB: 05-27=0, 05-26=0, 05-28=3 (live write-backs only). ⇒ cache effectively never populated ⇒ every popup click misses ⇒ slow live path (gpt-4o-mini, degraded vs intended gpt-5.4+web).

**FIX:** `max_tokens`→`max_completion_tokens` on both gpt-5.4 calls — committed `d73c281dd` → CLOUD `9e236e3ca`, ds-commit-gate PASS. DEPLOY (zip-rebuild + `terraform apply`, Rules 1-6) handed to 0.7.0_AE_CloudOps. Risk: `temperature=0.2` may be the next gpt-5.4 400 (flagged to AE for post-deploy verify).

**Cadence Q1:** already 2x-daily via chain-invoke; daily-default satisfied; no schedule change.

**Residual Phase-1 (small, COO-gated):** UTC today-partition cold-window in request path → latest-available-partition lookup (today → most-recent prior date) in portal_data_proxy (same class as FIND_INSURE.037). Post-deploy CVO verify on Inflection demo surface (AC3a/AC3d).

## Objective

The keyword/topic-cloud instant-analysis popup must **work and be fast**. Move the GPT analysis **off the request path**: precompute on a schedule (EventBridge) → cache to S3 → consumer (`TopicCloud.tsx`) pulls the ready artifact with graceful fallback. This folds in the previously-scoped-but-unimplemented **MKOV_DLYCLD** design — MKOV_DLYCLD is subsumed by this F3 (no separate MKOV decomposition).

## Phase 0 — confirm the current on-demand path (investigation-first)

1. Trace whether `TopicCloud.tsx` triggers a **live GPT call on the request path**, or whether `keyword_intelligence_generator` (or similar) **already precomputes** but isn't scheduled/consumed.
2. Identify: the trigger, the GPT call-site, and the consumer fetch.
3. Confirm cadence (MKOV_DLYCLD Q1) — surface to ws COO/Andrew if the refresh cadence is ambiguous (daily vs intraday). Default daily unless the consumer needs fresher.

## Phase 1 — async precompute (per CLAUDE.md deploy discipline)

4. EventBridge schedule → Lambda (precompute GPT analysis) → S3 cache artifact (date-partitioned key). **Terraform-only deploy** (Rules 1-6); source-map update (Rule 4); deliberate memory/timeout sizing (Rule 5); tag after 0-diff apply (Rule 6).
5. Repoint `TopicCloud.tsx` to pull the precomputed artifact with **graceful fallback** (last-good / loading state) when the day's artifact is absent.
6. Decommission the on-demand GPT-on-request path once the cached path is verified.

## Acceptance criteria (inherits MKOV_DLYCLD AC1-AC4)

- **AC3a.** Keyword popup loads from a **precomputed artifact** — near-instant, **no live GPT call on the request path**.
- **AC3b.** Graceful fallback (last-good or loading) when the day's artifact is absent — no hard error, no hang.
- **AC3c.** Schedule fires on the confirmed cadence; cache artifact lands at the documented S3 key; consumer reads it.
- **AC3d.** Verified working for the Inflection tenant demo surface specifically (this is why MKOV rolled into INFMVP).

## Dependencies

- Independent of F1/F2/F4/F5 (PRD §4 — F3 parallel).
- **MDPF_SCOPED overlap — RESOLVED 2026-05-28T~19:58Z (ws COO + CTO).** MDPF_SCOPED v0.1 landed (486da0470); CTO confirmed (PRD §6+§7 explicit) that MDPF_SCOPED does **NOT** touch the keyword-popup surface — it stays sole-owned by this F3. **The earlier COO-gate-before-Phase-1 hold is RELEASED:** proceed F3 Phase-0 → Phase-1 without an MDPF reconciliation gate. (The only ADVI↔MDPF shared primitive is firmAccess.ts + the partner-view pattern, which is F2/RD's surface, not F3's.) Still confirm cadence Q1 with COO before Phase-1 (that gate persists).

## Sequencing

1. ~15min: trace TopicCloud.tsx → GPT call-site → consumer; determine precompute-exists vs on-demand
2. ~15min: confirm cadence (Q1) + design cache artifact/key
3. **GATE: surface Phase-0 findings + MDPF_SCOPED-overlap check to ws COO before Phase-1 infra build**
4. Phase-1 build (EventBridge + Lambda + S3 + TF) after COO clears the overlap → RAVC2

## RAVC2 deliverable

`[RAVC2-Request] ADVI_INFMVP.F3 — keyword popup precompute` to ws COO. CC ws CTO. For Phase-0: interim findings MCP (current path + cadence + MDPF_SCOPED overlap assessment) before Phase-1. For Phase-1: TF apply 0-diff + tag + S3 cache verification + TopicCloud near-instant load evidence.

## Compiler tools mandate

- `comp-iam service <lambda>` for the new precompute Lambda's S3/secrets perms before deploy.
- `comp-transform schema-check TopicCloud` before the consumer repoint.
- Terraform-only deploy (Rules 1-6); `comp-pipescript deployed` MATCH before any production run.

## Cross-domain coordination

`<multi-lane/>` — DS (precompute logic) + AE 0.7 (EventBridge/Lambda/TF infra) + RD/DE (TopicCloud repoint). Coordinate the S3 cache key + artifact schema across DS↔AE↔FE. **Heavy MDPF_SCOPED overlap on the keyword-popup surface — COO-gate before Phase-1 build.**

## Notes

- MKOV_DLYCLD (`docs/architecture/MKOV_DLYCLD.md`, Phase 0/1) is **subsumed** by this F3 — its standalone decomposition is cancelled; execute its Phase 0/1 here.
- This is general-portal functionality rolled into INFMVP because it must work for the Inflection demo.

— ws COO /drive 2026-05-28T~19:46Z
