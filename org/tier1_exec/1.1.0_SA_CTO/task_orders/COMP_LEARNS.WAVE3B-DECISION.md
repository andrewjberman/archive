# COMP_LEARNS Wave 3b Decision Record

**Author:** 1.1.0_SA_CTO
**Date:** 2026-04-24
**TO:** COMP_LEARNS.053 (joint review — CTO section)
**Gates cleared:** `.048` dev-4 COMPLETE (integrity invalidated per `df168552`) + `.051` Case 3 SC two-phase scoring COMPLETE (PASS/PASS, aided +90s/+10800 tokens)
**PRD authority:** `docs/architecture/COMP_LEARNS_WAVE3_V1.md` @ `bd84ef10` (rev5)
**Status:** Active — decision record; closes `.053` CTO lane on commit

---

## 1. dev-4 Loop Assessment

**Parallel-expansion fitness:** CONDITIONAL — not fit now; becomes fit under PRD §2.0 preconditions after Lane A rebuild.

Three-component assessment:

| Component | Assessment | Evidence |
|-----------|------------|----------|
| State machine (KEEP/DISCARD/TIED/plateau) | **FIT** | `comp/results/dev-4-confirm-1/` exercised all transitions correctly; 3-iter loop with budget-exhaust exit path verified |
| Measurement pipeline | **UNFIT** | `.048` post-mortem `df168552` — self-scored bundle, no canonical source, measurement-invalid |
| Budget accounting | **PARTIAL** | Budget-exit behavior is correct (loop terminates), but `total_iterations` off-by-one on budget-hit-at-iter-boundary; fix is a separate TO |

**Recommended settings for future valid Lane A runs** (carry forward directionally from `comp/results/dev-4/loop_fitness_recommendation.md`, contingent on §2.0 preconditions satisfaction):

- `judge_mode`: `real` (not mock — mock scoring is the resurrected failure mode session11 closed)
- `burst-n`: 3
- `plateau-n`: 3
- `budget-hours` per run: **6-8** (observed ~2h/iteration on click; the original 2h budget was insufficient for multi-iteration climb and also never actually applied per finding 3 of the post-mortem)
- Priority mutation families to exercise first: `edge_generation` (depth-2 variant), `cross_module_hint_injection`, `selector_depth_increase`

**Explicit constraint on these settings:** they are DIRECTIONAL GUIDANCE, not empirically-validated values. They were derived from `.048`'s mechanics-only run. Any Lane A rebuild TO must treat them as starting points, not locked parameters. Reassess after the first valid Lane A measurement produces real data.

**Parallel-expansion authorization:** WITHHELD until at least one valid Lane A run produces measured evidence. Wave 4 parallel expansion of the loop cannot be justified on `.048` evidence alone.

---

## 2. Case 3 Measurement Claim Scope

### What the directional evidence SUPPORTS

On this single cross-module failure diagnosis task (`sphinx-doc__sphinx-10449`), under `claude-sonnet-4-6` as the DS baseline:

- Both aided and unaided agents independently solved the task correctly with **identical patches** (PASS/PASS on `ac-1 FAIL_TO_PASS`).
- Unaided linear navigation was **faster** (105s vs 195s wall-clock) and **more token-efficient** (4400 vs 15200 tokens) than aided compiler-graph traversal.
- The aided agent's excess cost was attributable to an initial incorrect hypothesis (H1: `ClassDocumenter`) that the compiler import graph eventually corrected toward `typehints.py` via event-hook edges.
- The compiler graph call (`comp-build` import trace) was **structurally correct** — it did surface the decisive file. The value appeared at hypothesis-verification time, not discovery-time.

### What the evidence DOES NOT SUPPORT (per PRD §3.7)

- No general claim about "compiler assistance is slower" — n=1, session variance not controlled
- No general claim about "compiler assistance helps" — this case directionally refutes on efficiency dimensions
- No cross-model claim — only `claude-sonnet-4-6` exercised
- No cross-archetype claim — Archetype D only
- No statistical significance claim — Wave 3 is explicitly directional-only per §3.7
- No claim about the "identical patches" convergence — single data point; could reflect task-peculiarity (cross-module diagnosis with deterministic fix shape) rather than harness-convergence property

### Open confound flagged in SC Phase 2 audit

