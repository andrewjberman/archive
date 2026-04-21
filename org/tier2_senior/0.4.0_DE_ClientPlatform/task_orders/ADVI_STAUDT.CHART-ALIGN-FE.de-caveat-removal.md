<task_order>
  <metadata>
    <id>ADVI_STAUDT.CHART-ALIGN-FE</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_STAUDT</project_code>
    <priority>P2 — UX cleanup. Removes a planned caveat (never shipped, or recently shipped depending on DE lane state) that explained chart↔leaderboard attribution divergence. Divergence is about to be eliminated by DS CHART-ALIGN, so the caveat text is obsolete.</priority>
    <sla>~1h (single-string / single-component removal + /frontend-dev acceptance)</sla>
    <decision_authority>Andrew 5-item walkthrough 2026-04-21 PM per CTO session log `org/tier1_exec/1.0.0_SA_CTO/logs/2026-04-21/session36_five_item_decisions.md` §2 — "DE removes any prior caveat about chart/leaderboard divergence once leaderboard matches chart (was staged from Option A contingency path)." Commit `0a37d545`.</decision_authority>
  </metadata>

  <references>
    <ref type="decision_record">org/tier1_exec/1.0.0_SA_CTO/logs/2026-04-21/session36_five_item_decisions.md §2</ref>
    <ref type="sibling_ds_to">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_STAUDT.CHART-ALIGN.ds-d00c-leaderboard-per-day-gate-cutover.md — DS cutover ships first; this FE TO fires on DS artifact-ready MCP.</ref>
    <ref type="project_json">org/projects/ADVI_STAUDT.json (phase updated `0a37d545`)</ref>
    <ref type="context">A chart↔leaderboard divergence caveat was staged (either shipped or planned, depending on DE lane state on 2026-04-20) as part of the Option A contingency during the AUA active-filter decision arc. Post-CHART-ALIGN, leaderboard NNA matches chart NNA, so the caveat text is no longer accurate.</ref>
  </references>

  <objective>
    Remove any portal text / tooltip / helper-icon copy that warns users about chart-vs-leaderboard NNA attribution divergence. Once this TO ships, chart and leaderboard both use per-day tagging-gated attribution and produce matching per-advisor NNA values — the caveat was correct at its time of authoring but is now obsolete.

    **EXPLICIT NON-SCOPE:**
    - No data logic changes. This is pure copy / presentation.
    - No new components, no layout restructure.
    - Do NOT remove the "AUA is current-snapshot while NNA is time-windowed" note if one exists — AUA↔NNA internal inconsistency is preserved by design (per §2 decision: AUA stays current-snapshot for role_breakdown).
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/** — audit any caveat text / tooltip / info-icon copy on Firm Overview, Leaderboard, AdvisorIntelligence, Books/Distribution tabs that mentions chart↔leaderboard attribution divergence. Remove or rewrite per Phase 1 discovery.</file>
      <file action="read-only">Other portal pages — if discovery surfaces caveat text outside the obvious surfaces, scope expands only for CHART-ALIGN-related strings, NOT for AUA↔NNA text.</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="caveat-text-discovery">
      DE greps/searches `portal/src/**` for the caveat string (expected forms: "chart and leaderboard may differ", "attribution methodology", "current snapshot vs time-windowed", "tagging window", or similar phrases tied to the Option A contingency). Documents every location found in session log.
    </deliverable>
    <deliverable id="removal-or-rewrite">
      For each location:
      - If the text exclusively concerns chart↔leaderboard NNA divergence: DELETE.
      - If the text conflates chart↔leaderboard divergence with AUA↔NNA inconsistency: REWRITE to preserve the AUA↔NNA note (AUA is current-snapshot, NNA is time-windowed) and remove only the chart↔leaderboard sentence.
      - If the text is about something else (e.g., unrelated methodology note): LEAVE IT. Surface to COO in session log if ambiguous.
    </deliverable>
    <deliverable id="frontend-dev-acceptance">
      Run `/frontend-dev` on the affected tabs (Firm Overview, Leaderboard, AdvisorIntelligence at minimum). Visual acceptance: caveat gone, no layout regression, no broken tooltip references.
    </deliverable>
    <deliverable id="types-scan">
      `bunx tsc -b` passes clean. No dead tooltip props / helper strings / unused types left behind after removal.
    </deliverable>
  </deliverables>

  <wire_contract>
    - Zero data layer impact. Pure copy removal on frontend.
    - Zero API endpoint change.
    - Zero new query key.
    - Minor DOM removal on affected pages; no layout shift expected (caveat text was small).
  </wire_contract>

  <acceptance_criteria>
    1. DS CHART-ALIGN complete (dependency gate — do NOT start this TO until DS MCPs artifact-ready + qa-runner pass).
    2. All chart↔leaderboard divergence caveat text removed from portal/src.
    3. AUA↔NNA internal-inconsistency text PRESERVED where it exists (per §2 decision).
    4. `/frontend-dev` acceptance PASS on affected tabs.
    5. `bunx tsc -b` clean — no dead props or unused strings.
    6. DE commits to `portal/` DEV branch per standard DE flow. DT 0.4 owns the DEV→CLOUD submodule pointer update if DE doesn't.
    7. Session log reproducing every `<run>` from `<compiler_tools_mandate>` with observed output + pass/fail vs `<expect>`. Include before/after screenshots of affected tabs.
    8. MCP COMPLETE to COO citing commit SHA(s) + screenshot paths.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Grep portal/src for caveat patterns: "chart" near "leaderboard", "divergence", "attribution", "time-window", "snapshot" — capture every hit.</run>
        <expect>Finite list of matches. Most likely concentrated in FirmOverview / Leaderboard / AdvisorIntelligence component files + any associated tooltip / info-copy constants file.</expect>
        <if_mismatch>If zero matches, caveat was never shipped — TO becomes a no-op. Document in session log and close. If dozens of matches, scope may expand — surface to COO.</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check FirmOverview / AdvisorIntelligence / FirmLeaderboard (whichever are affected)</run>
        <expect>No MISSING / NOTE / UNUSED surface from removal. The caveat was text-only — no schema tie.</expect>
        <if_mismatch>If UNUSED appears for a helper prop that was only fed by caveat state, delete the prop too (scope lock: only if unambiguously caveat-tied).</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>`bunx tsc -b` in portal/ subdirectory</run>
        <expect>0 errors. No dead types or unused props left behind.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>`/frontend-dev` on the affected tabs (Firm Overview + Leaderboard + AdvisorIntelligence at minimum)</run>
        <expect>PASS. Caveat gone visually. No layout regression. Tooltips on surrounding elements still work. AUA↔NNA note preserved if it was on-page.</expect>
        <if_mismatch>Iterate per /frontend-dev actionable fixes up to 5 times; escalate to COO if acceptance can't be reached.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-cache collisions (post-commit)</run>
        <expect>No new collisions. Caveat removal shouldn't touch react-query keys, but sanity-check.</expect>
        <if_mismatch>Unexpected — investigate.</if_mismatch>
      </step>
      <step>
        <run>Screenshot before/after capture at affected tabs; attach to session log</run>
        <expect>Visual evidence: caveat absent, surrounding UI intact.</expect>
        <if_mismatch>If a screenshot still shows the caveat, removal was incomplete — fast-follow patch.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>**GATED ON DS CHART-ALIGN** — do NOT start this TO until DS MCPs `ADVI_STAUDT.CHART-ALIGN` artifact-ready + qa-runner green + leaderboard NNA matches chart. Prematurely removing the caveat before data convergence = user sees inconsistent numbers without explanation.</item>
    <item>**AUA↔NNA note is OUT OF SCOPE.** Do not remove any text that explains AUA is current-snapshot while NNA is time-windowed — that internal inconsistency is preserved by design (per 5-item §2 decision).</item>
    <item>Paired GOs: COO issues CHART-ALIGN + CHART-ALIGN-FE together but DS fires first. DE inbox-watch should pick up DS artifact-ready MCP → DE flips staged→pending → starts work.</item>
  </cross_domain_coordination>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_STAUDT.CHART-ALIGN" status="staged">
      Gate hard. DE cannot start caveat removal before DS ships cutover + leaderboard matches chart. Dependency releases when DS MCPs artifact-ready.
    </dependency>
  </dependencies>

  <next>
    On DS CHART-ALIGN artifact-ready MCP: DE flips this TO staged→pending, runs Phase 1 grep + schema-check, removes caveat, runs Phase 2 tsc + /frontend-dev, commits to portal DEV, Phase 3 cache + screenshots, MCP COO COMPLETE.
  </next>
</task_order>
