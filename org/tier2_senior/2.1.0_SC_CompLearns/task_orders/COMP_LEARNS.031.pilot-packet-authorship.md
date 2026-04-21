<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-comp-learns-031-pilot-packets</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <reviewer>1.1.0_SA_CTO</reviewer>
    <date>2026-04-21</date>
    <status>active</status>
    <project_code>COMP_LEARNS</project_code>
  </metadata>

  <objective>
    Author concrete task packets for pilot Cases 1 and 2 per PARALLELIZATION_V1.md §10-11.
    Commit under `comp/tasks/task-001/packet.yaml` and `comp/tasks/task-002/packet.yaml`.
    CTO reviews and signs off before .032 (pilot wave execution) is dispatched.
    Gate: .030 GREEN/COMPLETE (eba6cb26). Schema scaffold in comp/tasks/task-000-example/.
  </objective>

  <context>
    .030 delivered the task packet schema, scoring context manifest schema, DS mode-switch
    doctrine (COMP_LEARNS_DS_ROLE_ADDENDUM.md), and SC checklist items 13-15. CTO signed off.
    .031 is the packet authorship step: making the two pilot task definitions concrete and
    committing them so DS agents can be dispatched in .032.

    Case 1 — OSS historical bug, structural localization (httpx):
    The task-000-example scaffold already targets httpx PR #1298 (NetRC host:authority mismatch).
    That is a strong candidate but you must verify the baseline commit still builds and the
    test suite is runnable before locking it. Alternative: another httpx or requests merged
    bug-fix PR where: (a) diff is small but investigation is non-trivial, (b) the harness
    graph/selector surface has known relevance, (c) acceptance criteria are test-suite-verifiable.
    Select the strongest candidate. Document the selection reasoning in the packet's
    backlog_provenance.notes field.

    Case 2 — click synthetic-serious refactor:
    Define the click subsystem to target (e.g. nested command-group dispatch or decorator
    option registration — both were flagged in the selector-ceiling watch-item from .009 memo).
    Specify the invariant set explicitly: the set of command/option shapes that must continue
    to resolve correctly after the refactor. Acceptance criteria must include: (a) all existing
    click tests pass, (b) a named subset of specific command dispatch behaviors passes a
    targeted test fixture you define. The invariant set is the hard specification — its concreteness
    is what makes the task a trustworthy measurement rather than a vague exercise.

    Both packets become the comparability anchor for the pilot. Any ambiguity in the packet
    is a downstream scoring validity problem. Err on the side of over-specifying fields.

    Baseline discipline: baseline_commit must be a real, verifiable git SHA that still builds
    and has a runnable test suite. For OSS targets you don't control, pin an older stable
    release tag SHA. Do NOT leave baseline_commit as a placeholder — the packet is invalid
    without a pinned commit.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before authoring):
    <run>cat comp/tasks/task-000-example/packet.yaml</run>
    <expect>Scaffold with all required fields. Your packets must conform to the same structure.</expect>
    <run>cat comp/tasks/scoring-context-manifest-schema.yaml</run>
    <expect>10-field manifest schema. Confirm your scorer_regime fields align.</expect>

    Phase 2 (during authoring):
    For Case 1: verify the httpx baseline_commit is real and test suite is runnable.
    For Case 2: verify click target repo + baseline_commit. Stub the invariant-check test
    fixture at comp/tasks/task-002/fixtures/invariant_check.py (can be a stub, not runnable
    without click, but schema-valid and reviewed by CTO).

    Phase 3 (after authoring):
    <run>python -c "import yaml; yaml.safe_load(open('comp/tasks/task-001/packet.yaml'))" </run>
    <expect>No parse error. YAML is valid.</expect>
    <run>python -c "import yaml; yaml.safe_load(open('comp/tasks/task-002/packet.yaml'))"</run>
    <expect>No parse error. YAML is valid.</expect>

    After committing: MCP 1.1.0_SA_CTO for review + sign-off. Do NOT dispatch .032 until
    CTO sign-off lands.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    reviewer: "1.1.0_SA_CTO reviews both packets before .032 dispatch. SC MCPs CTO
    immediately on commit with packet content summary."
    gated_by: ".030 GREEN (eba6cb26) — schema scaffold present."
    gates: ".032 (pilot wave execution — 1.1.0_DS + 1.3.0_DS intervention runners +
    2.1.0_SC scoring). .032 not dispatched until CTO sign-off on both packets."
    worktree: "feature_clb/ is the control-plane worktree for CTO/COO/SC coordination.
    Commit from feature_clb/ (CLOUD branch). Packet files go to comp/tasks/."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/tasks/task-001/packet.yaml committed: all REQUIRED fields populated,
       baseline_commit is a real pinned SHA, acceptance_criteria are test-suite-verifiable.
    2. comp/tasks/task-002/packet.yaml committed: invariant set explicitly specified,
       acceptance criteria include both full test suite + invariant fixture.
    3. comp/tasks/task-002/fixtures/invariant_check.py stubbed (or full if feasible).
    4. Both YAML files parse without error (python yaml.safe_load exit 0).
    5. Backlog provenance documented in both packets (selection reasoning for Case 1,
       watch-item reference for Case 2).
    6. Committed under --author="2.1.0_SC_CompLearns" to feature_clb/ CLOUD branch.
    7. MCP to 1.1.0_SA_CTO with packet content summary immediately on commit.
    8. MCP to 2.0.0_SA_COO on CTO sign-off received (or on CTO blocking concern).
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">comp/tasks/task-001/packet.yaml</file>
      <file action="create">comp/tasks/task-002/packet.yaml</file>
      <file action="create">comp/tasks/task-002/fixtures/invariant_check.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">baseline_commit must be a real, pinned, verifiable SHA — NOT a placeholder.</requirement>
    <requirement id="2">Case 1 selection: document why this bug was chosen over alternatives.</requirement>
    <requirement id="3">Case 2 invariant set: explicitly enumerated — not "the existing tests" but a named list of behavioral invariants the refactor must preserve.</requirement>
    <requirement id="4">CTO review required before .032 dispatch — MCP CTO immediately on commit.</requirement>
    <requirement id="5">YAML parse-clean: both packets validate via yaml.safe_load before commit.</requirement>
    <requirement id="6">Commit from feature_clb/ worktree (COMP_LEARNS control-plane), not ajb_workspace/.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">task-001/packet.yaml + task-002/packet.yaml + fixture stub committed to CLOUD.</deliverable>
    <deliverable type="signal">MCP 1.1.0_SA_CTO for review. MCP 2.0.0_SA_COO with CTO sign-off or blocking concern.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT leave baseline_commit as a placeholder. Pin a real SHA.</rule>
    <rule>Do NOT dispatch .032 before CTO sign-off on both packets.</rule>
    <rule>Do NOT author packets in ajb_workspace/ — commit from feature_clb/.</rule>
    <rule>Do NOT accept "all existing tests pass" as the full Case 2 invariant set — enumerate the specific behavioral invariants.</rule>
  </do_not>
</task_order>
