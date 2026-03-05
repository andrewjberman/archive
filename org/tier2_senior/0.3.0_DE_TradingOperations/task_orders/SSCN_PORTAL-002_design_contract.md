# Task Order: Security Scanner Design Contract — SSCN_PORTAL-002

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-05-sscn-design-contract</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-05</date>
    <project>SSCN_PORTAL</project>
    <thread>SSCN_PORTAL-002</thread>
    <status>pending</status>
  </metadata>

  <references>
    <ref type="thread">org/threads/SSCN_PORTAL-002-pattern-0-design-securityscanner-ui----p/</ref>
    <ref type="thread-receipt">org/tier2_senior/0.3.0_DE_TradingOperations/threads/SSCN_PORTAL-002-pattern-0-design-securityscanner-ui----p_0.3.1_RD_PortfolioManagement+0.3.4_RD_SecurityScanner.md</ref>
    <ref type="data-contract">docs/architecture/SSCN_DATA_CONTRACT.md</ref>
    <ref type="prd">docs/architecture/SECURITY_SCANNER_PRD.md</ref>
  </references>

  <objective>
    Produce a standalone SSCN design contract document that 0.3.4_RD_SecurityScanner
    builds against. The SSCN_PORTAL-002 thread agreed all design decisions (component
    reuse, table primitive, gradient semantics, column layout, shared util extraction)
    but DE's component reuse plan exists only inline in thread turn 3. This task order
    extracts that plan into a durable deliverable, equivalent to SSCN_DATA_CONTRACT.md
    for the architecture side.

    0.3.4_RD_SecurityScanner must not begin portal implementation until this document
    exists and is committed. It is the authoritative design brief they build against.
  </objective>

  <scope>
    <files>
      <file action="create">docs/architecture/SSCN_DESIGN_CONTRACT.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read your thread receipt:
        org/tier2_senior/0.3.0_DE_TradingOperations/threads/SSCN_PORTAL-002-pattern-0-design-securityscanner-ui----p_0.3.1_RD_PortfolioManagement+0.3.4_RD_SecurityScanner.md

      The key turns are:
        - Turn 3 (DE): initial component reuse plan + AG Grid ruling
        - Turn 5 (0.3.4): confirmed build plan against DE decisions
        - Turn 6 (DE): category order + gradient semantics approvals
        - Turn 7 (0.3.1): Tab 4 raw value column strategy (converge)
        - Turn 8 (0.3.4): final finalized reuse plan (converge)
    </requirement>

    <requirement id="2">
      Create docs/architecture/SSCN_DESIGN_CONTRACT.md with the following sections.
      Every decision must cite the turn that agreed it.

      Section 1: Header
        - Project: SSCN_PORTAL
        - Thread: SSCN_PORTAL-002
        - Participants: 0.3.1_RD_PortfolioManagement, 0.3.4_RD_SecurityScanner, 0.3.0_DE_TradingOperations
        - Date: 2026-03-05
        - Status: Contracted

      Section 2: Design Principle
        One paragraph. SSCN mirrors PortfolioManagement's visual language (panels, tab nav,
        header density, table styling) as closely as possible. No reinvention where PM
        already has a working pattern.

      Section 3: Component Reuse Plan (the core deliverable)
        Format exactly as the SSCN COMPONENT REUSE PLAN block from DE turn 3, expanded
        with any confirmations or modifications from turns 5-8. Four categories:

        A) IMPORT DIRECTLY (no changes needed):
           List every shared component/hook SSCN imports as-is.
           Include exact import paths and the specific exports used.
           Source: DE turn 3 + 0.3.4 turn 5.

        B) EXTRACT TO SHARED BEFORE USE (DE executes as portal refactor):
           List each PM utility being extracted, with source path, target path,
           and which function/export is being moved.
           Note: DE owns this extraction and must complete it before 0.3.4 begins
           wiring SSCN tables, so SSCN can import stable paths from day 1.
           Source: DE turn 3 (approved), 0.3.1 turn 4 (confirmed), DE turn 6 (confirmed).

        C) SSCN-LOCAL COPY (approved, no abstraction):
           List any patterns SSCN re-implements locally without extracting.
           Each must explain why it was not extracted.
           Source: DE turn 3.

        D) NEW (no PM equivalent):
           List each new component 0.3.4 must author from scratch.
           Include proposed file path and brief justification.
           Source: DE turn 3, 0.3.4 turn 2, 0.3.4 turn 5.

      Section 4: Table Primitive Ruling
        State the mandated table library for each tab.
        Include the reasoning (row/column scale, existing portal precedent).
        Source: DE turn 3 + 0.3.1 turn 1.

      Section 5: Gradient Semantics (percentile coloring)
        Document the exact formula SSCN uses for percentile gradient backgrounds,
        including the shared util function, the value transformation, and null handling.
        Source: DE turn 6, 0.3.4 turn 5, 0.3.4 turn 8.

      Section 6: Tab 4 Column Layout (Universe Scanner)
        Document the default column visibility decision and the raw-value toggle behavior.
        Include which columns are pinned, which are visible by default, where raw columns
        appear when revealed.
        Source: DE turn 6, 0.3.1 turn 7 (converge), 0.3.4 turn 8 (converge).

      Section 7: SSCN-Local Utilities
        Document the two SSCN-local utilities that are not shared:
          - categoryOrder.ts: path, exports, distinction from shared factorOrder.ts
        Source: DE turn 6, 0.3.4 turn 8.

      Section 8: Page Shell Composition
        Document the component composition order for SecurityScanner.tsx,
        mirroring PortfolioManagement.tsx's pattern.
        Include the exact shared component names and the new SSCN-local components
        in the order they appear in the render tree.
        Source: DE turn 3, 0.3.4 turn 5, 0.3.4 turn 8.

      Section 9: ScannerHeaderPanel Design
        Document the structure of the always-visible sticky header panel:
          - Closest PM analog
          - Component file path
          - Panel primitive usage (Panel / PanelHeader / PanelContent)
          - Left/right header actions
          - PanelContent sub-layout (factor chips, weight editor, validation strip)
        Source: 0.3.4 turn 2.

      Section 10: DESIGN_SPEC.md Assignment
        State that 0.3.4_RD_SecurityScanner is responsible for authoring
        portal/src/pages/SecurityScanner/DESIGN_SPEC.md using the ASCII skeleton
        from 0.3.4 turn 2 as the base, updated with:
          - AG Grid mandate for Tabs 2 and 4
          - Raw-value default-hide + toggle in Tab 4 actions
          - Shared util import paths (portal/src/utils/*)
          - SSCN-local category order path
        This DESIGN_SPEC.md is 0.3.4's first deliverable.
    </requirement>

    <requirement id="3">
      The document must be self-contained. 0.3.4_RD_SecurityScanner must be able
      to read this document alone and know exactly:
        - Which files to import from shared
        - Which files to write from scratch and where
        - What table library to use for each tab
        - How to apply gradient coloring to percentiles
        - What Tab 4 looks like by default vs with toggle enabled
      Do not use "as discussed" without stating the actual value.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">docs/architecture/SSCN_DESIGN_CONTRACT.md exists with all 10 sections.</criterion>
    <criterion id="2">Section 3 lists every item from DE turn 3's reuse plan, expanded with turn 5-8 confirmations.</criterion>
    <criterion id="3">Section 3B names exact source and target paths for both shared extractions.</criterion>
    <criterion id="4">Section 5 includes the exact value transformation formula (pctl - 50, min=-50, max=50) and null rendering rule.</criterion>
    <criterion id="5">Section 6 explicitly names the default-visible columns and where raw columns appear when revealed.</criterion>
    <criterion id="6">Section 8 lists components in render-tree order with exact import paths.</criterion>
    <criterion id="7">Section 10 clearly assigns DESIGN_SPEC.md authorship to 0.3.4_RD_SecurityScanner.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not write any portal code. This task order produces documentation only.</constraint>
    <constraint>Do not invent design decisions not agreed in the thread. If something is ambiguous, note it.</constraint>
    <constraint>Every section must name the thread turn(s) that established the decision.</constraint>
    <constraint>The design contract does not supersede SSCN_DATA_CONTRACT.md; it is the UI-side companion to it.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">docs/architecture/SSCN_DESIGN_CONTRACT.md -- standalone design contract</deliverable>
    <deliverable type="log">Session log at org/tier2_senior/0.3.0_DE_TradingOperations/logs/2026-03-05/ (optional)</deliverable>
  </deliverables>
</task_order>
```
