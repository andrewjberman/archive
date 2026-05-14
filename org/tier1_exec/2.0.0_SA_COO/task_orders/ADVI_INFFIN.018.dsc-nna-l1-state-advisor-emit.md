<task_order>
  <metadata>
    <id>ADVI_INFFIN.018</id>
    <slug>dsc-nna-l1-state-advisor-emit</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-14</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED 2026-05-14 ~19:35Z by COO per CTO 19:30Z routing (Track B Backend DS lane). RD 0.4.2 Track A FE display-bug fix dispatched directly by CTO in parallel.</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — Andrew-direct NNA Bell Curve Coverage feature-completeness; portal demo surface; Track B backend emit gap</priority>
    <sla>~3-5h wall per CTO sizing; ~1.5-2.5h actual per Pod 4 5-10× velocity pattern (with potential 10-14× upper-bound if pattern-reuse from NMCOHT/D-min/D-max compounds)</sla>
  </metadata>

  <references>
    <ref type="cto_route">CTO MCP 2026-05-14 ~19:30Z: "Track B Backend (DS lane) — ADVI_INFFIN.NNN.dsc-nna-l1-state-advisor-emit — please author for DS pod dispatch. Field names already match FE read path. Per-grain matches L2 by_city pattern. Estimated DS wall: ~3-5h for gold script emit + chain re-fire to materialize."</ref>
    <ref type="track_a_sibling">RD 0.4.2 ADVI_INFFIN.NNN.rd-nna-l0-firm-wide-display-bug — CTO direct GO + 4 likely failure-mode diagnostic guidance; ~1-2hr wall</ref>
    <ref type="andrew_direct">Andrew-flagged NNA Bell Curve Coverage gap — surfaced via RD 0.4.2 investigation per Andrew direction</ref>
    <ref type="adjacent_pattern">L2 by_city emit (existing) — per-city aggregate HH NNA distribution; this TO replicates pattern to L1 (state + advisor grain)</ref>
    <ref type="canonical_consumer_field">FE read path: `views.nna.[period].geo.drill[stateKey].total: DistributionStats` (per-state) + `views.nna.[period].adv.drill[advisorKey].distribution: DistributionStats` (per-advisor)</ref>
  </references>

  <context>
    Per RD 0.4.2 investigation 2026-05-14, NNA Bell Curve display shows:

    | Level | Data | FE Path | Status |
    |---|---|---|---|
    | L0 global (GEO + ADV) | ✅ ships | ✅ wired | FE display bug (RD Track A) |
    | **L1 GEO State** | ❌ no `total` key | ✅ wired | **Backend emit gap (this TO)** |
    | **L1 ADV Advisor** | ❌ empty `drill={}` | ✅ wired | **Backend emit gap (this TO)** |
    | L2 GEO City | ✅ | ✅ | Working |

    FE consumer paths are wired + match the spec. Backend gold-script emit is missing the L1 state + L1 advisor per-grain DistributionStats aggregates. L2 by_city emit already works; same pattern applies for L1.

    **No new feature design needed** — this is filling an emit gap to match the existing FE consumer contract. Pattern replication from L2 by_city.
  </context>

  <objective>
    Add backend emit for L1 state + L1 advisor per-grain NNA DistributionStats aggregates per FE consumer field-path:
    - `views.nna.[period].geo.drill[stateKey].total: DistributionStats` (per-state aggregate HH NNA)
    - `views.nna.[period].adv.drill[advisorKey].distribution: DistributionStats` (per-advisor aggregate HH NNA)

    Per-grain matches existing L2 by_city pattern. Apply across monthly + quarterly + annual partner_analytics view-mode artifacts.
  </objective>

  <scope>
    <files>
      <file action="identify_then_modify">Gold script(s) emitting `partner_analytics_{monthly,quarterly,annual}.json#views.nna.[period]` — likely INF_D_04 or sibling. Verify via comp-pipescript io OR grep on existing L2 by_city emit pattern.</file>
      <file action="readonly_reference">Existing L2 by_city emit logic — pattern source for L1 state + L1 advisor replication</file>
      <file action="readonly_reference">FE consumer read paths — `views.nna.[period].geo.drill[stateKey].total` + `views.nna.[period].adv.drill[advisorKey].distribution`</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io INF_D_04 (or sibling per gold-source identify); grep `views.nna` in `data/orion/scripts/gold/INF_D_*.py`</run>
      <expect>Identify the gold-script emitter for `partner_analytics_*.json#views.nna` + locate existing L2 by_city emit logic as pattern source.</expect>
      <if_mismatch>If multiple gold scripts emit `views.nna`, document each; identify whether L1 state + L1 advisor are emitted by same script or split.</if_mismatch>
    </step>
    <step>
      <run>aws s3 cp s3://opal-data-inf/platinum/firm/partner_analytics_quarterly.json - | jq '.views.nna.quarterly.geo.drill | keys' + jq '.views.nna.quarterly.adv.drill | keys'</run>
      <expect>Empirical confirmation of L1 emit state — RD investigation surfaced `no total key on state` + `empty drill={} on advisor`. Pre-touch baseline.</expect>
    </step>
    <step>
      <run>aws s3 cp s3://opal-data-inf/platinum/firm/partner_analytics_quarterly.json - | jq '.views.nna.quarterly.geo.by_city.SomeCityKey' (sample L2 working emit)</run>
      <expect>L2 by_city emit shape known — replicate same DistributionStats structure for L1 state + advisor.</expect>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <run>Replicate L2 by_city emit logic at L1 state grain — per-state aggregate HH NNA → DistributionStats. Apply across monthly + quarterly + annual view-mode artifacts.</run>
      <expect>Emit shape: `views.nna.[period].geo.drill[stateKey].total: { mean, median, p25, p75, p90, count }` (per L2 by_city DistributionStats convention).</expect>
    </step>
    <step>
      <run>Replicate same emit logic at L1 advisor grain — per-advisor aggregate HH NNA → DistributionStats.</run>
      <expect>Emit shape: `views.nna.[period].adv.drill[advisorKey].distribution: { mean, median, p25, p75, p90, count }`. Note: field name `distribution` (not `total`) per FE consumer read path; emit MUST match exactly.</expect>
    </step>
    <step>
      <run>ds-commit-gate.sh + safe-deploy.sh per CLAUDE.md Rule 13 + 14. `from __future__ import annotations` first import per Rule 15.</run>
      <expect>Both gates PASS. Author identity `--author="0.4.0_DS_ClientPlatform~C <0.4.0_DS_ClientPlatform~C@opal.agent>"`.</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>MCP AE 0.6.1 for chain re-fire — gold-d sequence sufficient (NNA emit is in INF_D_04-tier; not B-chain)</run>
      <expect>Chain re-fire ~13min wall. May bundle with concurrent BPMVH D-max chain re-fire if AE 0.6.1 hasn't fired yet (their decision per chain-stage semantics).</expect>
    </step>
    <step>
      <run>Post-chain sentinel: aws s3 cp s3://opal-data-inf/platinum/firm/partner_analytics_quarterly.json - | jq '.views.nna.quarterly.geo.drill | keys | length' + jq '.views.nna.quarterly.adv.drill | keys | length'</run>
      <expect>L1 state count > 0 (expected ~50 US states + DC max); L1 advisor count = 4 (Inflection advisor count).</expect>
    </step>
    <step>
      <run>Post-chain sample sentinel per-state + per-advisor: jq '.views.nna.quarterly.geo.drill.California.total' + jq '.views.nna.quarterly.adv.drill.peter_lee.distribution'</run>
      <expect>DistributionStats shape populated: mean / median / p25 / p75 / p90 / count fields all non-null with empirical values.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + DT 0.4 + RD 0.4.2</run>
      <expect>Evidence-bearing close: per-quarter L1 state + L1 advisor emit verified; sentinel matches FE consumer contract.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `views.nna.[period].geo.drill[stateKey].total: DistributionStats` emitted for monthly + quarterly + annual partner_analytics artifacts
    AC2: `views.nna.[period].adv.drill[advisorKey].distribution: DistributionStats` emitted (field name `distribution` matches FE read path; NOT `total`)
    AC3: DistributionStats shape matches L2 by_city convention (mean, median, p25, p75, p90, count per RD 0.4.2 wire-up)
    AC4: Per-state count > 0 across all view-mode artifacts (US states present per Inflection client geographic distribution)
    AC5: Per-advisor count = 4 (Inflection's 4 advisors: Patrick Scanlan + Peter Lee + Joe Brandenburg + IWM catchall)
    AC6: ds-commit-gate + safe-deploy PASS
    AC7: `from __future__ import annotations` first import preserved per CLAUDE.md Rule 15
    AC8: Post-chain S3 sentinel verifies emit shape + populated values
    AC9: RAVC2 to COO + CC CTO + DT 0.4 + RD 0.4.2 (RD 0.4.2 needed for Track A coord — if RD Track A ships <2h + DT hasn't promoted v2.1.87, fold into same bundle)
    AC10: Backward-compat: existing L0 + L2 emits unchanged; emit is purely additive
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: comp-pipescript io {INF_D_*} + grep `views.nna` for gold-source identify + S3 empirical pre-touch baseline + L2 by_city pattern source read
    Phase 2: ds-commit-gate.sh + safe-deploy.sh
    Phase 3: post-chain S3 sentinel + comp-pipescript deployed MATCH (or aws s3api head-object fallback per INF-bucket-scope gap)
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: None — pure backend emit-add; backward-compatible.
    PARALLEL-OK: with AE 0.6.1 TRIGMRK Phase 2 + AE 0.6.1 chain re-fire (which may bundle with this TO's chain re-fire) + RD 0.4.2 Track A FE fix.
    COORD WITH RD 0.4.2 TRACK A: if RD ships <2h + DT 0.4 hasn't promoted portal-v2.1.87 yet, fold into same bundle. Otherwise portal-v2.1.88 fast-follow. RD coordinates with DT 0.4 on inclusion timing.
    NO PORTAL CHANGES: FE consumer paths already wired per RD 0.4.2 investigation; backend emit fills the gap.
    OWNED-PATHS: gold scripts in data/orion/scripts/gold/ are DS-lane. Per [[feedback-owned-paths-hook-earns-keep-under-fast-ship]] hook will pass for DS-author edits. If TO ends up touching dispatch.sh (unlikely for NNA emit — should not require chain definition change), route per cross-lane MCP to AE.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Pure additive emit; backward-compat. Existing L0 + L2 emits unchanged. Materializes on next chain re-fire.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. Backend gold script L1 state emit per `views.nna.[period].geo.drill[stateKey].total: DistributionStats`
    2. Backend gold script L1 advisor emit per `views.nna.[period].adv.drill[advisorKey].distribution: DistributionStats`
    3. ds-commit-gate + safe-deploy PASS
    4. Chain re-fire materialization (possibly bundled with BPMVH D-max chain re-fire)
    5. Post-chain S3 sentinel verification
    6. RAVC2 to COO + CC CTO + DT 0.4 + RD 0.4.2
  </deliverables>

  <ravc>DS~C RAVC2 to COO + CC CTO + DT 0.4 + RD 0.4.2 on AC1-10 PASS.</ravc>

  <notes>
    **Pattern reuse opportunity:** L2 by_city existing emit logic + adjacent grain (L1 state, L1 advisor) — straight replication, no new design. Per Pod 4 5-10× velocity pattern, expected wall < CTO 3-5h sizing.

    **Sub-agent routing:** TO issued to DS~C per recent INF_D_04 territory (NMCOHT INF_D_04 augment + D-max β INF_B_00 ships). If DS~C bench-locked on D-max β chain re-fire monitoring, DS~D could absorb (also has INF_D_04 deep context post NMCOHT atomic Finding 1+2 ship). Bench-state sub-agent routing per agent judgment.

    **Author identity:** `--author="0.4.0_DS_ClientPlatform~C <0.4.0_DS_ClientPlatform~C@opal.agent>"` (or DS~D equivalent if absorbed).

    **No emoji per CLAUDE.md.** Inline comment provenance to this TO + RD 0.4.2 investigation when adding emit.

    **D-max β + this NNA emit chain re-fire bundling:** AE 0.6.1 may bundle both materializations into single chain re-fire (gold-b + gold-c + gold-d Option B) for efficiency. Sentinel matrices independent; both PASS independently.

    **No FE change required:** FE consumer paths already wired per RD 0.4.2 investigation. This is filling a backend gap to match existing FE consumer contract. Field names + types match FE read path exactly per RD investigation.

    **Banking observation candidate:** if pattern-reuse from L2 by_city → L1 grain is straightforward (~30min implementation), worth noting as "adjacent-grain emit replication low-cost when parent grain works" mini-pattern. Sister to D-min de-risks D-max via pattern reuse.
  </notes>
</task_order>
