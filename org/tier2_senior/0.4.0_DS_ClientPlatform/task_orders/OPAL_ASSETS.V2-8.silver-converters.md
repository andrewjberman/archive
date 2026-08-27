# OPAL_ASSETS.V2-8 — the silver converters (typechecked fact-table parquets, per channel family)

<issued_to>0.4.0_DS_ClientPlatform (orion/eclipse/cot mirror-silver + ETF families + C6 registry integration; smartx silver step: 0.5.0 co-owns) + 0.6.2_AE_PartnerETL (SCHWAB family -- see AMENDMENT-1)</issued_to>
<amendment id="1" date="2026-07-14" by="2.0.0_SA_COO">SCHWAB-FAMILY CARVE TO 0.6.2 per Andrew-direct ~07:5xZ (verbatim, recorded+broadcast in 0.6.2's 075349Z msg: "i think the next thing you can do is yes, figuring out the silver converter scripts for parquet-ing those bronze schwab files into nice columnar typed silver"). Precedent: the staging-side six-table Schwab converters are AE-owned by exception (Rule 13 SSE-deny carve); T1 trailer recon (ruling 11a) is 0.6.2 domain. Scope of the carve: schwab/08335338 + schwab/08242234 monolith bronze -> silver ONLY. Authoring may start NOW (pre-gate, like the lambda-contract note); DEPLOY stays behind the V2-5 cert + V2-7 container + CTO converter code-review, unchanged. 0.6.2 builds against the V2-7/V2-8 contract note (0.7.0 AE-half @ 29f4f1c89; DS cells pending) and the C6 registry patterns -- coordinate with DS, do not fork the registry. All other TO terms (ruling 23/25, INF-hold legality note, acceptance criteria) bind 0.6.2's family identically.</amendment>
<amendment id="2" date="2026-07-14" by="2.0.0_SA_COO">AC-6 (Schwab family, measured case -- CTO 075452Z from the 49F gold drill): every CRS-type converter is PASSTHROUGH-COMPLETE -- every vendor column preserved. The evidence: data/canonical/schwab/silver/build_dim_account.py docstring records that the EXISTING opal-data-schwab ACC silver is LOSSY ("drops title/CustType/address that the rebuild needs") and forced that consumer back to 01_raw/CRS*.ACC -- the exact Rule-17 field-slimming scar. The monolith silver must be the layer OPAL_RUNNERS dim builders read (PRD sec-3: boxes read only monolith silver) -- known-needed ACC fields include account id, full title text, CustType/entity_type, money_manager, strategy, taxpayer fields, and this list is a FLOOR never a filter: passthrough means ALL columns. Acceptance check: converter output schema column-count == vendor record column-count (+ standardized dtypes), asserted in the conversion manifest.</amendment>
<amendment id="3" date="2026-07-14" by="2.0.0_SA_COO">TABLE NAMING (Andrew-direct ~09:1xZ, dictionary v0.4 @ 8c2574c2e, via CTO 091657Z): silver tables = fact_{type} COMPLETE vendor tables; runner gold = tight dim_* projections; gold is the one parse-down point. BINDING NOW for the CRS family (0.6.2: rename pre-deploy). For every OTHER family (DS mirror-silver + ETF, 0.5.0 smartx incl. its five plan-pinned names): whether fact_ extends channel-wide is PARKED as an open cell in OPAL_ASSETS_V2_LAMBDA_CONTRACT.md -- build logic now, keep the table-name a one-line constant, and the cell settles (Andrew's word or contract review) BEFORE each family's first deploy. No mid-build churn.</amendment>
<issued_by>2.0.0_SA_COO (V2 decomposition; PRD author 1.0.0_SA_CTO)</issued_by>
<date>2026-07-14</date>
<status>complete -- SPRING-CLEAN 2026-08-25 (S2): <project> field repaired from "OPAL_ASSETS — V2 Phase II silver conversion layer" to OPAL_ASSETS, which is complete-as-superseded. Closed as a record act, not a work verdict. Prior status: pending</status>
<go>BUILD NOW, both families -- ANDREW-DIRECT (2026-07-14 ~08:4xZ, COO session, verbatim: "Yes, start silver builds ahead of the certificate") SUPERSEDES the V2-5-cert half of the hard gate for the BUILD. Author + build converters against contract note v1 (d68982c1e). UNCHANGED: deploy lands into V2-7's applied container; CTO's converter code-review gates every converter before deploy; CTO's first-conversion signoff (AC-3) stands; the V2-5 certificate continues in parallel as the completeness instrument.</go>
<project>OPAL_ASSETS</project>
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
5. Schwab Group-A column naming UNBLOCKED (Andrew ruling ~05:5xZ ET via CTO 20260714T060537Z,
   superseding ruling 23's waits-on-doc clause): mechanical/positional names + empirical dtypes NOW;
   the FAM/SLM vendor doc, when it arrives, becomes a documentation OVERLAY in the meta layer — never
   a schema change.
</acceptance_criteria>
