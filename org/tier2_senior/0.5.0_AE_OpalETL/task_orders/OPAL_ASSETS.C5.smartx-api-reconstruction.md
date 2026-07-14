# OPAL_ASSETS.C5 — The SmartX API reconstruction: raw JSON bronze off the LIVE REST path

<issued_to>0.5.0_AE_OpalETL</issued_to>
<issued_by>2.0.0_SA_COO (coordination lane, Andrew-direct ~01:07Z) — authored from PRD v1.3.1 §4 row C5 + §4a in full + §1 correction 2 + §3 rulings 2/7/8; architecture owner remains 1.0.0_SA_CTO</issued_by>
<date>2026-07-14</date>
<status>SUPERSEDED — by OPAL_ASSETS.C5.smartx-holdings-activity-etl.md (CTO-authored @ 9c7f234c0, Andrew-direct "give it to 0.5.0 now", GO'd 2026-07-14 ~04:10Z)</status>
<supersession date="2026-07-14 ~04:1xZ" by="2.0.0_SA_COO">
Andrew overruled the post-parity activation exactly as this TO's own activation clause anticipated ("if
Andrew overrules it comes through CTO" — it did: CTO authored + GO'd the successor on his word). The
SUCCESSOR TO is the operative spec: holdings-activity-grain, 8-feed map grounded on the yaliu HARs, the
Secrets-Manager auth-bundle requirement (Andrew-direct), the C2 distinct-landing conservation lesson baked
in as a required exercised guard, a DESIGN GATE to CTO before any scale-pull, and NOT-a-900s-Lambda for the
backfill. This file's §4a design content remains valid background reading; its ACTIVATION and SCOPE are
DEAD — do not execute from this file. ETF parity STILL OUTRANKS C5 for 0.5.0 (unchanged in both TOs);
the laptop stays ON.
</supersession>
<project>OPAL_ASSETS — Grand Consolidation P1–P2</project>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §4a (the design, verbatim authority) + §4 row C5 — authored against v1.3.8 @ a0ed08933; re-verify the §4a text at GO time (this TO is staged and the PRD is moving)</prd>

## Mandate

Andrew-direct (v1.1): **"reconstruct that entirely through the SmartX API endpoints."** Vendor egress:
SmartX is Andrew-LIFTED, recurring — **but the lift is on the WIRE, not the WORK**: this TO authorizes
pull + bronze + silver-inputs + internal cohort rows. See Boundary below for what it does NOT authorize.

Endpoint authority: `DATA_PLATFORM_D4_smartx_endpoint_sweep.md` (CVO PASS; fresh live exhaustion sweep
2026-06-24: 14 endpoints live, 21 confirmed-absent, GraphQL introspection-complete) + `data/smartx/API/`
(domain catalog, field dictionaries). Design lives in PRD §4a — it is the spec; this TO does not restate
what it can cite, it binds you to it.

## The bronze pull (PRD §4a, binding shape)

One Lambda cycle, daily, **≤17 calls/min** (~95 calls ≈ 6 min):
1. **Roster first, NEVER hardcoded:** `GET models` → live model list (11 today; 7 was the HAR-era count —
   the drift already happened once, and the current `smartx-rest-pull` hardcoding 7 models is the defect
   you are superseding). Chain `models/{modelId}` → `reportedModelId` — **TWO UUID SPACES** (D4 §4):
   calling holdings with a modelId 400s.
2. **Per model, land RAW JSON byte-for-byte** under `smartx/{model_short}/bronze/{feed}/{YYYYMMDD}/`
   (monolith grammar). **⚠ THE `{feed}` TOKEN TABLE IS NOT SPECIFIED — RATIFY BEFORE FIRST WRITE.**
   §4a names the ENDPOINTS but not the `{feed}` token each lands under, and bronze is never rewritten in
   place: an invented token becomes a permanent tree on the first write (the C4 lesson, 2026-07-14 —
   0.5.0's own catch). Before the first monolith write, submit your proposed endpoint→`{feed}` table
   through COO for CTO ratification. Asking costs zero; guessing costs a tree that never collapses: `models/{id}` · `models/{id}/performance?grouping=daily|weekly|monthly` (THE
   flow-adjusted return source) · `enterprises/aum?modelid=` · `enterprises/allocations?modelid=` ·
   `enterprises/advisors?modelid=` · `reportedmodels/{rmid}` · `reportedmodels/{rmid}/holdings`
   (snapshot-only upstream — **daily landing accrues the history SmartX does not keep**) ·
   `reportedmodels/{rmid}/changerequesthistory` · Surface B `models/performance?model_ids=` (monthly
   returns + risk stats).
3. **Platform scope** (`smartx/platform/bronze/…`): `models`, `reportedmodels`, `enterprises`,
   `benchmarks`, `accounts` collections. **GraphQL (compliance flags) and `users` are OUT** — not asset
   data.
4. **Raw means raw:** the response body AS RECEIVED, `.json`, no parquet, no field selection — the
   current pull's parquet-at-ingest defect (17a-class, §5 R8) dies here. Idempotent: skip-if-landed keyed
   on `{model}/{feed}/{date}`; `--force` rewrites; **an absent day is ABSENT** (no roll-forward, no
   zeros — the gap in the tree IS the record).
5. **THE COMPLETENESS LAW (PRD §2a) binds:** the FULL enterprise — all models on the roster, all
   allocations, all advisors, trade history, benchmarks — **not the 7 Opal cohorts.** A storage layer
   filtered to today's questions forecloses tomorrow's.

Silver is DS's C6 registry, not yours (vendor-bug handling lives THERE as parse rules — the mis-scaled
`totalAum`, the uniformly-"equity" `assetType`, the full-history `performance` dedup). Gold cohort rows
are C11 (DS). Your deliverable ends at verified raw bronze accruing daily.

## The retirement half (PRD §4a inventory — dispositions are RULINGS, not suggestions)

- `smartx-rest-pull` — **SUPERSEDE, do not patch.** Its consolidated-parquet output KEEPS FLOWING until
  P3 so the serving chain never blinks. You add the bronze pull beside it; you do not break it.
- `smartx-exporter` EC2 + Playwright scrape — **RETIRE, SEQUENCED:** inventory → REST parity attest →
  decommission. Deletion-class: the decommission itself needs explicit human confirm at that step.
- `smartx-daily-export-trigger` — **NEVER re-enabled** (§3 ruling 2). The census says its disablement
  was deliberate legacy retirement; "re-enable" would resurrect a superseded pipeline. Census vintage is
  2026-06-15 — RE-VERIFY LIVE FIRST (mandate below) but the working hypothesis flips the master plan's
  row-3 remedy.
- `smartx-jwt-refresher` — **KEEP.** Retire the `opal-data-bd` S3 JWT park (ruling 8; D4 §9.5
  firm-boundary flag): consumers repoint to Secrets Manager, which is ALREADY WRITTEN every run (§5 R8).
  The park retirement is a consumer repoint THEN a write removal — never a write removal first.
- `opal-smartx-ingestion-pipeline` — **KEEP UNCHANGED** (served/portal surface; out of consolidation
  scope; its input repoint is a later never-widen event, NOT this project).
- `smartx-model-monthly-pull` — **DO NOT REVIVE** (its data is IN the §4a pull; sidecar regeneration is
  portal-serving, flagged follow-on).
- `wsb_49f_smartx_model_aua.py` — **UNTOUCHED** ("No 49 Yet"). Record, do not build.

## Boundary (PRD §4a, functional not lexical — read twice)

The SmartX models ARE the 49F book's models, and "No 49 Yet" binds the BUILD of 49F gold runners. This
TO authorizes **pull + bronze + silver-inputs + internal cohort rows** (Andrew's consolidation mandate
names smartx explicitly). It does **NOT** authorize: `wsb_49f_smartx_model_aua.py` work · any mdpf
re-derive · any served/portal surface change · anything that would ADVANCE the held INF chain (the
functional test, every time). ⛔ Never compute a combined 0824+0833 total; never sum below gold.

## Fences

- Landing target depends on C1 (the monolith). Lambda deploy = Terraform only, via `safe-apply`, CTO
  apply gate; deps in Layers; source map updated; sized deliberately; tagged after 0-diff.
- JWT handling: the token exits `opal-data-bd` per ruling 8 — no new writes of secrets to ANY S3; Secrets
  Manager is the home.
- Rate discipline: ≤17/min is the vendor's ceiling — this is a standing-lift vendor relationship; do not
  be the reason it stops being one.
- NEVER rewrite historical bronze keys in place. Additive-only; `--force` is for a re-land of the same
  day, not a rewrite of history.

## <compiler_tools_mandate>
Phase 1 (before writing): **live re-verify BOTH trigger paths** — `aws events describe-rule` on
`smartx-daily-export-trigger` AND the rest-pull schedule + last-invoke timestamps (census is 2026-06-15
vintage — verify, don't trust; §4a mandate verbatim). `comp-blast` on the smartx lambdas you will touch.
Phase 2 (before commit): `.tools/commit-gate.sh` (automatic); `comp-iam service <pull-lambda>` after the
boto3 surface exists — necessary, NOT sufficient; the monolith is a new bucket and comp-iam FAILS GREEN.
Phase 3 (after CTO-gated apply): LISTING-BASED verification of landed raw objects per feed — ListObjectsV2
key + ETag + Size; head-object is never the acceptance instrument (CTO ruling 20260714T024205Z)
(denominators printed:
N models on the live roster × M feeds = expected objects vs landed); live simulate per 22a — one
`--resource-arns` per call, positive control separate.
</compiler_tools_mandate>

## <cross_domain_coordination>
- C1 (0.7.0) — landing target; your apply stacks behind his bucket + the SSE ruling.
- C6 (DS) — his parser registry consumes your bronze; the feed names + key grammar are the contract;
  coordinate BEFORE first landing, not after.
- C11 (DS) — gold cohort rows source from the silver your bronze feeds; the 7-model+platform cohort
  decoupling from frozen mdpf G1 only works if your landing is complete-per-the-roster.
- `opal-data-bd` — firm boundary; you touch it ONLY to retire the JWT park, consumer-repoint first.
- The ETF parity window (your own other lane) — C5 starts only after it closes; they never overlap.
</cross_domain_coordination>

## <acceptance_criteria>
1. Phase-1 live trigger re-verify quoted (both rules, states, last-invoke) BEFORE any build — if it
   contradicts the census hypothesis, STOP and route the contradiction (it changes ruling 2's premise).
2. Bronze accruing daily: for one full scheduled cycle, every roster model × every §4a feed lands raw
   `.json`, verified LISTING-BASED (ListObjectsV2 key + ETag + Size — never head-object, ruling
   20260714T024205Z), denominators printed (expected vs landed, per feed). Roster count read
   LIVE from `GET models` in the same cycle — not from this TO, not from D4.
3. Zero parquet under `smartx/*/bronze/` (17a) — quoted listing.
4. Idempotency exercised: same-day re-run lands 0 new objects, reports skip.
5. `smartx-rest-pull`'s existing output verified STILL FLOWING after your deploy (the serving chain
   never blinks — quote its post-deploy landing).
6. JWT park retirement: consumer inventory + repoint evidence BEFORE the S3 write is removed; the bd
   object gone only after.
7. Retirement sequence: inventory + parity attest documents committed; decommission NOT executed without
   the explicit deletion-class confirm.
8. Session log with Compiler Tools section. RAVC close to COO.
</acceptance_criteria>

## RAVC
ACK to COO on GO (not before — this TO is STAGED until the activation conditions above are met).
Evidence to COO. Apply gates, the SSE question, and any boundary call route to CTO through COO.
