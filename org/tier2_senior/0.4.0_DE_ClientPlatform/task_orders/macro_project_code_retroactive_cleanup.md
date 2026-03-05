# Task Order: Macro/Project Code Retroactive Cleanup — Pod 4 Scope

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-05-macro-project-code-de-cleanup</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-05</date>
    <status>complete</status>
  </metadata>

  <objective>
    The org system was upgraded on 2026-03-05 (commit 3d5fc658) to a two-level code
    system: macro codes (4 chars) and project codes (MACRO_6CHAR). Task order filenames
    now follow the rigid format: MACRO_6CHAR.task-code-and-description.md
    (dot separator between project code and task, dashes throughout, no underscores after the dot).
    This task order covers all pod 4 retroactive cleanup: rename task order files and thread
    receipt files for DE, DS, and RD agents, and update XML metadata content inside those files.
    DE has commit authority across all pod 4 paths and handles this in one pass.
    Session logs and thread folder internals are NOT touched.
  </objective>

  <scope>
    <files>
      <!-- FILENAME FORMAT REFERENCE:
           Old: ADVI-NNN-slug_with_underscores.md
           New: ADVI_V1VERS.NNN.description-words.md   (V1 completion work)
                ADVI_YANGV2.Y-task-code.description.md  (Yang V2 work)
           Dots between segments. Dashes between words within a segment. No underscores after project code.
           Segments: {PROJECT_CODE} . {task-code} . {description} -->

      <!-- === DE OWN TASK ORDERS (git mv + content update) === -->
      <file action="rename+modify">org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI-004-portal_types_wiring.md
          -> ADVI_V1VERS.004.portal-types-wiring.md</file>
      <file action="rename+modify">org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI-006-books_design_brief.md
          -> ADVI_V1VERS.006.books-design-brief.md</file>
      <file action="rename+modify">org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI-Y-phase3-de-type-wiring.md
          -> ADVI_YANGV2.Y-phase3.de-type-wiring.md</file>

      <!-- === DE OWN THREAD RECEIPTS (git mv only -- do not modify content) === -->
      <file action="rename">org/tier2_senior/0.4.0_DE_ClientPlatform/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DS_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md
          -> ADVI_V1VERS-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DS_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md</file>
      <file action="rename">org/tier2_senior/0.4.0_DE_ClientPlatform/threads/ADVI-005-pattern-0-stacked-bar--rolling-flows-dat_0.4.0_DS_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md
          -> ADVI_V1VERS-005-pattern-0-stacked-bar--rolling-flows-dat_0.4.0_DS_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md</file>
      <file action="rename">org/tier2_senior/0.4.0_DE_ClientPlatform/threads/ADVI-006-pattern-0-books-tab-design-brief-l2-l3-l_0.4.0_DS_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md
          -> ADVI_V1VERS-006-pattern-0-books-tab-design-brief-l2-l3-l_0.4.0_DS_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md</file>

      <!-- === DS TASK ORDERS (git mv + content update) === -->
      <file action="rename+modify">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI-004-adv_drill_cla.md
          -> ADVI_V1VERS.004.adv-drill-cla.md</file>
      <file action="rename+modify">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI-005-rolling_flows_data.md
          -> ADVI_V1VERS.005.rolling-flows-data.md</file>
      <file action="rename+modify">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI-Y-phase2-ds-data-batch.md
          -> ADVI_YANGV2.Y-phase2.ds-data-batch.md</file>

      <!-- === DS THREAD RECEIPTS (git mv only -- do not modify content) === -->
      <file action="rename">org/tier2_senior/0.4.0_DS_ClientPlatform/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DE_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md
          -> ADVI_V1VERS-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DE_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md</file>
      <file action="rename">org/tier2_senior/0.4.0_DS_ClientPlatform/threads/ADVI-005-pattern-0-stacked-bar--rolling-flows-dat_0.4.0_DE_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md
          -> ADVI_V1VERS-005-pattern-0-stacked-bar--rolling-flows-dat_0.4.0_DE_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md</file>
      <file action="rename">org/tier2_senior/0.4.0_DS_ClientPlatform/threads/ADVI-006-pattern-0-books-tab-design-brief-l2-l3-l_0.4.2_RD_AdvisorIntelligence+0.4.0_DE_ClientPlatform.md
          -> ADVI_V1VERS-006-pattern-0-books-tab-design-brief-l2-l3-l_0.4.2_RD_AdvisorIntelligence+0.4.0_DE_ClientPlatform.md</file>

      <!-- === RD TASK ORDERS (git mv + content update) === -->
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-004-distribution_continuous.md
          -> ADVI_V1VERS.004.distribution-continuous.md</file>
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-005-advisors_tab.md
          -> ADVI_V1VERS.005.advisors-tab.md</file>
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y1-Y4-Y6-Y12-phase1-visual.md
          -> ADVI_YANGV2.Y1-Y4-Y6-Y12.phase1-visual.md</file>
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y8-continuous-aua-stacked-bar.md
          -> ADVI_YANGV2.Y8.continuous-aua-stacked-bar.md</file>
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y3-Y5-FE-header-panel.md
          -> ADVI_YANGV2.Y3-Y5.fe-header-panel.md</file>
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y6b-Y6d-Y9-FE-drill-and-continuous-nna.md
          -> ADVI_YANGV2.Y6b-Y6d-Y9.fe-drill-and-continuous-nna.md</file>
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y13-FE-rolling-flows-nna-bar.md
          -> ADVI_YANGV2.Y13.fe-rolling-flows-nna-bar.md</file>
      <file action="rename+modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y15-books-tab-l2-l3-l4.md
          -> ADVI_YANGV2.Y15.books-tab-l2-l3-l4.md</file>

      <!-- === RD THREAD RECEIPTS (git mv only -- do not modify content) === -->
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
      Use git mv for all renames. Do not delete and recreate.
    </requirement>
    <requirement id="2">
      Task order filename format (rigid): MACRO_6CHAR.task-code.description.md
      Dots separate segments. Dashes separate words within a segment. No underscores after the project code.
      Segments: project code -> task code -> description. V1VERS for threads 004/005/006. YANGV2 for Y-series.
    </requirement>
    <requirement id="3">
      Thread receipt filenames use hyphen format (ADVI_V1VERS-NNN-...), NOT dot format.
      Receipts are auto-generated by the orchestrator and follow thread ID naming.
      Only update the project code prefix (ADVI- -> ADVI_V1VERS-), not the separator.
    </requirement>
    <requirement id="4">
      After renaming each task order, open the file and update the XML &lt;metadata&gt;&lt;id&gt;
      to reflect the new project code and dot-format filename. Update any &lt;thread_serial&gt;
      references from ADVI-NNN to ADVI_V1VERS-NNN. Do NOT change &lt;status&gt; fields.
    </requirement>
    <requirement id="5">
      Thread receipt file CONTENT is not modified -- only the filename changes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      No task order files remain under pod 4 with the old ADVI-* prefix.
      Verify: find org/tier2_senior/0.4.0_D* org/tier3_junior/0.4.2_RD* -name "ADVI-*.md"
      Expected result: zero matches.
    </criterion>
    <criterion id="2">
      All renamed task order files follow the dot format: ADVI_V1VERS.NNN-description.md
      or ADVI_YANGV2.Y-description.md. No underscores appear after the dot.
    </criterion>
    <criterion id="3">
      All thread receipt files (threads/ folder) follow ADVI_V1VERS-NNN-* format.
    </criterion>
    <criterion id="4">
      XML &lt;metadata&gt;&lt;id&gt; in all modified task orders uses new project code.
    </criterion>
    <criterion id="5">
      All changes in a single commit on CLOUD under DE authorship.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT rename thread folder directories under org/threads/. Only agent task_orders/ and threads/ receipt files change.</constraint>
    <constraint>Do NOT touch session logs, CONTEXT_COMPILED.md, messages/, or context/ subfolders inside thread folders.</constraint>
    <constraint>Do NOT modify the &lt;status&gt; field of any task order during this cleanup.</constraint>
    <constraint>Thread receipt filenames use hyphen (ADVI_V1VERS-NNN-...) not dot. Only task order filenames use the dot format.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;" -m "0.4.0_DE_ClientPlatform: retroactive macro/project code cleanup -- pod 4 scope"</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">All 27 file renames and content updates committed on CLOUD under DE authorship.</deliverable>
  </deliverables>
</task_order>
```