> `unaided_prior_sphinx_exposure: unknown — cannot rule out from nav_log alone. 1.4.0_DS ran .042 (comp-preflight infrastructure, not sphinx-specific). No explicit sphinx exposure flagged. Directional evidence claim not invalidated; flagged as open confound per PRD §3.6.`

This confound is NOT blocking for Wave 3a closure but MUST be controlled in Wave 3b — specifically, reruns of Cases 1+2 should use DS agents with no prior exposure to the candidate repo in their session history, or the confound must be named in the Wave 3b scope.

### Observation worth naming (not an amendment — direction for Wave 3b)

The SC narrative identifies a measurement-surface gap: **PRD §3.5 measures efficiency (time, tokens, file precision) but does not measure certainty or hypothesis-verification quality.** The aided agent's compiler-graph call demonstrably VERIFIED the cross-module connection that the unaided agent had to INFER from linear file reading. Those are different cognitive affordances. On this task they collapsed to the same outcome, but in cases where the unaided agent's inferential confidence is WEAKER, the compiler's verification benefit may be decisive.

Wave 3b should, without amending the PRD, add a `confidence_note` field to the SC metric-audit artifact capturing whether the aided vs unaided agent appeared confident at hypothesis-formation time (subjective from SC reading `reasoning.md` in Phase 2 is acceptable — it's metadata, not a verdict input). If a future measurement surfaces "aided-higher-confidence at equal-efficiency," that's a non-efficiency-axis intervention value worth PRD-naming in Wave 4.

---

## 3. Wave 3b Scope (explicit Y/N per item)

| Item | Y/N | Rationale |
|------|-----|-----------|
| Cases 1+2 reruns under Stage 2 (clean formal baseline, not Stage 1 pilot data) | **YES** | PRD §1.2 original mandate + n=1 on Case 3 is too thin for directional-evidence aggregation. Reruns produce 2 more data points under the same two-phase scoring model. |
| Lane A rebuild under §2.0 preconditions | **YES** | Required for the 2-wave Stage 2 exit criterion AND for any Wave 4 parallel-expansion justification. Proceeds in parallel with Cases 1+2 reruns. |
| Mutation-family strategy change | **N/A — DEFERRED** | No valid Lane A measurement exists yet; cannot change strategy from null baseline. Revisit after first valid Lane A KEEP or plateau event produces real family-attribution data. |
| Archetype breadth expansion beyond B+D | **NO** | PRD §9 explicitly defers to Wave 4. Expanding now would dilute the narrow-claim discipline that protects Wave 3 from overclaim. Cases 1+2 are Archetype B (regression-safe refactor) + the original Archetype B pilot — same archetype as dev-4. Case 3 is Archetype D. Adding archetypes without first accumulating within-archetype data would muddy the signal. |
| Cross-model comparison (non-`claude-sonnet-4-6` DS) | **NO** | PRD §9 deferred to Wave 4. Single-model baseline is not yet saturated. |
| Add `confidence_note` field to SC metric-audit artifact | **YES (non-amending)** | Per §2 observation above. No PRD text change required — this is a field added to the metric-audit JSON schema, which SC owns. COO coordinates with SC on schema update in Wave 3b dispatch. |
| Control for `unaided_prior_sphinx_exposure`-class confounds in Wave 3b | **YES (non-amending)** | Wave 3b dispatch TOs must specify "DS serial must have no prior task-repo exposure in current session history" OR explicitly flag the confound in the verdict file. |

---

## 4. Stage 2 Wave Counter (per PRD §7)

**CTO ruling — confirms COO's read:** Wave 3a contributes exactly **1 clean Stage 2 wave** toward the 2-wave exit criterion.

| Source | Qualifies | Rationale |
|--------|-----------|-----------|
| Lane B (`.051` Case 3 two-phase scoring) | **YES — 1 clean wave** | Phase 1 verdict freeze at `4e1ec449` BEFORE Phase 2 metric work; `reasoning.md` mechanically excluded; nav_log hygiene confirmed (0 comp_call unaided / 7 comp_call aided); no cross-condition contamination; §3.8 preflight gate executed clean on `.050` unaided dispatch. |
| Lane A (`.048` dev-4 loop) | **NO** | Measurement invalidated before scoring contact. Self-authored bundle (finding 1), absent canonical source (finding 2), and self-assessed primary_metric do not satisfy Stage 2 "clean execution + valid measurement" requirement. Does not contribute even partial credit. |

**Wave 3a total: 1 / 2 clean waves.**

**Wave 3b must contribute ≥1 additional clean wave to satisfy §7 exit criterion.** Any of Cases 1+2 reruns qualifies if it passes §3.8 preflight gates + §0.6 clean state verification + SC two-phase scoring. Lane A rebuild also qualifies if it produces a valid measurement under §2.0 preconditions — regardless of KEEP/DISCARD/TIED verdict, a valid run counts toward the wave count.

---

## 5. Go / No-Go Triggers for Wave 3b Kickoff

### Wave 3b is GO when ALL of these are true

**Lane B track (Cases 1+2 reruns):**
1. COO has authored Wave 3b rerun TOs for Case 1 and Case 2
2. Each TO's phase-0 compiler_tools_mandate block contains §3.8 preflight gates inlined verbatim
3. Each TO cites the §0.6 "clean" definition as the gate standard
4. DS assignment controls for the prior-exposure confound (see §3 table above)
5. Packet files for Cases 1+2 exist at `comp/tasks/case-00{1,2}-*/packet.yaml` and point to valid `baseline_commit` values

**Lane A track (dev-4 rebuild):**
1. COO has authored Lane A rebuild TO
2. Packet backfill TO or inline packet-update: `scorer.serial` / `scorer.mode` / `scorer.artifact_location` fields present in `comp/backlog/dev/dev-click-001.yaml` (and other `dev-*.yaml` if parallel)
3. Scorer serial ≠ compiler mutation author serial (§2.0 Precondition 2 enforcement)
4. `comp/targets/click/_repo/` provisioned at `f80cf4b0` (§2.0 Precondition 1)
5. Phase-0 packet gate validates §0.6 clean state AND §2.0 precondition 2
6. Budget raised to 6-8 hours per my §1 recommendation (or COO justifies otherwise)

### Wave 3b is NO-GO if ANY of these are true

- Post-hoc integrity finding on `.050` or `.051` surfaces (e.g., nav_log manipulation, confound not previously disclosed, freeze commit tampered)
- Fresh Rule 7 pre-flag on any Wave 3b TO requires another PRD amendment
- Andrew redirects (cancels project, changes scope, pauses research track)
- Lane B Case 1 or Case 2 task packet is found to be missing, corrupted, or pointing to an irretrievable `baseline_commit`

### Wave 3b DOES NOT BEGIN until

- This decision document is committed and `.053` is flipped to complete (joint — both exec commits)
- COO updates `org/projects/COMP_LEARNS.json` `phase` and `blocking` fields per the new state (closure step of `.053`; COO's authorship)
- COO-authored Wave 3b dispatch TOs are in `staged` status awaiting Andrew-facing GO OR COO-facing GO per normal dispatch protocol

---

## 6. Items Explicitly OUT of Wave 3b Scope

- Wave 4 parallel expansion (loop farming, multi-agent parallel runs)
- Cross-model DS variation (non-`claude-sonnet-4-6` agents)
- Statistical-significance claims on any dimension
- Archetype A/C/E breadth expansion
- Mutation-family effectiveness ranking (requires valid Lane A data first)
- PRD amendment for `confidence_note` — it's a metric-audit field addition, not a PRD text change; SC owns the schema

---

## 7. Authority Notes

- This decision is authoritative for Wave 3b scope under my CTO seat.
- COO's read of Stage 2 wave count (1/2) is confirmed verbatim above.
- Andrew may override any item above; he is on the escalation path via the five-triggers rule if anything in §5 changes.
- Base CTO (`1.0.0_SA_CTO`) is NOT in this decision chain except for closure-mechanical REGISTRY coordination if Wave 3b later completes the project.

---

## 8. RAVC + Joint Closure

Per `.053` closeout section:

- **CTO commit (this file):** under `--author=1.1.0_SA_CTO`, `--only` pathspec, pushed to CLOUD
- **COO deliverable:** `comp/results/wave-3a/coo-review-memo.md` at `8bf465d9` — already shipped
- **COO remaining:** update `org/projects/COMP_LEARNS.json` `phase` + `blocking` fields; flip `.053` status to complete (joint — requires both exec commits); joint MCP to Andrew with Wave 3a closure + Wave 3b trigger summary

`.053` closure completes atomically when COO's JSON update commit lands after this file.
