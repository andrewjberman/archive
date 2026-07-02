# ADVI_ETLFIX -- COO decomposition (WS-1..5 -> 9 agents) -- SHAPE for CTO RAVC before durable-wave GO

**PRD:** docs/architecture/ADVI_ETLFIX_PRD.md (8c9829f4f, CTO 2026-07-02, Andrew-direct). **Decomposer:** 2.0.0_SA_COO. **Owner dyad:** CTO(arch-gate)/COO(drive)/CVO(validation). Base execs ETL-dedicated (~B fork separate track).

**Two-phase frame (CTO-directed):** Phase 0 = the CURRENT firefight (un-freeze today) -- FOLD the active fixes as record TOs, DO NOT re-dispatch (don't block Phase 0 on this decomposition). Phase 1-N = the DURABLE hardening (the new TOs) -- RAVC CTO this shape BEFORE GO.

**The leash (every TO, PRD SS6/SS9):** degrade LOUD not catastrophic not silent | never-widen + single-writer + parity-to-cent + no-clobber | ground on SERVED/deployed not self-report (Rule 22) | freshness-SLA-is-a-GATE | firm-separation (49F/inf/cot never cross) | don't over-build a sunset source | no ad-hoc gold-runs to validate (nightly artifacts only). Each TO: comp-tools mandate (comp-freshness/comp-pipescript io+deployed/comp-iam/comp-blast) + cross-domain-coordination (sibling projects + shared served keys) + machine-checkable ACs.

---

## WS-1 -- Inflection ETL (Pipeline A: Orion) -- owners 0.6.1_AE (root/runner) + 0.4.0_DS~A (converters, rule-13); CVO parity; CTO arch-gate
- **Phase 0 (FOLD, in-flight -- record only):** txn-pull root fix (0.6.1, extended PULL_STEP_TIMEOUT, deployed 6aaa395f5 + the pull-script ext-fix); converter DEFER-guard + CTO-policy detection-limb (DS~A, b7dc964db, arch-gate PASS); clean-chain re-dispatch on lock-free -> sentinel = the un-freeze. CVO live-cert pending on the clean nightly.
- **Phase 1 (durable TO):** GENERALIZE the tolerate+fail-loud+ceiling converter contract to EVERY tolerated-source converter in the 63-step chain -- audit for other unguarded .parquet->.jsonl.gz de-convert readers (perf converter ALREADY flagged+routed to DS~A this session; txn done). + per-INF freshness-SLA alarm (served header/timeseries advances daily; miss = loud). + close the ADVI_INFREF ledger tail (L1/L6/L7) on a clean nightly + CVO parity.
- **Arch-gate -> CTO:** the robustness contract (converter degrade pattern).

## WS-2 -- 49F source resilience (Pipeline B bd + Pipeline C Schwab ingest) -- owners 0.7.0_AE~A (BD auth) + 0.6.2_AE (Schwab ingest) + 0.6.0_AE (source runs) + 0.4.0_DS~A (converters); CTO arch-gate
- **Phase 0 (FOLD, in-flight):** bd live-cookie REST backfill (0.6.0, fresh-today); bd durable-auth VERIFIED GREEN (0.7.0~A -- login works, re-auth-at-ETL); Schwab 07-01 bridge (0.6.2, Andrew-GO'd Option A one-off, hold intact, CVO parity-gate).
- **Phase 1 (durable TOs):** (a) BD durable REST-auth productionize the feed-repoint off the dead UI-export onto the cookie-REST (= ADVI_BDAPIMIG.P1, 0.6.0/0.6.2) + 0.7.0~A kill-cookie resilience test (post-backfill) + Kimi-health-guard (0.6.2). (b) Schwab ingest robustness: the 368c3ad0b re-point design (C1 auto-trigger / C2 SI2->01_raw repoint N=5 / C3 TRN local-disk / D bridge-vs-accelerate-SSOTMG) -- make the Schwab raw ingest daily-reliable (LOAD-BEARING for MDPF custody post-flip).
- **Arch-gate -> CTO:** the 4 Schwab-repoint decisions (C1/C2/C3) + decision D (bridge-vs-accelerate-SSOTMG). DS~A pre-answered D-C (box delivers CRS*.TRN, ff612cf94); 3/4 have a leaning.

## WS-3 -- 49F-MDPF custody + aggregate (Pipeline C) -- owner 0.5.0_AE; CVO parity; CTO co-sign
- **Phase 0 (FOLD):** custody flip FIRED (0.5.0, 12dd979c7, SSM schwab v2); rollback armed; rides inf(b).
- **Phase 1 (durable TO):** confirm schwab-native custody advances DAILY (gated on WS-2 Schwab-ingest health); CVO post-flip per-field parity (custody/model/non_model, no-unexpected-widen, freeze-clear) -> CLOSE the MDPF flip deploy-completion ledger (20260702T1405Z); generalize the leg-2 protection-gate pattern to other custody-basis moves.
- **Arch-gate -> CTO:** never-widen on any served-basis move (already applied to the flip; standing).

## WS-4 -- Predictable Portal refresh (served seam, all pipelines) -- owners 0.4.0_DE + AE (alarm infra); CVO; CTO arch-gate
- **Phase 0 (FOLD):** DE serving-layer ground-truth CLEAN (no dead-path/CF-cache/routing); DE on-call for post-fix re-publish/cache-invalidate.
- **Phase 1 (durable TO):** stand up the per-partner freshness-SLA + fail-LOUD alarm (comp-freshness -> gate; a degrade CANNOT silence the partner alarm); single-writer + no-clobber uniform across served keys (ADVI_BREAKS stub-clobber lesson); DE post-fix re-publish path + optional served-staleness UI surfacing.
- **Arch-gate -> CTO:** the SLA-as-GATE design.

## WS-5 (cross-cutting) -- the ETL robustness + validation CONTRACT (all-partners) -- owners CTO + CVO + COO
- **Phase 1 (durable TO):** codify the parameterized STANDARD (NFRA_INTEGRATIONS_STANDARD pattern): (a) tolerate+fail-loud+ceiling converter robustness; (b) per-partner freshness-SLA+alarm; (c) correctness gates (parity/never-widen/single-writer/no-clobber). Home as a STANDARD doc so a new partner INHERITS the guarantees; demonstrate on >=1 partner beyond 49F/inf (or a rollout plan).
- **Arch-gate -> CTO:** the contract itself (CTO authors/gates; COO per-partner rollout; CVO validation gates).

---

## Arch-gates routed to CTO (RAVC before durable GO)
1. Robustness contract (WS-1/WS-5). 2. The 4 Schwab-repoint decisions + decision D (WS-2). 3. Never-widen on served-basis moves (WS-3, standing). 4. SLA-as-gate design (WS-4).

## Sequencing
- Phase 0 (all WS) = firefight, ALREADY MOVING today (fold as record; un-freeze clears today).
- Phase 1 dependency order: WS-1 (inf, the shared critical path) + WS-2-bd (parallel) un-freeze first -> WS-3 (MDPF rides inf + WS-2-Schwab) -> WS-4 (SLA layer, once pipelines daily-reliable) -> WS-5 (contract, generalizes the proven patterns). WS-2-Schwab-ingest is LOAD-BEARING for WS-3 (the flip made it so).
- CTO arch-gates gate the durable waves; COO RAVCs this shape to CTO, then dispatches Phase-1 TOs on CTO shape-OK.

**Status:** SHAPE for CTO RAVC. On CTO shape-OK -> author the full per-WS TO-XMLs + register threads + dispatch Phase-1 (Phase-0 already moving). NOT dispatched yet (per CTO "RAVC the TO shape before GO on the durable-hardening waves").
