# IRPT_FNTEND.TO-FE-s-38 -- one server per worktree, and every browser verdict names it -- RESULT

**Worker:** 0.9.0_WK_IRPT_FNTEND~1 | **Cell:** FE-s-38 (`1.0.0_SA_CTO` RULING U, graduated as C-S81)
**Worktree pair:** `C:/tmp/wk-irpt_fntend-6-1-fe-s-38` (workspace, base 1f5d387e17) and `C:/tmp/wk-irpt_fntend-6-1-fe-s-38/portal` (portal, base 741bb54b), both on branch `wk-irpt_fntend-6-1-fe-s-38`
**Portal commit:** `ac13f8ab` (LOCAL; portal frozen) -- 10 files, +663 / -55

## What changed (portal ac13f8ab)

| File | Change |
|---|---|
| `vite.config.ts` | `cacheDir: path.resolve(__dirname, '.vite')`, plus a comment citing RULING U. Nothing else in the file changed. |
| `tsconfig.app.json` | `tsBuildInfoFile` changed from `./node_modules/.tmp/tsconfig.app.tsbuildinfo` to `./.tsbuild/tsconfig.app.tsbuildinfo`. |
| `tsconfig.node.json` | `tsBuildInfoFile` changed from `./node_modules/.tmp/tsconfig.node.tsbuildinfo` to `./.tsbuild/tsconfig.node.tsbuildinfo`. |
| `.gitignore` | Adds `.tsbuild/` with a comment. `.vite` was already ignored at `:17`. |
| `__tests__/fe-s-27/_dev-server.ts` | `DEFAULT_DEV_PORT` removed. `choosePort()` takes the port from `IRPT_FE_DEV_PORT`, else derives it from the helper's own git worktree (FNV-1a of the path, folded into 5400..5899), else throws `REFUSED: ...`. `devPort()` / `probeDevServer()` default to `choosePort()`. `Precondition` gains `state` (MET / ABSENT / FOREIGN) and `root`. The declaration line names the port, the measured served-from worktree and the port's source. `skipNotice` says "no dev server of this worktree". |
| `__tests__/fe-s-27/dev-server-probe.mjs` | argv[4] carries the portal root. After `/` answers, the probe GETs `/@fs/<root>/package.json`. HTTP 200 with bytes identical to the file on disk reads REACHABLE; anything else reads FOREIGN. |
| `__tests__/fe-s-27/precondition.test.ts` | Only F27-AC5's two claims that RULING U changes; see "fe-s-27 claims changed" below. |
| `__tests__/fe-s-38/isolation.test.ts` | F38-AC2..AC4, plus the FOREIGN control. |
| `__tests__/fe-s-38/resolve-config.mjs` | Runs under node. Reads the cache location from vite's `resolveConfig` (the default bundle loader, the same one the dev server uses) and the build-info locations from TypeScript's `getParsedCommandLineOfConfigFile`. One `grade` rule applies to every path, including the two retired locations used as negative controls. |
| `__tests__/fe-s-38/ambient-shims.d.ts` | Type-only: `node:os` tmpdir, `node:fs` mkdtempSync/rmSync, `bun:test` afterAll. |

### How "served from" is measured (RULING U's recording half)

An answer on the port is not a match. vite serves `/@fs/` only inside its own allow list, which is its root. Measured 2026-09-14 on this worktree's server (5261):
- `GET /@fs/C:/tmp/wk-irpt_fntend-6-1-fe-s-38/portal/package.json` returned HTTP 200, byte-identical to the file.
- `GET /@fs/C:/Users/AndrewBerman/Desktop/ajb_workspace/portal/package.json` returned HTTP 403 "outside of Vite serving allow list", and the allow list it printed named only this worktree's portal and vite's own client dir.

So another worktree's server on the probed port reads FOREIGN, which is not met, and the browser criteria SKIP by name instead of grading the wrong page. The in-suite control shows the check firing: the same bytes under a root this server does not serve read `FOREIGN (... HTTP 403)`.

## Where the main checkout's cache and build info live now

