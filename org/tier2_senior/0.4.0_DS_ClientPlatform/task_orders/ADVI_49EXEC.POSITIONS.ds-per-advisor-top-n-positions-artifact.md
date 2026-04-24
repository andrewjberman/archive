<task_order>
  <metadata>
    <id>ADVI_49EXEC.POSITIONS</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-24</date>
    <status>staged</status><!-- GO after ORPHRELID completes; gates TO 2 (LLM prose generator) authoring per CTO MCP 20260424 -->
    <project_code>ADVI_49EXEC</project_code>
    <priority>P1 — gates TO 2 generator Lambda authoring; biggest_position_gain/loss slot evaluators in shipped TO 1 reference this artifact</priority>
    <origin>
      CTO ruling MCP 20260424T13xxZ on ADVI_49EXEC.001+.005 close: "biggest_position_gain/loss slots require platinum/advisors/{id}/positions.json, which does not currently exist. Generator Lambda must not produce this artifact — that's DS lane. Before TO 2 is authored, queue a DS TO to produce positions.json from existing holdings_lots / D_04 gold artifacts (per-advisor top N positions with gain/loss delta vs prior period). Sequencing: positions.json DS TO → positions.json artifact in S3 → TO 2 can reference the contract."
    </origin>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_49EXEC.md (§3 slot triggers; biggest_position_gain + biggest_position_loss)</ref>
    <ref type="predecessor_to">ADVI_49EXEC.001 (complete 2026-04-24 commit 8cc69bab) — trigger_eval.py's biggest_position_gain/loss evaluators reference positions.json via evidence_keys</ref>
    <ref type="cto_ruling">CTO MCP 20260424T13xxZ — positions.json is DS lane, not generator Lambda (TO 2) scope</ref>
    <ref type="gold_source">data/black_diamond/scripts/gold/B_01.holdings_lots.py — per-account lot-level with cost_basis / market_value / gain_loss</ref>
    <ref type="gold_source">data/black_diamond/scripts/gold/D_02.advisor_client_detail.py — existing per-advisor aggregation pattern</ref>
    <ref type="gold_source">data/black_diamond/scripts/gold/D_04.client_portal_summary.py — existing platinum emit pattern (+ TO 5 prior_week rotation just shipped)</ref>
    <ref type="downstream_blocker">ADVI_49EXEC.002 (ds-llm-prose-generator) — cannot be authored until positions.json contract exists; gates Generator Lambda TF apply</ref>
  </references>

  <objective>
    Emit `platinum/advisors/{advisor_key}/positions.json` — per-advisor top-N positions artifact with current value + prior-period delta for LLM prompt consumption in generator Lambda (TO 2).

    Artifact consumed by `trigger_eval.evaluate_biggest_position_gain` + `evaluate_biggest_position_loss` in `data/black_diamond/scripts/exec_summary/trigger_eval.py` (shipped TO 1). detail_context from those evaluators becomes the LLM prompt input in TO 2.

    **EXPLICIT SCOPE LOCK:**
    - NO new gold-layer scripts — derive from existing holdings_lots + D-tier artifacts
    - NO generator-Lambda work (TO 2 scope)
    - NO lot-level granularity in output — positions aggregated to (advisor, ticker) grain
    - NO backfill (forward-emit only; rotation for prior-period snapshots handled via copy-on-write pattern similar to TO 5 leaderboard rotation)
    - Top-N count + "prior period" semantics: Phase 0 decides + documents. Default recommendation: N=10, prior_period=weekly (matches TO 5 leaderboard rotation cadence for semantic consistency).
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_04.client_portal_summary.py — add per-advisor positions.json emit block (or D_02 if better fit; Phase 0 picks)</file>
      <file action="modify">data/black_diamond/scripts/gold/lib/s3_layout.py — register new artifact key `platinum/advisors/{advisor_key}/positions.json` + `platinum/advisors/{advisor_key}/positions.prior_week.json`</file>
      <file action="modify">data/black_diamond/scripts/gold/gold_validate_config.yaml — add validator block (field-presence + top-N count cap + non-zero gain_loss)</file>
      <file action="read-only">data/black_diamond/scripts/gold/B_01.holdings_lots.py — source of per-lot cost_basis / market_value</file>
      <file action="read-only">data/black_diamond/scripts/exec_summary/trigger_eval.py — consumer; confirm evidence_keys align with emit shape</file>
    </files>
  </scope>

  <wire_contract>
    **Output shape `platinum/advisors/{advisor_key}/positions.json`:**
    ```
    {
      "advisor_key": "dan_sinnen",
      "snapshot_date": "2026-04-20",
      "prior_period": "weekly",
      "prior_snapshot_date": "2026-04-13",
      "top_n": 10,
      "positions": [
        {
          "rank": 1,
          "ticker": "AAPL",
          "asset_class": "stock",
          "current_mv": 12345678.90,
          "current_cost_basis": 10000000.00,
          "current_gain_loss_abs": 2345678.90,
          "current_gain_loss_pct": 23.46,
          "prior_mv": 11800000.00,
          "prior_gain_loss_abs": 1800000.00,
          "delta_mv": 545678.90,
          "delta_gain_loss_abs": 545678.90
        },
        ...
      ]
    }
    ```

    **Ranking criteria:** top N by `current_mv` (magnitude of position), descending. Phase 0 confirms or proposes alternative (e.g., top N by gain_loss_abs magnitude for trigger relevance).

    **Rotation:** prior_week snapshot via copy-on-write pattern like TO 5 (s3.copy_object src=positions.json dst=positions.prior_week.json BEFORE emit). NoSuchKey on first run handled gracefully as WARN.

    **Scope:** one file per advisor with non-zero AUA. Skip advisors with empty holdings (document count).
  </wire_contract>

  <deliverables>
    <deliverable id="phase-0-spec">
      Phase 0 session log documents: N count (default 10), prior_period cadence (default weekly matching TO 5), ranking criteria (default current_mv magnitude), grain decision (advisor_key from D_02 pattern), exclusion rule for empty-holdings advisors.
    </deliverable>
    <deliverable id="emit-block">
      D_04 (or D_02 per Phase 0) writes `platinum/advisors/{advisor_key}/positions.json` for each advisor with non-zero AUA; prior_week rotation via copy-on-write.
    </deliverable>
    <deliverable id="coverage-metric">
      Post-run: advisor count emitted + skipped (empty holdings) — log + session evidence. Expected ~45 advisors for BD firm (49F).
    </deliverable>
    <deliverable id="validator-block">
      gold_validate_config.yaml block: field-presence (advisor_key, snapshot_date, top_n, positions[]) + top-N cap (len(positions) <= N) + at least 1 position per emitted advisor + ticker non-null for all positions.
    </deliverable>
    <deliverable id="trigger-eval-consistency-check">
      Spot-check: run `evaluate_biggest_position_gain` from TO 1 trigger_eval.py against 3 sample advisors post-emit. Confirm TriggeredSlot returns populated detail_context with positions.json evidence_keys populated.
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">Phase 0 spec documents N + prior_period + ranking criteria + grain; any deviation from defaults includes rationale.</ac>
    <ac id="2">positions.json + positions.prior_week.json emit for all advisors with non-zero AUA; advisor count matches expected (~45 for 49F; ~9 for INFLEC if this script also runs on INF — Phase 0 addresses cross-firm scope).</ac>
    <ac id="3">Wire contract adhered: all 14 fields per position emitted (rank, ticker, asset_class, current_mv, current_cost_basis, current_gain_loss_abs, current_gain_loss_pct, prior_mv, prior_gain_loss_abs, delta_mv, delta_gain_loss_abs) + top-level metadata (advisor_key, snapshot_date, prior_period, prior_snapshot_date, top_n, positions[]).</ac>
    <ac id="4">Validator block added to gold_validate_config.yaml; `comp-validate D_04 --artifact /tmp/positions_sample.json` exits 0.</ac>
    <ac id="5">trigger_eval spot-check: 3 sample advisors return populated TriggeredSlot from evaluate_biggest_position_gain/loss when threshold met ($100k abs + 5% pct per TO 1 slot definitions).</ac>
    <ac id="6">No regression on existing D_04 outputs — `comp-blast D_04.client_portal_summary` post-change shows same consumer set; existing TO 5 leaderboard rotation still works.</ac>
    <ac id="7">py_compile + ds-commit-gate.sh exit 0 pre-commit per CLAUDE.md Rule 14.</ac>
    <ac id="8">`comp-pipescript deployed D_04` MATCH post-S3-upload.</ac>
    <ac id="9">Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail vs `<expect>`.</ac>
    <ac id="10">MCP COMPLETE to COO + CTO with: commit hash, advisor count emitted, spot-check outcome, contract confirmed for TO 2 authoring unblock.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="0" when="discovery">
      <step>
        <run>comp-pipescript io D_04.client_portal_summary</run>
        <expect>D_04 READS include silver/allocations + gold/timeseries/holdings_lots (or identify if new read needed). WRITES surface platinum/firm/* + platinum/advisors/* existing artifacts.</expect>
        <if_mismatch>If D_04 doesn't read holdings_lots, consider D_02 as the emit host instead — Phase 0 picks.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io D_02.advisor_client_detail</run>
        <expect>Per-advisor aggregation pattern surfaced for reference.</expect>
        <if_mismatch>If no per-advisor aggregation exists in D_02, derive from B_01 with groupby; document approach.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse platinum/advisors/*/positions.json</run>
        <expect>0 portal consumers (new artifact; portal-side consumption future DE TO).</expect>
        <if_mismatch>If a consumer surfaces, that key already exists upstream — rename or coordinate.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="before write">
      <step>
        <run>comp-blast D_04 (or D_02 if picked)</run>
        <expect>Current consumers enumerated; confirm positions.json emit doesn't break existing downstream.</expect>
        <if_mismatch>Investigate + coordinate before writing.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "import json; ev = json.load(open('data/black_diamond/scripts/exec_summary/trigger_eval.py'))" # placeholder — actual Phase 1: read trigger_eval.py and list evidence_keys on biggest_position_gain/loss</run>
        <expect>evidence_keys reference positions.json path; confirm path matches wire_contract output.</expect>
        <if_mismatch>If evidence_keys expect different shape/path, align wire_contract to match TO 1 (trigger_eval is already shipped; no churn there).</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_04.client_portal_summary.py data/black_diamond/scripts/gold/lib/s3_layout.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh data/black_diamond/scripts/gold/D_04.client_portal_summary.py data/black_diamond/scripts/gold/lib/s3_layout.py data/black_diamond/scripts/gold/gold_validate_config.yaml</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix AST/undefined-name issues.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-pipescript deployed D_04</run>
        <expect>MATCH.</expect>
        <if_mismatch>Re-upload.</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_04 --artifact /tmp/positions_sample.json</run>
        <expect>Exit 0; positions.json validator block passes.</expect>
        <if_mismatch>Iterate validator or fix emit shape until exit 0.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-bd/platinum/advisors/ --recursive | grep positions.json | head -5</run>
        <expect>Populated post-chain-run; ~45 advisor positions.json files for BD firm.</expect>
        <if_mismatch>Chain didn't write positions.json; inspect dispatch log.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "from data.black_diamond.scripts.exec_summary.trigger_eval import evaluate_biggest_position_gain; # stub per TO 1 wire contract; run on sample advisor + platinum_reads pulling fresh positions.json"</run>
        <expect>TriggeredSlot returned (or None for advisors below threshold) with populated detail_context; evidence_keys point to valid S3 paths.</expect>
        <if_mismatch>Wire contract mismatch; reconcile with trigger_eval.py (do NOT modify trigger_eval — modify positions.json shape).</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource file="data/black_diamond/scripts/gold/D_04.client_portal_summary.py">
      Recent active: CP-WP5 (2026-04-22 close), COHORT-A (2026-04-22 close), TO 5 prior-week rotation (2026-04-24 complete), TOPPOSOPAL (staged). Positions emit is additive; low collision risk but coordinate with TOPPOSOPAL if both land same commit cycle.
    </shared_resource>
    <shared_resource file="data/black_diamond/scripts/exec_summary/trigger_eval.py">
      Read-only reference here. DO NOT modify — already shipped in TO 1 (commit 8cc69bab). This TO aligns positions.json shape to trigger_eval's evidence_keys, not the other way around.
    </shared_resource>
    <downstream_pending>Generator Lambda (ADVI_49EXEC.002) — authoring unblocked by this TO's completion. DT TO 4 (generator Lambda Terraform apply + tag) gates on TO 2 close.</downstream_pending>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT modify trigger_eval.py (shipped in TO 1). Align positions.json shape TO the consumer's expectations.</rule>
    <rule>Do NOT emit lot-level granularity. Advisor × ticker aggregation only.</rule>
    <rule>Do NOT retroactively backfill historical positions.prior_week.json partitions.</rule>
    <rule>Do NOT author generator Lambda code in this TO — TO 2 scope.</rule>
    <rule>Do NOT widen scope to non-49F firms unless Phase 0 explicitly confirms cross-firm emit is in-scope (default: BD 49F firm only).</rule>
  </do_not>
</task_order>
