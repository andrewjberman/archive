# LGIC_LGCTFM.TO-LT-x-3-r1 -- second-run-diff -- result (0.9.0_WK_LGIC_LGCTFM~2)

Cell `LT-x-3` (PRD `LGIC_LGCTFM_PRD.md` DEC-12, T12; decomp v1.1 round-1 cell `LT-x-3`, sections 3
and 10). A second real run of `blackdiamond-49financial`, its `run_home.py diff` against the prior
run, and the OPENED-tension row it produces. No engine or schema code touched.

## What ran

1. **Practice/real wave, in a scratch worktree.** `git worktree add ../wk-lgic-lgctfm-1-4-scratch -b
   scratch/wk2-lt-x3-practice HEAD` (never pushed). Inside it:
   `python lib/opal_lgctfm.py run --subject 49financial --run-home-subject blackdiamond-49financial
   --seed opal-data-bd --seed opal-data-49financial --seed-loc opal-data-49financial:_campaign/
   --root workflows/legacy_transform`. The `--seed-loc` folds in one forks pass over a genuinely
   live, previously-unwalked S3 prefix: `.tools/aws s3api list-objects-v2 --bucket
   opal-data-49financial --prefix "_campaign/" --delimiter /` (read-only) returns exactly one child
   prefix, `_campaign/c02-reemit/`, holding one live object
   (`_campaign/c02-reemit/c02_reemit_mirror_pull.py`). Wrote 185 rows / 180 tensions (the prior run:
   184 / 179). `run_home.py`'s own forks-row renumbering (`_renumber_forks_rows`, starts past the
   walk's own max `R-####`) leaves every walk-only row_id untouched, so this is a small, real,
   deliberate change the walk can see -- not a fabrication and not a reorder of anything already
   there. The new run directory (`20260918T002711Z-caf0983`) was copied into
   `workflows/legacy_transform/blackdiamond-49financial/` here, then the scratch worktree/branch
   were deleted (`git worktree remove --force`, `git branch -D`).
2. **The diff.** `python workflows/legacy_transform/run_home.py diff
   workflows/legacy_transform/blackdiamond-49financial/20260917T233143Z-a89fd61
   workflows/legacy_transform/blackdiamond-49financial/20260918T002711Z-caf0983` (the prior run being
   the previously-committed last run of this subject) -- output committed verbatim as
   `workflows/legacy_transform/blackdiamond-49financial/20260918T002711Z-caf0983/DIFF.md`: `CLOSED: 0`,
   `OPENED: 1` (`R-0185|A3|GRAMMAR|R1`), `UNCHANGED: 179`. `MANIFEST.md` recompiled
   (`run_home.py manifest`) to list all four runs now on disk.
3. **The row.** One OPENED tension, one row:
   `org/missions/D8/ADVI/ADVI_FIRMBKTS/surprise-channel/investigations/INVESTIGATION_v1.md`
   `ADVI_FIRMBKTS-W2-S10` (class `OBSERVATION`, `hazard_standing` `INERT`), appended at the end of
   the file's last JSON array, every pre-existing row's bytes untouched (verified: the file's five
   `json` fences all still parse, the last now carrying 5 of 5 objects instead of 4).

## Why this row, R-0185

`lib/opal_naming.py grade('_campaign/c02-reemit/', 'S3Key')` raises `"K1: segment 1 '_campaign' is
neither a source nor a tier"` -- reproduced directly against the module at this seat, and matching
the row's own `desired.verdict` (`RAISE`) in the committed `contract.json`. Its `current.drift_class`
is `LIVE-no-DECLARED` (INFERRED) and `current.declaration` is `ABSENT` (terraform tree read) -- the
literal shape the WORKER FACE's own example names ("a DECLARE: a declaration entry that closes a
LIVE-no-DECLARED tension"), here on the OPENING side: no prior run of this subject ever seeded
`_campaign/`, so this row and its tension did not exist before this run.

## Criteria

Every invocation ran from `<WS>` =
`C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-lgctfm-1-4` against
`org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_lt_r1.py`.

- **X3R1-AC1** (`x3-two-runs`): PASS-X3-TWO-RUNS-ON-ONE-SUBJECT. 4 run directories under the subject,
  all 4 carrying `contract.json` + `VINTAGE.json`.
- **X3R1-AC2** (`x3-diff`): PASS-X3-COMMITTED-DIFF-REPRODUCES. A fresh `run_home.py diff` on the last
  two run directories reproduces `parse_diff()`-equal sections to the committed `DIFF.md`, rc=0.
- **X3R1-AC3** (`x3-nontrivial`): PASS-X3-WAVE-MOVED-SOMETHING. `CLOSED 0 + OPENED 1 = 1`.
- **X3R1-AC4** (`x3-filed`): PASS-X3-OPENED-ROWS-FILED. 1 OPENED tension; 1 new
  `ADVI_FIRMBKTS-*` row added on this branch (`ADVI_FIRMBKTS-W2-S10`).
- **X3R1-AC5**: judgment, no verdict here. `3.0.0_SA_CVO` at L9 reads: `DIFF.md` alone (`CLOSED: 0`,
  `OPENED: 1  R-0185|A3|GRAMMAR|R1`, `UNCHANGED: 179`) tells a reader who opens neither run exactly
  what moved; the practice wave itself (one new `--seed-loc`, one genuinely live, previously-unseeded
  S3 prefix) is described above and in the filed row's `world_is`.

## Mutant control

Backed up the committed `DIFF.md`, then mutated it in place: `OPENED: 1` -> `OPENED: 0`, deleting the
`R-0185|A3|GRAMMAR|R1` line beneath it (CLOSED/UNCHANGED untouched). Re-ran:
- `x3-diff`: `diff rc=0; sections equal to the committed DIFF.md: False` -> `VERDICT:
  FAIL-X3-COMMITTED-DIFF-REPRODUCES`.
- `x3-nontrivial`: `CLOSED 0 + OPENED 0 = 0` -> `VERDICT: FAIL-X3-WAVE-MOVED-SOMETHING`.

Both mutants fired as expected. Restored from the backup; `diff -q` against the backup and `git diff`
against the committed blob both read empty (byte-identical). Re-ran all four criteria: all four PASS,
same VERDICT lines as before the mutation.

## Determinism

All four criteria (`x3-two-runs`, `x3-diff`, `x3-nontrivial`, `x3-filed`) run twice in succession
against the unchanged committed/disk state produced byte-identical stdout both times (`diff` of the
two capture sets empty), rc=0 both runs.

## Surprises

None filed on `LGIC_LGCTFM`'s own channel this round. One `OBSERVATION`/`INERT` row filed on
`ADVI_FIRMBKTS`'s channel per DEC-12/T12 (`ADVI_FIRMBKTS-W2-S10`, above) -- that is this cell's own
deliverable, not an off-spec finding.
