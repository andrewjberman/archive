# Task Order: ADVI_INFGRD.001 — DS Phase 0: Orion CSV Firm-Tag Audit

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-infgrd-001</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-27</date>
    <status>open</status>
    <priority>HIGH — gates .002, .003, .004. Start immediately. No dependencies.</priority>
  </metadata>

  <objective>
    Inflection portal shows $429M total AUA; actual Inflection AUA is ~$191M. The Orion export
    under the Inflection account has read access to multiple firms (Keil Financial Partners +
    others). The silver-layer SCOPEFIX currently keeps ALL individual advisors regardless of firm.

    Phase 0: audit the Orion bronze CSVs to identify the firm-identifying field that can be used
    to filter to Inflection-only advisors in the silver layer. Produce the advisor-to-firm mapping
    and AUA sanity check. This output gates .002 (silver-layer fix) and Andrew's advisor-list
    confirmation.

    NOTE: supersedes ADVI_INFLEC.SCOPEFIX-2 Phase 0 (same audit task). INFGRD is the canonical
    project. SCOPEFIX-2 TO at org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/
    ADVI_INFLEC.SCOPEFIX-2.ds-inflection-only-advisor-filter.md is superseded — ignore it.
  </objective>

  <scope>
    <task id="1" label="Download and enumerate bronze CSVs">
      Pull latest Inflection bronze CSVs from S3:
        aws s3 ls s3://opal-data-inf/bronze/orion/ --recursive
        aws s3 cp s3://opal-data-inf/bronze/orion/ /tmp/infgrd-audit/ --recursive

      Target export types: TRN (transactions), AUM (aum snapshots), SlickGrid (rep/account dim).
      Enumerate ALL columns across all 3 export types.
    </task>

    <task id="2" label="Identify firm-membership candidates">
      From the column enumeration, identify every column that could carry firm membership
      for individual advisors. Priority candidates (per PRD §2.3):
        advisor_firm, firm_name, office, branch, team, parent_firm, affiliate,
        manager, office_code, rep_office

      For each candidate, list distinct values across the latest export batch.
    </task>

    <task id="3" label="Produce advisor-to-firm mapping">
      Using the identified candidate field(s), map each of the 9 advisors currently in
      platinum/firm/leaderboard.json to their identified firm value:
        - Tim Demuth, Dan Sinnen, Kevin Christensen, John Kurcz, Peter Lee,
          Patrick Scanlan, Daria Zalewska, Jeremy Keil, + Keil Financial Partners row

      Confirm which map to "Inflection Wealth Management" value and which to Keil / other.
      This table goes to Andrew for the ~4 actual Inflection employee confirmation.
    </task>

    <task id="4" label="Cross-export stability check">
      Confirm the firm-identifying field is present and consistent across TRN, AUM, and
      SlickGrid export types. If the field is missing from one export type, document which
      exports carry it and whether a LEFT JOIN to a firm-membership dimension would be needed.
    </task>

    <task id="5" label="AUA sanity check">
      Sum AUM rows for Inflection-tagged advisors only. Verify the sum is approximately
      $191M (Andrew's stated expectation). If the sum is significantly different, DO NOT
      proceed to .002 — escalate to CTO with the actual figure before writing the filter.
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      Session log (MCP message to 2.0.0_SA_COO + 1.0.0_SA_CTO) contains:
        (a) exact field name recommended for advisor_firm column
        (b) normalized value that maps to Inflection employees
        (c) normalized values that map to Keil / non-Inflection
        (d) 9-row advisor-to-firm table
        (e) AUA sanity check result (~$191M or escalation if not)
        (f) stability verdict across TRN, AUM, SlickGrid
    </criterion>
    <criterion id="2">
      AUA for Inflection-tagged advisors is in range $140M–$250M (±30% tolerance around $191M).
      If outside this range, escalate before proceeding to .002.
    </criterion>
    <criterion id="3">
      Firm-identifying field is present in at least one export type that feeds the advisor
      dimension (SlickGrid or AUM). TRN-only presence is acceptable with a JOIN strategy.
    </criterion>
    <criterion id="4">
      Pre-commit gate passes on any .py file touched (.tools/ds-commit-gate.sh). Even audit
      scripts count — run gate before committing session log or helper scripts.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Read-only audit — no writes to silver or gold artifacts during Phase 0.
    Do not trigger any chain re-runs from this task.</constraint>
    <constraint>No emojis in code, logs, or print statements.</constraint>
    <constraint>If AUA sanity check fails (outside $140M–$250M range), STOP and escalate.
    Do not proceed to .002 on bad data.</constraint>
  </constraints>

  <dependencies>
    <!-- No gates — start immediately -->
  </dependencies>

  <deliverables>
    <deliverable type="mcp">Session log sent to 2.0.0_SA_COO + 1.0.0_SA_CTO with all 6
    criterion items above. Subject: RAVC — ADVI_INFGRD.001 COMPLETE | [field_name] confirmed |
    [N] Inflection advisors | ~$[X]M AUA.</deliverable>
    <deliverable type="mcp">Advisor-to-firm mapping table forwarded to Andrew (via COO) for
    ~4 Inflection employee confirmation.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFGRD.md §4 — Phase 0 Investigation</ref>
    <ref type="project">org/projects/ADVI_INFGRD.json</ref>
    <ref type="silver_script">data/orion/scripts/silver/convert_orion_to_silver.py:105-144</ref>
    <ref type="s3_audit">s3://opal-data-inf/bronze/orion/ (read-only)</ref>
  </references>
</task_order>
```
