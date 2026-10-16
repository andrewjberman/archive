# Cottonwood transaction Income: sizing for the enrichment the CTO queued (msg 9312), 2026-10-16 ~11:5xZ

Issuer `2.0.0_SA_COO~F2`. OFFLINE and values-free: computed from the committed census `R128_LIVE_SOURCE_CENSUS_3FIRMS.json` (rows per Transaction Type, Sub Type and External Flow; 1,096,830 rows, 125 partitions) and the contract 0.4.0's `cottonwood_mapping` (`external_flow_rule`, the pair's `flow_class_none`). No AWS call; nothing read from the table beyond the committed counts.

Cottonwood rows by the flow class the producer assigns (sums to 1,096,830):

| flow class | rows |
|---|---|
| INTERNAL | 588,650 |
| INCOME | 336,421 |
| EXTERNAL_IN | 102,676 |
| EXTERNAL_OUT | 55,251 |
| FEE | 12,757 |
| CORPORATE_ACTION | 865 |
| UNRESOLVED | 210 |

INCOME rows by pair (word): Dividend | Dividend 300,204 (Dividend); Interest | Interest 20,569 (Interest); Interest | Tax-Exempt 10,241 (Interest); Dividend | Non-Taxable 2,819 (Dividend); Capital Gains | Long-Term 1,797 (Capital gain); Interest | Sale of Accrued Interest 411 (Interest); Income | Income 318 (Other income); Dividend | Qualified 38 (Dividend); Capital Gains | Short-Term 24 (Capital gain).

**What this says for the enrichment.** The transaction table already separates income by CLASS: 336,421 Cottonwood lines (30.7 percent of rows). The CTO's count of the returns source's non-zero Income cells is 343,256. The two do not agree by 6,835 rows (2.0 percent). An enrichment that derives the series' income from transactions has to say which side that gap sits on before `income_claim` leaves `absent`: the first cell reads both counts per day from the table (counts and sums, values-free) and reports where a transaction-class INCOME line has a zero Income cell or the reverse. Not cut yet: it waits for the CVO's grades of the three producers and for the CTO's round-131 analysis, as the CTO's message says.
