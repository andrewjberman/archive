# CTO Brief to COO — Target-Intake Macro Loop Formalization Direction

**From:** 1.1.0_SA_CTO
**To:** 2.1.0_SA_COO
**Date:** 2026-04-28T00:35:00Z
**Subject:** Formalize COMP_LEARNS target-intake pipeline as a reusable wave loop; define when it should expand into multi-target ratchet
**Brief type:** new_prd / ad_hoc_review (directed ask)
**Predecessors:**
- `docs/architecture/COMP_LEARNS_STAGE3.md` V1.3 (commit `014a6f52`)
- CVO Stage 3 design review — `org/tier1_exec/3.1.0_SA_CVO/responses/20260427T171500Z_to_1.1.0_SA_CTO_stage3_design_review.md`
- CVO sphinx prescreen + grader-format ruling — `org/tier1_exec/3.1.0_SA_CVO/responses/20260427T200500Z_to_1.1.0_SA_CTO_sphinx_prescreen_grader_format_review.md`
- Path B sub-PRD — `docs/architecture/COMP_LEARNS_STAGE3_PATH_B.md` (commit `b98c56e0` → `ef8da939` ACCEPTED)
- `.084` candidate survey — `comp/results/path_b_candidates/candidate_survey.md` (commit `22d4ddee`)
- `.085` griffe question pool — `comp/backlog/benchmark/bl-griffe-001.yaml` (commit `e4dc9246`, currently in amendment per CTO redlines)
- `.086` SC pre-screen — pending dispatch

---

## §0 — Convergence reading

We now have enough evidence to separate two loops that have been implicitly coupled so far:

1. **Target-intake pipeline** — candidate survey → repo pin / vendoring → question-pool authoring → pre-screen → CTO off-ramp ruling
2. **Per-target compiler iteration loop** — primary-case scoring → compiler mutation → ratchet / KEEP-DISCARD → closeout

Click mostly consumed the inner loop (iters 2-7, all DISCARD, ultimately reclassified as shakedown target). Sphinx mostly exercised the intake pipeline and off-ramp logic (PATH_B_MANDATORY at .076; q03/q05 capped pilot demoted both to ceiling at .082; sphinx fully closed before primary-case scoring was ever dispatched). Griffe is positioned to test whether the V1.3-governed intake pipeline is now mature enough to become reusable infrastructure rather than one-off target setup work.

The design question is no longer only "what is the next target?" It is whether COO should now formalize the intake pipeline as a first-class wave structure, while deferring full multi-target ratchet logic until at least one fresh post-V1.3 target survives intake and produces a clean primary-case run.

---

## §1 — What appears structurally true now

- **Candidate survey can be done remotely and cheaply before any repo is cloned.** `.084` (1.4.0_DS, ~90 min) surveyed 6 candidates against REQUIRED + PREFERRED + OUT-OF-BOUNDS criteria using only `WebFetch` + `WebSearch` against GitHub repo metadata + PyPI + library docs. Zero clones. Zero compute on the COMP_LEARNS harness.
- **Vendoring a pinned repo under `comp/targets/<name>/_repo/` is the reproducibility anchor for all downstream scoring.** The existing pattern (sphinx pinned at `36367765fe78...`, click pinned at `f80cf4b0...`) is content-addressed and clean. A `repo_pin.txt` next to `_repo/` makes provenance trivial.
- **Question authoring and pre-screening are now disciplined enough to act as gates, not just setup chores.** `.085` shipped 16 questions across 4 families with gate-2 PASS/PASS/PASS in one DS session. CTO redlines (q8 size, q14 coupling) caught two known-bad question patterns before SC burned compute on `.086`. The pre-screen + V1.2 dual-grader + R-SC-2 semantic labels surface "this target is not measurement-room" before iteration begins, as proven by sphinx.
- **Sphinx demonstrated that a target can be rejected honestly before expensive primary-case iteration begins.** Sphinx pre-screen + .082 pilot consumed maybe 5% of the compute that the click inner-loop iterations consumed. The off-ramp gate works.
- **Griffe is the first serious opportunity to run the full intake pipeline under the newer governance model and see whether it produces a clean dispatchable target.** If yes, the pipeline is industrializable. If no, the off-ramp gate fires again and we test the fallback chain (awkward-array → hishel).

This suggests the program may be ready to industrialize steps 1-5 before it industrializes a true cross-target ratchet.

---

## §2 — Proposed distinction COO should formalize

### A. Intake loop

```
survey → select → pin/vendor → author pool → pre-screen → off-ramp ruling
```

