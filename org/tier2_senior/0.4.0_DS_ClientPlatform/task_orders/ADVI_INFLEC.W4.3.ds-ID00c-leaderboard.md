<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w4.3-ID00c-leaderboard</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-21</date>
    <status>pending</status><!-- GO 2026-04-22 per Andrew directive — assigned to ~A -->
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Author `data/inflection/scripts/gold/I_D00c.portal_leaderboard.py` — per-advisor leaderboard with per-day Rep ID gating. Leverages Orion's native per-transaction Rep ID, eliminating the CHART-ALIGN complexity required for BD. Output: `platinum/firm/leaderboard.json` schema-identical to 49F equivalent. Handle the "Inflection Wealth Management" firm-rep bucket (287 HH / $193.6M) per Andrew's convention (PRD §10 Q4 — closed: maintain 49F structure as base).
  </objective>

  <context>PRD §9 W4.3. Orion has per-transaction Rep ID natively — no CHART-ALIGN needed (the 49F/BD complexity). The "firm rep" bucket (transactions attributed to the firm, not an individual advisor) should map to a `firm_rep` advisorKey bucket — parallel to BD's house-accounts pattern. PRD §10 Q7 (Keil dedup) affects leaderboard output — if Keil + Keil Financial Partners are separate rep records in silver, deduplicate before leaderboard ranking per convention in W3.1 schema spec. PRD §10 Q9 ("New Accounts Rep" 51,670 rows) — exclude from individual attribution per DS convention.</context>

  <compiler_tools_mandate>
    Phase 1: <run>comp-pipescript io D_00c (BD precedent)</run>
    <run>python -m py_compile ... && .tools/ds-commit-gate.sh ...</run>
    Phase 2: <run>comp-pipescript io I_D00c</run> — 0 COLUMN GAPS.
    Phase 3: <run>comp-pipescript deployed I_D00c</run> — MATCH.
    <run>comp-validate I_D00c --artifact /tmp/leaderboard.json</run> — exits 0 before signaling.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W4.1 (holdings) and W4.2 (NNA). Leaderboard consumes both."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Script exits 0. 0 COLUMN GAPS. ds-commit-gate pass.
    2. leaderboard.json has 11 advisors (per DS investigation brief: 11 Inflection advisors + firm-rep bucket).
    3. firm-rep bucket present for $193.6M / 287 HH.
    4. "New Accounts Rep" rows excluded from individual attribution.
    5. comp-validate: exits 0.
    6. Schema identical to 49F leaderboard.json.
    7. comp-pipescript deployed: MATCH.
    8. Session log.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">data/inflection/scripts/gold/I_D00c.portal_leaderboard.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">No CHART-ALIGN — Rep ID is natively per-day in Orion TRN.</requirement>
    <requirement id="2">firm-rep bucket: advisorKey = 'inflection_wealth_management' (or equivalent snake_case slug — confirm per schema spec).</requirement>
    <requirement id="3">Keil dedup per W3.1 convention.</requirement>
    <requirement id="4">comp-validate exits 0 before signaling COO.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">I_D00c committed + pushed.</deliverable>
    <deliverable type="document">Session log with comp-validate output.</deliverable>
  </deliverables>

  <do_not><rule>Do NOT add CHART-ALIGN logic.</rule><rule>Do NOT skip comp-validate.</rule></do_not>
</task_order>
