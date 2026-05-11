<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.DAILY-AUDIT</id>
    <project>ADVI_INFETL</project>
    <title>Per-dim daily-pull audit matrix — trigger / script / filter / shape / output / gap</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <completed_date>2026-05-11</completed_date>
    <completed_note>SHIPPED 2026-05-07 commits f365b8c72 + 5be235f67. COO confirmed 2026-05-11.</completed_note>
    <priority>medium</priority>
    <estimated_effort>~0.5d audit + doc</estimated_effort>
  </metadata>

  <references>
    <ref type="parent_prd">docs/architecture/ADVI_INFETL.md (CTO PRD v0.1, 2026-05-07)</ref>
    <ref type="andrew_directive">2026-05-07 — "lambdas should be doing both daily incremental ingestion and silver conversion. then our gold runner ec2 needs to be event-based to trigger at the receipt of all daily silver data"</ref>
    <ref type="incident_root_cause">INFNNA.001 root cause was a hardcoded rep_id list that drifted from canonical. This audit produces the matrix that surfaces other dims with similar drift risk.</ref>
    <ref type="output_target">docs/architecture/INFETL_DAILY_PULLS_MATRIX.md (NEW)</ref>
  </references>

  <context>
    Andrew's directive: every Inflection dim must have a daily Lambda that does both
    bronze pull + silver convert, with a per-dim sentinel that aggregates into a gold
    trigger. Before authoring the LAMBDA-DIMS TO, we need an audit of the current state
    so the gap analysis is concrete.

    9 known dims: tax, performance, billing, transactions, accounts_v2, unified_account_dim,
    representatives, assets_v2, positions_daily. Some have daily Lambdas (txn v1.7.30),
    some are EC2-orchestrator-bound, some have no daily mechanism at all.
  </context>

  <scope>
    <step>
      For each of 9 dims, document in matrix format:
        | dim | trigger (cron/event/manual) | script (path) | filter (rep_ids set) | bronze output path | silver output path | known issues |
    </step>
    <step>
      Specifically capture:
        - tax: ORION_PULL_DATE env, current trigger?
        - performance: --snapshot-date, current trigger?
        - billing: ORION_PULL_DATE env, monthly cadence
        - transactions: inf-api-txn Lambda v1.7.30 T-1 default cron 13:00 UTC, --start-date/--end-date supported
        - accounts_v2: pull_inflection_new_portfolio.py, daily trigger?
        - unified_account_dim: BROKEN (see INFNNA.UAD-CREATOR), current cron status?
        - representatives: pull_inflection_representatives.py, daily trigger?
        - assets_v2: per-client-iter, daily trigger?
        - positions_daily: per-client-iter, daily trigger?
    </step>
    <step>
      Identify gap categories per dim:
        - Gap A: no daily trigger at all
        - Gap B: daily trigger but EC2-orchestrator-bound (slower than Lambda would be)
        - Gap C: daily trigger but missing rep_id filter or other shape mismatch
        - Gap D: daily trigger but silver builder unwired or partial
    </step>
    <step>
      For each silver builder, document the rep_id filter set used (and whether it's
      hardcoded vs derived from a shared constant). Flag inconsistencies.
    </step>
    <step>
      Output: docs/architecture/INFETL_DAILY_PULLS_MATRIX.md with the matrix, gap
      summary, and recommended Lambda-build priority order.
    </step>
    <step>
      Commit + push + RAVC with matrix path + gap counts.
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-routes trace inf-* — full path enumeration for any Lambda-bound dims</tool>
    <tool>comp-iam service inf-* — IAM coverage check</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Matrix doc landed with all 9 dims documented.</criterion>
    <criterion id="AC2">Gap categories assigned per dim.</criterion>
    <criterion id="AC3">rep_id filter audit completed across silver builders.</criterion>
    <criterion id="AC4">Recommended Lambda-build priority order documented.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None.</upstream>
    <downstream>INFETL.LAMBDA-DIMS uses this matrix to scope per-dim Lambda work.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~18:00Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Ships in parallel with rectify series. ~0.5d.</message>
  </go_signal>
</task_order>
