# TO-OS-s-12 result -- the working-order census of the outset tools

**Produced by `0.9.0_WK_NFRA_OUTSET~3`**, worktree `C:/tmp/wk-OUTSET-3`, branch `wk-OUTSET-3`.
**Tree vintage for every measurement below:** HEAD `22e38e7963`.
This order was re-addressed to `~3` on BOTH limbs before seating (`<issued_to>` and all three
deliverables references), verified at HEAD with `git show` rather than in the checkout. **No wall,
no carry step, no row needed for addressing** -- the first face this round where that was true.

**TO:** `org/missions/D11/NFRA/NFRA_OUTSET/task-orders/NFRA_OUTSET.TO-OS-s-12.working-order-census.md`
· **verb:** build · **outcome_ref:** FWD-5 · **cell:** OS-s-12 · **depends_on:** OS-s-1, OS-s-4

## 0. THE ANSWER, up front

**9 of 9 outset tools censused. 8 WORKING, 1 FAILED.** The one that fails is `comp-pipescript
deployed` -- the brief's own named GIT->DEPLOY hop -- which returns no answer within 9 s, none
within 75 s either, and accepts no `--budget` for a caller to bound it with.

**The disclosure picture is the harder finding:** over the 9 tools, **answer-state 2/9**,
**vintage 2/9**, and **a budget line when a budget was offered 2/4**. Most of the outset surface
cannot today tell a caller what state its answer is in or how old it is.

## 1. What I built

**One file, and it is my whole code surface:** `.tools/tests/test_os12_census.py` (my `<paths>`
grants `.tools/tests/`). Nothing else in the repo was written. It is an on-demand instrument:
nothing is scheduled, nothing alarms, nothing is removed (PRD R-5, standing moratorium).

**It is not a second implementation.** Six of the nine tools already have a battery under
`.tools/tests/test_comp_*_battery.py` (`comp-heat`, `comp-drift`, `comp-similar`, `comp-pipescript`,
`comp-blast`, `comp-estate`; `comp-fedobs`, `comp-xray` and `comp-freshness` have none). A battery
asks *"is THIS tool correct?"*; the census asks *"which of the population can answer AT ALL today,
and what does each disclose?"* -- one read, one denominator. Different question, no duplicated logic:
the census invokes the tools' own CLIs and re-uses the estate's own `.tools/git_bash_resolver.py`
rather than reimplementing dispatch.

## 2. The plane I counted

**The LOCAL REPO CLI plane** -- the `.tools/<tool>` files in this worktree at `22e38e7963`. **NOT**
the `~/bin` shim plane, **NOT** any deployed or remote plane, **NOT** the tools' engines called as
functions. A census that does not name its plane cannot be checked, and an inner function is not
its CLI.

## 3. The denominator, and why it is checked rather than typed

The population is the brief's Part II sentence (`docs/briefs/comp-heat-and-the-semantic-estate-
pipeline-outset-tooling-brief-20260904.md`), which names nine tools. The census carries that list
as data **and arm A1 re-derives it from the brief at run time and fails on any mismatch** -- so the
denominator is compared against its source on every run instead of being typed once and trusted.
`brief_tool_list()` returns `[]` if the brief is unreadable, which **fails** A1 rather than agreeing
with an empty list (an empty expectation matches nothing and would pass vacuously).

Derived and declared agree: **9 and 9, identical and ordered.**

## 4. O12-AC1 -- the mechanical arm

**Invocation:** `timeout 120 python .tools/tests/test_os12_census.py` · **rc = 0** (read directly
from the command, not through a pipe) · deciding line:

```
=== test_os12_census: PASS (7/7) in 42.3s ===
```

Seven arms, `7/7`, inside the 120 s bound. The criterion's own words are *"the census runs AND a
PLANTED FAILURE reads FAILED with its denominator -- the arm that must be able to fail"*:

| arm | what it holds | result |
|---|---|---|
| A1 | tool list matches the brief's Part II enumeration | OK -- brief-derived 9 vs declared 9, identical and ordered |
| A2 | all named tools present on the counted plane | OK -- 9/9 present |
| A3 | census emits one row per tool with its denominator | OK -- 9 rows of 9 tools |
| **A4** | **planted failure reads FAILED and is COUNTED** | **OK -- denominator 3 (subset was 2); planted verdict=FAILED** |
| A5 | rc=0 with an empty body is not scored WORKING | OK -- `classify(rc=0, empty) -> NO-ANSWER-DISCLOSED` |
| A6 | positive control: resolver dispatch answers where bare-bash falsely fails | OK -- resolver rc=0 bytes=973; bare-bash rc=1 bytes=504 wsl_stub=True |
| A7 | per-probe deadline actually bounds a known-unbounded launcher | OK -- deadline 6 s returned in 7.2 s rc=124 |

**A4 is the arm that must be able to fail, and it is planted two ways.** The absent-tool plant must
read `FAILED` *and stay in the denominator* -- a census that silently drops what it cannot probe
reports a clean population it never had. A5 plants the subtler shape: `rc=0` with an empty body,
which must **never** score WORKING.

## 5. O12-AC2 -- the census (evidence, NO verdict)

**Invocation:** `timeout 120 python .tools/tests/test_os12_census.py` (the census prints as part of
the battery; `--census-only` prints the table alone). Output verbatim:

```
=== OS-s-12 WORKING-ORDER CENSUS -- outset tools ===
  plane: LOCAL REPO CLI (.tools/<tool> in this worktree) | probe deadline 9s | census budget 100s | elapsed 29.3s
  tool               rc  verdict                     state  vintg  budget       secs
  comp-heat           0  WORKING                     False  False  YES          0.7
  comp-fedobs         0  WORKING                     False  True   not-accepted 6.4
  comp-drift          0  WORKING                     False  False  NO-LINE      2.6
  comp-xray           0  WORKING                     False  False  not-accepted 3.7
  comp-similar        0  WORKING                     True   True   NO-LINE      2.4
  comp-pipescript   124  FAILED                      False  False  not-accepted 9.8   [bounded at 9s, no answer]
  comp-freshness      0  WORKING                     False  False  not-accepted 1.2
  comp-blast          0  WORKING                     True   False  not-accepted 1.9
  comp-estate         0  WORKING                     False  False  YES          0.6
  DENOMINATOR: 9 tool(s) censused; 8 WORKING, 1 FAILED, 0 NO-ANSWER-DISCLOSED, 0 NOT-PROBED-BUDGET-EXHAUSTED
  disclosure over the 9: answer-state 2/9, vintage 2/9, budget-line-when-offered 2/4
