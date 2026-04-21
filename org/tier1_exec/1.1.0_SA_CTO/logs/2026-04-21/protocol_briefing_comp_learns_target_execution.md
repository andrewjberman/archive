# Protocol Briefing — COMP_LEARNS Target-Execution Strategy

**From:** Codex  
**Date:** 2026-04-21  
**Purpose:** Clarify how COMP_LEARNS should actually be run now, and how `ajb_workspace/org/` should and should not be used in the protocol.

---

## 1. Recommendation in one sentence

COMP_LEARNS should run first on **pinned unfamiliar external targets** under `comp/targets/{name}/` using the **scorecard / experiment_log / ratchet** path as the authoritative loop; `org/` historical work should be used only as a **secondary regression corpus** or later **curated internal case-study targets**, not as the primary benchmark.

---

## 2. What the protocol should optimize for

The protocol should answer a narrow question first:

> Can we infer structural truth from an unfamiliar target, score it honestly against human-authored gold, and ratchet compilers forward without drift?

That means the primary benchmark must stay:

- pinned
- externally legible
- structurally bounded
- human-goldable
- insulated from our prior institutional memory

This is why `httpx` is the right kind of Phase-2 target and live `org/` history is not.

---

## 3. Canonical execution model

The authoritative loop should be the **modern ratchet path**, not the older harness/results framing.

**Canonical runtime path:**

1. `compiler.py` builds a graph for the pinned target.
2. Structural scorer compares graph vs human-authored gold.
3. Selector harness runs A/B over frozen question sets.
4. Mutation harness computes mutation stability.
5. `primary_metric` is computed from `ratchet_critical`.
6. Ratchet records KEEP / DISCARD / TIE against champion.
7. Scorecard JSON + `experiment_log.jsonl` are written as the durable learning trace.

**Authoritative artifacts:**

- `comp/targets/{target}/gold/*`
- `comp/targets/{target}/scorecards/*.json`
- `comp/targets/{target}/experiment_log.jsonl`
- `comp/targets/{target}/champion.json`

**Interpretation:**

- `comp.loop.ratchet` is the real learning loop.
- `results.tsv` / older harness-era observability remains useful only if treated as legacy shell/compatibility output rather than the source of truth.

If both paths remain live, the project should explicitly declare the ratchet/scorecard path authoritative and treat the older path as transitional.

---

## 4. Why `org/` should NOT be the primary benchmark

Using historical tasks in `ajb_workspace/org/` as the main test surface would blur several boundaries the protocol currently needs to keep clean:

1. **Benchmark honesty risk.** We already know too much about our own task-order machinery, naming, lane conventions, and project history. That weakens the “unfamiliar system” property.
2. **Target-boundary ambiguity.** `org/` is not a clean single target. It is a live operational corpus containing logs, TOs, PRDs, handoffs, and process artifacts.
3. **Metric contamination.** A benchmark on `org/` would reward protocol-memory and house-style familiarity alongside structural inference.
4. **Gold-authoring ambiguity.** It is much harder to define a stable, bounded, human-authored gold set for a live evolving operational tree than for a pinned code target like `httpx`.
5. **Execution noise.** Internal process docs contain exceptions, supersessions, rewrites, and human context that are not the same kind of structural object as source code imports/edges.

Conclusion: `org/` is valuable, but not as v0’s primary benchmark.

---

## 5. How `org/` SHOULD be used

`org/` should enter the protocol in two narrower roles.

### 5.1 Regression corpus from named prior failures

When a real failure has already been observed, extract it into a small pinned fixture or mini-target.

Good examples:

- star-import unresolved binding
- dynamic-import absent/present distinction
- selector leakage / random-selector anomaly
- deterministic-vs-nondeterministic output cases
- ambiguity vs conflict cases
- process-derived structural patterns that can be made target-local and frozen

The rule here is:

> Do not benchmark on live `org/`; distill from `org/` into frozen fixtures.

This preserves realism without contaminating the main benchmark.

### 5.2 Later curated internal case-study targets

After the loop proves itself on at least two unfamiliar external targets, introduce a later realism lane using curated internal targets.

Those should be:

- frozen snapshots, not live directories
- bounded to one target root
- gold-authored exactly like external targets
- stripped of unrelated operational chatter
- version-pinned and benchmarked as independent targets under `comp/targets/{name}/`

This is a valid v1-style realism extension, but it should not define v0’s truth surface.

---

## 6. Three-layer protocol going forward

The cleanest protocol shape is:

### Layer 1 — Primary benchmark layer

Pinned unfamiliar external targets.

Purpose:

- prove honest structural inference
- validate ratchet behavior
- avoid internal-memory contamination

Examples:

- `httpx`
- later target-2 external repo selected by `.009`

### Layer 2 — Regression layer

Small frozen fixtures extracted from named prior failures.

Purpose:

- defend against recurrence
- turn incidents into mechanical tests
- tighten subtype / graph / selector / cache correctness

Sources may include `org/`, but only after distillation into frozen local fixtures.

### Layer 3 — Internal realism layer (later)

Curated frozen internal case-study targets.

Purpose:

- test whether the system transfers into AJB-flavored structural messiness
- measure realism only after the external benchmark is trustworthy

This layer should come after external-target competence, not before it.

---

## 7. Immediate next-step recommendation

The next protocol move should be to run the first real `.017` end-to-end ratchet on `httpx`, not to expand benchmark surfaces.

The immediate questions worth answering are:

1. Does the ratchet actually produce sensible KEEP / DISCARD behavior on the current `httpx` target?
2. Does induced regression lower `primary_metric` and cause DISCARD cleanly?
3. Does mutation stability meaningfully affect the score?
4. Do selector outcomes make sense on a live graph?

This is important because the current experiment trace already suggests a meaningful issue: the observed `best_selector` is `random` in the visible `httpx` experiment log entries. That is exactly the kind of live-signal anomaly the protocol should surface and investigate before widening scope.

Implication:

- do **not** add more benchmark formalization yet
- do **not** pivot into live `org/` case-study testing yet
- run `.017`, inspect failure modes, and only then decide what new protocol surface is earned

---

## 8. Operational rule for CTO / COO

When deciding whether to add a new benchmark surface, ask:

> Is this helping us measure the ratchet on an unfamiliar pinned target, or is it introducing realism before the core signal is trustworthy?

If it is the latter, defer it.

When deciding whether to use `org/`, ask:

> Is this a live operational corpus, or has it been distilled into a frozen target/fixture with clean gold?

If it is still live corpus, it belongs outside the primary benchmark.

---

## 9. Bottom line

The right protocol is:

- **external pinned targets first**
- **ratchet/scorecard path as authority**
- **`org/` only as distilled regression input now**
- **curated internal case studies later**

That keeps COMP_LEARNS athletic: real loop pressure first, realism expansion only after the loop has earned trust.
