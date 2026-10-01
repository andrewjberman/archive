# DSGN_AMGTV1 -- ROUND 15 CLOSE RECORD (the Friday round) -- `2.0.0_SA_COO~D`, 2026-10-01 ~07:1xZ

**Issuance:** @010f7e4315, decomposition v15, 6 orders in 3 chains (cap 3); amendment to AV-f-3 @32d06739b7.
**Portal:** site-Z DEV a41cf763 (issuer types) -> f6fd9358 (~57) -> 78cf9877 (~58) -> **f4adf790** (~56). LOCAL (origin/DEV b336b141).
**CLOUD:** 3e10eb343c (~57), 31465758ae (~58), **b98f52c8db** (~56). Every merge read dropped 0, foreign 0. LOCAL.

## 1. Orders -- 6 of 6 terminal, every proof instance VALID

| order | slot | portal commit | DEV after the chain | CLOUD merge | check (worker, then issuer re-run with exit code) |
|---|---|---|---|---|---|
| AV-f-6 card face + header cards | ~57 | d3513968 | f6fd9358 | 3e10eb343c | cardface 3/3 |
| AV-f-4 served-day header + Z-S9 | ~58 | be83ec4c | (chain) | (chain) | headerread 3/3 exit 0 |
| AV-f-5 pack sentences | ~58 | cf5dd466 | 78cf9877 | 31465758ae | packwords 3/3 exit 0 |
| AV-f-1 price bars | ~56 | 1cc46e25 | (chain) | (chain) | pricebars 3/3 exit 0 |
| AV-f-2 chatter bubbles | ~56 | 5cbbdfcd | (chain) | (chain) | bubbles 3/3 |
| AV-f-3 panel header (amended) | ~56 | 424dbd27 | f4adf790 | b98f52c8db | panelhead 3/3 exit 0 |

On the final DEV f4adf790: all six round-15 checks 3 of 3; round-14 reasonwords, execfooter, bytes, modelhistory 3 of 3; 14 of 14
page harnesses; `tsc -b` rc=0.

## 2. The one real run

