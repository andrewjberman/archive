# Investor Reporting Suite -- status brief, in aggregate and per COO workstream (2026-10-15)

**Author:** `4.0.0_SA_CRO~DELL2`, on Andrew's word at the dell2 terminal. Ask: "I want to analyze where we're at here in our mission
to get the Investor Reporting Suite completely done. Please assess via the various COO workstreams what progress has been made and
what progress remains to be made." Export ask: "This is great we need this exported as an .md with all the included information and
committed as a brief."

**Scope (P1):** Andrew's 10-14 priorities
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261014_173xZ_DELIVERABLES_FOUR_PRIORITIES_AND_DATES.md:113`):
- the performance tab working for all clients at all firms;
- the holdings tab;
- the analysis function.

**Dates:** internal **Nov 15**, external **Dec 1**.

**Projects** (`PLAN_20261014_DELIVERABLES_BOX_ORGANIZATION.md:12`): IRPT_DASHBD, IRPT_BCKEND and DSGN_IRPTV1, plus IRPT_ANLREQ for the
analysis function.

**Basis:** read-only, 2026-10-15 ~21:30-21:45Z, from:
- the PRDs;
- the CTO round analyses and lane records;
- git;
- a live S3 read of each firm's holdings publication and performance gold.

**Live page:** https://claude.ai/artifact/EbQMfjEX1dQ3BidyQQewe3 (private until shared). It renders the same five data sets as this
file.

## 1. In aggregate

| Measure | Value |
|---|---|
| Planned outcomes realized | **3 of 41** (across the three PRDs) |
| Checkpoints done | **20 of 62** (named steps to completion, all workstreams) |
| Checkpoints blocked | **12** (waiting on another lane, a release or Andrew) |
| Workstreams waiting on another | **5 of 13** (the rest are building now) |
| Firms with current holdings | **1 of 3** (served as of T-1, 2026-10-14) |

**Takeaway:** the suite is mid-build, not near done. 3 of 41 planned outcomes are realized, and 20 of 62 named checkpoints are
done.
- **Holdings tab:** closest to finished, but two firms are stuck behind refused publishes.
- **Performance tab:** gold exists for every firm, but there is no default report on DEV yet.
- **Analysis request:** it reaches the report and the commentary, but no attachment lands on the ticket until releases r32 and r33
  are applied.

### Outcomes by project

| Project | Realized | In progress | Parked | Not started | Total |
|---|---|---|---|---|---|
| Performance tab and reports (IRPT_DASHBD) | 1 | 6 | 1 | 13 | 21 |
| Data behind the tabs (IRPT_BCKEND) | 2 | 7 | 0 | 4 | 13 |
| Analysis function (IRPT_ANLREQ) | 0 | 4 | 0 | 3 | 7 |

## 2. What each firm sees today

Holdings tab as-of, and the performance data behind the Performance tab. Live S3 read ~21:40Z; T-1 = 2026-10-14.

| Firm | Clients | Holdings as of | Trading days behind | Why | Performance |
|---|---|---|---|---|---|
| 49 Financial | 4,746 | 2026-10-12 | 2 | 10-14 refused: 2 accounts missing from custody | Reporting chain runs daily 07:41-08:45 NY; the default report is not on DEV yet |
| Cottonwood | 271 | 2026-10-08 | 4 | 10-14 refused: 4 accounts missing from custody | Daily returns from 07-10; 2013 to 06-22 history on a different contract; 12-trading-day gap |
| Inflection | 295 | 2026-10-14 | 0 | Current | Orion-based daily returns not yet running; 40 of 863 accounts lack a start date |

All three firms' holdings-basis performance gold is at 2026-10-14.

## 3. The analysis request, end to end

Today's test filing (run 2), step by step. Run 3 is the next milestone.

| # | Step | State |
|---|---|---|
| 1 | Staff opens the Ticket Center and fills the form | Works |
| 2 | Holdings file uploaded | Works |
| 3 | Ticket and analysis request created with the commentary flag | Works |
| 4 | Opal engine generates the report | Works |
| 5 | AI commentary drafted | Works |
| 6 | Report priced, all three report types | Built, not live |
| 7 | Attachments packaged onto the ticket | Broken (fix built in r32) |
| 8 | Four attachments shown on the open ticket | Not reached |

## 4. Workstreams and their checkpoints

Each COO lane: what it is doing now, what holds it, and its named checkpoints in order.

### Performance tab and reports (IRPT_DASHBD)

#### Performance tab: 49 Financial and the gold contract -- IN PROGRESS

- **Lane** `~D2`, round 143, last activity 2026-10-15 21:35 UTC. **2 of 6** checkpoints done, 2 blocked.
- **Scope:** 49F reporting gold, the sample builder, sole writer of the contract; also built Cottonwood's report function.
- **Doing now:** Chain-cap code-update pair (row S95) checker written.
- **Held by:** One 49F household on DEV waits on IRPT_BCKEND's report route (IB-pr-551).

| # | Checkpoint | Owner | State |
|---|---|---|---|
| 1 | Cottonwood report-build function live, 65 days backfilled | ~D2 | Done |
| 2 | Cottonwood daily returns landed 07-10 to 10-14 | ~D2 | Done |
| 3 | Chain-cap code-update pair (row S95) | ~D2 | In progress |
| 4 | Contract 0.4.2 (market-value claim, return-basis repair) | ~D2 | Not started |
| 5 | Cottonwood report schedule enabled on the CTO's word | CTO | Blocked |
| 6 | One 49F household served on DEV | ~D2 + ~P2 | Blocked |

#### Performance tab: Cottonwood -- WAITING

- **Lane** `~C2`, round 126, last activity 2026-10-15 14:45 UTC. **1 of 3** checkpoints done, 2 blocked.
- **Scope:** Cottonwood gold and its report runs.
- **Doing now:** No build cell; next act is reading the first scheduled Cottonwood report run.
- **Held by:** Report schedule stays off until ~D2's chain-cap pair lands; history before 07-10 waits on dell1's ADVI_COTBKF.

| # | Checkpoint | Owner | State |
|---|---|---|---|
| 1 | Cottonwood trace: silver to gold holds | ~C2 | Done |
| 2 | Read the first scheduled Cottonwood report runs | ~C2 | Blocked |
| 3 | Cottonwood history before 07-10 | ~C2 + dell1 | Blocked |

#### Performance tab: Inflection -- IN PROGRESS

- **Lane** `~I2`, round 125, last activity 2026-10-15 21:30 UTC. **1 of 6** checkpoints done, 3 blocked.
- **Scope:** Inflection gold from Orion.
- **Doing now:** Round 125 drained; 2 of 38 tests red on trunk.
- **Held by:** Real-row run waits on the Scope feed's first scheduled run; 40 of 863 accounts lack a start date (call c02c).

| # | Checkpoint | Owner | State |
|---|---|---|---|
| 1 | Round 125 drained | ~I2 | Done |
| 2 | Round 125 green on trunk (2 of 38 tests red) | ~I2 | In progress |
| 3 | Series-ended cause read (ruled: cut now) | ~I2 | Not started |
| 4 | Adopt contract 0.4.2 | ~I2 | Blocked |
| 5 | Real-row run on Orion data | ~I2 | Blocked |
| 6 | Start dates for 40 accounts (call c02c) | Andrew / Inflection | Blocked |

#### Default performance report: render, tab and export -- WAITING

- **Lane** `~F2`, round 118, last activity 2026-10-15 16:32 UTC. **1 of 5** checkpoints done, 1 blocked.
- **Scope:** FWD-21: one default report on the Performance tab and as the export.
- **Doing now:** Candidate branch ready (30 commits), not on DEV.
- **Held by:** Needs a served 49F sample (IB-pr-551, ~P2) and the disclosure page (calls a252, 90ef).

| # | Checkpoint | Owner | State |
|---|---|---|---|
| 1 | Rounds 114-118 closed; candidate ready | ~F2 | Done |
| 2 | Served 49F sample on DEV | ~F2 | Blocked |
| 3 | Version id printed on the report (row S70) | ~P2 | Not started |
| 4 | Client-facing approval registered | Andrew | Not started |
| 5 | Disclosure page (calls a252, 90ef) | Andrew | Not started |

### Data behind the tabs (IRPT_BCKEND)

#### Holdings producer and daily schedule -- IN PROGRESS

- **Lane** `~P`, round 198, last activity 2026-10-15 21:12 UTC. **1 of 4** checkpoints done, 1 blocked.
- **Scope:** The holdings producer, per-firm pins, the 6 AM New York schedule release.
- **Doing now:** Per-firm holdings mint (IB-pr-549) first leg closed; second leg reads at the next fire.
- **Held by:** 6 AM NY schedule release not started; row S206 (no CUSIP port on trunk) stops any HEAD-based 49F build.

| # | Checkpoint | Owner | State |
|---|---|---|---|
| 1 | Per-firm holdings mint, first leg (IB-pr-549 L1) | IB2 | Done |
| 2 | First fire read (IB-pr-549 L2) | IB2 | In progress |
| 3 | 6 AM New York schedule release, 49F first | ~P2 | Not started |
| 4 | CUSIP port on trunk (row S206) | MDPF_SECCLASS | Blocked |

#### Refused publishes (account_lost) -- IN PROGRESS

- **Lane** `~PJ / ~PQ`, round 5, last activity 2026-10-15 20:28 UTC. **2 of 6** checkpoints done, 0 blocked.
- **Scope:** Lets a firm publish past an account the custodian no longer carries.
- **Doing now:** Exemption pair packet and COO half.
- **Held by:** CTO half, then the IB-pr-605 apply.

| # | Checkpoint | Owner | State |
|---|---|---|---|
| 1 | Transplant digests met, all three firms | ~P2 | Done |
| 2 | 49F refusal anatomy (1 account, 4 securities) | ~P2 | Done |
| 3 | Exemption pair packet and COO half | ~P2 | In progress |
| 4 | CTO half | CTO | Not started |
| 5 | IB-pr-605 apply | IB2 | Not started |
| 6 | First publishing fire: 49F and Cottonwood current | ~P2 | Not started |

#### Split-adjusted returns -- IN PROGRESS

- **Lane** `~PM`, round 1, last activity 2026-10-15 20:00 UTC. **1 of 4** checkpoints done, 0 blocked.
- **Scope:** The stock-split rule in holdings returns (the VUG 6-for-1 on 04-21).
- **Doing now:** Split pair addendum 1 (1,291 of 266,455 account-days move).
- **Held by:** CTO signature, then the apply.

| # | Checkpoint | Owner | State |
|---|---|---|---|
| 1 | Split rule measured (1,291 account-days move) | ~P2 | Done |
| 2 | Split pair addendum 1 | ~P2 | In progress |
| 3 | Apply | IB2 | Not started |
| 4 | 04-21 VUG returns re-graded | ~P2 | Not started |

#### Inflection household feed -- IN PROGRESS

- **Lane** `~PN`, round 3, last activity 2026-10-15 21:12 UTC. **2 of 3** checkpoints done, 0 blocked.
- **Scope:** The Scope feed and household lift for Inflection.
- **Doing now:** IB-pr-596 applied 21:12Z; IAM grant IB-pr-600 live.
- **Held by:** The first scheduled run is the proof.

| # | Checkpoint | Owner | State |
|---|---|---|---|
| 1 | IB-pr-596 Scope feed applied | IB2 | Done |
| 2 | IB-pr-600 IAM grant live | IB2 | Done |
| 3 | First scheduled run proves the feed | ~P2 | In progress |

#### Inflection Orion re-cut -- IN PROGRESS

- **Lane** `~PO`, round 8, last activity 2026-10-15 19:00 UTC. **1 of 3** checkpoints done, 0 blocked.
- **Scope:** The Orion backfill and fold timing.
- **Doing now:** Pair (b) addendum 1 waits for an applier slot.
- **Held by:** Fold time moves to 06:00 NY only once T-1 completeness is proven.

| # | Checkpoint | Owner | State |
|---|---|---|---|
| 1 | Pair (a): 33-key backfill | ~P2 | Done |
| 2 | Pair (b) addendum 1 apply | IB2 | Not started |
| 3 | Fold time to 06:00 NY once T-1 is proven complete | ~P2 | Not started |

#### Filled-report export -- WAITING

- **Lane** `~PS`, round 6, last activity 2026-10-15 18:00 UTC. **1 of 3** checkpoints done, 1 blocked.
- **Scope:** The branded export's serve path.
- **Doing now:** Serve path built LOCAL.
- **Held by:** Deploy legs wait on IRPT_DASHBD's first cloud write of the report.

| # | Checkpoint | Owner | State |
|---|---|---|---|
| 1 | Filled-report serve path built LOCAL | ~P2 | Done |
| 2 | Deploy legs after the report's first cloud write | ~P2 | Blocked |
| 3 | Storage read grant checked | ~P2 | Not started |

### Analysis function (IRPT_ANLREQ)

#### Analysis request: filing and promote -- WAITING

- **Lane** `~Y2`, round 40, last activity 2026-10-15 21:33 UTC. **3 of 8** checkpoints done, 1 blocked.
- **Scope:** The Ticket Center filing, the FWD-1 run driver, PROD promotes.
- **Doing now:** Removing the price-date field (AR-y-360/361).
- **Held by:** Run 3 waits on report-machine releases r32 and r33 (~G2).

| # | Checkpoint | Owner | State |
|---|---|---|---|
| 1 | Firm chooser for staff on PROD | ~Y2 | Done |
| 2 | Did-you-mean hint on PROD | ~Y2 | Done |
| 3 | FWD-1 run 2: ticket, report and draft (0 of 4 attached) | ~Y2 | Done |
| 4 | Price-date field removed (AR-y-360/361) | ~Y2 | In progress |
| 5 | Run 3: four attachments on the open ticket | ~Y2 + AQ2 | Blocked |
| 6 | Ticket-page change re-promoted to PROD | ~Y2 | Not started |
| 7 | Andrew's own test | Andrew | Not started |
| 8 | Analysis tab as the manual path (FWD-6) | ~Y2 | Not started |

#### Analysis engine (report machine) -- IN PROGRESS

- **Lane** `~G2`, round 21, last activity 2026-10-15 21:31 UTC. **3 of 8** checkpoints done, 0 blocked.
- **Scope:** The Opal report engine, pricing, report types, the swap.
- **Doing now:** Release r32 built (packager fix, all three report-type maps, run-3 address).
- **Held by:** r32 needs its pair and apply; r33 not cut; pricing and the swap path not cut.

| # | Checkpoint | Owner | State |
|---|---|---|---|
| 1 | Release r31 live on the report machine | YC2 | Done |
| 2 | Release r32 built | ~G2 | Done |
| 3 | Price adapters, SPY and BIL proxies built | ~G2 | Done |
| 4 | r32 pair and apply | ~G2 + YC2 | Not started |
| 5 | r33: ticket stamps, derived price date | ~G2 | Not started |
| 6 | Pricing switched on | ~G2 | Not started |
| 7 | Comparison and Multi-Comp end to end | ~G2 | Not started |
| 8 | Typo and replacement swap path | ~G2 | Not started |

#### AI investment commentary -- WAITING

- **Lane** `~T2`, round 44, last activity 2026-10-15 20:35 UTC. **1 of 3** checkpoints done, 1 blocked.
- **Scope:** The commentary drafter and its PDF.
- **Doing now:** Figure block, closed vocabulary and INFO logger live (t34).
- **Held by:** First draft on a ticket waits on run 3.

| # | Checkpoint | Owner | State |
|---|---|---|---|
| 1 | Figure block, vocabulary and logger live | ~T2 | Done |
| 2 | Read why the transcript precedents are empty | ~T2 | Not started |
| 3 | First draft posted and its PDF opened on run 3 | ~T2 | Blocked |

## 5. Every planned outcome

From each PRD. Only IRPT_DASHBD FWD-8 carries a formal grade (REALIZED WITH NAMED RESIDUE, @8a8fed144f). The other states are read
from round records and order counts (basis "inferred").

| Outcome | What it delivers | State | Basis |
|---|---|---|---|
| IRPT_DASHBD FWD-1 | One 49F account's daily total-return history, any window | In progress | inferred |
| IRPT_DASHBD FWD-2 | Any account of any firm loads the same way | In progress | inferred |
| IRPT_DASHBD FWD-3 | Asset-class performance and mix over a window | Not started | inferred |
| IRPT_DASHBD FWD-4 | Realized, unrealized, income and an activity view | In progress | inferred |
| IRPT_DASHBD FWD-5 | Browse, filter and export transactions | Not started | inferred |
| IRPT_DASHBD FWD-6 | Trending topics at the deepest drawdown | Not started | inferred |
| IRPT_DASHBD FWD-7 | Household and client pages from the account grain | Not started | inferred |
| IRPT_DASHBD FWD-8 | A defensible return, tied out to Black Diamond | Realized | graded |
| IRPT_DASHBD FWD-9 | One Opal-shape gold for every firm, with contracts | In progress | inferred |
| IRPT_DASHBD FWD-10 | Where the data starts and which days are missing | Not started | inferred |
| IRPT_DASHBD FWD-11 | Inflection and Cottonwood on the same page | In progress | inferred |
| IRPT_DASHBD FWD-12 | One 49F advisor's quarter-end reports from Opal | Parked | inferred |
| IRPT_DASHBD FWD-13 | Every 49F and Cottonwood report for Q4 2026 from Opal | Not started | inferred |
| IRPT_DASHBD FWD-14 | Each firm's reports in its own template | Not started | inferred |
| IRPT_DASHBD FWD-15 | Cottonwood history as one record, 2013 to today | Not started | inferred |
| IRPT_DASHBD FWD-16 | Every Opal vs Black Diamond difference explained | Not started | inferred |
| IRPT_DASHBD FWD-17 | Every security valued from Opal's own record | Not started | inferred |
| IRPT_DASHBD FWD-18 | How far each firm is from switching off Black Diamond | Not started | inferred |
| IRPT_DASHBD FWD-19 | Inflection's reports from its Orion data | Not started | inferred |
| IRPT_DASHBD FWD-20 | For every Black Diamond figure, Opal's source | Not started | inferred |
| IRPT_DASHBD FWD-21 | One default performance report for any client | In progress | inferred |
| IRPT_BCKEND FWD-1 | Find a client and open its accounts without waiting | In progress | inferred |
| IRPT_BCKEND FWD-2 | Restricted advisors see only their clients | In progress | inferred |
| IRPT_BCKEND FWD-3 | Opal performance from holdings for Inflection and Cottonwood | In progress | inferred |
| IRPT_BCKEND FWD-4 | YCharts sensitivity analysis in client context | Not started | inferred |
| IRPT_BCKEND FWD-5 | Holdings by model, unassigned assets kept | In progress | inferred |
| IRPT_BCKEND FWD-7 | The client directory cannot go quietly stale | In progress | inferred |
| IRPT_BCKEND FWD-8 | Branded export with market context at big moves | In progress | inferred |
| IRPT_BCKEND FWD-9 | A forwarded holdings email becomes a request | Not started | inferred |
| IRPT_BCKEND FWD-10 | A request only lands in its own firm's storage | Realized | inferred |
| IRPT_BCKEND FWD-11 | One Global view across all firms | Not started | inferred |
| IRPT_BCKEND FWD-12 | Holdings-basis performance gold every trading day | In progress | inferred |
| IRPT_BCKEND FWD-13 | Opal's figure beside the vendor's at set periods | Not started | inferred |
| IRPT_BCKEND FWD-14 | A worse holdings publication is refused | Realized | inferred |
| IRPT_ANLREQ FWD-1 | Form to four attachments on the open ticket, no hands | In progress | inferred |
| IRPT_ANLREQ FWD-2 | The form fits the request and catches bad input | In progress | inferred |
| IRPT_ANLREQ FWD-3 | Commentary drafted from the report, as a branded PDF | In progress | inferred |
| IRPT_ANLREQ FWD-4 | A broken step is never silent | Not started | inferred |
| IRPT_ANLREQ FWD-5 | Another firm never sees the request | Not started | inferred |
| IRPT_ANLREQ FWD-6 | The Analysis tab as the manual path | Not started | inferred |
| IRPT_ANLREQ FWD-7 | Opal data, Yahoo then YCharts per security | In progress | inferred |

## 6. Waiting on Andrew

- The 49 Financial disclosure page (calls `a252` and `90ef`). It is the release gate for client delivery of the default report.
- The client-facing approval for the default performance report (NFRA_DEVPLN per-feature approval).
- Start dates for 40 of 863 Inflection accounts (call `c02c`).
- His own end-to-end test of the analysis request, after run 3.
- Not on the critical path: an S3 delete of 6 synthetic objects (call `2106`), and NFRA_TRNSPT FWD-8 (call `e260`, parked).

## 7. Also noted

- **DSGN_IRPTV1:**
  - all 84 orders are terminal;
  - the last commit is a8de52f8ce (10-12);
  - no seat works it, and the pivot direction recommended parking it.
- **TCKT_VNEXT `~V2`** (Ticket Center trade and meeting requests; P2, Oct 24):
  - the release and run pairs were signed 10-14 ~20:3xZ;
  - no commit since 10-14 20:44Z (about 25 h);
  - outside this brief's P1 scope, and listed so it is not lost.
- **Counts:**
  - IRPT_DASHBD: 298 task orders (292 complete, 3 pending, 3 superseded); 98 open surprise items, 20 ARMED.
  - IRPT_BCKEND: 491 task orders (about 415 complete, 3 pending); 766 commits since 10-13.
  - IRPT_ANLREQ: 196 task orders (193 complete, 2 pending).

## 8. Not read

- **Formal per-FWD grades:** none exist except IRPT_DASHBD FWD-8, so every other state is a reading.
- **The live portal:** no signed-in page walk.
- **The report machine:** the live resident host.
- **Pending detail:**
  - the r32 pair's sign state;
  - whether the portal commentary reader (AR-y-332) is on DEV;
  - the IB-pr-551 hop status;
  - call `a252`'s current state.
- **ARMED surprise rows:** IRPT_BCKEND's open count was not computed.
- **TCKT_VNEXT:** why `~V2` is idle.

-- 4.0.0_SA_CRO~DELL2
