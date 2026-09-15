# IRPT_FNTEND.TO-FE-s-45 -- result (AMENDMENT 1, RULING (B))

Worker `0.9.0_WK_IRPT_FNTEND~1`, slot ~1, round 7. The worktree pair is `C:/tmp/wk-irpt_fntend-7-1-fe-s-45` and its
`portal/`, both on branch `wk-irpt_fntend-7-1-fe-s-45`. The order was REOPENED by AMENDMENT 1 (2.0.0_SA_COO~F,
1.0.0_SA_CTO RULING (B)).

- **Portal commit: 06bf98fa** (LOCAL; portal is frozen). It sits on the DEV sync f504ab7c (0d075808, FE-s-42), which sits
  on the first run's df3a3353.
- Rows filed this run: **IRPT_FNTEND-W1-S69** and **IRPT_FNTEND-W1-S70**, both OBSERVATION and INERT.
- Rows W1-S67 and W1-S68 stand as filed.

## The mechanism: node plus the runner loader

RULING (B) rejects the first run's `bun --bun vite --configLoader native`, because it moved every dev server to the bun
runtime. The loaders failed under node only because `vite.config.ts` used `__dirname`, which only the bundle loader
injects in a `"type": "module"` package. With `vite.config.ts` amended, each loader was measured under node with
`loadConfigFromFile` and a watch of `node_modules/.vite-temp` (through the junction):

| loader | loads the amended config under node | `.vite-temp` writes | cacheDir | proxy keys | dependencies |
|---|---|---|---|---|---|
| bundle (the default) | yes | 3 | portal/.vite | 13 | `["vite.config.ts"]` |
| runner | yes | **0** | portal/.vite | 13 | `[]` |
| native | yes | 0 | portal/.vite | 13 | `[]` |

**Chosen: `--configLoader runner`**, as RULING (B) names. The runtime stays node. Why the empty dependency list
does not stop a restart on an edit to the config is row W1-S70 (vite 7.3.5 `config.js:26032`, `isConfig`).

### The package.json diff against 35797660 (dev, build and preview only; the overrides block untouched)

```
--- a/package.json
+++ b/package.json
@@ -10,11 +10,11 @@
   },
   "scripts": {
     "preinstall": "node scripts/preinstall.js",
-    "dev": "vite",
-    "build": "tsc -b && vite build",
+    "dev": "vite --configLoader runner",
+    "build": "tsc -b && vite build --configLoader runner",
     "typecheck": "tsc -b --noEmit",
     "lint": "eslint .",
-    "preview": "vite preview",
+    "preview": "vite preview --configLoader runner",
     "test:provenance-guard": "node scripts/provenance-read-guard.mjs",
     "test:provenance-read": "bun scripts/paired-provenance-read-exercise.mjs"
   },
```

### The vite.config.ts diff (both former `__dirname` sites, and the import they need)

```
@@ -1,6 +1,7 @@
 import { defineConfig } from 'vite'
 import react from '@vitejs/plugin-react'
 import path from 'path'
+import { fileURLToPath } from 'url'
@@ -10,10 +11,10 @@
-  cacheDir: path.resolve(__dirname, '.vite'),
+  cacheDir: path.resolve(path.dirname(fileURLToPath(import.meta.url)), '.vite'),
   resolve: {
     alias: {
-      '@': path.resolve(__dirname, './src'),
+      '@': path.resolve(path.dirname(fileURLToPath(import.meta.url)), './src'),
```

It uses `fileURLToPath`, not `import.meta.dirname`: `engines` declares node >=18.0.0. The node on this box is v26.8.2.

### fe-s-38/resolve-config.mjs (row W1-S68)

`resolveConfig({ ..., configLoader: 'runner', ... })`, and its header now names the runner loader as the one the dev script
names. `fe-s-38/isolation.test.ts` passes 5/0 on it, and `VITE cacheDir INSIDE THE WORKTREE, NOT THROUGH THE JUNCTION: yes`
appears in the whole-suite run.

