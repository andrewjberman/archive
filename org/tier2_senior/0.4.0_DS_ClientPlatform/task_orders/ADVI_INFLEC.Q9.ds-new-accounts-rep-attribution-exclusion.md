<task_order>
  <metadata>
    <id>ADVI_INFLEC.Q9</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to><!-- ~A lane per Andrew 2026-04-22 INFLEC DS reassignment -->
    <date>2026-04-24</date>
    <status>staged</status><!-- GO post-W4.13 AE completion; small scope — can run in parallel with W4.14 -->
    <project_code>ADVI_INFLEC</project_code>
    <priority>P2 — advisor-attribution accuracy; affects leaderboard correctness but not platinum LIVE</priority>
    <origin>
      INFLEC PRD §10 Q9 (docs/architecture/ADVI_INFLEC.md:515): "'New Accounts Rep' transactions (51,670 rows) — exclude from individual advisor attribution? OPEN — DS convention. Blocks: W4.3 (affects leaderboard output)."
      Andrew directive 2026-04-24 + COO convention: **exclude from advisor leaderboards, keep in firm totals.** Convention TO makes that explicit + implemented.
    </origin>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLEC.md §10 Q9</ref>
    <ref type="coo_convention">Exclude from advisor-scoped attribution (leaderboard, advisor NNA, advisor AUA growth). Keep in firm totals (firm NNA, firm AUA). Rationale: "New Accounts Rep" is a placeholder ID Orion assigns before a real advisor is attached — attributing 51,670 transactions to this placeholder distorts individual advisor metrics.</ref>
    <ref type="affected_scripts">data/orion/scripts/gold/I_A01.advisor_assignments.py — advisor-rep join; data/orion/scripts/gold/I_C07.advisor_attribution.py — advisor-scoped rollups</ref>
  </references>

  <objective>
    Implement the "New Accounts Rep exclusion from advisor-scoped attribution" convention:
    - Identify the "New Accounts Rep" placeholder rep_id in Orion TRN (typically a canonical string like "New Accounts Rep" or a specific numeric rep_id — Phase 0 confirms)
    - Add exclusion filter to I_A01 advisor_assignments.py (or I_C07 — pick at Phase 0) so transactions with that rep_id do NOT roll up to any individual advisor's leaderboard / NNA / AUA metrics
    - Ensure firm-level totals (firm_nna, firm_aua from I_D00c / I_D04) still INCLUDE these transactions — they happened, just not attributable to an individual advisor
    - Document exclusion count + dollar-impact in session log (51,670 rows per briefing; confirm)

    **EXPLICIT SCOPE LOCK:**
    - NO portal changes (if advisor count drops, that's correct)
    - NO firm-total changes (include New Accounts Rep in firm_nna/firm_aua)
    - NO retroactive backfill unless trivially cheap
    - Forward-emit: apply the exclusion to next chain run; platinum artifacts regenerate on full chain
  </objective>

  <scope>
    <files>
      <file action="investigate">silver/trn partitions — confirm "New Accounts Rep" rep_id string / numeric value + exact row count</file>
      <file action="modify">data/orion/scripts/gold/I_A01.advisor_assignments.py OR data/orion/scripts/gold/I_C07.advisor_attribution.py — add exclusion filter on advisor-scoped aggregation path (NOT firm-scoped)</file>
      <file action="modify">data/orion/scripts/gold/gold_validate_config.yaml — add validator: "New Accounts Rep" rows in advisor leaderboard output = 0 (ERROR if present)</file>
      <file action="read-only">data/orion/scripts/gold/I_D00c.portal_leaderboard.py — verify firm totals unaffected</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="exclusion-filter">
      Code change: advisor-scoped aggregation path filters OUT "New Accounts Rep" rows; firm-scoped aggregation unchanged.
    </deliverable>
    <deliverable id="count-documentation">
      Session log: exact count of excluded rows + dollar-impact on advisor-level totals (should match ~51,670 rows per briefing).
    </deliverable>
    <deliverable id="validator-block">
      gold_validate_config.yaml rule: ERROR if "New Accounts Rep" appears in platinum/advisors/* leaderboard output.
    </deliverable>
    <deliverable id="firm-total-confirmation">
      Spot-check: firm_nna + firm_aua from I_D00c / I_D04 post-exclusion = same as pre-exclusion (within rounding).
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">"New Accounts Rep" rep_id identified + exact row count confirmed in silver TRN (target ~51,670; log actual).</ac>
    <ac id="2">Exclusion filter shipped on advisor-scoped aggregation path (I_A01 or I_C07); NOT applied to firm-scoped.</ac>
    <ac id="3">gold_validate_config.yaml exclusion-ERROR rule added; `comp-validate` on affected script exits 0.</ac>
    <ac id="4">Firm totals unchanged pre-vs-post exclusion (within rounding): spot-check firm_nna + firm_aua from I_D00c.</ac>
    <ac id="5">Advisor totals DECREASE (expected): document sum of advisor-NNA reduction + advisor count (should be limited to those previously attributed New Accounts Rep rows).</ac>
    <ac id="6">py_compile + ds-commit-gate exit 0; comp-pipescript deployed MATCH.</ac>
    <ac id="7">Session log Compiler Tools section + MCP COMPLETE to COO with commit hash + exclusion count + advisor-total delta.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="0" when="discovery">
      <step>
        <run>python3 -c "import pyarrow.parquet as pq, pandas as pd; df = pq.read_table('s3://opal-data-inf/silver/trn/').to_pandas(); print(df[df['rep_name'].str.contains('New Accounts', na=False, case=False)].shape[0])"</run>
        <expect>Count ~51,670 (confirm briefing figure).</expect>
        <if_mismatch>If count materially different, adjust exclusion filter — rep_id may be encoded differently; investigate.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "# Same df; groupby rep_id | rep_name | count — surface all rep identifiers with 'New Accounts' or placeholder patterns"</run>
        <expect>Single canonical identifier for placeholder rep; document exact form (string / int / etc.).</expect>
        <if_mismatch>If multiple placeholder patterns, document each + decide inclusion scope (all placeholders or only "New Accounts Rep").</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io I_A01</run>
        <expect>I_A01 READS silver/trn + WRITES gold/advisor_assignments. Identify filter insertion point.</expect>
        <if_mismatch>If advisor-scoped filter more natural in I_C07, pivot Phase 1 there.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="before write">
      <step>
        <run>comp-blast I_A01</run>
        <expect>Downstream consumers include I_C07 + D-chain + platinum advisor artifacts. Confirm filter effect.</expect>
        <if_mismatch>Unexpected consumers = investigate.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/orion/scripts/gold/I_A01.advisor_assignments.py (or I_C07.py)</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh <affected files></run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix AST.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-pipescript deployed I_A01 (or I_C07)</run>
        <expect>MATCH.</expect>
        <if_mismatch>Re-upload.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "# Re-aggregate advisor-scoped NNA post-filter; compare to pre-filter firm-scoped NNA; confirm firm totals within rounding"</run>
        <expect>Firm NNA delta < $1K between pre/post exclusion (expected: zero — filter only affects advisor-scoped, not firm-scoped).</expect>
        <if_mismatch>Firm totals changed = filter accidentally applied to firm aggregation; rollback + fix.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <do_not>
    <rule>Do NOT apply exclusion to firm-scoped aggregation — firm totals must be unchanged.</rule>
    <rule>Do NOT backfill historical advisor platinum artifacts unless trivially cheap.</rule>
    <rule>Do NOT expand scope to other placeholder rep patterns beyond "New Accounts Rep" — separate TO if surfaced.</rule>
    <rule>Do NOT modify portal — advisor count display will decrease naturally on next chain run.</rule>
  </do_not>
</task_order>