- **Main checkout `C:/Users/AndrewBerman/Desktop/ajb_workspace/portal`, today:** nothing has moved yet. The portal is frozen and this change is LOCAL on `wk-irpt_fntend-6-1-fe-s-38`. The main checkout still runs its own `vite.config.ts` and tsconfigs at its own HEAD, so it caches in `node_modules/.vite` and writes `node_modules/.tmp/tsconfig.{app,node}.tsbuildinfo`. Both exist there, as the negative controls printed in F38-AC3/AC4 show.
- **Once ac13f8ab reaches the main checkout:** its vite cache moves to `C:/Users/AndrewBerman/Desktop/ajb_workspace/portal/.vite`, and its build info to `C:/Users/AndrewBerman/Desktop/ajb_workspace/portal/.tsbuild/`. Each linked worktree then keeps its own cache and build info under `<worktree>/portal/.vite` and `<worktree>/portal/.tsbuild/`. The old `node_modules/.vite` and `node_modules/.tmp` stop being written and can be left or deleted; nothing reads them.
- **Still through the junction:** vite's config loader writes a transient temp bundle into `node_modules/.vite-temp` (row W1-S63, INERT).

## Per criterion (deciding runs)

| Criterion | Server state | Deciding output | Verdict |
|---|---|---|---|
| F38-AC1 | irrelevant (typecheck) | `$ tsc -b --noEmit` / `rc=0` | PASS |
| F38-AC2 | this worktree's server UP on 5261, `IRPT_FE_DEV_PORT=5261` exported | `HELPER WITH NO PORT GIVEN AND NONE DERIVABLE: REFUSED`; `HELPER WITH NO PORT GIVEN IN A REAL WORKTREE: derived port 5805 from C:/tmp/wk-irpt_fntend-6-1-fe-s-38/portal`; 5 pass / 0 fail | PASS |
| F38-AC3 | same run | `VITE cacheDir INSIDE THE WORKTREE, NOT THROUGH THE JUNCTION: yes` (resolved `C:/tmp/wk-irpt_fntend-6-1-fe-s-38/portal/.vite`; control `node_modules/.vite` resolves to the main checkout, inside=no) | PASS |
| F38-AC4 | same run | `tsbuildinfo INSIDE THE WORKTREE, NOT THROUGH THE JUNCTION: 2 of 2` (both under `<portal>/.tsbuild/`; control inside=no) | PASS |
| F38-AC5 | this worktree's server UP on 5261, started from `<WS>/portal` by `bun run dev --port 5261 --strictPort` under the new config (cache built at `<WS>/portal/.vite/deps`) | `BODIES MOUNTED: 2 of 2`; 2 pass / 0 fail; 80.85 s | PASS |
| F38-AC6 | same run | `UNCERTAIN WITHOUT A WIRE STATE: 2 of 2` | PASS |
| F38-AC7 | same run | `PRECONDITION: dev server on http://localhost:5261 -- MET (HTTP 200 from http://localhost:5261/; served from worktree C:/tmp/wk-irpt_fntend-6-1-fe-s-38/portal: GET /@fs/.../package.json -> HTTP 200, byte-identical ...) [required worktree ...; port: env IRPT_FE_DEV_PORT; ...]` | PASS |
| F38-AC8 | `IRPT_FE_DEV_PORT=5271` exported, 5271 measured closed first (ECONNREFUSED, 304 ms); this worker's 5261 server was still up but not addressed | `527 pass / 14 skip / 0 fail`, `Ran 541 tests across 95 files`, rc=0 | PASS |
| F38-AC9 | -- | recorded below | RECORDED (judgment; L9) |

### F38-AC8 -- REFUSE loudly or SKIP by name? Both, depending on the case, and both appear in this run

