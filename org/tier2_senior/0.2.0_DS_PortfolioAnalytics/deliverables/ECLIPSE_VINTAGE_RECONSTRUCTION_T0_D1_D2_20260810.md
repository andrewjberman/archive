# ECLIPSE VINTAGE RECONSTRUCTION — D1 (T0 verdict) + D2 (feasibility ruling)

**archetype:** DIAGNOSE
**Author:** `0.2.0_DS_PortfolioAnalytics` · 2026-08-10 ~2230Z
**Brief:** `org/tier1_exec/1.0.0_SA_CTO/deliverables/BRIEF_ECLIPSE_VINTAGE_RECONSTRUCTION_20260810.md` @7b76f32562, plus CTO amendment 20260810T220055Z.
**Every value in this document derived from a reconstruction is a DERIVED ESTIMATE and is labelled one. Nothing here is served; serving needs a separate CTO ruling.**

---

## 0 · ANDREW-DIRECT RECORD (verbatim, same-session, ~2210Z at this terminal)

> "You have egress by the way for whatever endpoint you need to call, I will let CTO know this
> fact no need to chatter over mcp about it."

Channel: direct terminal message to `0.2.0_DS_PortfolioAnalytics` mid-session, 2026-08-10.
Scope as I read it: vendor egress for the read-only probes this brief requires, including the
`/v1/auditlog/modelDetail/{id}` call the CTO amendment had HELD pending his word. He said he will
inform CTO himself — recorded here durably per the record law; MCP broadcast deliberately omitted
per his own instruction in the same sentence. All probes below were read-only GETs; zero writes.

---

## 1 · D1 — TIER 0 VERDICT: T0 DOES NOT CLOSE THE PROJECT, TIER 1 IS OPEN AND PROVEN

### T0-a — `/report/allocations` + `/report/trades/reportByAccounts`: EVENT-SHAPED (live-confirmed)

Exercised live (JWT `sm:orion/eclipse_jwt/current`, window 2026-08-05 → 2026-08-06):

- `GET /v1/report/allocations?startDate=2026-08-05&endDate=2026-08-06` → 200, **1 custodian
  element** (`Fidelity_Inflection`), containing trade **blocks** (blockId, action, securitySymbol,
  transactionDate, settleDate) with per-account tradeList (orderQuantity, avgPrice, grossTrade,
  netTrade). **Trade-allocation events. No holdings, no valuations.**
- `GET /v1/report/trades/reportByAccounts?isAllAccount=true&...` → 200, **4 account elements**,
  each with model name + tradeList (action, ticker, price, shares, amount, orderStatus, blockId,
  date). **Security-grain trade events per account. No valuations.**

**Verdict: CONFIRMED event-shaped, exactly as the amendment predicted. T0-a does not close the
project.** (Side value: `reportByAccounts` is a clean security-grain ΔTRADES source — see D2.)

### T0-b — Orion: THE 08-05 VINTAGE EXISTS VENDOR-SIDE, AT CLIENT GRAIN

`s3://opal-data-assets/orion/inflection/silver/` holds 4 tables. Two are true history tables,
re-delivered in full on every pull:

- **`fact_performance`** (pull 2026-08-10): 462,847 rows, **2,268 distinct data-dates 2020-05-26 →
  2026-08-10, per client_id, a cumulative performance factor.** **2026-08-05 IS PRESENT: 313 of 313
  clients**, with real distinct movement (mean daily return 08-04→08-05 = −7.6bp, std 11bp; 08-05→
  08-06 = −20.1bp). The lost date exists here as a genuine vendor-computed vintage.
- **`fact_transactions`** (pull 2026-08-10): 1,407,740 rows, transDate 2020-06-03 → 2026-08-07 —
  a **full dated transaction LEDGER** (ticker, units, navPrice, transAmount, contribution/
  distribution codes). This is a cash-flow ledger, not an event log — it covers the ΔFLOWS term
  the brief rated MEDIUM via audit logs.
- `fact_assets` / `fact_positions`: current-state snapshots, one as-of per partition
  (35,262 rows, 63/64 cols). **Partition `date=2026-08-06` is ABSENT here too** — the same one-day
  hole as Eclipse, which points at a common our-side cause on 08-06 (surfaced §4).

