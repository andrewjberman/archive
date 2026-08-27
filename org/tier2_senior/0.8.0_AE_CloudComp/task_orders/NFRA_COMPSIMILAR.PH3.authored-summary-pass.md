<task_order>
<to_id>NFRA_COMPSIMILAR.PH3</to_id>
<title>Authored one-off summary pass — populate resource_summaries for the ~549 prime targets so comp-similar has real coverage, not derive-at-scan stubs</title>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<date>2026-07-17</date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_COMPSIMILAR, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
<priority>P3 (Andrew batch 2026-07-17). GATE: NFRA_COMPSIMILAR.PH2 landed (engine + supersede mode work).</priority>

<authority>
PRD phase ph3 (Andrew-scoped): the corpus is only as good as its summaries. derive-at-scan (PH1) gives v1
stubs; the real signal needs AUTHORED summaries for the prime targets (~549 named in the PRD) — the
consolidation-relevant resources where superseded-twin detection actually pays off.
</authority>

<gate>
DO NOT GO until PH2 has landed (the comp-similar engine + --supersede exist and dogfood-pass). Authoring
summaries before the engine works is premature — you can't validate a summary's usefulness without the scan.
COO fires GO on PH2 acceptance.
</gate>

<scope>
Author real, concise, functional summaries (what each resource DOES) for the ~549 prime targets, written into
the resource_summaries Iceberg table (append-only, ARN-keyed, one Nessie commit per batch). Prioritize the
consolidation-associated resources first (the ones OPAL_TAXONOMY/OPAL_CONSOLIDATION touch) so comp-similar's
supersede mode covers the live decommission surface. This is a DATA-authoring pass — no alert leg.
</scope>

<compiler_tools_mandate>
  <phase id="3" when="during/after the pass">
    <step>
      <run>After the pass: comp-similar --supersede over the newly-populated corpus vs the derive-at-scan-only baseline</run>
      <expect>Authored summaries measurably SHARPEN the supersede ranking vs stubs (the known superseded pairs rank higher / with less noise). Print the coverage denominator: N of ~549 authored, M ARNs still stub.</expect>
      <if_mismatch>Surface: if authored summaries don't improve the scan, the summary schema or the BM25 tuning needs review before scaling the pass.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Feeds the same OPAL_LCLRPO disposal pipeline + the census's unused-by-heat column. The node-writer enrichment
(making summaries a first-class graph_nodes field so they populate automatically, retiring the one-off pass) is
a SEPARATE follow-on per the PRD — flag it when this pass proves the value, don't fold it here.
</cross_domain_coordination>

<acceptance_criteria>
1. ~549 prime-target summaries authored into resource_summaries (coverage denominator printed: authored vs stub).
2. Consolidation-associated resources prioritized first (the live decommission surface covered).
3. Measured: authored summaries sharpen the --supersede ranking vs the derive-at-scan baseline.
4. Session log reproduces the mandate run + the coverage denominator.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/NFRA_COMPSIMILAR_PRD.md (ph3)</ref>
  <ref type="depends">NFRA_COMPSIMILAR.PH2 (engine must land first)</ref>
</references>
</task_order>
