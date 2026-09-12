# FE-s-22 -- the evidence plane's two instruments

`IRPT_FNTEND.TO-FE-s-22` | worker `0.9.0_WK_IRPT_FNTEND~2` | branch
`wk-irpt_fntend-3-6-fe-s-22` (workspace) and `wk-irpt_fntend-3-6-fe-s-22` (portal)
| portal commit `25062fce` LOCAL | cut from CLOUD `e4298a984e` / DEV `baf230eb`.

**All eight mechanical criteria PASS by output**; `F22-AC9` is RECORDED for the
CVO at L9. The order is `complete`.

> **AMENDED MID-ORDER.** `F22-AC8` was first measured against the bar as cut,
> `0 fail`, and REFUSED -- row `IRPT_FNTEND-W2-S17`. The issuer then corrected
> that bar to `1 fail` with a name check (CLOUD `0e25c1d422`, issuer row `S45`),
> the amended face was read AT THAT COMMIT with a positive control, and the
> criterion was re-measured and now PASSES. Section 4 carries both readings. The
> measurement never changed; the bar did.

---

## 1. THE CLAIM MODEL, stated in the terms a later cell will apply

This is the section the order asks for by name. A later capture set does not need
to re-derive any of it; it declares a descriptor and calls the rule.

### 1.1 What a capture set declares

`portal/src/pages/InvestorReporting/__tests__/fe-s-22/capture-hash.ts`

```ts
interface CaptureEntry {
  file: string                  // the capture, relative to captureRoot
  fixture: string               // the fixture map it was taken against
  claims: readonly string[]     // fixture FIELD NAMES this capture claims to render
  requires?: readonly string[]  // EXACT fixture paths the claim needs to be REACHABLE
  criterion?: string            // for the reader; never used to classify
}
interface CaptureSetDescriptor { set: string; entries: readonly CaptureEntry[] }
```

and calls

```ts
const verdict = gradeCaptureSet(descriptor, fileSources(PORTAL_ROOT, CAPTURE_ROOT))
assertCaptureSet(verdict)   // throws on a refused set
```

`memorySources(fixtures, bytes)` is the same interface over seeded objects, for a
set that has no files yet.

### 1.2 The three things the rule says, and why they are three

| the set's state | verdict | what the reader does with it |
|---|---|---|
| fixtures differ in a CLAIMED field, captures BYTE-IDENTICAL | `REFUSED-CLAIMED-FIELD-COLLIDES` | the surface did not vary with its input -- a PAGE defect |
| fixtures differ in a CLAIMED field, captures DISTINCT | `DISTINCT-AS-ASSERTED` | the evidence is evidence |
| fixtures differ ONLY in an UNCLAIMED field, captures identical | `ADMITTED-UNCLAIMED-FIELD-ONLY` | legitimate; the set DECLARES the field |
| an entry's `requires` path is absent from its own fixture | `defectiveFixtures` | the page never received the state -- a FIXTURE defect |
| fixtures identical | `IDENTICAL-FIXTURES` | nothing is claimed either way |

The fourth row is the limb `IRPT_FNTEND-S44` asked for. It is reported
**SEPARATELY** from the first, never folded into it, because the two have
**different owners and different remedies**: "the page did not render a field it
claims" is fixed in a page, "the page never received the state that would let it
reach the field" is fixed in a fixture. A single REFUSED verdict carrying only
the first reason would send a reader to the wrong file.

### 1.3 Four rules a later cell must not re-derive

1. **The claim is DECLARED, and it is never a filename.** The round-2 set's
   claims live in `round-2-holdings.claims.json` and are joined to the round-2
   capture manifest **BY CRITERION**; `file` and `fixture` come from the
   manifest, the digest comes from the PNG bytes. No filename anywhere selects,
   exempts or classifies a capture -- a filename allowlist absorbs exactly the
   cross-fixture collision the rule exists to catch (CTO ruling 4).
2. **`claims` matches on a SEGMENT TAIL; `requires` matches an EXACT PATH.** A
   claim is a field NAME (`basis` matches `...data.nodes[].basis`); a
   precondition is a PLACE ON THE WIRE. Measured, and this is why: a suffix match
   on `status` hits
   `/api/scoped/investor-reporting/analysis/.data.extraction_validation.status`
   in all three round-2 maps -- a field on a different response, three levels
   inside `data`. A suffix rule would have read the precondition as SATISFIED in
   the one case it exists to fail. The rule prints that control itself:
   `PATH DENOMINATOR: 325 paths ... EXACT: 0 hit(s) ... SUFFIX 'status': 1 hit(s)`.
3. **An unstated precondition is NOT a met one.** `preconditionMet` is
   `null | true | false`: `null` means no `requires` was declared. A two-valued
   field would have encoded "nobody asked" as "it passed".
4. **The digest is taken from the BYTES.** `fileSources` re-derives sha256 from
   the file; it never reads a manifest's recorded hash back. A recorded hash and
   the file it names are two different claims and only one of them is evidence.

