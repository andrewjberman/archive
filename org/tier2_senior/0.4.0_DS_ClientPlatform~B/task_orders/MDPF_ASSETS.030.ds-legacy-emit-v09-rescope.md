<task_order>
  <metadata>
    <id>MDPF_ASSETS.030</id>
    <slug>ds-legacy-emit-v09-rescope</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-20 (authored on .028 RAVC-accept + CTO~B sequence directive)</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>SEQUENCED AFTER MDPF_ASSETS.029 per CTO~B's directive (.028 -> .029 -> .030). Gates on .029 -- the v0.9 backfill methodology + the historical series should be settled before the legacy emitter is re-scoped (the legacy non_model_assets.json the live page reads must be consistent with the v0.9 series). COO~B flips to pending + GO when .029 has resolved (at minimum its Phase-0 methodology proven; whether .030 GOs before or after .029's Phase-1 rewrite is a COO~B call at that point). NOTE: .030 moves a LIVE CEO-visible number -- see <live_page_note>; the GO decision includes confirming whether an Andrew sign-off is needed for the live-page move at that time.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P2 -- the v0.9 successor to the cancelled MDPF_ASSETS.026. Brings build_legacy_compat_emit.py (the SoT for non_model_assets.json -- the artifact the LIVE Model Portfolios page reads) to the PRD v0.9 full-Schwab-49F basis, so the live legacy page matches the v0.9 platinum aggregate.</priority>
    <sla>~2-3h DS wall -- a focused re-scope of one emitter script to a now-settled methodology + reconciliation + deploy.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/MDPF_ASSETS.md PRD v0.9 (8951ce8f0). 49F = full Schwab 49F book; 1b = Schwab_49F_whole - 1a - 1c (SMA-exclusive); aggregator/headline 3-term.</prd>
    <origin>CTO~B re-scope sequence 2026-05-20 (.028 -> .029 -> .030). .030 is the v0.9 successor to MDPF_ASSETS.026 -- .026 was the v0.8-era legacy-emit re-scope, superseded by Andrew Mandate Change 3 / PRD v0.9 and never shipped (.026 closed/superseded; this is a fresh TO on the v0.9 basis).</origin>
    <predecessor_026>MDPF_ASSETS.026 Phase-0 (DS~B, brief docs/briefs/mdpf-assets-026-phase0-legacy-emit-delta-20260520.md) quantified the v0.8-basis delta and established two findings still relevant: (1) the legacy emitter's non_model_aum is ALREADY SMA-inclusive at the source line -- no SMA-term to drop; (2) the dominant correction is Cohort 0 -- the live legacy enterprise_total currently INCLUDES etf_public_residual, which v0.9/.024-line ruling makes audit-only. .030 must re-confirm both against the v0.9 (not v0.8) basis before scoping the exact edit.</predecessor_026>
    <pipeline_rule>Rule 13 (DS commit + S3 deploy cycle for gold scripts). Rule 14 (ds-commit-gate). Rule 15 (`from __future__ import annotations`). Rule 17 (gold tier -- build_legacy_compat_emit.py is a gold script).</pipeline_rule>
  </references>

  <live_page_note>
    build_legacy_compat_emit.py emits non_model_assets.json -- the artifact the CURRENT live Model Portfolios page reads. Shipping .030 MOVES the live CEO-visible AUA number to the v0.9 basis. The v0.9 methodology itself is fully Andrew-ruled (PRD v0.9), so .030 is not a new methodology decision -- but moving a live CEO-facing number is done deliberately. At the .030 GO point COO~B confirms whether an explicit Andrew sign-off / timing call is warranted (it may be moot if WS-F Phase 3 is replacing the legacy page on a near horizon -- the same now-vs-WS-F question that surfaced under .026). COO~B resolves that at GO time.
  </live_page_note>

  <context>
    The live Model Portfolios page reads non_model_assets.json, emitted by build_legacy_compat_emit.py. With v0.9 live on the platinum aggregate (.028), the legacy emitter is now on a stale basis -- the live page shows pre-v0.9 numbers. .030 brings the legacy emitter to v0.9 so the live page matches the canonical aggregate.
  </context>

  <scope>
    <step>Phase 0 -- re-confirm against v0.9. Re-read build_legacy_compat_emit.py and confirm, on the PRD v0.9 basis (not v0.8), the exact edits: (1) 49F basis -> full Schwab 49F book (the .028 crosswalk source); (2) 1b = Schwab_49F_whole - 1a - 1c, SMA-exclusive, consistent with .028's WS-E; (3) Cohort 0 / etf_public_residual OUT of the headline enterprise_total (audit-only per v0.9). Quantify the exact live-page delta on a recent date. Brief the edit plan + delta to COO~B (CC CTO~B).</step>
    <step>Phase 1 -- apply the v0.9 re-scope to build_legacy_compat_emit.py: the 49F basis, the SMA-exclusive 1b, Cohort 0 audit-only; methodology_version=v0_9 stamped on the legacy artifact.</step>
    <step>Phase 2 -- reconciliation: the legacy non_model_assets.json totals reconcile to-the-cent against the .028 v0.9 platinum aggregate for the same date. Fixtures (if any) re-baselined to v0.9.</step>
    <step>Phase 3 -- Rule 13 deploy: ds-commit-gate.sh -> safe-commit.sh agent --author -> push CLOUD -> aws s3 cp -> deployed MATCH; trigger/await the legacy emit so non_model_assets.json refreshes to v0.9.</step>
    <step>Phase 4 -- RAVC2 to COO~B CC CTO~B: edit diff, the live-page delta, reconciliation vs the v0.9 platinum, deploy transcript.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">build_legacy_compat_emit.py emits on the v0.9 basis: 49F = full Schwab 49F book; 1b SMA-exclusive (Schwab_49F_whole - 1a - 1c); Cohort 0 / etf_public_residual OUT of the headline enterprise_total (audit-only).</ac>
    <ac id="AC2">Legacy non_model_assets.json reconciles TO-THE-CENT against the .028 v0.9 platinum aggregate for the same date.</ac>
    <ac id="AC3">methodology_version=v0_9 stamped on the legacy artifact.</ac>
    <ac id="AC4">Rule 13 deploy cycle (ds-commit-gate -> safe-commit -> push -> aws s3 cp -> MATCH). Rule 14/15. No emoji. Session log with Compiler Tools section. RAVC2 to COO~B CC CTO~B.</ac>
  </acceptance_criteria>

  <out_of_scope>
    The v0.9 platinum aggregate / WS-E (.028, already live). The aggregate_aua_timeseries.json historical backfill (.029 Phase 1 -- a DIFFERENT artifact; NOTE per amendment A1, .030 DOES own the non_model_assets.json historical backfill). WS-F portal Phase 3 (the legacy-page replacement -- separate workstream). Re-deciding the v0.9 methodology (Andrew-ruled). Materializing pre-2025-12-23 dates (gated on the .029 2024-depth probe + a separate Andrew decision).
  </out_of_scope>

  <deliverables>
    - build_legacy_compat_emit.py re-scoped to PRD v0.9; non_model_assets.json refreshed + reconciled vs the v0.9 platinum; Rule 13 deploy; RAVC2 to COO~B CC CTO~B.
  </deliverables>

  <amendment id="A1" date="2026-05-21" by="2.0.0_SA_COO~B" authority="CTO~B re-scope direction off the .029 Phase-0 brief e8d176d8f">
    SCOPE GROWN -- the .029 Phase-0 dry-run brief (e8d176d8f) CONFIRMED, as a firm finding, the scope_pending hypothesis: the Model Portfolios "Daily AUA Analysis" chart reads aum-timeseries.json + non_model_assets.json, and BOTH are build_legacy_compat_emit.py's output (the .030 script). aggregate_aua_timeseries.json (the .029 target) has NO portal consumer. So a daily-forward-only .030 would leave the chart's historical 1b layer stale. .030 therefore GROWS from "legacy-emit v0.9 daily-forward re-scope" to ALSO include the **historical non_model_assets.json time_series backfill**.

    ADDED SCOPE (Phase 5, after the Phase 0-4 daily-forward re-scope lands):
    - Phase 5 -- historical non_model_assets.json backfill: re-materialize the non_model_assets.json daily series onto the v0.9 basis across the same date range .029 covers (the 97 partitions 2025-12-23 ... 2026-05-19 + the v0.9-forward dates). build_legacy_compat_emit.py reads aggregate_aua/{date}.json as its 49F source -- so each historical date's non_model_assets.json is re-emitted off the .029-rewritten v0.9 aggregate_aua partition.

    HARD DEPENDENCY + SEQUENCING (per the brief's risk table): .030 Phase 5 reads .029's rewritten partitions -> Phase 5 GATES on MDPF_ASSETS.029 Phase 1 completing (all 97 v0.9 partition writes + the rollup rebuild + verification). .029 and .030 historical phases MUST NOT INTERLEAVE. .030 Phases 0-4 (daily-forward) MAY proceed independently of .029; Phase 5 waits.

    ADDED ACs:
    - AC5: the non_model_assets.json daily series is re-materialized v0.9 across the .029 date range; each historical date's non_model_assets.json reconciles against its .029-rewritten v0.9 aggregate_aua/{date}.json partition (same 49F source, no boundary skew).
    - AC6: the Model Portfolios "Daily AUA Analysis" chart's 1b layer (non_model_assets.json overlay) shows a consistent v0.9 historical trend with NO v0.8/v0.9 cliff at the boundary -- same no-cliff bar as .029's aggregate-series check.
    - AC7: non-destructive -- versioned bucket, overwrite-in-place, pre-write backup; no object deleted (same guardrail class as .029 Phase 1).

    .030 STAYS dispatch_held: Phases 0-4 GO when COO~B dispatches (after the .030 Phase-0 live-page-delta + the Andrew live-page-move check per <live_page_note>); Phase 5 additionally gates on .029 Phase 1 landing. The AC list above is now FINAL (supersedes the provisional <scope_pending>).
  </amendment>
</task_order>
