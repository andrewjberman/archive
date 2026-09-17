# SESSION LOG -- `AMGT_RESAPP.TO-AMGT-rk-16` -- FWD-6's compare surface

- **Worker:** `0.9.0_WK_AMGT_RESAPP~23` (Chain A, order 5 of 5 -- the chain's FINAL order)
- **Worktree:** `C:/tmp/wk-amgt-12-23`, branch `wk-amgt_resapp-12-23`, HEAD `1fffcfa943` at start
- **Portal worktree:** `C:/tmp/wk-amgt-12-23/portal`, branch `wk-amgt_resapp-12-23-portal`
- **Session:** 2026-09-17

## 1. The bar

`git rev-parse --abbrev-ref HEAD` -> `wk-amgt_resapp-12-23`; `test -d org && test -d .tools` -> `TREE-OK`.
Every `<paths>` entry verified present before any act: the TO file itself, the deliverables directory, the
investigation file, `portal/src/pages/SecurityAnalysis/`, `portal/src/api/endpoints/amgt-lead-panel.ts`,
`portal/src/App.tsx`. No BLOCKING condition. AC1's pre-state was re-verified live and matched the issuer's
own pre-check exactly: 34 keys, `keys_with_2plus_stamps 4` (BA_US_Equity, BABA_US_Equity, SAP_GY_Equity at
5 stamps each, NVDA_US_Equity at 2).

## 2. What this session did

The reading surface FWD-6 asked for did not exist: AC3's own baseline read `version 1, earlier 0, compare
1, what moved 0` across 23 `.tsx` components, and the two `version`/`compare` hits were incidental code
comments (`RankedChart.tsx`, `ProvenanceLine.tsx`), not a compare feature.

Built, in `portal/`:

1. **`types.ts`** -- `ModelBlockVersionEntry`, `ModelBlockVersionsView`, `ModelBlockCompareField`,
   `ModelBlockCompareView`, transcribed from the MEASURED store shape (AC1's own read: stamp folders
   `YYYYMMDDTHHMMSSZ` under `derived/model_block/<security_key>/`), never invented.
2. **`api/endpoints/amgt-lead-panel.ts`** -- `getModelBlockVersions` and `compareModelBlockVersions`,
   declared against that contract. THE SERVER ROUTE IS NOT THIS ORDER'S: AC2 was moved off this cell by
   ISSUER AMENDMENT 8 onto `AMGT-rk-6` AC5 (chain B's route + deploy, ruling row `AMGT_RESAPP-Z-S127` under
   `AMGT_RESAPP-Z-S124`). Until that route lands, these calls 4xx at the edge -- the same documented
   relationship `getCoverageFreshness` had to its own route before `AMGT-rk-12` built it.
3. **`constants.ts` / `hooks/useLeadPanelApi.ts`** -- query keys and `useModelBlockVersions` /
   `useModelBlockCompare`, following the existing `SURFACED_STALE_TIME_MS` (30 min) discipline: a landed
   stamp does not move once written, so this is not a live feed and touches no monitoring moratorium.
4. **`components/VersionComparePanel.tsx`** (new) -- a picker of NAMED stamps (never an index or a
   relative label), a current-vs-earlier compare table, and a `what moved: N of M figure(s)` summary line.
   Wired into `tabs/ModelTab.tsx`, below the existing model sheet.

`portal/src/App.tsx` was read (no change needed -- no new route, only an existing tab enhanced).

`npm run typecheck` (`tsc -b --noEmit`) and `npx eslint` on every touched/new file: clean, zero errors, zero
warnings (one transient `react-hooks/set-state-in-effect` warning was fixed by moving the stamp-reset logic
to render-time state adjustment rather than an effect -- React's own documented pattern for resetting state
on a prop change).

## 3. Criteria, in order, each run LITERALLY under a bound

Every criterion was run byte-for-byte as the order writes it, under `timeout 120`. No invocation was
edited, widened or substituted. No criterion timed out; no retry was needed.

| id | result | deciding output | denominator |
|---|---|---|---|
| AC1 | PASS-by-output | `keys_with_2plus_stamps 4` | 34 keys in the live store; 4 carry 2+ stamps |
| AC3 | PASS-by-output | `version 48`, `earlier 22`, `compare 37`, `what moved 1` | 24 SecurityAnalysis `.tsx` components |

AC2 does not appear in this order's `<proof_of_spec>` block -- ISSUER AMENDMENT 8 moved it to `AMGT-rk-6`
AC5 and narrowed this cell's grant (removing `lib/research/api/scoped_amgt.py`). This instance's `acceptance`
array carries AC1 and AC3 only, matching the checker invocation the order names.

## 4. Controls

**Mutant (AC1):** the threshold in a scratch copy of the invocation was moved from `>=2` to `>=100`
(the store itself was never mutated -- writing to the versioned bucket is outside this order's grant and
would corrupt the very population AC1 measures). Moved `keys_with_2plus_stamps` to `keys_with_100plus_stamps
0`; restoring the threshold to `>=2` reproduced `4` again. The bar discriminates.

**Mutant (AC3):** `VersionComparePanel.tsx` was snapshotted to `.scratch/rk-16/VersionComparePanel.tsx.snapshot`
(6951 bytes), then overwritten with `export {}`. Re-running AC3's own invocation moved the counts to
`version 4, earlier 0, compare 4, what moved 0` (the residual 4/4 are incidental substring hits from
`RankedChart.tsx`/`ProvenanceLine.tsx`'s existing comments plus the string `"VersionComparePanel"` itself
inside `ModelTab.tsx`'s import line -- `earlier` and `what moved` both went to exactly 0, which is a FAILING
bar under the criterion's own text). Restored from the snapshot; `cmp` matched byte-for-byte; re-run
reproduced `version 48, earlier 22, compare 37, what moved 1`.

**Determinism:** AC1 and AC3's invocations were each run twice over the same committed inputs; `cmp` on the
captured stdout showed byte-for-byte identical output both times (`AC1-IDENTICAL`, `AC3-IDENTICAL`). Both
are static reads (an S3 listing over an already-landed store, and a `glob`+string count over committed
source) with no live, random or clock-dependent component, so identical repetition is the expected shape.

## 5. Commit

Portal repo has no `.tools/safe-commit.sh` of its own (row `AMGT_RESAPP-Z-W23-S4` already covers this --
the same substitute, `git commit --author "<serial> <email>" -F <msgfile>`, is used again here unchanged):
`d3962a722670e4f5dbf45d95b0f770ddc68a709f` on branch `wk-amgt_resapp-12-23-portal`, 6 files changed (5
modified, 1 new), verified via `git log -1 --format='%an <%ae>'` -> `0.9.0_WK_AMGT_RESAPP~23
<0.9.0_WK_AMGT_RESAPP~23@opal.agent>`. Superproject portal gitlink NOT staged/moved, per this order's own
instruction and the standing portal freeze (COMMIT YES / PROMOTE NO). No push, no merge, no rebase.

The workspace-repo commit (this session log, the proof instance, and the TO's own `<status>` flip) rides
`.tools/safe-commit.sh` as instructed.

## 6. Surprises

None filed this order. The work proceeded exactly as scoped by ISSUER AMENDMENT 6 and AMENDMENT 8: the
front-end surface was built and verified against the two criteria this order actually carries (AC1, AC3);
AC2 (the server route) is chain B's declared responsibility, not a gap this cell needed to route around.

## 7. Chain A status

With `AMGT-rk-16` terminal, chain A's whole five-order queue (`AMGT-rk-1`, `AMGT-rk-8`, `AMGT-rk-12`,
`AMGT-rk-15`, `AMGT-rk-16`) is done. `AMGT-rk-15` stays OPEN on AC4 (root-caused, ARMED row
`AMGT_RESAPP-Z-W23-S5`, disarm owner chain B) per the issuer's own drain of that order -- not reopened or
revisited here, per this order's explicit instruction ("not yours to revisit").
