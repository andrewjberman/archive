# LT-a-2 (round 2) -- the re-derivation record: result

`0.9.0_WK_LGIC_LGCTFM~1` on `LGIC_LGCTFM.TO-LT-a-2-r2`, worktree
`C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-lgctfm-2-1`, branch
`wk-lgic-lgctfm-2-1`, cut from `7b411da26a`.

## What this cell produced

- `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/RE_DERIVATION_R2.json` -- the record.
- `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/rederive_r1.py` -- the
  instrument it cites, TRACKED and committed in the same commit (`337afad5a7`), four subcommands:
  `position`, `denominator`, `mechanism`, `probes [--only <criterion>]`.
- One channel row, `LGIC_LGCTFM-W1-S21`, appended by textual splice.

Nothing was re-graded and no round-1 fixed input was edited (R-43). `check_lt_r1.py` was RUN many times
and MODIFIED never; `git status --porcelain` on the fixed-input directory is clean.

## The third position, and why it is third

`rederive_r1.py position`:

- branch `wk-lgic-lgctfm-2-1`, HEAD `7b411da26a54755a0fc243ceab2e4dd46248806e`
- **not a producing branch:** `git branch --list wk-lgic-lgctfm*` returns exactly two refs, both
  round-2 worktrees. Every round-1 worker branch was deleted at its drain; those commits survive only
  in history, reachable by author.
- **not the grading checkout:** `git worktree list` shows the shared tree
  `C:/Users/AndrewBerman/Desktop/ajb_workspace` at `508eb695ca` on `CLOUD` -- a different path and a
  different commit. Rows `S10` and `S18` both record that `3.0.0_SA_CVO` graded round 1 there.

## The denominator, taken from the orders

`rederive_r1.py denominator` reads the task-order directory UNSCOPED (all 17 `.md` files):

```
order files in the directory (ALL rounds): 17
criterion elements carrying judgment="true", any round: 17
of those, in a round-1 order: 14
pinned by R2_BASE.json: 14
in the ORDERS but NOT pinned (must be empty): []
pinned but NOT found in a round-1 order (must be empty): []
```

## The partition: 10 re-derived, 4 not, of 14

| criterion | class | the one-line reason |
|---|---|---|
| D1R1-AC3 | RE-DERIVED | pins resolve; cited bytes at `:878` and `:915`; both arms PASS. Qualifier: the citation names `build_row` and the dict is inside `cmd_forks` -- right line range, wrong function name. |
| E1R1-AC9 | RE-DERIVED | method-doc sections at `:13`/`:110`; the quoted `comp-trigger --list` text reproduces verbatim; four arms PASS. |
| E2R1-AC5 | **NOT** | its second limb's only named invocation cannot reproduce its stated result at any vintage from the cell's own build commit. |
| E3R1-AC6 | RE-DERIVED | the walk deliverable still carries 271 tensions and `T-0271`; three arms PASS. The 271 -> 179 move is in the RUN's contract, not this artifact. |
| E4R1-AC9 | RE-DERIVED | flag declaration and default read as cited; three a4 arms PASS. |
| H1R1-AC5 | RE-DERIVED | pinned blob + quoted string, the one citation shape that cannot age; two arms PASS. |
| P1R1-AC6 | RE-DERIVED | 1626 packages, `R-0221` and `R-0221-PORT` present; three arms PASS. |
| R1R1-AC5 | RE-DERIVED | renderer pin resolves; `.claude/skills/draw/SKILL.md` present and tracked; `PRD:239-242` still lands on DEC-7 (checked by printing the bytes, not by searching). |
| S1R1-AC7 | RE-DERIVED | both pinned objects resolve with their cited content; three arms PASS. |
| S2R1-AC8 | **NOT** | one cited object is unreachable at the vintage cited: `git cat-file` rc=128, the path postdates the pin by 24 minutes. |
| V1R1-AC5 | **NOT** | FWD-4's oracle is a named person; four v1 arms PASS and none reads Andrew's word. |
| X1R1-AC6 | **NOT** | the live-plane window is unrepeatable; `x1-fwd10`'s PASS re-reads the cell's own record. |
| X2R1-AC4 | RE-DERIVED | the planted diff and the 437-line file read as claimed; both gate polarities reproduce. Qualifier: `x2-flag` is a vacuous PASS here. |
| X3R1-AC5 | RE-DERIVED | the claim addresses its DIFF.md BY RUN ID, which is why it survives; three of its four arms do not. |

