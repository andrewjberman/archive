<task_order>
  <metadata>
    <id>ADVI_INFFIN.008</id>
    <slug>dsa-advisor-list-regression</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-05-13</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <priority>P0 — partner-visible regression on previously-working Advisor List panel; trumps .004 P2 in priority sequencing</priority>
    <sla>~30min Phase 1 empirical investigation; +~1-2h Phase 2 fix if data-side cause; fork to RD-A if FE-side cause</sla>
    <project_code>ADVI_INFFIN</project_code>
  </metadata>

  <references>
    <ref type="brief_addendum">DE 0.4 Surface #10 addendum MCP 2026-05-13 evening; brief file edit pending</ref>
    <ref type="project_json">org/projects/ADVI_INFFIN.json</ref>
    <ref type="authority">Andrew direct evening walkthrough + DE 0.4 follow-up flag — "you and DS~B need to figure out why Advisor List panel is not surfacing anymore on Inflection's ADVI page... A recent gold/platinum run just finished, that is the logical start place"</ref>
    <ref type="cross_link">Sibling: .004 DS~A directory artifact (your other active TO — P2 small isolated; .008 P0 takes priority sequencing). DE MCP'd both DS~A + DS~B parallel; DS~A is actual owner per FE root-cause trace (INF_D_00c leaderboard emit lane).</ref>
    <ref type="adjacent_ship">Your earlier ship INF_D_00c.portal_leaderboard.py `6b94d8a8a` (INFGRO.004 leaderboard GRO rollup; landed today). Likely regression source candidate.</ref>
  </references>

  <context>
    Andrew flagged via DE 0.4 a P0 partner-visible regression AFTER the initial 9-surface INFFIN walkthrough: Advisor List panel on Inflection AdvisorIntelligence → Books tab shows "No advisor data available" empty state with the entire panel suppressed.

    **FE root-cause path (DE traced):**
    - `portal/src/pages/AdvisorIntelligence/_partners/inflection/ClientsTab.tsx:803`
    - Ternary: `periodAdvisors.length > 0 ? <AdvisorSummaryTable> : <EmptyState>`
    - `periodAdvisors` derives from `dashboardQuery.data.employee_leaderboard.windows[1Y].entries[]`
    - Filtered by `INFLECTION_LAYOUT.panels.advisorList.allowedAdvisorKeys = ['inflection_wealth_management', 'peter_lee', 'patrick_scanlan', 'joe_brandenburg']`
    - Falls through to empty state if entries[] is empty OR advisor_id values no longer match the 4 hardcoded keys

    **Possible causes:**
    1. **Data-side:** chain #27 mode=full just completed (~20:50Z) — `s3://opal-data-inf/platinum/firm/leaderboard.json` `windows.1Y.entries[]` empty post-chain
    2. **Data-side:** advisor_id values mutated (case/whitespace/format drift) so FE filter doesn't match expected keys
    3. **FE-side:** filter logic bug introduced; entries[] populated but filter mis-applied

    **Likely candidates given chain #27 just landed:**
    - INF_D_00c.portal_leaderboard.py `6b94d8a8a` (your INFGRO.004 ship) — leaderboard emit; if this changed advisor_id casing/format inadvertently, would cause filter mismatch
    - INF_D_02 / INF_D_03 advisor_key derivation (Path β slug from rep_name) — confirmed EXACT 4 advisor distribution via chain #27 RAVC3 (Peter Lee 627 / Patrick Scanlan 150 / Joe Brandenburg 67 / IWM 17); so advisor_id values should be correct
    - INFGRO.003 INF_C_02 daily geometric decomp `252c6c608` — additive cols only on existing daily output; shouldn't affect leaderboard

    **Andrew quote:** "A recent gold/platinum run just finished, that is the logical start place" — confirms chain #27 as trigger.

    **Per DE alternative-split assignment:** DS~A is the actual owner (INF_D_00c.portal_leaderboard.py lane); DS~B is fallback per Andrew naming. DE MCP'd both in parallel; this TO formalizes DS~A as primary.
  </context>

  <objective>
    Investigate Advisor List panel regression via empirical S3 inspection + 4-step diagnosis fork:

    1. **Phase 1 (empirical):** download `s3://opal-data-inf/platinum/firm/leaderboard.json` post-chain-27; inspect `employee_leaderboard.windows.1Y.entries[]` count + advisor_id values
    2. **Phase 2 fork:**
       - **Data-side issue:** entries[] empty OR advisor_id values mismatch → fix INF_D_00c (or upstream emit script) + chain re-run (route to AE 0.6.1)
       - **FE-side issue:** entries[] populated + advisor_id correct → fork to RD 0.4.2 (.001 batch absorbs OR new RD TO authored)

    Lightweight TO; investigation-first + fork-on-finding. Priority sequencing: .008 P0 trumps .004 P2 for your wall time; .004 resumes after .008 closes.
  </objective>

  <scope>
    <surfaces>
      <surface id="10">Advisor List panel "No advisor data available" empty state on Inflection AdvisorIntelligence Books tab</surface>
    </surfaces>
    <files>
      <file action="empirical_inspect">s3://opal-data-inf/platinum/firm/leaderboard.json (post-chain-27 state)</file>
      <file action="investigate">data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py (your INFGRO.004 ship; advisor_id emit shape)</file>
      <file action="investigate">portal/src/pages/AdvisorIntelligence/_partners/inflection/ClientsTab.tsx:803 (FE root-cause trace per DE)</file>
      <file action="investigate">portal/src/pages/AdvisorIntelligence/_partners/inflection/constants.ts (INFLECTION_LAYOUT.panels.advisorList.allowedAdvisorKeys hardcoded values)</file>
      <file action="conditional">If data-side fix needed: edit INF_D_00c.portal_leaderboard.py + dispatch chain re-run via AE 0.6.1</file>
      <file action="conditional">If FE-side fix needed: route to RD-A for absorption into ADVI_INFFIN.001 OR new TO authored by COO</file>
    </files>
  </scope>

  <phase id="1" when="empirical-investigation">
    <step>
      <description>Download `s3://opal-data-inf/platinum/firm/leaderboard.json` post-chain-27 to local. Use `aws s3 cp` or similar.</description>
      <expect>JSON file local for inspection.</expect>
    </step>
    <step>
      <description>Inspect `employee_leaderboard.windows.1Y.entries[]`. Count entries. List `advisor_id` values for each entry.</description>
      <expect>Either entries[] empty (data-side issue) OR entries[] populated with values like `'peter_lee', 'patrick_scanlan', 'joe_brandenburg', 'inflection_wealth_management'` (FE-side issue) OR entries[] populated with DIFFERENT values (case/whitespace/format drift — data-side issue).</expect>
    </step>
    <step>
      <description>Cross-check FE expected keys: `['inflection_wealth_management', 'peter_lee', 'patrick_scanlan', 'joe_brandenburg']` per DE trace. Match emit values vs filter values.</description>
      <expect>Match confirms FE-side issue; mismatch confirms data-side drift.</expect>
    </step>
    <step>
      <description>If entries[] empty: walk back through INF_D_00c.portal_leaderboard.py to identify why emit dropped entries. Likely candidates: filter logic too strict; advisor_id derivation broken; upstream data source empty post-chain-27.</description>
      <expect>Empty cause identified.</expect>
    </step>
  </phase>

  <phase id="2" when="fork-fix">
    <branch_a>
      <condition>Data-side issue (entries[] empty OR advisor_id mismatch)</condition>
      <step>
        <description>Fix INF_D_00c.portal_leaderboard.py to emit entries[] with correct advisor_id values matching FE expected keys. Use the same advisor_key slug pattern proven through chain #27 (peter_lee + patrick_scanlan + joe_brandenburg + inflection_wealth_management).</description>
        <expect>Fix shipped; ds-commit-gate PASS + safe-deploy SHA-MATCH.</expect>
      </step>
      <step>
        <description>Dispatch chain re-run via AE 0.6.1. Light chain (gold-d mode acceptable since only INF_D_00c touched) materializes fixed leaderboard.json. Alternatively, Lambda direct-invoke if INF_D_00c is wrappable.</description>
        <expect>Fresh leaderboard.json with populated entries; Advisor List panel renders.</expect>
      </step>
      <step>
        <description>Empirical re-check: download leaderboard.json post-fix; verify entries[] populated + advisor_id values match FE filter.</description>
        <expect>Verified.</expect>
      </step>
    </branch_a>
    <branch_b>
      <condition>FE-side issue (entries[] populated + advisor_id correct; FE filter mis-applied)</condition>
      <step>
        <description>MCP COO with empirical evidence (entries[] count + values + screenshot/snippet of mismatch). COO routes to RD 0.4.2 (likely absorbed into .001 batch as defensive logging fix at ClientsTab.tsx:233 per DE diagnosis).</description>
        <expect>RD-A picks up fix; .008 DS-side closes with evidence-only deliverable.</expect>
      </step>
    </branch_b>
  </phase>

  <phase id="3" when="closure">
    <step>
      <description>Session log captures empirical evidence + diagnosis fork branch taken + fix commit hash (if data-side) OR RD handoff evidence (if FE-side).</description>
      <expect>Complete diagnostic trail logged.</expect>
    </step>
    <step>
      <description>MCP RAVC2 to COO with closure (data-side fix RAVC2 OR FE-side handoff RAVC2).</description>
      <expect>RAVC2 ships.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Empirical inspection of `s3://opal-data-inf/platinum/firm/leaderboard.json` post-chain-27 completed; entries[] count + advisor_id values documented.
    AC2: Diagnosis fork branch identified (data-side OR FE-side).
    AC3 (branch A): INF_D_00c (or relevant emit script) fixed; entries[] populated; advisor_id values match FE filter; ds-commit-gate PASS + safe-deploy SHA-MATCH; chain re-run (via AE 0.6.1 or Lambda direct-invoke) materializes fixed artifact.
    AC4 (branch A): Empirical re-check post-fix shows Advisor List panel renders.
    AC5 (branch B): MCP COO with empirical evidence + FE-side routing; RD-A absorbs (or new TO authored).
    AC6: Session log + RAVC2 to COO.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>aws s3 cp for empirical; grep/cat for JSON inspection</phase_1>
    <phase_2_a>comp-pipescript io INF_D_00c (column gaps + portal consumers); ds-commit-gate.sh on fix; safe-deploy SHA-MATCH</phase_2_a>
    <phase_2_b>FE handoff evidence; no DS-side ds-commit-gate needed</phase_2_b>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    PRIORITY SEQUENCING:
    - .008 P0 trumps .004 P2 for your wall time
    - Pause .004 after empirical Phase 1 reveals fork
    - .004 resumes after .008 closes
    - If Phase 1 is fast (~30min) and branch B (FE-side), .004 resumes immediately
    - If branch A (data-side, ~1-2h fix + chain re-run), .004 resumes after AE 0.6.1 chain RAVC2

    DOWNSTREAM:
    - If branch A: AE 0.6.1 chain re-run dispatch (small light chain, ~10-30min if gold-d acceptable)
    - If branch B: RD 0.4.2 fix absorption into .001 OR new TO

    NO CROSS-PROJECT IMPACT: leaderboard.json is firm-level artifact; doesn't conflict with .004 client_directory.json or other INFFIN scope.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <conditional>
      If data-side fix: chain re-run required to materialize fixed leaderboard.json. Light chain (gold-d) acceptable since only INF_D_00c touched.
    </conditional>
    <conditional>
      If FE-side fix: no data reprocess needed; FE rebuild only.
    </conditional>
  </data_reprocess_scope>

  <deliverables>
    1. Empirical leaderboard.json inspection evidence (Phase 1)
    2. Diagnosis fork branch identified
    3. If branch A: INF_D_00c (or relevant) fix commit + chain re-run RAVC2 ACK from AE 0.6.1
    4. If branch B: FE handoff to RD-A with evidence
    5. Session log with full diagnostic trail
    6. MCP RAVC2 to COO with closure
  </deliverables>

  <ravc>
    DS~A RAVC2 to COO post-AC1-6 PASS. COO ratifies + relays Advisor List panel rendering confirmation to Andrew/DE 0.4.
  </ravc>

  <notes>
    **Lightweight investigation TO** — full XML format per project convention but scope is investigation-first + fork-on-finding. Don't over-engineer; empirical inspection drives the fix path.

    **Per DE Surface #10 addendum:** this surface sits OUTSIDE the original 9-surface INFFIN 5-TO Phase 1/Phase 2 plan (regression vs greenfield). Added as .008 (sequential numbering preserved; not folded into existing TO).

    **Andrew named DS~B but DS~A is actual owner per FE root-cause trace** (INF_D_00c leaderboard emit lane). DE MCP'd both in parallel; this TO formalizes DS~A as primary. DS~B can stand down on Surface #10 (continue .005 49F audit) unless DS~A surfaces blocker.

    **Author identity:** `--author="0.4.0_DS_ClientPlatform~A <0.4.0_DS_ClientPlatform~A@opal.agent>"` per protocol.

    **Pause .004 priority sequencing:** P0 trumps P2. After Phase 1 empirical (~30min), .004 resumes if branch B (FE handoff). If branch A (data fix + chain re-run), .004 resumes after AE 0.6.1 chain RAVC2.
  </notes>
</task_order>
