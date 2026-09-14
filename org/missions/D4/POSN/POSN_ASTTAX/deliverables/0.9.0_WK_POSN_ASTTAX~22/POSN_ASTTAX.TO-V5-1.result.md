# POSN_ASTTAX.TO-V5-1 -- THE COLOUR REGISTRY

**Cell** `AT5-s-5` (round 5, F1) - **Outcomes** FWD-3, FWD-4 - **Worker** `0.9.0_WK_POSN_ASTTAX~22`
**Worktree** `C:/tmp/wk-posn-5-22` branch `wk-posn_asttax-5-22` - **Portal branch** `wk-posn-5-22-portal`
**Date** 2026-09-14

## THE ANSWER IN ONE PARAGRAPH

`ASSET_CLASS` now carries **`structured: PALETTE.pink500`** and **`commodities: PALETTE.yellow500`** --
those two strings are the contract `AT5-s-6` (F2) binds. The sub-asset map gained `'Metals'` and moved
`'Commodities'` off `PALETTE.blue950`, a shade of Equity's own blue, onto the ruled yellow. The five
ratified classes hold **five distinct values, 5 of 5, measured**. One commit landed inside the portal
submodule on the pin, the superproject gitlink did not move, and nothing was pushed, promoted or merged.

**TWO CRITERIA ARE REFUSED, NOT PASSED, AND THE ORDER STAYS OPEN.** `V5-AC2` requires the diff to *add*
`'Hedge'`; the key already exists at the pin, bound to the wrong class family, and the order's own refusal
clause bars the repair. `V5-AC5` requires `git diff --submodule=log -- portal` to print empty; that command
cannot print empty once the portal commit the same order mandates exists. Both are recorded with their
measurements. **`<status>` was not flipped.**

## VINTAGES -- every citation here resolves to one of these

| object | pin | how it was read |
|---|---|---|
| portal source, BEFORE | `e85f6eb84f3a1771a37011a7e77e372570bad02a` | `git -C portal show e85f6eb84f:<path>` -- by CONTENT |
| portal source, AFTER | `c475e31e7014cb7e18ccf0c1cb6a335ad0720044` | this worker's commit, parent = the pin |
| POSN_ASTTAX PRD v0.7 | `99cc431075` | `git cat-file -p 99cc431075:.../POSN_ASTTAX_PRD.md` |
| this worktree | `945d1ddd95aa5ab63cdcdf3ee47f1197d9bf8023` | `git rev-parse HEAD` |

## THE EDIT, VERBATIM

```
@@ -114,6 +114,10 @@ export const ASSET_CLASS = {
   fixedIncome:  PALETTE.green500,
   equity:       PALETTE.blue500,
   cash:         PALETTE.amber500,
+  // Structured is pink and Commodities is the electric yellow (PRD s.3 ratified five);
+  // NEVER amber for Commodities: amber500 is Cash.
+  structured:   PALETTE.pink500,
+  commodities:  PALETTE.yellow500,
   alternatives: PALETTE.orange500,
   realEstate:   PALETTE.orange500,
   other:        PALETTE.gray500,
@@ -305,7 +309,10 @@ export const SUB_ASSET_COLORS: Record<string, string> = {
   'Emerging Markets':       PALETTE.blue700,
   'Volatility':             PALETTE.blue900,
-  'Commodities':            PALETTE.blue950,
+
+  // Commodities -- yellow (class base PALETTE.yellow500, the ruled gold; NEVER amber)
+  'Commodities':            PALETTE.yellow500,
+  'Metals':                 PALETTE.yellow500,
 }
```

`1 file changed, 8 insertions(+), 1 deletion(-)`. Nothing else in the file moved.

**THE TOKEN NAMES F2 BINDS, PRINTED EXACTLY AS THE ORDER REQUIRES:**

```
ASSET_CLASS.structured
ASSET_CLASS.commodities
```

## THE FIVE RATIFIED CLASSES AFTER THE EDIT

Read from `portal/src/lib/chartColors.ts` at run time by the committed loader -- no hex re-typed.
The class list and its canonical order come from PRD v0.7 `@99cc431075` s.3, not from the task order.

