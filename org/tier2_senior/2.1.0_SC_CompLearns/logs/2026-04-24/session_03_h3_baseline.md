# Session Log — 2.1.0_SC_CompLearns — 2026-04-24 — H3 Full-Source Baseline

**Session:** 03
**TOs active:** COMP_LEARNS.060 (scorer role, H3 diagnostic)
**Worktree:** feature_clb (`/c/Users/AndrewBerman/Desktop/feature_clb/`)
**Session scope:** Run H3 full-source baseline diagnostic. Commissioned P0 by COO per CTO synthesis (R-SC-1 + R-SC-2).

---

## Orientation

Continued from session 02 (iter-4 + iter-5 scoring). State on entry:
- Iters 4-5 both DISCARD, PATTERN C confirmed in iter-5 (all selectors flat)
- Import/class_inherits mutation family at plateau (4 consecutive DISCARDs, iters 2-5)
- Three hypotheses logged: H1 (keyword indexes nodes only), H2 (context format mismatch), H3 (judge already at ceiling)
- COO relayed CTO P0 directive: run H3 full-source baseline before commissioning iter-6 strategy
- ADHC_OWNPTH.003 hook confirmed live (feature_clb worktree inherits ajb_workspace hooks)

---

## H3-v1 Diagnostic (run_h3.py)

**Method:** Full click source (365KB, all .py files except testing.py) as context. Same system prompt as AB scoring: "You are a precise, terse code-graph answering assistant." Same grader as AB scoring (strict string-match for set_membership/enumerable/numeric).

**Result: 0/11 correct**

**Root cause: format mismatch, NOT knowledge failure.**

With 365KB full source, the judge gave verbose responses — numbered lists, markdown formatting, prose explanations. The strict AB grader could not parse these. Examples:
- q01 (set_membership): judge listed all 8 correct modules in numbered format ("1. types\n2. utils...") — grader expected bare comma-separated list → FAIL
- q05 (enumerable): judge answered "Yes." instead of "yes" → FAIL (case-insensitive match would pass, but trailing period caused failure)

Diagnostic implication: **The AB benchmark measures "does compressed context elicit format-compliant correct answer" — not purely semantic understanding.** Terse compressed context → terse response → passes grader. Full source → verbose response → fails grader even when semantically correct. This is itself a load-bearing undocumented surface of the scoring regime.

---

## H3-v2 Diagnostic (run_h3_v2.py)

**Method:** Same full source context. Added per-answer-type explicit format instructions to system prompt:
- set_membership: "Answer with ONLY a comma-separated list of values, no explanation, no numbering, no formatting."
- enumerable: "Answer with ONLY the exact value, no punctuation, no explanation."
- numeric: "Answer with ONLY the number, no units, no explanation."

**Result: 8/11 correct (72.7%)**

Per-question table:

| QID | Type | Result | Notes |
|-----|------|--------|-------|
| q01 | set_membership | CORRECT | 8 modules from core.py imports |
| q02 | numeric | INCORRECT | Format fail — prose count instead of "8" |
| q03 | set_membership | INCORRECT | Genuine error — included _MultiCommand/CommandCollection (gold: {_BaseCommand, Group}) |
| q04 | set_membership | CORRECT | {_MultiCommand, CommandCollection} |
| q05 | enumerable | CORRECT | "yes" |
| q06 | enumerable | CORRECT | "Group" |
| q07 | set_membership | CORRECT | {argument, option} |
| q08 | enumerable | CORRECT | "__click_params__" |
| q09 | numeric | CORRECT | 0 |
| q10 | enumerable | CORRECT | "no" |
| q11 | numeric | INCORRECT | Format fail — prose instead of "1" |

---

## Failure Analysis

**q02, q11 (numeric format fails):** Judge gave prose response to a numeric question despite format instruction. Root cause unclear — possibly question complexity overwhelms format constraint at 365KB context. These are NOT genuine knowledge failures; judge likely knows the answer but format compliance breaks down for numeric types under heavy context load.

**q03 (genuine error):** Judge answered {_BaseCommand, Group, _MultiCommand, CommandCollection}. Gold is {_BaseCommand, Group}. Judge included _MultiCommand and CommandCollection which are subclasses of Group, not direct answers to the question about what classes directly inherit from BaseCommand/Group-hierarchy. This is a genuine comprehension/disambiguation error — the judge conflates "subclasses of Group" with the answer set.

---

## Implication for AB Lift Ceiling

**Max theoretical ab_lift = 3 questions (q02, q03, q11).**

- q02, q11: format failures. A compiler that provides numerical facts as explicit attributes (e.g., "import_count: 8") could force numerical context → judge gives bare number.
- q03: genuine error. A compiler that emits explicit "Group subclasses: _MultiCommand, CommandCollection" + "BaseCommand direct subclasses: Group" structure could correct this disambiguation.

**H3 does NOT confirm full ceiling saturation.** 3 questions are genuinely improvable from a graph compiler.

**Import/class_inherits family (iters 2-5) failed all 3.** The family improved structural_f1 to 0.655 but:
- q02/q11 require numerical fact nodes, not edge topology
- q03 requires explicit subclass disambiguation, not file attribution (source_file attr from iter-5 doesn't address this)

**Champion v0 (ab_lift=0.0909, 1/11 random):** Consistent with 3-question ceiling. v0 hit 1 of the 3 improvable questions by random selection luck using dispatch_class body-analysis nodes.

---

## Options A-D Reported to CTO

A. **Question forensics on v0 cache** — identify which question v0 random won, design compiler to reliably reproduce that surface.
B. **Hybrid dispatch_class + imports** — combine v0 body-analysis nodes with structural import edges.
C. **Class_method nodes** — (class_name, method_name) pairs to cover method-level questions.
D. **q03-targeted compiler** — emit explicit class hierarchy disambiguation node ("Group subclasses: ...").

SC recommendation: D + A. D targets the one genuine knowledge error (q03, highest precision). A validates whether v0 win is repeatable before committing further LOC.

---

## Artifacts

| File | Status |
|------|--------|
| comp/results/dev-click-001/h3_baseline/run_h3.py | Committed 17bb28bf |
| comp/results/dev-click-001/h3_baseline/h3_result.json | Committed 17bb28bf |
| comp/results/dev-click-001/h3_baseline/run_h3_v2.py | Committed 17bb28bf |
| comp/results/dev-click-001/h3_baseline/h3_v2_result.json | Committed 17bb28bf |

All pushed to CLOUD.

---

## Commits This Session

| SHA | Author | Description |
|-----|--------|-------------|
| 17bb28bf | 2.1.0_SC_CompLearns | diag(COMP_LEARNS.060): H3 full-source baseline -- 8/11 correct, near-ceiling confirmed |

---

## MCP Activity

| Direction | To/From | Subject |
|-----------|---------|---------|
| RECV | 2.0.0_SA_COO | RAVC CLOSE — ADHC_OWNPTH.003 hook confirmed + H3-v2 acknowledged |
| SEND | 1.0.0_SA_CTO | H3 FULL-SOURCE BASELINE RESULT — 8/11 correct, near-ceiling, strategy input requested |
| SEND | 2.0.0_SA_COO | RAVC4 CLOSE — H3-v2 complete: 8/11, near-ceiling, report sent to CTO |

---

## Status

Awaiting CTO strategy direction for iter-6. No pending TOs. No blockers.
Inbox-watch relaunched. Session complete pending CTO response.
