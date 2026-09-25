# DSGN_IRPTV1.TO-IV-e-23 -- session log (0.9.0_WK_DSGN_IRPTV1~14)

**Cell:** IV-e-23 (FWD-15, ruling R6) -- the firm chip and the identity card print the firm
name, never the token.

## What was found at base (portal DEV `8242412dde9a3ef807e118f648242cf24ffe2981`)

- `FirmAttribution.tsx` (part a): rendered the display name when a catalogue match was found,
  returned `null` (no chip at all) when none was found, and never carried the firm's token
  (`PermittedFirm.firmId`) anywhere -- not even in a disclosure. IVE18-AC4's failure ("F-CW"
  chip) predates this file's own history and was not reproducible at this base's bytes; what
  was missing against the cell's own rule ("a fact moves to a disclosure, it does not vanish")
  was the "not supplied" fallback and the token's own disclosure.
- `IdentityCard.tsx` (part b): line 344 already read
  `scope?.verifiedRequestFirm?.displayName ?? 'not supplied'` -- already correct, no token
  ever reached the WHO line. Filed as row `DSGN_IRPTV1-W14-S1` (premise mismatch, INERT,
  non-blocking).

## What changed

- `portal/src/pages/InvestorReporting/global/FirmAttribution.tsx`: now reads the matched
  `PermittedFirm` via `findPermittedFirm` (not just its display name), renders the display
  name on the face (falling back to "not supplied" when no match), and moves the token into
  a `title=` disclosure only when a match exists.
- `IdentityCard.tsx`: no code change (already correct; proven by a new test).
- Three new tests under `__tests__/dsgn-irptv1/`: `iv-e-23.firm-chip.test.ts` (AC1),
  `iv-e-23.identity-firm.test.ts` (AC2), `iv-e-23.parity-kept.test.ts` (AC3, subprocess run
  of the KEPT, unedited `fe-s-10/parity.test.ts`).

## Verification

- All three new tests: PASS, printing their required VERDICT lines, run twice for determinism
  (identical both times).
- Mutant control: removed the token from `FirmAttribution`'s `title=` -- AC1 FAILED as
  expected (`token absent from disclosure`); file restored from a saved copy, confirmed
  byte-identical (`diff` clean), re-ran clean.
- Regression: `bun run typecheck` rc=0; full `__tests__/dsgn-irptv1/` suite 75 pass / 0 fail
  (61 files); `__tests__/fe-s-10/` (FirmAttribution's own home suite) 36 pass / 0 fail;
  `__tests__/fe-s-5/` (ReportingTab/HoldingsTab consumers) 22 pass / 3 fail -- the same 3
  pre-existing failures (`performance.partial-scope` / `unavailable-metric` /
  `unsupported-benchmark`, none related to firm attribution) already documented in the round-3
  drain (IV-e-19's own proof, DSGN_IRPTV1-W11-S2), not introduced here.

## Surprise filed

`DSGN_IRPTV1-W14-S1` -- the cell text's premise that `IdentityCard.tsx` still leaks the token
does not hold at this order's own base; only `FirmAttribution.tsx` needed the fix. Non-blocking,
INERT.

## Commits

- Portal worktree `wk-DSGN_IRPTV1-14-portal`: `48a6032f` (FirmAttribution.tsx + 3 new tests).
