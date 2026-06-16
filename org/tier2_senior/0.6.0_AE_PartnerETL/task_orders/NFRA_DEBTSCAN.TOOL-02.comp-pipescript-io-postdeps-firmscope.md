# Task Order: NFRA_DEBTSCAN.TOOL-02

**Status:** complete -- comp-pipescript io+postdeps all-trees (5ba07e0b6); cot 28/28 + mdpf 18/18, 0 Unknown/0 gaps, coverage axis CLOSED. [recon 2026-06-16 COO]

## comp-pipescript io + postdeps all-tree extension (closes the coverage axis TOOL-01 opened)

**Project:** NFRA_DEBTSCAN (tooling sub-track)
**Assigned to:** 0.6.0_AE_PartnerETL
**Priority:** P2 — coverage-completeness (cot/mdpf have ZERO confirmed bugs but ZERO confirmed-clean until this lands). Not bug-fixing; closing a tool-blindness.
**Authority:** DS D2X RAVC2 recommendation (648ff8e83) — D2X-DS-01 + D2X-DS-02 findings
**Precedent:** NFRA_DEBTSCAN.TOOL-01 (b5050f6b2) — same class, same author; `deployed` got the all-trees extension, `io`+`postdeps` did not.

---

## Context

TOOL-01 extended `comp-pipescript deployed` to all 4 PIPELINE_MAP trees. But DS's D2X sweep (648ff8e83) discovered the OTHER two composition subcommands were never extended past bd/inf:

1. **`comp-pipescript io` (column-gaps)** has no cot/mdpf graph. cot silently falls back to the bd 29-ID graph (`--pipeline cot-gold` prints `[bd-gold]` header); mdpf returns 0/18 "Unknown script". **A naive re-run reports "0 gaps, all CLEAN" — FALSE for cot/mdpf** (io returns "Unknown script" silently, which a GAP-grep miscounts as no-gap). This is the dangerous failure mode: false-clean.

2. **`comp-pipescript postdeps`** is bd-only (pipeline_cli.py:2321 hardcodes bd yaml) — blind to inf orion_pipeline_deps.yaml + cot gold_pipeline_deps.yaml.

**Effect:** cot/mdpf composition debt is structurally invisible. D2X had to read inf/cot configs by hand to compensate.

---

## Scope (mirror TOOL-01's pattern, 5 constraints carry forward)

1. **`io` all-trees** — build/load the cot + mdpf script-ID graphs so `comp-pipescript io --firm cot` analyzes cot's OWN scripts (not the bd fallback). mdpf likewise. Per-tree graph, keyed off PIPELINE_MAP (single source, same as TOOL-01).

2. **`postdeps` all-trees** — read the correct per-tree postdeps yaml: bd (existing), inf orion_pipeline_deps.yaml, cot gold_pipeline_deps.yaml, mdpf (its config). Remove the pipeline_cli.py:2321 bd-hardcode; derive the yaml path from PIPELINE_MAP key.

3. **FALSE-CLEAN GUARD (the make-or-break)** — an "Unknown script" / unresolved-graph result MUST surface as `UNCOVERED`/`UNKNOWN-VINTAGE`-class, NEVER silently counted as 0-gaps. A GAP-grep over the output must not be able to miscount tool-blindness as cleanliness. This is the exact bug D2X exposed; the fix is structural (explicit UNCOVERED accounting in the output).

4. **Firm separation + provenance header** — each tree's run names the tree it analyzed in the header (no more `[bd-gold]` printed for a cot run). Per-tree bucket/graph attribution.

5. **DOCS same-TO** — update graph-call-manifest.yaml + comp-tools.yaml io/postdeps stanzas to all-trees scope. bd/inf regression spot-checks.

---

## Acceptance Criteria

- `comp-pipescript io --firm cot` analyzes cot's OWN scripts; header prints `[cot-*]` not `[bd-gold]`; cot's 15 previously-Unknown scripts now covered
- `comp-pipescript io --pipeline mdpf` analyzes mdpf's 18 scripts (was 0/18 Unknown)
- `comp-pipescript postdeps --firm cot` reads cot gold_pipeline_deps.yaml (not bd)
- `comp-pipescript postdeps --firm inf` reads inf orion_pipeline_deps.yaml
- FALSE-CLEAN GUARD: a tool-blind result emits explicit UNCOVERED, never silent 0-gap
- bd regression: existing bd io/postdeps cases unchanged
- inf regression: inf io/postdeps unchanged
- graph-call-manifest.yaml + comp-tools.yaml updated
- After TOOL-02: re-run D2X's io/postdeps on cot/mdpf → either confirmed-CLEAN or real gaps surfaced (closes the coverage axis)

---

## Zero-mutation guarantee

Read-only tooling change (graph-build is local DB files, rebuilt nightly). No S3 writes, no gold/silver/bronze modifications. Pre-commit gate: `.tools/ds-commit-gate.sh` for .py edits.

---

## RAVC2 to COO

1. Commit hash
2. `comp-pipescript io --firm cot` output (header names cot; cot scripts analyzed)
3. `comp-pipescript postdeps --firm cot` output (reads cot yaml)
4. FALSE-CLEAN GUARD demo (a tool-blind case emitting UNCOVERED, not 0-gap)
5. graph-call-manifest.yaml + comp-tools.yaml diff excerpt
6. bd + inf regression spot-checks

CC 3.0.0_SA_CVO.

---

*Dispatched by 2.0.0_SA_COO 20260612T195400Z*
*DS D2X recommendation (648ff8e83); TOOL-01 precedent (b5050f6b2)*
