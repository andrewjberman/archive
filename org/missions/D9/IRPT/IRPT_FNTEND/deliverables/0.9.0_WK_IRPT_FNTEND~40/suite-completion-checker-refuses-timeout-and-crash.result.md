# FE-s-90 -- suite-completion checker refuses timeout and crash -- result

**Disclosure.** All four mechanical acceptance criteria (F90-AC1..AC4) ran to PASS-by-output on this
worker's own worktree, against the exact invocations the task order names, verbatim. F90-AC5 is
judgment; this file records the evidence and gives no verdict. Two genuine environment surprises were
found and filed as rows `IRPT_FNTEND-W40-S1` and `IRPT_FNTEND-W40-S2` (both OBSERVATION/INERT,
GROUNDED) while building this cell's own controls; neither blocked delivery, both are documented in
the shipped code's own comments so a future cell does not have to re-discover them. No dev server was
started (HOW step 2 names one, ports 6015-6019) -- this cell's own four acceptance criteria are a
typecheck, two real `bun test` subprocess runs, and one standalone CLI invocation; none renders a page
or calls an HTTP surface, so a dev server would have been unused. This is a judgment call, not a
criterion refusal, and is disclosed here rather than filed as a row since it contradicts no spec
assertion (the HOW section is suggested workflow, not itself an acceptance criterion).

## What was built

- `portal/scripts/suite-complete-check.mjs` -- a standalone Node/Bun CLI tool (no new dependency).
  Runs a given `bun test ...` command (optionally itself wrapped in `timeout N ...`) as a real child
  process via `bash -lc "<joined command>"`, captures combined stdout+stderr and the real exit code,
  and refuses (`SUITE-COMPLETE: no`) unless: (a) the producer's exit code is not 124 (an unconditional
  hard refuse, independent of anything else); (b) bun's own completion line
  (`Ran <N> tests across <M> files.`, read live off this box's installed bun 1.3.9) is present in the
  captured output, regardless of exit code or how many/few failing-test lines exist; (c) every
  ANSI-stripped `<fail-glyph> <name>` failing-test line either matches an `--allow`-listed
  criterion-id substring BY NAME, or there are none unmatched. On success it prints
  `SUITE-COMPLETE: yes | PASS: <n> SKIP: <n> UNEXPECTED-FAIL: <n>`; on refusal,
  `SUITE-COMPLETE: no | REASON: <timeout|crash|incomplete-output|unreconciled-failure: <name>>` -- one
  grep-able anchor line either way. `--help` (or no command) prints usage and exits 0, invocable
  standalone (F90-AC3). Pure ASCII throughout (CLAUDE.md Rule 4): the bun fail-glyph (U+2717) is
  matched via a backslash-u-2717 escape sequence, never a literal byte, documented inline.

- `portal/src/pages/InvestorReporting/__tests__/fe-s-90/suite-complete-check.test.ts` -- the harness.
  Spawns the checker as a REAL child process (not mocked) for each of the four required controls,
  each with an explicit wrong-state/negative arm (HOW step 3):
  1. a completed, fully-passing run -> `SUITE-COMPLETE: yes`, `UNEXPECTED-FAIL: 0`.
  2. a completed run with one genuinely unexpected failure -> `SUITE-COMPLETE: no`,
     `unreconciled-failure: ... > one genuinely unexpected failure`.
  3. a completed run whose one failure matches an `--allow`-listed id -> `SUITE-COMPLETE: yes`,
     `UNEXPECTED-FAIL: 0` -- PLUS an identity-not-count cross-check: the SAME allow id against a
     DIFFERENT fixture whose one failure carries a DIFFERENT name still refuses, proving the checker
     reconciles by name, not by count coincidence (both fixtures fail exactly once).
  4. a run killed by a real `timeout` wrapper mid-execution -> `SUITE-COMPLETE: no`,
     `REASON: timeout: producer rc=124 ...`, `PRODUCER-RC: 124`, `COMPLETION-LINE: MISSING` -- PLUS a
     wrong-state arm: the identical `timeout N ...` wrapper against a fixture of the same async shape
     that finishes well inside the bound does NOT refuse, proving the discriminator is genuine
     non-completion, not merely the wrapper's presence.

- `portal/src/pages/InvestorReporting/__tests__/fe-s-90/fixtures/*.fixture.ts` -- five tiny real bun
  test files (passing, one-unexpected-failure, one-allowed-failure, slow/never-completes,
  quick-async/completes-in-time) authored under this cell's own grant. Named `.fixture.ts`, not
  `.test.ts`, specifically so bun's own directory-scan discovery (which drives F90-AC2 and F90-AC4)
  never runs a deliberately-failing or deliberately-hanging fixture directly -- verified live (see row
  `IRPT_FNTEND-W40-S1`) and documented in each fixture's own header comment.

- `portal/src/pages/InvestorReporting/__tests__/fe-s-90/ambient-shims.d.ts` -- the portal's
  established per-cell TypeScript ambient-declaration idiom (copied from fe-s-46's `test(label, fn,
  timeoutMs?)` overload verbatim; one NEW `node:child_process` `spawnSync` overload carrying
  `maxBuffer`, not present in any neighbouring cell's shim).

## Criteria, measured

- **F90-AC1** -- `cd WS/portal && timeout 180 bun run typecheck; echo rc=$?` -> `rc=0`. PASS-by-output.
- **F90-AC2** -- `cd WS/portal && timeout 120 bun test src/pages/InvestorReporting/__tests__/fe-s-90`
  -> `4 pass, 0 fail`, `Ran 4 tests across 1 file.` -- matches `(?<![0-9])0 fail`. PASS-by-output.
- **F90-AC3** -- `cd WS/portal && bun scripts/suite-complete-check.mjs --help; echo rc=$?` -> prints
  the full usage block, `rc=0`. Non-crashing output. PASS-by-output.
- **F90-AC4** -- `cd WS/portal && timeout 600 bun test src/pages/InvestorReporting` -> `665 pass, 27
  skip, 0 fail`, `Ran 692 tests across 129 files.`, rc=0. Matches `(?<![0-9])0 fail`. PASS-by-output.
- **F90-AC5** -- judgment, RECORDED, no verdict given. Evidence: the checker's own source
  (`scripts/suite-complete-check.mjs`) and this cell's four controls above, each a real subprocess run
  demonstrating the exact refusal/acceptance behaviour the task order names, plus the identity-vs-count
  and wrong-state cross-checks. The output format (`SUITE-COMPLETE: yes|no | ...`, one line, anchored
  at line start, grep-able via `^SUITE-COMPLETE:`) is the same shape used throughout this round's other
  criteria's `<expect>` regexes.

## Surprises filed

- `IRPT_FNTEND-W40-S1` -- `bun test <bare-relative-path>` (no leading `./`) that does not match bun's
  own test-naming discovery convention is silently treated as a substring FILTER against
  already-discovered files, not as an instruction to run that file -- drove the `.fixture.ts` naming
  plus explicit `./` prefixing on every fixture path in this cell's own code.
- `IRPT_FNTEND-W40-S2` -- `spawnSync` called from inside an already-running bun/node process cannot
  resolve an MSYS-style (`/c/...`) path directly (ENOENT); the Windows-native forward-slash form
  resolves and is far faster than routing through `bash -lc` when a shell is not otherwise needed --
  drove this cell's test harness spawning the checker directly rather than through an extra bash hop.

Both OBSERVATION/INERT, GROUNDED, filed in
`org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md`.
