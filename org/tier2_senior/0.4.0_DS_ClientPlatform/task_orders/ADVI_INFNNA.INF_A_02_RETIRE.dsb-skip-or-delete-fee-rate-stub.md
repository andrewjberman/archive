<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.INF_A_02_RETIRE</id>
    <project>ADVI_INFNNA</project>
    <title>INF_A_02.fee_rate_history — skip-in-orchestrator or delete-and-defer until Orion Advisory Fees data lands</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>pending</status>
    <priority>low</priority>
    <estimated_effort>~30 min (verify no consumer + pick option + ship)</estimated_effort>
    <authorized_by>Andrew direct 2026-05-11 — "GO on all 4 in your recommended sequence"</authorized_by>
    <execution_gate>BLOCKED by INF_A_LAYER_TXN-CACHE completion. Sequence #3 of 4.</execution_gate>
  </metadata>

  <references>
    <ref type="parent_audit">A-GROUP-AUDIT findings doc Finding #5</ref>
    <ref type="affected_script">data/orion/scripts/gold/INF_A_02.fee_rate_history.py</ref>
    <ref type="output_path">s3://opal-data-inf/gold/dimensions/fee_rate_history.parquet (0-row stub)</ref>
  </references>

  <context>
    INF_A_02 is a 97-line stub that writes a 0-row parquet to `gold/dimensions/fee_rate_history.parquet` every cascade. Per docstring: "Orion TRN silver does not carry a fee_bps or fee_schedule field. For v1, this script writes an empty parquet stub with the correct schema. When Orion Advisory Fees data becomes available (separate Orion export), this script will be updated to build a full SCD Type 2 fee rate history mirroring BD INF_A_02.fee_rate_history.py."

    Cost: ~1s per cascade + 1 unnecessary S3 PUT (boto3 init + upload of empty parquet).

    Two retirement options:

    **Option A (cleanest):** Delete the script + remove from cascade manifest. Recreate when Orion Advisory Fees data is ready. Risk: any downstream B/C/D script that does `s3.get_object('gold/dimensions/fee_rate_history.parquet')` will 404. Need to verify no consumer exists.

    **Option B (safer):** Add a skip-flag to the cascade orchestrator: `if config.skip_stub_scripts: continue`. Keeps the script file in repo as documentation of intended future schema. Low surface change.

    **Option C (no-op):** Leave as-is. The 1s + 1 PUT cost per cascade is noise.

    Recommend Option B unless `comp-blast` confirms zero consumers, in which case Option A.

    Lowest priority of the 3 audit-derived TOs. Pickup when bandwidth genuinely free.
  </context>

  <scope>
    <step>
      Run `comp-blast` on `gold/dimensions/fee_rate_history` artifact to enumerate downstream consumers. Likely zero (BD's analog feeds C-layer fee_efficiency scripts; INF doesn't have fee_efficiency wired yet).
    </step>

    <step>
      Greppage backstop: `grep -r "fee_rate_history" data/orion/ infra/aws/lambda/` to catch any consumers comp-blast might miss.
    </step>

    <step>
      If zero consumers: Option A. Delete `data/orion/scripts/gold/INF_A_02.fee_rate_history.py`. Remove from cascade manifest. `aws s3 rm s3://opal-data-inf/gold/dimensions/fee_rate_history.parquet` (DESTRUCTIVE — confirm with COO before execution).

      If consumer found: Option B. Add `INF_A_02` to a `cascade_config.skip_stub_scripts` list (or similar) in the orchestrator config. Annotate INF_A_02 source with a "still-skipped-pending-Orion-Advisory-Fees-feed" header comment.
    </step>

    <step>
      Pre-commit gate on any edited .py file.
    </step>

    <step>
      Cascade dry-run (or scoped QA) to confirm A-layer still completes after retirement.
    </step>
  </scope>

  <acceptance_criteria>
    1. comp-blast + grep confirm consumer set is empty (Option A) or enumerate consumers (Option B).
    2. Selected option implemented (delete + S3 rm OR orchestrator skip flag).
    3. Pre-commit gate exits 0.
    4. Cascade or scoped A-layer dispatch completes without A_02 step (or with skip flag honored).
    5. Session log captures decision rationale + comp-blast output + commit SHA.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>`comp-blast gold/dimensions/fee_rate_history`</run><expect>Empty consumer set (likely) OR enumerated downstream nodes.</expect></step>
      <step><run>`grep -r fee_rate_history data/orion/ infra/aws/lambda/`</run><expect>No live consumers (only INF_A_02 self-references and BD analog).</expect></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>`.tools/ds-commit-gate.sh` on edited .py files</run><expect>Exit 0.</expect></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>Scoped A-layer dispatch (if Option A: A_00 → A_01 → A_03 → A_04; if Option B: same with skip flag)</run><expect>A-layer completes successfully without A_02 work.</expect></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None. Independent of A_03 or TXN-CACHE TOs.
  </dependencies>

  <safety_note>
    Option A requires `aws s3 rm` of a deployed artifact — DESTRUCTIVE. Confirm with COO + Andrew before execution. CLAUDE.md autonomy section explicitly excludes "deleting S3 objects" from pre-authorized actions.
  </safety_note>

  <next>On retirement: A-layer cleaner + 1s saved per cascade. Recreate INF_A_02 when Orion Advisory Fees feed lands.</next>

  <draft_note>
    Authored DRAFT by 0.4.0_DS_ClientPlatform~B 2026-05-11 per AC9 scope-creep guard. Awaiting COO ratification + dispatch.
  </draft_note>
</task_order>