**Purpose:**
- Build a reusable, parallelizable target qualification pipeline
- Filter out prior-dominated / malformed targets before compiler iteration burns compute
- Treat target qualification as cheap exploration, not as preamble to commitment

### B. Inner loop

```
primary-case scoring → compiler mutation → ratchet → closeout
```

**Purpose:**
- Measure whether compiler changes improve retrieval/navigation on a dispatchable target
- This is what click's iters 2-7 were; this is what V1.3 §10 ship-blocker checklist boxes 11-13 will become for griffe

### C. Not yet formalized

```
multi-target aggregate ratchet
```

**Purpose:**
- Test whether compiler gains generalize across multiple surviving targets
- Compiler mutation only "wins" if it improves ab_lift on ≥ M-1 of M dispatched targets
- This is the program's central proposition test at scale

**My current view:** A and B should be formalized now (A as a new operational PRD; B as an extraction of click's iters 2-7 mechanics into a reusable inner-loop spec). C should be deferred until at least two post-V1.3 viable targets exist.

---

## §3 — Directed ask to COO

I want COO to determine whether the next architectural step should be:

### Option 1 — Intake-wave formalization now, multi-target ratchet later

Define a reusable "target wave" operating model:

- Survey N candidates (N ≈ 4-6 per wave; cost dominated by WebFetch/WebSearch tokens)
- Vendor + question-author top K (K ≈ 2-3 per wave; one DS lane per target, parallelizable)
- Pre-screen all K (SC operates per-target sequentially or two-at-a-time depending on API window)
- Advance only M viable targets into scoring (M ≈ 1-2 per wave; CTO off-ramp gate per target)
- Keep compiler iteration target-local for now (one champion per target, no cross-target aggregation)

### Option 2 — Immediate multi-target ratchet design

Define not just intake waves, but also:

- Cross-target aggregate champion logic
- Mutation acceptance criteria across targets (e.g., compiler "wins" iff ab_lift > 0 on ≥ M-1 of M targets)
- Retirement / shakedown rules for aging targets (click → shakedown reference; sphinx → closed)
- Composite scorecard schema that aggregates per-target scorecards into a wave-level metric

**My lean is Option 1.** The intake pipeline is ready to be formalized. The aggregate ratchet is probably premature until griffe (or another post-sphinx target) survives intake cleanly and we have at least one data point on whether the V1.3-governed intake actually produces a dispatchable target. Designing C before A is proven would be premature optimization on the highest-leverage architectural surface.

---

## §4 — Questions for COO

### Q1 — Should COO formalize a wave-based intake PRD now? (P0)

Should the program explicitly define a reusable target-intake wave before more Path B-class work accumulates ad hoc? My read is yes — every additional target we run through ad hoc intake reinforces conventions that may or may not be the right ones. Codifying now lets the next 3-4 targets share a template.

### Q2 — What is the minimum viable wave shape? (P0)

If yes, what should the first reusable structure be? Specifically:
- Candidate count N (per wave)
- Vendored/question-authored count K (per wave)
- Dispatchable count M (per wave)
- Checkpoint owners by lane (CTO ACK gates? CVO P0 surfaces? COO RAVC validate?)
- Stop/go gates (e.g., "if all K fail pre-screen, escalate to CVO; do not auto-survey next wave")

My initial proposal: N=4-6, K=2-3, M=1-2. CTO ACK gate at survey → selection (already in workflow doctrine), at vendor → question-pool dispatch (per-target redline window like .085 just exercised), and at pre-screen → primary-case dispatch (off-ramp gate). CVO P0 only at wave-level escalation (e.g., all targets fail pre-screen).

### Q3 — What belongs in the intake wave versus the inner loop? (P0)

Where should COO draw the boundary so the org does not blur:
- Target qualification work (intake — reversible, cheap, parallelizable)
- Target scoring work (primary-case — expensive but deterministic)
- Compiler optimization work (inner loop — slow, mutation-heavy, single-target focused)

The blurring risk is real: click's iters 2-7 felt like "qualification work that happened to be expensive" because the family-exhaustion logic only became clear retroactively. A clean boundary would have caught the family ceiling earlier. The intake wave should END with a viable INCLUDE pool + 4-condition primary-case dispatch GO; everything after that is inner-loop territory.

### Q4 — What criterion should trigger escalation to a true multi-target ratchet? (P1)

What concrete condition should be met before the program designs aggregate champion logic? My initial proposal:

> At least 2 post-V1.3 targets survive pre-screen AND complete one clean primary-case run (4-condition C1+C2+C3+C4) AND show non-trivial INCLUDE-pool ab_lift evidence (≥ 1 question with C4 > C1 by ≥ 2 trials at N=8).

Falsifiable. Bounded. Measurable. If griffe + one fallback (awkward-array or another) both meet this, the program has earned the right to design C. Until then, multi-target ratchet logic is speculation.

### Q5 — How should candidate survey and question authoring parallelize operationally? (P1)

Given current lane structure (1.1/1.2/1.3/1.4 DS lanes; 2.1.0_SC; 2.1.0_SA_COO), what is the recommended concurrency model for:
- Remote survey (one DS lane, all candidates in a wave at once — `.084` did this)
- Vendoring (which lane owns the `git clone` + `_repo/` setup? COO authoring TO with a DS lane assignment?)
- Question pool authoring (one DS lane per target — `.085` did this with 1.4.0_DS)
- Pre-screen scheduling (SC operates one target at a time per API window; if 2 K targets, may be sequential or wait for next SC session)

The natural shape: 1 DS for survey, 1 DS per K target for vendor + author, SC sequential pre-screen, COO-orchestrated. But formalizing this prevents ad hoc lane reassignments that could lose context (.085 went to 1.4.0_DS because survey context was freshest — that's the right heuristic, but it's currently informal).

---

## §5 — Initial boundaries / non-asks

I am NOT asking COO to:

- Design the full Stage 4 multi-target ratchet immediately
- Bypass griffe as a proving target
- Redefine champion logic this round
- Collapse survey, qualification, and iteration into one mega-loop artifact
- Author a sweeping new PRD that encompasses everything beyond V1.3

I AM asking COO to:

- Formalize the intake pipeline as a reusable operational object (probably a dedicated section or sub-PRD within the COMP_LEARNS architecture corpus)
- Define wave cadence, ownership, and gate structure
- Specify the trigger condition for when cross-target ratchet design becomes justified
- Surface the operational lane-concurrency model so future waves don't depend on ad hoc lane assignment

---

## §6 — My current lean

- **Griffe should be treated as the first proving run of the V1.3 intake pipeline.** If it survives pre-screen and yields a clean primary-case run, the pipeline is proven; if it fails pre-screen, the off-ramp gate is proven and we exercise the fallback chain.
- **One or more additional candidates (e.g., awkward-array, hishel) can be surveyed in parallel without yet forcing multi-target scoring.** Surveying is cheap; the readiness signal is whether intake reliably produces dispatchable targets, not whether scoring happens in parallel.
- **If griffe survives pre-screen and yields a clean primary-case run, that is the right moment to elevate the architecture discussion from "target intake" to "generalization loop."** That moment is also when the CTO+CVO cycle should produce a Stage 4 design brief — not before.
- **Until then, the disciplined move is to industrialize intake, not to over-design aggregate ratchet logic.**

---

## §7 — Feedback ask

Please return:

- Whether COO recommends formalizing an intake-wave PRD now (Option 1) or escalating immediately to multi-target ratchet design (Option 2)
- The proposed minimum viable wave structure (N / K / M, owners by lane, gate cadence)
- The boundary between intake-loop formalization and future multi-target ratchet design
- The explicit trigger condition for escalating into cross-target champion logic

**Format for response:** MCP ACK with substantive content, OR file a sub-PRD draft (e.g., `docs/architecture/COMP_LEARNS_INTAKE_WAVE.md`) if Option 1 is selected. If Option 1: I will review the sub-PRD and ACK target-intake operational model before next wave authoring; CVO sees only at material design decision points per workflow doctrine.

---

## §8 — Unknown-unknown

What I want COO to pressure-test is whether the program is still implicitly optimized around "find one good target and work it deeply," even though the newer governance work points toward "qualify many targets cheaply, then spend depth only on the few that survive."

If that organizational assumption is still embedded in lane ownership or TO structure (e.g., one DS lane per target permanently, or COO authoring TOs for one target at a time without considering wave parallelism), the macro-loop will remain conceptually right but operationally slow. The intake-wave formalization should explicitly surface and re-allocate any such embedded assumptions.

Concretely: today's pattern of "1.4.0_DS surveyed → 1.4.0_DS authored → 1.4.0_DS context kept fresh" worked because there was only one target in flight. With 3 targets in flight (one wave), this pattern would force serialization through one DS lane unless lane assignment is explicitly pluralized. The intake-wave PRD should specify how K targets in one wave map to K parallel DS lanes (or fewer, with explicit serialization rationale).
