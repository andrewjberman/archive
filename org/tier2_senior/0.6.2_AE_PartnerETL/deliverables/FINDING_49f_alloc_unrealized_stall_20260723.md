# FINDING — 49F BD allocations+unrealized point-in-time snapshot stall (source-side)

**Opened:** 2026-07-23T17:2xZ
**By:** 0.6.2_AE_PartnerETL~A (executed-for-0.6.0, CTO custody reassignment 164127Z)
**Class:** vendor source-side data gap → correct-guards-produce-a-frozen-served-value
**Routing:** CTO + COO. Feeds Andrew's open BD-vendor-question package (COO routing). Vendor contact GATED on Andrew's word.
**Not a deploy ledger** (CTO L6 disposition 172430Z: "the NEW freeze = a NEW thread, not L6's"). The bd-49f-empty-stub-asof-lag-root-fix ledger is CLOSED (deploy goal verified met).
**Grounding:** read-only; no re-run, no fix. All evidence = live/served state + source `file:line`.

---

## What

The client-facing 49F firm AUA served on `s3://opal-data-bd/platinum/firm/header_metrics.json` (`total.aua`) is **frozen at 1,879,986,733.13** across 9 consecutive object writes / 3 distinct vintages (07-17, 07-20, 07-21) since 2026-07-19T01:43:12Z. This value is the **2026-07-17 cert**.

This is a **DIFFERENT** freeze from the one the closed ledger fixed. The original frozen figure (1,837,159,865.68) **did clear** — served AUA advanced 1,837.16mm → 1,844.02mm → 1,857.83mm → 1,879.99mm. The deploy worked. This new freeze sits underneath it.

## Mechanism (source-confirmed + exercised — every guard is behaving correctly; do NOT "fix" C_02/D_00)

1. **Cert census** (`gold/aua_certification/`, key-sorted, 73 partitions): newest = `2026-07-17.json` (`certified_aua=1,879,986,733.13`, written 07-21T23:39:45Z). **No cert exists for any data-date after 07-17.**
2. **Why no cert:** `data/black_diamond/scripts/gold/C_02.client_performance.py:309-332` reads `silver/allocations/{date}.parquet`, sums `account_market_value` → `certified_aua`; if `<=0` it **SKIPs** (BRANCH-A floor — refuses a degenerate cert).
3. **silver/allocations census:** newest REAL partition = `2026-07-17.parquet` (1.22 MB, 07-19T00:31Z). Every date after 07-17 is absent or a 46,277-byte empty stub → `certified_aua<=0` → C_02 skips.
4. **Runner IS firing daily** (`bd-49f-runner` CW streams present every day 07-16..07-23; it fires on `bd-49f-session-complete`, the `bd-49f-runner-daily` cron being DISABLED is an intentional documented supersession). **Exercised proof** (07-23 + 07-21 streams): `REJECT: allocations @2026-07-22 export has 0 DATA ROWS (4557 bytes, header-only) -- BD has no point-in-time snapshot for this as-of date; NOT landing`. Same for `unrealized`. `RESULT: rejected=['allocations','unrealized'], landed=['transactions','realized']`. **The deploy's own empty-stub guard (L4) is working exactly as designed — it is the reason no stub lands.**
5. `data/black_diamond/scripts/gold/D_00.portal_aggregates.py:257-286` `_resolve_served_aua` → `_last_good_certified_aua(lookback_days=14)`: today's cert degenerate/absent → **HOLD last-good cert** (07-17's value). `DEGENERATE_CERT_MODE` default `'hold'`.

**ROOT:** BD is not delivering point-in-time **allocations + unrealized** snapshots for as-of dates after 2026-07-17 (source-side — 0-DATA-ROW exports, not a lag bug; `BD_SNAPSHOT_ASOF_LAG_BDAYS=1` is live and correct). The freeze is what CORRECT guards produce on a stub feed (`served-value-freeze-check.py` doctrine).

**Trading-calendar framing (NEVER#1):** `expected_last_trading_day(2026-07-23) = 2026-07-23 (Thu)`. Cert data-date 07-17 = **4 trading days** behind frontier — a REAL feed staleness, NOT a weekend artifact (07-20/21/22/23 are all trading days with 0-row exports). Transactions + realized DO advance (served `data_as_of=07-21`, 2 trading days behind); only the AUA-bearing allocations/unrealized feed is stalled.

## Cross-firm pattern (CTO-named, 172430Z)

**Same class as the COTTONWOOD BD feed** (`opal-data-cot`): allocations+unrealized stall while holdings advance (cot 07-08 freeze, partially cured 07-22 per `project_cot_snapshot_zero_row_freeze_20260709.md`). **Two firms, one vendor (Black Diamond), one gap class.** This is the pattern that belongs in the BD-vendor-question package.

## Forward risk — the 2026-08-01 silent cliff (computed)

`_last_good_certified_aua` uses `lookback_days=14` (`range(0,15)`). The 07-17 cert falls out of the 14-day window when today ≥ **2026-08-01** (today=07-31 → oldest probed 07-17, IN; today=08-01 → oldest 07-18, 07-17 OUT). At that point `_resolve_served_aua` floors to the GOLD fallback (`gold_aua`). 07-17 `gold_aua` = 1,780,856,838.03 vs certified 1,879,986,733.13 → a **silent −99.1 mm / −5.27% basis flip** on the client-facing firm AUA on 2026-08-01, with no signal (freeze-check watches value-CONSTANT not a drop; object-age stays GREEN).

## Disposition (CTO ruling 172430Z)

- **Cliff fix ruled in principle, built AFTER tonight (8d runway), at CTO gate:** D_00's degenerate-path fallback becomes **HOLD-last-good-with-a-VISIBLE-HELD-FLAG**, not a silent gold-floor (frozen-beats-unheld law applied at the fallback). Visibility rides **IN THE ARTIFACT** (`held_since` + `cert_data_as_of` + `hold_reason` beside `total.aua`) per Andrew's no-alarms standing word — NOT a new alarm/sentinel. Scheduled freeze-check as a cron was **declined** (alarm shape); the instrument stays available by hand.
- **Upstream (the real fix):** establish with BD/source whether allocations+unrealized after 07-17 is a genuine source gap or an as-of parameterization issue. Vendor contact gated on Andrew.
- **Nothing implemented tonight** — MDPF completion owns the evening.
