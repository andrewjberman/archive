# NFRA_OPLGTW.TO-OG-q-1 -- the bounded execution engine -- worker result

**Worker:** `0.9.0_WK_NFRA_OPLGTW~5` | **Branch:** `wk-nfra_oplgtw-1-5b` in `/c/tmp/wk-oplgtw-1-5b`, cut from `CLOUD` at
`da63a446ef` | **Build commit:** `187c69246f` (LOCAL, not pushed) | **Interpreter:** `.venv-og`, Python 3.12.10 with
`--system-site-packages`, reinstalled from the edited requirements file: `duckdb==1.2.2`, `pyarrow==18.1.0`,
`mcp==1.28.0`, `pytest==9.0.2`, `moto==5.2.3` (read from `pip freeze`).

## Verdict

14 of 14 mechanical criteria PASS by output. None is marked `judgment="true"`. One surprise row was filed:
`NFRA_OPLGTW-W5-S2` (OBSERVATION, INERT).

## Criteria, each run exactly as written (WS = /c/tmp/wk-oplgtw-1-5b)

| id | invocation (after `cd <WS> && timeout 120 .venv-og/Scripts/python`) | rc | deciding output |
|---|---|---|---|
| OGQ1-AC1 | `-m pytest infra/aws/ec2/opal-gateway/tests/test_schwab_engine.py::test_ogq1_ac01 -q -p no:cacheprovider --color=no` | 0 | `1 passed in 2.15s` |
| OGQ1-AC2 | `... ::test_ogq1_ac02 ...` | 0 | `1 passed in 3.79s` |
| OGQ1-AC3 | `... ::test_ogq1_ac03 ...` | 0 | `1 passed in 1.17s` |
| OGQ1-AC4 | `... ::test_ogq1_ac04 ...` | 0 | `1 passed in 6.90s` |
| OGQ1-AC5 | `... ::test_ogq1_ac05 ...` | 0 | `1 passed in 4.19s` |
| OGQ1-AC6 | `... ::test_ogq1_ac06 ...` | 0 | `1 passed in 4.35s` |
| OGQ1-AC7 | `... ::test_ogq1_ac07 ...` | 0 | `1 passed in 4.16s` |
| OGQ1-AC8 | `... ::test_ogq1_ac08 ...` | 0 | `1 passed in 2.23s` |
| OGQ1-AC9 | `... ::test_ogq1_ac09 ...` | 0 | `1 passed in 2.51s` |
| OGQ1-AC10 | `... ::test_ogq1_ac10 ...` | 0 | `1 passed in 1.38s` |
| OGQ1-AC11 | `... ::test_ogq1_ac11 ...` | 0 | `1 passed in 3.66s` |
| OGQ1-AC12 | `... ::test_ogq1_ac12 ...` | 0 | `1 passed in 1.02s` |
| OGQ1-AC13 | `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~5/probes/og_q1.py AC13` | 0 | `VERDICT: PASS-OGQ1-AC13` |
| OGQ1-AC14 | `... ::test_ogq1_ac14 ...` | 0 | `1 passed in 0.06s` |

The 13 pytest criteria ran one at a time against the working tree whose bytes are those committed in `187c69246f`.
No file was edited between the runs and the commit, apart from the mutant below, which was restored byte-identical.

The AC13 probe's full output:

```
host python (BASELINE.json OGP1-AC2 python_version): Python 3.11.15 -> --python-version 3.11
pins read from infra/aws/ec2/opal-gateway/requirements.txt: {'pyarrow': '18.1.0', 'duckdb': '1.2.2'}
pyarrow==18.1.0: pip rc=0 wheels=['pyarrow-18.1.0-cp311-cp311-manylinux_2_17_aarch64.manylinux2014_aarch64.whl']
  python tags ['cp311'] abi ['cp311'] platform ['manylinux_2_17_aarch64', 'manylinux2014_aarch64'] -> python_ok=True aarch64_ok=True
duckdb==1.2.2: pip rc=0 wheels=['duckdb-1.2.2-cp311-cp311-manylinux_2_17_aarch64.manylinux2014_aarch64.whl']
  python tags ['cp311'] abi ['cp311'] platform ['manylinux_2_17_aarch64', 'manylinux2014_aarch64'] -> python_ok=True aarch64_ok=True
resolved 2 of 2 pins for manylinux2014_aarch64 on Python 3.11
VERDICT: PASS-OGQ1-AC13
```

## Proof-of-spec check

