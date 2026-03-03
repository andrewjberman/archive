# Task Order — Pod Inventory: TradingOperations

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-pod-inventory-trading-operations</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-02</date>
    <status>complete</status>
  </metadata>

  <objective>
    Produce a pod_inventory.xml that gives you permanent ground-truth context
    about the TradingOperations pod. This is your activation document — read it
    at the start of every session to orient yourself without re-exploring the
    codebase each time. This pod contains the most operationally sensitive pages
    (PM optimization, trade submission) and has the richest Lambda backend of
    any pod. Thorough documentation here is especially critical.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/PortfolioManagement/</page>
      <page>portal/src/pages/TradeSubmission/</page>
      <page>portal/src/pages/DataRefresh/</page>
    </pages>
    <files>
      <!-- Source documents (read, do not modify) -->
      <file action="read">org/tier3_junior/0.3.1_RD_PortfolioManagement/deliverables/page_inventory.xml</file>
      <file action="read">org/tier3_junior/0.3.2_RD_TradeSubmission/deliverables/page_inventory.xml</file>
      <file action="read">org/tier3_junior/0.3.3_RD_DataRefresh/deliverables/page_inventory.xml</file>
      <!-- Portal API endpoint files for this pod -->
      <file action="read">portal/src/api/endpoints/portfolio-optimization.ts</file>
      <file action="read">portal/src/api/endpoints/trade-submission.ts</file>
      <file action="read">portal/src/api/endpoints/portfolio.ts</file>
      <!-- Shared hooks -->
      <file action="read">portal/src/hooks/useYangData.ts</file>
      <!-- Shared component layer -->
      <file action="read">portal/src/api/portal-proxy.ts</file>
      <!-- Output -->
      <file action="create">org/tier2_senior/0.3.0_DE_TradingOperations/deliverables/pod_inventory.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read all three RD page_inventory.xml files in full before writing anything.
      PortfolioManagement in particular has a large file tree (AG Grid, optimization
      report, trade grid, snapshot management). Document its full tab/section structure.
    </requirement>
    <requirement id="2">
      Read each portal API endpoint file. PortfolioManagement connects to the most
      Lambda functions of any page (opal-pm-*, opal-portfolio-*, yang-*). Document
      what each endpoint function does and which PM tab/action calls it.
    </requirement>
    <requirement id="3">
      DataRefresh is an admin/ops page. Document what it triggers and what Lambda
      or EC2 services it calls. Understand its role in the operational workflow.
    </requirement>
    <requirement id="4">
      TradeSubmission is the downstream of PM's Export flow. Document the handoff
      point between PortfolioManagement (export) and TradeSubmission (approval queue).
    </requirement>
    <requirement id="5">
      Produce pod_inventory.xml following the schema. Every section populated from
      actual file reads — no inference.
    </requirement>
    <requirement id="6">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      pod_inventory.xml exists at org/tier2_senior/0.3.0_DE_TradingOperations/deliverables/pod_inventory.xml
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
          Include PM-to-TradeSubmission export handoff as an intra-pod workflow dependency.
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
      PortfolioManagement is the most complex page in the portal. Do not skip
      sections — incomplete documentation here creates the most operational risk.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.3.1_RD_PortfolioManagement" task="page_inventory" status="complete"/>
    <dependency agent="0.3.2_RD_TradeSubmission" task="page_inventory" status="complete"/>
    <dependency agent="0.3.3_RD_DataRefresh" task="page_inventory" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.3.0_DE_TradingOperations/deliverables/pod_inventory.xml
    </deliverable>
  </deliverables>
</task_order>
```
