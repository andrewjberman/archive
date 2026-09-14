# IRPT_FNTEND.TO-FE-s-45 -- result

Worker `0.9.0_WK_IRPT_FNTEND~1`, slot ~1, round 7. The worktree pair is `C:/tmp/wk-irpt_fntend-7-1-fe-s-45` and its
`portal/`, both on branch `wk-irpt_fntend-7-1-fe-s-45`. Portal commit **df3a3353** (LOCAL; portal is frozen). Base:
workspace 4d11c008c2, portal 35797660. Rows filed: **IRPT_FNTEND-W1-S67** and **IRPT_FNTEND-W1-S68**, both OBSERVATION and INERT.

## The mechanism: the dev line, and why it is this one

The order grants the `dev` line and says to "choose the mechanism from the vite that is installed". vite 7.3.5 (`vite --help`)
has three config loaders. Each was measured on the committed `vite.config.ts` with an fs.watch of `node_modules/.vite-temp`,
which resolves through the junction to the main checkout:

| command | server | `.vite-temp` writes |
|---|---|---|
| `bun run vite` (the old script, bundle loader) | HTTP 200 | 3 (rename / change / rename of `vite.config.ts.timestamp-*.mjs`) |
| `vite --configLoader runner` (under node) | fails: ReferenceError on `__dirname` | 0 |
| `bun run vite --configLoader native` (under node) | fails: `__dirname is not defined in ES module scope` at vite.config.ts:13 | 0 |
| `bun --bun vite --configLoader native` (under the bun runtime) | HTTP 200 | **0** |

