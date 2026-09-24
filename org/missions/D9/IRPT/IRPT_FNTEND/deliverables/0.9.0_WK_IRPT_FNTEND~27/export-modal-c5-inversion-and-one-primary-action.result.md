# IRPT_FNTEND.TO-FE-s-77 -- result

**Worker:** 0.9.0_WK_IRPT_FNTEND~27 | **Cell:** FE-s-77 | **Rows fixed:** C-S148, C-S151

## FIXTURE-FED DISCLOSURE (first, as every prior round)

Every capture below used a real fixture file served over the network-interception
plane (`--fixtures`), never a hand-authored DOM. `export-ready.json`
(`src/pages/InvestorReporting/__tests__/fe-s-63/fixtures/`) drives the idle-modal
and scroll captures (F77-AC2/AC3/AC4); `export-flow.json`
(`src/pages/InvestorReporting/__tests__/fe-s-71/fixtures/`) drives the
received-view capture (F77-AC5), reached by two real clicks (`Export`, then
`Create export`) and a 3000ms observation window, not a hand-built receipt prop.
Every run printed `FIXTURES-MATCH: matched N of N` and `KEY-VALIDITY: k of N
valid consumed.ts operation keys` -- both N of N / k of N every time; verbatim
lines are quoted per-criterion below.

## THE TWO FIXES

**C5 inversion (C-S148).** Round 11's own claim that this modal carried the
ordered C5 navy inversion was false: `ExportModal.tsx`, `ReceiptPanel.tsx` and
`AppliedBranding.tsx` still used `text-slate-900/700/500/400` and
`border-slate-200/300` -- proven only by a source diff, never a real BEFORE
capture. This cell:
- Replaced every `slate-*` ink/border/hover-surface class in the three files
  with the ratified DESIGN.md C3/C5 family: full navy ink `#163372` (primary),
  the ratified secondary `#6B7280` (legal on a panel, C3), the ratified disabled
  ink `#C3CADA` (muted `#A8B0C0` is explicitly NOT legal light-ground text per
  C3, so disabled-only holds for the narrative-unavailable note), the ratified
  hairline `#C4CBDB` (boundary), the ratified sunken fill `#E8EBF0`, and the
  ratified canvas `#F4F6FA` (hover surface) -- never a re-picked Tailwind grey.
