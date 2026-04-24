<task_order>
  <metadata>
    <id>1.1.0_DS_CompLearns-2026-04-24-comp-learns-062-ratchet-src-layout-fix</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.1.0_DS_CompLearns</issued_to>
    <date>2026-04-24</date>
    <status>complete</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — unblocks .060 P0.4 cold measurement; fast-turnaround micro-TO</priority>
  </metadata>

  <references>
    <ref type="blocker">comp/loop/ratchet.py line 644 — target_root hardcoded as _repo/target; fails for src-layout packages (click)</ref>
    <ref type="cto_decision">CTO MCP 20260424T152630Z — Option B approved verbatim; no new tests required beyond smoke check</ref>
    <ref type="parent_to">COMP_LEARNS.060 Phase 0 Gap 2 — src layout mismatch discovered on P0.4 smoke run</ref>
  </references>

  <objective>
    Apply a 4-line existence-guarded fix to comp/loop/ratchet.py to handle src-layout
    packages (click uses src/click/; httpx uses flat _repo/httpx/). CTO approved the
    exact patch below. No behavioral change for existing flat-layout targets.

    ## The Fix

    Current code (line 644, inside iterate() call):
    ```
        target_root=target_dir / "_repo" / target,
    ```

    Approved patch — two edits:

    ### Edit 1: Add candidate resolution BEFORE `result = iterate(` (line 642)

    Insert these 6 lines immediately before `result = iterate(`:
    ```python
    candidate = target_dir / "_repo" / target
    if not candidate.exists():
        src_candidate = target_dir / "_repo" / "src" / target
        if src_candidate.exists():
            candidate = src_candidate
    target_root = candidate
    ```

    ### Edit 2: Replace hardcoded path inside iterate() call (line 644)

    Change:
    ```python
            target_root=target_dir / "_repo" / target,
    ```
    To:
    ```python
            target_root=target_root,
    ```

    ## Scope

    - Edit ONLY: comp/loop/ratchet.py
    - No new tests required (per CTO decision — existence-guarded, zero behavioral change for httpx)
    - Verify: python -m py_compile comp/loop/ratchet.py exits 0
    - Smoke check: confirm httpx path still resolves (comp/targets/httpx/_repo/httpx/ exists)
    - Smoke check: confirm click path now resolves (comp/targets/click/_repo/src/click/ exists)

    Explicitly out of scope:
    - Any other ratchet.py changes
    - imports_gold.jsonl authoring (CTO doing that in parallel)
    - Starting .060 P0.4 before COO relays that BOTH gaps are cleared
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before edit">
      <step>
        <run>python -m py_compile comp/loop/ratchet.py</run>
        <expect>Exit 0 (baseline compiles)</expect>
        <if_mismatch>MCP COO before proceeding.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after edit, before commit">
      <step>
        <run>python -m py_compile comp/loop/ratchet.py</run>
        <expect>Exit 0</expect>
        <if_mismatch>Fix syntax before commit.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh comp/loop/ratchet.py</run>
        <expect>Exit 0</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "from pathlib import Path; t='httpx'; d=Path('comp/targets/httpx'); c=d/'_repo'/t; print('httpx flat-layout:', c, 'exists:', c.exists())"</run>
        <expect>httpx flat-layout path exists: True</expect>
        <if_mismatch>Regression on httpx target_root resolution. Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "from pathlib import Path; t='click'; d=Path('comp/targets/click'); c=d/'_repo'/t; src=d/'_repo'/'src'/t; print('flat:', c.exists(), 'src:', src.exists())"</run>
        <expect>flat: False src: True</expect>
        <if_mismatch>click _repo/ state unexpected. MCP COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    1. ratchet.py compiles clean post-edit.
    2. httpx flat-layout path still resolves (existence check confirms).
    3. click src-layout path resolves via fallback (existence check confirms).
    4. Commit --only --author="1.1.0_DS_CompLearns &lt;1.1.0_DS_CompLearns@opal.agent&gt;" -- comp/loop/ratchet.py
    5. Pushed to CLOUD.
    6. MCP COMPLETE to 2.1.0_SA_COO with commit sha.
  </acceptance_criteria>

  <dependencies>
    - No prerequisites. Fast-path dispatch.
    - Unblocks: .060 P0.4 cold measurement (combined with CTO imports_gold.jsonl authoring, both needed)
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - Minimal-scope fix only. Read the file before editing.
    - Do NOT start .060 P0.4 on your own authority after this ships — wait for explicit COO signal that BOTH gaps (ratchet fix + imports_gold.jsonl) are cleared.
    - No emojis.
  </operational_notes>

  <closeout>
    - commit --only --author="1.1.0_DS_CompLearns &lt;1.1.0_DS_CompLearns@opal.agent&gt;" -- comp/loop/ratchet.py
    - push to CLOUD
    - flip TO status complete with commit sha
    - MCP COMPLETE to 2.1.0_SA_COO
  </closeout>
</task_order>
