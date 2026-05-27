# FIND_INSURE.008 — 99-IMO universe-run Lambda fan-out (C1 close)

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.4 §4 Phase 1 close gate (AC2 universe-scope mandate)
**Pod:** 0.7.0_AE_CloudOps~A
**Lane:** AE_CloudOps ~A (Phase 1 dispatch-orchestration tier)
**Issued to:** 0.7.0_AE_CloudOps~A
**Author:** 2.0.0_SA_COO 2026-05-27T~22:55Z (cycle 165 post-reboot Phase 1 close-gating triad)
**Sizing:** ~2-3h wall for 10-IMO validation subset + ~12-24h wall for full 96-IMO universe (Lambda async; observation window only)
**Authority anchor:** CVO /verify-channel verdict `54ace66c8` §C1 F-grade (3/99 = 3% coverage) + REPAIR-AMENDMENT-AUTHORIZED (a) trigger + Andrew sovereign goal-set 2026-05-27T~22:49Z (drive FIND_INSURE end-to-end through Phase 3 close); CVO P1 priority routed via COO 21:00Z mandate.

<status>pending</status>

## Objective

Fan out the deployed `find-insure-crawl-web` Lambda across the 96 IMOs not yet crawled, producing per-IMO bronze HTML + meta.json + silver records + gold score.json files for the full 99-IMO universe (3 already crawled — avantax + 1st-atlantic + carl-ostenson — preserved as-is). Phase 1 RAVC2-Accept gates on this completion.

**Two-stage execution per CVO P2 recommendation:**

**Stage 1 — 10-IMO TP/FP discrimination-validation subset (FIRST):**
- Andrew mandated 5 known-AM + 5 known-absent IMOs as a discrimination prelude before full-universe burn
- Lets P2 grade fire ahead of full run, surfaces methodology drift early (cost ~$5-20 vs full-universe ~$50-200; saves redo if W1 taxonomy fundamentally mis-calibrated)
- IMO list: COO recommends 5 known-AM from existing universe candidates (e.g., Avantax-class large RIAs) + 5 known-absent from insurance-only IMOs — final list ws CTO ratifies as `data/find/imo/config/p2-validation-subset-2026-05-27.json` (sister TO to .008 if ws CTO has not pre-staged)
- Halt-condition: if Stage 1 produces FP rate >20% OR FN rate >20% OR empty-body rate >40%, escalate to ws CTO before proceeding to Stage 2 (saves universe burn on a known-broken taxonomy)

**Stage 2 — full 96-IMO universe fan-out (AFTER Stage 1 pass):**
- Dispatch crawl-web Lambda on the remaining 96 IMOs from `s3://opal-data-imo/serving/_meta/source-list-2026-05-27.json` (skip the 3 already crawled + the 10 from Stage 1; net = 96 - 10 = 86 IMOs in Stage 2, or 96 if Stage 1 IMOs are not part of universe set)
- Per-IMO Lambda timeout per PRD §3.8 = 20-call hard-cap + soft-abort + EC2 escape (so AC-T2 logic is per-IMO bounded)
- Bronze write → silver Lambda chain auto-fires (EventBridge from .005 Lambda design); gold .006 Lambda chains from silver per design

## Acceptance criteria

- **AC1.** Stage 1 IMO list ratified + landed as `data/find/imo/config/p2-validation-subset-2026-05-27.json` (or equivalent). If ws CTO has not pre-staged, COO authors mid-flight via SYNC handoff — block at most ~10min.
- **AC2.** Stage 1 Lambda dispatch: 10 EventBridge invocations of `find-insure-crawl-web` against the 10-IMO subset; per-IMO crawl-success / blocked / empty-body / timeout counts logged to CloudWatch logs aggregated to a single `s3://opal-data-imo/qa/stage1-validation-subset-{run-date}.json` aggregate.
- **AC3.** Stage 1 P2 discrimination self-grade: read the 10 silver + 10 gold scoring outputs; emit `qa/stage1-p2-grade-{run-date}.json` with structure:
  ```
  {known_am_count, known_absent_count, tp_count, fp_count, fn_count, tn_count,
   tp_rate, fp_rate, empty_body_rate, recommended_proceed: bool, halt_reason: str|null}
  ```
  `recommended_proceed=true` only if FP rate ≤20% AND FN rate ≤20% AND empty_body rate ≤40%.
