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

## 2b. Addendum: the direct act `RV-c-2` (the RSI and Index Performance modals), merged and read

Order `DSGN_RBNDV2.TO-RV-c-2.modal-chart-chrome-2.md` (direct act, round-less), proof VALID when re-run from the worktree before the merge; portal merge @cf2bdeaa; merge-time portal checks printed in the workspace merge commit @4df2b0eb40: typecheck rc=0 (0 errors), `dsgn-rbndv2` tests 25 pass, 0 fail (25 files), eslint rc=0 (69 files, 0 errors). No white-alpha literal remains in either file.

Live read, same method as section 2 (the scratch walker copy is now deleted): pressing the row label "S&P 500" in the Equity Performance table opens the Index Performance modal ("S&P 500"): chart tick `fill` `rgb(74, 88, 120)`, axis `stroke` `rgb(107, 117, 144)`, grid `stroke` `rgb(227, 231, 239)` (the three tokens), body 615 of 615 (no scroll), surface 74 to 827 in a 900 viewport.
**Not read live:** the RSI modal (its trigger is a chart bar, not a labelled control): its six literal lines are mapped to the same tokens and verified as text only (rows W10-S2, W11-S1: line 229, a dot outline at alpha 0.3, was mapped to `--rb-quiet` as the nearest band).

## 3. What is still open

`RSIModal.tsx`'s chart chrome is verified as text only (its trigger is a chart bar the walker cannot press); the other three market modals are read or hold no literal white. The FWD-5 walk (288 faint
signal-colour elements on `/market` alone) waits on Andrew's YES to call `3c44`; FWD-4 waits on call `be0b`.
