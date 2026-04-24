<task_order>
  <metadata>
    <id>1.1.0_DS_CompLearns-2026-04-24-comp-learns-060-lane-a-rebuild</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.1.0_DS_CompLearns</issued_to>
    <date>2026-04-24</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Wave 3b Lane A rebuild; first valid dev-loop measurement run</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_WAVE3_V1.md §2.0 (preconditions, rev5) + §2.1-§2.7 — commit bd84ef10</ref>
    <ref type="integrity_finding">comp/results/dev-4/integrity_invalidation.md (df168552) — three findings that froze Lane A; §2.0 closes all three</ref>
    <ref type="cto_decision">org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.WAVE3B-DECISION.md §1 — dev-4 loop mechanics FIT; measurement pipeline UNFIT; rebuild authorized with §2.0 preconditions</ref>
    <ref type="budget_fix">.061 (1.2.0_DS budget fix) — should ship before this TO begins its loop run</ref>
    <ref type="scorer">2.1.0_SC_CompLearns — bundle scorer for this lane; scorer serial != compiler mutation author (you)</ref>
  </references>

  <objective>
    Execute the first VALID Lane A dev-loop run on click, satisfying all §2.0 preconditions.
    This is the loop-proving engine case: prove `comp-dev-loop.py` can climb against a hard
    quantitative target when measurement is honest.

    Context: .048 was invalidated due to (1) self-scored bundle, (2) no canonical click source,
    (3) budget off-by-one. All three are closed by this TO's protocol.

    ## Phase 0 — Preconditions (MANDATORY, hard gates)

    ### P0.1 — Canonical source provisioning (§2.0 Precondition 1)

    Provision click at f80cf4b0 in comp/targets/click/_repo/ if not present:
    ```bash
    git clone https://github.com/pallets/click comp/targets/click/_repo
    git -C comp/targets/click/_repo checkout f80cf4b09fbe36099b7bfc065fbde30d053da46d
    ```
    If _repo/ exists: verify HEAD:
    ```bash
    git -C comp/targets/click/_repo rev-parse HEAD | grep -q "^f80cf4b0" || { echo "HEAD MISMATCH"; exit 2; }
    ```

    Run §0.6 clean-state check on _repo/:
    ```bash
    git -C comp/targets/click/_repo diff --quiet || { echo "DIRTY"; exit 2; }
    git -C comp/targets/click/_repo diff --cached --quiet || { echo "STAGED"; exit 2; }
    [ -z "$(git -C comp/targets/click/_repo status --porcelain)" ] || { echo "UNTRACKED"; exit 2; }
    echo "CLEAN"
    ```
    Any fail = STOP. MCP COO.

    ### P0.2 — Packet scorer field backfill (§2.0 Precondition 4)

    dev-click-001.yaml predates rev5 and lacks the scorer field. Backfill it now.
    Read comp/backlog/dev/dev-click-001.yaml. Add under the existing fields:
    ```yaml
    scorer:
      serial: 2.1.0_SC_CompLearns
      mode: scorer_agent
      artifact_location: comp/dev-bundles/dev-click-001/
    ```
    Commit this backfill BEFORE any loop iteration:
    ```bash
    git commit --only --author="1.1.0_DS_CompLearns <1.1.0_DS_CompLearns@opal.agent>" \
      -m "feat(COMP_LEARNS.060): backfill dev-click-001.yaml scorer field per PRD §2.0 P4" \
      -- comp/backlog/dev/dev-click-001.yaml
    ```
    This commit is the §0.6 gate evidence for scorer-field presence.

    ### P0.3 — No stale dev bundles (§0.6 item 4)

    Clear any stale bundles from the invalidated .048 run:
    ```bash
    rm -rf comp/dev-bundles/dev-click-001/
    mkdir -p comp/dev-bundles/dev-click-001/
    ```
    comp/dev-bundles/ should NOT be committed — it is the runtime bundle drop zone, not a
    tracked artifact. If git tracks it, add to .gitignore (check first).

    ### P0.4 — Cold-run baseline measurement + target proposal

    4. Run cold measurement of click at f80cf4b0 (before any mutations):
       - Use `comp-learns-ratchet --once` or equivalent against comp/targets/click/ with
         the canonical source at _repo/. DO NOT use temp trees.
       - Record baseline_primary_metric in the target_metric block of dev-click-001.yaml.

    5. Propose target using the compound rule (§2.2):
       ```
       target >= baseline + max(baseline * 0.15, absolute_floor)
       ```
       Propose a specific absolute_floor based on your understanding of primary_metric units
       on the click task (from .017 experience on httpx).

    6. MCP COO AND CTO with:
       - baseline_primary_metric value
       - proposed target_primary_metric
       - proposed relative_gain_applied + absolute_floor_applied
       - Requested budget-hours: 6-8 per CTO Wave 3b decision §1

       **HARD GATE: DO NOT START ITERATION 1 UNTIL MCP ACK FROM COO OR CTO.**
       Record the approved target in dev-click-001.yaml target_metric block before starting.

    ## Phase 1 — Loop execution (manual-iteration mode)

    Due to §2.0 scorer-author separation, the loop runs in manual-iteration mode.
    You CANNOT self-author the bundle (that is Finding 1 from .048). Protocol per iteration:

    a. Write and commit a compiler mutation to comp/targets/click/compiler.py:
       ```bash
       git commit --only --author="1.1.0_DS_CompLearns <1.1.0_DS_CompLearns@opal.agent>" \
         -m "feat(COMP_LEARNS.060): click compiler mutation N -- <family>/<slug>" \
         -- comp/targets/click/compiler.py
       ```
       Record: mutation_family, intervention_slug, compiler_sha (the commit sha).

    b. MCP 2.1.0_SC_CompLearns with:
       - compiler_sha: <commit sha of your mutation>
       - task_id: dev-click-001
       - canonical_source: comp/targets/click/_repo/ at f80cf4b0
       - artifact_location: comp/dev-bundles/dev-click-001/iter-N/
       Request: "Please evaluate click compiler mutation <sha> and place result.json at
       artifact_location with scored_by: 2.1.0_SC_CompLearns."

    c. Wait for SC to MCP back with bundle placed confirmation. Do NOT proceed until SC
       confirms. SC evaluates the mutation against the canonical click source and places:
       ```json
       {
         "primary_metric": <float>,
         "scored_by": "2.1.0_SC_CompLearns",
         "compiler_sha": "<your mutation sha>",
         "evaluation_notes": "<SC neutral notes>"
       }
       ```
       at comp/dev-bundles/dev-click-001/iter-N/result.json.

    d. Run ONE loop iteration:
       ```bash
       python comp/bin/comp-dev-loop.py \
         --target dev-click-001 \
         --budget-hours 0.01 \
         --judge real \
         --burst-n 1 \
         --single-iter
       ```
       (Or equivalent manual invocation that consumes the pre-placed bundle and updates
       champion state. Check comp-dev-loop.py --help for available flags.)
       If --single-iter is not available, adapt: the loop must consume the bundle at
       artifact_location and update champion.json. MCP COO if loop invocation unclear.

    e. Record in experiment_log.jsonl:
       ```json
       {"iteration": N, "mutation_family": "<family>", "intervention_slug": "<slug>",
        "compiler_sha": "<sha>", "primary_metric": <float>, "delta": <vs prior>,
        "kept": <bool>, "scored_by": "2.1.0_SC_CompLearns"}
       ```

    f. Per §2.3 stop conditions (check after each iteration):
       1. Target hit (primary_metric >= target) + confirmed by 2 reruns → STOP (see §2.6)
       2. Budget exhausted (wall-clock or CTO/COO manual stop) → STOP
       3. Real plateau (3 consecutive non-KEEP burst barriers) → plateau analysis required
       4. Manual stop (CTO/COO directive) → STOP

       For this first valid run, budget is measured in real time (6-8h per CTO directive).
       Given manual-iteration overhead, aim for 3-5 substantive iterations before budget.

    7. Mutation families to try first (per CTO Wave 3b decision §1):
       - edge_generation (depth-2 variant): add second-hop edges from core.py group nodes
       - cross_module_hint_injection: inject cross-file call edges from decorators.py → core.py
       - selector_depth_increase: increase graph traversal depth for the click dispatch subsystem

    ## Phase 2 — Expected outputs

    8. All artifacts at comp/results/dev-5/ (NOT dev-4 — that directory contains the
       invalidated run artifacts which are preserved as evidence per integrity_invalidation.md):
       - experiment_log.jsonl (per-iteration records with scored_by field per each entry)
       - champion_history.json (ordered champion progression)
       - mutation_family_summary.md (which families moved metric; winning-mechanism analysis)
       - plateau_analysis.md (if plateau occurred)
       - loop_fitness_recommendation.md (is loop ready for automated expansion? what settings carry forward?)
       - result.json (final state per §2.7)

    9. dev-click-001.yaml target_metric block (committed in Phase 0 with approval_mcp_ref).

    Explicitly out of scope:
    - Self-authoring any bundle (scorer is SC, not you)
    - Using temp trees for measurement (must use _repo/ at f80cf4b0)
    - Starting iteration 1 before COO/CTO target approval MCP ACK
    - Touching Case 3 or Case 1/2 measurement work
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before Phase 0 starts">
      <step>
        <run>comp-build &amp;&amp; pytest comp/ -q 2>&amp;1 | tail -5</run>
        <expect>comp-build clean; at most 9 pre-existing reds. Note baseline count.</expect>
        <if_mismatch>Surface to COO before starting.</if_mismatch>
      </step>
      <step>
        <run>python comp/bin/comp-dev-loop.py --help</run>
        <expect>Help prints; confirms .044 shipped and loop is operational.</expect>
        <if_mismatch>STOP. Loop prerequisite missing. MCP COO.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before each mutation commit">
      <step>
        <run>.tools/ds-commit-gate.sh comp/targets/click/compiler.py</run>
        <expect>Exit 0</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>python -m py_compile comp/targets/click/compiler.py</run>
        <expect>Exit 0</expect>
        <if_mismatch>Fix syntax before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after Phase 0 target approval, before iteration 1">
      <step>
        <run>cat comp/backlog/dev/dev-click-001.yaml | grep -A8 "target_metric:"</run>
        <expect>target_metric block populated with baseline_primary_metric, target_primary_metric, relative_gain_applied, absolute_floor_applied, approval_authority, approval_mcp_ref, confirmation_runs_required: 2, tied_rerun_counts: true</expect>
        <if_mismatch>STOP. Commit target_metric block before iteration 1 (immutable record per §2.2).</if_mismatch>
      </step>
      <step>
        <run>cat comp/backlog/dev/dev-click-001.yaml | grep -A3 "scorer:"</run>
        <expect>scorer: serial: 2.1.0_SC_CompLearns (backfill committed)</expect>
        <if_mismatch>STOP. Backfill and commit scorer field first.</if_mismatch>
      </step>
      <step>
        <run>git -C comp/targets/click/_repo rev-parse HEAD | head -c 8</run>
        <expect>f80cf4b0</expect>
        <if_mismatch>Reset _repo/ to baseline before starting.</if_mismatch>
      </step>
    </phase>
    <phase id="4" when="after loop run completes">
      <step>
        <run>ls comp/results/dev-5/</run>
        <expect>All §2.7 artifacts present (experiment_log.jsonl, champion_history.json, mutation_family_summary.md, loop_fitness_recommendation.md, result.json; plateau_analysis.md if plateau occurred)</expect>
        <if_mismatch>Author missing artifacts before closing TO.</if_mismatch>
      </step>
      <step>
        <run>python -c "import json; log=[json.loads(l) for l in open('comp/results/dev-5/experiment_log.jsonl')]; assert all('scored_by' in e for e in log); print(f'All {len(log)} entries have scored_by')"</run>
        <expect>All entries have scored_by field (scorer-author separation evidence)</expect>
        <if_mismatch>Amend experiment_log.jsonl to include scored_by on all entries before committing.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>Scorer is 2.1.0_SC_CompLearns — you MUST MCP SC for each bundle evaluation. SC evaluates mutations independently; you may not author or modify result.json. Loop will likely span multiple sessions due to manual-iteration protocol. Between sessions: preserve champion.json state; SC must be available for re-engagement. .061 (budget fix) should ship before this TO runs its first iteration. Non-contamination rule §4: dev-5 results inform Wave 4 but must NOT be applied to Case 1/2 (wave-3b) measurement mid-flight.</note>
    <shared_artifacts>comp/targets/click/_repo/ (shared with .056/.057 but those run sequentially in Lane B; COO will coordinate timing); comp/backlog/dev/dev-click-001.yaml (written by this TO; read-only to others)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. §0.6 clean state verified at _repo/ before iteration 1 (paste evidence in ACK MCP).
    2. scorer field backfilled in dev-click-001.yaml and committed before iteration 1.
    3. target_metric block in dev-click-001.yaml with CTO/COO-approved values and approval_mcp_ref committed before iteration 1.
    4. All bundles authored by 2.1.0_SC_CompLearns (scored_by field in every result.json).
    5. Loop terminated on a §2.3 stop condition; result.json has stop_reason.
    6. experiment_log.jsonl has scored_by field on every entry.
    7. All §2.7 artifacts present at comp/results/dev-5/.
    8. loop_fitness_recommendation.md explicitly answers: "Is the current loop ready for parallel expansion? What settings should carry forward?"
    9. Commits --only --author="1.1.0_DS_CompLearns" for compiler mutations + results.
    10. Pushed to CLOUD.
    11. Session log(s) with Compiler Tools section + Phase 0 approval MCP reference.
    12. MCP COMPLETE to 2.1.0_SA_COO with: stop_reason + final champion primary_metric + mutation-family winners + target hit Y/N.
  </acceptance_criteria>

  <dependencies>
    - Gate: .061 (budget off-by-one fix) should land before iteration 1 begins. Not a hard stop if delayed — note in session log that fix was pending at run time.
    - Hard gate: COO/CTO MCP approval of target before iteration 1 (Phase 0 step 6).
    - Parallel (non-blocking): .054/.055/.056/.057 (Lane B — different lane, different agents).
    - Blocks: Wave 3b closure (this is the Lane A contribution to Stage 2 wave count).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - Manual-iteration mode is the design for this first valid run. Each iteration requires
      SC to evaluate the mutation independently. Expect 3-5 iterations in a 6-8h budget.
    - If SC is unavailable (mid-session), MCP COO. Do not self-author the bundle under any
      circumstances — that is Finding 1 from .048 and terminates the run's validity.
    - comp/results/dev-5/ is the measurement directory. Do NOT write to dev-4/ (preserved evidence).
    - No emojis in any artifact.
  </operational_notes>

  <closeout>
    On completion (regardless of stop reason):
    - commit --only --author="1.1.0_DS_CompLearns &lt;1.1.0_DS_CompLearns@opal.agent&gt;" -- comp/results/dev-5/** comp/backlog/dev/dev-click-001.yaml
    - push to CLOUD
    - flip TO status complete with stop_reason + target hit/not-hit + commit sha
    - MCP COMPLETE to 2.1.0_SA_COO
    - session log(s) covering full run with Compiler Tools section + Phase 0 approval MCP reference
  </closeout>
</task_order>
