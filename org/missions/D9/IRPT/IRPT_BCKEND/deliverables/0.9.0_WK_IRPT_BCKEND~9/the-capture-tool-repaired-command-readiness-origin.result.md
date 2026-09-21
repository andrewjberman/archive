# IRPT_BCKEND.TO-IB-rti-1 -- result (first pass, by 0.9.0_WK_IRPT_BCKEND~9)

**State: STOPPED ON THE PACKET ALONE, as the order expects.** Arms (a)-(e) done; arm (f)'s packet committed; NEITHER half
(`2.0.0_SA_COO~B`, `1.0.0_SA_CTO`) is at HEAD naming the packet blob `56ad32833417a7a70c1d3933927385f9d66accfb`, so the S3 publish
did not run, no ledger entry was opened, nothing was written to S3. The order stays OPEN on R91-AC6.

## Arm (a) baseline (unchanged source, unchanged CVO diagnostic, at my HEAD eecaad4985)
All three defects reproduced: `literalInstancePlaceholder=true` in all 3 cases; HTTP 500 + no password input => writes=1, success printed;
`https://example.invalid` + no password input => 2 navigations, writes=1, success printed. Output: `IB-rti-1_baseline_diagnostic_output.txt`.

## Repair (commit 8d1934ac7e) -- choices stated
- S125: instance id from env `IRPT_CAPTURE_INSTANCE_ID`, validated `^i-[0-9a-f]{8,17}$` in the .cjs; the .sh wrapper fills it from IMDSv2
  (2 s timeouts) when unset. Missing/invalid => exit 1, browser never launched, no command printed. Env-validate + wrapper metadata read was the smallest
  correct form (the .cjs stays testable under stubs).
- S126: marker `[data-print-state]` (AUTH_MARKER). Cited in the source comment: PrintEntry.tsx:165,179,190,210,230 @ portal 8894e765ac (attribute exists only
  there); App.tsx:576 @ 8894e765ac (mounted only inside `ProtectedRoute requireAdmin requireInternal`); ProtectedRoute.tsx:29-31 and :61 @ 8894e765ac
  (unauthenticated => `<Navigate to="/login">`, children rendered only after every check). Note the marker also requires an admin of the internal firm, which is
  what the render needs. Portal at that commit was read from the main checkout (this worktree's `portal` gitlink is empty); `git status src` there shows only untracked dirs.
- S127: `ALLOWED_ORIGINS=['https://opalinvest.dev']` + vendor denylist copied from render_export.cjs; check-route and first-navigation and every redirect hop
  must be same-origin; saved state filtered to the origin (cookies by domain match, origins by exact origin), written at mode 0600 by the tool itself.
  **Premise correction:** render_export.cjs holds no fixed origin allowlist (row W9-S1); the equality arm asserts the 4-entry vendor lists are equal.
- Retry: up to 5 failed ENTER checks, then exit 1 with no file (the order's "exits non-zero" made literal); hard refusals exit immediately.

## Controls run by the worker
Mutants of the source (marker check, status check, sign-in checks, hop check each removed in turn) each turned the matching battery arm FAIL; source restored
byte-identical (cmp). The first harness cut had a redirect-chain closure bug that made hop-dependent refusals pass for the wrong reason; caught when the
POSITIVE case failed, fixed before any output was committed.

## Not done / not claimed
Arm (f) publish (gated). No host start/stop, live login, credential, network call or real session file. NO on-host byte readback exists. The README sentences
that make behavioural claims map to: exact command -> `--arm command` README-equality check; "re-verified" -> `--arm readiness`; origin-scoped file -> `--arm origin`.
R91-AC7 is a judgment and carries no verdict from the worker.
