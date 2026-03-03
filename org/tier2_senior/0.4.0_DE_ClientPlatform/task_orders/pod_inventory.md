# Task Order — Pod Inventory: ClientPlatform

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-pod-inventory-client-platform</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-02</date>
    <status>complete</status>
  </metadata>

  <objective>
    Produce a pod_inventory.xml that gives you permanent ground-truth context
    about the ClientPlatform pod. This is your activation document — read it
    at the start of every session to orient yourself without re-exploring the
    codebase each time. ClientPlatform serves the advisor-facing layer of the
    portal — ModelPortfolios (Yang-driven) and AdvisorIntelligence (BD-driven).
    These two pages feed on fundamentally different pipelines.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/ModelPortfolios/</page>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <!-- Source documents (read, do not modify) -->
      <file action="read">org/tier3_junior/0.4.1_RD_ModelPortfolios/deliverables/page_inventory.xml</file>
      <file action="read">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/deliverables/page_inventory.xml</file>
      <!-- Portal API endpoint files for this pod -->
      <file action="read">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="read">portal/src/api/endpoints/aum.ts</file>
      <!-- Shared component layer -->
      <file action="read">portal/src/api/portal-proxy.ts</file>
      <!-- Output -->
      <file action="create">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read both RD page_inventory.xml files in full before writing anything.
      AdvisorIntelligence in particular is the most recently active development
      area (Leaderboard, Distribution view, Rolling Flows, Assets Overview were
      all developed in the Feb 23-27 sprint). Document its full tab/panel structure.
    </requirement>
    <requirement id="2">
      Read each portal API endpoint file. Note that AdvisorIntelligence draws
      from the BD pipeline (opal-partners-data, bd-portal-publisher, bd-portal-advisor-publisher,
      bd-client-detail) while ModelPortfolios draws from the Yang pipeline
      (yang-model-portfolio-benchmarks). Document this pipeline split clearly —
      it is architecturally significant for this pod.
    </requirement>
    <requirement id="3">
      Document the GEO/ADV cohort toggle and drill-down pattern in AdvisorIntelligence.
      This is a cross-panel pattern that the DE must understand to coordinate
      RD work correctly.
    </requirement>
    <requirement id="4">
      Produce pod_inventory.xml following the schema. Every section populated from
      actual file reads — no inference.
    </requirement>
    <requirement id="5">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      pod_inventory.xml exists at org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml
    </criterion>
    <criterion id="2">
      File follows this schema:
      &lt;pod_inventory&gt;
        &lt;metadata&gt; agent, pod, pages_owned[], date &lt;/metadata&gt;
        &lt;pages&gt;
          One &lt;page&gt; per portal page with:
            name, rd_agent, directory,
            &lt;summary&gt; 2-3 sentence description &lt;/summary&gt;
            &lt;tabs&gt; tab names and status &lt;/tabs&gt;
            &lt;primary_data_hook&gt; hook name and endpoint &lt;/primary_data_hook&gt;
            &lt;known_issues&gt; issues from RD inventory &lt;/known_issues&gt;
        &lt;/pages&gt;
        &lt;api_endpoints&gt;
          One &lt;endpoint&gt; per endpoint file with:
            file path, functions list, pages that use it
        &lt;/api_endpoints&gt;
        &lt;shared_components&gt;
          Components used by 2+ pages in this pod
        &lt;/shared_components&gt;
        &lt;cross_pod_dependencies&gt;
          Document the Yang pipeline dependency (ModelPortfolios) and BD pipeline
          dependency (AdvisorIntelligence) as separate upstream infrastructure items.
        &lt;/cross_pod_dependencies&gt;
        &lt;pod_health&gt;
          open_issues count, todo_count, summary sentence
        &lt;/pod_health&gt;
      &lt;/pod_inventory&gt;
    </criterion>
    <criterion id="3">
      All file paths and function names in the XML are verbatim from the source files,
      not paraphrased.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify any portal source files. This is a read-and-document task only.</constraint>
    <constraint>Do not modify the RD page_inventory.xml files.</constraint>
    <constraint>Do not commit any portal code from this task order.</constraint>
    <constraint>If a listed endpoint file does not exist, note it in pod_health as a missing contract.</constraint>
    <constraint>
      AdvisorIntelligence (0.0.14) is listed in the org chart but confirm the
      deliverable exists before treating it as complete input. If missing, note
      it as a blocker and document what is known from the portal source directly.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.1_RD_ModelPortfolios" task="page_inventory" status="complete"/>
    <dependency agent="0.4.2_RD_AdvisorIntelligence" task="page_inventory" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml
    </deliverable>
  </deliverables>
</task_order>
```
