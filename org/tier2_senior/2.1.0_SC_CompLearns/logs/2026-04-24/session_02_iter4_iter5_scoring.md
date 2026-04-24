# Session Log — 2.1.0_SC_CompLearns — 2026-04-24 — Iter-4 + Iter-5 Scoring

**Session:** 02
**TOs active:** COMP_LEARNS.060 (scorer role, no assigned TO — responding to COO/DS relay)
**Worktree:** feature_clb (`/c/Users/AndrewBerman/Desktop/feature_clb/`)
**Session scope:** Score iter-4 and iter-5 click dev-loop mutations. Emit CTO watch-item diagnostic.

---

## Orientation

Resumed from session 01 baseline. Prior state:
- All 4 assigned TOs (029, 030, 031, 032) complete
- COMP_LEARNS.060 click dev loop active: iters 1 (INVALIDATED), 2-3 (DISCARDED), champion at 0.1180 (v0 baseline, sha 7beb09b)
- Schema v3 live (COMP_LEARNS.063 completed by DS: compiler_content_sha / git_commit_sha split, human_iter_label / ratchet_iter_effective)
- feature_clb HEAD at d2cf4c7b on session start

---

## What I Did

### Iter-4 Scoring

**Bundle received:** Direct MCP from 1.1.0_DS_CompLearns (iter-4 GO, compiler_content_sha=01f7b504)
**Mutation:** module_name/class_name vocab alignment — added explicit module nodes with module_name + name attrs, added class_name to class_inherits edges, removed canonical_file from all edges

**Run:** `comp-learns-ratchet click --judge real --max-iter 1 --compiler-content-sha 01f7b504` from feature_clb
**Duration:** 24 minutes (33 fresh LLM calls — anomalous; likely API throttling)
**Exit:** MAX_ITER (10) — expected

**Scorecard (fe29f58_d869779f.json):**
- primary_metric: 0.0 / ab_lift: 0.0 (all selectors)
- structural_f1: 0.655, mutation_stability: 0.858, token_reduction: 0.958
- compiler_loc: 153
- tied_at_best: true (centrality/keyword/random all at 0.0)

**Verdict:** DISCARD. Committed `857b7f63` (result.json at comp/dev-bundles/dev-click-001/iter-4/).

**Root cause:** canonical_file removed in v4 → keyword selector cannot identify source-file attribution for q01/q02. Additionally, q05-q08 require method-level analysis not in any import/class edge type.

**Recommendation to DS:** Restore source_file attribute (filename only, e.g., 'core.py') on import + class_inherits edges.

---

### CTO Watch-Item — Per-Selector Protocol Established

COO relayed CTO watch-item: iter-5 retrospective must include per-selector lift breakdown to identify which of three patterns materializes (A=clean root cause, B=keyword index node-only, C=fix doesn't reach selector layer).

Confirmed protocol: will report keyword/centrality/random individually + explicit pattern conclusion.

---

### Iter-5 Scoring

**Bundle received:** COO relay — 1.3.0_DS commit e0094c00
**Mutation:** source_file=path.name on import + class_inherits edges (LOC 156, +3 from iter-4)
**ds-commit-gate:** PASS per commit message

**Run:** `comp-learns-ratchet click --judge real --max-iter 1 --compiler-content-sha e0094c00` from feature_clb
**Duration:** 1:55 (33 fresh LLM calls — fast API, no throttling)
**Exit:** MAX_ITER (10) — expected

**Scorecard (2249bbb_d869779f.json) — CTO watch-item per-selector:**

| Selector   | lift | token_reduction | cache_hit_rate |
|------------|------|-----------------|----------------|
| centrality | 0.0  | 0.958           | 1.0            |
| keyword    | 0.0  | 0.961           | 1.0            |
| random     | 0.0  | 0.958           | 1.0            |

- primary_metric: 0.0 / structural_f1: 0.655 / mutation_stability: 0.858
- tied_at_best: true, random_unique_win: false

**PATTERN: C** — all three selectors flat. Source_file attribute present but transparent to selector layer and judge outcomes. Every scoring metric IDENTICAL to iter-4 within measurement precision.

**Verdict:** DISCARD. Committed `0aeab57d` (result.json at comp/dev-bundles/dev-click-001/iter-5/).

**Three hypotheses logged in result.json:**
- H1: keyword selector indexes node attributes only, not edge attributes
- H2: context format mismatch — graph edges serialized as machine objects, not natural-language import lists
- H3: judge already answers most questions correctly from full source → no lift opportunity

---

## Family Plateau Assessment

Import/class_inherits mutation family — iters 2-5:

| Iter | LOC | ab_lift | struct_F1 | mut_stability | pattern |
|------|-----|---------|-----------|---------------|---------|
| 2 | 409 | 0.0909 (random only) | 0.651 | 0.852 | graph-size luck |
| 3 | 240 | 0.0 | 0.655 | 0.858 | graph pruned, surface lost |
| 4 | 153 | 0.0 | 0.655 | 0.858 | vocab fix, no file attribution |
| 5 | 156 | 0.0 | 0.655 | 0.858 | PATTERN C |

4 consecutive DISCARDs with ab_lift=0.0 (iters 3-5 identical structural metrics). Family ceiling confirmed. Escalated to COO/CTO with Options A-D.

---

## Compiler Tools

| Tool | Status | Result |
|------|--------|--------|
| `comp-learns-ratchet click --status` | N/A — ran full scoring | — |
| Manual scorecard read | DONE | Per-selector data extracted for both iters |
| Manual experiment_log read | DONE | Schema v3 field verification |
| `comp-pipescript io` | N/A — SC role, no gold script edits | — |
| `comp-blast` | N/A — no code files modified by SC | — |

SC role: compiler tools mandate satisfied by scorecard analysis and manual code inspection.

---

## Commits This Session

| SHA | Author | Description |
|-----|--------|-------------|
| 857b7f63 | 2.1.0_SC_CompLearns | score(COMP_LEARNS.060): click iter-4 DISCARD |
| 0aeab57d | 2.1.0_SC_CompLearns | score(COMP_LEARNS.060): click iter-5 DISCARD PATTERN C |

Both pushed to CLOUD via feature_clb.

---

## MCP Activity

| Direction | To/From | Subject |
|-----------|---------|---------|
| SEND | 1.1.0_DS | RAVC ACK iter-4 bundle received |
| SEND | 1.1.0_DS | RAVC CLOSE iter-4 DISCARD verdict |
| SEND | 2.0.0_SA_COO | iter-4 DISCARD + diagnostic |
| RECV | 2.0.0_SA_COO | iter-5 watch-item protocol |
| SEND | 2.0.0_SA_COO | RAVC ACK iter-5 watch-item |
| RECV | 2.0.0_SA_COO | iter-5 SCORE relay (e0094c00) |
| SEND | 2.0.0_SA_COO | RAVC ACK iter-5 scoring start |
| SEND | 2.0.0_SA_COO | RAVC CLOSE iter-5 DISCARD PATTERN C + Options A-D |
| RECV | 2.0.0_SA_COO | RAVC ACK, strategy forwarded to CTO |

---

## Status

Awaiting CTO strategy direction on which option (A/B/C/D) to commission for iter-6+.
No pending TOs. No blockers. Inbox empty. Watcher live (b8imze508).
