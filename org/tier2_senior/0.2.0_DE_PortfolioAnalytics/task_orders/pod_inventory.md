# Task Order — Pod Inventory: PortfolioAnalytics

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-pod-inventory-portfolio-analytics</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.2.0_DE_PortfolioAnalytics</issued_to>
    <date>2026-03-02</date>
    <status>complete</status>
  </metadata>

  <objective>
    Produce a pod_inventory.xml that gives you permanent ground-truth context
    about the PortfolioAnalytics pod. This is your activation document — read it
    at the start of every session to orient yourself without re-exploring the
    codebase each time. It synthesizes the RD page inventories with the portal
    API and shared component layer.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/Positioning/</page>
      <page>portal/src/pages/Attribution/</page>
      <page>portal/src/pages/FactorTilts/</page>
      <page>portal/src/pages/Valuation/</page>
      <page>portal/src/pages/Macroeconomics/</page>
      <page>portal/src/pages/Correlation/</page>
    </pages>
    <files>
      <!-- Source documents (read, do not modify) -->
      <file action="read">org/tier3_junior/0.0.4_RD_Positioning/deliverables/page_inventory.xml</file>
      <file action="read">org/tier3_junior/0.0.5_RD_Attribution/deliverables/page_inventory.xml</file>
      <file action="read">org/tier3_junior/0.0.6_RD_FactorTilts/deliverables/page_inventory.xml</file>
      <file action="read">org/tier3_junior/0.0.7_RD_Valuation/deliverables/page_inventory.xml</file>
      <file action="read">org/tier3_junior/0.0.8_RD_Macroeconomics/deliverables/page_inventory.xml</file>
      <file action="read">org/tier3_junior/0.0.9_RD_Correlation/deliverables/page_inventory.xml</file>
      <!-- Portal API endpoint files for this pod -->
      <file action="read">portal/src/api/endpoints/portfolio.ts</file>
      <file action="read">portal/src/api/endpoints/benchmarks.ts</file>
      <file action="read">portal/src/api/endpoints/valuation.ts</file>
      <file action="read">portal/src/api/endpoints/macro.ts</file>
      <!-- Shared hooks relevant to Yang-driven pages -->
      <file action="read">portal/src/hooks/useYangData.ts</file>
      <!-- Shared component layer -->
      <file action="read">portal/src/api/portal-proxy.ts</file>
      <!-- Output -->
      <file action="create">org/tier2_senior/0.2.0_DE_PortfolioAnalytics/deliverables/pod_inventory.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read all six RD page_inventory.xml files in full before writing anything.
      These are the ground truth for what each page owns. Note that this is the
      largest pod (6 pages) — all are Yang-pipeline driven.
    </requirement>
    <requirement id="2">
      Read each portal API endpoint file. Understand which Yang Lambda functions
      serve each page (yang-generate-positioning, yang-generate-holdings-attribution,
      yang-generate-factor-tilts, yang-generate-valuation, yang-generate-macro,
      yang-generate-correlation). Document the request/response contract per page.
    </requirement>
    <requirement id="3">
      Identify shared components that appear across multiple pages in the pod.
      The Yang pipeline pages likely share common panel components, data table
      patterns, and benchmark comparison UI.
    </requirement>
    <requirement id="4">
      Note which pages share a common data model (all are Yang-pipeline output).
      Document the shared upstream dependency in cross_pod_dependencies.
    </requirement>
    <requirement id="5">
      Produce pod_inventory.xml following the schema defined in acceptance criteria.
      Every section must be populated from actual file reads — no inference.
    </requirement>
    <requirement id="6">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      pod_inventory.xml exists at org/tier2_senior/0.2.0_DE_PortfolioAnalytics/deliverables/pod_inventory.xml
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
          Any imports from pages/components outside this pod.
          Include yang-pipeline as an upstream infrastructure dependency.
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
  </constraints>

  <dependencies>
    <dependency agent="0.0.4_RD_Positioning" task="page_inventory" status="complete"/>
    <dependency agent="0.0.5_RD_Attribution" task="page_inventory" status="complete"/>
    <dependency agent="0.0.6_RD_FactorTilts" task="page_inventory" status="complete"/>
    <dependency agent="0.0.7_RD_Valuation" task="page_inventory" status="complete"/>
    <dependency agent="0.0.8_RD_Macroeconomics" task="page_inventory" status="complete"/>
    <dependency agent="0.0.9_RD_Correlation" task="page_inventory" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.2.0_DE_PortfolioAnalytics/deliverables/pod_inventory.xml
    </deliverable>
  </deliverables>
</task_order>
```
