# Ruling on call dell2-20261017T004344Z-4e37: FWD-11's PROD path without the Trade Request upload (c05e3dda)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-17 ~00:5xZ. **RULED: the REC.** `~V2` makes a PROD-based re-cut of `12c164a0` (the meeting form) and
`8e4f0885` (the outcome line), WITHOUT `c05e3dda`. Andrew's hold on the Trade Request ("we should not push this til we actually have a
functioning channel for that") is left untouched: no Trade Request code reaches PROD, hidden or not.

**Measured by this seat**, in a scratch worktree on portal `origin/PROD` (removed after):
- **`12c164a0` applies to PROD with no conflict** (4 files: `tickets.ts`, `MeetingRequestParts.tsx`, `TicketCenter.tsx`, its test).
- **`8e4f0885` then conflicts in `TicketCenter.tsx` only, and the conflict is TEXTUAL.** Its side carries two DEV-only neighbours: the
  `TradeFormOpen` import (from `c05e3dda`) and the `AnalysisPackageRow` row (a DEV feature not on PROD). The meeting change itself
  (`showsMeetingOutcome`, `viewerIsCoordinator`) does not depend on either.
- `tickets.ts` is touched by both `12c164a0` and `c05e3dda`. The first pick took only the meeting hunks onto PROD.

**The resolution, exactly:**
1. Keep PROD's import of `TradeRequestForm` alone; no `TradeFormOpen`.
2. Take the meeting imports, including `showsMeetingOutcome` and `viewerIsCoordinator`.
3. Keep PROD's `AnalysisDraftAndPackage` row; `AnalysisPackageRow` is not pulled.
4. The meeting row's condition becomes `showsMeetingOutcome(t)`, with the coordinator controls behind `viewerIsCoordinator`.

**Before registration:**
- `meeting-request.test.tsx` and `meeting-outcome-visibility.test.tsx` pass on the re-cut, with typecheck rc 0.
- The two-dot diff against `origin/PROD` touches only the meeting files and the resolved lines. The string `TradeFormOpen` and the file
  `trade-form-upload.test.tsx` are ABSENT from it.
- Registered **opal-internal** (my bc18 ruling). This seat approves it by sha after re-reading `App.tsx:505` and `firmAccess.ts:148-153`
  at that sha.

-- `1.0.0_SA_CTO~DELL2`
