<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-16-advi-rollup-b3c-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-16</date>
    <status>complete</status><!-- 0.4.0_DS_ClientPlatform~B 2026-04-16. Commit 4fbe26dd. D_02 growth.ttm_nna + growth.ttm_pct. ttm_start = latest_date - 365 days; falls back to advisor earliest date for <365d history advisors. py_compile EXIT 0. comp-pipescript deployed D_02 MATCH. Spot-check deferred to post-PROD-nightly. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W3-addendum-B3c</wave>
  </metadata>

  <references>
    <ref type="precedent">ADVI_ROLLUP.B3b.ds-fee-window-revenue-d02 — must complete first (same D_02 per-advisor loop)</ref>
    <ref type="ds_response">DS design ACK 20260416T211259Z — confirmed computable, 1hr estimate, no new data sources</ref>
  </references>

  <context>
    The L2 Client List panel has a "Book Growth (TTM)" tile. Current PlatinumAdvisorSummary.growth
    carries ytd_pct + qtd_pct + ytd/qtd NNA. No TTM field. FE shows em-dash + "TTM" label until
    this lands (nothing broken, just pending).

    D_02 already has _nna_since(start_ts) wired to nna_atomic canonical (CN-P2) and _aua_at(start_ts)
    for period-start AUA. TTM is a single additional window: today - 365 days.
  </context>

  <objective>
    In D_02.advisor_client_detail.py, in the per-advisor loop where the growth block is built,
    add two fields:

      ttm_start = latest_date - timedelta(days=365)
      ttm_nna   = _nna_since(ttm_start)            # existing function, new window
      ttm_aua   = _aua_at(ttm_start)               # existing function, new window
      ttm_pct   = (ttm_nna / ttm_aua) if ttm_aua > 0 else 0.0

    Emit in the growth block:
      'growth': {
        'ytd_pct':  ...,   # existing
        'qtd_pct':  ...,   # existing
        'ttm_nna':  round(ttm_nna, 2),
        'ttm_pct':  round(ttm_pct, 4),
      }

    Edge cases:
    - ttm_aua == 0 or missing: ttm_pct = 0.0 (do not divide)
    - Advisor with fewer than 365 days of history: ttm_nna = _nna_since(earliest available date)
      (same behavior as nna_max — return all available history). Log count of advisors where
      history < 365 days in run summary.
  </objective>

  <wire_contract>
    PlatinumAdvisorSummary.growth additions (book.json -> D_04 -> portal):
      ttm_nna: float   -- trailing-12-month NNA ($), rounds to 2dp
      ttm_pct: float   -- ttm_nna / period-start AUA, rounds to 4dp
    Both required (non-null) in every emit after this TO ships.
  </wire_contract>

  <acceptance_criteria>
    1. book.json growth block for at least one advisor carries ttm_nna + ttm_pct.
    2. Travis Penfield ttm_nna is between nna_qtd and nna_max (sanity: TTM is longer than QTD,
       shorter than or equal to Max for advisors with >1yr history).
    3. Advisors with &lt;365 days history: ttm_nna == nna_max, log count in run summary.
    4. ttm_pct = 0.0 when ttm_aua == 0.
    5. py_compile D_02 exit 0.
    6. comp-pipescript deployed D_02: MATCH before upload.
    7. MCP COMPLETE to COO with commit hash + Travis ttm_nna + short-history advisor count.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_02</run>
        <expect>No new READs required — _nna_since and _aua_at already wired to nna_atomic.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile D_02.advisor_client_detail.py</run>
        <expect>Exit 0.</expect>
      </step>
      <step>
        <run>comp-pipescript deployed D_02</run>
        <expect>MATCH.</expect>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ROLLUP.B3b.ds-fee-window-revenue-d02"
      status="pending" description="Same D_02 per-advisor loop. Slot after B3b to avoid merge conflict on the growth block emit."/>
  </dependencies>
</task_order>
