<task_order>
  <metadata>
    <id>ADVI_ROLLUP.CP-MAP</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-17</date>
    <status>pending</status><!-- Flipped staged -> pending 2026-04-22 per Andrew "push all relevant agents to start" directive. CP-DS1 shipped + Gate 1 confirmed. -->
    <project_code>ADVI_ROLLUP</project_code>
    <priority>P1 parallel to CP-VETO-AUTH — structurally correct Gate 2 path</priority>
    <collaborators>0.4.0_DS_ClientPlatform (BD-side account identification)</collaborators>
  </metadata>

  <context>
    472 BD-mapped accounts have open positions in silver/unrealized but ZERO rows in
    silver/RPS (PCRA sleeve / SWTC / sub-master pattern). Their positions are custodied
    at Schwab but delivered under DIFFERENT Schwab account IDs than the BD account mapping expects.

    ~A evidence (2026-04-17): 376 / 618 unique CUSIPs from these 472 accounts DO appear in
    silver/RPS/date=20260415 — just under different account_id values. The securities are there.
    The mapping gap is in schwab_bd_account_mapping.parquet.

    Effect if fixed: these 472 accounts move from Population A (chronic, zero RPS) to
    Population B (has RPS, CUSIP match). CP-DS1 then handles them via direct CUSIP key.
    No special veto path needed. Structurally correct.

    CP-VETO-AUTH (DS, P1 parallel) is the fast bridge. CP-MAP is the long-term correct fix.
    Completion of EITHER + CP-WP5 achieves Gate 2 ($1.694B firm AUA recon).
  </context>

  <objective>
    Expand schwab_bd_account_mapping.parquet to include the sub-master Schwab account IDs
    that carry the 472 chronic-cohort accounts' positions.

    Two-phase work:
      Phase 1 (DS): Identify BD account IDs of the 472 chronic-with-open-lots + their CUSIPs.
        Source: ~A's offline repro (silver/unrealized/2026-04-15.parquet, 472 accounts, 618 CUSIPs).
        Provide to AE: list of (bd_account_id, cusip) pairs needing Schwab account mapping.

      Phase 2 (AE): For each CUSIP in that list, find the Schwab account_id in silver/RPS that
        carries that CUSIP. Join: (cusip → account_id) from RPS to get the Schwab sub-master IDs.
        Add entries to schwab_bd_account_mapping.parquet:
          (bd_account_id → schwab_sub_master_account_id)
        Verify the new mapping entries are logically consistent (no many-to-one conflicts).
  </objective>

  <acceptance_criteria>
    1. schwab_bd_account_mapping.parquet updated with sub-master entries for the 472 cohort.
    2. After mapping update + CP-DS1 active: the 472 accounts appear in bd_covered_with_rps
       (move from Population A to Population B).
    3. QA run: force-close cohort drops further from CP-DS1 baseline toward 0 (not just <50).
    4. No new many-to-one conflicts in the mapping (each BD account maps to one Schwab account).
    5. comp-pipescript deployed MATCH.
    6. MCP COMPLETE to COO + DS with: accounts mapped, residual chronic count, commit hash.
  </acceptance_criteria>

  <risk>
    Schwab sub-master account IDs may represent portfolio-level accounts, not individual BD
    accounts (many BD accounts map to one Schwab sub-master). This would create many-to-one
    ambiguity in position attribution. DS must verify the join cardinality before committing.
    If ambiguous: escalate to CTO. Do not force a bad mapping.
  </risk>

  <compiler_tools_mandate>
    Phase 1 (DS, before write):
      comp-blast gold/dimensions/schwab_bd_account_mapping — confirm all consumers before modifying.
    Phase 2 (AE, before commit):
      python -m py_compile on any modified scripts.
      Spot-check: verify 5 sample accounts from the 472 cohort appear in bd_covered_with_rps after mapping update.
  </compiler_tools_mandate>

  <dependencies>
    <dependency task="ADVI_ROLLUP.CP-DS1" status="staged"
      description="Gate 1 (halt cleared) must be confirmed before expanding mapping. Ensures the new mapping entries flow through the CUSIP match path correctly."/>
    <dependency task="council-research-~A" agent="0.4.0_DS_ClientPlatform~A"
      description="~A's offline repro provides the 472-account CUSIP list. DS must extract and hand off to AE."/>
  </dependencies>

  <next>
    CP-MAP COMPLETE + CP-WP5 COMPLETE = Gate 2. Firm total_aua gold output within 2% of $1,694,648,746.
    This is the structurally correct path. CP-VETO-AUTH (silver/unrealized veto) is the parallel bridge.
  </next>
</task_order>
