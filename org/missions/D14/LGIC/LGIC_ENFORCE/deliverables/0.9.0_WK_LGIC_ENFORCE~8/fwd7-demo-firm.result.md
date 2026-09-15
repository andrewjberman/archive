# LGIC_ENFORCE.TO-EN-d-1 -- result (0.9.0_WK_LGIC_ENFORCE~8)

Firm N+1 is one row (FWD-7), run on a practice copy with the fixed fictitious firm `quillwater` / `qwt`.
The exercise record is `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/EXERCISE_FWD7.md` @c47028d8fc.

## Evidence chain

Scratch branch `prac-lgic-enforce-d1`, cut at CLOUD @652d3a2204. It has never been pushed (ls-remote: 0 heads on
origin) and is left in place, unmerged. The practice worktree was removed clean before the records commit.

1. `b4afbb00c7` -- the new pipeline `deliverables/0.9.0_WK_LGIC_ENFORCE~8/pipeline/qwt_positions.py`, which builds
   its locations only through `lookup()`, `key()` and `address()`.
2. `5e6573d25f` -- **expected_set**, `deliverables/0.9.0_WK_LGIC_ENFORCE~8/expected_diff.txt`: 9 files, derived from
   `generate()`'s known targets. Every one carries the registry hash, so one row changes all 9.
3. `92bc3b51bf` -- **generated**, one `scopes.json` row and the unedited output of
   `python lib/opal_naming.py generate --out .` (9 written, registry@8f946960611a1880).

## Criteria (run in the slot worktree; each prints one VERDICT line, exit 0 on PASS)

| id | verdict line | deciding evidence |
|---|---|---|
| D1-AC1 | `VERDICT: PASS-FIXED-FIRM` | `FIRM: {'long': 'quillwater', 'short': 'qwt'}` |
| D1-AC2 | `VERDICT: PASS-EXPECTED-FIRST` | expected_set 5e6573d25f is an ancestor of generated 92bc3b51bf |
| D1-AC3 | `VERDICT: PASS-DIFF-EQUALS-EXPECTED` | `EXPECTED: 9  ACTUAL (minus the registry): 9  ONLY EXPECTED: []  ONLY ACTUAL: []` |
| D1-AC4 | `VERDICT: PASS-ADDRESS-REFUSED` | `NAMING REFUSE data/quillwater/config.py:1 opal-data-quillwater/silver/x -> {source}/quillwater/silver/x`, gate rc 1 |
| D1-AC5 | `VERDICT: PASS-NAME-REFUSED` | `NAMING REFUSE data/quillwater/firm_settings.py:1 quillwater -> lookup('quillwater')`, gate rc 1 |
| D1-AC6 | `VERDICT: PASS-PIPELINE-WRITTEN` | the pipeline path is present at 92bc3b51bf |

## Controls

- Base DELTA-0 before the row: `generate --out .` at HEAD in the practice copy left `git diff --quiet` at rc 0.
- Discrimination for D1-AC4 and D1-AC5: the same two patches in the slot worktree, with no quillwater row,
  are not refused. The address grades RAISE (K1), WARN, rc 0; the name reads PASS 0 graded, rc 0.
- Pipeline: as a new file and at a `data/` path it reads `NAMING-GATE: PASS 0 graded`, rc 0. A mutant with one
  added line `LEGACY_FIRM = "qwt"` is REFUSED, rc 1.

## Rows filed

- `LGIC_ENFORCE-W8-S1` (OBSERVATION, INERT): D1-AC3 and D1-AC6 hold together only if the pipeline precedes
  expected_set, so it was committed first. This departs from the order's step listing.
- `LGIC_ENFORCE-W8-S2` (OBSERVATION, INERT): validate warns that the firm is not in NAMING_SCHEMA.json
  firm_forms. The row alone still generates, and the gate still refuses.

Nothing was written to AWS and no Terraform command ran.