```

**Column grains, stated because a census's columns are where grain quietly slips:**
- `rc` -- exit code of a **real answer probe**, never `--help`. `--help` proves the CLI parses, not
  that the tool answers; each probe is the cheapest genuine answer the tool offers.
- `verdict` -- `WORKING` requires rc=0 **and** a non-trivial body. `FAILED` = non-zero or bounded-out.
  `NO-ANSWER-DISCLOSED` = the confident-zero shape. `NOT-PROBED-BUDGET-EXHAUSTED` = never started.
- `state` / `vintg` -- whether the answer body carries an answer-state token / a vintage token.
- `budget` -- `YES` = `--budget` offered **and** a disclosure line printed; `NO-LINE` = offered and
  **silently swallowed** (the NFRA_OUTSET-S6 shape); `not-accepted` = no `--budget` flag at all.

`comp-pipescript` is kept in the table at its FAILED verdict rather than dropped or excused: the
brief names `comp-pipescript deployed` explicitly, and *"could not answer within 9 s"* **is** its
working-order answer. Suppressing it would be precisely the empty section O5 forbids.

## 6. The three false-zero traps this census is built against

The coordinator's standing warning on this cell: *a census that cannot distinguish "I counted the
population and found none" from "I counted the wrong thing perfectly" is the exact failure this cell
exists to prevent elsewhere.* Three were met, all three measured, all three now pinned by arms.

**(1) The WSL-stub trap -- it would have falsified 4 of 9 rows.** Four of the nine tools are bash
launchers. A bare `subprocess.run(["bash", <script>])` on this host resolves to the System32 WSL
stub, which has no distribution: rc=1 with a UTF-16LE *"Windows Subsystem for Linux has no installed
distributions"* body. A census dispatching that way reports **4 of 9 outset tools BROKEN, with a
clean denominator, every verdict false.** This is the mirror of a false zero -- a false *verdict*,
which is harder to catch because the output looks like evidence rather than like silence.

**How it was caught:** all four failures had body length **exactly 504 bytes**. Four tools failing
independently do not produce four identical lengths; one shared dependency failing does. That is
"a check scoped to the members cannot see a defect in what the members share" arriving as a
measurement. **Remedy is the estate's own, not a new one:** `.tools/git_bash_resolver.py`, whose
docstring names this exact trap. Arm A6 keeps the contrast measured. Filed as `NFRA_OUTSET-W3-S7`,
**ARMED** -- because `.tools/drift_producer.py:155` makes that call today and counts `rc!=0` as
`tools_failed`, falsely convicting a healthy tool. Outside my `<paths>`, so filed and not fixed.

**A second dispatch error of my own, same family:** I first ran the *Python* tools through `bash`,
which produced authentic-looking tool errors that were really my error. The census therefore
dispatches by **shebang**, never by guess.

**(2) The unbounded-grandchild trap.** `subprocess` `timeout=` does **not** bound a shell launcher:
the launcher's python grandchild inherits and holds the stdout **pipe**, so the parent blocks on pipe
EOF past its own deadline. Measured: `comp-pipescript deployed` under `timeout=8` ran **91.8 s**, and
the aggregate pass then blew a 120 s outer bound and was killed with **zero output** -- which reads
exactly like `NFRA_OUTSET-S2` (comp-find rc=124, no bytes) and would be misread the same way. Fix:
output to a **file** rather than a pipe, plus a process-**tree** kill. Same probe now returns at
8.9 s. Arm A7 pins it. Filed as `NFRA_OUTSET-W3-S8`.

**(3) The confident-zero trap.** `rc=0` with an empty or state-free body is not a working tool.
Arm A5 plants that shape and fails if the census scores it WORKING.

## 7. Controls

- **Positive control (A6):** the instrument returns rc=0 / 973 bytes on `comp-xray`, a case known to
  exist, while the naive dispatch returns rc=1 / 504 bytes on the *same* tool. This proves both that
  a non-zero is obtainable and that the census's dispatch discriminates.
- **Mutant (A4/A5):** two planted failures, both fire.
- **Determinism:** two full runs compared on verdicts, denominators and disclosure counts --
  **identical**. Only wall-clock `secs` vary, which is expected and is not a verdict-bearing column.
- **Commit gate:** `bash .tools/commit-gate.sh .tools/tests/test_os12_census.py` -> rc=0,
  `All checks passed!`.

## 8. What would have changed the reading

- If `comp-pipescript deployed` had answered at the 75 s bound, its row would read WORKING-but-slow
  rather than FAILED. It was re-probed at 75 s precisely to separate *slow* from *not answering*;
  it returned 82 bytes, its shim line only.
- If the four bash launchers had each failed with *different* bodies, the shared-cause hypothesis
  would have died and I would have reported four broken tools. Identical lengths killed it.
- If the brief's Part II had named a different set, A1 would fail and the denominator would be wrong
  by construction -- which is why that arm exists rather than a typed constant.

## 9. Declared limits

- **`depends_on` names OS-s-4, which is not landed.** OS-s-4 adds vintage and catalog disclosure to
  `comp-heat federated`. This census reads the disclosure surface as it stands at `22e38e7963`, so
  `comp-heat`'s `vintg` column is a **pre-OS-s-4 reading** and is expected to change when OS-s-4
  lands. The census is the instrument; re-running it is the re-measurement. Not a blocker: no arm
  depends on OS-s-4's output.
- **Probe choice is a judgment.** Each tool's probe is one cheap answer, not its whole surface; a
  tool could be WORKING on this probe and broken on another subcommand. The census reports working
  *order*, not correctness -- that is what the batteries are for.
- **`comp-fedobs` reads a served artifact** and so its row depends on that artifact's reachability
  at run time; it answered with a vintage line at the time of this run.
- **Why `comp-pipescript` does not answer was NOT diagnosed.** The CLI's behaviour is measured; the
  cause is not, and no AWS plane was read. Naming a cause would staple an interpretation to a
  measurement.
- **The `["bash"` sweep behind W3-S7 is a narrow lexical pattern**, not a census of the hazard: a
  call built from a variable, via `shell=True`, or spelled `/bin/bash` would not match. The
  population question belongs to that row's disarm owner.

## 10. Rows filed

| id | class / hazard | one line |
|---|---|---|
| `NFRA_OUTSET-W3-S7` | OBSERVATION / **ARMED** | Bare-`bash` dispatch hits the WSL stub and would mark 4 of 9 outset tools falsely BROKEN; live victim measured at `.tools/drift_producer.py:155`. Disarm owner named; outside my `<paths>`, so filed not fixed. |
| `NFRA_OUTSET-W3-S8` | OBSERVATION / INERT | `subprocess` `timeout=` does not bound a shell launcher (91.8 s against an 8 s deadline); file-redirect + tree-kill fixes it; pinned by arm A7. |
| `NFRA_OUTSET-W3-S9` | OBSERVATION / INERT | Census result: `comp-pipescript deployed` gives no answer at 9 s or 75 s and accepts no `--budget` -- the one gap in the population. |

## 11. What I changed

Created `.tools/tests/test_os12_census.py`. Appended 3 rows to the project channel (append-only;
byte prefix asserted identical before the splice, array re-parsed to 34 rows, all ids distinct, no
existing row edited). Wrote this document and the proof-of-spec instance beside it. **No tool under
`.tools/comp-*` and nothing under `org/modules/` was modified** -- `comp-heat` and
`org/modules/heatmap/` are slot 1's this round and were not touched.
