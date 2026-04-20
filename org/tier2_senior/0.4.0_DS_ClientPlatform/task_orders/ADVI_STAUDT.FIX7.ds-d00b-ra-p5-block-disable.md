<task_order>
  <metadata>
    <id>ADVI_STAUDT.FIX7</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-20</date>
    <status>dispatched</status><!-- DISPATCHED 20260420T16:28Z by 2.0.0_SA_COO. CTO directive 20260420T162726Z. Bundle with FIX3B in same ~A wave (same D_00b file). -->
    <project_code>ADVI_STAUDT</project_code>
    <priority>P0 — same RA-class bug as FIX1, but on D_00b L788-798 (RA-P5) instead of D_00c L971-987 (RA-P3). Continuous-ADV-AUA = $330M instead of $1.649B (same ~20% role_aua/ shadow ratio). Fix is symmetric to FIX1.</priority>
    <lane>~A — bundled with FIX3B + INV4 in single D-script wave. Same commit as FIX3B (both touch D_00b).</lane>
    <bug_reference>CTO 20260420T162726Z. D_00b RA-P5 block (L788-798) replaces account_team/account_performance-derived ADV AUA with canonical role_aua/ (architect-only filter). role_aua/ P1 shadow → firm ADV-AUA = $330M instead of $1.649B. Code comment at L771 explains RA-P5's intent (covering $127M unassigned-architect drop), but the LEFT-merge at L777 already solved that. RA-P5 override at L788 is now redundant + actively wrong against P1 shadow state. Fallback at L800-801 (ap_attr.groupby account_performance) is correct and takes over when L788-798 is disabled.</bug_reference>
    <decision_authority>CTO 20260420T162726Z. Same pattern + commit-message language as FIX1.</decision_authority>
  </metadata>

  <references>
    <ref type="cto-directive">CTO 20260420T162726Z — comprehensive fix directive (FIX3B + FIX7 + INV4)</ref>
    <ref type="symmetric-fix">FIX1 (2fa1f2be) — D_00c L971-987 RA-P3 block disable. Same pattern; FIX7 applies to D_00b L788-798 RA-P5 block.</ref>
    <ref type="superseded-by">Option B — once role_aua/ canonical state is correct (post P1 shadow resolution), RA-P5 override may be re-enabled. FIX7 is INTERIM disable.</ref>
  </references>

  <objective>
    Disable (guard-clause) the RA-P5 override block at D_00b L788-798. The block currently replaces a correct account_team/account_performance-derived ADV AUA aggregation with role_aua/-filtered (architect-only) values pulled from the role_aua/ P1 shadow state, producing firm ADV-AUA = $330M (~20% of true $1.649B). Disabling this override hands aggregation back to the LEFT-merge at L777 + fallback at L800-801, which produce correct numbers. Symmetric to FIX1 in pattern and intent. Interim until Option B canonical role_aua/ stabilizes.
  </objective>

  <scope>
    **Defect (verbatim from CTO 20260420T162726Z):**
    D_00b L788-798 (RA-P5 block): replaces account_team/account_performance-derived ADV AUA with canonical role_aua/ (filtering architect role only). role_aua/ P1 shadow state → firm ADV-AUA = $330M instead of $1.649B (same ~20% ratio as Bug 1).

    Code comment at L771 explains WHY RA-P5 was introduced: inner-merge was dropping $127M of unassigned-architect AUA. The correct fix was the LEFT-merge at L777 (already in code), NOT the role_aua/ override at L788. The fallback at L800-801 (ap_attr.groupby account_performance path) IS correct and produces right numbers.

    **Fix surface — D_00b L788-798 only:**
    Add `if False and …` guard-clause OR comment-out the RA-P5 override block. Pattern symmetric to FIX1's D_00c L971-987 guard-clause. Fallback at L800-801 takes over.

    **Verbatim commit message language (per CTO 20260420T144506Z mandated style for FIX1 — adapted for FIX7):**
    `"interim revert of RA-P5 override; role_aua/ ADV canonical re-established under Option B"`

    **Bundling with FIX3B:**
    FIX7 touches D_00b. FIX3B also touches D_00b (revert CANONICAL_NNA_PREFIX → CANONICAL_NNA_ATOMIC_PREFIX). Bundle BOTH changes in the SAME commit. Different lines (L306-356 NNA prefix vs L788-798 RA-P5), no logical conflict.

    **OUT OF SCOPE:**
    - DO NOT touch RA-P5 block in any other script (it's D_00b-only)
    - DO NOT modify role_aua/ canonical or P1 shadow logic (Option B owns)
    - DO NOT touch the LEFT-merge at L777 or fallback at L800-801 — both are correct as-is
    - DO NOT modify FIX1 (D_00c L971-987) or FIX3B's NNA prefix work (different surfaces)
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="pre-fix verification — bundled with FIX3B Phase 0">
      <step>
        <run>Read D_00b L760-810 — confirm RA-P5 block boundaries (L788-798) and L800-801 fallback path</run>
        <expect>RA-P5 block self-contained between L788 and L798. L800-801 ap_attr.groupby fallback present and correct. L777 LEFT-merge present.</expect>
        <if_mismatch>If RA-P5 block boundaries are different than CTO indicated, MCP COO before patching. Read 20-line context window around it.</if_mismatch>
      </step>
      <step>
        <run>Local dry-run D_00b post-patch (with both FIX3B + FIX7 changes), assert firm ADV-AUA = ~$1.649B (NOT ~$330M)</run>
        <expect>ap_attr.groupby fallback produces firm ADV-AUA in $1.6B range. Per-advisor architect-AUA values look reasonable.</expect>
        <if_mismatch>If firm total is still anomalous (e.g., still near $330M, or now wildly off), guard-clause may be incomplete or fallback isn't activating. Escalate.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="post-fix validation — bundled with FIX3B Phase 1">
      <step>
        <run>Cross-view consistency: firm ADV-AUA in D_00b output (Continuous Activity timeseries) matches firm AUA in D_00 (header), D_00c (leaderboard sum), D_01 (header_metrics), within tolerance</run>
        <expect>All four agree on $1.649B (or current correct value) within $1k. No view shows $330M residual.</expect>
        <if_mismatch>If any view still shows $330M, that view has its own role_aua/-shadow path that needs separate investigation.</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_00b on its post-patch artifact</run>
        <expect>Exit 0. Add ADV-AUA invariant if not present: firm.adv_aua > $1B sentinel.</expect>
        <if_mismatch>Exit != 0 or ADV-AUA still anomalous = fix incomplete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/scripts/gold/D_00b.portal_timeseries.py</path>
      <description>RA-P5 block at L788-798 guard-claused (`if False and …`) with interim-revert comment citing CTO 20260420T162726Z + Option B re-enable condition. Bundled with FIX3B's CANONICAL_NNA_PREFIX revert in same commit.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/scripts/gold/gold_validate_config.yaml</path>
      <description>D_00b section: add ADV-AUA sentinel (firm.adv_aua > $1B WARN if missing).</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/FIX7/fix_to_7_evidence.md</path>
      <description>Phase 0 boundary verification + Phase 1 cross-view consistency table (D_00 / D_00b / D_00c / D_01 firm ADV-AUA all = $1.649B).</description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] RA-P5 block at D_00b L788-798 disabled via guard-clause
    - [ ] FIX3B + FIX7 bundled in single ~A commit (D_00b touched once)
    - [ ] Commit body cites CTO 20260420T162726Z + uses verbatim "interim revert of RA-P5 override; role_aua/ ADV canonical re-established under Option B"
    - [ ] Post-patch firm ADV-AUA = ~$1.649B (NOT $330M)
    - [ ] Cross-view consistency D_00 / D_00b / D_00c / D_01 all agree on firm ADV-AUA
    - [ ] comp-validate D_00b exit 0
    - [ ] gold_validate_config.yaml updated with ADV-AUA sentinel
  </acceptance_criteria>

  <guardrails>
    - **PRESERVE the LEFT-merge at L777 + fallback at L800-801** — both are correct, do not touch
    - **NO Option B scope creep** — do not investigate role_aua/ P1 shadow root cause
    - **No touching FIX1 (D_00c L971-987)** — different script, different fix
    - **Same commit as FIX3B** — single ~A commit covers both fixes on D_00b + the prefix reverts on other 5 files
    - **No emojis, selective staging, agent commit identity**
    - **DT push + S3 upload from `git show {sha}:path`** — no working-tree uploads
  </guardrails>

  <agent_context_setup>
    1. Same context as FIX3B (TO already in your inbox)
    2. Add: D_00b L760-810 — RA-P5 block + LEFT-merge + fallback context window
    3. CTO 20260420T162726Z bug analysis
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1: ACK in same MCP as FIX3B ACK
    - Phase 0 gate: bundle FIX3B + FIX7 + INV4 findings in single MCP to COO
    - Phase 1 gate: bundle FIX3B + FIX7 patch summary in single MCP
    - RAVC step 4: bundle commit SHA + cross-view evidence for both fixes
  </completion_protocol>
</task_order>
