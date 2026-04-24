<task_order>
  <metadata>
    <id>ADVI_ROLLUP.ORPHRELID</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to><!-- base lane, post CP-RES20/RA-P1c/SL-P1 close; DS bandwidth freed -->
    <date>2026-04-24</date>
    <status>pending</status><!-- dispatched 2026-04-24 with GO MCP; DS base has bandwidth post ROLLUP 52/0/3/+1 close -->
    <project_code>ADVI_ROLLUP</project_code>
    <priority>P2 — data-quality cleanup + CTO backlog fold-in; not blocking portal</priority>
    <origin>
      Surfaced by DS~B RAVC4 on ADVI_STAUDT.EOP2025 (2026-04-22 commit 70788788): 164 accounts with null relationship_id in canonical_nna/2025-12-31.parquet ($24.9M AUA; 156 bd source + 7 schwab_imputed + 1 unaccounted) are silently dropped by D_00b's pandas groupby default dropna=True. ~B shipped Option A D_00b fix (`groupby(..., dropna=False)`) to surface them in NMEC. This TO traces the UPSTREAM cause (why accounts lose relationship_id in A_00/B_00/canonical_nna ingestion) + folds in CTO standing-backlog item on `role_aua` validator target.
      CTO FYI accepted 2026-04-24 (MCP 20260424T124110Z post flex-acceptance context) + fold-in validated at MCP 20260424T124217Z (RA-P1c RAVC forward ACK).
    </origin>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (role_aua section) + canonical_nna architecture</ref>
    <ref type="upstream_finding">data/black_diamond/diagnostics/STAUDT/EOP2025/cohort_delta_trace.md (~B's EOP2025 root-cause analysis)</ref>
    <ref type="ds_b_fix">D_00b `groupby(..., dropna=False)` one-liner authorized (RAVC4 filesystem 20260422T205300Z) — ships 23:00Z nightly 2026-04-24. This TO investigates the UPSTREAM (why orphans exist) not the downstream display (already fixed)</ref>
    <ref type="cto_backlog_foldin">CTO MCP 20260424T124110Z (RA-P1c RAVC forward): "Standing backlog item (low priority): role_aua has no target in gold_validate_config.yaml. AC#4 satisfied via manual spot-check. Add to RA cleanup backlog TO when you author orphan-rel-id upstream TO post-23:00Z." — this TO.</ref>
    <ref type="precedent_script">data/black_diamond/scripts/gold/A_00.accounts_dimension.py — source of relationship_id mapping</ref>
    <ref type="precedent_script">data/black_diamond/scripts/gold/B_00.canonical_holdings.py — canonical_nna producer</ref>
    <ref type="precedent_script">data/black_diamond/scripts/gold/C_01c.role_aua_flow_join.py — role_aua producer (RA-P1c)</ref>
  </references>

  <objective>
    Two deliverables in one TO:

    **Deliverable 1 — Orphan relationship_id upstream trace:**
    Identify where in the A_00/B_00 ingestion chain the 164 accounts lose their `relationship_id`. Possible root causes (form hypotheses in Phase 0; gate to test in Phase 1):
    - H1: silver/accounts_dimension OR silver/allocations missing relationship_id values for these accounts (BD/Schwab feed gap)
    - H2: A_00 accounts_dimension join drops relationship_id when upstream source_tag is `schwab_imputed` and imputation doesn't carry rel_id
    - H3: Account-type filter (SLAT/DAF/HSA/corporate entities) intentionally strips rel_id
    - H4: Timing — rel_id was populated at some historical date but got nulled by a later batch update
    Output: classification of root cause + documented fix path (data-fix in upstream OR code-fix in A_00 rel_id propagation OR confirmation that null-rel-id is correct-by-design for this cohort).

    **Deliverable 2 — role_aua gold_validate_config target:**
    Add a validator block for `role_aua` output in `gold_validate_config.yaml`. Fields-presence + nna_txn non-null for non-zero-NNA rows + daily_inflow/outflow sum reconciles to nna_txn within tolerance. Closes RA-P1c AC#4 validate-gap flagged in CTO standing backlog.

    **EXPLICIT SCOPE LOCK:**
    - NO changes to D_00b (~B already shipped dropna-false fix; this TO is upstream only)
    - NO canonical_nna schema change unless trace confirms code-fix in A_00 is the right path AND scope stays minimal
    - NO retroactive rel_id backfill unless Andrew authorizes (potentially large cross-pipeline change)
  </objective>

  <scope>
    <files>
      <file action="investigate">data/black_diamond/scripts/gold/A_00.accounts_dimension.py — trace relationship_id source field + any conditional stripping</file>
      <file action="investigate">data/black_diamond/scripts/gold/B_00.canonical_holdings.py — trace relationship_id propagation to canonical_nna</file>
      <file action="read-only">silver/accounts_dimension (if exists) + silver/allocations recent partition — spot-check rel_id presence for sample 10 of the 164 orphan accounts</file>
      <file action="read-only">canonical_nna/{recent-date}.parquet — confirm 164 null-rel-id cohort current count + account IDs for trace</file>
      <file action="modify">data/black_diamond/scripts/gold/gold_validate_config.yaml — add role_aua validator block (Deliverable 2)</file>
      <file action="create-if-code-fix-path">data/black_diamond/scripts/gold/A_00.accounts_dimension.py OR B_00.canonical_holdings.py — minimal rel_id propagation fix IF trace confirms code-level miss</file>
      <file action="create">data/black_diamond/diagnostics/ROLLUP/orphan_rel_id_trace.md — investigation record</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="trace-doc">
      `data/black_diamond/diagnostics/ROLLUP/orphan_rel_id_trace.md` — investigation findings: 164-cohort account IDs sampled + silver-layer rel_id presence audit + A_00/B_00 code path trace + root-cause classification (H1/H2/H3/H4 or alternative) + proposed fix path.
    </deliverable>
    <deliverable id="fix-if-code-path">
      IF root cause is code-level (H2 most likely): minimal A_00 or B_00 patch to propagate rel_id correctly; IF data-level (H1 most likely): document AE-scope feed-expansion TO (similar to CP-FEEDEXP pattern); IF correct-by-design (H3/H4): document and close.
    </deliverable>
    <deliverable id="role-aua-validator">
      gold_validate_config.yaml role_aua block — covers: field-presence on (date, advisor, role, nna_txn, daily_inflow, daily_outflow, total_aua, fee_earning_aua); nna_txn non-null for rows where cum_nna != 0; sum(daily_inflow) - sum(daily_outflow) ≈ nna_txn delta within tolerance.
    </deliverable>
    <deliverable id="session-log">
      Session log reproducing every `<run>` + observed + pass/fail + root-cause classification.
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">Trace doc ships to `data/black_diamond/diagnostics/ROLLUP/orphan_rel_id_trace.md` with root-cause classification among H1/H2/H3/H4 (or explicit alternative).</ac>
    <ac id="2">Spot-check 10 of the 164 orphan accounts against silver/accounts_dimension (or silver/allocations if accounts_dimension absent for date) — document whether silver has rel_id for them.</ac>
    <ac id="3">If code-fix path chosen: minimal patch shipped with pre-commit-gate clean (py_compile + ds-commit-gate.sh exit 0); if data-fix path chosen: CP-FEEDEXP-style follow-on TO drafted for AE 0.6; if by-design: document rationale.</ac>
    <ac id="4">role_aua validator block added to gold_validate_config.yaml; `comp-validate C_01c --artifact <role_aua sample>` exits 0.</ac>
    <ac id="5">If fix path involves A_00 or B_00 re-run: coordinate with AE 0.6 for full cascade; out-of-scope for this TO to dispatch chain unless trivially cheap.</ac>
    <ac id="6">Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.</ac>
    <ac id="7">MCP COMPLETE to COO + CTO with: root-cause classification, commit hash (or "no code fix — trace-only"), orphan count post-fix (if code-fix), validator block addition confirmation.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="0" when="discovery">
      <step>
        <run>python3 -c "import pyarrow.parquet as pq, pandas as pd; df = pq.read_table('s3://opal-data-bd/canonical/nna/<latest>.parquet').to_pandas(); orphans = df[df['relationship_id'].isna()]; print(len(orphans), orphans['account_id'].head(10).tolist())"</run>
        <expect>~164 orphans (may shift post-dropna-false ship); print 10 sample account IDs for upstream trace.</expect>
        <if_mismatch>If count radically different, ~B's EOP2025 finding may have been date-specific; proceed with current count + account IDs.</if_mismatch>
      </step>
      <step>
        <run>comp-blast A_00</run>
        <expect>Downstream consumers enumerated (B_00, all C-chain, D-chain). Confirm scope of any rel_id change.</expect>
        <if_mismatch>Document any unexpected consumer before patching.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io A_00</run>
        <expect>relationship_id source field identified (silver/accounts_dimension or silver/allocations).</expect>
        <if_mismatch>If rel_id source field absent from A_00 READS, then A_00 code is not the propagation point — investigate B_00 or canonical_nna producer.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="investigation">
      <step>
        <run>python3 -c "import pyarrow.parquet as pq, pandas as pd; sliver = pq.read_table('s3://opal-data-bd/silver/accounts_dimension/<latest>.parquet').to_pandas(); orphans = ['<10 orphan ids from Phase 0>']; subset = sliver[sliver['account_id'].isin(orphans)]; print(subset[['account_id','relationship_id','source_tag']].to_string())"</run>
        <expect>Print rel_id presence for 10 sample orphan accounts in silver layer.</expect>
        <if_mismatch>Records on silver with non-null rel_id → H2 (A_00 propagation bug). Null or absent silver records → H1 (feed gap; AE scope).</if_mismatch>
      </step>
      <step>
        <run>python3 -c "import ast; tree = ast.parse(open('data/black_diamond/scripts/gold/A_00.accounts_dimension.py').read()); [print(n.lineno, ast.dump(n)[:120]) for n in ast.walk(tree) if isinstance(n, ast.Attribute) and hasattr(n,'attr') and n.attr == 'relationship_id']</run>
        <expect>Line-number map of every relationship_id reference in A_00 — use to trace propagation + any conditional null-fill.</expect>
        <if_mismatch>If no references in A_00, relationship_id must be upstream in silver or B_00 layer; trace there.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit (if code-fix path)">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/A_00.accounts_dimension.py data/black_diamond/scripts/gold/gold_validate_config.yaml</run>
        <expect>Exit 0 (yaml doesn't need py_compile but A_00 if touched must pass).</expect>
        <if_mismatch>Fix syntax before commit.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh data/black_diamond/scripts/gold/A_00.accounts_dimension.py data/black_diamond/scripts/gold/gold_validate_config.yaml</run>
        <expect>Exit 0 — py_compile + AST clean.</expect>
        <if_mismatch>Fix before commit (CLAUDE.md Rule 14).</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-validate C_01c --artifact /tmp/role_aua_sample.parquet</run>
        <expect>Exit 0; new role_aua validator block passes on sample.</expect>
        <if_mismatch>Iterate validator block thresholds until exit 0 (expected tolerance on nna_txn delta is ~$1K rounding).</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript deployed A_00 (if code-fix path ONLY)</run>
        <expect>MATCH after S3 upload.</expect>
        <if_mismatch>STALE = re-upload.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource file="data/black_diamond/scripts/gold/A_00.accounts_dimension.py">
      Potentially touched IF code-fix path chosen. Coordinate with AE 0.6 before shipping — A_00 is high-blast-radius (every B/C/D consumer depends on it). No active overlap with other TOs expected.
    </shared_resource>
    <shared_resource file="data/black_diamond/scripts/gold/gold_validate_config.yaml">
      Additive role_aua block; low conflict risk with any other TO.
    </shared_resource>
    <downstream_pending>IF data-fix path: draft CP-FEEDEXP-style follow-on TO for AE 0.6 (BD data-ops inquiry + feed enrichment), not in W4.14 scope.</downstream_pending>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT modify D_00b — ~B owns the dropna-false fix; this TO is upstream only.</rule>
    <rule>Do NOT retroactively backfill rel_id across historical canonical_nna partitions without Andrew authorization.</rule>
    <rule>Do NOT dispatch full A→D cascade from this TO — if code-fix path chosen, coordinate with AE 0.6 for scheduling; don't self-dispatch.</rule>
    <rule>Do NOT expand scope beyond the 164 orphan cohort. Separate investigations (e.g., other null-field drops) are standalone TOs.</rule>
  </do_not>
</task_order>
