<task_order>
  <metadata>
    <id>ADVI_ROLLUP.DH-1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-15</date>
    <status>complete</status>
    <evidence>Commit 516e39da; pushed CLOUD ba11a2ec; S3 upload ETag aef9d141715a021ead1122c890a23e48 (22:00:16 UTC). CTO NO-OBJECT 215957Z. Pre-flag to CTO+COO 215918/21Z. bash -n PASS pre+post; CHAIN_FULL analytically 26 scripts zero-dupe. Real regression test tonight 04:00 UTC EventBridge fire (CTO closeout checklist: chain label match, silver-prep fire, zero-dupe).</evidence>
    <project_code>ADVI_ROLLUP</project_code>
    <wave>DH (Dispatcher hygiene — Wave 6)</wave>
    <priority>P1 (gates DH-2/3/4 — chain definitions are the structural foundation)</priority>
  </metadata>

  <references>
    <ref type="superseded">org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/gold-dispatcher-hygiene-cleanup.md (10-item monolith chopped per Andrew 2026-04-15)</ref>
    <ref type="audit_source">Andrew gold_dispatch.sh audit 2026-04-15 (8 real bugs + 6 logic traps)</ref>
    <ref type="subject_file">data/black_diamond/scripts/runner/gold_dispatch.sh</ref>
  </references>

  <objective>
    Clean chain definitions in `gold_dispatch.sh`. This is the structural foundation of the dispatcher cleanup — DH-2/3/4 layer on top of these renamed/deduped chains.

    **Items in scope (4 of the 10 from monolith TO):**
    1. **Delete CHAIN_REBUILD** (line 145) — alias of `full`, dead code with misleading "rebuild" semantic. Remove constant + case arm + help line.
    2. **Dedupe CHAIN_FULL B_01b** — CHAIN_FOUNDATION ends `... B_01 B_01b` and CHAIN_CANONICAL starts `B_00 B_01b ...`. Concatenation runs B_01b twice per nightly. Resolves structurally via item 10.
    5. **Fix canonical help text** (line 343) — shows `B_00 B_02 B_03 C_00 C_01 C_02 C_04`; actual is `B_00 B_01b B_02 B_03 C_00 C_01 C_02 C_04`. Sync.
    10. **Rename CHAIN_FOUNDATION** — split into `CHAIN_DIMENSIONS` (A_* only) + `CHAIN_HOLDINGS_SEED` (B_01 B_01b). Rewrite CHAIN_FULL to concatenate `CHAIN_DIMENSIONS + CHAIN_HOLDINGS_SEED + CHAIN_CANONICAL + CHAIN_DOWNSTREAM`. Closes item 2 structurally.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/runner/gold_dispatch.sh</file>
    </files>
  </scope>

  <wire_contract>
    No runtime behavior change for healthy paths. CHAIN_FULL produces identical script sequence post-cleanup minus the duplicate B_01b execution (B_01b is idempotent — verify pre-ship). External callers using `--chain rebuild` will break (acceptable; alias removed per Andrew direction).
  </wire_contract>

  <acceptance_criteria>
    1. Items 1, 2, 5, 10 applied in one commit.
    2. `bash -n data/black_diamond/scripts/runner/gold_dispatch.sh` exits 0.
    3. `gold_dispatch.sh --help` shows the new chain names (`CHAIN_DIMENSIONS`, `CHAIN_HOLDINGS_SEED`) and the corrected canonical sequence.
    4. `gold_dispatch.sh --chain full --dry-run` script-sequence has no duplicate IDs.
    5. `gold_dispatch.sh --chain rebuild` returns explicit error (alias removed).
    6. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail vs `<expect>` (CTO Rule 7).
    7. MCP COMPLETE to COO with commit hash + diff summary + `--dry-run` sequence output evidence.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>bash -n data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>Exit 0 (baseline syntactically valid).</expect>
        <if_mismatch>Pre-existing syntax error — STOP, surface to COO.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --chain full --dry-run 2>&amp;1 | grep -oE '[A-Z]_[0-9a-z]+' | sort | uniq -c | sort -rn | head -5</run>
        <expect>B_01b appears with count=2. Baselines the dedup target.</expect>
        <if_mismatch>If B_01b already count=1, item 2 is stale — re-baseline.</if_mismatch>
      </step>
      <step>
        <run>grep -n 'CHAIN_REBUILD\|CHAIN_FOUNDATION\|CHAIN_CANONICAL' data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>All 3 patterns present at stated line ranges. Confirms scope.</expect>
        <if_mismatch>Re-baseline against current file; update commit body line refs.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bash -n data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>Exit 0 post-edit.</expect>
        <if_mismatch>Fix syntax before commit.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --chain full --dry-run 2>&amp;1 | grep -oE '[A-Z]_[0-9a-z]+' | sort | uniq -c | awk '$1 &gt; 1'</run>
        <expect>Empty (no script appears more than once).</expect>
        <if_mismatch>Dedup incomplete. STOP.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --help 2>&amp;1 | grep -E 'CHAIN_(DIMENSIONS|HOLDINGS_SEED|CANONICAL|DOWNSTREAM)'</run>
        <expect>All 4 new/preserved chain names appear in help; CHAIN_FOUNDATION absent.</expect>
        <if_mismatch>Help text drift; resync before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit + S3 upload">
      <step>
        <run>aws s3 cp data/black_diamond/scripts/runner/gold_dispatch.sh s3://opal-data-bd/code/runner/gold_dispatch.sh &amp;&amp; aws s3api head-object --bucket opal-data-bd --key code/runner/gold_dispatch.sh --query ETag</run>
        <expect>Upload success; ETag matches local md5.</expect>
        <if_mismatch>Retry; surface to COO if persists.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency description="No live gold chain in flight at edit time (HARD GATE)" status="pending"/>
  </dependencies>

  <next>
    DH-1 close unblocks DH-2/3/4 parallel ship. Tonight's natural EventBridge fire is the first real regression test.
  </next>
</task_order>
