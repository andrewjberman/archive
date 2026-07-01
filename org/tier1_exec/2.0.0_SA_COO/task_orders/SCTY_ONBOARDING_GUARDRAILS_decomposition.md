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

## CTO Part-A ruling + UPDATED BAR (172000Z, PRD SS5 committed)
- **Part A (tier-model + S0 surface) = PASS** (CTO-grounded vs identity.py + tools.py). 0.5.0 UNBLOCKED to build tier_resolve.
- **tier_resolve RULE:** fail-closed + EXACT-MATCH andrew@ pin (not pattern) + unknown-identity -> least-priv. Elevated tier ONLY under a signature-VERIFIED provider (alb_oidc/configured-cloudflare); verified_access(verify_signature=False)/tailscale/header -> force read-only-for-all.
- **UPDATED do-before-onboarding BAR** (what COO tracks; G3-first reorder, G4 deferred): **tier-model + G2(fail-closed) + G3(confirm-on-irreversible) + G1(recipient-cap) + B2(read-only-scope) + A1(token-revoke) + G6(audit/alert)**. G4-reversibility + G1-item-cap = FUTURE (activate when a delete tool is added; surface is currently SEND-ONLY, 4 irreversible sends + create_draft, NO delete). OneDrive headline protected via G2+B2 -- no protection dropped.
- **P1b SEQUENCING (pending 0.7.0's IDENTITY_PROVIDER):** verified_access -> P1b (signature-verify) is a HARD CO-REQUISITE, pull forward -- NO elevated tier (incl Andrew) functions until P1b/D1 lands. alb_oidc -> tier-model independent, P1b parallel. RESOLVES on 0.7.0's answer (now LIVE + answering 0.5.0's sync) -> COO flags CTO + 0.5.0 the instant it replies.
- **S0-CLOSE condition:** 0.8.0 confirms _run() (tools.py:47) is the SOLE dispatch path (no bypass). A bypass defeats the guard.
- CTO arch-gates the implementable-change BEFORE it touches the live dispatch path; CVO certs each guard on LIVE behavior.
