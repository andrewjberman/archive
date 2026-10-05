# AMGT_CORPUS round 36 -- the ONE REAL RUN of al-2 + al-5: the Model tab on the candidate portal against the redeployed API

- **Instrument:** `/ui-walk` (`walk.mjs --route /security-analysis --security <key>`) on `bun run dev:live --port 5174`, served from
  the al-2 candidate checkout `C:/tmp/wk-crps-r36-1/portal` @`75efe9d6`, which DEV fast-forwarded to at 22:5xZ (MSTR~Z msg
  29299, CI run 37241631766 success). The API is the deployed `opal-amgt-scoped-api` CodeSha256 `2rFeF57l...` (al-5, 22:42:11Z).
- **Walks:** BA `tmp/ui-walk/20261004T224710Z` (37 shots, 0 API issues) and 1299 HK `tmp/ui-walk/20261004T225046Z` (29 shots,
  21 1299_HK_Equity requests, 0 non-200). Both disarms read REFUSED (401).

## What 1299 HK's Model tab shows (`011-1299-HK-Equity-Model.png`, read by the issuer)

- **The V3 group** "VALUATION, RETURN AND BALANCE-SHEET LINES" sits after "EBITDA AND MARGIN HISTORY". Its rows are in words with
  their type: Total assets (millions), the Average / Highest / Lowest price and enterprise-value multiples, Capital expenditure,
  Cash flow from operations, Market capitalisation at the fiscal year end, Return on assets / equity normalised, and Total equity.
- **The facts line:** "Company short name: AIA; Country: HONG KONG; Average daily value traded (three months): 2,079,092,000; Market
  capitalisation: 715,988 million."
- **The reason line:** "Lines with no figure: Bloomberg returned no value for this line for this company." The "No figures served
  for:" footnote names the fully-absent lines (Goodwill, Other intangible assets, Shares outstanding as reported, Total current
  liabilities, the trailing-EBITDA averages, Fiscal year of the financial statements, ..., Cash flow per share (consensus)).
- The existing groups and "What changed" are DSGN's, unchanged.

## What the page does NOT do (for the CVO's AC3 judgment and the analysis)

1. **A gap inside a row has no reason.** On 1299 HK the price-dated range rows read `--` in 2016, 2017 and 2022. Those are exactly
   the years the API now serves with "not dated at the fiscal period end (non-December FYE, fye_join)" (al-5: 97 entries), but
   al-2 words a reason only for a FULLY absent row. FWD-20 asks that "a row that still cannot show says why"; a blank year inside
   a showing row is a narrower case, and it is not covered.
2. **Money lines name no currency.** The V3 money rows carry the page's "* currency not stated by the source" mark. The facts
   line's market cap and average daily value traded print without a currency (TSM: row `AMGT_CORPUS-Z-W2-S20`; the CTO carries
   "market cap and average daily value should name their currency" to the round-36 analysis).
