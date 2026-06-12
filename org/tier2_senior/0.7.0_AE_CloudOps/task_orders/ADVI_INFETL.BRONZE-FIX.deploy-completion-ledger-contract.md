# Task Order: ADVI_INFETL.BRONZE-FIX (structural #5)
## Deploy-completion ledger contract + RED COO alarm (the NO-HALF-DEPLOYS enforcement)

**Project:** ADVI_INFETL (deploy-integrity hardening) — the structural answer to the 2026-06-12 P0
**Assigned to:** 0.7.0_AE_CloudOps (lead) — DESIGN WITH AE 0.6 (alongside structural #1 dual-prefix) + DS (the (f) FATAL loud-channel + (e) D-1 default legs)
**Priority:** P1 — Andrew-direct, the highest-leverage structural fix. NO-HALF-DEPLOYS is now CLAUDE.md NEVER-law (e38cc2b16).
**Authority:** Andrew-direct doctrine (his words: "half-finished deploys are red-alert material; a confirmed+begun deploy absolutely must finish in that session"); CTO relay 212246Z

---

## Context — why this is THE fix

The 2026-06-12 inf-ADVI P0 was ONE 06-11 cutover bundle that stranded THREE deploy legs (bronze-runner prefix mismatch, code/gold-vs-silver collision twins, mdpf registry v4) + an invisible on-instance FATAL. Each leg individually = a stranded-deploy (MDPF_COUNTS class). The COMMON failure: a multi-leg deploy was begun, partially landed, and NOBODY had a structural signal that legs were left unfinished. Andrew's demand: a confirmed+begun deploy MUST finish in-session, and a half-finished one must BLARE.

This TO is the "blaring error for COO" Andrew demanded + answers his "critical_paths should have caught this."

---

## Scope — the contract

### 1. Deploy-start: open a completion-ledger entry with the FULL manifest
Every multi-leg deploy (cutover bundle, pipeline-script deploy touching >1 S3 prefix/activation step, container rebuild + code push) OPENS a change_management ledger entry at deploy-START declaring its COMPLETE manifest:
- every S3 prefix it must land (code/bronze, code/bronze-runner, code/gold, code/silver, registry, etc.)
- every activation step (container rebuild, runner sync, trigger arm)
- the verification proof required per leg (comp-pipescript deployed MATCH per prefix — leverages TOOL-03's all-prefix coverage)

Rides the existing §10.6 ledger machinery — entry-OPEN at start, entry-CLOSE on full verification. Same pattern as approval-as-entry.

### 2. Deploy-completion: close ONLY when every leg verifies
The entry closes ONLY when every declared leg has its MATCH/verification proof. A leg without proof = entry stays OPEN.

### 3. RED COO alarm on unclosed-at-session-end
An OPEN completion-ledger entry at session end (or after a deploy-window timeout) fires a RED alert to COO via broker push (the loud channel). This is the structural catch: a half-finished deploy cannot end a session silently — it blares to the COO.

### 4. CONSISTENCY MANDATE (Andrew explicit)
The contract applies to EVERY deploy leg uniformly — orion-api AND eclipse AND mdpf, same standard. Two+ endpoints, one contract. (Pairs with: required-dim quorum #2, chain-liveness alarms, source-vintage #4, deployed-check coverage TOOL-03 — all consistency-mandated across legs.)

---

## Design collaboration (CTO-directed)
- AE 0.7 (lead) + AE 0.6: design alongside structural #1 (dual-prefix collapse — same root class; the ledger's per-prefix MATCH leg uses #1's canonical prefixes + TOOL-03's coverage)
- DS: the (f) FATAL loud-channel (an on-instance FATAL must surface, not stay invisible) + (e) D-1 default — these are the runtime-failure-visibility companions to the deploy-completion-visibility this TO provides

---

## Acceptance Criteria

- AC1: deploy-start opens a §10.6 completion-ledger entry with the full multi-leg manifest (every prefix + activation + verification-proof-required)
- AC2: entry closes ONLY when every leg has its MATCH/verification proof
- AC3: an unclosed entry at session-end / window-timeout fires a RED broker-push alert to COO
- AC4: contract applies uniformly to orion-api + eclipse + mdpf legs (consistency mandate)
- AC5: replay the 2026-06-12 bundle: opening its 3-leg manifest (bronze-runner + gold/silver + registry) → 2 legs stranded → entry stays OPEN → RED COO alarm fires (the incident is now caught structurally)
- AC6: rides existing §10.6 machinery (no parallel system); entry-closure IS the completion proof

## RAVC2 to COO
Commit + the contract design + AC5 replay (the 06-12 bundle now blares) + the consistency-mandate coverage proof (orion+eclipse+mdpf). CC 1.0.0_SA_CTO + 3.0.0_SA_CVO + 0.6.0_AE + 0.4.0_DS (design collaborators).

---

*Dispatched by 2.0.0_SA_COO 20260612T212300Z — Andrew-direct full-drive*
*CTO relay 212246Z; NO-HALF-DEPLOYS NEVER-law e38cc2b16; design-with-AE-0.6 + DS*
