<task_order>
  <metadata>
    <id>ADVI_STAUDT.BFIX2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-20</date>
    <status>dispatched</status><!-- DISPATCHED 20260420T17:25Z by 2.0.0_SA_COO. Andrew approval 2026-04-20 in chat ("Agreed on all counts go ahead") on engine refinement plan. -->
    <project_code>ADVI_STAUDT</project_code>
    <priority>P1 — engine refinement, bundled with BFIX1 in same ~A wave (same script B_00.canonical_holdings.py). Closes 38% of the firm AUA accuracy gap ($18.5M of $48.3M).</priority>
    <lane>~A — bundled with BFIX1.</lane>
    <bug_reference>~A engine accuracy report 20260420T (data/black_diamond/diagnostics/STAUDT/engine_accuracy_2026-04-20.md §"#3 — Truly non-Schwab dropped"): 62 accounts not in `schwab_bd_account_mapping` at all are dropped at the canonical layer. B_00 may simply skip them rather than passing them through as BD-authoritative. Includes insurance, annuity, 401K plan, BrokerageLink accounts. $18.5M MV total = 38% of the -284bps firm AUA gap.</bug_reference>
    <decision_authority>Andrew chat 2026-04-20 ("Agreed on all counts go ahead") on engine refinement plan.</decision_authority>
  </metadata>

  <references>
    <ref type="diagnostic">data/black_diamond/diagnostics/STAUDT/engine_accuracy_2026-04-20.md §"#3"</ref>
    <ref type="related-fix">ADVI_STAUDT.BFIX1 — bundled. bd_stale predicate tightening. Same script, same commit.</ref>
    <ref type="related-context">engine_accuracy §"#4 — Non-Schwab kept overshoot (+$16M)" — partial offset to BFIX2's expected gain. After BFIX1+BFIX2: net firm AUA likely ~+$8M overshoot side, within 50bps.</ref>
  </references>

  <objective>
    Add a `bd_only` pass-through code path in B_00.canonical_holdings.py so that accounts NOT in `schwab_bd_account_mapping` are admitted to canonical/holdings using BD positions data directly (units + price from BD), without attempting Schwab reconciliation. Recovers ~$18.5M of MV currently dropped at the canonical layer for 62 truly-non-Schwab accounts (insurance, annuity, 401K plans, BrokerageLink). Closes 38% of the firm AUA accuracy gap.
  </objective>

  <scope>
    **Defect (verbatim from engine_accuracy_2026-04-20.md §"#3"):**
    62 accounts aren't in `schwab_bd_account_mapping` at all and don't survive into canonical. They include the chunk of insurance, annuity, 401K plan, and BrokerageLink accounts profiled earlier. Without Schwab feeds to reconcile against, B_00 may simply skip them rather than passing them through as BD-authoritative.

    **Fix surface — B_00.canonical_holdings.py:**
    Add a new code path that activates when an account ID is NOT in `schwab_bd_account_mapping`. For these accounts, write canonical rows with:
    - `units` = BD positions units (no reconciliation)
    - `price` = BD positions price (or canonical_prices.parquet if present, document choice)
    - `source` = `'bd_only'` (or whatever the existing source-tracking column is — ~A confirms in Phase 0)
    - `nna_txn` = BD transactions sum (same logic as today's bd_stale=False path, just without Schwab anchor)

    The path should be additive — does NOT modify existing reconciled-Schwab path or current bd_stale logic (BFIX1 owns that).

    **Acceptance per engine_accuracy §"#3":** 62 accounts admitted to canonical with non-zero MV summing to ~$18.5M ± tolerance. Per-account spot check on 3-5 of the named accounts (~A picks representative samples from insurance / annuity / 401K plan / BrokerageLink).

    **Source code path preference:**
    - If `silver/positions/` or `silver/holdings_lots` already contains BD positions data for these 62 accounts, BFIX2's pass-through reads from there
    - If BD positions only exist in bronze, escalate — that's a deeper ingestion question
    - Confirm the data source in Phase 0 via comp-pipescript io B_00 + grep for non-Schwab handling

    **Coordination with §"#4" overshoot:**
    The diagnostic notes a +$16M overshoot in 559 non-Schwab kept accounts (BFIX2 doesn't change those — they're already in canonical, just over-valued). After BFIX1+BFIX2, the +$16M overshoot becomes more visible. Document this as a known follow-up; not BFIX2 scope.

    **OUT OF SCOPE:**
    - Schwab kept undershoot ($19.5M, ~A drilling separately) — separate fix
    - Non-Schwab kept overshoot (+$16M) — separate diagnostic post-BFIX1+2
    - Pricing methodology unification — separate concern
    - bd_stale predicate logic — that's BFIX1, bundled but separate scope
    - Bronze-layer ingestion changes — out of scope; if needed, scope an AE TO
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="pre-fix diligence (bundled with BFIX1 Phase 0)">
      <step>
        <run>Read B_00.canonical_holdings.py — locate the current account-iteration loop. Identify the implicit "if account in mapping" gate and where non-mapped accounts currently fall off.</run>
        <expect>Clear gate location + drop point. Confirm the 62 accounts truly fall off (no silent inclusion via a default branch).</expect>
        <if_mismatch>If non-mapped accounts are silently included via a different code path, BFIX2 may be moot. Escalate.</if_mismatch>
      </step>
      <step>
        <run>Identify BD positions source for non-mapped accounts. Check silver/positions, silver/holdings_lots, and bronze/positions if needed.</run>
        <expect>Source confirmed at silver-layer. Document the read path for the new bd_only branch.</expect>
        <if_mismatch>If only available at bronze, escalate — needs ingestion work or AE coordination.</if_mismatch>
      </step>
      <step>
        <run>Numerical preview: count exactly how many accounts are in BD positions/transactions but NOT in schwab_bd_account_mapping. Confirm matches the diagnostic figure of 62 accounts / ~$18.5M.</run>
        <expect>62 accounts ± few, $18.5M ± $1M.</expect>
        <if_mismatch>Significant baseline drift = re-validate before patching.</if_mismatch>
      </step>
      <step>
        <run>Identify representative sample accounts for Phase 1 spot-check (3-5 accounts: 1 insurance, 1 annuity, 1 401K plan, 1 BrokerageLink). Document name + BD MV for post-patch verification.</run>
        <expect>Representative sample documented in Phase 0 evidence.</expect>
        <if_mismatch>If no representative sample available (e.g., only one cohort in the 62), document.</if_mismatch>
      </step>
      <step>
        <run>MCP COO with bundled BFIX1+BFIX2 Phase 0: BFIX1 direction choice + BFIX2 source confirmation + sample accounts + intended combined patch shape.</run>
        <expect>COO ACK + GO before patching</expect>
        <if_mismatch>If COO objects, iterate</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="patch + validation (bundled with BFIX1)">
      <step>
        <run>Apply BFIX2 path additively in same commit as BFIX1. New `bd_only` branch in account loop, no logic changes to existing branches.</run>
        <expect>Single commit covering both fixes. Diff shows: BFIX1 predicate tightening + BFIX2 new branch addition.</expect>
        <if_mismatch>Any modification to existing reconciled-Schwab path = scope creep, escalate.</if_mismatch>
      </step>
      <step>
        <run>Local dry-run B_00 + downstream C_01 on current prod date. Verify the 62 non-Schwab-mapped accounts now appear in canonical/holdings with non-zero MV.</run>
        <expect>62 accounts present in canonical, MV sum ~$18.5M. Sample accounts (per Phase 0 list) match BD MV within tolerance.</expect>
        <if_mismatch>Missing accounts or MV mismatch = path didn't activate or wrong source. Fix.</if_mismatch>
      </step>
      <step>
        <run>End-to-end firm AUA: re-run engine_accuracy diagnostic post BFIX1+BFIX2. Confirm gap to BD silver/allocations within 50bps.</run>
        <expect>Combined fix lands firm AUA within ±$9.7M of BD silver. Likely ~+$8M overshoot side per diagnostic forecast.</expect>
        <if_mismatch>Gap not closing = mechanism understanding wrong. Halt + escalate.</if_mismatch>
      </step>
      <step>
        <run>comp-validate B_00 + downstream C_01</run>
        <expect>Exit 0 for both.</expect>
        <if_mismatch>Exit != 0 = fix incomplete</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/scripts/silver/B_00.canonical_holdings.py</path>
      <description>New `bd_only` pass-through branch added to non-mapped account handling. Bundled with BFIX1 in same commit.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/scripts/gold/gold_validate_config.yaml</path>
      <description>Add sentinel: canonical/holdings should contain ≥ ~6,500 accounts post-fix (vs ~5,967 today). And: source-distribution check (bd_only ≥ 50 accounts).</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/BFIX2/bfix2_evidence.md</path>
      <description>Phase 0 source identification + Phase 1 per-account MV diff + sample account spot-check (insurance/annuity/401K/BrokerageLink) + bundled firm-level AUA close-out.</description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] Phase 0 BFIX2 source identification + sample account list MCP'd bundled with BFIX1 Phase 0
    - [ ] Single ~A commit covering BFIX1 + BFIX2 on B_00
    - [ ] Post-patch: 62 (or close) non-Schwab-mapped accounts admitted to canonical with non-zero MV
    - [ ] Sample 3-5 accounts (insurance/annuity/401K/BrokerageLink) MV matches BD positions within 1%
    - [ ] No regression on existing canonical accounts (reconciled-Schwab path unchanged)
    - [ ] Combined BFIX1+BFIX2 closes firm AUA gap to within 50bps of BD silver/allocations
    - [ ] comp-validate B_00 + canonical/holdings exit 0
    - [ ] DT upload from `git show {sha}:path` (committed-ref pattern)
    - [ ] Pre-flag CTO+COO before B_00 S3 upload (silver-layer falls under A→D-rerun-sensitive rule)
  </acceptance_criteria>

  <guardrails>
    - **Additive only:** new code path for non-mapped accounts; do NOT touch reconciled-Schwab path or BFIX1's bd_stale predicate work (different lines in same commit, fine).
    - **No source-of-truth changes** for BD positions — read from existing silver/positions or silver/holdings_lots as-is.
    - **Bundled with BFIX1.** Single commit, single S3 upload, single qa-runner cycle.
    - **Non-Schwab kept overshoot (+$16M) is OUT OF SCOPE** — that's a follow-up diagnostic after BFIX1+BFIX2 lands. Don't try to fix the overshoot in this TO; the diagnostic forecasts ~+$8M net within 50bps tolerance, which is acceptable.
    - **No emojis, selective staging, agent commit identity, working-tree S3 upload prohibition** per existing memory rules.
  </guardrails>

  <agent_context_setup>
    1. Same context as BFIX1 (you authored the diagnostic; you have it)
    2. Add: B_00 account-iteration loop + non-Schwab handling (or absence of)
    3. silver/positions or silver/holdings_lots structure (BD positions data source)
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1: ACK bundled with BFIX1
    - Phase 0 gate: bundled MCP
    - Phase 1 gate: bundled MCP — sample-account spot-check + firm-level AUA pre/post
    - RAVC step 4: bundled DT push + S3 upload + qa-runner B-layer + acceptance evidence
  </completion_protocol>
</task_order>
