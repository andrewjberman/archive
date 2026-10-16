# TCKT_VNEXT R20-pt-1 -- the DEV-overlap waiver set for the DEV-based candidate (`2.0.0_SA_COO~V2`, 2026-10-16)

**Candidate:** `cand/dell2/tckt-meeting-outcome-visibility`, head `8e4f088522685acf223c1054cb5e896df613cbeb` (on origin, ls-remote read), ONE feature commit on portal `origin/DEV` `fcbf2bcecb45eb502da8517c0933aafee68a688c`. **PROD:** `origin/PROD` `fa21a303d87271a1e2d60c514d13501d71f9f020` (fetched this tick).
**Why a waiver:** the registration check refuses the candidate `dev-overlap overlap=53 commits=54`. The 53 are DEV's own history of features approved on their own rows; the 54th is this feature. The candidate is DEV-based because the cell was cut from DEV (the Ticket Center board it edits carries the DEV-only meeting form).
**Measured:** `git rev-list origin/PROD..8e4f0885` = 54; `git rev-list origin/DEV..8e4f0885` = 1 (the feature); the overlap = 53. The 53 equal, sha for sha, `git rev-list origin/PROD..origin/DEV` (`comm -3` difference: empty; DEV did not move between the cut and this read).
**Precedent:** `CTO_RULING_DELL2_05CE_DEV_OVERLAP_WAIVER_TICKET_HOP_FAILURE_READ_DEV_20261016.md` (waiver for DEV only, never a PROD promote; the PROD promote list puts the overlapping features first).

## The 53 commits (sha, subject; read from git)

