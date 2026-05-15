<task_order>
  <metadata>
    <id>ADVI_INFLEC.NMCOHT</id>
    <slug>dsd-nmnc-cohort-bucketing-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-05-14</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED 2026-05-14 by COO per Andrew direct dispatch via DS~D brief. Investigation + execution starts immediately on Andrew direct framing; this TO ratifies + adds compiler mandate + structured AC + INF_D_08 timing-window coord with DS~C $156K investigation.</dispatch_unblock_condition>
    <project_code>ADVI_INFLEC</project_code>
    <priority>P1 — Andrew direct 2026-05-14 PM (IWM NMNC $20M current vs ~$5M historical surfaced structural model issue)</priority>
    <sla>~9-11h total (DS ~3-5h emit + DE ~3-5h consume + 45min mid-flight schema-lock check-in)</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inf-nmnc-cohort-bucketing-fix-20260514.md (DS~D authored; commit 63bac3803)</ref>
    <ref type="andrew_direct">2026-05-14: "we want to know when clients came in, new HH IDs, so then the frontend can bucket them depending on view mode"</ref>
    <ref type="binary_invariant">Andrew 2026-05-06: `nmnc + nmec = total_aua` binary split — preserved by Option A FE-bucketing model</ref>
    <ref type="empirical_anchor">chain_full_20260514_131842 partner_analytics_quarterly.json — current $19,979,134 / q1 $16,271,487 / q2 $12,604,363 / q3 $11,847,354 — rolling-window overlap signature</ref>
    <ref type="load_bearing_files">
      INF_D_04.client_portal_summary.py:992-1107 (primary surface — `_compute_hh_lifecycle()` produces partner_analytics_*.json donut.segments[nmnc])
      INF_D_08.nmec_nmnc_nna.py:213-217 + line 18 (sibling surface — firm + per-advisor aggregates)
    </ref>
    <ref type="cross_pod_dependency">DE 0.4 FE consumption — schema-lock check-in mid-flight</ref>
    <ref type="adjacent_investigation">DS~C ADVI_INFFIN.015 + $156K investigation (Andrew direct P1) — INF_D_08 read-only currently; coordinate edit timing window</ref>
  </references>

  <context>
    The portal's "NMNC by quarter / month / year" view is computed off a single rolling-365-day lifecycle window. Every period block (Q1/Q4/Q3/current) anchors its 365d cutoff to that period's end date and re-classifies the same population — adjacent quarters show overlapping cohorts; numbers drift monotonically rather than reflecting "clients who entered IN that quarter."

    Andrew's intended model: NMNC is a per-HH cohort attribute keyed off inception date (first_trade_date / first_txn_date). Each view mode (monthly/quarterly/annual) buckets clients dynamically by whether their inception falls within the bucket's date range. Same client appears in exactly one bucket per view mode; no overlap; numbers reflect real per-period acquisition.

    Fix is small at the data layer — per-HH inception is already computed at gold (INF_D_04._compute_hh_lifecycle() + INF_D_08._lifecycle_table()) — just isn't emitted. Aggregator + FE need the per-HH list to do the bucketing.

    Option A (FE buckets dynamically) recommended per Andrew preference + brief §3. Preserves Andrew 2026-05-06 binary invariant.
  </context>

  <objective>
    Emit per-HH `hh_lifecycle` array from both INF_D_04 (per-advisor) and INF_D_08 (firm + per-advisor) gold scripts. Each record: `{household_id, advisor_key, rep_id, first_trade_date, aua, window_net_nna}`. Keep existing rolling-window aggregates as legacy back-compat fields during cutover. FE consumption + view-mode dynamic bucketing in DE 0.4 lane (Phase 2 of this TO).
  </objective>

  <scope>
    <files>
      <file action="modify">data/orion/scripts/gold/INF_D_04.client_portal_summary.py — emit per-HH `hh_lifecycle` array alongside existing `views.aua` blocks; preserve rolling-window aggregates as legacy fields</file>
      <file action="modify">data/orion/scripts/gold/INF_D_08.nmec_nmnc_nna.py — same emit pattern on firm + per-advisor side; preserve `nmnc_aua / nmec_aua` aggregates as legacy fields</file>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts (DE 0.4 lane) — TypeScript schema `HhLifecycleRow`; adapter pass-through</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/* (DE 0.4 lane) — view-mode dynamic bucketing replacing donut.segments[nmnc] reads</file>
      <file action="readonly_reference">docs/briefs/inf-nmnc-cohort-bucketing-fix-20260514.md (canonical scope reference)</file>
    </files>
  </scope>

  <phase id="0" when="before code touch">
    <step>
      <run>§5 empirical probe (DS~D self-execute) — pull gold/dimensions/accounts_dimension_latest.parquet + bronze transactions for trailing 4 quarters; group by HH first_txn_date bucketed into calendar quarters; report per-quarter inception AUA sums</run>
      <expect>(a) typical baseline ~$5M + current-quarter spike ~$20M empirically confirmed (Andrew intuition validated); OR (b) spike is data artifact (e.g. Orion dim refresh re-keyed legacy HH_IDs as "new"). Branching decision gates on outcome.</expect>
      <if_mismatch>If (b) — data artifact — surface to AE 0.6.1 + COO BEFORE fix lands. Underlying bronze/silver has a problem; fix the wrong layer if proceeding without root cause.</if_mismatch>
    </step>
    <step>
      <run>MCP findings to COO + DE 0.4 + Andrew before code touch</run>
      <expect>Decision point reached: (a) GO on fix; (b) escalate upstream; (c) hybrid (fix per-period model AND escalate Orion dim concern in parallel)</expect>
    </step>
  </phase>

  <phase id="1" when="before INF_D_04 edit">
    <step>
      <run>comp-pipescript io INF_D_04.client_portal_summary</run>
      <expect>Confirm upstream silver dependencies + downstream portal consumers + S3 emit paths. Critical: enumerate which view-mode artifacts call _compute_hh_lifecycle (quarterly/monthly/annual siblings).</expect>
      <if_mismatch>If comp-pipescript surfaces unexpected dependencies or known-bug per DS~A 2026-05-14 finding, document inline + fallback to grep + direct file read.</if_mismatch>
    </step>
    <step>
      <run>comp-blast INF_D_04.client_portal_summary</run>
      <expect>Blast radius surface — partner_analytics_quarterly.json + monthly + annual sibling emits; downstream FE consumers in portal/src/pages/AdvisorIntelligence/_partners/*/index.tsx + DistributionTab.tsx + PartnerAnalytics.tsx.</expect>
    </step>
    <step>
      <run>DS-DE schema-lock check-in (45min slot, DS~D + DE 0.4 joint)</run>
      <expect>HhLifecycleRow TypeScript shape locked + FE-side bucketing logic prototyped before DS commits. Catches schema-mismatch class at design-time (see [[feedback-audits-underspecify-by-default]] meta-rule).</expect>
    </step>
  </phase>

  <phase id="2" when="DS edits — INF_D_04 + INF_D_08">
    <step>
      <run>Emit per-HH `hh_lifecycle` array in INF_D_04 alongside existing `views.aua` blocks; preserve rolling-window aggregates as legacy fields (back-compat during cutover). Add documentation comment citing this TO + brief.</run>
      <expect>Existing fields unchanged; new `hh_lifecycle` array added at top-level (or under existing `views.aua` block per schema-lock outcome).</expect>
    </step>
    <step>
      <run>Coordinate INF_D_08 edit timing with DS~C $156K investigation. DS~C is read-only on INF_D_08 currently; expected close ~15-20min post brief authoring. DS~D INF_D_04 edit can land in parallel (~3-4h ship); INF_D_08 edit (~1h) waits on DS~C $156K close to avoid concurrent-edit risk.</run>
      <expect>INF_D_04 + INF_D_08 ship sequentially OR INF_D_04 ships first + INF_D_08 ships post-DS~C-close.</expect>
      <if_mismatch>If DS~C $156K investigation surfaces structural concern about INF_D_08, surface to COO + revise INF_D_08 edit shape accordingly.</if_mismatch>
    </step>
    <step>
      <run>ds-commit-gate.sh + safe-deploy.sh per CLAUDE.md Rule 13 + 14. `from __future__ import annotations` first import per Rule 15.</run>
      <expect>Both gates PASS. Author identity --author="0.4.0_DS_ClientPlatform~D <0.4.0_DS_ClientPlatform~D@opal.agent>".</expect>
    </step>
  </phase>

  <phase id="3" when="DE consumes — Phase 2 of TO">
    <step>
      <run>DE 0.4 lane: TypeScript schema `HhLifecycleRow` in advisor-intelligence.ts; adapter pass-through; FE bucketing in view-mode toggle</run>
      <expect>FE filters per-HH array by inception date per view-mode period (calendar quarter/month/year). Donut.segments[nmnc] FE-side computed dynamically.</expect>
    </step>
    <step>
      <run>Component tests + cross-firm visual smoke (49F + Inflection)</run>
      <expect>Per-quarter NMNC AUA reflects real per-period acquisition; numbers do NOT overlap across adjacent quarters; current quarter shows the $20M (if §0 probe confirmed real); typical baseline ~$5M.</expect>
    </step>
  </phase>

  <phase id="4" when="after end-to-end ship">
    <step>
      <run>Andrew visual confirm on IWM NMNC current-quarter $20M + historical ~$5M baseline</run>
      <expect>Andrew empirical signal: model fixed; per-quarter inception NMNC AUA matches intuition.</expect>
    </step>
    <step>
      <run>Deprecate rolling-window legacy fields (cutover close)</run>
      <expect>Once FE fully on FE-bucketed model + Andrew empirical confirms, deprecate `views.aua.{period}.donut.segments[nmnc]` rolling-window field. Cutover close.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: §0 empirical probe COMPLETE + decision branching documented (a/b/c per Phase 0)
    AC2: HhLifecycleRow TypeScript schema locked between DS~D + DE 0.4 BEFORE DS commits
    AC3: INF_D_04 emits per-HH `hh_lifecycle` array; existing rolling-window fields preserved as back-compat
    AC4: INF_D_08 emits same per-HH array on firm + per-advisor side; existing aggregates preserved
    AC5: ds-commit-gate.sh + safe-deploy.sh PASS for both INF_D_04 + INF_D_08 edits
    AC6: `from __future__ import annotations` first import preserved per CLAUDE.md Rule 15
    AC7: FE consumption + view-mode dynamic bucketing shipped (DE 0.4 lane)
    AC8: Cross-firm visual smoke clean (49F + Inflection); per-quarter NMNC AUA reflects real per-period acquisition (no overlap signature)
    AC9: Andrew empirical confirm on IWM NMNC current-quarter $20M + ~$5M baseline (gate before legacy-field deprecation)
    AC10: Andrew 2026-05-06 binary invariant preserved (`nmnc + nmec = total_aua` across all view modes)
    AC11: Session logs + RAVC2 to COO + CC CTO + DE 0.4
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 (comp-pipescript io + comp-blast) before INF_D_04 edit. Phase 2 ds-commit-gate.sh + safe-deploy.sh per commit. Phase 3 DE-side TypeScript build + visual smoke.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: §0 empirical probe outcome (Phase 0 gates Phase 1). DS-DE schema-lock check-in (Phase 1 gates Phase 2). DS~C $156K investigation close (gates INF_D_08 edit ordering).
    PARALLEL-OK: INF_D_04 edit + DS~C $156K investigation (different scripts; no conflict). DE 0.4 schema design + DS~D §0 probe (independent prep).
    PORTAL SUBMODULE: DT 0.4 push post DE 0.4 ship.
    PHASE 1 INFINC INTERACTION: NONE. D-stage Pattern D (latest-state) orthogonal to skip-gate work `d88b7a7a4`.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Artifact regenerates with both old + new fields on next normal nightly chain run. FE switches when DE ships. No PROD chain re-fire needed.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. §0 empirical probe findings MCP to COO + DE + Andrew (Phase 0)
    2. INF_D_04 edit + commit + safe-deploy PASS (Phase 2)
    3. INF_D_08 edit + commit + safe-deploy PASS (Phase 2; gated on DS~C close)
    4. DE 0.4 FE schema + adapter + bucketing ship (Phase 3)
    5. Andrew empirical confirm (Phase 4)
    6. Legacy-field deprecation commit (Phase 4 cutover close)
    7. Session log + RAVC2 to COO + CC CTO + DE 0.4
  </deliverables>

  <ravc>DS~D RAVC2 to COO + CC CTO + DE 0.4 on AC1-11 PASS. Andrew empirical confirm gates legacy-field deprecation.</ravc>

  <notes>
    **Andrew direct framing:** "we want to know when clients came in, new HH IDs, so then the frontend can bucket them depending on view mode." Brief §3 Option A (FE buckets) is the canonical model.

    **Author identity:** `--author="0.4.0_DS_ClientPlatform~D <0.4.0_DS_ClientPlatform~D@opal.agent>"`.

    **PII discipline:** household IDs are numeric not PII-leaking; safe in emit. Verify `advisor_key` + `rep_id` carry no externally-identifying info per Inflection partner data agreement.

    **Banking opportunity:** if §0 probe surfaces an Orion dim refresh re-keying issue (HH_IDs treated as new because of upstream dim regen), worth banking as `feedback_orion_dim_refresh_rekey_class.md` — generalizes to silver-tier first_seen-style fields. Cross-link to [[feedback-audit-grain-consistency]] sister.

    **Coordination with DS~C $156K:** brief notes "Phase 1 INFINC interaction: none" — confirmed orthogonal to INFINC skip-gate work. ALSO confirmed orthogonal to DS~C investigation (different scripts; INF_C_00 + client_performance pipeline). INF_D_08 edit timing window coord required to avoid concurrent-edit risk.

    **Phase 1 scope:** this TO covers full end-to-end fix (DS emit + DE consume + Andrew confirm). Treat as multi-phase TO not multi-TO project — DS~D's "single tight scope, not multi-phase initiative" framing.
  </notes>
</task_order>
