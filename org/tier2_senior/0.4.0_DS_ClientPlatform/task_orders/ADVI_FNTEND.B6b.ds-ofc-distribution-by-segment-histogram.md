<task_order>
  <metadata>
    <id>ADVI_FNTEND.B6b</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-15</date>
    <status>staged</status><!-- Follow-up to B6 HOLD per CTO Path C+ approval 22:13Z -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>A (followup)</wave>
    <priority>P2 (FE OfcAdvisorListPanel L1 bell-curve render gated on this fix)</priority>
  </metadata>

  <references>
    <ref type="parent">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_FNTEND.B6.ds-ofc-snapshot-parity.md (HOLD pending this fix)</ref>
    <ref type="trigger">CTO Path C+ approval 2026-04-15 22:13Z + ~B B-TO sweep 22:11Z (acceptance #c L0 PASS, L1 GAP)</ref>
    <ref type="related_clarification">CTO 2026-04-14 RD-audit clarification (origin of by_segment[office] histogram requirement)</ref>
  </references>

  <objective>
    Fix D_01 producer-side emission for `views.nna.{q}.ofc.distribution.by_segment[office]`:

    - **Current (broken):** single value per office, count=1.
    - **Required:** histogram of per-advisor NNA values within that office (count = N_advisors_in_office).

    The single-value-per-office output breaks `OfcAdvisorListPanel` L1 bell-curve render (it has nothing to bin).

    Patch D_01 to emit per-advisor NNA values within each office segment, structured as a histogram. Per-segment count = number of advisors within the office.

    Verify post-nightly: `OfcAdvisorListPanel` L1 bell-curve renders with per-office distribution shape.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_01.partner_analytics.py (by_segment[office] histogram emission for views.nna.{q1,q2,q3,current}.ofc.distribution)</file>
    </files>
    <s3_writes>
      <write>s3://opal-data-bd/code/gold/D_01.partner_analytics.py</write>
    </s3_writes>
  </scope>

  <wire_contract>
    Output schema for `views.nna.{q}.ofc.distribution.by_segment[office]`: `{count: N_advisors, values: [per-advisor-nna...], histogram: {bins, counts}}`. FE consumer (OfcAdvisorListPanel L1) reads `histogram` for bell-curve render.
  </wire_contract>

  <acceptance_criteria>
    1. Per-office histogram emission populated for all 4 quarters (q1, q2, q3, current).
    2. Per-segment count = N_advisors_in_office (matches `office.advisor_ids[].length`).
    3. py_compile clean.
    4. S3 upload with documented etag.
    5. Post-nightly verification: `OfcAdvisorListPanel` L1 bell-curve renders with non-empty per-office distribution. Spot-check 3 offices.
    6. Parent B6 TO flipped staged → complete with reference to this commit.
    7. Session log Compiler Tools reproduces every `<run>` + observed + pass/fail.
    8. MCP COMPLETE to COO + CTO with commit hash + S3 etag + post-nightly screenshot evidence.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>grep -nE 'by_segment|ofc\.distribution' data/black_diamond/scripts/gold/D_01.partner_analytics.py | head -10</run>
        <expect>Current single-value emission visible. Confirms scope.</expect>
        <if_mismatch>Re-baseline emission location.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse views.nna.q2.ofc.distribution.by_segment</run>
        <expect>OfcAdvisorListPanel listed as consumer. Confirms FE binding.</expect>
        <if_mismatch>Confirm consumer locator before proceeding.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_01.partner_analytics.py</run>
        <expect>PY_COMPILE_OK.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
      <step>
        <run>{D_01 dry-run for q2 ofc segment, dump first office's distribution}</run>
        <expect>Histogram populated; count = N_advisors; values list non-empty.</expect>
        <if_mismatch>Iterate.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit + nightly">
      <step>
        <run>jq '.views.nna.q2.ofc.distribution.by_segment | to_entries | .[0]' platinum/firm/partner_analytics_quarterly.json</run>
        <expect>First office shows histogram + per-advisor values; count > 1 (where data exists).</expect>
        <if_mismatch>Investigate emission bug.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>

  <next>
    B6b close → flip parent ADVI_FNTEND.B6 to complete with cross-ref. Re-screenshot OfcAdvisorListPanel L1 to verify bell-curve render.
  </next>
</task_order>