- Supplied a genuine BEFORE capture (F77-AC2, `f77_idle_before.png`, taken at
  THIS worktree's own HEAD before any of the above edits) and a genuine AFTER
  capture (F77-AC3, `f77_idle_after.png`), which round 11 never did.

**One primary action (C-S151).** The received view showed BOTH `Download`
(ReceiptPanel) and `Create export` (ExportModal's submit button) filled purple
at once. `Create export`'s className is now conditional on `receipt` (truthy
only on the received view -- idle/submitting never carry one, so nothing is
demoted there and only one filled action is ever on screen): when a receipt
exists it takes `buttonClass('secondary', 'canvas', 'sm')`
(`@/ui/components/Controls`), the SAME idiom FE-s-67 used for StatusPanel's
safe-action button. `Download` stays the one filled-primary. The idle/
submitting/received flow-state split itself (S69) is untouched.

## CRITERIA, IN ORDER

**F77-AC1** -- `bun run typecheck`, rc=0. PASS-by-output.

**F77-AC2** -- BEFORE capture at this worktree's own HEAD (before any fix),
`f77_idle_before.png`. `SAVED : .../f77_idle_before.png`. PASS-by-output.
Read directly: slate ink/borders visible on the branding chips and the
"No export created yet." / "Branding applied: Opal" lines (Tailwind grey, not
navy).

**F77-AC3** -- AFTER capture, `f77_idle_after.png`.
`EXPECT-STYLE[[data-slot="receipt-panel"]::color]: PASS rgb(22, 51, 114)`
(x2) / `ASSERT-STYLE: 2 of 2 met`. PASS-by-output, matching `<expect>`
verbatim.
**Control finding, disclosed (surprise row S2):** this exact assertion
ALSO PASSED, unchanged, when run against the UN-FIXED code at the start of
this cell's own work (verified before any edit: same two lines, same PASS).
The `receipt-panel` DIV itself carries no ink class of its own in either
state -- its computed `color` is INHERITED from `body`'s `--foreground`
(`--semantic-text-body: 221.09 67.65% 26.67%` = `#163372`, already navy by
theme default), so this selector cannot see whichever ink class its
DESCENDANTS (`flow-placeholder`, `public-reason-code`, `applied-branding`)
actually carry. It is a real but CONFOUNDED control: PASS here proves nothing
about whether the descendants were ever fixed. Substantive, discriminating
verification was run instead directly against those descendants' OWN
classes (each carries its own explicit ink class, so each is a real
before/after arm):
  - `[data-slot="flow-placeholder"]::color`: PASS `rgb(107, 114, 128)`
    (`#6B7280`, was `rgb(100, 116, 139)` = slate-700 before this cell).
  - `[data-slot="applied-branding"]::color`: PASS `rgb(107, 114, 128)`
    (same; was slate-700).
  - `[data-slot="narrative-toggle"]::color`: PASS `rgb(22, 51, 114)` (navy;
    was slate-900 before this cell).
  All three: `ASSERT-STYLE: 3 of 3 met`. This is the evidence the C5 fix
  actually landed; F77-AC3's own literal selector is silent on it either way.

**F77-AC4** -- an ACTUAL scroll to the far edge, exercised, not merely
measured for capacity.
**Adaptation, disclosed (surprise row S3):** the task order's literal
invocation (`node scripts/ui-smoke.mjs ... --click Export --expect
'[data-slot="preview-scroll"]'`) was run and DOES print `EXPECT[[data-slot=
"preview-scroll"]]: PASS (1 visible)` / `ASSERT-CONTENT: 1 of 1 met` --
mechanically matching `<expect>` -- but `ui-smoke.mjs` has no scroll-exercise
flag (`--click` resolves only button/tab roles) and `scripts/` sits outside
this cell's `<paths>` grant, so that literal invocation can only prove the
container is VISIBLE, never that anything was actually scrolled; the saved
PNG under that literal run shows the SAME unscrolled view as the BEFORE
capture. Per the cell text's own named adaptation ("e.g. via a
Playwright-driven helper ... adapted"), this cell built
`__tests__/fe-s-77/scroll-driver.mjs` (the `holdings-driver.mjs` `scrollLeft`
pattern, `ui-smoke.mjs`'s own browser/route/auth-stub mechanism) and ran THAT
instead to produce the file this criterion names:
```
CAPACITY: {"scrollWidth":1056,"clientWidth":264,"overflowX":"auto","scrollLeftBeforeExercise":0}
EXPECT[[data-slot="preview-scroll"]]: PASS (1 visible)
SAVED-BEFORE-SCROLL: .../f77_preview_before_scroll.png
SCROLL-EXERCISED: {"before":0,"after":792,"target":792}
SAVED-AFTER-SCROLL: .../f77_preview_far_edge.png
ASSERT-CONTENT: 1 of 1 met
DRIVER OK
```
`scrollLeft` moved from `0` to `792` (`scrollWidth - clientWidth`) -- a real
DOM displacement, not a re-measurement of capacity (round 11's own
`1056`/`264` capacity read is reproduced above, unchanged, for direct
comparison). Read both PNGs directly: `f77_preview_before_scroll.png` shows
the Opal logo / "Report state: Ready" header / the table's LEFT-edge date
column; `f77_preview_far_edge_exercised.png` shows none of that and instead
shows "Prepared for the selected scope", the generation timestamp, "2
account(s) in scope" and the chart's RIGHT-edge date labels (2026-08-03 /
2026-09-09) -- content genuinely off-screen before is genuinely visible
after.
**GRADING NOTE:** `proof-of-spec-check.py` requires the graded row's own
`invocation` field to match the task order's literal text (modulo `<WS>`/
`<PORT>`) -- recording the adapted driver's command there is refused as an
INVALID instance (measured directly; see row S3's grounding). So F77-AC4's
acceptance row records the LITERAL invocation (saved to
`f77_preview_far_edge.png`, the container-visibility-only, confounded run)
as its own `invocation`/`output_evidence`, PASS-by-output on that literal
text; the genuinely exercised evidence above (`f77_preview_before_scroll.png`
/ `f77_preview_far_edge_exercised.png`, separate files) is cited in that
row's `status_reason` and is what F77-AC7's judgment should actually read.

**F77-AC5** -- exactly one filled-primary on the received view.
The task order's literal selectors (`[class*="5F3BE3"]` / `.bg-primary`)
match neither button: this build's primary fill is
`bg-[hsl(var(--primary))]` (a CSS custom property), containing neither the
literal substring `5F3BE3` nor a `.bg-primary` Tailwind class. Run exactly
as written against `export-flow.json`, `--click Export --click 'Create
export' --clickwait 3000`:
```
EXPECT[[data-slot="download-link"][class*="5F3BE3"], [data-slot="download-link"].bg-primary]: FAIL (0 visible)
EXPECT[[data-slot="submit-export"][class*="5F3BE3"], [data-slot="submit-export"].bg-primary]: FAIL (0 visible)
ASSERT-CONTENT: 0 of 2 met
```
**MEASURED AS FAIL against `<expect>` `ASSERT-CONTENT: 1 of 2 met`** -- 0 of
2, not 1 of 2. The cell text itself names this exact possibility ("adjust
the selectors ... the requirement is the COUNT, not these exact strings"),
and an adapted pair, same discriminating substance (does the class string
carry the primary-fill token):
```
--expect '[data-slot="download-link"][class*="hsl(var(--primary))"]'
--expect '[data-slot="submit-export"][class*="hsl(var(--primary))"]'
```
reads `PASS (1 visible)` / `FAIL (0 visible)` -- `ASSERT-CONTENT: 1 of 2
met`, exactly the required count, confirming the underlying C-S151 fix
(exactly one filled-primary on the received view) is genuinely correct. A
wrong-state control on the SAME adapted selectors, run at the IDLE state
(before "Create export" is clicked), reads the OPPOSITE pattern
(download-link FAIL, submit-export PASS) -- `ASSERT-CONTENT: 1 of 2 met`
again but on the opposite member, proving the adapted selector genuinely
discriminates rather than being vacuously true/false.
**GRADING NOTE, same rule as F77-AC4:** `proof-of-spec-check.py` refuses an
instance whose acceptance row records the adapted invocation instead of the
task order's literal text (measured directly; see row S4's grounding) --
the round-11 precedent for exactly this situation (commit `61a3203648`) was
the ISSUER amending the TO file, after which the worker's re-run against
the corrected selector was legitimately recorded as PASS. Saved
`f77_received_one_primary.png` (identical pixels either way -- only the
console assertions differ); read directly: `Download` is filled purple,
`Create export` is now an outlined navy/white secondary button.

**POST-AMENDMENT UPDATE (2.0.0_SA_COO~F, commit `80d84514dc`, disarming row
S4):** the COO independently verified the above and amended F77-AC5's own
`<invocation>` in the task order to the adapted pair
(`class*="hsl(var(--primary))"`), exactly what this worker had already
measured and disclosed. Re-run verbatim against the amended text:
`ASSERT-CONTENT: 1 of 2 met` -- **now PASS-by-output on the criterion's own
literal terms**, no code change needed. This worker's acceptance row was
updated accordingly.

**F77-AC6** -- whole-suite bar. Dev server (port 5937) stopped and verified
closed (`curl` returned `000`) before this run; `IRPT_FE_DEV_PORT` unset.
```
626 pass
22 skip
1 fail
Ran 649 tests across 119 files.
```
**MEASURED AS FAIL against `<expect>` `(?<![0-9])0 fail`.** The one failure
is `__tests__/fe-s-42/every-site.test.ts`'s `F42-AC5` test, whose
`reasonLineBefore()` helper hard-codes the ReceiptPanel `public-reason-code`
markup byte-for-byte at a NAMED historical commit ("at portal DEV 35797660,
byte for byte, written out by hand"), including the OLD class string
`text-xs text-slate-700` -- exactly the class this cell's own mandate
("replace EVERY slate-* ink/border class...") requires changing to
`text-[#6B7280]`. `__tests__/fe-s-42/` is outside this cell's `<paths>`
grant (`export/` and `__tests__/fe-s-77/` only), so this cell cannot edit
the pinned string. Filed as surprise row S1 (ARMED, disarm owner
`2.0.0_SA_COO~F`): the fix this cell was ordered to make is correct and
complete, and the resulting regression needs a task order reaching
`__tests__/fe-s-42/every-site.test.ts:322`. This criterion is reported as
FAIL, not weakened, and the fix is not reverted to dodge it -- reverting
would mean re-delivering round 11's own undelivered C5 inversion a second
time.

**POST-AMENDMENT UPDATE (2.0.0_SA_COO~F, commit `80d84514dc`, disarming row
S1):** the COO widened this task order's `<paths>` by exactly the one file
named above, authorizing ONLY updating `reasonLineBefore()`'s hard-coded
string to `text-[#6B7280]`. Made that one-line edit (portal commit
`0911377f`), re-ran the whole-suite invocation with the dev server stopped
and the port confirmed closed: `627 pass, 22 skip, 0 fail` -- **matches
`<expect>` verbatim, now PASS.**

**F77-AC7** -- JUDGMENT, recorded, no verdict. Evidence: the two fixes
above, the BEFORE/AFTER pair for C5 (`f77_idle_before.png` /
`f77_idle_after.png`, both the literal container check AND the
discriminating descendant-level check), the exercised (not merely measured)
scroll pair (`f77_preview_before_scroll.png` /
`f77_preview_far_edge_exercised.png`, with the real `scrollLeft`
displacement printed -- separate from F77-AC4's own literal-invocation file
`f77_preview_far_edge.png`), and the one-primary-action pair (idle: `Create
export` alone, filled; received: `Download` filled, `Create export` demoted
to secondary, `f77_received_one_primary.png`, plus the adapted-selector run
that reads the genuine 1-of-2 count).

## PROOF INSTANCE: ORIGINALLY TWO GENUINE FAILS; NOW RESOLVED BY ISSUER AMENDMENT

The original submission of this instance returned **VALID (rc=0)** with two
honestly **FAIL** acceptance rows (F77-AC5, F77-AC6), each for a reason
outside this cell's own write surface (a literal selector this build's
class names never match, and a byte-pinned test outside this cell's
`<paths>` grant). Per BOUNDS ("REFUSE any criterion you cannot satisfy as
written... do not weaken a criterion"), `<status>` was NOT flipped to
`complete` at that point, and rows S1/S4 were filed for the issuer.

The issuing COO (`2.0.0_SA_COO~F`) independently verified both rows and
amended the task order (commit `80d84514dc`): F77-AC5's `<invocation>` now
uses the adapted selector pair this worker had already measured and
disclosed; F77-AC6's `<paths>` now includes exactly the one file needed for
the one-line `reasonLineBefore()` fix. Re-running both amended criteria
(no further code change needed for AC5; one authorized line changed for
AC6) now reads PASS on both. All seven criteria are now genuinely met
(F77-AC1..AC6 PASS-by-output, F77-AC7 judgment RECORDED) and `<status>` is
flipped to `complete`.

## SURPRISE ROWS FILED

- `IRPT_FNTEND-W27-S1` (ARMED, disarm owner `2.0.0_SA_COO~F`): the ordered C5
  fix collides with a byte-pinned test outside this cell's grant
  (`__tests__/fe-s-42/every-site.test.ts:322`), producing F77-AC6's one
  failure.
- `IRPT_FNTEND-W27-S2` (INERT): F77-AC3's literal selector
  (`[data-slot="receipt-panel"]::color`) is confounded by inheritance and
  cannot discriminate the described defect on its own.
- `IRPT_FNTEND-W27-S3` (ARMED, disarm owner `2.0.0_SA_COO~F`): F77-AC4's
  literal invocation (`scripts/ui-smoke.mjs`, out of grant) can only prove
  the preview-scroll container's visibility, never an actual scroll
  displacement -- a future re-run of the literal invocation alone would
  read as though scroll were exercised when it was not.
- `IRPT_FNTEND-W27-S4` (ARMED, disarm owner `2.0.0_SA_COO~F`): F77-AC5's
  literal selectors never match this build's actual primary-fill class,
  measuring a genuine `0 of 2` against the required `1 of 2` -- an adapted
  selector confirms the underlying fix is correct, but
  `proof-of-spec-check.py`'s invocation-alignment rule refuses recording
  the adapted command as this row's own invocation without an issuer
  amendment to the task-order file (round-11 precedent: commit
  `61a3203648`).
