# TASK ORDER — DATA_SSOTMG.TO-7

<issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete</status>
<!-- RAVC2 2026-06-29 by 0.4.0_DS_ClientPlatform~B (commit 6d48d4782). dim_advisor_role enriched (schema 2.0): implementor/consultant/local_ops/additional_advisor + 6 split-% from BD silver/allocations, bridged via xref, roles_source='bd-allocations-bridge' + roles_source_as_of bd-flagged (AC#1+2). 82% bridged, 98% architect-coherent, 81% split-sum~100. G11 re-materialized carrying all 13 BD-bridged fields (Wave-2 parity substrate); G12/G13 clean (G13 AUA ties G11). Co-own guards honored (idempotent --date/asof contract, write in canonical/schwab/silver, coherence-flag-not-overwrite). Residual gaps DISTINCT (AC#3): fee-coverage 8.3% (separate xref issue), G13 split-weighted attribution (next parity step, CVO formula coordination). RAVC base-DS(co-own)+COO + CC CTO. -->
<priority>HIGH — the WAVE-2 cutover parity PREREQ (CTO PRD re-issue 866670ca0). Without it the canonical advisor surfaces can't parity-match BD's served leaderboard.</priority>
<date>2026-06-29</date>

## Context

CTO re-issued the DATA_SSOTMG_PRD (866670ca0) staging the cutover into 2 WAVES: WAVE-1 = custodial core
(G1-G10, independent, cuts over FIRST); WAVE-2 = advisor surfaces (G11-G13), GATED on the
dim_advisor_role reaching parity. TO-3 built G11-G13 (d81ea44a0) on the LEAN dim
(architect/manager/money_manager only) — but implementor/consultant/local_ops + split-% (the fields
Andrew called "delicate") live in BD silver/allocations, NOT in the canonical dim, and fee coverage is
only 8.3% (static xref). So the lean dim CANNOT parity-match BD's served advisor leaderboard/partner-
analytics. This enrichment is the WAVE-2 parity prereq (CTO PRD §7 new TO + §8 deltas).

Assigned to DS~B: you built G11-G13 on the lean dim + just ground-truthed the exact BD-allocation
advisor-fields in the DERISK-2 census, so you know precisely what's missing — best-positioned. It's a
0.4.0 DS silver authoring script (build_dim_advisor_role.py), so COORDINATE with base-DS (same lane,
owns the silver-dim authoring + build_canonical_daily.py) to keep the silver-dim coherent + avoid a
collision on the authoring file.

## Objective

Enrich the canonical dim_advisor_role to carry the full advisor model — implementor / consultant /
local_ops roles + the split-% — sourced from BD silver/allocations, so the WAVE-2 advisor gold
surfaces (G11-G13) can reach parity with the BD-served leaderboard.

## Scope

- Add to the canonical dim_advisor_role (from BD silver/allocations): implementor, consultant,
  local_ops roles + the advisor split-% allocations (beyond the current architect/manager/money_manager).
- Honest provenance: every BD-sourced field carries the bd-source flag + source_as_of (same AC#2 pattern
  as G11-G13) — Schwab-native vs BD-bridged distinguishable.
- Re-materialize G11-G13 on the enriched dim (the parity target) OR confirm they pick up the enriched
  dim cleanly. The fee-coverage limitation (8.3% static xref) is a SEPARATE issue (improves on xref
  refresh) — note it, don't conflate it with the role/split-% enrichment.

<compiler_tools_mandate>
- comp-pipescript io build_dim_advisor_role.py (column gaps + the G11-G13 consumers) before write.
- ds-commit-gate; from __future__ import annotations (Rule 15).
- Ground the new fields against the actual BD silver/allocations source (cite it); flag every bd-sourced field.
</compiler_tools_mandate>

<cross_domain_coordination>
SAME 0.4.0 DS lane as base-DS (which owns build_dim_advisor_role.py / build_canonical_daily.py silver authoring) — COORDINATE the authoring-file edit with base-DS to keep the silver-dim coherent (you author the enrichment; base-DS reviews/co-owns the silver-authoring file). Reads BD silver/allocations (the BD-bridged source — the thin tether). Feeds the WAVE-2 G11-G13 parity (CVO's TO-4 harness Class-B/expected-divergence surfaces depend on it). NOT daily-wired yet (D4 cadence open).
</cross_domain_coordination>

<acceptance_criteria>
1. dim_advisor_role carries implementor/consultant/local_ops + split-%, sourced from BD silver/allocations, bd-source-flagged.
2. G11-G13 re-materialized (or confirmed clean) on the enriched dim — the WAVE-2 parity target.
3. The enrichment is parity-sufficient for the BD-served advisor leaderboard (or the residual gap — e.g. the 8.3% fee coverage — is explicitly enumerated as a separate known limitation, not silently folded).
4. Per-table RAVC to 2.0.0_SA_COO + CC 1.0.0_SA_CTO (the WAVE-2 parity gate input) + coordinate-confirm with base-DS on the silver-authoring file.
</acceptance_criteria>

## Note

Wave-2 GATE: this enrichment + the CVO parity harness reaching CLEAN on the advisor surfaces is what
gates the Wave-2 cutover. Andrew §8 decision (a) "implementor/split-% enrichment PRIORITY — how close
Wave-2 trails Wave-1" is queued; build the enrichment now (it's the prereq regardless of the cadence call).
