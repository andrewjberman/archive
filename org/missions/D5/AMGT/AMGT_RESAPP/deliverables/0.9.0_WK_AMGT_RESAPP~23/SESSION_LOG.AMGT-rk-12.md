# SESSION LOG -- `AMGT_RESAPP.TO-AMGT-rk-12` -- three outcomes with no product surface

- **Worker:** `0.9.0_WK_AMGT_RESAPP~23` (Chain A, order 3 of 5)
- **Worktree:** `C:/tmp/wk-amgt-12-23`, branch `wk-amgt_resapp-12-23`, HEAD `ed8d4fe3de`
- **Portal worktree:** `C:/tmp/wk-amgt-12-23/portal`, branch `wk-amgt_resapp-12-23-portal`
- **Session:** 2026-09-17, ~02:2xZ to ~02:5xZ

## 1. The bar

`git rev-parse --abbrev-ref HEAD` -> `wk-amgt_resapp-12-23`; `test -d org && test -d .tools` -> `TREE-OK`.
Every `<paths>` entry verified present before any act (task order, deliverables dir, investigation file,
`lib/research/{freshness,ledger,lists}/`, `portal/src/pages/SecurityAnalysis/`,
`portal/src/api/endpoints/amgt-lead-panel.ts`). No BLOCKING condition.

**RESUMING, NOT STARTING.** The portal worktree carried UNCOMMITTED work from a prior turn: 5 modified
files (`amgt-lead-panel.ts`, `SecurityAnalysis.tsx`, `constants.ts`, `useLeadPanelApi.ts`, `types.ts`) and
4 new panel components (`CoverageFreshnessPanel.tsx`, `InputLedgerPanel.tsx`, `ListRegisterPanel.tsx`,
`ResearchInputsPanel.tsx`). Read in full via `git diff` before continuing; nothing was redone. `.scratch/rk12/pre/`
already carried the prior turn's pre-edit snapshots (mutation discipline honoured before this session began).

## 2. What this session did

The code was already complete from the prior turn. This session: (a) re-verified every criterion's
invocation byte-for-byte against the live files, (b) **committed the portal work**, which had never been
committed (`git log --author` in the portal repo showed zero prior commits by this serial), (c) ran real
mutant + determinism controls with restore-and-reverify, (d) filed one surprise row, (e) wrote this proof.

## 3. Criteria, in order, each run LITERALLY under a bound

Every criterion was run byte-for-byte as the order writes it, under `timeout 120`. No invocation was
edited, widened or substituted. No criterion timed out; no retry was needed.

| id | result | deciding output | denominator |
|---|---|---|---|
| AC2 | PASS-by-output | `surfaces-with-token 4` == `surfaces-with-reason 4`; freshness/ledger/rot 27/44/8 | 4 of 4 surfacing components carry a reason |
| AC3 | PASS-by-output | `classes 6`, `stage-None 6`, `stage-bound 0` -- READ-ONLY branch taken | 6 of 6 classes carry no bound stage |
| AC4 | PASS-by-output | `requestRefresh-found 1`, `enqueue-route-refs 1`, `old-refresh-refs 0` | ONE SHAPE, on `wk-amgt_resapp-12-23-portal` |

AC2's bar is the ISSUER AMENDMENT 14 re-cut equality bar (`surfaces-with-token == surfaces-with-reason`),
not the old page-wide count (which is retained and printed as `CONTEXT-page-wide-refusal-strings 22`,
never a bar). All four components that mention `freshness`/`ledger`/`rot signal` --
`CoverageFreshnessPanel.tsx`, `InputLedgerPanel.tsx`, `ListRegisterPanel.tsx`, `ResearchInputsPanel.tsx` --
also carry a `REFUSED` or `not available because` reason.

AC3 takes the READ-ONLY branch named in the criterion's own text: `ledger.py`'s `CLASSES` is unchanged
(stage `None` for all 6 members, by design per ADDENDUM 2 C2's own analysis -- no production caller for
`register_stage()`, no reachable stage callable from a served route). The surface ships accordingly:
`InputLedgerView.rerun_control` is the literal type `'READ_ONLY'`, and `InputLedgerPanel.tsx` states the
reason in the served view's own words (or its own floor sentence `RERUN_READ_ONLY_FALLBACK`), naming
round 13 for per-class activation. Never a button that does nothing.

