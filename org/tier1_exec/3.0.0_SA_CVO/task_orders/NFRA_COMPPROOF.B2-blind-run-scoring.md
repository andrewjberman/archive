# TASK ORDER -- NFRA_COMPPROOF.B2 (blind-run scoring: the independent judge)

<issued_to>3.0.0_SA_CVO~B</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>done -- B-09..B-20 judged 2026-07-02 (tranche 1 B-02..B-07 prior). Aggregate (as-runs): 7 SOLVED / 8 MISS / 2 VOID(false-pos) / 3 PENDING(B-01/B-08 dropped + B-13 held). Merits-corrected full corpus: 10 SOLVED / 8 MISS of 18 = 55.6%. Deliverables: JUDGE_REPORT_TO-B2_CVO-B_tranche2_B09-B20.md + judge_axes.json. 3 items blocked on ~D fixes (FINDING E context-gate false-VOID -> B-15/B-16; FINDING F B-13 defective seal). RAVC'd COO~B CC CTO.</status>
<!-- TRANCHE-2 VERDICT 2026-07-02 (CVO~B): independent per-incident grounding (12 parallel grounding-assistants + own reads on B-12/B-13/B-17). SOLVED B-10/B-15**/B-16**/B-19; MISS B-09/B-11/B-12*/B-14/B-17(trip)/B-18/B-20(trip); HELD-OUT B-13 (seal defective). Grounding-resilience caught B-17+B-20 confident-wrong trips (axis validated). Findings E(context-gate false-VOID)/F(B-13 mis-sealed, major)/G(run_meta.cheat false-pos persists)/H(binary-reach can't express B-12 1-of-2) + side-finding (live lambda-source-map.json 6 misplaced keys). *=partial-substance; **=merits-SOLVED, VOID as-runs pending gate fix. -->
<compproof_scope_note>This TO's isolation clause bars ~B (the validation subject) from judge/solver/author. CVO~B (the JUDGE lane) is a DISTINCT role from the ws ~B validation subject -- judge independence preserved (author=~D != solver=MSTR-spawned != judge=CVO~B).</compproof_scope_note>
<priority>HIGH -- B is the spine; B2 is the judge half. Isolation-gate enforcement = load-bearing. PRD SS2-B/SS6 + arch doc 1315f9a03.</priority>
<date>2026-07-01</date>

## Context
COMPPROOF-B splits author (catalog, ~D/TO-B1) != solver (fresh-spawned per incident, MSTR) != JUDGE (you). You are the independent judge: score each blind-run vs the SEALED judge-view root-cause, and ENFORCE the isolation gate (VOID-on-violation). If the judge sees what the solver saw or the author judges, B measures nothing. HELD until B1's harness + blind-runs land.

## Objective
Independently score every blind-run on the 3-axis rubric vs the known root-cause; enforce isolation (VOID violations); produce the aggregate coverage verdict.

## Scope
1. **Per-incident scoring** vs the SEALED judge-view (root-cause): REACH (reached root cause?) x USABILITY (usable-in-the-moment, not >150s/fell-to-raw) x GROUNDING-RESILIENCE (did the solver catch a success-shaped-but-WRONG output, or record it as truth?). SOLVED requires all 3; PARTIAL/MISS otherwise.
2. **Isolation-gate enforcement (VOID-on-violation):** for each incident, confirm the solver payload contained NO answer field (the diff-gate held) + author!=solver!=judge. Any violation -> VOID that incident (it measures nothing), don't score it as data.
3. **Aggregate + honesty:** aggregate SOLVED/PARTIAL/MISS %; confirm 100% MISS/PARTIAL -> filed gap-charter; the GROUNDING-RESILIENCE axis specifically catches the Goodhart "technically-covered" false-SOLVED.

<compiler_tools_mandate>
  <phase id="1" when="verify">
    <step><run>independently exercise each blind-run vs the sealed root-cause (not the solver's self-assessment); confirm the isolation diff-gate held per incident; score the 3 axes</run>
    <expect>Every incident scored vs the known root-cause by YOU (not the solver/author); isolation confirmed or VOIDed; aggregate %.</expect>
    <if_mismatch>An isolation violation VOIDs the incident (re-run needed); a solver-self-graded score is not accepted -- you re-judge.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 0.8.0_AE_CloudComp~D (TO-B1): builds the harness + runs the blind-solvers; hands you the outputs. The isolation gate is what makes your scoring meaningful.
- 1.0.0_SA_CTO: arch-lead (1315f9a03); CC on the aggregate.
- 2.0.0_SA_COO~B: on your aggregate + charters, I route the gap-charters into the D gap-feed + the program ledger.
- ~B: OFF-LIMITS (validation subject) -- not a judge/solver/author.
</cross_domain_coordination>

<acceptance_criteria>
1. Every blind-run independently scored (judge != author != solver) on REACH x USABILITY x GROUNDING-RESILIENCE vs the sealed root-cause.
2. Isolation-gate enforced: violations VOIDed, not scored. Aggregate SOLVED/PARTIAL/MISS %.
3. 100% MISS/PARTIAL -> filed gap-charter; GROUNDING-RESILIENCE catches success-shaped-wrong false-SOLVEDs. RAVC COO~B + CC CTO.
</acceptance_criteria>

## Note
You are the honesty of B. A solver grading itself, or an author who judges, voids the whole benchmark. Independent judging + VOID-on-violation is the discipline. HELD until B1 delivers.
