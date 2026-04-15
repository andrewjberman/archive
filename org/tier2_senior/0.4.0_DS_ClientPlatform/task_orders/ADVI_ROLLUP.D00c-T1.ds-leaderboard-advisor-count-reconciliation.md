<task_order>
  <metadata>
    <id>ADVI_ROLLUP.D00c-T1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to><!-- ~C surfaced via validator sweep T1d (commit 5c217dda); COO assigned + delegated TO authoring 22:06Z -->
    <date>2026-04-15</date>
    <status>complete</status><!-- COMPLETE 2026-04-15 18:14 ET (~C). Path (b) DELIBERATE chosen. Doc-only ship: docs/data/d00c_leaderboard_eligibility_criteria.md. Verified hypothesis: 11-advisor MAX gap = 4 sentinels (49f_house/unassigned/unknown/unresolved) + 7 zero-current-activity advisors. Path b correct: leaderboard intentionally narrower than summary universe (current snapshot vs full-timeseries). No code change needed. Side finding flagged: D_02 summary.json for zero-current-activity advisors shows contradictory tagged_aua=$0 + role_breakdown non-zero -- separate triage. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>3 (Frontend correctness — D_00c producer triage)</wave>
    <priority>P3 (user-facing impact via leaderboard render; no consumer breakage)</priority>
    <slug_note>Slug uses D00c (the actual producer script) rather than COO's suggested "D02-T1" since D_00c.portal_leaderboard is the relevant producer; D_02 produces summary books on a different code path.</slug_note>
  </metadata>

  <references>
    <ref type="trigger">~C validator sweep T1d (commit 5c217dda) — leaderboard 152 entries vs advisor summary 163 (validator T1d.QTD comparison)</ref>
    <ref type="related">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_ROLLUP.D01-T1.ds-d01-geo-aua-snapshot-gap-triage.md (same shape — verify, decide path, ship)</ref>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md</ref>
  </references>

  <objective>
    Validator T1d reported `platinum/firm/leaderboard.json` QTD entries (152) != advisor summary count (163) = 11-advisor gap.

    Verify whether the gap is:
    - **(a) Bug** — D_00c filter excludes advisors that should appear; patch.
    - **(b) Deliberate** — D_00c criteria legitimately exclude (e.g. zero current AUA, no current accounts, sentinel placeholders); document rationale + optionally surface count metadata.
  </objective>

  <scope>
    <files>
      <file action="modify_or_document">data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py (modify if path a) OR docs/data/d00c_leaderboard_eligibility_criteria.md (create if path b)</file>
    </files>
  </scope>

  <wire_contract>
    Path (a): leaderboard entry count == advisor summary count (within sentinel exclusions). Path (b): documented rationale + optional `excluded` metadata count on leaderboard output.
  </wire_contract>

  <acceptance_criteria>
    1. Hypothesis verified or rejected with quantitative evidence: list missing advisors, show their summary.json state.
    2. Path chosen and documented in commit body / TO closeout.
    3. If (a): D_00c patched, S3 uploaded, post-nightly verification.
    4. If (b): rationale doc shipped; FE consumer (DE) notified.
    5. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    6. MCP COMPLETE to COO with chosen path + evidence + verification artifact path.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_00c</run>
        <expect>READS visible (account_team, advisor_fee_detail, role_aua); WRITES employee_leaderboard.json; producer confirmed.</expect>
      </step>
      <step>
        <run>comp-blast D_00c</run>
        <expect>Script-node empty (use fn name); D_04 picks up employee_leaderboard for platinum/firm/leaderboard.json composition.</expect>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-bd/platinum/advisors/ + diff vs leaderboard advisor_id set per window</run>
        <expect>Identify missing advisor IDs + classify (sentinel vs structural).</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile D_00c.portal_leaderboard.py</run>
        <expect>Exit 0 (path a only).</expect>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>{post-nightly D_00c run; recount leaderboard.json windows.{QTD,YTD,MAX}.entries vs advisor folders}</run>
        <expect>Path (a): equal count. Path (b): documented rationale + optional excluded count.</expect>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>

  <next>
    D00c-T1 close → if path (b), backlog item: D_02 summary.json data inconsistency for zero-current-activity advisors (tagged_aua=$0 + account_count=0 but role_breakdown contains non-zero historical values). Flag for separate triage.
  </next>
</task_order>
