# Task Order: Macro/Project Code Retroactive Cleanup — COO Scope

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-05-macro-project-code-coo-cleanup</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>2.0.0_SA_COO</issued_to>
    <date>2026-03-05</date>
    <status>pending</status>
  </metadata>

  <objective>
    The org system was upgraded on 2026-03-05 (commit 3d5fc658) to a two-level code
    system: macro codes (4 chars, surface area) and project codes (MACRO_6CHAR, specific
    initiative). This task order covers the COO-scope retroactive cleanup: updating
    THREAD.json project/serial fields and renaming task orders owned by AE and DT agents.
    Session logs and CONTEXT_COMPILED.md files are historical artifacts -- do NOT touch them.
  </objective>

  <scope>
    <files>
      <!-- THREAD.json updates: change project field from "ADVI" to "ADVI_V1VERS"
           and serial field from "ADVI-NNN" to "ADVI_V1VERS-NNN" -->
      <file action="modify">org/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c/THREAD.json</file>
      <file action="modify">org/threads/ADVI-005-pattern-0-stacked-bar--rolling-flows-dat/THREAD.json</file>
      <file action="modify">org/threads/ADVI-006-pattern-0-books-tab-design-brief-l2-l3-l/THREAD.json</file>

      <!-- AE task order rename + content update -->
      <file action="rename+modify">org/tier2_senior/0.7.0_AE_CloudOps/task_orders/ADVI-J1-partner-identity-dynamo.md
          -> ADVI_V1VERS-J1-partner-identity-dynamo.md</file>

      <!-- DT task order rename + content update -->
      <file action="rename+modify">org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/ADVI-J2-J3-auth-handler-authorizer.md
          -> ADVI_V1VERS-J2-J3-auth-handler-authorizer.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      In each of the 3 THREAD.json files: update "project" field value from "ADVI"
      to "ADVI_V1VERS". Update "serial" field: "ADVI-004" -> "ADVI_V1VERS-004",
      "ADVI-005" -> "ADVI_V1VERS-005", "ADVI-006" -> "ADVI_V1VERS-006". The thread
      folder directory names are NOT renamed -- only the JSON field values change.
    </requirement>
    <requirement id="2">
      Use git mv to rename the AE task order file. J1 is V1VERS scope (partner
      identity DynamoDB was a scoped auth requirement from V1 completion PRD).
    </requirement>
    <requirement id="3">
      Use git mv to rename the DT task order file. J2/J3 are V1VERS scope (portal
      auth handler and authorizer were V1 completion requirements).
    </requirement>
    <requirement id="4">
      Inside the renamed AE and DT task order files, update any &lt;id&gt; field in
      &lt;metadata&gt; that contains "ADVI-J" to use "ADVI_V1VERS-J". Update any
      &lt;thread_serial&gt; or &lt;thread_ref&gt; fields that reference the old format.
    </requirement>
    <requirement id="5">
      The ADVI-Y* task orders (Yang V2 work) were issued by COO to DS, DE, and RD.
      COO must review the &lt;metadata&gt;&lt;id&gt; fields in each of those task orders and
      update any that use the old "ADVI-Y" prefix to "ADVI_YANGV2-Y". Those files
      are owned by pod 4 agents -- coordinate with DE who is handling the pod 4
      file renames (see DE's companion task order).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      All 3 THREAD.json files have project="ADVI_V1VERS" and the correct
      ADVI_V1VERS-NNN serial. Verify with: grep -r '"project"' org/threads/ADVI-*/THREAD.json
    </criterion>
    <criterion id="2">
      AE and DT task order files exist at new ADVI_V1VERS-prefixed paths.
      Old paths no longer exist.
    </criterion>
    <criterion id="3">
      No remaining files under COO ownership reference "project": "ADVI" without the
      _V1VERS or _YANGV2 suffix.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT rename thread folder directories (e.g., org/threads/ADVI-004-.../). Only update field values inside THREAD.json.</constraint>
    <constraint>Do NOT touch CONTEXT_COMPILED.md, messages/, or context/ subfolders inside thread folders. These are compiled historical snapshots.</constraint>
    <constraint>Do NOT touch any session logs -- they are historical records and renaming them would destroy context traceability.</constraint>
    <constraint>Commit with: git commit --author="2.0.0_SA_COO &lt;2.0.0_SA_COO@opal.agent&gt;" -m "org(2.0.0_SA_COO): retroactive macro/project code cleanup -- COO scope"</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">All 5 file changes committed on CLOUD branch under 2.0.0_SA_COO authorship.</deliverable>
  </deliverables>
</task_order>
```
