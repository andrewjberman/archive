# AMGT_CORPUS round 34, CRPS-aj-2 leg v.4 -- BA's Model tab after the on-demand fire

- **Instrument:** `/ui-walk` (`node .claude/skills/ui-walk/walk.mjs --route /security-analysis --security BA_US_Equity`). It signed
  in as the walker on the local `dev:live` build (port 5174), reading live data through CloudFront.
- **Walk:** `tmp/ui-walk/20261003T235538Z`, 23:55-23:59Z. The account disarmed and a re-login was refused (401). Screenshots are
  kept local under the ui-walk law, and this file transcribes them.
- **Requests:** every `/api/scoped/amgt/security/BA_US_Equity/*` request returned 200. That is thesis 1, versions 1, compare 16,
  ledger 1, overlay 1, peers 1, timeline 1 and timeline/day 2.

## What the Model tab shows (shot `031-BA-US-Equity-Model.png`)

- **The sheet** renders its 17 rows over 2016-2025, plus "CONSENSUS (BLOOMBERG)" for 2026E-2028E (EPS -0.83 / 3.85 / 8.00).
  The footer reads "Showing 147 fiscal figures from the model block".
- **Versions:** "20 versions have landed". The newest is "The version of October 3rd, 2026, 23:27 UTC", which is this fire's
  block.
- **What moved, September 10th 22:44 UTC to October 3rd 23:27 UTC:** "566 figures added, 0 removed, 7 changed, 172 unchanged".
  The seven are all base header figures, in words:
  - Enterprise value USD 194B to USD 185B
  - Market cap USD 162B to USD 153B
  - Beta 1.35 to 1.36
  - Share price (last close) USD 204.80 to USD 193.56
  - Short interest ratio 2.9039 to 3.036
  - Short interest 2.0% to 1.8%
  - Average volume 5.52M to 7.46M
- **Where each input came from:** "Market data: Bloomberg; last ran October 3rd, 2026 and worked".

## The CTO half's added condition (msg 29061)

"On BA's Model tab, the 52 new mnemonics must not show their pointer unit or a raw list value. That count must read 0."

- **Measured: 0.** None of the 52 is itemised anywhere on the tab. The sheet rows and header cards are fixed lists that name
  none of them; 0 of 40 SecurityAnalysis files name any. The version compare lists only CHANGED figures, and the 566 added
  ones are counted, not listed.
- The walk's findings carry 0 hits for `field_map`, `not yet built`, `announcement_date` or `object Object`.
- **Not in this act's radius:** the walk's netlog holds 8 non-200 requests (its summary reports 6 "API issues"). Two are
  `/auth/refresh` 401s. The other six are `DE_US_Equity` thesis and peers 404s, 3 each: Deere has 0 model_block objects ever
  and is not among the 96 registered names (row `AMGT_CORPUS-Z-S86`).
