<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-22-ornren-001-ds-orion-rename</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-22</date>
    <status>active</status>
    <project_code>ADVI_INFLEC</project_code>
    <urgency>HIGH — rename before next Orion D-chain dispatch so runner pulls correct names from S3.</urgency>
    <andrew_directive>2026-04-22 in-session: Orion scripts must not carry firm-specific I_ prefix. data/orion/ is a vendor-level folder shared by future clients. Match BD convention (A_00, B_00, C_00).</andrew_directive>
  </metadata>

  <objective>
    Rename all Orion gold + silver scripts from I_* convention to BD-matching vendor convention
    (A_00, B_00, C_00 etc). Rename-only — zero logic changes. DS owns local rename + internal
    reference updates + git commit + S3 upload cycle. AE owns dispatch wiring (ORNREN.002).
  </objective>

  <spec>
    Local directory: data/orion/scripts/gold/ and data/orion/scripts/silver/

    Gold script renames:
      I_A00.accounts_dimension.py        -> A_00.accounts_dimension.py
      I_A01.advisor_assignments.py       -> A_01.advisor_assignments.py
      I_A02.fee_rate_history.py          -> A_02.fee_rate_history.py
      I_A03.positions_cube.py            -> A_03.positions_cube.py
      I_A04.client_dimension.py          -> A_04.client_dimension.py
      I_00.canonical_holdings.py         -> B_00.canonical_holdings.py
      I_B01.holdings_lots.py             -> B_01.holdings_lots.py
      I_B01b.classify_new_securities.py  -> B_01b.classify_new_securities.py
      I_B02.canonical_lots.py            -> B_02.canonical_lots.py
      I_B03.account_gains.py             -> B_03.account_gains.py
      I_C00.canonical_performance.py     -> C_00.canonical_performance.py
      I_C01.canonical_nna.py             -> C_01.canonical_nna.py
      I_C01b.role_aua_backfill.py        -> C_01b.role_aua_backfill.py
      I_C02.client_performance.py        -> C_02.client_performance.py
      I_C03.account_performance.py       -> C_03.account_performance.py
      I_C04.validate_aua.py              -> C_04.validate_aua.py
      I_C05.client_tax_liability.py      -> C_05.client_tax_liability.py
      I_C06.client_mix_timeseries.py     -> C_06.client_mix_timeseries.py
      I_C07.advisor_attribution.py       -> C_07.advisor_attribution.py
      I_C08.advisor_fee_efficiency.py    -> C_08.advisor_fee_efficiency.py
      I_09.generate_partner_analytics.py -> 09.generate_partner_analytics.py
      I_D00c.portal_leaderboard.py       -> D_00c.portal_leaderboard.py
      I_D02.advisor_client_detail.py     -> D_02.advisor_client_detail.py
      I_D04.client_portal_summary.py     -> D_04.client_portal_summary.py
      build_canonical_prices_inf.py      -> build_canonical_prices.py
      inf-gold-dispatch.sh               -> orion-gold-dispatch.sh
      inf_w49_runner.py                  -> orion_runner.py
      inf_w49_resume.py                  -> orion_resume.py

    Silver script renames:
      backfill_yahoo_prices_inf.py       -> backfill_yahoo_prices.py
      convert_orion_to_silver.py         -> (already correct, no change)
      inject_scoped_overrides.py         -> (already correct, no change)
  </spec>

  <steps>
    <step id="1">
      git mv each script to its new name locally. Use git mv (not cp) to preserve git history.
    </step>
    <step id="2">
      Grep all renamed scripts for cross-references to old names (e.g. import patterns,
      orion-gold-dispatch.sh download list, any hardcoded I_* strings). Update all internal
      references to new names. This is the highest-risk step — be thorough.
      Key file to update: orion-gold-dispatch.sh (the dispatch script downloads scripts by name).
    </step>
    <step id="3">
      Run ds-commit-gate.sh + py_compile on all renamed .py files. Must exit 0 before commit.
    </step>
    <step id="4">
      git commit with author 0.4.0_DS_ClientPlatform. git push CLOUD.
    </step>
    <step id="5">
      For each renamed script, upload new key to S3:
        aws s3 cp data/orion/scripts/gold/A_00.accounts_dimension.py \
          s3://opal-data-inf/code/gold/A_00.accounts_dimension.py
      (repeat for all renamed scripts, gold + silver)
      Then delete old keys:
        aws s3 rm s3://opal-data-inf/code/gold/I_A00.accounts_dimension.py
      (repeat for all old keys)
    </step>
    <step id="6">
      Run comp-pipescript deployed on each renamed script to confirm MATCH (not STALE/MISSING).
      All scripts must show MATCH before signaling AE.
    </step>
    <step id="7">
      MCP AE CloudOps + COO: "ORNREN.001 DS complete — all scripts renamed, S3 uploaded,
      comp-pipescript deployed MATCH. AE clear to proceed ORNREN.002."
    </step>
  </steps>

  <acceptance_criteria>
    1. All I_* local files renamed via git mv, history preserved.
    2. Internal cross-references updated — no I_* strings remaining in script bodies or dispatch file.
    3. ds-commit-gate.sh + py_compile PASS on all renamed .py files.
    4. Committed + pushed to CLOUD.
    5. S3 new keys uploaded, old keys deleted (opal-data-inf/code/gold/ + code/silver/).
    6. comp-pipescript deployed MATCH for all renamed scripts.
    7. MCP AE + COO confirming ORNREN.001 complete.
  </acceptance_criteria>

  <sequencing>
    ORNREN.001 (DS) gates ORNREN.002 (AE). AE must not update dispatch wiring until DS
    confirms S3 new keys are live (comp-pipescript deployed MATCH).
    Can run concurrently with AUAGAP.002 D-chain (different pipeline/runner — no conflict).
  </sequencing>

  <do_not>
    <rule>Do NOT modify script logic — rename only. If you see a bug while renaming, flag it separately.</rule>
    <rule>Do NOT delete S3 old keys until new keys are confirmed uploaded and MATCH.</rule>
    <rule>Do NOT skip ds-commit-gate.sh — standard pre-commit gate applies.</rule>
    <rule>Do NOT signal AE until comp-pipescript deployed shows MATCH for all scripts.</rule>
  </do_not>
</task_order>
