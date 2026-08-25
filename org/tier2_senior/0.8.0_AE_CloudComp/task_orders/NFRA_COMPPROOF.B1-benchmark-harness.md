# TASK ORDER -- NFRA_COMPPROOF.B1 (the B harness: incident-regression graph-solvability benchmark -- THE SPINE)

<issued_to>0.8.0_AE_CloudComp~D</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_COMPPROOF is complete; this TO was last touched 2026-07-01, predating the project close 2026-07-07. Closed as a record act, not a work verdict. Prior status: dispatched</status>
<!-- PROGRESS 2026-07-01 (0.8.0_AE_CloudComp~D): HARNESS BUILT + self-tested + committed 51196d3a9 (org/modules/graph/compproof/ under lane grant 38142e83b). Structural ACs MET: AC#1 STRIP DIFF-GATE 20/20; AC#2 isolation VOID-on-violation (structural); AC#4 3-axis scorer + gap-charter + aggregate + standing self-test; ADVI_BREAKS #1 worked example -> PARTIAL+charter. AC#3 (the 20-incident blind RUN) HANDED OFF to the execution phase -- MSTR spawns fresh solvers (spawn_payload only), CVO~B (B2) judges; I'm the AUTHOR (isolation-barred from solve/judge). TO stays open pending the blind-run. RAVC->COO~B, CC CTO+CVO~B. -->

<priority>HIGH -- B is the SPINE (seeds C's intent-set + D's gap-feed). CTO arch-leads; you build. PRD NFRA_COMPPROOF_PRD.md (3d78e1f5b) SS2-B + SS6.</priority>
<date>2026-07-01</date>

