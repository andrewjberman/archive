# IRPT_FNTEND.TO-FE-s-17 -- Lato packaging: result record

**Worker:** `0.9.0_WK_IRPT_FNTEND~2` | **Cell:** `FE-s-17` (decomp v0.2 @`430c5fcb4a`)
**Workspace worktree:** `/c/tmp/wk-irpt_fntend-2-3-fe-s-17`, branch `wk-irpt_fntend-2-3-fe-s-17`, base `6ecffd5b15`
**Portal worktree:** `/c/tmp/wk-irpt_fntend-2-3-fe-s-17/portal`, branch `wk-irpt_fntend-2-3-fe-s-17`, base `32a744dc`, work commit `5af5ed26` (LOCAL)

## OUTCOME: the order stays OPEN

Seven of the eight mechanical criteria PASS by their own output. **`F17-AC6` FAILS**
(`EXTERNAL: 2`, bar `EXTERNAL: 0`) and **`F17-AC8` FAILS** carrying that same single
assertion (`333 pass, 1 skip, 1 fail`). The cause is `src/index.css` line 16 -- the
portal SHELL's `@import url('https://fonts.googleapis.com/css2?family=Inter...')` --
which is present at this branch's base commit, fires on every route including
`/investor-reporting/print`, and sits in a file this order's `<paths>` does not name.
No act available to this worker moves that number. Row `IRPT_FNTEND-W2-S7`.
`<status>` is therefore left at `blocked`; it was not flipped.

The render package's OWN faces are clean on the criterion's intent: `EXTERNAL (render
package faces only): 0 of 3`, all three fetched from `http://localhost:5182` and served
`200`.

## FIRST ACT -- grounding (all four checks passed before any edit)

| check | result |
|---|---|
| `git rev-parse --abbrev-ref HEAD` (workspace) | `wk-irpt_fntend-2-3-fe-s-17` @ `6ecffd5b15` |
| `test -d org && test -d .tools` | `TREE-OK` |
| `git rev-parse --abbrev-ref HEAD` (portal) | `wk-irpt_fntend-2-3-fe-s-17` @ `32a744dcd3b5551f86c450a3a7807f553ce0f320` |
| `ls render/assets/fonts/` | `FONT_LICENSE.txt` only -- exactly as the cell states |
| `sha256sum .runtime/.../fonts/Lato-*.ttf` | 3 of 3 equal to the order's table, byte counts equal too |

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
  `@font-face` block changed** (diff: 45 insertions, 17 deletions, both hunks inside the
  header comment and the faces block).
- **`render/manifest.ts`** -- `fonts` corrected from the aspirational
  `['Lato-Regular','Lato-Bold','Lato-Italic']` to the three real file names, plus a new
  `fontPackage` mirroring `fonts.manifest.json` field for field. See row
  `IRPT_FNTEND-W2-S8` for why the mirror is a sibling key and not `fonts` itself.
- **`__tests__/fe-s-17/`** -- `fonts.test.ts` (AC2/AC3/AC4/AC7), `fonts-served.test.ts`
  (AC6), `ambient-shims.d.ts` (two type-only declarations; the existing shims under
  `fe-s-1/`, `fe-s-3/`, `fe-s-7/` were NOT edited).

## CRITERIA, AS RUN

| id | verdict | deciding line |
|---|---|---|
| F17-AC1 | PASS | `rc=0` (`tsc -b --noEmit`, whole portal) |
| F17-AC2 | PASS | `FONTS: 3 of 3` |
| F17-AC3 | PASS | `EXTERNAL FONT HOSTS: 0` (3 url()s, 3 local, 0 missing) |
| F17-AC4 | PASS | `STAND-IN DECLARED: 700<-600` |
| F17-AC5 | PASS | `CONSOLE[log]: REFS RESOLVED: 1 of 1` |
| **F17-AC6** | **FAIL** | **`EXTERNAL: 2`** (bar `EXTERNAL: 0`); `LATO REQUESTS: 3` meets its own half |
| F17-AC7 | PASS | `LICENCE: OFL-1.1 -- FONT_LICENSE.txt (4499 chars), covering 3 face(s)` |
| **F17-AC8** | **FAIL** | **`333 pass, 1 skip, 1 fail`**; the one failure IS F17-AC6's assertion |
| F17-AC9 | RECORDED (judgment) | PNG at `fe-s-17_print_performance_1440.png`, 351294 bytes -- graded at L9, no verdict here |

`DID NOT LAND` printed on the AC5 run, as the face says it does for a route carrying a
query string; `rc=0` and the resolver line are the bar.

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
`5af5ed26`, and the criteria were re-run clean afterwards (`FONTS: 3 of 3`,
`EXTERNAL FONT HOSTS: 0`, `STAND-IN DECLARED: 700<-600`, `LICENCE: OFL-1.1`, 9 pass 0 fail,
typecheck rc=0).

## WHY F17-AC6 WAS NOT MADE TO PASS

The narrowing was available and was refused. Scoping the EXTERNAL count to the render
package's own three faces returns `0` and would have turned the criterion green -- and a
scoped zero arrives with a printed denominator, so it reads as MEASURED and would have
authorised a "the print route fetches no font off-box" claim the capture does not
support (CLAUDE.md Rule 24: a subtraction whose domain is not the claim's population is
blinder than recall, and the failure mode is a GREEN). The instrument prints BOTH
numbers, unnarrowed first:

```
FONT REQUESTS: 5 of 144 logged
  OFF-ORIGIN: GET 200 https://fonts.googleapis.com/css2?family=Inter:wght@...&display=swap
  OFF-ORIGIN: GET 200 https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2
EXTERNAL: 2
EXTERNAL (render package faces only): 0 of 3
EXTERNAL (portal shell, src/index.css @import -- NOT this cell's grant): 2
```

Unscoped corroboration of the cause (`comp-find 'fonts\.googleapis\.com'`, DENOMINATOR 4
hits across 1198 files, `corpus=all`): one hit is this cell's own test constant, one is
`src/index.css:16`, two are archived design-language prose. `src/index.css` is the sole
live producer, and `git status --porcelain src/index.css` is empty in this worktree.

## OPEN FOR THE ISSUER

1. Was `F17-AC6`'s population meant to be the whole page or the render package's faces?
   (Row `IRPT_FNTEND-W2-S7`. Either answer is cheap; the test prints both numbers today.)
2. Should `RENDER_PACKAGE.fonts` itself be re-typed as the rich object the cell's wording
   suggests? That needs `__tests__/fe-s-4/manifest.test.ts` inside the same grant.
   (Row `IRPT_FNTEND-W2-S8`.)
3. Self-hosting the shell's Inter webfont is the act that would close AC6 as written. It
   is outside this order entirely and is named here, not attempted.
