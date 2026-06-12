# Task Order: ADVI_SEGFE — advisor-drill Continuous-ADV-AUM interval/window toggle regression

**Lane:** DE/RD portal (0.4.0_DE_ClientPlatform primary; 0.4.2_RD_AdvisorIntelligence CC — advisor-intelligence surface)
**Priority:** P2 — 1 of Andrew's 5 Segment Analytics bugs; the ONLY FE one (the other 3 are data -> ADVI_49NNAFIX)
**Origin:** DE's FE-vs-data triage of Andrew's 5 Segment Analytics bugs (docs/briefs/advi-49nnafix-project-request-20260612.md); CTO HANDOFF 221239Z explicitly carved this out as "PORTAL bug, DE/RD lane — track it as its own item so it doesn't get miscategorized as data."

---

## The bug (DE's own diagnosis — fill from your trace)

The advisor-drill **Continuous-ADV-AUM toggle** drops its interval/window selection in the **relationship-stacked path**. DE diagnosed this as FE (a portal control-state regression), NOT a data gap — the underlying ADV-AUM data is present; the FE control isn't passing/honoring the interval+window through the relationship-stacked drill path.

This is a **portal/FE fix** — control-state wiring, not a producer/canonical change. Stays portal-side; does NOT touch the data pipeline.

## Scope
- Trace the advisor-drill ADV-AUM toggle's interval/window state through the relationship-stacked path; find where the selection is dropped (likely a prop-drill / state-reset on the stacked-relationship render branch).
- Restore interval+window propagation so the toggle behaves consistently with the non-stacked advisor-drill path.
- `comp-transform schema-check` on any component touched (Rule 20 frontend gate); ternary-audit if a new mode/branch is involved.
- Portal lane discipline: DEV worktree, VALGATE, normal promote cycle. NOT a tonight-urgent (P2); slot in DE's portal queue.

## Acceptance Criteria
- AC1: advisor-drill ADV-AUM toggle preserves interval+window selection in the relationship-stacked path (parity with the non-stacked path).
- AC2: comp-transform schema-check clean on touched components; no new undefined-at-runtime.
- AC3: before/after captured (the dropped-then-restored toggle behavior); DE smoke on DEV.

## RAVC2 to COO
The trace finding (where state was dropped) + the fix + DEV smoke. CC RD (advisor-intelligence surface) + (if it rides a promote) the promote RAVC2.

---

*Authored by 2.0.0_SA_COO 20260612T2228Z — /drive cycle; CTO carve-out 221239Z. Separate from ADVI_49NNAFIX (the 3 DATA bugs) so the FE fix isn't miscategorized as data.*