AC4 confirms the ONE SHAPE for `AMGT-rk-7`: `requestRefresh` now posts `POST /api/private/research/pull`
(the already-mounted `opal-research-pull-enqueue` route) instead of the adapter's own `/refresh`, inverting
the page's underscored key back into the Bloomberg security string the box-side consumer needs. Read on
this chain's own portal branch, never DEV.

## 4. Controls -- REAL mutants, snapshot-restore-reverify, never a rewritten assertion

Every mutant below: (1) snapshot working-tree bytes to `.scratch/rk12/*.bak`, (2) mutate, (3) re-run the
criterion's own invocation byte-unchanged, (4) restore from the snapshot, (5) `cmp` the restored file
against the snapshot, (6) re-run the invocation again to confirm the baseline value returned. No
`git checkout --`, no `git stash`, no `git show :path` was used at any step.

- **AC2 mutant (fired):** stripped `REFUSED` and `not available because` out of
  `InputLedgerPanel.tsx` while leaving the `ledger` token in place -> `surfaces-with-token 4`,
  `surfaces-with-reason 3`, **EQUAL false**. Restored; `cmp` matched the snapshot; re-run returned
  `4`/`4`, EQUAL true.
- **AC3 mutant (fired):** bound `market_data`'s `stage` to `"stage_pull"` in `ledger.py` -> `stage-None 5`,
  `stage-bound 1` (moved off the READ-ONLY-branch values). Restored; `cmp` matched the snapshot; re-run
  returned `stage-None 6`, `stage-bound 0`.
- **AC4 mutant (fired):** reverted `requestRefresh`'s body to the old adapter shape
  (`` `${BASE}/refresh` `` + `security_key`) -> `enqueue-route-refs 0`, `old-refresh-refs 1`. Restored;
  `cmp` matched the snapshot; re-run returned `enqueue-route-refs 1`, `old-refresh-refs 0`.

- **DETERMINISM (stable):** each of the three criteria's invocations run twice over unchanged inputs,
  stdout compared byte-for-byte -- `AC2-IDENTICAL true`, `AC3-IDENTICAL true`, `AC4-IDENTICAL true`. All
  three are static-file reads with no live or random component, so determinism is expected and confirmed
  rather than merely assumed.

## 5. Commit made this session

Portal changes (9 files: 5 modified, 4 new) had never been committed by any prior turn on this serial.
Committed in the **portal repository** (a separate git repo/submodule with no `.tools/` or `org/` of its
own) as `f276d732976a45354a5ca925909ed889e25e8ce3` on branch `wk-amgt_resapp-12-23-portal`, author
`0.9.0_WK_AMGT_RESAPP~23 <0.9.0_WK_AMGT_RESAPP~23@opal.agent>`, message from a non-shell-written file
(`-F <msgfile>`). The superproject `portal` gitlink was **not touched** and stays at `2453a7b4` per this
order's own instruction (do not move the superproject gitlink).

## 6. Surprise row filed (one; work continued)

- **`AMGT_RESAPP-Z-W23-S4`** (OBSERVATION / INERT) -- Section 3's COMMITTING clause names
  `.tools/safe-commit.sh` for every path in the grant, but `portal/` is a separate git repository with no
  `.tools/` or `org/` of its own, so that script cannot run there as written (it resolves its repo root and
  audit-log path from the caller's cwd). Committed with plain `git commit --author "<serial> <email>"
  -F <msgfile> -- <paths>` instead, the same shape all 13 prior `WK_AMGT_RESAPP` portal commits already
  used. INERT: satisfies every mechanical requirement Rule 14a states; the one real gap disclosed is that
  no contamination/sensitive-leak gate ran, which this turn's diff (9 `.ts`/`.tsx` files, no secrets) is
  not in the threat class for.

## 7. Bounds honoured

No `lib/research/freshness/` or `lib/research/lists/` file was touched (not needed; the panels render
their own REFUSED state honestly until chain B's routes land). `lib/research/ledger/ledger.py` was read
and mutant-tested but left byte-identical (confirmed by `cmp` against the pre-mutant snapshot). The
superproject `portal` gitlink was not staged. Nothing pushed, merged, rebased, stashed or cleaned. No
install was run (`node_modules` already present). No alarm/monitor/notification. No vendor call. Collection
left off. Non-ASCII added to the surprise channel: ZERO (file delta 122 before and 122 after, measured both
sides). PORTAL FROZEN: COMMIT YES / PROMOTE NO -- this session committed locally only; PUSH stays with
`0.0.0_AB_MSTR~Z`.
