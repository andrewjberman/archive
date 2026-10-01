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