`py -3.12 .tools/proof-of-spec-check.py org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~5/NFRA_OPLGTW.TO-OG-q-1.execution-engine.proof_of_spec.json OGQ1-AC1,...,OGQ1-AC14`
returned rc=0, `acceptance rows=14 | violations=0`, `VALID (rc=0)` (checker vintage ae97defa81). Other lines from
the run:
- invocation-alignment: 14 of 14 recorded invocations match the criterion text;
- surprises: 1 entry, which resolves to a channel row;
- artifact resolution: 6 resolved at pin 187c69246f, plus this file, which rides the proof commit.

The order's `<status>` was flipped to `complete` after this run.

## What each test measures

- **AC1:** a probe job reports its own pid (not the parent's), its ppid (the parent), and no running asyncio loop. A
  real query (PyArrow + DuckDB, account policy) returns `AAA 170.10`, `BBB 70.07` from another child pid. Both
  children are dead afterwards.
- **AC2 (difference):** a 10 ms latency probe on the loop. With a 1.5 s CPU spin in the child, max lag stays under
  0.25 s (at least 30 samples). The same spin run inside the loop gives a max lag over 1.0 s, and over 4x the child arm.
- **AC3:** at the default 256 MiB cap, a child allocating toward 512 MiB is killed: `LIMIT_EXCEEDED`/`memory`, no
  value, peak RSS over 256 MiB, dead child. A 32 MiB job completes (difference).
- **AC4:** the defaults are 30 s and 31 s is refused. With the deadline lowered to 3 s by configuration, a 20 s
  accumulating job (query and export kinds) is killed at 3-8 s with `LIMIT_EXCEEDED`/`deadline` and `value None`,
  so no partial total comes back, and the child is dead. A 0.3 s job returns its total.
- **AC5:** while one job runs for `p-same`, a second for `p-same` is `BUSY`/`per_principal_busy` in under 0.5 s with
  no child. `p-other` is admitted at the same moment, and `p-same` is admitted again after the first ends.
- **AC6:** with two jobs running, a third principal gets `BUSY`/`global_busy` in under 0.5 s. The running count
  stays 2, nothing is queued or started later, and the slot is admitted after the drain. `global_jobs=3` and
  `queue_size=1` are refused as configuration.
- **AC7:** reads `peak_rss_kB` from OG-p-1's BASELINE.json and asserts the engine's cited constant equals it
  (188700 kB). It asserts the reserve is `ceil(peak x 1.25) + 128 MiB`. The injected host memory runs four arms:
  - one byte short of reserve + one job: `BUSY`/`headroom_busy`;
  - exactly enough: admitted;
  - one job running, one byte short of two: `BUSY` below the global cap of 2;
  - enough for two: admitted.

  Weakening the peak, the multiplier or the OS reserve is refused.
- **AC8:** each arm submits sources, and the expected result follows the arrow:
  - 12 data objects + 1 policy dependency = 13 -> `LIMIT_EXCEEDED`/`source_objects`, and the suggestion names 13, 12 and "policy dependencies included";
  - 11 + 1 = 12 -> admitted, and the sums over 11 files are correct;
  - 32 + 32 MiB declared plus the policy file -> `source_bytes`;
  - exactly 64 MiB -> admitted;
  - a file whose declared size understates its real size (limit lowered to 1000 bytes) -> refused, because the real size counts.

  No suggestion contains a path.
- **AC9:** inside a child, and inside a real query job, the six lockdown settings read back as expected
  (`enable_external_access`, `autoload_known_extensions`, `autoinstall_known_extensions`,
  `allow_community_extensions` and `allow_unsigned_extensions` false; `lock_configuration` true), and they still
  read that way after the attempts below. The attempts:
  - a remote `read_parquet('https://...')`, a local `read_csv` and a `COPY TO` each raise `PermissionException`, and the copy target is not created;
  - `INSTALL`, `LOAD`, re-enabling external access, unlocking and re-enabling autoload are all refused.
- **AC10:** 325 corpus strings, each carrying a `ZQ` sentinel: 25 hand-written injections plus 300 seeded random
  strings (quotes, semicolons, comments, NUL, bidi, CJK). Each string is used as column names, aggregate aliases
  and filter values in a rows plan and an aggregate plan, 650 plans in total. The checks:
  - no generated SQL contains the sentinel;
  - every statement matches `[A-Za-z0-9_ ,()?*=<>]+`;
  - the values arrive only as parameters;
  - each shape produces exactly one SQL text across the whole corpus, so the SQL depends on the plan's shape only;
  - a caller string in an operator, function, direction or type slot is refused.

  End to end, a Parquet file with hostile column names and values answers the equality filter with exactly the one matching row.
- **AC11:** at construction, stale `ogq1-job-*` entries (a directory with spill and export files, plus a file) are
  removed, and an unrelated file is kept. After a successful job, a failing job, a cancelled job (its directory
  seen present while running), a real query and a real export, no job directory remains.
- **AC12:** a 60 s child is alive, the awaiting task is cancelled, `CancelledError` propagates within 5 s, the pid is
  no longer alive, no job is active, and the principal is admitted again.
- **AC14:** the requirements file's only `mcp` line is `mcp==1.28.0`, still under its PINNED comment. `pyarrow` and
  `duckdb` are exact `==` pins.

## Controls

- **Mutant (discrimination).** The mutant made two edits to `engine.py`:
  - `open_duckdb` forces `enable_external_access = True`;
  - the memory check compares against 100x the cap.

  AC3 and AC9 then ran, and both failed:
  - AC3: rc=1, `1 failed in 21.47s`, `AssertionError: JobResult(ok=True, ... value={'held_bytes': 536870912}, ... peak_child_rss_bytes=579162112 ...)`;
  - AC9: rc=1, `1 failed in 3.76s`, `AssertionError: enable_external_access`.

  Restored: sha256 `7a4e19925b89cdc89978d5c3c8226b267fcf14860f784b1c05c48f091582f6bc` before and after, 0 MUTANT lines.
- **Two runs.** The development run of the whole file read `1 failed, 12 passed in 36.72s`. The failure was the
  AC1 test's own arithmetic: it expected `matched_rows == 2`, the engine returned 4, and 4 is correct (source rows
  inside the policy, before grouping). The test was corrected before the criterion runs, and the engine was not
  changed. The criterion runs then read 13 of 13 `1 passed`.
