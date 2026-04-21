<task_order>
  <metadata>
    <id>ADVI_STAUDT.BFIX4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-20</date>
    <status>complete</status><!-- CANCELLED 2026-04-20 ~22:00Z per Andrew "we don't track that" directive — same cohort-disposition as BFIX3 cancellation. ~$32M A_03 positions_cube gap lives in the structurally-BD-excluded cohort (SLATs/DAFs/HSAs/corporate entities ~654 accts / $52M). Andrew decision: do not inject synthetic AUA for untracked accts. Superseded by CTO active-filter brief (docs/briefs/aua_active_account_filter_redesign.md — DRAFT awaiting Andrew read) which proposes multi-signal active-account detector to recover ~$41M via the correct mechanism (admit accts with recent tx+custodian evidence, not synth cash in A_03). BFIX1+BFIX2 (081223b5 + 1a54d46a fix-forward) closes ~$20.8M of the original $48M gap; BFIX4's proposed A_03 synth path is NOT the right closure for the remaining $32M. Evidence: CTO session 34 continuation log `aua_active_filter_investigation_and_brief.md`; ~A BFIX1+2 Phase 0 mechanism note. Was DISPATCHED 20260420T19:XX Z by 2.0.0_SA_COO per CTO directive 20260420T194200Z (combined-deploy plan change). Cancelled 20260420T22:00Z per Andrew chat directive. Reconciled by CTO session 36 audit 2026-04-21. -->
    <project_code>ADVI_STAUDT</project_code>
    <priority>P2 — investigation-only TO, ships as part of combined BFIX1+2+3+4 package per CTO 20260420T194200Z plan change. Phase 0 evidence fills in when ~A reaches it post-BFIX3 close.</priority>
    <lane>~A — sequential after BFIX3 close. Continues engine-accuracy investigation chain on single ~A lane with full mental context.</lane>
    <bug_reference>~A's BFIX1+BFIX2 Phase 0 mechanism note (commit 081223b5) surfaced that ~$32M of the engine accuracy gap lives upstream in A_03.positions_cube.py, NOT in B_00 silver-layer scope. Per-account decomposition: 69 accts ($23.7M) absent_from_cube (account not in positions_cube AT ALL — examples: BRYAN GRUNDHOEFER $5.08M, CRAIG SMITH TTEE $2.50M, CHARLES SCHWAB TRUST BANK $2.32M, Stephanie Bourland PCRA $2.26M); 17 accts ($8.3M) fp_dust_in_cube (cube has positions but units 1e-13 to 1e-11 = FIFO depletion); 8 accts ($4.2M) non-financial absent_from_cube from BFIX2 cohort overlap (Silverthorne Home $2M, Austin Home $1.75M, insurance VULs). Total ~$36M (rounds to the briefed $32M). BFIX1+BFIX2 close ~$20.8M of the original $48M gap; BFIX4 closes the remaining ~$32M from the upstream A_03 surface.</bug_reference>
    <decision_authority>CTO 20260420T194200Z (combined-deploy plan change). Andrew approval implicit via prior engine refinement plan ("Agreed on all counts go ahead", and 50bps target).</decision_authority>
  </metadata>

  <references>
    <ref type="evidence-source">data/black_diamond/diagnostics/STAUDT/BFIX1/bfix1_phase0_mechanism_note.md (~A's Phase 0 evidence file in commit 081223b5 — surfaced the 69 absent_from_cube + 17 fp_dust + 8 non-financial decomposition)</ref>
    <ref type="briefing">data/black_diamond/diagnostics/STAUDT/BRIEFING_aua_engine_accuracy_2026-04-20.md (~A briefing — Bug 1 + Bug 3 originally framed as B_00 scope; Phase 0 audit corrected to mostly A_03 upstream)</ref>
    <ref type="parent">project_bd_is_ground_truth.md (BD silver/allocations is the source-of-truth comparison anchor)</ref>
    <ref type="parent">feedback_no_unverified_theories_as_conclusions.md (treat any A_03 mechanism hypothesis as theory until evidence closes)</ref>
    <ref type="prior-engine-fixes">BFIX1+BFIX2 (commit 081223b5, P1) — closes ~$20.8M of $48M gap. BFIX4 closes remaining ~$32M from upstream A_03.</ref>
    <ref type="cto-plan-change">CTO 20260420T194200Z — combined deploy: BFIX1+2+3+4 ship as one package. One pre-flag, one S3 upload, one qa-runner cycle, one PROD deploy.</ref>
  </references>

  <objective>
    Trace the upstream A_03.positions_cube.py logic to identify why ~$32M of accounts (69 fully absent + 17 with fp-dust units + 8 non-financial) are missing from positions_cube despite having BD positions activity. Produce a written trace document with mechanism root cause + per-account evidence (3+ accounts per cohort) + decision verdict on whether the fix is a 1-file surgical patch in A_03 or requires multi-layer scope decomposition. NO code changes in this TO — investigation only. Phase 1 fix authoring (BFIX4b) follows separately if 1-file fix is feasible.
  </objective>

  <scope>
    **Three account cohorts to trace (per ~A's BFIX1 Phase 0 evidence):**

    **Cohort 1 — absent_from_cube (69 accounts, $23.7M):**
    - Account exists in BD positions / fees / mapping but ZERO rows in positions_cube
    - Top examples: BRYAN GRUNDHOEFER (Joint, $5.08M), CRAIG SMITH TTEE (Trust, $2.50M), CHARLES SCHWAB TRUST BANK (Trust, $2.32M), Stephanie Bourland PCRA ($2.26M), Buck NCF DAF ($2.30M)
    - Pattern observation: PCRA / Schwab Trust Bank / DAF / Joint trusts heavily represented
    - Question: at what step does A_03 drop these accounts? Filter clause? JOIN failure? Source-data absence?

    **Cohort 2 — fp_dust_in_cube (17 accounts, $8.3M):**
    - Account exists in positions_cube but units are 1e-13 to 1e-11 (essentially zero from FIFO depletion)
    - Top examples: TROY ESTES ($2.01M BD vs 1 row units 3.6e-11), Kent Marcuson PCRA ($1.87M BD vs 6 rows summing 2.8e-13)
    - Question: is this FIFO over-depletion (sells exceed buys due to missing buy transactions), unit-quantity mismatch between BD and Schwab, or a tax-lot accounting artifact?

    **Cohort 3 — non-financial absent_from_cube (8 accounts, $4.2M):**
    - Non-financial accounts (homes, insurance VULs, illiquid)
    - Examples: Silverthorne Home $2M, Austin Home $1.75M, insurance VULs
    - Question: is A_03 architecturally designed to exclude non-financial assets (intentional), or is it a downstream filter that could be loosened?
    - Likely overlap with BFIX2 cohort (~A noted in BFIX2 Phase 0 these "can't be re-injected via BD positions because they don't have transactions")

    **Investigation steps (read-only):**

    1. **comp-pipescript io A_03.positions_cube** — full READ + WRITE manifest. Identify all source data, filter clauses, JOIN keys.
    2. **comp-blast positions_cube + comp-blast canonical/positions** — downstream consumer chain. Confirm what depends on the cube (B_00, B_01, C_03, C_06, D_02, D_03 per CTO 20260420T190431Z).
    3. **Per-account trace** for 3-5 accounts in each cohort: pull from (a) BD positions / silver source, (b) Schwab RPS, (c) any intermediate A_03 working table, (d) positions_cube output. Identify the drop/depletion point.
    4. **Source-data check** for the absent_from_cube cohort: is the data IN BD positions feed at all, or is it absent at silver/bronze layer?
       - If IN BD but dropped by A_03: A_03 has filter logic to investigate.
       - If absent at silver: bug is upstream of A_03 (AE escalation territory).
    5. **FIFO depletion mechanism** for fp_dust cohort: trace one account's complete buy/sell history vs A_03's lot-tracking output. Identify if buy transactions are missing (truncation) or if the FIFO logic over-depletes.
    6. **Non-financial filter check:** grep A_03 for asset-class filters (`is_cash`, `is_equity`, `is_bond`, asset_type = ...). Document the asset universe A_03 admits.

    **Hypotheses to evaluate (do not pre-commit):**
    - H1: A_03 has an account-class filter (e.g., excludes non-Schwab-brokerage account types) that drops the 69 absent_from_cube cohort
    - H2: A_03 JOIN keys mismatch for PCRA/DAF/trust account types (sub-account namespaces)
    - H3: BD positions feed itself is missing data for these accounts (upstream of A_03, AE territory)
    - H4: FIFO logic in A_03 over-depletes when historical buy transactions are truncated (lookback window too short for older accounts)
    - H5: Non-financial assets are intentionally excluded from A_03's asset universe (documented design choice, not a bug)
    - H6: Multiple of the above — likely, given the cohort heterogeneity

    **Decision tree post-investigation:**
    - **If 1-file surgical fix in A_03 + Phase 0 evidence is unambiguous:** propose BFIX4b TO with patch shape, expected MV recovery, regression risk. Bundle into combined deploy package per CTO plan change.
    - **If multi-file/architectural fix needed:** MCP CTO+COO immediately — combined-deploy plan must pivot back to staged per CTO branch-point clause ("if BFIX3 or BFIX4 root cause is multi-file/architectural instead of surgical 1-file, MCP CTO+Andrew — may need to pivot back to staged").
    - **If upstream BD ingestion bug:** escalate to AE for BD positions feed audit; A_03 fix may not be possible.
    - **If non-financial cohort is intentionally excluded:** document as design choice; recovery for those 8 accts requires separate non-financial-account architecture work (separate TO).

    **OUT OF SCOPE for this TO:**
    - NO code changes (investigation only)
    - NO fix authoring within this TO (BFIX4b is a SEPARATE follow-on TO if applicable)
    - BFIX1 / BFIX2 / BFIX3 scope (separate fixes, sequenced before this on the same ~A lane)
    - B_00 silver-layer modifications
    - canonical_holdings / canonical_nna / firm_composition pipeline
    - Pricing methodology (canonical_prices, etc.)
    - Bronze-layer ingestion changes (if needed, escalate to AE)
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="surface mapping (mandatory before per-account trace)">
      <step>
        <run>comp-pipescript io A_03.positions_cube — full READ + WRITE manifest</run>
        <expect>Source enumeration: BD positions, BD transactions, Schwab RPS, mapping, asset dim, etc. Filter clauses + JOIN keys identified.</expect>
        <if_mismatch>If A_03 isn't the actual producer of positions_cube, identify the real producer.</if_mismatch>
      </step>
      <step>
        <run>comp-blast positions_cube — downstream consumer chain</run>
        <expect>Consumers: B_00, B_01, C_03, C_06, D_02, D_03 (per CTO 20260420T190431Z). Confirm + document any additional consumers.</expect>
        <if_mismatch>Surprise consumers = blast radius wider than known; flag in Phase 0.</if_mismatch>
      </step>
      <step>
        <run>grep A_03 for filter/exclusion clauses: account_type, asset_class, is_*, custodian, etc.</run>
        <expect>Full list of conditions that determine which accounts/positions reach the cube.</expect>
        <if_mismatch>If filters are implicit (not explicit conditions), code structure analysis needed.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="per-account evidence collection">
      <step>
        <run>For 3-5 accounts in Cohort 1 (absent_from_cube) — full trace: BD source → A_03 working tables → cube output. Identify drop point.</run>
        <expect>File:line root cause for each account. Likely converges on 1-2 mechanism types.</expect>
        <if_mismatch>If accounts drop at different points, multiple bugs exist; document each.</if_mismatch>
      </step>
      <step>
        <run>For 3-5 accounts in Cohort 2 (fp_dust_in_cube) — full buy/sell history trace + A_03 lot-tracking output. Identify FIFO depletion mechanism.</run>
        <expect>Clear evidence of whether buys are truncated (lookback issue) or FIFO over-depletes.</expect>
        <if_mismatch>If neither hypothesis fits, document the actual mechanism.</if_mismatch>
      </step>
      <step>
        <run>For 3-5 accounts in Cohort 3 (non-financial absent_from_cube) — confirm asset class + check A_03's asset-class admission logic.</run>
        <expect>Either: (a) explicit exclusion clause for non-financial assets (intentional), or (b) implicit drop via some other filter (potential fix).</expect>
        <if_mismatch>If non-financial assets are admitted but still dropped, mechanism is elsewhere.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="trace document + decision">
      <step>
        <run>Author trace document at data/black_diamond/diagnostics/STAUDT/BFIX4/a03_positions_cube_trace.md per scope</run>
        <expect>Complete trace doc: surface map, hypothesis evaluation (H1-H6), per-account evidence (3+ per cohort), file:line root cause(s), decision verdict.</expect>
        <if_mismatch>If trace is inconclusive after Phase 1, document additional data needed to close.</if_mismatch>
      </step>
      <step>
        <run>MCP COO + CTO with trace doc + decision verdict. If 1-file fix proposable, include BFIX4b TO sketch. If architectural, surface for combined-deploy plan pivot.</run>
        <expect>Decision-ready summary. CTO+COO can authorize BFIX4b authoring (or pivot to staged deploy) from the trace.</expect>
        <if_mismatch>If decision is unclear, MCP for adjudication before committing to a fix path</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/BFIX4/a03_positions_cube_trace.md</path>
      <description>End-to-end A_03 trace covering all three cohorts (absent_from_cube / fp_dust_in_cube / non-financial absent). Surface map, hypothesis evaluation H1-H6, per-account evidence (3+ per cohort), file:line root cause(s), decision verdict (1-file fix / multi-file / upstream-BD / intentional-design).</description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] a03_positions_cube_trace.md identifies root cause(s) with file:line evidence for 3+ accounts per cohort (9+ total accounts traced)
    - [ ] Hypothesis evaluation section weighs H1-H6 against gathered evidence (rules in / out)
    - [ ] Decision verdict: (a) 1-file fix proposable + BFIX4b shape, (b) multi-file/architectural escalation needed + combined-deploy pivot recommendation, (c) upstream BD ingestion bug + AE escalation, or (d) intentional design choice (non-financial cohort) + separate-TO recommendation
    - [ ] MCP to COO+CTO with trace doc + verdict before any further action
    - [ ] NO code changes in this TO (investigation only)
    - [ ] Phase 0 sequencing: starts after BFIX3 close (single ~A lane with engine-wave context preserved)
  </acceptance_criteria>

  <guardrails>
    - **Investigation only.** Do NOT patch A_03 or any other script in this TO. Fix dispatch is a separate BFIX4b TO if warranted.
    - **No theory-as-conclusion.** Per `feedback_no_unverified_theories_as_conclusions.md`, label hypotheses as theories until evidence closes them. The "PCRA filter", "FIFO depletion", "non-financial exclusion" candidates are all theories until traced.
    - **Sequential after BFIX3 close.** Don't start until BFIX3 trace is filed and verdict reached. Keeps engine-accuracy investigation linear on ~A's lane.
    - **Read-only.** No S3 writes. No A_03 patches. No deploy.
    - **Combined-deploy plan dependency:** if BFIX4 root cause is 1-file surgical, BFIX4b ships as part of combined BFIX1+2+3+4 package per CTO 20260420T194200Z. If multi-file/architectural, MCP CTO+Andrew immediately to pivot back to staged deploy.
    - **No emojis, selective staging, agent commit identity** per existing memory rules.
  </guardrails>

  <agent_context_setup>
    1. Same context as BFIX1+BFIX2+BFIX3 (engine_accuracy + briefing already in your head; BFIX1 Phase 0 mechanism note already authored)
    2. Add: A_03.positions_cube.py (likely full file given cube architecture is central)
    3. BD positions / silver positions structure
    4. A_03 working tables / intermediate artifacts (find via comp-pipescript io A_03)
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1: ACK after BFIX3 trace + decision verdict closes
    - Phase 0+1+2 gate: single MCP to COO+CTO with trace doc + decision verdict
    - RAVC step 4: closeout when (a) BFIX4b TO authored OR (b) escalation pivot to staged deploy proposed OR (c) upstream-BD escalation surfaced to AE OR (d) design-choice documented + non-financial separate TO proposed
  </completion_protocol>
</task_order>
