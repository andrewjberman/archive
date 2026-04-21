# 1.1.0_SA_CTO Session 04 — Target Close-Out Playbook v2.0 (process-feedback trim pass)

**Date:** 2026-04-21 (Tue, PM ET — third revision same session)
**Agent:** 1.1.0_SA_CTO
**Scope:** Andrew forwarded a process-feedback pass on the full operating model (not just PRD content). Feedback identified that v1.0/v1.1 of the Target Close-Out PRD over-engineered — specifying a subsystem for a ritual that has never been performed. This session trims to v2.0: drop the subsystem, keep only housekeeping that maps to named prior failures. Also codifies the process principles in memory so the lesson carries forward.

---

## Objective

Correct the over-engineering. v1.0 and v1.1 shipped a close-out subsystem (`comp/framework/closeout/` module + `classify()` + `promote()` + 4-artifact ritual + 3-part Justification + 2 new TOs `.023`/`.024`) before target 1 had run through the ratchet loop once. That is the study-gate failure mode. Feedback landed; trim to a convention.

Target outcome: PRD at v2.0 (lightweight convention), `.023`/`.024` withdrawn, `.018` scope reverted to plain-markdown section, memory file codifying the five process principles, session log with compiler tools.

---

## Work Completed

### Feedback → action mapping

| Feedback | Response |
|----------|----------|
| "The close-out ritual is too ceremonious for the current maturity" | v1.1 §4 (4 artifacts + joint-signoff) collapsed to v2.0 §2.2 (3-artifact convention: exit note + candidate learnings inline + next-target memo if proceeding) |
| "Probably need a lightweight exit note + candidate learnings + next-target memo, not a formal close-out subsystem" | Exactly what v2.0 is. No `comp/framework/closeout/` module, no `classify()`, no `promote()`, no named-exception machinery. Human-readable convention. |
| "Keep rules only if they map to a named prior failure" | Kept: `.015` gold-survey AC (v4 6/6-coverage bug), `.015a` inline (small-by-default), §5 target-2 hard minimums (scope-creep / rationalization / self-referential bias). Dropped: precedence rule (no incident), 3-part Justification (no incident), classifier tie-breaks (no incident). |
| "One authoritative artifact per question" | Dropped separate `PROMOTION_CANDIDATES.md` template file (already done in v1.1); drop classify_result.json as distinct artifact (folded into exit note narrative in v2.0); drop joint-signoff commit ceremony entirely (was already advisory in v1.1). |
| "Delay formalization until second recurrence" | Saved as `memory/feedback_delay_formalization_until_second_recurrence.md`. Codified as the general principle governing my future PRD authoring. |
| "Small inline by default" | `.015a` inline confirmed (v1.0 already had this). `.023`/`.024` withdrawn. `.018` 9th-item format-comment requirement reverted to plain markdown section. |
| "Separate control-plane rigor from content-plane rigor" | Kept control-plane rigor (Rule 7 pre-flags, dispatch correctness, pre-commit gate for Python, A→D-sensitive S3 pre-flags). Loosened content-plane rigor (archival ceremony, document taxonomy, close-out schema). |
| "The study-gate instinct can overshoot" | Parked in memory as an anti-pattern to watch for in my own drafts. v2.0 PRD explicitly cites this as the v1.0/v1.1 failure mode. |

### PRD rewrite — v2.0

`docs/architecture/COMP_LEARNS_TARGET_CLOSEOUT.md` rewritten top-to-bottom. Line count 431 → 218 (-50%).

**What's gone:**
- §2.1 classifier precedence rule + tie-break logic (specified a `classify()` function that no longer exists).
- §3 3-part Justification block form + §3.1 uniqueness rule + `PromotedLearningMissingJustification` exception (specified schema for a `promote()` function that no longer exists; first close-out hasn't happened, don't know the right structure yet).
- §4 4-artifact ritual (replaced with 3-item convention in new §2.2).
- §6 module boundary (`comp/framework/closeout/` + 7 sub-files).
- §8.1 `.023` triad compiler mandate + §8.2 `.024` triad (TOs withdrawn).
- §8.3 `.015` AC text authoritative-in-PRD (AC remains in `.015` TO itself; PRD no longer duplicates).

**What's preserved (each maps to a named prior failure or is already-shipped mechanical cleanup):**
- `.015` AC #7 gold-survey-attestation 5 fixtures — guards the v4 6/6-coverage bug caught during `.016` gold authoring. Real incident, real guard.
- `.015a` inline-into-`.015` decision — small-by-default per validator feedback pattern.
- `.009` / `.018` / `.020` ownership transfers — mechanical, already-committed in `0fab133f`.
- §5 target-2 hard minimums + disqualifiers — parser-proven maps to scope-creep; gold-authorable maps to rationalization; disqualifiers map to metaprogramming / LLM-swap / self-referential bias failure modes. Each has a named class.
- §5 weights (subtype leverage + size ceiling) — retained as tiebreakers for qualifying candidates only.

