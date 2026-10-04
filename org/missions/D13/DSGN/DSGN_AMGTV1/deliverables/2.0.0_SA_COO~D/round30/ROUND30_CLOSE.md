# DSGN_AMGTV1 -- ROUND 30 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-03 ~01:4xZ) -- ONE UNIVERSE PER FACE + REPAIRS

**Input:** decomposition v30 and the issuance are @a427b2ef70, over PRD v0.13 @e398ee2294 (ADMITTED). The base is portal e370eb7c, the
CTO-approved round-29 candidate.

## 1. ORDERS (2 of 2 terminal, drained)

| order | cell | worker | portal | AC1 / AC2 / AC3 | outer drain |
|---|---|---|---|---|---|
| `AV-zh-1` | each Lead Panel face reads one served universe; no movement-basis words | ~86 | df863c97d4 | 4/4, 3/3, battery 0 skipped | 4aed6b5ae8 |
| `AV-zh-2` | repairs: no-tone token, canonical Refresh, render-check back hook, links only where served, What-changed at display precision, height off the stack | ~87 | 621f553e | 4/4, 3/3, battery 0 skipped | 8b73dd0f5b |

Both instances are VALID and every blob is LF with no 0x08. `chartColors.ts`'s 63 non-ASCII characters were there at base; this round
added two ASCII lines. Row `Z-W87-S1` is admitted: `CoverageItem.url` typed `string` and `HEADER_FEED_VISIBLE_COUNT = 3` sit outside the
cell, so the cell guarded both locally.

## 2. THE CANDIDATE -- portal `2defab11` (worktree 82, branch `dsgn-r30-onto-dev`, LOCAL)

It is e370eb7c plus ~86 and ~87, merged onto remote DEV c9d303db, a fast-forward over c9d303db. It carries round 29 too, whose own DEV push
still waits on Andrew's word at MSTR~Z.
**Issuer run on 2defab11:**
- `battery29.sh` with NO skip: ALL PASS (14 of 14 harnesses, tsc 0).
- round 30: universe 4/4, resolutionwords 3/3, chrome 4/4, served 3/3.
- every round-29 check at full marks: timeline 4/4 + 4/4, header 4/4 + 4/4, leadprice 4/4 + 3/3, collage 4/4 + 4/4, model 4/4 + 4/4, tabs
  4/4 + 4/4.
- round 27 identity 3/3; round 28 fixture 3/3.

## 3. THE REAL RUN -- walk `tmp/ui-walk/20261003T012558Z` (5174 = 2defab11; ARM 01:25:59Z / DISARMED 01:32:29Z; login after: REFUSED)

81 shots, walk void no, every tab walked on BA, VLO and AMD. The findings match round 29's in class:
- tab-not-found and no-event-element are the walker's stale navigation and selectors;
- the API issues are the pre-existing Posture comparable 404s;
- the `$` is served prose (ruled (b), CTO msg 28836).

**SAUX-15 first viewport, measured** (pixel scan of shot 005 for the active tab's purple underline):

| walk | underline y |
|---|---|
| round 29 (20261002T233653Z) | 963 |
| round 30 (this walk) | 917 |

The underline rose 46 px; the cell's own arithmetic was about 116 px. **NOT YET MET:** the first panel starts at about y 943, against the
900 target. The gap is served growth: RESAPP's an-7 redeploy now serves BA 69 feed items (it was 1). The news card therefore draws 2 open
items plus "Expand (67 more)", about 66 px more than the 1-item card the cell's arithmetic assumed. Showing 1 item at rest recovers about
49 px, which brings the panel to about 894. That is a round-31 item (`HeaderBrief.tsx` + `constants.ts` `HEADER_FEED_VISIBLE_COUNT`).

## 4. OPEN -> ROUND 31

- **FWD-26 presets** (LeadPanel / PriceBars / ChatterBubbles / useLeadPanelApi; PRD v0.11+):
  - Chatter reads the served `?days=` windows (c9 YES on deployed kSeyeO0v; window_start/window_end, window_note on 365).
  - Price trending `?days` is a RESAPP gap. It is fixed on CLOUD and serves at an-7 leg 2 (COO~Z msg 28860). Until then the face reads
    the served window fields and says plainly when a window is not served.
- **First viewport:** the news card shows 1 item at rest (see section 3).
- **The CTO's product-file review of 2defab11.**
- **DEV pushes on Andrew's word:** round 29 (e370eb7c) is carded at MSTR~Z, and 2defab11 supersedes it if he prefers one push.