- **The port is given (the census's own condition, 5271 closed):** every browser test SKIPS BY NAME. That is 13 named notices: F19-AC4/AC5, F27-AC4, F30-AC6/AC7, F31-AC6, the W1-S61 re-run, F32-AC2..AC6, and the new F38 served-from control. The 14th skip is the pre-existing `SKIPPED: .scratch/app.diff absent`. The run before this cell had 13 skips across 94 files; the +1 is the new FOREIGN control.
- **No port given, inside a worktree:** the helper DERIVES the port and the browser test SKIPS BY NAME on it. In the same whole-suite run, `fe-s-38/isolation.test.ts` ran `fe-s-19/mounted-from-wire.test.ts` as a child with `IRPT_FE_DEV_PORT` removed, not emptied. Output: `A BROWSER TEST GIVEN NO PORT: SKIPPED BY NAME (2 of 2 criteria named, derived port, 0 defaults)`, with the child declaring `port: derived from worktree C:/tmp/wk-irpt_fntend-6-1-fe-s-38/portal` on port 5805, child exit 0.
- **No port given and none derivable:** the helper REFUSES. It throws `REFUSED: IRPT_FE_DEV_PORT is unset and no worktree is derivable from ... -- this helper has no default port (1.0.0_SA_CTO RULING U) ...`, printed in the same run as `HELPER WITH NO PORT GIVEN AND NONE DERIVABLE: REFUSED`. A consumer that calls `probeDevServer()` at module scope in that condition errors loudly at load. The "no worktree" directory is a fresh `mkdtemp` under the OS temp dir. git itself reported it as not a repository, and the same instrument, run from the helper's own directory, returned the worktree (positive control). The directory is removed in `afterAll`.
- **Failures outside the grant: none.** 0 fail, so there is no BLOCKING row.

## fe-s-27 claims changed (each cites RULING U, each shown both ways)

1. **"with it unset -> the documented default"** became **"with it unset -> derived from this worktree, never the retired default"**. Both ways: `devPort() with IRPT_FE_DEV_PORT=54999 -> 54999; with it unset -> 5805 (derived from worktree ...; RULING U -- before it, the fixed 5181)`. The assertions are `fromUnset === portForWorktree(worktree)` and `fromUnset !== '5181'`. The REFUSED way is proven in fe-s-38 (above).
2. **"the documented default is declared once, in fe-s-27/_dev-server.ts"** became **"the helper declares no default"**. Both ways: `SCAN fe-s-27/_dev-server.ts for the retired default 5181 (RULING U): 0 hit(s) now; 1 hit(s) in the helper at portal 741bb54b (git show rc=0)`, with the positive control at 1 hit. The retired number lives only in the test, as `RETIRED_DEFAULT_PORT`, the thing the scans look for.

Every other assertion in `precondition.test.ts` is unchanged. F27-AC3/AC4/AC7 ran green on this worktree's own server: 4 pass / 0 fail; present arm `mounted 2 of 2`; truth table PASS / FAIL / SKIPPED.

## `scripts/ui-smoke.mjs`

Not touched. It does not import the helper and does not use its default: it has its own `--port` flag, defaulting to 5175 (`scripts/ui-smoke.mjs:45`). So there is no row.

## F38-AC9 -- recorded, not graded

- Every browser verdict line now names its server. The line printed on every run of fe-s-19/30/31/32/27/38 has the form `PRECONDITION: dev server on http://localhost:<port> -- <MET|ABSENT|FOREIGN> (<probe detail, which for MET includes "served from worktree <root>: GET /@fs/<root>/package.json -> HTTP 200, byte-identical ...">) [required worktree <root>; port: <env IRPT_FE_DEV_PORT | derived from worktree <root> | given by the caller>; ...]`. Every skip notice carries the state and the detail.
- F35's ENVELOPE_BODY "never seen mounted" qualification: on this worktree's own server, after FE-s-35's refusal of no-identity bodies (portal 850d7718 is in this worktree's history), F19-AC4 printed `BODIES MOUNTED: 2 of 2` (reporting at `slot=reporting-body`, holdings at `slot=holdings-tab`). F19-AC5 printed `UNCERTAIN WITHOUT A WIRE STATE: 2 of 2` (both at `status-panel@UNCERTAIN`). `PAGE CRASHES: 0`, `DRIVER EXIT: 0`. Whether this lifts the qualification is the L9 call.

## Rows filed (INVESTIGATION_v2.md)

- `IRPT_FNTEND-W1-S63`: vite's config loader still writes a transient temp bundle through the junction (`node_modules/.vite-temp`). OBSERVATION, INERT.
- `IRPT_FNTEND-W1-S64`: the fe-s-19 header comment still says "documented default second". Outside the grant. OBSERVATION, INERT.
- `IRPT_FNTEND-W1-S65`: fe-s-31/fe-s-32 per-cell vite overrides still point the cache at `.scratch`, which is now a second cache home. Outside the grant. OBSERVATION, INERT.
- `IRPT_FNTEND-W1-S66`: a closed loopback port refused in under 0.5 s, not ~2 s as BOUNDS and the probe comment state. OBSERVATION, INERT.

## Server

This worker's dev server was started on 5261 (measured ECONNREFUSED first) from `<WS>/portal` under the new config. It was killed after F38-AC8: PID 9272 and its child were taskkilled, and 5261 then probed `ECONNREFUSED` with 0 LISTENING sockets.
