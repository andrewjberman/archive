# LGIC_ENFORCE.TO-EN-v-3 -- result (0.9.0_WK_LGIC_ENFORCE~5)

Cell `EN-v-3`: the two IRPT `firm_bucket_map()` definitions, replaced by the generator's view. Branch
`wk-lgic-enforce-1-5`, spawn base `b02fdaa849`, registry `50e4fabd1cb6a150`.

## What landed

| File | Pre-image (@b02fdaa849) | View |
|---|---|---|
| `data/assets/scripts/gold/investor_reporting/directory_runner.py` | `:170-174` parsed FIRM_CONFIG out of `firm-config.mjs` | `:170-180` GENERATED block, a dict literal |
| `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py` | `:145-153` the same parse, its own regex | `:145-155` GENERATED block, the same literal |

Written with `python lib/opal_naming.py generate --out . --target <each path>` ("GENERATE: 2 written, 0 skipped
... at registry@50e4fabd1cb6a150"). The bytes are identical (`cmp`) to a generation into `.scratch/gen_v3`. Diff: 2 files, +20 -12,
nothing outside the two blocks. Line endings stay `i/lf w/lf`. Nothing was deployed, and no consumer was repointed.

## Criteria (each run under `timeout 120` from the worktree root)

| Id | Subcommand | Deciding output | rc |
|---|---|---|---|
| V3-AC1 | `v3-header` | `FILES: [...2...]  WITHOUT A GENERATED MARK AT REGISTRY HASH 50e4fabd1cb6a150: []` / `VERDICT: PASS-GENERATED-HEADER` | 0 |
| V3-AC2 | `v3-delta0` | `BASE: b02fdaa849  FILES: 2  EXPORTS EQUAL: 2  DIFFER: []` / `VERDICT: PASS-DELTA0` | 0 |
| V3-AC3 | `v3-tests` | `CMD: python -m pytest -q .../test_directory_runner.py  rc=0  20 passed` / `VERDICT: PASS-CONSUMER-TESTS` | 0 |

## Controls (`.scratch/ctl_v3.py`, not committed)

- **Mutant.** Check_en.py's own `_compare_carriers` ran on the base copy against a mutated view (directory_runner's
  inflection bucket changed to `opal-data-inx`, holdings_snapshot's demo row dropped): `EXPORTS EQUAL: 0  DIFFER: [both]`.
  Unmutated: `EXPORTS EQUAL: 2  DIFFER: []`.
- **Order.** The mappings are equal but the order differs in both files. The base returns 49financial, inflection,
  mockadv, demo, cottonwood; the view returns 49financial, inflection, cottonwood, mockadv, demo. This is row W5-S1.
- **Determinism.** The three subcommands ran twice. The outputs are identical after stripping ANSI codes and pytest's wall clock
  (11 lines, 3 PASS verdicts each time).
- **Commit-gate stages, run by hand before commit.** `py_compile` rc 0, `ruff check --target-version py39` "All checks passed!",
  `ds-precommit-check.py` rc 0, 0 non-ASCII bytes in either file.

## Rows filed

- `LGIC_ENFORCE-W5-S1` OBSERVATION / INERT. The mapping is equal, but its iteration order is registry order, not firm-config.mjs order.
  check_en.py's DELTA=0 compare does not see order. 5 of 5 in-file call sites use keyed lookups or pass the map on.
- `LGIC_ENFORCE-W5-S2` OBSERVATION / INERT. V3-AC3's text and the test's name (`..._comes_from_firm_config_mjs`) name
  firm-config.mjs as the source, but the view reads no file. The test asserts values and passes.
- `LGIC_ENFORCE-W5-S3` OBSERVATION / ARMED, disarm owner `2.0.0_SA_COO~G`. The order's pre-flip validation, run
  unstaged, reads INVALID rc=1: `.tools/proof-of-spec-check.py:383-386` refuses the two MODIFIED tracked carriers as
  CCX. Run the same way against a scratch copy of the index holding the commit's paths (`GIT_INDEX_FILE`), it reads
  VALID rc=0, with the real index untouched. The flip was made on that rc 0. The commit's own hook run is the authority.

## Not claimed

- Any importer of `firm_bucket_map()` outside the two carriers was not censused.
- `_FIRM_CFG_RE` (directory_runner.py:166-167) and `FIRM_CONFIG_PATH` stay defined. The generated block replaces only the
  function, and neither name is in the block.
- No deploy. Per Rule 13 a deploy rides its owner's path, byte-equivalent, and nothing live was read or moved.
