<task_order>
  <metadata>
    <id>ADVI_STAUDT.BFIX1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to><!-- originally ~A sub-lane; base serial post 2026-04-21 sub-lane-cleanup -->
    <date>2026-04-20</date>
    <status>pending</status><!-- DISPATCHED 20260420T17:25Z by 2.0.0_SA_COO. Andrew approval 2026-04-20 in chat ("Agreed on all counts go ahead") on engine refinement plan. Code shipped 081223b5 + fix-forward 1a54d46a; AE uploaded. Awaiting cf5bd5ad chain-full validation + comparison-pack attribution evidence for RAVC4 close. Status normalized 2026-04-21 (dispatched -> pending for operator schema). -->
    <project_code>ADVI_STAUDT</project_code>
    <priority>P1 — engine refinement, NOT P0 (qa-runner watchdog incident in flight, no immediate deploy pressure). Closes 80% of the firm AUA accuracy gap ($38.6M of $48.3M). Bundled with BFIX2 (non-Schwab pass-through) in same ~A wave; same script B_00.canonical_holdings.py.</priority>
    <lane>~A — bundled with BFIX2. ~A authored the engine_accuracy diagnostic and owns the B-layer surface for this wave.</lane>
    <bug_reference>~A engine accuracy report 20260420T (data/black_diamond/diagnostics/STAUDT/engine_accuracy_2026-04-20.md §"#1 — bd_stale overreach"): B_00.canonical_holdings.py L456-500 implements `bd_stale` rule that zeros BD positions for "Schwab-covered" accounts when no Schwab RPS match. The "Schwab-covered" predicate is `account_id present in schwab_bd_account_mapping` — true for any account that ever appeared in a Schwab fee file, even when Schwab RPS structurally doesn't carry positions (PCRA, AQR, Fidelity 401k, Schwab Trust Bank). 111 accounts incorrectly zeroed = $38.6M MV loss = 80% of the -284bps firm AUA gap.</bug_reference>
    <decision_authority>Andrew chat 2026-04-20 ("Agreed on all counts go ahead") on engine refinement plan (1)+(2)+(3 deferred).</decision_authority>
  </metadata>

  <references>
    <ref type="diagnostic">data/black_diamond/diagnostics/STAUDT/engine_accuracy_2026-04-20.md (~A loss decomposition + 50bps target framing)</ref>
    <ref type="related-fix">ADVI_STAUDT.BFIX2 — bundled with this; non-Schwab pass-through path. Same script, same wave, single ~A commit.</ref>
    <ref type="diagnostic-precedent">data/black_diamond/diagnostics/STAUDT/phantom_buyhold_partition_2026-04-20.{md,json,parquet} (Schwab-side gap profile)</ref>
    <ref type="cross-reference">ADVI_STAUDT.KPI — engine accuracy 50bps sentinel TO (~C lane). After BFIX1+BFIX2 land, KPI sentinel becomes the regression gate.</ref>
  </references>

  <objective>
    Tighten the `bd_stale` predicate in B_00.canonical_holdings.py L456-500 so it only fires when there is positive evidence that an account's positions ARE actually carried on Schwab RPS (not merely that the account appears in any Schwab fee mapping). Recovers ~$38.6M of MV currently zeroed for PCRA / AQR / Fidelity-401k / Schwab Trust Bank accounts that are mapped via fees but not present on the Schwab RPS feed. Closes 80% of the firm AUA accuracy gap toward the 50bps target.
  </objective>

  <scope>
    **Defect (verbatim from engine_accuracy_2026-04-20.md §"#1"):**
    `bd_stale` rule sets units = 0 if a BD position has no matching Schwab RPS entry AND the account is "Schwab-covered". The "Schwab-covered" predicate is `account_id present in schwab_bd_account_mapping`. That predicate is too loose — it's true for any account that ever appeared in a Schwab fee file, even if Schwab RPS structurally never carries the account's positions. 111 accounts affected, $38.6M MV lost. Floating-point dust signature (1e-11 to 1e-15 non-zero canonical units in 15 of these accounts) confirms zero-by-multiplication, not absent.

    **Two viable directions to evaluate in Phase 0 + choose for Phase 1:**

    **Direction 1 — custodian classification field on the mapping:**
    Add a `custodian_class` column to `schwab_bd_account_mapping` (or join from a custodian dimension): values in {`schwab_brokerage`, `schwab_pcra`, `non_schwab_via_schwab_fees`}. Apply `bd_stale` ONLY when `custodian_class == 'schwab_brokerage'`. Cleaner long-term; requires upstream mapping data + classification logic.

    **Direction 2 — positive-RPS-evidence requirement:**
    Apply `bd_stale` ONLY when the account has at least N positions on Schwab RPS within the last K days (suggested defaults: N=1, K=30). If Schwab RPS is structurally silent for the account, bd_stale doesn't fire and BD positions are trusted. No mapping-schema change; lookup against the Schwab RPS partition.

    **Trade-offs to document in Phase 0 evidence:**
    - Direction 1 is more declarative + easier to audit + supports future custodian-aware logic, but requires source-of-truth on custodian classification (does silver/holdings_lots or another silver source already carry this?).
    - Direction 2 is more conservative + self-evidencing + immediately deployable, but adds a Schwab RPS lookup per account in B_00 (perf cost — confirm it's negligible at the candidate-account level).

    **Acceptance per engine_accuracy_2026-04-20.md §"Path to 50bps" #1:** ~$38.6M recovered. Specifically, the 15 named PCRA/AQR/Fidelity/Schwab-Trust-Bank top accounts (BRYAN GRUNDHOEFER $5.08M, CRAIG SMITH $2.50M, David Victor IRA $2.47M, etc.) should have non-zero canonical units matching BD silver MV within reasonable tolerance ($10K per account or ratio match within 1%).

    **Pre-fix safety check (mandatory):**
    Verify that BFIX1 doesn't INCREASE canonical MV for any well-reconciled Schwab-brokerage account. The fix should ONLY restore zeroed MV; it should not double-count or cause new overshoot for accounts that were correctly zeroed. Compare per-account MV pre-fix vs post-fix on the 5,439 Schwab-mapped cohort — only the 111 problematic accounts (and small adjacent pop) should change.

    **OUT OF SCOPE:**
    - Schwab kept-account undershoot ($19.5M, ~A is currently drilling separately) — separate fix needed
    - Non-Schwab pass-through ($18.5M) — that's BFIX2, bundled
    - Non-Schwab kept overshoot (-$16M) — separate diagnostic
    - Pricing methodology unification (canonical_prices vs BD internal pricing) — separate concern
    - Mapping schema migration (if Direction 1 chosen, scope the schema change but defer execution to a separate TO if AE involvement needed)
    - Option B canonical/D-layer scope (OPB owns) — engine fixes are silver-layer, separate concern
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="pre-fix diligence">
      <step>
        <run>Read B_00.canonical_holdings.py L450-510 — full bd_stale block context. Identify: predicate location, mapping-lookup mechanism, Schwab RPS reference path.</run>
        <expect>Clear identification of the L456-500 block boundaries + dependencies. Document current predicate logic exactly.</expect>
        <if_mismatch>If block boundaries differ from diagnostic, MCP COO with grep + line-number evidence.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io B_00.canonical_holdings — confirm READS for schwab_bd_account_mapping + Schwab RPS partition</run>
        <expect>Mapping source + Schwab RPS source both enumerated. If Direction 2 chosen, confirm Schwab RPS read is already in B_00's reads list (no new dependency).</expect>
        <if_mismatch>If Schwab RPS isn't already read, Direction 2 adds a new dependency — flag in Phase 0 mechanism note.</if_mismatch>
      </step>
      <step>
        <run>comp-blast B_00 — confirm downstream consumers of B_00's canonical/holdings output</run>
        <expect>Map: B_00 canonical/holdings → C-layer scripts (C_01, C_03, etc.) → D-layer. Identify any consumer that might be sensitive to the recovered MV (e.g., advisor leaderboards, AUM caps).</expect>
        <if_mismatch>Surprise consumers = scope must address them in BFIX1 acceptance. If FIX7-class RA-P5 logic re-fires on different MV, escalate.</if_mismatch>
      </step>
      <step>
        <run>Numerical preview: with current code, count exactly how many of the 111 problematic accounts have BD positions and zero canonical units; sum BD MV. Confirm matches the $38.6M diagnostic figure.</run>
        <expect>~111 accounts, ~$38.6M total. If significantly different, recompute baseline before patching.</expect>
        <if_mismatch>If baseline drift > $5M from diagnostic, refresh diagnostic before patching.</if_mismatch>
      </step>
      <step>
        <run>Investigate Direction 1 feasibility: does silver/holdings_lots, silver/accounts_dim, or any silver source already carry custodian classification? Grep silver-layer scripts for "custodian", "PCRA", etc.</run>
        <expect>Either find existing classification source OR confirm none exists.</expect>
        <if_mismatch>If existing classification source has incorrect data for the 111 accounts (e.g., classifies all as schwab_brokerage), Direction 1 needs upstream fix first.</if_mismatch>
      </step>
      <step>
        <run>MCP COO with Phase 0 finding: chosen direction (1 vs 2) + rationale + intended patch shape + perf estimate (Direction 2) or upstream-data confirmation (Direction 1). Wait for COO go before Phase 1.</run>
        <expect>COO ACK + GO before patching</expect>
        <if_mismatch>If COO objects to direction, iterate on direction choice</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="patch + validation">
      <step>
        <run>Apply chosen direction patch to B_00.canonical_holdings.py L456-500. Bundle with BFIX2 (non-Schwab pass-through) in same commit if both Phase 0 gates passed.</run>
        <expect>Single commit on B_00 covering both fixes. Comment block citing engine_accuracy diagnostic + Andrew approval.</expect>
        <if_mismatch>Any logic change beyond the predicate + new pass-through path = scope creep, escalate.</if_mismatch>
      </step>
      <step>
        <run>Local dry-run B_00 + downstream C_01 (canonical_nna writer) on current prod date. Compare canonical/holdings MV pre-fix vs post-fix per account.</run>
        <expect>~111 accounts move from $0 → BD MV (sum ~$38.6M). 5,300+ Schwab-brokerage accounts unchanged. No double-counting or new overshoot in the well-reconciled cohort.</expect>
        <if_mismatch>If MV change extends beyond the 111 + adjacency, re-audit predicate. If any well-reconciled account shifts > $10K, regression — fix.</if_mismatch>
      </step>
      <step>
        <run>End-to-end firm AUA: re-run engine_accuracy diagnostic post-patch. Firm canonical MV should land within $9.7M of BD silver ($1,697.7M target, +/- 50bps tolerance).</run>
        <expect>Post-BFIX1 alone: gap closes to ~-$9.7M (50bps). Post-BFIX1+BFIX2 combined: gap likely flips to ~+$8M overshoot (still within 50bps absolute).</expect>
        <if_mismatch>Gap not closing as expected = mechanism understanding wrong. Halt + escalate.</if_mismatch>
      </step>
      <step>
        <run>comp-validate B_00 (or canonical_holdings if separate config exists)</run>
        <expect>Exit 0. If a 50bps sentinel exists post-KPI TO, also exit 0.</expect>
        <if_mismatch>Exit != 0 = fix incomplete or KPI tightening conflict</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/scripts/silver/B_00.canonical_holdings.py</path>
      <description>bd_stale predicate tightening at L456-500 per chosen direction (1 or 2). Bundled with BFIX2 in same commit.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/scripts/gold/gold_validate_config.yaml</path>
      <description>If BFIX1 chooses Direction 1, add a sentinel for custodian_class field presence + non-null. If Direction 2, add a sentinel that bd_stale fires on at most ~5,439 - 111 = 5,328 accounts (don't over-zero).</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/BFIX1/bfix1_evidence.md</path>
      <description>Phase 0 direction choice + rationale + Phase 1 per-account MV diff + firm-level AUA pre/post + recovered-account sample table (15 named accts from diagnostic).</description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] Phase 0 direction choice (1 vs 2) MCP'd to COO + GO received before patching
    - [ ] Single ~A commit covering BFIX1 + BFIX2 on B_00
    - [ ] Commit message cites engine_accuracy_2026-04-20.md + Andrew chat approval
    - [ ] Post-patch: 15 named diagnostic accounts (BRYAN GRUNDHOEFER / CRAIG SMITH / David Victor IRA / etc.) have non-zero canonical units within 1% of BD silver MV
    - [ ] No well-reconciled Schwab-brokerage account MV moves >$10K (no regression)
    - [ ] Firm AUA gap closes to within 50bps of BD silver/allocations
    - [ ] comp-validate B_00 exit 0
    - [ ] DT upload from `git show {sha}:path` (committed-ref pattern)
    - [ ] BFIX2 acceptance criteria also met (bundled)
  </acceptance_criteria>

  <guardrails>
    - **No Option B overlap:** BFIX1 is silver-layer (B_00); OPB is canonical/D-layer. If Phase 0 surfaces "while I'm here, also do schema work", defer.
    - **No mapping schema migration without AE:** if Direction 1 needs new `custodian_class` column added to upstream mapping, scope the schema change but DEFER execution — that's an AE / silver-ingestion TO.
    - **Pre-flag CTO+COO before B_00 S3 upload** — silver-layer scripts also fall under A→D-rerun-sensitive pre-flag (engine MV change has firm-wide blast radius).
    - **Bundled with BFIX2.** Single commit, single S3 upload, single qa-runner cycle. Don't ship BFIX1 alone — combined fixes give the cleanest validation story.
    - **No emojis, selective staging, agent commit identity, working-tree S3 upload prohibition** per existing memory rules.
  </guardrails>

  <agent_context_setup>
    1. Register + inbox-watch (first two tool calls)
    2. Read:
       - data/black_diamond/diagnostics/STAUDT/engine_accuracy_2026-04-20.md (your own diagnostic)
       - B_00.canonical_holdings.py L450-510 (bd_stale block)
       - schwab_bd_account_mapping source (silver/ or canonical/ — confirm via comp-pipescript io)
       - silver/holdings_lots + any custodian-classification source (Direction 1 evaluation)
    3. Heartbeat every 60s during active work
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1: ACK within 5 min, bundled with BFIX2
    - Phase 0 gate: bundled MCP with BFIX2 Phase 0
    - Phase 1 gate: bundled MCP — per-account MV diff + firm-level AUA pre/post for both fixes
    - RAVC step 4: DT upload + qa-runner B-layer cycle (or full --group ABC if needed) + per-account validation evidence
  </completion_protocol>
</task_order>
