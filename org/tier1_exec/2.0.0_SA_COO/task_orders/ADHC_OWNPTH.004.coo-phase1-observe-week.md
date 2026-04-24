<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <id>2.0.0_SA_COO-2026-04-24-adhc-ownpth-004-coo-phase1-observe-week</id>
  <project>ADHC_OWNPTH</project>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_to>2.0.0_SA_COO</issued_to>
  <issued_date>2026-04-24</issued_date>
  <status>staged</status><!-- STAGED: gates on ADHC_OWNPTH.003 (AE hook wiring + Phase 1 live) completion -->

  <title>ADHC_OWNPTH TO 4 — COO Phase 1 observation week + go/no-go report</title>

  <references>
    <ref type="prd">docs/architecture/ADHC_OWNPTH.md</ref>
    <ref type="audit">org/git-author-override-audit.log (primary observation surface)</ref>
  </references>

  <context>
    Phase 1 begins when TO 3 (AE hook wiring) completes. The hook runs in warn-mode
    (OWNED_PATHS_MODE=warn or unset) for 7 days. Every commit by every agent triggers the
    hook; violations log WARN to org/git-author-override-audit.log; legitimate commits log
    PASS. COO monitors daily, classifies all WARN entries, and produces a Phase-1-Observation-
    Report at day 7 with go/no-go recommendation for Phase 2 flip (fail-closed).

    The observation window also surfaces any YAML gaps: paths not covered → UNDEFINED entries
    that need YAML diffs before Phase 2. COO routes YAML diff requests to CTO.
  </context>

  <scope>
    1. DAILY (for 7 days from Phase 1 start):
       - `wc -l org/git-author-override-audit.log` — record count
       - `diff` vs prior day — surface new entries
       - Classify each new WARN entry into:
           (a) YAML adjustment needed (rule too tight / path not covered)
           (b) Legitimate cross-lane commit (document --author-override pattern)
           (c) Real violation (root-cause + memory/incident entry)
       - Log classification in COO session log (minimum 1 line per day)
       - Route (a) → CTO with YAML diff request; route (c) → Andrew if pattern repeats

    2. At DAY 7:
       - Produce `docs/architecture/ADHC_OWNPTH_phase1_observation_report.md`:
           - Total commit count during observation window (PASS + WARN + OVERRIDE counts)
           - WARN classification breakdown (a/b/c) with resolved/unresolved counts
           - YAML diff recommendations (for (a) class WARNs)
           - --author-override pattern documentation (for (b) class)
           - Any real violations (c) + resolutions
           - Explicit go/no-go recommendation: GO if zero unresolved WARNs + zero
             unresolved true-positives; CONDITIONAL GO if YAML diffs needed (describe);
             NO-GO if Phase 1 surfaced systemic YAML coverage gaps or false-positive risk
       - Commit report under 2.0.0_SA_COO author.

    3. On GO signal from Andrew or CTO:
       - MCP CTO with go-signal + link to report (cites commit hash of report)
       - CTO executes TO 5 (Phase 2 flip)

    Do NOT flip OWNED_PATHS_MODE (TO 5 scope).
    Do NOT modify hook script or YAML during observation without CTO coordination.
  </scope>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="ADHC_OWNPTH.003" status="staged"
                required="Phase 1 must be live (hook wired + audit log bootstrapped) before observation begins."/>
  </dependencies>

  <compiler_tools_mandate>
    <phase id="1" when="daily (7 days)">
      <step>
        <run>wc -l org/git-author-override-audit.log</run>
        <expect>Line count increases daily (hook is running). If count stagnant for 24h during heavy commit periods, investigate hook installation on agent worktrees.</expect>
        <if_mismatch>NOTE: hook may not be wired on some agent worktrees. Broadcast install-owned-paths.sh reminder.</if_mismatch>
      </step>
      <step>
        <run>tail -N org/git-author-override-audit.log (N = new lines since prior check)</run>
        <expect>New PASS / WARN / OVERRIDE entries. Classify each WARN. Document in COO session log.</expect>
        <if_mismatch>N/A — manual classification is the step output.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="day 7 — before report commit">
      <step>
        <run>awk '{print $2}' org/git-author-override-audit.log | sort | uniq -c</run>
        <expect>Count breakdown: PASS=N, WARN=M, BLOCK=0 (Phase 1 never blocks), OVERRIDE=K, BOOTSTRAP=1. Document in report.</expect>
        <if_mismatch>N/A — used for report statistics.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after report commit">
      <step>
        <run>git log --oneline -3 -- docs/architecture/ADHC_OWNPTH_phase1_observation_report.md</run>
        <expect>Report commit appears with 2.0.0_SA_COO author. Confirms committed before MCP CTO go-signal.</expect>
        <if_mismatch>STOP. Commit report before sending go-signal to CTO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    1. Daily audit log scans logged in COO session logs for all 7 days (minimum 1 line per day).
    2. All WARN entries during observation window classified — zero dangling unresolved.
    3. YAML diffs routed to CTO for (a) class WARNs; real violations (c) documented in incident memory.
    4. `docs/architecture/ADHC_OWNPTH_phase1_observation_report.md` produced on day 7;
       committed under 2.0.0_SA_COO author.
    5. Report contains: PASS/WARN/OVERRIDE counts, WARN classification breakdown,
       YAML diff recommendations, go/no-go recommendation with cited evidence.
    6. Go-signal MCP to CTO includes commit hash of report.
    7. TO 5 fires only after Andrew or CTO confirms go-signal.
  </acceptance_criteria>

  <evidence>
    <!-- To be filled by COO on completion (day 7 report) -->
  </evidence>
</task_order>
