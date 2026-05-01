<task_order>
  <metadata>
    <id>ADVI_49FRECN.001A</id>
    <project>ADVI_49FRECN</project>
    <title>Phase 0 Slice A — Opal-Side Reference Snapshot + Per-Axis Matrix Shell</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-01</issued_date>
    <status>open</status>
    <priority>P1 — parallel-runs with .001B + .001C; feeds into .001D consolidation</priority>
    <estimated_effort>0.5–1d</estimated_effort>
    <parallel_with>ADVI_49FRECN.001B (DS~B), ADVI_49FRECN.001C (DS~C)</parallel_with>
  </metadata>

  <context>
    49F partner data accuracy investigation v2. Andrew's quantified gaps:
    - AUA: Opal portal 3.59% LOW vs 49F's actual reported number
    - Accounts: Opal ~6025 vs 49F's 6611 (586 missing, 8.86% undercount)

    Drift from ADVI_AUAVAR 99.1% accuracy baseline (closed 2026-03-09).

    This work is parallelized across THREE DS lanes (per Andrew directive — fast turnaround, multi-angle attack):
    - **YOU (DS~A): structural Opal-side extraction + axis matrix shell** (this TO)
    - DS~B: missing-account bronze→silver→gold trace + 49F-side data integration (.001B)
    - DS~C: AUA decomposition + classification drift verification (.001C)
    - DS~B then consolidates all three into final report (.001D)
  </context>

  <objective>
    Produce the structural backbone of the reconciliation: Opal-side reference numbers
    at a chosen reference date, broken out across all reconcilable axes (per-advisor,
    per-account-type, per-custodian if available). DS~B and DS~C will append to this
    backbone with their angle-specific findings.
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>Pick reference date + extract Opal-side firm-level totals</title>
      <detail>
        Choose the most recent gold artifact date that has clean, complete data (likely 2026-04-30 or
        most recent nightly). Document the date choice. Extract:
        - Total AUA (firm-level, from `gold/d_00/...`)
        - Total account count (distinct account-id from underlying gold artifacts; cite the script)
        - Per-advisor breakdown (from `gold/d_00b/...` or equivalent)

        Use `comp-pipescript io <script>` BEFORE reading any gold script — confirms exact column availability.
      </detail>
    </ac>

    <ac id="2">
      <title>Per-account-type breakdown</title>
      <detail>
        Pull account count + AUA grouped by account_type (taxable / IRA / Roth / 401k / SMA / etc.).
        Source artifact likely `bd_accounts_dim` joined with the canonical positions. Document the
        artifact path and the join logic.

        If the source data has account_type bucketing inconsistent with how 49F categorizes,
        flag it explicitly so DS~B can request the matching 49F categorization.
      </detail>
    </ac>

    <ac id="3">
      <title>Per-custodian breakdown (best-effort)</title>
      <detail>
        Pull per-custodian count + AUA. If we have a `custodian` field anywhere in the bronze/silver/gold
        layer, use it. If the field is absent or sparse, document what we DO have and what's missing
        (DS~B will use this to request supplementary data from 49F-side).

        Common Opal custodian hints: Schwab, Fidelity, TD, Pershing — but verify which appear in
        actual data, not memory.
      </detail>
    </ac>

    <ac id="4">
      <title>Matrix shell — markdown tables ready for 49F-side numbers</title>
      <detail>
        Emit three markdown tables with these columns: dimension value | Opal count | Opal AUA |
        49F count [BLANK — DS~B fills] | 49F AUA [BLANK] | account delta | AUA delta $/% | gap classification.

        Tables: per-advisor, per-account-type, per-custodian. Sorted by Opal AUA desc.
        Leave the 49F columns + delta + classification blank — they get filled when DS~B
        integrates 49F-side data in .001B.
      </detail>
    </ac>

    <ac id="5">
      <title>Account-id list extraction</title>
      <detail>
        Produce a flat list of all distinct account-ids in Opal at the reference date.
        Save as parquet or CSV at `tmp/49frecn/opal_accounts_2026-MM-DD.parquet` (or matching name).
        DS~B uses this to set-diff against 49F's list during .001B.
      </detail>
    </ac>

    <ac id="6">
      <title>Deliverable to shared report stub</title>
      <detail>
        Append your section to `docs/architecture/49F_RECONCILIATION_2026-05-01.md` under
        a `## Slice A — Opal-Side Reference Snapshot (DS~A)` heading. Include:
        - Reference date used + rationale
        - All 3 matrix tables with Opal-side columns filled
        - Account-id list path
        - Caveats / data gaps / fields we don't have

        First DS to commit this file creates it. Subsequent DSes append. No git conflicts because
        each section is bounded by H2 headers.
      </detail>
    </ac>
  </acceptance_criteria>

  <constraints>
    <constraint>Discovery only — read-only S3 + parquet inspection. NO code edits, NO pipeline reruns.</constraint>
    <constraint>49F-only scope (s3://opal-data-bd/). Do NOT cross-investigate into Inflection.</constraint>
    <constraint>Compiler tools first: `comp-pipescript io <script>` before reading any gold script.</constraint>
    <constraint>If you author any Python helper for data extraction, run pre-commit gate per CLAUDE.md Rule 14.</constraint>
    <constraint>Coordinate with DS~B + DS~C via MCP if your axis discoveries change scope assumptions for theirs.</constraint>
  </constraints>

  <ravc_target>
    <to>0.4.0_DS_ClientPlatform~B (consolidation owner)</to>
    <on_complete>RAVC4 to DS~B with: commit ref, parquet/CSV path of Opal account-id list, link to your section in the shared report. CC CTO.</on_complete>
  </ravc_target>
</task_order>
