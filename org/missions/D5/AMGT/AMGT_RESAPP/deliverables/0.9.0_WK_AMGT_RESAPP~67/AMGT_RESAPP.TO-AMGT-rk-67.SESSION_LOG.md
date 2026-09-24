# SESSION LOG -- `0.9.0_WK_AMGT_RESAPP~67` on `AMGT_RESAPP.TO-AMGT-rk-67`

Worktree `C:/tmp/wk-amgt-16-67`, branch `wk-amgt-16-67`, based at `006dd1e344` (round-16 issuance
`ce51efce21`). First act: `git rev-parse --abbrev-ref HEAD` -> `wk-amgt-16-67`; `org/` and `.tools/` present.
Section 4 security bounds read before any command; `wk-amgt-14-50` and `C:/tmp/wk-amgt-14-50` never touched.

## Measured state re-check

Re-read `.tools/comp-secrets` at branch HEAD (`006dd1e344`) before editing. The cell's cited lines
(`cmd_get` `:214-255`, the defect at `:236-238`, `main()`'s `get` subparser `:341-360`/`:350`) matched the
order's citations. No citation had moved.

## Build

1. `.tools/comp-secrets`:
   - `cmd_get`: added an up-front refusal for `--value-only` without `--reveal` (rc 2) and `--value-only`
     with `--json` (rc 2), BEFORE any client/AWS act. Added a new `if args.json and args.reveal:` branch
     emitting `json.dumps({**meta, "value": ...})` (value `null` for a binary secret). The prior
     `if args.json and not args.reveal:` branch is untouched. Added a `value_only` branch (reached only
     with `--reveal`, without `--json`) printing `_ascii(value)` through `print()` (one LF, nothing else);
     binary -> rc 1, stderr line, empty stdout. The default text block (`name:`/`firm:`/`arn:`/`value:` or
     `shape:`) is byte-identical -- no line inside it was touched.
   - `main()`: reworded `--reveal`'s help text (no longer implies a bare-value idiom), added `--value-only`'s
     own help (states it requires `--reveal`, refused with `--json`). Updated the module docstring's
     `Usage:` line to show the new flag. Left the logging comment (`:246-250` pre-edit) and the docstring
     guarantee (`:9-11`) unedited in substance.
2. `.tools/tests/test_comp_secrets.py` (NEW): 8 named arms per the order, offline, `SourceFileLoader`-loaded,
   `_client` monkeypatched to a `FakeClient` returning only the literal sentinel `SENTINEL-NOT-A-SECRET`
   (or a binary blob `b"x"` for the binary arms). `test_text_block_unchanged` diffs the live module's
   default `--reveal` output against `git show HEAD:.tools/comp-secrets` loaded independently, same fake.
   `test_collect_parser_still_reads` monkeypatches `collect.subprocess.run` -- the real tool/AWS is never
   reached.

## Criteria

- AC1: `python -m pytest .tools/tests/test_comp_secrets.py -v` -- 8 passed, 0 failed, all 8 named arms
  present and PASSED.
- AC2: the python probe over `cmd_get`'s body -- all six printed values matched the order's `<expect>`
  exactly (`fallthrough_condition_present False`, `json_reveal_branch_present True`,
  `value_only_flag_declared True`, `help_names_value_only True`, `help_line_old_text_present False`,
  `cmd_get_opens_files False`).
- AC3: `py_compile` rc 0; both files `crlf 0`; `.tools/comp-secrets` `non_ascii_byte_delta 0`, matching the
  re-measured base (`006dd1e344`, `base_non_ascii_byte_delta 0`, `base_crlf 0`, `base_lines 364`); new test
  file `non_ascii_byte_delta 0`, `crlf 0`; new `.tools/comp-secrets` line count (395) is larger than the base
  (364).

## Controls

- Mutant: re-ran AC2's exact probe against `git show HEAD:.tools/comp-secrets` (the pre-fix bytes, still
  carrying the old fallthrough and no `--value-only`). Observed the OPPOSITE of every load-bearing value:
  `fallthrough_condition_present True`, `json_reveal_branch_present False`, `value_only_flag_declared
  False`, `help_names_value_only False`, `help_line_old_text_present True`. `cmd_get_opens_files False` on
  both (a neutral field, unaffected by this cell) -- AC2's discriminating fields all flip.
- Determinism: ran AC1's full pytest invocation twice in succession, no fixtures touch the clock or
  randomness (fixed sentinel string, fixed fake ARN); both runs "8 passed", 0 failed.

## Security confirmation

Every command run against `.tools/comp-secrets`/`test_comp_secrets.py` in this session used a stubbed
`_client()` returning the literal sentinel `SENTINEL-NOT-A-SECRET` or a synthetic binary blob `b"x"`. No
command called `boto3.client("secretsmanager")`, no `aws secretsmanager` command ran, and
`lib.research.social.collect.read_api_key` was invoked exactly once, with `collect.subprocess.run`
monkeypatched, never unpatched. No output recorded anywhere in this log, the test file, or the proof
instance carries any value other than the literal sentinel. Branch `wk-amgt-14-50` and directory
`C:/tmp/wk-amgt-14-50` were never read, diffed, shown or checked out.
