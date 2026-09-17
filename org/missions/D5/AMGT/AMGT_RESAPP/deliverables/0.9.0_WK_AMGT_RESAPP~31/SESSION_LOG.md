# SESSION_LOG -- 0.9.0_WK_AMGT_RESAPP~31, AMGT_RESAPP.TO-AMGT-rk-19 (page half), resumption

## Resumption context

This worker's prior turn stopped BLOCKING (commit 5f680cff85, row AMGT_RESAPP-Z-W31-S1): the
worktree's `portal/` gitlink was empty (no `.gitmodules` URL mapping, no package.json, no `src/`).
The issuing seat (`2.0.0_SA_COO~Z`) resolved that gap outside this worker's `<paths>` grant --
cloning `portal/` fresh at the exact recorded gitlink commit (`2453a7b4c6b7ff91ea89db499890a9486265d1a0`,
branch DEV) and running `bun install` -- and handed the same task order back verbatim, plus a
diagnosed-but-unfixed environment note about `npx tsc -b` on this device.

## What was found

`ThesisDriverChart.tsx` is the component rendering `ThesisTab`'s one chart, consuming
`thesis_driver_chart` from the thesis bundle. The adapter half (chain B, already drained at
`ba9afc0dc4`, code at `0e974a48e7`) serves a SECOND branch when the exact model-block join
misses: `source: "filing"`, points shaped `{period, value, unit, span, passage_id}` -- a
DIFFERENT point shape than the original model-block branch's `{fiscal_year, value, unit}`
(`period` vs `fiscal_year` is the live discriminator; `passage_id` only appears here).

No existing route/component in the portal resolves a bare passage id to text -- the established
pattern for that (`postureCites.ts`'s `E:` case, and `ThesisTab.tsx`'s own `EvidencePassages`
block) resolves an evidence id by scanning the SAME thesis bundle's `drafted_sections[].
sentences[].evidence[]` for a matching id. That is the mechanism this order's click-through
reuses -- no second lookup surface, no hover tooltip (the estate's own banned idiom for evidence).

## What was built

- `types.ts`: `DriverChartPoint` gains optional `period` and `passage_id`; `fiscal_year` becomes
  optional too (the filing branch never carries it).
- `ThesisDriverChart.tsx`: labels a `source === 'filing'` series "-- from the filing, not the
  model"; renders a per-point passage link (button) when a point carries a `passage_id`, which
  toggles an inline expanded blockquote showing the resolved passage text (`findEvidenceById`,
  mirroring `postureCites.ts`'s own `E:` resolution) or a named miss reason if the id does not
  resolve on this bundle. A point without a `passage_id` states that inline, never a dead link.
- `ThesisTab.tsx`: passes its already-computed `draftedSections` through as the new `sections` prop.

## AC1

`components 19 / from the filing 6 / passage 32 / source === 1 / source == 1` -- PASS. The
worker's actual wording is "from the filing, not the model" (matches the criterion's own named
substring).

## AC2 -- the device quirk, measured not assumed

The literal invocation `cd portal && npx tsc -b 2>&1 | tail -30` reproduced exactly the quirk
named in this resumption's dispatch: `npx` resolves an unrelated npm-registry decoy package
literally named `tsc` ("This is not the tsc command you are looking for") instead of this
bun-managed tree's locally-installed `typescript`. Measured, not assumed:

- Piped form (the literal invocation): banner output, pipeline's reported exit code 0 (that is
  `tail`'s exit status, not `npx`'s -- Rule 22a's own piped-exit-code trap).
- Unpiped form, run twice: byte-identical banner, `npx` exit code 1 both times.
- Direct binary (`./node_modules/.bin/tsc.exe -b`), run before and after this order's edits and
  again after planting+reverting a mutant: clean (rc=0, zero output) both times the code was
  unmutated; the mutant (`pointLabel`'s return type changed to `number`) reliably produced
  `error TS2322` x2 at rc=2, reverted byte-identical, re-confirmed clean.

AC2 is recorded FAIL on the literal invocation's own terms per the REFUSAL CLAUSE -- the banner
carries no information about whether this order's edits compile cleanly (a DISCRIMINATION
failure), so it cannot be graded PASS even though the direct-binary reading is clean. The
direct-binary reading is corroborating evidence about code health only, named separately, never
substituted for AC2's own grade. Filed row `AMGT_RESAPP-Z-W31-S2` (OBSERVATION, ARMED,
disarm_owner `0.4.0_DT_ClientPlatform`) -- a device/tooling defect, not a code defect.

## Disposition

This order's `<status>` is NOT flipped to `complete`: AC1 genuinely passes, AC2 genuinely fails
on its own literal terms. The task-order file itself is left untouched (no RECORD FACE write).
Per the order's own section 6, this worker does not proceed to `AMGT-rk-30` on an open predecessor.
