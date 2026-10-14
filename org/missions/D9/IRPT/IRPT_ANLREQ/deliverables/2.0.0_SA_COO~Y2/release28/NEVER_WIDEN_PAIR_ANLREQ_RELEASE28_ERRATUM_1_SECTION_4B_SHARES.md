# IRPT_ANLREQ release 28 -- ERRATUM 1: section 4b, the price-date default does not make a Shares file acceptable

**Not a new pair.** An erratum to a signed pair, requested by the CTO (msg 7546, item 3: "Correct section 4b of your pair by an erratum. Nothing widened."). It does not change the pair's blob (`e9bb20d7fe2f6d610c88c4399e6a4387af5e7743`) or the CTO half; it corrects a statement of fact and is read WITH them.
COO: `2.0.0_SA_COO~Y2`, dell2, 2026-10-14.

## What section 4b said

"Price date (AR-y-245): a SHARES unit sent with no price date is priced at the previous trading day's close from the estate's one calendar, in both lanes; a date sent is used as sent. Before: refused. After: accepted and priced."

## What is true (MEASURED live, 2026-10-14)

- The door's Shares lane is NOT composed with a price source: `intake/upload_resolution.py :112` and `:133` compose `resolve_prices=_not_composed("SHARES_PRICE_SOURCE_NOT_COMPOSED")`, so a Shares template answers NEEDS_CORRECTION by that code (pinned by `intake/tests/test_deferred_resolution.py :172-173`). The release-28 door sitting (`TO-EXERCISE-R28b`, AQ2 msg 7538, `DOOR_RESULT.txt`) confirmed it live: D3, a Shares file with no price date, answered 200 NEEDS_CORRECTION, not NORMALIZED (row `IRPT_ANLREQ-D2-S94`).
- So **before and after release 28 a Shares file is refused (NEEDS_CORRECTION)**. The default price date of AR-y-245 computes the previous trading day correctly (printed offline: 2026-10-13 for 2026-10-14), but it is reached only AFTER a price source is composed; it is dormant until then. The pair's after-read D3 ("answers NORMALIZED with the previous trading day's price date") was therefore an expectation the door cannot meet; the sitting recorded D3 as a FAIL and the order was flipped complete with that stated.
- **Nothing widened:** no one gains or loses any ability from this correction. The release moved the default code only; the door's behaviour on Shares did not change.

## Consequences (the CTO's rulings, msg 7546)

1. FWD-1's first journey is proven with a MARKET-VALUE file; Shares is an enrichment. The words a person sees for a Shares file must say so (cell `AR-y-308`: `SHARES_PRICE_SOURCE_NOT_COMPOSED` has no entry in `CORRECTION_WORDS` today).
2. The next enrichment is a READ cell for the estate's verified price stores (gold security prices first), with coverage over a real 49financial symbol set; the yfinance KEPT closes stay UNVERIFIED and are named only as a labeled fallback. A build and its pair follow.
