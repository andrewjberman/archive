<task_order>
  <metadata>
    <id>1.3.0_DS_CompLearns-2026-04-24-comp-learns-056-case2-condition-a-unaided</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.3.0_DS_CompLearns</issued_to>
    <date>2026-04-24</date>
    <status>complete <!-- commit 5efb357f, pushed CLOUD 2026-04-24 — bundle restored after AE sweep abfed84d deleted TO file; SC scored via .059 (Phase 1 290bd61f, Phase 2 2d2337fb), verdict PASS --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Wave 3b Lane B, Case 2 unaided intervention runner</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_WAVE3_V1.md §0.5 + §0.6 + §3.8 (gates adapted for click) — bd84ef10</ref>
    <ref type="prd">docs/architecture/COMP_LEARNS_DS_ROLE_ADDENDUM.md §2a-§2e + §4 + §5 + §6</ref>
    <ref type="packet">comp/tasks/case-002-click-refactor/packet.yaml — baseline_commit f80cf4b0</ref>
    <ref type="wave3b_decision">COMP_LEARNS.WAVE3B-DECISION.md — prior_exposure: 1.3.0 ran Case 2 in pilot wave 1; flag in bundle</ref>
  </references>

  <objective>
    Serve as the Wave 3b unaided intervention runner for Case 2
    (case-002-click-refactor). Condition a: no compiler harness. Navigation by source
    reading alone.

    Confound note: 1.3.0_DS ran Case 2 in pilot wave 1 (prior session). Flag in bundle:
    ```
    prior_exposure: pilot-wave-1 case-002, separate session, no context carryover
    ```

    ## Phase 0 — Provisioning + preflight (BEFORE navigation)

    1. Provision click canonical source if not present:
       ```bash
       git clone https://github.com/pallets/click comp/targets/click/_repo
       git -C comp/targets/click/_repo checkout f80cf4b09fbe36099b7bfc065fbde30d053da46d
       ```
       If _repo/ exists, verify HEAD:
       ```bash
       git -C comp/targets/click/_repo rev-parse HEAD | grep -q "^f80cf4b0" || { echo "GATE 1 FAIL"; exit 2; }
       ```

    2. Run §3.8 preflight gates (adapted for click):
       ```bash
       git -C comp/targets/click/_repo rev-parse HEAD | grep -q "^f80cf4b0" || { echo "GATE 1 FAIL"; exit 2; }
       git -C comp/targets/click/_repo diff --quiet || { echo "GATE 2a FAIL"; exit 2; }
       git -C comp/targets/click/_repo diff --cached --quiet || { echo "GATE 2b FAIL"; exit 2; }
       [ -z "$(git -C comp/targets/click/_repo status --porcelain)" ] || { echo "GATE 2c FAIL"; exit 2; }
       echo "All gates PASS"
       ```
       Any gate fail = STOP. MCP COO. Do not navigate.

    3. Create bundle directory:
       ```bash
       mkdir -p comp/tasks/case-002-click-refactor/bundles/ds-1.3.0-condition_a
       ```

    ## Phase 1 — Unaided navigation (condition_a)

    4. Work ONLY in comp/targets/click/_repo/ at baseline f80cf4b0.
       No compiler tools. No comp/ artifacts. Source reading, grep, git log, test runner only.
       No access to comp/targets/click/compiler.py or any COMP_LEARNS graph output.

    5. Task: refactor click's nested command-group dispatch subsystem while preserving the
       8 structural invariants in packet.yaml. Target files: src/click/core.py (Group.invoke /
       Group.parse_args / Group.resolve_command) and src/click/decorators.py.

       The 8 invariants MUST be preserved exactly (see packet.yaml for full spec):
       (1) _protected_args dispatch (2) Decorator accumulation reversal (3) ctx.obj inheritance
       (4) _check_nested_chain guard (5) invoke_without_command semantics (6) result_callback chaining
       (7) Eager param ordering (8) CommandCollection source fallback

    6. Produce nav_log.jsonl concurrently:
       ```jsonl
       {"ts":"<ISO8601>","event":"file_open","path":"src/click/core.py","compiler_assisted":false}
       {"ts":"<ISO8601>","event":"hypothesis","text":"<text>","correct":false}
       {"ts":"<ISO8601>","event":"token_count","cumulative":5600}
       {"ts":"<ISO8601>","event":"hypothesis","text":"<text>","correct":true}
       ```
       Required events: file_open (all significant file accesses), hypothesis (mark first
       correct=true), token_count (at hypotheses + session end).
       comp_call events: expected 0 for condition_a.

       Decisive file set for Case 2: src/click/core.py (Group subsystem — primary refactor
       target), src/click/decorators.py (decorator accumulation). Recording when you open
       core.py relative to other files gives SC the navigation efficiency signal.

    ## Phase 2 — Bundle production

    7. Run acceptance criteria in comp/targets/click/_repo/:
       ```bash
       pytest tests/ -q                                           # ac-1
       pytest tests/ -q -k 'group or nested or subcommand'       # ac-2
       pytest tests/ -q -k 'option or param or decorator'        # ac-3
       pytest tests/ -q -k 'invoke or result_callback or chain'  # ac-4
       pytest tests/ -q -k 'help or version or eager'            # ac-5
       ```
       All five must exit 0. Capture full output to test_output.txt.

    8. Produce bundle at comp/tasks/case-002-click-refactor/bundles/ds-1.3.0-condition_a/:
       - changes.patch — `git -C comp/targets/click/_repo diff f80cf4b0 HEAD`
       - test_output.txt — combined ac-1 through ac-5 output
       - reasoning.md — invariant analysis + refactor rationale + navigation trace
         Include: prior_exposure: pilot-wave-1 case-002, separate session, no context carryover
       - nav_log.jsonl — machine-readable nav log

    Explicitly out of scope:
    - Using any comp/ compiler or harness tools
    - Case 1 (httpx) — that is .054/.055
    - Communicating with aided condition (.057) during run
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before navigation (Phase 0)">
      <step>
        <run>git -C comp/targets/click/_repo rev-parse HEAD 2>/dev/null | head -c 8</run>
        <expect>f80cf4b0</expect>
        <if_mismatch>Provision _repo/ per Phase 0 step 1. STOP until provisioned and clean.</if_mismatch>
      </step>
      <step>
        <run>git -C comp/targets/click/_repo status --porcelain | wc -l</run>
        <expect>0</expect>
        <if_mismatch>Reset: git -C comp/targets/click/_repo reset --hard f80cf4b0. MCP COO if persistent.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before bundle commit">
      <step>
        <run>ls comp/tasks/case-002-click-refactor/bundles/ds-1.3.0-condition_a/</run>
        <expect>changes.patch + test_output.txt + reasoning.md + nav_log.jsonl</expect>
        <if_mismatch>Author missing artifacts.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>Non-contamination: no communication with .057 (condition_b) during run. COO resets _repo/ between conditions. SC (.059) gates on both .056 and .057 bundles.</note>
    <shared_artifacts>comp/targets/click/_repo/ (COO resets between conditions); comp/tasks/case-002-click-refactor/bundles/ (each DS writes own subdir)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Phase 0 preflight all exit 0 before navigation.
    2. ac-1 through ac-5 all exit 0.
    3. nav_log.jsonl: at least 1 file_open, at least 1 correct=true hypothesis, 0 comp_call events.
    4. All 4 bundle artifacts present at ds-1.3.0-condition_a/.
    5. reasoning.md includes prior_exposure field.
    6. Commit --only --author="1.3.0_DS_CompLearns &lt;1.3.0_DS_CompLearns@opal.agent&gt;" -- comp/tasks/case-002-click-refactor/bundles/ds-1.3.0-condition_a/**.
    7. Pushed to CLOUD.
    8. MCP COMPLETE to 2.1.0_SA_COO with: commit sha + ac verdicts + decisive-file (core.py) found Y/N.
  </acceptance_criteria>

  <dependencies>
    - Gate: Wave 3b authorized (satisfied).
    - Parallel (non-blocking): .054 (Case 1, different target repo — no contamination).
    - Parallel (non-blocking): .057 (Case 2 condition_b, 1.4.0_DS — different agent, same repo but separate; gate enforces clean state).
    - Blocks: .059 (SC Case 2 scoring — requires .056 AND .057).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - Work target is comp/targets/click/_repo/ at f80cf4b0.
    - Write nav_log.jsonl in real time.
    - No emojis in any artifact.
  </operational_notes>

  <closeout>
    - commit --only --author="1.3.0_DS_CompLearns &lt;1.3.0_DS_CompLearns@opal.agent&gt;" -- comp/tasks/case-002-click-refactor/bundles/ds-1.3.0-condition_a/**
    - push to CLOUD
    - flip TO status complete
    - MCP COMPLETE to 2.1.0_SA_COO
    - session log with Compiler Tools section
  </closeout>
</task_order>
