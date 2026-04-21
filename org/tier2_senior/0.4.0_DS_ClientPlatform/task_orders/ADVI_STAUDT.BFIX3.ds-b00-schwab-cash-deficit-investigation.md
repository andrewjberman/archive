<task_order>
  <metadata>
    <id>ADVI_STAUDT.BFIX3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-20</date>
    <status>complete</status><!-- CANCELLED 2026-04-20 ~22:00Z per Andrew "we don't track that" directive. Phase 0 by ~A surfaced BD has two incompatible cash models (allocations model: account-level cash_market_value from accounting; transactions model: cash via tx side-effects only). A_03.positions_cube reads model 2 → only 14% of accts (853/5,919) have cash in cube; 5,397 accts ($27.95M) have BD-reported cash never entering cube. Originally planned Path Alpha (A_03 synth injection). Andrew decision: do not pass-through the ~654 untracked accts / $52M — BD structurally excludes these (SLATs/DAFs/HSAs/corporate entities); injecting black-box AUA with no composition is worse than omitting. Superseded by CTO active-filter brief (docs/briefs/aua_active_account_filter_redesign.md — DRAFT awaiting Andrew read) which proposes multi-signal active-account detector recovering ~$41M of currently-dropped cohort via different mechanism (admit accts with recent tx+custodian evidence, don't synth cash). Evidence: CTO session 34 continuation log `aua_active_filter_investigation_and_brief.md`; ~A BFIX3 Phase 0 mechanism note. Was DISPATCHED 20260420T18:30Z by 2.0.0_SA_COO per CTO directive 20260420T182548Z + Andrew approval 20260420T181200Z. Cancelled 20260420T22:00Z per Andrew chat directive. Reconciled by CTO session 36 audit 2026-04-21. -->
    <project_code>ADVI_STAUDT</project_code>
    <priority>P2 — investigation-only, 1-2h read-only scope. Sequential after BFIX1+BFIX2 close (keeps engine-accuracy investigation on single ~A lane with full context).</priority>
    <lane>~A — sequential after BFIX1+BFIX2. Investigation-only TO; ~A's existing engine_accuracy + briefing context is the foundation.</lane>
    <bug_reference>~A briefing 20260420 (data/black_diamond/diagnostics/STAUDT/BRIEFING_aua_engine_accuracy_2026-04-20.md §"Bug 2 — Schwab-side cash deficit"): $18.8M Schwab-mapped cash missing from canonical; 4,950 accounts with material BD cash NOT in canonical. Cohorts cancel ($25.7M Schwab BD cash → $6.9M canonical = -$18.8M Schwab; +$10.6M non-Schwab overshoot; firm net -$8.1M). Schwab RPS DOES carry cash (verified in RPS samples) and B_00's `_CASH_PATTERNS` constant explicitly excludes cash from `bd_stale` zeroing — so cash SHOULD flow through but doesn't. Investigation needed before fix dispatch.</bug_reference>
    <decision_authority>CTO 20260420T182548Z dispatch directive. Andrew approval 20260420T181200Z on briefing sequencing.</decision_authority>
  </metadata>

  <references>
    <ref type="briefing">data/black_diamond/diagnostics/STAUDT/BRIEFING_aua_engine_accuracy_2026-04-20.md (~A's exec briefing — Bug 2 §)</ref>
    <ref type="diagnostic">data/black_diamond/diagnostics/STAUDT/engine_accuracy_2026-04-20.md (loss decomposition — Bug 2 surfaced as part of "Schwab kept undershoot" cohort)</ref>
    <ref type="parent">project_bd_is_ground_truth.md (BD silver/allocations is the source-of-truth comparison anchor)</ref>
    <ref type="parent">feedback_no_unverified_theories_as_conclusions.md (treat the cause hypothesis as theory until evidence closes; investigate before dispatching fix)</ref>
    <ref type="prior-fixes-on-same-script">BFIX1 (bd_stale predicate, P1 in ~A lane) + BFIX2 (non-Schwab pass-through, P1 in ~A lane). BFIX3 sequences AFTER both close.</ref>
  </references>

  <objective>
    Trace `is_cash` (and equivalent cash-handling) end-to-end through B_00.canonical_holdings.py and the upstream BD positions feed to localize where the Schwab-mapped cash deficit ($18.8M, 4,950 accounts) is being introduced. Produce a written cash-flow trace document with file:line evidence for the drop point + BD-vs-canonical comparison for 3+ specific accounts. If the localized root cause supports a 1-file surgical fix, propose a follow-on BFIX3b TO with the patch shape. If it spans multiple layers, surface to CTO+COO for scope decomposition. NO code changes in this TO — investigation only.
  </objective>

  <scope>
    **Investigation question (verbatim from briefing §"Bug 2"):**
    Is cash being filtered or skipped on the BD side of the merge in B_00, OR is the upstream BD positions feed not carrying cash?

    **Specific accounts to trace as proof-of-mechanism:**
    Per briefing top examples (all Schwab-mapped, all $0 in canon_cash but material BD cash):
    - Craig Smith Rollover IRA: BD cash $2.51M, canonical $0
    - DONALD WAYNE CRABBE: BD $1.10M, canonical $0
    - Steve Jr & Mary Humphrey Joint Brokerage: BD $1.07M, canonical $0
    - Tracey Hopper Individual: BD $950K, canonical $0
    - Matthew & Malita Nixon JTWROS: BD $700K, canonical $0
    - Ila Jehl Rollover IRA: BD $673K, canonical $0

    **Trace path (read-only investigation):**

    1. **Bronze layer / BD positions feed:** Does BD positions data (silver/positions or whatever feeds B_00) carry cash positions for these specific accounts on 2026-04-16? If absent at bronze/silver source, the bug is in BD ingestion (out of B_00 scope). If present, continue to B_00.

    2. **Schwab RPS layer:** Does Schwab RPS partition for 2026-04-16 carry cash positions for these accounts? Per briefing, RPS samples confirmed YES — re-confirm for the named accounts specifically.

    3. **B_00.canonical_holdings.py:** Read the cash-handling code paths. `_CASH_PATTERNS` constant is referenced as excluding cash from `bd_stale` zeroing — confirm this exclusion is correctly applied at the merge step. Look for: filter/where clauses that drop is_cash rows, account-level cash fields that are not propagated to per-position output, JOIN keys that don't match for cash positions.

    4. **canonical/holdings output:** Confirm cash positions are absent from canonical/holdings/2026-04-16.parquet for the named accounts (already confirmed via diagnostic; this just validates the trace endpoint).

    **Hypotheses to evaluate (do not pre-commit to one — gather evidence first):**
    - H1: B_00 filter clause drops is_cash rows from BD positions before the merge
    - H2: The merge JOIN key mismatches for cash positions (e.g., BD cash uses synthetic asset_id, Schwab RPS uses 'CASH' literal, no match)
    - H3: B_00 cash-handling code path exists but is gated on a flag/condition that's not firing for Schwab-mapped accounts
    - H4: Upstream BD positions feed itself is incomplete for cash (bug is outside B_00)
    - H5: Reconciliation logic treats cash differently for Schwab vs non-Schwab (asymmetric handling explains the cohort cancellation pattern: -$18.8M Schwab, +$10.6M non-Schwab)

    **Decision tree post-investigation:**
    - **If 1-file surgical fix in B_00:** propose BFIX3b TO with patch shape, expected MV recovery, regression risk. ETA <1h authoring.
    - **If multi-layer fix needed:** surface to CTO+COO with decomposition proposal (which TOs to author, which lanes, sequencing).
    - **If upstream BD ingestion bug:** surface to AE for BD positions feed audit.

    **OUT OF SCOPE for this TO:**
    - NO code changes (investigation only)
    - NO fix authoring within this TO (BFIX3b is a SEPARATE follow-on TO if applicable)
    - BFIX1 / BFIX2 scope (separate fixes, sequenced before this)
    - Non-Schwab cash overshoot ($10.6M direction) — that's the offsetting cohort, document but don't try to fix in BFIX3
    - Pricing methodology unification — separate concern
    - Bug 1 + Bug 3 deepdives (already handled by BFIX1 + BFIX2)
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="surface mapping">
      <step>
        <run>comp-pipescript io B_00.canonical_holdings — full READ + WRITE manifest, identify all cash-related code paths</run>
        <expect>Sources for BD positions, Schwab RPS, mapping table all enumerated. Cash-handling code locations identified.</expect>
        <if_mismatch>If cash-handling code is not visible from comp-pipescript io output, expand grep manually.</if_mismatch>
      </step>
      <step>
        <run>comp-trace account_market_value --direction both (or equivalent for cash flow) — trace cash through the silver→canonical→firm_composition chain</run>
        <expect>Full upstream + downstream chain. Confirm cash drop point is between BD positions input and canonical/holdings output.</expect>
        <if_mismatch>If drop point is upstream of B_00, escalate to AE — BD ingestion is out of B_00 scope.</if_mismatch>
      </step>
      <step>
        <run>grep -n -E "is_cash|cash|CASH" data/black_diamond/scripts/silver/B_00.canonical_holdings.py — enumerate every cash reference</run>
        <expect>Full list of cash-handling lines: filter clauses, _CASH_PATTERNS usage, account-level cash fields, JOIN logic.</expect>
        <if_mismatch>If grep output is sparse (e.g., <5 cash references), cash handling may be implicit (e.g., no special path = cash flows through general path) — investigate why named accounts don't.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="account-level evidence collection">
      <step>
        <run>For each of 3-5 named accounts (Craig Smith Rollover IRA, DONALD WAYNE CRABBE, Steve Jr & Mary Humphrey, etc.), pull cash position from: (a) BD positions/silver source, (b) Schwab RPS 2026-04-16, (c) canonical/holdings output. Build per-account 3-column table.</run>
        <expect>Clear evidence of where each account's cash exists vs disappears. Likely all three rows: BD has cash, Schwab RPS has cash, canonical has $0.</expect>
        <if_mismatch>If BD or Schwab RPS does NOT have cash for these accounts, the briefing premise is wrong; surface immediately.</if_mismatch>
      </step>
      <step>
        <run>Local dry-run B_00 with print/log instrumentation around the cash code paths for the named accounts. Identify the exact line where cash is dropped.</run>
        <expect>Line-level identification of the drop. Document file:line in the trace doc.</expect>
        <if_mismatch>If dry-run cannot be instrumented locally, document the closest hypothesized line + reason.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="trace document + decision">
      <step>
        <run>Author trace document at data/black_diamond/diagnostics/STAUDT/BFIX3/cash_flow_trace.md per scope.</run>
        <expect>Complete trace doc: surface map, hypothesis evaluation, account-level evidence, root-cause file:line, decision verdict (1-file fix / multi-layer / upstream).</expect>
        <if_mismatch>If trace is inconclusive after Phase 0+1, document what additional data is needed to close.</if_mismatch>
      </step>
      <step>
        <run>MCP COO + CTO with trace doc location + decision verdict + (if applicable) BFIX3b TO proposal shape</run>
        <expect>Decision-ready summary with file:line root cause. COO+CTO can authorize BFIX3b authoring (or scope decomposition) from the trace.</expect>
        <if_mismatch>If decision is unclear, MCP for adjudication before committing to a fix path</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/BFIX3/cash_flow_trace.md</path>
      <description>End-to-end is_cash handling trace through B_00 + upstream BD positions feed. Surface map, hypothesis evaluation, per-account 3-column evidence (BD / Schwab RPS / canonical), file:line root cause, decision verdict.</description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] cash_flow_trace.md identifies exact source of cash drop (file:line) with BD-vs-canonical evidence for 3+ named accounts
    - [ ] Hypothesis evaluation section weighs H1-H5 against gathered evidence (rules in / out)
    - [ ] Decision verdict: (a) 1-file fix proposable + BFIX3b shape, (b) multi-layer escalation needed + decomposition proposal, or (c) upstream BD ingestion bug + AE escalation
    - [ ] MCP to COO+CTO with trace doc + verdict before any further action
    - [ ] NO code changes in this TO (investigation only)
  </acceptance_criteria>

  <guardrails>
    - **Investigation only.** Do NOT patch B_00 or any other script in this TO. Fix dispatch is a separate BFIX3b TO if warranted.
    - **No theory-as-conclusion.** Per `feedback_no_unverified_theories_as_conclusions.md`, label hypotheses as theories until evidence closes them. The "B_00 filter logic" and "BD positions feed" candidates are both theories until you trace.
    - **Sequential after BFIX1+BFIX2.** Don't start until those close; keeps your engine-accuracy mental context unified and avoids B_00 working-tree conflicts.
    - **Read-only.** No S3 writes. No B_00 patches. No deploy.
    - **No emojis, selective staging, agent commit identity** per existing memory rules.
  </guardrails>

  <agent_context_setup>
    1. Same context as BFIX1 + BFIX2 (engine_accuracy + briefing already in your head)
    2. Add: B_00.canonical_holdings.py cash-handling code window
    3. Schwab RPS partition structure for 2026-04-16
    4. BD positions / silver positions structure for 2026-04-16
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1: ACK after BFIX1+BFIX2 close
    - Phase 0+1+2 gate: single MCP to COO+CTO with trace doc + decision verdict
    - RAVC step 4: closeout when (a) BFIX3b TO authored OR (b) escalation decomposition proposed OR (c) upstream-BD escalation surfaced to AE
  </completion_protocol>
</task_order>
