# DSGN_IRPTV1.TO-IV-e-30 -- ai-drill-tenant-thread -- result

Row `DSGN_IRPTV1-W19-S1`. IV-e-29 gave `ConsolidatedOverviewPanel` an optional `tenantLayout` prop but its only
product caller, `CanonicalBookView`, never passed it, so Cottonwood's real client drill still coloured cash in
the MIX_PIE amber instead of the tenant palette. This cell threads `tenantLayout` from `CanonicalBookView` down
through every one of its callers (`AdvisorBookView.tsx`, `ClientsTab.tsx`) and through `AdvisorBookClientDetail`
(which has no firm id of its own and forwards what its parent gives it) to its own `CanonicalBookView` call.

## Changes (strictly additive; every prop optional)

- `portal/src/pages/AdvisorIntelligence/_shared/panels/CanonicalBookView.tsx` -- new optional `tenantLayout?:
  TenantLayoutConfig` prop, forwarded verbatim to `ConsolidatedOverviewPanel`.
- `portal/src/pages/AdvisorIntelligence/_shared/AdvisorBookView.tsx` -- passes its existing
  `useTenantLayout(firmId, firmOverride)` result (`tenantLayout`, line ~379) to both its L3
  `<AdvisorBookClientDetail>` call (~930) and its L2 `<CanonicalBookView level="l2">` call (~1086).
- `portal/src/pages/AdvisorIntelligence/_shared/tabs/ClientsTab.tsx` -- passes `dataSourceLayout`
  (`useTenantLayout(firmId, firmOverride)`, ~151, the firm being viewed) to its L3 `<AdvisorBookClientDetail>`
  call (~730) and its N1 `<CanonicalBookView level="n1">` call (~812).
- `portal/src/pages/AdvisorIntelligence/_shared/AdvisorBookClientDetail.tsx` -- new optional
  `tenantLayout?: TenantLayoutConfig` prop (this file has no firm id of its own), forwarded to its own
  `<CanonicalBookView>` call.
- `node-builtins.d.ts` in the test folder gains a `readFileSync` ambient declaration (AC2's scan reads file
  contents from disk).

Nothing else changes: an omitted `tenantLayout` prop at any layer keeps today's exact behaviour (verified by
IVE30-AC1's difference-control arm).

## Acceptance

- **IVE30-AC1** (`cot-drill-thread.render.test.tsx`) -- PASS. Renders the real `CanonicalBookView` with the
  discovered Cottonwood layout and a composition carrying `cash` + `other`: the legend carries the resolved
  `ASSET_CLASS.cash` (`#86efac`) and `PALETTE.purple600` (`#9333ea`) colours. The same render WITHOUT
  `tenantLayout` carries the MIX_PIE cash colour (`#f59e0b`) instead, never the tenant colour --
  `VERDICT: DRILL-THREAD-OK`.
- **IVE30-AC2** (`cot-drill-thread.callsites.test.ts`) -- PASS. A disk scan of every `.tsx` file under
  `AdvisorIntelligence/` (tests excluded) finds 3 `<CanonicalBookView` usages and 2 `<AdvisorBookClientDetail`
  usages (the printed denominators), every one carrying `tenantLayout=`, and confirms
  `AdvisorBookClientDetail.tsx` forwards `tenantLayout={tenantLayout}` to its own `<CanonicalBookView` --
  `VERDICT: CALLSITES-THREADED-OK`.
- **IVE30-AC3** -- judgment=true. RECORDED, no verdict taken by this worker; graded by `2.0.0_SA_COO~D` at the
  drain on the running page.

## Controls

- **Mutant (AC1):** removed `tenantLayout={tenantLayout}` from `CanonicalBookView`'s forward to
  `ConsolidatedOverviewPanel` (in-worktree only). AC1 failed as expected (`VERDICT: DRILL-THREAD-FAIL` -- legend
  missing both resolved colours). Reverted; `git diff --stat` confirmed the file returned to the intended
  8-insertion state; AC1 re-ran to `VERDICT: DRILL-THREAD-OK`.
- **Mutant (AC2):** removed `tenantLayout={dataSourceLayout}` from `ClientsTab.tsx`'s N1 `<CanonicalBookView>`
  call (in-worktree only). AC2 failed as expected, naming the exact file and truncated tag. Reverted; `git diff
  --stat` confirmed the file returned to its intended 2-insertion state; AC2 re-ran to
  `VERDICT: CALLSITES-THREADED-OK`.
- **Determinism:** AC1 and AC2 each run three times total (including the two runs bracketing the mutant
  reverts) with identical console lines and verdicts each time. `bun x tsc -b --noEmit` rc=0 (0 diagnostics)
  both before and after all edits.

## Declared exclusions

- Editing `pages/InvestorReporting/**`, `contracts/**`, `api/**`, `src/lib/**` or any other page -- out of this
  cell's `<paths>` grant.
- Starting a dev server / exercising `localhost:5174` -- the task order reserves that to `2.0.0_SA_COO~D`'s
  drain (IVE30-AC3).
- Push, merge, rebase, `checkout --` or `clean` of either repository -- forbidden by BOUNDS. All commits are
  LOCAL on `wk-DSGN_IRPTV1-20` (workspace) and `wk-DSGN_IRPTV1-20-portal` (portal).

No surprises filed -- every premise in the WORKER FACE held against live state (`b997c9e5` matched the
worktree's actual base; IV-e-29's `tenantLayout` prop and Cottonwood's `colorPalette.other = PALETTE.purple600`
/ `colorPalette.cash = ASSET_CLASS.cash` were exactly as described).