- **AC4.** Stage 1 → Stage 2 gate: if AC3 `recommended_proceed=true` AND ws CTO + ws COO + ws CVO all ACK the Stage 1 grade (via inline RAVC2-Request to ws COO, CC ws CTO + ws CVO), proceed to Stage 2 same-cycle. If halt-condition fires, surface to ws COO `[STAGE1-HALT]` with CWL evidence + grade-json; ws COO routes to ws CTO for W1/W2 taxonomy refinement before Stage 2.
- **AC5.** Stage 2 Lambda dispatch: ≤96 EventBridge invocations against the remaining-universe IMOs; per-IMO async; Lambda-side per-IMO timeout per PRD §3.8 enforced. Emit aggregate `qa/stage2-universe-{run-date}.json` with per-IMO outcome class table (SUCCESS / EMPTY-BODY / BLOCKED-anti-bot / TIMEOUT / ERROR).
- **AC6.** Cost gate per PRD §3.7 KMS + cost-gate config — monitor running cost via CloudWatch + the cost-gate schema config (sns:Publish alert if Lambda cumulative-cost exceeds COO-set ceiling — COO recommends $50 ceiling for Stage 2 with $10 alert threshold).
- **AC7.** Post-universe-run S3 inventory confirms 99 `corp/{slug}/bronze/web-scrape/2026-05-27/` prefixes exist + 99 `silver/web-scrape/` + 99 `gold/web-scrape/score.json` files. `aws s3 ls s3://opal-data-imo/corp/ --recursive | awk -F/ '{print $2}' | sort -u | wc -l` returns 99. C1 grade flips F → A.
- **AC8.** AC-T2 EMPTY-BODY rate empirically determined (was statistically invalid at n=3); if universe-wide empty-body class >5-10% per PRD AC-T2 threshold, surface `[AC-T2-TRIGGER]` to ws CTO for scraping_browser1 v0.3.0 escape-valve dispatch (per CVO P4 + AE 0.7~B source pre-build at `40b18d724`).
- **AC9.** Telemetry: `qa/stage2-universe-{run-date}.json` is the AC-T1 (crawl-coverage telemetry) deliverable per PRD; standardized aggregate format consumable by Phase 3 serving consolidation (.023).
- **AC10.** `comp-iam service find-insure-crawl-web` re-confirms s3:PutObject scope covers all 99 IMO write prefixes; `comp-pipescript deployed find-insure-crawl-web` returns MATCH.

## Dependencies

- **FIND_INSURE.004 RAVC2-Accept (crawl-web Lambda deployed)** — landed pre-reboot at `imo-pipeline-v0.2.0`; this TO fan-outs the deployed Lambda, no fresh Lambda code change required.
- **FIND_INSURE.005 deployed (parse-web silver Lambda)** — landed pre-reboot at `imo-pipeline-v0.3.0`; bronze→silver chain operational.
- **FIND_INSURE.006 deployed (score-web gold Lambda)** — landed pre-reboot at commit `877ca495d`; silver→gold chain operational.
- **FIND_INSURE.007 RAVC2-Accept (Rule 17 silver passthrough patch)** — **NOT a hard dependency** for .008. The patch additively extends silver schema; .008 can proceed in parallel. If .007 lands mid-flight in Stage 1, re-run the silver-Lambda on Stage 1 IMOs to pick up the 5-field extension (small re-burn cost ~$1).
- **Source-list:** `s3://opal-data-imo/serving/_meta/source-list-2026-05-27.json` (99 IMOs, landed Phase 0 deliverable 3).
- **Stage 1 IMO subset config:** COO produces if ws CTO has not (block ≤10min).

## Sequencing — Stage 1 first, Stage 2 on validation pass

1. ~10min: Pre-launch — read CVO 11-axes §C1+C2+P2 + PRD §3.7 cost-gate + §3.8 per-IMO timeout; confirm find-insure-crawl-web Lambda + IAM role + KMS key all operational (no fresh Terraform needed)
2. ~10min: Stage 1 IMO subset confirm/author (`p2-validation-subset-2026-05-27.json` — request from ws CTO via SYNC handoff if not pre-staged)
3. ~2-3h: Stage 1 — 10 EventBridge invocations + chain to silver + chain to gold + AC3 grade-json emit + RAVC2-Request gate
4. ~30min: Stage 1 grade ACK round-trip with ws COO + ws CTO + ws CVO (parallel ACKs)
5. ~12-24h: Stage 2 — 86-96 EventBridge invocations; primarily observation (Lambda async); cost-gate monitoring + AC-T2 threshold watch
6. ~30min: Stage 2 close — AC7 inventory confirm + AC8 threshold evaluation + AC9 telemetry aggregate finalize + RAVC2-Request