### 1.4 Array handling, stated because it is a real decision

The field census collapses array indices to `[]`, so `data.nodes[].basis` is ONE
comparable fact carrying the multiset of values across the array. Consequence a
later cell should know: **a reordering of equal nodes is NOT reported as a
difference.** That is deliberate -- a capture cannot see array order the page
does not render -- but a set whose claim IS the ordering must declare the
ordered field explicitly rather than relying on this census.

---

## 2. THE MEASUREMENT THE ROUND ASKED FOR: are those fixtures defective?

The issuer raised, as CONTEXT and not spec, that the three round-2 Holdings maps
carry no `status` member, so under the FE-s-19 seam they render identical panels
*by the contract*, and asked whether that makes them DEFECTIVE FIXTURES rather
than an admitted collision -- a question the CTO owns and has not ruled.

**The distinction is expressible, and both findings are TRUE OF THIS SET AT
ONCE. They are also INDEPENDENT, which corrects one clause of `S44`.**

```
ROUND-2 COLLISION REPRODUCED: 3 of 3
DEFECTIVE FIXTURES: 3 of 3
INDEPENDENCE: preconditions stripped -> defective=0, refused-pairs=3, refused=true
```

`S44` wrote *"without that limb the scoped rule would have ADMITTED this
collision as legitimate."* Measured, it would not have. The three maps **do**
differ in the claimed fields -- `basis` across observed/target, `classification`
across observed/missing-attribution -- so the collision arm refuses all three
pairs on its own with `requires` stripped out entirely. `S44`'s sentence uses
"the claimed field" for two different fields: the one the fixtures VARY, and the
one the wire must carry for the page to REACH it. Both are measured here, and
neither rescues the other.

**`F22-AC4` therefore passes AS WRITTEN** -- the order's premise that `basis` and
`classification` are claimed by those captures, and that the rule must refuse
them, holds on the bytes. Nothing was softened to make it pass. Row
`IRPT_FNTEND-W2-S18` carries the correction and the CTO's open question, with
`disarm_owner 1.0.0_SA_CTO`: **the code states the distinction; it does not rule
it.**

---

## 3. THE DETECTOR (`W1-S36`) -- one line, both directions

`scripts/ui-smoke.mjs:341`, the ONLY change to that file:

```diff
-console.log('LOC   :', state.loc, state.loc === route ? '' : ' <-- DID NOT LAND (auth redirect? bad route?)')
+console.log('LOC   :', state.loc, state.loc === new URL(ORIGIN + route).pathname ? '' : ' <-- DID NOT LAND (auth redirect? bad route?)')
```

`git diff --numstat` read `1  1  scripts/ui-smoke.mjs`. The file is the whole
portal's shared smoke instrument and nothing else in it moved.

**The test drives the SHIPPED BYTES, not a copy.** `ui-smoke.mjs` is a script --
importing it launches a browser -- and this cell's grant over it is one
comparison line, so it cannot be refactored to export the predicate. Re-typing
the comparison in the test would have graded a COPY, which stays green across any
future edit to the real line: precisely the defect class this cell exists to
close. So `smoke-detector.test.ts` reads the file, extracts the comparison
EXPRESSION out of `:341` and compiles it, **asserting its own denominator** --
exactly one line in the file mentions `DID NOT LAND` -- so a later edit that
moves, duplicates or reshapes the line fails this file loudly.

```
EXTRACTED from ui-smoke.mjs:341 -- state.loc === new URL(ORIGIN + route).pathname
LANDED QUERY ROUTE: no DID NOT LAND -- 3 of 3 landed cases clean
GENUINELY BAD ROUTE: DID NOT LAND -- 4 of 4 failed cases detected
  of which query-bearing: 2 of 4
DISCRIMINATION: 3 of 3 landed cases pass AND 4 of 4 failed cases fire
```

**Negative control, compiled the same way from the PRE-FIX expression:**
`PRE-FIX (state.loc === route): fired on 2 of 3 LANDED cases` and
`PRE-FIX indiscriminate: fired on 4 of 4 FAILED and 2 of 2 LANDED query-bearing
cases -- the same output for both states`. That last line is the whole finding:
the old predicate produced identical output for a run that landed and a run that
was redirected, which is what "not a detector" means. Fixing an always-firing
detector by making it never fire satisfies `F22-AC6` alone; `F22-AC7` and the
discrimination arm are what make that impossible.

**And it was exercised live, not only at the unit level.** The `F22-AC5` capture
ran through the fixed instrument and printed `LOC   : /investor-reporting/print`
with **no** `DID NOT LAND` line, beside `REFS RESOLVED: 1 of 1`. That same
capture under the pre-fix bytes is the class of run that produced round 2's five
spurious lines.

---

## 4. `F22-AC8` -- REFUSED AT THE BAR AS CUT, PASSING AT THE CORRECTED ONE

Both readings are kept, because the second one is only trustworthy beside the
first: **the measured world is identical in both, and only the bar moved.**

