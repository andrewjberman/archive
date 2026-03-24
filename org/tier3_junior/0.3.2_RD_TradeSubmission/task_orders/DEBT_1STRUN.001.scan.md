<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-23-debt-1strun-001-0.3.2_rd_tradesubmission</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.3.2_RD_TradeSubmission</issued_to>
    <date>2026-03-23</date>
    <status>pending</status>
    <project_code>DEBT_1STRUN</project_code>
  </metadata>

  <objective>
    Scan your page directory for technical debt across 6 categories.
    Produce a structured findings log. Report to your pod DE (0.3.0_DE_TradingOperations).
  </objective>

  <scope>
    <files>
      <file action="scan">portal/src/pages/TradeSubmission/</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Scan your page directory (portal/src/pages/TradeSubmission/) and all files within it
      for the following 6 categories of technical debt. For each finding,
      record: file path, line number(s), category, severity (high/medium/low),
      and a 1-2 sentence description of what is wrong and why it matters.

      CATEGORIES:

      C1 - DEAD CODE
      Unreachable functions, unused imports, commented-out blocks, components
      that are defined but never rendered, props that are declared but never
      passed, event handlers wired to nothing. If removing it would change
      zero behavior, it is dead code.

      C2 - DEPRECATED / SUPERSEDED
      Code that still runs but has been replaced by a newer pattern elsewhere.
      Old API endpoint references that point to routes no longer in use.
      Legacy type definitions kept for backwards compatibility but no longer
      matching the actual data shape. Stale TODO/FIXME/HACK comments.

      C3 - DUPLICATION / DRIFT RISK
      Copy-pasted components or utility functions that exist in both your page
      and another page (or shared components). Inline logic that duplicates
      what a shared hook or utility already does. Two components that do the
      same thing with slightly different implementations.

      C4 - HARDCODED CONFIGURATION
      Magic numbers (timeouts, retry counts, page sizes). Hardcoded API paths
      that should come from a route config. Inline color values that should
      reference the theme. Hardcoded feature flags or environment checks.

      C5 - ORPHANED INFRASTRUCTURE
      Routes defined in the page's routing config that lead to removed or
      empty components. Lazy-loaded chunks that are never navigated to.
      API hooks or fetch functions defined but never called.

      C6 - STALE ERROR HANDLING
      try/catch blocks that swallow errors silently. Error boundaries that
      show generic messages instead of actionable feedback. Loading/error
      states that reference old data shapes. Retry logic with no backoff
      or wrong retry conditions.
    </requirement>

    <requirement id="2">
      OUTPUT FORMAT: Write your findings as a session log at:
        0.3.2_RD_TradeSubmission/logs/2026-03-23/debt_1strun_scan.md

      Use this structure:
        # DEBT_1STRUN Scan — 0.3.2_RD_TradeSubmission
        **Date:** 2026-03-23
        **Scope:** portal/src/pages/TradeSubmission/

        ## Findings

        | # | File | Lines | Category | Severity | Description |
        |---|------|-------|----------|----------|-------------|
        | 1 | path/to/file.tsx | 45-67 | C1 Dead | High | ... |
        | 2 | ... | ... | ... | ... | ... |

        ## Summary
        - Total findings: N
        - By category: C1: N, C2: N, C3: N, C4: N, C5: N, C6: N
        - High severity: N
        - Recommended priority fixes: [top 3 items by impact]

      If you find ZERO debt in a category, state "None found" — do not skip it.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All 6 categories scanned — none skipped</criterion>
    <criterion id="2">Every finding has file path, line numbers, category, severity, and description</criterion>
    <criterion id="3">Findings log written to logs/2026-03-23/debt_1strun_scan.md</criterion>
    <criterion id="4">Summary section with counts and top 3 priority recommendations</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Scan only YOUR page directory — do not scan other pages or shared components (DE handles those)</constraint>
    <constraint>Do not fix anything — this is a scan-only task. Fixes come in .002+ task orders.</constraint>
    <constraint>Report to 0.3.0_DE_TradingOperations — your DE will aggregate your findings into the pod report.</constraint>
    <constraint>Be concrete: name files, line numbers, function names. No vague "could be improved" findings.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">logs/2026-03-23/debt_1strun_scan.md with structured findings table</deliverable>
  </deliverables>
</task_order>
