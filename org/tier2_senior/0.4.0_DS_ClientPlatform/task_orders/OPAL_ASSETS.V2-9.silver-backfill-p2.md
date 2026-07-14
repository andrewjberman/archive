# OPAL_ASSETS.V2-9 — backfill P-2: historical conversion over every held bronze byte

<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO (V2 decomposition; PRD author 1.0.0_SA_CTO)</issued_by>
<date>2026-07-14</date>
<status>staged</status>
<go>HARD GATE: V2-8 converters deployed + CTO first-conversion signoff. COO dispatches the GO.</go>
<project>OPAL_ASSETS — V2 Phase II silver conversion layer</project>
<prd>docs/architecture/OPAL_ASSETS_V2_PRD.md §3 ruling 24 + V2-9 (@ 53ba45c5f); inherits CONSOLIDATION_PRD v1.6.0 whole</prd>

## THE GOAL (ruling 24 — verbatim)
"Historical conversion over every held bronze byte runs the SAME converter code as the event path (one
pattern per channel, backfill and daily share it — the v1.5.0 population law), operator-driven,
S3-checkpointed, idempotent skip-if-landed, re-invokable to convergence."

## <compiler_tools_mandate>
Denominators enumerated at run time per folder (13b). Per-folder set-identity verdicts committed
(ruling 25). `meta/backfill-status.json` updated BY THE PROCESS ITSELF (V2-6's schema). A re-run lands 0
(idempotency exercised, not asserted).
</compiler_tools_mandate>

## <acceptance_criteria>
1. Every held bronze folder has its silver counterpart or a NAMED honest hole (the 10 inf parquet-only
   dates stay honest holes per ruling 16).
2. Convergence proven: final re-invoke = 0 conversions, set-identity verdicts clean, committed.
3. backfill-status.json reflects the end state, written by the process.
</acceptance_criteria>
