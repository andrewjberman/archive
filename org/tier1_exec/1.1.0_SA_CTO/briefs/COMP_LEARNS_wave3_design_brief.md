# COMP_LEARNS — Wave 3 Design Brief

**Date:** 2026-04-22
**Author:** 1.1.0_SA_CTO
**Status:** Issued — for Wave 3 PRD authoring + team alignment
**Predecessor:** Wave 2 closeout brief + GPT review session (rev 2 — primary case proposition added)

---

## Strategic Read

Wave 2 was a real success. The important outcome is not just that we authored more structure; it is that COMP_LEARNS is now a runnable apparatus with backlog separation, automation tooling, and an active Stage 2 path. That is the right kind of progress.

The next risk is not under-building. It is trying to make Wave 3 prove too many things at once and diluting the one thing that matters most right now: **locking in a genuinely high-velocity, objective iteration loop that can drive compiler improvement repeatedly against a hard target.**

The highest-leverage thing in front of us is not broadening the case pool, adding more comparison axes, or trying to claim generality early. It is proving that we can take one well-chosen case, define a stringent quantitative success target, and run the loop repeatedly against that target until we hit it. If we can get that cycling strategy dialed in — with objective meters and a ratchet that actually works under pressure — that becomes the engine for everything else. Once that works on one case, parallelization stops being theoretical and becomes multiplicative.

**Wave 3 should be designed first to lock in a high-speed, objective compiler-improvement loop on a hard target. Once that engine is proven, broader comparative measurement and true parallelization become much more valuable and much less speculative.**

---

## What the Compiler Is Actually For

Before selecting the primary case or setting any target, the program goal needs to be stated precisely, because it shapes every downstream decision.

The project is not trying to make frontier models better at software tasks in the abstract. The real goal is to build graphing and indexing compilers that let frontier models navigate complex, interdependent codebases with less blind exploration, less wasted wall-clock time, and less wasted token spend.

The central proposition the program is testing:

> **Does the compiler materially improve the model's ability to find, localize, and act on the correct structural context in a hard codebase, relative to unaided exploration?**

That is the intervention being tested. The primary Wave 3 case should be structured to test that proposition directly — not task difficulty in general, not reasoning quality in the abstract, not generic improvement. Structural navigation efficiency is the thing being measured.

The accomplishment we are after is narrower and more operational than "get a KEEP" or "solve the task." The compiler should:

1. Increase the probability that the model reaches the correct working set of files, nodes, and edges
2. Get the model there faster than the unaided path
3. Reduce wasted search and irrelevant context traversal
4. Do so on an objective meter, not just a subjective impression

---

## Design Decisions

### 1. One primary looping case, not all four

Do not define Wave 3 as "run all 4 cases under both conditions." That is too diffuse for the current moment. Instead:

- **One primary case** — the loop-driving case, selected to test the structural navigation proposition directly
- **One or two secondary eval cases** — for measurement sanity, not for driving the loop

The distinction matters: the primary case is where the machine iterates. The secondary cases are integrity checks on the measurement path.

**Case selection criteria for the primary case.** The best inaugural case is not simply whichever one is available first. It must satisfy:

- The compiler's graph and index are plausibly load-bearing (structural traversal is required, not optional)
- The correct working set is non-obvious without structure (unaided exploration genuinely wastes work)
- The case requires cross-module or dependency-aware reasoning (not just local editing skill)
- There is a measurable intermediate success signal before final task completion
- It is possible to quantify "got to the right context faster and cleaner"

**A cross-module diagnosis case is likely better than a purely local bug fix for the first formal measurement lane.** Cases 3 (sphinx, Archetype D) and Case 4 (httpx, Archetype D) both satisfy these criteria. Case selection between them is a Wave 3 PRD decision, but the criteria above should drive it — not sequencing convenience.

### 2. dev-4 is central, not peripheral

A dev-4 KEEP (`dev-click-001`, Archetype B, compiler-win ratchet on click triple-nested chain) is not itself formal aided-vs-unaided measurement. But it is the strongest available evidence that the inner loop can produce real gains under the current runtime.

**dev-4 is the primary compiler-improvement lane for Wave 3.** Design it explicitly around:
- Compound success target (see §3 below — not just a KEEP threshold)
- Repeated cycling until target is hit, budget is exhausted, or real plateau is demonstrated
- Mutation-family tracking (not just KEEP/DISCARD per iteration — track what kinds of changes move the metric and whether they cluster around a useful mechanism)
- Plateau handling: when the loop stalls, diagnose before declaring failure
- Clear stop condition tied to a hard metric threshold, not vague "improvement"

That is the loop. Once it works on one case, parallel lanes become the multiplier.

### 3. The benchmark target is compound, not a single scalar

A KEEP is useful but it is only local evidence that one mutation beat the prior champion. It is not yet the real benchmark. The benchmark must have two layers.

**Layer 1 — Compiler-internal success (loop ratchet surface)**

This is the immediate ratchet target. It requires:
- Sustained `primary_metric` improvement, not a one-off jump
- Repeated KEEP behavior or equivalent evidence that gains are not accidental
- Plateau detection deferred until a meaningful range of mutation families has been exercised
- Evidence that winning changes cluster around a useful mechanism rather than random noise

**Layer 2 — Task-mediated success (program-relevant outcome)**

This is the actual value the compiler is supposed to deliver. It requires:
- Aided condition reaches the correct task-relevant context faster than unaided
- Aided condition uses fewer tokens or less wall-clock to reach the same or better result
- Aided condition shows better structural localization (fewer irrelevant files, fewer wasted traversals)
- Final task correctness is at least preserved, and ideally improved

