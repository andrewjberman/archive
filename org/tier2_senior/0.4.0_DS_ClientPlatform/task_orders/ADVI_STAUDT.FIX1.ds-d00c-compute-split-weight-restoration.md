<task_order>
  <metadata>
    <id>ADVI_STAUDT.FIX1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-20</date>
    <status>complete</status><!-- PATCHED + LOCAL-VALIDATED 20260420T~14:58Z by ~B: D_00c L971-987 RA-P3 guard-clause, gold_validate_config.yaml D_00c regression sentinels added, comp-validate exit 0, 5 target advisors inv1+inv2 PASS, firm-wide inv1 fails dropped 22->18 (16 sub-cent rounding + 2 genuine residuals for follow-up), firm-wide inv2 fails dropped 146->5 (explicitly FIX2 scope). Evidence: STAUDT/FIX1/fix_to_1_evidence.md + lb_local_run_2026-04-20.json. DT owns push per lane protocol. -->
    <project_code>ADVI_STAUDT</project_code>
    <priority>P0 — user-visible portal defect. Inv2 (`fee_paying.aua + no_fee.aua == tagged_aua`) fails 146/152 advisors at T3 via silent clip at L565. Inv1 fails 22/152 ($0 rounding + 3 outliers). Earlier "152/152 crisis" framing was an artifact of stale pre-FIX3A T3 leaderboard.json; actual production state per ~B Phase 0 dry-run is Inv2-dominant.</priority>
    <lane>~B — FIX-TO 1 then FIX-TO 2 (sequential on D_00c). ~B owns both in order.</lane>
    <bug_reference>RA-P3 override at D_00c L971-987 (commit e53f0afa, 2026-04-15 17:54 ET, CTO Rule 7 sanctioned) sets `tagged_aua_counts = ra_latest.groupby('advisor')['aua_tagged_total'].sum()`. role_aua/ is in P1 SHADOW state (source_filter_stack='p1_shadow_equal_split_no_fee_bucket_no_flow_join') → tagged_aua underscaled to ~20% of true book tagged_aua. Meanwhile fee_aua at L520 reads from C_08 advisor_fee_detail at REAL account-team scale → scale mismatch → silent clip at L565 → no_fee=0 firm-wide. Subsidiary surface per AE INV1: leaderboard MAX total_aua = 0.2012 × book.summary.tagged_aua on Travis Penfield / Kyle Sims / Hunter Lloyd.</bug_reference>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md §3.0 (Class 2 — role-split + fee-split)</ref>
    <ref type="b-phase-0-evidence">data/black_diamond/diagnostics/STAUDT/FIX1/fix_to_1_evidence.md (~B authoritative mechanism note — REPLACES ~D synthesis framing for this TO)</ref>
    <ref type="inv1-ruling">data/black_diamond/diagnostics/STAUDT/INV1/historical_nna_mechanism.md (AE commit ab1da7c8 — 0.2012 identity confirmation on 3/3 cross-check advisors; confirms Bug 1 surfaces at leaderboard.total_aua, not just role_breakdown sum)</ref>
    <ref type="handoff">data/black_diamond/diagnostics/STAUDT/SYNTHESIS/coo_handoff.md §FIX-TO 1 (original framing — superseded by ~B evidence for mechanism; acceptance criteria preserved)</ref>
    <ref type="attribution">data/black_diamond/diagnostics/STAUDT/SYNTHESIS/bug_attribution.md Bug 1 (original symptom attribution valid; root-cause claim superseded)</ref>
    <ref type="upstream-mcp">CTO 20260420T134734Z (fix-TO wave authorization) + CTO 20260420T144506Z (Option A directive via Andrew)</ref>
    <ref type="root-commit">e53f0afa (2026-04-15 17:54 ET, RA-P3 canonical cutover — Rule 7 sanctioned; this TO is an interim revert of the tagged_aua_counts override while role_aua/ matures beyond P1 SHADOW)</ref>
    <ref type="retracted-ref">0804b377 + 9f6faf9 — RETRACTED from root-cause list. 9f6faf9 is a portal/ submodule AdvisorsTab frontend fix and does not modify D_00c (category error). 0804b377 is in the D_00c commit history but not the defect origin per ~B dry-run.</ref>
  </references>

  <objective>
    Disable (comment out or guard-clause) the RA-P3 override block at D_00c.portal_leaderboard.py L971-987 so that `tagged_aua_counts` and `at_role_breakdown` both stay sourced from their pre-RA-P3 account_team-scale code path (L769 for tagged; `_weighted_aua` for role_breakdown). This removes the scale mismatch between role_aua/ P1-SHADOW-derived tagged_aua and C_08-derived fee_aua. Post-fix: Inv1 and Inv2 both hold firm-wide. This is an INTERIM revert of RA-P3 while role_aua/ remains in P1 shadow state. Option B (architectural — nna_atomic/ schema expansion + D-script flip to broader universe) re-establishes the role_aua/ canonical cutover under mature data. Commit message cites that explicitly per CTO directive.
  </objective>

  <scope>
    **Defect mechanism (per ~B Phase 0 evidence file, reconciled with AE INV1 findings):**

    D_00c.portal_leaderboard.py has a pre-RA-P3 code path (L769 region) that computes `tagged_aua_counts` from account_team-level aggregation — this is the TRUE scale, matches book.json `summary.tagged_aua` (e.g., Travis Penfield = $434.4M).

    The RA-P3 override block at L971-987 (commit e53f0afa, Wed 2026-04-15 17:54 ET) overwrites this:
    ```
    if role_aua is not None and not role_aua.empty:
        ...
        tagged_aua_counts = ra_latest.groupby('advisor')['aua_tagged_total'].sum()  # L975
        at_role_breakdown = ...  # role_aua-derived
    ```
    role_aua/ is in P1 SHADOW state (source_filter_stack='p1_shadow_equal_split_no_fee_bucket_no_flow_join'), so `aua_tagged_total` per advisor is ~20% of the true book scale. Travis post-override: tagged_aua = $87.4M (shadow) vs $434.4M (true).

    Meanwhile `fee_aua` at L520 reads from C_08.advisor_fee_detail at real account-team scale. For Travis: fee_aua = $346.5M.

    Silent clip at L565: `no_fee_aua = max(0.0, tagged_aua - fee_aua)` = max(0, $87M - $347M) = $0. Fires for 146/152 advisors firm-wide because shadow-scale tagged is systematically < real-scale fee.

    **In current production (leaderboard.json s3://opal-data-bd/platinum/firm/ last_modified 2026-04-17T16:48Z):**
    - tagged_aua = $434M (account_team scale — the RA-P3 override somehow did NOT fire for tagged_aua_counts)
    - rb_sum = $86M (shadow scale — RA-P3 override DID fire for at_role_breakdown)
    - ratio = 0.198 → THE 20% bug Andrew observed

    Path-dependence in the override block produces per-field variance; in some runs tagged_aua stays real-scale, role_breakdown goes shadow-scale (current production). In ~B's local dry-run both get override-applied. Either way: the override is the defect source.

    **Source file (CLOUD tip post-FIX3A 43c3693a, 2026-04-20):**
    `data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py`
    - L769 region: pre-RA-P3 `tagged_aua_counts` computation (account_team scale — PRESERVE)
    - L839: `_compute_split_weight(grp)` three-case rule (weights CORRECTLY sum to 1.0; not the bug)
    - L881: `melted['_weighted_aua'] = melted['total_aua'] * melted['_split_weight']` (correct; account_team scale)
    - L893: `grp_aua = role_rows.groupby('advisor')['_weighted_aua'].sum()` (pre-RA-P3 at_role_breakdown)
    - L971-987: RA-P3 override block (`if role_aua is not None and not role_aua.empty:`) — **DISABLE THIS**
    - L520: `fee_aua` from C_08 advisor_fee_detail (UNCHANGED)
    - L565: `no_fee_aua = max(0.0, tagged_aua - fee_aua)` silent clip — will naturally resolve to positive values after override disable (FIX-TO 2 separately hardens the explicit handling at L565)

    **Minimum-surface patch (Option A per CTO):**
    Guard the L971-987 block:
    ```
    if False and role_aua is not None and not role_aua.empty:  # RA-P3 override disabled pending role_aua/ P2+ maturity; re-enabled under Option B post-cutover
        ...
    ```
    OR comment the block out with a pointer comment. CTO discretion left on style; prefer the cleaner diff-readable form for future Option B re-enablement.

    **Invariants to restore (post-fix):**
    ```
    Inv1: For every advisor a:
      sum([rb['aua'] for rb in leaderboard[a]['role_breakdown']]) == leaderboard[a]['tagged_aua']
    
    Inv2: For every advisor a:
      leaderboard[a]['fee_breakdown']['fee_paying']['aua'] + leaderboard[a]['fee_breakdown']['no_fee']['aua'] == leaderboard[a]['tagged_aua']
    
    Subsidiary (per AE INV1): 
      leaderboard MAX total_aua == book.json summary.tagged_aua (for all advisors; ratio 1.000, not 0.2012)
    ```
    Tolerance: exact to 2 decimal places.

    **OUT OF SCOPE:**
    - No changes to L520 (fee_aua from C_08 is correct)
    - No changes to _compute_split_weight (the three-case rule is correct and becomes the active code path post-fix)
    - No changes to NNA-path constants (FIX-TO 3A's domain)
    - No changes to C-layer / role_aua/ / account_performance (FIX-TO 4 / Option B scope)
    - No changes to build_advisor_books or D_02 (out of blast radius)
    - Do NOT touch L565 in this TO. FIX-TO 2 is the silent-clip hardening. However, if FIX-TO 2 is picked up in the same ~B session AFTER FIX-TO 1, the clip becomes dead-code for most advisors and the explicit-form replacement can be atomic.
    - No refactors, renames, or "while I'm here" cleanups
    - No killing of the RA-P3 architectural intent — Option B owns re-establishment at broader universe
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="pre-fix diligence — MOSTLY COMPLETE per ~B Phase 0 gate 20260420T144129Z">
      <step>
        <run>DONE: comp-pipescript io D_00c + ~B local dry-run at role_aua/2026-04-15.parquet + git log inspection</run>
        <expect>Phase 0 already complete. Evidence file STAUDT/FIX1/fix_to_1_evidence.md holds the mechanism note. RE-READ the evidence file before patching to confirm line numbers against CLOUD tip post-FIX3A.</expect>
        <if_mismatch>If CLOUD tip has moved since ~B's dry-run (e.g., DT pushed something), re-verify L769 + L971 line numbers before patching. Minor line drift expected; mechanism unchanged.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="patch application (MINIMUM surface)">
      <step>
        <run>Edit D_00c.portal_leaderboard.py: guard-clause or comment out the L971-987 RA-P3 override block</run>
        <expect>Single edit. No other files touched except gold_validate_config.yaml (see Phase 2). Diff readable; block clearly marked as "RA-P3 override disabled pending Option B".</expect>
        <if_mismatch>Any other file edited = scope creep. Stop and MCP COO.</if_mismatch>
      </step>
      <step>
        <run>Local dry-run D_00c.portal_leaderboard.py against current prod date</run>
        <expect>Script runs. Output contains Travis with tagged=$434M, rb_sum=$434M (Inv1 1.000), fp=$346M, nf=$88M (Inv2 passes). Spot-check same for Kyle Sims + Hunter Lloyd.</expect>
        <if_mismatch>Any invariant fails post-patch = mechanism hypothesis incomplete. Re-inspect; MCP COO before deploying.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="post-fix validation + regression protection">
      <step>
        <run>Assert both invariants across all 152 advisors on local dry-run output</run>
        <expect>Inv1 PASS for 152/152 (to 2dp). Inv2 PASS for 152/152 (to 2dp). Subsidiary: MAX total_aua per advisor matches book.json summary.tagged_aua (or matches within documented per-source rounding).</expect>
        <if_mismatch>Any advisor fails either invariant = fix incomplete; investigate that advisor's rows.</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_00c.portal_leaderboard --artifact /tmp/leaderboard.json</run>
        <expect>Exit 0. If gold_validate_config.yaml doesn't have invariant checks for Inv1 AND Inv2 AND subsidiary (leaderboard total_aua == book tagged_aua), ADD them now as regression protection. Required part of this TO.</expect>
        <if_mismatch>Exit != 0 = fix incomplete. Signal MCP COO with validator output.</if_mismatch>
      </step>
      <step>
        <run>Append Phase 1/2 results to existing STAUDT/FIX1/fix_to_1_evidence.md</run>
        <expect>Evidence file contains: ~B's Phase 0 mechanism note (already there) + Phase 1 patch diff summary + Phase 2 152-advisor invariant pass + comp-validate output.</expect>
        <if_mismatch>Missing sections = incomplete evidence; add before close.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py</path>
      <description>Guard-clause or comment-out of L971-987 RA-P3 override block. Commit message MUST use this verbatim language per CTO directive: "interim revert of RA-P3 override; role_aua/ canonical cutover re-established under Option B after nna_atomic/ schema expansion". Commit body cites ~B evidence file + INV1 ab1da7c8 + CTO 20260420T144506Z.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/FIX1/fix_to_1_evidence.md</path>
      <description>~B's Phase 0 mechanism note (already committed) + Phase 1 patch summary + Phase 2 invariant-pass table (all 152 advisors).</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/gold_validate_config.yaml</path>
      <description>Regression invariants for D_00c: (1) Inv1, (2) Inv2, (3) subsidiary leaderboard.total_aua == book.json summary.tagged_aua. Add all three if missing.</description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] Phase 0 evidence file present (~B's pre-patch mechanism note)
    - [ ] Patch applied to D_00c.portal_leaderboard.py ONLY (no other files touched except gold_validate_config.yaml)
    - [ ] Inv1 `sum([rb['aua'] for rb in role_breakdown]) == tagged_aua` holds for all 152 advisors post-run (to 2dp)
    - [ ] Inv2 `fee_paying.aua + no_fee.aua == tagged_aua` holds for all 152 advisors post-run (to 2dp)
    - [ ] Subsidiary: leaderboard MAX total_aua matches book.json summary.tagged_aua (per AE INV1 ab1da7c8 — 0.2012 identity disappears post-fix; ratio 1.000)
    - [ ] No advisor has `role_breakdown[*].aua == 0` for a role where that advisor has confirmed AUA
    - [ ] comp-validate D_00c exits 0 with the three regression invariants loaded
    - [ ] gold_validate_config.yaml updated with Inv1 + Inv2 + subsidiary invariant for D_00c
    - [ ] Commit uses CTO's verbatim language in the message summary
    - [ ] DT coordinates push + S3 upload + bd-gold-qa-runner trigger (DT-online protocol per CTO 20260420T142143Z — not DS; AE escalation only)
    - [ ] Post-deploy validation artifact pulled from qa-runner run; invariants confirmed on live S3 artifact (not just local)
  </acceptance_criteria>

  <guardrails>
    - **DT owns push** (per CTO 20260420T142143Z DT-online protocol). ~B commits to local CLOUD only; DT handles `git push`, S3 upload, bd-gold-qa-runner trigger. AE escalation-only.
    - **No emojis in code** (CLAUDE.md #13). Plain-ASCII prefixes only in print statements and commit messages.
    - **Selective staging:** `git add data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py data/black_diamond/gold_validate_config.yaml` — never `git add -A`.
    - **Agent commit identity:** `git commit --only --author="0.4.0_DS_ClientPlatform~B &lt;0.4.0_DS_ClientPlatform~B@opal.agent&gt;" -- &lt;paths&gt;`
    - **No RA-P3 kill pretense:** the commit is INTERIM. RA-P3's architectural intent stands; Option B re-establishes it at broader universe post-role_aua/ P2+ maturation. Don't edit docs to say RA-P3 was wrong — it was premature.
    - **Pre-flag A→D-rerun-sensitive writes:** this fix should NOT touch canonical paths. If investigation surfaces a dependency you didn't expect, stop and escalate.
    - **Single-TO focus:** if Phase 1 surfaces new scale-mismatch downstream (D_02, D_04, platinum rollups), STOP and MCP COO. Do not expand scope.
    - **Rebase check:** pull latest CLOUD before patching — ~A's FIX3A + other commits may have moved line numbers from ~B's dry-run. Verify L971-987 before editing.
  </guardrails>

  <agent_context_setup>
    1. Register with MCP: `register_agent 0.4.0_DS_ClientPlatform~B`
    2. Launch `bash org/mcp/inbox-watch.sh 0.4.0_DS_ClientPlatform~B` in background
    3. Read in order (UPDATED post-revision):
       - docs/architecture/ADVI_STAUDT.md (PRD, §3.0 + §4.4)
       - data/black_diamond/diagnostics/STAUDT/FIX1/fix_to_1_evidence.md (~B's OWN Phase 0 mechanism note — this is now the authoritative mechanism doc)
       - data/black_diamond/diagnostics/STAUDT/INV1/historical_nna_mechanism.md (AE ab1da7c8 — subsidiary Bug 1 surface at leaderboard.total_aua)
       - data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py (focus L520, L565, L769 region, L839-L893, L971-987)
       - SYNTHESIS/coo_handoff.md §FIX-TO 1 (original — now superseded for mechanism; acceptance criteria updated in this TO)
    4. Heartbeat every 60s during active work
    5. RAVC step 1 ACKNOWLEDGE to COO already fired; proceed directly to Phase 1 patch per CTO GO 20260420T144506Z
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1 (Acknowledge): ALREADY FIRED 20260420T142159Z. No repeat needed.
    - Phase 1 gate: MCP COO with patch diff summary + local 152-advisor invariant-pass table BEFORE requesting DT push
    - RAVC step 4 (Close): MCP COO with deploy commit SHA (via DT push) + bd-gold-qa-runner output summary + production artifact invariant confirmation
    - If blocked at any phase: MCP COO with specific blocker; do not wait silently
  </completion_protocol>
</task_order>
