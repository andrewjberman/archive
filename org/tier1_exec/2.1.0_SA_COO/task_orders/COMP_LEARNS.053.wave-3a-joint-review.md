<task_order>
  <metadata>
    <id>2.1.0_SA_COO-and-1.1.0_SA_CTO-2026-04-22-comp-learns-053-wave-3a-joint-review</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SA_COO + 1.1.0_SA_CTO (joint)</issued_to>
    <date>2026-04-22</date>
    <status>complete <!-- COO 8bf465d9 + CTO 954f86e6; joint closure commit 2026-04-24; Wave 3a closed; Wave 3b authorized --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — mandatory Wave 3a closure gate (§10 success criterion 3); CTO Wave 3b decision</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_WAVE3_V1.md §6 step 8 (CTO review) + §7 (Stage 2 wave counting) + §10 (success criteria) — commit 30971db1</ref>
    <ref type="prerequisite_tos">.048 dev-4 loop-proving COMPLETE + .051 Case 3 two-phase scoring COMPLETE</ref>
    <ref type="wave3b_scope">.053 decision input to Wave 3b scope (Cases 1+2 rerun under Stage 2 + mutation-family strategy expansion)</ref>
  </references>

  <objective>
    Close Wave 3a with a joint review of dev-4 output + Case 3 verdict. Issue Wave 3b
    decision (proceed as planned, course-correct, or pause).

    ## COO section (2.1.0_SA_COO)

    1. Read dev-4 outputs from comp/results/dev-4/:
       - experiment_log.jsonl + champion_history.json + mutation_family_summary.md +
         plateau_analysis.md + loop_fitness_recommendation.md + result.json

    2. Read Case 3 outputs from comp/results/wave-3a/:
       - Phase 1 verdict files (per-condition) + Phase 2 metric_audit JSON + integrity_audit.md

    3. Write COO review memo at `comp/results/wave-3a/coo-review-memo.md`:
       - dev-4 loop summary: target hit Y/N, confirmation run evidence, primary winning
         mutation family, recommended settings for parallel expansion
       - Case 3 verdict summary: PASS/FAIL per condition, aided-vs-unaided efficiency
         delta narrative (one paragraph), noise flags if any
       - COO recommendation for Wave 3b: proceed | course-correct | pause, with one-line
         rationale
       - Stage 2 wave counting: Wave 3a = 1 of 2 clean waves toward §7 exit criterion.
         Confirm: zero preflight false-passes + zero integrity violations this wave.

    4. MCP CTO with stage2-gate bundle (this memo + links to all artifacts).

    ## CTO section (1.1.0_SA_CTO)

    5. Review COO memo + dev-4 outputs + Case 3 outputs independently.

    6. Independent Wave 3b decision, authored at
       `org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.WAVE3B-DECISION.md`:

       Required content:
       - dev-4 loop assessment (fit for parallel expansion? If YES, name the settings)
       - Case 3 measurement claim scope (what does directional evidence support? what
         does it NOT support per §3.7?)
       - Wave 3b scope: Cases 1+2 rerun under Stage 2? mutation-family strategy change?
         archetype breadth expansion? explicit Y/N per item
       - Stage 2 wave counter update: "Wave 3a contributes 1 of 2 clean waves" (or
         document why not, if preflight false-passes or integrity violations occurred)
       - Go/no-go trigger for Wave 3b kickoff

    7. If proceed: CTO may author Wave 3b PRD as separate document; this TO only closes
       Wave 3a.

    ## Closure

    8. Update org/projects/COMP_LEARNS.json `phase` + `blocking` fields to reflect Wave
       3a closure + Wave 3b trigger state (COO authors JSON update).

    9. Both flip TO status; this TO is JOINT ownership, requires both sign-offs.

    Explicitly out of scope:
    - Authoring Wave 3b PRD (separate CTO product after .053).
    - Re-executing dev-4 or Case 3 (only review here).
    - Making Wave 3b dispatch decisions ahead of CTO Wave 3b PRD (Wave 3b starts only
      after CTO issues Wave 3b PRD + COO decomposes into TOs).
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before COO memo">
      <step>
        <run>ls comp/results/dev-4/ comp/results/wave-3a/</run>
        <expect>All .048 + .051 output artifacts present.</expect>
        <if_mismatch>STOP. Upstream TOs not yet complete. Do not force review.</if_mismatch>
      </step>
      <step>
        <run>cat comp/results/wave-3a/integrity_audit.md | head -20</run>
        <expect>Integrity audit confirms Phase 1→2 ordering, reasoning.md exclusion, nav_log hygiene, no contamination.</expect>
        <if_mismatch>Flag SC to re-author integrity audit before review.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before COO commit">
      <step>
        <run>cat comp/results/wave-3a/coo-review-memo.md | head -5</run>
        <expect>Memo opens with explicit dev-4 summary + Case 3 summary + Wave 3b recommendation.</expect>
        <if_mismatch>Re-author with required opener.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after CTO Wave 3b decision">
      <step>
        <run>ls org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.WAVE3B-DECISION.md</run>
        <expect>CTO's Wave 3b decision TO exists.</expect>
        <if_mismatch>Wait for CTO ship before flipping .053 to complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>Joint TO — COO drafts + routes; CTO reviews + decides. If Wave 3b decision = pause, COO does not decompose further TOs. If proceed, CTO PRD → COO decomposition → next wave.</note>
    <shared_artifacts>comp/results/wave-3a/coo-review-memo.md (COO authors); org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.WAVE3B-DECISION.md (CTO authors); org/projects/COMP_LEARNS.json (COO updates phase + blocking)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/results/wave-3a/coo-review-memo.md authored with dev-4 summary + Case 3 summary + Wave 3b recommendation + Stage 2 wave counter update.
    2. CTO independent Wave 3b decision TO authored at org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.WAVE3B-DECISION.md.
    3. COMP_LEARNS.json phase + blocking fields updated to reflect Wave 3a closure + Wave 3b trigger state.
    4. Stage 2 wave count explicitly documented (Wave 3a = 1 of 2 per §7).
    5. Commits under respective authors; --only pathspec each.
    6. Pushed to CLOUD.
    7. Joint session log entries.
    8. MCP to Andrew: Wave 3a closed, Wave 3b decision issued, summary line.
  </acceptance_criteria>

  <dependencies>
    - Gate: .048 dev-4 (1.1.0_DS) COMPLETE with full §2.7 artifacts.
    - Gate: .051 SC two-phase scoring (2.1.0_SC) COMPLETE with Phase 1 + Phase 2 + integrity audit.
    - Parallel / informational: .052 dev-stress classifications (integrate into memo if notable).
    - Blocks: Wave 3b kickoff (CTO must issue Wave 3b decision before next wave can begin).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - Per §10 this is a MANDATORY Wave 3 closure gate — cannot skip even if all other Wave
      3a TOs ship cleanly.
    - Stage 2 counting per §7: Wave 3a is ONE wave; condition_a + condition_b are events
      within. Document explicitly in COO memo.
    - Wave 3 claim scope per §3.7: directional evidence only. Memo narrative must NOT
      overstate (e.g. "compiler works" → too strong; "aided run surfaced typehints.py
      faster on this case under single-model baseline" → correct scope).
    - No emojis.
  </operational_notes>

  <closeout>
    On completion:
    - COO: commit coo-review-memo.md + COMP_LEARNS.json update under --author=2.1.0_SA_COO
    - CTO: commit COMP_LEARNS.WAVE3B-DECISION.md under --author=1.1.0_SA_CTO
    - Both push to CLOUD
    - Flip .053 status to complete (joint — both execs' commits must land)
    - Joint MCP to Andrew with Wave 3a closure + Wave 3b trigger summary
    - Session logs under each exec's folder
  </closeout>
</task_order>