**Total ETA:** ~16-30h wall (Stage 1 ~3-4h + Stage 2 ~12-24h + close ~1h); dominated by Lambda fan-out compute, not your authoring time.

## RAVC2 deliverable

Two RAVC2-Requests in sequence:

1. **Stage 1:** `[RAVC2-Request] FIND_INSURE.008 Stage 1 P2 validation subset` to ws COO with: AC2 dispatch evidence + AC3 grade-json + AC4 gate-decision recommendation. CC ws CTO + ws CVO (CVO will independently grade — pre-positioning per [[feedback_cvo_proactive_verdict_landing_pattern]]).
2. **Stage 2:** `[RAVC2-Request] FIND_INSURE.008 Stage 2 universe-run + Phase 1 close-gate` to ws COO with: AC5+AC7+AC8+AC9 evidence + cost-gate compliance + comp-iam/comp-pipescript outputs. CC ws CTO + ws CVO. **This is the Phase 1 RAVC2-Accept gate** — ws COO + ws CTO + ws CVO joint-accept lands FIND_INSURE Phase 1 close.

## Compiler tools mandate

- **Before launch:** `comp-pipescript deployed find-insure-crawl-web` (MATCH) + `comp-iam service find-insure-crawl-web` (no MISSING) + `comp-blast find-insure-crawl-web` (Stage-2 universe burn impacts downstream parse-web + score-web Lambda CWL + S3 cost — confirm blast radius matches expectation)
- **Before Stage 2:** repeat `comp-pipescript deployed` (Stage 1 may have triggered code rebuild)
- **After Stage 2 close:** `comp-iam gaps` (confirm no permission drift from universe burn)

## Cross-domain coordination

- **FIND_INSURE.007 (DS~A Rule 17 silver patch)** — silver-schema extension; .008's Stage 1 may run before or after .007 lands. If after: silver records pick up the 5 extra fields automatically. Coordinate via SYNC MCP to DS~A: "ETA on .007 deploy?" — if .007 ships before Stage 2, Stage 2 silver records carry the 5 fields universe-wide (preferred); if .007 ships during Stage 2, in-flight invocations may have heterogeneous schema (acceptable; downstream consumers handle null gracefully).
- **FIND_INSURE.023 (DS~B/~E P2 W3 serving consolidation)** — Phase 3 enabling TO; consumes `qa/stage2-universe-{run-date}.json` (your AC9 deliverable) + 99 `gold/score.json` outputs to emit `serving/scoring.json`. .023 is STAGED behind your AC7 close.

## Notes

- Per CVO P1 priority: "Suggest 10-IMO P2 TP/FP validation subset (5 known-AM + 5 known-absent) FIRST as a discrimination-validation prelude, then full 99-IMO universe — this lets P2 grade fire ahead of the full run." Two-stage discipline encoded above.
- Per [[feedback_pre_staged_recovery_path_pattern_delivers_autonomous_post_cap_dispatch]] + [[feedback_substrate_continuity_multiplier_reproduces_across_subsequent_FIX_class_TOs]]: your Stage 1 → Stage 2 staging matches the in-fabric ADVI_DEMOV1 Fire 4 → Fire 7 cascade pattern — substrate-continuity gives 90%+ confidence Stage 2 inherits Stage 1's mechanics without surprises.
- Cost-gate ceiling ($50 Stage 2) is COO conservative; if ws CTO has prior empirical anchor on Bright Data per-IMO crawl-cost, refine the ceiling pre-Stage-2 dispatch.
- Andrew Q1 pre-Phase-2 subset-cut decision (top-quintile + Series-license-mention) is a DOWNSTREAM gate (Phase 2A entry, not Phase 1 close). Your AC7 close UNLOCKS the Q1 ask to Andrew; do NOT block on Q1.
- Per LD-0090 ALWAYS-PROCEED: if any gate-ACK round-trip stalls >2 cycles (≥40min), surface to ws COO for SPAWN-WITH-DIRECTION or escalation per LD-0026 backstop chain.

— ws COO /drive cycle 165 post-reboot Phase 1 close-gating triad 2026-05-27T~22:55Z
