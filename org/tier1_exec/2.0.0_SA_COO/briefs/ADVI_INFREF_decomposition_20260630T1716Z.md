# ADVI_INFREF — COO decomposition (P1-P5 onto the lane map)

**Source PRD:** `docs/architecture/ADVI_INFREF_PRD.md` (1.0.0_SA_CTO, Andrew-direct, born from ADVI_BREAKS).
**Decomposed by:** 2.0.0_SA_COO 2026-06-30T1716Z. **CTO arch-gates each leg; CVO independently validates + holds the standing gate.**
**Sequencing (Andrew-locked):** inflection FULLY (impl + validation + cleanup) BEFORE Cottonwood. **All P1-P5 apply work sequences BEHIND today's tactical inf recovery** (which is LANDING — served-RICH flip minutes out at decomposition time). The 2 early-gating tasks (read-only) start first.

## Lane map (standing conventions — [[project-06n-ae-firm-mapping]] + [[project-inf-refactor-lane-preservation]])

| Role | Lane | Scope |
|---|---|---|
| **inf DS** | `0.4.0_DS_ClientPlatform~A` | ALL pull/silver/gold script work + chain composition (SPEC-1/2/3 scripts). The inf lane owner; deep recovery context. |
| **inf AE** | `0.6.1_AE` (Inflection — **SPAWN at P1 dispatch** via MSTR) | runner/EC2/EventBridge/decommission infra + auth (SPEC-4). 0.6.N firm-map: 0.6.1 = Inflection. |
| **validation** | `3.0.0_SA_CVO` | standing gate; co-signs each LANDED artifact (deployed != resolved); parity-gates the cutover. |
| **arch** | `1.0.0_SA_CTO` | arch-gates each leg E2E. |
| **PRESERVED — do NOT pull onto inf** | base → cot, `~B` → 49F | lane-preservation directive (Andrew-direct). base+~B keep their firm context. |

## Early-gating tasks (READ-ONLY — dispatch FIRST, queued behind ~A's served-RICH RAVC)

- **EG-1 writer-map confirm (R-Point 4) → ~A.** SOURCE-CONFIRM the full `platinum/firm/*` writer-map: do INF_D_04 (gold chain) AND `inf-portal-publisher` λ both write `header_metrics.json` (or any shared served key)? DISJOINT → document the map, single-writer holds. OVERLAP on header_metrics → TO-2 second-writer hazard → D_04 is canonical sole writer, remove the publisher's overlapping write. Invariant: exactly ONE writer per served key. (TO-2 class; gates P1 gold.)
- **EG-2 yahoo per-consumer edge-check (R-Point 5) → ~A.** For each of the 4 consumers (INF_B_00, INF_B_01, INF_B_01b, INF_D_07): confirm its price-need is held-position-only (covered by `positions_mv`) — i.e. no consumer needs a price for an asset on a date it was NOT held. All-clear → repoint+retire per consumer. A real gap → re-opens a 3rd-party source (Andrew posture: remove-now, reopen only on a real surfaced gap). Gates the §2 yahoo removal.

## Phases

- **P1 — unified flow (RT-R1):** `~A` bronze raw-native single-pull-layer (all cataloged dims onto the EC2; 4-dim de-convert {positions,assets,performance,transactions} JSON-at-bronze) -> silver one-dispatch full-fidelity (raw->parquet, consolidate converter sprawl, repoint, `silver/orion-api/{dim}/snapshot_date={date}/`) -> gold two-flow (current-day B+C + partition-freshness assert, G-R1 Part-2 already co-signed `c76540ebe`). `0.6.1_AE` the single-pull-layer EC2/runner plumbing. **Structural-fix thesis:** single-pull-layer collapses the duplicate-perf-pull hang class (supersedes the `9ea447b3a` timeout-tolerate interim). Yahoo repoint (§2) after EG-2 clears. CTO arch-gate; CVO validates.
- **P2 — parallel-parity (RT-R2, never-widen):** new single runner alongside legacy; silver/gold output parity-equal to pre-refactor, **several clean days**. `0.6.1_AE` infra; `~A` parity diffs; CVO parity-gate.
- **P3 — decommission (RT-R3, ordered, deploy-LEDGERED, never-widen on shared roles):** 9 cron pull λ + EventBridge -> `inf-bronze-runner` + triggers -> stub/redundant λ -> `inf_gold_qa_runner` (AFTER cutover, R-Point 3) -> yahoo thread artifacts. `0.6.1_AE` owns; every leg a deploy-completion ledger entry (NEVER half-land).
- **P4 — auth/OTP harden (RT-R4 — FINAL step):** cookie-age pre-expiry alarm (T-7d), loud JWT-fail, robust BD-style OTP relay, Eclipse-422 alarm. `0.6.1_AE`. **Ties the Andrew-sovereign persistent-login directive** (consolidate login+ingestion + persistent session, Schwab/0.0.1_UA pattern) — but note R-Point 3 KEEPS inf-exporter auth-box ISOLATED from the data runner; the persistent-login design reconciles with that isolation (CTO/CVO loop). 49F's analogous persistent-login (0.6.0 designing post-un-freeze) is the sister effort.
- **P5 — single-writer/single-runner sweep (RT-R5):** confirm no orphan producer/runner/writer. `0.6.1_AE` + CVO sweep.
- **POST-SETUP VALIDATION (§3, Andrew-sequenced AFTER build):** freshness / value-parity NO-TOLERANCE (served==positions_mv==Orion to the cent) / completeness / single-writer sweep / auth health / parity-gate. **The inf value-defect closes HERE on the refactored flow's LANDED served artifact — CVO co-signs the artifact, not the deploy.**

## Ratification points (CTO-ruled §4 — DO NOT re-open)
1. Bronze folder-migration = GO-FORWARD + on-demand backfill (old prefixes frozen READ-ONLY). 2. Gold A-stage cache-by-default on incremental (nightly stays full; governs manual/future-incremental). 3. inf-exporter KEEP-isolated; inf_gold_qa_runner retain-then-retire-after-cutover. 4. writer-map confirm-first (EG-1). 5. yahoo per-consumer edge-check (EG-2).

## Dispatch plan
1. **EG-1 + EG-2 -> ~A** NOW, queued behind the served-RICH RAVC (no idle gap). [dispatched this cycle]
2. **SPAWN 0.6.1_AE -> MSTR** (allocation signal) at P1 dispatch — the inf-refactor AE lane. [signaled via /allocation]
3. **P1 dispatch** held until the tactical recovery lands (served-RICH 06-30 confirmed + value-parity quiet) — then ~A P1-scripts + 0.6.1 P1-infra in parallel, CTO arch-gate, CVO validate.
4. base/~B UNTOUCHED (cot + 49F lanes preserved).
