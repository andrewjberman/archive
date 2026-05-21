<task_order>
  <metadata>
    <id>YALP_MDSRC.A2</id>
    <slug>ds-ycharts-per-requirement-endpoint-spec</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-05-20</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO NOW — Andrew-direct, immediate (verbatim: "i want to know what the endpoints are for each of our requirements, immediately"). No gate. Start on receipt.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 urgent — Andrew-direct immediate. The definitive YCharts endpoint-per-requirement spec; it becomes the build spec for TO-C2.</priority>
    <sla>Fast — largely synthesis of the overnight recon already gathered + targeted gap-fill probes. Deliver the spec as soon as it is complete; interim partials welcome.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.3 §5.2 (the 32-surface migration decision matrix — the requirement list this TO maps).</prd>
    <recon>docs/briefs/mdsrc-ycharts-master-reconnaissance-20260520.md (1fd7650f4) — the 26-endpoint capability catalog + portal coverage map (your overnight recon — the input to sharpen).</recon>
    <ticker_map>docs/briefs/mdsrc-ycharts-ticker-map-and-fidelity-20260520.{md,csv} (dc01d4b8a) — the 71-row crosswalk + fidelity.</ticker_map>
  </references>

  <context>
    Andrew-direct, 2026-05-20: he wants the exact YCharts endpoint for EACH portal data requirement — definitively, immediately. The overnight recon catalogued 26 endpoint classes and a portal coverage map at the data-class level; this TO sharpens that to a per-requirement, per-surface specification: for every requirement, THE endpoint that serves it, with method + params + response field. This is the concrete answer to "how does each surface get sourced" and becomes the build spec for TO-C2 (the YCharts market-data pull).
  </context>

  <scope>
    <in_scope>
      - For EVERY portal data requirement in the PRD v0.3 §5.2 migration matrix (all 32 surfaces — prioritize the 17 YCharts-touched: the 7 YCharts-replaceable + the YCharts-input legs of the 10 hybrid; but cover every surface so the spec is complete, marking the proprietary / SmartX / FRED ones explicitly as not-YCharts with the one-line reason), specify the EXACT YCharts endpoint(s) that satisfy it:
        * surface ID + the requirement (what data the surface needs)
        * YCharts endpoint: HTTP method + full path + the query/POST params (incl. the symbol/ticker param resolved via the dc01d4b8a crosswalk)
        * the response field(s) that carry the required data
        * status: VERIFIED (you pulled it live and confirmed the field) vs UNVERIFIED (recon-inferred, needs a confirm probe)
      - Where the overnight recon already nailed the endpoint, cite it. Where there is a gap, run a targeted confirm probe (you hold the seat / are the capture hub) to fill it — do NOT leave a requirement UNVERIFIED if a quick probe can settle it.
      - Flag any requirement with NO viable YCharts endpoint (a genuine coverage gap) explicitly — that is a material finding.

      FOCAL POINT (Andrew-direct, 2026-05-20) — THE 27 IMPERFECT CASES + the alternatives hunt:
      The overnight recon found ~44/53 tickers fidelity-matched and a residue of imperfect cases — the ~9 wide-variance + ~18 unmapped. Andrew wants this residue fully resolved on the page, not summarized:
      - Enumerate EVERY one of the imperfect cases INDIVIDUALLY — for each: the surface ID + portal entity, its `bbg_ticker` (from data_pkl), the current YCharts mapping IF ANY (the ^-symbol tried), and the EXACT variance (portal_1Y vs ycharts_1Y, the numeric gap). No "9 wide cases" as a count — the actual 9, named, with numbers; the actual 18 unmapped, named, with the reason each is unmapped.
      - ALTERNATIVES HUNT — make this a focal part of the audit, not an afterthought: for each imperfect/unmapped case, SEARCH the full available YCharts endpoint surface (the indexFamily lists, the index/security namespaces, the 26 endpoint classes) for a NEAR-MATCH or ALTERNATIVE — a different YCharts symbol, index variant, or endpoint — that is a CLOSER fidelity match to the portal's Bloomberg series than the current attempt. Report the candidate alternative(s) per case + their measured variance vs the portal series. The goal is: for each imperfect case, either a better alternative is found (with evidence) or it is documented that none exists in the available YCharts surface.
      - The output is a per-case table: case / bbg_ticker / current-YCharts-attempt + variance / candidate-alternative(s) + variance / verdict (resolved-by-alternative | best-available-still-wide | genuinely-unmapped).
    </in_scope>
    <out_of_scope>
      - Building the pull — that is TO-C2; A2 is the spec C2 builds against.
      - The official-API-vs-scrape decision (Q1) — spec the endpoints on the path the recon used (the web-app endpoints); note where the official API would differ if known, but do not block on Q1.
      - SmartX / FRED / proprietary surfaces — list them with the not-YCharts reason; no endpoint mapping needed for those.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before">
      <step>
        <run>(none) — YCharts is an external system, not in the comp-graph; the spec is synthesis of the live recon + targeted probes.</run>
        <expect>Documented-none per PRD §10. Evidence base is the recon briefs + live confirm probes.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit"><step><run>(none) — spec doc, no code.</run><expect>No code gate applies.</expect><if_mismatch>N/A.</if_mismatch></step></phase>
    <phase id="3" when="after commit"><step><run>(none) — the spec's VERIFIED/UNVERIFIED column is its self-validation.</run><expect>Checked by AC2.</expect><if_mismatch>N/A.</if_mismatch></step></phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    The A2 spec becomes the TO-C2 build spec (0.1.0_DS + 0.2.0_DS). Hand the WS-2-domain rows to 0.2.0_DS as you finalize. If a confirm probe needs the live YCharts seat, you are the capture hub — no contention. No shared files.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Every PRD §5.2 requirement has a row: surface ID, requirement, YCharts endpoint (method + path + params + response field) OR an explicit not-YCharts marker (SmartX / FRED / proprietary) with reason.</ac>
    <ac id="AC2">Each YCharts-endpoint row carries a VERIFIED / UNVERIFIED status; UNVERIFIED rows are minimized by targeted confirm probes — any remaining UNVERIFIED row states why a probe could not settle it.</ac>
    <ac id="AC3">Any genuine coverage gap (a requirement with no viable YCharts endpoint) is explicitly flagged.</ac>
    <ac id="AC5">EVERY imperfect case (the ~9 wide-variance + ~18 unmapped) enumerated individually in a per-case table: case / portal entity / bbg_ticker / current-YCharts-attempt + measured variance (portal_1Y vs ycharts_1Y) / reason-unmapped where applicable. No aggregate counts standing in for the named cases.</ac>
    <ac id="AC6">Alternatives hunt completed for every imperfect case: the available YCharts endpoint surface searched for a near-match / alternative symbol or endpoint; candidate alternative(s) reported per case with their measured variance; each case carries a verdict — resolved-by-alternative (with evidence) | best-available-still-wide | genuinely-unmapped.</ac>
    <ac id="AC4">Deliverable is a committed spec (e.g. docs/briefs/mdsrc-ycharts-endpoint-spec-20260520.md, machine-readable table form) pushed + push-confirmed on origin/CLOUD. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO. Interim partials may be surfaced as they complete — Andrew wants this fast.</ac>
  </acceptance_criteria>

  <deliverables>
    - The definitive per-requirement YCharts endpoint specification (committed, push-confirmed).
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT block on Q1 — spec the endpoints on the recon's path; note official-API deltas where known.</rule>
    <rule>Do NOT leave a requirement UNVERIFIED if a quick live probe can confirm it — you hold the seat.</rule>
    <rule>Do NOT build the pull — that is TO-C2; A2 is the spec.</rule>
    <rule>No emojis in the spec, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
