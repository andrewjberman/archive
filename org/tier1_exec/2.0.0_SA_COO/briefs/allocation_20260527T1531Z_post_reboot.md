# /allocation — post-reboot supply-signal — 2026-05-27T15:31Z

**COO:** 2.0.0_SA_COO (ws fabric)
**Cycle:** /drive #165 (first post-reboot)
**Anchor:** MSTR-DIRECT 2026-05-27T~14:53Z mass session-log + device reboot ~14:55Z. F-001 liveness_gap currently 4-canonical-only.

## LIVE NOW (4-canonical Tier-1)

| Serial | State |
|---|---|
| 0.0.0_AB_MSTR | LIVE (~150s heartbeat) |
| 1.0.0_SA_CTO | LIVE (just registered) |
| 2.0.0_SA_COO | LIVE (this cycle) |
| 3.0.0_SA_CVO | LIVE (just registered) |

## SPAWN-NEEDED (urgency-ordered)

### HIGH — within ~60min

**0.7.0_AE_CloudOps**
- **Why:** ADVI_DEMOV1.012 Fire 1 SSM `5caba4eb-aee8-4162-8cb0-0fc327632fe3` InProgress on AWS (started ~11:30Z, 6h budget terminal ETA ~17:30-18:30Z). SSM survives reboot; local monitor does not.
- **Risk if delayed:** SSM terminal-state report unwatched → if Fire 1 TimedOut/SIGKILLed, Fire 7 scan-only contingency dispatch + joint Phase 4 RAVC2 prep is delayed.
- **Spawn-with-direction:** "ADVI_DEMOV1.012 Fire 1 SSM 5caba4eb monitoring resume; ETA ~17:30-18:30Z; pre-staged Fire 7 scan-only contingency JSON if TimedOut per cycle 157 pattern; joint Phase 4 RAVC2 with DS~D once Fire 1 terminal."

### MEDIUM — within ~90min (parallel to AE)

**0.4.0_DS_ClientPlatform~D**
- **Why:** ADVI_DEMOV1.012 Phase 1 AC1 SHIPPED `8de9c5415` (PASS-2 completion-gate instrumentation). Phase 3 joint RAVC2 wrap with AE 0.7 pending Fire 1 terminal.
- **Spawn-with-direction:** "ADVI_DEMOV1.012 Phase 3 joint RAVC2 prep with AE 0.7; .012 Phase 1 AC1 shipped 8de9c5415; standing for AE 0.7 Fire 1 terminal."

### LOW — opportunistic (~2-4h)

**0.1.0_DS_MarketIntelligence~A**
- **Why:** YALP_MACROS Phase 2 Andrew /goal DISCHARGED end-of-prior-session; TO-008c (AAII/ConferenceBoard HAR-RE adapters) pending Andrew HARs. No urgency until HARs land in inbox.
- **Spawn-with-direction (when HARs arrive):** "YALP_MACROS.008c HAR-RE adapters; Andrew HARs in inbox; sub-2h cascade-compression target per ~A precedent."

**0.4.0_DE_ClientPlatform / 0.4.0_DT_ClientPlatform / 0.4.2_RD_AdvisorIntelligence**
- **Why:** ADVI_SHARED.008 (DT+RD joint visual smoke Phase 1 close gate) STAGED with .007 RD wrap complete. ADVI_DEMOV1.010 (DE label-fix) PENDING follow-on. Non-time-critical; low Andrew-gate.

## KILL-CANDIDATE

None.

## Cycle disposition

COO recommends MSTR spawn AE 0.7 + DS~D as priority pair this allocation window (~60min). Other workers can wait next cycle without project-risk. Tier-1 canonical preserved; within 16-cap easily (4 LIVE + 2 spawn = 6 of 16).

— 2.0.0_SA_COO /drive #165 1531Z