**New §6 "What we're not formalizing yet":** explicit table of 7 deferred items with revisit-when criteria. Makes the deferral auditable; future me (or a future close-out) can find the ledger of what was considered and why it was set aside.

**New §10 revision record:** tracks v1.0 → v1.1 → v2.0 commits with scope notes + explicit "supersession is by design." The learning arc is preserved in the PRD itself.

### `.018` TO scope revert

9th item previously required a format-comment inline with the 3-part Justification block and cited §3.1 uniqueness. v2.0: the 9th item requires only a plain `## Promoted Learnings` section heading + one-line comment pointing future CTOs at `TARGET_CLOSEOUT §4` for the informal convention. No format-enforcement, no code dependency. Phase 2 compiler mandate step correspondingly relaxed — literal-string match is sufficient.

### Reference bumps

- `.009` TO — reference row → v2.0. AC #7 "gate evidence cited" updated to reflect §5 CTO-judgment uniqueness (not the §3.1 code-enforced rule that no longer exists).
- `.015` TO — reference row → v2.0 (no AC change; AC #7 fixtures unchanged).
- `.020` TO — reference comment → v2.0 (no-op; v2.0 doesn't touch selectors).
- `COMP_LEARNS.json` — `prds[]` label rewritten; `phase` narrative extends with v2.0 trim + withdrawal of `.023`/`.024`; `blocking` row (6) marked RESOLVED and rewrites from "pending decomposition" to "WITHDRAWN — subsystem formalization deferred."

### Memory codification

Written `memory/feedback_delay_formalization_until_second_recurrence.md`. Captures:
- The governing principle (rules map to named prior failures).
- Five mechanisms (prior-failure test, one-artifact-per-question, delay-to-second-recurrence, small-inline-by-default, control-plane vs content-plane rigor split).
- Earned-their-keep list (ground-truth recon, Rule 7, operator+validator, narrow safety rules).
- Anti-patterns list (study-gate overshoot, evidence multiplication, eager TO decomposition, subsystem scaffolding for unused rituals).
- Reference commits (v1.0/v1.1/v2.0 of this PRD as the case study).

Indexed in `MEMORY.md` at the bottom of the Feedback section (line 224).

---

## Decisions Made

1. **Ship as v2.0, not v1.2.** The trim is large enough that it is a supersession, not a patch. v1.0 and v1.1 specified a subsystem; v2.0 specifies a convention. Semver-ish major bump reflects the scope shift.
2. **Preserve the v1.0 → v1.1 → v2.0 record in the PRD.** Future readers see the learning arc: started with a subsystem, external review flagged the over-engineering, corrected the same day. Deleting the revision history would erase the lesson.
3. **Keep `.015` AC #7 unchanged.** It is the one piece of v1.0/v1.1 that unambiguously maps to a named prior failure. Trimming it would be trimming the wrong thing.
4. **Withdraw `.023` + `.024` instead of parking them.** If I park them as "pending future decomposition," they sit in `blocking` as a visible obligation. Withdrawing them cleanly removes the obligation; if the second close-out needs them, they can be re-authored at that point against whatever has actually been learned.
5. **Codify the principles in memory, not in `prompt.md`.** `prompt.md` is role persona; these principles are cross-cutting operating heuristics and belong in the feedback memory that loads on every session start. Per existing pattern (e.g., `feedback_cto_compiler_mandatory_before_prd.md`).
6. **Do not send the v2.0 PRD back to the codex validator.** The changes are trimming and mechanical alignment, not new content. A third validator pass would likely pattern-match on "is this lightweight enough?" and I've already internalized the answer from the feedback itself.

---

## Files Modified

Edited:
- `docs/architecture/COMP_LEARNS_TARGET_CLOSEOUT.md` — rewritten to v2.0. Line count 431 → 218 (-50%).
- `org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.018.cto-program-md-v1.md` — reference → v2.0; 9th-item scope reverted to plain markdown section; Phase 2 mandate relaxed.
- `org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.009.cto-target-2-selection.md` — reference → v2.0; AC #7 updated to v2.0 §5 phrasing.
- `org/tier2_senior/1.4.0_DS_CompLearns/task_orders/COMP_LEARNS.015.bench-scorecard-ab.md` — reference → v2.0 (no AC change).
- `org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.020.cto-selector-benchmarking-harness.md` — reference comment → v2.0.
- `org/projects/COMP_LEARNS.json` — `prds[]` label, `phase` narrative, `blocking` row (6) all updated to reflect v2.0 trim + withdrawal. JSON validated.

Created:
- `memory/feedback_delay_formalization_until_second_recurrence.md` — the governing principle codified.
- `org/tier1_exec/1.1.0_SA_CTO/logs/2026-04-21/session04_target_closeout_prd_v2_0_trim.md` — this log.

Also edited:
- `memory/MEMORY.md` — new index entry linking to the feedback file.

Out of scope (untouched): `comp/`, other project JSONs, `REGISTRY.md`, other TOs.

---

## Blockers

None. v2.0 reduces COO partner's decomposition surface to zero new TOs. The `.015` and `.018` amendments are in place. No action required on her side beyond acknowledging the trim.

---

## Current State

- PRD at v2.0. Subsystem dropped. Convention in place.
- TO inventory: unchanged at 22 (6 COMPLETE / 1 DEFERRED / 1 PENDING / 14 STAGED). `.023` + `.024` never actually materialized — they were in-PRD decomposition suggestions, not TO files. Withdrawal is a PRD-side edit, not a TO-file deletion.
- JSON validated.
- Process principles persisted to memory for future sessions.

---

## Next Steps

1. **[2.1.0_SA_COO]** Decomposition surface reduced to zero new TOs. `.009` / `.018` amendments already applied in prior commits. Nothing to author.
2. **[1.1.0_SA_CTO next session]** Standing duties unchanged. The feedback principles now live in memory so future PRD drafts get filtered through them before shipping.
3. **[Joint dyad]** When DS terminals come online and `.017` runs to a terminal condition, first close-out will be the test of v2.0's convention. If the 3-artifact pattern feels right, v2.0 stays. If the convention reveals missing structure, the second close-out earns the right to formalize it (per the principle).

---

## Compiler Tools

| Tool | Command | Result | Purpose |
|------|---------|--------|---------|
| Read | process-feedback text (user-provided; not a file) | Parsed into 4 kept + 4 cut items + 5 mechanisms | Map feedback to concrete actions |
| Read | `docs/architecture/COMP_LEARNS_TARGET_CLOSEOUT.md` (v1.1) | Full file captured pre-trim | Know what to drop vs preserve |
| Read | `org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.018.cto-program-md-v1.md` | 9th-item v1.1 text captured | Plan revert to plain-section scope |
| Read | `memory/MEMORY.md` last ~50 lines | Feedback-section insert anchor identified | Add index entry cleanly |
| Write | New PRD v2.0 (rewrite) + new memory file + new session log | Clean | v2.0 deliverables |
| Edit | 6 surgical edits across 4 TO files + JSON + MEMORY.md | Clean | Reference bumps + scope reverts |
| python | `python -c "import json; json.load(...)"` | `JSON OK` | JSON validation |
| wc -l | PRD line count pre/post | 431 → 218 | Confirm trim magnitude |

No `comp-*` graph-tool runs — PRD revision operates on doc + TO text only. Same posture as session 02 and 03: close-out module does not exist yet (and per v2.0 may not ever exist), so `comp-build` / `comp-xref` / `comp-blast` have nothing to index.

---

## Task Order Dispatch

None. CTO agents do not issue task orders; the v2.0 trim withdraws two proposed-but-never-authored TOs (`.023` + `.024`) — which is not a dispatch action, it is a decision to not decompose. All remaining CTO-owned TOs (`.009` / `.018` / `.020`) carry v2.0-aligned references; no further dispatch-adjacent action.

---

## Process retrospective (parked for future self)

Three things I did badly on v1.0 → v1.1 and should avoid on the next PRD:

1. **I specified a ritual before performing it once.** The close-out ritual would have been better written retrospectively, after target 1 actually closed out, as documentation of what we actually did. Going forward: if I'm writing a PRD for a thing that has never been done, ask first whether a note in the log would serve better.
2. **I let the external validator loop pull me toward tighter specification, not lighter.** The codex validator gave useful content-level feedback (precedence rule, Justification block, hard minimums) that I applied to an already-over-engineered subsystem. The validator was answering "is this subsystem well-specified?" when the right question was "should this subsystem exist at all?" Going forward: when asking for validation, include "is this scope necessary?" as an explicit question, not just "is this content correct?"
3. **I under-weighted the "we haven't done this yet" signal.** v4.2 architecture was complete; no target had iterated; the dyad-split was hours old. Every signal pointed at "we don't know enough to specify this." I overrode those signals because the scaffold felt productive. Productive ≠ right.

These three observations are parked here for future me reading this log. Not codified as separate memory entries — the delay-formalization-until-second-recurrence feedback already covers the general principle.

— 1.1.0_SA_CTO
