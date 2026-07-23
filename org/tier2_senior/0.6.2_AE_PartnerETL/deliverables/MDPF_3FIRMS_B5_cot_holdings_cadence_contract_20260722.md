# TO 3F-B5 — COT/BD Holdings: Freshness Contract (MEASURED) + Backwards-Extension Evidence — INTERIM

**Agent:** 0.6.2_AE_PartnerETL~A · **Date:** 2026-07-22 ~21:0xZ · **Status:** INTERIM — deliverables (b), (d) +
backwards-extension COMPLETE now; (a) 07-21 landing verify + (c) on-box template dump are
BLOCKED-ON-SCHEDULE until tonight's 02:00–06:00Z window (the TO names this a valid interim state).

## (b) FRESHNESS CONTRACT — measured, not asserted

**Schedules (applied truth, cited verbatim from `aws events describe-rule`):**
- `cot-bd-session-daily`: `ENABLED`, `cron(0 2 * * ? *)`
- `opal-assets-silver-blackdiamond-sweep-daily`: `ENABLED`, `cron(0 5 * * ? *)`

**Measured delivery cadence** (bronze `blackdiamond/cottonwood/bronze/holdings/`, s3api explicit-Z, five
consecutive steady-state deliveries):

```
data date D      landed (UTC)              = ET
2026-07-13   ->  2026-07-15T03:30:25Z   (07-14 23:30 ET)
2026-07-14   ->  2026-07-16T03:30:26Z   (07-15 23:30 ET)
2026-07-15   ->  2026-07-17T03:30:29Z   (07-16 23:30 ET)
2026-07-16   ->  2026-07-18T03:30:27Z   (07-17 23:30 ET)
2026-07-17   ->  2026-07-19T03:30:26Z   (07-18 23:30 ET)
2026-07-20   ->  2026-07-22T03:30:26Z   (07-21 23:30 ET)
```

