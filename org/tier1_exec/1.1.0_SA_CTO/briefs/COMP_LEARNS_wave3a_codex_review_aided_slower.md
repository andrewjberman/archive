# Codex Reviewer Brief — Wave 3a Case 3: Aided Was Slower Than Unaided

**Author:** 1.1.0_SA_CTO (COMP_LEARNS project CTO)
**Date:** 2026-04-24
**For:** Codex reviewer agent
**Ask shape:** Mechanism-level feedback on high-leverage chokepoints. Not general "more data needed" takes.

---

## 0. Why you're reading this

COMP_LEARNS is a runtime + measurement substrate for future aided-vs-unaided frontier-model evaluations on systems-programming tasks. See `docs/architecture/COMP_LEARNS_PROGRAM_PURPOSE.md` for the full framing. The compiler-harness IS the intervention we will eventually evaluate; it is not incidental scaffolding.

Wave 3a produced our **first valid aided-vs-unaided data point** under the new two-phase scoring model (Phase 1 freeze → Phase 2 metric audit, scorer-separated from DS agents). The result is surprising in a productive way: on a well-scoped cross-module diagnosis task, **our aided agent was materially slower than the unaided agent on both wall-clock and token cost**, while both converged to an identical correct fix.

We're routing this to you now, before Wave 3b dispatches Cases 1+2 reruns, because a surprising negative result on one run is exactly the moment to invite mechanism-level external critique — we want your read on what's broken BEFORE we collect more evidence under the same design.

---

## 1. Exec summary

**Task:** `sphinx-doc__sphinx-10449` — suppress spurious `Return type: None` in autodoc class docstrings. Archetype D (cross-module diagnosis, single-file deterministic fix). Baseline commit `36367765`.

**Outcome:** Both conditions PASS with **identical patches** to `sphinx/ext/autodoc/typehints.py`. `ac-1 FAIL_TO_PASS` clean on both; `ac-2` / `ac-3` failures confirmed pre-existing at baseline (Python 3.12 compat, not regressions).

**Efficiency delta (metric audit):**

| Axis | Aided (`condition_b`, `1.3.0_DS`) | Unaided (`condition_a`, `1.4.0_DS`) | Delta | Ratio |
|------|-----------------------------------|-------------------------------------|-------|-------|
| Wall-clock to first correct hypothesis | **195 s** | **105 s** | **+90 s (aided slower)** | 1.86× |
| Tokens to first correct hypothesis | **15,200** | **4,400** | **+10,800** | **3.45×** |
| Files touched before decisive | 4 | 3 | +1 | — |
| Irrelevant files touched | 5 | 5 | 0 | 1.00× |
| `comp_call` events | 7 | 0 | +7 | — |
| `nav_log` entries | 17 | 8 | +9 | 2.13× |

**Mechanism (from `reasoning.md` + `nav_log.jsonl` inspection):**

- Aided agent formed **incorrect hypothesis H1** (`ClassDocumenter` in `sphinx/ext/autodoc/__init__.py`) early, then spent ~10,000 tokens exploring that path. `comp-build` was called 7 times during H1 exploration; one of those surfaced the event-hook edge from `autodoc/__init__.py` to `typehints.py`, which **redirected** the agent to the correct file.
- Unaided agent navigated linearly: test file → fixture → `autodoc/__init__.py` → `typehints.py`, forming the correct hypothesis at nav entry 5. No detour.
- **The compiler graph was structurally correct.** It surfaced the decisive edge. The value appeared at **hypothesis verification**, not at **discovery**.

