<task_order>
  <metadata>
    <id>ADVI_ROLLUP.DH-6</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- Shipped bd-v2.24.3 2026-04-16 (co-ship with DH-5) -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>DH (Dispatcher hygiene — Wave 6)</wave>
    <priority>P3 (data-correctness gate; logic trap 12 from audit)</priority>
  </metadata>

  <references>
    <ref type="audit_source">Andrew gold_dispatch.sh audit 2026-04-15 — logic trap 12</ref>
    <ref type="subject_file">data/black_diamond/scripts/runner/gold_dispatch.sh</ref>
  </references>

  <objective>
    Freshness gate currently guards `full/downstream/rebuild` chain modes — but `--chain downstream` invoked directly does NOT validate that silver gap dates are filled. Extend the gate to cover `--chain downstream` standalone invocation (and verify any other downstream-only entry points).

    **Why it matters:** `--chain downstream` runs C/D layers against silver. If silver has gap dates (missing forwardfill or missing transactions), downstream layers compute against a hole and produce silently-wrong artifacts. The gate exists for `full` because `full` includes the silver-prep dependencies; `downstream` skips them and therefore needs the gate even more.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/runner/gold_dispatch.sh</file>
    </files>
  </scope>

  <wire_contract>
    `--chain downstream` standalone invocation runs the freshness gate before executing C/D. If gate fails, rejects with explicit error (date list of missing silver partitions). `--force` continues to override.
  </wire_contract>

  <acceptance_criteria>
    1. Freshness gate extended to `--chain downstream`.
    2. `--force` still overrides for `downstream` mode.
    3. Test fire: simulate a missing silver partition (or use a deliberately-stale check window), invoke `--chain downstream --dry-run`, observe gate triggers and lists missing dates.
    4. `bash -n` exits 0.
    5. Help text documents the gate now applies to downstream.
    6. Session log Compiler Tools reproduces every `<run>` + observed + pass/fail.
    7. MCP COMPLETE with commit hash + dry-run transcript showing gate behavior.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>grep -n 'freshness\|gap\|silver_dates\|--force' data/black_diamond/scripts/runner/gold_dispatch.sh | head -20</run>
        <expect>Freshness gate logic visible; current chain-mode guard list (full/downstream/rebuild) confirmed.</expect>
        <if_mismatch>Re-baseline gate location.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bash -n data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --chain downstream --dry-run 2>&amp;1 | grep -iE 'freshness|gap|missing'</run>
        <expect>Gate evaluation visible in dry-run output (PASS or FAIL printed).</expect>
        <if_mismatch>Gate not invoked for downstream mode.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --chain downstream --force --dry-run 2>&amp;1 | grep -iE 'force.*override|gate.*skip'</run>
        <expect>Override message visible.</expect>
        <if_mismatch>--force override broken.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit + S3 upload">
      <step>
        <run>aws s3 cp data/black_diamond/scripts/runner/gold_dispatch.sh s3://opal-data-bd/code/runner/gold_dispatch.sh &amp;&amp; aws s3api head-object --bucket opal-data-bd --key code/runner/gold_dispatch.sh --query ETag</run>
        <expect>ETag matches local md5.</expect>
        <if_mismatch>Retry.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency to="ADVI_ROLLUP.DH-1" description="DH-1 chain definitions land first" status="complete" evidence="516e39da"/>
  </dependencies>
</task_order>
