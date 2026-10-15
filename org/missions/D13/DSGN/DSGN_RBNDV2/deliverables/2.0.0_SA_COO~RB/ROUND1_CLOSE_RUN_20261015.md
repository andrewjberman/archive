# DSGN_RBNDV2 -- round 1 close run (the ONE real run of FWD-1's thread) and the L8 packet

**Author:** `2.0.0_SA_COO~RB`, 2026-10-15 ~07:2xZ. **Decomposition:** `DSGN_RBNDV2_DECOMP.md` v1 (@b475e9badc) with addenda 1 and 2.
**Branch:** `feature/dsgn-rbndv2-light` in the portal repo, LOCAL, no upstream, never pushed (C-BRANCH, FWD-6). Orders: six complete
(`RV-t-1`, `RV-s-1`, `RV-p-1`, `RV-h-1`, `RV-r-1`, `RV-r-2`), every proof-of-spec instance VALID when run from inside its worker worktree.

## 1. The run

- `bun run dev:live --port 5174` from the feature-branch worktree: the local build against the real backend (the CloudFront front door).
- `node .claude/skills/ui-walk/walk.mjs --route /market` as the UI walker: armed, signed in, one page load, disarmed; the post-disarm
  login was REFUSED both times. Walks: `tmp/ui-walk/20261015T063315Z` (before the repairs) and `tmp/ui-walk/20261015T071654Z` (the final
  branch). Both folders are gitignored (the walker marks them as possibly carrying client data) and the screenshots are NOT committed.
  A reader on this laptop opens `file:///C:/Users/AndrewBerman/Desktop/ajb_workspace/tmp/ui-walk/20261015T071654Z/shots/001--market-load.png`.
- Drain checks on the merged branch: `bun run typecheck` rc=0; 9 of 9 `dsgn-rbndv2` tests pass; eslint rc=0 on the 21 files changed up to the
  repairs.

## 2. What the final screenshot shows (read by the COO, in words)

- The page ground is `rgb(234, 234, 247)` (`#EAEAF7`). The sidebar rail is the same lavender, text-led, with a square initial at the foot
  (collapsed 48px rail; the expanded sidebar is covered by its own test).
- Every panel is white with a thin silver edge, an eyebrow title with the violet underline, a hairline under the header and a quiet source
  caption; no navy strips and no box inside a box.
- Before the repairs (first walk) the Equity, Fixed Income and Commodities heat tables and the Trending and Top/Bottom tiles kept their navy
  grounds and their text read navy on navy (141 text elements under 3:1). After the repairs those tables and tiles read white and silver, the
  instrument names are navy and legible, and the period chips (WTD, 90D) read as navy ink.
- Still open on this page: the walker counts 288 text elements under 3:1. The samples are the signal green `rgb(25, 210, 154)` at 1.96:1 on
  white (the delta and arrow glyphs) and the reds beside them. That is the FWD-5 population (round 3). Two headline labels truncate
  ("Trump Announces $80B Taiwan LNG Deal", "Netflix Cuts 1,000 Jobs as Growth Worries Mount"). The red/green delta figures keep their colour
  by design (Andrew: reds and greens are looked at after step 3).

## 3. FWD state after this round (what is measured, what is Andrew's)

| FWD | state | evidence |
|---|---|---|
| FWD-2 sidebar and ground `#EAEAF7` | APPLIED on the page walked | canvas read `rgb(234, 234, 247)`; sidebar test `SIDEBAR-OK`; the nav pages other than `/market` are not walked |
| FWD-3 panels and modals | panels APPLIED; modals NOT STARTED | panel test `PANEL-LIGHT-OK`; modals are round 2 (C-MODAL) |
| FWD-4 heat | the scale is DEFINED; the heat tables read white and silver on `/market` through the inner-surface tokens; the eight F10 files are NOT repointed | `HEAT-SCALE-OK`, `INNER-SURFACES-OK`; premise finding below |
| FWD-5 walk | NOT STARTED (round 3) | 288 under-3:1 elements on `/market` alone |
| FWD-6 nothing leaves the laptop | APPLIED | the branch has no upstream; `git -C portal ls-remote` of it is not run (it is not on origin); no push |
| FWD-1 Andrew opens `/market` and says yes or no | OPEN: Andrew's | the dev build serves the feature branch on `http://localhost:5174/market` now (real login with MFA) |

**Premise finding for the CTO (rows `DSGN_RBNDV2-W4-S1` to `S5`, `DSGN_RBNDV2-S3`):** brief F10's "blue scale" is not a hue in the eight listed
files. They shade with semantic red/green overlays. The navy that FWD-4 means is the ground of the heat tables and tiles
(`--semantic-background-contentPanel`, `--bg-header`, `--bg-medium`), which `RV-r-2` flips to white and silver inside a light panel. Whether the
eight files should additionally take the one `heatColor` scale for their cell shading (a sign-less magnitude scale cannot carry red/green sign)
is a design call for Andrew's read of the live page.

## 4. The L8 packet: what the CVO grades

JUDGMENT criteria (never self-graded; the COO's reading above is the instrument, Andrew's eye is the final word per DEC-5):
`RB1S-AC3` (sidebar reads as the A-light board), `RB1P-AC3` (panels read as the A-light board), `RB1H-AC3` (tell high from low at a glance; no heat
map left in the blue), `RB1R-AC2` (chips and panel-header buttons read navy), `RB1R2-AC2` (heat tables and tiles read white and silver).
Artifact: section 2 above and the screenshot path in section 1.

ARMED rows and the COO's disposition request (the CVO owns the remediation rows):

| row | disposition requested |
|---|---|
| `DSGN_RBNDV2-S1` | DISARMED: the scoped rule landed and `/market` bodies read |
| `DSGN_RBNDV2-S2` | DISARMED: the period chips read navy in the final walk |
| `DSGN_RBNDV2-S3` | DISARMED: the heat tables and tiles read white and silver |
| `DSGN_RBNDV2-W1-S2` | CARRIED_BY the round-3 walk (a `text-white` on a solid fill inside a light panel) |
| `DSGN_RBNDV2-W5-S2` | CARRIED_BY the round-3 walk (idle grey status dots turned navy by the palette remap) |
| `DSGN_RBNDV2-W2-S3` | CARRIED_BY round 2 (the account-menu popup stays dark; it is a pop-up, C-MODAL's population) |
| `DSGN_RBNDV2-W1-S1` | CARRIED_BY a theme-owner act: the theme header's generator does not reproduce the committed theme file; the four canvas lines were set by hand to the generator's value |
| `DSGN_RBNDV2-W6-S2` | NOT_A_DEFECT: the order file carries its record face below the worker face by the template; the worker took no action from it |

## 5. For the round-2 enrichment list (to the CTO)

C-MODAL (one frame, every modal; includes the account-menu popup); the panel number prop and page numbering (from W3-S1); heat cell shading for the
eight F10 files on Andrew's pointer; the two truncated headline labels; the `index.css` comments and contrast figures still naming `#F4F6FA`
(W1-S3); `PanelFooter`'s stale `ground='band'` name and `PanelExamples`/README (W3-S2); the theme generator reconciliation (W1-S1).
