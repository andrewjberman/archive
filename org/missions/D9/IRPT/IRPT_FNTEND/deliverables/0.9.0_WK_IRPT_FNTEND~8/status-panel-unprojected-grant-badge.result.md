# FE-s-58 -- StatusPanel renders the carried unprojected_grant, Global mode confirmed to inherit it

Worker `0.9.0_WK_IRPT_FNTEND~8`, task order `IRPT_FNTEND.TO-FE-s-58`.

## What changed

- `portal/src/pages/InvestorReporting/state/status.ts`: `TabEnvelope` and `AvailabilityLike` each
  gain `unprojectedGrant?: UnprojectedGrant | null`, mirroring `producerState`'s established
  pattern. `envelopeFromAvailability` copies it across with the same conditional-spread idiom
  `producerState` already uses. `envelopeFromRefusal` is unchanged -- the omission is already
  correct there, exactly like `producerState`.
- `portal/src/pages/InvestorReporting/tabs/StatusPanel.tsx`: a new `data-slot="partial-disclosure"`
  block, sited between the existing `reason-code` and `safe-actions` slots, rendered only when
  `envelope.unprojectedGrant && envelope.unprojectedGrant.count > 0`, showing the count,
  denominator and kinds in the panel's existing idiom (`text-xs text-slate-600`, the SAME classes
  the adjacent `reason-code` slot already uses -- navy-family ink on the white panel, never
  light-on-light).
- `portal/src/pages/InvestorReporting/__tests__/fe-s-58/status-panel-badge.test.ts`: F58-AC2..AC5.
- `portal/src/pages/InvestorReporting/__tests__/fe-s-58/browser-driver.mjs`: the real-browser
  driver F58-AC5 spawns.

## Criteria measured

- **F58-AC1** (typecheck): PASS -- `rc=0` at portal `6b206370`.
- **F58-AC2** (badge renders, count/denominator/kinds verbatim): PASS.
- **F58-AC3** (both arms -- count=0 and null -- absent): PASS.
- **F58-AC4** (refusal path: `unprojectedGrant` absent, reason-code unchanged): PASS.
- **F58-AC5** (Global mode, cross-firm, count>0, badge visible): PASS, via a REAL browser
  (`browser-driver.mjs`), not `renderToStaticMarkup` -- `global/useFirmContext.ts`'s own validation
  runs in a `useEffect`, which the static renderer never executes. A genuine two-firm
  `resolve-scope` wire response lands the page on Global (`header/firm.ts`'s own
  `DEFAULT_FIRM_ID = 'global'`, no click needed), `useFirmContext`'s real mount effect keeps it
  there (`resolveFirmSelection('global', scope)` on a 2-firm catalogue), and a `performance-report`
  wire response carrying `unprojected_grant.count=3` renders the badge in the live DOM. Read off
  the page: `firmSelectValue="global"`, `firmSelectOptions=["global","F-49F","F-CW"]`,
  `badgeText="3 of 10 (positions) not yet projected"`.
- **F58-AC6** (whole suite green): measured **2 fail** (`fe-s-32/holdings-in-a-browser.test.ts`
  F32-AC3, F32-AC5), confirmed by HEAD-restore isolation to be PRE-EXISTING and unrelated to this
  cell's edits -- `fe-s-32/` is not in this order's `<paths>`. This is `IRPT_FNTEND-W5-S9`'s
  already-ARMED hazard ("the assertion is FALSE the moment the precondition is MET ... latent, not
  yet exercised") firing for real for the first time in this channel, because this worker started
  its own worktree's dev server to satisfy F58-AC5's own declared precondition, and the whole-suite
  run inherited that live server. **REFUSED as literally invoked** -- see surprise row
  `IRPT_FNTEND-W8-S1`.
- **F58-AC7** (judgment, color law + Global-mode-genuinely-different-path): RECORDED, NO VERDICT.
  Evidence: a real full-page screenshot from the same browser driver
  (`.scratch/fe-s-58/captures/fe-s-58_global_reporting_badge_1440.png`, sha256
  `2166ba31d189fe760e1d02e9c1636568e653909bc44c23f3330effc68f864829`) shows the badge text
  ("3 of 10 (positions) not yet projected") rendered in the SAME dark slate ink as the adjacent
  `reason-code` line, on the white panel -- consistent with `portal/CLAUDE.md`'s color law
  ("Containers are white panels ... ink is navy" / "Light text, light buttons ... are ILLEGAL on
  the canvas AND on every white panel", lines 22-28) and with the pre-existing `reason-code` slot's
  own idiom (unchanged by this cell). The Firm dropdown reads "Global (All)" in the same capture,
  confirming F58-AC5's control is a DIFFERENT code path than F58-AC2 (a real page, the real hook's
  effect, a real wire response) rather than a relabelled copy of the direct-`StatusPanel`-prop
  render AC2 uses.

## Isolation control (mutant + pre-existing-defect discrimination)

Restored `state/status.ts` and `StatusPanel.tsx` to HEAD~1 (pre-this-commit) bytes and re-ran:
- `bun test src/pages/InvestorReporting/__tests__/fe-s-58/status-panel-badge.test.ts` -> F58-AC2
  FAILS (`badgePresent: false`), F58-AC3/AC4 still pass (their assertions are about absence, true
  either way) -- confirms the mutant fires exactly where expected.
- `bun test src/pages/InvestorReporting/__tests__/fe-s-32` alone -> SAME 2 fail as the whole-suite
  run, confirming those two failures are pre-existing and independent of this cell's edit.

Both files were then restored from a backup copy and re-verified byte-identical to the committed
state (`git diff --stat` empty).

## Commits

- Workspace: `79ac666dc3` (surprise row `IRPT_FNTEND-W8-S1`), branch `wk-irpt_fntend-9-58-fe-s-58`.
- Portal: `6b206370`, branch `wk-irpt_fntend-9-58-fe-s-58-portal` (LOCAL only -- portal is frozen).
