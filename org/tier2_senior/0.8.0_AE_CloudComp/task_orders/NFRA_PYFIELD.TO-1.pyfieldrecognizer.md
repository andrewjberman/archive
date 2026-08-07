<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-07-pyfield-recognizer</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.8.0_AE_CloudComp</issued_to>
    <date>2026-08-07</date>
    <status>complete</status>
    <project_code>NFRA_PYFIELD</project_code>
  </metadata>

  <objective>
    Build `PyFieldRecognizer` — the ONE new component in NFRA_PYFIELD — emitting D1-conformant
    field-grain `FLOWS_TO` edges for Python gold/silver scripts, with an honest coverage declaration
    for everything it cannot resolve. Field grain exists in the dependency graph on the PORTAL
    substrate ONLY; on the substrates where every gold script lives it does not exist at all. This
    populates it so `comp-pipescript` can emit a per-script field IO list and `comp-dataflow` can walk
    it BACKWARD — Andrew's migration question, *"if I change this field, what breaks downstream."*
  </objective>

  <context>
    PRD: `docs/architecture/NFRA_PYFIELD_PRD.md` @004588f9cb (v1.0, AUTHORIZED). Architecture is
    RULED — §3 (flow-local inference, option (b), with (c) as mandatory coverage policy), §4
    (component spec), §9 (three mechanisms). These are NOT open questions; do not relitigate them.

    AUTHORIZATION: Andrew-direct 2026-08-07 — *"Yeah i want the python data tracing"*, consumer
    *"it will be comp-pipescript"*, use case *"when we do migrations it will be essential to be able
    to track field dependencies in pipelines."* He separately named THIS SEAT to spearhead the work.

    >> TO-0 IS DONE. THE DENOMINATOR EXISTS AND YOUR BAR IS WRITTEN AGAINST IT. <<
    `4.0.0_SA_CRO`, @7a5be4b4c7, deliverable
    `org/tier1_exec/4.0.0_SA_CRO/deliverables/NFRA_PYFIELD_COLUMN_DENOMINATOR_20260807.md`,
    independently re-derived at the COO seat (3/3 exact):

      2,744 of 4,406 name-based string-literal subscripts are COLUMNS — 62.3% [95% CI 56.8–68.3]
      vintage 2026-08-07T152209Z · pandas 2.3.3 · grain = AST Subscript NODES
      SWEPT: data/inf/scripts/gold + data/assets/scripts/gold (124 files, 0 parse errors)
      UNSWEPT: bd, cot, mdpf, the assets monolith, and EVERY silver tree
      classification: column 1,905 / not-column 607 / undecidable-at-this-site 1,894

    **YOUR BAR IS AGAINST ~2,744, NOT 4,896.** About 38% of the subscript population was NEVER a
    column and is CORRECTLY unresolved. **A recognizer that never touches it is not failing.**
  </context>

  <compiler_tools_mandate>
    Phase 1 — BEFORE writing any code (this is the BUILD LADDER, run it in order):
      <run>comp-which "python field extraction recognizer"</run>
      <expect>Routes to a rich tool, or RUNS comp-find. As of @a3a9df7911 the router emits
      `comp-find`; if you see `comp-grep`/`comp-glob` anywhere in its output, the repoint regressed —
      report it, do not work around it.</expect>

      <run>comp-find "class .*Recognizer" org/modules/graph</run>
      <expect>The existing recognizers — `comp_recognizers_code.py`, `_config.py`, `_tsx.py`.</expect>
      <if_mismatch>BUILD LADDER rung 2: REUSE THE EXISTING PATTERN, DO NOT INVENT ONE. If you cannot
      find the pattern, that is a search failure, not an absence — say so before writing a new shape.</if_mismatch>
      ⚠ **`comp-find` COUNTS LINES, NOT AST NODES.** Its 4,336 against TO-0's 4,897 is a GRAIN
      difference, not a disagreement. Never use a comp-find count as a denominator in this TO.

      <run>comp-estate --definitions</run>
      <expect>The RATIFIED term registry. Adopt ratified terms; do not re-coin beside them.</expect>

    Phase 2 — before committing:
      <run>comp-blast [the recognizer registry]</run>
      <expect>Registry consumers only. This TO adds a recognizer; it modifies no gold script, no
      Lambda, no portal component, no IAM.</expect>

    Phase 3 — after committing:
      <run>comp-kuzu census of the emitted edges</run>
      <expect>DENOMINATOR AND VINTAGE PRINTED BESIDE EVERY COUNT. See acceptance criterion 1.</expect>
      <if_mismatch>A count without its denominator is the defect this whole project exists to
      prevent. Do not report one.</if_mismatch>

    Results in the session log Compiler Tools table. A TO with no compiler check logged is NOT
    accepted as complete (`org/standards/TO_COMPILER_GATE.md`).
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: `org/modules/graph/**` (exec-locked) + the comp-tool registry
    - also_in_to: no other ACTIVE TO on these files known at issue time; CTO~D reported none
    - required_action: run `comp-blast` at Phase 1 per the parallel-wave protocol and MCP the owner
      of anything that appears in 2+ blast radii BEFORE committing.
    ⚠ `comp-pipescript` and `comp-dataflow` are the CONSUMERS (tool-fit RULED: pipescript EXTRACTS,
    dataflow TRAVERSES). This TO does not modify either; it populates what they read.
  </cross_domain_coordination>

  <acceptance_criteria>

    >> 1. THE TWO PINS. THIS IS THE CRITERION THAT MAKES THE OTHERS MEAN ANYTHING. <<
       **A COVERAGE FIGURE IS UNSTATEABLE WITHOUT PINNING BOTH THE RESOLVER AND THE MARKER SET,
       because BOTH ARE INSTRUMENT PROPERTIES — measured, not theorised:**
         · the column FLOOR moves **5.5×** with the MARKER SET (MINIMAL 228 / MID 735 / WIDE 1,247)
         · binding REACH moves **3.6×** with the RESOLVER, on ONE IDENTICAL POPULATION
           (9.9% constructor-only / 27.6% the PRD spike / 35.3% with annotations + return summaries)
       So every coverage number this TO publishes MUST carry, inline: **resolver identity + version,
       marker-set identity + the pandas version it was derived from, the denominator, and a vintage.**
       ⛔ FORBIDDEN: *"the recognizer resolves N% of columns."* That sentence is not true or false —
       it is UNDERSPECIFIED, and it is underspecified in a way that lets any number be defended.

    2. `props` CARRIES THE SAME SEVEN KEYS AS PORTAL `FLOWS_TO` — `srcField`, `dstField`, `kind`,
       `rename`, `condition`, `via`, `resolution`. Machine-checkable. **The two substrates are ONE
       SCHEMA** (PRD §4); this is what lets the semantic-evolution loop see python field grain at all.

    3. `Coverage.unresolved` IS NON-EMPTY AND ENUMERATES `<expr>` BASES.
       ⛔ **ZERO UNRESOLVED IS A FAILURE, NOT A PASS.** 491 expr-base sites (`f()["x"]`,
       `d["a"]["b"]`) are UNREACHABLE BY CONSTRUCTION — a name-keyed mechanism structurally cannot
       attempt them. A run reporting full coverage has lost the honest-degrade channel (LAW-1), which
       is worse than low coverage because it is low coverage that lies.
       ⛔ **AND THE 491 MUST NEVER BE SCORED AGAINST THE RECOGNIZER AS MISSES.** A bar that counts
       them is unpassable by construction.

    4. `.iterrows()` IS HANDLED, AND IT IS NOT AN EDGE CASE — **257 sites, measured.**
       `row['col']` on an `.iterrows()` row **IS a column access.** A recognizer that treats loop
       variables as records mis-calls every one of the 257. State explicitly how you handle it.

    5. THE EXCLUSION SET IS **DERIVED FROM THE INSTALLED PANDAS API AT RUNTIME, AND VERSION-PINNED.**
       ⛔ DO NOT LIFT `_DF_METHODS`: hand-drawn, incident-driven, 71 names against a real universe of
       240 — **missing 170 (70.8%)** — carrying one entry that can never fire, not version-pinned.
       If any instruction anywhere says "reuse `_DF_METHODS`", it is wrong.

    6. ALL THREE AXES FROM THE START, not binding-first. Binding-side 27.6%, usage-side 23.1%, only
       34.6% overlap (union 41.1%) — **largely independent**, so a binding-only build leaves a cheap
       signal on the table. Exclusion-side already runs in `comp-pipescript`.

    7. A MUTANT CONTROL, EXERCISED AND RECORDED. CRO's probe self-tests 19/19 including one that
       empties the constructor set and proves **the binding axis goes DARK, not green.** Yours must
       have an equivalent: a mutation that SHOULD break the emitter and demonstrably does.
       *A test suite that has never failed has never been tested.*

    8. Session log with a Compiler Tools section and an archetype tag.

  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/modules/graph/[the new PyFieldRecognizer module]</file>
      <file action="reference">org/modules/graph/comp_recognizer_sdk.py</file>
      <file action="reference">org/modules/graph/comp_recognizers_code.py</file>
      <file action="reference">org/tier1_exec/4.0.0_SA_CRO/deliverables/pyfield_to0/pyfield_column_probe.py</file>
      <file action="reference">docs/architecture/NFRA_PYFIELD_PRD.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Implement `PyFieldRecognizer` per PRD §4. The engine, the front-ends and
    `emit_cse` are used AS-IS — this is the only new component.</requirement>
    <requirement id="2">LIFT THE RESOLVER MECHANISM FROM CRO'S PROBE RATHER THAN REINVENTING IT
    (BUILD LADDER rung 2). The two additions that produced the 3.6× lift are DataFrame-typed
    parameter ANNOTATIONS and one-hop local RETURN summaries — ~60 lines, already implemented and
    self-tested under `--resolver v2`, with v1 kept selectable so the delta is RE-DERIVABLE rather
    than a claim about a resolver nobody can run. Neither is type inference (mypy/pyright/pytype/jedi
    are ALL ABSENT — rung 5 was run; do not add a dependency).</requirement>
    <requirement id="3">Publish coverage with both pins, the denominator, and a vintage (criterion 1).</requirement>
    <requirement id="4">Declare which trees you swept and which you did NOT, in the same sentence as
    any figure. TO-0's figure is inf+assets gold ONLY.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">The recognizer module + its test battery incl. the mutant control.</deliverable>
    <deliverable type="document">A coverage report satisfying criterion 1.</deliverable>
    <deliverable type="document">Session log with Compiler Tools section.</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT state any coverage figure without BOTH pins, its denominator and its vintage.</rule>
    <rule>DO NOT score the 491 expr-base sites as recognizer misses.</rule>
    <rule>DO NOT lift `_DF_METHODS`. Derive from the installed pandas API and pin the version.</rule>
    <rule>DO NOT add a type-inference dependency. Rung 5 was run; all four are absent by measurement.</rule>
    <rule>DO NOT modify any gold or silver script. They are the SUBJECT of this TO, never its target.</rule>
    <rule>DO NOT treat a comp-find count as a denominator — it counts LINES, not AST nodes.</rule>
    <rule>DO NOT tune the recognizer against the hand-audited sample TO-0 produced. That would be
    overfitting a scorer to its own eval cases (Andrew-direct 2026-08-06) and would make the
    published interval a fiction. The audit measures the PROCEDURE; it is not training data.</rule>
    <rule>DO NOT call any external vendor API. DO NOT build any alert, alarm, SNS topic, SES send,
    freshness checker or monitor.</rule>
  </do_not>
</task_order>