## Context
NFRA_COMPPROOF proves the COMP* program actually SOLVES real problems (the PHASE-2 meta-test). B is the spine: for each real nasty incident, run the counterfactual -- starting ONLY from the symptom as first seen, can an agent reach the true root cause TODAY via graph traversal + comp-tools? CTO architects the harness (arch-lead); you build it. ~B is OFF-LIMITS (it's the validation subject) -- you are the AE builder. Anti-drift self-consistency: ONE home `org/modules/graph/compproof/` + one program ledger, disjoint verbs, no scatter.
**BUILD TO THE CTO ARCH DESIGN:** `docs/architecture/NFRA_COMPPROOF_B_HARNESS_DESIGN.md` (1315f9a03) -- the 4-component pipeline + isolation protocol + the 3-axis scorer + the ADVI_BREAKS worked example are pre-designed. This TO decomposes against it; the arch doc wins on any detail divergence.

## Objective
Build the standing, re-runnable B benchmark harness: corpus-loader + blind-solver spawn protocol + REACH x USABILITY scorer + the gap-charter emitter.

## Scope
1. **Corpus loader + root-cause STRIP (per the arch doc):** bind the CAPPED top-20 incident corpus (`docs/briefs/nfra-compproof-B-incident-corpus-top20-20260701.md`, 5402f130b), 2026-only real-record, 10 failure-classes. Per-incident 5-field schema: `symptom_as_first_seen | true_root_cause | how_it_was_actually_found | graph_traversal_test | verdict | gap`. The loader emits a SOLVER-VIEW (symptom + estate + tools ONLY) + a SEALED JUDGE-VIEW (root-cause), with a **DIFF-GATE that asserts root_cause NOT-IN solver_view for ALL 20** (the structural strip proof). START with ADVI_BREAKS (#1).
2. **BLIND-SOLVER SPAWN PROTOCOL (HARD GATE -- author != solver != judge, VOID-on-violation):** the blind-solver = a FRESH-spawned agent PER incident (MSTR spawns solvers per the split), given ONLY the solver-view, NEVER the answer; an independent judge (CVO, TO-B2) scores vs the sealed judge-view. VOID-on-violation: if author=solver or the solver payload contains any answer field, that incident's result is VOID. Structurally enforced (the diff-gate + the spawn payload), not by convention.
3. **3-AXIS scorer = REACH x USABILITY x GROUNDING-RESILIENCE (per the arch doc + MSTR):** REACH = graph reaches root cause; USABILITY = usable-in-the-moment (a >150s-under-load timeout / fell-back-to-raw = FUNCTIONAL PARTIAL, not SOLVED); GROUNDING-RESILIENCE = does the solver CATCH a success-shaped-but-WRONG output (a 0-count / empty / rc=0-but-incomplete confidently-wrong result -- anchored on tonight's grep-BRE-error + the rc=0-but-54%-missing STEP3) or record it as truth? SOLVED requires all 3; the 3rd is the Goodhart/false-confidence probe. Emit per-incident 3-axis + aggregate %.
4. **Standing re-runnable suite + gap-charter emitter:** the whole thing re-runs as a repeatable gate ("can the graph still solve the classics"); every MISS/PARTIAL auto-emits a gap-charter (feeds D). SEED baseline = ~B's 4e9f0258d (its E1/E2 = the first documented MISS/PARTIAL).

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>read the top-20 corpus brief (5402f130b) + the ADVI_BREAKS record; comp-which "how do I spawn an isolated blind-solver agent" (or the Agent-tool isolation pattern); confirm org/modules/graph/compproof/ is the one home</run>
    <expect>The corpus + schema understood; the blind-solver isolation mechanism identified; one-home confirmed.</expect>
    <if_mismatch>Coordinate with CTO (arch-lead) on the isolation mechanism before building -- it's the load-bearing methodology.</if_mismatch></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>harness self-test on ADVI_BREAKS (#1): load -> strip -> blind-solver-input-excludes-answer (assert the solver payload has NO root_cause/how-found fields) -> scorer emits SOLVED/PARTIAL/MISS -> gap-charter on miss; ds-commit-gate + non-ASCII + from __future__ import annotations</run>
    <expect>ADVI_BREAKS runs end-to-end; the solver payload PROVABLY excludes the answer (isolation gate structurally holds); scorer + charter work.</expect>
    <if_mismatch>STOP. If the solver payload can see the answer, the isolation gate is broken -- B measures nothing. Fix before any blind-run.</if_mismatch></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>run the harness across the top-20 (blind-solver per incident) -> per-incident verdict + aggregate coverage %; hand the blind-run outputs to CVO (TO-B2) for independent scoring</run>
    <expect>>=20 incidents on the 5-field schema, each blind-tested; aggregate SOLVED/PARTIAL/MISS %; 100% MISS/PARTIAL -> filed gap-charter. CVO scores independently.</expect>
    <if_mismatch>A skipped incident or an un-charted MISS = incomplete. The isolation gate holds on EVERY incident or the result is void.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 1.0.0_SA_CTO: ARCH-LEAD (the harness architecture + the blind-solver isolation mechanism). Build to his arch; RAVC him.
- 3.0.0_SA_CVO~B: TO-B2 = the independent blind-run JUDGE (scores vs known root-cause). Your harness feeds her; the isolation gate is what makes her scoring meaningful.
- ~B (0.8.0_AE_CloudComp~B): OFF-LIMITS (validation subject) -- do NOT involve ~B in authoring/solving/judging. ~B's 4e9f0258d is the seed baseline (a DATA input, not a participant).
- COMPLEARN/D: every gap-charter feeds the D gap-feed.
</cross_domain_coordination>

<acceptance_criteria>
1. Corpus loader binds the top-20 (5-field schema) + STRIPS root-cause; the blind-solver payload PROVABLY excludes the answer (isolation structurally enforced -- the HARD gate).
2. Blind-solver spawn (fresh agent/incident, symptom-only) + REACH x USABILITY scorer + gap-charter emitter; standing re-runnable suite in org/modules/graph/compproof/.
3. >=20 incidents blind-tested; aggregate coverage %; 100% MISS/PARTIAL -> filed gap-charter. CVO (B2) scores independently.
4. Session log Compiler Tools reproduces every run. RAVC COO~B + CC CTO + CVO~B. One home, one ledger (anti-drift self-consistency).
</acceptance_criteria>

## Note
B is the SPINE + the whole program's honesty rests on the blind-solver isolation gate (author != solver != judge). If that's weak, B voids. Build it structurally-enforced, not by convention. Start with ADVI_BREAKS.
