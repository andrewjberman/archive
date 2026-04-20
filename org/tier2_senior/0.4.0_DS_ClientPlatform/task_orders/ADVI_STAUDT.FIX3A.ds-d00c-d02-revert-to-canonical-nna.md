<task_order>
  <metadata>
    <id>ADVI_STAUDT.FIX3A</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-20</date>
    <status>draft</status>
    <project_code>ADVI_STAUDT</project_code>
    <priority>P1 — can run parallel to FIX-TO 1 (different code paths in D_00c + D_02).</priority>
    <bug_reference>Bug 3 Option A per SYNTHESIS/bug_attribution.md — NNA live schism. Option A = interim revert to nna/; Option B (nna_atomic/ schema fix) parked as separate follow-up initiative.</bug_reference>
    <decision_authority>Andrew 2026-04-20 authorized Option A interim. Option B scoping is CTO-backlog AFTER this wave. Do NOT bundle Option B work into this TO.</decision_authority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md §3.0 (Class 1 — path sub-class)</ref>
    <ref type="handoff">data/black_diamond/diagnostics/STAUDT/SYNTHESIS/coo_handoff.md §FIX-TO 3</ref>
    <ref type="attribution">data/black_diamond/diagnostics/STAUDT/SYNTHESIS/bug_attribution.md Bug 3</ref>
    <ref type="layer-c-evidence">data/black_diamond/diagnostics/STAUDT/layer_C/c01_nna_schema_diff.md (universe analysis — 5,987 vs 9,581 accounts + 376-account shadow-writer asymmetry)</ref>
    <ref type="upstream-mcp">CTO 20260420T134734Z — Option A authorized by Andrew</ref>
    <ref type="prior-partial-revert">cd177553 — reverted D_00b + D_01 + D_04 + C_08 to CANONICAL_NNA_PREFIX but did NOT revert D_00c or D_02. This TO completes that revert.</ref>
  </references>

  <objective>
    Complete the cd177553 partial revert by flipping D_00c + D_02 from `CANONICAL_NNA_ATOMIC_PREFIX` back to `CANONICAL_NNA_PREFIX`, so all 5 D-group scripts (D_00b, D_00c, D_01, D_02, D_04) read the same `gold/canonical/nna/` universe. This is the Option A interim fix: eliminate the schism, accept the smaller 5,987-account universe today, and park the 9,581-account Option B (nna_atomic/ schema fix) as a separate follow-up initiative. The change is a targeted import + paginator constant swap on two files — no logic changes, no schema changes.
  </objective>

  <scope>
    **Defect (verbatim from bug_attribution.md Bug 3):**
    NNA live schism at T3 — D_00c+D_02 on `gold/canonical/nna_atomic/` (9,581 accounts); D_00b+D_01+D_04 on `gold/canonical/nna/` (5,987 accounts). Same advisor shows different NNA in leaderboard vs timeseries vs partner analytics. ~3,600-account delta.

    **Option A fix surface — two files, minimal changes:**

    **File 1: `data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py`**
    - L35 import: `CANONICAL_NNA_ATOMIC_PREFIX` → `CANONICAL_NNA_PREFIX`
    - L121 paginator: `Prefix=CANONICAL_NNA_ATOMIC_PREFIX` → `Prefix=CANONICAL_NNA_PREFIX`
    - Any other reference to `CANONICAL_NNA_ATOMIC_PREFIX` in D_00c: revert

    **File 2: `data/black_diamond/scripts/gold/D_02.advisor_client_detail.py`**
    - L62 import: `CANONICAL_NNA_ATOMIC_PREFIX` → `CANONICAL_NNA_PREFIX`
    - L1624 paginator: `Prefix=CANONICAL_NNA_ATOMIC_PREFIX` → `Prefix=CANONICAL_NNA_PREFIX`
    - Any other reference to `CANONICAL_NNA_ATOMIC_PREFIX` in D_02: revert

    **Acceptance model (per coo_handoff.md §FIX-TO 3):**
    All 5 D scripts (D_00b, D_00c, D_01, D_02, D_04) read the same nna/ path. D_00c and D_02 tagged_aua / NNA consistent with D_00b / D_01 / D_04 for same advisor/window.

    **Column safety check (confirmed by ~D but DS must re-verify):**
    D_00c and D_02 request only 5 safe columns from the NNA partitions. These columns exist in BOTH `nna/` (14 cols) and `nna_atomic/` (22 cols), so the path flip will NOT cause a C_08-style crash. Re-verify this before deploy — the `nna/` schema has 14 columns total; confirm every column D_00c + D_02 read is present in that 14-column set. Ref layer_C/c01_nna_schema_diff.md for the full column diff.

    **OUT OF SCOPE (CRITICAL — do not do these):**
    - DO NOT modify C_01 to add aua_current/growth to nna_atomic/ schema (that is Option B, parked as follow-up)
    - DO NOT re-backfill nna_atomic/ partitions
    - DO NOT touch D_00b, D_01, D_04, or C_08 (already on nna/ post-cd177553)
    - DO NOT investigate the 376-account shadow-writer asymmetry (~C layer evidence notes this; Option B follow-up absorbs it)
    - NO refactors, NO logic changes, NO cleanups — this is a constant-name revert only
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="pre-fix diligence">
      <step>
        <run>grep -n CANONICAL_NNA data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py data/black_diamond/scripts/gold/D_02.advisor_client_detail.py</run>
        <expect>Enumerate EVERY reference. Confirm only imports + paginator calls (no logic that behaves differently per prefix). If any non-obvious usage appears, document + escalate before patching.</expect>
        <if_mismatch>Any reference that isn't a simple constant swap = escalate to COO.</if_mismatch>
      </step>
      <step>
        <run>Column safety audit: list every column that D_00c and D_02 read from their NNA partition; cross-check against the 14-column nna/ schema (ref layer_C/c01_nna_schema_diff.md)</run>
        <expect>All columns D_00c + D_02 read are present in the 14-column nna/ schema. No reads for aua_current, growth, client_state (the 3 nna_atomic/-only cols).</expect>
        <if_mismatch>If any read targets an nna_atomic/-only column, THIS BECOMES OPTION B (cannot revert). STOP and MCP COO + CTO.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io D_00c.portal_leaderboard &amp;&amp; comp-pipescript io D_02.advisor_client_detail</run>
        <expect>Column-read manifest for each script. Cross-check step 2 result against this tool's output.</expect>
        <if_mismatch>Any mismatch between grep-based audit and comp output = trust comp output; re-audit step 2.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="post-fix validation">
      <step>
        <run>Run D_00c + D_02 end-to-end against current prod date after revert</run>
        <expect>Both scripts complete without error.</expect>
        <if_mismatch>Any crash = revert fix; something depends on nna_atomic/ that wasn't caught. Escalate.</if_mismatch>
      </step>
      <step>
        <run>Cross-script NNA consistency check: for a sample of 10 advisors, compare NNA values from D_00c leaderboard output vs D_00b timeseries output vs D_01 partner_analytics output for the same advisor/window.</run>
        <expect>Values agree (or agree within documented per-script aggregation differences).</expect>
        <if_mismatch>If D_00c / D_02 disagree with D_00b / D_01 / D_04 on the same advisor/window post-revert, the revert didn't land or there's a deeper path split.</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_00c + comp-validate D_02 (whichever have configs)</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Exit != 0 = fix incomplete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py</path>
      <description>Import + paginator revert to CANONICAL_NNA_PREFIX only. No other changes.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/scripts/gold/D_02.advisor_client_detail.py</path>
      <description>Import + paginator revert to CANONICAL_NNA_PREFIX only. No other changes.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/FIX3A/fix_to_3a_evidence.md</path>
      <description>
        Pre-fix column safety audit (proving no nna_atomic/-only columns are read) + post-fix cross-script NNA consistency check (D_00c vs D_00b vs D_01 for sample advisors).
      </description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] Column safety audit confirms D_00c + D_02 read only columns present in 14-col nna/ schema BEFORE revert
    - [ ] Single commit reverting D_00c + D_02 imports + paginator calls (no other changes in commit)
    - [ ] Commit body cites bug_attribution.md Bug 3 + cd177553 completion framing
    - [ ] Post-revert D_00c + D_02 run end-to-end without crash
    - [ ] Cross-script NNA consistency verified for ≥10 sample advisors (D_00c vs D_00b/D_01/D_04)
    - [ ] comp-validate exits 0 for D_00c + D_02
    - [ ] Scripts deployed + production run validated
    - [ ] FIX3A evidence file documents both the pre-fix audit and post-fix cross-script check
  </acceptance_criteria>

  <guardrails>
    - **Option A scope only:** if investigation reveals Option A is not safe (e.g., aua_current is actually read somewhere), STOP immediately. Do NOT attempt Option B under this TO — Option B is a separate follow-up initiative requiring DE involvement.
    - **No schema changes:** zero C-layer edits, zero ingestion changes, zero re-backfills.
    - **Parallel to FIX-TO 1:** this TO touches different code paths in D_00c (lines 35 + 121) from FIX-TO 1 (lines 839-881). Coordinate git commits so they don't collide on D_00c.portal_leaderboard.py — commit FIX-TO 1 or FIX-TO 3A first (whichever finishes), then rebase the other.
    - **No emojis, selective staging, agent commit identity** per standard rules.
  </guardrails>

  <agent_context_setup>
    1. Register + inbox-watch (first two tool calls)
    2. Read:
       - docs/architecture/ADVI_STAUDT.md §3.0 (Class 1 path sub-class)
       - SYNTHESIS/coo_handoff.md §FIX-TO 3
       - SYNTHESIS/bug_attribution.md Bug 3
       - layer_C/c01_nna_schema_diff.md (full universe + column diff)
       - D_00c.portal_leaderboard.py L30-L130 (imports + paginator)
       - D_02.advisor_client_detail.py L55-L130 + L1600-L1650 (imports + paginator)
    3. Heartbeat every 60s during active work
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1: ACK within 5 min
    - Phase 0 gate: MCP COO with column safety audit result before patching
    - RAVC step 4: MCP COO with deploy commit SHA + cross-script consistency evidence
    - If column safety audit fails (i.e., can't do Option A): MCP COO + CTO with the finding — do NOT attempt Option B here
  </completion_protocol>
</task_order>
