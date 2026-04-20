<task_order>
  <metadata>
    <id>ADVI_STAUDT.KPI</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-20</date>
    <status>dispatched</status><!-- DISPATCHED 20260420T17:25Z by 2.0.0_SA_COO. Andrew approval 2026-04-20 in chat ("Agreed on all counts go ahead") on engine refinement plan (1)+(2). -->
    <project_code>ADVI_STAUDT</project_code>
    <priority>P2 — engine quality framework, no time pressure. Codifies the 50bps firm AUA accuracy target as a regression sentinel + makes the loss-decomposition diagnostic re-runnable. Independent of qa-runner watchdog incident; can author + draft now.</priority>
    <lane>~C — idle post-FIX5 close. Independent lane from BFIX1+BFIX2 (~A). KPI work doesn't conflict with B_00 patching (different files).</lane>
    <bug_reference>~A engine_accuracy_2026-04-20.md identified 50bps target (= $8.5M tolerance) and current state at -284bps. KPI need: codify the target as a production gate so future drift is caught automatically, not via ad-hoc investigation.</bug_reference>
    <decision_authority>Andrew chat 2026-04-20 ("Agreed on all counts go ahead") on engine refinement plan (2).</decision_authority>
  </metadata>

  <references>
    <ref type="diagnostic">data/black_diamond/diagnostics/STAUDT/engine_accuracy_2026-04-20.md (~A's loss-decomposition methodology + 50bps framing)</ref>
    <ref type="paired-fixes">ADVI_STAUDT.BFIX1 + BFIX2 (~A lane) — these fixes close the current -284bps gap. KPI sentinel becomes the regression gate after BFIX1+BFIX2 land.</ref>
    <ref type="config-precedent">data/black_diamond/scripts/gold/gold_validate_config.yaml (existing per-script sentinels for D_00c, D_04, etc. — KPI extends this to firm-level engine accuracy)</ref>
  </references>

  <objective>
    Codify firm AUA accuracy (within 50bps of BD silver/allocations) as an automated regression sentinel in `gold_validate_config.yaml`. Build a re-runnable loss-decomposition diagnostic so the per-mechanism accuracy breakdown (Schwab undershoot / non-Schwab dropped / overshoot / etc.) can be tracked over time. Convert engine accuracy from "ad-hoc investigation when something breaks" to "first-class production metric tracked every run."
  </objective>

  <scope>
    **Two deliverables:**

    **(1) `gold_validate_config.yaml` sentinel — firm AUA accuracy gate:**
    Add a new validator entry (severity ERROR) that:
    - Reads `gold/firm_composition.json` (current canonical firm AUA)
    - Reads `silver/allocations/{latest_date}.parquet` (current BD silver firm MV)
    - Computes `abs(canonical_firm_aua - bd_silver_firm_mv) / bd_silver_firm_mv`
    - Fails if > 50bps (0.005)
    - Optional WARN tier at 25bps for early warning

    Plus auxiliary sentinels:
    - Schwab-cohort accuracy: `abs(canonical_schwab_mv - bd_silver_schwab_mv) / bd_silver_schwab_mv ≤ 50bps` (ERROR)
    - Non-Schwab-cohort accuracy: same target (ERROR; tighter cohort highlights regressions)
    - Account count parity: `canonical_account_count >= bd_silver_account_count - 5` (WARN; catches account-drop regressions)

    **(2) Re-runnable diagnostic at `data/black_diamond/scripts/diagnostics/engine_accuracy_diagnostic.py`:**
    Convert ~A's manual analysis methodology into a Python script that:
    - Pulls current BD silver/allocations + canonical/holdings + canonical/nna + firm_composition.json
    - Stratifies by Schwab-mapped vs non-Schwab cohort
    - Computes the 5-mechanism loss decomposition (bd_stale overreach / Schwab kept undershoot / non-Schwab dropped / non-Schwab kept overshoot / Schwab-mapped dropped)
    - Outputs Markdown report mirroring the structure of engine_accuracy_2026-04-20.md
    - Run via `python data/black_diamond/scripts/diagnostics/engine_accuracy_diagnostic.py --date YYYY-MM-DD --output {path}`
    - Default output: `data/black_diamond/diagnostics/STAUDT/engine_accuracy_{date}.md`

    **Coordination with BFIX1 + BFIX2:**
    - The sentinel will FAIL today (-284bps) until BFIX1+BFIX2 land
    - Add the sentinel as DISABLED initially (commented out OR with `enabled: false` flag)
    - Enable the sentinel ONLY after BFIX1+BFIX2 close + qa-runner validates < 50bps
    - Coordinate enablement timing with ~A in their RAVC4

    **Compiler-tools verification:**
    - comp-validate must support the new validator entry; if `gold_validate_config.yaml` schema doesn't have a "cross-source-comparison" validator type, scope a minimal extension to the comp-validate runtime (or use a script-based validator that comp-validate invokes)

    **OUT OF SCOPE:**
    - Engine FIX execution (BFIX1+BFIX2 own that)
    - Per-account drill-down beyond what the diagnostic computes (separate per-account audit script if needed later)
    - Multi-source pricing reconciliation (separate concern)
    - Historical accuracy backfill (the diagnostic is forward-looking; no need to compute historical 50bps on every prior date)
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="pre-build diligence">
      <step>
        <run>Read existing gold_validate_config.yaml + comp-validate source. Identify whether cross-source-comparison sentinels already exist (e.g., comparing two artifacts).</run>
        <expect>Either a precedent exists (use that pattern) or a new validator type is needed (scope the addition).</expect>
        <if_mismatch>If comp-validate can only compare a single artifact against fixed thresholds, the cross-source check needs to be a script-validator pattern (script computes ratio, sentinel checks script's output JSON).</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io on canonical/holdings + firm_composition.json producers — identify what date the firm_composition is computed for (latest available date vs trailing date)</run>
        <expect>Date alignment: silver/allocations and firm_composition both reflect the same trading date.</expect>
        <if_mismatch>If date alignment is off-by-one or different, the sentinel must account for that.</if_mismatch>
      </step>
      <step>
        <run>MCP COO with: chosen sentinel pattern (native vs script-validator), date-alignment confirmation, intended config + script structure.</run>
        <expect>COO ACK + GO before building.</expect>
        <if_mismatch>If COO objects, iterate.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="build + validation">
      <step>
        <run>Build the engine_accuracy_diagnostic.py script. Test against the 2026-04-16 date (matches ~A's manual report).</run>
        <expect>Script output ≈ ~A's manual report. Topline -284bps gap reproduces. Loss decomposition mechanism counts within 5%.</expect>
        <if_mismatch>If script output diverges materially from ~A's manual numbers, debug. ~A's manual is ground truth for 2026-04-16.</if_mismatch>
      </step>
      <step>
        <run>Add gold_validate_config.yaml sentinel entries (DISABLED initially per BFIX1+BFIX2 coordination)</run>
        <expect>Config syntax valid. comp-validate parses without error. Sentinel doesn't fire (because disabled).</expect>
        <if_mismatch>Config syntax error = fix.</if_mismatch>
      </step>
      <step>
        <run>Document enablement procedure in BFIX1+BFIX2 RAVC4 expectation: "When BFIX1+BFIX2 close + firm AUA within 50bps, flip KPI sentinel `enabled: true` and verify comp-validate exit 0."</run>
        <expect>Procedure documented; ~A acknowledges in their RAVC4 plan.</expect>
        <if_mismatch>If procedure unclear, iterate with ~A.</if_mismatch>
      </step>
      <step>
        <run>comp-validate dry-run with sentinel enabled (locally only, not deployed) on a hypothetical post-BFIX1+BFIX2 firm AUA value to confirm sentinel logic works.</run>
        <expect>Sentinel exit 0 when AUA within 50bps; exit != 0 otherwise.</expect>
        <if_mismatch>Sentinel logic broken = fix.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/scripts/diagnostics/engine_accuracy_diagnostic.py</path>
      <description>Re-runnable engine accuracy report generator. CLI: --date + --output. Default: today + diagnostics/STAUDT/engine_accuracy_{date}.md.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/scripts/gold/gold_validate_config.yaml</path>
      <description>New sentinels for firm AUA 50bps + Schwab/non-Schwab cohort 50bps + account count parity. Initially DISABLED; enabled post-BFIX1+BFIX2 close.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/KPI/kpi_evidence.md</path>
      <description>Phase 0 sentinel pattern choice + Phase 1 diagnostic-script vs manual-report parity check + sentinel-logic dry-run + enablement procedure documentation.</description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] engine_accuracy_diagnostic.py reproduces ~A's manual report numbers within 5% for 2026-04-16
    - [ ] gold_validate_config.yaml sentinels added (firm AUA + cohort + account count)
    - [ ] Sentinels DISABLED initially with clear enablement procedure documented
    - [ ] comp-validate parses config without error
    - [ ] Sentinel-logic dry-run confirms exit 0 / non-zero behavior at 50bps boundary
    - [ ] Enablement procedure coordinated with ~A's BFIX1+BFIX2 RAVC4
    - [ ] Diagnostic script committed; can be run by anyone via `python ... --date 2026-MM-DD`
  </acceptance_criteria>

  <guardrails>
    - **Sentinels DISABLED initially.** Do NOT enable a sentinel that will fail in current state — that breaks every qa-runner cycle. Coordinate enablement with ~A's RAVC4.
    - **No engine fix logic.** KPI is observability + regression gate ONLY. BFIX1+BFIX2 own the actual fixes.
    - **No B_00 modifications.** ~A is patching B_00; you are NOT to touch it. Different files = no merge conflict.
    - **Diagnostic script must match manual methodology.** ~A's report is ground truth for 2026-04-16; if the script's automated numbers don't match within 5%, debug the script (not the report).
    - **DT push + S3 upload from `git show {sha}:path`** — diagnostic + config goes via standard deploy.
    - **No emojis, selective staging, agent commit identity** per existing memory rules.
  </guardrails>

  <agent_context_setup>
    1. Register + inbox-watch (first two tool calls)
    2. Read:
       - data/black_diamond/diagnostics/STAUDT/engine_accuracy_2026-04-20.md (manual report = ground truth)
       - data/black_diamond/scripts/gold/gold_validate_config.yaml (existing sentinel pattern)
       - .tools/comp-validate (or wherever comp-validate source lives — find via `which comp-validate` + readlink)
       - data/black_diamond/scripts/silver/B_00.canonical_holdings.py (just enough to understand the canonical/holdings output schema; you are NOT modifying this)
    3. Heartbeat every 60s during active work
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1: ACK within 5 min: "ACK STAUDT.KPI — starting Phase 0 sentinel pattern + comp-validate audit"
    - Phase 0 gate: MCP COO with sentinel pattern choice + intended config + script structure
    - Phase 1 gate: MCP COO with diagnostic-script vs manual-report parity + sentinel dry-run results
    - RAVC step 4: MCP COO with deploy commit SHA + enablement procedure for ~A coordination
  </completion_protocol>
</task_order>
