<task_order>
  <metadata>
    <id>ADVI_ROLLUP.DH-2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-15</date>
    <status>complete</status>
    <evidence>Commit aaccd4e8 (1 file, +37 -13); push `03a47f45..aaccd4e8`; S3 `opal-data-bd/code/gold/gold_dispatch.sh` ETag `80fb73b1255767228d84ef4878d9498c` @ 22:20:56 UTC. CTO NO-OBJECT 222022Z; COO pre-flagged 222007Z. All 5 acceptance criteria PASS (4 error-path smoke tests + live A_00 dry-run with S3-synced scripts + flag propagation + EXIT 0). bash -n PASS pre+post. Real regression test tonight 04:00 UTC.</evidence>
    <project_code>ADVI_ROLLUP</project_code>
    <wave>DH (Dispatcher hygiene — Wave 6)</wave>
    <priority>P1 (foot-gun closure)</priority>
  </metadata>

  <references>
    <ref type="superseded">org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/gold-dispatcher-hygiene-cleanup.md (items 3 + 9)</ref>
    <ref type="subject_file">data/black_diamond/scripts/runner/gold_dispatch.sh</ref>
  </references>

  <objective>
    Tighten argument validation and resolve the `--incremental` worst-of-both state.

    **Items in scope (2 of the 10 from monolith TO):**
    3. **--incremental restriction (option a chosen by Andrew)** — line 226-231 currently strips `--incremental` for all scripts except A_00 and C_06. Restrict `--incremental` to `--single A_00|C_06` only. Reject all other combinations with explicit error message. Open follow-up TO if/when wider script coverage is desired.
    9. **Arg-parser validation** — currently `--single --bg` silently sets `TARGET="--bg"` and consumes next arg. Add explicit check: if `--chain/--group/--single` is followed by a flag (starts with `--`) or EOF, reject with clear error.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/runner/gold_dispatch.sh</file>
    </files>
  </scope>

  <wire_contract>
    `--incremental` behavior narrows from silent-passthrough to explicit rejection for unsupported scripts — documented deviation, visible-in-error-output. `--single --bg` (or any flag-as-target) starts erroring instead of silently mis-targeting.
  </wire_contract>

  <acceptance_criteria>
    1. Items 3 + 9 applied in one commit.
    2. `bash -n` exits 0.
    3. `gold_dispatch.sh --single --bg` returns explicit error: `--single requires a script id argument (got flag '--bg')` or equivalent.
    4. `gold_dispatch.sh --chain full --incremental` returns explicit error: `--incremental only valid with --single A_00|C_06` or equivalent.
    5. `gold_dispatch.sh --single A_00 --incremental --dry-run` succeeds and propagates `--incremental` to the wrapped script.
    6. `gold_dispatch.sh --single B_01 --incremental` returns explicit error.
    7. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    8. MCP COMPLETE with commit hash + smoke-test transcripts (all 4 above commands).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>grep -n '\-\-incremental\|\-\-single\|\-\-chain\|\-\-group' data/black_diamond/scripts/runner/gold_dispatch.sh | head -30</run>
        <expect>Argument parsing block visible; current line refs match items 3 (226-231) and 9 (arg parser top).</expect>
        <if_mismatch>Re-baseline line refs in commit body.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --single --bg 2>&amp;1 || echo "EXIT=$?"</run>
        <expect>Reproduces the silent-mis-target bug (TARGET becomes `--bg`, `--bg` consumed). Baselines the fix.</expect>
        <if_mismatch>If already errors cleanly, item 9 is stale.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bash -n data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --single --bg 2>&amp;1; echo EXIT=$?</run>
        <expect>Explicit error message + non-zero exit.</expect>
        <if_mismatch>Fix arg validation.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --chain full --incremental 2>&amp;1; echo EXIT=$?</run>
        <expect>Explicit error: `--incremental only valid with --single A_00|C_06` + non-zero exit.</expect>
        <if_mismatch>Fix --incremental restriction.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --single A_00 --incremental --dry-run 2>&amp;1 | head -20</run>
        <expect>Dry-run sequence shows A_00 invoked with `--incremental` flag propagated.</expect>
        <if_mismatch>Restriction over-tightened — A_00 must still accept incremental.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit + S3 upload">
      <step>
        <run>aws s3 cp data/black_diamond/scripts/runner/gold_dispatch.sh s3://opal-data-bd/code/runner/gold_dispatch.sh &amp;&amp; aws s3api head-object --bucket opal-data-bd --key code/runner/gold_dispatch.sh --query ETag</run>
        <expect>ETag matches local md5.</expect>
        <if_mismatch>Retry; surface to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency to="ADVI_ROLLUP.DH-1" description="DH-1 chain definitions must land first (renamed chains affect arg-parser context)" status="pending"/>
  </dependencies>
</task_order>
