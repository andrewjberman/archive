<task_order>
  <metadata>
    <id>ADVI_STAUDT.CHART-ALIGN</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <lane_preference>~D (D_00c was previously ~D-owned; if ~D is idle, prefer that continuity)</lane_preference>
    <date>2026-04-21</date>
    <status>complete</status>
    <acked>2026-04-21 ~13:03 ET (DS)</acked>
    <project_code>ADVI_STAUDT</project_code>
    <priority>P1 — corrects leaderboard attribution methodology to match chart methodology. Prevents comp gaming (advisor onboarding mid-quarter claiming pre-tag flows) and fixes the historical-truth semantic on "Lifetime Activity" chart ↔ leaderboard surfaces.</priority>
    <sla>~4h (single-script change in D_00c L764-779 + validator + qa-runner --group D validation)</sla>
    <decision_authority>Andrew 5-item walkthrough 2026-04-21 PM per CTO session log `org/tier1_exec/1.0.0_SA_CTO/logs/2026-04-21/session36_five_item_decisions.md` §2. Commit `0a37d545`. Paired with DE sibling TO `ADVI_STAUDT.CHART-ALIGN-FE` (caveat removal).</decision_authority>
  </metadata>

  <references>
    <ref type="decision_record">org/tier1_exec/1.0.0_SA_CTO/logs/2026-04-21/session36_five_item_decisions.md §2</ref>
    <ref type="sibling_fe_to">org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_STAUDT.CHART-ALIGN-FE.de-caveat-removal.md — DE removes chart/leaderboard divergence caveat ONCE DS CHART-ALIGN lands + leaderboard matches chart.</ref>
    <ref type="chart_precedent">D_02 commit `048af6a3` — already implements per-day tagging gate correctly for chart. CHART-ALIGN propagates the same rule to D_00c leaderboard. Chart HOLDS, leaderboard cuts over.</ref>
    <ref type="expected_result">Travis Penfield Q2 leaderboard NNA converges from `-$6.311M` (current pre-cutover, current-snapshot × full-window) → `-$6.845M` (chart value, per-day tagging gate). Exact convergence is the acceptance criterion.</ref>
    <ref type="cto_resolution">CTO Option A PASS — 2026-04-21. AC2 corrected: Travis architect-role QTD NNA convergence (per-day tagging gate). Original pre-C_01 target of -$6.845M superseded (pre-dates Schwab Phase 6a baseline shift 2026-04-21). Post-C_01 current: D_02 architect = -$6.532M, D_00c architect = -$6.541M, delta $9K = 0.14% — PASS. Methodology correct. DE caveat removal authorized.</ref>
    <ref type="canonical_rule">All FLOW attribution (NNA, leaderboard, chart) is time-windowed per-day tagging-gated: a flow on account `A` on day `D` is attributed to advisor `V` iff `V` was tagged to `A` on day `D`. No backfill attribution for pre-tag flows. AUA (stock) is EXEMPT — stays current-snapshot for `role_breakdown.aua`.</ref>
    <ref type="project_json">org/projects/ADVI_STAUDT.json (phase updated `0a37d545`)</ref>
  </references>

  <objective>
    Cut `D_00c.portal_leaderboard.py` L764-779 (leaderboard attribution loop) from the current "current-snapshot × full-window" rule to the per-day tagging-gated rule already shipped on D_02 chart (048af6a3). Validate convergence on Travis Penfield Q2 leaderboard NNA: pre-cutover `-$6.311M` → post-cutover `-$6.845M` (matches chart).

    **EXPLICIT NON-SCOPE:**
    - NO change to `role_breakdown.aua` — AUA stays current-snapshot (internally inconsistent with NNA by design; AUA is "what do you manage today", NNA is "what flows did you cause during your tagged window").
    - NO change to D_02 chart — chart already correct.
    - NO change to any non-leaderboard artifact.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py — L764-779 attribution loop. Replace current-snapshot × full-window with per-day tagging gate.</file>
      <file action="modify">data/black_diamond/scripts/gold/gold_validate_config.yaml — add/extend validator block for D_00c leaderboard attribution: Travis Penfield Q2 NNA spot-check at `-$6.845M ±$0.05M`, plus general firm-level leaderboard NNA sum parity with chart sum (if chart sum is available in validator context).</file>
      <file action="read-only">data/black_diamond/scripts/gold/D_02.advisor_client_detail.py L~??? (the 048af6a3 per-day gate logic, as implementation reference)</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="d00c-attribution-cutover">
      Rewrite D_00c L764-779 attribution loop:
      - For each (account, date) pair in the flow window, look up which advisor(s) were tagged to that account ON that date (not the current snapshot).
      - Accumulate attribution to the advisor(s) tagged at flow-date.
      - If no advisor was tagged at flow-date, flow is untagged (same treatment as chart — untagged flows surface in a firm-level bucket, not per-advisor).
      - Preserve the existing output schema — no new fields, no dropped fields; only the attribution numbers change.
    </deliverable>
    <deliverable id="travis-penfield-convergence-check">
      In-script or post-run validator: Travis Penfield Q2 leaderboard NNA MUST come within ±$0.05M of `-$6.845M` (chart value). If `-$6.311M` or anything outside the tolerance, cutover incomplete or methodology drift — STOP.
    </deliverable>
    <deliverable id="validator-extension">
      Add to `gold_validate_config.yaml`:
      - Spot-check: Travis Penfield Q2 NNA `-$6.845M ±$0.05M` (named-advisor sentinel; allowed to document temporal drift if the post-cutover value moves naturally)
      - Chart↔leaderboard convergence: if chart's firm-level NNA sum and leaderboard's firm-level NNA sum are both available, assert `abs(chart_nna_sum - leaderboard_nna_sum) / chart_nna_sum < 50bps` (defensive — catches future methodology drift between the two surfaces)
    </deliverable>
    <deliverable id="qa-runner-validation">
      After DS commit + S3 upload, qa-runner `--group D` (or `--from D_00c`) dispatches the new D_00c. Acceptance: qa-runner clean + Travis spot-check passes + any other leaderboard-consumer tests green.
    </deliverable>
  </deliverables>

  <wire_contract>
    - D_00c output schema UNCHANGED. Leaderboard attribution numbers shift per methodology — advisors who onboarded mid-quarter see smaller NNA (correctly attributed only to their tagged window), advisors tagged through full quarter see matching chart numbers.
    - Firm-level NNA sum may shift slightly if pre-tag flows were previously attributed that now become untagged. Expected residual untagged bucket: ~2-5% of firm-level NNA historically (per CTO session log §2; exact number surfaces in Phase 1).
    - Chart (D_02) is idempotent — no change expected.
    - role_breakdown.aua idempotent — no change expected.
  </wire_contract>

  <acceptance_criteria>
    1. D_00c L764-779 replaced with per-day tagging gate logic matching D_02 048af6a3 pattern.
    2. AC2 (corrected by CTO 2026-04-21): Travis architect-role QTD NNA convergence — D_00c per-advisor architect-role NNA must match D_02 per-advisor architect-role NNA within 50bps. Original pre-C_01 target of -$6.845M superseded (pre-dates Schwab Phase 6a baseline shift 2026-04-21). Post-C_01 current: D_02 architect = -$6.532M, D_00c architect = -$6.541M, delta $9K = 0.14% — PASS.
    3. `comp-validate D_00c --artifact /tmp/leaderboard_*.json` exits 0 (validator extension included).
    4. qa-runner `--group D` (or `--from D_00c`) exits clean on the new code.
    5. Chart ↔ leaderboard firm NNA sum within 50bps (or documented gap with residual-untagged bucket evidence).
    6. D_02 chart output byte-identical pre vs post (idempotent check — chart should not shift).
    7. role_breakdown.aua output byte-identical pre vs post (AUA is NOT touched).
    8. Session log reproducing every `<run>` from `<compiler_tools_mandate>` with observed output + pass/fail vs `<expect>`. Include Travis Penfield manual spot-check.
    9. MCP DE on DS commit + S3 upload so DE can fire the CHART-ALIGN-FE caveat removal TO.
    10. MCP COMPLETE to COO with commit hash + qa-runner evidence + Travis convergence + chart↔leaderboard parity.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_00c</run>
        <expect>READS include silver/roles (or equivalent tagging source) + silver/transactions (for flow dates). WRITES includes leaderboard_*.json under gold/platinum/*. No COLUMN GAPS.</expect>
        <if_mismatch>If silver/roles not in READS, the current attribution is likely reading from a current-snapshot join — that IS the bug. Add silver/roles with full history window.</if_mismatch>
      </step>
      <step>
        <run>Read D_02.advisor_client_detail.py 048af6a3 — locate the per-day tagging gate logic</run>
        <expect>Find the date-indexed tagging join pattern (likely a merge_asof or date-gated filter). Capture the exact structure to replicate in D_00c.</expect>
        <if_mismatch>If pattern is unclear from D_02, surface to COO — may need CTO architecture clarification before writing.</if_mismatch>
      </step>
      <step>
        <run>comp-blast D_00c</run>
        <expect>Downstream = leaderboard-consuming portal components (AdvisorIntelligence, FirmLeaderboard, PartnerAnalytics, etc. — confirm via comp-platinum reverse). No unexpected consumers.</expect>
        <if_mismatch>If new downstream appears, flag to COO.</if_mismatch>
      </step>
      <step>
        <run>Manual Travis Penfield Q2 spot-check against current D_00c output (pre-cutover baseline)</run>
        <expect>Current value `-$6.311M ±tolerance`. Confirms baseline matches CTO session log §2 figure. This is your pre-cutover reference point.</expect>
        <if_mismatch>If pre-cutover Travis NNA diverges from `-$6.311M`, data has shifted since CTO's measurement. Document but proceed; post-cutover convergence target remains `-$6.845M` from chart.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>`python -c "import ast; ast.parse(open('data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py').read())"` AND importlib exec_module smoke gate (HLOT2 standardization)</run>
        <expect>Both exit 0. Catches latent NameError / missing import / top-level ImportError — same-class defense as 081223b5 / 048a6fa3.</expect>
        <if_mismatch>STOP. Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>Local run of D_00c against latest silver; manual Travis Penfield Q2 NNA spot-check</run>
        <expect>Travis Q2 NNA = `-$6.845M ±$0.05M` (converges to chart value). Firm-level NNA sum within 50bps of chart firm-level NNA sum.</expect>
        <if_mismatch>STOP. If Travis doesn't converge, attribution rule is wrong — iterate. Do NOT commit divergent methodology.</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_00c --artifact /tmp/leaderboard_*.json</run>
        <expect>Exit 0. New validator block passes (Travis spot-check + chart↔leaderboard sum parity).</expect>
        <if_mismatch>STOP. Do not commit until ERROR clean.</if_mismatch>
      </step>
      <step>
        <run>Idempotency check: re-run D_00c twice against identical inputs; diff outputs byte-by-byte</run>
        <expect>Byte-identical. Per-day tagging gate is deterministic given fixed silver inputs.</expect>
        <if_mismatch>Non-determinism surfaced — debug (likely dict ordering or float precision) before commit.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>qa-runner `--group D` (or `--from D_00c`) dispatched by DS per DS-owned deploy cycle (CLAUDE.md Rule 13 / ADHC_DSFLOW)</run>
        <expect>Exit clean. D_02 chart output byte-identical pre vs post. role_breakdown.aua byte-identical pre vs post. D_00c leaderboard shifted per new methodology, Travis converged.</expect>
        <if_mismatch>qa-runner failure = rollback S3 artifact + re-examine methodology. Chart or AUA non-idempotent = BUG, STOP, escalate.</if_mismatch>
      </step>
      <step>
        <run>MCP DE (0.4.0_DE_ClientPlatform) with commit hash + artifact-ready signal so DE can fire CHART-ALIGN-FE caveat removal</run>
        <expect>DE ACK + DE starts FE TO.</expect>
        <if_mismatch>If DE doesn't ACK within reasonable time, escalate to COO.</if_mismatch>
      </step>
      <step>
        <run>comp-blast D_00c post-commit</run>
        <expect>Same consumer set as Phase 1. No new downstream during write.</expect>
        <if_mismatch>Flag to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>**CHART-ALIGN-FE (DE caveat removal) GATED ON THIS TO**. DE cannot remove the planned chart/leaderboard divergence UX caveat until DS CHART-ALIGN ships + leaderboard matches chart. DS must MCP DE on commit + qa-runner pass.</item>
    <item>**No coordination with COHORT-A** — different surface. COHORT-A emits D_04 summary; CHART-ALIGN modifies D_00c leaderboard. Parallel-safe.</item>
    <item>**KPI 50bps sentinel CANCELLED** (separate 5-item decision §2). Do NOT add a 50bps firm AUA sentinel — Andrew explicit: sentinel is irrelevant, not a gate. The chart↔leaderboard convergence check in this TO's validator is about methodology parity, not AUA accuracy.</item>
    <item>D_02 (chart) HOLDS. Do NOT modify D_02 in this TO. If the per-day logic needs upstream refactor to share between D_02 + D_00c, scope it as a follow-up refactor TO — not in CHART-ALIGN.</item>
  </cross_domain_coordination>

  <next>
    On staged→pending GO from COO: DS Phase 1 (compiler mandate phase 1) → build cutover → local Travis spot-check converges → commit → S3 upload → qa-runner --group D → MCP DE with artifact-ready → MCP COO COMPLETE with evidence bundle.
  </next>
</task_order>
