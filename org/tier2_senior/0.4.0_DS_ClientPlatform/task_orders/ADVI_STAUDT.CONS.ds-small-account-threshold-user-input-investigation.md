<task_order>
  <metadata>
    <id>ADVI_STAUDT.CONS</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-20</date>
    <status>dispatched</status><!-- DISPATCHED 20260420T19:XX Z by 2.0.0_SA_COO. Andrew directive 2026-04-20 in chat. ~C lane (KPI in parallel; both P2/P3, no overlap with ~A engine wave). -->
    <project_code>ADVI_STAUDT</project_code>
    <priority>P2 — feature-investigation TO. Output is a scoping/architecture briefing, not code. Independent of FIX wave + engine wave; no qa-runner dependency.</priority>
    <lane>~C — alongside KPI TO. Both are framework/architecture work, no overlap with ~A engine wave or ~B EOP2025 diagnostic.</lane>
    <bug_reference>Andrew chat 2026-04-20: "explore how we can make the small account threshold a user input in the Consolidation Opportunities toggle in Revenue Operations & Analysis panel in /Books tab in ADVI." Current state: threshold is hard-coded at $40k per ADVI_ROLLUP.B9 (commit f2ec98d1 "C_08 small_account_count per advisor (threshold $40k)"). User wants to drag/slide the threshold from the portal UI and have the count + avg AUA + downstream visualizations update.</bug_reference>
    <decision_authority>Andrew directive 2026-04-20 in chat. Investigation-only authorization; implementation TO follows after briefing review.</decision_authority>
  </metadata>

  <references>
    <ref type="originating-feature">ADVI_ROLLUP.B9 commit f2ec98d1 — "C_08 small_account_count per advisor (threshold $40k)"</ref>
    <ref type="follow-on-feature">ADVI_ROLLUP.B10 commit bb426933 — "C_08 small_account_avg_aua at (advisor, role) grain + advisor grain"</ref>
    <ref type="portal-context">/Books tab → "Revenue Operations & Analysis" panel → "Consolidation Opportunities" toggle (frontend component name TBD via Phase 0 portal-side audit)</ref>
    <ref type="parent-project">project_bd_is_ground_truth.md (BD silver/allocations is authoritative for active accounts; threshold computations should respect the BD active-account universe)</ref>
  </references>

  <objective>
    Investigate how to make the small_account threshold (currently hard-coded at $40k per ADVI_ROLLUP.B9) a user input in the Consolidation Opportunities toggle within /Books → Revenue Operations & Analysis. Produce an architecture briefing covering: current state (where the $40k constant lives + propagation chain), three implementation architecture options (server-precompute-multiple-buckets vs server-compute-on-demand vs client-side-compute), trade-offs (latency, server cost, PII exposure, cache implications, UX), recommended path, and a follow-on implementation TO sketch. NO code changes in this TO — investigation only.
  </objective>

  <scope>
    **Current state to map:**

    1. **Where the $40k constant lives:** Per ADVI_ROLLUP.B9 (f2ec98d1), C_08.advisor_fee_efficiency.py implements the small-account count + avg AUA computation. Identify exact file:line for the $40k constant + every computation that depends on it.

    2. **What gets computed using the threshold:**
       - `small_account_count` per advisor (from B9)
       - `small_account_avg_aua` at (advisor, role) grain + advisor grain (from B10)
       - Any other downstream fields (e.g., consolidation_opportunity_dollars, count_below_threshold, etc.)

    3. **Propagation chain:**
       - C_08 writes `gold/artifacts/advisor_fee_efficiency.json` (per comp-pipescript io C_08)
       - D_04 reads advisor_fee_efficiency.json and writes platinum aggregations
       - Portal frontend reads platinum (or maybe direct gold artifact) for /Books → Revenue Operations & Analysis → Consolidation Opportunities

    4. **Portal-side wiring:**
       - Identify React component name for the "Consolidation Opportunities" toggle (use comp-routes + comp-transform schema-check)
       - Identify the React Query key + endpoint serving the data
       - Identify any current toggle/filter UI patterns in the same panel (precedent for adding a slider)

    **Three architecture options to evaluate:**

    **Option A — Server precompute multiple threshold buckets.**
    - C_08 (or new C-script) computes small_account_count + avg_aua at predefined buckets: $10k / $25k / $40k / $75k / $100k / $250k
    - Portal toggle/dropdown selects between buckets, no per-request compute
    - **Pros:** instant client UX, no latency added, server cost is a one-time precompute increase, cache-friendly (each bucket has a stable key)
    - **Cons:** discrete bucket choices (no slider), schema changes to gold/artifact for each bucket, potential balloon if buckets multiply

    **Option B — Server compute on-demand per request.**
    - Portal sends threshold value as query param to a Lambda/API endpoint; server computes count + avg_aua against silver/canonical data on-the-fly
    - **Pros:** continuous slider possible (any threshold), no schema growth
    - **Cons:** request latency added (per-request compute), needs Lambda or new API endpoint, cache strategy more complex (every threshold value is a separate cache key, potential cache thrash)

    **Option C — Client-side compute on raw account data.**
    - Portal receives raw account-level data (account_id + AUA) for the advisor's book, filters client-side based on slider position
    - **Pros:** instant slider feedback, zero server cost per change
    - **Cons:** PII exposure (account-level data exposed to portal client — verify PII classification per `comp-pii audit`), payload size scales with account count, still need server-side count for downstream aggregates
    - **Hybrid sub-option C':** client-side slider for visual count, but firm-level/role-level rollup stays server-precomputed at common buckets

    **Trade-off dimensions to evaluate per option:**
    - **Latency:** time from slider movement → updated number on screen
    - **Server cost:** compute + S3 storage delta
    - **PII exposure:** does the option expose more raw account data to the portal client than current state?
    - **Cache safety:** per `feedback_cache_invalidation_react_query` patterns — are existing cache keys safe?
    - **UX flexibility:** continuous slider vs discrete buckets
    - **Engineering cost:** TOs needed (C-script change, Lambda, portal frontend, deploy cycle)
    - **Forward extensibility:** can other thresholds (e.g., large-account threshold, fee-tier breakpoints) reuse the same architecture?

    **Threshold-state persistence question:**
    Where does the user's chosen threshold live?
    - URL parameter (shareable links — useful for "send Andrew a link to my $25k consolidation view")
    - User profile preference (sticky across sessions)
    - Session ephemeral (no persistence — slide and forget)
    Recommend a default + document the trade-offs.

    **Recommended implementation path:**
    Pick one of A/B/C/C' with rationale + propose a phased implementation:
    - Phase 1: backend C-script change (if needed)
    - Phase 2: Lambda/API endpoint (if Option B)
    - Phase 3: portal frontend wiring + toggle UI
    - Phase 4: cache invalidation strategy (if needed)
    - Phase 5: validation + acceptance

    **OUT OF SCOPE for this TO:**
    - NO code changes (investigation only)
    - NO portal frontend implementation
    - NO C-script modifications
    - NO PRD-level architectural decision — just options analysis with recommendation
    - Backend pricing logic
    - Other portal toggles (only Consolidation Opportunities scope)
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="current state mapping (mandatory before architecture analysis)">
      <step>
        <run>grep -n "small_account\|40_000\|40000\|small.account.threshold" data/black_diamond/scripts/gold/C_08.advisor_fee_efficiency.py — locate the $40k constant + every dependent computation</run>
        <expect>Exact file:line for the constant. Enumerate every variable + output field that depends on it.</expect>
        <if_mismatch>If the threshold is parameterized as a function arg or config field rather than a literal, document.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io C_08.advisor_fee_efficiency — confirm WRITES manifest includes small_account_* fields + identifies downstream consumers</run>
        <expect>Full producer chain. small_account_count + small_account_avg_aua should be in C_08's output manifest. Downstream consumer is D_04 per session context.</expect>
        <if_mismatch>If the field isn't in C_08's output manifest, the threshold may live elsewhere — investigate.</if_mismatch>
      </step>
      <step>
        <run>comp-blast small_account_count + comp-blast small_account_avg_aua — full downstream consumer map</run>
        <expect>Map: C_08 → D_04 → platinum/firm/* (or platinum/advisors/*) → portal API → portal component. Identify every consumer for cache-invalidation + schema-change blast radius.</expect>
        <if_mismatch>If portal reads C_08 output directly (not via D_04), document — affects implementation Path A's deploy cadence.</if_mismatch>
      </step>
      <step>
        <run>comp-routes for /Books tab → Revenue Operations & Analysis → Consolidation Opportunities (or grep portal source for "consolidation" / "small account")</run>
        <expect>React component name + API endpoint identified. React Query key documented.</expect>
        <if_mismatch>If feature isn't yet wired (greenfield), document — affects Phase 3 portal scope estimate.</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check on the Consolidation Opportunities component — verify field names match C_08's writes</run>
        <expect>Schema alignment confirmed. No MISSING fields surfacing.</expect>
        <if_mismatch>If MISSING surfaces, the portal expects a field C_08 doesn't write — document the alignment gap before architecture analysis.</if_mismatch>
      </step>
      <step>
        <run>comp-pii audit on small_account_count + small_account_avg_aua + any account-level fields that would be exposed under Option C</run>
        <expect>Pseudonymization vs cleartext status documented. Flag any cleartext PII that would surface if account-level data were exposed to portal client.</expect>
        <if_mismatch>If PII is cleartext, Option C/C' may be a non-starter without pseudonymization work.</if_mismatch>
      </step>
      <step>
        <run>comp-cache collisions for the React Query key serving the Consolidation Opportunities widget</run>
        <expect>No existing collisions. Document key shape + TTL.</expect>
        <if_mismatch>If cache key already overloaded, option B's per-threshold caching needs new key namespace.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="architecture briefing draft">
      <step>
        <run>Author briefing at data/black_diamond/diagnostics/STAUDT/CONS/small_account_threshold_briefing.md per scope sections</run>
        <expect>Briefing covers: current state map (Phase 0 evidence), three options A/B/C/C' with full trade-off analysis, persistence question, recommended path with rationale, phased implementation TO sketch, open questions for COO/CTO/Andrew.</expect>
        <if_mismatch>If any section is "TBD" at submission, surface to COO before sending to Andrew.</if_mismatch>
      </step>
      <step>
        <run>MCP COO with briefing location + 1-paragraph executive summary covering recommended option + headline trade-off</run>
        <expect>Decision-ready exec summary; full briefing as reference.</expect>
        <if_mismatch>If recommendation unclear (e.g., trade-offs make all 3 viable), surface the choice point explicitly to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/CONS/small_account_threshold_briefing.md</path>
      <description>Architecture investigation briefing. Sections: TL;DR + recommendation, current state (where $40k lives + propagation chain), Three options A/B/C/C' with trade-off matrix (latency / server cost / PII / cache / UX / engineering / extensibility), threshold-state persistence (URL param vs user pref vs ephemeral), recommended path with rationale, phased implementation TO sketch, open questions for COO/CTO/Andrew.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/CONS/comp_evidence.md</path>
      <description>Per-compiler-tool output (comp-pipescript io C_08, comp-blast small_account_*, comp-routes, comp-transform schema-check, comp-pii audit, comp-cache collisions). Required by CLAUDE.md cross-domain compiler-tools mandate before architecture briefing.</description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] Phase 0 compiler-tools evidence file complete + filed at data/black_diamond/diagnostics/STAUDT/CONS/comp_evidence.md
    - [ ] Briefing identifies exact file:line of $40k constant in C_08
    - [ ] Briefing maps full propagation chain: C_08 → D_04 → platinum → portal API → portal component
    - [ ] Briefing presents three implementation options A/B/C (with C' hybrid sub-option) with full trade-off matrix
    - [ ] Briefing addresses PII implications under Option C/C' explicitly
    - [ ] Briefing addresses cache-invalidation implications under Option B explicitly
    - [ ] Briefing recommends a path with cited rationale + phased implementation TO sketch
    - [ ] Briefing addresses threshold-state persistence (URL param vs user pref vs ephemeral) with recommendation
    - [ ] Executive summary MCP'd to COO before forwarding to Andrew
    - [ ] NO code changes in this TO
  </acceptance_criteria>

  <guardrails>
    - **INVESTIGATION ONLY** — no code, no schema migrations, no implementation TOs in this TO. Implementation follows after Andrew's review of the briefing.
    - **No PII expansion.** If recommendation is Option C/C', address PII pseudonymization explicitly. Don't propose any path that exposes raw account-level data to portal client without pseudonymization first.
    - **No cache invalidation surprise.** Option B's per-threshold caching pattern needs explicit cache-key strategy in the briefing — no hand-waving.
    - **Compiler-tools evidence is mandatory** per CLAUDE.md cross-domain rule. Do NOT submit briefing without comp-pipescript io + comp-blast + comp-routes + comp-transform schema-check + comp-pii + comp-cache outputs filed.
    - **No KPI overlap.** Your KPI TO (`ADVI_STAUDT.KPI`) is separate scope (engine quality framework). Don't bundle. If KPI surfaces a related sentinel opportunity (e.g., "small_account_count consistency check"), note it as a follow-up but don't bundle.
    - **Coordinate with ~A** if Phase 0 mapping reveals the threshold or downstream computation is affected by ~A's BFIX1+BFIX2+BFIX4 engine-accuracy work (e.g., if the small_account count is currently inaccurate due to bd_stale overreach). Mention in briefing — don't try to fix.
    - **Coordinate with ~B** if EOP2025 cohort decomposition surfaces a related rollup-methodology question. Mention in briefing.
    - **No emojis, selective staging, agent commit identity** per existing memory rules.
  </guardrails>

  <agent_context_setup>
    1. Register + inbox-watch (first two tool calls)
    2. Read:
       - C_08.advisor_fee_efficiency.py (full file, focus on small_account_count + small_account_avg_aua functions and the $40k constant)
       - ADVI_ROLLUP.B9 + B10 commit messages (f2ec98d1, bb426933) for original feature intent
       - portal/ source for /Books tab → Revenue Operations & Analysis (find via grep "Consolidation" or "consolidation_opportunities")
       - docs/architecture/ if there's a portal feature index
       - project_bd_is_ground_truth.md + feedback_no_unverified_theories_as_conclusions.md (apply same rigor as engine wave)
    3. Heartbeat every 60s during active work
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1: ACK within 5 min: "ACK STAUDT.CONS — starting Phase 0 current-state mapping in parallel with KPI"
    - Phase 0 gate: MCP COO with comp-evidence file complete + brief mechanism note
    - Phase 1 gate: MCP COO with briefing + executive summary; COO forwards to Andrew for direction-setting
    - RAVC step 4: closeout when Andrew approves a direction; implementation TO authoring follows separately
  </completion_protocol>
</task_order>
