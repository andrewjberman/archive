# Task Order: ADVI_INFLV2.004 — DS~A: Revenue Ops 3-Candidate Design Brief

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-inflv2-004</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-27</date>
    <status>cancelled</status>
    <cancelled_date>2026-04-29</cancelled_date>
    <cancellation_reason>Andrew picked all 3 candidates (Activity Scan + Cash Drag Monitor + Position Concentration Risk) directly without needing a brief. .005 scope expanded to all 3 artifacts; brief no longer needed. Per COO 20260429T133551Z + 20260429T135300Z. Status edit by 0.4.0_DE_ClientPlatform.</cancellation_reason>
    <priority>HIGH — gates INFLV2.005 (Andrew pick required)</priority>
  </metadata>

  <objective>
    Andrew direction: "The 'Revenue Operations and Analysis' panel needs to be recreated
    for Inflection. Part of DS task order needs to be thinking about what cool scatters
    we could design based off the data available to us … find 3 options including [the
    activity scan] and identify how to realize them."

    DS~A produces a design brief with exactly 3 candidate InflectionInsightsPanel concepts.
    Each candidate fully specified. Andrew picks the winner(s). INFLV2.005 implements.

    Gate: INFLV2.001 COMPLETE (books inventory + feasibility confirmed, so DS~A knows
    which data sources are available).
  </objective>

  <scope>
    <task id="1" label="Candidate 1 — Client Activity Scan (Andrew-specified)">
      Andrew named this explicitly. Design spec:
        - Data inputs: Orion TRN transaction rows, date range selector
        - Metric: per-HH transaction frequency (TRN rows / window) → activity score
        - Segmentation: "Active" (above-median frequency) vs "Buy-and-Hold" (below-median)
        - Visualization: scatter (x=AUA, y=activity score, colored by segment) or
          sorted bar (HH ranked by activity). Include data availability confirmation.
        - Implementation effort: Low / Medium / High
        - Narrative: "Your most active clients generate X% of transactions from Y% of AUA"
    </task>

    <task id="2" label="Candidate 2 — DS~A pick (justify with data evidence)">
      Select one from this non-exhaustive menu based on Orion data availability:
        - Buy/sell concentration: which clients drive the most buy vs sell flow?
        - Asset-class drift: distance between current allocation and inferred target
        - Cash drag: HH % in cash-equivalent vs invested; time-in-cash histogram
        - Position concentration risk: Herfindahl index across top holdings per HH
        - Client tenure distribution: cohort age vs AUA growth rate

      Include: data inputs, visualization type, implementation effort, narrative hook.
      Justify why this candidate is interesting for Inflection specifically.
    </task>

    <task id="3" label="Candidate 3 — DS~A pick (justify with data evidence)">
      Select a second candidate (different from candidate 2). Same spec format.
    </task>

    <task id="4" label="Commit design brief">
      File: docs/briefs/inflv2-revenue-ops-candidates.md

      Format per candidate:
        ## Candidate [N]: [Name]
        **Data inputs:** ...
        **Visualization:** ...
        **Narrative hook:** ...
        **Inflection data availability:** [CONFIRMED / PARTIAL / ASSUMPTION: explain]
        **Implementation effort:** Low / Medium / High
        **COO recommendation:** [if DS~A has a preference, state it]

      Commit with:
        git commit --only docs/briefs/inflv2-revenue-ops-candidates.md
        Author: 0.4.0_DS_ClientPlatform_A <0.4.0_DS_ClientPlatform_A@opal.agent>
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      Brief committed with exactly 3 candidates, each with all 5 fields filled.
    </criterion>
    <criterion id="2">
      Each candidate includes an explicit Inflection data availability assessment
      (citing Orion fields from INFLEC_DATA_INVENTORY.md or INFLV2_BOOKS_SCOPE_FREEZE.md).
    </criterion>
    <criterion id="3">
      At least one candidate is CONFIRMED feasible from Orion txn data alone
      (not dependent on external joins).
    </criterion>
    <criterion id="4">
      RAVC to 2.0.0_SA_COO with commit hash + a one-line COO recommendation on
      which candidate to surface to Andrew first.
      Subject: RAVC — ADVI_INFLV2.004 COMPLETE | 3 candidates ready | recommend [N]
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Gate: INFLV2.001 must be complete. DS~A must have the books inventory
    + feasibility verdicts before claiming data is available.</constraint>
    <constraint>Do NOT implement any insight in this TO. Brief only. Implementation
    is INFLV2.005, gated on Andrew pick.</constraint>
    <constraint>No emojis in the brief doc (CloudWatch ASCII rule applies to all
    content that may appear in logs; markdown docs are plain ASCII).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform + 0.4.0_DS_ClientPlatform~A"
                task="ADVI_INFLV2.001"
                status="open"
                note="Books inventory + txn feasibility must be complete before
                claiming data availability for candidates 2 and 3."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">docs/briefs/inflv2-revenue-ops-candidates.md — 3-candidate
    design brief for InflectionInsightsPanel.</deliverable>
    <deliverable type="mcp">RAVC to 2.0.0_SA_COO. COO surfaces to Andrew for pick.
    Andrew pick is the go-signal for INFLV2.005.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLV2.md §3 (Andrew direction on Revenue Ops)</ref>
    <ref type="component">portal/src/pages/AdvisorIntelligence/_shared/tabs/FeeEfficiencyPanel.tsx (to be replaced by InflectionInsightsPanel)</ref>
    <ref type="inventory">docs/briefs/data-scientist-inflec-advisor-granularity.md §2 (Orion field inventory)</ref>
  </references>
</task_order>
```
