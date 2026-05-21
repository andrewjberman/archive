<task_order>
  <metadata>
    <id>YALP_MDSRC.A3</id>
    <slug>ds-ycharts-internal-api-reverse-engineering</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO NOW — Andrew-direct, 2026-05-20. Andrew ruled Q1: integrate YCharts by reverse-engineering the internal API that feeds its web app, and go DEEPER than A2's page-level spec. Andrew framing — this is NOT "scraping": it is integrating against the provider's own backend API, and it is the TEMPLATE approach for ALL third-party data sources. No gate. Start on receipt. 0.1.0_DS is idle and holds the YCharts capture seat — this is its real work.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 urgent — Andrew-direct. This is the definitive YCharts access mechanism. It upgrades the A2 page-level endpoint spec to the actual backend JSON API and becomes the real build spec for TO-C1 (credential/session pipeline) + TO-C2 (market-data pull).</priority>
    <sla>Substantial structured reverse-engineering — comparable to a WS-domain audit (~2-4 effort-days). Deep, empirical, complete. Interim partials welcome — Andrew wants depth, not speed.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.3.2 §5.2 (the 32-surface migration matrix — the requirement list this TO re-maps onto the internal API).</prd>
    <a2_spec>docs/briefs/mdsrc-ycharts-endpoint-spec-20260520.md — the A2 per-requirement endpoint spec (page-level). A3 UPGRADES this: A2 mapped requirements to YCharts surfaces; A3 maps them to the actual internal JSON API calls behind those surfaces.</a2_spec>
    <recon>docs/briefs/mdsrc-ycharts-master-reconnaissance-20260520.md — the 26-endpoint capability catalog.</recon>
    <ops_pattern>docs/briefs/mdsrc-ws4-ycharts-operational-pattern-20260520.md — the WS-4 YCharts operational-access pattern audit.</ops_pattern>
    <ticker_map>docs/briefs/mdsrc-ycharts-ticker-map-and-fidelity-20260520.{md,csv} — the 71-row crosswalk + fidelity; the 27 imperfect cases to re-test against the internal API.</ticker_map>
    <a1_sibling>YALP_MDSRC.A1 (0.7.0_AE_CloudOps, in flight) — the headless-capture viability probe (does the AWS WAF JS-challenge clear headless). A1 = can a bot get IN; A3 = once in, WHAT API does the app call. Complementary — coordinate, do not duplicate.</a1_sibling>
  </references>

  <context>
    Andrew-direct, 2026-05-20, verbatim intent: "We can definitely scrape them, we just need to go deeper. We need to study their endpoints and how their endpoints actually feed the web app. Obviously what is feeding the web app is an API to their database, so we should be able to get very high-fidelity robust data by reverse-engineering their endpoints. That is what 0.1.0_DS should be doing."

    This RULES Q1 (official paid Data API vs. self-integration): self-integrate, by reverse-engineering the YCharts web app's INTERNAL JSON API — the XHR/fetch calls the single-page app issues to the YCharts backend. That backend is an API to their database; calling it directly yields structured, high-fidelity JSON. Andrew's framing, 2026-05-20: this is explicitly NOT "scraping" — it is integrating against the provider's OWN backend API, the same contract their web app uses, and it is the CANONICAL TEMPLATE approach for ALL third-party data sources (not a YCharts one-off). A2 catalogued the YCharts surfaces and a page-level endpoint spec; A3 goes one layer down to the actual request/response contract of the backend API so TO-C1/C2 can be built against a concrete, empirically-verified API — not a parse of the rendered DOM.
  </context>

  <scope>
    <in_scope>
      PHASE 1 — Internal-API discovery (capture every backend call the web app makes).
      Drive the YCharts web app with browser devtools (Network tab, XHR/fetch filter) or a capture proxy; for EACH distinct surface type the portal needs — security/equity quote page, index page, fund/ETF page, fundamentals, historical time-series / chart data, indicator/economic series, screener/comparison views — load the page and capture EVERY XHR/fetch request the app issues to the YCharts backend. For each captured internal endpoint document:
        * full URL pattern (host + path, with the path params templated, e.g. /api/v3/securities/{symbol}/timeseries)
        * HTTP method + the query params and/or JSON request body, with each param's meaning and allowed values
        * required request headers — especially the auth surface: which cookies are sent (ycsessionid + others), any CSRF / X-CSRF-Token / X-Requested-With header, Referer/Origin requirements, any bearer or app token
        * the response: content-type, JSON schema (the structure + the field carrying each datum), pagination/range semantics
      Deliver a structured internal-API endpoint reference — one row per endpoint.

      PHASE 2 — Auth / session model.
      Characterize precisely how the internal API authenticates an XHR call: the cookie set that must be present (and which of A1's measured ycsessionid TTL governs it), how a CSRF token is sourced (a meta tag in the initial HTML? a cookie? a bootstrap call?) and whether it must be echoed in headers/body, session lifetime under real use, and any observed rate-limit / throttle behavior (429s, headers, request budgets). This Phase is the build spec for TO-C1 (the credential/session pipeline) — it must answer: what does an automated client need to hold and refresh to keep making valid internal-API calls.

      PHASE 3 — Requirement -> internal-API mapping (upgrades A2).
      For EVERY portal data requirement in PRD v0.3.2 §5.2 that A2 marked YCharts-served, specify the internal API call that satisfies it: the endpoint + exact params (symbol resolved via the crosswalk) + the JSON path to the required value. Where A2's page-level mapping and the internal API diverge, the internal API is canonical — note the delta. The output is the per-requirement internal-API build spec C2 builds against.

      PHASE 4 — Re-test the 27 imperfect cases against the internal API (FOCAL).
      Andrew's hypothesis: the backend DB API exposes richer, cleaner data than the page-level mapping found. Take the 27 imperfect cases from the A2 fidelity work (9 wide-variance + 18 unmapped) and re-test each against the internal API — does a backend endpoint expose a series, symbol variant, or raw field that resolves the variance or the unmapped gap that the surface-level mapping could not? Per case: the internal endpoint tried, the result, and an updated verdict (resolved-via-internal-API | still-wide | genuinely-unmapped). This is the empirical test of whether "going deeper" closes the residue.
    </in_scope>
    <out_of_scope>
      - Building the pull / the credential pipeline — that is TO-C2 / TO-C1; A3 is the empirically-verified spec they build against.
      - The headless-vs-attended capture-mechanism verdict — that is A1 (AE 0.7.0). A3 documents the API contract regardless of how the session is obtained; coordinate with A1 on the session-acquisition side, do not re-run it.
      - SmartX / FRED / proprietary surfaces — already mapped by S1 / F1; not YCharts, not this TO.
      - Any portal / Terraform / pipeline code change — A3 is reverse-engineering + spec only.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before">
      <step>
        <run>(none) — YCharts is an external system, not in the comp-graph; the spec is empirical capture + targeted probes.</run>
        <expect>Documented-none per PRD §10. Evidence base is live devtools/proxy capture against the YCharts web app + the prior recon briefs.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit"><step><run>(none) — spec + reference docs, no code authored.</run><expect>No code gate applies.</expect><if_mismatch>N/A.</if_mismatch></step></phase>
    <phase id="3" when="after commit"><step><run>(none) — the VERIFIED-against-live-capture column is the deliverable's self-validation.</run><expect>Checked by AC.</expect><if_mismatch>N/A.</if_mismatch></step></phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    A1 (0.7.0_AE_CloudOps) is the session-acquisition sibling — its headless-WAF verdict + ycsessionid Set-Cookie Max-Age measurement feed A3 Phase 2 (the session model). MCP-coordinate: take A1's TTL number rather than re-measuring it. 0.1.0_DS holds the YCharts capture seat — no contention. The A3 deliverable becomes the build spec for TO-C1 (0.7.0_AE / credential pipeline) and TO-C2 (0.1.0_DS + 0.2.0_DS / market-data pull) — hand the WS-2-domain rows to 0.2.0_DS as they finalize. RAVC2 to COO + CC CTO feeds the PRD v0.4 amendment. No shared files written (reverse-engineering + spec only).
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase 1: a structured internal-API endpoint reference — every backend XHR/fetch endpoint the YCharts web app calls for the in-scope surface types, each with URL pattern + method + params + required headers (incl. the auth surface) + response JSON schema, all captured live.</ac>
    <ac id="AC2">Phase 2: the auth/session model documented definitively — the cookie set, CSRF-token sourcing + echo requirement, session lifetime, observed rate limits. This explicitly states what an automated client must hold + refresh (the TO-C1 build spec).</ac>
    <ac id="AC3">Phase 3: every PRD v0.3.2 §5.2 YCharts-served requirement mapped to its internal API call — endpoint + params + JSON path to the value; deltas vs the A2 page-level spec noted, internal API canonical. Machine-readable table.</ac>
    <ac id="AC4">Phase 4: all 27 imperfect cases (9 wide-variance + 18 unmapped) re-tested against the internal API, each with the endpoint tried, the result, and an updated verdict (resolved-via-internal-API | still-wide | genuinely-unmapped).</ac>
    <ac id="AC5">Deliverable: a committed YCharts internal-API reverse-engineering brief + the requirement->internal-API mapping table (e.g. docs/briefs/mdsrc-ycharts-internal-api-20260520.md + a machine-readable table), pushed + push-confirmed on origin/CLOUD. Session log. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO. Interim partials welcome.</ac>
  </acceptance_criteria>

  <deliverables>
    - The YCharts internal-API endpoint reference (Phase 1) + auth/session model (Phase 2).
    - The per-requirement internal-API build spec (Phase 3) + the 27-imperfect-case re-test (Phase 4).
    - A committed brief + machine-readable mapping table, push-confirmed on origin/CLOUD.
    - Session log. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT parse rendered HTML / the DOM — the explicit Andrew directive is to integrate against the internal JSON API behind the web app, not "scrape" a page. DOM parsing is the fallback of last resort, only for a datum genuinely served no other way, and must be flagged as such.</rule>
    <rule>Frame the deliverable as an INTEGRATION spec, not a "scraping" guide — Andrew directive 2026-05-20: "we do not scrape." This is integration against the provider's own backend API; the brief's language must reflect that.</rule>
    <rule>Do NOT build the pull or the credential pipeline — A3 is the empirical spec; TO-C1/C2 build against it.</rule>
    <rule>Do NOT re-run A1's headless-capture viability probe — consume its result; A3 owns the API contract, A1 owns session acquisition.</rule>
    <rule>Do NOT expose YCharts credentials / cookie values in chat / MCP / git / logs / the brief — document the auth MECHANISM (which cookie, which header) without the secret values.</rule>
    <rule>No emojis in the brief, the mapping table, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
