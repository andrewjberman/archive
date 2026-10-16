# The dev-overlap waiver set for the DEV-based ticket-page candidate (derived from git, 2026-10-16)

**Candidate to be registered:** `cand/dell2/ticket-hop-failure-read-dev`, head `bdeeaa88f3596a761b85dd66fd377f850e390bde`: five commits (the worker's `e24facfa`, `eafc9aee`, `f4e5cc18`, `f488e20a`, `69208b1e`, cherry-picked) on the DEV tip `34a6baf8657bb166676dc3b8c3eec97ee8d3e585`. Measured on that tree: `tsc -b` rc 0; `bun test src/pages/TicketCenter` 196 pass, 0 fail across 31 files; the cell's check `V31-FAILURE-OK pass=13`.
**Why a waiver:** the registration check (`open-calls.py add --kind approval`) refuses a branch that carries commits already on DEV: `APPROVAL-REGISTER result=REFUSED reason=dev-overlap overlap=38 commits=43`. The 38 are not the feature's: they are the DEV history that this branch is built on, and they are exactly `git rev-list origin/PROD..origin/DEV` (PROD `8012cd1afbaad0e537cf48b1fa5f5ddb1e549f9f`), the approved-but-unpromoted features already merged to DEV. The remaining 5 of the 43 are the feature's own.
**What the waiver needs (`open-calls.py add --waive-overlap <shas> --waiver-ref <ruling file>`):** the shas named (never a count), and a ruling file that names them and exists. The cross-adjudication `XA-20261016T073942Z-102b` is OPEN with its ruling pending and has no record file in the repository yet; this file is the list its ruling can cite. The CTO re-approves the DEV-based head by its own sha after reading its diff against DEV (his message 9177).

## The 38 waived commits (38), full sha and subject

| # | sha | subject |
|---|---|---|
| 1 | `34a6baf8657bb166676dc3b8c3eec97ee8d3e585` | Merge cand/dell2/irpt-series-mirror-contract-031 into DEV (approved feature) |
| 2 | `a020da0bff1f043fb8dd58060e818f5290e307ab` | DB-c-26: page mirror takes on series contract 0.3.1 (IRPT_DASHBD round 148) |
| 3 | `03f92d82c23fc270e1115c15989e7637f430e16d` | Merge cand/dell2/irpt-fwd10-partial-history-sentence into DEV (approved feature) |
| 4 | `f7eb6b1459037d22cbc019d1be36767b106f3421` | Merge cand/dell2/anlreq-filing-notice into DEV (approved feature) |
| 5 | `39dab87f3b0c846db4354abda527f1c18825796d` | Merge cand/dell1/amgt-sa-withheld-reasons into DEV (approved feature) |
| 6 | `9e0bcb6003df6464d87b15d8632f6f85e2b1bed0` | fix(irpt-dashbd): FWD-10 partial-history sentence says where the data starts, no cause; fallback absence pinne |
| 7 | `0ba0cb13558246f2b980a702e47de3d34f3def68` | feat(TicketCenter): show the door's not-covered NOTICE under a filed outcome (AR-y-365, IRPT_ANLREQ round 41) |
| 8 | `e58c64ad7996261b184b4f99c5a6bbd47b76f07a` | fix(TicketCenter): the filing decision tree is gated on TICKER_NOT_FOUND, not on NAME_PROXY (AR-y-364) |
| 9 | `9b20efde91269e8b89fada01e1670a41402078a1` | feat(TicketCenter): C-FILING-DECISION-TREE for an unknown ticker, Yes / Replace / No (AR-y-363, PRD v0.19) |
| 10 | `d6fd06842f85e21f448b82309d95c92cd593bada` | Merge cand/dell2/tckt-meeting-and-trade-form into DEV (approved feature) |
| 11 | `ee278065576ea771f60291190f5b2307d73d3087` | Merge cand/dell1/amgt-sa-team-estimate-mark into DEV (approved feature) |
| 12 | `ad7c100b5cca9020f18a2957112361f4b9083272` | Merge cand/dell2/anlreq-ticket-commentary-pdf-reader into DEV (approved feature) |
| 13 | `e0b033253b973fcc19779a3783bc4979c14c65a0` | Merge cand/dell1/mdpf-canon-global-trend-variant1-rf-dev into DEV (approved feature) |
| 14 | `85f1d324bdfa69438a03b197c5a20864d3bf7485` | MDPF_CANON round 9 (2.0.0_SA_COO~D1): DEV resolution of the Global AUA Trend candidate -- origin/DEV e578b378  |
| 15 | `e578b378d332ad1505018be3801466dac7aeeade` | Merge cand/dell1/satellite-returns-method into DEV (approved feature) |
| 16 | `bbad56e354e9091170fe8a94c02b03c824bc4aba` | Merge cand/dell1/trsb-history-excel-download into DEV (approved feature) |
| 17 | `90d615c0873f6c74e49dcbd19f3fd7d276d86cef` | Merge cand/dell2/anlreq-internal-filer-chooses-firm into DEV (approved feature) |
| 18 | `66d221626ec3ca04b68485b95ec7998d0dd60264` | Merge cand/dell2/asof-date-only-no-invented-clock into DEV (approved feature) |
| 19 | `c05e3ddaa1ce97ecb98fe26d5f592dd01fbf0e2a` | feat(TicketCenter): Trade Request as a form upload; engine submit unwired (candidate) |
| 20 | `12c164a0732db6b040df78a0a5d820e9fb220a96` | feat(TicketCenter): Meeting Request form and coordinator outcome (candidate) |
| 21 | `a17932990a377161ce94c69375f2639348542eb1` | test(IRPT_ANLREQ AR-y-332): mirror analysis-request-pdf for analysis-request-commentary-pdf in the InvestorRep |
| 22 | `284e54d27206025ef7bfc3d7b3bf7f276c1bc52a` | feat(IRPT_ANLREQ AR-y-332): the Ticket Center's Commentary item opens the standalone commentary PDF |
| 23 | `b763674bb4d5e62e40e6dbec78f4d7dacc34ba06` | golden: the ModelPortfolios date-only footer prints its date words, no invented clock (IRPT_DASHBD round 110,  |
| 24 | `9de7c7e3227c321d45c2b6d3d3ccf72590b20710` | Merge cand/dell1/satellite-factsheet-prod into DEV (approved feature) |
| 25 | `3db44fe0e9c3392e37cb39f4ef142fd3f22b3514` | lint: the unused formatDataAsOfDisplay options argument is named _options (DB-b-219) |
| 26 | `00f5c1b44cd257a63eacac0ec0cf15202ddf51cd` | fix(as-of): a date-only value never shows an invented clock (IRPT_DASHBD round 110, DB-b-219) |
| 27 | `9e637fe51ebfa6322910cc032945a1e755e9ea13` | Merge cand/dell1/mdpf-canon-aua-trend-groups-and-as-of into DEV (approved feature) |
| 28 | `1c5f9daeb887b138a3d67f7a84c4952b0b6ae162` | Merge cand/dell1/sechist-frontier-label into DEV (approved feature) |
| 29 | `7f6c698d429cffeb5990265ed35d20a46e6735e3` | Merge cand/dell2/anlreq-commentary-always-requested into DEV (approved feature) |
| 30 | `34cd12d2d041e225767c8c80176570d6921a011a` | FWD-3 follow-on (MDPF_CANON round 7, CN-l-2, 0.9.0_WK_MDPF_CANON~18): the Model Portfolios Other Models card d |
| 31 | `4f1004518604cac12f296c7c808d81475e903cec` | FWD-9 (MDPF_CANON round 7, CN-i-1, 0.9.0_WK_MDPF_CANON~18): AUA Trend groups custom models and draws the strat |
| 32 | `97c66c93640b5853e2ec1dbd5d73765f2e888321` | Merge cand/dell1/amgt-sa-pe-basis-and-reasons into DEV (approved feature) |
| 33 | `22795405240520ea0fb4f87f942b20c285190696` | Merge cand/dell2/partner-firm-stack into DEV (approved feature) |
| 34 | `2deb4f1d864d8fa23cccbf9a11fb3266c88e1042` | Merge cand/dell2/irpt-ytd-from-first-day-and-wider-export-modal into DEV (approved feature) |
| 35 | `ab8ecc5662c9166bc4b3ff3d9ba370733ba4d3cf` | Merge cand/dell1/aifill-blocks-prod into DEV (approved feature) |
| 36 | `514df1bbf04d91f88dad30f6336b8992228710a6` | Merge cand/dell1/amgt-sa-currency-symbol-and-reasons into DEV (approved feature) |
| 37 | `5e40e54119474b50702f71db979df861481615a4` | Merge cand/dell1/amgt-sa-header-money-and-dash-reasons into DEV (approved feature) |
| 38 | `24877b67b7a175bcfe73c779f69c0bf7c3c639c8` | Merge cand/laptop/contributing-boxes into DEV (approved feature) |

## The comma-separated form for `--waive-overlap`

```
34a6baf8657b,a020da0bff1f,03f92d82c23f,f7eb6b145903,39dab87f3b0c,9e0bcb6003df,0ba0cb135582,e58c64ad7996,9b20efde9126,d6fd06842f85,ee278065576e,ad7c100b5cca,e0b033253b97,85f1d324bdfa,e578b378d332,bbad56e354e9,90d615c0873f,66d221626ec3,c05e3ddaa1ce,12c164a0732d,a17932990a37,284e54d27206,b763674bb4d5,9de7c7e3227c,3db44fe0e9c3,00f5c1b44cd2,9e637fe51ebf,1c5f9daeb887,7f6c698d429c,34cd12d2d041,4f1004518604,97c66c93640b,227954052405,2deb4f1d864d,ab8ecc5662c9,514df1bbf04d,5e40e5411947,24877b67b7a1
```