- `00f5c1b44cd257a63eacac0ec0cf15202ddf51cd` fix(as-of): a date-only value never shows an invented clock (IRPT_DASHBD round 110, DB-b-219)
- `03f92d82c23fc270e1115c15989e7637f430e16d` Merge cand/dell2/irpt-fwd10-partial-history-sentence into DEV (approved feature)
- `0ba0cb13558246f2b980a702e47de3d34f3def68` feat(TicketCenter): show the door's not-covered NOTICE under a filed outcome (AR-y-365, IRPT_ANLREQ round 41)
- `11395a805752a9403edb663eed5eeef7ede75836` fix(TicketCenter): no status call unless the ticket is an analysis request with a request id and no package (IRPT_ANLREQ TO-AR-v31 AMENDMENT 2, AR-v-31)
- `12c164a0732db6b040df78a0a5d820e9fb220a96` feat(TicketCenter): Meeting Request form and coordinator outcome (candidate)
- `1510cd7a8573a00282e66ec1a9b97c9e7f24a3c7` MDPF_CANON CN-s-3 (AMENDMENT 2 repair): cottonwoodTrend.ts reads the Total and the five primary lines through the paired accessor
- `1c5f9daeb887b138a3d67f7a84c4952b0b6ae162` Merge cand/dell1/sechist-frontier-label into DEV (approved feature)
- `1d7ed40d4e006d0664478beb608b54e0c4b7a519` Merge cand/dell1/mdpf-canon-v2-band-repair into DEV (approved feature)
- `22795405240520ea0fb4f87f942b20c285190696` Merge cand/dell2/partner-firm-stack into DEV (approved feature)
- `24877b67b7a175bcfe73c779f69c0bf7c3c639c8` Merge cand/laptop/contributing-boxes into DEV (approved feature)
- `284e54d27206025ef7bfc3d7b3bf7f276c1bc52a` feat(IRPT_ANLREQ AR-y-332): the Ticket Center's Commentary item opens the standalone commentary PDF
- `2deb4f1d864d8fa23cccbf9a11fb3266c88e1042` Merge cand/dell2/irpt-ytd-from-first-day-and-wider-export-modal into DEV (approved feature)
- `34a6baf8657bb166676dc3b8c3eec97ee8d3e585` Merge cand/dell2/irpt-series-mirror-contract-031 into DEV (approved feature)
- `34cd12d2d041e225767c8c80176570d6921a011a` FWD-3 follow-on (MDPF_CANON round 7, CN-l-2, 0.9.0_WK_MDPF_CANON~18): the Model Portfolios Other Models card draws "as of <date>" when its value is carried
- `39dab87f3b0c846db4354abda527f1c18825796d` Merge cand/dell1/amgt-sa-withheld-reasons into DEV (approved feature)
- `3db44fe0e9c3392e37cb39f4ef142fd3f22b3514` lint: the unused formatDataAsOfDisplay options argument is named _options (DB-b-219)
- `4d080de4f997288205cf01d2005b31b40e826d77` test(TicketCenter): hop-failure-read harness registers its own DOM as partner-view does (IRPT_ANLREQ TO-AR-v31, AR-v-31)
- `4f1004518604cac12f296c7c808d81475e903cec` FWD-9 (MDPF_CANON round 7, CN-i-1, 0.9.0_WK_MDPF_CANON~18): AUA Trend groups custom models and draws the strategy groups as chips
- `514df1bbf04d91f88dad30f6336b8992228710a6` Merge cand/dell1/amgt-sa-currency-symbol-and-reasons into DEV (approved feature)
- `5e40e54119474b50702f71db979df861481615a4` Merge cand/dell1/amgt-sa-header-money-and-dash-reasons into DEV (approved feature)
- `62b3dd53461cae63327f0258a1c2f693098e7463` MDPF_CANON CN-s-4: the Variant 2 Models band is never carried forward on or after per_model_detail_begins
- `66d221626ec3ca04b68485b95ec7998d0dd60264` Merge cand/dell2/asof-date-only-no-invented-clock into DEV (approved feature)
- `7d5f953cfffd16aa3fdb5514be4c30b658ee7cf8` fix(TicketCenter): the hop failure shows for a ticket with neither a draft nor a package, and no blank row (IRPT_ANLREQ TO-AR-v31 AMENDMENT 1, AR-v-31)
- `7f6c698d429cffeb5990265ed35d20a46e6735e3` Merge cand/dell2/anlreq-commentary-always-requested into DEV (approved feature)
- `85f1d324bdfa69438a03b197c5a20864d3bf7485` MDPF_CANON round 9 (2.0.0_SA_COO~D1): DEV resolution of the Global AUA Trend candidate -- origin/DEV e578b378 plus the approved cand/dell1/mdpf-canon-globa
- `90d615c0873f6c74e49dcbd19f3fd7d276d86cef` Merge cand/dell2/anlreq-internal-filer-chooses-firm into DEV (approved feature)
- `97c66c93640b5853e2ec1dbd5d73765f2e888321` Merge cand/dell1/amgt-sa-pe-basis-and-reasons into DEV (approved feature)
- `9b20efde91269e8b89fada01e1670a41402078a1` feat(TicketCenter): C-FILING-DECISION-TREE for an unknown ticker, Yes / Replace / No (AR-y-363, PRD v0.19)
- `9de7c7e3227c321d45c2b6d3d3ccf72590b20710` Merge cand/dell1/satellite-factsheet-prod into DEV (approved feature)
- `9e0bcb6003df6464d87b15d8632f6f85e2b1bed0` fix(irpt-dashbd): FWD-10 partial-history sentence says where the data starts, no cause; fallback absence pinned (DB-c-24, round 146)
- `9e637fe51ebfa6322910cc032945a1e755e9ea13` Merge cand/dell1/mdpf-canon-aua-trend-groups-and-as-of into DEV (approved feature)
- `a020da0bff1f043fb8dd58060e818f5290e307ab` DB-c-26: page mirror takes on series contract 0.3.1 (IRPT_DASHBD round 148)
- `a17932990a377161ce94c69375f2639348542eb1` test(IRPT_ANLREQ AR-y-332): mirror analysis-request-pdf for analysis-request-commentary-pdf in the InvestorReporting pins
- `a7f4de88c408061db58986abae4aa880c3f1c641` MDPF_CANON CN-s-3 repair (AMENDMENT 1): the Cottonwood carried keys carry the display names of the five primary series
- `ab8ecc5662c9166bc4b3ff3d9ba370733ba4d3cf` Merge cand/dell1/aifill-blocks-prod into DEV (approved feature)
- `ad7c100b5cca9020f18a2957112361f4b9083272` Merge cand/dell2/anlreq-ticket-commentary-pdf-reader into DEV (approved feature)
- `b763674bb4d5e62e40e6dbec78f4d7dacc34ba06` golden: the ModelPortfolios date-only footer prints its date words, no invented clock (IRPT_DASHBD round 110, DB-b-219)
- `bbad56e354e9091170fe8a94c02b03c824bc4aba` Merge cand/dell1/trsb-history-excel-download into DEV (approved feature)
- `bdeeaa88f3596a761b85dd66fd377f850e390bde` fix(TicketCenter): the page shows the generator words for ANALYSIS_FAILED, ANALYSIS_REQUIRES_ATTENTION and DELIVERIES_EXHAUSTED (IRPT_ANLREQ TO-AR-v31 AMEN
- `c05e3ddaa1ce97ecb98fe26d5f592dd01fbf0e2a` feat(TicketCenter): Trade Request as a form upload; engine submit unwired (candidate)
- `c748b8fe27a898bc1f3f0c82c0b527b5f909f836` feat(TicketCenter): the ticket page reads a hop failure through the status route (IRPT_ANLREQ TO-AR-v31, AR-v-31, FWD-4)
- `d1f9ca29675bd9012284272806afc9c587ef55f0` Merge cand/dell1/aifill-provenance-wording-v2 into DEV (approved feature)
- `d407bd676319abe1c49fc77e01e0a5f9f93a4317` MDPF_CANON CN-s-3: the Cottonwood AUM Trend starts at its first measured total, fills Other AUM, carries the 12 absent model legs
- `d6fd06842f85e21f448b82309d95c92cd593bada` Merge cand/dell2/tckt-meeting-and-trade-form into DEV (approved feature)
- `dc057891b086d6cb3752aedd7033e3df13b0a9d0` Merge cand/dell2/ticket-hop-failure-read-dev into DEV (approved feature)
- `e0b033253b973fcc19779a3783bc4979c14c65a0` Merge cand/dell1/mdpf-canon-global-trend-variant1-rf-dev into DEV (approved feature)
- `e578b378d332ad1505018be3801466dac7aeeade` Merge cand/dell1/satellite-returns-method into DEV (approved feature)
- `e58c64ad7996261b184b4f99c5a6bbd47b76f07a` fix(TicketCenter): the filing decision tree is gated on TICKER_NOT_FOUND, not on NAME_PROXY (AR-y-364)
- `ee278065576ea771f60291190f5b2307d73d3087` Merge cand/dell1/amgt-sa-team-estimate-mark into DEV (approved feature)
- `f7eb6b1459037d22cbc019d1be36767b106f3421` Merge cand/dell2/anlreq-filing-notice into DEV (approved feature)
- `f91881ad5ca7e75d8a2f4c0389b8e0ec38aa2763` Merge cand/dell2/irpt-series-mirror-contract-033 into DEV (approved feature)
- `fc174c6917a27daef4a5db577c97a0f899a9d056` Merge cand/dell1/aifill-provenance into DEV (approved feature)
- `fcbf2bcecb45eb502da8517c0933aafee68a688c` Merge cand/dell1/mdpf-canon-cottonwood-trend-upgrade into DEV (approved feature)
