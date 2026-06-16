# Task Order: NFRA_DEBTSCAN.TOOL-03

**Status:** complete -- comp-pipescript bronze first-class + aux check-only prefixes (b2ff049ce); Rule-13 bronze-verifiability gap closed. [recon 2026-06-16 COO]

## comp-pipescript bronze + auxiliary-prefix coverage (closes the Rule-13 bronze-verifiability gap)

**Project:** NFRA_DEBTSCAN (tooling sub-track)
**Assigned to:** 0.6.0_AE_PartnerETL
**Priority:** P1 — Andrew-sourced field-report (via CVO relay 204408Z); closes a Rule-13 structural gap
**Authority:** Andrew field-report (an agent had to hand-diff the inf bronze orchestrator dim list vs S3 — no tool covers it); CVO relay 204408Z
**Precedent:** TOOL-01 (b5050f6b2, all-trees `deployed`) + TOOL-02 (io/postdeps) — same family, same author
**Timing:** ideally before tomorrow's COTETL bronze-gate review (so the gate's deploy check is tool-verified, not hand-diffed); hand-diff is the fallback if not ready — NOT a hard blocker. Respawn tomorrow AM early (per AE 0.6 deferred-respawn).

---

## Context — the structural gap (CVO's sharpest framing)

CLAUDE.md Rule 13's deploy cycle requires `comp-pipescript deployed MATCH` for `data/*/scripts/{gold,silver,BRONZE}`. But TOOL-01's tree registry (pipeline_cli `_LABEL_TO_DEPLOYED_PIPELINE` → `*-gold`/`*-silver` branches) enumerates ONLY gold + silver per firm. **The tool structurally cannot produce the bronze leg** — so the Rule-13 cycle is UNVERIFIABLE for every bronze deploy, and the MDPF_COUNTS stranded-deploy class persists.

opal-data-inf/code/ carries EIGHT prefixes: `bronze/`, `bronze-runner/`, `cleanup/`, `exporter/`, `manual_api/`, `runner/` + `gold/`, `silver/`. The deployed-sweep covers 2 of 8. Real repo trees: `data/inf/scripts/bronze/orchestrator.py` (the hand-diffed one), `data/cot/scripts/bronze/` (COTETL's bronze gate is tomorrow AM — near-term value).

---

## Scope (3 parts, mirror TOOL-01/02 pattern)

### (a) Bronze trees — first-class deployed coverage
Extend the tree registry with per-firm bronze trees: repo `data/{black_diamond,inf,cot}/scripts/bronze` → `code/bronze/`, same MATCH/STALE/MISSING semantics as gold/silver. Keyed off PIPELINE_MAP (single source — constraint carries from TOOL-01).

### (b) Auxiliary prefixes — CHECK-ONLY trees (mdpf pattern)
`bronze-runner/`, `runner/`, `exporter/`, `cleanup/`, `manual_api/` where the repo-home → S3-prefix mapping is nonstandard: append as explicit documented CHECK-ONLY trees (the mdpf TOOL-01 precedent), so they're swept without corrupting the deploy gate. If a prefix's repo-home is ambiguous, surface it as UNCOVERED (not silent-clean — the TOOL-02 false-clean-guard discipline applies).

### (c) PIPELINE_MAP single-source
No hand-copied maps. Bronze + aux enumeration derives from safe_deploy_core.PIPELINE_MAP.

---

## Acceptance Criteria

- `comp-pipescript deployed data/inf/scripts/bronze/orchestrator.py` → queries opal-data-inf/code/bronze/, returns MATCH/STALE/MISSING (the hand-diff is now a tool call)
- `comp-pipescript deployed data/cot/scripts/bronze/<script>.py` → queries opal-data-cot/code/bronze/
- `comp-pipescript deployed --firm cot` → now includes the bronze leg
- Auxiliary prefixes (bronze-runner/runner/exporter/cleanup/manual_api) appear as CHECK-ONLY rows, each naming its bucket; ambiguous repo-home → UNCOVERED not silent-clean
- No cross-bucket read (firm separation); per-tree bucket banner
- bd/inf/cot gold+silver regression: unchanged (TOOL-01/02 cases still pass)
- graph-call-manifest.yaml + comp-tools.yaml updated (bronze + aux scope)

---

## Zero-mutation guarantee

Read-only tooling change. No S3 writes, no script modifications. ds-commit-gate for .py edits.

---

## RAVC2 to COO

1. Commit hash
2. `comp-pipescript deployed data/inf/scripts/bronze/orchestrator.py` output (the retired hand-diff)
3. `comp-pipescript deployed --firm cot` including the bronze leg (first rows)
4. Auxiliary-prefix CHECK-ONLY rows (named buckets) + any UNCOVERED
5. bd/inf/cot gold+silver regression spot-check (no TOOL-01/02 regression)
6. graph-call-manifest.yaml + comp-tools.yaml diff excerpt

CC 1.0.0_SA_CTO + 3.0.0_SA_CVO.

---

*Dispatched (queued for AE 0.6 tomorrow-AM respawn) by 2.0.0_SA_COO 20260612T204400Z*
*Andrew field-report via CVO relay 204408Z; TOOL-01/02 family*
