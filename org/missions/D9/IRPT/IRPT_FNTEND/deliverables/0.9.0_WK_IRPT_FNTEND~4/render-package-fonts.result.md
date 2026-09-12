# IRPT_FNTEND.TO-FE-s-24 -- RESULT

**Worker:** `0.9.0_WK_IRPT_FNTEND~4` (slot ~4, queue position 1) · **Cell:** `FE-s-24` · **Round 3**
**Workspace:** `/c/tmp/wk-irpt_fntend-3-4-fe-s-24`, branch `wk-irpt_fntend-3-4-fe-s-24` (cut from CLOUD @9762d5b8a3)
**Portal:** `/c/tmp/wk-irpt_fntend-3-4-fe-s-24/portal`, same branch name (cut from DEV @f0443ba8)
**Push state:** LOCAL in BOTH repos. Nothing pushed, merged, rebased, checked out or cleaned. Portal is frozen.

---

## OUTCOME

All seven criteria PASS by output. `proof-of-spec-check.py` rc=0 (VALID). Two surprise rows filed,
both OBSERVATION / INERT. The task order's `<status>` is flipped to `complete` in the same commit as
the proof instance and this file.

## WHAT CHANGED, AND WHY IT IS NOT A ONE-CHARACTER EDIT

`RENDER_PACKAGE.fonts` named three faces while `fontPackage.files` declared four. FE-s-18 packaged
Lato-Bold.ttf (700) and could not name it in the flat array, because
`__tests__/fe-s-4/manifest.test.ts:216` pinned that array's length to a **typed-in 3** and fe-s-4 was
outside FE-s-18's write grant. That worker named the blocker (`IRPT_FNTEND-W1-S28`) and left it, which
was correct. This cell owns both files.

**A typed-in 4 would have reproduced the defect one face later.** The expected face list is now read off
the package itself:

```ts
const derived = pkg.fontPackage.files.map((file) => file.name)   // the PACKAGE's own declaration
const flat    = pkg.fonts.slice()                                 // what is being graded
```

and the assertion is on **names and order**, not on a count (`expect(flat).toEqual(derived)`). Three
files moved, all inside `<paths>`:

| file | change |
|---|---|
| `render/manifest.ts` | `fonts` gains `'Lato-Bold.ttf'` in `fontPackage.files` order; the WARN paragraph explaining the shortfall is replaced by the closing note and the three-file rule for adding a face. Nothing else in the file moved. |
| `__tests__/fe-s-4/manifest.test.ts` | the literal-3 pin is gone and is NOT replaced by a 4: a derived-agreement arm, a seeded-disagreement arm in both directions, and a self-source scan. |
| `__tests__/fe-s-17/fonts.test.ts` | the "SHORT subset, and this test says by how much" arm returns to the EQUALITY it was before FE-s-18, graded against `fonts.manifest.json` -- the hashed record, a **different source** from the one fe-s-4 derives its count from. |

**No font file was touched.** Four `.ttf` on disk, four declared, every sha256 MATCH, including
`Lato-Bold.ttf` 656544 B `sha256=8a0aace75d33794eece4b28187bfc1df0bbd2888b5d8a56e01788c8d65d16be1`.
`git show --stat 5500c4ae` names three paths and nothing under `render/assets/`.

## CRITERIA -- deciding line, verbatim

