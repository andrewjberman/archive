<task_order>
  <metadata>
    <id>ADVI_ROLLUP.W4-CG</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-15</date>
    <status>staged</status><!-- HARD GATE: ALL of RA-P2, RA-P2b, RA-P3, CN-P2, CN-P3, RA-P1b, CN-P1b must PASS before this fires -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>4 (Structural convergence — closeout gate)</wave>
    <priority>P1 (formal Wave 4 closure; without this we ship with consumers silently disagreeing)</priority>
  </metadata>

  <references>
    <ref type="trigger">CTO redline 2026-04-15 21:43Z — ~B's RA-P3 Rule 7 pre-flag exposed missing convergence check between cross-consumer canonical readers</ref>
    <ref type="prd">docs/architecture/ROLE_AUA_CANONICAL_CONVERGENCE_PLAN.md</ref>
    <ref type="prd">docs/architecture/ADVI_CANNNA_PLAN.md</ref>
  </references>

  <objective>
    Validate that all consumers of canonical role_aua + nna_atomic agree within $0.01 for Travis Penfield + 5 spot-check advisors after every Wave 4 cutover lands. Without this gate, we ship Wave 4 with three D_02-side surfaces (summary, timeseries roll-up) and one D_00c surface (leaderboard) and one D_01 surface (partner_analytics) potentially disagreeing on the same advisor x role x window, with no formal close gate.

    **Validation matrix:**

    For each (advisor, role) in {Travis Penfield, 5 spot-check advisors} × {architect, lead, support, ...all roles in the canonical schema}:

    | Surface | Source | Expected behavior |
    |---------|--------|-------------------|
    | leaderboard.json (D_00c, RA-P3) | canonical/role_aua/{latest}.parquet | sum-by-role per latest date |
    | summary.role_breakdown.{role}.aua (D_02, RA-P2 snapshot) | canonical/role_aua/{latest}.parquet | sum-by-role per latest date |
    | timeseries.{role}_aua data[-1] (D_02, RA-P2b) | canonical/role_aua/{date}.parquet per-date | last point matches the snapshot |
    | partner_analytics.views.role.{role} (D_01, RA-P4) | canonical/role_aua/{latest}.parquet | sum-by-role per latest date |

    Identical pattern for nna_atomic (CN-P2/P3/P4 + CN-P1b backfill).

    **Spot-check advisor selection:** Travis Penfield + Sydney Cobb + Kyle Sims + alex_bright + collin_plotts + 1 random from leaderboard top-20 outside this set.

    **Acceptance gate is binary:** any pair-wise disagreement > $0.01 on any (advisor, role, surface) triple = REWORK on the cutover that produces the disagreeing value. Identify which cutover caused the divergence and surface to CTO + COO before declaring Wave 4 complete.
  </objective>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/diagnostics/wave4_cross_consumer_convergence.py — one-off diagnostic script computing the matrix</file>
      <file action="create">docs/data/2026-04-{XX}_wave4_convergence_evidence.md — output evidence with full table</file>
    </files>
    <s3_reads_only/>
  </scope>

  <wire_contract>
    Read-only diagnostic. No S3 writes. Produces evidence doc + script. Commits both.
  </wire_contract>

  <acceptance_criteria>
    1. Diagnostic script created and runs against post-cutover platinum + canonical artifacts.
    2. Evidence doc contains full table (6 advisors × N roles × 4 surfaces for role_aua; same for nna_atomic).
    3. ALL pair-wise comparisons within $0.01 OR each divergence documented with root cause + remediation TO reference.
    4. If any divergence > $0.01: surface to CTO + COO with diagnosis BEFORE declaring Wave 4 complete.
    5. Session log Compiler Tools reproduces every `<run>` + observed + pass/fail.
    6. MCP COMPLETE to COO + CTO with: evidence doc path, table summary (PASS count / FAIL count), divergence remediation status if any.
    7. Once PASS: COO updates project JSON Wave 4 status → complete; REGISTRY entry rewritten.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>aws s3 ls s3://opal-data-bd/gold/canonical/role_aua/ | wc -l &amp;&amp; aws s3 ls s3://opal-data-bd/gold/canonical/nna_atomic/ | wc -l</run>
        <expect>Both partition counts at backfilled levels (RA-P1b + CN-P1b complete).</expect>
        <if_mismatch>Backfills not closed — STOP. Cannot run convergence gate without full canonical.</if_mismatch>
      </step>
      <step>
        <run>for to in RA-P2 RA-P2b RA-P3 RA-P4 CN-P2 CN-P3 CN-P4 RA-P1b CN-P1b; do grep -l "$to" org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/*.md | xargs grep -l 'status>complete'; done</run>
        <expect>All 9 TOs marked complete.</expect>
        <if_mismatch>Wave 4 not yet ready for convergence gate. STOP, surface to COO.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse role_aua &amp;&amp; comp-platinum reverse nna_atomic</run>
        <expect>Lists all consumer surfaces. Confirms the matrix is exhaustive.</expect>
        <if_mismatch>If consumer surface missing from matrix, extend the validation script.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python data/black_diamond/scripts/diagnostics/wave4_cross_consumer_convergence.py --report-format markdown</run>
        <expect>Full table output; row count = 6 advisors × N roles × 4 surfaces × 2 metrics.</expect>
        <if_mismatch>Script bug — fix.</if_mismatch>
      </step>
      <step>
        <run>python data/black_diamond/scripts/diagnostics/wave4_cross_consumer_convergence.py --fail-on-divergence; echo EXIT=$?</run>
        <expect>EXIT=0 (all within $0.01).</expect>
        <if_mismatch>EXIT=1 means at least one divergence — investigate, surface to CTO+COO before COMPLETE.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>git log --oneline -1 -- data/black_diamond/scripts/diagnostics/wave4_cross_consumer_convergence.py</run>
        <expect>Commit visible with author=~B.</expect>
        <if_mismatch>Re-commit with correct author scoping.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency to="ADVI_ROLLUP.RA-P2" status="complete"/>
    <dependency to="ADVI_ROLLUP.RA-P2b" status="pending"/>
    <dependency to="ADVI_ROLLUP.RA-P3" status="complete"/><!-- shipped 2026-04-15 commit e53f0afa per ~B -->
    <dependency to="ADVI_ROLLUP.RA-P4" status="staged"/>
    <dependency to="ADVI_ROLLUP.CN-P2" status="pending"/>
    <dependency to="ADVI_ROLLUP.CN-P3" status="staged"/>
    <dependency to="ADVI_ROLLUP.CN-P4" status="staged"/>
    <dependency to="ADVI_ROLLUP.RA-P1b" status="staged"/>
    <dependency to="ADVI_ROLLUP.CN-P1b" status="staged"/>
  </dependencies>

  <next>
    W4-CG PASS = Wave 4 formal close. COO updates ADVI_ROLLUP.json wave[4].status → complete; REGISTRY entry rewritten.
  </next>
</task_order>
