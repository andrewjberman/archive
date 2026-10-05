# AMGT_CORPUS round 37 -- the real run of am-3 on portal DEV `2e7c5cdb` (gap reasons), before am-2

- **Instrument:** `/ui-walk` on `bun run dev:live --port 5174`, served from `C:/tmp/wk-crps-r37-2/portal` @`2e7c5cdb`. That is portal
  DEV, pushed by MSTR~Z on Andrew's "approved" (@b6361adaa5); CI run 37248822834 success. The API is the deployed
  `opal-amgt-scoped-api` (`2rFeF57l`, round 36 al-5), which serves `model.fiscal_unresolved`.
- **Walk:** 1299 HK `tmp/ui-walk/20261005T005134Z`, 29 shots, 0 API issues, disarm REFUSED.

## What the Model tab shows (`011-1299-HK-Equity-Model.png`, read by the issuer)

- **Gap reasons (FWD-20 limit 1): met on the page.** Every `--` inside a showing row carries footnote mark 1, with a hover title.
  That covers Dividend yield, FCF yield, P/E and P/B in 2016, 2017 and 2022, and the V3 price-dated range rows in the same years.
  The note under the table reads once: "1 The price-dated range is not reported at this company's fiscal year end, because its
  fiscal year does not end in December."
- **Currency (FWD-20 limit 2): NOT yet visible.** The money rows (Total assets, Capital expenditure, Cash flow from operations,
  Market capitalisation at the fiscal year end, ...) still carry the `*` "currency not stated by the source" mark. The served
  blocks still have currency null on those figures. The page half is ready, and the served half is CRPS-am-2's re-derive, which
  runs after the 2026-10-05 13:00Z fire's read. TSM's page is re-read in am-2's leg v.
