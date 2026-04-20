<task_order>
  <metadata>
    <id>ADVI_STAUDT.FIX2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-20</date>
    <status>draft</status>
    <project_code>ADVI_STAUDT</project_code>
    <priority>P0 (dependent on FIX-TO 1). Expected to self-resolve for most advisors after FIX-TO 1 completes; residual cases need explicit handling.</priority>
    <lane>~B — picks this up AFTER FIX-TO 1 closes. Same lane, same context, same D_00c working tree. Do NOT hand off to a different instance.</lane>
    <bug_reference>Bug 2 per SYNTHESIS/bug_attribution.md — D_00c no_fee_aua silent max(0, ...) clip. ~148/152 advisors no_fee=0 at T3.</bug_reference>
    <depends_on>ADVI_STAUDT.FIX1 — must land + deploy + validate before this TO executes.</depends_on>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md §3.0 (Class 2 — fee-split)</ref>
    <ref type="handoff">data/black_diamond/diagnostics/STAUDT/SYNTHESIS/coo_handoff.md §FIX-TO 2</ref>
    <ref type="attribution">data/black_diamond/diagnostics/STAUDT/SYNTHESIS/bug_attribution.md Bug 2</ref>
    <ref type="decomposition">data/black_diamond/diagnostics/STAUDT/SYNTHESIS/group_d_tagged_aua_decomposition.md</ref>
    <ref type="upstream-mcp">CTO 20260420T134734Z (fix-TO wave authorization)</ref>
  </references>

  <objective>
    After FIX-TO 1 restores `_weighted_aua` so that advisors' tagged_aua is correct, re-run D_00c and audit the residual no_fee=0 population. For most advisors Bug 2 self-resolves (Bug 1 was making `tagged_aua` artificially small, so `no_fee = max(0, tagged_aua - fee_aua)` clipped to 0 because fee_aua > artificially-small tagged_aua). For advisors where `fee_aua > true tagged_aua` still exists post-FIX-1, apply explicit handling — a silent `max(0, …)` clip is not acceptable; the case needs a principled computation or an explicit error surfacing.
  </objective>

  <scope>
    **Defect (verbatim from bug_attribution.md Bug 2):**
    `no_fee_aua = max(0.0, tagged_aua - fee_aua)` at D_00c L565 silently clips negative values to 0. With Bug 1 reducing tagged_aua to ~20% of actual, `fee_aua > tagged_aua` for nearly all advisors → clips to 0. ~148/152 advisors affected at T3.

    **Source file:**
    `data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py`
    - `no_fee_aua = max(0.0, tagged_aua - fee_aua)` at L565
    - Context L553-L571 (fee_breakdown construction)
    - Downstream: `'aua': round(no_fee_aua, 2)` at L605 (fee_breakdown.no_fee.aua)

    **Expected state after FIX-TO 1:**
    - Most advisors: tagged_aua returns to true value → fee_aua ≤ tagged_aua → no_fee_aua positive → Bug 2 naturally resolves
    - Residual cases: advisors where fee_aua > true tagged_aua (fundamental data inconsistency, not a clip bug)

    **What DS must do:**
    1. Confirm FIX-TO 1 has deployed + run end-to-end (do NOT start FIX-TO 2 work before confirming)
    2. Re-run D_00c and count advisors with `no_fee.aua == 0`
    3. If residual count ≤ 5: verify each residual case has a genuine data reason (e.g., advisor truly has no no-fee accounts) vs a latent second bug
       - For each residual: dump `tagged_aua`, `fee_aua`, `fee_breakdown.fee_paying.aua`, raw account list, billable flag distribution
       - If genuine: document in evidence file, no code change needed (but add the documentation)
    4. If residual count > 5: audit `fee_aua` computation vs true `tagged_aua` for those advisors → root-cause the overage → fix with explicit handling (not silent clip)
    5. Replace silent `max(0, …)` at L565 with explicit handling:
       - Happy path: `no_fee_aua = tagged_aua - fee_aua` (no clip needed if invariant holds)
       - If negative is still possible after FIX-1: emit a WARN log with (advisor, tagged_aua, fee_aua, delta) + explicit documented behavior for the edge case (NOT a silent zero)

    **Mandatory invariant to restore:**
    ```
    For every advisor a in the leaderboard output:
      a.fee_breakdown.fee_paying.aua + a.fee_breakdown.no_fee.aua == a.tagged_aua
    ```
    Tolerance: exact to 2 decimal places.

    **OUT OF SCOPE:**
    - Anything FIX-TO 1 covers (weight normalization)
    - Anything FIX-TO 3A covers (NNA path)
    - D_04 fee_breakdown handling (different surface; if parallel bug, file separate TO)
    - Fee-paying account classification logic (`billable_account_ids` + `split_pct > 0` filter) — unless residual investigation pins the bug there
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="pre-fix diligence (AFTER FIX-TO 1 deployed + validated)">
      <step>
        <run>Verify FIX-TO 1 is deployed — check bd-gold-trigger run log + comp-validate output + COO close MCP.</run>
        <expect>FIX-TO 1 status=complete in project registry; deployed commit SHA known.</expect>
        <if_mismatch>STOP. FIX-TO 2 cannot start before FIX-TO 1 is complete. MCP COO asking for FIX-TO 1 ETA.</if_mismatch>
      </step>
      <step>
        <run>Re-run D_00c against current prod date and count `no_fee.aua == 0` advisors</run>
        <expect>Count substantially less than 148 (ideally 0-5). Document exact count.</expect>
        <if_mismatch>If count is still ~148, FIX-TO 1 didn't land. Re-verify FIX-TO 1 deploy + invariant 1 before proceeding.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io D_00c.portal_leaderboard</run>
        <expect>Confirm fee_aua + tagged_aua column sources unchanged post-FIX-1. No new column gaps.</expect>
        <if_mismatch>Any new gap = escalate to COO before touching L565.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="post-fix validation">
      <step>
        <run>Re-run D_00c end-to-end; validate invariant 2 on output</run>
        <expect>`fee_paying.aua + no_fee.aua == tagged_aua` for all 152 advisors to 2dp.</expect>
        <if_mismatch>Fix incomplete; investigate the failing advisor's raw rows.</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_00c.portal_leaderboard --artifact /tmp/leaderboard.json</run>
        <expect>Exit 0. Add an invariant check to gold_validate_config.yaml for this computation if one doesn't already exist.</expect>
        <if_mismatch>Exit != 0 = fix incomplete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py</path>
      <description>
        Minimum-surface patch at or near L565. If residual count is 0 after FIX-1, ONLY replace the silent clip with documented explicit form (and add assertion or WARN for negative delta). If residual count > 0, fix the underlying computation and apply the explicit form.
      </description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/FIX2/fix_to_2_evidence.md</path>
      <description>
        Post-FIX-1 residual no_fee=0 count, per-advisor dump of any genuine residual (≤5 expected), mechanism note for any non-genuine residual found, invariant-2 validation.
      </description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/gold_validate_config.yaml</path>
      <description>
        If an invariant check for `fee_paying.aua + no_fee.aua == tagged_aua` does not exist, add it.
      </description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] FIX-TO 1 confirmed deployed + validated BEFORE any FIX-TO 2 work begins
    - [ ] Post-FIX-1 residual no_fee=0 count documented in fix_to_2_evidence.md
    - [ ] Silent `max(0, …)` at L565 replaced with explicit form (happy path if invariant holds, or explicit WARN/handling if edge case persists)
    - [ ] `fee_paying.aua + no_fee.aua == tagged_aua` holds for all 152 advisors post-run (to 2dp)
    - [ ] No regression to invariant 1 (sum(role_breakdown[*].aua) == tagged_aua still holds)
    - [ ] comp-validate D_00c exits 0
    - [ ] Regression invariant added to gold_validate_config.yaml
    - [ ] Script deployed + run end-to-end via standard DS cycle; production artifact validated
  </acceptance_criteria>

  <guardrails>
    - **Sequencing is strict:** FIX-TO 2 cannot start until FIX-TO 1 is complete. If no_fee counts don't drop after FIX-TO 1, either FIX-TO 1 didn't land correctly OR Bug 2 is independent — investigate before patching.
    - **No emojis in code** (CLAUDE.md #13)
    - **Selective staging + agent commit identity** per `feedback_selective_staging_only.md` + `feedback_commit_only_flag.md`
    - **Single-TO focus:** if investigation reveals `fee_aua` itself is computed wrong (not just the clip), that is a scope expansion — stop and MCP COO; do not silently broaden.
  </guardrails>

  <agent_context_setup>
    1. Register + inbox-watch (first two tool calls)
    2. Read:
       - docs/architecture/ADVI_STAUDT.md §3.0 + §4.4
       - SYNTHESIS/coo_handoff.md §FIX-TO 2
       - SYNTHESIS/bug_attribution.md Bug 2
       - FIX1 evidence file (to understand what changed + residual state)
       - D_00c.portal_leaderboard.py L540-L620
    3. Confirm FIX-TO 1 is status=complete in project registry before starting
    4. Heartbeat every 60s during active work
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1 (Acknowledge): within 5 min of receipt, MCP COO with "ACK STAUDT.FIX2 — waiting on FIX-TO 1 close before starting"
    - When FIX-TO 1 closes: MCP COO "STAUDT.FIX2 starting Phase 0"
    - Phase 0 gate: MCP COO with residual count + per-advisor dump summary before patching L565
    - RAVC step 4 (Close): MCP COO with deploy commit SHA + invariant-2 validation evidence
  </completion_protocol>
</task_order>
