# Task Order: NFRA_DEBTSCAN.TOOL-01

**Status:** complete -- comp-pipescript deployed all-PIPELINE_MAP-tree scope (b5050f6b2); inf/cot/mdpf UNKNOWN-VINTAGE blind spot closed; RAVC2 to COO filed. [recon 2026-06-16 COO]

## comp-pipescript all-PIPELINE_MAP-tree scope (firm-scoped + mdpf)

**Project:** NFRA_DEBTSCAN (tooling sub-track)
**Assigned to:** 0.6.0_AE_PartnerETL
**Priority:** P1 — cut ahead of DS DEBTSCAN freshness sweeps (CTO CONCUR 184705Z + CVO CC 184603Z)
**Authority:** CTO cleared (no scoping round) — Andrew-direct 'absolutely need' via CVO relay 184542Z
**Precedent:** NFRA_COT_TOOLING 6bc1f1ce3 (COT auto-routing, same class: tool-coverage fill under ratified architecture)

---

## Context

comp-pipescript (`.tools/pipeline_cli.py`) deployed/io/dag modes enumerate only the bd-tree-rooted
script namespace. inf/cot/mdpf scripts never appear in sweep mode because the default walk is
bd-rooted. Bucket overrides exist (`pipeline_cli.py:1450/1458/1464`, `safe_deploy_core.PIPELINE_MAP`)
but the enumeration surface does not key off them.

Effect: DEBTSCAN DS-lane freshness sweeps for inf/cot/mdpf file with UNKNOWN-VINTAGE caveat (same
deployed-blind stranded-deploy blind spot as MDPF_COUNTS 2026-06-05).

---

## Scope (5 CTO constraints, non-negotiable)

**1. ALL PIPELINE_MAP trees** — bd + inf + cot + mdpf (not just 3 firms). mdpf S3 layout is
`code/scripts/<layer>/` — its bucket override already exists at `pipeline_cli.py:1464`.

**2. SINGLE SOURCE** — tree enumeration + bucket resolution derive from
`safe_deploy_core.PIPELINE_MAP` (import it). No hand-copied map in pipeline_cli (it will drift).
Existing if-chain overrides may stay but enumeration keys off the canonical map.

**3. FIRM SEPARATION** — each tree's deployed-check reads ONLY its own bucket. No cross-bucket
fallback. Cross-firm guard classes apply to tooling reads.

**4. SWEEP OUTPUT PROVENANCE** — new flags:
- `--firm {bd,inf,cot}` or `--pipeline <any-PIPELINE_MAP-key>`: single-tree scope
- path auto-detect: derive from script path → PIPELINE_MAP key
- sweep default (no flag) = ALL trees
Every MATCH/STALE/MISSING row names the bucket it checked. An un-attributed MATCH is how blind spots
hide.

**5. DOCS SAME-TO** — update `org/modules/graph/graph-call-manifest.yaml` (cloud.* comp-pipescript
entries) + `.tools/comp-tools.yaml` comp-pipescript stanza. bd/inf regression spot-checks per
COT_TOOLING precedent.

---

## Acceptance Criteria

- `comp-pipescript deployed data/inf/scripts/gold/X.py` → queries opal-data-inf, returns MATCH/STALE/MISSING
- `comp-pipescript deployed data/cot/scripts/gold/X.py` → queries opal-data-cot
- `comp-pipescript deployed data/mdpf/scripts/gold/X.py` → queries opal-data-mdpf
- `comp-pipescript deployed --firm cot` → sweeps all COT gold scripts against opal-data-cot
- `comp-pipescript deployed` (no args) → sweeps ALL PIPELINE_MAP trees; each row names its bucket
- No cross-bucket read on any deployed check (firm separation enforced)
- `graph-call-manifest.yaml` + `comp-tools.yaml` updated with all-trees scope
- bd regression: existing bd cases MATCH/STALE as expected (no regression)
- inf regression: at least one real MATCH against a known-deployed inf script

---

## Zero-mutation guarantee

Read-only tooling change. No S3 writes, no gold/silver/bronze modifications, no TF changes.
Pre-commit gate: `.tools/ds-commit-gate.sh` for any .py edits. No gold-runner invocations.

---

## RAVC2 to COO

Include in body:
1. Commit hash
2. `comp-pipescript deployed data/inf/scripts/gold/<real_script>.py` output (bucket + MATCH/STALE)
3. `comp-pipescript deployed --firm cot` first 5 rows (pipeline + bucket named)
4. graph-call-manifest.yaml + comp-tools.yaml diff excerpt (updated stanzas)
5. bd regression spot-check (1 known MATCH case)

CC 3.0.0_SA_CVO on RAVC2.

---

*Dispatched by 2.0.0_SA_COO 20260612T1848Z*
*CTO cleared 184705Z (no scoping round, Andrew-direct 'absolutely need')*
*CVO CC 184603Z (Andrew-direct priority, DEBTSCAN inf/cot de-caveat)*
