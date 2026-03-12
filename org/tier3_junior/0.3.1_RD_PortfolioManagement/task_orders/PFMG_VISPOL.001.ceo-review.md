# Task Order: PFMG_VISPOL CEO Review — Visual Polish Sign-Off

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-06-PFMG_VISPOL-001-ceo-review</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.1_RD_PortfolioManagement</issued_to>
    <date>2026-03-06</date>
    <status>complete</status>
    <thread_serial>PFMG_VISPOL-001</thread_serial>
  </metadata>

  <objective>
    A forensic audit confirmed that all 13 Yang visual polish items (PFMG_VISPOL) were
    implemented prior to the agent system being established — attributed to an outside
    consultant. Andrew (CEO) wants to personally review every item before closing the
    project. Your job is to walk him through each item 1-13 in sequence, presenting
    exactly what Yang asked for and exactly how it was executed. Andrew may request
    ad hoc revisions at any point. This task order is complete only when Andrew
    explicitly approves all 13 items.
  </objective>

  <references>
    <ref type="prd">docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md</ref>
    <ref type="audit">org/tier1_exec/2.0.0_SA_COO/logs/2026-03-06/pfmg_vispol_forensic_audit.md</ref>
  </references>

  <review_protocol>

    For each item 1 through 13, you present two things in order:

    1. YANG'S REQUEST (verbatim):
       Copy the relevant requirement text exactly as written in the PRD at
       docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md. Include the item title,
       scope, and the specific "Change:" block. Do not paraphrase.

    2. EXECUTION SUMMARY (concise):
       In 2-4 sentences: which file(s) were changed, what function or constant was
       added or modified, and the exact threshold values, color tokens, or logic used.
       Name specific line numbers or function names where it aids clarity.
       If a partial gap exists (only Item 6 By Group view), call it out explicitly.

    Then STOP and wait for Andrew's response before proceeding to the next item.

    Andrew will respond with one of:
      - "Approved" or equivalent — proceed to next item
      - A revision request — implement the change, confirm what you did, then wait
        for re-approval before proceeding
      - "Skip" — mark item as acknowledged and proceed

    Do NOT batch-present multiple items. One item at a time. Wait for response.

  </review_protocol>

  <requirements>

    <requirement id="1">
      Present Item 1 first. Quote the full "Change:" block from the PRD for
      Item 1 (Capitalize Group Columns). Then state which files received the
      `capitalize` CSS class and on which elements.
    </requirement>

    <requirement id="2">
      Present Item 2 (Risk Decomposition — Exposure Highlighting). Quote the
      PRD table showing column thresholds. State which function implements the
      logic and the exact threshold values used.
    </requirement>

    <requirement id="3">
      Present Item 3 (Risk Decomposition — Contribution Highlighting). Quote
      the PRD table and the directionality note. State the function names and
      threshold values.
    </requirement>

    <requirement id="4">
      Present Item 4 (Alpha Tab Conditional Highlighting). Quote the PRD table
      including the note that Trade threshold changed from +-0.01 to +-0.1.
      Confirm the current threshold in code and that it was updated.
    </requirement>

    <requirement id="5">
      Present Item 5 (Sector Tab Conditional Highlighting). Quote the PRD table.
      State the function names and the exact thresholds in code.
    </requirement>

    <requirement id="6">
      Present Item 6 (Model Tab Gradient Color Scale). Quote the PRD change
      description. State which view(s) are implemented and call out explicitly
      that the By Group view is MISSING the gradient (known gap). Present
      Andrew with the choice: approve as-is (By Factor only) or request the
      By Group view be fixed before approval.
    </requirement>

    <requirement id="7">
      Present Item 7 (Trade Tab Zero Weights to Blank). Quote the PRD change
      description and the list of columns affected. Confirm which columns
      received the en-dash formatter and what value triggers the blank.
    </requirement>

    <requirement id="8">
      Present Item 8 (Trade Tab Risk Color Scale). Quote the PRD change
      description. State the function call used and confirm the `inverted`
      parameter is set to produce the green-low / red-high direction.
    </requirement>

    <requirement id="9">
      Present Item 9 (initialBet Coloring + finalBet Column). Quote the full
      PRD change block including both sub-items. State the valueGetter formula
      for finalBet and confirm gradient is applied to both columns.
    </requirement>

    <requirement id="10">
      Present Item 10 (Size Column Highlighting). Quote the PRD table of values
      and colors. State the exact rgba values used in the cellStyle and confirm
      the background vs text color distinction.
    </requirement>

    <requirement id="11">
      Present Item 11 (Security Detail Modal Factor Order + Capitalization).
      Quote both sub-items from the PRD. State the sort function used and which
      element receives the capitalize class.
    </requirement>

    <requirement id="12">
      Present Item 12 (Reset Zero Button). Quote the full PRD change block
      including the behavior description. State which files were touched and
      confirm the callback chain (TradeTab prop -> PortfolioManagement handler
      -> useOptimizationState function).
    </requirement>

    <requirement id="13">
      Present Item 13 (Alpha + Model Tab Canonical Group Ordering). Quote the
      PRD including the CANONICAL_GROUP_ORDER constant. State which files use
      it, confirm it is now in portal/src/utils/factorOrder.ts (shared), and
      name the helper function called at each sort site.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      Andrew has explicitly approved (or approved with revisions applied) each
      of the 13 items in sequence. No item is skipped without Andrew's
      acknowledgment.
    </criterion>
    <criterion id="2">
      Any revision Andrew requests during the review is implemented, confirmed
      in your response, and re-approved before the review advances.
    </criterion>
    <criterion id="3">
      Item 6 By Group gap is resolved — either Andrew approves the current
      partial state or you implement the gradient fix before advancing.
    </criterion>
    <criterion id="4">
      After all 13 items are approved: mark this task order status as
      "complete" and write a one-paragraph session log at
      org/tier3_junior/0.3.1_RD_PortfolioManagement/logs/YYYY-MM-DD/
      pfmg_vispol_ceo_review.md summarizing what was approved and any
      revisions made.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      Present items strictly 1 through 13 in order. Do not skip ahead or
      present multiple items in one response.
    </constraint>
    <constraint>
      The PRD quote must be verbatim — copy the text directly from
      docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md. Do not paraphrase
      Yang's request.
    </constraint>
    <constraint>
      If Andrew requests a code change: use the Edit tool, confirm the change
      in your next message with the exact lines modified, then ask for
      re-approval. Do not mark the item approved yourself.
    </constraint>
    <constraint>
      Do not mark this task order complete until Andrew has reviewed all 13
      items. "All 13 approved" is the only completion condition.
    </constraint>
    <constraint>
      Commit author for any revisions:
      git commit --author="0.3.1_RD_PortfolioManagement &lt;0.3.1_RD_PortfolioManagement@opal.agent&gt;" -m "..."
    </constraint>
    <constraint>
      After any portal code change: run bunx tsc -b in the portal directory
      and confirm it passes before presenting the change to Andrew.
    </constraint>
    <constraint>No emojis in code, logs, or commit messages.</constraint>
  </constraints>

  <dependencies>
    <!-- No blocking dependencies — all 13 items are already implemented.
         This is a review-and-revise task, not a build task. -->
  </dependencies>

  <deliverables>
    <deliverable type="review">CEO approval of all 13 PFMG_VISPOL items</deliverable>
    <deliverable type="commit">Any ad hoc revisions requested during review</deliverable>
    <deliverable type="document">Session log at org/tier3_junior/0.3.1_RD_PortfolioManagement/logs/YYYY-MM-DD/pfmg_vispol_ceo_review.md</deliverable>
    <deliverable type="status">This task order marked complete</deliverable>
  </deliverables>

</task_order>
```
