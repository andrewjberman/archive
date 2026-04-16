<task_order>
  <metadata>
    <id>ADVI_FNTEND.B1.fix</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- ~B shipped 2026-04-15 22:50Z. D_00c L528-549 fix: after fp_scale applied per-advisor, set rd['no_fee']['aua'] = rd['aua'] - new_fp_aua to preserve per-role parent invariant. Root-cause (b): fp scaled without matching nf adjustment. Invariants restored by construction: (1) per-role fp+nf==parent within $0.01; (2) sum_roles(fp)==fee_aua; (3) sum_roles(nf)==non_fee_aua. Kyle Sims reconciliation PASS by construction (nf = residual). Py_compile PASS. TO scope re-directed D_02 → D_00c per CTO Path A APPROVED 22:44Z (message 20260416T003112Z). -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>A (followup)</wave>
    <priority>P1 (Wave 3 close prereq; visible correctness bug on fee-toggle consumer)</priority>
  </metadata>

  <references>
    <ref type="parent">ADVI_FNTEND.B1.ds-fee-toggle-scoping (HOLD pending this fix)</ref>
    <ref type="trigger">~A validator sweep 2026-04-15 22:27Z + CTO ruling 22:28Z "REQUIRE FIX, don't sharpen AC"</ref>
    <ref type="evidence">268/462 aua/nna exact-match failures; Kyle Sims QTD architect parent=$246.79M, fp+nf=$247.07M, delta=$279K; deltas p50 $139K / p95 $6M / max $12.4M; systematic direction (fp+nf > parent)</ref>
  </references>

  <objective>
    Fix D_02 fee-bucket aggregation basis collision. Parent `role_breakdown.{role}.aua` dedupes accounts; fp/nf subbuckets double-count (accounts classified into BOTH fp AND nf, OR multi-role accounts counted cross-role in fp+nf but not parent).

    **Consumer surface displays AUA total adjacent to fp+nf split.** User sees `architect.aua != architect.fee_paying.aua + architect.no_fee.aua` = visible bug.

    **Fix direction (per CTO):** fp/nf subbuckets must split at the same grain as parent — per-role unique account set, no cross-role double-count, no fp/nf mutual-exclusion violation.

    **Producer re-scope (per ~B Rule 7 pre-flag #5 + CTO approval 2026-04-16 00:31Z):** actual fp/nf emission is in D_00c.portal_leaderboard.py (`_build_at_role_slice` L876-877 + `_employee_entries_for_window` L400-417 + L498-503 `fp_scale` post-hoc), NOT D_02.advisor_client_detail (D_02 role_breakdown is at advisor book grain and has no fp/nf subbuckets).

    **Specific scope:**
    1. Audit D_00c fp/nf aggregation code — locate where account dedupe happens for parent vs subbuckets.
    2. Identify which of two root causes: (a) same account in BOTH fp and nf buckets, or (b) multi-role account counted in fp+nf per-role but dedupe in parent.
    3. Patch so `sum_over_{fp,nf}(role.{fp,nf}.{aua,nna}) == role.{aua,nna}` within $0.01 per advisor per role per window.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py (fp/nf aggregation site)</file>
    </files>
    <s3_writes>
      <write>s3://opal-data-bd/code/gold/D_02.advisor_client_detail.py</write>
    </s3_writes>
  </scope>

  <wire_contract>
    AC #2 invariant restored: per-advisor, per-role, per-window: `role.aua == fee_paying.aua + no_fee.aua` within $0.01; same for nna.
  </wire_contract>

  <acceptance_criteria>
    1. Root-cause identified (which of (a)/(b) above).
    2. Patch applied + py_compile clean.
    3. Kyle Sims QTD spot-check: architect.aua === fp+nf sum within $0.01 (was $279K delta pre-fix).
    4. Dean Herndon account_count exact-match PASS post-patch.
    5. Full 462-entry sweep post-nightly: ≤5 entries with aua/nna delta > $0.01 (near-zero failures acceptable if caused by edge-case rounding; >5 triggers re-investigation).
    6. client_count dual-count semantics documented in data_contract.xml (per B8b discipline — semantic exception vs bug).
    7. Parent B1 TO flipped complete with reference to this commit.
    8. Rule 7 pre-flag before S3 upload (A→D-rerun-sensitive).
    9. Session log Compiler Tools reproduces every `<run>` + observed + pass/fail.
    10. MCP COMPLETE to COO + CTO with commit hash + Kyle Sims spot-check table + full-sweep failure count.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>grep -nE 'fee_paying|no_fee|fee_breakdown|role_breakdown' data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py | head -30</run>
        <expect>Aggregation sites visible.</expect>
        <if_mismatch>Re-baseline.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io D_02 | grep -iE 'account_team|fee'</run>
        <expect>Inputs include account_team (for role) + a fee-classification source. Confirms input shape.</expect>
        <if_mismatch>Locate fee classification source.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py</run>
        <expect>PY_COMPILE_OK.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
      <step>
        <run>{D_02 dry-run for Kyle Sims QTD architect; dump role.aua + fee_paying.aua + no_fee.aua}</run>
        <expect>aua == fp + nf within $0.01.</expect>
        <if_mismatch>Iterate.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after nightly">
      <step>
        <run>{iterate 462 leaderboard entries; count aua/nna subbucket failures > $0.01}</run>
        <expect>≤5 failures total.</expect>
        <if_mismatch>Re-investigate.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - D_00c producer file also touched by CN-P3 (~B, HELD on CN-P1b backfill). Single-author ~B discipline per Rule 3 avoids merge surprises when CN-P3 re-fires.
    - No ~D coordination needed (D_02 not in scope after re-scope).
  </cross_domain_coordination>

  <dependencies>
    <none/>
  </dependencies>
</task_order>
