<task_order>
  <metadata>
    <id>ADVI_ROLLUP.DH-4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-15</date>
    <status>complete</status>
    <evidence>Commit a1a31507 (+31 -9); push `aaccd4e8..a1a31507`; S3 ETag `f91d72c06a6e6a03a0bdb06c413d33ee` @ 22:24:08 UTC. CTO NO-OBJECT 222335Z. Live --bg test PASS: `--single S_00 --bg --dry-run` produced exactly 1 log in /tmp/gold_logs/ (`single_S_00_20260415_182218.log`). bash -n PASS pre+post. Diagnostics line rewritten (grep "run directly" returns no match). 04:00 UTC fire will verify --bg log dedup on PROD.</evidence>
    <project_code>ADVI_ROLLUP</project_code>
    <wave>DH (Dispatcher hygiene — Wave 6)</wave>
    <priority>P2 (logs cleanup, no behavior change)</priority>
  </metadata>

  <references>
    <ref type="superseded">org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/gold-dispatcher-hygiene-cleanup.md (items 4 + 6)</ref>
    <ref type="subject_file">data/black_diamond/scripts/runner/gold_dispatch.sh</ref>
    <ref type="evidence">2026-04-15 17:27 UTC fire produced both `chain_full_20260415_172741.log` AND `full_20260415_172741.log` (orphan in /tmp/gold_logs/)</ref>
  </references>

  <objective>
    Resolve `--bg` log duplication and fix the misleading "diagnostics run directly" comment.

    **Items in scope (2 of the 10 from monolith TO):**
    4. **Dedupe --bg logs** — `--bg` re-invokes itself; wrapper + foreground each compute their own `$log_file` with different timestamps. Wrapper log stays on disk; only foreground uploads via `upload_log`. Decision: skip wrapper log creation entirely (cleaner than uploading both). Wrapper just re-execs into background; logging is foreground's job.
    6. **Fix "E Diagnostics (run directly, not through dispatch)" line** (line 389) — comment is false: S_00 IS run through dispatch (`--chain silver-prep` / `--single S_00`). Rewrite accurately.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/runner/gold_dispatch.sh</file>
    </files>
  </scope>

  <wire_contract>
    Single log file per `--bg` invocation (wrapper log no longer created). Diagnostics comment accurate.
  </wire_contract>

  <acceptance_criteria>
    1. Items 4 + 6 applied in one commit.
    2. `bash -n` exits 0.
    3. After a `--bg` test fire (e.g. `gold_dispatch.sh --single S_00 --bg --dry-run`), `/tmp/gold_logs/` contains exactly one log file (no orphan wrapper log).
    4. The line-389 comment about diagnostics is rewritten to reflect that S_00 IS dispatcher-invoked.
    5. Session log Compiler Tools reproduces every `<run>` + observed + pass/fail.
    6. MCP COMPLETE with commit hash + ls evidence on `/tmp/gold_logs/` post-test-fire.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>sed -n '385,395p' data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>Diagnostics comment visible at line ~389. Baselines text to rewrite.</expect>
        <if_mismatch>Re-baseline line ref.</if_mismatch>
      </step>
      <step>
        <run>grep -n 'log_file\|--bg' data/black_diamond/scripts/runner/gold_dispatch.sh | head -20</run>
        <expect>Two `log_file=` assignments visible (wrapper + foreground branch).</expect>
        <if_mismatch>Re-baseline log path computation.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bash -n data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>rm -f /tmp/gold_logs/*.log; gold_dispatch.sh --single S_00 --bg --dry-run 2>&amp;1; sleep 2; ls /tmp/gold_logs/*.log 2>/dev/null | wc -l</run>
        <expect>Exactly 1 log file in /tmp/gold_logs/ post-fire.</expect>
        <if_mismatch>Wrapper log still being created. Patch.</if_mismatch>
      </step>
      <step>
        <run>grep -n 'diagnostics' data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>The rewritten comment no longer claims diagnostics are "run directly, not through dispatch".</expect>
        <if_mismatch>Comment unchanged — rewrite.</if_mismatch>
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
    <dependency to="ADVI_ROLLUP.DH-1" description="DH-1 chain definitions land first" status="pending"/>
  </dependencies>
</task_order>
