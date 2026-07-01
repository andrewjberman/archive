# SCTY Employee-Onboarding Guardrails — COO Decomposition + GO

**Andrew-direct 2026-07-01** (employees onto MCP -> user-type action-guardrails; compromised-endpoint-with-MCP threat; Andrew = master-admin @ andrew@opalinvest.com).
**Chain:** 0.5.0_AE assessment brief `c9ab8e986` -> CTO fold `fd9113e82` (GAP-1 tier-model + GAP-2 onboarding-gating re-phase both folded) -> CTO GO-RELEASE 170711Z -> **this COO decomposition + GO**.
**Priority:** HOT — security-GATES employee-onboarding (do-before-onboarding minimum bar; no non-Andrew employee provisioned until the bar lands).

## Authorization (CTO GO-released, both held GOs cleared)
1. GO **SCTY_MCPGUARD.S0** (destructive-surface enum) + cut **G1-G6** on its enum output.
2. OPEN the **SCTY_PREMCP decomposition** — **P1a (token-revocation) + B2 (read-only-scope)** FIRST.
Andrew's directive IS the review-GO (MCPGUARD S0 was "GO held for Andrew PRD review"; PREMCP decomposition was "Andrew-GO'd HELD").

## Lane assignment
- **BUILD LANE = 0.5.0_AE_OpalETL** (dedicated; offered + knows the design; freed post-ETFS-close + Yang-done). Do NOT block behind 0.7.0's ETFS/STEP-C queue (CTO rec — hot).
- **HARD coordination requirement (CTO):** the guard slots into the LIVE gateway tool-dispatch path -> the builder MUST sync with **0.7.0_AE** (gateway code+infra owner-of-record, integration point) + **0.8.0_AE_CloudComp** (grounded the call-path). A build diverging from the live dispatch path is THE failure mode. 0.7.0 stays gateway-owner-of-record even without the build pen.
- Fresh MSTR-spawn is the fallback if 0.5.0 reloads.

## DO-BEFORE-ONBOARDING BAR (ordered; CTO arch-gates each; CVO verifies LIVE)
- **(0) USER-TYPE TIER MODEL — FIRST** (prerequisite + highest arch-risk; everything keys off identity->tier resolution). **MUST resolve off the ES256-verified OIDC email claim (`app/identity.py` x-amzn-oidc-data), NEVER a spoofable header/body** — a spoofable tier key defeats the whole model. Tiers: master-admin/systems / standard-employee / read-only-service. CTO ARCH-GATES this FIRST.
- **(0b) MCPGUARD.S0** destructive-surface enum -> the `destructive_ops` registry (fail-closed on unclassified). Feeds G1-G6.
- **(1) MCPGUARD Phase-1:** G2 classify -> G1 blast-cap -> G4 reversibility-first (OneDrive-stopper).
- **(2) PREMCP:** A1 token-revocation (leaked-refresh kill-path = the virus scenario) + B2 read-only-scope (Files.Read.All-never-ReadWrite at the PERMISSION layer — destructive impossible, not guard-caught).
- **(3) G6** audit/alert (compromised-endpoint mass action loud in seconds).
- **Fast-follow (NOT the hard gate):** G3-confirm, G5-anomaly, PREMCP network/WAF.

## Arch-gates (CTO gates each at spec+implementable; CVO certs on LIVE behavior, verifier-not-fixer)
(a) tier-resolution off the verified OIDC claim **[FIRST]**; (b) S0 destructive_ops registry fail-closed-on-unclassified; (c) each G at spec + implementable-change; (d) B2 = Files.Read.All-never-ReadWrite at the PERMISSION layer. CVO certs actual over-cap-rejected / actual-undo-restores / read-token-cannot-write LIVE.

## START SET (GO now, parallel)
- **(0) tier-model** (arch-critical-path — CTO arch-gates the moment the spec lands) + **(0b) MCPGUARD.S0 enum**.
- Build-lane 0.5.0 syncs 0.7.0 + 0.8.0 on the integration point BEFORE landing anything on the live dispatch path.

## Adjacent (parked, correct)
- oplmcp-workflow-scoping -> NFRA_COMPLEARN follow-on AFTER guardrails land (brief SS5). No action this cycle.

## Flow
0.5.0 builds -> CTO arch-gates each (tier-resolution FIRST) -> CVO certs LIVE -> COO tracks the do-before-onboarding bar to complete before any non-Andrew provisioning. RAVC COO at each item.
