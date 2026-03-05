# Task Order: Macro/Project Code Retroactive Cleanup — Pod 4 Scope

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-05-macro-project-code-de-cleanup</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-05</date>
    <status>pending</status>
  </metadata>

  <objective>
    The org system was upgraded on 2026-03-05 (commit 3d5fc658) to a two-level code
    system: macro codes (4 chars) and project codes (MACRO_6CHAR). This task order
    covers all pod 4 retroactive cleanup: rename task order files and thread receipt
    files for DE, DS, and RD agents, and update XML metadata content inside those files.
    DE has commit authority across all pod 4 paths and handles this in one pass.
    Session logs and thread folder internals are NOT touched.
  </objective>

  <scope>
    <files>
      <!-- === DE OWN TASK ORDERS (git mv + content update) === -->
      <!-- V1VERS scope -->
      <file action="rename+modify">org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI-004-portal_types_wiring.md
          -> ADVI_V1VERS-004-portal_types_wiring.md</file>
      <file action="rename+modify">org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI-006-books_design_brief.md
          -> ADVI_V1VERS-006-books_design_brief.md</file>
      <!-- YANGV2 scope -->
      <file action="rename+modify">org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI-Y-phase3-de-type-wiring.md
          -> ADVI_YANGV2-Y-phase3-de-type-wiring.md</file>

      <!-- === DE OWN THREAD RECEIPTS (git mv) === -->
      <file action="rename">org/tier2_senior/0.4.0_DE_ClientPlatform/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DS_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md
          -> ADVI_V1VERS-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DS_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md</file>
      <file action="rename">org/tier2_senior/0.4.0_DE_ClientPlatform/threads/ADVI-005-pattern-0-stacked-bar--rolling-flows-dat_0.4.0_DS_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md
          -> ADVI_V1VERS-005-pattern-0-stacked-bar--rolling-flows-dat_0.4.0_DS_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md</file>
      <file action="rename">org/tier2_senior/0.4.0_DE_ClientPlatform/threads/ADVI-006-pattern-0-books-tab-design-brief-l2-l3-l_0.4.0_DS_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md
          -> ADVI_V1VERS-006-pattern-0-books-tab-design-brief-l2-l3-l_0.4.0_DS_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md</file>

      <!-- === DS TASK ORDERS (git mv + content update) === -->
      <!-- V1VERS scope -->
      <file action="rename+modify">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI-004-adv_drill_cla.md
          -> ADVI_V1VERS-004-adv_drill_cla.md</file>
      <file action="rename+modify">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI-005-rolling_flows_data.md
          -> ADVI_V1VERS-005-rolling_flows_data.md</file>
      <!-- YANGV2 scope -->
      <file action="rename+modify">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI-Y-phase2-ds-data-batch.md
          -> ADVI_YANGV2-Y-phase2-ds-data-batch.md</file>

      <!-- === DS THREAD RECEIPTS (git mv) === -->
      <file action="rename">org/tier2_senior/0.4.0_DS_ClientPlatform/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DE_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md
          -> ADVI_V1VERS-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DE_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md</file>
      <file action="rename">org/tier2_senior/0.4.0_DS_ClientPlatform/threads/ADVI-005-pattern-0-stacked-bar--rolling-flows-dat_0.4.0_DE_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md
          -> ADVI_V1VERS-005-pattern-0-stacked-bar--rolling-flows-dat_0.4.0_DE_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md</file>
      <file action="rename">org/tier2_senior/0.4.0_DS_ClientPlatform/threads/ADVI-006-pattern-0-books-tab-design-brief-l2-l3-l_0.4.2_RD_AdvisorIntelligence+0.4.0_DE_ClientPlatform.md
          -> ADVI_V1VERS-006-pattern-0-books-tab-design-brief-l2-l3-l_0.4.2_RD_AdvisorIntelligence+0.4.0_DE_ClientPlatform.md</file>

      <!-- === RD TASK ORDERS (git mv + content update) === -->
      <!-- V1VERS scope -->
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-004-distribution_continuous.md
          -> ADVI_V1VERS-004-distribution_continuous.md</file>
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-005-advisors_tab.md
          -> ADVI_V1VERS-005-advisors_tab.md</file>
      <!-- YANGV2 scope -->
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y1-Y4-Y6-Y12-phase1-visual.md
          -> ADVI_YANGV2-Y1-Y4-Y6-Y12-phase1-visual.md</file>
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y8-continuous-aua-stacked-bar.md
          -> ADVI_YANGV2-Y8-continuous-aua-stacked-bar.md</file>
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y3-Y5-FE-header-panel.md
          -> ADVI_YANGV2-Y3-Y5-FE-header-panel.md</file>
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y6b-Y6d-Y9-FE-drill-and-continuous-nna.md
          -> ADVI_YANGV2-Y6b-Y6d-Y9-FE-drill-and-continuous-nna.md</file>
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y13-FE-rolling-flows-nna-bar.md
          -> ADVI_YANGV2-Y13-FE-rolling-flows-nna-bar.md</file>
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y15-books-tab-l2-l3-l4.md
          -> ADVI_YANGV2-Y15-books-tab-l2-l3-l4.md</file>

      <!-- === RD THREAD RECEIPTS (git mv) === -->
      <file action="rename">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DS_ClientPlatform+0.4.0_DE_ClientPlatform.md
          -> ADVI_V1VERS-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DS_ClientPlatform+0.4.0_DE_ClientPlatform.md</file>
      <file action="rename">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/threads/ADVI-005-pattern-0-stacked-bar--rolling-flows-dat_0.4.0_DS_ClientPlatform+0.4.0_DE_ClientPlatform.md
          -> ADVI_V1VERS-005-pattern-0-stacked-bar--rolling-flows-dat_0.4.0_DS_ClientPlatform+0.4.0_DE_ClientPlatform.md</file>
      <file action="rename">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/threads/ADVI-006-pattern-0-books-tab-design-brief-l2-l3-l_0.4.0_DS_ClientPlatform+0.4.0_DE_ClientPlatform.md
          -> ADVI_V1VERS-006-pattern-0-books-tab-design-brief-l2-l3-l_0.4.0_DS_ClientPlatform+0.4.0_DE_ClientPlatform.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Use git mv for all renames so git history tracks the rename. Do not delete
      and recreate -- use git mv exclusively.
    </requirement>
    <requirement id="2">
      V1VERS assignment: task orders prefixed ADVI-004, ADVI-005, ADVI-006 (thread-sourced,
      V1 completion work) become ADVI_V1VERS-NNN. All thread receipts (ADVI-004/005/006)
      become ADVI_V1VERS-NNN.
    </requirement>
    <requirement id="3">
      YANGV2 assignment: task orders prefixed ADVI-Y* (Yang V2 feedback items) become
      ADVI_YANGV2-Y*. These include phase2 DS batch, phase3 DE type wiring, and all
      RD visual items (Y1, Y3, Y5, Y6b, Y6d, Y8, Y9, Y12, Y13, Y15).
    </requirement>
    <requirement id="4">
      After renaming, open each task order file and update the XML &lt;metadata&gt;&lt;id&gt;
      field to reflect the new project code prefix. Also update any &lt;thread_serial&gt;
      or &lt;thread_ref&gt; fields that reference the old ADVI-NNN format.
    </requirement>
    <requirement id="5">
      Do not rename or modify thread receipt file CONTENT -- only the filename changes.
      Receipts are historical records; their internal content stays as-is.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      No files remain under any pod 4 agent task_orders/ or threads/ folder with
      an ADVI-NNN or ADVI-Y prefix. All are ADVI_V1VERS-NNN or ADVI_YANGV2-Y.
      Verify: find org/tier2_senior/0.4.0_D* org/tier3_junior/0.4.2_RD* -name "ADVI-*.md"
    </criterion>
    <criterion id="2">
      XML &lt;metadata&gt;&lt;id&gt; fields in all modified task orders reflect the new project
      code format.
    </criterion>
    <criterion id="3">
      All changes committed as a single commit on CLOUD under DE authorship.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT rename thread folder directories under org/threads/. Only agent task_orders/ and threads/ receipt files change.</constraint>
    <constraint>Do NOT touch session logs, CONTEXT_COMPILED.md, messages/, or context/ subfolders inside thread folders.</constraint>
    <constraint>Do NOT modify the STATUS field of any task order -- only rename the file and update the id/serial fields in metadata.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;" -m "0.4.0_DE_ClientPlatform: retroactive macro/project code cleanup -- pod 4 scope"</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">All 27 file renames and content updates committed on CLOUD under DE authorship.</deliverable>
  </deliverables>
</task_order>
```
