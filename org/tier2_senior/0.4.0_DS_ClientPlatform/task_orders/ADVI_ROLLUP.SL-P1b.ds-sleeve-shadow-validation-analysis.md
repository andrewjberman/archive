<task_order>
  <metadata>
    <id>ADVI_ROLLUP.SL-P1b</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-22</date>
    <status>complete</status>
    <acked>2026-05-01 DS~B</acked><!-- Verdict: ITERATE. Apportionment denominator bug confirmed. Jones FAIL 86.7%. Fix B spec in ADVI_SLEEVE_P1B_ANALYSIS.md. Commit: see session log 2026-05-01. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>SL-P1b (post-shadow validation + analysis)</phase_label>
    <priority>P1 — gate between shadow-emit and production promotion. Without this, SL-P2 promote = ungrounded call.</priority>
    <sla>~1 day (analysis + report). After SL-P1 has ≥3 nightly shadow emissions.</sla>
    <decision_authority>Andrew 2026-04-22 — "make sure that one of the TOs attached to ROLLUP is the actual validation and analysis post-run."</decision_authority>
    <dependency to="SL-P1" status="pending">SL-P1 must fire in nightly and produce ≥3 days of `gold/timeseries/holdings_lots_shadow/{date}.parquet`. Current block: bd-gold-nightly-fallback re-enable post chain recovery. Flips to pending when shadow count >= 3 dates.</dependency>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #9)</ref>
    <ref type="ds_plan">docs/architecture/ADVI_SLEEVE_PLAN.md</ref>
    <ref type="predecessor">ADVI_ROLLUP.SL-P0.ds-sleeve-discovery.md (decision memo at docs/architecture/ADVI_SLEEVE_P0_DECISION.md)</ref>
    <ref type="direct_predecessor" status="pending">ADVI_ROLLUP.SL-P1.ds-sleeve-shadow-emit.md — code shipped `28818eaf`, gated on nightly re-enable</ref>
    <ref type="direct_successor" status="staged">ADVI_ROLLUP.SL-P2.ds-sleeve-promote-to-production.md — gated on this TO's PROMOTE verdict</ref>
    <ref type="canonical_test_case">Jones z0817905851: silver `$2,396,510` vs gold `$82,423` — shadow should close this gap to ≤2%</ref>
  </references>

  <objective>
    Evaluate the sleeve-shadow output after ≥3 nightly emissions. Produce an explicit PROMOTE / ITERATE / ABANDON verdict for SL-P2 to act on.

    This TO is the CTO-audit layer between "we can emit sleeve lots" (P1) and "we replace prod holdings_lots with sleeve-augmented lots" (P2). No promotion happens based on Jones-alone; this TO forces a systematic look across the full 403 mapped-no-RPS cohort + stability + edge cases.
  </objective>

  <scope>
    <files>
      <file action="read-only">gold/timeseries/holdings_lots_shadow/*.parquet (S3 — ≥3 nightly emissions)</file>
      <file action="read-only">gold/timeseries/holdings_lots/*.parquet (production comparison)</file>
      <file action="read-only">silver/unrealized/*.parquet (ground truth per SL-P0 decision)</file>
      <file action="read-only">silver/allocations/*.parquet (account-level MV comparison)</file>
      <file action="create">docs/architecture/ADVI_SLEEVE_P1B_ANALYSIS.md (verdict memo)</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="cohort-level-parity">
      For the full 403 mapped-no-RPS cohort on the latest shadow date:
      - Shadow `sum(market_value)` vs silver `sum(cash_market_value + amv)` — absolute $ delta + % delta
      - Per-account parity distribution: count of accounts within 2% / 5% / 10% / worse
      - Named top-20 worst-parity accounts with hypotheses (corp action missing? cost basis source drift? sleeve-confidence-edge?)
    </deliverable>
    <deliverable id="stability-over-time">
      Compare shadow emissions across the ≥3 available dates:
      - Per-account market_value day-over-day change distribution
      - Any account with >20% day-over-day drift without a corresponding silver event → flag for RCA
      - Cohort-count drift: are accounts entering/leaving the cohort? Is confidence score stable?
    </deliverable>
    <deliverable id="canonical-test-cases">
      - Jones z0817905851: explicit `account_market_value`, silver target `$2,396,510`, delta %, PASS/FAIL at 2% threshold
      - 3-5 additional named cases spanning the confidence distribution (high / mid / low sleeve_confidence) — document each
    </deliverable>
    <deliverable id="downstream-reader-counterfactual">
      For each downstream consumer of `holdings_lots/` (identified via `comp-blast gold/timeseries/holdings_lots/`), answer: if we promote shadow as authoritative, does ANY downstream artifact move in a way that surprises us? Projected impact on firm AUA, per-advisor AUA, D_04 summary, D_02 per-advisor detail.
    </deliverable>
    <deliverable id="verdict">
      Written verdict committed to `docs/architecture/ADVI_SLEEVE_P1B_ANALYSIS.md`:
      - PROMOTE — shadow quality sufficient; SL-P2 flips to pending + the merge/cutover strategy (full swap, additive, cohort-gated)
      - ITERATE — named fixes needed first; enumerate specific issues; SL-P1 code patches before re-emitting
      - ABANDON — cost/value ratio doesn't justify; pull SL-P1 from nightly; document the learning
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">≥3 dates of `holdings_lots_shadow/{date}.parquet` present in S3 before analysis starts.</ac>
    <ac id="2">Cohort-level parity table committed with firm-wide $ delta + distribution.</ac>
    <ac id="3">Stability day-over-day table committed with drift distribution + any flagged accounts.</ac>
    <ac id="4">Jones z0817905851 test result recorded with PASS/FAIL at 2% threshold.</ac>
    <ac id="5">Downstream-reader counterfactual for every consumer of `holdings_lots/` (enumerate via `comp-blast`).</ac>
    <ac id="6">Verdict committed to `docs/architecture/ADVI_SLEEVE_P1B_ANALYSIS.md` with explicit PROMOTE / ITERATE / ABANDON label.</ac>
    <ac id="7">MCP to 2.0.0_SA_COO with verdict summary + commit hash. COO routes to CTO for co-sign if PROMOTE.</ac>
    <ac id="8">Session log with Compiler Tools section (`comp-blast`, `comp-validate holdings_lots_shadow`, parity distribution SQL/parquet scan).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1 (before analysis):
    <run>comp-validate holdings_lots_shadow --artifact s3://opal-data-bd/gold/timeseries/holdings_lots_shadow/{latest_date}.parquet</run>
    Expected: exit 0; confirms schema parity with production.
    <run>comp-blast gold/timeseries/holdings_lots</run>
    Expected: enumerate every downstream consumer — each one needs a counterfactual entry.

    Phase 2 (during analysis):
    <run>comp-pipescript feeds B_01</run>
    Expected: confirm silver/unrealized is still the authoritative source for sleeve; no drift from SL-P0 decision memo.

    Phase 3 (after verdict):
    <run>comp-blast holdings_lots_shadow</run>
    Expected: still 0 readers (shadow stays shadow until SL-P2). If anything started reading, flag it — may indicate accidental pre-promotion.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <downstream to="SL-P2" status="staged">Promote-or-abandon decision is this TO's output. SL-P2 inherits the merge/cutover strategy from this verdict.</downstream>
    <upstream to="SL-P1" status="pending">Blocked until SL-P1 first-fires and ≥3 nightlies accumulate shadow artifacts.</upstream>
    <potential_reader_coordination>If verdict = PROMOTE, downstream consumers of `holdings_lots/` (D_02, D_04, D_00c, etc.) may need coordinated re-run — route through COO at SL-P2 authoring, not under this TO.</potential_reader_coordination>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT make promotion changes to any production `holdings_lots` key or reader code under this TO — that's SL-P2's scope.</rule>
    <rule>Do NOT run the analysis on a single day of shadow output. Minimum 3 dates to observe stability.</rule>
    <rule>Do NOT default to PROMOTE if Jones alone passes — cohort-level parity + stability are co-requirements.</rule>
    <rule>Do NOT skip the downstream counterfactual. If we promote, we own the blast-radius characterization upfront, not in post-mortem.</rule>
  </do_not>
</task_order>