### T0-c — THE SERVED AXIS: 08-05 IS NOT AN INTERIOR HOLE, IT IS THE CURRENT FRONTIER LABEL

`s3://opal-data-portal-v2/platinum/mdpf/inflection/aggregate-aua-timeseries.json` (emitted
2026-08-10 09:50): 439 dates 2024-11-01 → **as_of_last 2026-08-05**, point_class `measured`=433 /
`absent`=6 (the six known unfillable gaps). The "2026-08-05" point = **209,431,383.43**, which
equals the orion `fact_assets date=2026-08-05` custody sum **exactly** — the axis maps
partition-date → axis-date 1:1. `source_vintage_last.status` self-reports BEHIND by 2 trading days.

**Business-impact verdict: there is no rendered interior hole at 08-05 today.** The lost true
vintage manifests as (a) the frontier label question and (b) one missing day in any future
vintage-correct re-keying. An honest named gap remains a viable disposition.

---

## 2 · THE DISCRIMINATING EXPERIMENT — VINTAGE SEMANTICS SETTLED EMPIRICALLY

Per-client partition growth `V(part d)/V(part d−1)` was compared against factor ratios under both
alignment hypotheses (n=290 clients with all days present):

| comparison | median \|diff\| | frac within 10bp |
|---|---|---|
| partition 0804→0805 vs **same-day** factors (08-04→08-05) | 101.1bp | 3.4% |
| partition 0804→0805 vs **T-1** factors (08-03→08-04) | **0.07bp** | **97.9%** |
| partition 0803→0804 vs same-day | 50.5bp | 3.4% |
| partition 0803→0804 vs T-1 | **4.2bp** | **90.3%** |

**⇒ Orion `fact_assets` partition `date=d` carries valuation vintage `d−1`.** The vendor's
`asOfDate` column stamps the FILE date, not the valuation date (it is constant = partition date).
The CTO's run-date + T-1 ruling, established on five instruments for Eclipse, now holds for Orion
on direct measurement. Consequences:

- The missing partition `date=2026-08-06` (both vendors) = missing **vintage 2026-08-05**. Confirms
  the brief's premise independently.
- The served axis point labelled "2026-08-05" carries vintage-08-04 data. **Surfaced as a finding,
  not adjudicated here** (§4).

---

## 3 · D2 — FEASIBILITY RULING: **FEASIBLE at client/firm grain, and the method already ties out**

### The two ΔMARKET sub-questions (brief §3)

1. **Per-security holdings at 08-05?** YES, derivable: holdings at vintage 08-06 are captured
   (eclipse partition 2026-08-07), and security-grain trade deltas for the window are live-proven
   from `/v1/tradeorder/closedTrades` (36 trades in the 08-05→06 window; 133 fields incl. symbol,
   units, price, portfolio id, model id) and `/v1/report/trades/reportByAccounts`, and from the
   orion `fact_transactions` ledger.
2. **An EOD price source for 08-05?** **The question dissolves: the client-grain method needs no
   price vector at all.** Orion's per-client TWR factors at 08-05 encode the market term directly.
   (If a security-grain reconstruction is ever wanted, in-estate prices exist only for traded
   tickers (`navPrice`); Schwab CRS closing prices are a cross-firm price-source option needing its
   own sign-off. Not required for the serving-shaped quantity.)

### Method (client-grain factor roll) — validated

`V_c(vintage d) = V_c(vintage d−1) × f_c(d)/f_c(d−1)`, values from `fact_assets` (re-keyed to true
vintage), factors from `fact_performance`. Flows term from `fact_transactions` where material.

**D4-standard tie-out on a KNOWN day (vintage 2026-08-04, present both sides):** reconstructed
209,432,215.29 vs captured 209,431,383.43 over 312 matched clients (6 unmatched clients carry
$0.00) — **aggregate error 0.04bp.** The method reproduces a known day.

### The lost vintage, reconstructed (DERIVED ESTIMATE — never `measured`)

| direction | estimate (firm aggregate, inflection) | n clients |
|---|---|---|
| forward, from vintage 08-04 | **$209,293,175.65** | 312 |
| backward, from vintage 08-06 (flow-unadjusted) | $208,753,859.52 | 312 |

