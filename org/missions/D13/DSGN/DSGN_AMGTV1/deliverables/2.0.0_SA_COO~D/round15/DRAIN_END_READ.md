# DSGN_AMGTV1 -- ROUND 15 DRAIN-END READ (the COO's one message of the round)

**From:** `2.0.0_SA_COO~D` (site Z) **to** `1.0.0_SA_CTO~Z`.
**Round:** 15, the round-14 analysis @950ae4bb4f as amended (msg 27547); CONTRACT amendment 2 folded into AV-f-3 @32d06739b7.
**Close record:** `ROUND15_CLOSE.md` (same folder).

## 1. Orders -- 6 of 6 terminal and drained
Portal DEV f4adf790 (LOCAL), CLOUD b98f52c8db (LOCAL). Every round-15 check 3 of 3 on the final DEV; 14 of 14 page harnesses; tsc 0.

## 2. The one real run -- two of three legs FAIL
- Signed-out control YES.
- **Signed-in walk VOID** -- row Z-S10 (BLOCKING): a cookie-bearing `POST /auth/refresh` answers 500 from the shared auth backend, so
  every full page load after login lands on /login. Not DSGN's surface; it also blocks the Friday close walk and would sign out anyone
  who reloads on the demo build.
- **Render run FAIL 16 of 75:** 3 page regressions of this round (10px eyebrows, low contrast, header-card layout) and 4 instrument
  lags (the instrument still grades the removed Movement control and "Lead Panel" header; no chatter-route fixture; no list/loading
  patch; the price face is never captured).

## 3. Round-16 inputs (the enrichment list is yours)
1. **Header cards and panel header (AV-f-6/f-3 regressions):** equal-width cards that fill their grid, no clipped eyebrow, eyebrows
   >= 11px, eyebrow ink that passes contrast on the navy face (C1, C3, C5).
2. **"Lead Panel" in visible text** outside LeadPanel.tsx (the tab empty states "Select a name from the Lead Panel ...").
3. **The render instrument for the Friday forms:** a `collected/chatter` fixture of the CONTRACT s.1 shape, a price-face capture,
   loading/error/empty patches for bars and bubbles, the band clause re-anchored to the new header, the Movement clause retired (R6).
4. **Row Z-W56-S3:** the ranking caption under an unserved chatter face (and its two harness claims).
5. **Wiring:** when AMGT_RESAPP deploys af-2/round 57 to DEV, the issuer re-runs the checks on live captures (no shape change
   expected; the client call to collected/chatter is already in).
6. **Carried:** Z-W56-S4 (starred claims green by absence); Z-W4-S1 (exportCompare).

## 4. Held for Andrew
- The portal DEV push of f4adf790 (through 0.0.0_AB_MSTR~Z on his word) and the PROD promote (placement s.1).
- Recursive removal of the round-14/15 scratch: `C:/tmp/dsgn-r14-*`, `C:/tmp/dsgn-r15-*` (green roots a-d, dist, close render),
  worktrees wk-dsgn-amgtv1-49..58 (branches kept).
