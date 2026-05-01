<task_order>
  <metadata>
    <id>ADVI_49FRECN.001C</id>
    <project>ADVI_49FRECN</project>
    <title>Phase 0 Slice C — AUA Gap Decomposition + Classification Drift Verification</title>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-01</issued_date>
    <status>open</status>
    <priority>P1 — parallel with .001A + .001B; feeds .001D consolidation</priority>
    <estimated_effort>0.5–1d</estimated_effort>
    <parallel_with>ADVI_49FRECN.001A (DS~A), ADVI_49FRECN.001B (DS~B)</parallel_with>
  </metadata>

  <context>
    49F partner data accuracy investigation v2. Quantified gaps: 3.59% AUA undershoot, 586 missing
    accounts. Drift from ADVI_AUAVAR 99.1% baseline (2026-03-09 — full $73.6M gap attributed; BKF
    fix shipped at the time).

    Parallelization map:
    - DS~A: Opal-side axis matrix (.001A)
    - DS~B: missing-account trace + 49F integration + consolidation (.001B + .001D)
    - **YOU (DS~C): AUA decomposition + classification drift** (this TO)

    Your strength here: you have the Geo + GRO market-component path lineage from INFGRD.005
    work (`10e5ce74b`). That gives you intuition for how artifacts get built up by classification
    bucket — the right lens for finding axis-level drift.
  </context>

  <objective>
    Decompose the 3.59% AUA gap into axis-level components and identify whether any of the gap
    is attributable to classification drift since the ADVI_AUAVAR / ADVI_CLSPT2 closeouts in
    March. Output: AUA decomposition table + classification audit findings.
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>Account-undercount × avg-AUA bound</title>
      <detail>
        Once DS~B has the matched-vs-missing account split (.001B AC #2), multiply the
        MISSING_FROM_OPAL count by the average Opal account AUA to bound the AUA contribution
        of the 586 missing accounts.

        - If that contribution >= 3.59% gap → essentially the whole AUA gap is explained by
          missing accounts; classification drift is minor.
        - If contribution < 3.59% gap → there's a residual AUA gap on MATCHED accounts to allocate.

        Document the bound and which case applies. (You may need to wait for DS~B's #2 output;
        coordinate via MCP. Until then, do AC #2-4 in parallel.)
      </detail>
    </ac>

    <ac id="2">
      <title>AUA breakdown by asset class</title>
      <detail>
        From Opal's gold artifacts, decompose the firm-level AUA by asset class:
        - Fixed Income
        - Equity
        - Alternatives
        - Cash
        - Other / Unclassified

        Use `bd_assets_dim` joined with `bd_securities` (per the recent ASSETCLASSc work
        `090d11f6` — bd_assets_dim join replaces the cost_per_unit ≤ 2.0 heuristic). Document
        the join logic.

        Compare against 49F's asset-class breakdown if Andrew shares it. If 49F doesn't share
        per-asset-class numbers, flag the gap and proceed to AC #3.
      </detail>
    </ac>

    <ac id="3">
      <title>Classification drift audit (ETFClassifier + post-CLSPT2)</title>
      <detail>
        ETFClassifier (ADVI_CLSPT2) closed 2026-03-25 with 3,855 securities classified.
        Verify it's still in place + check for drift since then:
        - Any new securities since 2026-03-25 that aren't classified? Run `comp-pipescript io 06b` (or whichever script consumes ETFClassifier) to see how many securities have classification = NULL or "Other".
        - Sample 20 of those — what should they be? Misclassification at the high-AUA tail
          can swing the per-class breakdown materially.
        - Compare against `bd_securities` table — any cases where bd_securities has a class
          but the runtime publisher is overriding it to "Other"?
      </detail>
    </ac>

    <ac id="4">
      <title>BKF (ADVI_AUAVAR) fix verification</title>
      <detail>
        ADVI_AUAVAR's $73.6M gap was attributed to a BKF (BlackRock fund family or similar — verify exactly which) issue, fixed at closeout 2026-03-09. Verify:
        - Read the ADVI_AUAVAR closing session log to identify the exact fix location.
        - Confirm the fix code path is still in place (not regressed by subsequent silver/gold rebuilds).
        - If still in place, document; if regressed, flag for Phase 1 immediate revert.
      </detail>
    </ac>

    <ac id="5">
      <title>Per-holding-type residual gap allocation</title>
      <detail>
        If after AC #1 there's residual gap on MATCHED accounts, allocate by holding type:
        - Mutual fund NAV
        - ETF NAV
        - Bond price
        - SMA holdings
        - Equity at exchange close
        - Cash at face value

        For each holding type, what fraction of total Opal AUA does it represent, and is there
        a hypothesis for why Opal undershoots 49F? (e.g., stale prices, settled-vs-trade-date,
        holdings count gap)
      </detail>
    </ac>

    <ac id="6">
      <title>Deliverable to shared report</title>
      <detail>
        Append your section to `docs/architecture/49F_RECONCILIATION_2026-05-01.md` under
        `## Slice C — AUA Decomposition + Classification Drift (DS~C)`.

        Include:
        - AC #1 bound result (which case applies)
        - AC #2 asset-class breakdown table
        - AC #3 classification drift findings (count of unclassified securities + sample)
        - AC #4 BKF fix verification verdict
        - AC #5 holding-type residual table
      </detail>
    </ac>
  </acceptance_criteria>

  <constraints>
    <constraint>Same as .001A/B: discovery only, 49F-only, compiler tools first, pre-commit on any Python helper.</constraint>
    <constraint>For AC #1 you may need DS~B's set-diff output — coordinate via MCP. Don't block on it; do the rest in parallel and circle back.</constraint>
  </constraints>

  <ravc_target>
    <to>0.4.0_DS_ClientPlatform~B (consolidation owner)</to>
    <on_complete>RAVC4 to DS~B with: commit ref, link to your section, summary of AUA-gap allocation. CC CTO.</on_complete>
  </ravc_target>
</task_order>
