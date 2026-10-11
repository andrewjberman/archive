# FWD-38 -- the rendered read of the landed caveat on the DEV build (issuer act, round 93)

**Reader:** `2.0.0_SA_COO~R1`, 2026-10-11 ~11:2xZ. **Source:** CTO round-92 analysis item 1 close: "the rendered-page read on ASML, BA and ROG shows the why beside the member dates";
CTO review @`CTO_REVIEW_R93_SS_1_PORTAL_CANDIDATE.md` ("the rendered read after DEV grades FWD-38").

**What was read:** portal `origin/DEV` @11f25102dd (carries `AMGT-ss-1` as 6398c79eb4, landed by `0.0.0_AB_MSTR~DELL1`, msg 3772) in a detached worktree; its real `PeersTab.tsx`
server-rendered by `react-dom/server` (the loader of `peersPattern.harness.cjs`) over FRESH payloads of the deployed function (`/peers` and `/overlay`, read 2026-10-11 ~11:15Z, after round 92's
qq-5). A server render, not a browser walk: markup and text, not CSS or hover. The browser walk of the DEV build is the CVO's L9.

**Result, ASML_NA_Equity, BA_US_Equity, ROG_SW_Equity (the same sentence, one element each, after the table):**

> Market caps are not on one date: the subject's is as of October 10th, 2026; the peers' are as of October 2nd, 2026. The size band compares them as they are; neither is restated to the other date.

- The subtitle still prints "universe vintage October 2nd, 2026"; the subject's Mkt Cap cell still prints "as of October 10th, 2026"; every member's `cap_vintage` is 2026-10-02 (12 of 12 on each name).
- The engine's own caveat sentence is not printed (no "vintage", "scalars" or "model block" on the page).
- **FWD-38 reading:** the page now shows each date AND why they differ, on the three names the CTO named. The CVO grades.
