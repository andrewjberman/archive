<task_order>
  <metadata>
    <id>1.1.0_DS_CompLearns-2026-04-22-comp-learns-048-dev-4-loop-proving</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.1.0_DS_CompLearns</issued_to>
    <date>2026-04-22</date>
    <status>complete <!-- mechanics verified; measurement invalidated — see comp/results/dev-4/integrity_invalidation.md; CTO adjudication 20260422T204400Z Option C; Lane A frozen pending PRD amendment --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Wave 3 Lane A (loop-proving engine case); answers "can the compiler-improvement loop climb against a hard quantitative target?"</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_WAVE3_V1.md §2 (dev-4 lane) + §4 (non-substitution rule) + §6 (sequence) + §8 (TO decomposition) + §10 (success criteria) — commit b8f1beb5</ref>
    <ref type="backlog">comp/backlog/dev/dev-click-001.yaml — Archetype B, target pallets/click at baseline f80cf4b0</ref>
    <ref type="prerequisite_shipped">comp/bin/comp-dev-loop.py (0d0dec04, your prior ship in .044) — the runner this TO exercises</ref>
    <ref type="prerequisite_shipped">comp/bin/comp-preflight.py (f6f29836) — called per iteration in dev mode</ref>
    <ref type="target_harness">comp/targets/click/ (present, your earlier .036 work)</ref>
  </references>

  <objective>
    Execute dev-4 as the loop-proving engine case for Wave 3 Lane A. Produce a full
    champion-progression record + mutation-family analysis + loop-fitness recommendation
    against a CTO/COO-approved hard target. This is NOT the formal measurement lane;
    do not conflate with Case 3 aided-vs-unaided work.

    Explicitly in scope:

    ## Phase 0 — Baseline cold-run + target proposal (BEFORE any loop iteration)

    1. Verify dev-click-001.yaml in comp/backlog/dev/ — confirm baseline_commit is pinned
       to f80cf4b0. If blank, STOP and MCP COO (§9 rule 7 hard gate).

    2. Cold-run measurement against click 8.3.1 (baseline_commit f80cf4b0):
       - Run `comp-learns-ratchet --once` OR equivalent to produce champion.json with
         baseline `primary_metric`
       - Record baseline_primary_metric value
       - Do NOT start `comp-dev-loop.py` iteration yet

    3. Propose target using the compound rule per §2.2:
       ```
       target >= baseline + max(relative_gain, absolute_floor)
       where relative_gain = baseline * 0.15
             absolute_floor = <you propose; CTO/COO sets final at approval>
       ```
       Propose a specific absolute_floor based on your knowledge of primary_metric units
       on the click task (from .017 proving experience).

    4. MCP CTO + COO with:
       - baseline_primary_metric value
       - proposed target_primary_metric value
       - proposed relative_gain_applied + absolute_floor_applied
       - requested approval_authority (CTO or COO)

    5. **HARD GATE: DO NOT START ITERATION 1 UNTIL MCP ACK FROM CTO OR COO.** §2.2 is
       explicit — this is a hard gate, not a recommendation. Write the approved target +
       approval_mcp_ref into dev-click-001.yaml under `target_metric:` block before
       starting the loop. This record is IMMUTABLE for the duration of the Wave 3 loop run.

    ## Phase 1 — Loop execution

    6. Launch `comp-dev-loop.py`:
       ```
       python comp/bin/comp-dev-loop.py \
         --target dev-click-001 \
         --budget-hours {N} \
         --judge real \
         --burst-n 3 \
         --plateau-n 3    # per §2.4 recommended
       ```
       Budget-hours: propose in target-approval MCP (suggest 2-4 hours for first dev-4 run).

    7. Per-iteration mutation tracking (§2.5) — every iteration must emit:
       - `mutation_family`: class of change (e.g. import_graph_expansion,
         selector_depth_increase, edge_weight_adjustment, cross_module_hint_injection)
       - `intervention_slug`: short label for the specific mutation
       - `primary_metric_delta`: improvement vs prior champion
       - `kept`: bool

       These feed `experiment_log.jsonl` per §12 schema + mutation_family_summary.md.

    8. Stop conditions per §2.3 (priority order):
       1. Target hit + confirmed (2 confirmation runs per §2.6; TIED at new level counts)
       2. Integrity failure (cache-identity or comparability corruption → escalate CTO)
       3. Budget exhausted
       4. Real plateau (3 consecutive burst barriers without KEEP + diagnostic run)
       5. Manual stop (CTO / Andrew redirect)

       On ANY stop: write result.json with final champion + stop_reason + mutation-family summary.

    9. Plateau handling per §2.4:
       - Run REQUIRED diagnostics before strategy change (which families exercised, partial
         movement signals, baseline drift check, target feasibility check)
       - Decision tree per §2.4; MCP COO with plateau_analysis.md snapshot

    10. Reproduction / confirmation per §2.6:
        - One KEEP at target level = PROVISIONAL
        - Confirmation: 2 fresh-session independent reruns (same baseline_commit + task)
          that produce primary_metric >= target (TIED counts)
        - On confirmation: tag the winning commit (e.g. `comp-learns-dev4-v1`) + note
          confirmation run evidence in result.json

    ## Phase 2 — Expected outputs (§2.7)

    11. All of the following MUST be produced in comp/results/dev-4/:
        - `experiment_log.jsonl` (per-iteration mutation records)
        - `champion_history.json` (ordered champion progression with metric values + SHAs)
        - `mutation_family_summary.md` (which families moved the metric; winning mechanism analysis)
        - `plateau_analysis.md` (if plateau occurred: diagnostics + decision + rationale)
        - `loop_fitness_recommendation.md` (is the current loop ready for parallel expansion? What settings carry forward? — primary handoff artifact for Wave 4 per §2.7)
        - `result.json` (machine-readable final state per §4 micro-cycle contract)

    12. All artifacts committed with --only pathspec scoped to comp/results/dev-4/** and
        comp/backlog/dev/dev-click-001.yaml (for target-metric block update).

    Explicitly out of scope:
    - Case 3 / sphinx aided-vs-unaided measurement (that is .049 + .050 + .051).
    - Wave 3b scope (Cases 1+2 rerun under Stage 2).
    - Mid-flight compiler changes applied to Case 3 — §4 non-contamination rule:
      dev-4 results may inform Wave 4 but must NOT be applied to Case 3 condition_a
      during Case 3 execution.
    - Running the loop without CTO/COO target approval — Phase 0 hard gate.
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write (Phase 0 + Phase 1 start)">
      <step>
        <run>comp-build && pytest comp/ -q</run>
        <expect>Clean baseline. 9 pre-existing reds accepted; no new.</expect>
        <if_mismatch>Rebase or fix before starting.</if_mismatch>
      </step>
      <step>
        <run>cat comp/backlog/dev/dev-click-001.yaml | grep baseline_commit</run>
        <expect>baseline_commit: f80cf4b0... (non-blank, real SHA)</expect>
        <if_mismatch>STOP. §9 rule 7 hard gate. MCP COO; do not start loop.</if_mismatch>
      </step>
      <step>
        <run>python comp/bin/comp-dev-loop.py --help</run>
        <expect>CLI help printing; confirms .044 shipped and ready.</expect>
        <if_mismatch>STOP. MCP COO — dev-loop prerequisite missing.</if_mismatch>
      </step>
      <step>
        <run>ls comp/targets/click/</run>
        <expect>compiler.py + repo_pin.txt + gold/ present (from .036).</expect>
        <if_mismatch>STOP. MCP COO — click harness missing.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before each commit">
      <step>
        <run>python -m py_compile comp/bin/comp-dev-loop.py</run>
        <expect>Exit 0 (your own tool, sanity check).</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh {any python files touched}</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/ -q</run>
        <expect>No NEW reds vs 9 pre-existing baseline.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after target approval, before loop iter 1">
      <step>
        <run>cat comp/backlog/dev/dev-click-001.yaml | grep -A6 "target_metric:"</run>
        <expect>target_metric block populated with baseline_primary_metric, target_primary_metric, relative_gain_applied, absolute_floor_applied, approval_authority, approval_mcp_ref, confirmation_runs_required: 2, tied_rerun_counts: true.</expect>
        <if_mismatch>STOP. Target-metric block is required IMMUTABLE record per §2.2. Commit before loop.</if_mismatch>
      </step>
    </phase>
    <phase id="4" when="after loop completion">
      <step>
        <run>ls comp/results/dev-4/</run>
        <expect>All 6 artifacts per §2.7 present.</expect>
        <if_mismatch>Author missing artifacts before closing TO.</if_mismatch>
      </step>
      <step>
        <run>comp-build</run>
        <expect>Clean rebuild post-commit.</expect>
        <if_mismatch>Surface to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>Non-substitution rule (§4): a dev-4 result does not substitute for Case 3 evidence. Non-contamination rule: dev-4 compiler changes must NOT be applied to Case 3 condition_a during Case 3 execution. .049 (1.3.0_DS Case 3 aided) is running in parallel; do NOT coordinate mid-flight compiler mutations with them. Only after both .048 + .051 complete does .053 review propagate dev-4 learnings forward.</note>
    <shared_artifacts>comp/backlog/dev/dev-click-001.yaml (written by this TO target-metric block; read-only to others); comp/results/dev-4/** (created by this TO)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Phase 0: baseline cold-run measurement recorded in dev-click-001.yaml.
    2. Phase 0: target proposed via MCP to CTO + COO; CTO or COO ACK received; approval_mcp_ref recorded in dev-click-001.yaml.
    3. Phase 0: target_metric block IMMUTABLE-committed before loop iteration 1 (per §2.2).
    4. Phase 1: comp-dev-loop.py executed with CTO/COO-approved target; mutation-family tracking per §2.5 in experiment_log.jsonl.
    5. Phase 1: loop terminates on one of the §2.3 stop conditions; result.json has stop_reason + final champion.
    6. Phase 1 (if KEEP achieved): confirmation runs executed per §2.6; 2 fresh-session reruns at target level; winning commit tagged.
    7. Phase 1 (if plateau): plateau_analysis.md authored with §2.4 required diagnostics before decision.
    8. Phase 2: all 6 artifacts in comp/results/dev-4/ per §2.7 (experiment_log.jsonl, champion_history.json, mutation_family_summary.md, plateau_analysis.md if applicable, loop_fitness_recommendation.md, result.json).
    9. loop_fitness_recommendation.md explicitly answers: "Is the current loop ready for parallel expansion? What settings should carry forward?" (primary Wave 4 handoff).
    10. All commits --only --author=1.1.0_DS_CompLearns; pushed to CLOUD.
    11. Session log at org/tier2_senior/1.1.0_DS_CompLearns/logs/2026-04-22/ (or actual date) with Compiler Tools section + target approval MCP reference.
    12. MCP COMPLETE to 2.1.0_SA_COO with commit shas + stop_reason + champion metric + mutation-family winners.
  </acceptance_criteria>

  <dependencies>
    - Gate: Wave 3 PRD b8f1beb5 (locked). GO'd on dispatch.
    - Hard gate: CTO or COO MCP approval of target before iteration 1 (Phase 0 step 5).
    - Parallel (non-blocking): .049 (Case 3 aided by 1.3.0), .052 (bg stress by 1.2.0). Do NOT coordinate compiler mutations with .049 mid-flight (non-contamination rule §4).
    - Blocks: .053 joint review (.053 gates on .048 + .051 complete).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - Phase 0 is a hard sequence — do not start loop until MCP ACK on target.
    - If target is rejected or adjusted by CTO/COO in the approval MCP, use the approved
      value (not your proposed one); record approval_authority accordingly.
    - Mutation-family taxonomy is open — the PRD §2.5 examples are illustrative. If your
      loop invents a family not in the example set, tag it with a new family name; the
      mutation_family_summary.md must still group by family for the winning-mechanism
      analysis.
    - Plateau is defined by burst barriers (§2.4), NOT raw iteration count. Multiple
      DISCARDs within a single burst are expected and do not constitute plateau.
    - Confirmation runs (§2.6) are fresh DS sessions — you must actually restart, not
      re-use session state. Document fresh-session evidence in result.json.
    - No emojis anywhere.
    - Budget-hours suggestion: start with 2-4 hours for first dev-4 run; if you learn a
      different budget is appropriate after Phase 0, request adjustment in approval MCP.
  </operational_notes>

  <closeout>
    On completion (regardless of stop reason):
    - commit --only --author="1.1.0_DS_CompLearns &lt;1.1.0_DS_CompLearns@opal.agent&gt;" -- comp/results/dev-4/** comp/backlog/dev/dev-click-001.yaml
    - push to CLOUD
    - flip TO status to complete with commit ref + stop_reason + target hit/not-hit
    - MCP COMPLETE to 2.1.0_SA_COO — this is the .053 gate contributor (.048 portion)
    - session log with Compiler Tools section + Phase 0 approval MCP ref + full Phase 1 run summary
  </closeout>
</task_order>
