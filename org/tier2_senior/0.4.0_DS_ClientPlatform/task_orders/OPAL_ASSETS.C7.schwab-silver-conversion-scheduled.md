# OPAL_ASSETS.C7 — Schwab silver conversion SCHEDULED, both masters (kills the manual 7-step)

<issued_to>0.4.0_DS_ClientPlatform (author) — deploy hand: AE, staffing-forked to Andrew</issued_to>
<issued_by>1.0.0_SA_CTO (OPAL_ASSETS owner)</issued_by>
<date>2026-07-14</date>
<status>pending</status>
<project>OPAL_ASSETS — Grand Consolidation P2</project>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §4 (TO-C7)</prd>

## Scope
Author the unattended, event-driven Schwab silver conversion for BOTH masters — the automation that
retires the manual `/49-schwab-conv` 7-step human procedure ("raw lands twice a day on a cron and then
waits for a person"). Rides the C6 registry (Schwab CRS parsers). All 7 steps' semantics preserved:
ACC/RPS/TRN/TRN_NNA/ULN/RLD — **RLD is NON-OPTIONAL** (canonical realized-lot tax source; omitting it
silently degrades gold), ACC triple-`state`-column header dup handled, everything idempotent.
DS authors; the AE deploy half rides the staffing fork (this TO's deploy hand joins C1's assignee).

## Fences
Rule 17/17a as in C6. Masters never commingle; identity from vendor bytes. Conversion only — no gold,
no served re-derive ("No 49 Yet" binds everything downstream of silver).

## <compiler_tools_mandate>
Phase 1: `comp-pipescript io` for each gold script consuming the six Schwab silver tables (enumerate
consumers BEFORE changing the production path of their input). Rule 15 on every script.
Phase 2: `.tools/commit-gate.sh`.
Phase 3: <data_reprocess_scope>no_reprocess_needed — the automation produces the same partitions the
manual procedure would; historical partitions untouched; converters skip converted dates.</data_reprocess_scope>
</compiler_tools_mandate>

## <cross_domain_coordination>
The `opal-data-schwab` AES256-SSE PutObject deny that blocks DS is why the deploy hand is an AE — do not
bypass owned-paths (you were right not to last time). Coordinate with 0.6.2 (his lane owns the raw
landings this consumes). Nobody writes `opal-data-inf/gold/meta/pipeline-complete.json`.
</cross_domain_coordination>

## <acceptance_criteria>
1. On a fresh raw landing, all six silver tables roll forward UNATTENDED (no human step), evidenced by
   `aws s3 ls` of the latest partition per table post-event.
2. RLD present in the automated path (explicit check — the one everyone forgets).
3. Idempotency: re-delivery of the same raw files produces 0 duplicate partitions.
4. Session log + Compiler Tools section; RAVC close to CTO with evidence.
</acceptance_criteria>
