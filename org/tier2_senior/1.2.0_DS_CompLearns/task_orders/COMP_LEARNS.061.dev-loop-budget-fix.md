<task_order>
  <metadata>
    <id>1.2.0_DS_CompLearns-2026-04-24-comp-learns-061-dev-loop-budget-fix</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.2.0_DS_CompLearns</issued_to>
    <date>2026-04-24</date>
    <status>complete <!-- commit eaf25d6a pushed CLOUD 2026-04-24 by 1.2.0_DS_CompLearns --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — dev-loop infrastructure fix; should land before .060 Lane A rebuild run</priority>
  </metadata>

  <references>
    <ref type="finding">comp/results/dev-4/integrity_invalidation.md finding 3 — budget accounting off-by-one (authored by 1.1.0_DS_CompLearns at df168552)</ref>
    <ref type="source">comp/bin/comp-dev-loop.py — the loop runner</ref>
    <ref type="prd">docs/architecture/COMP_LEARNS_WAVE3_V1.md §2.3 (stop conditions) — budget-exit is a valid stop reason; result.json must accurately reflect total_iterations</ref>
  </references>

  <objective>
    Fix the off-by-one bug in `comp/bin/comp-dev-loop.py` total_iterations accounting
    on budget exit, as documented in finding 3 of integrity_invalidation.md.

    ## Finding (verbatim from df168552)

    The loop checks budget at the START of each iteration, before `total_iterations += 1`:
    ```
    while True:
        iteration += 1
        elapsed = time.monotonic() - t0
        if elapsed >= budget_sec:
            exit_reason = "budget"
            break
        total_iterations += 1   # NOT reached if budget hit here
    ```
    If budget exhausted at start of iter-2, total_iterations still shows 1 (only iter-1
    incremented it). result.json shows the last completed iteration count, not the total
    attempted.

    ## Fix

    Move `total_iterations += 1` to BEFORE the budget check, so the count reflects every
    iteration that was entered — regardless of whether budget cut it off:

    ```python
    while True:
        iteration += 1
        total_iterations += 1   # count the iteration we entered
        elapsed = time.monotonic() - t0
        if elapsed >= budget_sec:
            exit_reason = "budget"
            break
        # ... rest of loop body
    ```

    Read the actual source before editing — the variable names may differ from this sketch.
    Fix only the budget-accounting off-by-one. Do not refactor surrounding logic.

    ## Scope

    - Edit ONLY: comp/bin/comp-dev-loop.py
    - Verify: existing pytest comp/ tests still pass after fix
    - Verify: python -m py_compile comp/bin/comp-dev-loop.py exits 0
    - Do NOT change any output schema, loop semantics, or stop conditions

    Explicitly out of scope:
    - Any other bugs in comp-dev-loop.py
    - Lane A rebuild (.060) — separate TO
    - Case scoring work
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before edit">
      <step>
        <run>python -m py_compile comp/bin/comp-dev-loop.py</run>
        <expect>Exit 0 (baseline compiles)</expect>
        <if_mismatch>File is already broken. MCP COO before proceeding.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/ -q 2>&amp;1 | tail -5</run>
        <expect>At most 9 pre-existing reds. Note baseline count.</expect>
        <if_mismatch>Surface baseline test state to COO before editing.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after edit, before commit">
      <step>
        <run>.tools/ds-commit-gate.sh comp/bin/comp-dev-loop.py</run>
        <expect>Exit 0</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>python -m py_compile comp/bin/comp-dev-loop.py</run>
        <expect>Exit 0</expect>
        <if_mismatch>Fix syntax error before commit.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/ -q 2>&amp;1 | tail -5</run>
        <expect>Same number of reds as baseline (no new failures)</expect>
        <if_mismatch>Fix regression before commit.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>Should ship before .060 (Lane A rebuild) begins, since the rebuild will run the loop and result.json accuracy matters. Non-blocking to .054/.055/.056/.057 (different files).</note>
    <shared_artifacts>comp/bin/comp-dev-loop.py (sole touched file)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp-dev-loop.py compiles clean (python -m py_compile exit 0).
    2. No new pytest failures vs baseline.
    3. Finding 3 logic is fixed: total_iterations incremented before budget check.
    4. Commit --only --author="1.2.0_DS_CompLearns &lt;1.2.0_DS_CompLearns@opal.agent&gt;" -- comp/bin/comp-dev-loop.py.
    5. Pushed to CLOUD.
    6. MCP COMPLETE to 2.1.0_SA_COO with commit sha.
  </acceptance_criteria>

  <dependencies>
    - No prerequisite TOs.
    - Should complete before .060 Lane A rebuild begins (not a hard gate, but preferred).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - Minimal-scope fix only. Read the file before editing.
    - No emojis.
  </operational_notes>

  <closeout>
    - commit --only --author="1.2.0_DS_CompLearns &lt;1.2.0_DS_CompLearns@opal.agent&gt;" -- comp/bin/comp-dev-loop.py
    - push to CLOUD
    - flip TO status complete with commit sha
    - MCP COMPLETE to 2.1.0_SA_COO
  </closeout>
</task_order>