`vite.config.ts` uses `__dirname` at :13 (FE-s-38's cacheDir) and :16 (the alias). Only the bundle loader injects that
name. Bun's own module loader strips the types AND defines `__dirname` in an ES module, so `native` under bun loads
the config as committed and creates no temporary file. **Chosen: `bun --bun vite --configLoader native`.**

What the order did not name, filed as row W1-S67:
- `bun run dev` now runs the dev server under bun, not node, for every user of the script.
- Startup measured 1.7-14.7 s under bun (the first, cold start 14.7 s) against 0.5-2.7 s under node.
- `native` reports no config dependencies, so an edit to vite.config.ts no longer restarts the server.
- No FE-s-45 criterion exercises the `/api` proxy entries under bun.
- The alternative that keeps node needs two things: `__dirname` -> `import.meta.dirname` at vite.config.ts:13 and :16,
  plus `vite --configLoader runner|native`. vite.config.ts is not in this order's grant.

The dependency cache under bun goes to the worktree's own `portal/.vite`: the optimizer wrote 191 events there.
`node_modules/.vite/deps/_metadata.json` was last touched at 14:19:48 -0400, before this session.

A wider read, NOT the criterion's location: the whole `node_modules` tree was watched during a new-script start that
also fetched `/src/main.tsx` (port 5296). It saw 0 files created or deleted and 5 `change` events on 3 packages
(@tailwindcss/postcss 2, autoprefixer 2, @esbuild/win32-x64 1). A read-only control (2 reads, 2 imports) produced 0
events, so it cannot say whether those 5 were reads or writes. They are disclosed, not claimed either way.

### The package.json diff (the `dev` line only; the overrides block untouched)

```
--- a/package.json
+++ b/package.json
@@ -10,7 +10,7 @@
   },
   "scripts": {
     "preinstall": "node scripts/preinstall.js",
-    "dev": "vite",
+    "dev": "bun --bun vite --configLoader native",
     "build": "tsc -b && vite build",
     "typecheck": "tsc -b --noEmit",
     "lint": "eslint .",
```

## The criteria (deciding runs, portal df3a3353)

`IRPT_FE_DEV_PORT` was exported on every `bun test` run. For AC2 through AC5 and AC7 it was 5261, measured closed
(`PROBE UNREACHABLE ECONNREFUSED`) with the server down. For AC6 it was 5261 with my own server up under the new script.

- **F45-AC1**: `bun run typecheck` -> `$ tsc -b --noEmit` / `rc=0`. The four overrides are removed, and the fe-s-32 one
  was a `.ts` inside the app program.
- **F45-AC2**: `residuals.test.ts` (timeout 240), rc 0, 3 pass / 0 fail. The driver `fe-s-45/dev-script-writes.mjs` runs
  under node. It starts the portal's OWN script (`bun run dev --port 5900 --strictPort`) on a port measured closed,
  waits for HTTP, asks fe-s-27's probe whether the server serves this worktree, and stops the whole process tree.
  It then does the same for the old script on 5901.
  - `.vite-temp` readings:
    - **new script**: BEFORE `[]`, AFTER `[]`, writes seen during the start **0**. HTTP 200 after 1787 ms. Served from
      this worktree (`/@fs/.../package.json` HTTP 200, byte-identical, 2387 bytes). Port closed after the stop.
    - **old script (positive control)**: BEFORE `[]`, AFTER `[]`, writes seen **3**
      (`rename/change/rename: vite.config.ts.timestamp-1789426715315-bc83446f47a4e8.mjs`). Port closed after the stop.
  - The listing reads the same before and after in both arms: vite deletes the file within milliseconds. That is why
    the verdict rests on the watch, and why the old script is the control.
  - The working dev line equals the committed one (both printed).
  - `DEV SCRIPT WRITES NOTHING THROUGH THE JUNCTION: yes`.
  - The AC3/AC4 invocation (timeout 120) re-ran the same file: again 0 writes (new) and 3 writes (control), and the same
    verdict.
- **F45-AC3**: `git ls-tree -r HEAD` at df3a3353 has 1461 tracked paths; 35797660 has 1463. The CONTROL, the same rule at
  35797660, finds `4 of 4 present`. Committed `vite*.config.*` under `__tests__/` at HEAD: 0.
  `PER-CELL VITE OVERRIDES REMAINING: 0 of 4`.
  Census before the deletion: src + scripts, **830 files scanned**. 21 references in 4 files, **0 outside the four files
  themselves**. The pattern was `vite.worktree.config`, `vite-cache-fe-s-(31|32|39|40)`, `WORKTREE_CACHE_DIR`.
- **F45-AC4**: the committed blob `HEAD:.../fe-s-19/mounted-from-wire.test.ts`. The rule reads the one header paragraph
  that names `fe-s-27/_dev-server`, which must contain no "default". It now reads: "`IRPT_FE_DEV_PORT` first, else a
  port derived from this worktree, else the helper REFUSES: it has no fallback port (1.0.0_SA_CTO RULING U; this line
  re-worded at FE-s-45)". The CONTROL, the same rule on the 35797660 blob ("environment first, documented default
  second"), reads `NAMES A DEFAULT`. `fe-s-19 NAMES NO DEFAULT PORT: yes`.
- **F45-AC5**: `one-writer.test.ts` (timeout 180), rc 0, 11 pass / 0 fail.
  - F41-AC5's five maps are read as `git cat-file blob HEAD:<path>` at portal df3a3353, rc=0 for each, and the verdict
    is unchanged: `rev-49f-000091 -- 5 of 5`.
  - The in-memory perf-9 control now also starts from the committed blob: `maps bound 0 of 5`.
  - The seeded control commits the portal HEAD's own five blobs into a scratch repository under `<WS>/.scratch/`. It
    shows `holds the portal HEAD's own blob for 5 of 5 maps`. It then rewrites each map in place to name perf-9 and
    leaves the edit uncommitted: `git status: 5 of 5 modified`.
  - Result: committed read `rev-49f-000091`; checkout read (the pre-FE-s-45 read) `NOT BOUND`.
    `F41-AC5 READS THE COMMITTED BLOB: 5 of 5 maps`.
  - Why a scratch repository: the maps are outside this order's grant, so the in-place edit cannot be made in the
    portal's own working copy. The scratch commit holds the SAME objects (the blob ids are compared and printed).
  - F41-AC2's census still finds one writer (`fe-s-14/gen-maps.ts`). A first version of the control named its scratch
    prefix `...-committed-read-`, and the census's identifier expansion followed "committed" to the Global map through
    F41-AC4's variables. The prefix is now `fe-s-41-inplace-`, with a comment saying why.
  - One debug run saw a single `git cat-file` in the scratch repository return a null status while bun reported
    "killed 1 dangling process". `core.fsmonitor` is unset and no daemon was running, so the cause is unknown. The one
    reader now retries ONCE on a null status (never on a non-zero one) and prints the first attempt's reason. No
    recorded run needed the retry.
- **F45-AC6**: my server was started with `bun run dev --port 5261 --strictPort` from `<WS>/portal` after 5261 was
  measured closed (`VITE v7.3.5 ready in 1829 ms`). `PRECONDITION ... MET (... served from worktree
  C:/tmp/wk-irpt_fntend-7-1-fe-s-45/portal ...)`, `PAGE CRASHES: 0`, `DRIVER EXIT: 0`, `BODIES MOUNTED: 2 of 2`,
  `UNCERTAIN WITHOUT A WIRE STATE: 2 of 2`. 2 pass / 0 fail.
- **F45-AC7, the census of record**: server killed, 5261 measured closed. `Ran 569 tests across 101 files`:
  **553 pass, 16 skip, 0 fail**. 7 `PRECONDITION ... ABSENT` declarations, and fe-s-38's no-port child printed
  0 pass / 2 skip / 0 fail. The run also carries every FE-s-45 line: DEV SCRIPT ... yes, OVERRIDES 0 of 4, NAMES NO
  DEFAULT PORT yes, F41-AC5 5 of 5.
- **F45-AC8** (judgment): recorded, not graded. This order leaves one residual of RULING U: FE-s-38's
  `resolve-config.mjs` still loads the config with the bundle loader. Every run of `fe-s-38/isolation.test.ts`
  therefore writes through the junction (3 events measured), and its header's reason ("the loader the dev server
  uses") is no longer true. That is row W1-S68; fe-s-38/ is NOT YOURS. F41-AC5 grades what is committed (AC5).

## Servers

I started, and stopped:
- the experiment servers on 5291, 5293, 5294, 5295 and 5296 (5292 never came up), each stopped by `taskkill /T /F`
  and measured closed;
- the driver's servers on 5900 and 5901, stopped by the driver and measured closed;
- my own server on 5261, killed before AC7 and measured closed.

5263 (the sibling's) was never touched. The 5949 listener is on 0.0.0.0 and not mine (the vite servers above bind
::1). Its owner is in the WORKER REPORT.
