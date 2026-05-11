<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFTGT.TO-4</id>
    <project>ADVI_INFTGT</project>
    <title>[P0] Sign-correct Continuous NNA (Inflows+/Outflows-) + remove "Pending Script 09 deploy (D1)" placeholder at DistributionTab.tsx:3355</title>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>complete</status>
    <priority>P0 — partner-blocking</priority>
    <authorized_by>Andrew direct GO 2026-05-11; PRD ADVI_INFTGT v0.1 (1.0.0_SA_CTO)</authorized_by>
  </metadata>

  <context>
    1. DistributionTab.tsx Continuous view shows sign-inverted NNA:
       Inflows display as -$496K (negative), Outflows display as +$1.98K (positive).
       Convention: Inflows MUST be positive, Outflows MUST be negative.

    2. DistributionTab.tsx:3355 has hardcoded "Pending Script 09 deploy (D1)" string.
       COO decision: HIDE this panel entirely until Script 09 ships.
       No customer-facing "pending" text — remove or conditionally hide.

    PRD §4.5 + §4.9. DistributionTab.tsx is the primary target.
  </context>

  <scope>
    <step>Phase 1 — Compiler runs:
      `comp-transform schema-check DistributionTab`
      `comp-routes trace getNmecNmncNna`
      `comp-cache collisions`
    </step>

    <step>Phase 2 — Sign fix: locate where Inflows/Outflows are rendered in the
      Continuous NNA view. Flip sign: Inflows = positive, Outflows = negative.
      Verify against nmec_nmnc_nna.json artifact (`total_nna: -33761.29` is net
      negative, which means Outflows &gt; Inflows — the sign convention must
      preserve this relationship correctly).</step>

    <step>Phase 3 — Remove placeholder: find DistributionTab.tsx:3355 (or current line).
      Conditionally hide the State-Relationship-Flow panel when Script 09 artifact
      is absent. No hardcoded "Pending" text. Use a clean conditional:
        `{script09Data &amp;&amp; &lt;StateRelationshipFlowPanel /&gt;}`
      or simply remove the section until the TO that ships Script 09.</step>

    <step>Phase 4 — Default state for "Account Sizes by State": auto-select the
      largest state (Washington based on geo data) on first render per PRD §4.9.</step>

    <step>Portal: `bun install && bun run dev --port 5175` — visual verify:
      - Continuous NNA: Inflows green/positive, Outflows red/negative
      - No "Pending Script 09" text visible anywhere
      - Account Sizes by State shows Washington data by default</step>

    <step>Portal commit on submodule DEV branch + push.</step>

    <step>RAVC2 to COO with screenshots: Continuous NNA sign-corrected + Distribution tab clean.</step>
  </scope>

  <acceptance_criteria>
    1. No "Pending Script 09 deploy (D1)" text visible on any partner build.
    2. Continuous NNA: Inflows ≥ 0, Outflows ≤ 0 across all windows.
    3. "Account Sizes by State" auto-selects largest state on first render.
    4. No layout breakage.
    5. Portal submodule commit on DEV.
    6. RAVC2 with screenshots.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      `comp-transform schema-check DistributionTab`
      `comp-routes trace getNmecNmncNna`
      `comp-cache collisions`
    </phase>
    <phase id="3" when="after commit">
      Visual diff: Continuous view sign; Distribution tab clean
    </phase>
  </compiler_tools_mandate>

  <notes>
    DE coordination: if Script 09 (INF_D_09.account_timeseries) is being scoped for
    an upcoming sprint, flag to COO; the conditional hide in step 3 can be swapped for
    the real panel when the artifact lands. For now: hide is the clean default.
  </notes>
</task_order>
