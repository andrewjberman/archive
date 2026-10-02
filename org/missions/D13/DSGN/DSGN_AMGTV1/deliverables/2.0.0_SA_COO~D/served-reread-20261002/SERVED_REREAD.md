# DSGN_AMGTV1 -- SERVED RE-READ, FWD-2 and FWD-24 (issuer `2.0.0_SA_COO~D`, 2026-10-02 18:42Z)

**Why now:** CTO msg 28577 ruled that the next DSGN act is the served re-read once a producer cell lands. AMGT_RESAPP r63
`AMGT-am-3` adds ticker / classification / places_moved to chatter rows. Its AMENDMENT 1 (drain 514cdf5366) adds places_moved
to the overlay's breakout_price row. Both are inside the code am-6 leg 1 deployed, 4197279e67; its NEVER-2 entry is closed
@6e67441488, and `git merge-base --is-ancestor 514cdf5366 4197279e67` holds.

**The page:** 5174 on site Z is another seat's dev server (PID 39760, started 17:14Z) on the live backend. Its five Security
Analysis sources (PriceBars, ChatterBubbles, SecurityOverlay, reasonWords, types) are byte-equal to portal PROD dcdc89b1
(portal-v2.1.195); I compared sourcemap `sourcesContent` with `git show dcdc89b1:<path>`.

**The instrument:** `servedread.mjs` (here) reuses the round-21 hover probe's walker harness: arm HOLDER, GET-only routes,
holder disarm in finally. It captures the served payloads, reads each mark's hover title or the header text, and compares field
by field. Final run: `read-20261002T184239Z/` (servedread.json + 5 screenshots), ARM 18:42:40Z, DISARMED 18:43:29Z.

## Result -- 9 of 9 marks clean

| read | marks | result |
|---|---|---|
| FWD-2 bubbles | AMD, ASML, BA (the first 3 drawn) | 3 of 3: name, collected count, ticker, asset class, sub-asset class, places moved as served (down 4 / up 15 / the served reason) |
| FWD-2 bars | AMD, SNPS, INTU (the 3 largest moves) | 3 of 3: name (ticker), asset class, sub-asset class, the 30-day figure, places moved as served (the served reason / no change) |
| FWD-24 header | BA, VLO, AMD | 3 of 3: "Breakout (price) #72, -4.71%, up 16 places"; "#7, +5.79%, up 13 places"; "#4, +12.88%, down 3 places" |

Served census at the read: collected-chatter rows carrying ticker 95 of 95, classification 93 of 95, a places_moved number 32 of 95.

## WHAT THIS READ DOES NOT GRADE -- the served values' correctness (added 19:0xZ)

This read grades PRESENTATION: each mark prints the value its served row carries. It does not test whether that value is right.
It is: CVO~Z's row `DSGN_AMGTV1-Z-C-S36` (ARMED) found the producer's places-moved join uses two key forms. On the base, 62 of 94
bars carry a false places_moved and 32 a correct one. So "up 16 places" and the like above are faithfully printed but not
established as true. The repair is RESAPP r63 am-3 AMENDMENT 2, cell R1 (@8ed109961e, CTO msg 28666). FWD-24's "places moved prints
wherever served" limb is met as presentation; its truth rides on R1.

## THE OPEN LIMB -- sector (already ruled: RESAPP am-3 AMENDMENT 2 cell R2, row Z-C-S37)

Every mark reads "sector not served". The producer serves no sector: measured with the route's own resolver
(`scoped_amgt.resolve_identity` + `_classification_for_ticker`), 0 of 95 covered names carry one. 85 have
`classification.sector` null and 10 have no classification row. The page says so in words, as designed. Ruled already: am-3 AMENDMENT 2 cell R2 serves an
equity's `classification.sector` = sub_asset_class when GICS-11 (with `sector_source`), else null with `sector_reason`. The page
prints a served sector as served and needs no change. Next: a served re-read after R1 and R2 deploy.

FWD-7 is not read here: its served write (RESAPP r63 am-7) is still pending.
