# AMGT_HARVST gold rebuild #8 -- the rule gate run, read (issuer `2.0.0_SA_COO~H`, 2026-10-07 ~19:3xZ)

**Run:** `gold_rebuild8.signing4.py` beside this file, 18:01Z-19:09Z, on the list file the act will pass
(`securities.universe.r60.json`, 242 securities, equal to `universe_securities.build()` at HEAD), applying
`gold_rebuild8_rule.rule` against the served snapshot. **PUTS SENT 0.** Output `gold_rebuild8.signing4.out`, record
`gold_rebuild8.signing4.json`.

## THE RULE AS WRITTEN IS BROKEN, ON ONE CAUSE

| | served | built | gone | added | changed |
|---|---|---|---|---|---|
| mention | 33,665 | 47,900 | **17** | 14,252 | 12,032: class (g) own-alias 3,257, class (f) co-mention 8,730, **UNEXPLAINED 45** |
| daily | 59,148 | 67,760 | 0 | 8,612 | 38,266: class (a) touched security 37,433, class (d) past-day coverage 558, **OTHER 275** |

Added 14,252 = on an unchanged alias set 7,754 + on a new security 3,881 + on a security whose alias set differs 2,617.
Mention count went DOWN on 2 rows, both `ASML_US_Equity`, a security that lost a served alias (allowed by the rule).

**The cause of all three breaks: the refusal of the ticker form `ICT` reaches a SERVED security.**
`ticker_refusals` refuses by ticker root, and two securities share the root: `ICT_PM_Equity` (new in the list, where the form
was graded 0 of 10) and `ICT_US_Equity` (in the served file, with the served form `ICT`). `ICT_US_Equity` is the ONE common
security that loses a served exact-case ticker form (read over all 212). Its served alias is the cut name
`International Container Termin`, which matches no text, so every served pair it holds rests on `ICT`:

- **GONE 17 = all 17 served pairs of `ICT_US_Equity`** (read from the served snapshot, `ICT_US_SERVED_PAIRS.json`):
  `match_forms` is `["ICT"]` on 17 of 17; 16 Seeking Alpha, 1 Bloomberg.
- **UNEXPLAINED 45:** co-mention fields on other securities' rows in those 17 articles (Apple, Nvidia, Hon Hai, Alibaba),
  which lose `ICT_US_Equity` from their co-mentioned set. The rule's "moved" set counted added and own-alias rows, not gone
  ones.
- **Daily OTHER 275:** `ICT_US_Equity`'s own day rows, which lose those mentions. Same omission.

The 17 served pairs, by title (none is about International Container Terminal Services; this is the issuer's reading of
titles, and the form's grade is the CVO's 0 of 10 on the sibling security):

| # | publisher | article | title |
|---|---|---|---|
| 1 | bbg | bbg:TCJXA4KJH6V400 | Huawei Growth Stalls After Apple Comeback Offsets China AI Push |
| 2 | sa | sa:4625693 | Foxconn July revenue surges 54% on AI demand; eyes strong Q3 on peak tech season |
| 3 | sa | sa:4600932 | Foxconn sees Q2 growth above prior forecast after record May revenue |
| 4 | sa | sa:4585375 | Foxconn sees record April revenue amid AI server rack growth |
| 5 | sa | sa:4564632 | Foxconn’s Q4 profit misses estimates; sees strong AI server growth in 2026 |
| 6 | sa | sa:4547683 | Foxconn's January revenue soars, sees strong Q1 amid AI demand |
| 7 | sa | sa:4536532 | Foxconn's Q4 revenue surges 22% Y/Y driven by AI demand |
| 8 | sa | sa:4528821 | Apple iPhone assembler Foxconn posts 25.53% November revenue gain despite sequential decline |
| 9 | sa | sa:4520302 | Foxconn sees AI-driven growth in 2026, teases OpenAI announcement |
| 10 | sa | sa:4515426 | Apple iPhone assembler Foxconn reports 11.3% Y/Y revenue growth in October |
| 11 | sa | sa:4501860 | Top iPhone assembler Foxconn posts record revenue for Q3, but falls short of expectations |
| 12 | sa | sa:4478167 | Nvidia partner Foxconn's July sales growth slows |
| 13 | sa | sa:4465497 | Foxconn Q2 sees record revenue amid AI demand |
| 14 | sa | sa:4420581 | Foxconn sees strong growth in 2025 after Q4 net profit miss, AI server revenue to double in Q1 |
| 15 | sa | sa:4043228 | Foxconn raises Q4 outlook on back of peak season, November revenue climbs Y/Y |
| 16 | sa | sa:3924072 | Apple may release $99 AirPods, new AirPods Max headphones as soon as next year |
| 17 | sa | sa:3642211 | NTT and SAP deepen strategic global alliance |

## The decision this needs (`1.0.0_SA_CTO~Z`), because a never-widen rule says no served pair goes

- **(h) REFUSED-FORM REMOVAL:** a served pair that rests ONLY on a ticker form refused on a graded census is removed, each
  one named in the pair. Here: 17 pairs, one security, which then holds 0 pairs until it carries a name that matches text.
  The rule then counts a gone pair's security as moved, which explains the 45 and the 275; anything else stays a break.
- **or EXEMPT `ICT_US_Equity`** from the refusal: nothing served goes, and the 17 Foxconn and Huawei articles stay on that
  company's page.

## Not in this read

- Dry run 3's cause split and per-form table on this same list (in flight at this writing; `gold_rebuild8.signing3.out`).
- The 9 ticker forms no sampled row reached (17 pairs), the 3 Carlisle pairs on CSL, and the empty-alias fallback: stated
  bounds for the pair, unchanged.
