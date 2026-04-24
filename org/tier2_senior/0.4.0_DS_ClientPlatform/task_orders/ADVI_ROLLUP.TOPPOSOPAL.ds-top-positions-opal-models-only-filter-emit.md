<task_order>
  <metadata>
    <id>ADVI_ROLLUP.TOPPOSOPAL</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-24</date>
    <rewritten>2026-04-24 — FULL REWRITE per Andrew ruling (via CTO MCP 20260424T17xxxxZ). Original scope (position/account-level `is_opal_model` filter flag) INVALIDATED by DS Phase 0: no such field exists in BD data stack + 31.74% cost_basis coverage premise obsoleted by SL-P1 ship (today 99.87%). Andrew verbatim: "there is no way to filter to opal models, all we can do is identify what securities are included in opal models and infer." Option B redefine — ticker-inference, not position-filter. Filename slug preserved (saves REGISTRY churn); TO body fully rescoped.</rewritten>
    <status>staged</status><!-- Authored 2026-04-24 PM post Andrew-Option-B ruling. PHASE 0 INTERPRETATION GATE (soft): source-of-truth discovery for opal_model_ticker_universe. If DS Phase 0 finds it in data stack: auto-proceed. If not found: DS escalates to Andrew via COO for external materialization (CSV / sheet / config). GO dispatch fires after this rewrite + my MCP to DS. -->
    <project_code>ADVI_ROLLUP</project_code>
    <priority>P2 — Top Positions widget UX enrichment; not portal-breaking. Downstream imperfect-proxy signal for Opal-model exposure. Deprioritized vs POSITIONS / TO 2 / DSFLOW.004 backfill; DS slots in when bandwidth allows.</priority>
    <origin>
      Original TOPPOSOPAL (2026-04-24 AM) scoped around 31.74% cost_basis coverage gap + position-level `is_opal_model` filter. DS Phase 0 on 2026-04-24 PM found: (a) no such field exists in BD data, (b) 31.74% premise invalidated by SL-P1 shipping (today 99.87% coverage). DS invoked interpretation-hold discipline. COO escalated to Andrew via CTO; Andrew ruled Option B on 2026-04-24: "there is no way to filter to opal models, all we can do is identify what securities are included in opal models and infer." This rewrite encodes the Option B direction.
    </origin>
  </metadata>

  <references>
    <ref type="andrew_ruling">CTO MCP 20260424T17xxxxZ relaying Andrew verbatim ruling — Option B ticker-inference</ref>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md — Top Positions widget context</ref>
    <ref type="original_to_scope">Prior TO body (pre-rewrite): see git history — position-filter scope invalidated by Phase 0</ref>
    <ref type="phase_0_findings">DS MCP 20260424T17xxxxZ — interpretation hold + evidence dump (accounts_dimension + silver/allocations + bd_assets_dim + holdings_lots all checked)</ref>
    <ref type="predecessor_context">ADVI_ROLLUP.SL-P1 (complete 2026-04-24) — shipped cost_basis coverage to 99.87% invalidating original TOPPOSOPAL premise</ref>
    <ref type="compiler_mandate_auto_rule_4">CTO org prompt + COO prompt — silver-tier write requires `<data_reprocess_scope>` block (new silver/opal_models/ writes; Phase 3 re-ingest + mtime gate)</ref>
    <ref type="pending_rule_15">CLAUDE.md Rule 15 live post ADHC_DSFLOW.004 commit 6156d428 — new `.py` must have `from __future__ import annotations` line 1</ref>
    <ref type="potential_downstream">ADVI_49EXEC.002 prose generator — could read `has_opal_model_exposure` from positions.json for narrative context ("of your top holdings, 12 are held within Opal models"). Optional forward-compat field (see <scope> + <cross_domain_coordination>).</ref>
  </references>

  <objective>
    Produce a per-ticker `is_opal_model_security` flag by enumerating the Opal model portfolios + taking the union of their constituent tickers as the `opal_model_ticker_universe`. Emit the flag as a silver/gold-tier artifact consumable by D-tier scripts. D_04 then joins on ticker to emit per-position `has_opal_model_exposure` (bool) as an additive field to existing platinum artifacts (summary.json / positions.json). Consumers (FE Top Positions widget, LLM prose generator) infer Opal-model exposure from the flag.

    **ACCEPTED IMPERFECTION (Andrew-ruled explicitly):**
    - FALSE POSITIVE: advisor holds a ticker via legacy/inherited route; ticker is in a model → flagged but not actually Opal-managed.
    - FALSE NEGATIVE: Opal-managed account holds a ticker NOT in any current model (client-directed trade within a model account, legacy holding) → not flagged.
    - Andrew's framing: "all we can do is... infer." Best-available signal, not a perfect proxy.

    **EXPLICIT SCOPE LOCK (per CTO A-E direction):**
    - Source-of-truth discovery is PHASE 0 DS DISCOVERY — no code-write before resolving. If not in data stack, escalate via COO to Andrew for external materialization (CSV / Google Sheet / config file / manual ticker list).
    - Producer: likely new silver or B-tier enrichment producing `silver/opal_models/current_tickers.parquet` (or similar; schema in wire_contract).
    - D_04 extension: add ticker-join to emit `has_opal_model_exposure: bool` as additive field on existing platinum artifacts (scope decision in wire_contract — summary.json + positions.json).
    - NO new Lambda / TF — pure DS data-pipeline extension.
    - NO cross-firm (49F scope only; INFLEC Orion models out of scope this TO).
    - NO backfill of historical `has_opal_model_exposure` — forward-emit only; first populates on first nightly post-ship.
  </objective>

  <assumptions>
    <assumption id="accepted-imperfection" andrew_ruling="20260424">
      Andrew explicitly accepts false-positive + false-negative imperfection of the ticker-inference proxy: "all we can do is... infer." DS must NOT chase strict model-membership compliance. Document this in session log + TO completion report so downstream consumers (FE + TO 2 prose-gen) don't request tighter coupling.
    </assumption>
    <assumption id="source-of-truth-tbd" cto_direction="A">
      Opal model ticker universe source-of-truth is UNKNOWN at authoring time. Phase 0 DS discovery must identify. Candidates (CTO-listed, not exhaustive):
      - yang-pipeline model_portfolios table (Pod 1)
      - silver/models/ S3 prefix
      - trade-pipeline model reference data (Pod 3)
      - Static ticker list externally maintained by Andrew (sheet / config)
      If Phase 0 finds it in data stack → auto-proceed. If not → STOP + MCP COO → escalate to Andrew for materialization ask before any code-write.
    </assumption>
    <assumption id="forward-compat-positions-json" cto_direction="C">
      OPTIONAL: DS may add `has_opal_model_exposure: bool` to positions.json schema as forward-compat for TO 2 prose-gen narrative consumption ("of your top holdings, 12 are held within Opal models"). Emit ONLY IF:
      - Phase 0 resolves upstream source-of-truth cleanly, AND
      - TO 2 authoring is not yet closed (so schema change slots in cleanly).
      If TO 2 ships before TOPPOSOPAL or if upstream escalation is in flight, skip positions.json addition; emit the ticker-universe artifact standalone and wire later via a follow-on TO.
    </assumption>
    <assumption id="filename-preserved">
      Filename slug kept as `ds-top-positions-opal-models-only-filter-emit` (literally inaccurate post-rewrite but preserves REGISTRY row + git history). TO content fully rescoped. Future consumers see the mismatch; body clarifies. OPALTKR rename considered + rejected for churn economy.
    </assumption>
  </assumptions>

  <scope>
    <files>
      <file action="investigate">Phase 0 only — probe ALL of: (a) `silver/models/` S3 prefix; (b) yang-pipeline model_portfolios (`yang-pipeline` Pod 1 DS), (c) trade-pipeline model reference data (`trade-pipeline` Pod 3 DS), (d) any `data/black_diamond/silver/` config/reference files, (e) Andrew-external list via COO escalation path. Document what was checked + findings.</file>
      <file action="create_if_source_found">data/black_diamond/scripts/silver/build_opal_model_tickers.py OR extension to existing silver builder — produces `silver/opal_models/current_tickers.parquet` with columns: `ticker` (str, primary), `is_opal_model_security` (bool, always true if emitted), `models_containing` (array[str], list of model_ids containing this ticker for observability), `as_of_date` (date).</file>
      <file action="modify">data/black_diamond/scripts/gold/D_04.client_portal_summary.py — add ticker-join to existing emit pipeline; emit `has_opal_model_exposure: bool` as additive field on platinum artifact(s). Scope decision: add to `positions.json` (if forward-compat with TO 2 acceptable per assumption id="forward-compat-positions-json") AND/OR `summary.json`. DS Phase 0 documents choice.</file>
      <file action="modify">data/black_diamond/scripts/gold/gold_validate_config.yaml — add validator block for `has_opal_model_exposure` field presence + type-check (bool) + coverage-ratio check (non-null % expected — likely 100% since ticker-join fills false where no match).</file>
      <file action="modify">data/black_diamond/scripts/gold/lib/s3_layout.py — register new artifact key `silver/opal_models/current_tickers.parquet` if new silver path.</file>
      <file action="read-only">data/black_diamond/scripts/gold/B_01.holdings_lots.py — ticker join surface reference.</file>
      <file action="read-only">data/black_diamond/scripts/gold/D_04.client_portal_summary.py — existing Step 15 POSITIONS emit pattern (13eaca78).</file>
    </files>
    <s3_writes>
      <write>s3://opal-data-bd/silver/opal_models/current_tickers.parquet — OR alternative path per Phase 0 decision (e.g., extending existing silver/models/ prefix if pre-existing)</write>
      <write>s3://opal-data-bd/platinum/advisors/{advisor_id}/positions.json — forward-compat additive field `has_opal_model_exposure: bool` per-position, if assumption id="forward-compat-positions-json" holds</write>
      <write>s3://opal-data-bd/platinum/advisors/{advisor_id}/summary.json — alternative emit path per Phase 0 DS choice; aggregate field `opal_model_coverage_pct: float` (share of advisor AUM in Opal-model securities) possible</write>
    </s3_writes>
  </scope>

  <wire_contract>
    **silver/opal_models/current_tickers.parquet schema:**
    ```
    ticker: string (primary key)
    is_opal_model_security: bool  (always true if row present; row absence ≡ false)
    models_containing: array[string]  (list of model_ids for observability; e.g., ["opal-balanced-v2", "opal-growth-v1"])
    as_of_date: date  (ticker universe snapshot date; refreshes on model rebalance or quarterly)
    ```

    **D_04 ticker-join logic:**
    ```
    positions_enriched = positions.merge(
        silver_opal_models[['ticker', 'is_opal_model_security']],
        on='ticker',
        how='left'
    )
    positions_enriched['has_opal_model_exposure'] = positions_enriched['is_opal_model_security'].fillna(False).astype(bool)
    ```
    Left-join fills False for non-matching tickers. No nulls in emit.

    **Per-position field addition to positions.json (forward-compat, per assumption):**
    ```json
    {
      "ticker": "NVDA",
      "security_name": "NVIDIA Corporation",
      "asset_class": "equity",
      "market_value": 1250000.00,
      ...existing 13 fields...,
      "has_opal_model_exposure": true  // NEW
    }
    ```
    Becomes 14 per-position fields (was 13 per §4.5).

    **Optional aggregate field on summary.json:**
    ```json
    {
      "advisor_id": "aj_lenartowicz",
      ...existing...,
      "opal_model_coverage_pct": 0.47  // share of advisor AUM in Opal-model-flagged tickers
    }
    ```
    If DS Phase 0 chooses to emit this, document in session log.

    **Accepted imperfection documented inline in schema:** field docstring / README block for silver/opal_models + positions.json must cite Andrew's ruling + false-pos/false-neg framing so downstream consumers don't over-trust.
  </wire_contract>

  <deliverables>
    <deliverable id="phase-0-discovery-report">
      Session log documents: (a) candidates checked (silver/models/ + yang-pipeline model_portfolios + trade-pipeline ref-data + any ds-accessible reference files); (b) findings per candidate (exists / schema / access-path); (c) chosen source + rationale; OR (d) escalation-to-Andrew ask if not found — stop code-write here.
    </deliverable>
    <deliverable id="silver-opal-models-producer">
      If Phase 0 finds upstream: `silver/opal_models/current_tickers.parquet` (or alternative path per Phase 0 decision) emitted with the 4 schema fields; refresh cadence matches source (nightly / on-rebalance / quarterly — DS decides based on upstream volatility).
    </deliverable>
    <deliverable id="d04-ticker-join-emit">
      D_04 adds left-join ticker enrichment + emits `has_opal_model_exposure: bool` on positions.json (forward-compat) and/or summary.json (DS choice, document rationale).
    </deliverable>
    <deliverable id="validator-block">
      `gold_validate_config.yaml` D_04 validator entry updated to include `has_opal_model_exposure` field-presence + type-check + 100% non-null coverage assertion.
    </deliverable>
    <deliverable id="accepted-imperfection-documentation">
      Session log + code docstring(s) cite Andrew's Option B ruling verbatim + false-positive/false-negative framing. Downstream consumers must not over-trust the flag.
    </deliverable>
    <deliverable id="data-reprocess-scope-block">
      Per Auto-Rule 4: `<data_reprocess_scope>` block in TO (below) specifies reprocess semantics. Backfill N/A (forward-emit only per scope lock); ticker-universe refresh cadence determines future re-ingest triggers (document in session log).
    </deliverable>
    <deliverable id="session-log-compiler-section">
      Reproduces every `<run>` from mandate triad + observed + pass/fail vs `<expect>`. Append 6+ rows to `org/compiler-tools-log.md`.
    </deliverable>
    <deliverable id="ravc4-mcp">
      RAVC4 to COO + CTO with: commit SHA, Phase 0 source-of-truth decision + rationale, silver/opal_models/ S3 path + sample head-5, D_04 emit path + sample positions.json with new field, validator config diff, imperfection documentation cite.
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">Phase 0 source-of-truth discovery report — 4+ candidate paths checked with findings; clear decision OR escalation-to-Andrew flag.</ac>
    <ac id="2">If Phase 0 proceeds: silver/opal_models/current_tickers.parquet (or alternative) emitted per nightly with 4-field schema (ticker + is_opal_model_security + models_containing + as_of_date). Ticker universe row-count documented (expected range determined by Phase 0).</ac>
    <ac id="3">D_04 emits `has_opal_model_exposure: bool` additive field on positions.json (and/or summary.json per Phase 0 choice); 100% non-null coverage; distribution documented (expected: ~X% true per Andrew's commercial context — DS documents actual).</ac>
    <ac id="4">`gold_validate_config.yaml` validator entry for the new field(s); `comp-validate D_04 --artifact /tmp/sample.json` exits 0.</ac>
    <ac id="5">Accepted-imperfection documentation: Andrew's ruling cited verbatim in session log + inline code docstring; false-positive/false-negative framing documented.</ac>
    <ac id="6">No regression on existing D_04 outputs (positions/summary/timeseries/mix/nna_clients) — `comp-blast D_04.client_portal_summary` post-change shows same downstream consumer set.</ac>
    <ac id="7">py_compile + ds-commit-gate.sh (with ruff target-version=py39 per Rule 14 + __future__ import per Rule 15) exit 0 on all modified `.py` files.</ac>
    <ac id="8">`comp-pipescript deployed D_04` MATCH post-S3-upload.</ac>
    <ac id="9">Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail vs `<expect>`.</ac>
    <ac id="10">RAVC4 MCP bundle per <deliverable id="ravc4-mcp">.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="0" when="discovery (BEFORE write — interpretation gate)">
      <step>
        <run>aws s3 ls s3://opal-data-bd/silver/models/ 2>&amp;1 || aws s3 ls s3://opal-data-bd/silver/opal_models/ 2>&amp;1</run>
        <expect>Either prefix exists with ticker-universe content OR both return empty — document finding.</expect>
        <if_mismatch>If content found, inspect schema + freshness; document as primary candidate. If both empty, continue to next candidate.</if_mismatch>
      </step>
      <step>
        <run># Probe yang-pipeline model_portfolios table (Pod 1) — via yang-pipeline MCP or manifest check</run>
        <expect>Table/file exists with {model_id, ticker, weight} or similar shape that enumerates Opal model constituents.</expect>
        <if_mismatch>If absent, continue to trade-pipeline candidate.</if_mismatch>
      </step>
      <step>
        <run># Probe trade-pipeline model reference data (Pod 3)</run>
        <expect>Reference data surfaces Opal model ticker universe.</expect>
        <if_mismatch>If absent, continue to ds-accessible reference files (data/*/config/, data/*/reference/).</if_mismatch>
      </step>
      <step>
        <run># Probe repo config files for ticker-list references — grep for opal_model_tickers, opal_universe, model_constituents</run>
        <expect>Static reference file in repo OR nothing.</expect>
        <if_mismatch>If all 4 candidates absent, STOP. MCP COO with explicit escalation ask: "Phase 0 exhausted data-stack candidates. Need Andrew to either (a) materialize ticker-universe as CSV/sheet, (b) name a source I haven't checked, or (c) cancel TOPPOSOPAL as infeasible." DO NOT proceed to code-write.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io D_04.client_portal_summary</run>
        <expect>Post-POSITIONS state: READS include HOLDINGS_LOTS + ACCOUNT_TEAM + ACCOUNTS_DIMENSION; WRITES include platinum/advisors/{*}/summary + timeseries + mix + nna_clients + positions.</expect>
        <if_mismatch>If D_04 state unexpected, surface to COO before emit plan.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="before commit (auto-rule 4 — silver write)">
      <step>
        <run>comp-platinum reverse 'silver/opal_models/current_tickers.parquet' (or chosen silver path)</run>
        <expect>PRODUCER empty pre-ship (new artifact).</expect>
        <if_mismatch>If PRODUCER non-empty, someone shadow-wrote the file — investigate before commit.</if_mismatch>
      </step>
      <step>
        <run>comp-blast D_04.client_portal_summary</run>
        <expect>Consumer set unchanged — no surprise downstream edges from adding has_opal_model_exposure field.</expect>
        <if_mismatch>Investigate + coordinate before commit.</if_mismatch>
      </step>
      <step>
        <run>python -m py_compile data/black_diamond/scripts/silver/build_opal_model_tickers.py data/black_diamond/scripts/gold/D_04.client_portal_summary.py data/black_diamond/scripts/gold/gold_validate_config.yaml</run>
        <expect>Exit 0 on all.</expect>
        <if_mismatch>STOP. Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh {modified files}</run>
        <expect>OK — ruff target-version=py39 pass + ds-precommit AST clean + py_compile clean. Files under `data/*/scripts/{gold,silver,bronze}/` must have `from __future__ import annotations` line 1 per Rule 15.</expect>
        <if_mismatch>STOP. Fix Rule 14 / Rule 15 issues flagged.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit (validator)">
      <step>
        <run>python3 -c "# Dry-run D_04 positions + ticker-join locally on one advisor; write /tmp/positions_with_exposure_sample.json"</run>
        <expect>has_opal_model_exposure field present; distribution is non-trivial (not 100% false); schema conforms.</expect>
        <if_mismatch>STOP. Investigate ticker-join logic.</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_04 --artifact /tmp/positions_with_exposure_sample.json</run>
        <expect>Exit 0.</expect>
        <if_mismatch>STOP. Iterate validator entry or emit until clean.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit + post-nightly">
      <step>
        <run>comp-pipescript deployed D_04</run>
        <expect>MATCH.</expect>
        <if_mismatch>Re-upload.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-bd/silver/opal_models/current_tickers.parquet</run>
        <expect>Populated; mtime recent.</expect>
        <if_mismatch>Silver producer didn't emit; inspect.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse 'silver/opal_models/current_tickers.parquet'</run>
        <expect>PRODUCER=build_opal_model_tickers (or chosen producer name); downstream consumer = D_04.</expect>
        <if_mismatch>Surface to COO.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "# spot-check 3 advisors post-nightly — verify has_opal_model_exposure present in positions.json + distribution sensible (not all-true, not all-false)"</run>
        <expect>Distribution plausible per commercial expectation. Andrew spot-review if surprising.</expect>
        <if_mismatch>Flag distribution anomaly to COO + Andrew.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <reprocess_required>
      Per Compiler Mandate Auto-Rule 4. This TO writes to `silver/opal_models/` (new silver prefix).

      **Initial ship:** first emit on first nightly post-commit populates `silver/opal_models/current_tickers.parquet` + downstream D_04 picks up on same run. No historical backfill (forward-emit only per scope lock).

      **Ongoing reprocess triggers:**
      - Model rebalance (upstream source updates ticker set) → silver builder re-runs → D_04 picks up on next nightly. Mtime gate: verify silver/opal_models/ mtime post-commit > silver builder ship-time before downstream D_04 emit trusted.
      - Source-of-truth cadence (Phase 0 determines — likely quarterly on model rebalance OR nightly if upstream is dynamic).

      **Downstream consumer freshness gate:**
      - D_04 reads `silver/opal_models/current_tickers.parquet` at emit time; failure-to-read or stale-partition = `has_opal_model_exposure` defaults to False for all positions (left-join behavior). Session log documents if observed.
      - Portal FE Top Positions widget + potential TO 2 prose-gen consumption: no additional gate (platinum is daily-refreshed).
    </reprocess_required>
  </data_reprocess_scope>

  <cross_domain_coordination>
    <shared_resource file="data/black_diamond/scripts/gold/D_04.client_portal_summary.py">
      **Recent co-writers:**
      - CP-WP5 complete 2026-04-22 `296b778e`
      - CP-RES20 complete 2026-04-22 `f0f326d2`
      - TO 5 prior-week leaderboard rotation complete 2026-04-24 `8cc69bab`
      - POSITIONS Step 15 complete 2026-04-24 `13eaca78` (13-field positions.json)
      **Active co-writers:**
      - ADHC_DSFLOW.004 backfill sweep PENDING (`6156d428` Phase 1 shipped; sweep held per sequencing awaiting TOPPOSOPAL + POSITIONS land → this rewrite lands → backfill sweeps on top of all)
      Coordination: this TO's D_04 edit lands BEFORE DSFLOW.004 backfill sweep (per DS sequencing plan). Additive ticker-join field merges cleanly; backfill sweep adds `from __future__` atop whatever state D_04 is in.
    </shared_resource>
    <shared_resource file="data/black_diamond/scripts/gold/gold_validate_config.yaml">
      Current co-writers: POSITIONS (13eaca78 D_04_positions_output block shipped), SCOPEFIX INFLEC (2d3de276 + compat 6c1362de SCOPEFIX assertions shipped). This TO adds `has_opal_model_exposure` field-presence block — additive, no collision.
    </shared_resource>
    <shared_resource file="data/black_diamond/scripts/silver/">
      New directory (or existing — Phase 0 determines). If silver/ is newly created for opal_models, add `from __future__ import annotations` per Rule 15 + register in lib/s3_layout.py.
    </shared_resource>
    <shared_resource artifact="platinum/advisors/{id}/positions.json">
      Producer: POSITIONS TO (D_04 Step 15, shipped 13eaca78). Consumer: TO 2 prose-gen (staged 175a6d84).
      **Optional forward-compat extension:** this TO may add `has_opal_model_exposure: bool` to 14 per-position fields IF Phase 0 resolves upstream source cleanly + TO 2 not yet shipped. See assumption id="forward-compat-positions-json".
      If TO 2 ships before TOPPOSOPAL or upstream escalation is in flight: this TO ships silver artifact standalone + defers platinum emit to follow-on TO.
    </shared_resource>
    <potential_downstream>
      ADVI_49EXEC.002 prose-gen (staged 175a6d84): could read `has_opal_model_exposure` for narrative context. Not hard-gated; if this TO ships the field in positions.json before TO 2 ships its Lambda, TO 2 picks it up naturally via the schema contract. If TO 2 ships first, a follow-on TO extends positions.json or TO 2 re-reads as v2.
    </potential_downstream>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT chase strict Opal-model-membership compliance. Andrew's ruling explicitly accepts imperfection (false positives + negatives). Ticker-inference is the best available signal, not a perfect proxy.</rule>
    <rule>Do NOT emit position-level or account-level `is_opal_model` boolean (the original TOPPOSOPAL scope). Andrew ruled "no way to filter." Ticker-universe inference only.</rule>
    <rule>Do NOT proceed past Phase 0 if source-of-truth not found in data stack. Escalate to Andrew via COO with materialization ask.</rule>
    <rule>Do NOT retroactively backfill `has_opal_model_exposure` on historical positions. Forward-emit only.</rule>
    <rule>Do NOT widen scope to INFLEC Orion gold chain. BD 49F scope only (data/black_diamond/); Inflection future RD if needed.</rule>
    <rule>Do NOT author Lambda or TF — pure DS data-pipeline extension. No infra changes.</rule>
    <rule>Do NOT skip Auto-Rule 4 data_reprocess_scope accounting — this TO writes silver/opal_models/. Reprocess semantics are mandatory per compiler mandate.</rule>
    <rule>Do NOT skip Rule 15 `from __future__ import annotations` on any new `.py` file per CLAUDE.md live mandate.</rule>
    <rule>Do NOT modify TOPPOSOPAL filename slug. Rewrite body only; preserves REGISTRY + git history.</rule>
  </do_not>
</task_order>
