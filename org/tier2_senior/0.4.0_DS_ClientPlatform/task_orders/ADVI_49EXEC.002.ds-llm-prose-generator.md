<task_order>
  <metadata>
    <id>ADVI_49EXEC.002</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to><!-- base lane; ~lane OK if bandwidth -->
    <date>2026-04-24</date>
    <rewritten>2026-04-24 — full rewrite per CTO TO 2 authoring direction MCP 20260424T164858Z (6 scope additions A-F) + 3 ambiguity defaults resolved MCP 20260424T16xxxxZ. Original 2026-04-15 TO preserved only in git history.</rewritten>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. --><!-- Authored 2026-04-24 iter 4 of /loop ADVI. GATES MET contract-wise: TO 1 COMPLETE (8cc69bab) + TO 3 COMPLETE (c0a00bcc) + TO 5 COMPLETE (8cc69bab) + POSITIONS COMPLETE (13eaca78, contract-locked; 5/10 AC post-nightly verification gated on tonight's 23:00Z). GO DISPATCH HELD until POSITIONS Phase 3 post-nightly validation clears tomorrow AM per CTO flip-back condition discipline. On Phase 3 clean: dispatch GO. On Phase 3 miss: POSITIONS flips back to pending + TO 2 stays staged. -->
    <project_code>ADVI_49EXEC</project_code>
    <priority>P1 — closes 49EXEC Phase 1. Gates TO 4 (DT generator Lambda Terraform apply + tag) + TO 7 (DT EventBridge wiring). Primary visible feature for exec-summary v1.</priority>
    <origin>
      ADVI_49EXEC PRD §7 TO 2 (original 2026-04-15). Rewritten per CTO direction MCP 20260424T164858Z adding 6 scope additions post-POSITIONS ship (positions.json as READ, null-handling contract, slot-trigger mapping, /claude-api skill routing, 4-phase compiler mandate, Auto-Rule 4 <no_reprocess_needed> reasoning). 3 ambiguity defaults resolved MCP 20260424T16xxxxZ by CTO (concentration_risk threshold static constant / top-N hard 3 / wash-sale 30d v1 heuristic).
    </origin>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_49EXEC.md §3 (artifact schema exec_summary.json) + §4.5 (positions.json schema + edge-case semantics) + §5 (security/PII) + §7 TO 2 (original + additions)</ref>
    <ref type="prd_amendment_commit">5059cdf0 — §4.5 positions.json schema authoring</ref>
    <ref type="prd_amendment_commit">7b052d6f — §4.5 edge-case semantics (zero-cost-basis + null acquisition_date)</ref>
    <ref type="cto_authoring_direction">MCP 20260424T164858Z — full A-F scope addition</ref>
    <ref type="cto_ambiguity_resolutions">MCP 20260424T16xxxxZ — 3 defaults accepted with rationale</ref>
    <ref type="predecessor_to">ADVI_49EXEC.001 (complete 8cc69bab) — trigger_eval.py 6 slot evaluators this Lambda wraps</ref>
    <ref type="predecessor_to">ADVI_49EXEC.003 (complete c0a00bcc) — anthropic-sdk-deps Lambda layer this Lambda imports</ref>
    <ref type="predecessor_to">ADVI_49EXEC.005 (complete 8cc69bab) — D_04 prior_week leaderboard rotation this Lambda consumes</ref>
    <ref type="predecessor_to">ADVI_49EXEC.POSITIONS (complete 13eaca78) — D_04 Step 15 positions.json emit this Lambda reads</ref>
    <ref type="downstream_blocker">ADVI_49EXEC.004 dt-generator-lambda-terraform — DT 0.4 TF apply + tag gates on this TO's testable artifact</ref>
    <ref type="downstream_blocker">ADVI_49EXEC.007 dt-eventbridge-wiring-and-deploy — DT 0.4 EventBridge wiring gates on TO 4 close</ref>
    <ref type="skill">/claude-api — MANDATORY skill invocation for Lambda implementation per CTO item D</ref>
  </references>

  <objective>
    Author the exec-summary-generator Lambda that wraps TO 1's `trigger_eval.py` 6 slot evaluators. For each triggered slot, (a) read 4 platinum artifacts per advisor, (b) construct a slot-specific Claude Sonnet 4.6 prompt with caching, (c) call the anthropic SDK using the `/claude-api` skill patterns, (d) validate the response (240-char cap + URL strip-and-reject + PII assertion + per-slot schema parse), (e) write the final `exec_summary.json` artifact to `s3://opal-data-bd/platinum/advisors/{advisor_id}/exec_summary.json` per PRD §3 schema. Cost telemetry via CloudWatch metrics per PRD §4.2.

    **EXPLICIT SCOPE LOCK (per CTO direction A-F):**
    - **READS per advisor (4 platinum inputs):** summary.json + timeseries.json + nna_clients.json + positions.json (§4.5 spec, shipped 13eaca78). Plus `platinum/leaderboards/{firm}.json` + `.prior_week.json` (TO 5 rotation) for firm-scoped context.
    - **Null-handling contract for positions.json fields (§4.5 edge cases, 7b052d6f):**
      - `unrealized_gain_pct == null` (zero-cost-basis): `top_gainer` / `top_loser` rank by `unrealized_gain` absolute dollars (not pct). `concentration_risk` uses `pct_of_advisor_aum` (unaffected). `tax_loss_candidate` uses `unrealized_gain` sign (ignores pct nullness).
      - `oldest_lot_holding_days == null` (missing acquisition_date): `tax_loss_candidate` SKIPS the position (tax-loss eligibility requires holding-period data).
      - `first_acquisition_date` / `last_acquisition_date == null`: LLM prompt omits timing language ("held since..."); fall back to generic "currently held" phrasing.
    - **Slot-trigger logic (per CTO item C — implemented inside or adjacent to trigger_eval.py):**

      | Slot | Input fields | Trigger logic |
      |------|-------------|---------------|
      | top_gainer | `positions[].unrealized_gain` | Top 1-3 positions by absolute `unrealized_gain` > $0; sorted desc |
      | top_loser | `positions[].unrealized_gain` | Top 1-3 positions by absolute `unrealized_gain` < $0; sorted asc |
      | concentration_risk | `positions[].pct_of_advisor_aum` | Positions where `pct_of_advisor_aum >= 0.10` (static constant per CTO) |
      | tax_loss_candidate | `positions[].unrealized_gain < 0` AND `oldest_lot_holding_days >= 30` AND `oldest_lot_holding_days NOT null` | Tax-loss eligible; LLM narrates holding-period context |

    - **/claude-api skill routing (MANDATORY per CTO item D):** DS invokes `/claude-api` at start of Lambda implementation. Skill enforces: (i) prompt caching with 5-min TTL ephemeral `cache_control` on system prompt + slot-template blocks; (ii) anthropic-version header pinning; (iii) structured response via tool-use or JSON-mode (not raw text); (iv) explicit model ID `claude-sonnet-4-6` (not alias).
    - **NO silver/bronze writes** — this is a platinum-tier consumer + platinum-tier producer. Auto-Rule 4 applies as `<no_reprocess_needed>` (see block).
  </objective>

  <assumptions>
    <assumption id="concentration-risk-threshold" cto_ack="20260424T16xxxxZ">
      `concentration_risk` threshold is a STATIC CONSTANT = 0.10 in `lambda_function.py` or `config.py`. Rationale (per CTO): no admin UI consumes a tunable value; env var adds Terraform surface without operational benefit; DDB adds per-invoke fetch cost. Keep the three concentration_risk params (threshold, max_flagged, asset_class_nuance) together in a single dict so promotion to env-var or DDB is a 1-line change if Andrew later requests admin-tunability.
    </assumption>
    <assumption id="top-gainer-loser-ceiling" cto_ack="20260424T16xxxxZ">
      `top_gainer` and `top_loser` cite a HARD CEILING of 3 positions per slot. Rationale (per CTO): prompt budget math — ~500 input tokens per slot × ~30 tokens per position cite = 90 tokens of position cites, fits cleanly in 500. Budget-bounded is over-engineering for v1; promote to dynamic later if slot length-cap forces truncation.
    </assumption>
    <assumption id="wash-sale-30d-heuristic" cto_ack="20260424T16xxxxZ">
      `tax_loss_candidate` filter uses `oldest_lot_holding_days >= 30` as a proxy for wash-sale safety. This is an IMPERFECT HEURISTIC, NOT strict wash-sale compliance. Real wash-sale rule is bidirectional (30d before or after a sale of the same security) which is a transactional constraint, not a holding-period constraint. The oldest-lot filter catches ~95% of "don't recommend harvesting a 5-day-old position" cases; the remaining 5% (long-held position with a recent-loss-lot subset) is handled as LLM-narrative nuance ("consider wash-sale rule before executing"). V1 explicit scope — DO NOT chase strict wash-sale compliance in this TO.
    </assumption>
  </assumptions>

  <scope>
    <files>
      <file action="create">infra/aws/lambda/exec-summary-generator/lambda_function.py — main handler: iterate active advisors, for each build slot-triggered prompts, invoke Claude, validate + write artifact</file>
      <file action="create">infra/aws/lambda/exec-summary-generator/config.py — concentration_risk_params dict (threshold=0.10, max_flagged, asset_class_nuance); top_n ceilings; prompt budget constants; wash-sale heuristic floor (30d)</file>
      <file action="create">infra/aws/lambda/exec-summary-generator/platinum_reader.py — 4-input + leaderboards reader; handles all 3 null-field edge cases (unrealized_gain_pct null / oldest_lot_holding_days null / first|last_acquisition_date null) per CTO item B</file>
      <file action="create">infra/aws/lambda/exec-summary-generator/prompts/system.txt — system prompt with cache_control ephemeral 5-min TTL</file>
      <file action="create">infra/aws/lambda/exec-summary-generator/prompts/top_gainer.txt — slot template with cache_control</file>
      <file action="create">infra/aws/lambda/exec-summary-generator/prompts/top_loser.txt — slot template with cache_control</file>
      <file action="create">infra/aws/lambda/exec-summary-generator/prompts/concentration_risk.txt — slot template with cache_control</file>
      <file action="create">infra/aws/lambda/exec-summary-generator/prompts/tax_loss_candidate.txt — slot template with cache_control + wash-sale narrative guidance per assumption id="wash-sale-30d-heuristic"</file>
      <file action="create">infra/aws/lambda/exec-summary-generator/prompts/{additional_2_slots}.txt — remaining 2 slots per TO 1 trigger_eval.py enumeration</file>
      <file action="create">infra/aws/lambda/exec-summary-generator/validator.py — 240-char cap + URL regex strip-and-reject + PII assertion + per-slot JSON schema parse</file>
      <file action="create">infra/aws/lambda/exec-summary-generator/metrics.py — CloudWatch metric emit per PRD §4.2 (ExecSummaryAdvisorsProcessed / ExecSummaryLLMCallsMade / ExecSummaryTokensIn / ExecSummaryTokensOut / ExecSummaryEmptyAdvisors / ExecSummarySlotDropped)</file>
      <file action="create">tests/exec_summary/test_llm_generator.py — mocked anthropic responses; all 6 slots × (happy path + schema-fail + PII-detected + URL-detected + null-handling edge cases × 3) test coverage</file>
      <file action="create">tests/exec_summary/fixtures/sample_positions.json — test fixture with 13-field schema including null edge cases (zero-cost-basis row + null-acquisition-date row + all-valid rows)</file>
      <file action="read-only">data/black_diamond/scripts/exec_summary/trigger_eval.py (TO 1 shipped 8cc69bab) — consumer contract; DO NOT modify</file>
      <file action="read-only">docs/architecture/ADVI_49EXEC.md §3 (exec_summary.json schema) + §4.5 (positions.json schema + edge cases) + §5 (PII)</file>
      <file action="read-only">data/black_diamond/scripts/gold/D_04.client_portal_summary.py (POSITIONS 13eaca78 shipped) — producer of positions.json this Lambda reads</file>
    </files>
    <s3_reads>
      <read>s3://opal-data-bd/platinum/advisors/{advisor_id}/summary.json — existing</read>
      <read>s3://opal-data-bd/platinum/advisors/{advisor_id}/timeseries.json — existing</read>
      <read>s3://opal-data-bd/platinum/advisors/{advisor_id}/nna_clients.json — existing</read>
      <read>s3://opal-data-bd/platinum/advisors/{advisor_id}/positions.json — NEW (§4.5, shipped 13eaca78)</read>
      <read>s3://opal-data-bd/platinum/leaderboards/{firm}.json + .prior_week.json — existing (TO 5 rotation)</read>
    </s3_reads>
    <s3_writes>
      <write>s3://opal-data-bd/platinum/advisors/{advisor_id}/exec_summary.json — one per active advisor per nightly</write>
    </s3_writes>
  </scope>

  <wire_contract>
    **Lambda handler input (EventBridge event from TO 7 future wiring):** chain-complete signal payload (firm scope, date). Lambda enumerates `platinum/advisors/` prefix to identify active advisors (same set as POSITIONS.json emit set per nightly). Iterates synchronously; target completion ≤ 90 min post gold-chain-complete signal (per PRD §10 AC #1).

    **Lambda IAM (DT TO 4 provisions via iam.tf):**
    - `s3:GetObject` on `arn:aws:s3:::opal-data-bd/platinum/advisors/*` + `platinum/leaderboards/*`
    - `s3:PutObject` on `arn:aws:s3:::opal-data-bd/platinum/advisors/*/exec_summary.json`
    - `secretsmanager:GetSecretValue` on `anthropic-api-key` ARN
    - `cloudwatch:PutMetricData` on namespace `Opal/ExecSummary`

    **Artifact shape `platinum/advisors/{id}/exec_summary.json` (per PRD §3):**
    ```json
    {
      "advisor_id": "aj_lenartowicz",
      "firm_id": "49financial",
      "generated_at": "2026-04-24T23:45:00Z",
      "model": "claude-sonnet-4-6",
      "input_hash": "sha256-of-concatenated-input-fingerprints",
      "bullets": [
        {
          "slot": "top_gainer",
          "detail": "240-char bounded LLM output citing NVDA up $510K (+69%) as the biggest winner this week",
          "evidence_keys": ["positions.json#NVDA"]
        }
      ],
      "permissions_scope": "firm:49financial;advisor:aj_lenartowicz"
    }
    ```

    **Validation pipeline per LLM response:**
    1. 240-char cap on `detail` field — truncate + log warning + optional retry at lower token budget if first response exceeded
    2. URL regex strip (any `https?://` match → reject + retry once with explicit "no URLs" system-prompt reinforcement)
    3. PII assertion: `assert PII_PATTERN.search(detail) is None` per PRD §5.1; raise on hit (should never occur — pseudonymized inputs; defense-in-depth gate)
    4. Per-slot JSON schema parse: if response structurally invalid, drop that slot (emit CloudWatch `ExecSummarySlotDropped` metric); continue other slots
    5. If all slots drop for an advisor: still write artifact with empty `bullets[]` (so downstream portal sees "no data this period" not 404)

    **Prompt caching strategy (per /claude-api skill):**
    - System prompt: `cache_control: {"type": "ephemeral"}` — 5-min TTL
    - Per-slot template blocks: `cache_control: {"type": "ephemeral"}` — 5-min TTL
    - Per-advisor variable content (platinum reads): NO cache_control — recomputed per advisor
    - Expected cache hit rate: system+template stable across advisors within a nightly run → hit-rate ≥ 80% on 2nd+ advisor per slot

    **Model ID:** explicit `claude-sonnet-4-6` (NOT an alias). Pin anthropic-version header per /claude-api skill.

    **Rate limiting + retry:** anthropic SDK default backoff; surface rate-limit errors as CloudWatch metrics; no synthetic retry beyond SDK.
  </wire_contract>

  <deliverables>
    <deliverable id="lambda-handler">
      `lambda_function.py` main handler: enumerate active advisors → per advisor read 4 platinum artifacts + leaderboards → trigger_eval.py invocation → per triggered slot build prompt + Claude call + validate + accumulate → write exec_summary.json to S3 → emit CloudWatch metrics.
    </deliverable>
    <deliverable id="config-py">
      `config.py` with concentration_risk_params dict (threshold=0.10, max_flagged=5, asset_class_nuance={}) + top_n ceilings (top_gainer=3, top_loser=3) + wash-sale-heuristic-floor-days=30 + prompt-budget-tokens (500 per slot input).
    </deliverable>
    <deliverable id="platinum-reader">
      `platinum_reader.py` loads 4 artifacts per advisor + leaderboards; handles all 3 null-field cases per CTO item B; returns structured dataclass or dict for trigger_eval consumption.
    </deliverable>
    <deliverable id="slot-prompt-templates">
      6 slot prompt template files (top_gainer / top_loser / concentration_risk / tax_loss_candidate + 2 remaining per trigger_eval.py); each has `cache_control` ephemeral markup for /claude-api caching.
    </deliverable>
    <deliverable id="validator-pipeline">
      `validator.py` — 4-stage pipeline (240ch cap + URL strip-and-reject + PII assert + per-slot JSON schema parse); SlotDropped metric on failure; graceful-empty on all-drop.
    </deliverable>
    <deliverable id="metrics-module">
      `metrics.py` — 6 CloudWatch metrics per PRD §4.2 emitted per Lambda invocation + per advisor + per slot.
    </deliverable>
    <deliverable id="unit-tests">
      `tests/exec_summary/test_llm_generator.py` — mocked anthropic responses covering 6 slots × (happy path + schema-fail + PII-detected + URL-detected) + null-handling edges (zero-cost-basis → top_gainer ranks by $ / null acquisition_date → tax_loss_candidate skip / null first_acquisition_date → LLM prompt omits timing). Target ≥ 40 test cases.
    </deliverable>
    <deliverable id="local-invoke-evidence">
      Session log captures local mock invocation (1 advisor, full 6-slot cycle) with: CloudWatch metric values, sample exec_summary.json artifact, prompt-cache-hit stats (expect 0% on 1st-advisor + 80%+ on 2nd+), anthropic-version header + model ID echoed in request.
    </deliverable>
    <deliverable id="session-log-compiler-section">
      Session log Compiler Tools section reproduces every `<run>` from mandate triad + observed + pass/fail vs `<expect>`. Append 8+ rows to `org/compiler-tools-log.md`.
    </deliverable>
    <deliverable id="ravc4-mcp">
      RAVC4 to COO + CTO with: commit SHA, test pass count, Lambda code path, sample artifact on S3 (or local), CloudWatch metric values, /claude-api skill invocation confirmation, prompt-cache-hit evidence.
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">PRD §3 schema artifact written — all required fields populated (advisor_id, firm_id, generated_at, model, input_hash, bullets[], permissions_scope).</ac>
    <ac id="2">All 6 slot prompt templates produce LLM responses within 240-char detail cap post-validator. If truncation needed, logged + metric emitted.</ac>
    <ac id="3">URL-strip-and-reject + PII-assert + schema-parse-drop all unit-tested with mocked anthropic responses. Target ≥ 40 test cases covering all 6 slots × 4 validation paths + 3 null-handling edges.</ac>
    <ac id="4">Cost telemetry: all 6 CloudWatch metrics per PRD §4.2 emitted per invocation. Local-mock-invoke evidence in session log.</ac>
    <ac id="5">Prompt caching per /claude-api skill: `cache_control: ephemeral` markup on system prompt + slot templates; local-mock evidence of cache-hit on 2nd+ advisor per slot (≥ 80% hit rate expected).</ac>
    <ac id="6">Explicit model ID `claude-sonnet-4-6` (not alias) in all invocations. anthropic-version header pinned per /claude-api skill.</ac>
    <ac id="7">3 null-handling edge cases from CTO item B implemented + unit-tested: (a) unrealized_gain_pct null → top_gainer/loser rank by $; (b) oldest_lot_holding_days null → tax_loss_candidate skip; (c) first/last_acquisition_date null → LLM omits timing language.</ac>
    <ac id="8">3 assumptions block present with CTO ACK timestamps encoded (concentration_risk threshold static / top-N hard 3 / wash-sale 30d v1 heuristic).</ac>
    <ac id="9">py_compile + ds-commit-gate.sh exit 0 per CLAUDE.md Rule 14. `from __future__ import annotations` at line 1 of every `.py` module under `infra/aws/lambda/exec-summary-generator/` per pending Rule 15 (ADHC_DSFLOW.004) — apply proactively.</ac>
    <ac id="10">Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail vs `<expect>`. RAVC4 MCP bundle to COO + CTO with all evidence per <deliverable id="ravc4-mcp">.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="0" when="discovery (before write)">
      <step>
        <run>comp-platinum page AdvisorPublicProfile --feature positions</run>
        <expect>positions.json wired into served path (getPlatinumAdvisorPositions endpoint via auto-pattern *.json -> S3). If no --feature flag support, run plain `comp-platinum page AdvisorPublicProfile` and inspect the fetch list for positions.json consumer (may not surface until TO 6 DE consumer added).</expect>
        <if_mismatch>If positions.json shows no consumer path, confirm POSITIONS D_04 emit is live post-nightly first. Acceptable in Phase 0 discovery to have the auto-pattern pending.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-bd/platinum/advisors/aj_lenartowicz/positions.json</run>
        <expect>File exists post-POSITIONS Phase 3 verification. Use as live read-target for local-mock invocation.</expect>
        <if_mismatch>If missing, POSITIONS Phase 3 didn't land — pause TO 2 ship and flag to COO.</if_mismatch>
      </step>
      <step>
        <run>/claude-api skill invocation confirmation — Skill tool result shows API patterns loaded (caching, pinning, structured, explicit model ID)</run>
        <expect>Skill tool acknowledges /claude-api; DS reads skill instructions before writing Lambda handler.</expect>
        <if_mismatch>STOP. Do not write Lambda handler without /claude-api skill guidance loaded.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="before commit (auto-rule 3 applies — IAM-gated resource touch)">
      <step>
        <run>comp-iam service exec-summary-generator</run>
        <expect>Lambda not yet in graph (new). Document expected IAM: s3:GetObject on platinum/advisors/* + platinum/leaderboards/*, s3:PutObject on platinum/advisors/*/exec_summary.json, secretsmanager:GetSecretValue on anthropic-api-key, cloudwatch:PutMetricData. DT TO 4 provisions.</expect>
        <if_mismatch>If Lambda exists in graph already (shouldn't), TO 4 may have shipped early — coordinate with DT 0.4.</if_mismatch>
      </step>
      <step>
        <run>comp-pii audit 'platinum/advisors/*/positions.json'</run>
        <expect>Zero cleartext hits post-POSITIONS Phase 3. Field set is position-level by construction (no client names/account numbers); PII stance confirmed.</expect>
        <if_mismatch>If cleartext detected, halt TO 2 and MCP COO + CTO — positions.json schema must be tightened before prose generator reads it.</if_mismatch>
      </step>
      <step>
        <run>comp-cache collisions</run>
        <expect>Existing 4 collisions in AdvisorIntelligence (firmOverride-scoped, intentional). Zero NEW collisions introduced by exec_summary.json consumer (TO 6 adds useAdvisorExecSummary hook; auto-detect via next cache pass).</expect>
        <if_mismatch>If new collision appears with exec_summary cache key, investigate before TO 6 ships.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit (code + tests)">
      <step>
        <run>python -m py_compile infra/aws/lambda/exec-summary-generator/*.py</run>
        <expect>Exit 0 on all modules (lambda_function.py + config.py + platinum_reader.py + validator.py + metrics.py).</expect>
        <if_mismatch>STOP. Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh infra/aws/lambda/exec-summary-generator/*.py tests/exec_summary/*.py</run>
        <expect>OK: pre-commit gate clean. All modules have `from __future__ import annotations` at line 1 (pending Rule 15 from ADHC_DSFLOW.004; apply proactively).</expect>
        <if_mismatch>STOP. Fix AST/undefined-name or missing __future__ import.</if_mismatch>
      </step>
      <step>
        <run>pytest tests/exec_summary/test_llm_generator.py -v</run>
        <expect>All tests PASS. ≥ 40 test cases covering 6 slots × 4 validation paths + 3 null-handling edges.</expect>
        <if_mismatch>STOP. Fix Lambda logic until all tests pass.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "# Local mock invoke — 1 advisor, full 6-slot cycle with mocked anthropic responses; log CloudWatch metric values; dump sample exec_summary.json"</run>
        <expect>Single advisor produces 1 exec_summary.json artifact; 6 slots attempt; per-slot metrics emitted; `generated_at` + `model` + `input_hash` populated; `bullets[]` has ≥ 1 entry (or empty if no triggers fire); prompt-cache-hit stats logged.</expect>
        <if_mismatch>STOP. Iterate until mock invoke clean.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit (pre-deploy validation)">
      <step>
        <run>comp-platinum reverse 'platinum/advisors/*/exec_summary.json'</run>
        <expect>PRODUCER=exec-summary-generator (post TO 4 deploy). SERVED_VIA=getAdvisorExecSummary (consumed by AdvisorPublicProfile per PRD §7 TO 6). Pre-deploy: PRODUCER may be empty or show D_04-prefix-match stale — that's OK. Post-TO-4-deploy: must show exec-summary-generator.</expect>
        <if_mismatch>If post-deploy PRODUCER is not exec-summary-generator, something in TF pipeline diverged — surface to DT 0.4 + COO.</if_mismatch>
      </step>
      <step>
        <run>aws lambda invoke --function-name exec-summary-generator --payload ... (after TO 4 deploys)</run>
        <expect>S3 artifacts written for ≥ 1 advisor in sample invocation; CloudWatch metrics emit; no PII-assert failures.</expect>
        <if_mismatch>Investigate prompt or trigger_eval wiring.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-bd/platinum/advisors/ --recursive | grep '/exec_summary.json$' | head -5</run>
        <expect>Post first nightly run with EventBridge (TO 7 close): artifacts populated for ~45 active 49F advisors within 90 min of gold-chain-complete signal per PRD §10 AC #1.</expect>
        <if_mismatch>Timing breach — investigate Lambda concurrency or EventBridge trigger.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Per Compiler Mandate Auto-Rule 4. TO 2 is a platinum-tier consumer + platinum-tier producer. It reads `platinum/advisors/*.json` + `platinum/leaderboards/*.json` and writes `platinum/advisors/*/exec_summary.json`. It does NOT modify any silver-tier converter, bronze-tier ingestion, or any script writing to `silver/*` or `bronze/*` prefixes. No data-reprocess implications upstream or downstream; exec_summary.json populates on first post-TO-7-wiring EventBridge fire, forward-only emit.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    <shared_resource artifact="platinum/advisors/{id}/exec_summary.json">
      Producer: TO 2 (this TO). Consumer: TO 6 DE (portal AdvisorPublicProfile useAdvisorExecSummary hook; PRD §7 TO 6 stub shipped e8651920; full wire TBD post-TO-2 close). Schema §3 is the binding contract.
    </shared_resource>
    <shared_resource artifact="platinum/advisors/{id}/positions.json">
      Read-only dependency. Producer: POSITIONS TO (D_04 Step 15, 13eaca78 shipped, Phase 3 verification pending 23:00Z). §4.5 schema + edge-case semantics (7b052d6f) locked.
    </shared_resource>
    <shared_resource file="data/black_diamond/scripts/exec_summary/trigger_eval.py">
      Read-only. TO 1 shipped 8cc69bab. DO NOT MODIFY. If slot-trigger behavior needs adjustment, author a follow-on TO — never edit TO 1 artifact in this TO.
    </shared_resource>
    <shared_resource file="infra/aws/lambda/exec-summary-generator/">
      Single-writer: this TO. Lambda directory new. DT TO 4 owns Terraform wiring (post-this-TO close); does not modify Python source.
    </shared_resource>
    <downstream_pending>
      - ADVI_49EXEC.004 dt-generator-lambda-terraform — DT 0.4 TF apply + tag gates on this TO close (testable Lambda artifact in repo)
      - ADVI_49EXEC.007 dt-eventbridge-wiring-and-deploy — DT 0.4 gates on TO 4 close
    </downstream_pending>
    <auto_rule_4_check>
      Auto-Rule 4 applicability: NO — platinum consumer + platinum producer, no silver/bronze writes. `<data_reprocess_scope><no_reprocess_needed>` block captures reasoning per mandate.
    </auto_rule_4_check>
  </cross_domain_coordination>

  <dependencies>
    <dependency to="ADVI_49EXEC.001" status="complete" required="trigger_eval.py 6 slot evaluators shipped 8cc69bab"/>
    <dependency to="ADVI_49EXEC.003" status="complete" required="anthropic-sdk-deps layer shipped c0a00bcc"/>
    <dependency to="ADVI_49EXEC.005" status="complete" required="D_04 prior_week leaderboard rotation shipped 8cc69bab"/>
    <dependency to="ADVI_49EXEC.POSITIONS" status="complete" required="D_04 Step 15 positions.json emit shipped 13eaca78; contract-locked; Phase 3 verification tonight 23:00Z"/>
  </dependencies>

  <do_not>
    <rule>Do NOT modify `trigger_eval.py` (TO 1 artifact, 8cc69bab). If slot-trigger behavior needs adjustment, author a separate TO.</rule>
    <rule>Do NOT bypass /claude-api skill invocation. All Claude calls MUST follow skill patterns (caching, pinning, structured, explicit model ID).</rule>
    <rule>Do NOT use an alias for the model ID. Explicit `claude-sonnet-4-6` only.</rule>
    <rule>Do NOT chase strict wash-sale compliance (per assumption id="wash-sale-30d-heuristic"). V1 scope uses the 30d holding-period heuristic.</rule>
    <rule>Do NOT skip the PII assertion in code path even though pseudonymization makes hits unlikely. Defense-in-depth per PRD §5.1.</rule>
    <rule>Do NOT emit exec_summary.json for inactive advisors. Active-set enumeration mirrors POSITIONS.json emit set (same upstream).</rule>
    <rule>Do NOT write to any S3 path outside `platinum/advisors/*/exec_summary.json`. All other paths are read-only for this Lambda.</rule>
    <rule>Do NOT skip `from __future__ import annotations` on any Lambda module — Rule 15 (pending ADHC_DSFLOW.004) applies proactively.</rule>
    <rule>Do NOT retroactively backfill exec_summary.json for historical dates. Forward-emit only; first emit on first post-TO-7-wiring EventBridge fire.</rule>
  </do_not>
</task_order>
