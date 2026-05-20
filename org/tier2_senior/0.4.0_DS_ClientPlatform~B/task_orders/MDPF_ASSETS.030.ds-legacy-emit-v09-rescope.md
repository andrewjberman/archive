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
    The v0.9 platinum aggregate / WS-E (.028, already live). The historical backfill (.029). WS-F portal Phase 3 (the legacy-page replacement -- separate workstream). Re-deciding the v0.9 methodology (Andrew-ruled).
  </out_of_scope>

  <deliverables>
    - build_legacy_compat_emit.py re-scoped to PRD v0.9; non_model_assets.json refreshed + reconciled vs the v0.9 platinum; Rule 13 deploy; RAVC2 to COO~B CC CTO~B.
  </deliverables>

  <scope_pending date="2026-05-20" by="2.0.0_SA_COO~B">
    AC LIST PROVISIONAL -- DO NOT GO ON THE CURRENT SCOPE. Per CTO~B's .029/.030-boundary directive (Andrew reinforced: the v0.9 backfill must reach the WHOLE Model Portfolios "Daily AUA Analysis" chart, not just the aggregate series): the chart consumes TWO daily-series artifacts -- aum-timeseries.json (model layers 1a/2a/1c) AND non_model_assets.json (the 1b Schwab-residual overlay, build_legacy_compat_emit.py's output). .029 backfills aggregate_aua_timeseries; .030 as currently scoped is daily-FORWARD only -- which would leave the chart's 1b layer historically stale. .030 likely needs to GROW from "legacy-emit v0.9 re-scope (daily-forward)" to "legacy-emit v0.9 re-scope + historical non_model_assets.json time_series backfill," co-sequenced with .029 Phase 1 so both artifacts' historical series land on the SAME v0.9 basis with no boundary skew. COO~B holds .030's final AC list until DS~B's .029 Phase-0 dry-run brief lands (the brief traces backward from the chart + enumerates every artifact + the partition-write plan); CTO~B relays the .030 re-scope direction off that brief. .030 stays dispatch_held meanwhile.
  </scope_pending>
</task_order>