| # | class | `ASSET_CLASS` key | PALETTE token | hex |
|---|---|---|---|---|
| 1 | Fixed Income / Cash | `fixedIncome` | `green500` | `#10b981` |
| 2 | Equity | `equity` | `blue500` | `#3b82f6` |
| 3 | Structured | `structured` | `pink500` | `#ec4899` |
| 4 | Commodities | `commodities` | `yellow500` | `#eab308` |
| 5 | Alternatives | `alternatives` | `orange500` | `#f97316` |

**5 ratified classes; 0 absent; 5 DISTINCT values. Collisions among the ratified five: 0.**
Denominator: 65 PALETTE tokens, 8 `ASSET_CLASS` keys, 22 `SUB_ASSET_COLORS` keys, all parsed from the file.

**The pre-existing `alternatives` / `realEstate` pair is disclosed and unchanged**: both are `orange500`.
`realEstate` is not one of the ratified five -- s.3 row 5 holds "real assets (not commodities), private
equity, private credit, real estate", and C-SUB-ASSET names `Real Estate` = VNQ as a sub-asset. A class
sharing a colour with its own sub-asset is not a class-vs-class collision. Neither line was touched.

## CRITERIA

| id | verdict | deciding output | denominator |
|---|---|---|---|
| `V5-AC1` | **PASS** | `e85f6eb84f3a...bad02a`, both ancestry directions rc=0, measured before any write | 2 of 2 directions |
| `V5-AC2` | **FAIL** | `1 file changed, 8 insertions(+), 1 deletion(-)`; 5 of 6 limbs MET, the `'Hedge'` limb REFUSED | 6 limbs |
| `V5-AC3` | **PASS** | `5 ratified classes; 0 absent; 5 DISTINCT`; `COLLISIONS ... : 0` | 5 of 5 classes |
| `V5-AC4` | **PASS** | `tsc -b` rc=0; control fired `error TS2322` rc=2 then reverted | 1807 files, 481 under `src/` |
| `V5-AC5` | **FAIL** | limb 1 MET (1 commit, right author, parent = pin); limb 2 printed 162 bytes where "empty" was required | 2 limbs |
| `V5-AC6` | **PASS** | the ledger row naming branch, head, pin and drain ref | 4 of 4 elements |
| `V5-AC7` | **RECORDED (judgment)** | readings only; render UNREAD and stated as such; no verdict offered | 6 swatches, 4 dE pairs |

### `V5-AC1` -- the clone, at the pin, proved both ways

Before any write: `git -C portal rev-parse HEAD` -> `e85f6eb84f3a1771a37011a7e77e372570bad02a`, rc=0;
`merge-base --is-ancestor HEAD e85f6eb84f` rc=0; `merge-base --is-ancestor e85f6eb84f HEAD` rc=0.
Both directions printed. The working tree was clean and `cat portal/.git` confirmed the COO's pre-cut
linked worktree (`gitdir: .../portal/.git/worktrees/portal`) on branch `wk-posn-5-22-portal` -- it was
verified, never re-created.

> **RE-RUNNING THIS AFTER THE MANDATED COMMIT READS DIFFERENTLY, AND THAT IS NOT DRIFT.** HEAD is now
> `c475e31e70` and the forward ancestor test exits 1, because HEAD is exactly one commit **ahead** of the
> pin. The property the precondition guards survives and `V5-AC5` proves it independently: the commit's
> parent is the pin. **Do not take the criterion's "Otherwise detach to the pin" branch on the post-commit
> reading** -- it would abandon `c475e31e70`. Filed as `POSN_ASTTAX-Z-W22-S5`.

### `V5-AC2` -- REFUSED on one limb of six

Five limbs met: one file changed; `structured: PALETTE.pink500` added; `commodities: PALETTE.yellow500`
added; `'Commodities'` moved off `blue950` to the yellow family; nothing else touched. `'Metals'` added.

**The sixth limb cannot be satisfied by any act.** At the pin, read by content:

```
294:  'Hedge':                  PALETTE.green900,
```

and the block that contains it opens at `285` with the file's own comment
`// Fixed Income -- Green gradient (base is green-500, avoid re-using it)`. PRD v0.7 `@99cc431075` s.4
C-SUB-ASSET encodes `Hedge` as a `sub_asset_class` under **Structured**. So the key is not missing --
it is present and bound to the wrong class family. You cannot add a key that exists, and re-binding it
is a repair the order's own refusal clause forbids: *"never repaired, widened or satisfied by another
route."* Refused with its measurement. `POSN_ASTTAX-Z-W22-S1`.

