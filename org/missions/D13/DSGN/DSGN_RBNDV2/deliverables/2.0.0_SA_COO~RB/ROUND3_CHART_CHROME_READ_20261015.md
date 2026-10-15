# DSGN_RBNDV2 -- round 3: the modal chart chrome and footer read (RV-c-1), measured in the live build

**Author:** `2.0.0_SA_COO~RB`, 2026-10-15 ~11:5xZ. **Order:** `DSGN_RBNDV2.TO-RV-c-1.modal-chart-chrome.md` (round 3, decomp v3 @74ed99710a), merged into `feature/dsgn-rbndv2-light` @6396217d (LOCAL, never pushed).
**Asked by:** the CTO's round-2 analysis `ROUND_ANALYSIS.round2.md` @3c2a9cae02: "proved by a computed-style read of a tick in both modals", and the footer no longer clipping the signal row.

## 1. Merge-time portal checks (the CTO's item 2, printed per merge)

On `feature/dsgn-rbndv2-light` @6396217d: `bun run typecheck` rc=0 (0 errors); the `dsgn-rbndv2` tests 24 pass, 0 fail (24 files); eslint rc=0 on 68 changed files (0 errors). The same counts are in the workspace merge
commit message @fed0709400.

## 2. The read

A patched scratch copy of the UI walker (`walk-rbprobe.mjs`, a copy of `.claude/skills/ui-walk/walk.mjs` that prints computed styles after a press; the copy is deleted when this round closes and was never committed) loaded `/market` on the
dev build of the feature-branch worktree at port 5174 against the real backend, signed in as the walker (armed, one load, one press, disarmed; the post-disarm login was REFUSED both times), pressed the panel label that opens the modal, and read the open dialog:

| modal | chart tick `fill` (computed) | axis line `stroke` | grid line `stroke` | body `scrollHeight` / `clientHeight` | surface top to bottom (viewport 900) |
|---|---|---|---|---|---|
| CNN Fear & Greed Index (press "Fear & Greed") | `rgb(74, 88, 120)` = `#4A5878` = `--rb-ink-3` | `rgb(107, 117, 144)` = `#6B7590` = `--rb-quiet` | `rgb(227, 231, 239)` = `#E3E7EF` = `--rb-rule` | 856 / 730 (the body scrolls; its surface is at the frame's cap, 16 to 884) | 16 to 884 |
| U.S. Regime: Momentum (press "Multi-Asset Momentum") | `rgb(74, 88, 120)` | `rgb(107, 117, 144)` | `rgb(227, 231, 239)` | 571 / 571 (no scroll: nothing is clipped) | 96 to 805 |

**Reading:** both modals' chart chrome resolves to the three navy-grey tokens, never white, in the rendered page. The Market Regime surface no longer carries the 72vh cap: its body needs no scrolling at 1440 x 900, so the
signal row is fully visible above the footer (its round-2 clip is cured). The Fear & Greed body is taller than the viewport and scrolls inside the frame's own cap with its footer in view; that is the frame working as designed.

## 3. What is still open

`IndexPerformanceModal.tsx` and `RSIModal.tsx` hold the same literal white chart props (rows `DSGN_RBNDV2-W10-S1`, `W10-S2`): order `RV-c-2` (direct act, round-less) is cut for them. `KeywordSentimentModal.tsx` holds none. The FWD-5 walk (288 faint
signal-colour elements on `/market` alone) waits on Andrew's YES to call `3c44`; FWD-4 waits on call `be0b`.