**The compound success target looks like:**
- `primary_metric` exceeds a predeclared threshold on the looping case
- Aided condition beats unaided on at least one efficiency axis (wall-clock, token count, or context precision)
- The result reproduces on rerun, not just once

Do not pick a success bar that can be cleared by one lucky mutation. The right target requires sustained progress and makes the loop prove it can keep climbing.

### 4. Primary case definition must be explicit before looping begins

Before the dev-loop runs against the primary case, the Wave 3 PRD must define five things:

**1. Structural objective**
What is the correct working set the compiler is supposed to help surface? Name the specific files, modules, or nodes the aided path should reach and the unaided path likely misses or reaches late.

**2. Navigation-efficiency objective**
How will we measure whether the compiler reduces exploration waste? Specify the metric(s): tokens to first correct hypothesis, wall-clock to first correct hypothesis, number of files touched before reaching the decisive file set, number of irrelevant files touched. The baseline for each must be established from the unaided condition run.

**3. Ratchet objective**
What hard `primary_metric` threshold is the loop trying to reach? This number must be set before the loop runs and must be hard enough to require real iteration, not a first-attempt ceiling.

**4. Reproduction requirement**
How many successful reruns are required before we treat a gain as real? A result that clears the target once is insufficient. Specify the minimum replication count.

**5. Failure and plateau interpretation**
Define in advance what each failure mode means so they can be distinguished:
- "The loop is not finding a better compiler" → plateau signal, tune mutation strategy
- "The case is poorly chosen" → case selection error, not compiler failure
- "The metric is misaligned" → measurement design error, escalate to CTO

Conflating these three is how programs misread a measurement failure as a compiler failure or vice versa.

### 5. The measurement package for the primary case

The first Wave 3 primary case scoring should capture:

| Signal | Purpose |
|--------|---------|
| Final correctness / verdict | Task-level outcome |
| Wall-clock to first correct hypothesis | Navigation-efficiency (speed) |
| Token usage to first correct hypothesis | Navigation-efficiency (cost) |
| Files touched before reaching the decisive file set | Structural precision |
| Irrelevant files touched | Exploratory waste |
| Aided-vs-unaided delta on each of the above | Compiler intervention effect |

This package answers the real question: does the compiler help the model get to the right part of a hard codebase faster, cheaper, and more correctly than unaided exploration?

### 6. Apparatus stress runs in parallel — not as a hard prerequisite

`dev-1` (selector_ceiling, 3-hop import chain) and `dev-2` (ABCache cache_identity near-collision) should run concurrently as silent-failure detectors. They are useful as coverage-gap signals, not as gate conditions.

Escalation rule:
- **Ordinary coverage gap** → useful input, does not stop the main loop
- **Cache-identity or comparability corruption** → stop-the-line event

`dev-1` and `dev-2` do not block the core loop unless they expose an integrity failure.

### 7. Narrow measurement claims for this wave

Wave 3 needs to prove three things:

1. The loop can drive a compiler upward against a hard compound target on a structural navigation case
2. Stage 2 eval can produce clean formal verdicts with aided-vs-unaided efficiency deltas
3. The system can distinguish real navigation gains from local noise

That is enough. The following are explicitly deferred:
- Cross-model comparison (adds a second variance source; separate after single-model baseline)
- Case 5 / third repo family (current 4-case pool is sufficient for narrow first claims)
- Formal Archetype B/C benchmark coverage (add after measurement path is proven)
- General "systems-programming improvement" claims (only defensible after loop is validated on multiple case families)

---

## Recommended Sequence

1. **Choose one primary looping case.** Apply the case selection criteria in §1. Likely Case 3 (sphinx) or Case 4 (httpx) — both Archetype D cross-module. Decision criteria: which has the clearer unaided-vs-aided structural navigation gap and the more measurable intermediate signal?

2. **Define the 5-part primary case spec before looping begins.** Structural objective, navigation-efficiency objective, ratchet objective, reproduction requirement, failure interpretation. This is the most important design work of Wave 3.

3. **Set the compound success target.** Two layers: ratchet threshold + efficiency axis beat + reproduction count. Hard enough to require real iteration.

4. **Run `comp-dev-loop.py` repeatedly against that target.** Track mutation families. Treat plateau as diagnostic input. Capture the full measurement package per run.

5. **Run one formal eval event in parallel** (Stage 2, comp-wave-runner) to keep the measurement lane honest and satisfy Stage 2 exit criterion progress.

6. **Run apparatus-stress cases in the background** (`dev-1`, `dev-2`). Escalate only on integrity-threatening findings.

7. **After loop behavior is understood**, expand: reruns of Cases 1+2 under Stage 2, broader Wave 3 measurement claims, eventually cross-model and additional archetype coverage.

---

## PRD Authoring Instructions

The Wave 3 PRD (to be authored as `COMP_LEARNS_WAVE3_V1.md`) must lock in:

- Primary case selection with justification against the structural navigation criteria
- The 5-part primary case definition (structural objective, navigation-efficiency objective, ratchet objective, reproduction requirement, failure interpretation)
- Compound success target (ratchet threshold + efficiency delta + reproduction)
- The full measurement package (6 signals listed in §5) and how each is collected
- Stop conditions for the dev-loop (target hit / budget / plateau)
- Secondary eval case(s) and the formal verdict process
- Parallel apparatus-stress sequencing rules
- Measurement claims scope (what this wave proves, what it does not)
- Stage 2 exit criterion tracking (2+ waves zero-false-pass)
- Wave 3b scope (Cases 1+2 rerun under Stage 2 once Wave 3a loop behavior is understood)

The design center is: **loop-first, measurement-second, claims-narrow, navigation-efficiency as the intervention axis.**
