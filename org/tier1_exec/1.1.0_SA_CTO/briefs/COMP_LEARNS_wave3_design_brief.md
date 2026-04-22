# COMP_LEARNS — Wave 3 Design Brief

**Date:** 2026-04-22
**Author:** 1.1.0_SA_CTO
**Status:** Issued — for Wave 3 PRD authoring + team alignment
**Predecessor:** Wave 2 closeout brief + GPT review session

---

## Strategic Read

Wave 2 was a real success. The important outcome is not just that we authored more structure; it is that COMP_LEARNS is now a runnable apparatus with backlog separation, automation tooling, and an active Stage 2 path. That is the right kind of progress.

The next risk is not under-building. It is trying to make Wave 3 prove too many things at once and diluting the one thing that matters most right now: **locking in a genuinely high-velocity, objective iteration loop that can drive compiler improvement repeatedly against a hard target.**

The highest-leverage thing in front of us is not broadening the case pool, adding more comparison axes, or trying to claim generality early. It is proving that we can take one well-chosen case, define a stringent quantitative success target, and run the loop repeatedly against that target until we hit it. If we can get that cycling strategy dialed in — with objective meters and a ratchet that actually works under pressure — that becomes the engine for everything else. Once that works on one case, parallelization stops being theoretical and becomes multiplicative.

**Wave 3 should be designed first to lock in a high-speed, objective compiler-improvement loop on a hard target. Once that engine is proven, broader comparative measurement and true parallelization become much more valuable and much less speculative.**

---

## Design Decisions

### 1. One primary looping case, not all four

Do not define Wave 3 as "run all 4 cases under both conditions." That is too diffuse for the current moment. Instead:

- **One primary case** — the loop-driving case. Compiler assistance must be plausibly load-bearing; success must be definable quantitatively enough to support repeated ratcheting. In practice this means Case 3 (sphinx, Archetype D, cross-module) or Case 4 (httpx, Archetype D, cross-module) as the formal measurement lane.
- **One or two secondary eval cases** — for measurement sanity, not for driving the loop.

The distinction matters: the primary case is where the machine iterates. The secondary cases are integrity checks on the measurement path.

### 2. dev-4 is central, not peripheral

A dev-4 KEEP (`dev-click-001`, Archetype B, compiler-win ratchet on click triple-nested chain) is not itself formal aided-vs-unaided measurement. But it is the strongest available evidence that the inner loop can produce real gains under the current runtime.

**dev-4 is the primary compiler-improvement lane for Wave 3.** Design it explicitly around:
- Stringent quantitative success target (not "can we get a KEEP?" but "can we drive this case to a hard benchmark level using objective meters and repeated ratchet cycles?")
- Repeated cycling until target is hit, budget is exhausted, or real plateau is demonstrated
- Mutation-family tracking (not just KEEP/DISCARD per iteration — track what kinds of changes move the metric)
- Plateau handling: when the loop stalls, diagnose and adjust before declaring failure
- Clear stop condition tied to a metric threshold, not vague "improvement"

That is the loop. Once it works on one case, parallel lanes become the multiplier.

### 3. The benchmark target must be stringent enough to force real iteration

Do not pick a success bar that can be cleared by one lucky mutation. The right target is one that requires sustained progress and makes the loop prove it can keep climbing. A target that is too easy validates nothing. A target that is genuinely hard and quantitative is the proof of the engine.

The concrete target definition is a Wave 3 PRD decision, but the design principle is: **require the system to iterate meaningfully to reach it, not just execute once.**

### 4. Apparatus stress runs in parallel — not as a hard prerequisite

`dev-1` (selector_ceiling, 3-hop import chain) and `dev-2` (ABCache cache_identity near-collision) should run concurrently as silent-failure detectors. They are useful as coverage-gap signals, not as gate conditions.

Escalation rule:
- **Ordinary coverage gap** → useful input, does not stop the main loop
- **Cache-identity or comparability corruption** → stop-the-line event

`dev-1` and `dev-2` do not block the core loop unless they expose an integrity failure.

### 5. Narrow measurement claims for this wave

We do not need to prove everything at once. Wave 3 needs to prove three things:

1. The loop can drive a compiler upward against a hard quantitative target
2. Stage 2 eval can produce clean formal verdicts on a small number of benchmark-grade cases
3. The system can distinguish real gains from local noise

That is enough. The following are explicitly deferred:
- Cross-model comparison (adds a second variance source; separate cleanly after single-model baseline)
- Case 5 / third repo family (current 4-case pool is sufficient for narrow first claims)
- Formal Archetype B/C benchmark coverage (add after measurement path is proven)
- General "systems-programming improvement" claims (only defensible after the loop is validated on multiple case families)

---

## Recommended Sequence

1. **Choose one primary looping case now.** Likely Case 3 (sphinx) or Case 4 (httpx). Decision criteria: which case has the clearest quantitative success bar and the most plausible compiler load-bearing surface?

2. **Set a stringent quantitative benchmark target for that case.** This is the most important design decision of Wave 3. It must be hard enough to require iteration, precise enough to be objective, and scoped to the compiler's actual levers.

3. **Run `comp-dev-loop.py` repeatedly against that target** until hit, budget exhausted, or real plateau demonstrated. Track mutation families. Treat plateau as diagnostic input, not failure.

4. **Run one formal eval event in parallel** (Stage 2, comp-wave-runner) to keep the measurement lane honest. This satisfies Stage 2 exit criterion progress and provides the first aided-vs-unaided delta reading.

5. **Run apparatus-stress cases in the background** (`dev-1`, `dev-2`). Escalate only on integrity-threatening findings.

6. **After loop behavior is understood**, then expand: reruns of Cases 1+2 under Stage 2 for formal baseline, broader Wave 3 measurement claims, eventually cross-model and additional archetype coverage.

---

## PRD Authoring Instructions

The Wave 3 PRD (to be authored as `COMP_LEARNS_WAVE3_V1.md`) should lock in:

- Primary looping case selection with justification
- Quantitative benchmark target definition (the hard number / metric)
- Stop conditions for the dev-4 loop (target hit / budget / plateau)
- Secondary eval case(s) and the formal verdict process
- Parallel apparatus-stress sequencing rules
- Measurement claims scope (what this wave proves, what it does not)
- Stage 2 exit criterion tracking (2+ waves zero-false-pass)
- Wave 3b scope (Cases 1+2 rerun under Stage 2 once Wave 3a loop behavior is understood)

The PRD does not need to specify the full scoring rubric — SC authoring handles that. It needs to specify the design center: **loop-first, measurement-second, claims-narrow**.
