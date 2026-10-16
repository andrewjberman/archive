# G4 enable pair -- the measurements read so far (2.0.0_SA_COO~R1, 2026-10-16 ~01:1xZ)

Prep for the separate enable pair the CTO ruled (`ledger/CTO_RULING_G4_CUT_BN6_20261015.md`). Nothing is registered or enabled. Nothing was spent: both reads below are read-only.

## Filings batch: population and per-name cost

- **Population, measured** (`python -m lib.research.filings.batch --universe newest --plan-only`, rc 0, run 2026-10-16 ~01:0xZ on dell1; `PLAN-ONLY: no document fetched, no model call, no pool write, no task run`): 302 universe rows = 5 SKIP-UNCHANGED, **171 WOULD-RUN**, 126 UNRESOLVED-SOURCE (filing_identity.source is 'none': no cik and expected form to fetch by). The first fire runs the 171, by rule (b).
- **Per-name cost, recorded by the producer, not independently measured:** the five stored analyses (analyzer `opal-filings-analyze/2.1.0`, `filings/v1/<key>/<accession>.analysis.json`, read through `harvest_read`) each carry `usage.usd`, which the analyzer computes from its token counts and its own rate constants (`lib/research/filings/analyze.py` lines 349-358).

| name | input tokens | output tokens | usd |
|---|---|---|---|
| ASML NA | 60,419 | 12,451 | 0.6133 |
| PBR US | 70,593 | 12,346 | 0.6616 |
| SAP GY | 71,557 | 13,103 | 0.6854 |
| BABA US | 78,020 | 12,763 | 0.7092 |
| NU US | 79,106 | 16,336 | 0.8039 |

  Mean 0.6947, range 0.6133 to 0.8039 (n = 5 of 176 names with a resolvable source). The five are the names that already had an analysis, so they are not a random draw of the 171.
- **First-fire figure, filings only (inferred):** 171 x 0.6947 = about USD 118.8 (range 104.9 to 137.5). A stop at 1.5 times the central figure is about USD 178.
- **Not read:** that the rate constants still match the model's current price; the management batch's cost (it also calls the model; no stored usage read yet); the scores batch (S3 reads and math, no model call).

## Management batch: population and what it spends (read 2026-10-16 ~01:4xZ, read-only)

- **Population, measured** (`python -m lib.research.management.batch --dry-run`, rc 0: `nothing built, no Lusha call, no SERP call, no pool write, no task run`): 243 records = 14 real-filing, 179 placeholder-only, 50 no-object; **14 would be built** (6861 JP, ASML NA, BABA US, BA US, CAT US, COST US, HAL US, HD US, INTU US, KMB US, NU US, PBR US, SAP GY, VLO US). The first fire builds those 14.
- **What it spends is vendor credits, not model tokens, on every stored record (14 of 14 read through boto3 `get_object`, bucket `opal-data-harvest`, newest `management/v1/<key>/` object per name, read-only, 2026-10-16 ~02:3xZ):** `lusha_enrichment.status` CALLED on 5 names (BABA US, BA US, COST US, HD US, SAP GY) at `credits_used` 2 each; SKIPPED at 0 credits on the other 9 (6861 JP, ASML NA, CAT US, HAL US, INTU US, KMB US, NU US, PBR US, VLO US). Sum 10 credits, mean 0.71 a name, range 0 to 2, over the 14. None of the 14 carries a model-usage field. Each build also runs a Bright Data SERP query for the CEO's public profile (`ceo_public_profile.status` RESOLVED on 2, ABSENT on 12); its price is not recorded on the records. `ceo_search.py` also holds an Anthropic path (`anthropic_call`, max 2,000 tokens, rated at USD 5e-6 an input token and 25e-6 an output token), whose use on a real run is NOT read here.
- **First-fire bound, inferred:** at most 14 x 2 = 28 Lusha credits if every one of the 14 is CALLED (10 were on the last stored run); 14 SERP queries. No dollar figure: the Lusha credit price and the SERP price are not in the repository files read here.
- **Correction to my bn-6 grade note and the card:** "only filings and management make model calls" holds for management only through that CEO-search path; the recorded spend of a management build is Lusha credits and a SERP query. The price of a Lusha credit and of a SERP query is not in the repository files read here.

## What the pair still needs before the enable

1. The management batch's spend as a figure: the Lusha credit price and the SERP price (not read), and whether a real run calls the Anthropic CEO-search path; the credit counts are read (14 of 14).
2. A claim line on the figure: which of the numbers above the CTO reads as measured (the 171) and which as inferred (the product).
3. Whether the first fire runs the whole 171 or a capped first fire (a CTO call; rule (b) makes the first fire due for the whole population).