## How the population was searched

Stated in full in the record's `unscoped_read`. In short: the census is of the MECHANISM and on a
DIFFERENT INSTRUMENT from the one that found the silent pair. `S18` grepped one helper name
(`base_ref()`); this parses the AST of `check_lt_r1.py`, builds the call graph over all 165 function
definitions, takes the denominator from the checker's own dispatch table (**67 arms**) and computes
transitive reachability of position-relative primitives -- 56 arms reach none, 11 do, and those 11 were
inspected by hand (4 confirmed position-resolved, 4 cleared as R-40 manifest-identity arms, 1 cleared as
a heuristic false positive, 1 recorded as a shared-directory denominator, 1 is `x2-flag`).

It reproduces `{x2-flag, x3-filed}` for the ambient-ref class exactly -- corroboration on a different
instrument, not repetition -- and finds three things the handed list does not name:

- `x3-diff` -> `FAIL-X3-COMMITTED-DIFF-REPRODUCES`, "absent: DIFF.md in the latest run" (a third
  `_last_two()` arm, in neither `R2_BASE`'s four nor `S18`'s evidence)
- `x2-flag`'s **second** ambient limb: the `git status --porcelain` read, which certifies the invoking
  worktree's cleanliness and not the cell's act
- `x3-two-runs`'s shared-directory bar: "run directories 5; with contract.json + VINTAGE.json: 5" --
  a `>= 2` test any cell's runs satisfy

And running the arms after the census found what no static census can see: **LIVE-BUILDER DRIFT**.
`e2-reproduce` reads `FAIL-E2-DESIRED-EQUALS-BUILDER` here, 273 of 278 rows reproducing, because
`lib/opal_naming.py grade()` now returns `advi-inf-accounts-v2-daily` where the frozen contract holds
`{system}-inf-accounts-v2-daily`.

## S10's repair, verified from a third position

`x1-r16` -> `PASS-X1-MARK-COMMIT-PRINTS-TARGETS` and `x1-footprint` -> `PASS-X1-REPO-FOOTPRINT-BOUNDED`,
run from a checkout that is neither the producing branch nor the grading tree. The false fails are gone.
`x2-flag` and `x3-filed` still read PASS on empty sets and are not repaired (R-43, correctly).

## Acceptance

| id | verdict | invocation | deciding line |
|---|---|---|---|
| A2R2-AC1 | PASS | `check_lt_r2.py a2-partition` | `VERDICT: PASS-A2-PARTITION-COVERS-ROUND-1` |
| A2R2-AC2 | PASS | `check_lt_r2.py a2-mechanism` | `VERDICT: PASS-A2-EVERY-CLASS-NAMES-ITS-MECHANISM` |
| A2R2-AC3 | PASS | `check_lt_r2.py a2-floor` | `VERDICT: PASS-A2-KNOWN-FOUR-ARE-A-FLOOR` |
| A2R2-AC4 | PASS | `check_lt_r2.py a2-instrument` | `VERDICT: PASS-A2-INSTRUMENT-IS-TRACKED` |
| A2R2-AC5 | UNVERIFIABLE-BY-INSTRUMENT | judgment | for `3.0.0_SA_CVO` at L9 |

`selftest-arms` was run FIRST, before any work: 28 arms, 10 positive-satisfiability,
`VERDICT: PASS-ARMS-DISCRIMINATE`. No arm was unsatisfiable by work believed right, so no blocking row
was owed on that head.

## Declared, not hidden

- The count of `not_re_derivable` EQUALS the floor of four. The arm says so itself and requires the
  `unscoped_read` note, which is why that note records the METHOD rather than the finding. The four are
  CRITERIA and the handed four are ARMS; only one of the four (X1R1-AC6) is a cell whose arms appear in
  the handed list.
- The arm-level census found MORE than four affected arms (seven, listed above). Those are recorded as
  arm findings and as a channel row rather than converted into criterion-level verdicts they do not
  support -- a criterion whose own evidence re-reads cleanly is re-derivable even when a sibling arm of
  its cell is not.
- One probe in this run was initially WRONG-OBJECT: the first needle for D1's FORK dict was the
  citation's own spelling `kind="FORK"`, which reads ABSENT because the file spells it `"kind": "FORK"`.
  The fix and the reason are in the instrument's own comment at that probe. An ABSENT that is really a
  wrong needle and an ABSENT that is really a missing blob read identically until you print the bytes.
