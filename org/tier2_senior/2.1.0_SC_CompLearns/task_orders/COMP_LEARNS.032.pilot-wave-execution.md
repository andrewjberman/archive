<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-comp-learns-032-pilot-wave</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>1.1.0_DS_CompLearns + 1.3.0_DS_CompLearns (intervention runners) + 2.1.0_SC_CompLearns (scorer)</issued_to>
    <date>2026-04-21</date>
    <status>complete</status>
    <project_code>COMP_LEARNS</project_code>
  </metadata>

  <objective>
    Execute the first parallel scoring pilot wave (PARALLELIZATION_V1 §10).
    Two DS agents run Cases 1 and 2 under both harness conditions (aided + unaided).
    SC scores each event fresh (stateless new session per scoring event).
    Output: scoring verdicts with comparability-class labels + parallel-scoring
    integrity audit document demonstrating zero context leakage across all events.
  </objective>

  <context>
    .031 is GREEN (f0fdc5f5). Both task packets committed and CTO-signed:
    - Case 1: comp/tasks/task-001-httpx-netrc-host-authority/packet.yaml
              httpx PR #1298 — NetRC host:authority mismatch, structural bug localization
    - Case 2: comp/tasks/case-002-click-refactor/packet.yaml
              click 8.3.1 (SHA f80cf4b0) — nested command-group dispatch refactor,
              8-invariant preservation contract

    PILOT SHAPE (PRD §10 — hard scope):
    - Two DS agents: 1.1.0_DS_CompLearns + 1.3.0_DS_CompLearns
    - Two cases: Case 1 (structural localization) + Case 2 (regression-safe refactor)
    - Two conditions per case: unaided (condition_a) + aided_full (condition_b)
    - One scorer: 2.1.0_SC_CompLearns — fresh session per event, no exceptions
    - Total scoring events: 2 agents x 2 cases x 2 conditions = 8

    WORKTREE ISOLATION (PRD §8):
    Each DS agent works in their own worktree seeded from the task's baseline_commit.
    Worktree paths:
      C:/Users/AndrewBerman/Desktop/worktrees/comp-learns/task-001/ds-a/  (1.1.0_DS, Case 1)
      C:/Users/AndrewBerman/Desktop/worktrees/comp-learns/task-001/ds-b/  (1.3.0_DS, Case 1)
      C:/Users/AndrewBerman/Desktop/worktrees/comp-learns/task-002/ds-a/  (1.1.0_DS, Case 2)
      C:/Users/AndrewBerman/Desktop/worktrees/comp-learns/task-002/ds-b/  (1.3.0_DS, Case 2)
    Scorer worktrees: provisioned fresh per scoring event, disposed after verdict.

    CANDIDATE ARTIFACT BUNDLE (what each DS must produce per case/condition):
    - *.patch: git diff against baseline_commit showing all changes
    - test_output.txt: full pytest output for all acceptance criteria
    - reasoning.md: DS reasoning log (NOT exposed to scorer pre-verdict; exposed post-verdict for audit)

    SEQUENCING:
    Stage 1 — Human-gated (this wave). Each DS->Scorer handoff requires COO relay.
    DS completes a run → bundles artifacts → MCP COO → COO relays to SC → SC scores fresh session
    → SC verdict MCP to COO → COO records and relays to DS.
    Do NOT hand artifacts directly DS→SC without COO relay (Stage 1 gate discipline).

    SCORING DISCIPLINE (SC):
    - Fresh stateless session per scoring event (not /clear inside running session)
    - Clean worktree seeded from packet's baseline_commit + candidate bundle only
    - Scorer inputs: task_packet + candidate_bundle (diff + test_output ONLY) — NO reasoning.md
    - Every verdict must include: comparability class label + manifest_hash evidence
    - Items 13-15 checklist active (context isolation integrity, regime homogeneity, cross-run cert)
  </context>

  <run_order>
    Recommended sequencing (parallelize within each stage where possible):

    Stage A — unaided runs (condition_a):
    1a. 1.1.0_DS: Case 1 unaided (task-001, condition_a, worktree task-001/ds-a/)
    1b. 1.3.0_DS: Case 2 unaided (case-002, condition_a, worktree task-002/ds-b/)
    [1a + 1b run in parallel — different cases, no shared state]
    After both: 1.1.0_DS runs Case 2 unaided; 1.3.0_DS runs Case 1 unaided
    [complete all 4 unaided bundles before any aided runs]

    Stage B — aided runs (condition_b):
    2a. 1.1.0_DS: Case 1 aided (task-001, condition_b, fresh worktree task-001/ds-a-aided/)
    2b. 1.3.0_DS: Case 2 aided (case-002, condition_b, fresh worktree task-002/ds-b-aided/)
    [2a + 2b in parallel; then cross-case aided runs]

    SC scores each bundle as it arrives — no batching. Fresh session per event.
    COO collects all 8 verdicts and commissions the integrity audit document.
  </run_order>

  <acceptance_criteria>
    1. 8 candidate bundles produced (2 DS x 2 cases x 2 conditions). Each bundle: diff + test_output.
    2. 8 scoring verdicts issued by SC — each with comparability class + manifest_hash.
    3. Zero context-leakage incidents across all scoring events (SC certifies per §5 checklist items 13-15).
    4. At least one cross-DS comparison emitted with manifest-hash evidence.
    5. At least one aided-vs-unaided comparison on the same case.
    6. Parallel-scoring integrity audit document: comp/results/pilot-wave-1/integrity_audit.md
       — covers every scoring event, all cross-run comparisons, context-isolation verification.
    7. All 8 scorer verdicts committed to comp/results/pilot-wave-1/ by SC.
    8. .031 success bar (PRD §15) all 7 items checked TRUE.
    9. MCP COO on pilot complete: integrity audit committed + all 7 success-bar items checked.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">worktrees/comp-learns/ (DS worktrees — outside ajb_workspace/)</file>
      <file action="create">comp/results/pilot-wave-1/integrity_audit.md</file>
      <file action="create">comp/results/pilot-wave-1/verdicts/ (8 verdict files, SC-authored)</file>
    </files>
  </scope>

  <ds_instructions>
    FOR 1.1.0_DS_CompLearns AND 1.3.0_DS_CompLearns:

    1. Read docs/architecture/COMP_LEARNS_DS_ROLE_ADDENDUM.md — mode-switch to intervention-runner.
       You are NOT building infrastructure. You ARE the frontier model being evaluated.
    2. Read your assigned task packet(s) fully before starting a session.
    3. Unaided condition (condition_a): work from raw source tree only. No comp/ artifacts, no
       scorecards, no compiler.py, no graph outputs.
    4. Aided condition (condition_b): repo + full comp/targets/{target}/ directory.
    5. Stay within budget: wall_clock_max_sec=3600, token_max=200000 per run.
    6. Produce: diff (*.patch against baseline_commit), test_output.txt, reasoning.md.
    7. reasoning.md is for audit only — do NOT expose to scorer. Bundle diff + test_output only.
    8. When bundle ready: MCP COO with bundle path + run metadata (case, condition, wall_clock, tokens).
    9. COO relays to SC. You do NOT contact SC directly.
    10. No cross-DS coordination during active runs — your deliberation log is yours alone.
  </ds_instructions>

  <sc_instructions>
    FOR 2.1.0_SC_CompLearns:

    1. Score ONLY when COO relays a bundle. Never contact DS directly during a run.
    2. Each scoring event = fresh stateless session. No /clear shortcuts.
    3. Scorer inputs: task_packet + candidate_bundle (diff + test_output). NO reasoning.md.
    4. Emit verdict with: score on each measurement axis + comparability class label +
       manifest_hash + items 13-15 checklist result.
    5. Commit verdict to comp/results/pilot-wave-1/verdicts/{scoring_event_id}.json
    6. MCP COO with verdict summary after each scoring event.
    7. After all 8 events: author integrity_audit.md and MCP COO with PILOT COMPLETE.
  </sc_instructions>

  <requirements>
    <requirement id="1">Stage 1 gate: all DS->SC handoffs via COO relay. No direct DS->SC transfer.</requirement>
    <requirement id="2">Fresh scorer session per event — stateless invocation, not /clear.</requirement>
    <requirement id="3">reasoning.md excluded from scorer inputs (PARALLELIZATION_V1 §5).</requirement>
    <requirement id="4">Every verdict includes comparability class label (locally_valid | within-task | cross-DS | cross-model).</requirement>
    <requirement id="5">Unaided runs complete before aided runs (cross-contamination guard).</requirement>
    <requirement id="6">DS mode-switch: read COMP_LEARNS_DS_ROLE_ADDENDUM.md before first run.</requirement>
    <requirement id="7">Integrity audit document required before pilot COMPLETE signal to COO.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="artifacts">8 candidate bundles (diff + test_output) per DS run.</deliverable>
    <deliverable type="verdicts">8 scored verdicts with comparability class, committed to comp/results/pilot-wave-1/verdicts/.</deliverable>
    <deliverable type="document">comp/results/pilot-wave-1/integrity_audit.md — zero leakage certification.</deliverable>
    <deliverable type="signal">MCP COO: PILOT COMPLETE with PRD §15 success-bar checklist.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT hand artifacts directly DS→SC — all handoffs via COO relay (Stage 1 gate).</rule>
    <rule>Do NOT score in an existing session — fresh stateless invocation per event.</rule>
    <rule>Do NOT expose reasoning.md to scorer before verdict.</rule>
    <rule>Do NOT run aided condition before unaided condition (for any DS/case pair).</rule>
    <rule>Do NOT declare pilot COMPLETE without integrity_audit.md committed.</rule>
  </do_not>
</task_order>
