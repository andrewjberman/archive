# DSGN_RBNDV2 -- round 4 close run: the alpha-white class sweep (TO-RV-w-1, criterion RB4W1-AC3)

**Author:** `2.0.0_SA_COO~RB`, 2026-10-15 13:1xZ. **Branch read:** `feature/dsgn-rbndv2-light` @7f8731df (LOCAL, never pushed), dev build at port 5174 (HMR from `rbndv2-int`), against the real backend.
**Method:** the scratch UI walker copy (`walk-rbprobe.mjs`, untracked, deleted at round close) signed in as the walker (armed, one load, one action, disarmed; the post-disarm login was REFUSED, HTTP 401, every time), pressed a label or clicked a selector, and read the open dialog. A text element counts as "white" when its computed colour is `rgb(255,255,255...)` or `oklab(0.99...)`.

## Drain (merge-time checks, on the integration worktree after the portal merge 7f8731df)

- Proof `VALID` re-run from the worker's worktree BEFORE the merge; diff reviewed: 3 portal files (`src/index.css` +140, `rb-1-t.tokens.test.ts` 6 lines, new `rb-4-w1.alpha-sweep.test.ts`), 0 non-ASCII bytes; the exception rule is the last rule of the block.
- typecheck `tsc --noEmit` rc=0; `src/__tests__/dsgn-rbndv2` 5 pass 0 fail (5 files), `VERDICT: ALPHA-SWEEP-OK`, selectors before 4, after 118, difference control 120 failures on the base text; eslint rc=0.
- Workspace merge `c73bac20c0` (safe-merge fast lane, 3 files); worktree `rbndv2-12` and both worker branches removed (portal branch was an ancestor of the feature branch; C: 21G free).

## The computed colours (AC3, before and after)

| modal (trigger) | white text BEFORE | white text AFTER | what the AFTER ones are | inactive chips AFTER |
|---|---|---|---|---|
| Index Performance (press "S&P 500") | 3 | **1** | the ACTIVE chip `1Y`: `rgb(255,255,255)` on the violet fill (intended) | `30D`, `90D`, `3Y`: `rgb(10, 23, 51)` (navy ink) |
| U.S. Regime: Momentum (press "Multi-Asset Momentum") | 4 | **3** | active chip `90D` white on violet (intended); tooltip labels `Score`, `RSI Score` `rgba(255,255,255,0.85)` on the violet tooltip (legitimately white, unchanged) | `1Y`, `3Y`: `rgb(10, 23, 51)` |
| CNN Fear & Greed (press "Fear & Greed") | 0 (inactive) | **1** | active chip `90D` white on violet | `7D`, `14D`, `30D`: `rgb(10, 23, 51)` |
| Global RSI (chart-bar click) | 0 | **1** | active chip `Spotlight` white on violet | not in this view |

**Reading:** every inactive chip now computes to the ink `rgb(10, 23, 51)` (was `oklab(0.999994 ... / 0.6)` in Index Performance and U.S. Regime). Every remaining white text element is either an active chip on its solid violet fill (the defect-2 fix: it computed navy `rgb(10, 23, 51)` at about 2.6:1 before) or a tooltip label on its violet tooltip. Zero white-alpha text on a light surface remains. The chart tick fills stay `rgb(74, 88, 120)` (the round-3 token), so the sweep moved nothing else.
The "before" counts in the first table of `ROUND4_RSI_AND_ALPHA_READ_20261015.md` counted inactive white-alpha only; the "after" counts above also include the active chips, which are white by design, so the criterion's expectation (inactive chip navy, active chip white) is read per chip, not by the total.

## Surprise rows

`DSGN_RBNDV2-W12-S1` (OBSERVATION, INERT): the proof kind enum has no stylesheet member. No new armed row. `W1-S2` (text-white on a solid fill) is measured fixed by this read.
