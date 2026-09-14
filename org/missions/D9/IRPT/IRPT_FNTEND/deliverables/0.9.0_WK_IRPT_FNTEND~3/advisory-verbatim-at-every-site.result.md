# FE-s-42 result -- RULING W at every site it names, and no test rewrites committed evidence

- Task order: `IRPT_FNTEND.TO-FE-s-42` (round 7, cell `FE-s-42`). Its source is `1.0.0_SA_CTO` RULING Z, round-6 analysis @4713211d87 s.3.
- Worker: `0.9.0_WK_IRPT_FNTEND~3`.
- Worktree pair: `C:/tmp/wk-irpt_fntend-7-3-fe-s-42`, with the portal nested inside it. Both are on the branch `wk-irpt_fntend-7-3-fe-s-42`.
- Base: workspace `4d11c008c2`, portal DEV `35797660`.
- Portal change: `e028fb4dde86a39793a897a2ee9d99190e540aac` (LOCAL; the portal is FROZEN, never pushed or merged).

## 1. What changed, site by site

| Site | Row | Change |
|---|---|---|
| `contracts/adapt.ts` (the directory cohort's advisory, formerly `:585`) | W3-S29 | `ADVISORY_FOR_WIRE[...] ?? 'unknown'` becomes `advisoryFromWire(wire.cohort.advisory_status)`. That is the Holdings rule, the same function, so an out-of-enum token is carried verbatim as `{ outOfEnum }`. It also looks up own properties only: a token such as `constructor` used to resolve to `Object`'s constructor function, and no longer does. |
| `contracts/index.ts` `CohortValue` | W3-S29 | Admits `OutOfEnumAdvisory`. Nothing else in the file changed. |
| `contracts/validate.ts` | W3-S30 | New `advisoryOneOf`. It accepts a closed-set member, or exactly `{ outOfEnum: string }`. It still refuses an unflagged out-of-range string, and any other object. It is applied at two places: the directory cohort value, on the **advisory axis only** (every other axis stays `oneOf`); and the Holdings classification pin (formerly `:448`). |
| `header/ScopeSummary.tsx` | W3-S29 | Adds `cohortToken(value)`. It decides with `isOutOfEnumAdvisory` and prints `ADVISORY_OUT_OF_ENUM_WORDS`, both imported from `tabs/holdings/slices.ts`. An out-of-enum value renders as `advisory: <token> (<words>)` with `data-cohort-out-of-enum="true"`. An in-enum value's button is byte-identical to DEV 35797660. |
| `export/ReceiptPanel.tsx` | W2-S33 | The reason line adds FE-s-40's `UnnamedReasonCodeFlag`, imported from `render/Page.tsx`, with slot `public-reason-code-flag`. A named code's line is byte-identical to before. |
| fe-s-32 and fe-s-40 browser tests | W3-S31 | Details below. |

The two browser tests changed as follows:
- **Default destination.** Captures go to `.scratch/fe-s-<n>/captures/`, outside every folder named `deliverables`.
- **Named destination.** They go into a committed folder only when the run names it in `IRPT_FE_CAPTURE_DIR`.
- **One rule.** The destination logic lives in one place, `__tests__/fe-s-42/_captures.ts`.
- **The proof.** Each test reads `git status --porcelain --untracked-files=all` of the deliverables tree, plus the sha256 of every path listed. It reads once before the driver runs and once after. It prints `CAPTURES OUTSIDE EVERY COMMITTED DELIVERABLES FOLDER: yes` only when the reading is unchanged, the destination is outside every such folder, and the captures exist.
- **Drivers.** Neither driver was edited: each writes only to its `argv[4]`, which the test now supplies.

## 2. The runs

| Criterion | Run | Deciding output |
|---|---|---|
| F42-AC1 | `bun run typecheck` at e028fb4d's tree | `rc=0` |
| F42-AC2..AC5 | `bun test .../fe-s-42/every-site.test.ts`, IRPT_FE_DEV_PORT=5269 (closed) | `...VERBATIM AND FLAGGED IN THE HEADER: yes`, `...UNCHANGED: 3 of 3`, `VALIDATE: ... yes` (5 of 5 arms), `RECEIPT REASON: ... yes`; 4 pass, 0 fail |
| F42-AC6, AC7 | `bun test .../fe-s-32/holdings-in-a-browser.test.ts`, IRPT_FE_DEV_PORT=5263 (own server, MET) | `HOLDINGS UNDER THE GATE, IN A BROWSER: 4 of 4`; 15 of 15 captures in `.scratch/fe-s-32/captures/`; tree 0 paths before and after; `CAPTURES OUTSIDE ...: yes`; **8 pass, 0 fail** |
| F42-AC8 | `bun test .../fe-s-40/band-at-390.test.ts`, IRPT_FE_DEV_PORT=5263 | `REASON CODE INSIDE ITS BAND AT 390: 16 of 16`; 8 of 8 captures in `.scratch/fe-s-40/captures/`; `CAPTURES OUTSIDE ...: yes`; **3 pass, 0 fail** |
| F42-AC9 | whole suite, IRPT_FE_DEV_PORT=5263 measured closed, portal e028fb4d | **553 pass, 18 skip, 0 fail** of 571 across 101 files |

The browser runs used my own server on 5263, launched after measuring the port closed and stopped before the census. The sibling port 5261 was never touched.

### How the new counts reconcile

- **The census against the baseline.** The baseline is the same suite at the unmodified base: 547 pass, 16 skip, 2 fail of 565 across 100 files. The census adds 6 tests: the 4 in fe-s-42, plus F42-AC7 and F42-AC8. It adds 2 skips: AC7 and AC8, which are gated off while the server is down.
- **The baseline's two fails.** Both were bun timeouts at the 5000 ms default, in files outside this grant. Row W3-S33 carries them.

### The both-ways evidence

- **fe-s-42 test on the unmodified portal.** It read:
  - AC2 `advisory: unknown`, verdict `no`;
  - AC4 2 of 5 arms (the flagged shape was refused on both Holdings and the directory);
  - AC5 no flag on `IR-EXPORT-RENDER-REJECTED`, verdict `no`.
- **AC3's "before" markup.** It was checked against the buttons that unmodified run printed. They are byte-identical to the post-change in-enum buttons.
- **Capture mutant** (`.scratch/captures-mutant.ts`, not committed). It wrote one probe file into this worker's own deliverables folder. The instrument read `0 paths -> 1 path -> CHANGED` and printed `CAPTURES OUTSIDE EVERY COMMITTED DELIVERABLES FOLDER: no`. The probe was then unlinked, and the tree digest returned to `e3b0c44298fc1c14`.

## 3. Rows filed (INVESTIGATION_v2.md, all OBSERVATION, INERT, UNDER_INVESTIGATION)

- **IRPT_FNTEND-W3-S33.** F40-AC5 and F41-AC2 sometimes run past bun's 5000 ms default: at the base, twice in the whole suite, and F40-AC5 once more on its own. The census of record read 0 fail. A later cell's census can go red on them with nothing it may change.
- **IRPT_FNTEND-W3-S34.** RULING X's three granted tests (fe-s-1, fe-s-9, fe-s-16) needed no change. None of their asserted values is reached by RULING Z, and all three pass as committed.
- **IRPT_FNTEND-W3-S35.** A no-status `directory-search` body through the real adapter yields a document (UNCERTAIN, with no reason) that `validateContract` refuses. The FE-s-42 test gives its body a READY status, so that AC4 grades the cohort only.

## 4. Declared, not done

- **The adapt.ts comment at `:447-448`.** It still says the directory cohort accepts `ADVISORY_FOR_WIRE`'s result. That is still true, since `CohortValue` still takes those members. The one-purpose bound limits the file to the site formerly at `:585`, so the comment was left.
- **A non-authoritative directory cohort.** It still renders `advisory: unknown` under "Cohort (not asserted)". This is the authoritative gate, the same one Holdings' `renderedClassification` applies. It is not a rename. Graded at L9 under F42-AC10.
- **The named-run branch of the capture rule** (`IRPT_FE_CAPTURE_DIR` pointing into a committed folder). No browser run exercised it, because that run would dirty the tree it grades. The branch that decides it (`insideDeliverables`) was exercised by the mutant above.
- **Not touched:**
  - the four reader tests (fe-s-11, fe-s-18, fe-s-22, fe-s-26);
  - `fe-s-32/holdings-no-answer.json` and every fixture map;
  - the two `vite.worktree.config` files;
  - `package.json`;
  - both drivers.

## 5. Commits

- **Portal:** `e028fb4d`, LOCAL on `wk-irpt_fntend-7-3-fe-s-42`. Nine files: the five source files, the two capture writers, and `__tests__/fe-s-42/{every-site.test.ts,_captures.ts}`.
- **Workspace:** the three rows, this file, the proof instance and the order's `complete` flip, in one commit, LOCAL on `wk-irpt_fntend-7-3-fe-s-42`.
