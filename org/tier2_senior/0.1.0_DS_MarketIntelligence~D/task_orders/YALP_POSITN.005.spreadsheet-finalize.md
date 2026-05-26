<task_order>
<metadata>
  <to_id>YALP_POSITN.005</to_id>
  <project>YALP_POSITN</project>
  <title>Side-by-side spreadsheet finalize (CSV + markdown narrative)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~D</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <status>complete</status>
  <go_source>ws COO MCP-body CASCADE GO 2026-05-26T~19:20Z</go_source>
</metadata>
<scope>
Generate side-by-side spreadsheet CSV with per-row dual-T* + verdict + sourcing/methodology columns from positioning_data + holdings_attribution + TO-002 pull results. Markdown narrative folded into brief §14-§16.
</scope>
<acceptance_criteria>
- AC1: CSV generated programmatically (no manual entry)
- AC2: Per-row t_star column populated per dual-T* discipline
- AC3: Verdict class column populated per Level-2 taxonomy
- AC4: Sourcing/methodology column populated for all GAP-class rows
- AC5: Verdict distribution summary in §14.2
</acceptance_criteria>
<expected_evidence>
- `docs/briefs/yalp_positn_side_by_side_spreadsheet_2026-05-22.csv` (4943 data rows)
- Generator: `.runtmp/yalp_positn_to002/populate_spreadsheet.py` (gitignored)
- Brief §14.2 verdict distribution table
</expected_evidence>
</task_order>