| id | bar | deciding output | denominator | verdict |
|---|---|---|---|---|
| F24-AC1 | `rc=0` | `$ tsc -b --noEmit` / `rc=0` | whole-program `tsc -b`, portal `src/` via project references | PASS |
| F24-AC2 | `FONT NAMES: 4 of 4` | `FONT NAMES: 4 of 4` | 4 derived names (off `fontPackage.files`) vs the flat array, both printed in full; assertion on names AND order | PASS |
| F24-AC3 | `COUNT IS DERIVED, NOT LITERAL` | `LITERAL COUNT COMPARISONS: 8 of 8 found, 0 of them grade the FONT count` / `POSITIVE CONTROL: scan of a seeded typed-in line found 1 hit` / `FONT NAME COUNT IS DERIVED, NOT LITERAL` | 0 of 8 over 352 source lines, read at run time via `import.meta.url`; scoping filed as `W4-S3` | PASS |
| F24-AC4 | `DISAGREEMENT CAUGHT: 1 of 1` | `SEEDED (flat short by one): flat 3, packaged 4, missing Lato-Bold.ttf` / `DISAGREEMENT CAUGHT: 1 of 1` (+ reverse direction, 1 of 1) | 1 of 1 ordered direction + 1 of 1 reverse; seeded on COPIES, real package re-asserted in the same run | PASS |
| F24-AC5 | `FONTS: 4 of 4` | `FONTS: 4 of 4` / `BOLD ON DISK: ... sha256=8a0aace7...16be1` / `FLAT FONT LIST: 4 of 4 packaged faces named` | every `.ttf` re-hashed from bytes vs `fonts.manifest.json`; 11 pass 0 fail | PASS |
| F24-AC6 | `0 fail` | `31 pass` / `0 fail` / `Ran 31 tests across 5 files.` | 31 of 31 across 5 of 5 files in the folder (baseline 28; +3 are this cell's arms) | PASS |
| F24-AC7 | `2 fail` | `422 pass` / `1 skip` / `2 fail` / `Ran 425 tests across 69 files.` | 2 of 425 across 69 files; the SAME two as the pre-edit baseline (419 pass / 2 fail) | PASS |

### F24-AC7 -- both failing test names, as ordered

```
(fail) producer fixtures > the generated wire types were generated from THESE schemas
(fail) F18-AC3 -- the captures are the files the manifest claims > UNIQUE HASHES -- no two entries share a hash (FAILS at this commit; see the file header)
```

The first is the stale schema pin (FE-s-20's; one contract, `StatusEnvelope`, per row `IRPT_FNTEND-S35`'s
correction of S33). The second is the capture-hash collision (FE-s-19's). Both are the ordered pair, and
**both were measured on this worktree BEFORE any file was edited** -- baseline 419 pass / 1 skip / 2 fail,
same two names. No third failure appeared; the +3 pass is exactly this cell's three new arms. No BLOCKING
row was owed on this criterion.

## CONTROLS

- **Mutant (live, on the committed artifact), two arms, both FIRED.** ARM A removed `Lato-Bold.ttf` from
  the flat array -> `FONT NAMES: 3 of 4`, `NOT NAMED IN THE FLAT LIST: Lato-Bold.ttf`, 9 pass **3 fail**.
  ARM B instead renamed the fourth entry on the PACKAGE side -> `NOT NAMED IN THE FLAT LIST: Lato-Boldx.ttf`,
  `NAMED BUT NOT PACKAGED: Lato-Bold.ttf`, 9 pass **3 fail**. ARM B is the one that matters: a check that
  derived its expectation from the array it grades would not notice it at all. Both reverted; `git diff --stat`
  clean.
  **Disclosed:** the first run of this harness crashed inside ARM A (a `subprocess` call could not resolve
  the MSYS-style bun path on the Windows plane) and left the mutated bytes on disk. Restored from
  `git show HEAD:<path>` with the worktree EOL re-applied -- **not** `git checkout`, which this worker may
  not run -- and `git diff --stat` verified clean before anything else ran. A `finally` limb was added so a
  dead runner can no longer leave a mutant applied. No commit was taken while the mutant was on disk.
- **Determinism: STABLE.** Two same-input runs, timing lines filtered, 43 lines diffed byte for byte,
  empty diff. Stable by construction -- no clock, no network, no directory-order dependence, no seed.

## SURPRISE ROWS

Both in `org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md` @`77b714db26`.

- **`IRPT_FNTEND-W4-S3`** (OBSERVATION / INERT) -- F24-AC3's zero is reachable only when the scan is scoped
  to the FONT count. The file already carried two literal count comparisons against a digit before this cell
  existed (`files.length > 8`, `templates.length).toBe(2)`), neither about fonts; an unscoped zero would mean
  deleting a bar this cell does not own, and the only derivation available for the template count is
  tautological with the assertion on the next line. The unscoped denominator (8) and every hit are PRINTED.
- **`IRPT_FNTEND-W4-S4`** (OBSERVATION / INERT) -- the face orders ids "starting at `IRPT_FNTEND-W4-S1`
  (the W4 coordinate has no round-3 rows yet; if the file carries no W4 sequence, yours opens it)". Both
  halves of that parenthetical are true and the conclusion is still wrong: `INVESTIGATION_v1.md` holds
  W4-S1 and W4-S2 from round 1, and the row gate allocates over the whole **plane**, not per document. The
  ordered id was minted, staged and BLOCKED by the gate's own run; the uncommitted block was backed out
  (file verified byte-identical to HEAD) and re-minted at the next unused numbers. The trap is Rule 24's:
  the pre-mint re-read was scoped to the document the face named, and a zero from a scoped domain read as
  an absence.

## COMMITS (both LOCAL)

| repo | commit | subject |
|---|---|---|
| portal | `5500c4ae` | `FE-s-24: RENDER_PACKAGE.fonts names all four packaged faces, and the count it is graded against is DERIVED from the package` |
| workspace | `77b714db26` | `rows(IRPT_FNTEND-W4-S3, W4-S4): F24-AC3's unscoped zero is unreachable inside this grant, and the face's ordered row id collides across the channel plane` |
| workspace | this commit | proof instance + this result file + the `<status>` flip to `complete` |

An earlier workspace commit attempt was REFUSED by the surprise-row gate on the ordered id `W4-S1` as a
cross-document collision; that refusal is `W4-S4`'s evidence and is the only gate refusal in this order.

## PROOF

`org/missions/D9/IRPT/IRPT_FNTEND/deliverables/0.9.0_WK_IRPT_FNTEND~4/IRPT_FNTEND.TO-FE-s-24.render-package-fonts.proof_of_spec.json`

```
python .tools/proof-of-spec-check.py <instance> F24-AC1,F24-AC2,F24-AC3,F24-AC4,F24-AC5,F24-AC6,F24-AC7
proof-of-spec-check | structural=jsonschema | acceptance rows=7 | violations=0
  checker-vintage: 709b9556a3 2026-09-10T14:37:30Z
  alignment-forward-1 (criterion -> cell): 7/7 criteria carry >=1 cell_ref
  alignment-backward (declared cell -> criterion): 1/1 cell(s) declared in the TO's <owned_cells> are reachable
  surprises-frame: 2 entries; 2 open with a row id; 2 resolve to a channel row; mode ENFORCE
VALID (rc=0)
```

Run BEFORE the `<status>` flip. Three artifact rows read `UNRESOLVED-HERE` because their pins are portal
commits and the portal is a separate repository -- announced by the checker, not asserted by it.

## FOR THE ADJUDICATOR

This order carries **no judgment criterion**; every bar is mechanical by output, so nothing here is
self-graded. Two things are left open and are NOT decided by this worker: whether F24-AC3's wording should
be narrowed to "the font count" in future faces (or the two out-of-scope literals cut by a cell that owns
them), and whether a task-order face should name a starting row number at all when only the allocator can
know it. Both are carried on their rows.