## The reach, by subtraction (re-run at my vintage; printed by F45-AC9 from the committed tree)

- **Scripts**:
  - at 35797660: 8 minus 5 that load no vite config = **3** (dev, build, preview);
  - at HEAD 06bf98fa: 8 minus 5 (preinstall, typecheck, lint, test:provenance-guard, test:provenance-read) = **3**.
- **Programmatic loaders**, the CTO's pattern `resolveConfig|loadConfigFromFile|configLoader|createServer\(` read at call
  grain (an awaited or assigned call):
  - at 35797660: 13 lines, 4 calls, minus 1 plain `http.createServer` (`.frontend-dev/runners/category-views-fixture-proxy.mjs:72`)
    = **3**: `fe-s-32/vite.worktree.config.ts:48`, `fe-s-38/resolve-config.mjs:59`, `fe-s-39/vite.worktree.config.mjs:33`;
  - at HEAD: 20 lines, 2 calls, minus 1 plain = **1**.

### Each loader's disposition

| # | loader | disposition | `.vite-temp` writes (deciding run) | run |
|---|---|---|---|---|
| 1 | script dev `vite --configLoader runner` | runner | 0 | HTTP 200, stopped closed |
| 2 | script build `tsc -b && vite build --configLoader runner` | runner | 0 | exit 0, index.html built |
| 3 | script preview `vite preview --configLoader runner` | runner | 0 | HTTP 200, stopped closed |
| 4 | `fe-s-38/resolve-config.mjs:63` (`:59` at 35797660) | runner | 0 | exit 0, RESOLVED_JSON |
| 5 | `fe-s-32/vite.worktree.config.ts:48` | RETIRED (deleted, W1-S65) | -- | -- |
| 6 | `fe-s-39/vite.worktree.config.mjs:33` | RETIRED (deleted, W1-S65) | -- | -- |

- **Named residuals: none.**
- The old-script control on the same tree, `vite`: 3 writes.

### The build decision

