# Task Order: ADVI_INFETL.BRONZE-FIX (structural #1)

> **[CLOSED — COMPLETE-SUPERSEDED 2026-06-29, COO 2.0.0_SA_COO]** Absorbed into Andrew-confirmed-closed ADVI_INFETL (closed 2026-05-25). The dual-prefix collapse was the root-cause P0 fix shipped in recovery. MSTR-delegated orphan cleanup (20260629T130229Z).
## Collapse the code/bronze vs code/bronze-runner dual-prefix (root cause of the 2026-06-12 inf-ADVI P0)

**Project:** ADVI_INFETL (bronze deploy-path hardening)
**Assigned to:** 0.6.0_AE_PartnerETL (bronze pipeline; coordinate AE 0.7 on S3/runner-sync side)
**Priority:** P1 — structural prevention of the live P0 class (CTO-assigned post-recovery TO #1)
**Authority:** CTO root-cause + structural-TO assignment (relay 204522Z); Andrew live-P0 4:37p ET 2026-06-12
**Gate:** finalize against DS's R1-R5 recovery once it lands (the recovery confirms the canonical prefix)

---

## Context — the incident

2026-06-12 inf ADVI showed $202M vs Orion $204.6M. Root cause: yesterday's 8-dim orchestrator was uploaded to `code/bronze/`, but the inf bronze RUNNER syncs from `code/bronze-runner/` which held a May-8 orchestrator WITHOUT the transactions dim. Today's first run pulled everything except transactions → `_BRONZE_COMPLETE` falsely reported success → gold held fail-closed → platinum froze 06-11. Classic stranded-deploy (MDPF_COUNTS family), this time caused by the DUAL PREFIX: two S3 locations for the same logical bronze code, with the runner reading the wrong one.

---

## Scope

1. **Determine the canonical bronze code prefix** for the inf runner (which does the runner actually sync from — `code/bronze-runner/`? confirm via the runner's sync command + live S3). DS's recovery (R1) syncs the current orchestrator to the runner prefix — align with whatever R1 establishes as canonical.
2. **Collapse to ONE prefix.** Either: (a) the runner syncs from `code/bronze/` (consolidate to the standard prefix the deploy-cycle uploads to), or (b) the deploy-cycle uploads to `code/bronze-runner/` (align the upload target to where the runner reads). Pick the one that makes the deploy-cycle's upload target == the runner's sync source. Document the choice + why.
3. **Update safe_deploy_core / file_to_s3_target** so the Rule-13 deploy-cycle uploads bronze to the canonical prefix (no more split).
4. **Verify** via TOOL-03 (`comp-pipescript deployed data/inf/scripts/bronze/orchestrator.py` → MATCH against the canonical prefix) once TOOL-03 lands — the deploy is now tool-verifiable.
5. **Sweep the other firms** (bd/cot) for the same dual-prefix exposure; collapse if present.

---

## Acceptance Criteria

- AC1: ONE canonical bronze prefix per firm; deploy-upload-target == runner-sync-source (proven)
- AC2: safe_deploy_core updated; a bronze deploy lands where the runner reads
- AC3: TOOL-03 `comp-pipescript deployed` on a bronze script → MATCH (tool-verified, no hand-diff)
- AC4: bd/cot dual-prefix exposure swept + collapsed if present
- AC5: the May-8 stale orchestrator at the abandoned prefix removed (or documented if intentionally retained)

## RAVC2 to COO
Commit + canonical-prefix decision + TOOL-03 MATCH proof + cross-firm sweep result. CC CTO + CVO.

---

*Dispatched by 2.0.0_SA_COO 20260612T204800Z — Andrew-direct full-drive (no slowdown)*
*CTO structural-TO #1; finalize against DS R1-R5 recovery*
