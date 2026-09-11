# IRPT_FNTEND.TO-FE-s-17 -- Lato packaging: result record

**Worker:** `0.9.0_WK_IRPT_FNTEND~2` | **Cell:** `FE-s-17` (decomp v0.2 @`430c5fcb4a`)
**Workspace worktree:** `/c/tmp/wk-irpt_fntend-2-3-fe-s-17`, branch `wk-irpt_fntend-2-3-fe-s-17`, base `6ecffd5b15`
**Portal worktree:** `/c/tmp/wk-irpt_fntend-2-3-fe-s-17/portal`, branch `wk-irpt_fntend-2-3-fe-s-17`, base `32a744dc`
**Portal work commits:** `5af5ed26` (the packaging) and `8c980f43` (the amended F17-AC6 instrument), both LOCAL
**Issuer amendment consumed:** workspace `37bdae313a` (`2.0.0_SA_COO~F`)

## OUTCOME: COMPLETE

All eight mechanical criteria PASS by their own output against the amended face.
`F17-AC9` is a judgment criterion, recorded with no verdict. `<status>` flipped to
`complete` in the commit that carries this record and the proof instance.

## THE TWO ROUNDS, AND WHY THERE WERE TWO

**Round 1** delivered the packaging and reported `F17-AC6` **FAIL** at `EXTERNAL: 2`.
The bar counted *every* font request the page made; two of them were the portal
SHELL's Inter webfont, `@import`ed from Google Fonts by `portal/src/index.css` line 16
at base commit `32a744dc` -- a file outside this order's `<paths>`, untouched in this
worktree, loaded on every route including the print route. No act available to this
worker moved that number. Row `IRPT_FNTEND-W2-S7` was filed and the order was left open.

The narrowing that makes the criterion pass was available from the first run and was
**refused**: scoping the count to the render package's own three faces returns `0`, and
a scoped zero arrives with a printed denominator, so it reads as MEASURED and would have
authorised a "the print route fetches no font off-box" claim the capture does not
support (Rule 24 -- the failure mode of a wrong domain is a GREEN).

**The issuer amended the criterion** at `37bdae313a`. The diff is exactly two lines:
`F17-AC6`'s `<expect>` moves from `EXTERNAL: 0` to `LATO OFF-ORIGIN: 0`, and its prose
is replaced by the recorded/graded split. Nothing else changed -- not the cell text, not
another criterion, not a path -- so the fonts, `print.css` and `render/manifest.ts`
needed no rework and none was done. **Round 2** changed one file:
`__tests__/fe-s-17/fonts-served.test.ts` at `8c980f43`.

The bar moved; the measurement did not. The same capture yields both numbers and the
instrument still prints both.

## ROW `IRPT_FNTEND-W2-S7` -- STANDING

The row **stands exactly as filed and was not edited.** Its `BLOCKING` class **no longer
blocks this order**, because the amended bar no longer counts the request it describes.
What the row asserts remains true of the world: the portal shell still fetches Inter
off-origin on every route. It does not go quiet -- the `F17-AC6` instrument prints
`SHELL FONT REQUESTS OFF-ORIGIN: 2` and enumerates both requests on every run.
Disposition stays `UNDER_INVESTIGATION` for the CVO at L9.

## FIRST ACT -- grounding (all four checks passed before any edit)

| check | result |
|---|---|
| `git rev-parse --abbrev-ref HEAD` (workspace) | `wk-irpt_fntend-2-3-fe-s-17` @ `6ecffd5b15` |
| `test -d org && test -d .tools` | `TREE-OK` |
| `git rev-parse --abbrev-ref HEAD` (portal) | `wk-irpt_fntend-2-3-fe-s-17` @ `32a744dcd3b5551f86c450a3a7807f553ce0f320` |
| `ls render/assets/fonts/` | `FONT_LICENSE.txt` only -- exactly as the cell states |
| `sha256sum .runtime/.../fonts/Lato-*.ttf` | 3 of 3 equal to the order's table, byte counts equal too |

Re-grounded again before acting on the amendment: `git show --stat 37bdae313a` -- one
file, two lines, author `2.0.0_SA_COO~F`.

## WHAT WAS WRITTEN

- **`render/assets/fonts/Lato-{Regular,Light,SemiBold}.ttf`** -- `cp` from the on-box
  capture. Nothing was fetched from any host.
