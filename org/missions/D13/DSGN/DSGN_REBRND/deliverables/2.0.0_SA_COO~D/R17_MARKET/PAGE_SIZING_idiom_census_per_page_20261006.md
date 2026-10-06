# Light-on-dark idiom census per page -- the size of "page by page" (read-only, 2026-10-06 ~08:2xZ, portal DEV 4ca437eb)

Instrument: `node scripts/idiom-census.mjs <dir>` over each `src/pages/<Page>` (tests and docs skipped). Idiom = a utility class that paints white at an alpha on the assumption of a dark container: INK text-white*, SURFACE bg-white*, BOUNDARY border/divide/ring-white*. It counts classes only (inline chart props are not in this count).

| page dir | idioms | files |
|---|---|---|
| AdvisorIntelligence | 1232 | 64 |
| PortfolioManagement | 431 | 40 |
| TradeSubmission | 238 | 19 |
| DataRefresh | 153 | 15 |
| Macroeconomics | 148 | 10 |
| Attribution | 143 | 9 |
| FactorTilts | 129 | 9 |
| SecurityScanner | 115 | 16 |
| Positioning | 99 | 15 |
| InvestorReporting | 76 | 144 (its own lease, DSGN_IRPTV1) |
| Valuation | 68 | 9 |
| ModelPortfolios.tsx | 56 | 1 (the CRO's MDPF_TAXSMA page) |
| Correlation | 47 | 8 |
| CapitalMarketAssumptions | 39 | 9 |
| auth | 27 | 7 (out of the commission) |
| TicketCenter | 27 | 2 |
| ModelPortfolios/ | 21 | 1 |
| SecurityAnalysis | 13 | 42 (site Z) |
| MarketPerformance | 2 | 24 (delivered: R17 page 1) |
| shared (components, ui, lib, hooks, contexts) | 279 | 43 (after the market slice's shared primitives) |

Total of the page rows: about 3,000 idioms. /market took 351 (page slice) + 82 (lib/designTokens) + the shared panel primitives, with five modals drawn; a page's cost is roughly its idiom count PLUS the data-coloured text and the chart inks the count does not see (on /market: the Fear & Greed, RSI, regime and keyword modals each needed hand edits found only by drawing).

Honest limits: the count is regex-based (class strings built at runtime are unseen); it is not a time estimate; the order of the pages is Andrew's, not this table's; AdvisorIntelligence is 41 percent of the whole and has no fixtures for most of its tabs.
