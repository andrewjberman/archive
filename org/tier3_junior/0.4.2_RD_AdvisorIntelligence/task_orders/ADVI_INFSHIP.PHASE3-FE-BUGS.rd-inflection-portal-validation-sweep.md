<task_order>
  <metadata>
    <id>ADVI_INFSHIP.PHASE3-FE-BUGS</id>
    <project>ADVI_INFSHIP</project>
    <title>Inflection Portal Phase 3 RD Validation Bug Sweep — Frontend Findings 2026-05-01</title>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-01</issued_date>
    <status>open</status>
    <priority>P1 — gates ADVI_INFSHIP Phase 3 closure + V2 Andrew sign-off</priority>
    <estimated_effort>1-2d (4 frontend bugs + Phase 0 diagnostic)</estimated_effort>
    <branch>portal DEV (then PROD via DT push)</branch>
  </metadata>

  <context>
    Andrew validated the Inflection portal end-to-end on 2026-05-01 14:50 ET (login as Andrew → Select Partner → Inflection per Option C devauth path). Five problem areas surfaced. CTO triaged each into "data gap" (will resolve when HISTBF Wave B + silver/gold cascade finishes — currently blocked) versus "real frontend bug" (parallel-trackable now).

    This TO covers ONLY the frontend-side real bugs. The data-gap items are explicitly OUT OF SCOPE — they will resolve on the gold rerun cascade and re-validation will follow. The DS-side publisher bugs (Q2 '26 anchor, GRO methodology, monthly null-spike) are also OUT OF SCOPE here — those will be filed as separate DS TOs.

    Inflection tenant context (do not misapply BD/49F patterns):
    - 4 flat advisors (no Architect/Consultant/Implementor/Additional/LocalOps role taxonomy — that's BD/49F)
    - Firm-centric tenant template (PartnerAnalytics + Distribution stubbed + Books Firm Overview→ClientsList; no advisor profile drill)
    - 49F regression spot-check is also expected (W8.3 7/7 PASS prior, but multi-tenant changes mean a quick smoke is cheap insurance)

    Memory references:
    - feedback_inflection_advisor_structure.md (4 flat advisors, no role hierarchy)
    - project_inflection_advisor_structure.md (firm-level + per-advisor only)
    - feedback_inflec_frontend_dev_auth_path.md (Option C login path)
  </context>

  <objective>
    Investigate and fix the 4 frontend bugs surfaced in Andrew's 2026-05-01 portal validation. Phase 0 diagnostic confirms category (real bug vs data gap vs scope gap) for each finding before any code is touched. Each AC produces a verdict + fix or a clean root-cause writeup if not RD-actionable.
  </objective>

  <acceptance_criteria>
    <ac id="0">
      <title>Phase 0 diagnostic — confirm bug category for each finding</title>
      <detail>
        Before fixing anything, walk each finding and produce a written verdict: REAL_FE_BUG | DATA_GAP_AWAITING_HISTBF | SCOPE_GAP_NEW_COMPONENT | BACKEND_BUG_HANDOFF. Use browser DevTools Network panel to inspect failing requests; check React Query cache state; check S3 for the artifact paths the panel expects. This is the single most valuable artifact of the TO — it tells CTO/COO whether to wait on HISTBF or dispatch parallel fixes immediately.
      </detail>
    </ac>

    <ac id="1">
      <title>Distribution panel: state-drill error fallback</title>
      <symptom>
        Drilling into any state on Distribution → Snapshot → GEO surfaces "Unable to Load Distribution" error. Snapshot view itself works ($183M total, Washington 89.9%, etc.) — only the per-state drill fails.
      </symptom>
      <investigation>
        1. Open DevTools Network tab. Click on Washington (or any state) in the donut. Capture the failing request URL, status code, and response body.
        2. Identify the endpoint owner (Lambda? CloudFront behavior? Static S3 artifact?).
        3. If 404: artifact doesn't exist (data gap or scope gap). If 5xx: backend bug. If 200 with empty payload: client-side render failure.
      </investigation>
      <fix>
        If 404/empty: replace error message with graceful empty-state ("No historical state-level data yet for {state}. Available after the historical backfill completes."). Do not show "Unable to Load Distribution" — that reads as a system failure, not a data-availability state.
        If 5xx: file a BACKEND_BUG_HANDOFF writeup with endpoint + repro for AE/DT to fix.
      </fix>
      <pass>Drill on each state either renders data OR shows the graceful empty-state message. No "Unable to Load Distribution" error surface.</pass>
    </ac>

    <ac id="2">
      <title>Distribution panel: missing bell curve + last-period-snapshots container</title>
      <symptom>
        Distribution tab on Inflection has no bell curve component and no "last period snapshots" container. Both are present on BD/49F.
      </symptom>
      <investigation>
        1. Locate the BD/49F Distribution panel definitions (likely under portal/src/.../partners/{bd|49financial}/Distribution.tsx or analogous).
        2. Locate the Inflection Distribution layout config (per ADVI_INFLV2.006 useTenantLayout hook + layout config).
        3. Determine: are these components (a) tenant-gated OFF for Inflection by config, (b) wired but waiting on a data artifact that doesn't exist for Inflection yet, or (c) entirely missing from the Inflection tenant's layout config.
      </investigation>
      <fix>
        Case (a): flip the gate ON in the Inflection layout config and verify components render. Possibly with empty-state fallback if data isn't available.
        Case (b): write up the data dependency (which S3 artifact, which publisher) for DS handoff.
        Case (c): scope the layout config addition + propose to CTO (do NOT build new components without explicit approval — verify intent first).
      </fix>
      <pass>Either the components render with data, OR there's a clean writeup explaining what's needed and the dependency chain.</pass>
    </ac>

    <ac id="3">
      <title>Books tab: advisor list role filter wrong for Inflection</title>
      <symptom>
        Books tab → Advisor List shows 5 role chips (Architect, Consultant, Implementor, Additional Advisor, Local Ops) all on, but list is empty: "No advisors in current filter." Inflection has 4 flat advisors with no role taxonomy — these chips don't apply.
      </symptom>
      <investigation>
        1. Find the AdvisorList component and the role-filter chip implementation.
        2. Check if there's already a tenant-conditional render path (e.g., useTenantLayout hook returns Inflection-specific config).
        3. Confirm the actual advisor data source for Inflection — should return 4 flat entries (IWM, Peter, Patrick + 1 per project memory).
      </investigation>
      <fix>
        Hide the role-filter chip row for tenant=inflection. Render the 4 advisors flat. If no tenant-conditional render exists yet, add one keyed off the firm picker context. Do NOT shoehorn Inflection advisors into the BD/49F role buckets.
      </fix>
      <pass>Inflection Books tab shows 4 advisors as a flat list with no role chips visible. 49F regression: spot-check that 49F advisor list still renders all 5 role chips correctly.</pass>
    </ac>

    <ac id="4">
      <title>Books tab: missing firm overview panel</title>
      <symptom>
        Books tab on Inflection has no firm overview panel at the top. Per ADVI_INFLV2.007 BooksTab full impl spec, the firm overview panel was supposed to render at the top.
      </symptom>
      <investigation>
        1. Find the BooksTab component and check if a firm-overview panel exists in the JSX.
        2. If present: check tenant-conditional rendering (might be gated for BD/49F only).
        3. Check if it's wired to a data source that's currently empty (HISTBF data gap) — in which case the panel may be hidden by an `isEmpty` guard rather than missing.
        4. If the panel renders an empty container vs. is genuinely absent, take screenshots to disambiguate.
      </investigation>
      <fix>
        If gated off: enable for Inflection tenant.
        If empty-data hidden: replace silent hide with a "No firm overview data yet" empty-state container so users know the panel exists.
        If genuinely missing: scope the addition + propose to CTO before building.
      </fix>
      <pass>Firm overview panel either renders with data OR shows a labeled empty-state at the top of Books.</pass>
    </ac>

    <ac id="5">
      <title>49F regression smoke (cheap insurance)</title>
      <detail>
        Open one 49Financial advisor profile. Walk the panels you'd expect to render (Profile + Book + Distribution + GRO snapshot). Confirm no regressions from the multi-tenant changes that landed during INFLEC W4/INFLV2 work. W8.3 was 7/7 PASS prior — this is a 5-minute confirmation, not a full re-test.
      </detail>
      <pass>49F advisor profile loads cleanly, panels render with data, no console errors, no "Unable to Load" surfaces.</pass>
    </ac>
  </acceptance_criteria>

  <out_of_scope>
    Explicitly NOT in this TO (confirmed data gaps that will resolve on HISTBF rerun cascade):
    - AUA NMNC/NMEC split (vintage classification — needs accounts_v2 historical, currently UNAVAILABLE per HISTBF probe)
    - Asset mix breakdown (assets_v2 + positions_mv historical — pending Wave B)
    - GRO Quarterly view "data unavailable" (positions_mv historical — pending Wave B)
    - Distribution Continuous gray bars (per-state historical — pending Wave B)
    - Distribution NNA state view (vintage + transactions — pending Wave B)
    - Books Revenue Ops zeros (positions_mv + transactions joined to HHs — pending Wave B)
    - Books Concentration Risk placeholder (next clean gold dispatch)

    Also NOT in scope (DS-side publisher bugs — will be filed as separate DS TOs):
    - Q2 '26 = $0 anchor bug in D_00c period logic
    - GRO Annual 2026 YTD-vs-full methodology
    - GRO Monthly Feb/Apr '24 phantom -$178M spike (null-handling in period-diff)

    If RD discovers during Phase 0 that any of the above is actually a frontend bug rather than a data gap or DS bug, raise it with CTO immediately rather than expanding scope unilaterally.
  </out_of_scope>

  <gates_and_dependencies>
    <gates>None. Andrew's validation report is the input. Run from portal DEV; standard /frontend-dev workflow.</gates>
    <unblocks>ADVI_INFSHIP Phase 3 V1 RD smoke completion; V2 Andrew sign-off.</unblocks>
  </gates_and_dependencies>

  <ravc_target>
    <to>1.0.0_SA_CTO</to>
    <on_complete>
      RAVC4 with: Phase 0 diagnostic verdicts table (5 findings × category), commit refs for each fix, screenshots before/after, 49F regression result. If any finding requires backend handoff, include the endpoint + repro for the appropriate AE/DT.
    </on_complete>
  </ravc_target>

  <inputs>
    <input>Andrew's 2026-05-01 validation screenshots (5 problem areas, ~2:28-2:53 PM ET)</input>
    <input>CTO triage of the 5 problems (data-gap vs real-bug, in conversation 2026-05-01 ~18:50Z)</input>
    <input>memory/feedback_inflection_advisor_structure.md</input>
    <input>memory/feedback_inflec_frontend_dev_auth_path.md</input>
    <input>ADVI_INFLV2.007 BooksTab impl spec (firm overview panel intent)</input>
  </inputs>
</task_order>
