<task_order>
  <metadata>
    <id>YALP_MDSRC.A4</id>
    <slug>ds-ycharts-granularity-depth-full-entity-sweep</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <paired_with>0.7.0_AE_CloudOps~A</paired_with>
    <date>2026-05-21</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — Andrew-direct (2026-05-21): "It's not enough to look at the S&P alone; we need to explore every index and every ETF tracked on the portal." PAIRED TO (Andrew directive 2026-05-21): 0.1.0_DS_MarketIntelligence = deliverable lead (the analysis, verdicts, matrix, brief — holds the A3 internal-API context + crosswalk + probe method); 0.7.0_AE_CloudOps~A = paired AE, owns the YCharts authenticated-session / capture side (see <pairing> block). 0.7.0_AE_CloudOps BASE is deliberately NOT on this TO — base stays on the F2/F5/C1 critical path uninterrupted. ~A's A4 work begins AFTER ~A completes the F2/F3 post-apply verification-harness run (that fires on base's F2 v1.0.1 apply-complete signal — minutes of work); 0.1.0_DS may begin Phase 0 universe-enumeration (DynamoDB / etf_returns.json reads — no YCharts seat needed) immediately in parallel. A4 feeds C2 as a pre-build input — land before/alongside the C2 build.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — Andrew-direct. A4 establishes, per entity, whether a YCharts pull can actually replace the Bloomberg data_pkl feed for that surface. A3 established the endpoint MAPPING; A4 establishes the GRANULARITY + DEPTH the endpoints actually deliver. Without A4, C2 builds against an unverified n=1 assumption (only S&P 500 was spot-probed).</priority>
    <sla>~1-2 effort-days — an investigation sweep of ~78-83 entities, one series pull + analysis each.</sla>
  </metadata>

  <references>
    <scoping_brief>docs/briefs/mdsrc-ycharts-granularity-depth-scoping-20260521.md (commit 8ae8c3056, origin/CLOUD) — the DS-authored scoping brief. CONSUME THIS AS THE PRIMARY INPUT: §2 entity universe, §3 the per-entity checks, §4 method, §5 deliverable, §6 dependencies/risks, §7 seed ACs.</scoping_brief>
    <a3>docs/briefs/mdsrc-ycharts-internal-api-20260520.md + the P3 mapping mdsrc-ycharts-internal-api-mapping-20260520.tsv — A3 reverse-engineered the YCharts internal API: which endpoint serves each requirement, params, JSON path, schema. A3 did NOT establish per-entity granularity/depth — that is exactly the A4 gap.</a3>
    <crosswalk>mdsrc-ycharts-ticker-map-20260520.csv (71-row crosswalk, commit dc01d4b8a) — entity -> YCharts symbol. MUST be used WITH the A2/A3 corrections applied: the MSCI-country LOC-variant fix (^MS**L) and the bond plain-USD symbols. A wrong-variant symbol granularity-checks the wrong series — that is the single biggest correctness risk.</crosswalk>
    <prd>docs/architecture/YALP_MDSRC.md — the parent PRD; portal granularity+depth requirements (~6yr daily for the DynamoDB backbone; monthly for Valuation time_series + risk-premium surfaces).</prd>
    <standard>docs/architecture/THIRD_PARTY_DATA_INTEGRATION_STANDARD.md (RATIFIED, 73e4da697) — A4 drives the YCharts internal/backend API with the live authenticated session. This is an INTEGRATION against the provider's backend API — never "scrape".</standard>
  </references>

  <pairing>
    A4 is a PAIRED TO per Andrew's 2026-05-21 directive. The split:

    0.1.0_DS_MarketIntelligence — DELIVERABLE LEAD:
    - Owns the analysis and the deliverable: the per-entity granularity/depth matrix, the meets/partial/gap verdicts, the C2-implications brief.
    - Owns symbol resolution against the corrected crosswalk + the securities-search attempt for the 5 unmapped entities.
    - Owns universe enumeration (Phase 0 DynamoDB / etf_returns.json reads — no YCharts seat needed; may start immediately).
    - Defines what to probe per entity and interprets the returned series (granularity, depth, resample boundary).
    - Flips A4 <status> to complete; RAVC2 to COO + CC CTO.

    0.7.0_AE_CloudOps~A — PAIRED AE (YCharts session / capture side):
    - Owns the YCharts authenticated-session mechanics: holding the F1 single-concurrent-session seat, auth/credential handling, driving the fund_data.json date-bounded series pulls (+ table_data snapshots) at a measured request rate — the same capture mechanism used in A1/A3.
    - Runs the actual API capture for each entity 0.1.0_DS enumerates; hands the raw series back to 0.1.0_DS for the granularity/depth analysis.
    - This keeps the YCharts-seat work in the ~A lane so it does NOT contend with 0.7.0_AE_CloudOps BASE, which stays on the F2/F5/C1 critical path.
    - ~A begins A4 only AFTER completing the F2/F3 post-apply verification-harness run (RAVC2 that first). RAVC2s ~A's capture-side contribution to 0.1.0_DS + COO.

    Working mode: tight pair — 0.1.0_DS enumerates + specifies, ~A captures, 0.1.0_DS analyses. MCP each other directly to hand off entity batches; do not route batch handoffs through COO. Surface to COO only on a blocker (seat contention, an entity class the capture mechanism can't reach, a symbol that won't resolve).
  </pairing>

  <context>
    A3 mapped the YCharts internal API per portal requirement but verified granularity/depth for exactly ONE entity — S&P 500 (^SPX), Andrew's spot-probe: fund_data.json returned ~76yr depth + clean daily (trading-day) granularity when date-bounded. Encouraging but n=1. Granularity and depth genuinely vary by entity-class — older/smaller/foreign/bond/commodity series and ETFs can have shorter history or coarser native granularity, and the daily-vs-weekly auto-resample boundary can sit at a different point per entity. A4 verifies granularity + depth for EVERY portal-tracked index and ETF — a full sweep, not a sample.

    COO SCOPING DECISION (the brief flagged this for a COO/Andrew call): the 7 COMMODITY entities ARE IN SCOPE. They face the identical granularity/depth question; excluding them would leave a known market-data gap and force a follow-up sweep. Fold them in. Total universe ~78-83 entities (53 INDEX + 11 BOND_INDEX + 7 COMMODITY + the ETF set; exact ETF count is the TO's first deliverable).
  </context>

  <scope>
    <in_scope>
      PHASE 0 — UNIVERSE ENUMERATION + SYMBOL RESOLUTION:
      - Enumerate the exact entity universe: INDEX (DynamoDB opal-portal-market-data entity_type=INDEX, ~53), BOND_INDEX (~11), COMMODITY (7 — IN SCOPE per the COO decision above), and the ETF set (json/benchmarks/etf_returns.json / the yang ETF-benchmark set WS2-MP-04 — produce the exact ETF list as the first deliverable).
      - Resolve every entity to its YCharts symbol via the 71-row crosswalk WITH the A2/A3 corrections applied (MSCI-country ^MS**L LOC-variant fix; bond plain-USD symbols).
      - The 5 entities genuinely-unmapped from A3-P4 (Silver, Brent, Natural Gas, Copper, MSCI USA Size): attempt symbol resolution via the YCharts securities-search endpoint first. Any entity still unresolved after that attempt is scoped "blocked-pending-symbol" — listed explicitly, NOT silently dropped, and NOT blocking the rest of the sweep.

      PHASE 1 — PER-ENTITY GRANULARITY + DEPTH PROBE (for every resolved entity):
      - Finest granularity obtainable — date-bound the request, confirm whether daily (trading-day) data returns, note inter-point spacing.
      - History depth — earliest available data point; total span in years.
      - Daily-vs-resample boundary — at what range / maxPoints the endpoint stops returning daily and auto-resamples to weekly/monthly (so C2 knows how to bound its pulls).
      - Requirement-match verdict — meets / partial / gap, against the consuming portal surface's granularity+depth requirement (~6yr daily for the DynamoDB backbone; monthly for Valuation time_series + risk-premium surfaces).
      - Endpoint note — confirm fund_data.json (date-bounded) is the canonical time-series endpoint for C2, OR nail the correct general_data.json time-series invocation (general_data.json returned empty for the metric=price time-series combo in the A3 probe — resolve that ambiguity for C2).

      PHASE 2 — DELIVERABLE:
      - A committed machine-readable per-entity matrix: one row per entity — entity, yc_symbol, finest_granularity, history_depth_years, earliest_date, resample_boundary, portal_requirement, verdict.
      - A brief: count of meets vs partial vs gap; entity-classes that systematically differ; C2 implications (how to bound pulls; any entity that cannot be daily-sourced from YCharts and therefore STAYS Bloomberg-pkl — that is a real migration-scope finding).
    </in_scope>
    <out_of_scope>
      - Building the C2 pull itself — A4 is a pre-build verification input to C2, not the build.
      - Re-doing A3's endpoint mapping — A4 consumes A3's mapping; it adds the granularity/depth dimension only.
      - Resolving symbols beyond a single securities-search attempt for the 5 unmapped entities — anything still unresolved is documented as blocked-pending-symbol, not chased indefinitely.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <note>A4 is a YCharts-internal-API investigation TO — it modifies no gold script, no portal component, no route, no IAM, no schema. No comp-* graph tool covers the YCharts backend-API probe surface, so the phase assertions below are structural/empirical self-checks (the audit record the TO_COMPILER_GATE requires), not comp-* runs. The one graph-relevant downstream is C2; comp- coverage of C2 is A3/C2's mandate, not A4's.</note>
    <phase id="0" when="after universe enumeration, before probing">
      <step>
        <run>Count the enumerated universe and cross-check against the brief's expected classes (INDEX ~53 + BOND_INDEX ~11 + COMMODITY 7 + ETF set).</run>
        <expect>Total ~78-83 entities; the ETF count is concrete (no longer "~5"); every entity has a resolved YCharts symbol OR is on the explicit blocked-pending-symbol list.</expect>
        <if_mismatch>If the count is materially short of ~78 or a class is missing, the enumeration is incomplete — re-pull the DynamoDB entity_type partitions before probing. Do not probe a partial universe.</if_mismatch>
      </step>
      <step>
        <run>Verify the crosswalk A2/A3 corrections are applied for every resolved symbol (spot-check the MSCI-country ^MS**L variants + the bond plain-USD symbols against the A3 brief).</run>
        <expect>No symbol uses a pre-correction variant. MSCI-country entities resolve to ^MS**L form; bond indices to the plain-USD symbols.</expect>
        <if_mismatch>A wrong-variant symbol granularity-checks the wrong series — re-resolve from the corrected crosswalk before probing that entity.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before declaring the TO complete">
      <step>
        <run>Row-count the committed matrix against the Phase-0 universe.</run>
        <expect>Exactly one matrix row per enumerated entity; every row has all 8 columns populated; blocked-pending-symbol entities present as rows with the verdict column = blocked, not absent.</expect>
        <if_mismatch>A missing row = a skipped entity = AC1 fail. Probe it or, if blocked-pending-symbol, add the explicit row.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - F1 SINGLE YCHARTS SESSION SEAT: A4's sweep needs the live authenticated YCharts session. The seat is owned, for A4, by the paired AE 0.7.0_AE_CloudOps~A (see <pairing>) — ~A holds the seat for the measured-rate sweep and releases it on completion. This is precisely why A4 is paired with ~A and NOT with 0.7.0_AE_CloudOps base: base owns C1 (the YCharts credential-pipeline work) and is on the F2/F5/C1 critical path; routing A4's seat use through ~A keeps it off base's path. Still: per the F1 single-concurrent-session constraint there is exactly ONE seat — ~A must confirm with base that no C1 YCharts-seat activity overlaps the A4 sweep window before starting (a quick ~A<->base MCP), and sequence around it if it does. ~A begins the A4 sweep only after completing the F2/F3 verification-harness run.
    - A4 FEEDS C2: the granularity/depth matrix is a C2 pre-build input. Land A4 before or alongside the C2 build. C2 owner (0.1.0_DS — same agent) consumes the matrix to bound its pulls and to know which entities stay Bloomberg-pkl.
    - No silver/bronze/gold script or S3-data-prefix changes — auto-rule 4 (data reprocess scope) is N/A; A4 produces a docs/briefs/ matrix + brief only.
  </cross_domain_coordination>

  <acceptance_criteria>
    - AC1 — every portal INDEX + BOND_INDEX + COMMODITY + ETF enumerated and probed; none skipped. Entities unresolvable to a YCharts symbol after one securities-search attempt are present as explicit blocked-pending-symbol rows, not omitted.
    - AC2 — per entity: finest granularity, history depth (earliest date + span-years), and daily-vs-resample boundary recorded from a LIVE pull (not inferred).
    - AC3 — per entity: a meets / partial / gap verdict against the consuming portal surface's granularity+depth requirement.
    - AC4 — any entity YCharts cannot serve at the required granularity/depth explicitly flagged as stays-Bloomberg-pkl — a real migration-scope finding called out in the brief, not buried in the matrix.
    - AC5 — the canonical C2 time-series endpoint question resolved: fund_data.json (date-bounded) confirmed as canonical, OR the correct general_data.json time-series invocation nailed.
    - AC6 — committed machine-readable matrix (docs/briefs/) + summary brief; the session log Compiler Tools section reproduces each Phase-0/Phase-2 <run> + observed result + pass/fail vs <expect>.
    - AC7 — RAVC2 to COO + CC CTO on completion; the brief explicitly states the C2 implications.
  </acceptance_criteria>
</task_order>
