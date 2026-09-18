# LGIC_LGCTFM.TO-LT-h-1-r1 -- run-home-diff -- result (0.9.0_WK_LGIC_LGCTFM~2)

Cell `LT-h-1` (PRD `LGIC_LGCTFM_PRD.md` DEC-12; decomp v1.1 round-1 cell `LT-h-1`). Built
`workflows/legacy_transform/run_home.py` (three subcommands: `new`, `manifest`, `diff`) and
`workflows/legacy_transform/README.md`, per the interface fixed in the task order's WORKER FACE.

## Design notes

- `new` creates `<root>/<subject>/<run-id>/` and writes `VINTAGE.json` with the four keys
  (`repo_head`, `graph_built`, `registry_hash`, `run_id`); prints the run directory path. Default
  `run-id` is `<UTC YYYYMMDDTHHMMSSZ>-<first 7 chars of --repo-head>`. **A directory that already
  exists is refused (`sys.exit(1)`, message to stderr) and touched nowhere** -- `os.makedirs` is
  called only after the existence check, so a refused call never allocates a partial run.
- `manifest` scans `<root>/<subject>/` for every immediate subdirectory carrying a readable
  `VINTAGE.json`, sorted by run-id, and rewrites `MANIFEST.md` from that scan every call
  (compile-on-view -- nothing carried forward from a prior manifest).
- `diff` reads `<run>/contract.json`'s `tensions[]` (empty list if the file is absent -- never a
  traceback) and keys each tension on `<row_id>|<axis>|<kind>|<deciding_rules sorted,
  comma-joined>`, exactly the identity the task order's interface names. Prints `CLOSED:`,
  `OPENED:`, `UNCHANGED:` in that order, each with its count then one two-space-indented line per
  key. A tension whose only change is a non-identity field (e.g. `note`) keys the same on both
  sides and reports UNCHANGED, never CLOSED+OPENED.

## Criteria

Every invocation below ran from `<WS>` = `C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-lgctfm-1-2`
against the checker at
`org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_lt_r1.py`.

- **H1R1-AC1** (`h1-headings`): PASS-H1-DIFF-CLOSED-OPENED-UNCHANGED, rc=0. Two planted runs (one
  tension closed, one opened, one unchanged with an unchanged prose field); `diff` reported
  `CLOSED: 1 / OPENED: 1 / UNCHANGED: 1` with the exact identity strings the checker's own core
  computed (`core_diff` compared got vs want, all three sections matched).
- **H1R1-AC2** (`h1-identity`): PASS-H1-DIFF-KEYED-ON-IDENTITY, rc=0. Same two-run plant, but the
  UNCHANGED tension's `note` field differs between the two runs (`prose_change=True`); the identity
  key ignores `note`, so it still reports UNCHANGED, not CLOSED+OPENED.
- **H1R1-AC3** (`h1-no-overwrite`): PASS-H1-SECOND-RUN-NEVER-OVERWRITES, rc=0. First `new` call:
  rc=0, `VINTAGE.json` written. Second `new` call at the same `--run-id` with a different
  `--registry-hash`: rc=1 (refused), and the first run's `VINTAGE.json` bytes are byte-identical
  before and after the refused call.
- **H1R1-AC4** (`h1-manifest`): PASS-H1-MANIFEST-LISTS-EVERY-RUN, rc=0. Two planted runs; the
  compiled `MANIFEST.md` (plus `manifest`'s own stdout) carries both runs' run-id and their three
  vintage values -- `core_manifest` found zero omitted triples out of 2.
- **H1R1-AC5**: judgment, no verdict here. `3.0.0_SA_CVO` at L9 reads: `MANIFEST.md` is compiled
  from the tree at view time (`_iter_runs` re-scans the subject directory every call; no wall-clock
  value beyond what is already fixed inside each run's own `VINTAGE.json` enters the output), and
  the README states the never-overwrite rule (`README.md` "`new` -- one run, never overwritten")
  and the identity key (`README.md` "`diff` -- CLOSED / OPENED / UNCHANGED, keyed on identity").

## Negative control

Before this build, `workflows/legacy_transform/run_home.py` did not exist in the tree (confirmed:
`workflows/legacy_transform/` itself was absent -- `ls` of `workflows/` listed only
`atom_decomposition`, `atom_layer0`, `vendor_watch`, `ycharts`). Re-run with the file moved aside
(`mv workflows/legacy_transform/run_home.py /tmp/... ; check_lt_r1.py h1-headings; mv back`):
`_h1_guard` fires `FAIL-H1-DIFF-CLOSED-OPENED-UNCHANGED` naming `absent:
workflows/legacy_transform/run_home.py`. The fix flips this to PASS by output; the mutant fired.

## Determinism

Each of the four arms (`h1-headings`, `h1-identity`, `h1-no-overwrite`, `h1-manifest`) run twice in
succession on the committed tree produced byte-identical stdout both times (diff of the two capture
files was empty), rc=0 both runs.

## Surprises

None filed. `org/missions/D14/LGIC/LGIC_LGCTFM/surprise-channel/investigations/INVESTIGATION_v1.md`
carries no prior `LGIC_LGCTFM-W2-S` row and nothing outside this order's mandate was found.
