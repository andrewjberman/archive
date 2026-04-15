<task_order>
  <metadata>
    <id>ADVI_ROLLUP.D01-T1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to><!-- ~C surfaced via B7 closeout side-finding; natural fit -->
    <date>2026-04-15</date>
    <status>complete</status><!-- COMPLETE 2026-04-15 18:05 ET (~C). Path (b) DELIBERATE chosen. Code+doc commit f2824a21, S3 ship 18:02 ET. Hypothesis verified at D_01.py L758-763 (state filter explicit). Quantified $3-4M / 0.24-0.26% gap across q1/q2/q3; current overridden by ADVI_PSCFIX (separate concern). Additive donut.unassigned + donut.unassigned_pct fields shipped. Rationale doc: docs/data/d01_geo_filter_rationale.md. Post-nightly verification deferred. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>3 (Frontend correctness — D_01 producer triage)</wave>
    <priority>P3 (known producer gap, no consumer breakage; FE-noticeable when comparing donuts side-by-side)</priority>
  </metadata>

  <references>
    <ref type="trigger">~C B7 closeout brief side-finding 2026-04-15 (commit d08d4bb7) — D_01 producer-side intra-snapshot gap</ref>
    <ref type="related">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_FNTEND.B7.ds-q4-aua-divergence-investigation.md (closed COMPLETE per CTO ACCEPT)</ref>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md</ref>
  </references>

  <objective>
    D_01 producer-side intra-snapshot gap: `views.geo.q2.donut.total = $1,440.8M` vs `views.aua.q2.donut.total = $1,444.5M` = **$3.73M (0.26%) gap**. Same producer (D_01), same as-of date.

    ~C's hypothesis: accounts with null state field excluded from geo donut but counted in tax-status donut.

    **Tasks:**
    1. Verify the hypothesis. Read D_01 geo aggregation logic. Identify the state filter. Quantify accounts with null state vs accounts in the gap.
    2. Decide:
       - **(a) Bug** — null-state accounts should be in geo (perhaps as "Unknown" bucket or distributed proportionally). Patch D_01.
       - **(b) Deliberate** — null-state accounts legitimately excluded from geo (no state to assign). Document in `docs/data/d01_geo_filter_rationale.md` + add a footnote-able value to the geo donut output (e.g. `views.geo.q2.donut.unassigned: $3.73M`).
    3. If (a): patch D_01, ship via gold dispatch, verify post-nightly that `views.geo.q2.donut.total == views.aua.q2.donut.total` within $0.01.
    4. If (b): document, ship the rationale doc, optionally add the unassigned value to D_01 output for FE display.
  </objective>

  <scope>
    <files>
      <file action="modify_or_document">data/black_diamond/scripts/gold/D_01.partner_analytics.py (modify if path a) OR docs/data/d01_geo_filter_rationale.md (create if path b)</file>
    </files>
  </scope>

  <wire_contract>
    Path (a): geo + aua donut totals agree within $0.01. Path (b): documented rationale + optional `unassigned` field on geo donut output.
  </wire_contract>

  <acceptance_criteria>
    1. Hypothesis verified or rejected with quantitative evidence.
    2. Path chosen and documented in commit body / TO closeout.
    3. If (a): D_01 patched, S3 uploaded, post-nightly verification PASS.
    4. If (b): rationale doc shipped; FE consumer (DE) notified that unassigned value is available if they want to display it.
    5. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    6. MCP COMPLETE to COO with chosen path + evidence + verification artifact path.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_01</run>
        <expect>READS visible; WRITES include views.geo + views.aua. Confirms producer.</expect>
        <if_mismatch>Locate actual producer.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse views.geo &amp;&amp; comp-platinum reverse views.aua</run>
        <expect>Both lists D_01 as producer; consumer = portal partner_analytics page.</expect>
        <if_mismatch>If consumer differs, re-scope.</if_mismatch>
      </step>
      <step>
        <run>grep -nE 'state|geo' data/black_diamond/scripts/gold/D_01.partner_analytics.py | head -30</run>
        <expect>State-field filter visible in geo aggregation block.</expect>
        <if_mismatch>If no filter found, hypothesis fails — investigate alternate cause.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_01.partner_analytics.py</run>
        <expect>PY_COMPILE_OK (if path a was chosen).</expect>
        <if_mismatch>Fix syntax (path a only).</if_mismatch>
      </step>
      <step>
        <run>{D_01 dry-run output for views.geo.q2.donut + views.aua.q2.donut}</run>
        <expect>Path (a): totals agree within $0.01. Path (b): unassigned field populated.</expect>
        <if_mismatch>Iterate.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>{post-nightly D_01 run; cat platinum/firm/partner_analytics.json | jq '.views.geo.q2.donut.total, .views.aua.q2.donut.total'}</run>
        <expect>Path (a): equal within $0.01. Path (b): unassigned field present.</expect>
        <if_mismatch>Re-investigate.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>

  <next>
    D01-T1 close → if path (a), no follow-up needed. If path (b), DE may pick up display TO for the unassigned value.
  </next>
</task_order>
