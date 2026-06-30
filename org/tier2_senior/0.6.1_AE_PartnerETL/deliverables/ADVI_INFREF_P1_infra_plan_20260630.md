# ADVI_INFREF P1 — AE-infra PLAN (single-pull-layer EC2 + two-flow EventBridge)

**Author:** 0.6.1_AE_PartnerETL (inf-refactor AE lane) | **Date:** 2026-06-30
**For:** 1.0.0_SA_CTO arch-gate (RAVC) | **cc:** 2.0.0_SA_COO, 0.4.0_DS_ClientPlatform~A (scripts-lane counterpart), 3.0.0_SA_CVO (landed-artifact validation)
**Source authority:** ADVI_INFREF_PRD §1/§4/§5 · SPEC-1 §2/§3/§5 (bronze) · SPEC-4 §1/§5 (runtime) · COO decomp brief · CTO arch-gate criteria (msg 20260630T173703Z)
**Status:** PLAN — RAVC for arch-gate BEFORE build. No build action taken.

---

## 0. Thesis (source-confirmed `9ea447b3a`)

The recurring nightly freeze is the gold chain's **REDUNDANT inline perf re-pull** (`pull_inflection_performance_rest.py`) hanging on the Orion perf endpoint (103/41 min) BEFORE B_00 under `set -e`. Tactical fix is live (`timeout -k30 600 + tolerate` on every `INF_API_PULL_*`, `9ea447b3a`; served VERIFIED restored 17:20Z, $202.13M, data_as_of 06-30). **The structural fix = a single timeout-guarded pull per dim on `inf_gold_layer_runner` EC2** — once each dim is pulled exactly once, there is no redundant second pull left to hang the chain. This plan is the AE-infra half (runner/EC2/EventBridge/IAM); `~A` owns the pull/silver/gold SCRIPTS + catalog/chain composition.

## 1. Current state (grounded)

- **Runner:** `inf_gold_layer_runner` EC2 runs `data/inf/scripts/gold/orion-gold-dispatch.sh` (synced from `s3://opal-data-inf/code/{gold,silver,bronze,manual_api}/` → `/tmp` once at chain entry). c6i.4xlarge (per `merge_perf_report`). `~A`-owned shell.
- **Pull today is interleaved INTO the gold chain:** `CHAIN_FULL` carries `INF_API_PULL_{REPS,ASSETS_V2,NEW_PORTFOLIO,TXN,PERF,POSITIONS_DAILY}` steps mixed with silver + A/B/C/D (catalog L235-297, CHAIN_FULL L314). `run_script()` (L499-590) now wraps any `INF_API_PULL_*` in `timeout -k30 ${PULL_STEP_TIMEOUT:-600}` + tolerate-on-fail (the `9ea447b3a` band-aid).
- **9 cron pull λ pull the SAME dims in parallel** (`inf-api-{reps,assets-v2,positions,txn}`, `inf-{accounts-v2,unified-account-dim,tax,billing,performance}-daily`) — `tax/billing/unified_account_dim` are cron-ONLY; the rest are DOUBLE-pulled (cron CSV + inline). The inline-`_rest` path also double-WRITES perf+txn as own-prefix parquet (`bronze/{performance,transactions}/{date}.parquet`) — SPEC-1 §3.
- **Trigger:** single `inf-gold-trigger` λ is the chain dispatcher. `inf-canonical-prices-daily` cron (14:00 UTC) → `inf-gold-trigger {mode:"full",source:"cron"}` (FALLBACK; primary is event-driven via the silver-aggregator). `inf-jwt-trigger` (12:13 + 21:00 UTC) drives auth on the ISOLATED `inf-exporter` box.

## 2. P1-infra deliverables (build against CTO arch-gate criteria)

