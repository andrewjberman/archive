<task_order>
  <metadata>
    <id>1.4.0_DS_CompLearns-2026-04-24-comp-learns-054-case1-condition-a-unaided</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.4.0_DS_CompLearns</issued_to>
    <date>2026-04-24</date>
    <status>staged</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Wave 3b Lane B, Case 1 unaided baseline</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_WAVE3_V1.md §0.5 (seam integrity) + §0.6 (clean def) + §3.8 (preflight gates) — commit bd84ef10 (rev5)</ref>
    <ref type="prd">docs/architecture/COMP_LEARNS_DS_ROLE_ADDENDUM.md §2a-§2e + §4 + §5 + §6</ref>
    <ref type="packet">comp/tasks/task-001-httpx-netrc-host-authority/packet.yaml — baseline_commit 354c4cac</ref>
    <ref type="wave3b_decision">org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.WAVE3B-DECISION.md — prior_exposure control: flag in verdict if exposed in prior session</ref>
  </references>

  <objective>
    Serve as the Wave 3b unaided intervention runner for Case 1
    (task-001-httpx-netrc-host-authority). Condition a: no compiler harness, no comp/
    artifacts. Navigation by source reading alone.

    Confound note: 1.4.0_DS ran task-001 condition_a in pilot wave 1. That was a prior
    session — no context carryover. Flag this explicitly in your reasoning.md and bundle
    (field: "prior_exposure": "pilot-wave-1 condition_a, separate session, no carryover")
    so SC can account for it in verdict notes.

    ## Phase 0 — Provisioning + preflight (BEFORE any navigation)

    1. Provision httpx canonical source if not present:
       ```bash
       cd /c/Users/AndrewBerman/Desktop/feature_clb
       git clone https://github.com/encode/httpx comp/targets/httpx/_repo
       git -C comp/targets/httpx/_repo checkout 354c4cac1f1796ee4d8861a4c978807398852ad5
       ```
       If `_repo/` already exists, verify HEAD: `git -C comp/targets/httpx/_repo rev-parse HEAD`
       must output `354c4cac...`. If not, `git -C comp/targets/httpx/_repo checkout 354c4cac...`.

    2. Run §3.8 preflight gates (adapted for httpx). Paste exit-0 evidence in ACK MCP:
       ```bash
       git -C comp/targets/httpx/_repo rev-parse HEAD | grep -q "^354c4cac" || { echo "GATE 1 FAIL"; exit 2; }
       git -C comp/targets/httpx/_repo diff --quiet || { echo "GATE 2a FAIL"; exit 2; }
       git -C comp/targets/httpx/_repo diff --cached --quiet || { echo "GATE 2b FAIL"; exit 2; }
       [ -z "$(git -C comp/targets/httpx/_repo status --porcelain)" ] || { echo "GATE 2c FAIL"; exit 2; }
       echo "All gates PASS"
       ```
       Any gate fail = STOP. MCP COO immediately. Do not start navigation.

    3. Create bundle output directory:
       ```bash
       mkdir -p comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.4.0-condition_a
       ```

    ## Phase 1 — Unaided navigation (condition_a)

    4. Work ONLY in comp/targets/httpx/_repo/ at baseline 354c4cac.
       No compiler tools. No comp/ artifacts. Source reading, grep, git log, test runner only.
       No access to comp/targets/httpx/compiler.py, scorecards, champion.json, or any COMP_LEARNS
       graph output.

    5. Produce the required nav_log.jsonl concurrently as you navigate.
       Write one JSON line per significant event (no buffering — emit as events happen):
       ```jsonl
       {"ts":"<ISO8601>","event":"file_open","path":"httpx/_utils.py","compiler_assisted":false}
       {"ts":"<ISO8601>","event":"hypothesis","text":"<text>","correct":false}
       {"ts":"<ISO8601>","event":"token_count","cumulative":4200}
       {"ts":"<ISO8601>","event":"hypothesis","text":"<text>","correct":true}
       ```
       Required event types: file_open, hypothesis (mark correct=true on first correct one),
       token_count (at minimum: emit at each hypothesis, at session end).
       comp_call events: expected 0 for condition_a (you have no harness).

    6. Decisive file set for Case 1: httpx/_utils.py (root cause — NetRCInfo.get_credentials).
       Secondary surface: httpx/_client.py (call site). Finding typehints.py in your nav_log
       before producing the fix indicates correct localization.

    7. Produce the fix: extract host from authority before netrc.authenticators() call.
       Minimal change — do not refactor beyond the bug.

    8. Add test: tests/client/test_auth.py — test_netrc_auth_non_standard_port (or similar,
       must match -k netrc_non_standard_port) using the existing .netrc fixture at
       tests/fixtures/.netrc (machine: netrcexample.org) with a non-standard port URL.

    ## Phase 2 — Bundle production

    9. Run acceptance criteria in comp/targets/httpx/_repo/:
       ```bash
       pytest tests/client/test_auth.py -q -k netrc          # ac-1
       pytest tests/client/test_auth.py -q -k netrc_non_standard_port  # ac-2
       pytest tests/client/test_auth.py tests/test_auth.py -q          # ac-3
       ```
       All three must exit 0. Capture full output to test_output.txt.

    10. Produce bundle artifacts at comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.4.0-condition_a/:
        - changes.patch — `git -C comp/targets/httpx/_repo diff 354c4cac HEAD`
        - test_output.txt — combined ac-1 + ac-2 + ac-3 output
        - reasoning.md — navigation log + hypothesis trace + fix rationale
          (NOT exposed to SC in Phase 1 scoring; audit only)
        - nav_log.jsonl — machine-readable navigation log per §3.5 format

        In reasoning.md, include:
        ```
        prior_exposure: pilot-wave-1 condition_a, separate session, no context carryover
        ```

    Explicitly out of scope:
    - Using any comp/ compiler artifacts or harness tools
    - Case 2 (click) — that is .056/.057
    - Any interaction with aided condition DS agent mid-flight
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before navigation (Phase 0)">
      <step>
        <run>git -C comp/targets/httpx/_repo rev-parse HEAD 2>/dev/null | head -c 8</run>
        <expect>354c4cac (first 8 chars of baseline_commit)</expect>
        <if_mismatch>Provision _repo/ per Phase 0 step 1. STOP until provisioned.</if_mismatch>
      </step>
      <step>
        <run>git -C comp/targets/httpx/_repo diff --quiet &amp;&amp; git -C comp/targets/httpx/_repo diff --cached --quiet &amp;&amp; echo "CLEAN"</run>
        <expect>CLEAN — no diffs</expect>
        <if_mismatch>Run git reset --hard 354c4cac in _repo/. MCP COO if persistent.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before bundle commit">
      <step>
        <run>ls comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.4.0-condition_a/</run>
        <expect>changes.patch + test_output.txt + reasoning.md + nav_log.jsonl all present</expect>
        <if_mismatch>Author missing artifacts before committing.</if_mismatch>
      </step>
      <step>
        <run>python -c "import json; rows=[json.loads(l) for l in open('comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.4.0-condition_a/nav_log.jsonl')]; assert any(r['event']=='hypothesis' and r.get('correct') for r in rows); print('nav_log has correct hypothesis')"</run>
        <expect>nav_log has correct hypothesis</expect>
        <if_mismatch>Ensure at least one hypothesis event with correct=true is in nav_log.jsonl</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>git log --oneline -1 --author="1.4.0_DS_CompLearns"</run>
        <expect>Commit present with correct author</expect>
        <if_mismatch>Re-commit with --author=1.4.0_DS_CompLearns flag.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>Non-contamination: do not share navigation findings with 1.2.0_DS (Case 1 condition_b) during or before your run. Conditions must be independent. Between conditions, COO will reset _repo/ to baseline. SC (.058) gates on both bundles (yours + .055).</note>
    <shared_artifacts>comp/targets/httpx/_repo/ (shared target repo — gates enforce clean state between conditions); comp/tasks/task-001-httpx-netrc-host-authority/bundles/ (each DS writes own subdirectory)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Phase 0 preflight gates all exit 0 before navigation begins (paste evidence in ACK MCP).
    2. ac-1: pytest tests/client/test_auth.py -q -k netrc exits 0.
    3. ac-2: pytest tests/client/test_auth.py -q -k netrc_non_standard_port exits 0 (new test added).
    4. ac-3: pytest tests/client/test_auth.py tests/test_auth.py -q exits 0.
    5. nav_log.jsonl present with at least one file_open event, at least one correct=true hypothesis, at least one token_count event.
    6. nav_log.jsonl has zero comp_call events (unaided).
    7. reasoning.md includes prior_exposure field.
    8. All 4 bundle artifacts present at ds-1.4.0-condition_a/.
    9. Commit --only --author="1.4.0_DS_CompLearns &lt;1.4.0_DS_CompLearns@opal.agent&gt;" -- comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.4.0-condition_a/**.
    10. Pushed to CLOUD.
    11. MCP COMPLETE to 2.1.0_SA_COO with: commit sha + ac-1/2/3 verdict + decisive-file-found Y/N.
  </acceptance_criteria>

  <dependencies>
    - Gate: Wave 3b authorized (COMP_LEARNS.WAVE3B-DECISION.md — satisfied).
    - Parallel (non-blocking): .055 (Case 1 condition_b, 1.2.0_DS). Do NOT coordinate.
    - Parallel (non-blocking): .056/.057 (Case 2, different target repo — no contamination).
    - Blocks: .058 (SC Case 1 scoring — requires both .054 AND .055 bundles).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - Work target is comp/targets/httpx/_repo/ at 354c4cac. Do NOT work in the main repo.
    - Write nav_log.jsonl in real time as you navigate — do not reconstruct from memory after.
    - Prior_exposure is flagged, not invalidating. Your result counts. The flag is for SC's
      narrative note in the verdict file.
    - No emojis in any artifact.
  </operational_notes>

  <closeout>
    On completion:
    - commit --only --author="1.4.0_DS_CompLearns &lt;1.4.0_DS_CompLearns@opal.agent&gt;" -- comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.4.0-condition_a/**
    - push to CLOUD
    - flip TO status to complete with commit sha
    - MCP COMPLETE to 2.1.0_SA_COO
    - session log at org/tier2_senior/1.4.0_DS_CompLearns/logs/{date}/ with Compiler Tools section
  </closeout>
</task_order>
