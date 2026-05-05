<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-28-infship-a2-orion-asset-api-vendor-investigation</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.6.1_AE_PartnerETL~B</issued_to>
    <date>2026-04-28</date>
    <status>complete</status><!-- 2026-05-05: verdict — per-client REST GET (pull_inflection_assets_v2.py, HISTBF.003) satisfies AC#1; Envision Asset-grouping OFFICIALLY DECLINED (4 timeouts 300-900s all scopes); Track 1 dead-end (no async pattern in HAR(10)); Track 2 viable (per-account GET 322ms) but not required for v1; catalog updated with new Portfolio/Assets section + production sourcing row; RAVC4 sent to CTO 2026-05-05 -->
    <project_code>ADVI_INFSHIP</project_code>
    <to_serial>A2</to_serial>
    <priority>MEDIUM</priority>
    <prd>docs/architecture/ADVI_INFSHIP.md (Phase 1.L4 Path C deferral)</prd>
  </metadata>

  <objective>
    Determine whether Orion Connect's Custom Reports / Envision Generate POST
    can deliver Asset-grouping (per-(account,asset) holdings) data within an
    operational time budget, OR conclusively classify the endpoint as
    vendor-blocked. INFSHIP Phase 1.L4 currently ships via Path C (canonical
    holdings parquet, advisor_key allowlist filter, $91.8M Inflection-only)
    because the synchronous Generate endpoint timed out 4x during
    DS~D's pull attempts. Path C is functional for v1 but is structurally
    inferior to a direct API pull — it inherits canonical's chain-rerun
    cadence and multi-firm contamination requires post-filter.
  </objective>

  <context>
    DS~D's L4 RAVC4 (2026-04-28 ~05:49Z, commits f470da03 / 976913f6 /
    6d91064d) documented the timeout pattern empirically:

      v1 (firm scope, 3y window, 300s timeout):    timed out
      v2 (entityIds=[3,11,12], 3y window, 900s):   timed out
      v3 (entityIds=[3,11,12], 7d window, 900s):   timed out
      v4 (firm scope, 7d window, 900s):            timed out

    Sanity probe: GET /Verbose?top=1 returned 200 in 0.9s (API itself
    reachable; endpoint-specific load issue). All orphan saved queries
    cleaned (DELETE 204 confirmed) — not a query-state issue.

    DS~D's pull script: data/orion/scripts/pull_inflection_assets.py
    (commits 4d1bba92 + 76dcba9f naming-fix). Worth using as the probe
    script base for any new request shape — it already handles auth +
    saved-query lifecycle + response framing.

    Custom Reports endpoint family:
      POST /api/v1/Reporting/Custom/{id}/Generate/csv
    Envision endpoint family:
      POST /api/v1/Reporting/Envision/ExcelReports/{id}/Generate
    Both observed in HAR captures; both synchronous — limit appears to be
    the Generate execution itself, not the request shape.

    Path C silver currently lands $91.8M Inflection-only AUA at
    s3://opal-data-inf/silver/api_dims/assets/snapshot_date=YYYY-MM-DD/
    (snapshot date = canonical parquet date). Once INFGRD.004 chain rerun
    completes (currently on Andrew hold; will trigger autonomously once
    ORIAPI's autonomous JWT pipeline lands), Path C silver auto-refreshes
    toward $200M. Functional for INFSHIP Phase 2 DE B5/B6.

    INFSHIP.A2 is therefore not a v1 ship blocker. It is a structural
    upgrade for v2 — direct-pull source-of-truth for assets dim, mirroring
    the pattern DS~B/DS~A/DS~C use for billing/tax/performance/household.
  </context>

  <files_to_modify>
    <file>data/orion/scripts/pull_inflection_assets.py (probe iterations on top of DS~D's base)</file>
    <file>docs/architecture/INFLEC_API_ENDPOINTS_CATALOG.md (update Custom Reports + Envision sections with vendor-investigation findings)</file>
    <file action="create-if-needed">data/orion/scripts/pull_inflection_assets_async.py (only if a polling/async endpoint variant is discovered)</file>
  </files_to_modify>

  <spec_summary>
    Three investigation tracks, ordered by expected payoff:

    **Track 1 — Async/Polling Endpoint Discovery (HIGH payoff if it exists).**
    HAR-recapture a manual Asset grouping export from the Orion Connect web UI
    in long-format (>1 hour data window). Look for any `Status` or `Poll` or
    `Job` endpoint in the request chain — an async pattern would mean Generate
    POST returns a job_id immediately, then a separate GET polls for completion
    and downloads. If found, port to pull_inflection_assets_async.py and
    document in catalog.

    Probe via `.tools/har-scan.py` (already shipped). Target HAR: a 24h+
    Asset-grouping report download from the UI.

    **Track 2 — Per-Account Batching (MEDIUM payoff).**
    DS~D noted: "If v4 also times out, next move is per-account chunking
    (split 2,755 Inflection accounts into N batches via entity='Account' +
    entityIds=[<batch>])." Test at multiple batch sizes (50 / 100 / 250) to
    find the largest batch that completes within 60-120s. Build a parallel
    pool dispatching N workers; concatenate results.

    Risk: 2,755 / 100 = 28 batches; if each takes 60s and we run 4 in
    parallel = ~7 min total, acceptable. If each takes 300s and we run 1 at
    a time = ~140 min, unacceptable. Probe small first.

    **Track 3 — Vendor Ticket (LOW payoff, LONG cycle).**
    File support ticket with Orion describing the timeout pattern (4 attempts,
    300-900s, GET /Verbose responsive). Reference ticket ID in INFSHIP.A2
    closeout. Vendor cycle is multi-week; track but don't block on this.

    Recommended sequence: Track 1 first (1-2 hour HAR recapture + parse). If
    Track 1 yields async endpoint, ship that. If not, Track 2 with small
    batch probe. Track 3 fires in parallel with Track 2.
  </spec_summary>

  <acceptance_criteria>
    <ac>1. Final disposition of the Orion API Asset-grouping path:
        EITHER (a) working direct-pull script that produces Inflection-only
        assets dim within 10min wall-clock, OR (b) documented vendor-blocked
        verdict with ticket ID + reproduction steps + recommended Path C
        long-term posture.</ac>
    <ac>2. INFLEC_API_ENDPOINTS_CATALOG.md updated with the investigation
        findings (timeout pattern, async endpoint discovery if any, batch
        size limits if Track 2 succeeds, vendor ticket reference).</ac>
    <ac>3. If a working pull path is found: silver layer
        build_assets_dim.py refactored to consume the new bronze CSV
        instead of canonical (or both with a feature flag for AUA
        comparison).</ac>
    <ac>4. If vendor-blocked: Path C remains the long-term posture; no
        further work required until vendor ticket resolves. Path C
        documented as the ratified architecture in catalog + PRD.</ac>
    <ac>5. RAVC4 to CTO with verdict + commit refs + catalog updates.</ac>
  </acceptance_criteria>

  <gates_and_dependencies>
    <gates>None — runs anytime AE 0.6.1~B has bandwidth between primary
        ORIAPI infra work (autonomous JWT pipeline + dispatch primitives).</gates>
    <unblocks>Long-term assets dim source-of-truth upgrade. Does NOT
        unblock any v1 INFSHIP Phase 2 work — Path C is functional for
        DE B5/B6 ship.</unblocks>
  </gates_and_dependencies>

  <coordination>
    CC DS~D (0.4.0_DS_ClientPlatform~D) on RAVC4 — they hold full context
    on the pull script, timeout patterns, and Path C trade-off. They are
    NOT a co-owner; this TO is fully AE-side. DS~D consultation only on
    request.

    HAR captures should land in user's Downloads/ as before; AE re-runs
    .tools/har-scan.py to extract endpoint signatures. User may need to
    initiate the manual UI export themselves (24h+ Asset grouping pull is
    a substantial UI action).
  </coordination>

  <ravc_target>
    <to>1.0.0_SA_CTO</to>
    <on_complete>RAVC4 with verdict (working path / vendor-blocked) +
        evidence (probe results, batch size data, vendor ticket ref) +
        catalog + PRD updates.</on_complete>
  </ravc_target>

  <estimated_effort>
    Track 1 alone: 2-4 hours (HAR recapture + parse + probe scripting).
    Track 2 alone: 4-8 hours (batch sizing + parallel pool + integration).
    Track 3: 30 min to file ticket + N weeks for vendor.
    Full investigation cycle: 1-2 sessions for AE.
  </estimated_effort>
</task_order>
