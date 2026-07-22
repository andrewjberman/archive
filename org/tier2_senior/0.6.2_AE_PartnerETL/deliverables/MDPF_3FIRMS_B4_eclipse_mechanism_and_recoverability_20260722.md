# TO 3F-B4 (AMENDED @1c42b3fd9) — INF/Eclipse: Mechanism Named + Recoverability Verdict

**Agent:** 0.6.2_AE_PartnerETL~A · **Date:** 2026-07-22 ~21:3xZ · **Struck deliverable honored:** zero
probes spent on pre-05-15 depth (Andrew @0b06b5a14: models began 2026-05-15; the floor is CORRECT).
**⛔ Compliance:** zero use of the eclipse puller `--date` for any purpose in this TO.

## (a) THE MECHANISM, NAMED — and why every rules census "missed" it

**The eclipse puller is not an EventBridge target at all.** `pull_eclipse_portfolios.py` runs as the
**ECLIPSE-BLOCK** — a best-effort, post-sentinel chain segment inside the INF gold dispatch:
`data/inf/scripts/gold/orion-gold-dispatch.sh:307` (step `INF_ECLIPSE_PULL|pull_eclipse_portfolios.py|--date {date}`),
`:482` (`CHAIN_ECLIPSE="INF_ECLIPSE_PULL INF_ECLIPSE_SILVER INF_E_00"`), `:2003` (execution loop) @HEAD.
The daily cycle roots at EventBridge `opal-inf-bronze-runner-cron` — `ENABLED`, `cron(30 13 * * ? *)`,
target `arn:aws:lambda:us-east-1:313476888478:function:inf-bronze-trigger`, LIVE fired-evidence 7x in the
trailing window (comp-trigger) — through the bronze->silver->gold event chain to the gold runner, whose
dispatch tail fires the eclipse pull (~14:5xZ landings corroborate: bronze `pull_complete.json` 07-22 at
14:54:49Z). Monolith silver conversion: `opal-assets-silver-eclipse-sweep-daily` `ENABLED`
`cron(0 16 * * ? *)` -> Lambda `opal-assets-silver-eclipse` (OnFailure DLQ `opal-assets-silver-dlq`).

**Census RE-DERIVED (per CTO 204330Z — PRD §9 not inherited), all three surfaces, denominators:**
- (a) `events list-rules`, fully paginated: **29 matched of 141 TOTAL rules** (patterns inf|eclipse|orion;
  full match list in evidence). No eclipse-named PULLER rule exists — the two eclipse-named objects are
  the silver sweep + nothing else, which is CORRECT given the mechanism above.
- (b) `scheduler list-schedules`: **0 matched of 10 TOTAL schedules**.
- (c) `lambda get-function-event-invoke-config` on candidates: `inf-bronze-trigger` = none,
  `inf-gold-trigger` = none, `opal-assets-silver-eclipse` = OnFailure->`opal-assets-silver-dlq` only.
- comp-trigger corroboration (its own denominator: 141 rules + 10 schedules scanned).
- Partition censuses derived from FULL KEY LISTINGS throughout — the `--delimiter` shim trap avoided.

