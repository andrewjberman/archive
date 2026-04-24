<task_order>
  <metadata>
    <id>ADVI_INFLEC.SCOPEFIX</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to><!-- ~A lane per Andrew 2026-04-22 INFLEC DS reassignment + 2026-04-24 scope-bug halt -->
    <date>2026-04-24</date>
    <status>complete</status><!-- GO fired 2026-04-24 post CTO contract review (MCP 20260424T14xxZ). COMPLETE 2026-04-24 — commit 2d3de276 by 0.4.0_DS_ClientPlatform~A. S3 MATCH verified MD5 655ce81e7280c49b5b48aecab6b4f185. Phase 0 guards ship (ValueError on col-absent + zero-cohort). Filter applied in build_trn_silver()+build_aum_silver()+build_accounts_dim(). gold_validate_config.yaml created with SCOPEFIX assertions. -->
    <project_code>ADVI_INFLEC</project_code>
    <priority>P0 — HIGHEST. Blocks all INF pipeline work (W4.14, Q8/Q9/Q10, W4.13b, W5.1 DE); Andrew directive 2026-04-24 on cross-firm bug halt</priority>
    <origin>
      Scope bug surfaced 2026-04-24 by AE 0.6.1 mid-W4.13 PROD chain. Orion silver is cross-firm aggregate (multi-firm share on Orion platform); I_A00/I_A01 lack firm filter. Andrew direct 2026-04-24: "429.4m AUA is not inflection AUA. Inflection AUA is around 193m. You need to make sure that we can reliably and appropriately scan based on inflection AUA, not orion data in aggregate."
      Andrew follow-up confirmed: "Scope A is correct" = `rep_name == "Inflection Wealth Management"` filter (CTO brief §8.1 row 1: 287 HH, $193.6M, 29% of aggregate).
      CTO contract review MCP 20260424T14xxZ: 4 rulings + DE gate note.
    </origin>
  </metadata>

  <references>
    <ref type="andrew_directive">Direct chat 2026-04-24 "Scope A is correct" + "$193m" target</ref>
    <ref type="cto_contract_review">MCP 20260424T14xxZ — Option 1 silver-layer ENDORSED (Option 2 rejected); normalize predicate; Phase 0 guard MANDATORY; threshold $180M-$200M banded</ref>
    <ref type="ae_patch_analysis">AE 0.6.1 MCP 20260424T13xxZ — silver-layer rationale + expected output table</ref>
    <ref type="cto_brief">docs/briefs/cto-brief-inflection-partner-data-investigation.md §8.1 — rep cohort breakdown (authoritative source for filter target)</ref>
    <ref type="halted_work">W4.13 PROD chain halted (SSM stopped); W4.14 B-chain paused; Q8/Q9/Q10 paused; W5.1 DE signal held; platinum/firm + advisors + clients quarantined to `_quarantine_scope_bug_20260424/` prefix</ref>
    <ref type="ae_collateral">AE 0.6.1 owns `data/inf/config/dim_inf_advisor_office.csv` rewrite (11 rows → 1 row) — separate scope, fold into W4.13b prep</ref>
  </references>

  <objective>
    Add a firm-scope filter at the silver layer of the Orion ingestion pipeline, filtering to the "Inflection Wealth Management" rep cohort only. Single filter point; no gold-layer touch-points.

    **EXPLICIT SCOPE LOCK (CTO-ruled):**
    - **Option 1 silver-layer ONLY.** Do NOT implement Option 2 (gold-layer N touch-points) — it is the same anti-pattern that produced the original scope bug.
    - **NO gold-script modifications** in this TO (I_A00/I_A01/I_A04/I_C01 etc. all stay as-is; they'll naturally read scope-filtered silver).
    - **NO dim_inf_advisor_office.csv edits** — AE 0.6.1 owns that rewrite.
    - **NO W4.13b re-dispatch** — AE 0.6.1 owns post-SCOPEFIX SSM after CSV rewrite + SCOPEFIX MATCH confirmation.
    - **NO retroactive backfill** — silver forward-only; current bugged silver partitions will be overwritten by scope-filtered re-run.
  </objective>

  <scope>
    <files>
      <file action="modify">data/orion/scripts/silver/convert_orion_to_silver.py — add silver-layer rep_name filter with mandatory Phase 0 guard (CTO-ruled normalization + cohort-count assertion)</file>
      <file action="modify">data/orion/scripts/silver/gold_validate_config.yaml (if validator exists for silver) OR data/orion/scripts/gold/gold_validate_config.yaml — add row-count sanity validator: post-filter silver TRN row count within sanity band (e.g., 500K-2M) + post-filter unique rep_name == 1 ("Inflection Wealth Management")</file>
      <file action="read-only">Raw Orion source (silver input path) — confirm `rep_name` column presence + values for cohort-count Phase 0 check</file>
    </files>
  </scope>

  <wire_contract>
    **Filter predicate (CTO-required normalization):**
    ```python
    NORMALIZED_INFLECTION_REP = "inflection wealth management"

    # Phase 0 guard (MANDATORY per CTO ruling):
    if 'rep_name' not in df.columns:
        raise ValueError(
            f"SCOPEFIX Phase 0 failure: 'rep_name' column not found in source DataFrame. "
            f"Available columns: {df.columns.tolist()}"
        )

    normalized_rep = df['rep_name'].str.strip().str.lower()
    cohort_count = (normalized_rep == NORMALIZED_INFLECTION_REP).sum()
    if cohort_count == 0:
        raise ValueError(
            f"SCOPEFIX Phase 0 failure: zero rows matched '{NORMALIZED_INFLECTION_REP}' "
            f"after normalization. Unique rep_names in source: {df['rep_name'].unique().tolist()}"
        )

    # Apply filter (post-guard):
    df_filtered = df[normalized_rep == NORMALIZED_INFLECTION_REP].copy()
    ```

    **Integration point:** inside `convert_orion_to_silver.py` immediately after the raw-Orion DataFrame is loaded and column normalization is complete, BEFORE any partitioning/write operations. Single filter point, single logical block.

    **Expected post-filter characteristics (per CTO brief §8.1 row 1):**
    - Row count: ~1.25M TRN (vs ~5M aggregate)
    - Unique rep_names post-filter: exactly 1 (the Inflection cohort)
    - household count: ~287
    - Downstream total_aua: ~$193.6M (within $180M-$200M CTO-banded threshold)
  </wire_contract>

  <deliverables>
    <deliverable id="filter-patch">
      `convert_orion_to_silver.py` patch: normalized predicate + mandatory Phase 0 column-exists + cohort-count-nonzero guards + ValueError on either failure with explicit diagnostic message.
    </deliverable>
    <deliverable id="validator-block">
      gold_validate_config.yaml (or silver validator if separate): post-filter silver TRN row count sanity band + unique rep_name cardinality == 1 assertion.
    </deliverable>
    <deliverable id="commit-ship">
      Pre-commit gate (py_compile + ds-commit-gate.sh) clean; commit under ~A author with --only pathspec; push CLOUD; upload to `s3://opal-data-inf/code/silver/convert_orion_to_silver.py`; `comp-pipescript deployed` MATCH.
    </deliverable>
    <deliverable id="handoff-ack">
      MCP COMPLETE to COO with commit hash + MATCH confirmation + Phase 0 guard execution evidence (run it locally against bugged silver input to verify cohort_count > 0 before ship) — signals AE 0.6.1 to proceed with W4.13b re-dispatch coordination.
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">Filter implemented at Option 1 silver-layer location only. No gold-script modifications. CTO ruling enforced.</ac>
    <ac id="2">Predicate uses normalization: `.str.strip().str.lower() == "inflection wealth management"`. NOT exact string match on raw `rep_name`.</ac>
    <ac id="3">Phase 0 guard ships as HARD ValueError on: (a) `rep_name` column absent, (b) normalized cohort count == 0. Both with explicit diagnostic messages including available columns / unique rep_names for debuggability.</ac>
    <ac id="4">gold_validate_config.yaml (or silver validator) block added: post-filter TRN row count in [500K, 2M] sanity band + unique rep_name cardinality == 1. `comp-validate` on silver output exits 0.</ac>
    <ac id="5">Pre-commit gate (py_compile + ds-commit-gate.sh) exit 0 on modified file(s).</ac>
    <ac id="6">`comp-pipescript deployed convert_orion_to_silver` MATCH post-S3-upload.</ac>
    <ac id="7">Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail vs `<expect>` + includes Phase 0 guard dry-run evidence (cohort_count > 0 output).</ac>
    <ac id="8">MCP COMPLETE to COO with: commit hash + MATCH confirmation + Phase 0 dry-run output + next-step handoff to AE 0.6.1 for W4.13b re-dispatch.</ac>
    <ac id="9">Zero modifications to: I_A00, I_A01, I_A04, I_C01, any other gold script, dim_inf_advisor_office.csv, or any platinum artifact — scope lock per CTO.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="0" when="discovery — MANDATORY pre-write">
      <step>
        <run>python3 -c "import pyarrow.parquet as pq; df = pq.read_table('s3://opal-data-inf/silver/trn/<latest partition>.parquet').to_pandas(); assert 'rep_name' in df.columns, f'rep_name absent; cols={df.columns.tolist()}'; print('rep_name col present'); print(df['rep_name'].str.strip().str.lower().value_counts().head(15))"</run>
        <expect>rep_name column present; "inflection wealth management" appears in value_counts with non-zero count. Print confirms cohort_count > 0 at current silver snapshot.</expect>
        <if_mismatch>STOP. If column absent OR cohort_count == 0, MCP COO immediately with observed columns/values — filter-predicate may need revision before code ship.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "# Same df; count rows where rep_name normalized matches; assert within sanity band 500K-2M"</run>
        <expect>Row count ≈ 1.25M (per CTO brief §8.1 expected value; anywhere in [500K, 2M] is sanity-band PASS).</expect>
        <if_mismatch>If count wildly different (e.g., 100K or 5M+), filter-predicate may be wrong — MCP COO with observed counts before proceeding.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io convert_orion_to_silver</run>
        <expect>READS + WRITES enumerated; identify exact integration point post-column-normalization pre-partition-write.</expect>
        <if_mismatch>If script structure differs from expected, document in Phase 0 session-log entry.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="before write">
      <step>
        <run>comp-blast convert_orion_to_silver</run>
        <expect>Downstream consumers = entire INF gold chain. Confirms single-point-of-filter = everything inherits correctly.</expect>
        <if_mismatch>Unexpected consumer = investigate before writing.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/orion/scripts/silver/convert_orion_to_silver.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax (CLAUDE.md Rule 14).</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/scripts/silver/convert_orion_to_silver.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix AST / undefined-name.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "# Dry-run the patched convert_orion_to_silver.py's filter block on a recent silver input; verify cohort_count > 0 + filtered row count ≈ 1.25M + unique rep_name cardinality == 1"</run>
        <expect>Phase 0 guard passes + filter produces expected row count + single rep_name.</expect>
        <if_mismatch>Filter block bug; iterate before commit.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-pipescript deployed convert_orion_to_silver</run>
        <expect>MATCH.</expect>
        <if_mismatch>Re-upload.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "# Optional: dry-trigger silver conversion on a small partition; verify silver output has single rep_name"</run>
        <expect>Post-filter silver partition has unique rep_name == {"inflection wealth management"} (normalized).</expect>
        <if_mismatch>Filter not applied in end-to-end flow; debug.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource file="data/orion/scripts/silver/convert_orion_to_silver.py">
      Low-collision: no other INF TO touches this file today. AE 0.6.1's dim_inf_advisor_office.csv rewrite is parallel + non-overlapping.
    </shared_resource>
    <downstream_handoff>
      On SCOPEFIX MCP COMPLETE + MATCH: AE 0.6.1 proceeds with:
      1. `dim_inf_advisor_office.csv` rewrite (1 row; their scope)
      2. W4.13b SSM re-dispatch (`--chain full` from I_A00 — may be feasible end-to-end now that silver is ~1.25M rows vs ~5M)
      3. Scope-corrected platinum artifacts emit to live paths (NOT quarantine prefix)
      4. DE briefing on advisor count 9 → 1 (per CTO DE gate note) BEFORE W5.1 signal fires
    </downstream_handoff>
    <w5_1_de_gate>
      CTO MCP 20260424T14xxZ mandatory DE briefing: "platinum/advisors/ will drop from 9 subdirs → 1 post-SCOPEFIX. Portal components designed expecting N advisors will see 1 Inflection Wealth Management entity. DE must be briefed on this before any W5.x component work starts. Do not lift W5.1 without this briefing."
      COO owns routing this briefing to DE when W4.13b re-dispatch completes.
    </w5_1_de_gate>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT implement Option 2 (gold-layer filter). CTO ruling: "Option 2 is the same anti-pattern that produced the original scope bug."</rule>
    <rule>Do NOT use exact string match on raw `rep_name`. Normalization (strip + lower) is mandatory.</rule>
    <rule>Do NOT skip Phase 0 guards (column-exists + cohort-count > 0). Hard AC.</rule>
    <rule>Do NOT modify gold scripts, dim_inf_advisor_office.csv, or platinum artifacts. Scope lock.</rule>
    <rule>Do NOT dispatch W4.13b re-run. That's AE 0.6.1 scope post your MATCH confirmation + AE CSV rewrite.</rule>
    <rule>Do NOT unblock W4.14 / Q8 / Q9 / Q10 autonomously. Those resume on COO dispatch post-W4.13b PASS.</rule>
  </do_not>
</task_order>
