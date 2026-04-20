<task_order>
  <metadata>
    <id>ADVI_STAUDT.FIX6</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-20</date>
    <status>dispatched</status><!-- DISPATCHED 20260420T14:47Z by 2.0.0_SA_COO. CTO approval MCP 20260420T144745Z "APPROVED as drafted (f1c685aa)... No edits required." Andrew called ~D to spawn (rationale: ~D just mapped platinum NNA consumers in their synthesis → Phase 0 is at-hand context). -->
    <project_code>ADVI_STAUDT</project_code>
    <priority>P1 — schedules after FIX1 lands (parallel to FIX2/FIX3A closeout). Addresses Andrew's top-level historical-NNA concern that INV1 confirmed as a real firm-grain universe asymmetry, NOT a per-advisor code bug.</priority>
    <bug_reference>Pre-2023 universe asymmetry between silver/transactions (broader flow-tracked universe) and holdings_lots-derived AUA (narrower tracked universe). INV1 Q1 20260420T143042Z quantified: 4.28x ratio firm NNA/AUA in 2020, converging to 0.91x by 2024. See data/black_diamond/diagnostics/STAUDT/INV1/historical_nna_mechanism.md (when AE publishes).</bug_reference>
    <lane>~D — single-TO lane. Andrew-assigned 2026-04-20T14:47Z. Rationale: ~D's synthesis just mapped platinum's NNA consumers + the full B/C/D propagation chain; the Phase 0 comp-pipescript/blast surface-identification is at-hand context. Option B work (post-FIX1) also slated for ~D + AE joint, so continuity is preserved.</lane>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md §3.0 (Class 1 — path sub-class) — universe-asymmetry context</ref>
    <ref type="inv1">data/black_diamond/diagnostics/STAUDT/INV1/historical_nna_mechanism.md (AE — ruling on firm-level NNA vs AUA asymmetry, pending final commit)</ref>
    <ref type="cto-authorization">CTO 20260420T143914Z — "NEW TO — PORTAL-GATE 3-YEAR NNA HISTORY CAP". Andrew authorized directly.</ref>
    <ref type="ae-firm-q1-mcp">AE to COO 20260420T143042Z — firm-level Q1 numeric table + mechanism identification</ref>
    <ref type="superseded-by">Option B scoping initiative (post-FIX1) — fixes the asymmetry root cause (flip D-scripts to nna_atomic/ universe). FIX6 is INTERIM surface-level gate to protect users until Option B ships.</ref>
  </references>

  <objective>
    Add a 3-year lookback gate on NNA historical-timeseries display, so the portal never renders pre-2023 NNA against pre-2023 AUA where the universe asymmetry produces the apparent 2-4x stock/flow violation. Implement at the platinum layer (preferred — all D-outputs inherit) if feasible, otherwise at D_00b + D_02 partition-filter logic. This is an INTERIM cover while Option B's architectural fix (nna_atomic/ schema expansion + D-script flip to broader universe) ships in weeks. After Option B lands, FIX6 may be rolled back or retained as a UX choice — that decision lives with Option B.
  </objective>

  <scope>
    **Defect (verbatim from INV1 Q1):**
    Portal firm-level NNA cumulative at 2020-12-31 = $118.20M vs Portal firm AUA = $27.65M (ratio 4.28x). Same pattern 2020-2022 (4.28x / 3.82x / 2.85x). Converges to <1x by 2024. Root cause: silver/transactions covers WIDER account universe than holdings_lots-derived AUA in 2020-2022 (441 "flow-only" accounts at 2020-12-31, 1,100 at 2021-12-31, 1,817 at 2022-12-30). As holdings coverage expanded 2023+, ratio normalized. Real flows, legitimate data, universe-mismatch rendering.

    **Andrew's directive (verbatim from CTO 20260420T143914Z):**
    "Cap NNA history display on the portal at 3 years max rather than full history. Simplest implementation likely lives in the portal's timeseries query layer or D_00b/D_02 partition-filter logic. Prefer: platinum layer, not portal layer, so all D outputs inherit."

    **Phase 0 — implementation surface identification (MANDATORY before coding):**
    Run comp-pipescript io on D_00b, D_02, and every platinum/* script that consumes their NNA output. Enumerate which scripts produce firm-level-NNA-timeseries and advisor-level-NNA-timeseries fields currently on the portal. The 3-year gate should apply to BOTH firm and advisor surfaces — identify every surface.

    Candidate implementation surfaces (investigate in order of preference):
    1. **Platinum layer (preferred):** find the platinum aggregator that produces `firm_nna_timeseries` and `advisor_nna_timeseries` portal feeds. If such an aggregator exists and has a date-filter hook, apply the gate there.
    2. **D_00b (portal_timeseries):** filter NNA timeseries partitions at the D-script level so anything read by platinum/portal is already 3-year-capped.
    3. **D_02 (advisor_client_detail):** same for advisor-level NNA fields in book.json.
    4. Portal frontend (least preferred): client-side filter. Use ONLY if upstream surfaces can't be gated cleanly.

    Document which surface(s) you pick + why in a Phase 0 mechanism note. MCP COO with surface selection BEFORE coding.

    **Gate semantics:**
    - Lookback window: exactly 3 years from the current portal render date. E.g., if portal is displaying data as of 2026-04-20, NNA history starts 2023-04-20.
    - Rolling window — not fixed-year — so the gate evolves naturally as time passes.
    - Applies to BOTH cumulative NNA and daily/monthly NNA timeseries displays.
    - Applies at both firm-level and advisor-level surfaces.
    - Portal AUA stock display is UNCHANGED (the AUA field is unaffected; only the NNA timeseries is gated).

    **Pre-gate cache invalidation:** if platinum outputs are cached (React Query, CloudFront, S3 caching layer), document what needs invalidation. If cache keys include date filters, new cache entries will be created naturally; if not, flag for DT coordination.

    **OUT OF SCOPE:**
    - No changes to how NNA is COMPUTED — only to how it's DISPLAYED historically. Gate, not fix.
    - No changes to nna_atomic/ schema or canonical/nna/ schema (Option B owns that)
    - No changes to holdings_lots coverage or canonical/nna/.aua_current computation
    - No changes to FIX1/2/3A/5 scope
    - No portal visual redesign — simply gate the timeseries query

    **After Option B lands:**
    FIX6 may be retained (as a UX choice — pre-2023 NNA is simply too sparse to be useful) OR rolled back (if Option B's broader-universe AUA eliminates the visual asymmetry). This decision lives with Option B scoping, not FIX6.
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="implementation surface identification (MANDATORY before coding)">
      <step>
        <run>comp-pipescript io D_00b &amp;&amp; comp-pipescript io D_02</run>
        <expect>Column manifests for both. Identify every output field that carries NNA timeseries to platinum or portal.</expect>
        <if_mismatch>If NNA timeseries fields aren't where you expect, MCP COO with findings.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io on every platinum/* script + grep for NNA field consumption across platinum</run>
        <expect>Map: D_00b NNA fields → platinum aggregator → portal API route. Identify the SINGLE UPSTREAM-MOST gate-applicable surface.</expect>
        <if_mismatch>If platinum doesn't aggregate NNA at all and it goes D-script→portal directly, gate at D-script.</if_mismatch>
      </step>
      <step>
        <run>comp-cache collisions (per CLAUDE.md — React Query cache safety)</run>
        <expect>Identify any cache-key collision risk if gated field names stay the same but filter behavior changes.</expect>
        <if_mismatch>Collision risk = may need cache key addition or explicit invalidation. Flag for DT coordination.</if_mismatch>
      </step>
      <step>
        <run>comp-blast on the gate-application surface script</run>
        <expect>Full downstream consumers of the field. Confirms no surprise portal pages or Lambda functions consume it beyond the firm/advisor timeseries widgets.</expect>
        <if_mismatch>Any unexpected consumer = assess whether gate applies there too; MCP COO before deciding.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="implementation">
      <step>
        <run>Code change: apply 3-year lookback gate at the chosen surface</run>
        <expect>Gate applies uniformly firm + advisor; today - 3 years, rolling. Gated field documented in script docstring or comment.</expect>
        <if_mismatch>Any test showing pre-3yr data still reaching portal = gate mis-applied.</if_mismatch>
      </step>
      <step>
        <run>Unit/integration test: produce script output for today's date; assert oldest NNA timeseries date is >= today - 3yr</run>
        <expect>Passes. Oldest date = today - 3 years exactly (or nearest trading date).</expect>
        <if_mismatch>Fails = gate mis-applied; fix.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="validation">
      <step>
        <run>End-to-end run of the gated script + downstream platinum/portal pipeline on current prod date</run>
        <expect>Script completes, output contains only 2023-04-20 onward NNA timeseries (assuming 2026-04-20 run date).</expect>
        <if_mismatch>Any older NNA data = investigate; do not deploy.</if_mismatch>
      </step>
      <step>
        <run>comp-validate against gated script's config (if applicable)</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Add invariant to gold_validate_config.yaml if missing — regression protection.</if_mismatch>
      </step>
      <step>
        <run>Portal smoke test: firm-level + advisor-level NNA timeseries widgets load without error, show 3yr history only</run>
        <expect>Widgets render; pre-2023 data NOT visible. If portal caches are stale, coordinate with DT to invalidate.</expect>
        <if_mismatch>Pre-2023 still showing = cache not invalidated OR gate applied at wrong surface. Escalate to DT+COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/scripts/... (surface to be identified in Phase 0)</path>
      <description>Minimum-surface code change applying the 3-year rolling gate at the upstream-most feasible surface. Commit message cites CTO 20260420T143914Z + INV1 ruling + "interim gate until Option B ships".</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/FIX6/fix_to_6_evidence.md</path>
      <description>Phase 0 surface-identification note + Phase 1/2 validation outputs (oldest-date assertions, portal smoke test screenshots or widget JSON).</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/gold_validate_config.yaml (if needed)</path>
      <description>Regression invariant asserting oldest NNA timeseries date is within last 3 years for the gated script.</description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] Phase 0 mechanism note identifies the single chosen gate surface + rationale (MCP'd to COO BEFORE coding)
    - [ ] Gate applies uniformly to BOTH firm-level and advisor-level NNA timeseries
    - [ ] Rolling 3-year window (today - 3yr), not fixed year
    - [ ] Portal AUA display unchanged
    - [ ] Post-deploy portal smoke test confirms pre-2023 NNA is not visible on firm and advisor widgets
    - [ ] No regression to NNA CURRENT-year values or recent-period accuracy
    - [ ] Cache invalidation coordinated with DT if platinum/portal caching requires it
    - [ ] comp-validate exits 0 on gated script
    - [ ] Evidence file documents Phase 0-1-2 per protocol
  </acceptance_criteria>

  <guardrails>
    - **Gate, not fix:** don't change NNA computation. Don't touch universe logic. Don't rewrite history. Just hide pre-3yr NNA from display.
    - **Prefer upstream:** platinum > D-script > portal-frontend. Pick the single upstream-most surface that gates both firm + advisor simultaneously.
    - **No Option B overlap:** if Phase 0 surfaces temptation to "while I'm here, flip to nna_atomic/" or "while I'm here, fix the universe asymmetry" — STOP. That is Option B's scope. This TO is the 3-week interim gate only.
    - **Cache safety:** per CLAUDE.md + comp-cache collisions — same field name post-gate means existing cache entries will serve STALE data until invalidated. Coordinate cache invalidation with DT if required.
    - **Portal coordination via DT:** if any portal-layer change is needed (e.g., display a "3-year window" label or disclaimer), route via DT for portal deploy. Don't push to portal directly.
    - **No emojis, selective staging, agent commit identity** per standard rules.
    - **DT owns push** (per CTO 20260420T142143Z DT-online protocol clarification).
  </guardrails>

  <agent_context_setup>
    1. Register + inbox-watch (first two tool calls)
    2. Read:
       - docs/architecture/ADVI_STAUDT.md §3.0
       - data/black_diamond/diagnostics/STAUDT/INV1/historical_nna_mechanism.md (AE's final ruling document)
       - data/black_diamond/scripts/gold/D_00b.portal_timeseries.py (current NNA timeseries emitter)
       - data/black_diamond/scripts/gold/D_02.advisor_client_detail.py (advisor-level NNA)
       - data/black_diamond/scripts/platinum/* (aggregator candidates)
    3. Heartbeat every 60s during active work
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1 (Acknowledge): within 5 min of receipt, MCP COO with "ACK STAUDT.FIX6 — starting Phase 0 surface identification"
    - Phase 0 gate: MCP COO with surface selection + rationale BEFORE coding. WAIT for COO go-signal.
    - Phase 1 gate: MCP COO with patch summary + validation headline before requesting DT push
    - RAVC step 4 (Close): MCP COO with deploy commit SHA + portal smoke-test evidence + any DT cache-invalidation confirmation
  </completion_protocol>
</task_order>
