<task_order>
  <metadata>
    <id>YALP_MDSRC.A5</id>
    <slug>ds-ycharts-har-endpoint-assessment</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-05-21</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — Andrew-direct (2026-05-21). Andrew had Alyssa record an HAR (HTTP Archive — a full browser network capture) of a YCharts session and is handing the file directly to 0.1.0_DS. This is the INTERIM unblock: live YCharts exploration is gated on the dedicated seat Andrew is acquiring, but a static HAR lets 0.1.0_DS assess endpoints NOW without a live seat. A5 is 0.1.0_DS's immediate priority — its output feeds the A4 follow-ups + the C2 pre-stage already in flight. Interleave with / ahead of C2 pre-stage.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — interim YCharts-endpoint unblock. Live exploration waits on the dedicated seat (D1-cutover gate); the HAR is a static capture that resolves endpoint DISCOVERY now. Directly feeds two in-flight items: the A4 36-entity general_data.json invocation pinning + the 9 blocked-pending-symbol resolutions, and C2 pre-stage endpoint coverage.</priority>
    <sla>~0.5-1 effort-day — a focused static-artifact analysis, no live API calls.</sla>
  </metadata>

  <references>
    <har>The YCharts session HAR — recorded by Alyssa, handed to 0.1.0_DS by Andrew. CONFIRM THE FILE PATH back to COO as the first step (Andrew is delivering it; path TBD). SECURITY: an HAR captures live request headers — Cookie / Authorization / session tokens. Do NOT commit the raw HAR to git. Keep it under a gitignored path (.runtmp/ or similar). The committed deliverable is the SANITIZED assessment brief — endpoint shapes + params only, never cookie/token values.</har>
    <a3>docs/briefs/mdsrc-ycharts-internal-api-20260520.md + the P3 mapping .tsv — A3's reverse-engineered endpoint map. A5 extends/corrects it from real captured traffic.</a3>
    <a4>docs/briefs/mdsrc-a4-granularity-depth-matrix-20260521.csv + brief (d4a61092f) — A4's 76-entity matrix. A5 targets A4's two open residues (below).</a4>
    <standard>docs/architecture/THIRD_PARTY_DATA_INTEGRATION_STANDARD.md (RATIFIED) — reverse-engineer the provider's backend API; an HAR analysis is exactly that — reading the contract the YCharts app itself uses. Never "scrape".</standard>
  </references>

  <context>
    A3 mapped the YCharts internal API; A4 swept granularity/depth and left two endpoint residues that need browser-in-loop capture: (1) the general_data.json working invocation — A3 saw metric=price return empty, and general_data.json is the canonical endpoint for the 29 MSCI + 7 Bloomberg-bond indices (the 403s on it were operational session-eviction per Andrew's ruling, NOT entitlement — full coverage stands); (2) the securities-search XHR — ~A could not locate it without a browser in the loop (needed for the 5 unmapped symbols: Silver/Brent/NatGas/Copper/MSCI-USA-Size). An HAR is a browser-in-loop capture — it contains both, if Alyssa's session exercised them. A5 mines the HAR to resolve these + inventory any other endpoint coverage useful to C2.

    SCOPE BOUNDARY: the HAR is a STATIC snapshot. A5 resolves endpoint DISCOVERY — exact endpoints, params, invocation shapes, response schemas. It does NOT and cannot produce live data pulls or the 36-entity granularity/depth NUMBERS — those still require a live session (~A's 2nd capture batch, on a contention-free or dedicated seat). A5 hands the capture mechanism a correct invocation spec; it does not replace the capture.
  </context>

  <scope>
    <in_scope>
      PHASE 0 — INGEST + INVENTORY:
      - Confirm the HAR file path (from Andrew) back to COO. Place/keep it under a gitignored path.
      - Inventory what the HAR captured: which YCharts pages/views, which XHR endpoints, which entities/symbols, the auth/session mechanics visible in the request flow.

      PHASE 1 — TARGETED ENDPOINT EXTRACTION (priority order):
      1. general_data.json — the working invocation: exact endpoint, the metric/params that return a non-empty index time series, the calc semantics, response schema/JSON path. This is the A4-36-entity capture-spec input.
      2. The securities-search XHR — endpoint, params, response shape — the symbol-resolution mechanism for the 5 A4-unmapped entities. If the HAR exercised a search, resolve as many of the 5 as the capture allows.
      3. Any other endpoints in the HAR relevant to C2 / portal requirements that A3 did not pin or pinned incompletely — corrections + additions to the A3 map.

      PHASE 2 — DELIVERABLE:
      - A committed, SANITIZED endpoint-assessment brief: what the HAR resolved (per endpoint: invocation + params + schema), what it did NOT cover (gaps still needing the live seat), and how each finding feeds the A4 follow-ups + C2.
      - If the HAR pins the general_data.json invocation: hand the corrected capture spec to 0.7.0_AE_CloudOps~A (it owns the A4 36-entity 2nd capture batch) and to COO.
    </in_scope>
    <out_of_scope>
      - Live YCharts API calls — A5 is HAR-only; live exploration waits on the dedicated seat.
      - The actual 36-entity granularity/depth capture — that is ~A's 2nd batch; A5 only supplies the invocation spec.
      - Committing the raw HAR or any cookie/token value to git.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <note>A5 is a static-artifact (HAR) analysis — it modifies no gold script, portal component, route, IAM, or schema. No comp-* graph tool covers HAR analysis; the phase assertions are structural/empirical self-checks (the audit record the TO_COMPILER_GATE requires).</note>
    <phase id="0" when="after HAR ingest">
      <step>
        <run>Inventory the HAR's captured XHR endpoints + entities; check coverage against the A5 priority targets (general_data.json, securities-search, C2-relevant endpoints).</run>
        <expect>A coverage list. If the HAR does NOT contain a general_data.json call or a securities-search XHR, that is a finding — surface to COO immediately (the HAR may need a re-record with targeted actions).</expect>
        <if_mismatch>If a priority target is absent from the HAR, do not fabricate it from A3 inference — report the gap; COO decides whether to request a targeted re-record.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before declaring complete">
      <step>
        <run>Verify the committed brief contains zero cookie/Authorization/token values (grep the deliverable for the captured session-cookie substrings).</run>
        <expect>Zero secret values in the committed brief — endpoint shapes + params only. Raw HAR not staged for commit.</expect>
        <if_mismatch>Strip any leaked secret value before commit; the raw HAR stays gitignored.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - FEEDS the A4 36-entity 2nd capture batch (0.7.0_AE_CloudOps~A): A5's general_data.json invocation spec is the input ~A needs to pin its capture. Hand it directly to ~A.
    - FEEDS C2 pre-stage (0.1.0_DS + 0.2.0_DS): corrected/extended endpoint coverage. A5 should land before C2's endpoint-dependent build steps.
    - The dedicated YCharts seat (Andrew's procurement) remains the gate for LIVE exploration + production operation — A5 does not change that; it maximizes what is learnable from the static capture in the interim.
    - No silver/bronze/gold or S3-data changes — auto-rule 4 N/A.
  </cross_domain_coordination>

  <acceptance_criteria>
    - AC1 — HAR ingested; captured-coverage inventory produced; HAR path confirmed to COO; raw HAR kept gitignored.
    - AC2 — general_data.json: either the working invocation (endpoint + metric/params + schema) is pinned from the HAR, OR documented as not-present-in-this-HAR with a re-record request.
    - AC3 — securities-search XHR: endpoint + params + response shape pinned from the HAR if present; the 5 unmapped entities resolved as far as the capture allows.
    - AC4 — committed SANITIZED endpoint-assessment brief; Phase-2 self-check confirms zero secret values in the committed deliverable.
    - AC5 — findings explicitly routed: general_data.json spec to ~A; endpoint coverage to C2; gaps-needing-the-seat listed.
    - AC6 — session log Compiler Tools section reproduces the Phase-0/Phase-2 self-checks; RAVC2 to COO + CC CTO.
  </acceptance_criteria>
</task_order>
