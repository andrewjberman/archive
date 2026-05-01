<task_order>
  <metadata>
    <id>ADVI_49FRECN.001D</id>
    <project>ADVI_49FRECN</project>
    <title>Phase 0 Consolidation — Merge .001A/B/C + Phase 1 TO Recommendations</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-01</issued_date>
    <status>complete</status>
    <priority>P1 — gates Phase 1 remediation</priority>
    <estimated_effort>0.25d (consolidation only)</estimated_effort>
    <gates_on>ADVI_49FRECN.001A + .001B + .001C all RAVC4 complete</gates_on>
  </metadata>

  <context>
    Three parallel discovery slices feed this consolidation step. You (DS~B) own the merge.

    Inputs:
    - .001A (DS~A): Opal-side axis matrix shell + account-id list
    - .001B (you): missing-account trace + 49F-side integration + matrix completion
    - .001C (DS~C): AUA decomposition + classification drift audit

    Output: single coherent reconciliation report + Phase 1 remediation TO recommendations
    that CTO can dispatch from.
  </context>

  <objective>
    Merge the three slice findings into a single executive-level reconciliation document.
    Cross-validate findings (does DS~C's AUA gap allocation reconcile with DS~B's missing-account
    contribution?). Surface contradictions if any. Produce Phase 1 remediation TO recommendations.
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>Cross-validation</title>
      <detail>
        DS~C's AC #1 bound (account-undercount × avg-AUA) should reconcile with the actual
        AUA gap residual after subtracting MISSING_FROM_OPAL accounts. Verify the math is
        consistent across slices. If contradictions surface (e.g., DS~A's account count
        differs from DS~B's MATCHED+MISSING_FROM_OPAL count), flag and resolve before report.
      </detail>
    </ac>

    <ac id="2">
      <title>Executive summary</title>
      <detail>
        Two-paragraph summary at the top of `docs/architecture/49F_RECONCILIATION_2026-05-01.md`:
        - Paragraph 1: what we found (key gap quantification + dominant root cause)
        - Paragraph 2: recommended next moves (top 2-3 Phase 1 TOs by ROI)
      </detail>
    </ac>

    <ac id="3">
      <title>Unified reconciliation matrix</title>
      <detail>
        Single canonical version of the per-advisor / per-account-type / per-custodian tables
        with all columns filled (Opal-side from .001A; 49F-side from .001B; deltas computed).
        Live in a `## Reconciliation Matrix (Unified)` section.
      </detail>
    </ac>

    <ac id="4">
      <title>Phase 1 remediation TO recommendations table</title>
      <detail>
        Final section: `## Phase 1 Remediation Recommendations`.

        Markdown table: TO ID (suggest .002, .003, .004...) | Title | Lane (DS / AE / DT / RD) |
        Estimated effort | AC sketch (1-2 lines) | Priority (P0/P1/P2/P3) | Depends-on.

        Examples (do not prescribe — let findings drive):
        - DS C_01 + bd-pipeline ingest filter relaxation for in-flight rollover accounts
        - AE silver-stage backfill of {custodian} feed gap from {date}
        - DS classification drift fix — ETFClassifier coverage refresh
        - DT/DE Mix-tab bucket migration if classification axis is wrong
        - DS BD silver dedup logic — joint-account double-count

        For Schwab TRN NNA Phase 6 C_01 — explicit verdict: merge into a Phase 1 TO, keep parallel,
        or drop as superseded by 49FRECN findings.
      </detail>
    </ac>

    <ac id="5">
      <title>Open questions for CTO / Andrew</title>
      <detail>
        If anything in the discovery is unresolvable from data alone (e.g., 49F-side data Andrew
        couldn't share, ambiguity about whether closed-still-listed accounts SHOULD be included
        per partner agreement), list them in a `## Open Questions` section.
      </detail>
    </ac>

    <ac id="6">
      <title>Final commit + RAVC4</title>
      <detail>
        Single commit on CLOUD with the consolidated `49F_RECONCILIATION_2026-05-01.md`.
        Author: `0.4.0_DS_ClientPlatform_B <0.4.0_DS_ClientPlatform_B@opal.agent>` (underscore form
        per memory `feedback_author_serial_no_tilde.md`).

        RAVC4 to CTO with: commit ref + executive summary copied into the message + Phase 1 TO
        recommendation count.
      </detail>
    </ac>
  </acceptance_criteria>

  <ravc_target>
    <to>1.0.0_SA_CTO</to>
    <on_complete>RAVC4 with executive summary + commit ref + Phase 1 recommendations table. CTO dispatches Phase 1 TOs from your recommendations.</on_complete>
  </ravc_target>
</task_order>
