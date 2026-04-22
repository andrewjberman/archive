<task_order>
  <metadata>
    <id>1.2.0_DS_CompLearns-2026-04-22-comp-learns-052-dev-stress-dev-1-dev-2</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.2.0_DS_CompLearns</issued_to>
    <date>2026-04-22</date>
    <status>pending <!-- GO'd on dispatch per Wave 3 PRD 30971db1 --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P2 — Wave 3 background apparatus-stress monitor; NON-BLOCKING to main lanes</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_WAVE3_V1.md §5 (background apparatus stress) + §6 step 4 — commit 30971db1</ref>
    <ref type="backlog">comp/backlog/dev/dev-httpx-001.yaml (dev-1: selector_ceiling, 3-hop import chain)</ref>
    <ref type="backlog">comp/backlog/dev/dev-httpx-002.yaml (dev-2: ABCache cache_identity near-collision)</ref>
  </references>

  <objective>
    Run dev-1 + dev-2 as Wave 3 integrity monitors. These are apparatus-stress cases
    (Archetype E per §5) — they DETECT rather than GATE. Main lanes (.048 dev-4 +
    .049/.050 Case 3) DO NOT block on your results unless you detect cache-identity
    corruption or comparability corruption.

    Explicitly in scope:

    ## dev-1 — selector_ceiling stress (3-hop import chain)

    1. Resolve baseline_commit for dev-httpx-001.yaml if blank (§9 rule 7). If blank,
       pin to a recent httpx commit that exhibits the 3-hop chain; record pin authority.

    2. Run the selector against the 3-hop chain. Document:
       - Where does the selector truncate (if it does)?
       - What edge types are reached / missed?
       - Does the expected 3-hop path surface in selector output?

    3. Write `comp/results/dev-stress/dev-1-selector-ceiling.md` with:
       - Configuration used (selector depth, edge-type filter, etc.)
       - Observed truncation point (or NO_TRUNCATION if clean)
       - Coverage-gap list (edges missed)
       - Finding classification: ordinary coverage gap | comparability corruption | cache-identity issue | no finding

    4. Action matrix per §5:
       - Ordinary coverage gap → log + note in main file + main lanes continue
       - Cache-identity near-collision confirmed → STOP-THE-LINE + MCP CTO + do NOT proceed
       - Comparability corruption → STOP-THE-LINE + MCP CTO
       - No finding → no action beyond recording

    ## dev-2 — ABCache cache_identity near-collision

    5. Similar to dev-1 but targeting ABCache key-space near-collisions per dev-httpx-002
       scenario. If baseline_commit blank, pin.

    6. Execute the near-collision probe. Document at
       `comp/results/dev-stress/dev-2-cache-identity.md`:
       - Cache key construction tested
       - Whether near-collision occurred + whether identity held
       - Classification + action per matrix

    ## Non-blocking rule

    7. Your runs do NOT gate main lanes. If you find:
       - Nothing → silent pass, log, done
       - Ordinary coverage gap → informational; flag in session log + MCP COO as heads-up
       - Cache-identity OR comparability corruption → STOP-THE-LINE per §5 table; immediate
         MCP to CTO + COO; do NOT dispatch further main lane work until resolved

    Explicitly out of scope:
    - Fixing any gap you find — document + classify only. Fixes are separate TOs.
    - Running dev-3 or dev-4 (dev-4 is .048, dev-3 is not in Wave 3).
    - Re-tuning the compiler during the stress run.
    - SC involvement (dev-stress has no formal scoring per §5).

    If you need to pin a baseline_commit, you may do it inline under
    --author=1.2.0_DS_CompLearns --only pathspec on the dev-*.yaml file. Document the
    pin authority in a notes line on the YAML.
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-build && pytest comp/ -q</run>
        <expect>Baseline clean (9 pre-existing reds accepted).</expect>
        <if_mismatch>Rebase / fix.</if_mismatch>
      </step>
      <step>
        <run>cat comp/backlog/dev/dev-httpx-001.yaml comp/backlog/dev/dev-httpx-002.yaml | grep baseline_commit</run>
        <expect>Both pinned OR you resolve inline per §9 rule 7.</expect>
        <if_mismatch>If blank, Phase 0 = pin both before running stress.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>ls comp/results/dev-stress/</run>
        <expect>dev-1-selector-ceiling.md + dev-2-cache-identity.md both present.</expect>
        <if_mismatch>Author missing before commit.</if_mismatch>
      </step>
      <step>
        <run>grep -E "Classification: (ordinary|cache-identity|comparability|no finding)" comp/results/dev-stress/*.md</run>
        <expect>Both files have an explicit classification line.</expect>
        <if_mismatch>Add classification per §5 action matrix.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/ -q</run>
        <expect>No new reds.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-build</run>
        <expect>Clean rebuild.</expect>
        <if_mismatch>Surface to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>NON-BLOCKING to .048/.049/.050/.051. You only block on CACHE-IDENTITY or COMPARABILITY findings (stop-the-line trigger per §5). Ordinary coverage gaps are informational. Parallel run with all other Wave 3 TOs.</note>
    <shared_artifacts>comp/results/dev-stress/** (created by this TO); comp/backlog/dev/dev-httpx-001.yaml + dev-httpx-002.yaml (may get inline baseline pins)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. dev-1 stress run executed + documented at comp/results/dev-stress/dev-1-selector-ceiling.md.
    2. dev-2 stress run executed + documented at comp/results/dev-stress/dev-2-cache-identity.md.
    3. Both files have an explicit finding classification per §5 action matrix.
    4. If cache-identity OR comparability corruption detected: STOP-THE-LINE MCP sent to CTO + COO before main lanes continue.
    5. Baseline_commits pinned on dev-httpx-001 + dev-httpx-002 YAMLs if blank at start.
    6. Commit --only --author=1.2.0_DS_CompLearns pathspec scoped to comp/results/dev-stress/** and comp/backlog/dev/dev-httpx-*.yaml (if pinned).
    7. Pushed to CLOUD.
    8. Session log with Compiler Tools section.
    9. MCP COMPLETE to 2.1.0_SA_COO with classification summary (dev-1: X | dev-2: Y) + any informational flags.
  </acceptance_criteria>

  <dependencies>
    - Gate: Wave 3 PRD 30971db1 (locked). GO on dispatch.
    - Parallel / non-blocking: all other Wave 3 TOs.
    - Blocks: NOTHING (unless STOP-THE-LINE fires).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - Priority P2 — take at your own cadence; no hard deadline. Main lanes run in parallel.
    - You have NO other Wave 3 TO — this is your Wave 3 assignment.
    - If you find cache-identity or comparability issues, that's actually the whole POINT of
      apparatus-stress cases. STOP-THE-LINE is the correct response, not a failure.
    - Finding classification vocabulary is exact per §5: "ordinary coverage gap" | "cache-identity" | "comparability" | "no finding". Use these exact phrases.
    - No emojis.
  </operational_notes>

  <closeout>
    On completion:
    - commit --only --author="1.2.0_DS_CompLearns &lt;1.2.0_DS_CompLearns@opal.agent&gt;" -- comp/results/dev-stress/** comp/backlog/dev/dev-httpx-*.yaml
    - push to CLOUD
    - flip TO status to complete with commit ref + classifications
    - MCP COMPLETE to 2.1.0_SA_COO with classification summary
    - session log with Compiler Tools section
  </closeout>
</task_order>
