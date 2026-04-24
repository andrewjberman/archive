<task_order>
  <metadata>
    <id>ADVI_49EXEC.001</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to><!-- base lane; ~ instances may be re-dialed if base saturated -->
    <date>2026-04-15</date>
    <status>pending</status><!-- dispatched 2026-04-24 by COO per Andrew 'unblock 49EXEC lane' directive; DS base bandwidth freed post ROLLUP 52/0/3/+1. Runs parallel with TO 5; TO 2 remains staged pending TO 1 close. -->
    <project_code>ADVI_49EXEC</project_code>
    <priority>P1 (gates TO 2 LLM generator)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_49EXEC.md §3 (template library) + §7 TO 1</ref>
    <ref type="prd_commit">2523e149</ref>
  </references>

  <objective>
    Build the deterministic Python that reads platinum artifacts and evaluates the 6 slot triggers from PRD §3:
    - leaderboard_rank_delta
    - top_nna_mover
    - biggest_position_gain
    - biggest_position_loss
    - fee_change
    - cohort_drift

    Emits structure: `triggered_slots: [{slot, headline, evidence_keys}]` per advisor. Pure data — NO LLM call in this TO. Unit tests per slot with fixture data.

    **PII GATE (HARD):** No cleartext can enter prompt construction surface. Phase 1 `comp-pii audit` must pass before any prose-prompt scaffolding is committed.

    **Output:** Python module(s) at `data/black_diamond/scripts/exec_summary/` (or wherever fits gold-script convention); pytest fixtures at `tests/exec_summary/`.
  </objective>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/exec_summary/template_library.py</file>
      <file action="create">data/black_diamond/scripts/exec_summary/trigger_eval.py</file>
      <file action="create">tests/exec_summary/test_trigger_eval.py</file>
      <file action="create">tests/exec_summary/fixtures/*</file>
    </files>
  </scope>

  <wire_contract>
    Per-slot trigger function signature: `evaluate_{slot}(advisor_id, platinum_reads) -> Optional[TriggeredSlot]`. TriggeredSlot dataclass: `{slot: str, headline: str, evidence_keys: list[str], detail_context: dict}`. detail_context is what TO 2 will use to build the LLM prompt; this TO produces the structured input.
  </wire_contract>

  <acceptance_criteria>
    1. All 6 slot evaluators implemented per PRD §3 trigger conditions.
    2. Per-slot pytest fixture coverage: trigger-positive case + trigger-negative case + edge case (e.g. missing data field).
    3. `evidence_keys` populated correctly for each triggered slot per PRD schema (S3 paths to source artifacts).
    4. PII assertion: `comp-pii audit platinum/advisors/*` + `comp-pii audit platinum/leaderboards/*` returns ZERO cleartext fields the templates depend on.
    5. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    6. MCP COMPLETE to COO + CTO with: module paths, test pass count, comp-pii audit transcript.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write — HARD GATE">
      <step>
        <run>comp-pii audit platinum/advisors/*</run>
        <expect>Zero cleartext fields. All advisor-scoped fields are pseudonymized.</expect>
        <if_mismatch>STOP. PII gate violated; surface to CTO + COO before proceeding. No prompt scaffolding work until clean.</if_mismatch>
      </step>
      <step>
        <run>comp-pii audit platinum/leaderboards/*</run>
        <expect>Zero cleartext fields.</expect>
        <if_mismatch>STOP. PII gate violated.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io D_00c &amp;&amp; comp-pipescript io D_02 &amp;&amp; comp-pipescript io D_04</run>
        <expect>Confirms platinum producers for leaderboard / advisor summary / position artifacts that the templates read.</expect>
        <if_mismatch>Re-baseline producer paths.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>pytest tests/exec_summary/ -v</run>
        <expect>All test cases PASS.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
      <step>
        <run>comp-blast template_library</run>
        <expect>No unexpected edges; new module standalone.</expect>
        <if_mismatch>Document new edges or refactor.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    Producer/consumer pair with TO 2 (DS LLM generator). TriggeredSlot dataclass is the contract.
  </cross_domain_coordination>

  <dependencies>
    <none/>
  </dependencies>

  <next>
    TO 1 close → TO 2 (DS LLM prose generator) consumes the trigger evaluator output.
  </next>
</task_order>
