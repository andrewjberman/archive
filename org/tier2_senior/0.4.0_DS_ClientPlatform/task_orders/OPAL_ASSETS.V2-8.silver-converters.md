# OPAL_ASSETS.V2-8 — the silver converters (typechecked fact-table parquets, per channel family)

<issued_to>0.4.0_DS_ClientPlatform (smartx silver step: 0.5.0 co-owns)</issued_to>
<issued_by>2.0.0_SA_COO (V2 decomposition; PRD author 1.0.0_SA_CTO)</issued_by>
<date>2026-07-14</date>
<status>staged</status>
<go>HARD GATE: V2-5 certificate accepted + V2-7 container landing (coordinate lambda names/handlers with 0.7.0 BEFORE his TF lands — that coordination may start immediately). CTO's converter code-review gates every converter before deploy.</go>
<project>OPAL_ASSETS — V2 Phase II silver conversion layer</project>
<prd>docs/architecture/OPAL_ASSETS_V2_PRD.md §3 rulings 23/25 + V2-8 (@ 53ba45c5f); inherits CONSOLIDATION_PRD v1.6.0 whole</prd>

## THE GOAL (ruling 23 — THE SILVER CONTRACT, verbatim)
"One converter lambda per channel family; pyarrow with EXPLICIT schema (never inferred); typed/asserted
vendor-shape boundary that RAISES loud on drift; Rule 17 scope EXACTLY (dedup + dtype standardization;
never slim/fillna/filter); Schwab parsers carry ruling-11a T1 trailer reconciliation (hard raise); every
converter emits its denominator and a persisted conversion manifest; grammar
`{source}/{scope}/silver/{fact_table}/` hive `date=` partitions (v1.2). Column naming for Schwab Group-A
waits on the FAM/SLM vendor layout doc (Andrew item, unchanged)."

C6 registry FOLDS IN (authored + mutant-exercised already — deploy it, don't re-derive). C7's deploy leg
completes here. ORDER: schwab (T1-recon pattern proven at `44a5328ce`) -> orion/eclipse/cot mirror-silver
-> ETF (monolith-native parquet form; legacy CSV silver keeps serving until the ruled cutover) -> smartx
(C5's silver step, 0.5.0 co-owns).

## >> THE INF-HOLD LEGALITY NOTE (CTO, verbatim mandate — read it EXACTLY, neither over- nor under-) <<
Mirror-silver (orion/eclipse/cot) is **FUNCTIONALLY LEGAL under the INF hold**: monolith-native
converters writing `opal-data-assets` silver advance NOTHING in the held INF chain — the functional
test ("would doing this ADVANCE the INF chain?") passes. **The frozen-3 stay untouched**
(`build_assets_dim.py` · `_orion_api_silver_lib.py` · `convert_transactions_to_silver.py`) — this is
NEW code in NEW territory. Do not self-block on the hold; do NOT read this as license to touch the
frozen libs or any INF-chain resource. Nothing writes `opal-data-inf/gold/meta/pipeline-complete.json`.

## <compiler_tools_mandate>
Ruling 25 verbatim: "Set-identity per folder (every bronze partition has its silver counterpart or a
named honest hole), mutant-exercised before first real conversion; meta manifests disjoint from guarded
prefixes; nothing event-triggers on meta keys." Every .py `from __future__ import annotations` (Rule 15);
`.tools/commit-gate.sh`; `comp-pipescript io` before editing any gold-adjacent script; comp-blast note at
authoring (COO): `upsert_history` is NOT a graph node (in-file legacy ETF silver code — the seam you must
NOT touch until the ruled cutover); denominator printed on every conversion run.
</compiler_tools_mandate>

## <acceptance_criteria>
1. Per-channel converter deployed (TF-only, tagged), schema EXPLICIT, boundary RAISES on a planted
   drift mutant (transcript committed).
2. Silver set-identity guard mutant-exercised BEFORE first real conversion (ruling 25).
3. First real conversion signed off by CTO (silver first-conversion signoff is his gate).
4. Rule 17 compliance stated per converter (what dedup key, what dtype map, NOTHING else).
5. Schwab Group-A column naming BLOCKED-named on the FAM/SLM doc until Andrew's item closes — build the
   rest, leave that seam explicit.
</acceptance_criteria>
