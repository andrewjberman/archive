# LGIC_LGCTFM.TO-LT-r-1-r1 -- renderer result (round 1)

**Cell:** LT-r-1 (the two flow diagrams, rendered never by hand). **Assignee:** `0.9.0_WK_LGIC_LGCTFM~3`.
**Commit:** `d795f75122` on `wk-lgic-lgctfm-1-3` (LOCAL).

## What was built

`lib/lgctfm_render.py` (new, stdlib + ASCII only, DEC-2's contract). Two verbs:

- `render <contract.json> --out <dir>` writes `<dir>/flow.current.md` (built from `rows[].current` and
  `edges[]` only) and `<dir>/flow.desired.md` (built from `rows[].desired`, FORK rows'
  `one_job`/`canonical_member`, and `edges[]` only -- **no `current.*` cell is read while building it**).
- `check <contract.json> --out <dir>` regenerates both files in memory and diffs them byte for byte
  against the committed pair, exiting 0 on a match, printing `STALE <file> (absent|differs)` and exiting
  non-zero otherwise.

Column layout reads DEC-7's "triggers left, compute centre, tiers right, serving routes reading them" as a
left-to-right READING ORDER (TRIGGERS section, then COMPUTE, then TIERS, then SERVING), each row printed as
one full-length line rather than squeezed into a fixed-width grid -- the first version of this renderer used
a side-by-side grid and truncated every field to 40 characters, which silently dropped almost all of a
row's real values (SKILL.md's "use the real names ... never generic" is violated by truncation as surely as
by a placeholder). Caught before commit by reading the actual rendered output, not just the checker's rc.

`NODE_TYPE_COLUMN` assigns all 33 schema `node_type` values (org/standards/LGCTFM_CONTRACT.schema.json
`$defs.node_type`) to exactly one of the four columns, MECE by count (7 + 8 + 8 + 10 = 33); a node_type the
map does not carry falls into SERVING defensively rather than being silently dropped (none does today --
the map is exhaustive over the enum as read).

## Acceptance (post-commit re-run, worktree HEAD `d795f75122`)

| id | subcommand | verdict |
|---|---|---|
| R1R1-AC1 | r1-identical | PASS-R1-TWO-RENDERS-BYTE-IDENTICAL |
| R1R1-AC2 | r1-edit | PASS-R1-EDIT-CHANGES-ONLY-ITS-ROW |
| R1R1-AC3 | r1-hand-edit | PASS-R1-HAND-EDIT-FAILS-CHECK |
| R1R1-AC4 | r1-fresh | PASS-R1-FRESH-RENDER-PASSES-CHECK |
| R1R1-AC5 | judgment | UNVERIFIABLE-BY-INSTRUMENT, for `3.0.0_SA_CVO` at L9 |

`check_lt_r1.py selftest-arms` also shows the `r1-edit` PURE CORE (`core_edit`, the stray-line detector
itself) PASS against its own doctored fixture ("a stray line changed").

## Mutant / determinism evidence (self-supplied, beyond the fixed battery)

- Ran `r1-identical` twice in direct succession; both runs printed `VERDICT: PASS-R1-TWO-RENDERS-BYTE-IDENTICAL`
  (the arm itself already asserts byte-identity across its own two renders per invocation; this is a second,
  independent invocation showing the same result, not a repeat of the same process).
- Mutant: `lib/lgctfm_render.py` temporarily moved out of the worktree (restored immediately after;
  `git status --porcelain -- lib/lgctfm_render.py` clean both before and after) and `r1-fresh` re-run:
  printed `absent: lib/lgctfm_render.py` and `VERDICT: FAIL-R1-FRESH-RENDER-PASSES-CHECK` -- the checker's
  own convention (a missing input is a FAIL verdict, never a traceback).

## Declared exclusions

- The exact box-drawing skeleton in `.claude/skills/draw/SKILL.md` (nested boxes, `┌─┐` glyphs)
  is not reproduced literally; the renderer uses a plain-ASCII sectioned list in DEC-7's reading order
  instead, prioritising full, untruncated real values (name/arn/drift/live/client_facing on current;
  form/builder/verdict on desired) over the skeleton's exact glyphs. R1R1-AC5 is the judgment criterion
  this reads against; the trade is stated here rather than hidden.
- The two "planes" in `.claude/skills/draw/SKILL.md` are query-plane vs build-plane; this renderer's two
  FILES (current vs desired) are a different split named by DEC-7 itself, not the skill's own plane split.
  Declared: DEC-7's split governs since T7/LT-r-1 cites DEC-7, not the skill's generic template verbatim.
