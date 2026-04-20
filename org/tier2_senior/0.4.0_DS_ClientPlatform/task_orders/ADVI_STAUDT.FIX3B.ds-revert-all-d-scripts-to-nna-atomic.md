<task_order>
  <metadata>
    <id>ADVI_STAUDT.FIX3B</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-20</date>
    <status>complete</status><!-- CANCELLED 2026-04-20 — Phase 0 parquet verification proved `aua_current` IS present in canonical/nna/ (original identity-break hypothesis wrong). FIX3A's D_00c+D_02 nna/ revert held structurally; FIX3B scope is moot. Evidence: DS~A log `staudt_engine_accuracy_bfix12.md`. CTO reconciliation session 35. -->
    <project_code>ADVI_STAUDT</project_code>
    <priority>P0 — BLOCKS PROD. The FIX3A path-uniformity direction was wrong; canonical/nna/ lacks aua_current → identity broken in Assets Overview portal. Reverse direction immediately, restore Wednesday state (all D-scripts on nna_atomic/), park nna/ migration for Option B.</priority>
    <lane>~A — single-TO lane. Continuation of ~A's FIX3A work; ~A owns the entire D-prefix surface.</lane>
    <bug_reference>CTO 20260420T161035Z root-cause: cd177553 + FIX3A (43c3693a) both swapped readers to canonical/nna/, but canonical/nna/ schema (14 cols) lacks aua_current + growth (only canonical/nna_atomic/ 22-col schema has them). D_00b L408 reads aua_current → defensive fill L425-427 zeros it → AUA stock falls back to account_performance narrow universe → AUA/NNA/GRO identity broken. Andrew flagged Penfield $400M-vs-$434M discrepancy as portal symptom.</bug_reference>
    <decision_authority>CTO 20260420T161035Z. Andrew portal-flagged.</decision_authority>
  </metadata>

  <references>
    <ref type="cto-root-cause-mcp">CTO 20260420T161035Z — "URGENT: Assets Overview identity breakdown — cd177553 root cause + immediate fix directive"</ref>
    <ref type="prior-half-revert">cd177553 — swapped D_00b + D_01 + D_04 + C_08 to CANONICAL_NNA_PREFIX (the half-swap that broke identity)</ref>
    <ref type="prior-other-half">43c3693a (FIX3A) — completed cd177553 by swapping D_00c + D_02 to CANONICAL_NNA_PREFIX (compounded the identity break)</ref>
    <ref type="fix1-stays">2fa1f2be (FIX1) — D_00c L971-987 RA-P3 override guard-clause. INDEPENDENT of NNA prefix. STAYS. Do NOT revert FIX1.</ref>
    <ref type="schema-evidence">data/black_diamond/diagnostics/STAUDT/layer_C/c01_nna_schema_diff.md — 22-col nna_atomic/ vs 14-col nna/ column diff</ref>
    <ref type="superseded-by">Option B scoping initiative (post-FIX1-prod-close) — adds aua_current + growth to canonical/nna/ schema, broadens canonical/nna/ universe to ~9,581 accounts, then re-flips D-scripts back to nna/. FIX3B is INTERIM revert until Option B ships.</ref>
  </references>

  <objective>
    Reverse cd177553 + FIX3A by reverting ALL D-group + C_08 NNA readers from `CANONICAL_NNA_PREFIX` back to `CANONICAL_NNA_ATOMIC_PREFIX`. Restores the pre-cd177553 (Wednesday) state where ALL D-scripts read the same 22-col canonical/nna_atomic/ universe (single-universe AUA + NNA + GRO identity holds). FIX1 (RA-P3 override guard-clause in D_00c L971-987) is INDEPENDENT of the prefix and STAYS in place. This is interim until Option B (canonical/nna/ schema expansion) ships.
  </objective>

  <scope>
    **Defect (verbatim from CTO 20260420T161035Z):**
    cd177553 swapped D_00b (+ D_01, D_04, C_08) from CANONICAL_NNA_ATOMIC_PREFIX to CANONICAL_NNA_PREFIX. D_00b reads aua_current DIRECTLY from the NNA prefix at L408 to compute the AUA stock timeseries. nna/ lacks aua_current → defensive fill L425-427 zeros it → AUA stock falls back to account_performance (holdings_lots narrow universe, $27.6M in 2020). NNA comes from nna/ flows. GRO from account_performance. THREE different universes = identity broken.

    **Surface — five files, constant-swap reverts only:**

    **File 1: `data/black_diamond/scripts/gold/D_00b.portal_timeseries.py`**
    - Revert cd177553's swap: every `CANONICAL_NNA_PREFIX` referencing the canonical NNA partition prefix → `CANONICAL_NNA_ATOMIC_PREFIX`
    - Includes L408 reader + paginator + import statements

    **File 2: `data/black_diamond/scripts/gold/D_01.partner_analytics.py`** (or whatever D_01's actual filename is — confirm via Phase 0)
    - Revert cd177553's swap: every `CANONICAL_NNA_PREFIX` reference → `CANONICAL_NNA_ATOMIC_PREFIX`

    **File 3: `data/black_diamond/scripts/gold/D_04.client_portal_summary.py`**
    - Revert cd177553's swap: every `CANONICAL_NNA_PREFIX` reference → `CANONICAL_NNA_ATOMIC_PREFIX`
    - **DO NOT TOUCH** the FIX6 (b7a75374) gate logic in `build_firm_pass_throughs()` and `build_advisor_summaries()` — those are 3-yr lookback gates on date columns, independent of which prefix supplies the data.

    **File 4: `data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py`**
    - Revert FIX3A (43c3693a) at L35 + L121: `CANONICAL_NNA_PREFIX` → `CANONICAL_NNA_ATOMIC_PREFIX`
    - **DO NOT TOUCH** the FIX1 (2fa1f2be) RA-P3 override guard-clause at L971-987. FIX1 is independent of NNA prefix and stays.

    **File 5: `data/black_diamond/scripts/gold/D_02.advisor_client_detail.py`**
    - Revert FIX3A (43c3693a) at L62 + L1624: `CANONICAL_NNA_PREFIX` → `CANONICAL_NNA_ATOMIC_PREFIX`

    **File 6 (lower urgency, can batch-include): `data/black_diamond/scripts/gold/C_08.advisor_fee_efficiency.py`**
    - Revert cd177553's swap. C_08 uses NNA only for reference per CTO note — less urgent but include for state coherence.

    **Acceptance model:**
    - All 5 D scripts (D_00b, D_00c, D_01, D_02, D_04) read from CANONICAL_NNA_ATOMIC_PREFIX
    - C_08 reads from CANONICAL_NNA_ATOMIC_PREFIX
    - AUA stock + NNA + GRO all sourced from canonical/nna_atomic/ (22-col schema with aua_current + growth)
    - AUA/NNA/GRO identity holds for sample advisors in Assets Overview portal view
    - Penfield AUA = $434M consistent across leaderboard + detail views (aua_current from nna_atomic/ matches account_team tagged_aua)
    - FIX1 (RA-P3 guard-clause) intact in D_00c L971-987

    **Pre-fix column safety check (CRITICAL — DO NOT SKIP):**
    canonical/nna_atomic/ schema is a SUPERSET of canonical/nna/ (22 cols vs 14 cols). All columns currently read by D-scripts MUST be present in canonical/nna_atomic/. Verify via Phase 0 audit. If any D-script reads a column that exists in canonical/nna/ but NOT canonical/nna_atomic/ (unlikely given column count, but verify), STOP and escalate.

    **OUT OF SCOPE:**
    - DO NOT modify canonical/nna/ schema (Option B owns)
    - DO NOT touch C_01 ingestion / nna_atomic/ writer
    - DO NOT touch FIX1 (2fa1f2be) RA-P3 guard-clause logic in D_00c L971-987
    - DO NOT touch FIX6 (b7a75374) date gate logic in D_04
    - DO NOT touch FIX5 (1d8f32d1) C_01 backfill logic
    - NO refactors, NO logic changes — constant-name reverts only
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="pre-fix diligence">
      <step>
        <run>grep -n CANONICAL_NNA data/black_diamond/scripts/gold/D_00b.portal_timeseries.py data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py data/black_diamond/scripts/gold/D_01.*.py data/black_diamond/scripts/gold/D_02.advisor_client_detail.py data/black_diamond/scripts/gold/D_04.client_portal_summary.py data/black_diamond/scripts/gold/C_08.advisor_fee_efficiency.py</run>
        <expect>Enumerate EVERY CANONICAL_NNA_PREFIX reference. Confirm only imports + paginator/reader calls (no logic that behaves differently per prefix).</expect>
        <if_mismatch>Any reference that isn't a simple constant swap = escalate to COO.</if_mismatch>
      </step>
      <step>
        <run>Column safety audit: list every column each script reads from its NNA partition; cross-check against the 22-column nna_atomic/ schema (ref layer_C/c01_nna_schema_diff.md)</run>
        <expect>All columns present in 22-col nna_atomic/ schema (which is a SUPERSET of nna/ — should pass trivially). Specifically: D_00b reads aua_current at L408 → confirm aua_current in nna_atomic/ schema (it is — that's the whole point of this revert).</expect>
        <if_mismatch>If any read targets a nna/-only column (none expected, but verify), STOP — that would be a separate issue.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io on all 6 scripts</run>
        <expect>Column-read manifest for each. Cross-check audit. Confirm no surprise consumers (e.g., D_03 or platinum scripts reading either prefix).</expect>
        <if_mismatch>If comp-pipescript shows additional readers beyond the 6 listed, ESCALATE — scope may need expansion.</if_mismatch>
      </step>
      <step>
        <run>Verify FIX1 (commit 2fa1f2be) D_00c L971-987 guard-clause is preserved and FIX6 (b7a75374) D_04 gate logic is preserved BEFORE patching</run>
        <expect>git diff shows FIX1 + FIX6 logic intact in the working tree. Your revert touches DIFFERENT lines.</expect>
        <if_mismatch>Any overlap = stop and escalate. Constant-swap reverts must not touch FIX1/FIX6 lines.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="post-fix validation">
      <step>
        <run>Run D_00b + D_00c + D_01 + D_02 + D_04 + C_08 end-to-end against current prod date after revert</run>
        <expect>All scripts complete without error. comp-validate D_00c + D_04 = exit 0.</expect>
        <if_mismatch>Any crash = revert fix; column safety audit was wrong somewhere.</if_mismatch>
      </step>
      <step>
        <run>AUA/NNA/GRO identity check on platinum/firm/leaderboard.json + platinum/firm/timeseries_chart.json: AUA stock should equal opening_AUA + sum(NNA flows) + sum(GRO) within tolerance for sample window (e.g., QTD)</run>
        <expect>Identity holds within $1k for firm-level QTD. AUA stock no longer collapses to $27.6M-style narrow-universe value.</expect>
        <if_mismatch>Identity still broken = revert incomplete or another script is sourcing AUA from a different universe. Escalate.</if_mismatch>
      </step>
      <step>
        <run>Per-advisor sample check (≥10 advisors including Penfield): AUA stock from nna_atomic/ aua_current matches tagged_aua from account_team within tolerance</run>
        <expect>Penfield AUA = ~$434M (matches FIX1-corrected leaderboard tagged_aua). Other advisors equally consistent.</expect>
        <if_mismatch>Penfield mismatch = aua_current source still wrong. Escalate.</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_00c + D_04 + (any others with configs)</run>
        <expect>Exit 0 for all.</expect>
        <if_mismatch>Exit != 0 = fix incomplete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/scripts/gold/D_00b.portal_timeseries.py</path>
      <description>CANONICAL_NNA_PREFIX → CANONICAL_NNA_ATOMIC_PREFIX revert. No other changes.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py</path>
      <description>CANONICAL_NNA_PREFIX → CANONICAL_NNA_ATOMIC_PREFIX revert at L35 + L121 ONLY. FIX1 RA-P3 guard-clause at L971-987 PRESERVED.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/scripts/gold/D_01.*.py</path>
      <description>CANONICAL_NNA_PREFIX → CANONICAL_NNA_ATOMIC_PREFIX revert. No other changes.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/scripts/gold/D_02.advisor_client_detail.py</path>
      <description>CANONICAL_NNA_PREFIX → CANONICAL_NNA_ATOMIC_PREFIX revert at L62 + L1624 ONLY. No other changes.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/scripts/gold/D_04.client_portal_summary.py</path>
      <description>CANONICAL_NNA_PREFIX → CANONICAL_NNA_ATOMIC_PREFIX revert. FIX6 b7a75374 date-gate logic in build_firm_pass_throughs() + build_advisor_summaries() PRESERVED.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/scripts/gold/C_08.advisor_fee_efficiency.py</path>
      <description>CANONICAL_NNA_PREFIX → CANONICAL_NNA_ATOMIC_PREFIX revert. No other changes.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/FIX3B/fix_to_3b_evidence.md</path>
      <description>Phase 0 column safety audit + Phase 1 identity-restoration evidence (firm AUA/NNA/GRO identity equation, Penfield per-advisor consistency, comp-validate output).</description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] Phase 0 column safety audit confirms all D-script + C_08 reads target columns present in 22-col nna_atomic/ schema
    - [ ] Phase 0 confirms FIX1 (2fa1f2be) + FIX6 (b7a75374) lines NOT touched by revert
    - [ ] Single commit reverting prefix references in all 6 files (no other changes in commit)
    - [ ] Commit message cites CTO 20260420T161035Z + "interim revert until Option B canonical/nna/ schema expansion ships"
    - [ ] Post-revert all 6 scripts run end-to-end without crash
    - [ ] AUA/NNA/GRO identity holds for firm-level QTD within $1k
    - [ ] Penfield AUA stock = ~$434M consistent with FIX1-corrected leaderboard tagged_aua
    - [ ] Cross-script NNA consistency verified for ≥10 sample advisors (D_00c vs D_00b/D_01/D_04)
    - [ ] comp-validate exits 0 for D_00c + D_04
    - [ ] DT uploads from `git show {sha}:path` (NOT working tree) per FIX3A bundling-incident lesson
    - [ ] Scripts deployed to qa-runner, identity validated, then PROD via bd-gold-trigger
  </acceptance_criteria>

  <guardrails>
    - **PRESERVE FIX1:** D_00c L971-987 guard-clause MUST stay. Verify via grep `if False and role_aua` in D_00c BEFORE and AFTER your patch.
    - **PRESERVE FIX6:** D_04 build_firm_pass_throughs() + build_advisor_summaries() date-gate logic MUST stay. Verify via grep for `1095` (3-year lookback days) in D_04 BEFORE and AFTER.
    - **NO Option B scope creep:** if Phase 0 surfaces temptation to "while I'm here, add aua_current to nna/ schema" or "fix the universe asymmetry" — STOP. That is Option B. This TO restores the Wednesday state and ships.
    - **No emojis, selective staging, agent commit identity** per standard rules.
    - **DT owns push + S3 upload from committed ref** — NOT working tree (per FIX3A bundling lesson, see feedback memory update incoming).
  </guardrails>

  <agent_context_setup>
    1. Register + inbox-watch (first two tool calls)
    2. Read:
       - CTO MCP 20260420T161035Z (in your inbox or via get_agent_status broker)
       - data/black_diamond/diagnostics/STAUDT/layer_C/c01_nna_schema_diff.md (22-col vs 14-col diff)
       - D_00b.portal_timeseries.py L400-L430 (aua_current reader + defensive fill)
       - D_00c.portal_leaderboard.py L30-L130 + L971-987 (imports + paginator + FIX1 guard-clause)
       - D_02.advisor_client_detail.py L55-L130 + L1600-L1650 (imports + paginator)
       - D_04.client_portal_summary.py (imports + build_firm_pass_throughs + build_advisor_summaries — confirm FIX6 logic)
       - C_08.advisor_fee_efficiency.py (imports)
    3. Heartbeat every 60s during active work
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1: ACK within 5 min of receipt: "ACK FIX3B — starting Phase 0 column safety + FIX1/FIX6 preservation audit"
    - Phase 0 gate: MCP COO with column safety audit + FIX1/FIX6 line preservation confirmation BEFORE patching. Wait for COO go.
    - Phase 1 gate: MCP COO with identity-restoration evidence (firm AUA/NNA/GRO equation + Penfield consistency) BEFORE requesting DT push.
    - RAVC step 4: MCP COO with deploy commit SHA + identity-validation evidence + DT-upload-from-ref confirmation
  </completion_protocol>
</task_order>
