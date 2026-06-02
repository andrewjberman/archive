# verify-channel — ADVI_INFPRM.W2-FE (portal DEV 8ff69f18): Symptom-2 resolved + diagnosis-correction

**archetype:** VALIDATE | **Reviewer:** 3.0.0_SA_CVO | RD~C VERIFY-REQUEST | supersedes my 1918Z CONDITIONAL on INFPRM

## Verdict: PASS (logic+data). Symptom-2 (Firm Overview/clients/book blank for external Inflection) RESOLVED. Remaining = Andrew/CTO rendered-pixel L1 smoke.

### What 8ff69f18 changed
Removed the firmOverride-required client-side throws across the wrapper functions (getPlatinumFirmDashboard, getClientsTab, getFirmLeaderboard, fee_efficiency, getPlatinumAdvisorSummary, ...). Diff = throw-removal + omit-param comments ONLY (no new getClientsTab/split/merge logic added — verified via the diff). The omit-param ternary `firmOverride ? base?firm= : base` (L871) preserves the EXACT prior URL when firmOverride is defined.

### Why Symptom-2 is resolved (full chain, external Inflection: firmOverride=undef, firmId='inflection')
1. dashboardQuery enabled (firmId truthy, W1 prop). 
2. getPlatinumFirmDashboard(undef): fetches base dashboard.json stub; **split=true** (verified on served stub) -> SPLIT MODE.
3. Split mode (L894-911, PRE-EXISTING) fetches in parallel + merges: getFirmLeaderboard -> employee_leaderboard; fee_efficiency; **getClientsTab(undef) -> clients_tab** (L907/919).
4. getClientsTab(undef) omits ?firmId= -> W2 backend firmId-fallback self-scopes to inflection (my W2 SECURITY PASS) -> clients_tab.json populated (300 clients, 61KB, verified served).
5. Throws removed -> the composite + all split fetches RUN for external Inflection (pre-8ff69f18 they THREW -> blank).
=> ClientsTab.tsx:307 dashboardQuery.data.clients_tab = the 300-client populated merge. Firm Overview/clients NOT blank.

### DIAGNOSIS CORRECTION (sharper-test-binds) — supersedes "empty dashboard.json -> rewire-required"
The earlier finding (AE/COO/my 1918Z: "ClientsTab reads empty dashboard.json, zero getClientsTab refs, rewire-required") was a ClientsTab.tsx-LEVEL grep that did NOT trace into getPlatinumFirmDashboard. The composite is SPLIT-MODE and ALREADY merges getClientsTab->clients_tab (pre-existing, not added by 8ff69f18). The 308b dashboard.json is the split STUB (by design: carries firm_id/headline/ytd/split flag; clients_tab/leaderboard/fee come from the parallel split fetches), NOT an empty defect. The real root cause = the firmOverride throws blocking the split fetches. 8ff69f18 (throw-removal) is the COMPLETE fix; NO ClientsTab source-repoint was required. My deeper trace binds.

### Regression (49F/demo/internal): SAFE
firmOverride defined -> ternary truthy branch = exact prior URL; split-mode + merge unchanged. No behavior change.

### Honest limits
- Rendered-pixel (Peter actually SEES Firm Overview/clients/book) = Andrew/CTO visual smoke (headless down). This is logic+data/trace.
- The 8 omit-param wrappers rely on per-endpoint backend JWT-fallback; getClientsTab confirmed (W2 PASS); getFirmLeaderboard + fee_efficiency + others rely on the same shared-advisor-router JWT-route (RD~C asked AE to confirm Lambda coverage per-endpoint) — if any endpoint's Lambda lacks the fallback, that specific panel could 400; flagged as the one open dependency.
- DistributionTab:1951 Segment-Analytics caller is RD~B's (firmId-threading handoff) — separate.

## INFPRM closure stance (updated)
W1 (regression PASS) + W2-backend (security PASS) + W2-FE (this PASS) = Symptom-2 resolved at logic+data. INFPRM closeable on the data/logic axis; sole remaining = Andrew/CTO rendered-pixel L1 visual smoke + the per-endpoint JWT-fallback coverage confirm (AE). My 1918Z CONDITIONAL is LIFTED on the data/logic axis.

RAVC2 PASS to RD~C; CC COO/CTO (diagnosis-correction relevant to their closure record).
— 3.0.0_SA_CVO
