<to_id>DATA_ANALYTICS.FE1</to_id>
<project>DATA_ANALYTICS</project>
<title>DATA_ANALYTICS FE1 -- ADVI dashboard PANEL -> frontend-COMPONENT -> PLATINUM-artifact -> Group-D-script threaded manifest, PER PARTNER (49F / Inflection / Cottonwood)</title>
<assigned_to>0.4.0_DE_ClientPlatform (DE-lead -- pipescript thread-traversal + comp-transform fields/schema-check + comp-which + comp-routes)</assigned_to>
<verify>3.0.0_SA_CVO (manifest COMPLETENESS -- every visible panel threaded, no silent Unknown; per-partner correctness)</verify>
<arch_gate>1.0.0_SA_CTO (FE1 feeds the portal-contract for the Schwab-raw-native canonize-gold rebuild; CTO arch-gates the rebuild)</arch_gate>
<issued_by>2.0.0_SA_COO (Andrew-direct 2026-06-25; under DATA_ANALYTICS "Gold-Analytics Clean-Rebuild"; frontend-down complement to A1's gold->ADVI backend-up ledger)</issued_by>
<issued_date>2026-06-25</issued_date>
<status>complete</status>
<!-- COMPLETE 2026-06-25 @ 98764fb65 (0.4.0_DE). Manifest: org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/DATA_ANALYTICS.FE1_advi_panel_platinum_groupd_manifest.md. All ADVI panels (PartnerAnalytics/Distribution/Advisors/Books/Profile/CohortA/InflectionInsights) enumerated -> shared component -> platinum key -> Group-D producer, per partner. pipescript spine + comp-platinum reverse + comp-transform. 2 producer gaps flagged (COT advisor_nna_canonical absent; header_metrics_fresh bd/cot). CVO verifies completeness. cc DS for portal-contract reconcile. --> 
<!-- GO: Andrew-direct 2026-06-25 (COO spawned 0.4.0_DE_ClientPlatform FOR this TO). CAN-START-NOW: read-only trace/manifest of the EXISTING ADVI dashboard + served estate; no ingest/DATA_PLATFORM dependency. -->

<objective>
Produce a MANIFEST of the threaded relationships from the ADVI dashboard FRONTEND down to the producing gold-tier, for each partner. The thread, per visible panel:

  ADVI dashboard PANEL  ->  underlying frontend COMPONENT(s)  ->  PLATINUM artifact(s) the component reads  ->  Group-D script(s) that GENERATE those platinum artifacts

Threaded PER PARTNER: 49F, Inflection, Cottonwood. This is the FRONTEND-DOWN complement to DATA_ANALYTICS.A1 (which threads gold-script -> output -> ADVI/MDPF consumer backend-UP) and to the Schwab-raw-native reframe's portal-field-requirements (DS, backend D-tier): FE1 + those converge on the single PORTAL CONTRACT -- exactly which platinum fields each rendered panel needs, and which Group-D scripts are therefore portal-load-bearing (essential) vs not. Directly feeds the canonize-gold essential-vs-agnostic classification + the lean rebuild.
</objective>

<the_work>
1. ENUMERATE every visible panel on the ADVI dashboard, BY PANEL -- the complete set (not a sample). Match each panel to its underlying frontend component(s) (the React/portal component that renders it). Use comp-transform (fields / schema-check) + the portal source as the rail (not raw grep).
2. PIPESCRIPT-TRACE each panel/component's data dependency: which PLATINUM artifact(s) the component reads, and which Group-D script(s) generate those platinum artifacts. Use `pipescript <name>` (named-thread estate traversal -- the tool Andrew named: every resource + producers->served->frontend + owning tool, whole estate, NO silent Unknown) as the spine; comp-which to route any sub-question; comp-routes if a serving-path/4xx ambiguity arises.
3. THREAD PER PARTNER (49F / Inflection / Cottonwood): for each partner, the panel -> component -> platinum -> Group-D chain, surfacing per-partner DIVERGENCES (a panel/platinum/Group-D path that differs or is absent for a given partner -- e.g. a partner with no valued history for a panel).
4. Output the MANIFEST: a structured, per-partner table/graph of the threaded relationships. Every panel resolved to its full thread OR explicitly flagged Unknown/gap (no silent omission).
</the_work>

<compiler_tools_mandate>
- BEFORE: comp-which to route the panel/platinum/Group-D questions; comp-transform fields/schema-check on the ADVI components (the DE mandate for components rendering data) to map panel->component->fields.
- DURING: `pipescript` (the named-thread estate traversal -- the load-bearing tool here, Andrew-named) to thread component->platinum->Group-D; comp-routes behaviors if any serving-path/4xx ambiguity.
- AFTER: the manifest is the deliverable; log every comp-tool run in the session log + append the org/compiler-tools-log.md line. Rail-grounded (pipescript/comp-transform), NOT raw grep.
</compiler_tools_mandate>

<cross_domain_coordination>
HARD coordination with 0.4.0_DS_ClientPlatform (DATA_ANALYTICS A1 + the Schwab-raw-native reframe's portal field-requirements / silver-DIM design). FE1 (panel->platinum->Group-D, frontend-DOWN) and DS's work (gold->consumer backend-UP + D-tier portal-field-requirements) are the TWO HALVES of the SAME portal contract -- they MUST reconcile into one. Coordinate with DS so the FE-panel field-needs and the backend D-tier/Group-D outputs converge (no panel needing a field no Group-D produces; no Group-D output no panel consumes = an agnostic-drop candidate). cc DS on the manifest; reconcile divergences with DS before RAVC2. NOT a code change -> no blast-radius (read-only trace); the shared resource is the portal-contract knowledge, not a file.
</cross_domain_coordination>

<acceptance_criteria>
1. EVERY visible ADVI dashboard panel enumerated by-panel + matched to its underlying frontend component(s). No panel omitted (CVO verifies completeness).
2. Each panel/component pipescript-threaded to its platinum artifact(s) -> the Group-D script(s) generating them -- the full panel->component->platinum->Group-D chain.
3. Threaded PER PARTNER (49F / Inflection / Cottonwood), surfacing per-partner divergences.
4. NO silent Unknown: any unresolved panel/component/thread explicitly flagged as a gap, not omitted (pipescript no-dead-end discipline).
5. Rail-grounded (pipescript + comp-transform, not raw grep). Manifest deliverable + session log (Compiler Tools section). RAVC2 COO; CVO verifies completeness + per-partner correctness; CTO arch-gate folds it into the portal-contract for the Schwab-raw-native rebuild.
</acceptance_criteria>
