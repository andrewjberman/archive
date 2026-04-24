<task_order>
  <metadata>
    <id>1.4.0_DS_CompLearns-2026-04-24-comp-learns-057-case2-condition-b-aided</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.4.0_DS_CompLearns</issued_to>
    <date>2026-04-24</date>
    <status>staged</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Wave 3b Lane B, Case 2 aided intervention runner</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_WAVE3_V1.md §0.5 + §0.6 + §3.8 — bd84ef10</ref>
    <ref type="prd">docs/architecture/COMP_LEARNS_DS_ROLE_ADDENDUM.md §2a-§2e + §4 + §5 + §6</ref>
    <ref type="packet">comp/tasks/case-002-click-refactor/packet.yaml — baseline_commit f80cf4b0</ref>
    <ref type="sequencing">Dispatched AFTER .054 (Case 1 condition_a, also 1.4.0_DS) completes. Different task repo — no cross-case contamination.</ref>
  </references>

  <objective>
    Serve as the Wave 3b aided intervention runner for Case 2
    (case-002-click-refactor). Condition b: full comp/ harness available.

    Note: you also ran .054 (Case 1 httpx unaided) this wave. These are different task repos
    with different fix targets. Cross-task contamination is not possible. Your prior_exposure
    for Case 2 is none from pilot wave 1.

    In reasoning.md, include:
    ```
    prior_exposure: none (Case 2); separate case from .054 (httpx, different repo)
    ```

    ## Phase 0 — Provisioning + preflight (BEFORE navigation)

    1. COO will reset comp/targets/click/_repo/ to f80cf4b0 after .056 (condition_a) ships
       and before dispatching you. Verify clean state:
       ```bash
       git -C comp/targets/click/_repo rev-parse HEAD | grep -q "^f80cf4b0" || { echo "GATE 1 FAIL"; exit 2; }
       git -C comp/targets/click/_repo diff --quiet || { echo "GATE 2a FAIL"; exit 2; }
       git -C comp/targets/click/_repo diff --cached --quiet || { echo "GATE 2b FAIL"; exit 2; }
       [ -z "$(git -C comp/targets/click/_repo status --porcelain)" ] || { echo "GATE 2c FAIL"; exit 2; }
       echo "All gates PASS"
       ```
       Any gate fail = STOP. MCP COO.

       If _repo/ missing (not yet provisioned):
       ```bash
       git clone https://github.com/pallets/click comp/targets/click/_repo
       git -C comp/targets/click/_repo checkout f80cf4b09fbe36099b7bfc065fbde30d053da46d
       ```

    2. Create bundle directory:
       ```bash
       mkdir -p comp/tasks/case-002-click-refactor/bundles/ds-1.4.0-condition_b
       ```

    ## Phase 1 — Aided navigation (condition_b)

    3. Work in comp/targets/click/_repo/ at f80cf4b0.
       Full comp/ harness: comp/targets/click/compiler.py, scorecards, graph outputs.
       Condition b allowed artifacts per packet.yaml:
       - repo_source_tree, comp_targets_dir, compiler_py, scorecards, champion_json, selector_outputs
       Forbidden: ab_cache, prior_scoring_verdicts, other_ds_bundles.

    4. Task: refactor click's nested command-group dispatch subsystem preserving the 8
       structural invariants (see packet.yaml). Use the compiler's structural graph to map
       the Group dispatch subsystem before refactoring. The harness provides cross-module
       call chains, decorator accumulation relationships, param registration surfaces.

    5. Produce nav_log.jsonl concurrently:
       ```jsonl
       {"ts":"<ISO8601>","event":"file_open","path":"src/click/core.py","compiler_assisted":true}
       {"ts":"<ISO8601>","event":"comp_call","tool":"comp-build","args":""}
       {"ts":"<ISO8601>","event":"comp_call","tool":"comp-trace","args":"Group.invoke --direction both"}
       {"ts":"<ISO8601>","event":"hypothesis","text":"<text>","correct":true}
       {"ts":"<ISO8601>","event":"token_count","cumulative":11200}
       ```
       Required: file_open events, all comp_call events (you should have multiple — use the
       harness), hypotheses (first correct marked correct=true), token_count.

       Decisive file set: src/click/core.py (Group subsystem), src/click/decorators.py.
       Recording how quickly core.py appears in your nav_log relative to other files gives
       SC the localization precision signal.

    ## Phase 2 — Bundle production

    6. Run acceptance criteria in comp/targets/click/_repo/:
       ```bash
       pytest tests/ -q                                           # ac-1
       pytest tests/ -q -k 'group or nested or subcommand'       # ac-2
       pytest tests/ -q -k 'option or param or decorator'        # ac-3
       pytest tests/ -q -k 'invoke or result_callback or chain'  # ac-4
       pytest tests/ -q -k 'help or version or eager'            # ac-5
       ```
       All five must exit 0. Full output to test_output.txt.

    7. Produce bundle at comp/tasks/case-002-click-refactor/bundles/ds-1.4.0-condition_b/:
       - changes.patch — `git -C comp/targets/click/_repo diff f80cf4b0 HEAD`
       - test_output.txt — ac-1 through ac-5 output
       - reasoning.md — invariant analysis + compiler tool usage + hypothesis trace + prior_exposure field
       - nav_log.jsonl — machine-readable nav log

    Explicitly out of scope:
    - Case 1 (httpx) — already done in .054; this is a separate run
    - Accessing other_ds_bundles or prior_scoring_verdicts
    - Communicating with .056 (condition_a) during run
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before navigation (Phase 0)">
      <step>
        <run>git -C comp/targets/click/_repo rev-parse HEAD 2>/dev/null | head -c 8</run>
        <expect>f80cf4b0</expect>
        <if_mismatch>Provision or reset _repo/. STOP until clean.</if_mismatch>
      </step>
      <step>
        <run>git -C comp/targets/click/_repo status --porcelain | wc -l</run>
        <expect>0</expect>
        <if_mismatch>Reset: git -C comp/targets/click/_repo reset --hard f80cf4b0. MCP COO if persistent.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before bundle commit">
      <step>
        <run>ls comp/tasks/case-002-click-refactor/bundles/ds-1.4.0-condition_b/</run>
        <expect>changes.patch + test_output.txt + reasoning.md + nav_log.jsonl</expect>
        <if_mismatch>Author missing artifacts.</if_mismatch>
      </step>
      <step>
        <run>python -c "import json; rows=[json.loads(l) for l in open('comp/tasks/case-002-click-refactor/bundles/ds-1.4.0-condition_b/nav_log.jsonl')]; cc=[r for r in rows if r['event']=='comp_call']; print(f'comp_calls: {len(cc)}')"</run>
        <expect>comp_calls: 1 or more</expect>
        <if_mismatch>Flag as noise (0 comp_calls in aided run) in reasoning.md and MCP COO before committing.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>This TO is dispatched AFTER .054 (Case 1 unaided) and AFTER .056 (Case 2 condition_a) ship. COO resets click _repo/ to f80cf4b0 before dispatching you. Different repo from .054 (httpx vs click) — no cross-contamination. SC (.059) gates on .056 AND .057.</note>
    <shared_artifacts>comp/targets/click/_repo/ (COO-reset between conditions); comp/tasks/case-002-click-refactor/bundles/</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Phase 0 preflight all exit 0 before navigation.
    2. ac-1 through ac-5 all exit 0.
    3. nav_log.jsonl: at least 1 comp_call, at least 1 correct=true hypothesis.
    4. All 4 bundle artifacts present at ds-1.4.0-condition_b/.
    5. Commit --only --author="1.4.0_DS_CompLearns &lt;1.4.0_DS_CompLearns@opal.agent&gt;" -- comp/tasks/case-002-click-refactor/bundles/ds-1.4.0-condition_b/**.
    6. Pushed to CLOUD.
    7. MCP COMPLETE to 2.1.0_SA_COO with: commit sha + ac verdicts + comp_call count.
  </acceptance_criteria>

  <dependencies>
    - Sequenced after .054 (Case 1 condition_a, also 1.4.0_DS) — same agent, sequential dispatch.
    - Sequenced after .056 ships (COO resets _repo/ before dispatching you).
    - Blocks: .059 (SC Case 2 scoring).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - Write nav_log.jsonl in real time.
    - No emojis in any artifact.
  </operational_notes>

  <closeout>
    - commit --only --author="1.4.0_DS_CompLearns &lt;1.4.0_DS_CompLearns@opal.agent&gt;" -- comp/tasks/case-002-click-refactor/bundles/ds-1.4.0-condition_b/**
    - push to CLOUD
    - flip TO status complete
    - MCP COMPLETE to 2.1.0_SA_COO
    - session log with Compiler Tools section
  </closeout>
</task_order>