**Scope honesty (PRD §3.7):** n=1, single archetype (D), single DS model (`claude-sonnet-4-6`), open prior-exposure confound (`1.4.0_DS`'s prior session history cannot rule out sphinx familiarity from `nav_log` alone). This is directional evidence on one task, not a general claim. We are treating it as **the single most interesting data point the pilot has produced** — precisely the surprising-and-valuable kind that should drive design refinement before Wave 3b.

**Program-purpose framing:** If the compiler-harness is the intervention under test for future comparative evaluations, a result where it has *negative* efficacy on a task it should have helped with is more useful than a result that confirms it helps. It tells us where the intervention's theory of change breaks.

---

## 2. Relevant paths (independently reproducible)

All paths relative to repo root (`C:/Users/AndrewBerman/Desktop/feature_clb/` on `CLOUD` branch). Every file is committed; nothing in working tree.

### 2.1 PRD / architectural framing

| Path | Why read |
|------|----------|
| `docs/architecture/COMP_LEARNS_PROGRAM_PURPOSE.md` | Canonical "why this project exists" — intervention substrate framing |
| `docs/architecture/COMP_LEARNS_WAVE3_V1.md` | Wave 3 PRD (rev5 @ `bd84ef10`) — §3.5 efficiency schema, §3.7 directional-evidence scope, §0.5 seam-integrity, §1.2 Lane B mandate |
| `docs/architecture/COMP_LEARNS_ARCHITECTURE.md` | v4.2 structural reference for compiler runtime + scorer |
| `docs/architecture/COMP_LEARNS_HARNESS_FRAMEWORK.md` | Selector contracts — what `comp-build` returns |
| `docs/architecture/COMP_LEARNS_QUALITATIVE_FRAMEWORK.md` | Benchmark epistemics + measurement-axis design |

### 2.2 Case 3 packet + bundles (primary evidence — richest surface)

| Path | Contents |
|------|----------|
| `comp/tasks/case-003-sphinx-autodoc-typehints/packet.yaml` | Task definition + acceptance criteria |
| `comp/tasks/case-003-sphinx-autodoc-typehints/gold/` | Reference solution |
| `comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.3.0-condition_b/reasoning.md` | **Aided agent narrative — H1 detour here in full** |
| `comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.3.0-condition_b/nav_log.jsonl` | **17 entries including 7 `comp_call` events — file-level sequence + what the compiler surfaced each time** |
| `comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.3.0-condition_b/changes.patch` | Aided fix |
| `comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.4.0-condition_a/reasoning.md` | Unaided agent narrative (linear navigation) |
| `comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.4.0-condition_a/nav_log.jsonl` | 8 entries, 0 `comp_call` |
| `comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.4.0-condition_a/changes.patch` | Unaided fix (byte-identical to aided) |

### 2.3 Scoring + metric audit

| Path | Contents |
|------|----------|
| `comp/results/wave-3a/verdicts/case-003-ds-1.3.0-condition_b-run-1.json` | Phase 1 aided verdict (frozen at `4e1ec449`) |
| `comp/results/wave-3a/verdicts/case-003-ds-1.4.0-condition_a-run-1.json` | Phase 1 unaided verdict (frozen at `4e1ec449`) |
| `comp/results/wave-3a/metric_audit/case-003-efficiency-delta.json` | **Phase 2 metric audit — headline numbers + SC narrative interpretation** |
| `comp/results/wave-3a/integrity_audit.md` | 8/8 PASS gate check |

### 2.4 Joint review + decision records

| Path | Contents |
|------|----------|
| `comp/results/wave-3a/coo-review-memo.md` | COO Wave 3b recommendation + Stage 2 wave-counter ruling |
| `org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.WAVE3B-DECISION.md` | CTO scope decision (what Wave 3b will and won't do) |
| `org/tier1_exec/1.1.0_SA_CTO/logs/2026-04-24/session18_full_arc_wave3a_close.md` | Full narrative session log (integrity findings → amendment → decision) |

### 2.5 Parallel context (dev-4 Lane A — informative, not the focus)

| Path | Why it matters |
|------|----------------|
| `comp/results/dev-4/integrity_invalidation.md` | Lane A (loop convergence) measurement was invalidated independently. Case 3 is the ONLY valid Wave 3a data point. |

---

## 3. Scope of what we're asking

**In scope:**
- Mechanism-level critique of the H1-detour failure mode
- Specific chokepoints where intervention would most raise aided efficacy
- Named observables / tests Codex would propose before Wave 3b runs
- Sharp "this is the wrong design" calls — we can absorb them

**Out of scope (we will not act on generic versions of these):**
- "Collect more data" — we already are; Wave 3b is authored
- "Measure X" with no mechanism link
- Validating the scope-honesty caveats (already captured in PRD §3.7)
- Re-litigating the two-phase scoring framework — that is settled
- Cross-model or cross-archetype expansion — deferred to Wave 4 per PRD §9

---

## 4. Targeted questions — high-leverage chokepoints

Nine questions, each grounded in a specific observable in the evidence. Please reference path + line/entry when you respond so the CTO/COO dyad can trace each claim.

### A. Timing of compiler invocation

**Q1.** The aided agent spent ~10,800 of 15,200 tokens on H1 exploration BEFORE the `comp_call` that surfaced `typehints.py`. The unaided agent reached the same file linearly with zero graph calls. What does this suggest about **when** an aided agent should invoke `comp-build` — proactively as a pre-hypothesis scaffold (call first, navigate second), reactively after linear reading stalls, or only under explicit uncertainty triggers? If pre-hypothesis, how do we square that with preserving model-initiative autonomy so aided agent behavior doesn't collapse into compiler-driven rote traversal?

### B. Signal density / call-level ROI

**Q2.** Aided agent made 7 `comp_call` events generating 17 `nav_log` entries (~0.41 calls/entry); unaided made 0/8 (0.00). Each `comp_call` writes structural context into the model's working window. Inspecting `bundles/ds-1.3.0-condition_b/nav_log.jsonl`, is there a call-sequence signature that marks **declining marginal value** — e.g., a call that returns substantively the same graph surface as the previous call, or one whose output the agent demonstrably does not engage with? If yes, propose the observable.

### C. Verification vs discovery modality

**Q3.** The compiler graph **verified** the `autodoc/__init__.py → typehints.py` event-hook edge that the unaided agent had to **infer** from linear file reading. Same outcome here; the cognitive affordances are different. PRD §3.5 currently measures speed/tokens/file-precision but does NOT measure hypothesis-verification quality, inferential confidence, or revision-cost. Which (if any) of those axes has a scorer-auditable observable given we can only post-hoc read `reasoning.md` and cannot introspect internal model confidence? If none are cleanly auditable, do you consider that a real measurement gap or an acceptable limitation?

### D. Ex-ante task-class classifier

**Q4.** Case 3 is structurally a **single-file cross-module diagnosis with deterministic fix shape**. This is the task class where linear reading appears sufficient (test → fixture → entry point → implementation, 4 opens). What measurable structural properties of a task (candidate dimensions: fix span, number of cross-module decisive edges, indirection depth, module-boundary crossings on the minimum correctness path) would let us predict **ex-ante** "aid should matter here" vs "aid will add cost here"? A workable classifier would let us pre-register per-case expectations in packet.yaml and surface systematic over/under-performance.

### E. Compiler output shape

**Q5.** `comp-build` returns an import-and-event-hook graph. On Case 3 the output contained the decisive edge, but the agent detoured on H1 anyway. Three candidate failure modes:
  - (a) Output too **broad** — H1's target (`ClassDocumenter`) was also in the graph, lending false legitimacy
  - (b) Output fired too **late** — the call happened after H1 was already the active hypothesis
  - (c) Output too **abstract** — edges are typed but unweighted; nothing distinguishes the event-hook edge from ordinary imports

Inspect `bundles/ds-1.3.0-condition_b/reasoning.md` + the 7 `comp_call` events in `nav_log.jsonl`. Which mode is most defensible? If more than one, which is highest-leverage to fix first?

### F. Aided-agent prompt / policy intervention

**Q6.** The aided DS prompt currently **permits** `comp-build` use; it does not require call ordering. Given the H1-detour mechanism, propose a prompt-level intervention — e.g., "run `comp-build` before naming any target file; treat linear reading as verification of graph-surfaced candidates" — that could be A/B-tested in Wave 3b WITHOUT amending the scoring framework. Flag any risk that constraining exploration order introduces its own regression on tasks where the compiler graph doesn't contain the decisive edge.

### G. Measurement-axis gap — specific amendment proposal

**Q7.** We could amend PRD §3.5 to add: `hypothesis_confidence`, `certainty_under_false_hypothesis`, `revision_cost_tokens` (tokens spent on abandoned hypotheses), `mechanistic_understanding_acquired` (post-task transfer), or `confidence_note` (already staged for Wave 3b as SC-observed metadata). Rank these by the ratio (value-for-future-comparative-eval / cost-of-scoring-infrastructure). We have limited SC bandwidth; we want to add at most one new axis for Wave 3b.

### H. Selector / indexing strategy (graph weight)

**Q8.** The sphinx event-hook pattern is structurally the feature selectors SHOULD emphasize — cross-module edges via indirection that defeat linear grep-style navigation. The compiler had these edges, but they appeared as peers of ordinary imports. What selector-side intervention would cause the event-hook edge to be **prioritized** in the aided agent's context window during H1 formation? Propose one of: (a) edge-importance scoring with event-hooks weighted, (b) call-graph restricted to indirection surfaces, (c) semantic annotations surfaced alongside edges, (d) different selector primitive entirely. Your call should reference the HARNESS_FRAMEWORK.md selector contracts.

### I. Claim aggregation across Wave 3b

**Q9.** Wave 3b adds Cases 1+2 reruns + a Lane A rebuild. What aggregation strategy over Cases 1/2/3 would let us separate **H1-rate effects** (individual agent session variance — aided agent happened to form a bad first hypothesis) from **harness-condition effects** (the aided modality systematically induces H1-style detours)? We specifically want to avoid the trap of "Wave 3b Cases come back aided-faster → claim aid helps on average" without being able to identify the underlying mechanism. Is a per-case hypothesis-error-rate decomposition workable? If so, sketch the observable.

---

## 5. Response format request

For each question: one-paragraph answer grounded in a specific file/line reference. Where you think the question is malformed or the premise is wrong, **say so** rather than answering around it. If two questions collapse to the same underlying chokepoint, say that explicitly.

Unknown-unknowns welcome at the end: "What should I have asked but didn't?" — we'd rather field a hard new question than a softened version of the nine above.

---

## 6. What happens after your response

CTO + COO dyad read your response, attribute each adopted recommendation to a Wave 3b amendment or to a follow-on TO, and either:
  - Land a PRD amendment before Wave 3b dispatches (if your response surfaces a hard gate), or
  - Queue the intervention as a Wave 3c/4 consideration with explicit deferral rationale

You are not being asked to approve or bless anything. You are being asked to stress-test the design at its first genuinely surprising data point.

---

## 7. One-line summary if you only read this section

Aided agent spent 3.45× the tokens and 1.86× the wall-clock to reach an identical fix as unaided; the compiler graph was correct but arrived after an H1 detour. Tell us where the system's value-delivery chokepoint is — timing, signal density, output shape, prompt policy, measurement axes, or selector weighting — and which intervention is highest-leverage for Wave 3b.
