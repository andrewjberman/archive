<task_order>
  <metadata>
    <id>ADVI_STAUDT.FIX1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-20</date>
    <status>draft</status>
    <project_code>ADVI_STAUDT</project_code>
    <priority>P0 — firm-wide user-visible crisis. 152/152 advisors fail invariant 1 at T3. Top critical path.</priority>
    <lane>~B — FIX-TO 1 then FIX-TO 2 (sequential on D_00c). ~B owns both in order.</lane>
    <bug_reference>Bug 1 per SYNTHESIS/bug_attribution.md — role_breakdown sum ~20% of tagged_aua (firm-wide).</bug_reference>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md §3.0 (Class 2 — role-split)</ref>
    <ref type="handoff">data/black_diamond/diagnostics/STAUDT/SYNTHESIS/coo_handoff.md §FIX-TO 1</ref>
    <ref type="attribution">data/black_diamond/diagnostics/STAUDT/SYNTHESIS/bug_attribution.md Bug 1</ref>
    <ref type="decomposition">data/black_diamond/diagnostics/STAUDT/SYNTHESIS/group_d_tagged_aua_decomposition.md (three independent tagged_aua derivations)</ref>
    <ref type="upstream-mcp">CTO 20260420T134734Z (fix-TO wave authorization, Option A interim)</ref>
    <ref type="root-commits">0804b377 (2026-04-13) + 9f6faf9 (DE allChecked early-return removal)</ref>
  </references>

  <objective>
    Restore the D_00c `_compute_split_weight()` + `_weighted_aua` chain so that for every advisor, `sum(role_breakdown[*].aua) == tagged_aua`. Current production state: firm-wide (152/152 advisors) sum is ~20% of tagged_aua. This is a single-script, D-native bug (Layer A CLEAN-BILL; B/C propagation confirmed by ~D to NOT reach this code path). Fix is a surgical logic repair in D_00c.portal_leaderboard.py — NO upstream changes, NO C-layer edits, NO refactors beyond the weight-normalization chain.
  </objective>

  <scope>
    **Defect (verbatim from SYNTHESIS/bug_attribution.md Bug 1):**
    `_compute_split_weight()` returns ~0.20 weight per role instead of distributing weights that sum to 1.0 per (account_id, advisor) group. Each `_weighted_aua = total_aua * _split_weight` produces ~20% of total_aua, so the role_breakdown array sums to ~20% of tagged_aua total.

    **Source file (all citations against CLOUD tip, 2026-04-20):**
    `data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py`
    - `_compute_split_weight(grp)` at L839 (three-case rule: all_fp / none_fp / mixed)
    - `melted['_split_weight'] = melted.groupby(['account_id', 'advisor'], group_keys=False).apply(_compute_split_weight)` at L866-869
    - `melted['_weighted_aua'] = melted['total_aua'] * melted['_split_weight']` at L881
    - `grp_aua = role_rows.groupby('advisor')['_weighted_aua'].sum()` at L893 (feeds `role_breakdown[*].aua` at L898-902)

    **Root-cause commits (per ~D synthesis):**
    - `0804b377` (2026-04-13) — weight-logic alteration
    - `9f6faf9` — DE allChecked early-return removal; interacts with the weight normalization

    **What DS must do — Phase 1 investigation (PRE-FIX):**
    The failing-invariant symptom (rb_sum ≈ 20% × tagged_aua) is firm-wide and stable. ~D confirmed the symptom at T3 but did NOT fully isolate which line produces the 0.2× factor. Possible mechanisms to audit in order:
    1. Does `melted` pre-filter out non-fee-paying rows BEFORE `_weighted_aua` is applied, so the three-case Case-3 "no-fee get 0" cuts ~80% of per-account AUA contribution?
    2. Does the `_is_fee_paying` mask at L832-836 (`billable_account_ids & split_pct > 0`) interact with Case 3 such that the advisor's no-fee roles contribute 0 weight, but no-fee accounts are still in the `total_aua` baseline used by `tagged_aua`?
    3. Is there an asymmetry between which row-set feeds `tagged_aua` (D_00c:528 `row.total_aua` fallback + D_04 override per §3.0 Class 2) vs which row-set feeds `role_breakdown[*].aua` (via `_weighted_aua` aggregation)?
    4. Did `9f6faf9` (DE allChecked early-return removal) change which rows are included in `melted` before the weight computation?

    Do not patch blindly. Identify the specific line(s) that produce the 0.2× factor, write a one-paragraph mechanism note, THEN apply the minimum-surface fix.

    **Invariant to restore (post-fix):**
    ```
    For every advisor a in the leaderboard output:
      sum([rb['aua'] for rb in leaderboard[a]['role_breakdown']]) == leaderboard[a]['tagged_aua']
    ```
    Tolerance: exact to 2 decimal places (the rounding grain used in the output).

    **OUT OF SCOPE:**
    - No changes to `fee_breakdown.no_fee.aua` computation (that is FIX-TO 2, dependent; expect Bug 2 to self-resolve here)
    - No changes to NNA-path constants (that is FIX-TO 3A, parallel)
    - No changes to C-layer / role_aua/ / account_performance (Bug 4, deprioritized)
    - No changes to the `build_advisor_books` path or D_02 (out of this TO's blast radius)
    - No refactors, renames, or "while I'm here" cleanups
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="pre-fix diligence (MANDATORY before any code edit)">
      <step>
        <run>comp-pipescript io D_00c.portal_leaderboard</run>
        <expect>Column gaps report. Confirms your mechanism hypothesis against the actual column-load manifest; surfaces any COLUMN GAP that would change the fix surface. Also enumerates PORTAL CONSUMERS that depend on `role_breakdown[*].aua`.</expect>
        <if_mismatch>If the tool reports a column gap you weren't aware of, pause — MCP COO before proceeding.</if_mismatch>
      </step>
      <step>
        <run>comp-blast _compute_split_weight &amp;&amp; comp-blast _weighted_aua</run>
        <expect>Likely "No nodes matching" per ~D's note (ADHC_ROUTER Phase 2 graph gap for function-level nodes). In that case: manually grep the repo for any other caller of `_compute_split_weight` or consumer of `_weighted_aua` outside D_00c. Document the manual blast in fix_to_1_evidence.md.</expect>
        <if_mismatch>If comp-blast DOES return hits, treat them as required coordination points and list in the fix commit body.</if_mismatch>
      </step>
      <step>
        <run>git log --oneline 0804b377^..HEAD -- data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py</run>
        <expect>Full commit stack affecting D_00c since Bug 1 introduction. Read diffs for `0804b377` and `9f6faf9` specifically; write a mechanism note citing which commit introduced the 0.2× symptom.</expect>
        <if_mismatch>If log shows additional in-window commits not referenced in ~D synthesis, include them in your mechanism note.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="post-fix validation (MANDATORY before signaling complete)">
      <step>
        <run>python data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py --date 2026-04-15 (or current prod date)</run>
        <expect>Script runs to completion. Output `leaderboard.json` artifact produced.</expect>
        <if_mismatch>Any exception or nonzero exit = fix incomplete. Do NOT signal complete; debug and re-run.</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_00c.portal_leaderboard --artifact /tmp/leaderboard.json</run>
        <expect>Exit 0. Config `gold_validate_config.yaml` must include an invariant check for `sum(role_breakdown[*].aua) == tagged_aua` per advisor — if it doesn't, ADD IT as part of this TO (the check must live in config so it catches regression).</expect>
        <if_mismatch>Exit != 0 = fix incomplete. Signal MCP COO with validator output.</if_mismatch>
      </step>
      <step>
        <run>Python one-liner or small scratch script against /tmp/leaderboard.json: `for a in data: assert abs(sum(r['aua'] for r in a['role_breakdown']) - a['tagged_aua']) &lt; 0.01, a['advisor']`</run>
        <expect>Pass for all 152 advisors with zero AssertionError.</expect>
        <if_mismatch>Any advisor fails = fix incomplete. Fix-TO stays open; investigate that advisor's (account_id, role) rows specifically.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py</path>
      <description>Minimum-surface patch restoring the weight-normalization chain. Commit message MUST cite: (a) the specific line(s) that produced the 0.2× factor, (b) the mechanism in one sentence, (c) reference to bug_attribution.md Bug 1.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/FIX1/fix_to_1_evidence.md</path>
      <description>Pre-fix mechanism note (Phase 0 output) + post-fix invariant verification (Phase 1 output). Must include: 152 advisors × rb_sum vs tagged_aua table, or at minimum an assertion that all 152 pass with a sample of 10 shown.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/gold_validate_config.yaml</path>
      <description>If an invariant check for `sum(role_breakdown[*].aua) == tagged_aua` does not already exist, add one for D_00c. Regression protection.</description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] Pre-fix mechanism note written in fix_to_1_evidence.md BEFORE the code patch lands
    - [ ] Patch applied to D_00c.portal_leaderboard.py ONLY (no other files touched except gold_validate_config.yaml)
    - [ ] `sum([rb['aua'] for rb in role_breakdown]) == tagged_aua` holds for all 152 advisors post-run (to 2dp)
    - [ ] No advisor has `role_breakdown[*].aua == 0` for a role where that advisor has confirmed AUA (per ~D decomposition)
    - [ ] comp-validate D_00c exits 0
    - [ ] Regression invariant added to gold_validate_config.yaml
    - [ ] Script deployed + run end-to-end via standard DS gold-script deploy cycle (commit → push → S3 → bd-gold-trigger) per `feedback_ds_commits_ae_deploys.md`
    - [ ] Post-deploy validation artifact pulled from production run; invariant confirmed on live S3 artifact (not just local run)
  </acceptance_criteria>

  <guardrails>
    - **Lane discipline:** DS owns full gold-script deploy cycle (commit + push + S3 + bd-gold-trigger). AE only escalated if deploy cycle fails.
    - **No emojis in code** (CLAUDE.md #13). Plain-ASCII prefixes only in print statements and commit messages.
    - **Selective staging:** `git add data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py data/black_diamond/gold_validate_config.yaml` — never `git add -A`.
    - **Agent commit identity:** `git commit --only --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" -- &lt;paths&gt;`
    - **Pre-flag A→D-rerun-sensitive writes:** if your fix ends up touching `canonical_prices`, `holdings_lots`, or `canonical_nna` S3 writes, pre-flag to CTO+COO BEFORE `aws s3 cp`. This fix should NOT touch those — but if investigation surfaces a dependency, stop and escalate.
    - **Single-TO focus:** if Phase 0 investigation reveals the bug actually lives in C-layer or D_04, STOP and MCP COO. Do not expand scope.
    - **Rebase on ~A's FIX3A commit:** ~A ships FIX-TO 3A (D_00c L35 + L121 constant swap) first. Pull latest CLOUD before starting; rebase cleanly on top of ~A's commit. FIX-TO 1 touches L839-L881 (different function) so textual conflict is unlikely, but confirm after rebase. If conflict: it's textual only — ~A's constant swap lines are unrelated to your weight-chain fix.
  </guardrails>

  <agent_context_setup>
    1. Register with MCP: `register_agent 0.4.0_DS_ClientPlatform` (no tilde suffix per `feedback_ds_addressing_no_tilde.md`)
    2. Launch `bash org/mcp/inbox-watch.sh 0.4.0_DS_ClientPlatform` in background
    3. Read in order:
       - docs/architecture/ADVI_STAUDT.md (PRD, §3.0 + §4.4)
       - data/black_diamond/diagnostics/STAUDT/SYNTHESIS/coo_handoff.md (fix scope)
       - data/black_diamond/diagnostics/STAUDT/SYNTHESIS/bug_attribution.md (Bug 1 section)
       - data/black_diamond/diagnostics/STAUDT/SYNTHESIS/group_d_tagged_aua_decomposition.md (three derivations)
       - data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py (full file, focus L800-L960)
    4. Heartbeat every 60s during active work
    5. RAVC step 1 ACKNOWLEDGE to COO within 5 minutes of receipt
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1 (Acknowledge): within 5 min of receipt, MCP COO with "ACK STAUDT.FIX1 — starting Phase 0 diligence"
    - RAVC step 2/3 (Validate/signal): MCP COO at Phase 0 gate with mechanism note summary before applying patch
    - RAVC step 4 (Close): MCP COO with deploy commit SHA + S3 bd-gold-trigger output + invariant-pass evidence
    - If blocked at any phase: MCP COO with specific blocker; do not wait silently
  </completion_protocol>
</task_order>
