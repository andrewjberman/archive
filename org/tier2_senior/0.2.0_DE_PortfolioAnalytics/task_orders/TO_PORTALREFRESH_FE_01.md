# TO_PORTALREFRESH_FE_01 — DataRefresh rollback UI: confirm dialog + in-flight lockout + progress display

**Project:** OPAL_PORTALREFRESH  **Issuer:** 1.0.0_SA_CTO  **Assignee:** 0.2.0_DE_PortfolioAnalytics
**Status:** ACTIVE  **Issued:** 2026-07-17T13:40Z  **Priority:** P1 (starts immediately; no dependency on the BE leg)

## Why (one paragraph, grounded)

During the 2026-07-17 ST-Benchmark P0, Andrew clicked the portal rollback control; it worked
end-to-end but rendered NOTHING — no confirmation, no in-flight state, no success. He clicked ~6
times; each click re-fired the entire yang pipeline (6 racing executions, live in
/aws/lambda/opal-data-refresh-api 12:50–13:05Z — benign only because the inputs were identical).
Andrew-direct scope (MSTR brief 20260717T133342Z, verbatim): *"a fix … on frontend in terms of
making the UI responsive and locking out additional clicks, e.g. a popup 'Are you sure you want to
rollback to {date}' which the user acknowledges or cancels, and then displays the update process."*

## Deliverables

1. **Confirmation dialog** — "Are you sure you want to rollback to {date}?" with explicit
   acknowledge / cancel. No rollback request leaves the browser without the acknowledge.
2. **Click lockout** — from acknowledge until terminal state, the rollback control is disabled
   (all rollback rows, not just the clicked one — the hazard is two racing rollbacks with
   DIFFERENT inputs). Lockout survives re-render; it may NOT rely on component-local state alone.
3. **Progress display** — surface the in-flight execution through completion. The BE already
   returns `method` / `newExecutionId` / `status` on POST, and `GET /data-refresh/status/{id}`
   exists for polling. Show: submitted → running (poll) → success (with what was restored) or
   failure (with the error). The hook currently toasts errors only and swallows success
   (`useDataRefreshState.ts:445`) — success gets a first-class terminal state.

## Surfaces

- `portal/src/pages/DataRefresh/tabs/HistoryTab.tsx`
- `portal/src/pages/DataRefresh/hooks/useDataRefreshState.ts` (path corrected per DE ACK 134359Z)
- `portal/src/api/portal-proxy.ts` (`rollbackDataRefresh`)

## Law that binds

- Portal main worktree stays on **DEV** (CLAUDE.md Rule 19).
- New visual surface ⇒ **/frontend-dev** render-LOOK-commit loop + silver-canvas color law
  (the dialog and progress states are new visual surfaces — screenshot before commit).
- `comp-transform schema-check` on touched components (Rule: MISSING = runtime undefined).
- **You cannot push** — DT batches the promote (pod discipline). Commit to portal DEV; name your
  commits in your closure message so DT's batch picks them up (their pending batch already carries
  3b516623/84b24af8).

## Scope adds (Andrew-direct to DE's session, 2026-07-17 ~13:5xZ; recorded by CTO amendment)

4. **Time Machine panel REMOVAL** — delete the Time Machine panel from the DataRefresh History
   tab; the feature is no longer in production (consistent with the parked DRFR_PTMCH_PRD).
   Immediate; rides the FE_01 commit batch. (CTO batching ruling: YES, same batch.)
5. **Emergency Rollback tab — SKETCH-FIRST, GATED ON ANDREW'S PICK.** New tab for non-technical
   operators: a single panel + single button that rolls back to the last successful upload, with
   upload-tab-style animation and panel structure. Andrew wants ASCII sketches (/draw options) in
   DE's chat and will approve one BEFORE implementation — no code for this tab until his pick.
   Design constraints binding when implementation starts: reuses FE_01's confirm/lockout/progress
   machinery (single POST, existing rollback endpoint, target = last successful upload); the
   confirm dialog is NOT optional here — an emergency control for non-technical users needs the
   acknowledge step and the in-flight lockout MORE, not less; and it must surface BE's
   ALREADY_RUNNING rejection as a calm "a rollback is already in progress" state, never an error
   wall. Silver-canvas + /frontend-dev law applies (it is a new visual surface).

The rollback POST response shape (`method`/`newExecutionId`/`status`) and the status-polling
payload are the FE↔BE contract. DT's BE leg (TO_PORTALREFRESH_BE_01) may extend the status
endpoint (e.g. an ALREADY_RUNNING rejection). Build the FE to treat an unknown/rejected status as
a clean terminal failure state, and coordinate any payload change with DT by MCP before relying on it.

## Acceptance

- Exercised in the rendered portal (not config-read): (a) cancel ⇒ zero network calls; (b)
  acknowledge ⇒ exactly ONE POST regardless of click count; (c) progress reaches a terminal state
  on both a real success and a forced failure; (d) /frontend-dev screenshot attached to closure.
- Closure message to 1.0.0_SA_CTO + CC 0.2.0_DT with commit SHAs.
