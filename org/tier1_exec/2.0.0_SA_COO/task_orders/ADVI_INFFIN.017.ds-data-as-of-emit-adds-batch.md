<task_order>
  <metadata>
    <id>ADVI_INFFIN.017</id>
    <slug>ds-data-as-of-emit-adds-batch</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-14</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED 2026-05-14 by COO per CTO route 2026-05-14 ~18:0XZ — opportunistic SLA non-gating on ADHC_FECACHE_COHERENCE categorical PR (which SHIPPED 120df453 portal/DEV at 18:35Z). DS sub-agent routing: DS~A / DS~C / DS~D opportunistic pickup based on bench-state when authoring lane bandwidth permits.</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P3 — non-gating data_as_of universality completion; narrows FECACHE_COHERENCE multi-key normalization interceptor scope from 28 canonical / 3 aliases / 7 lack → 32 canonical / 3 aliases / 3 lack (where the 3 remaining = legitimate-skip metadata response types)</priority>
    <sla>~40min total wall (4 emit-adds × ~10min each); opportunistic batch OR single-emit-per-touch DS judgment</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_FECACHE_COHERENCE.md §"data_as_of universality census results (CTO Q1 — 2026-05-14 17:58Z)" — 7 lack chain-bound freshness marker; 4 flagged DS follow-on</ref>
    <ref type="cto_route">CTO MCP 2026-05-14 ~18:0XZ: "4 P3 follow-on TOs surfaced for your authoring lane (opportunistic SLA, NON-GATING on categorical PR)" + DE 0.4 census brief</ref>
    <ref type="categorical_pr_anchor">DE 0.4 ADHC_FECACHE_COHERENCE.001 SHIPPED 120df453 portal/DEV at ~18:35Z — multi-key normalization helper extracts `data_as_of` || `as_of_date` || `snapshot_date`. Until these 4 response types emit one of those keys, interceptor silently no-ops on them (partial coverage).</ref>
  </references>

  <context>
    DE 0.4 ADHC_FECACHE_COHERENCE.001 categorical FE-cache coherence interceptor (~270 LOC; portal/DEV `120df453`) reads chain-bound freshness from `data_as_of` || `as_of_date` || `snapshot_date` via `extractChainTimestamp()` multi-key helper. Per CTO Q1 census 2026-05-14 17:58Z, 28 response types canonically have `data_as_of`; 3 use field aliases; **7 lack any chain-bound freshness marker**.

    Of the 7 lacking, 3 are LEGITIMATE skips (admin/metadata response types):
    - `PartnersResponse` (admin list — no chain-bound freshness applies)
    - `FiltersResponse` (filter-options metadata)
    - `AdvisorExecSummary` (LLM-generated; has `generated_at` per LLM semantic)

    **The remaining 4 are FLAG — DS follow-on (this TO scope):**
    - `AdvisorNnaClientsResponse` — per-advisor NNA client list
    - `ConcentrationResponse` — concentration analysis response
    - `AdvisorDrilldownSummary` — advisor drilldown summary
    - `InflecTimeseriesChartResponse` — Inflection-specific timeseries chart

    Until DS ships `data_as_of` emit-add on these 4, FECACHE_COHERENCE interceptor silently no-ops on their response types (no canonical-store update; no cross-callsite invalidation triggered by these fetches). FE-cache coherence partial coverage; structurally correct (fail-closed) but reduces invariant strength.

    Also flagged per census (non-blocking optional): `ClientDirectoryResponse` has optional `data_as_of?`; recommend require.
  </context>

  <objective>
    Add `data_as_of` field emit to gold-emit source(s) for 4 flagged response types. Each emit-add ~10min single-field addition; total ~40min DS work. Materializes on next chain run; FE picks up via existing FECACHE_COHERENCE interceptor (no FE change required).
  </objective>

  <scope>
    <files>
      <file action="modify">data/orion/scripts/gold/INF_D_*.py — the gold scripts emitting the 4 response types (DS to identify exact source per type via comp-pipescript io OR grep)</file>
      <file action="no_modify">portal/src/types/ — TypeScript schema additions optional follow-on (DE 0.4 lane; if needed, type extensions are backward-compatible since `data_as_of?: string` already permitted)</file>
    </files>
    <emits_to_add>
      <emit>
        <response_type>AdvisorNnaClientsResponse</response_type>
        <gold_source>DS to identify via `comp-pipescript io` OR grep `nna_clients` in INF_D_*.py</gold_source>
        <field>`data_as_of: chain_date` matching firm canonical emit pattern</field>
      </emit>
      <emit>
        <response_type>ConcentrationResponse</response_type>
        <gold_source>Likely INF_D_07 or INF_D_07a (concentration_risk + firm_concentrations); DS to confirm via comp-pipescript io</gold_source>
        <field>`data_as_of: chain_date` matching firm canonical</field>
      </emit>
      <emit>
        <response_type>AdvisorDrilldownSummary</response_type>
        <gold_source>DS to identify via comp-pipescript io OR grep `drilldown_summary` in INF_D_*.py</gold_source>
        <field>`data_as_of: chain_date` matching firm canonical</field>
      </emit>
      <emit>
        <response_type>InflecTimeseriesChartResponse</response_type>
        <gold_source>Likely INF_D_04 (`timeseries_chart.json` emit); DS to confirm via comp-pipescript io</gold_source>
        <field>`data_as_of: chain_date` matching firm canonical</field>
      </emit>
    </emits_to_add>
  </scope>

  <phase id="1" when="before each emit-add">
    <step>
      <run>comp-pipescript io {INF_D_*} (per gold-source identification) — confirm response type emit script + downstream FE consumer</run>
      <expect>Surfaces emit path + portal consumers. If known-bug for INF scripts per DS~A surfacing, fall back to grep + direct file read.</expect>
    </step>
    <step>
      <run>grep -rn "{response_type}" portal/src/api/endpoints/ portal/src/types/ — verify FE adapter doesn't add `data_as_of` synthetically</run>
      <expect>Confirms FE expects gold-emit-provided. If adapter strips or doesn't pass-through, route to DE 0.4 for adapter pass-through fix (separate concern).</expect>
    </step>
  </phase>

  <phase id="2" when="emit-add per response type">
    <step>
      <run>Add `data_as_of: chain_date` to emit dict for response type (single-field add; ~10 LOC inclusive of comment provenance to this TO + FECACHE_COHERENCE canonical PR)</run>
      <expect>Field added at same position as firm canonical pattern (e.g., top-level OR `_meta.data_as_of` per existing artifact convention). DS judgment per artifact's existing shape.</expect>
    </step>
    <step>
      <run>ds-commit-gate.sh + safe-deploy.sh per CLAUDE.md Rule 13 + 14. `from __future__ import annotations` first import preserved per Rule 15.</run>
      <expect>Both gates PASS. Author identity per agent serial.</expect>
    </step>
  </phase>

  <phase id="3" when="after batch ship">
    <step>
      <run>AE 0.6.1 chain-fire materialization (bundling opportunistic with other in-flight materializations)</run>
      <expect>Each updated emit reaches platinum on next chain run.</expect>
    </step>
    <step>
      <run>Post-chain sentinel verify: aws s3 cp s3://opal-data-inf/{path}/{artifact}.json - | jq '.data_as_of' per 4 response types</run>
      <expect>Each artifact emits `data_as_of` matching chain date.</expect>
    </step>
    <step>
      <run>RAVC2 to COO</run>
      <expect>Evidence-bearing close: per-response-type commit SHA + safe-deploy log + post-chain sentinel.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `AdvisorNnaClientsResponse` gold-source emits `data_as_of` matching firm canonical
    AC2: `ConcentrationResponse` gold-source emits `data_as_of` matching firm canonical
    AC3: `AdvisorDrilldownSummary` gold-source emits `data_as_of` matching firm canonical
    AC4: `InflecTimeseriesChartResponse` gold-source emits `data_as_of` matching firm canonical
    AC5: ds-commit-gate + safe-deploy PASS for each emit-add
    AC6: Post-chain S3 sentinel verifies `data_as_of` present per response type
    AC7: FECACHE_COHERENCE interceptor coverage census narrows from 28 canonical / 3 aliases / 7 lack → 32 canonical / 3 aliases / 3 lack (3 legitimate skips: PartnersResponse + FiltersResponse + AdvisorExecSummary)
    AC8: RAVC2 to COO with per-response-type evidence
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 (comp-pipescript io per response type before emit). Phase 2 ds-commit-gate + safe-deploy per commit. Phase 3 post-chain sentinel.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: None — pure emit-add; backward-compatible.
    PARALLEL-OK: with any other DS lane; with AE 0.6.1 chain re-fires; with DE 0.4 stale-stub audit.
    NO FE CHANGE REQUIRED: TypeScript `data_as_of?: string` is already permitted; multi-key normalization already extracts it via existing FECACHE_COHERENCE interceptor `120df453`.
    BATCH OR SINGLE-EMIT-PER-TOUCH DS JUDGMENT: TO permits either pattern. Opportunistic single-emit-per-INF_D_* maintenance touch is acceptable; batch ship via single chain-fire is acceptable. DS sub-agent ratify on cadence.
    OPTIONAL FOLLOW-ON: `ClientDirectoryResponse` has optional `data_as_of?`; recommend require — DS opportunistic touch when next adjacent maintenance.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Each emit-add is additive; backward-compatible. Materializes on next normal chain run.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. 4 emit-adds (one per response type) shipped via ds-commit-gate + safe-deploy
    2. Optional 5th emit-add for ClientDirectoryResponse if opportunistic
    3. Post-chain S3 sentinel verification per response type
    4. RAVC2 to COO with per-response-type commit SHA + sentinel
  </deliverables>

  <ravc>DS RAVC2 to COO on AC1-8 PASS. FECACHE_COHERENCE interceptor coverage validates census narrow post-chain.</ravc>

  <notes>
    **Author identity:** `--author="{serial} <{serial}@opal.agent>"` per agent.

    **Opportunistic SLA:** non-gating; pickup based on bench-state. If DS sub-agent has 10min between primary task + next dispatch, single-emit pickup is appropriate.

    **DS sub-agent routing:** DS~A / DS~C / DS~D all eligible. DS~B currently focused on BD pipeline + cash_drag follow-on (per CLAUDE.md memory `feedback_ds_sub_agent_routing.md` — direct sub-agent address when base shows `[LIVE xN]`).

    **TypeScript schema update follow-on (optional, DE 0.4 lane):** if any response type's TypeScript schema declares `data_as_of?: string` already, no FE change needed. If declared without the field, DE 0.4 opportunistic addition per stale-stub audit pattern (parallel work).

    **No emoji per CLAUDE.md.** Inline comment provenance to ADHC_FECACHE_COHERENCE PRD + this TO when adding emit.

    **Phase 4 alignment:** post-chain, FECACHE_COHERENCE interceptor's multi-key normalization needs no code change (already reads `data_as_of` first); coverage narrows to 32 canonical with this batch.

    **Banking opportunity:** if any of the 4 response types surfaces a non-trivial emit-add (e.g., needs `data_as_of` at multiple grain levels), worth banking as `feedback_response_type_data_as_of_emit_grain.md` — uncommon but possible.
  </notes>
</task_order>