- **Signed-out control** (`round14/checks/walkvoid.sh` on 5174 = f4adf790 via CTO~Z's 93134bae): walker rc=3, WALK VOID 1, account
  lines 0 -- **YES**.
- **Signed-in walk** `tmp/ui-walk/20261001T070037Z` (BA, VLO, 6501): **VOID.** Login 200 at /market; the full load of
  /security-analysis calls `POST /auth/refresh` with the session cookie and the shared auth backend answers **500** twice
  (netlog lines 259, 263) -> /login. A cookie-less refresh answers 401 "No refresh token". Walk N on 2026-09-30 23:53Z navigated the
  same routes signed in. Account disarmed (status=disabled, SSM ABSENT). **Row Z-S10 BLOCKING/ARMED** @9fd3584fb1, routed to
  1.0.0_SA_CTO~Z for placement with the auth writer. No signed-in walk of the round-15 faces exists.
- **The render run** (`node scripts/ui-contract-check.mjs --dist C:/tmp/dsgn-r15-dist/final --out C:/tmp/dsgn-r15-close-render
  --states-sweep`, a vite build of f4adf790): **PASS 58, FAIL 16, NOT_EXERCISED 0, N/A 1 -- RESULT FAIL.**
  - **Page regressions this round introduced (the static checks could not see them):**
    - `sizes` FAIL in all six states: smallest 10px (C1 floor 11). The `GraphicCard` eyebrow (PanelEyebrow) on the four header cards
      and the panel header.
    - `lowContrastChars` FAIL: 31 (list), 48 (every tab state). Read on `thesis.png`: the header cards' eyebrow ink on the navy face.
    - **Header card layout** (read on `thesis.png`): the four cards render at uneven widths in a wide grid; "MARKET FEATURES" overlaps
      its icon; cards do not fill their columns.
  - **Instrument lag (the instrument grades forms ruling R5/R6 removed):** `list.bandIsIdentityHeader` (the panel header is no longer
    titled "Lead Panel"), `list.fwd18_controls` ("Movement is not a segmented control" -- Movement removed by R6),
    `fwd19_designedStates` missing `list/loading` (the sweep has no loading patch for the bars/bubbles face). The render fixtures have no
    `collected/chatter` capture, so the chatter face renders "Read failure" (`list.png`); the sweep never captures the price face.
  - **Harness:** `posture` rc=1 (reads S3 live; unstable, excluded from every bound this round).
- **PNGs read:** `list.png` (the panel header in the card face: eyebrow "SECURITY ANALYSIS", "What is moving", Chatter/Price and All
  names/Starred only Segmented, search; the chatter face's read failure for want of a fixture; the ranking footer under it) and
  `thesis.png` (above). The thesis empty state reads "Select a name from the **Lead Panel** to open its Thesis." -- the internal name on
  a face outside LeadPanel.tsx (panelhead.cjs grades LeadPanel's text only).

## 3. Rows this round
- Z-W56-S1..S4: OBSERVATION, INERT (S2 folded into AV-f-3; S3 the ranking caption still shows while the chatter payload is unserved;
  S4 errorEmpty's starred claims green by absence).
- Z-S10: BLOCKING, ARMED (auth refresh 500), disarm owner 1.0.0_SA_CTO~Z.

## 4. ADDENDUM 07:3xZ -- the signed-in walk, after the walker account was freed (CTO 27608, MSTR~Z serialisation)

- Arm and disarm posted to 0.0.0_AB_MSTR~Z (laptop held). Walk `tmp/ui-walk/20261001T073050Z` (5174 = DEV f4adf790; BA, VLO, 6501):
  armed 07:30:53Z, logged in 07:31:13Z, **walk void: no**, 143 shots, 5.8 min, disarm 07:36:40Z proven (a login with the walk
  password after the disarm is REFUSED, HTTP 401).
- **Read on the shots:**
  - `004-lead-Trending-Price-List.png`: the price face sits in its loading skeleton with "Source: no ranking has been read"; the
    selected-name header reads "no ranking has been published for this date yet" -- the live ranking read has no row for today until
    AMGT_RESAPP's server-side T-1 fallback (af-2) deploys. Server-side, not DSGN.
  - The chatter face: `GET /api/scoped/amgt/lead-panel/timeseries/collected/chatter` answers **400** (15 calls) -- the route is not
    deployed yet (RESAPP round 57); the face prints "Read failure" (round-16 cell 4 replaces it with a designed sentence).
  - `010-BA-US-overlay.png`: the four header cards at uneven widths, "MARKET FEATURES" over its icon (round-16 cell 2); the Thesis
    pillars "no research pack for this security" (page text from reasonWords.ts:33, AMGT_RESAPP row Z-W200-S1 -> round-16 cell 5).
  - Every tab with no name selected: "Select a name from the Lead Panel ..." (round-16 cell 5).
- **Findings:** 21 unique; `walker:control-missing` x4 (the walker still walks Trending/Breakout x List/Chart -- removed by R5/R6;
  round-16 cell 1 item 2); `design:contrast` x9 (the header eyebrows and the band's secondary ink; cell 2); `design:tinted-status`
  x3; `format:money` x1 ("USD 1,234" beside "$1,234"); `timeline:no-event-element` x2 (VLO, 6501: no event served); `occluded-popover`
  x1 (the Price tile's tooltip covers the description).
- **Round-14 render checks re-run on DEV f4adf790** (`/c/tmp/cood-r15-close.log`): foldopen 3/3; peersempty 2/3 (arm 1 needs a full
  fwd19 PASS -- fails on `list/loading` missing, round-16 cell 3); styles 2/3 (sizes FAIL 10px in six states, round-16 cell 2);
  rendercontrol 2/3 (arm 3: the posture harness rc=1 -- it reads S3 live, unstable, excluded from every bound). No new cause.