- **`render/assets/fonts/fonts.manifest.json`** -- per file: `name`, `bytes`, `sha256`,
  `weight`, `style`, `licence` `OFL-1.1`, `licence_file` `FONT_LICENSE.txt`, `source`;
  plus top-level `stand_ins: {"700": "Lato-SemiBold.ttf (600)"}` and
  `not_packaged: ["700","italic"]`.
- **`render/print.css`** -- the `@font-face` block rewritten to three faces (300 / 400 /
  700), `format('truetype')`, `local()` first, every `url()` a local package path; the
  700 face's `src` is the SemiBold file under a comment naming the stand-in and the
  carried call (the CTO's packaging-input ruling); no italic face, under a comment
  saying none is packaged. The header note was also rewritten -- it asserted "no Lato
  binary exists in this repo", which this commit makes false. **No RULE outside the
  `@font-face` block changed.**
- **`render/manifest.ts`** -- `fonts` corrected from the aspirational
  `['Lato-Regular','Lato-Bold','Lato-Italic']` to the three real file names, plus a new
  `fontPackage` mirroring `fonts.manifest.json` field for field. See row
  `IRPT_FNTEND-W2-S8` for why the mirror is a sibling key and not `fonts` itself.
- **`__tests__/fe-s-17/`** -- `fonts.test.ts` (AC2/AC3/AC4/AC7), `fonts-served.test.ts`
  (AC6), `ambient-shims.d.ts` (two type-only declarations; the existing shims under
  `fe-s-1/`, `fe-s-3/`, `fe-s-7/` were NOT edited, and tsconfig was not touched).

## CRITERIA, AS RUN (amended face)

| id | verdict | deciding line |
|---|---|---|
| F17-AC1 | PASS | `rc=0` (`tsc -b --noEmit`, whole portal; 4 runs, all clean) |
| F17-AC2 | PASS | `FONTS: 3 of 3` |
| F17-AC3 | PASS | `EXTERNAL FONT HOSTS: 0` (3 url()s, 3 local, 0 missing) |
| F17-AC4 | PASS | `STAND-IN DECLARED: 700<-600` |
| F17-AC5 | PASS | `CONSOLE[log]: REFS RESOLVED: 1 of 1` (2 runs, PNG byte-identical) |
| F17-AC6 | PASS | `LATO OFF-ORIGIN: 0` (denominator 3; recorded first: `FONT REQUESTS: 5 of 144`, `SHELL FONT REQUESTS OFF-ORIGIN: 2`) |
| F17-AC7 | PASS | `LICENCE: OFL-1.1 -- FONT_LICENSE.txt (4499 chars), covering 3 face(s)` |
| F17-AC8 | PASS | `335 pass, 1 skip, 0 fail` (336 tests, 50 files, rc=0) |
| F17-AC9 | RECORDED (judgment) | PNG `fe-s-17_print_performance_1440.png`, 351294 bytes -- graded at L9, no verdict here |

`DID NOT LAND` printed on the AC5 run, as the face says it does for a route carrying a
query string; `rc=0` and the resolver line are the bar.

## THE F17-AC6 INSTRUMENT, AS AMENDED

```
FONT REQUESTS: 5 of 144 logged                      <- RECORDED, unnarrowed, FIRST
  GET 200 [portal shell,   OFF-ORIGIN] https://fonts.googleapis.com/css2?family=Inter...
  GET 200 [render package, this origin] .../render/assets/fonts/Lato-SemiBold.ttf
  GET 200 [render package, this origin] .../render/assets/fonts/Lato-Regular.ttf
  GET 200 [render package, this origin] .../render/assets/fonts/Lato-Light.ttf
  GET 200 [portal shell,   OFF-ORIGIN] https://fonts.gstatic.com/s/inter/v20/...woff2
SHELL FONT REQUESTS OFF-ORIGIN: 2                   <- RECORDED, never a bar
LATO REQUESTS: 3                                    <- GRADED (n>=1, all 200)
LATO REQUESTS NOT 200: 0 of 3
LATO OFF-ORIGIN: 0                                  <- GRADED
  denominator: 3 Lato request(s) classified, dev origin http://localhost:5182
```

Two design choices worth a reader's attention:

1. **The dev origin is derived from the capture's own document request**, never typed in
   -- a hard-coded port would let the test pass for the wrong reason on another port.
2. **The origin comparator is exercised on two CONSTRUCTED inputs**, not on "this capture
   contains some off-origin request". The latter control would pass only while the portal
   shell keeps its Google Fonts import: it would **fail the day the estate improves** and
   be misread as a Lato regression. The capture's own off-origin count is printed and
   asserted on by nothing.
3. `expect(lato.length).toBe(3)` guards the vacuous case -- a zero over an empty set is
   not a pass.

**Disclosed limit of the absence claim:** `LATO OFF-ORIGIN: 0` is an absence, and each
netlog is a single capture inside ui-smoke's 3000 ms post-load window, which the tool
discloses itself. A Lato request firing after the window would not appear. Two things
bound that and neither is the window: `F17-AC3` reads `print.css` statically, where 3 of
3 `url()`s are local package paths and none names a host, so no declared off-origin Lato
target exists for a longer window to reveal; and the Lato request count is asserted at
exactly 3, so a capture that missed one fails rather than passing quietly.

## THE GRAIN CHECK THAT MATTERED

`core.autocrlf=true` with no `.gitattributes` in the portal repo: the checkout is CRLF
while blobs are LF. A worktree `sha256sum` therefore hashes the CHECKOUT, not the
record. The committed BLOBS were hashed independently:

```
git cat-file blob $(git rev-parse 5af5ed26:src/.../Lato-Regular.ttf) | sha256sum
  d636e4683231f931eda222d588e944d082bfd3bdba02f928bee461c0f185b251  656568 bytes
  cf2a774503baf418d584f49967bd160e1e03f087c13b25602f28024ec7788f08  643884 bytes  (Light)
  71b8b7decbe75a881ed267be539d402bd1e9420b799658aada4e0d1bd5af803c  668548 bytes  (SemiBold)
```

3 of 3 equal to the order's table -- git treated the `.ttf`s as binary and applied no
EOL conversion. Both text patches were applied with anchor-count assertions against an
LF-normalised copy and written back in the checkout's own EOL, so neither file carries a
whole-file EOL churn.

## MUTANT CONTROL -- both arms fired

A digest comparison can be vacuously true and a `url()` scan can be a constant; both
would read as `FONTS: 3 of 3` / `EXTERNAL FONT HOSTS: 0`.

| arm | mutation | predicted | observed |
|---|---|---|---|
| A | one character of ONE `sha256` in `fonts.manifest.json` flipped | `FONTS: 2 of 3`, only the Regular row MISMATCH | `FONTS: 2 of 3`, `Lato-Regular.ttf ... MISMATCH (expected 0636e4...)` |
| B | one `url()` repointed at `https://fonts.gstatic.com/...` | `EXTERNAL FONT HOSTS: 1` | `EXTERNAL FONT HOSTS: 1`, `url(https://fonts.gstatic.com/s/lato/Lato-Light.ttf) EXTERNAL HOST` |

`6 pass / 3 fail`, rc=1. Restored by writing the saved bytes back (no `git checkout --`);
`git status --porcelain -- src/pages/InvestorReporting/render` then read EMPTY against
`5af5ed26`, and every criterion was re-run clean afterwards.

## DETERMINISM

`typecheck` 4 runs, `fonts.test.ts` 3 runs, `fonts-served.test.ts` 3 runs, the whole IR
set 2 runs, the ui-smoke capture 2 runs against two separately started dev servers. Every
printed value identical within each round; the only value that moved across rounds is the
graded line of `F17-AC6`, because the bar moved. The second capture reproduced the PNG
**byte-identically** (`git status` on the deliverables folder read empty after it
overwrote the first).

## STILL OPEN, FOR THE ISSUER -- named, not attempted

1. **`IRPT_FNTEND-W2-S8`:** should `RENDER_PACKAGE.fonts` itself be re-typed as the rich
   object the cell's wording suggests? That needs `__tests__/fe-s-4/manifest.test.ts`
   (`.join(', ')` at :214, `.length` asserted 3 at :216) inside the same grant.
2. **`IRPT_FNTEND-W2-S7`:** self-hosting the portal shell's Inter webfont. Outside this
   order and outside this project's scope per the amendment; the fact is printed on every
   `F17-AC6` run so it cannot go quiet.
3. The 700 slot renders in SemiBold, one step light of true Bold, wherever the stylesheet
   sets `font-weight: 700`. Declared in three places; a grader comparing the PNG against
   `brand.json` should expect SemiBold there.
