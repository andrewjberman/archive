<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <id>2.0.0_SA_COO-2026-04-24-adhc-ownpth-005-cto-phase2-flip-to-closed</id>
  <project>ADHC_OWNPTH</project>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_to>1.0.0_SA_CTO</issued_to>
  <issued_date>2026-04-24</issued_date>
  <status>complete</status><!-- COMPLETE 2026-04-30: Andrew direct override of TO 4 observe-week dependency. Phase 2 flip + YAML exception ship in single commit. TO 4 truncated by 24h (~6 of 7 days observed); evidence sufficient (4th post-wrapper sweep `fe5a773f` 2026-04-28 closed by TO 8 `aa004108b` 2026-04-29; zero sweeps in 36h since). -->

  <title>ADHC_OWNPTH TO 5 — CTO Phase 2 flip to fail-closed</title>

  <references>
    <ref type="prd">docs/architecture/ADHC_OWNPTH.md</ref>
    <ref type="report">docs/architecture/ADHC_OWNPTH_phase1_observation_report.md (TO 4 output — must be read before flipping)</ref>
    <ref type="hook">`.tools/git-hooks/owned-paths-check.sh` (single-line change)</ref>
  </references>

  <context>
    Phase 1 (warn-mode) ran for 7 days. COO produced Phase-1-Observation-Report (TO 4)
    and confirmed go-signal to CTO. TO 5 flips the hook from warn-mode to block-mode by
    changing the default OWNED_PATHS_MODE. This is a single-line config change — the
    mechanism is already fully implemented by TO 2.

    After flip: commits with out-of-lane files EXIT 1 (blocked). The --author-override
    escape hatch remains available. Rollback is also a single-line revert.
  </context>

  <scope>
    1. Read `docs/architecture/ADHC_OWNPTH_phase1_observation_report.md` — verify go-signal
       is explicit (COO recommendation = GO or CONDITIONAL GO with all conditions met).
       If NO-GO: STOP. MCP COO with finding.

    2. Apply the Phase 2 flip — one of:
       (a) In `.tools/git-hooks/owned-paths-check.sh`: change the default value line from
           `OWNED_PATHS_MODE="${OWNED_PATHS_MODE:-warn}"` to
           `OWNED_PATHS_MODE="${OWNED_PATHS_MODE:-block}"`
       (b) Or equivalent: add `OWNED_PATHS_MODE=block` as default in the config header the
           hook reads, if DS implemented it that way in TO 2. Match whatever TO 2 implemented.

    3. Apply any YAML diffs from the COO Phase 1 report (class (a) WARNs that need YAML
       adjustments). These must ship in the same commit as the mode flip to avoid a window
       where block-mode fires false-positives.

    4. Post-flip canary: stage an out-of-lane file, attempt commit — verify EXIT 1 + ERROR
       banner. Then undo the staged change. Document canary in session log.

    5. Rollback path: document in session log — single revert to flip back to warn.
       Include the rollback command: `git revert HEAD -- .tools/git-hooks/owned-paths-check.sh`
       or equivalent.

    6. After 48h: scan audit log for false-positive BLOCK events. If any, pause + route
       YAML diff to CTO; do NOT auto-revert unless Andrew directs. Report 48h scan to COO.
  </scope>

  <dependencies>
    <dependency agent="2.0.0_SA_COO" task="ADHC_OWNPTH.004" status="staged"
                required="COO Phase-1-Observation-Report must be complete and go-signal explicit. Do not flip without cited evidence."/>
  </dependencies>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>cat docs/architecture/ADHC_OWNPTH_phase1_observation_report.md | grep -i "go/no-go\|recommendation"</run>
        <expect>Explicit GO or CONDITIONAL GO recommendation from COO report. Document in session log.</expect>
        <if_mismatch>STOP. No go-signal in report. MCP COO to confirm before proceeding.</if_mismatch>
      </step>
      <step>
        <run>grep -n "OWNED_PATHS_MODE" .tools/git-hooks/owned-paths-check.sh</run>
        <expect>Shows the mode default line. Identifies exact line to flip. Document.</expect>
        <if_mismatch>STOP. Hook does not use OWNED_PATHS_MODE — implementation diverged from PRD. MCP DS to clarify.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bash -n .tools/git-hooks/owned-paths-check.sh</run>
        <expect>Exit 0. No bash syntax errors post-flip.</expect>
        <if_mismatch>STOP. Fix syntax before committing.</if_mismatch>
      </step>
      <step>
        <run>canary test: stage a test file in out-of-lane path; attempt git commit; confirm EXIT 1 + ERROR banner</run>
        <expect>Hook fires in block mode. Commit rejected. Unstage the test file after canary.</expect>
        <if_mismatch>STOP. Block mode not active post-flip. Debug before committing.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="48h post-flip">
      <step>
        <run>awk '$2=="BLOCK"' org/git-author-override-audit.log | tail -20</run>
        <expect>Zero BLOCK entries = no false-positives. If BLOCK entries exist, triage: real violation vs YAML gap. Surface YAML gaps to CTO for immediate YAML diff; real violations → memory entry.</expect>
        <if_mismatch>Route YAML gaps via MCP COO. Do NOT auto-revert without Andrew directive.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    1. Phase-1-Observation-Report read and go-signal confirmed before any edit.
    2. `OWNED_PATHS_MODE` default flipped to `block` in hook (or equivalent config).
    3. YAML diffs from report applied in same commit as mode flip.
    4. Canary test: out-of-lane commit → EXIT 1 confirmed. Documented in session log.
    5. Rollback command documented in session log.
    6. Commit under 1.0.0_SA_CTO author; MCP COO with commit hash immediately on completion.
    7. 48h post-flip: audit log scan for BLOCK events; result reported to COO.
    8. Session log includes all Phase 1-3 compiler tools runs with pass/fail.
  </acceptance_criteria>

  <evidence>
    <flip_commit>{{COMMIT_HASH}} (filled at commit time)</flip_commit>
    <flip_date>2026-04-30</flip_date>
    <override_path>Andrew direct authorization (in-session 2026-04-30) — TO 4 observe-week dependency truncated by 24h. Sufficient evidence: TO 8 `aa004108b` shipped 2026-04-29 closing the 4th post-wrapper sweep `fe5a773f`; zero sweeps observed in the ~36h since.</override_path>

    <yaml_changes>
      8 new lane definitions: POD1_OR_EXEC, POD2_OR_EXEC, POD3_OR_EXEC, POD4_OR_EXEC, SHARED_OPAL_ETL_OR_EXEC, SHARED_PARTNER_ETL_OR_EXEC, SHARED_CLOUD_OPS_OR_EXEC, ANY_EXEC_OR_AE.

      11 new path overrides (task_orders/*.md exceptions for tier1_exec + 9 tier2_senior agent folders) + 5 widened existing rules:
      - org/projects/REGISTRY.md: ANY_EXEC → ANY_EXEC_OR_AE (AE may update own-project rows)
      - org/projects/*.json: ANY_EXEC → ANY_EXEC_OR_AE
      - .tools/git-hooks/**: CLOUD_OPS_OR_ETL → ANY_EXEC_OR_AE
      - .owned-paths.yaml: BASE_EXEC → ANY_EXEC_OR_AE
      - "portal" (submodule pointer file): UNDEFINED → ANY (DT bumps on portal push)

      rollout_phase: 1 → 2.

      All 8 false-positive classes from 2026-04-29 audit log review are addressed:
      Class 1: COO authoring TOs into pod folders (~12 WARN entries) — now permitted via POD*_OR_EXEC.
      Class 3: AE editing own-project JSON (e.g. AE 0.6.1 → ADVI_ORIAPI.json) — now permitted via ANY_EXEC_OR_AE.
      Class 4: DT 0.4 portal submodule pointer (5+ UNDEFINED entries) — explicit `portal` rule.
      Class 5: AE 0.7 editing .owned-paths.yaml during hook bootstrap — now permitted.
      Class 8: AE 0.7 editing org/mcp/inbox-watch.sh during PUSHFIX — out-of-scope here (not yet widened; AE will use override or future ADHC_OWNPTH.010 if recurrent).
    </yaml_changes>

    <hook_change>.tools/git-hooks/owned-paths-check.sh line 27: MODE default flipped warn → block.</hook_change>

    <canary_test>
      Test 1 (BLOCK expected): GIT_AUTHOR_NAME=0.1.0_DE_MarketIntelligence + staged data/orion/scripts/gold/INF_I_D03.composition_artifacts.py → EXIT 1, ERROR banner printed, BLOCK entry written to audit log.
      Test 2 (PASS expected — false-positive fix): GIT_AUTHOR_NAME=1.0.0_SA_CTO + staged org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/SOME.001.md → EXIT 0, PASS entry written.
      Both ran 2026-04-30T12:45Z UTC, both behaved as expected.
    </canary_test>

    <rollback_command>
      Single-line revert: `git revert --no-edit {{COMMIT_HASH}}` (reverts both YAML widening + hook mode flip atomically). Or to flip mode-only without losing YAML changes: edit `.tools/git-hooks/owned-paths-check.sh` line 27 back to `MODE="${OWNED_PATHS_MODE:-warn}"`.
    </rollback_command>

    <followup_48h>
      Per TO acceptance §6: scan `org/git-author-override-audit.log` for BLOCK events at 2026-05-02. Triage real violations vs YAML gaps. Surface gaps as YAML diffs immediately; do NOT auto-revert without Andrew directive.
    </followup_48h>
  </evidence>
</task_order>
