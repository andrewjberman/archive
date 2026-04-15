<task_order>
  <metadata>
    <id>ADVI_ROLLUP.DH-3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-15</date>
    <status>staged</status><!-- Gates on DH-1 close. Can ship parallel with DH-2/4. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>DH (Dispatcher hygiene — Wave 6)</wave>
    <priority>P2 (pure docs)</priority>
  </metadata>

  <references>
    <ref type="superseded">org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/gold-dispatcher-hygiene-cleanup.md (items 7 + 8)</ref>
    <ref type="subject_file">data/black_diamond/scripts/runner/gold_dispatch.sh</ref>
  </references>

  <objective>
    Collapse two-source flag truth into one. Document `--force`. Remove top-of-file FLAGS block.

    **Items in scope (2 of the 10 from monolith TO):**
    7. **Document --force** — top-of-file FLAGS block (line 47-50) omits `--force` entirely. Freshness-gate override with zero discoverability is a foot-gun.
    8. **Sync --no-shutdown docs** — appears in `--help` but missing from top-of-file FLAGS. Two sources of truth out of sync. Andrew preference: collapse to `show_help` single source; remove the top-of-file FLAGS block.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/runner/gold_dispatch.sh</file>
    </files>
  </scope>

  <wire_contract>
    No runtime behavior change. Top-of-file FLAGS block removed; `show_help` becomes the single canonical flag documentation source. `--force` and `--no-shutdown` both documented in `show_help` (was: `--force` undocumented, `--no-shutdown` only in help).
  </wire_contract>

  <acceptance_criteria>
    1. Items 7 + 8 applied in one commit.
    2. `bash -n` exits 0.
    3. `gold_dispatch.sh --help` output documents all flags including `--force` and `--no-shutdown`.
    4. Top-of-file FLAGS comment block removed from script source.
    5. No second-source flag list anywhere in the file (grep verifies).
    6. Session log Compiler Tools reproduces every `<run>` + observed + pass/fail.
    7. MCP COMPLETE with commit hash + `--help` output snippet showing both flags.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>sed -n '40,60p' data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>Top-of-file FLAGS block visible at lines 47-50; baselines the deletion target.</expect>
        <if_mismatch>Re-baseline location of FLAGS block.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --help 2>&amp;1 | grep -E '\-\-force|\-\-no-shutdown'</run>
        <expect>Only `--no-shutdown` appears (current state: `--force` missing from help).</expect>
        <if_mismatch>If `--force` already in help, item 7 partially complete — verify scope.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bash -n data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --help 2>&amp;1 | grep -cE '\-\-force|\-\-no-shutdown'</run>
        <expect>Count = 2 (both flags in help).</expect>
        <if_mismatch>Re-add missing flag.</if_mismatch>
      </step>
      <step>
        <run>grep -nE '^# *FLAGS|^# *Flags:' data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>No matches (top-of-file FLAGS block removed).</expect>
        <if_mismatch>FLAGS block still present — delete.</if_mismatch>
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
    <dependency to="ADVI_ROLLUP.DH-1" description="DH-1 chain definitions land first (help text references chain names)" status="pending"/>
  </dependencies>
</task_order>
