# Task Order: Stream I2 — Leaderboard Sort Stability

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-advi-i2-leaderboard-sort</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Investigate and fix leaderboard sort instability in the Advisors tab. Determine
    whether the root cause is frontend sort instability on NNA ties or a data issue
    in the publisher output. Start in your first activation session — no thread dependency.
    DE session logs are MANDATORY — your first log is also the O3 trigger that allows
    COO to schedule the ADVI-004/005/006 alignment threads.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</ref>
    <ref>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="investigate">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
      <file action="modify">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="I2.1">
      Read AdvisorsTab.tsx and locate the leaderboard sort logic.
      Determine root cause:
        (a) Frontend: JS .sort() with no secondary key — unstable on NNA ties.
        (b) Data: architect_leaderboard.json entries not pre-sorted or rank field incorrect.
        (c) Both.
      Check the S3 output for architect_leaderboard.json to confirm the rank field
      and sort order of entries.
    </requirement>
    <requirement id="I2.2">
      If (a) or (c): implement stable sort in AdvisorsTab.tsx.
      Add a secondary sort key (name as tiebreaker) for equal NNA values:
        .sort((a, b) => a.nna !== b.nna ? a.nna - b.nna : a.name.localeCompare(b.name))
      Run bunx tsc -b to confirm no type errors. Commit the fix.
    </requirement>
    <requirement id="I2.3">
      If (b) or (c): document the data-side sort issue in your session log.
      Add a next-steps item for DS to fix publisher sort logic, and for DT to deploy.
      Do not wait on this to mark I2 complete — the frontend fix is the immediate action.
    </requirement>
    <requirement id="I2.4">
      Update pod_inventory.xml to reflect the current leaderboard sort behavior
      (resolved vs. still-open data-side issue).
    </requirement>
    <requirement id="LOG.1">
      Write a session log for this work session at:
        org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-03-03/{scope}.md
      Minimum sections: Objective, Work Completed, Decisions Made, Files Modified,
      Blockers, Current State, Next Steps. Include portal DEV commit hash in header.
      This log is mandatory and serves as the O3 trigger for COO to schedule
      ADVI-004/005/006 alignment threads.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Root cause determined (a, b, or c) with specific file/line evidence cited.</criterion>
    <criterion id="2">Frontend sort fix committed if (a) or (c). bunx tsc -b passes.</criterion>
    <criterion id="3">Data-side issue flagged in session log next steps if (b) or (c).</criterion>
    <criterion id="4">pod_inventory.xml updated for leaderboard sort resolution status.</criterion>
    <criterion id="5">Session log written — mandatory, no exceptions.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Session logs are MANDATORY for DE — not optional. Write one for every work session.</constraint>
    <constraint>Do NOT push to DEV yourself. DT owns all pushes. Your role: commit and signal DT.</constraint>
    <constraint>Do NOT use emojis in any code or log output. Plain ASCII only.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;" -m "0.4.0_DE_ClientPlatform: AdvisorIntelligence/AdvisorsTab -- leaderboard sort fix"</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">Leaderboard stable sort fix in AdvisorsTab.tsx (if frontend root cause)</deliverable>
    <deliverable type="document">Session log with root cause determination and fix notes</deliverable>
    <deliverable type="commit">pod_inventory.xml updated for leaderboard sort status</deliverable>
  </deliverables>
</task_order>
```
