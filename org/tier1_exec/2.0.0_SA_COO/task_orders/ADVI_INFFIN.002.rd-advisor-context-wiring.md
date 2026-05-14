<task_order>
  <metadata>
    <id>ADVI_INFFIN.002</id>
    <slug>rd-advisor-context-wiring</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-13</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — bundles 2 visible-state defects (drill non-functional + L3 entry-path regression); investigates whether DS~A directory artifact (.004) is required or FE-iteration suffices</priority>
    <sla>~2-3h wall; ships standalone; routes to .004 (DS~A directory) if HH→advisor lookup requires backend emit</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inflection-finalize-20260513.md (DE 0.4 INFFIN brief, commit e7965874b)</ref>
    <ref type="project_json">org/projects/ADVI_INFFIN.json</ref>
    <ref type="authority">Andrew direct evening walkthrough 2026-05-13</ref>
    <ref type="cross_link">Sibling: .001 RD UI parity batch (parallel, lands canonical NNA chart primitive that Surface #3 inherits) + .003 DS~C INF emit (parallel) + .004 DS~A directory artifact (potential contingent dep — RD investigates first) + .005 DS~B 49F audit + .006 RD Phase 2 + .007 AE 0.6.1 Phase 2</ref>
    <ref type="adjacent_ship">DS~C 0997324d6 (per-advisor relationship_since shipped earlier — Surface #3 New Clients tile data already available)</ref>
  </references>

  <context>
    Two surfaces share lane (RD 0.4.2 FE wiring) and both involve resolving advisor context. Surface #4 has a backend-side option (.004 DS~A directory artifact) that RD investigates first before requiring; FE-side iteration of 4 advisor `book.json` files is the cheap alternative.

    **Surface #3 — Continuous-ADV-NNA L1 drill not filtering by selected advisor + New Clients tile stuck at `--`.** Page: AdvisorIntelligence → Distribution → Segment Analytics. View: Continuous/ADV/NNA/Quarter/1Y, Peter Lee selected in left rail.

    Symptom A: right-side bar+line chart still shows firm-aggregate ($31.1M inflows / -$19M outflows / +$12M net); header still reads "1Y WINDOW NNA BY ADVISOR" (firm label). Advisor selection in left rail does not filter the chart.

    Symptom B: "New Clients" tile shows `--` regardless of advisor selection or window.

    Andrew quote: "I should be seeing his specific NNA via L1 drill, which we've already accounted for in his AdvisorPublicProfile so the information is already ready, need that set up here."

    Expected: Click Peter Lee → chart re-renders with his per-period inflows/outflows/net + line, matching values rendered on his AdvisorPublicProfile. Header chip flips to "1Y WINDOW NNA — PETER LEE". Click "All Advisors" → reverts to firm aggregate. New Clients tile shows actual integer count for selected window × cohort × L0/L1 state.

    Per-advisor `clients[].relationship_since` already shipped (DS~C `0997324d6`); data should be available client-side.

    **Surface #4 — L3 ClientDetailPage missing advisor context + HH display_name when entered via BI deeplink.**

    Comparison:
    - **BI deeplink path:** title shows raw HH ID "338"; breadcrumb `All Advisors > Advisor > 338` with placeholder "Advisor" (no advisor name)
    - **From Peter's Book path:** title shows "NOEL SODERBLOM" (HH display_name); full advisor chrome (Peter Lee header + `View: Profile / Book` toggle + `"Back to Book"` button)

    Andrew quote: "We should always see the advisor whose client this is, regardless of how you get to this page."

    Expected: Identical L3 chrome regardless of entry path. Advisor name resolved + Profile/Book toggle + Back-to-Book + HH display_name as section title.

    Data dependency: HH → advisor reverse lookup. Two viable approaches:
    - **FE-side:** iterate 4 advisor `book.json` files on L3 mount to build reverse index (cheap — 4 advisors only)
    - **DS-side (.004 DS~A):** emit `s3://opal-data-inf/platinum/firm/client_directory.json` (hh_id → {advisor_id, advisor_name, display_name}) for O(1) lookup

    RD picks path at implementation time. If FE-iteration suffices, .004 DS~A directory artifact deliverable still ships as standalone deliverable but RD doesn't gate on it.
  </context>

  <objective>
    Wire advisor selection through Continuous-ADV-NNA L1 chart + New Clients tile (Surface #3); unify L3 ClientDetailPage chrome across both entry paths (Surface #4) with HH → advisor reverse lookup.

    Surface #4: investigate FE-iteration approach first (cheap, no backend dep); if shape mismatch or perf concern, switch to consuming .004 DS~A directory artifact when available.

    Surfaces #3 NNA chart inherits canonical `<NnaBarLineChart>` primitive from .001 (cross-link).
  </objective>

  <scope>
    <surfaces>
      <surface id="3">Continuous-ADV-NNA L1 advisor selection wiring + New Clients tile fix</surface>
      <surface id="4">L3 ClientDetailPage unified chrome via BI deeplink (HH → advisor reverse lookup)</surface>
    </surfaces>
    <files>
      <file action="investigate">portal/src/pages/AdvisorIntelligence/_partners/inflection/AdvisorPublicProfile.tsx (or similar) — locate NNA inflows/outflows/net field path; verify field shape matches DistributionTab accessor</file>
      <file action="investigate">portal/src/pages/AdvisorIntelligence/_shared/components/DistributionTab/ContinuousView/ (or similar) — confirm advisor-id parameterized accessor exists or needs wiring</file>
      <file action="modify">DistributionTab Continuous-ADV-NNA chart accessor — advisor-scoped data filtering</file>
      <file action="modify">DistributionTab New Clients tile — integer count from per-advisor `clients[].relationship_since` already in book.json</file>
      <file action="investigate">portal/src/pages/AdvisorIntelligence/L3/ClientDetailPage.tsx (or similar) — current chrome differential between BI deeplink vs From Peter's Book path</file>
      <file action="modify">L3 ClientDetailPage mount — unified chrome resolution + HH → advisor reverse lookup</file>
      <file action="conditional">If FE-iteration approach: build reverse index from 4 advisor book.json files on L3 mount (cheap)</file>
      <file action="conditional">If .004 DS~A directory artifact approach: consume `s3://opal-data-inf/platinum/firm/client_directory.json` for O(1) lookup</file>
    </files>
  </scope>

  <phase id="1" when="investigation">
    <step>
      <description>Surface #3 step 1: `comp-transform fields AdvisorPublicProfile` to locate NNA inflows/outflows/net field path. Verify the data is on per-advisor book.json shape currently consumed by AdvisorPublicProfile.</description>
      <expect>Field path identified; shape matches expected NNA chart accessor.</expect>
    </step>
    <step>
      <description>Surface #3 step 2: `comp-transform schema-check DistributionTab` to confirm advisor-id parameterized accessor exists. If exists → pure FE rebind. If not → adapter needed.</description>
      <expect>Either accessor exists (rebind) OR adapter needed (small FE work).</expect>
      <if_mismatch>If AdvisorPublicProfile NNA series field shape DIFFERS from DistributionTab's expected accessor shape, this routes to .003 DS~C contingent (normalized emit needed). Surface to COO before re-routing.</if_mismatch>
    </step>
    <step>
      <description>Surface #4: empirical check — does `s3://opal-data-inf/platinum/advisors/{id}/timeseries.json` or `book.json` contain HH → advisor mapping accessible from L3 mount? Check 4 advisor book.json files for clients[] array structure.</description>
      <expect>Either (a) FE-iteration of 4 book.json files yields the lookup table at L3 mount (cheap; ~4 fetches OR cache-once on app boot), OR (b) requires DS~A directory artifact (.004) for O(1) lookup at platinum/firm/client_directory.json.</expect>
      <if_mismatch>If 4-advisor-iteration latency is unacceptable (e.g., L3 mount blocking), switch to consuming .004 DS~A directory artifact. .004 ships in parallel; RD consumes when available.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <description>Surface #3 chart: wire advisor selection through Continuous-ADV-NNA L1 chart accessor. Click Peter Lee → chart re-renders with his per-period inflows/outflows/net + line + header chip flips to "1Y WINDOW NNA — PETER LEE". Click "All Advisors" → reverts to firm aggregate. Use canonical `<NnaBarLineChart>` primitive from .001 (consume when .001 ships).</description>
      <expect>All 4 advisors filter the chart; "All Advisors" reverts to firm aggregate.</expect>
    </step>
    <step>
      <description>Surface #3 tile: wire New Clients tile to integer count from per-advisor `clients[].relationship_since` (already shipped DS~C 0997324d6). Firm-wide at L0, advisor-scoped at L1, scoped to selected window. Apply null-elimination rule: never `--`, always integer (zero if no new clients in window).</description>
      <expect>Integer count for any selected window × cohort × L0/L1 state.</expect>
    </step>
    <step>
      <description>Surface #3 sanity: at L0 (no advisor selected), New Clients tile sums across all advisors. Confirm at acceptance (DE brief open question #5 flag).</description>
      <expect>L0 sum across all 4 advisors.</expect>
    </step>
    <step>
      <description>Surface #4: unify L3 ClientDetailPage chrome regardless of entry path. Mount-time HH → advisor lookup (via FE-iteration of 4 book.json files OR .004 directory artifact, whichever investigation surfaced). Resolve advisor name + HH display_name; render full chrome (advisor header + Profile/Book toggle + Back-to-Book + display_name as section title).</description>
      <expect>Both entry paths render identical L3 chrome; HH-page title is always pseudonymized display_name (never raw hh_id); advisor resolves correctly for all 4 Inflection advisors.</expect>
    </step>
  </phase>

  <phase id="3" when="audit">
    <step>
      <description>Surface #3 NNA chart canonical-design audit: ensure DistributionTab Continuous-NNA chart consumes the canonical `<NnaBarLineChart>` + `<ChartTooltip>` primitives from .001 (cross-link). If .001 ships first → straightforward consumption. If .002 ships first → either wire local NNA chart for now (placeholder) and migrate post .001 OR coordinate ship order via COO.</description>
      <expect>Surface #3 chart uses canonical primitive on final ship.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1 (Surface #3 chart): Click Peter Lee → bars/line redraw with his series; header chip flips to "1Y WINDOW NNA — PETER LEE"; all 4 advisors work the same way. Deselect or "All Advisors" → reverts to firm aggregate.
    AC2 (Surface #3 tile): New Clients tile shows integer count for any selected window × cohort × L0/L1 state. No `--` em-dashes (null-elimination rule).
    AC3 (Surface #3 L0 sanity): New Clients tile at L0 (no advisor selected) sums across all advisors correctly.
    AC4 (Surface #4 unified chrome): Both entry paths (BI deeplink + From Peter's Book) render identical L3 chrome — advisor header + Profile/Book toggle + Back-to-Book + display_name title.
    AC5 (Surface #4 lookup): HH → advisor reverse lookup works for all 4 Inflection advisors; no raw hh_id ever rendered in title slot; no "Advisor" placeholder in breadcrumb.
    AC6 (Surface #4 routing decision): documented in session log — FE-iteration OR .004 directory artifact consumed. If contingent dep, .004 ship signal is the unblock.
    AC7: Surface #3 NNA chart uses canonical primitive (consumed from .001 when shipped).
    AC8: tsc 0 errors on portal build.
    AC9: bun run dev smoke against L0/L1 drill flow + L3 entry paths (BI deeplink + From Peter's Book).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>comp-transform fields AdvisorPublicProfile (locate NNA field path); comp-transform schema-check DistributionTab (advisor-id accessor); component-tree walk for L3 entry path differential</phase_1>
    <phase_2>tsc + bun run dev smoke; per-surface visual verify; both L3 entry paths visited in dev environment</phase_2>
    <phase_3>cross-link with .001 canonical NNA chart consumption verify</phase_3>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    POTENTIAL DS DEPS:
    - .004 DS~A directory artifact (HH → advisor reverse lookup): RD investigates FE-iteration first; routes to .004 if needed. Empirically validated routing decision documented in AC6.
    - .003 DS~C INF emit (advisor-scoped NNA shape): RD investigates AdvisorPublicProfile field path first; routes to .003 if shape mismatch. Empirical decision in Phase 1 step 2.

    PARALLEL ACTIVITY:
    - .001 RD UI parity batch (canonical NNA chart primitive; Surface #3 chart consumes when .001 ships; coordinate ship order if needed)
    - .003/.004/.005 DS lanes (parallel; no FE-side conflict)

    PORTAL SUBMODULE: DT 0.4 owns portal submodule push.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Pure frontend wiring. No data emit changes. No Lambda redeploys. No chain re-fires.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. Surface #3: advisor-id-scoped NNA chart accessor + canonical primitive consumption + New Clients tile integer count + L0 sum
    2. Surface #4: unified L3 chrome + HH → advisor reverse lookup (FE-iteration OR .004 artifact)
    3. Session log documenting Phase 1 routing decisions (FE-iteration vs DS~A consumption) per AC6
    4. Single or multiple commits under 0.4.2_RD_AdvisorIntelligence author per RD discipline
    5. tsc 0 errors + visual diff smoke on dev
    6. MCP RAVC2 to COO post-AC1-9 PASS with per-surface evidence
  </deliverables>

  <ravc>
    RD 0.4.2 RAVC2 to COO post-AC1-9 PASS. If routing decision in Phase 1 routes Surface #4 to .004 DS~A directory artifact, dispatch_held inherits on Surface #4 portion until .004 ships. Surface #3 ships standalone in either case. COO ratifies + relays acceptance to Andrew.
  </ravc>

  <notes>
    **Per DE brief recommendations:** this TO bundles Surface #3 + #4 because both are advisor-context-resolution problems sharing FE wiring + lifecycle. The investigative routing (whether .004 directory is needed) is part of this TO's Phase 1 scope.

    **Cross-link with .001:** Surface #3 NNA chart consumes the canonical primitive landed in .001. If .002 starts before .001 ships, RD can land Surface #3 chart with a local placeholder and migrate to canonical primitive post-.001 — or coordinate ship order via COO. Default: .001 ships first.

    **Open question #2 (HH→advisor directory path):** RD-B routing decision empirically. If .004 needed, surface to COO + I'll relay to DS~A. .004 ships in parallel either way.

    **Author identity:** `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"` per agent commit identity protocol.
  </notes>
</task_order>
