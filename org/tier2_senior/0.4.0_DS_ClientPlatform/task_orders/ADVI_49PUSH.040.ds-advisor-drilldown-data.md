<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-040-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-09</date>
    <status>complete -- 0.4.0_DS_ClientPlatform~C, commit 10df0f0f</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>10</wave>
    <phase>Advisor drilldown data</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Produce three new platinum artifacts needed by the Advisor Drilldown page (DE .041):
    1. platinum/advisors/{id}/timeseries.json -- per-date AUA/NNA with role breakdown
    2. active_since field added to platinum/advisors/{id}/summary.json
    3. Role-breakdown snapshot fields confirmed/added to platinum summary

    All three are new D_04 additions reading from existing D_02 gold outputs.
  </objective>

  <context>
    AE session state as of 2026-04-09 afternoon ET:
      Platinum is live: 165 advisors, 14,769 files, 3.3 GB.
      D_02 multi-role + SCD PIT + fee decomposition are deployed and running.
      Travis Penfield confirmed: $427.3M tagged / $342.6M fee-earning / 33.2 bps.
      All gold scripts (D_00, D_02, D_04, C_06, C_08) deployed to S3.

    PENDING UPSTREAM CHANGE -- A_01 multi-role split normalization:
      Andrew approved rule: when the same advisor holds 2+ roles on the same account
      with split_pct > 0, sum their splits and divide equally across roles.
      Example: Alex Bright impl=40 + local_ops=10 → impl=25 + local_ops=25 (sum stays 50).
      _normalize_multi_role_splits() was implemented in A_01.advisor_assignments.py
      (lines 287-346) but is sitting in the local repo ONLY -- not yet uploaded to S3
      or run through the chain.
      Impact on drilldown: fee_earning_aua and avg_fee_bps_earned in advisor summaries
      will be slightly off for the 18 advisors affected (3.76% of SCD records) until
      A_01 runs. Upload A_01 to S3 and request AE to run the full chain BEFORE or AS
      PART OF this TO's AE deploy step.

    DE .041 builds a full-page drilldown when a user clicks an advisor in the leaderboard.
    The page has three panels:
      Top-left:  Summary card (identity, AUA, flows, fee) -- reads summary.json
      Top-right: Role composition donut -- reads summary.json role_breakdown
      Bottom:    Stacked area AUA + diverging NNA over time -- reads timeseries.json

    The flows section of the summary card (NNA, Inflows, Outflows, New Clients) must
    update when the time window changes (QTD/YTD/1Y/Max). DE derives period flows from
    the cumulative timeseries by differencing window endpoints -- no pre-bucketed windows
    needed in the platinum data. DS only needs to provide the cumulative daily series.

    D_02 already writes gold/entities/advisors/{id}/timeseries.json with:
      per-date: total_aua, cum_inflows, cum_outflows, nna
    D_04 currently does NOT publish this to platinum. It also lacks role breakdown.
  </context>

  <deliverable_1 label="platinum/advisors/{id}/timeseries.json -- with role breakdown">
    <description>
      Step 1: Add per-role AUA to D_02's build_advisor_timeseries output.

      The current timeseries loop (line ~1132) groups by (date, advisor_name) and sums
      total_aua. We need to also sum AUA separately for each role the advisor holds.

      For each date, for each advisor, compute:
        architect_aua     = sum(total_aua) for accounts where this advisor is architect
        implementor_aua   = sum(total_aua) for accounts where this advisor is implementor
        consultant_aua    = sum(total_aua) for accounts where this advisor is consultant
        local_ops_aua     = sum(total_aua) for accounts where this advisor is local_ops
        addl_advisor_aua  = sum(total_aua) for accounts where this advisor is additional_advisor

      Note on double-counting: an account where this advisor holds MULTIPLE roles will
      appear in MULTIPLE role buckets. This is INTENTIONAL for the donut/stacked chart --
      the visual shows "what is their presence as each role type" not a sum-to-total stack.
      The total_aua field (deduplicated) remains authoritative for the headline figure.
      The role_aua fields are for visual proportionality only -- do not sum them.

      Implementation: after building the deduplicated `melted` DataFrame (line ~1130),
      build a SEPARATE un-deduplicated long-form for role breakdown:
        for each role in ROLES_FOR_TS:
          role_sub = acct[acct[role].notna()][['date', 'account_id', role, 'total_aua']]
              .rename(columns={role: 'advisor_name'})
          [filter advisor_name]
          role_ts[role] = role_sub.groupby(['date', 'advisor_name'])['total_aua'].sum()

      Add to each data_row dict:
        'architect_aua':    round(float(role_ts['architect'].get((date, advisor), 0)), 2),
        'implementor_aua':  round(float(...), 2),
        'consultant_aua':   round(float(...), 2),
        'local_ops_aua':    round(float(...), 2),
        'addl_advisor_aua': round(float(...), 2),

      Step 2: D_04 -- publish gold/entities/advisors/{id}/timeseries.json to platinum.
      Add to build_advisor_summaries() (or a new build_advisor_timeseries() step):
        For each advisor with a gold timeseries.json, write it verbatim to
        platinum/advisors/{id}/timeseries.json
        (The gold file is already the right shape after Step 1 adds role breakdown.)

      Final schema per data row:
        {
          date, total_aua, cum_inflows, cum_outflows, nna,
          architect_aua, implementor_aua, consultant_aua, local_ops_aua, addl_advisor_aua
        }
    </description>
  </deliverable_1>

  <deliverable_2 label="active_since added to summary.json">
    <description>
      The summary card shows "Active Since {date}" -- the earliest date this advisor
      appears in the dataset.

      Source: advisor_assignments_history.parquet (A_01), which D_02 already reads.
      For each advisor: min(effective_date) across all SCD records where advisor_name matches.
      If no SCD record exists: fall back to min(date) in account_performance where the
      advisor appears in any role column.

      Add active_since to book.json summary (D_02) and propagate to
      platinum/advisors/{id}/summary.json (D_04).

      Format: ISO date string "YYYY-MM-DD". DE will format for display ("Jan 15, 2023").
    </description>
  </deliverable_2>

  <deliverable_3 label="role_breakdown confirmed in summary.json">
    <description>
      The donut chart reads role_breakdown from the platinum summary.
      Verify that platinum/advisors/{id}/summary.json already has a role_breakdown section
      structured as:
        role_breakdown: {
          architect:         { aua: N, account_count: N, pct_of_tagged: N },
          implementor:       { aua: N, account_count: N, pct_of_tagged: N },
          consultant:        { aua: N, account_count: N, pct_of_tagged: N },
          local_ops:         { aua: N, account_count: N, pct_of_tagged: N },
          additional_advisor:{ aua: N, account_count: N, pct_of_tagged: N },
        }
      where aua = AUA of accounts in that role (NOT deduplicated across roles).
      pct_of_tagged = role_aua / tagged_aua (for display in the donut legend).

      If already present with this shape: no change needed, confirm only.
      If missing or differently shaped: add/fix in D_02 book.json and D_04 summary publish.

      Note: pct values will NOT sum to 100% if the advisor holds multiple roles on
      shared accounts. This is expected and correct -- the donut is proportional,
      not a partition. DE handles the visual treatment.
    </description>
  </deliverable_3>

  <acceptance_criteria>
    1. platinum/advisors/{id}/timeseries.json exists for all advisors, contains role AUA fields
    2. Spot-check Travis Penfield: architect_aua ~= $180M, total_aua ~= $427M on latest date
    3. platinum/advisors/{id}/summary.json has active_since: "YYYY-MM-DD" field
    4. role_breakdown present with aua + pct_of_tagged per role
    5. Session log: note whether role_breakdown was already correct or required fixes
    6. Notify DE inbox when platinum data is ready (unblocks .041)
  </acceptance_criteria>


  <compiler_tools>
    comp-pipescript io D_02
      -- Full I/O manifest for D_02. Confirms what timeseries.json currently writes
         (which fields exist, which are missing) without reading all 1,700 lines.
         Run first -- this is the authoritative answer to "what does D_02 produce?"

    comp-blast gold/entities/advisors/
      -- Shows all scripts that read from gold/entities/advisors/ prefix.
         Confirms D_04 is in the blast radius when D_02's timeseries schema changes.
         Run before adding role breakdown fields to timeseries.json.

    comp-pipescript io D_04
      -- Confirms how D_04 currently handles advisor entities (which gold files it reads,
         which platinum files it writes). Tells you exactly where to add the new
         platinum/advisors/{id}/timeseries.json publisher step.
  </compiler_tools>

</task_order>
