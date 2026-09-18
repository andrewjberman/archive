# LT-p-2 (round 3) -- `dependencies` -> `step_dependencies`

`0.9.0_WK_LGIC_LGCTFM~1` on `LGIC_LGCTFM.TO-LT-p-2-r3.step-dependencies`, branch
`wk-lgic-lgctfm-3-1b`, worktree
`C:\Users\AndrewBerman\Desktop\ajb_workspace\.worktrees\wk-lgic-lgctfm-3-1b`.

Code + canon: `df4753e185`. Surprise rows: `18223979a2`. Both LOCAL on the branch (not pushed; a
worker never pushes).

---

## THE NUMBERS THE ORDER ASKS FOR

| quantity | value | instrument |
|---|---|---|
| packages in the plan | **1074** | `check_lt_r3.py p2-renamed`, engine `plan` on a scratch copy of the graded run |
| packages carrying the OLD `dependencies` | **0** of 1074 | same |
| packages carrying `step_dependencies` | **1074** of 1074 | same |
| populated (non-empty) values | **895** of 1074 | `check_lt_r3.py p2-values-preserved` |
| **values that DIFFER, old vs new** | **0** of 1074 | same, compared package by package |
| graded-run manifest files re-hashed | 8 of 8, **0 differ** | `git hash-object`, the instrument `HASHES.json` itself names |

179 packages carry an empty list (1074 - 895): they are the MAP step, which has no prior R19 step.

---

## WHAT CHANGED -- three sites, two files

**1. `lib/opal_lgctfm.py:131` `PACKAGE_FIELDS`** -- the second of the eight fields is now
`step_dependencies`. Tuple length, order and every other member unchanged. A comment above it records
the old spelling, why it moved, and that a real cross-row relation is FWD-6's separate
`resource_dependencies`.

**2. `lib/opal_lgctfm.py` `_build_one_package()`** -- the key is renamed; the expression that produces
the value (`["%s-%s" % (row_id, prior_step)] if prior_step else []`) is byte-identical. That is why
the values arm reads 0 of 1074 differ rather than merely "no exception raised".

**3. `infra/logic/10_LEGACY_TRANSFORM.md` s.Plan** -- the eight-field list names the new spelling, plus
a paragraph recording the measured basis (895 same-row, 0 cross-row), that the rename moves the NAME
only, that runs frozen before it keep the old spelling under R-43, and that `resource_dependencies` is
deliberately NOT emitted empty.

**NOT changed, deliberately:**

- **No `resource_dependencies`, not even empty.** WHAT YOU BUILD 4: an empty field named for a relation
  is the same hazard in a new spelling. It is FWD-6's, after FWD-1.
- **Nothing under `workflows/legacy_transform/`.** Both arms copy the graded run to a temp directory;
  `git status --porcelain workflows/` reads 0 paths after every run in this session, including the
  controls.
- **No discovery, coverage-block or schema change** -- `LT-e-5`'s, already drained.
- **`render_plan_md()`** -- see row `LGIC_LGCTFM-W1-S30`: it never printed the field under either
  spelling, so there was nothing to rename there and nothing was invented to make the premise true.

---

## ACCEPTANCE -- 3 of 3 mechanical PASS by output, 1 judgment recorded

The checker's own controls were run FIRST, before any edit: `check_lt_r3.py selftest-arms` ->
**27 arms, 9 POSITIVE built from `R3_BASE.json`'s own shape, 2 REAL negatives on the graded run, 16
mutant/other, `VERDICT: PASS-ARMS-DISCRIMINATE`**. Re-run unchanged after the commit.

- **P2R3-AC1** `p2-renamed`: `packages 1074; carrying \`dependencies\` 0; carrying
  \`step_dependencies\` 1074` -- `PASS-P2-RENAMED`.
- **P2R3-AC2** `p2-values-preserved`: `values compared package by package: 0 of 1074 differ; 895
  populated` -- `PASS-P2-VALUES-PRESERVED`.
- **P2R3-AC3** `p2-old-untouched` (guard-shaped, PASS at the cut and still PASS):
  `graded run's 8 manifest file(s) re-hashed with git hash-object (HASHES.json's own instrument): 0
  differ` -- `PASS-P2-OLD-UNTOUCHED`.
- **P2R3-AC4** JUDGMENT, `3.0.0_SA_CVO` at L9. No verdict offered. The record it needs is the census
  below and row `LGIC_LGCTFM-W1-S31`.

---

## CONTROLS

**MUTANT -- the adversarial move the preflight names, driven for real.** A copy of the committed
engine under a scratch tree, one line changed so every package emits `"step_dependencies": []`
(the cheapest move that satisfies AC1), run over a copy of the graded run:

