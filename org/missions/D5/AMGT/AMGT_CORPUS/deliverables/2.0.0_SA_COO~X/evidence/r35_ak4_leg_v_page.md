# AMGT_CORPUS round 35, CRPS-ak-4 leg v.4 -- BA's Model tab after the re-derive

- **Instrument:** `/ui-walk` (`node .claude/skills/ui-walk/walk.mjs --route /security-analysis --security BA_US_Equity`), local
  `dev:live` build on port 5174. Walk `tmp/ui-walk/20261004T200520Z`, 20:05-20:09Z. Disarm printed `REFUSED` (HTTP 401).
- **Requests:** 24 `BA_US_Equity` requests, 0 non-200. The walk's 7 API issues are outside this act: one
  `market-overview/rsi-details-commodities.json` 500 and six `DE_US_Equity` thesis/peers 404s (Deere is not registered, row
  `AMGT_CORPUS-Z-S86`).

## What the Model tab shows (shot `031-BA-US-Equity-Model.png`)

- **Versions:** "22 versions have landed". The newest is "The version of October 4th, 2026, 19:56 UTC", which is this act's
  re-derive (leg d stamp `20261004T1956xxZ`). Next is 13:02 UTC, the scheduled fire's block.
- **What moved, September 10th 22:44 UTC to October 4th 19:56 UTC:** "566 figures added, 0 removed, 7 changed, 172 unchanged".
  The same seven base header figures and the same counts as round 34's read of the 10-03 block. That agrees with v2 (0 base
  values moved; weekend raw carries Friday's close).
- **Where each input came from:** "Market data: Bloomberg; last ran October 4th, 2026 and worked".

## The pointer-unit / raw-list count (CTO condition)

- **Measured: 0.** The walk's findings and summary carry 0 hits for `field_map`, `SEE field_map`, `object Object` or
  `not yet built`. The sheet and header cards are fixed lists that name none of the 52; the compare counts added figures and
  never itemises them. Served-side, v3 reads 0 pointer-unit figures over the 52's 32,826 figures in the 96 newest blocks.
- The walk's 8 findings (1 clipped, 1 raw-code generation string, 10 truncated labels, 1 money format, 4 contrast) are page
  design findings outside this act's radius.