**As cut (`0 fail`) -- REFUSED.** Measured: `446 pass / 1 skip / 1 fail`,
`2021 expect() calls`, `Ran 448 tests across 75 files`, rc=1. BLOCKING row
`IRPT_FNTEND-W2-S17`, which stands unchanged -- the channel is append-only and a
landed row is never edited.

**Corrected (`1 fail`, with a name check) -- PASSES.** `2.0.0_SA_COO~F` corrected
the bar on CLOUD at `0e25c1d422` after this worktree was cut, carrying its own
row `S45`: the `0 fail` was a prediction that `F18-AC3`'s collision would clear
once the seam landed, and it cannot (row `S44` -- the three Holdings smoke maps
carry no `status` members and no round-3 cell holds the fixtures). Re-measured
against the corrected bar, with the dev server restarted on 5182 so the run is
comparable:

```
FAIL-MARKED LINES (denominator of failures): 1
  FAILING TEST NAME: F18-AC3 -- the captures are the files the manifest claims
                     > UNIQUE HASHES -- no two entries share a hash
446 pass / 1 skip / 1 fail / 2021 expect() calls
Ran 448 tests across 75 files.
```

Identical totals to the pre-amendment run, as expected -- the amendment touches
no source, no fixture and no test file. **The name check is answered with its own
denominator:** exactly one fail-marked line, and it IS `F18-AC3`'s. No second
failure and no different one, so the corrected bar's BLOCKING condition did not
trigger. The failing test is still `__tests__/fe-s-18/manifest.test.ts`, still
outside this order's grant, and this cell's own 13 tests still read 0 fail.

**How the amendment was taken** (procedure row `IRPT_FNTEND-S43`, invented by the
worker on slot ~1 under exactly this condition): `git merge-base --is-ancestor
0e25c1d422 HEAD` = FALSE and `git cat-file -t 0e25c1d422` = `commit` -- reachable
in the shared object store, **absent from this branch**, so this tree's own copy
still held the retracted bar and grading from it would have been wrong. The face
was read with `git show 0e25c1d422:<order>` (12125 bytes, rc=0) **beside a
positive control**, because a mangled `git show` returns clean-empty on this box:
the same command on a non-existent path at the same ref returned `fatal: path ...
does not exist in '0e25c1d422'` at rc=128, not empty. The diff was bounded before
anything was written -- 115 lines each side, **exactly two differing** (61 and
62), both inside the `F22-AC8` block, `<status>` `pending` on both sides -- and
only those two lines were written, CRLF preserved (114/114 measured after the
write), the result verified byte-identical to the blob modulo EOL.
`git diff --numstat` read `2	2`. No merge, rebase, `checkout --` or `clean` was
run in either repo. Row `IRPT_FNTEND-W2-S19` carries the re-measurement; it
carries **no** `adjudicates` field, because dispositioning `W2-S17` is the CVO's
act at L9 and not this worker's.

**`F22-AC1` was not re-run, and that is a decision with a reason rather than an
omission:** the only file this pass changed is the task order's own markdown,
which lives in the workspace repo and is not in the portal's TypeScript program
(`tsconfig.app.json` includes `src`). No source file, fixture or test file moved,
so the recorded `tsc -b --noEmit` rc=0 stands over the same program. The other
six criteria were not re-run on the same ground.

## 5. WHAT THIS CELL DID NOT TOUCH

- `__tests__/fe-s-18/` -- carried untouched by CTO ruling 1. This cell READS the
  round-2 manifest and the round-2 PNGs and writes nothing there.
- Anything in `scripts/ui-smoke.mjs` beyond the one comparison.
- The fixture maps. The three Holdings maps are measured here and unmodified;
  giving them distinct `status` members is the round-4 fixture work `S44` names,
  and it is in no round-3 cell's grant.

## 6. FILES

| path | what |
|---|---|
| `portal/scripts/ui-smoke.mjs` | the one-line landing comparison |
| `portal/src/pages/InvestorReporting/__tests__/fe-s-22/capture-hash.ts` | the reusable scoped rule |
| `portal/src/pages/InvestorReporting/__tests__/fe-s-22/capture-hash.test.ts` | `F22-AC2` / `F22-AC3` / `F22-AC4` |
| `portal/src/pages/InvestorReporting/__tests__/fe-s-22/round-2-holdings.claims.json` | the round-2 set's declared claim model |
| `portal/src/pages/InvestorReporting/__tests__/fe-s-22/smoke-detector.test.ts` | `F22-AC6` / `F22-AC7` |
| `portal/src/pages/InvestorReporting/__tests__/fe-s-22/ambient-shims.d.ts` | type-only node builtins |
| `org/.../deliverables/0.9.0_WK_IRPT_FNTEND~2/fe-s-22_landed_query_route_1440.png` | the `F22-AC5` capture |

Push state: **LOCAL** on both branches. Portal is FROZEN; no push, merge, rebase,
`checkout --` or `clean` was run in either repo.
