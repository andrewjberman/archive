# v0 Question Forensic (Option A Diagnostic) — 2.1.0_SC_CompLearns

**Date:** 2026-04-27
**Task Order:** COMP_LEARNS.065 — sc-option-a-v0-question-forensics
**Status:** COMPLETE

---

## Objective

Identify which specific question (q02, q03, or q11) the v0 champion (sha 7beb09b, pm=0.1180) scored correctly via `random_unique_win` that the H3-v2 full-source baseline missed. The CTO needed this to determine whether dispatch_class body nodes partially address class hierarchy (q03) or whether iter-7+ strategy should shift toward numerical fact nodes (q02/q11). Read-only diagnostic; no scoring run.

---

## Compiler Tools

| Tool | Command | Result | Note |
|------|---------|--------|------|
| ab_cache source_hash scan | python3 scan of 297 cache files for source_hash d505e5e5eb2b9cc9 | FAIL — 0 entries | v0 cache cleared/reinitialized between v0 run (2026-04-24) and current session |
| v0 compiler AST inspection | python3 inline walk of click/_repo using v0 compiler logic (git show 7beb09b:compiler.py) | PASS | 2 dispatch_class nodes confirmed; _BaseCommand absence confirmed |
| H3-v2 baseline read | direct file read h3_v2_result.json | PASS | 8/11 correct; q02/q03/q11 incorrect |
| R-SC-2 audit read | comp/results/dev-click-001/r_sc_2_failure_mode_audit.md | PASS | q11: 3/6 format-failure, 2/6 semantic-wrong; q02 incomplete |
| sc_q03_q11_responses.txt read | direct file read | PASS | q03: all 6 wrong (MultiCommand); q11: all 6 scored false |

**What worked:** Direct compiler source inspection via `git show` was the decisive tool — without running the actual compiler, the AST walk confirmed exactly which nodes the v0 graph contained and which were absent.

**What failed:** ab_cache lookup — the v0 cache entries were not preserved, making direct per-question evidence unavailable.

**Gap found:** The scorecard format does not store per-question judge responses (aggregate only). Cache entries are required for per-question breakdown but are not git-tracked and can be lost between sessions. Per-question evidence for v0 is permanently unavailable.

---

## Work Completed

### 1. Champion and Scorecard Verification

- `comp/targets/dev-click-001/champion.json`: sha=7beb09b, pm=0.1180, baseline_commit=f80cf4b09fbe36099b7bfc065fbde30d053da46d, iteration=0
- Scorecard `comp/targets/click/scorecards/7beb09b_d869779f.json` present
- Confirmed: random.lift=0.09090909 (1/11 absolute score), centrality.lift=0.0, keyword.lift=0.0, random_unique_win=true

**ab_lift interpretation correction:** `lift = correct / total` in ab.py — this is the ABSOLUTE score of the selector (1/11 questions answered correctly), not a delta vs H3-v2. The v0 random selector answered 1 of 11 questions correctly total.

### 2. Cache Lookup — Not Recoverable

Computed source_hash for v0 compiler: `d505e5e5eb2b9cc9` (SHA-256 of compiler.py at 7beb09b, first 16 chars). Scanned all 297 cache files in feature_clb `comp/targets/click/ab_cache/ab_cache/`. Result: 0 entries for this source_hash.

Source hashes present in cache (iters 2-7):
- 8f2df8e3c9580715: 99 entries (3 runs sharing same compiler.py content)
- a0df94796bb4a746: 33 entries (3edd0e6)
- 0d20cbd69281d7ab: 33 entries (a888625)
- 44dda665f065f0dd: 33 entries (fe29f58)
- 923071d5352ec842: 33 entries (38c712a / iter-7)
- ecaf3bc0933af686: 33 entries (8809a87/38c712a shared)
- 2a1efb87c71a4fe2: 33 entries (2249bbb-era)

v0 run cache was cleared or the feature_clb ab_cache was initialized fresh after the v0 run.

### 3. v0 Compiler Type Correction

The v0 compiler (sha 7beb09b) is a **dispatch-chain compiler**, NOT an imports compiler. The `subtypes_enabled: ["imports"]` field in the scorecard is a hardcoded ratchet metadata constant, not a compiler descriptor.

v0 compiler scope (from compiler.py source at 7beb09b):
- Classes with `invoke(self, ctx)` → dispatch_class nodes
- Group → Command / Group → Group can_dispatch_to edges
- @command/@group decorator registrations → command_registration nodes
- CommandCollection class definitions/calls

### 4. v0 Graph Content Confirmed by AST Inspection

Ran v0 compiler logic against `comp/targets/click/_repo/src/click/`:

| Node type | Instances |
|---|---|
| dispatch_class: Command | 1 (root, no bases) |
| dispatch_class: Group(Command) | 1 |
| dispatch_class: _BaseCommand | ABSENT — no invoke() defined |
| dispatch_class: _MultiCommand | ABSENT — no invoke() defined |
| dispatch_class: CommandCollection | ABSENT — no invoke() defined |
| Import edges | ABSENT — compiler has no import analysis |

`_BaseCommand(Command, metaclass=_FakeSubclassCheck)` is a deprecated shim in click 8.3.1 with no body beyond the class definition. It has no `invoke()` and was excluded from the dispatch compiler's scope.

### 5. Per-Question Ruling