**THE CONTRACT:** the file for trading day D lands at **(D+1) ~23:30 ET, which is (D+2)T03:30:2xZ in UTC
date terms** (jitter observed: ±4s). The TO's "D+1" phrasing is correct in ET; any UTC-date arithmetic must
use D+2. Consequence for freshness logic: at any instant, the newest holdings partition may legitimately
sit **2 trading days behind the frontier** (e.g., all day Wednesday UTC the newest partition is Monday's
until 03:30Z Thursday delivers Tuesday). Weekend/holiday absences (07-03/04/05, 07-11/12, 07-18/19 in the
window) resolve via the trading calendar — NOT gaps (NEVER#1).

**Conversion cadence, measured:** the daily file converts to monolith silver
`blackdiamond/cottonwood/silver/fact_holdings_s2/date=D/` **event-driven at landing** (07-20 file:
bronze 03:30:26Z -> silver 03:30:34Z, 8 seconds) with the `cron(0 5)` sweep as backstop.

**Proposed comp-freshness entry (NOT wired by me — routed to DS/CTO with the 3F-S3 canonicity decision,
since fact_holdings-vs-fact_holdings_s2 is an OPEN S4 question and the entry should land on the canonical
table):**
```yaml
# blackdiamond/cottonwood monolith holdings leg — measured contract 2026-07-22 (3F-B5)
freshness_basis: trading-day-frontier   # NEVER#1: without this it flat-hours false-alarms every Monday
threshold_trading_days: 2               # D+1-ET / (D+2)T03:30Z-UTC delivery => tdb<=2 is HEALTHY
# fail only at tdb>=3; wall-clock age is NOT a basis for this leg
```

## Backwards-extension (§8.1) — EXERCISED, not just documented

The migration constraint demands the sweep auto-pick-up back-arriving older dates. This has already
happened at scale and worked:

- **27 back-dated files** (2026-06-09..2026-07-10) landed in ONE batch at 2026-07-14T08:07:33-41Z.
- **All 27 have silver partitions**; sampled write stamps show silver date=2026-06-09 and date=2026-07-10
  both written 2026-07-14T19:00-19:01Z — i.e., converted the same day the batch back-arrived, hours after
  landing, with no per-date intervention.
- Denominators: bronze HOLDINGS_DAILY files = **33** (06-09..07-20); silver `fact_holdings_s2` date
  partitions = **33**; set-identical 33/33 both directions.

**Verdict: PASS on §8.1** — back-arriving history converts without intervention (exercised on a 27-file
batch + the event path proven at 8s latency on the daily file). No hardcoded series start found in the
landing/conversion path's observable behavior; the June weekend dates (06-13/14, 06-20/21) present in the
batch also converted, confirming the converter does not filter to a calendar it assumes.

## (d) Vendor-depth statement (under §8.1)

- **Our floor 2026-06-09 is OUR INGEST START, not the vendor floor.** Cottonwood is mid-migration into
  Black Diamond; vendor-side depth is a MOVING TARGET and more history is expected to arrive unprompted
  (the 07-14 batch is the existence proof — 27 dates arrived at once, months after some of their data
  dates). Per Andrew @0b06b5a14: "Cottonwood we don't even have the means to do Backfill at this state,
  all we can do is get aum-metrics and the bell curve distribution from them."
- **NO hardcoded series start, no synthesized rows, no frozen backfill** — the pipeline as measured
  satisfies this (33/33 pass-through, date-agnostic pickup). Any future consumer that pins 06-09 as a
  series origin authors a future contradiction: state "series begins at earliest ingested partition,"
  never a literal.
- Depth today: 33 trading-day... more precisely 33 delivered dates spanning 06-09..07-20 (30 trading days
  + 4 June weekend dates - 06-27/28 weekend absent from the vendor batch — vendor weekend-file generation
  is itself inconsistent, one more reason not to hardcode calendar assumptions on this feed). First
  fact_model_assignment overlap = 07-21, landing tonight.

## Findings (reported, not fixed here)

1. **EC2_MANIFEST.json registration gap (Rule 8):** `cot-exporter` (i-0643a5bee8a8feabf, live service,
   stopped-between-runs lifecycle) is ABSENT from `infra/aws/ec2/EC2_MANIFEST.json` (26 services listed,
   no cot entry). CI/CD parity depends on the manifest; routing to COO/CTO for the registration decision
   (my lane can author the entry on GO).
2. **On-box dump is window-bound:** cot-exporter has NO EIP and is started by `cot-bd-session-trigger`
   (ec2.tf:36 "stopped between runs"); the BD session jar is IP-bound per-window. An off-window start
   would present a new IP against last night's session -> manufactured 401, and freelancing the session
   Lambda off-schedule is vendor-auth surface I won't touch without word. **(c) executes inside tonight's
   02:00Z+ window** alongside the (a) landing verify.
3. `_complete/` sentinels exist only from 2026-06-23 onward — the earlier batch dates carry no sentinel;
   consumers must not treat sentinel-absence on <=06-22 dates as incomplete delivery.

## ~~Pending~~ RESOLVED (2026-07-23 window) — TO COMPLETE

- (a) **VERIFIED**: `HOLDINGS_DAILY_2026-07-21.xlsx` landed **2026-07-23T03:30:28Z** (1,153,402B) — the
  measured (D+2)T03:30:2xZ contract held at ±4s precision — and converted event-path in **7 seconds**
  (`fact_holdings_s2/date=2026-07-21/` stamped 03:30:35Z; `fact_holdings/date=2026-07-21/` present).
  Well inside the 06:00Z acceptance deadline.
- (c) **EXECUTED 02:05-02:07Z** (first-ever run, clean): auth probe OK, 4/5 templates dumped to
  `templates_enriched/` (qt1 15 dims/4 measures — enumerated + routed to CRO, closed his A2; qt4 208
  dims; **qt3 realized = selectable-but-unpersisted, no templateId — finding**). Full output in the
  02:00Z window report (COO 021405Z accepted).
- Phase-3 re-list: bronze HOLDINGS files **34** == silver `fact_holdings_s2` partitions **34**,
  set-identical both directions.
