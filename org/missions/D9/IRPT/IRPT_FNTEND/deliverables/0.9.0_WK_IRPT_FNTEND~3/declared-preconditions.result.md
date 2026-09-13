# FE-s-27 -- an absent precondition is not a failure

**TO** `IRPT_FNTEND.TO-FE-s-27` · **cell** `FE-s-27` · **worker** `0.9.0_WK_IRPT_FNTEND~3`
**worktree** `/c/tmp/wk-irpt_fntend-4-3-fe-s-27` branch `wk-irpt_fntend-4-3-fe-s-27` from `f3b42b1e0b`
**portal** `/c/tmp/wk-irpt_fntend-4-3-fe-s-27/portal` branch `wk-irpt_fntend-4-3-fe-s-27` from `237a9027`
**portal commit** `3ad6fcc2f5` -- **LOCAL, NOT PUSHED, GITLINK NOT BUMPED** (portal is frozen by a
standing Andrew-direct; the workspace repo's ` M portal` is expected and was never staged).

---

## 1. THE TWO-WAY MEASUREMENT, WHICH IS THIS CELL'S OWN PROOF

The order requires this pair explicitly, because the cell's subject is that one command over one set of
bytes produced two different verdicts and said nothing about why. **Every criterion below is recorded
with the world it was measured in.** One dev server was used: `bun run dev --port 5181`, started in the
background from `<WS>/portal`, **and it is DOWN at the time of this report** (`netstat -ano | grep -i
listening | grep 5181` returns nothing, exit 1; the probe returns `PROBE UNREACHABLE ECONNREFUSED from
http://localhost:5181/`).

| criterion | measured with the dev server | why that world |
|---|---|---|
| `F27-AC1` typecheck | **DOWN** | no environmental precondition; also run UP earlier, rc=0 both times |
| `F27-AC2` the declaration itself | **BOTH** | the criterion's whole point: it passes in either world |
| `F27-AC3` ABSENT arm | **UP** | the arm does not depend on the ambient world -- it DRIVES absence at a port it measured closed first. Also observed identical in the DOWN run of AC6 |
| `F27-AC4` PRESENT arm | **UP** | it cannot be measured any other way; with the server DOWN this criterion SKIPS itself, by name, which is the rule applied to this file |
| `F27-AC5` port from environment | **UP** (source scan; world-independent) | also observed identical in the DOWN run of AC6 |
| `F27-AC6` both folders green | **DOWN** | the criterion says NO dev server, and that is the deliverable stated as a bar |
| `F27-AC7` the skip is loud | **UP** (reads the driven-absent child) | also observed identical in the DOWN run of AC6 |
| `F27-AC8` judgment | recorded, not graded | L9, `3.0.0_SA_CVO` |

**THE HEADLINE PAIR, one commit, one command, both worlds:**

```
dev server DOWN   bun test fe-s-19 fe-s-27  ->  6 pass / 3 skip / 0 fail   (9 tests, 4 files)
dev server UP     bun test fe-s-27/precondition.test.ts -> 4 pass / 0 fail, and its
                  PRESENT child run -> BODIES MOUNTED: 2 of 2 / UNCERTAIN WITHOUT A
                  WIRE STATE: 2 of 2 / 2 pass / 0 fail
```

Before this cell the same down-server world produced **3 fail** and the failure text was
`driverStatus=1`, `slot=NO DRIVER LINE`.

## 2. WHAT CHANGED, AND WHAT DELIBERATELY DID NOT

Five files in the portal, no app source, **`scripts/ui-smoke.mjs` untouched** (it is not this order's).

| file | what it is |
|---|---|
| `fe-s-27/dev-server-probe.mjs` (new) | the reachability measurement, one line of output, never a non-zero exit for an absent server. Bound is the caller's argument. |
| `fe-s-27/_dev-server.ts` (new) | `IRPT_FE_DEV_PORT` first, documented default second; the precondition line; the skip notice. **The default constant lives here, not in `fe-s-19/`** -- which is why F27-AC5's scan of that folder is a true zero rather than a wording trick, and the disclosure is printed in the run itself. |
| `fe-s-19/_mounted-grade.ts` (new) | the grading rule lifted out of the test, so the negative control runs the SAME rule. A control that re-implements the rule agrees with itself, not with the test. |
| `fe-s-19/mounted-from-wire.test.ts` (edited) | measures and prints the precondition **at module scope** (a `beforeAll` a fully-skipped file may not run cannot declare anything), gates the two tests on it, and takes the port from the environment. |
| `fe-s-27/precondition.test.ts` (new) | drives both arms. |

⛔ **NOTHING F19-AC4 / F19-AC5 ASSERT WAS WEAKENED.** Both bars are still `2 of 2`, both still require
`driverStatus === 0`, and both still run the real browser driver when the precondition is met -- proved
in section 3 under `F27-AC4`, not asserted here. F19-AC2/AC3/AC6/AC7 were not touched; `network-state.test.ts`'s
own seed-prop scan re-ran over the folder at 7 files (it now includes `_mounted-grade.ts`) and reported
`SEEDED PROPS USED: 0` with its positive control firing.

## 3. CRITERION BY CRITERION -- the deciding output, verbatim

### `F27-AC1` -- PASS by output. Dev server DOWN.
```
$ tsc -b --noEmit
rc=0
```
**DISCRIMINATION, because `tsc -b` is incremental and a skipped build also prints nothing:** a type error
was seeded into the new file (`const SEEDED_TYPE_ERROR: number = 'positive control'`) and the same
invocation returned
`src/pages/InvestorReporting/__tests__/fe-s-27/precondition.test.ts(49,7): error TS2322: Type 'string' is not assignable to type 'number'.`
with **rc=2**. The control was then removed and rc=0 re-measured. The new files are genuinely in the program.

### `F27-AC2` -- PASS by output. Measured in BOTH worlds, which is the criterion.
DOWN:
```
PRECONDITION: dev server on http://localhost:5181 -- ABSENT (ECONNREFUSED from http://localhost:5181/) [port from default; set IRPT_FE_DEV_PORT to change it]
 0 pass / 2 skip / 0 fail
```
UP:
```
PRECONDITION: dev server on http://localhost:5181 -- MET (HTTP 200 from http://localhost:5181/) [port from default; set IRPT_FE_DEV_PORT to change it]
 2 pass / 0 fail
```
The line names **what is needed** (a dev server), **on which port**, **whether it is there**, and **how to
change it**. It is printed at module scope, so it survives every test in the file being skipped.

### `F27-AC3` -- PASS by output. Dev server UP (the arm drives its own absence).
```
DRIVEN ABSENT: port 54021 measured closed before the child run
  DECLARED: PRECONDITION: dev server on http://localhost:54021 -- ABSENT (ECONNREFUSED from http://localhost:54021/) [port from env; ...]
  SKIPPED CRITERIA: 2 of 2
  CHILD FAIL COUNT: 0
  CHILD EXIT: 0
ABSENT PRECONDITION: reported SKIPPED, 0 failures
```
The child's own summary is `0 pass / 2 skip / 0 fail`. **DRIVEN, not observed:** the port is probed closed
first and only then handed to the child, so the arm does not depend on the ambient world and reproduces
identically in the UP run and the DOWN run.

### `F27-AC4` -- PASS by output. Dev server UP on 5181. **Three legs, because AC3 alone is indistinguishable from deleting the tests.**
```
  DECLARED: PRECONDITION: dev server on http://localhost:5181 -- MET (HTTP 200 from http://localhost:5181/) [port from env; ...]
  REAL DRIVER OUTPUT   -> mounted 2 of 2
  SEEDED BREAKAGE      -> mounted 1 of 2
  precondition MET   + good seam   -> PASS (expected PASS)
  precondition MET   + broken seam -> FAIL (expected FAIL)
  precondition ABSENT + broken seam -> SKIPPED (expected SKIPPED)
PRESENT PRECONDITION: assertions still enforced
```
LEG 1 is a real child run of `mounted-from-wire.test.ts` against the live server: `DRIVER OK`,
`PAGE CRASHES: 0`, `BODIES MOUNTED: 2 of 2`, `UNCERTAIN WITHOUT A WIRE STATE: 2 of 2`, `2 pass / 0 fail`.
LEG 2 takes **those same bytes** and removes one `SCENARIO ready TAB reporting` line. LEG 3 runs all three
cells through `verdictFor`, the function the graded test itself uses -- so the control cannot agree with
itself instead of with the test. **The MET+broken cell is FAIL, not SKIPPED. The skip can still become a
real failure.**

### `F27-AC5` -- PASS by output. World-independent (a source scan), recorded from the UP run.
```
  SCAN __tests__/fe-s-19/ for the literal 5181: 0 hit(s) across 7 file(s)
  POSITIVE CONTROL (seeded copy): 1 hit(s) across 1 file(s)
  DISCLOSURE: the documented default is declared once, in fe-s-27/_dev-server.ts, as 5181 -- a constant of the precondition, not a literal in the driving test.
  devPort() with IRPT_FE_DEV_PORT=54999 -> 54999; with it unset -> 5181
PORT FROM ENVIRONMENT: no literal
```
**Denominator printed (7 files), positive control printed, and the one place the number still lives is
disclosed rather than hidden behind the scan's scope.** The control is run BEFORE the real scan and is
built from the real shape (`const PORT = '5181'`), so a scan that could not fire cannot return the same
zero a clean folder returns. The last line is the separate claim that the environment is actually read.

### `F27-AC6` -- PASS by output. Dev server DOWN -- **the bar, in the world the bar names.**
```
 6 pass
 3 skip
 0 fail
 22 expect() calls
Ran 9 tests across 4 files. [1365.00ms]
```
`0 fail` with nothing running. The 3 skips are named in the same output: F19-AC4, F19-AC5 (the ambient
absent server) and F27-AC4 (this file's own precondition, skipping itself by the same rule).

### `F27-AC7` -- PASS by output. Recorded from the UP run; identical in the DOWN run.
```
  SKIPPED: F19-AC4 -- a READY envelope on the wire mounts both tab bodies -- PRECONDITION ABSENT: no dev server on http://localhost:54021 (ECONNREFUSED from http://localhost:54021/)
  SKIPPED: F19-AC5 -- a status carrying no state reaches both tabs as UNCERTAIN -- PRECONDITION ABSENT: no dev server on http://localhost:54021 (ECONNREFUSED from http://localhost:54021/)
  CRITERIA NAMED WITH A REASON: 2 of 2
SKIPPED IS VISIBLE: named in the output
```
Each notice carries **the criterion id**, **what it proves**, **that the precondition was ABSENT**, and
**the measured reason**. The child also prints the summary line
`PRECONDITION ABSENT -> 2 criteria SKIPPED, 0 failures. This is not a code defect.`

### `F27-AC8` -- JUDGMENT. RECORDED, NO VERDICT. Graded at L9 by `3.0.0_SA_CVO`.
The output a reader gets, with no knowledge of any port, is in the four blocks above. Offered without a
verdict: the run distinguishes *not exercised* from *exercised and held* in three independent places --
the runner's own `skip` count, the `SKIPPED: <criterion> -- ... -- PRECONDITION ABSENT: <reason>` notices,
and the presence-or-absence of the `BODIES MOUNTED: N of 2` bar, which only an exercised run emits.

## 4. SURPRISE ROWS

Two, both in `org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md`,
appended (diffstat read: `45 insertions(+)`, 0 deletions), no existing row edited. W3 plane-max was
verified as S16 across BOTH `INVESTIGATION_v1.md` and `_v2.md` before minting.

- **`IRPT_FNTEND-W3-S17`** (OBSERVATION, **ARMED**, disarm owner `2.0.0_SA_COO~F`) -- the worker face's
  "a closed loopback port TIMES OUT on this box, never refuses" is falsified (it REFUSES, immediately, on
  both ports measured), and the practically dangerous half is the reverse: vite binds `localhost` as
  IPv6-only here, so a 127.0.0.1 probe reads UNREACHABLE against a server answering HTTP 200. Under the
  law this cell installs, that FALSE ABSENT skips a runnable criterion quietly. Already known in-tree at
  `portal/.frontend-dev/runners/category-views-fixture-proxy.mjs:95` -- the duplicate discovery is the
  evidence that the carrier is wrong, not the knowledge.
- **`IRPT_FNTEND-W3-S18`** (OBSERVATION, INERT) -- under bun 1.3.9, mutating `process.env` does not reach
  a `spawnSync` child; the first build of the ABSENT arm silently exercised the ambient environment and
  **every assertion except the one naming the value it had set still passed**. Remedy is in-tree.

## 5. WHAT THIS DELIVERABLE DOES NOT DO

- It does not make the precondition pattern available to other cells by any mechanism other than
  `fe-s-27/_dev-server.ts` being importable. No other folder was touched and none was in the grant.
- It does not change `scripts/ui-smoke.mjs`, which shares the false-absent hazard of row W3-S17 in
  principle; that file is explicitly not this order's, and the row names the hazard rather than reaching
  for the file.
- It does not bump the portal gitlink and it does not push. Portal is frozen.
- The `devPort()` default is a real literal in a real file. The criterion scopes its scan to `fe-s-19/`
  and that scan is a true zero, but **a scan scoped to one folder cannot certify the absence of the
  number from the repository**, and this file says so rather than letting the printed zero imply it.
