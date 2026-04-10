<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-advi-nna-canonical-source</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-10</date>
    <status>staged</status>
    <project_code>ad-hoc</project_code>
    <related_to>ADVI_REBORN (NNA reconciliation), ADVI_49PUSH (post-wave D_00c fee breakdown already shipped)</related_to>
  </metadata>

  <objective>
    Extend `build_timeseries_overview()` in `data/black_diamond/scripts/gold/D_04.client_portal_summary.py` to emit per-category NNA breakouts (`by_geo` + `by_adv`) nested inside every entry of `nna.{monthly|quarterly|annually}`. Top-9 + Other rule. Sum-invariant with the top-level firm totals. Canonical single-source-of-truth for the AdvisorIntelligence NNA numbers so Assets Overview (PartnerAnalytics) and Segment Analytics (DistributionTab Continuous NNA) structurally tie at every period × granularity × cohort.

    Closes Andrew's 2026-04-10 "NNA numbers don't tie" issue (concrete observation: Assets Overview Q2 2026 bar = $5.3M vs Segment Analytics Continuous GEO-NNA Q2 2026 tooltip = $10.3M at 3Y + Quarter + NNA). The frontend side is a companion RD task order (`rd-advi-nna-frontend-migration.md`) that can ship independently of this one via a fallback path.
  </objective>

  <context>
    **Authoritative brief:** `docs/briefs/ds-brief-advi-nna-canonical-source.md` — READ IN FULL before starting. This task order does not restate the technical detail from the brief; it wraps the brief with org protocol (compiler gate, cross-domain coordination, acceptance criteria delta, deploy sequence).

    **Root cause summary (from the brief):**
    - Path 1 (PartnerAnalytics): reads `platinum/firm/timeseries_overview.json.nna[granularity]`, pre-aggregated per-period.
    - Path 2 (DistributionTab Continuous NNA): reads `platinum/firm/cumulative_chart.json.nna_geo` / `nna_adv`, cumulative weekly-downsampled, with pairwise-diff computed in the frontend.
    - Drift sources: weekly-downsample snapping, canonical vs bronze lineage divergence, floating-point accumulation, period-boundary snapping differences. Any one of them is enough to produce the $5.3M vs $10.3M gap.
    - Frontend-only fixes (buffer extension, sum-of-bars hero, period-boundary swap) are all subsumed by this single-canonical-source approach. See brief Appendix A.

    **COO compiler-verified route map (2026-04-10 pre-TO runs, logged in org/compiler-tools-log.md):**
    - `comp-platinum reverse platinum/firm/timeseries_overview.json` — Producer: D_04 `build_timeseries_overview()`, fed by A_04, C_06, C_08, D_00, D_00b, D_00c, D_01, D_02, D_03. Served via `getTimeseriesOverview` → `/api/scoped/advisor-intelligence/platinum/firm/timeseries_overview.json` → S3-direct (`S3-opal-data-bd`) with edge auth via `shared-advisor-router`. Consumer today: `PartnerAnalytics` only.
    - `comp-pipescript io D_04` — **D_04 does NOT currently read `gold/canonical/nna/` directly.** D_00 and D_00b both read `CANONICAL_NNA_PREFIX` and pre-aggregate into `HEADER_METRICS` (D_00) and `TIMESERIES_CHART` (D_00b). D_04 reads the pre-aggregated outputs. The brief's §"Canonical source lineage" suggests reading `canonical_nna` directly from D_04 — this requires adding a new D_04 input (`CANONICAL_NNA_PREFIX`) if DS picks that path. DS has a second option: pre-aggregate the breakouts upstream in D_00 (or a new D_00d) and have D_04 consume the pre-aggregated per-period-per-category output. Either path is acceptable; pick whichever minimizes layering churn and document the rationale in the session log.
    - `comp-cache collisions` — no existing collision with the new `['advisor-intelligence', 'timeseries-overview', firmOverride]` key that RD will deduplicate against. Only intentional shared key today is `['firm-leaderboard', firmOverride]`. Clean.
    - `comp-transform fields PartnerAnalytics` — confirms consumer access pattern `timeseriesData?.nna?.[auaGranularity]`. The new `by_geo`/`by_adv` fields must nest inside each period entry so this access pattern extends naturally.

    **File size impact:** Each nna period entry expands from ~6 fields to ~26 fields (6 + 10 geo breakout keys × 3 + 10 adv breakout keys × 3, with rounding). Current file size ~50-100KB, projected ~250-500KB. Well within CloudFront/S3 limits; no infra change needed.

    **Shared serving path note:** `timeseries_overview.json` is served through `/api/scoped/advisor-intelligence/*.json` which is one of the paths that ADVI_PROFIL.004a will eventually scope for per-advisor access control. This is forward-compatible — adding fields does not change the scoping rule.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    - `comp-pipescript io D_04` — re-confirm current inputs/outputs. Read the full output; understand where `build_timeseries_overview()` already pulls its data from and pick the minimal-delta path for adding the breakouts.
    - `comp-pipescript io D_00` and `comp-pipescript io D_00b` — if you pick the "pre-aggregate upstream" path, confirm these are the right insertion points. Both already read `CANONICAL_NNA_PREFIX`.
    - `comp-blast D_04.client_portal_summary.py` — confirm no unexpected downstream consumers of `build_timeseries_overview()` output beyond `timeseries_overview.json` (note: comp-blast currently shows zero downstream edges because platinum/* keys are terminal in the graph — cross-check manually against PartnerAnalytics.tsx for the frontend consumer).
    - `comp-platinum reverse platinum/firm/timeseries_overview.json` — re-verify the single-consumer property holds (PartnerAnalytics only). The RD migration in `rd-advi-nna-frontend-migration.md` will add DistributionTab as a second consumer.
    - Read the current `build_timeseries_overview()` function in full before editing. Understand the existing `nna.{monthly|quarterly|annually}` builder loop so your new `by_geo`/`by_adv` insertion is minimally invasive.
    - Read `D_00b._nna_drill_data()` (around lines 759-777, per the DS brief) to understand the cumsum logic that feeds the OTHER path (cumulative_chart.json) — this is reference-only, you are not modifying D_00b.
    - Read `data/black_diamond/scripts/gold/lib/*` for any shared top-N helpers (`top_states`, `top_architects`). The brief acceptance criterion 3 requires byte-for-byte category key parity with `cumulative_chart.json.nna_geo.categories`, so reuse the same helper rather than re-deriving.

    Phase 2 (before committing):
    - `py_compile` on every modified Python file. Mandatory per memory `feedback_compile_before_upload.md`.
    - Run `build_timeseries_overview()` locally against the latest gold snapshot (or dev if available). Inspect 3-5 entries in `nna.quarterly`:
      - Verify `sum(by_geo[*].inflow) ≈ entry.inflow` within $0.01 (brief invariant #1)
      - Verify `sum(by_geo[*].outflow) ≈ entry.outflow` within $0.01 (brief invariant #2)
      - Verify `sum(by_geo[*].net) ≈ entry.net` within $0.01 (brief invariant #3)
      - Same for `by_adv`
      - Verify `by_geo` keys match `cumulative_chart.json.nna_geo.categories` byte-for-byte (brief invariant #5)
      - Verify `outflow` values are NEGATIVE (brief invariant #7)
    - **Pre-write sum-invariance assertion in the code itself.** Do not rely on the session-log spot check alone. Per the brief's "Invariants" section, add a hard assert in the builder that fails the run if any period violates invariants #1-4. This is load-bearing — silent partitioning drift defeats the entire point of the change.
    - Diff the old vs new `timeseries_overview.json` to confirm the top-level `period`/`label`/`end_date`/`inflow`/`outflow`/`net` fields are BYTE-FOR-BYTE unchanged (within rounding). Log the diff summary (entry count, top-level diff count = 0, new breakout field presence = 100%) in the session log.
    - Spot-check Q2 2026 specifically (Andrew's referenced period): the `by_geo` net values should sum to the top-level `net` value, and the top-level `net` value should remain what it is today (this task does NOT change top-level totals per scope constraint #1 of the brief).

    Phase 3 (after committing, before S3 upload):
    - `comp-pipescript io D_04` re-run — verify the new fields are picked up by the pipescript catalog. If you added a new input (e.g., `CANONICAL_NNA_PREFIX`), it should appear in the READS list.
    - `comp-pipescript consumers D_04` — confirm no downstream script silently depends on the old `nna.*` shape (this is an additive change; should be zero impact, but verify).
    - `comp-platinum reverse platinum/firm/timeseries_overview.json` re-run — should still show the same consumer (PartnerAnalytics), just with richer content.

    Log every tool run with result to `org/compiler-tools-log.md` using the standard `DATE | AGENT | TO | TOOL | COMMAND | RESULT | NOTE` format.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `platinum/firm/timeseries_overview.json` schema contract — DS extends the schema (this TO), RD consumes the extended schema (`rd-advi-nna-frontend-migration.md`). Schema becomes frozen at the `by_geo` + `by_adv` nested-object shape defined in the DS brief §"Schema". Any future change to the breakout shape requires a coordinated DS + RD pass.
    shared_resource: `data/black_diamond/scripts/gold/D_04.client_portal_summary.py` — DS owns. No other agent touches D_04 in this TO window.
    shared_resource: Top-N category selection helper (`top_states` / `top_architects`) — reuse the existing helper so `by_geo` keys match `cumulative_chart.json.nna_geo.categories` byte-for-byte (brief invariant #5). If no shared helper exists today, extract one and use it from both producers (D_00b `_nna_drill_data` + D_04 `build_timeseries_overview`).
    shared_resource: CANONICAL_NNA_PREFIX (`gold/canonical/nna/*.parquet`) — already read by D_00 and D_00b. If DS picks the "D_04 reads canonical_nna directly" path, D_04 becomes a third reader — document in the session log.
    last_write_owner: 0.4.0_DS_ClientPlatform for D_04 and any shared lib helpers.
    required_action: "DS ships this TO independently. No RD coordination needed at commit time — RD's companion TO (`rd-advi-nna-frontend-migration.md`) includes a fallback path that degrades gracefully until this TO's output lands in the next gold runner cycle. After this TO ships and the next bd-gold-layer-runner cycle writes the extended file, RD's frontend auto-activates the canonical path on the next React Query cache refresh."
  </cross_domain_coordination>

  <acceptance_criteria>
    All 5 criteria from the DS brief §"Acceptance criteria" apply verbatim. Wrapping them here with explicit sign-off language + COO-layer additions:

    1. **Q2 2026 parity (or equivalent current partial period).** `by_geo.*.net` summed across all geo keys equals the top-level `net` within $0.01 for the period Andrew is looking at. Same for `by_adv`. Same for `inflow` and `outflow`. Verified post-regeneration.

    2. **Sum invariance at every period and granularity — enforced by hard assert in the builder.** For every entry in `nna.{monthly|quarterly|annually}`, `sum(by_geo[*].inflow) == inflow` and same for `outflow` / `net`, same for `by_adv`. Pre-write assert must FAIL the pipeline run if any period violates. Silent partitioning drift is not acceptable.

    3. **Category key parity with `cumulative_chart.json`.** For each granularity, `by_geo` keys match `cumulative_chart.json.nna_geo.categories` byte-for-byte; same for `by_adv` vs `nna_adv.categories`. Prefer reusing the shared top-N helper. If none exists, add one and use from both call sites — also extract the key-parity check as a unit test or a post-build assertion.

    4. **No regression on existing top-level fields.** `period`, `label`, `end_date`, `inflow`, `outflow`, `net` fields in `nna.*` entries are byte-for-byte unchanged from pre-deploy values (within rounding). Diff the old and new `timeseries_overview.json` to verify. Log the diff summary in the session log.

    5. **Cross-panel tie-out (post RD frontend ship + next gold run).** After the companion RD TO ships and the next bd-gold-layer-runner cycle writes the extended `timeseries_overview.json`, Segment Analytics Continuous NNA Q2 2026 tooltip and Assets Overview Q2 2026 NNA bar show identical values at every window × granularity combination, for both GEO and ADV cohorts. This is the user-facing close condition Andrew described.

    **COO-layer additions:**

    6. **Compiler Tools section in the session log.** Every compiler tool run from §compiler_tools_mandate Phases 1-3, with command + result + one-line note, copied into the session log and appended to `org/compiler-tools-log.md`. Non-negotiable per feedback memory `feedback_coo_compiler_mandatory_before_task_orders.md` (the TO-authoring analog for agents).

    7. **DS deploy cycle end-to-end.** Per memory `feedback_ds_commits_ae_deploys.md`, DS owns the full cycle: commit with `--author=0.4.0_DS_ClientPlatform`, push to CLOUD, `aws s3 sync` or targeted `aws s3 cp` to `s3://opal-data-bd/code/gold/`, etag parity scan (local md5 == S3 etag), broker message to AE 0.6.0 announcing the staging. Do NOT trigger the gold runner directly — let the next scheduled cycle (or Andrew's manual trigger) pick it up.

    8. **Session log format.** `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-{NN}/advi_nna_canonical_source.md` with: brief compliance checklist, path decision rationale (direct canonical_nna read vs upstream pre-aggregation), compiler tools log, diff-before-ship output, 3-5-period spot check on Q2 2026 + other periods, commit SHA, S3 etag, and Next Steps naming AE 0.6.0 for runner pickup and 0.4.2_RD_AdvisorIntelligence for the companion frontend activation.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_04.client_portal_summary.py → `build_timeseries_overview()`</file>
      <file action="modify or create">data/black_diamond/scripts/gold/lib/* (shared top-N helper if one does not yet exist)</file>
      <file action="reference">data/black_diamond/scripts/gold/D_00b.portal_timeseries.py → `_nna_drill_data()` (lines ~759-777) — reference only, do NOT modify</file>
      <file action="reference">data/black_diamond/scripts/gold/D_00.portal_aggregates.py — reference only, inputs include CANONICAL_NNA_PREFIX if DS picks the "pre-aggregate upstream" path</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Read the DS brief (`docs/briefs/ds-brief-advi-nna-canonical-source.md`) in full before starting. The brief is authoritative on schema, invariants, scope constraints, and top-N rule.</requirement>
    <requirement id="2">Sum-invariance must be a HARD assert in the builder, not a session-log spot check. Fail the pipeline run on any period violation.</requirement>
    <requirement id="3">Top-level `nna.*` values must be byte-for-byte unchanged (within rounding). This TO is additive. If the existing top-level totals don't match the canonical partition sums, surface the discrepancy as a finding in the session log — do NOT silently re-derive.</requirement>
    <requirement id="4">`outflow` stored NEGATIVE per the top-level sign convention. Brief invariant #7. Non-negotiable.</requirement>
    <requirement id="5">Category keys byte-for-byte match `cumulative_chart.json.nna_geo.categories` / `nna_adv.categories`. If you can't reuse a shared helper, add one and call it from both producers.</requirement>
    <requirement id="6">Do NOT touch `build_cumulative_chart()`. Different function, still needed for the AUA continuous view. Brief scope constraint #3.</requirement>
    <requirement id="7">Do NOT add a new top-level JSON file. Extend `timeseries_overview.json` in place. Brief scope constraint #4.</requirement>
    <requirement id="8">Do NOT include city-level drill, per-client drill, or any deeper breakdown than state + architect aggregate. Brief scope constraint #5.</requirement>
    <requirement id="9">Do NOT compute `by_geo` / `by_adv` from the cumulative series via pairwise-diff. Always aggregate from daily flows in the canonical source. Brief scope constraint #7.</requirement>
    <requirement id="10">Follow the standard DS deploy protocol per CLAUDE.md + memory `feedback_ds_commits_ae_deploys.md`: commit → push CLOUD → S3 sync → etag parity scan → broker message to AE 0.6.0 for runner pickup. Do NOT trigger the gold runner directly.</requirement>
    <requirement id="11">`py_compile` is a mandatory gate before S3 upload per `feedback_compile_before_upload.md`. Do not skip.</requirement>
    <requirement id="12">Log every compiler tool run to `org/compiler-tools-log.md` using the standard format.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">D_04 modified + any shared-lib helper added, committed on CLOUD with `--author=0.4.0_DS_ClientPlatform`.</deliverable>
    <deliverable type="s3_upload">Modified scripts uploaded to `s3://opal-data-bd/code/gold/`. Etag parity verified.</deliverable>
    <deliverable type="document">Session log at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-{NN}/advi_nna_canonical_source.md` with path decision rationale, compiler tools log, diff-before-ship output, Q2 2026 spot check, commit SHA, S3 etag, and Next Steps.</deliverable>
    <deliverable type="message">Broker message to 0.6.0_AE_PartnerETL announcing the staging and requesting pickup on the next gold runner cycle. Broker message to 0.4.2_RD_AdvisorIntelligence (via Andrew per memory `feedback_no_direct_ds_messages.md` — Andrew relays) announcing schema is live once the first post-ship gold run completes.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT change top-level `nna.*` values. Additive only.</rule>
    <rule>Do NOT touch `build_cumulative_chart()` or `cumulative_chart.json`. Still needed for AUA + drilled NNA views.</rule>
    <rule>Do NOT compute breakouts via pairwise-diff on cumulative data. Daily-flow aggregation only.</rule>
    <rule>Do NOT add a new top-level JSON file. Extend in place.</rule>
    <rule>Do NOT include city-level or per-client drill data. Scope is state + architect aggregate only.</rule>
    <rule>Do NOT skip the pre-write sum-invariance assertion. It is load-bearing.</rule>
    <rule>Do NOT skip py_compile before S3 upload.</rule>
    <rule>Do NOT trigger the gold runner directly. Announce staging, let the next scheduled cycle pick it up.</rule>
    <rule>Do NOT send a direct broker message to RD announcing completion — per memory, Andrew routes to 0.4.2_RD.</rule>
  </do_not>
</task_order>