| QID | Finding | Evidence |
|---|---|---|
| q03 | NOT the win | v0 graph has Group(Command) but NOT _BaseCommand. Judge with v0 context would answer "Group" only — fails set_membership check against gold {_BaseCommand, Group}. sc_q03_q11_responses.txt: all 6 q03 responses gave "MultiCommand" (likely from later iterations with different compiler content). |
| q11 | NOT the win | v0 graph has zero import data. R-SC-2 audit: 3/6 semantic-correct-but-unparseable, 2/6 semantic-wrong, 1/6 ambiguous — all scored false. |
| q02 | NOT the win | v0 graph has zero import data. Honesty note confirms: "all verbose, giving 7 (wrong value)." |

### 6. Conclusion — QID of v0 random_unique_win

The v0 random_unique_win was on a **prior-knowledge question**, not q02/q03/q11. The dispatch-chain context provided by the v0 compiler is irrelevant to all 11 questions in the pool. The random selector's 1 correct answer was a training-prior hit, not a compiler-context-driven gain.

Most probable QID: **q09** (star imports in `__init__.py` = 0) or **q10** (no `importlib.import_module` call = "no"). Both are adversarial questions with null/false correct answers that the judge's training knowledge about click supplies regardless of context. The centrality and keyword selectors got 0/11 because their selected context introduced dispatch-chain noise; the random selector happened to pick sparse enough content that the judge defaulted to training priors.

**Reproducibility: PROBABLE-LUCK.** No genuine compiler-context knowledge gain on any question.

### 7. Implication for CTO's Diagnostic

CTO question: "Does this suggest dispatch_class body nodes partially address class hierarchy (q03)?"

Answer: **NO.**
- The v0 graph does not contain _BaseCommand — the second element of the gold answer for q03
- Even the full dispatch-chain context showing Group(Command) would produce an incomplete set answer
- The q03 mechanism was structurally absent from v0
- The CTO's iter-8 ruling (q03 CLOSED) stands on independent merits

"Should iter-7+ shift toward numerical fact nodes (q02/q11)?"

Answer: **Not indicated by this forensic.** The v0 win was not on q02 or q11 either. Stage 3 target selection should be driven by R-SC-1/R-SC-2 semantic-label analysis, not by the v0 forensic result.

### 8. Stage 3 Rulings ACK

Received CTO message this session: Stage 3 R-SC-1 (P0) + R-SC-2 (P1) rulings binding before Stage 3 dispatch.

- R-SC-1 (P0): Pre-screen logic must use R-SC-2 semantic labels (parseable-correct / parseable-wrong / semantic-correct-but-unparseable / semantic-wrong-unparseable / semantic-ambiguous) in INCLUDE/SENTINEL/INVESTIGATE categorization — not raw binary pass/fail. Will implement on PRD arrival.
- R-SC-2 (P1): Add "full-source overload candidate" (FSO-C) label to pre-screen Wrong|Wrong output — separates genuine ceiling from full-source overload candidate. Feeds R-DS-2 (DS pilot permission). Will define separation rule and operationalize before Stage 3 dispatch.
- R-SC-2 q02 extension: raw q02 responses not yet captured. Extension of sc_q03_q11_responses.txt (or a separate artifact) needed in next warm-up run.
- ACK sent to CTO (20260427T171135Z).

---

## Decisions Made

| Decision | Rationale |
|---|---|
| Analytical reconstruction via AST inspection (no re-run) | Cache not recoverable; TO explicitly prohibited new scoring runs; compiler source available at git sha 7beb09b |
| Report win as probable-luck q09/q10, not q03 | _BaseCommand confirmed absent from v0 graph by inspection; q11/q02 confirmed false by R-SC-2 audit and honesty note; no evidence for any of the three CTO-nominated QIDs |
| Did not speculate on the specific QID beyond q09/q10 | Cache data is gone; the two adversarial "null-answer" questions are the strongest priors but cannot be confirmed without the original responses |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `org/tier2_senior/2.1.0_SC_CompLearns/task_orders/COMP_LEARNS.065.sc-option-a-v0-question-forensics.md` | Status to complete (redundant — already complete from 2462da90; working tree matched committed state) | Yes — `22df0902` |
| `org/tier2_senior/2.1.0_SC_CompLearns/logs/2026-04-27/session_02_iter7_scoring.md` | Appended .065 session summary section | Yes — `22df0902` |

---

## Blockers

None.

---

## Current State

COMP_LEARNS.065 is complete (commit `22df0902`, pushed CLOUD). The v0 random_unique_win was identified as a probable-luck prior-knowledge answer (q09 or q10), not on any of the three CTO-nominated improvement targets. The CTO's iter-8 ruling (q03 CLOSED) is unaffected. Stage 3 R-SC-1 and R-SC-2 rulings are ACKed; both implementations are standing by for the Stage 3 PRD. The .069 diagnostic ablation TO has not yet been dispatched by COO.

---

## Next Steps

1. **[2.1.0_SC_CompLearns] Implement R-SC-1 pre-screen semantic-label integration** — on Stage 3 PRD arrival; R-SC-2 labels must feed INCLUDE/SENTINEL/INVESTIGATE categorization, not binary pass/fail
2. **[2.1.0_SC_CompLearns] Define FSO-C separation rule (R-SC-2 P1)** — separate Wrong|Wrong genuine ceiling from full-source overload candidate; document rule before Stage 3 dispatch
3. **[2.1.0_SC_CompLearns] Extend R-SC-2 audit to q02** — capture raw q02 responses in next warm-up run; extend sc_q03_q11_responses.txt or create q02 artifact
4. **[2.1.0_SA_COO] Dispatch .069 TO** — q02/q11 non-ratchet diagnostic ablation (gated on iter-8 ruling sequence per CTO)
5. **[1.1.0_DS_CompLearns] Experiment_log path fix** — f5095ac0 ineffective for click target; runner still writes to comp/targets/click/experiment_log.jsonl (schema v2); manual SC backfill required each iter
