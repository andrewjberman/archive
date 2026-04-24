<task_order>
  <metadata>
    <id>ADVI_49EXEC.POSITIONS</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-24</date>
    <status>staged</status><!-- Rewritten 2026-04-24 post CTO PRD amendment 5059cdf0. Gate met: 49EXEC TO 1+5 complete (8cc69bab) + ORPHRELID complete (a8cf3c83/e28e0f5d/a0a57005). Draft offered to CTO for pre-dispatch review per their MCP 20260424T160xxxZ offer. Pending: CTO OK → flip to pending + GO dispatch. -->
    <project_code>ADVI_49EXEC</project_code>
    <priority>P1 — single unblock on TO 2 (LLM prose generator) authoring; downstream-gates TO 4 (DT generator Lambda TF apply + tag) and TO 7 (DT EventBridge wiring)</priority>
    <origin>
      ADVI_49EXEC PRD amendment 2026-04-24 `5059cdf0` authored by 1.0.0_SA_CTO after COO pre-TO compiler study (`comp-platinum reverse 'platinum/advisors/*/positions.json'` + `aws s3 ls platinum/advisors/aj_lenartowicz/`) surfaced the artifact as net-new rather than existing. Original PRD §4.1 step 3 wrongly labeled "existing"; §4.5 new section is the correct spec. TO POSITIONS block at §7 is CTO's canonical scope per locked TO mandate format.
    </origin>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_49EXEC.md §4.5 (schema contract) + §7 TO POSITIONS block (compiler mandate + AC) + §8 AC1 addition + §9 compiler log rows</ref>
    <ref type="prd_amendment_commit">5059cdf0 — CTO PRD amendment 2026-04-24 authoring TO POSITIONS scope</ref>
    <ref type="predecessor_to">ADVI_49EXEC.001 ds-template-library-and-trigger-eval (complete 2026-04-24 commit 8cc69bab) — TO 1 ships `trigger_eval.py` with biggest_position_gain/biggest_position_loss/concentration_risk/tax_loss_candidate slot evaluators that reference positions.json</ref>
    <ref type="producer">data/black_diamond/scripts/gold/D_04.client_portal_summary.py — single-writer extension; existing producer of summary/timeseries/mix/nna_clients siblings</ref>
    <ref type="upstream_gold_already_loaded_by_d04">HOLDINGS_LOTS_PREFIX (gold/timeseries/holdings_lots/ ← B_01) + ACCOUNT_TEAM (gold/views/account_team.parquet ← C_07) + ACCOUNTS_DIMENSION (gold/dimensions/accounts_dimension_latest.parquet ← A_00) — verified via `comp-pipescript io D_04` 2026-04-24</ref>
    <ref type="validator_config">data/black_diamond/scripts/gold/gold_validate_config.yaml — add `D_04_positions_output` entry (additive, no existing entry changes)</ref>
    <ref type="downstream_blocker">ADVI_49EXEC.002 ds-llm-prose-generator — HOLD until this TO ships the artifact contract to S3</ref>
  </references>

  <objective>
    Extend `D_04.client_portal_summary.py` to emit a fifth platinum artifact per active advisor: `platinum/advisors/{advisor_id}/positions.json`. Flat top-N=25 positions (ticker, security_name, asset_class, market_value, cost_basis, unrealized_gain, unrealized_gain_pct, pct_of_advisor_aum, account_count, lot_count, first_acquisition_date, last_acquisition_date, oldest_lot_holding_days) sorted by `market_value` descending. Artifact consumed by generator Lambda (TO 2) for slot-trigger evaluation (top_gainer / top_loser / concentration_risk / tax_loss_candidate).

    **EXPLICIT SCOPE LOCK (per CTO PRD §4.5 + §7):**
    - **PRODUCER:** extend D_04 — HARDCODED fifth write mirroring existing summary/timeseries/mix/nna_clients emit pattern. No new producer script. No new D-tier. No D_02 alternative.
    - **UPSTREAM:** no new READS. D_04 already loads HOLDINGS_LOTS_PREFIX + ACCOUNT_TEAM + ACCOUNTS_DIMENSION per 2026-04-24 `comp-pipescript io D_04` verified. Phase 0 check re-verifies.
    - **SHAPE:** flat top-N=25 per §4.5. NO pre-sliced gainers/losers/concentrations buckets (TO 2 filters in Python at prompt time).
    - **NO PRIOR-PERIOD / ROTATION** — current snapshot only. Generator does period-delta at prompt construction.
    - **NO BACKFILL** — forward-emit only; artifact populates from first nightly post-ship.
    - **NO new S3 prefix** — slots into existing `platinum/advisors/{advisor_id}/`.
    - **NO new Lambda / Terraform** — pure D_04 Python extension + gold_validate_config.yaml add.
    - **NO CROSS-FIRM** — BD firm scope only for 49F active advisors; INFLEC advisors out of scope this TO (INFLEC has separate gold chain under data/orion/; future RD if needed).
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_04.client_portal_summary.py — add positions-emit block adjacent to existing summary/timeseries/mix/nna_clients HARDCODED pattern</file>
      <file action="modify">data/black_diamond/scripts/gold/gold_validate_config.yaml — add `D_04_positions_output` entry (required-fields, schema-type checks, positions count ≤ top_n_limit)</file>
      <file action="read-only">data/black_diamond/scripts/gold/D_04.client_portal_summary.py — existing summary.json emit block at ~L717 and nna_clients.json at ~L2674 (pattern reference)</file>
      <file action="read-only">docs/architecture/ADVI_49EXEC.md §4.5 — schema contract (JSON example + field rationale)</file>
      <file action="read-only">data/black_diamond/scripts/gold/B_01.holdings_lots.py — source of per-lot cost_basis + market_value (already loaded by D_04; no modification)</file>
    </files>
  </scope>

  <wire_contract>
    **Output shape `platinum/advisors/{advisor_id}/positions.json` (per PRD §4.5):**
    ```json
    {
      "advisor_id": "aj_lenartowicz",
      "firm_id": "49financial",
      "as_of_date": "2026-04-24",
      "total_aum": 47500000.00,
      "positions_count": 142,
      "top_n_limit": 25,
      "positions": [
        {
          "ticker": "NVDA",
          "security_name": "NVIDIA Corporation",
          "asset_class": "equity",
          "market_value": 1250000.00,
          "cost_basis": 740000.00,
          "unrealized_gain": 510000.00,
          "unrealized_gain_pct": 0.6892,
          "pct_of_advisor_aum": 0.0263,
          "account_count": 12,
          "lot_count": 18,
          "first_acquisition_date": "2022-11-18",
          "last_acquisition_date": "2024-03-04",
          "oldest_lot_holding_days": 1254
        }
      ]
    }
    ```

    **Aggregation grain:** `(advisor_id, ticker)`. Aggregate across accounts held by the advisor per ACCOUNT_TEAM mapping. `account_count` = distinct account_ids holding the position; `lot_count` = count of open lots across those accounts.

    **Sort + cap:** `market_value` descending. First N=25 of sorted positions; `positions_count` reports the full count pre-cap (for generator sizing context).

    **Field semantics:**
    - `market_value` = sum of lot-level market_value (current snapshot).
    - `cost_basis` = sum of lot-level cost_basis.
    - `unrealized_gain` = market_value − cost_basis.
    - `unrealized_gain_pct` = unrealized_gain / cost_basis (float; display-formatting is consumer concern).
    - `pct_of_advisor_aum` = market_value / total_aum (float).
    - `first_acquisition_date` = earliest `acquisition_date` across lots.
    - `last_acquisition_date` = latest `acquisition_date` across lots.
    - `oldest_lot_holding_days` = `as_of_date` − `first_acquisition_date` in whole days.

    **as_of_date:** matches D_04 run date (same date used by summary/timeseries/mix/nna_clients).

    **firm_id:** "49financial" for current BD scope. Pulled from ACCOUNTS_DIMENSION firm mapping.

    **Advisors emitted:** one `positions.json` per active advisor with non-zero holdings (same emit set as `summary.json`). Inactive advisors + advisors with zero holdings: skip (no file).

    **PII stance:** ticker + security_name are public market data, not PII. Zero cleartext client names / account numbers / client pseudonyms in artifact by construction (position-level grain, not client-level).
  </wire_contract>

  <deliverables>
    <deliverable id="d04-positions-emit-block">
      D_04 emits positions.json per active advisor matching §4.5 schema exactly. Uses existing HOLDINGS_LOTS + ACCOUNT_TEAM + ACCOUNTS_DIMENSION reads (no new loads). Emit pattern mirrors existing `items.append((payload, f'platinum/advisors/{aid}/*.json'))` at L717/L724/L728/L2674.
    </deliverable>
    <deliverable id="validator-config-entry">
      `gold_validate_config.yaml` new `D_04_positions_output` entry: required top-level fields (advisor_id, firm_id, as_of_date, total_aum, positions_count, top_n_limit, positions) + required per-position fields (14 listed in §4.5) + schema-type checks + positions count ≤ top_n_limit + positions count ≥ 1 (emitted advisors have at least one position by construction).
    </deliverable>
    <deliverable id="session-log-compiler-section">
      Session log `Compiler Tools` section reproduces every `<run>` from the mandate triad + observed output + pass/fail vs `<expect>`. Append 4+ rows to `org/compiler-tools-log.md` via auto-context.
    </deliverable>
    <deliverable id="mcp-complete-to-coo-cto">
      RAVC4 bundle to me + CTO: commit SHA + S3 MATCH confirmation + advisor count emitted + spot-check reconciliation result (3 advisors, top/median/tail AUM) + contract confirmed ready for TO 2 authoring unblock.
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">D_04 emits positions.json for every active advisor post-nightly; count mirrors existing summary.json emit count per run.</ac>
    <ac id="2">Schema matches §4.5 spec EXACTLY — field names + types + sort order (market_value desc) + top-level metadata (advisor_id, firm_id, as_of_date, total_aum, positions_count, top_n_limit, positions[]).</ac>
    <ac id="3">Validator exit 0 on all emitted advisors in the nightly run; `comp-validate D_04 --artifact /tmp/positions_sample.json` passes.</ac>
    <ac id="4">Spot-check 3 advisors (one top-AUM, one median-AUM, one tail-AUM): sum(positions[].market_value) across top-25 ≤ total_aum; unrealized_gain reconciles with holdings_lots source to ±$1 per position.</ac>
    <ac id="5">No cleartext client identifiers in artifact (spot-check via grep of known client-pseudonym-list against emitted artifacts — zero hits).</ac>
    <ac id="6">No regression on existing D_04 outputs — `comp-blast D_04.client_portal_summary` post-change shows same consumer set; summary/timeseries/mix/nna_clients continue emitting unchanged.</ac>
    <ac id="7">py_compile + `.tools/ds-commit-gate.sh` exit 0 pre-commit per CLAUDE.md Rule 14.</ac>
    <ac id="8">`comp-pipescript deployed D_04` MATCH post-S3-upload to `s3://opal-data-bd/code/gold/`.</ac>
    <ac id="9">Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail vs `<expect>`.</ac>
    <ac id="10">RAVC4 MCP to COO + CTO with commit hash, advisor count, spot-check outcome, contract-confirmed-for-TO-2 signal. On RAVC ACK, TO 2 (ds-llm-prose-generator) authoring unblocks.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="0" when="discovery (before write)">
      <step>
        <run>comp-pipescript io D_04.client_portal_summary</run>
        <expect>READS include HOLDINGS_LOTS_PREFIX + ACCOUNT_TEAM + ACCOUNTS_DIMENSION (verified 2026-04-24 by COO). Existing WRITES: summary.json + timeseries.json + mix.json + nna_clients.json at `platinum/advisors/{aid}/`. No COLUMN GAPS.</expect>
        <if_mismatch>STOP. If any of the 3 required upstream reads are absent, the no-new-reads claim in this TO breaks; surface to COO before writing. Re-check with CTO before proceeding.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="before commit (auto-rule 1 — new platinum artifact)">
      <step>
        <run>comp-platinum reverse 'platinum/advisors/*/positions.json'</run>
        <expect>PRODUCER=empty + SERVED_VIA=empty + CONSUMED_BY=empty (pre-ship; artifact does not yet exist).</expect>
        <if_mismatch>If PRODUCER is non-empty, a shadow-write exists — investigate before commit. If CONSUMED_BY surfaces before shipping, another agent wired the consumer path ahead of producer — coordinate.</if_mismatch>
      </step>
      <step>
        <run>comp-blast D_04.client_portal_summary</run>
        <expect>Existing consumer set: D_00b + existing platinum readers. No surprise new nodes.</expect>
        <if_mismatch>Investigate + surface to COO — a new downstream appeared during write.</if_mismatch>
      </step>
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_04.client_portal_summary.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>STOP. Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh data/black_diamond/scripts/gold/D_04.client_portal_summary.py data/black_diamond/scripts/gold/gold_validate_config.yaml</run>
        <expect>OK: pre-commit gate clean.</expect>
        <if_mismatch>STOP. Fix AST/undefined-name issues flagged by ds-precommit-check.py.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit (validator-local)">
      <step>
        <run>python3 -c "# Dry-run D_04 positions emit block locally against a recent gold/timeseries/holdings_lots/ partition + account_team snapshot; write /tmp/positions_sample.json for one advisor (e.g., aj_lenartowicz)"</run>
        <expect>/tmp/positions_sample.json conforms to §4.5 schema; all 14 per-position fields present; sort order market_value desc; len(positions) ≤ 25; positions_count ≥ len(positions).</expect>
        <if_mismatch>STOP. Schema contract violated; iterate emit block until conformant.</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_04 --artifact /tmp/positions_sample.json</run>
        <expect>Exit 0. All ERROR checks in `D_04_positions_output` validator entry pass. WARN count documented in session log (does not block).</expect>
        <if_mismatch>STOP. Do not commit until ERROR clean.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit + post-nightly">
      <step>
        <run>comp-pipescript deployed D_04</run>
        <expect>MATCH (committed-ref SHA == S3 ETag).</expect>
        <if_mismatch>Re-upload. Do not fire nightly until MATCH.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-bd/platinum/advisors/ --recursive | grep '/positions\.json$' | head -5</run>
        <expect>One positions.json per active advisor post-nightly (~45 for 49F). mtime within last 2h of D_04 completion.</expect>
        <if_mismatch>Chain didn't write positions.json for expected advisor set; inspect D_04 log for emit failures.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse 'platinum/advisors/*/positions.json'</run>
        <expect>PRODUCER=D_04. SERVED_VIA=empty until TO 2 wires consumer path (`getPlatinumAdvisorPositions`).</expect>
        <if_mismatch>If PRODUCER is not D_04, something shadow-wrote the file between commit + nightly. Investigate.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "# Spot-check 3 advisors: pull positions.json via boto3, verify (sum(market_value of top-25) ≤ total_aum); reconcile unrealized_gain against holdings_lots source ±$1 per position; scan for cleartext client pseudonym-list hits"</run>
        <expect>Top-AUM advisor + median-AUM + tail-AUM all reconcile. Zero cleartext hits.</expect>
        <if_mismatch>Reconciliation miss: investigate aggregation logic. Cleartext hit: STOP + COO/CTO escalation (PII breach class).</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource file="data/black_diamond/scripts/gold/D_04.client_portal_summary.py">
      **Active co-writers:** TO 5 prior-week leaderboard rotation (complete 2026-04-24 commit 8cc69bab at L~2398) — no conflict; rotation is leaderboard-scoped, positions is advisor-scoped. TOPPOSOPAL (staged, is_opal_model D-tier emit) — additive flag on different artifact set; coordinate commit ordering if both land same cycle but no emit-set collision.
    </shared_resource>
    <shared_resource file="data/black_diamond/scripts/gold/gold_validate_config.yaml">
      Add-only. Existing validator entries (D_00/D_00c/D_02/D_04/etc.) unchanged. SCOPEFIX INFLEC validator also landed 2026-04-24; different scope, no conflict.
    </shared_resource>
    <shared_resource artifact="platinum/advisors/{advisor_id}/positions.json">
      Producer/consumer pair: TO POSITIONS (DS writes, via D_04 extension) + TO 2 (DS reads, via generator Lambda). Schema §4.5 is the binding contract. TO 2 authoring unblocks on TO POSITIONS completion.
    </shared_resource>
    <downstream_pending>
      - ADVI_49EXEC.002 ds-llm-prose-generator — HOLD until this ships; CTO authors TO 2 on RAVC4 ACK.
      - ADVI_49EXEC.004 dt-generator-lambda-terraform — DT 0.4 chain-gate on TO 2 close.
      - ADVI_49EXEC.007 dt-eventbridge-wiring-and-deploy — DT 0.4 chain-gate on TO 4 close.
    </downstream_pending>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT emit pre-sliced gainers/losers/concentrations/tax-loss buckets. Flat + sorted only. TO 2 filters in Python at prompt time (§4.5 rationale).</rule>
    <rule>Do NOT emit lot-level granularity. Aggregate to (advisor_id, ticker).</rule>
    <rule>Do NOT add prior-period snapshot / rotation logic. Current snapshot only; generator computes period-delta at prompt construction.</rule>
    <rule>Do NOT author the generator Lambda or any LLM prompt logic. That's TO 2 scope.</rule>
    <rule>Do NOT modify `trigger_eval.py` (TO 1 shipped 8cc69bab). Align positions.json shape to the §4.5 schema, not to any prior trigger_eval field assumptions.</rule>
    <rule>Do NOT widen scope beyond 49F active advisors. INFLEC advisors have separate gold chain (data/orion/); cross-firm positions is a future RD if needed.</rule>
    <rule>Do NOT retroactively backfill historical positions.json partitions. Forward-emit only.</rule>
    <rule>Do NOT add cleartext client names/account numbers/client pseudonyms to the artifact. Field set is position-level; PII stance is "public market data only" by construction.</rule>
  </do_not>
</task_order>
