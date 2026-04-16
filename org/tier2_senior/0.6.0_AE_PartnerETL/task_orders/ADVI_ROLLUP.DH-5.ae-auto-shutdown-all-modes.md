<task_order>
  <metadata>
    <id>ADVI_ROLLUP.DH-5</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-15</date>
    <status>staged</status><!-- Stays staged; lower priority follow-up to DH-1..DH-4 -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>DH (Dispatcher hygiene — Wave 6)</wave>
    <priority>P3 (cost optimization; logic trap 11 from audit)</priority>
  </metadata>

  <references>
    <ref type="audit_source">Andrew gold_dispatch.sh audit 2026-04-15 — logic trap 11</ref>
    <ref type="subject_file">data/black_diamond/scripts/runner/gold_dispatch.sh</ref>
  </references>

  <objective>
    **Item A — Auto-shutdown all modes (logic trap 11 from monolith audit):** Auto-shutdown currently fires only for `MODE=chain`. `--group D` and `--single X` modes never trigger shutdown — leaves the c6i.16xlarge runner warm indefinitely after ad-hoc invocations. Extend auto-shutdown to all invocation modes (default ON; `--no-shutdown` opt-out remains the override).

    **Cost framing:** PROD runner is bd-gold-layer-runner (c6i.16xlarge per memory `feedback_ec2_gold_runner_sizing.md`). At ~$2.72/hr on-demand, every forgotten warm hour after an ad-hoc run is real cost. QA runner (bd-gold-qa-runner) is the same instance type.

    **Item B — B_01 `holdings_lots` terminal-output audit (DS~A peer-review flag per AE 0.6 MCP 221649Z):** Compiler shows B_01's `holdings_lots` S3 output as terminal — nothing reads it. Two possibilities: (1) compiler missed a dynamic reader (e.g. B_01b uses dynamic key resolution per DH-3 item 12, may consume holdings_lots; verify after DH-3 lands), OR (2) holdings_lots is a dead artifact and B_01 only feeds downstream via accounts_dimension overwrite + DynamoDB bd-securities to B_01b. Audit decision: either document the dynamic reader OR remove the dead emit from B_01. If item B reveals a dead-emit, ship the removal in same commit.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/runner/gold_dispatch.sh</file>
    </files>
  </scope>

  <wire_contract>
    All invocation modes (`--chain`, `--group`, `--single`) auto-shutdown on completion unless `--no-shutdown` is passed. Behavior change for `--group` and `--single` users (previously left warm). Document in `show_help`.
  </wire_contract>

  <acceptance_criteria>
    1. Auto-shutdown logic extended to MODE=group and MODE=single.
    2. `--no-shutdown` opt-out continues to work for all modes.
    3. `--dry-run` does NOT trigger shutdown (no actual run = no shutdown).
    4. Help text documents the behavior change.
    5. `bash -n` exits 0.
    6. Test fire: `gold_dispatch.sh --single S_00 --no-shutdown --dry-run` shows shutdown SKIPPED in dry-run output.
    7. Session log Compiler Tools reproduces every `<run>` + observed + pass/fail.
    8. MCP COMPLETE with commit hash + dry-run transcript demonstrating shutdown gate.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>grep -n 'shutdown\|MODE=' data/black_diamond/scripts/runner/gold_dispatch.sh | head -20</run>
        <expect>Shutdown logic visible, gated on `MODE=chain`. Confirms scope.</expect>
        <if_mismatch>Re-baseline.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bash -n data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --single S_00 --dry-run 2>&amp;1 | grep -i shutdown</run>
        <expect>Output shows shutdown intent for single-mode (would shutdown if not dry-run).</expect>
        <if_mismatch>Extension incomplete.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --single S_00 --no-shutdown --dry-run 2>&amp;1 | grep -i shutdown</run>
        <expect>Output shows shutdown SKIPPED due to --no-shutdown.</expect>
        <if_mismatch>Opt-out broken.</if_mismatch>
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
    <dependency to="ADVI_ROLLUP.DH-2" description="DH-2 arg validation lands first (clean target id parsing)" status="complete" evidence="aaccd4e8"/>
  </dependencies>
</task_order>
