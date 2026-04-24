<task_order>
  <metadata>
    <id>1.2.0_DS_CompLearns-2026-04-24-comp-learns-055-case1-condition-b-aided</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.2.0_DS_CompLearns</issued_to>
    <date>2026-04-24</date>
    <status>staged</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Wave 3b Lane B, Case 1 aided intervention runner</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_WAVE3_V1.md §0.5 + §0.6 + §3.8 — commit bd84ef10 (rev5)</ref>
    <ref type="prd">docs/architecture/COMP_LEARNS_DS_ROLE_ADDENDUM.md §2a-§2e + §4 + §5 + §6</ref>
    <ref type="packet">comp/tasks/task-001-httpx-netrc-host-authority/packet.yaml — baseline_commit 354c4cac</ref>
    <ref type="wave3b_decision">COMP_LEARNS.WAVE3B-DECISION.md — no prior exposure for 1.2.0_DS on this case</ref>
  </references>

  <objective>
    Serve as the Wave 3b aided intervention runner for Case 1
    (task-001-httpx-netrc-host-authority). Condition b: full comp/ harness available.
    Use compiler tools to navigate to the bug fix.

    No prior Case 1 exposure for this agent. Confound field in reasoning.md:
    ```
    prior_exposure: none
    ```

    ## Phase 0 — Provisioning + preflight (BEFORE navigation)

    1. COO will reset comp/targets/httpx/_repo/ to baseline 354c4cac between conditions.
       Verify before starting:
       ```bash
       git -C comp/targets/httpx/_repo rev-parse HEAD | grep -q "^354c4cac" || { echo "GATE 1 FAIL"; exit 2; }
       git -C comp/targets/httpx/_repo diff --quiet || { echo "GATE 2a FAIL"; exit 2; }
       git -C comp/targets/httpx/_repo diff --cached --quiet || { echo "GATE 2b FAIL"; exit 2; }
       [ -z "$(git -C comp/targets/httpx/_repo status --porcelain)" ] || { echo "GATE 2c FAIL"; exit 2; }
       echo "All gates PASS"
       ```
       Any gate fail = STOP. MCP COO. Do not navigate.

       If _repo/ is missing entirely (not provisioned), provision first:
       ```bash
       git clone https://github.com/encode/httpx comp/targets/httpx/_repo
       git -C comp/targets/httpx/_repo checkout 354c4cac1f1796ee4d8861a4c978807398852ad5
       ```

    2. Create bundle directory:
       ```bash
       mkdir -p comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.2.0-condition_b
       ```

    ## Phase 1 — Aided navigation (condition_b)

    3. Work in comp/targets/httpx/_repo/ at 354c4cac.
       Full comp/ harness available: comp/targets/httpx/compiler.py, scorecards, champion.json,
       selector outputs. You may run compiler.py to generate selector output, query the graph,
       use comp-trace to follow import and call edges.

       Condition b harness artifacts per packet.yaml:
       - repo_source_tree: allowed
       - comp_targets_dir: allowed (comp/targets/httpx/)
       - compiler_py: allowed
       - scorecards: allowed
       - champion_json: allowed
       - selector_outputs: allowed (may generate via compiler.py)
       - ab_cache: FORBIDDEN
       - prior_scoring_verdicts: FORBIDDEN
       - other_ds_bundles: FORBIDDEN

    4. Produce nav_log.jsonl concurrently as you navigate:
       ```jsonl
       {"ts":"<ISO8601>","event":"file_open","path":"httpx/_utils.py","compiler_assisted":true}
       {"ts":"<ISO8601>","event":"comp_call","tool":"comp-trace","args":"<args used>"}
       {"ts":"<ISO8601>","event":"hypothesis","text":"<text>","correct":false}
       {"ts":"<ISO8601>","event":"token_count","cumulative":8400}
       {"ts":"<ISO8601>","event":"hypothesis","text":"<text>","correct":true}
       ```
       Required: file_open events in order, all comp_call events, hypotheses (first correct
       marked correct=true), token_count at each hypothesis and at session end.
       Unaided condition must have 0 comp_call events. Aided (you) should have >0.

    5. Decisive file set: httpx/_utils.py (root cause), httpx/_client.py (call site).
       Document your hypothesis trace — how did the graph guide you to _utils.py?

    6. Fix: extract host from authority before netrc.authenticators() call in
       httpx/_utils.py NetRCInfo.get_credentials().

    7. Add test: tests/client/test_auth.py — test_netrc_auth_non_standard_port (or similar
       matching -k netrc_non_standard_port). Use existing .netrc fixture at
       tests/fixtures/.netrc (machine netrcexample.org). Non-standard port URL in test
       (e.g. http://netrcexample.org:8080). Test must fail at baseline without fix.

    ## Phase 2 — Bundle production

    8. Run acceptance criteria:
       ```bash
       pytest tests/client/test_auth.py -q -k netrc          # ac-1
       pytest tests/client/test_auth.py -q -k netrc_non_standard_port  # ac-2
       pytest tests/client/test_auth.py tests/test_auth.py -q          # ac-3
       ```
       All three must exit 0. Capture full output to test_output.txt.

    9. Produce bundle at comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.2.0-condition_b/:
       - changes.patch — `git -C comp/targets/httpx/_repo diff 354c4cac HEAD`
       - test_output.txt — combined ac-1/2/3 output
       - reasoning.md — navigation trace + compiler tool calls + hypothesis trace + fix rationale
         Include: prior_exposure: none
       - nav_log.jsonl — machine-readable nav log

    Explicitly out of scope:
    - Case 2 (click) — that is .056/.057
    - Accessing other_ds_bundles or prior_scoring_verdicts
    - Communicating findings to .054 agent during run
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before navigation (Phase 0)">
      <step>
        <run>git -C comp/targets/httpx/_repo rev-parse HEAD 2>/dev/null | head -c 8</run>
        <expect>354c4cac</expect>
        <if_mismatch>Provision or reset _repo/ per Phase 0 step 1. STOP until clean.</if_mismatch>
      </step>
      <step>
        <run>git -C comp/targets/httpx/_repo status --porcelain | wc -l</run>
        <expect>0 (clean working tree)</expect>
        <if_mismatch>Reset: git -C comp/targets/httpx/_repo reset --hard 354c4cac. MCP COO if persistent.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before bundle commit">
      <step>
        <run>ls comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.2.0-condition_b/</run>
        <expect>changes.patch + test_output.txt + reasoning.md + nav_log.jsonl</expect>
        <if_mismatch>Author missing artifacts.</if_mismatch>
      </step>
      <step>
        <run>python -c "import json; rows=[json.loads(l) for l in open('comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.2.0-condition_b/nav_log.jsonl')]; cc=[r for r in rows if r['event']=='comp_call']; print(f'comp_calls: {len(cc)}')"</run>
        <expect>comp_calls: 1 or more (aided run must have used compiler)</expect>
        <if_mismatch>If 0 comp_call events, flag as noise in reasoning.md and MCP COO before committing. Do not re-run without COO guidance.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>git log --oneline -1 --author="1.2.0_DS_CompLearns"</run>
        <expect>Commit present</expect>
        <if_mismatch>Re-commit with correct author.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>Non-contamination: no communication with .054 (condition_a) during or before your run. COO resets _repo/ between conditions. SC (.058) gates on both bundles.</note>
    <shared_artifacts>comp/targets/httpx/_repo/ (COO resets between conditions); comp/tasks/task-001-httpx-netrc-host-authority/bundles/ (each DS writes own dir)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Phase 0 preflight all exit 0 before navigation (paste evidence in ACK MCP).
    2. ac-1: pytest -k netrc exits 0.
    3. ac-2: pytest -k netrc_non_standard_port exits 0 (new test present).
    4. ac-3: full auth suite exits 0.
    5. nav_log.jsonl has at least 1 comp_call event (aided must use harness).
    6. nav_log.jsonl has at least 1 correct=true hypothesis.
    7. All 4 bundle artifacts present at ds-1.2.0-condition_b/.
    8. Commit --only --author=1.2.0_DS_CompLearns -- comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.2.0-condition_b/**.
    9. Pushed to CLOUD.
    10. MCP COMPLETE to 2.1.0_SA_COO with: commit sha + ac verdicts + comp_call count.
  </acceptance_criteria>

  <dependencies>
    - Gate: COO confirms _repo/ reset after .054 completes (or provisioned fresh if .054 runs first).
    - Parallel (non-blocking): .054 (condition_a, 1.4.0_DS). Do NOT coordinate.
    - Blocks: .058 (SC Case 1 scoring).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - Write nav_log.jsonl in real time. Do not reconstruct post-session.
    - If you see 0 comp_call events at session end, flag as noise and MCP COO before committing.
    - No emojis in any artifact.
  </operational_notes>

  <closeout>
    - commit --only --author="1.2.0_DS_CompLearns &lt;1.2.0_DS_CompLearns@opal.agent&gt;" -- comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.2.0-condition_b/**
    - push to CLOUD
    - flip TO status complete with commit sha
    - MCP COMPLETE to 2.1.0_SA_COO
    - session log with Compiler Tools section
  </closeout>
</task_order>