`'Volatility': PALETTE.blue900` at `:307` -- inside the Equity blue gradient, PRD-bound for Structured --
**shares the mechanism** and is named in the same row rather than left for a later census.

### `V5-AC4` -- the build, with an instrument that can fail

`timeout 600 bash -c "cd portal && bun run tsc -b"` -> rc=0, zero bytes of output. It is not vacuous:
`--verbose` shows three projects built (`tsconfig.app.json` in 14 s, `tsconfig.node.json`), and
`tsc -p tsconfig.app.json --noEmit --listFiles` returns **1807 files** in the app program, **481** under
`portal/src/`, with `chartColors.ts` in the list. `node_modules` was absent in the pre-cut worktree;
`bun install` installed 420 packages rc=0 and left `bun.lock` and `package.json` unmodified.

Positive control, required by the criterion and run: a one-line type error injected into the edited file
produced `src/lib/chartColors.ts(546,14): error TS2322: Type 'string' is not assignable to type 'number'.`
rc=2. Reverted from a byte snapshot taken before the injection; sha256
`47b72bf729cf87054e3e69dd366c4dff097636c2c874529c1be3277c12c9d96f` matched and the `V5-AC2` diff re-read
identical.

### `V5-AC5` -- committed inside the submodule; the gitlink unmoved; limb 2 unsatisfiable

Limb 1 is fully met: `c475e31e7014cb7e18ccf0c1cb6a335ad0720044 0.9.0_WK_POSN_ASTTAX~22 ...`, one commit
on the branch, parent `e85f6eb84f3a1771a37011a7e77e372570bad02a`.

Limb 2 printed 162 bytes:

```
Submodule portal e85f6eb84f..c475e31e70:
  > POSN_ASTTAX.TO-V5-1 (AT5-s-5, F1): the colour registry gains Structured (pink) and Commodities (yellow, never amber)
```

`git diff` with no revision compares the **index** to the **working tree**, and for a gitlink the
working-tree side is the submodule's current HEAD. So this is non-empty the instant the mandated commit
exists, and the only way to silence it is `git add portal` -- the act s.4 forbids. **The criterion fails
exactly the workers who comply.** `POSN_ASTTAX-Z-W22-S2`.

**The bar s.4 actually states -- "no gitlink change STAGED OR COMMITTED by you" -- is met, four ways:**

```
git diff --cached --submodule=log -- portal   -> (empty), rc=0
git ls-tree HEAD -- portal                    -> 160000 commit e85f6eb84f3a1771a37011a7e77e372570bad02a  portal
git ls-files -s -- portal                     -> 160000 e85f6eb84f3a1771a37011a7e77e372570bad02a 0  portal
git log --format='%H %an %s' SITEZ..HEAD -- portal -> (no rows)
```

`git add portal` was never run. This worker offers no verdict on whether the intent should carry the
grade -- that is `3.0.0_SA_CVO~Z`'s at L9 -- and every read is printed so the decision rests on evidence.

### `V5-AC7` -- JUDGMENT, graded by `3.0.0_SA_CVO~Z` at L9. READINGS ONLY.

**RENDERED SWATCH: NOT READ -- stated, not inferred.** `portal/CLAUDE.md:54-57` names the render path
(`/frontend-dev`, `scripts/ui-smoke.mjs`) and it renders **app pages**. This order's `<paths>` grant holds
exactly one portal path, `src/lib/chartColors.ts` -- no page, no route, no `scripts/` path -- and no
surface displays a Commodities or Metals chip until `C-RETAG-SET` lands. The figures below are **computed,
never observed**, and that distinction is part of the reading. The law's own words are not evaded:
*"A grep cannot see contrast."*

Silver canvas, derived from the law's own HSL `222 24% 81%` -> `rgb(195,202,218)` `#c3cada`, which
reproduces the value `portal/CLAUDE.md:14` states independently.

