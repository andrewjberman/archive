# Task Order: AdvisorIntelligence DE Completion — 0.4.0_DE_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-de-advisor-intelligence-completion</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Drive completion of the AdvisorIntelligence page to v1.0 shippable state.
    DE responsibilities: leaderboard sort stability investigation (I2), review
    gate for all RD deliverables before DT pushes, NMNC/NMEC classification
    acknowledgment for DS (A2 gate), and Books tab coordination (G — blocked by thread).
    DE session logs are MANDATORY and are the primary status signal for COO tracking.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-continuous-nna-cla-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-advisors-stacked-bar-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-books-tab-design.sh</ref>
    <ref>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml</ref>
    <ref>portal/src/pages/AdvisorIntelligence/</ref>
    <ref>portal/src/api/endpoints/advisor-intelligence.ts</ref>
    <ref>portal/src/pages/AdvisorIntelligence/types.ts</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="investigate">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
      <file action="review">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
      <file action="modify">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml</file>
    </files>
  </scope>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM I2 — Leaderboard sort stability investigation + fix       -->
    <!-- UNBLOCKED                                                         -->
    <!-- ================================================================ -->
    <requirement id="I2.1">
      Investigate the leaderboard sort stability issue:
        (a) Frontend: check whether JS .sort() on equal NNA values is stable.
            Read AdvisorsTab.tsx sort logic — if there is no secondary sort key
            for ties, add name as a stable tiebreaker.
        (b) Data: check architect_leaderboard.json S3 output — confirm the rank
            field is correctly set and entries are pre-sorted by rank in the publisher.
      Determine root cause (a), (b), or both.
    </requirement>
    <requirement id="I2.2">
      If (a) — frontend sort fix: implement stable sort in AdvisorsTab.tsx.
        Use: .sort((a, b) => a.nna !== b.nna ? a.nna - b.nna : a.name.localeCompare(b.name))
        or equivalent. Commit the fix.
      If (b) — data fix: document the publisher sort bug in your session log and
        file a follow-up item in your next steps for DS + DT to address via script
        update and Lambda deploy.
      If both: fix the frontend sort now; flag the data issue separately.
    </requirement>
    <requirement id="I2.3">
      After investigation, update pod_inventory.xml to reflect the current leaderboard
      sort behavior (resolved vs. open).
    </requirement>

    <!-- ================================================================ -->
    <!-- PATTERN 0 THREAD PARTICIPATION — A1+A2 and A3                   -->
    <!-- ================================================================ -->
    <requirement id="thread.1">
      You are a participant in two Pattern 0 alignment threads. These threads run
      BEFORE DS writes any code for A1, A2, and A3. Your role in each:

      Thread 1 (2026-03-03-continuous-nna-cla-alignment):
        After DS describes available gold layer data, specify:
        - The TypeScript interface name(s) and shape the portal will use for adv_drill
        - The TypeScript interface name(s) and shape for cla_timeseries
        - The NMNC/NMEC definition your portal types currently expect
          (check header_metrics.json CLA structure vs what DS proposes)
        - Any query key or endpoint path change needed in advisor-intelligence.ts

      Thread 2 (2026-03-03-advisors-stacked-bar-alignment):
        After DS describes what script 10 can produce, specify:
        - The TypeScript interface for the stacked bar data per period
        - The TypeScript interface for the rolling 1Y series
        - How the period toggle maps to data keys
        - Outflow encoding requirement from a portal typing perspective

      The thread receipts are the binding interface specs. Your task orders for
      C2, C4, and 4C (issued to RD) reference these receipts. Do NOT finalize
      those stream requirements before the receipts are available.
    </requirement>

    <!-- ================================================================ -->
    <!-- RD REVIEW GATE — all streams before DT push                      -->
    <!-- ================================================================ -->
    <requirement id="review.1">
      You are the QA review gate for all RD (0.4.2_RD) commits before DT pushes to DEV.
      Review each stream as RD completes it:
        - C1 (GEO continuous): verify drill interaction works correctly, breadcrumb is clear
        - C3 (CLA snapshot): verify two-color NMNC/NMEC labels are accurate and match header_metrics.json field values
        - H (portal primitives refactor): verify no visual regression, panel structure is correct
        - I (Top Performers): verify rank clarity, period toggle updates rankings
        - C2, C4, 4C: review when RD signals completion (after DT B1/B2 deploys)
      Signal DT to push to DEV only after you have reviewed and approved.
    </requirement>
    <requirement id="review.2">
      After each RD stream you review, note it in your mandatory session log:
        - Stream reviewed, what you found, any corrections sent back to RD, approval status
      This is your primary status reporting mechanism to COO.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM G — Books tab coordination (BLOCKED by Stream D thread)   -->
    <!-- ================================================================ -->
    <requirement id="G.1">
      BLOCKED: Do not begin Books tab wiring until Stream D thread completes.
      When thread receipt lands in your threads/ folder, read the Books design brief at:
        docs/architecture/advisor_intelligence/books_tab_design_brief.md
      Your role for Books tab: API wiring (hook up L2/L3/L4 endpoints), auth gating
      logic (admin vs advisor view), and component structure — RD owns visual layout.
    </requirement>
    <requirement id="G.2">
      Auth gating for Books tab:
        - Admin (userRole === 'admin'): show advisor selector dropdown (all advisors)
        - Advisor: land directly on their own book — no dropdown, no selection
        - Use existing useAuth pattern for isInternal() / isDev() for L1 gating
        - Advisor identity resolution (JWT userId -> advisor name): implement ONLY after
          DS A5 investigation confirms the opal-users-v2 -> gold layer mapping exists.
          Do not assume the mapping exists until DS confirms.
    </requirement>
    <requirement id="G.3">
      Update pod_inventory.xml when Books tab API endpoints are wired.
      The Books tab section in pod_inventory.xml is currently missing — add it.
    </requirement>

    <!-- ================================================================ -->
    <!-- ONGOING — Session log mandate                                     -->
    <!-- ================================================================ -->
    <requirement id="log.1">
      DE session logs are MANDATORY. Write a session log for EVERY work session at:
        org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-03-03/{scope_action}.md
      Minimum sections: Objective, Work Completed, Decisions Made, Files Modified,
      Blockers, Current State, Next Steps.
      Include portal DEV commit hashes in header and Files Modified table.
    </requirement>
    <requirement id="log.2">
      Your first session log is also the pre-flight signal for COO to schedule
      the Books design thread (Stream D). COO cannot run the thread until you have
      at least one session log (O3 constraint in THREAD_KNOWLEDGE.md).
      Write your first session log after your initial orientation, before beginning I2.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">I2: Leaderboard sort root cause identified; frontend fix committed if applicable; data issue flagged if applicable.</criterion>
    <criterion id="2">A2-gate: NMNC/NMEC classification acknowledged in writing in session log before DS commits cla_timeseries.</criterion>
    <criterion id="3">All RD streams reviewed and documented in session log before DT pushes each stream to DEV.</criterion>
    <criterion id="4">Session log written for every work session (mandatory — no exceptions).</criterion>
    <criterion id="5">pod_inventory.xml updated for I2 resolution and Books tab endpoint wiring (post-thread).</criterion>
    <criterion id="6">Books tab auth gating wired and functional after DS A5 confirms mapping (post-thread).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Session logs are MANDATORY for DE — not optional. This is a system-wide rule, not just for this task order.</constraint>
    <constraint>Do NOT push to DEV yourself. DT owns all pushes. Your role: review and approve.</constraint>
    <constraint>Do NOT implement Books tab auth gating until DS A5 confirms opal-users-v2 -> gold layer mapping exists.</constraint>
    <constraint>Do NOT use emojis in any code or log output. Plain ASCII only.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
    <constraint>NOTE: You have no prior session logs. Write your first log immediately after orientation — it is the trigger for the COO to schedule the Books thread.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="A2-gate requires DS to send classification logic for acknowledgment"/>
    <dependency agent="2.0.0_SA_COO" task="Stream-D-thread" status="pending" note="G blocked until thread completes"/>
    <dependency agent="0.4.2_RD_AdvisorIntelligence" task="advisor_intelligence_completion" status="pending" note="Review gate on all C/H/I/G streams"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Leaderboard sort fix in AdvisorsTab.tsx (if frontend root cause)</deliverable>
    <deliverable type="document">Mandatory session log for every work session — first log triggers COO thread scheduling</deliverable>
    <deliverable type="document">Written NMNC/NMEC classification acknowledgment in session log</deliverable>
    <deliverable type="document">RD stream review notes in session log for each reviewed stream</deliverable>
    <deliverable type="commit">Books tab API wiring + auth gating (post-thread, per design brief)</deliverable>
    <deliverable type="commit">pod_inventory.xml updated for I2 and Books tab</deliverable>
  </deliverables>
</task_order>
```