```
core_p2_renamed(mutant) = True    packages 1074; carrying `dependencies` 0; carrying `step_dependencies` 1074
core_p2_values(mutant)  = False   values compared package by package: 895 of 1074 differ; 895 populated
core_p2_renamed(real)   = True    packages 1074; ... `step_dependencies` 1074
core_p2_values(real)    = True    values compared package by package: 0 of 1074 differ; 895 populated
```

So AC1 alone is forgeable and AC2 is what stops it -- and AC2 discriminates the exact forgery, at the
exact count of populated values. `lib/opal_lgctfm.py` in the worktree was never edited for this; the
mutant is a copy.

**DETERMINISM.** The committed engine's `plan` verb on two independent copies of the graded run:
`plan.json` sha256 `fab24c9f068152b8...` and `plan.md` sha256 `5469d080f91e7b0e...` on BOTH runs,
byte-identical. `workflows/` dirty paths after all of it: 0.

---

## EVERY PLACE THE OLD NAME STILL APPEARS, AND WHY IT STAYS

Census instrument: `comp-find '"dependencies"' --all --files` -- **8235 hit(s) across 36015 file(s)
scanned, corpus=all**, plus `comp-read <file> --enumerate` per file. The overwhelming majority of that
denominator is `package.json`/`bun.lock`/`package-lock.json` npm manifests, which share only the word.
Scoped to the LGCTFM plan package field:

| where | band | why it stays |
|---|---|---|
| `lib/opal_lgctfm.py:129` | COMMENT | The VERBATIM ATOM_DECOMP `SKILL.md` quote ("one objective plus explicit dependencies, reads, writes, ..."). Editing a quotation to match a rename falsifies the citation. `(?<![_a-z])dependencies` over the file at the pin returns 2 hits, **both COMMENT, CODE=0** -- this quote and my own rename note. |
| `infra/logic/10_LEGACY_TRANSFORM.md` s.Plan | PROSE | The new paragraph NAMES the old spelling on purpose, so a reader of an old run can resolve it. |
| `projects/ATOM_DECOMP/skill/atomic-decomposition/SKILL.md:71` and `org/tier1_exec/1.0.0_SA_CTO/deliverables/ATOM_DECOMP_SPEC/skill/atomic-decomposition/SKILL.md:57` | DOC (skill) | The upstream doctrine sentence about atomic work packages in general. Not this engine's field, not in `<paths>`, and the concept it names is the one this rename PRESERVES. |
| `workflows/legacy_transform/blackdiamond-49financial/*/plan.json` (5 runs) | frozen artifact | **R-43**: frozen runs are not rewritten. AC3 is the guard that proves they were not. |
| `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~2/plan_r1/plan.json` | frozen deliverable | Round 1's graded artifact. Same reason. |
| `.../fixed_inputs/r1/check_lt_r1.py:84` `PACKAGE_FIELDS` | **a CHECKER, and the one that matters for AC4** | Outside `<paths>`, so not edited. Measured BOTH ways: its `p1-fields` arm reads the FROZEN `plan_r1/plan.json` and still reads **PASS** (`packages 1626; missing one of the eight fields: 0`), while the SAME core driven over a plan built by the edited engine reports **1074 of 1074 missing `['dependencies']`**. That is an EXPOSURE, not an incident: nothing was admitted, round 1's evidence stands, and the remedy is one token in a round-1 fixed input. Row `LGIC_LGCTFM-W1-S31`, `disarm_owner 2.0.0_SA_COO~G`. |
| `.../fixed_inputs/r3/check_lt_r3.py` | the round-3 checker | Correct by design: `core_p2_values` must read the OLD field on the old plan to compare it against the new one. |
| this order file and this cell's own records | record | They are about the rename. |

## SURPRISE ROWS

- **`LGIC_LGCTFM-W1-S30`** (OBSERVATION / INERT) -- the order names three write sites and one does not
  exist: `render_plan_md()` never printed the field under either spelling.
- **`LGIC_LGCTFM-W1-S31`** (OBSERVATION / ARMED, `disarm_owner 2.0.0_SA_COO~G`) -- round 1's
  fixed-input checker still names the old spelling; measured PASS today against its frozen plan, and
  1074 of 1074 missing against a fresh one.

Spliced textually into the ONE fence of `INVESTIGATION_v1.md` that parses as a list: 46 insertions, 0
deletions; 6 fences before and after, all parse; list 33 -> 35 rows; non-ASCII CHARACTERS 0 -> 0;
backslash-u 0 -> 0; byte delta 6008 = the inserted block exactly, every byte before the insertion point
identical. Ids minted after re-measuring every document under the channel at write time (highest `S29`
across 136 occurrences in 3 documents).
