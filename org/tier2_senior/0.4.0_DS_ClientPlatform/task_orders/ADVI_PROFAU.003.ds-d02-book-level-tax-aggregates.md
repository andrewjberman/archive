<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-13-profau-003</id>
    <issued_by>2.0.0_SA_COO (retroactive — DS self-delivered from audit roadmap)</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-13</date>
    <status>complete</status>
    <project_code>ADVI_PROFAU</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/audits/advisor-profile-book-input-mapping-2026-04-13.md</ref>
    <ref type="audit_response">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/profau_gap_audit_response.md (Q1)</ref>
  </references>

  <objective>
    Add book-level capital gains and cost basis aggregates to D_02 advisor summary output,
    so that `platinum/advisors/{id}/summary.json` carries `capital_gains_ttm` and
    `cost_basis_by_year` in the `tax_exposure` field. This unblocks DE to wire
    `TaxCostBasisPanel` at L2 (advisor/book level) in AdvisorBookView.
  </objective>

  <scope>
    Script: `data/black_diamond/scripts/gold/D_02*.py`
    Changes: add `capital_gains_ttm` + `cost_basis_by_year` aggregation loop across
    per-client `detail.json` entries in the advisor book builder. Emit both fields
    under `tax_exposure` in `platinum/advisors/{id}/summary.json` via D_04 passthrough.
    Note: `top_gain_positions` is a separate follow-up TO (requires D_04 holdings_lots join).
  </scope>

  <completion_evidence>
    Commit: b2e4e668 — "0.4.0_DS_ClientPlatform: ADVI_PROFAU.003 -- D_02 book-level tax aggregates (capital_gains_ttm, cost_basis_by_year)"
    QA verification: PENDING (c6i.16xlarge capacity issue during 2026-04-13 session; DS will retry and MCP-signal AE/DE on confirmation)
    DE unblock condition: QA run confirms fields present in platinum/advisors/{id}/summary.json
  </completion_evidence>

  <acceptance_criteria>
    - `platinum/advisors/{id}/summary.json` contains `tax_exposure.capital_gains_ttm` (number, $USD)
    - `platinum/advisors/{id}/summary.json` contains `tax_exposure.cost_basis_by_year` (array of {year, cost_basis, market_value, unrealized_gain})
    - Values cross-check against sum of per-client `detail.json` capital gains for the same advisor
    - D_04 passthrough requires no changes (verified by DS in message to DE)
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1 (pre-write): comp-pipescript io D_02 — verify D_04 reads book.json and emits tax_exposure passthrough.
    Phase 2 (pre-commit): comp-trace capital_gains_ttm --direction both — confirm terminal at platinum/advisors/{id}/summary.json.
    Phase 3 (post-commit): QA runner spot-check: aws s3 cp s3://opal-data-bd/platinum/advisors/{id}/summary.json - | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('tax_exposure',{}).get('capital_gains_ttm','MISSING'))"
  </compiler_tools_mandate>

  <cross_domain_coordination>
    DE ADVI_PROFAU.005 wiring depends on this TO. DE must not wire TaxCostBasisPanel at L2 until
    QA run confirms field presence. DS to MCP-signal DE when QA verified.
  </cross_domain_coordination>
</task_order>
