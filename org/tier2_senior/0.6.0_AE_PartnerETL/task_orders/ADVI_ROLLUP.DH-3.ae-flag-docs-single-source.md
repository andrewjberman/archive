<task_order>
  <metadata>
    <id>ADVI_ROLLUP.DH-3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- Shipped 2026-04-16 12:55 UTC in 0fc54608 -->
    <evidence>
      Commit `0fc54608` feat(dh-3): collapse dispatcher flag docs to show_help + compiler visibility fixes (5 files).
      S3 uploads (s3://opal-data-bd/code/gold/):
        - gold_dispatch.sh ETag f98f58163a13f0c816113a50c0b84f76
        - B_01.holdings_lots.py ETag a6ee33be1181cc27f1244eddf125fa94
        - B_01b.classify_new_securities.py ETag a220a612e2db4516d5ad9647e1b08e5d
        - lib/s3_layout.py ETag 65a58edb0c56454bea6ca24b782cdbc8
      Acceptance criteria:
        1. Items 7+8+11+12 in one commit (bundled)
        2. bash -n gold_dispatch.sh: exit 0
        3. --help docs --force AND --no-shutdown: confirmed
        4. Top-of-file FLAGS block removed: grep '^# *FLAGS|^# *Flags:' matches zero
        5. No second-source flag list: confirmed
        6. Session log with Compiler Tools: written 2026-04-16 session log
        7. MCP COMPLETE: see DH-7 combined closeout (same session)
      Compiler gains:
        - B_01 WRITES 4 -> 3 (ACCOUNTS_DIMENSION substring-alias false-positive removed via inline)
        - B_01b "(none detected)" -> READS(2) + WRITES(1) (import from lib.s3_layout)
      CTO ACK 2026-04-16 12:56 UTC; COO ACK 2026-04-16 12:56 UTC.
    </evidence>
    <project_code>ADVI_ROLLUP</project_code>
    <wave>DH (Dispatcher hygiene — Wave 6)</wave>
    <priority>P2 (pure docs)</priority>
  </metadata>

  <references>
    <ref type="superseded">org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/gold-dispatcher-hygiene-cleanup.md (items 7 + 8)</ref>
    <ref type="subject_file">data/black_diamond/scripts/runner/gold_dispatch.sh</ref>
  </references>

  <objective>
    Collapse two-source flag truth into one + audit pipeline-graph hygiene flagged by ~A peer review.

    **Items in scope (4 — items 7+8 from monolith + 2 audit additions from DS~A peer-review of bd-v2.24.1+DH-1 per AE 0.6 MCP 221649Z):**
    7. **Document --force** — top-of-file FLAGS block (line 47-50) omits `--force` entirely. Freshness-gate override with zero discoverability is a foot-gun.
    8. **Sync --no-shutdown docs** — appears in `--help` but missing from top-of-file FLAGS. Two sources of truth out of sync. Andrew preference: collapse to `show_help` single source; remove the top-of-file FLAGS block.
    11. **A_00 + B_01 dual-writer audit on `gold/dimensions/accounts_dimension_latest.parquet`** — compiler shows both as writers to the same key. Either B_01 enriches with holdings-sourced columns A_00 can't know about (OK, document the enrichment surface in a comment), OR it's vestigial dead code from prior refactor (remove from B_01). Audit + decide + document or remove.
    12. **B_01b dynamic-key compiler invisibility** — `comp-pipescript io B_01b` returns "(none detected)" because B_01b uses `f'{PREFIX}/...'` + `s3.list_objects`. Future dependency regressions won't be caught. Add one-line static S3 key constants at top of B_01b so compiler can trace I/O. (Doesn't change runtime behavior; restores graph visibility.)
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
