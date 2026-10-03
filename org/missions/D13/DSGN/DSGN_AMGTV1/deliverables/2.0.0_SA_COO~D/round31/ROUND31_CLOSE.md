# DSGN_AMGTV1 -- ROUND 31 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-03 ~17:3xZ) -- ROLLING WINDOWS + ONE NEWS ITEM AT REST

**Input:** decomposition v31 and the issuance are @812179b412, with a stamp correction @f1d0ca880e, over PRD v0.13 @e398ee2294
(ADMITTED). The base is portal 2defab11, the round-30 candidate. The session made no call from ~01:57Z to ~16:2xZ (the account's
weekly model limit), and the workers ran on the Sonnet override.

## 1. ORDERS (2 of 2 terminal, drained)

| order | cell | worker | portal | AC1 / AC2 / AC3 | outer drain |
|---|---|---|---|---|---|
| `AV-zi-1` | rolling windows: 30D / 90D / 365D presets on Chatter and Price (FWD-26) | ~88 | 28a1a16c | presets 4/4, windowread 4/4 (KEEP 7/7), battery 0 skipped | 9969dcfe49 |
| `AV-zi-2` | one news item at rest (SAUX-15) | ~89 | d32aa7ca | feedrest 4/4, battery 0 skipped | fd0f97c885 |

Both proof instances are VALID, run from each worktree's own checker. Every committed blob is LF with no 0x08 and no non-ASCII; the
checkouts use autocrlf, so the working-tree CRs are not in the blobs.

Row `Z-W88-S1` (INERT) is ruled the worker's way. The order asked for `ground="band"` on the preset control, but the Subject and
Starred controls beside it pass no ground. The order's clause came from LeadPanel.tsx's stale header comment (AMGT-rl-8), so the
default ground is right.

**Issuer amendments landed this round:**
- round29 `leadprice/leadface.cjs` AMENDMENT 1 (@812179b412): no month cursor; the face reads the served 30-day window.
- round30 `repairs/chrome.cjs` AMENDMENT 1 (@ef23a6706b): the chartColors census grades the round-30 token, not other projects'
  landed edits. Remote DEV's DSGN_REBRND commits add PALETTE.pink400 and getAssetClassInkOnDark. Against the round-30 base sources
  the arm still FAILS.

## 2. THE CANDIDATE -- portal `76a15c1b` (worktree 82, branch `dsgn-r31-onto-dev`, LOCAL)

The candidate is 2defab11 plus ~89 and ~88, merged with remote DEV 525c9404. It fast-forwards DEV 525c9404, which it contains, and it
carries rounds 29 and 30. The DEV merge touched two Security Analysis files: chartColors.ts (+18 lines, DSGN_REBRND) and the
comments in renderCheck.tsx.

**Issuer run on 76a15c1b:**
- `battery29.sh` with NO skip: ALL PASS (14 of 14 harnesses, tsc 0).
- round 31: presets 4/4, windowread 4/4, feedrest 4/4.
- round 30: universe 4/4, resolutionwords 3/3, chrome 4/4 (as amended), served 3/3.
- round 29, every check at full marks: chart, dayopen, face, figures, pricemovers, leadface (as amended), collage, tone,
  whatchanged, etwords, tabwords, peersmenu.
- round 27 identity 3/3; round 28 fixture 3/3 and render 3/3.

## 3. THE REAL RUN -- three walks on 5174 (= 76a15c1b; ARM 17:08Z, DISARMED 17:21:39Z; login after each disarm: REFUSED)

**Walk `tmp/ui-walk/20261003T170837Z`** (BA, VLO, AMD; 80 shots; walk void no).

**SAUX-15 first viewport: MET.** Pixel scan of shot 004 (BA, 1440 wide):

| walk | tab underline y | first panel top |
|---|---|---|
| round 29 (20261002T233653Z) | 963 | ~989 |
| round 30 (20261003T012558Z) | 917 | ~943 |
| round 31 (this walk) | **868** | **894** (border row measured) |

The news card shows one item plus "Expand (68 more)". The first tab panel starts 6 px inside the 900 target. The margin is thin: one
more line above the tabs would cross it.

**Walks `20261003T171510Z` and `20261003T171945Z`.** The walker's `/security-analysis` branch does not run `--press`, so walk 3
reached the same page as `/%73ecurity-analysis` (the plain-route branch) and pressed the presets in a real browser.
- **FWD-26 / FWD-21 Chatter.** 30D reads "Articles collected over the last 30 days to October 2nd, 2026", with 55 of 95 names. 90D
  reads "... 90 days ...", with 64 of 95, and the bubble sizes change. 365D reads "... 365 days to October 2nd, 2026, since January
  1st, 2026", with 70 of 95. Each count matches the served window. No "Earlier month" or "Later month" is drawn.
- **FWD-26 / FWD-22 Price.** 30D draws 20 bars at rest under "Change over the last 30 days to October 2nd, 2026" (a newer served
  generation than the fixture). 365D prints the served reason, "the 90- and 365-day price windows are not produced yet: ...", with
  0 bars and no 30-day words. Pressing back to 30D brings the bars back.

**Findings, by class:**
- **Walker stale selectors** (`walker:control-missing`: "Earlier month", which FWD-26 retired, and the tab names) and
  `timeline:no-event-element`: as in rounds 29 and 30.
- **`design:contrast`** in the day dialog is an instrument false positive. The text is white on the dialog's navy hero gradient,
  which the contrast reader takes as white (shot 005).
- **`format:money`** is served prose ("$2.9 billion" beside "USD"), ruled (b) by CTO msg 28836.
- **`layout:truncated`** marks long names on the Price bars ("Advanced Micro Devices ..."). These existed before this round; each
  bar row carries its hover.
- **`format:dates`** is REAL. The Chatter footer prints the served `as_of` raw ("As of 2026-10-02", LeadPanel.tsx:546), beside
  long dates in the caption. FWD-27 wants one date format. This goes to round 32.

## 4. OPEN -> ROUND 32 (enrichment list)

- **Repairs (one batched cell):**
  - the Chatter footer prints `as_of` in words (FWD-27);
  - the Price face at 90D/365D drops the "Source: ranking details are not carried on this payload" line (system wording, FWD-27);
  - "this period" reads "in this window";
  - LeadPanel.tsx's header comment stops saying `ground="band"`.
- **Not cut:** retiring ChatterBubbles' month mode, together with the round-15/29/30 checks that render it.
- **The CTO's product-file review of 76a15c1b.** It supersedes 2defab11.
- **DEV push on Andrew's word:** 76a15c1b, which carries rounds 29, 30 and 31, is carded at MSTR~Z.