`build` takes runner, because the dist manifests are EQUAL. `vite build --configLoader bundle` and
`--configLoader runner` were built on one tree (portal working tree = 06bf98fa's content), into
`<WS>/.scratch/build-bundle` and `<WS>/.scratch/build-runner`. The sha256 of every file gives:
- 73 files and 73 files;
- 0 files on one side only;
- 0 with the same name and a different hash;
- `MANIFESTS EQUAL: True`.

The bundle build wrote through the junction as expected (the same 3-4 events as every bundle load).

## The criteria (deciding runs, portal 06bf98fa)

`IRPT_FE_DEV_PORT` was exported on every `bun test` run:
- AC2, AC3, AC4, AC7, AC9, AC10 and AC11: 5261, measured closed (ECONNREFUSED) with my server down;
- AC5: 5262, measured closed;
- AC6: 5261, with my own server up under the committed script.

The results:
- **F45-AC1**: `$ tsc -b --noEmit` / `rc=0` at 06bf98fa.
- **F45-AC2** (timeout 240, rc 0, 64 s, 6 pass / 0 fail):
  - the new script (`bun run dev --port 5900`): HTTP 200, serves this worktree, `.vite-temp` BEFORE `[]` AFTER `[]`, writes 0, port closed after the stop;
  - the old script's control on 5903: writes 3;
  - the working and committed dev lines are equal;
  - `DEV SCRIPT WRITES NOTHING THROUGH THE JUNCTION: yes`.
- **F45-AC3** (timeout 120, rc 0, 62 s): 1464 committed paths at 06bf98fa, the control finds 4 of 4 at 35797660,
  `PER-CELL VITE OVERRIDES REMAINING: 0 of 4`.
- **F45-AC4** (the same run): the control reads `NAMES A DEFAULT`, the committed paragraph names the refusal,
  `fe-s-19 NAMES NO DEFAULT PORT: yes`.
- **F45-AC5** (timeout 180, rc 0, 11 pass / 0 fail): read as `git cat-file blob HEAD:<path>` at 06bf98fa, 5 of 5 maps
  bound, the in-memory perf-9 control 0 of 5, the seeded uncommitted in-place edit moves the checkout read and not the
  committed one: `F41-AC5 READS THE COMMITTED BLOB: 5 of 5 maps`.
- **F45-AC6** (timeout 240, rc 0, 2 pass / 0 fail). My server was restarted after the portal commit, because a debug
  run had re-optimized the shared `portal/.vite` under the first one. It was started with
  `bun run dev --port 5261 --strictPort` after 5261 was measured closed: `$ vite --configLoader runner --port "5261"
  --strictPort`, `VITE v7.3.5 ready in 1530 ms`, under node. Results: `PRECONDITION ... MET (... served from worktree
  C:/tmp/wk-irpt_fntend-7-1-fe-s-45/portal ...)`, `PAGE CRASHES: 0`, `BODIES MOUNTED: 2 of 2`,
  `UNCERTAIN WITHOUT A WIRE STATE: 2 of 2`.
- **F45-AC7, the census of record** (timeout 600, rc 0, 91 s): `Ran 578 tests across 102 files`, **560 pass, 18 skip,
  0 fail**. Every skip is a browser criterion skipped by name on `PRECONDITION ... ABSENT`. The run carries every
  FE-s-45 verdict line.
- **F45-AC9** (timeout 600, rc 0, 58 s, 6 pass / 0 fail): the reach and dispositions above;
  `EVERY CONFIG LOADER IN THE REACH WRITES NOTHING THROUGH THE JUNCTION: 4 of 4`.
- **F45-AC10** (the same run):
  - the dev script's listener on 5900 is pid 40880, **node.exe**;
  - its preloaded record is `"release":"node","bun":null`: **process.release.name = node**;
  - the negative control is the first run's line read from df3a3353, `bun --bun vite --configLoader native`, whose
    listener on 5901 is **bun.exe** with no record;
  - the bun:test process itself prints `process.release.name "node", process.versions.bun "1.3.9"`, which is why the
    name alone is not the verdict (row W1-S69);
  - `THE DEV SERVER RUNS ON NODE: yes`.
- **F45-AC11** (the same run): `/api/auth/me` goes through vite.config.ts's `'/api/auth'` entry and its rewrite
  function. It answers **401 under the new script** (5900) and **401 under the old** (5903). vite's own answer for the
  unproxied `/fe-s-45-not-proxied` is 200 on both, so the 401 came from upstream.
  `A PROXIED /api ROUTE ANSWERS THE SAME STATUS UNDER THE NEW AND OLD DEV SCRIPTS: yes`.
- **F45-AC8** (judgment): recorded, not graded.
  - RULING U leaves no residual at 06bf98fa: 6 of 6 loaders dispositioned, 4 on runner under node with 0 writes, and
    2 retired. W1-S68's resolver is among the 4.
  - F41-AC5 grades what is committed (AC5).
  - For L9: F45-AC10's named field does not discriminate by itself (W1-S69), and my row S67's cost (3) is corrected
    by W1-S70.

Determinism: residuals.test.ts ran under all three of its invocations (600, 240, 120) and inside the whole suite. It
gave the same verdicts each time: 0 writes on every kept loader and 3 on the control, in 58, 64 and 62 s. A pre-commit
debug run of the same file (the committed dev line still bun, build and preview still bundle) read NO for AC2 and AC9.
It named 4 residuals and 4 writes from the bundle build, so the verdict lines are shown able to say no.

## Servers

I started and stopped these, each measured closed after its stop:
- my own 5261 server twice (the first killed after the debug runs, the second after F45-AC6);
- the driver's servers on 5900-5903 in each run.

A final listener sweep shows only 5173, 5174 and 5949, none of them mine. 5263 was never touched.
