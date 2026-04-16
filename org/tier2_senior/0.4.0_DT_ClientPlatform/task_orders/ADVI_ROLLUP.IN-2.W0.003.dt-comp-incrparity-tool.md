<task_order>
  <metadata>
    <id>ADVI_ROLLUP.IN-2.W0.003</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-15</date>
    <status>complete</status>
    <project_code>ADVI_ROLLUP</project_code>
    <wave>7 — IN Wave 0 Foundation</wave>
    <priority>P1 (HARD-BLOCKS Wave 2+; no per-script conversion without parity tool)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/INCREMENTAL_RUNS_DESIGN.md §5 (parity validator spec) + §7 Wave 0</ref>
    <ref type="prereq">ADVI_ROLLUP.IN-2.W0.002 (watermark + atomic_write helper lib)</ref>
    <ref type="related_convention">.tools/comp-* existing tools (comp-pipescript, comp-blast, comp-routes, etc.) for convention reuse</ref>
  </references>

  <objective>
    Ship `.tools/comp-incrparity` — the parity validator that gates every per-script incremental promotion. NO SCRIPT can be converted to incremental without this tool.

    **Tool spec per PRD §5:**
    ```bash
    comp-incrparity <script_id> --date YYYY-MM-DD [--mode quick|deep]
    ```

    Behavior:
    1. Snapshot current production output for the date (`s3://opal-data-bd/gold/.../{script outputs}`).
    2. Run the script in FULL-rebuild mode against the same input snapshot; write to `s3://opal-data-bd/gold/_parity/{script_id}/{run_ts}/full/`.
    3. Run the script in INCREMENTAL mode against the same input snapshot starting from the prior watermark; write to `s3://opal-data-bd/gold/_parity/{script_id}/{run_ts}/incremental/`.
    4. Diff the two outputs:
       - **Quick mode:** byte-diff for parquet; JSON deep-diff for JSON files. Fast fail on any byte/key diff.
       - **Deep mode:** value-by-value comparison with $0.01 numeric tolerance; surfaces specific (row, column) divergences for parquet + (path, old, new) for JSON. Slower but comprehensive.
    5. EXIT 0 on parity match; EXIT 1 + diff report to stderr on any mismatch.

    **CI smoke test:** `comp-incrparity C_06 --mode deep` MUST PASS as part of the ship (C_06 is already incremental, parity must hold by construction — this is the tool's own sanity check).

    **Also support: `comp-incrparity ALL --mode quick`** — iterate all promoted scripts (read a promotion list from `gold/meta/incremental_promoted.json` that W0.004 establishes; empty at ship time). This is the Sunday EventBridge invocation.

    **Report format (on FAIL):** structured JSON to stderr + human-readable summary to stdout. Diff written to `s3://opal-data-bd/gold/_parity_reports/{script_id}/{run_ts}/diff.json`.

    **Implementation:** Python script. Reuse existing comp-* tool scaffolding (look at .tools/comp-pipescript or .tools/comp-blast for the convention).
  </objective>

  <scope>
    <files>
      <file action="create">.tools/comp-incrparity (executable Python script per existing convention)</file>
      <file action="create">tests/comp_tools/test_comp_incrparity.py</file>
      <file action="create">gold/meta/incremental_promoted.json (initial empty list — "[]")</file>
    </files>
    <s3_writes>
      <write>s3://opal-data-bd/gold/_parity/{script_id}/{run_ts}/full/ (staging)</write>
      <write>s3://opal-data-bd/gold/_parity/{script_id}/{run_ts}/incremental/ (staging)</write>
      <write>s3://opal-data-bd/gold/_parity_reports/{script_id}/{run_ts}/diff.json (on FAIL)</write>
    </s3_writes>
  </scope>

  <wire_contract>
    `comp-incrparity <script> --mode {quick|deep}` exits 0 on parity, 1 on mismatch. `comp-incrparity ALL --mode quick` iterates promoted list. Output `gold/meta/incremental_promoted.json` maintained as the source of truth for "which scripts are currently in incremental mode in production."
  </wire_contract>

  <acceptance_criteria>
    1. Tool installed at `.tools/comp-incrparity`, executable from PATH.
    2. `comp-incrparity C_06 --mode deep` exits 0 (smoke test — C_06 already incremental).
    3. `comp-incrparity C_06 --mode quick` exits 0 (same smoke).
    4. Synthetic failure test: inject a deliberate numeric difference in incremental output; tool EXIT 1 + emits diff report at expected path.
    5. `comp-incrparity ALL --mode quick` handles empty `incremental_promoted.json` gracefully (exits 0, no scripts to check).
    6. Unit tests pass.
    7. `gold/meta/incremental_promoted.json` exists with initial empty list `[]`.
    8. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    9. MCP COMPLETE to COO + CTO with tool path, smoke-test transcripts (C_06 PASS + synthetic FAIL + ALL-empty PASS), unit test count.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>ls .tools/comp-* | head -5 &amp;&amp; head -30 .tools/comp-pipescript</run>
        <expect>Existing comp-* tool pattern visible (shebang, arg parsing, output format).</expect>
        <if_mismatch>Locate actual convention.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io C_06</run>
        <expect>C_06 outputs enumerated. Informs what to diff for the smoke test.</expect>
        <if_mismatch>Locate C_06 outputs.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/comp-incrparity C_06 --mode quick 2>&amp;1; echo EXIT=$?</run>
        <expect>EXIT=0.</expect>
        <if_mismatch>Debug; smoke test MUST pass.</if_mismatch>
      </step>
      <step>
        <run>.tools/comp-incrparity C_06 --mode deep 2>&amp;1 | tail -20; echo EXIT=$?</run>
        <expect>EXIT=0; clean summary report.</expect>
        <if_mismatch>Debug.</if_mismatch>
      </step>
      <step>
        <run>pytest tests/comp_tools/test_comp_incrparity.py -v</run>
        <expect>All synthetic failure + empty-promoted + edge cases PASS.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Consumes `_lib/watermark.py` from W0.002.
    - Output `gold/meta/incremental_promoted.json` consumed by W0.004 EventBridge rule.
    - Blocks Wave 2+ per PRD §6 hard gate #2.
  </cross_domain_coordination>

  <dependencies>
    <dependency to="ADVI_ROLLUP.IN-2.W0.002" status="staged"/>
  </dependencies>

  <next>
    W0.003 close → W0.004 (EventBridge weekly parity) can wire up; Wave 2+ per-script conversions can start (each gated on 7-night parity).
  </next>
</task_order>
