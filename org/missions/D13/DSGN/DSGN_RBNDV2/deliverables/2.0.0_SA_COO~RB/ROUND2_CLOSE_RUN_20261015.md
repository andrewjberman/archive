# DSGN_RBNDV2 -- round 2 close run and the L8 packet

**Author:** `2.0.0_SA_COO~RB`, 2026-10-15 ~10:5xZ. **Decomposition:** `DSGN_RBNDV2_DECOMP_v2.md` (@95d724679e), one issuance @8078760476 (`fanout: 2 of 2 chains, cap 8`).
**Branch:** `feature/dsgn-rbndv2-light` in the portal repo, LOCAL, no upstream, never pushed (C-BRANCH, FWD-6). Orders: seven complete (`RV-i-1`, `RV-m-1` to `RV-m-6`), every
proof-of-spec instance VALID when re-run by the COO from inside the worker worktree before the merge. The CTO's round-1 item 1 (the accent) is served by direct act
`RV-r-3`, proved by `ACCENT_COMPUTED_STYLE_PROOF_20261015.md` @9b53a758a8; item 4 (FWD-4, heat maps) is held for Andrew's design call.

## 1. The run

- Drain checks on the merged branch: `bun run typecheck` rc=0; 22 of 22 `dsgn-rbndv2` tests pass; eslint rc=0 on 66 changed files (only existing fast-refresh warnings).
- `bun run dev:live --port 5174` from the integration worktree against the real backend; `node .claude/skills/ui-walk/walk.mjs --route /market --press "Fear & Greed"` as the UI walker
  (armed, signed in, one page load, one press, disarmed; the post-disarm login was REFUSED). Walk folder `tmp/ui-walk/20261015T104206Z` (gitignored; it may carry client data; no screenshot
  is committed). A reader on this laptop opens
  `file:///C:/Users/AndrewBerman/Desktop/ajb_workspace/tmp/ui-walk/20261015T104206Z/shots/002--market-press-Fear-Greed.png` (the opened modal) and `.../001--market-load.png` (the page).

## 2. What the shots show (read by the COO, in words)

- **Hairline sections (`RB2I1-AC3`):** Trending Topics and Top / Bottom Performers render as plain sections inside the white panel: no bordered inset card, no coloured left bar; the
  Bullish/Bearish and Top/Bottom columns sit under their own small headings. The hairline divider between the two columns is a vertical rule at the `xl` breakpoint.
- **The modal frame (`RB2M1-AC2`, `RB2M4-AC3`):** pressing the Fear & Greed title opens the CNN Fear & Greed Index modal as a white surface with a thin silver edge, an eyebrow title with the violet underline,
  a square close control top right, a hairline under the header and above the footer, and a quiet footer line with a Close button; the sections inside (status, composite, 90-day trend, key insights, component
  indicators) are on white and legible, the trend chart keeps its own colours, and the old dark content ground is gone.
- **Not walked this run:** the RSI modal (its trigger is a chart bar, not a labelled control), the Market Regime modal, the account-menu popup (needs the user-menu press), `SessionTimeoutWarning` (a timed dialog),
  the autoFocus inputs of two PortfolioManagement modals, and every modal outside `/market`. Those are source-text and class-text verified only.
- Still open on the page (FWD-5, round 3): the walker counts 288 text elements under 3:1 before the press and 305 with the modal open; the samples are the signal green `rgb(25, 210, 154)` at 1.96:1 on white.
  Two headline labels truncate.

## 3. The L8 packet: what the CVO grades

JUDGMENT criteria (never self-graded; Andrew's eye is the final word, DEC-5): `RB2I1-AC3` (hairline sections), `RB2M1-AC2` (the frame reads as the A-light panel), `RB2M4-AC3` (a market modal reads as the A-light
panel, content legible). Artifact: section 2 and the screenshot paths in section 1.

ARMED rows and the COO's disposition request (the CVO owns the remediation rows; rows already graded by `ADJUDICATION_v1.md` C-S2 and C-S3 are not repeated):

| row | disposition requested |
|---|---|
| `DSGN_RBNDV2-W7-S1` | DISARMED: the named test file was authored by the worker at that path and passes |
| `DSGN_RBNDV2-W9-S1` | DISARMED: ruled; round-1 arm (f) rewritten to the section contract, `rb-1-p` and `rb-2-i1` both print their VERDICT |
| `DSGN_RBNDV2-W8-S9` | DISARMED for `FearGreedModal` (walked: content on white); CARRIED_BY the next walk for `RSIModal` (literal ground replaced, source-text verified only) |
| `DSGN_RBNDV2-W8-S6` | CARRIED_BY the next walk: the focus guard landed and has a source-text arm; whether an autoFocus input keeps focus on open is not exercised |
| `DSGN_RBNDV2-W8-S11` | CARRIED_BY the next walk: `SessionTimeoutWarning`'s hidden Close is class text only |
| `DSGN_RBNDV2-W8-S1` | CARRIED_BY the CTO: the commit-gate and risk-reflex checked 0 of 3 `.tsx` files (an instrument blind spot, not a defect of the cells) |
| `DSGN_RBNDV2-W2-S3` | the account-menu popup took the A-light surface in `RV-m-6` (class text only); CARRIED_BY the next walk to confirm |

INERT observations for the record (not armed): `W8-S8` (`ExecutiveSummary`'s `DrilldownModal` keeps its own overlay and is on no list: a wall; carried to the CTO), `W8-S10`, `W8-S12`, `W8-S14`, `W8-S15`.

## 4. For round 3 and the CTO

The FWD-5 walk (every nav page and every opened modal, signal colours darkened at the token); the `DrilldownModal` in `ExecutiveSummary.tsx`; whether the modals' `autoFocus` and close behaviour hold in a browser; Andrew's design call for FWD-4 (queued on the box list) and the PRD addendum it triggers;
the `index.css` comments that still name `#F4F6FA` (W1-S3); the theme generator reconciliation (W1-S1).