### D1 — Single-pull-layer on `inf_gold_layer_runner` (the keystone)
- Stand up a **dedicated pull STAGE** that runs at the FRONT of the chain: **every cataloged dim pulled EXACTLY ONCE**, each pull `timeout -k30 ~600s` guarded (carry the dispatch timeout onto every unified pull so no single pull can block the chain — generalizes `9ea447b3a` from band-aid to design). Raw-native land into `bronze/orion-api/{date}/` (JSON stays JSON, CSV stays CSV — no parquet at bronze; the 4-dim {positions,assets,performance,transactions} de-convert is `~A`'s script change, my infra carries the prefix/IAM).
- **Full cataloged surface, not today's 6+3:** the 3 cron-only dims (tax, billing, unified_account_dim) + the unpulled S1 surface (Trading/Models, Custom Reports, per-client Assets snapshot) move onto the EC2 pull-stage (SPEC-1 §4). Eclipse pull moves onto the SAME EC2 into the SEPARATE `bronze/eclipse-api/{date}/` domain (R5; two domains never share a prefix).
- **AE-infra scope here:** EC2 readiness for the heavier pull surface (instance-size/disk review for the full raw surface; watchdog grace-window unaffected); the run-stage ORCHESTRATION wiring is co-designed with `~A` (their `orion-gold-dispatch.sh`/catalog is the execution substrate). **`~A` owns:** the pull scripts, the de-convert, the catalog/chain edits, one-script-per-dim retirement.
- **Crons stay LIVE during P1/P2** (parallel-run, never-widen). The EC2 pull-stage stands up ALONGSIDE the 9 crons; decommission is **P3, AFTER the parity gate** — NOT this leg.

### D2 — EventBridge two-flow composition (single trigger path)
- **Full flow (KEEP):** `inf-canonical-prices-daily` cron → `inf-gold-trigger {mode:full}` → EC2 `--chain full`. It runs today and reaches B_00 via the timeout fix. Unchanged in P1 except it now front-loads the single-pull-stage.
- **Incremental flow (design, manual/future per SPEC-3 §6):** a second `inf-gold-trigger` mode → EC2 `--chain incremental` that **refreshes current-day B+C** (`INF_B_00..B_03 + C_00..C_09 --date={today}`) so `gold/canonical/holdings_{today}.parquet` is built every run and `INF_D_04.load_latest_holdings()` reads fresh + asserts `partition_date == data_as_of` (G-R1 Part-2, already co-signed `c76540ebe`). Wired but NOT armed as a cron in P1 (manual invoke); the nightly stays `--chain full`.
- **Single trigger path preserved:** all dispatch flows through the one `inf-gold-trigger` λ via its mode payload — no second dispatcher. The DLQ + retry_policy(0) on the fallback rule stays (no retry-storm).

### D3 — IAM (never-widen, live-grounded)
- The expanded pull surface adds NEW bronze prefixes (full orion-api dims + eclipse-api on this runner) and possibly new Secrets/endpoint reads. **Before any apply:** `comp-iam service` on the `inf_gold_layer_runner` instance role + `comp-iam gaps`, then **ground-truth on LIVE `aws iam get-role-policy`** (comp-iam DESIRED won't catch a declared-but-unapplied control; Rule 22). Add only the minimum S3 write (new bronze prefixes) + Secrets read needed — never-widen, no role sharing with the auth box.

### D4 — Honesty fix fold-in (infra-side, §8)
- `data_as_of` / "updated today" MUST reflect the true DATA date, never gold-run time. The value-logic lives in `INF_D_00` header build (`~A`); my infra fold = ensure the trigger/runner path doesn't re-stamp a fresh mtime as freshness, and (P4-adjacent) the served-vs-source parity alarm (comp-drift seam-7) so a frozen-value/fresh-label divergence alarms Sat, not Monday-by-Andrew. P1 carries the alarm SCAFFOLD; the alarm itself can ride into validation.

## 3. Lane boundary (with 0.4.0_DS~A)
| Owns | `~A` (scripts) | `0.6.1_AE` (infra) |
|---|---|---|
| pull scripts, de-convert, catalog, chain composition | ✅ | — |
| `orion-gold-dispatch.sh` shell logic | ✅ (co-review infra hooks) | co-design |
| EC2 instance/size/disk/watchdog, IAM role | — | ✅ |
| EventBridge rules, `inf-gold-trigger` λ, modes | — | ✅ |
| silver/gold value parity diffs | ✅ | — |
| deploy-ledger + safe-apply each infra leg | — | ✅ |

## 4. Out of scope for P1 (explicit)
- **P3 decommission** (9 cron λ + EventBridge rules + `inf-bronze-runner` + stubs + `inf_gold_qa_runner`) — later, ordered, deploy-ledgered, never-widen, AFTER parity gate.
- **P4 auth/OTP harden** — `inf-exporter` stays ISOLATED (R-Point 3; NOT folded). The Andrew-sovereign persistent-login directive reconciliation is the CTO+CVO loop at P4, FLAGGED here, NOT designed into P1.
- **Yahoo repoint** (§2) — gated on `~A`'s EG-2 per-consumer edge-check.

## 5. Sequencing & asks
1. **CTO arch-gate** this plan (the D1 single-pull-stage shape + D2 two-flow + D3 never-widen IAM posture).
2. Coordinate D1 execution substrate with `~A` (their dispatch.sh/catalog is where the pull-stage lands; I supply EC2/IAM/trigger).
3. Build per leg: code→TF→source-map→safe-commit→plan→safe-apply (HALTGT)→0-diff→tag `inf-v{X.Y.Z}`→push `--follow-tags`; **deploy-completion ledger opened-at-start/closed-at-completion** per leg (`org/critical_paths/change_management/`), never half-land.
4. CVO co-signs the LANDED artifact (deployed != resolved); parity-gated cutover before any P3 teardown.

**Open question for CTO/~A:** does the single-pull-stage land as a NEW front-of-chain stage in `orion-gold-dispatch.sh` (pull-all-then-build), or as a separate pre-chain pull script the trigger invokes before the gold chain? Both satisfy "one guarded pull per dim"; the first keeps one runner/one script, the second cleanly separates pull from compute. Rec: **front-of-chain stage in the existing dispatch** (one runner, one script, minimal disruption — PRD §1 silver "minimal disruption" ethos), with each pull individually timeout-guarded.

---

## 6. ADDENDUM — D3 IAM baseline grounding (read-only, `infra/aws/terraform/inf-pipeline/iam.tf`)

Captured the current `inf_gold_layer_runner` instance role (`inf-gold-layer-ec2-role`, profile `inf-gold-layer-profile`) as the never-widen "before":
- **`s3-scoped-inf`:** `GetObject/PutObject/DeleteObject/HeadObject/ListBucket` on `opal-data-inf` + `opal-data-inf/*` — **WILDCARD over the whole bucket.** ⇒ the expanded bronze prefixes (full `bronze/orion-api/{date}/` surface + `bronze/eclipse-api/{date}/` on this runner) are **ALREADY covered — NO S3 IAM widening needed for the pull-surface expansion.** Also covers the S3-mirror JWT read (`orion/jwt/current.json`).
- **`runner-shared-read`:** RO `opal-runner-shared/*` (telemetry profiler). **`ssm-access`:** `ssm:GetParameter*` (Resource `*`). **`cloudwatch-logs`** + **`cloudwatch-put-metric`** (namespace-scoped `Inflection/GoldChain`).
- **Net D3 surface is SMALL** — the only plausibly-new grants when the pull-stage expands: (a) `secretsmanager:GetSecretValue` IF the Eclipse pull / a new endpoint reads its token from SM directly rather than the S3-mirror the role already covers (TBD — confirm read-path with `~A` at build); (b) cross-bucket read IF the crawler-frontier ingests from `opal-crawl-catalog/`. **Build-time gate:** `comp-iam service`/`gaps` + LIVE `aws iam get-role-policy inf-gold-layer-ec2-role` ground-truth (Rule 22, not TF-DESIRED) once the dim list is fixed. This de-risks the apply: most of the "stand up the full pull surface" leg requires zero IAM change.