| swatch | hex | contrast vs silver canvas |
|---|---|---|
| `yellow500` (Commodities, this order) | `#eab308` | **1.17** |
| `amber500` (Cash, pre-existing) | `#f59e0b` | **1.31** |
| `pink500` (Structured, this order) | `#ec4899` | 2.15 |
| `green500` (Fixed Income) | `#10b981` | 1.54 |
| `blue500` (Equity) | `#3b82f6` | 2.24 |
| `orange500` (Alternatives) | `#f97316` | 1.71 |

CIE76 dE(Lab), the subject pair with three controls so the number can be read:

| pair | dE76 |
|---|---|
| **SUBJECT** `yellow500` vs `amber500` | **16.42** |
| CONTROL identical pair (`amber500` vs itself) | 0.00 |
| CONTROL `blue500` vs `orange500` (nobody disputes these are distinct) | 135.55 |
| CONTROL `green400` vs `green500` (one adjacent step inside a ramp) | 9.14 |

Lab: `yellow500` (75.92, 7.70, 77.63); `amber500` (72.16, 23.50, 75.23).

Text on the two chips, because the value change reaches `getSubAssetTextColor`: white on `yellow500`
= **1.92**, dark `gray900` on the same yellow = **9.25**; the function's `lightBackgrounds` list holds
8 entries, all green/blue ramp steps or white, and no yellow. `POSN_ASTTAX-Z-W22-S4`.

`PALETTE`'s own comment at `:78` calls `yellow500` *"electric yellow (not amber)"* -- the file asserting
the very distinction this criterion asks to be judged.

**NO VERDICT IS OFFERED.**

## SURPRISE ROWS FILED -- five, all `UNDER_INVESTIGATION`

| id | class / hazard | one line |
|---|---|---|
| `POSN_ASTTAX-Z-W22-S1` | OBSERVATION / **ARMED** (`2.0.0_SA_COO~Z`) | `'Hedge'` already exists at `:294` on `green900` under Fixed Income while the PRD puts it under Structured; `'Volatility'` shares the mechanism |
| `POSN_ASTTAX-Z-W22-S2` | OBSERVATION / **ARMED** (`2.0.0_SA_COO~Z`) | the gitlink limb cannot print empty once the mandated commit exists; it fails exactly the compliant worker |
| `POSN_ASTTAX-Z-W22-S3` | OBSERVATION / INERT | the yellow family is one token wide, so `'Metals'` and `'Commodities'` cannot be a gradient; no ratified bar violated |
| `POSN_ASTTAX-Z-W22-S4` | OBSERVATION / **ARMED** (`2.0.0_SA_COO~Z`) | the move to yellow flipped the chip text to white-on-yellow at contrast 1.92; the one-line fix is barred by the same scope clause |
| `POSN_ASTTAX-Z-W22-S5` | OBSERVATION / INERT | `V5-AC1` is a pre-write precondition whose re-run reads off-pin; its "detach to the pin" branch must not be taken |

## WHAT WAS NOT DONE, AND WHY

- **`'Hedge'` not added and the existing line not re-bound** -- it exists; re-binding is a repair the
  refusal clause forbids. `S1`.
- **`'Volatility'` not moved** -- not named by the cell. Surfaced inside `S1`.
- **No PALETTE token minted**, so `'Metals'` and `'Commodities'` share `yellow500` -- *"Nothing else in
  the file moves."* `S3`.
- **`getSubAssetTextColor` not extended** -- same scope clause. `S4`.
- **`holdings-shared.tsx`'s duplicate map not touched and not re-filed** -- known as `W18-S2`, out by
  Andrew's word, and outside this order's `<paths>`.
- **No gitlink move, no promote, no DEV/PROD push, no branch move of DEV, no merge, no rebase, no push.**
- **No render** for `V5-AC7` -- recorded UNREAD with its reason rather than converted into a verdict.
- **`<status>` not flipped to `complete`** -- two mechanical criteria are FAIL by output. A VALID proof
  instance is not a met order.

## THE DRAIN

Branch `wk-posn-5-22-portal`, head `c475e31e7014cb7e18ccf0c1cb6a335ad0720044`, cut from
`e85f6eb84f3a1771a37011a7e77e372570bad02a`, destination `refs/drains/posn-5-portal`. Recorded at
`org/missions/D4/POSN/POSN_ASTTAX/ledger/PORTAL_REFS.md`, created by this order.