**Freshness contract implied by the mechanism (measured):** eclipse bronze for day D lands ~14:54Z on D;
monolith silver `date=D` materializes at **(D+1)~03:30Z** on the current cadence (measured: date=2026-07-21
written 2026-07-22T03:30:30Z; bronze 07-22 landed 14:54Z and is correctly still unconverted at 21:2xZ —
today's 16:00Z sweep did not convert same-day). ⚠ Residual (small): the 16:00Z sweep's date scope vs the
03:30Z pass doing the effective conversion is not source-determined here — the EMPIRICAL cadence is stated;
wiring a freshness entry should use (D+1)03:30Z i.e. tdb<=2, same shape as the COT contract.

## (b) RECOVERABILITY VERDICT — six gap dates, two surfaces, one answer each

Gap set (silver census re-derived: **54 partitions, floor=2026-05-15 ✓, frontier=2026-07-21; trading
census 05-15..07-22: 39 of 46 present**): missing = 05-21 (DS S2's new find, confirmed), 06-01, 07-01,
07-13, 07-14, 07-15 (+ 07-22 which is CADENCE-PENDING, not a gap — lands ~03:30Z 07-23).

**VERDICT: FULL SNAPSHOTS NOT RECOVERABLE — ASSIGNMENT DELTAS RECOVERABLE — VALUATIONS DERIVABLE.**

1. **Full point-in-time snapshots (what `fact_portfolios_full` holds): NOT RECOVERABLE, on vendor-side
   evidence with a control that could have failed, re-exercised TODAY.** `GET /v1/portfolio/portfolios`
   with 8 candidate date params (`asOfDate, asOf, date, effectiveDate, asofdate, snapshotDate,
   valuationDate, fromDate`) = 2026-07-09 — a date whose true book is KNOWN different from today's (65
   IWM->Opal flips on 07-10, source: the B7 zero-residual decomposition) — returned HTTP 200,
   **byte-identical sha256 to the un-parameterized call, 8/8**. A date-honoring surface MUST have
   differed; the control proves the probe could have detected one. The surface is CURRENT-ONLY. (Not
   concluded from the puller's shape — concluded from the vendor's wire behavior.)
2. **Assignment-change deltas: RECOVERABLE.** `/v1/auditlog/portfolio/{id}?fromDate&toDate` is DATED and
   works. Census of the gap dates (848/848 portfolios swept each, 0 residual errors after retries;
   positive control: the 07-10 sweep finds the migration cluster — 66 changed vs the banked 67, one-off
   delta noted, the cluster unambiguous):
   | gap date | portfolios with audit entries |
   |---|---|
   | 2026-05-21 | 2 (pids 1349, 1372) — NEW, this TO |
   | 2026-06-01 | 0 |
   | 2026-07-01 | 2 |
   | 2026-07-13 | 14 |
   | 2026-07-14 | 1 |
   | 2026-07-15 | 7 |
   The audit log carries ZERO value fields (grounded in the prior session; unchanged).
3. **Valuations: DERIVABLE from Orion holdings** (orion bronze is COMPLETE across all six dates incl. the
   07-11..15 repair) — a reconstruction is a **silver/gold artifact WITH provenance**, never a
   `bronze/eclipse/` key (the architectural line held from the prior session).

**D-3 hand-off to COO for Andrew (per acceptance 6):** the permanently-absent-as-bronze list is
{05-21, 06-01, 07-01, 07-13, 07-14, 07-15}. Recommendation: **honest gaps + a methodology note** at
bronze; OPTIONALLY the costed silver/gold reconstruction (carry-forward + audit deltas + Orion-derived
valuations — total assignment churn across all six dates is 26 portfolio-days, small) if Andrew wants the
axis visually complete. NEVER interpolation, NEVER a bronze write, and Eclipse-computed analytics
(`percentDeviations` etc.) are not faithfully reproducible — any reconstruction must state that.

## Escalation triggers checked

- No gap silently filled (census re-derived at HEAD state).
- The vendor does NOT hold temporal portfolio data (probe above) — the leg does not change.
- Nothing new touches Andrew's 07-06/07-07/07-10 window (that carrier, 3F-B7, is CLOSED —
  CVO-verified @6bb15dbcb).

## Evidence inventory

comp-which -> comp-trigger (routed; denominator 141+10); 3-surface census (boto3, paginated, denominators
above); probe + audit sweep scripts in session scratchpad (`b4_asof_probe.py`, `b4_audit_sweep_0521.py` —
read-only vendor GETs under the standing ORION egress lift + this TO's mandate); silver census via full key
listing; `git show`-verified line cites @HEAD for the dispatch chain.