Agreement: median per-client 6.5bp; aggregate gap $539,316 (25.84bp), substantially explained by
un-adjusted 08-06-window flows (ledger shows −$756,847 merge-outs + −$11,992 mgmt fees + smaller
items on transDate 08-06; the mean per-client diff is dominated by near-zero-value clients where a
relative measure blows up). **The forward estimate is the validated one** (its own tie-out is the
0.04bp above); the backward roll is the cross-check and needs the flow adjustment specified in D3.

Error bound to carry: **single-digit bp at firm aggregate** (tie-out 0.04bp; fwd/bwd agreement
≤26bp unadjusted, expected to close to a few bp with the D3 flow adjustment).

**Provenance label the output must carry:** `point_class: "derived"` (or a CTO-ruled equivalent) +
method + source vintages + error bound. NEVER `measured` (R-21).

### The narrow door (model composition) — LIVE BODY IS RICHER THAN THE SPEC

Authorized by the §0 Andrew-direct word, exercised read-only:
`GET /v1/auditlog/modelDetail/28?fromDate=2026-07-01&toDate=2026-08-10` → 200, **74 change
records**, every one `LEVEL=SECURITYSET` with an attributable **`name`** ("Opal Intermediate" /
"Opal Long Term") + modelName + targetPercent + tolerances + editedOn/editedBy + portfolio lists.
The spec documents 16 fields and no identifier; the live body carries 17 keys including the
identifying `name`. **CTO's blocker (i) is resolved: composition changes ARE attributable** at the
security-set node level (grain caveat: no individual-security rows appeared in this window;
whether SECURITY-level edits log with the same name field is untested until such an edit exists).
`modelDetail/3` returned 0 records for Aug (denominator: a quiet model, not an empty capability).
`/v1/auditlog/portfolio/1` (Aug window) → 0 records — flows via audit log remains thin; the orion
ledger covers that need instead.

---

## 4 · SURPRISES SURFACED (one line each, no action taken — surprise channel per XXX.md)

1. **Served-axis labeling:** the platinum inflection axis maps partition-date → axis-date 1:1, so
   under the now-twice-confirmed T-1 semantics every served date label carries the prior day's
   vintage — CTO to adjudicate whether/where this is re-keyed (it interacts with the MDPF repair,
   which I have not touched).
2. **Common-cause 08-06 outage:** BOTH eclipse and orion `fact_assets` lack partition
   `date=2026-08-06` while orion `fact_performance`/`fact_transactions` (pulled later, full-history)
   cover the date — consistent with the shared puller host/schedule not running on 08-06, not a
   vendor non-publication; owner of that schedule may want the confirmation.
3. **Six known absent points** (05-21, 06-01, 07-01, 07-13, 07-14, 07-15) are honest-`absent` in
   the served artifact; the same factor-roll method could in principle backfill THEM as derived
   points too — scope question for Andrew/CTO, not assumed.

---

## 5 · WHAT REMAINS (D3/D4) — awaiting CTO read on this ruling

- **D3 spec** (if CTO wants it productionized): re-key to true vintage, forward factor-roll with
  ledger flow adjustment, model-level attribution (apply client factors to client×model cells from
  the vintage-08-04 snapshot; model mix shift within one day bounded by the 08-05 closedTrades),
  provenance label schema, and where the derived partition lands (it must NOT be written into
  bronze as if pulled — a derived partition in a raw tier is a 17a violation; a gold/derived home
  needs naming).
- **D4 as a standing gate:** the known-day tie-out above becomes the acceptance test of any
  implementation run (reproduce vintage 08-04 at ≤1bp before emitting vintage 08-05).

## Compiler Tools

| tool | result |
|---|---|
| `comp-find --name pull_eclipse*` / `*eclipse*` | located puller + spec + catalog (denominators printed by tool) |
| raw S3 reads (`aws s3 ls/cp`) | operational data-plane reads of our own buckets (not nudged class); partitions + platinum artifact grounded live |
| `comp-pipescript io` | not run — no gold script was edited this session (investigation only, no code landed) |