- **Regression.** `cd <WS> && .venv-og/Scripts/python -m pytest infra/aws/ec2/opal-gateway/tests -q -p no:cacheprovider
  --color=no --ignore=infra/aws/ec2/opal-gateway/tests/test_schwab_engine.py` -> rc=0, `91 passed, 34 subtests passed`.
- **Commit gate.** `bash .tools/commit-gate.sh <3 .py files>` -> rc=0, `OK: pre-commit gate clean for 3 of 3 file(s)`.
  safe-commit's surprise-corpus limb reads `new=0` at `187c69246f`.

## Design choices the order did not state (each is inside the grant; none is a surprise row)

- **Where the peak RSS lives.** The engine carries OG-p-1's value as a cited constant
  (`MEASURED_EXISTING_PEAK_RSS_KB = 188700`). It does not read BASELINE.json at runtime, because the deployed
  Gateway has no `org/` tree. AC7's test binds the constant to the file.
- **Admission memory.** Admission budgets against host memory: `MemTotal`, bounded by the service's cgroup v2
  `memory.max` when numeric. The rule is `reserve + (running + 1) x 256 MiB <= host memory`. On the current
  t4g.nano (MemTotal 428644 kB, BASELINE OGP1-AC2), this admits no job, which matches the PRD's "not presumed to
  have capacity".
- **Memory cap.** The parent polls the child's RSS (`/proc/<pid>/status` VmRSS on the host) every 20 ms and kills
  at the cap. An unreadable RSS kills the job, so the cap fails closed. psutil is not used because the host venv
  does not carry it (BASELINE OGP1-AC2 package list, 51 packages). DuckDB is additionally given half the cap as its
  `memory_limit`, spilling into the job's own directory.
- **Policy dependencies.** `SourceObject.role = "policy"` counts toward both source caps. Only `data` objects are
  scanned as rows. Account policy reaches the engine as `PolicyFilter`s, applied in PyArrow before DuckDB, so the
  policy field need not be a granted column. How OG-q-2 turns a grant into these is OG-q-2's.
- **`matched_rows`.** This counts source rows inside policy and filters, before grouping and paging.

## Declared exclusions

- **Tool wiring.** Registering the five tools, the response envelope, cursors and the audit call before release
  belong to OG-q-2.
- **Deploy.** Nothing deploys, and no AWS call was made. The only egress was to the Python package index: the
  Interpreter bound's install, the AC13 probe's `pip download`, and one read of PyPI's JSON index for duckdb/pyarrow
  wheel tags (row W5-S2).
- **Untracked `audit.jsonl` at the worktree root.** The existing suite's `test_ratelimit`, run from the workspace
  root, appended to the cwd-relative `./audit.jsonl`: the mechanism row NFRA_OPLGTW-W3-S2 records, landing at the
  root instead of the tracked Gateway copy. It is outside the grant, so it is neither committed nor removed.
- **The "known red" test.** `tests/test_identity_scope.py::test_scoped_deny_by_default` passed in this worktree
  when run from the workspace root (`1 passed in 0.05s`). Row NFRA_OPLGTW-S1 measured it red from
  `infra/aws/ec2/opal-gateway`. The difference is the run directory. Neither the test nor the allowlist was touched.
