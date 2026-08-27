# RIDER 1 — MATERIALITY PRINT (RPS-1) — ADVI_49F.RPS-CUSTODY

**Seat:** `0.4.0_DS_ClientPlatform` (producer-owner, WS-E)
**Issued by:** `2.0.0_SA_COO` (GO 76140, 2026-08-27T16:13:40Z)
**Measured:** 2026-08-27T16:0x-16:4xZ
**Status:** RPS-1 PRINTED. **NO REPOINT MADE** — RIDER 1 forbids it before this number exists, and
this print changes what the repoint should target (see FINDING B).

---

## VERDICT IN ONE LINE

**DELTA IS LARGE — the caveat branch fires.** The client-facing `non_model_aua` served for
2026-08-26 is understated by **+$91,476,329.17 (+63.07%)**, and the TO's named successor is the
**wrong Schwab account** — repointing to it as written would have moved the figure **+103.14%** and
silently swapped the account population.

---

## 1. THE PRINT — `partner_custody_total`, legacy vs successor, BOTH DENOMINATORS

Computed by replicating `compute_partner_custody_total_schwab()`
(`data/mdpf/scripts/gold/build_mdpf_wse_49f_non_model_aua.py:564` @ HEAD `fb79e6a4cd`) exactly:
`sum(market_value)` over the partition, excluding literal-cash rows (`ticker.strip().upper() == "CASH"`).

| # | Source | Partition | `partner_custody_total` | rows read | positions summed | distinct accounts |
|---|---|---|---|---|---|---|
| **1** | **LEGACY** `s3://opal-data-bd/schwab/silver/rps/` — **the live WS-E basis** | `date=20260723` | **$1,641,269,345.33** | 93,126 | 93,125 | **6,005** |
| **2** | **SUCCESSOR 08242234** `s3://opal-data-assets/schwab/08242234/silver/fact_rps/` | `date=2026-08-26` | **$1,732,745,674.50** | 101,080 | 101,079 | **6,148** |
| 3 | SUCCESSOR 08335338 (**the TO-named one**) `s3://opal-data-assets/schwab/08335338/silver/fact_rps/` | `date=2026-08-26` | $1,790,858,012.07 | 103,203 | 103,202 | 6,174 |
| C1 | CONTROL — SUCCESSOR 08242234 at the **legacy vintage** | `date=2026-07-23` | **$1,641,269,345.33** | 93,131 | 93,130 | **6,005** |
| C2 | CONTROL — SUCCESSOR 08335338 at the **legacy vintage** | `date=2026-07-23` | $1,696,352,525.05 | 94,637 | 94,636 | 6,031 |

Literal-cash excluded per the WS-E rule: 1 row in every partition ($16,687.63 at the 07-23 vintage;
$16,460.76 at 08-26).

**Rows 1 and 2 are the side-by-side RIDER 1 asked for. Rows C1/C2 are the control that makes the
delta interpretable** — without a fixed-vintage arm, a single legacy-vs-successor number conflates
*staleness* with *population*, and here it would have hidden a wrong-account repoint completely.

---

## 2. FINDING A — THE STALENESS, RE-READ (not carried forward from 08-19)

- Legacy newest partition: **`date=20260723`**, **634** materialised partitions — **unchanged since
  the 08-19 measurement.** The prefix has not advanced.
- **25 trading days behind** the expected frontier (`lib/trading_calendar.py`:
  `expected_last_trading_day(2026-08-27)` = `2026-08-27`, `trading_days_behind` = **25**).
  The TO's "27 days" was 08-19 **calendar** days; this is the current **trading-day** re-read
  (NEVER#1 — the trading calendar is resolved before any staleness claim).
- Both successors are **current**: newest `date=2026-08-26` (T-1, correct for a T-1 pipeline).
- **The basis flag is live:** SSM `/mdpf/custody_source` = **`schwab`** (read 2026-08-27). WS-E is
  reading the stale legacy prefix **today**.

### The compounding — this is why it is worse than a stale number

`non_model_aua = partner_custody_total − model_aua_input − sma_aua_input`. The minuend is **frozen**;
the subtrahend **advances daily**. The residual absorbs 100% of the divergence.

Measured across the **18 most-recent served partitions** (of 65 total) in
`s3://opal-data-mdpf/mdpf/feeds/non_model_aua/49financial/`:

| | 2026-08-05 | 2026-08-26 | move |
|---|---|---|---|
| `partner_custody_total` | 1,641,269,345.33 | 1,641,269,345.33 | **+0.00 — bit-identical, 18/18 partitions** |
| `model_aua_input` | 1,440,437,783.16 | 1,473,258,520.42 | +32,820,737.26 |
| `non_model_aua` (**served, client-facing**) | 177,958,391.99 | **145,028,157.87** | **−32,930,234.12** |

Served `non_model_aua` is drifting **−$1,937,073/day**. The runtime fail-closed band is
`SCHWAB_NON_MODEL_SANE = (50M, 500M)`; at that rate the served figure reaches the **$50M floor in
~49 days**, at which point WS-E fails closed and stops publishing. **The band is far too wide to
catch this** — and the figure has *already* drifted below the design's own stated observed range
(~$180M–$203M, `build_mdpf_wse_49f_non_model_aua.py:166`) without any alarm.

**Discriminating check (Rule 22 DISCRIMINATION):** the served 2026-08-26 row reproduces **to the
cent** from the July-23 legacy partition —
`1,641,269,345.33 − 1,473,258,520.42 − 22,982,667.04 = 145,028,157.87`, which is exactly the served
`non_model_aua`. If the served basis were anything other than the July-23 partition, this identity
would not close. The staleness is confirmed at the **APPLIED/served** layer, not inferred from the
producer's source.

---

## 3. FINDING B — ⛔ THE TO NAMES THE WRONG SUCCESSOR ACCOUNT

**The TO face and the COO GO both name `opal-data-assets/schwab/08335338/silver/fact_rps/`.
Measurement says the correct successor is `08242234`.**

At a **held-constant vintage** (`date=2026-07-23`), against the legacy partition:

| Comparison | `partner_custody_total` | accounts | ∩ legacy | legacy-only | successor-only |
|---|---|---|---|---|---|
| legacy vs **08242234** | **identical to the cent** ($1,641,269,345.33) | 6,005 vs **6,005** | **6,005** | **0** | **0** |
| legacy vs 08335338 | +$55,083,179.72 (+3.36%) | 6,005 vs 6,031 | 5,993 | **12** | **38** |

- `08242234` = master account **`0008242234` "49 WEALTH MANAGEMENT LLC"** — reproduces the legacy
  book **exactly**: same value to the cent, same 6,005 accounts, **zero** accounts on either side of
  the difference.
- `08335338` = master account **`0008335338` "49 FINANCIAL"** — a **different book**: 12 legacy
  accounts absent, 38 accounts the legacy book never had. It is **not a superset** either.

Three carriers agree, and the measurement is the decisive one:
1. **Measured** (above) — cent-identical at fixed vintage, zero-symmetric-difference account sets.
2. WS-E's own docstring: *"the RPS delivery IS 49F's Schwab-custodied book (account 08242234)"*
   (`build_mdpf_wse_49f_non_model_aua.py:569-571`).
3. The standing account distinction: `08242234` = MDPF Model Portfolios; `08335338` = ADVI Advisor
   Intelligence. **WS-E is an MDPF producer** (`data/mdpf/scripts/gold/`).

**Had the repoint been executed as written**, `non_model_aua` would have moved **+$149,588,666.74
(+103.14%)** — of which only ~$91.5M is the staleness correction and **~$58.1M is a silent
population swap into a different account's book.** This is precisely the "repoint that silently
moves a client-facing figure by an unknown amount" RIDER 1 exists to prevent.

---

## 4. FINDING C — THE REPOINT IS NOT A PATH SWAP; THE SCHEMA DIFFERS

The successor is a different table family and **does not carry the columns WS-E reads**:

| WS-E reads (legacy) | Successor `fact_rps` | |
|---|---|---|
| `market_value` | **absent** → `market_value_settled_unsettled` | must be mapped |
| `ticker` | **absent** → `ticker_symbol` | must be mapped |
| `account_id` | `account_id` | present |
| partition `date=YYYYMMDD` | partition **`date=YYYY-MM-DD`** | `_latest_rps_partition()` regex `date=(\d{8})/` **matches nothing** on the successor |

The successor carries 57 columns vs the legacy 11. A path-only repoint fails: `_latest_rps_partition()`
would raise `no date= partitions`, and the column reads would `KeyError`. **RIDER 2 is a code change
with a column contract, not a constant edit** — and it needs its own equivalence check (the C1
control above is exactly that check at one vintage, and it passes to the cent).

> Instrument note, banked: my first partition sweep returned **0 partitions** for both successors
> because I matched `date=[0-9]{8}` against a hyphenated `date=YYYY-MM-DD` key. **A format-mismatched
> grep returns a zero byte-identical to a real absence.** I caught it only by re-reading the raw
> listing instead of trusting the count. `fact_rps` object counts: 08335338 = 538, 08242234 = 566.

---

## 5. RPS-2 — CAVEAT DECISION (stated)

**A CAVEAT IS REQUIRED.** The delta is large by any reading: **+63.07%** on the served client-facing
figure, **$91.5M** absolute, on a number that is drifting a further **−$1.94M/day** and is already
outside its own design-stated observed range.

**Wherever `non_model_aua` for 49financial is quoted — any as_of date from 2026-07-24 onward — it
must carry:** *"Non-model AUA is computed against a custody snapshot frozen at 2026-07-23; the figure
is understated by approximately $91M (+63%) as at 2026-08-26 and the understatement grows ~$1.9M per
day until the custody basis is repointed."*

Scope of the caveat: **23 served partitions** carry a July-23 custody basis (every partition from
2026-07-24 through 2026-08-26 — the frozen value is bit-identical across all 18 I read, and the
prefix has not advanced since 07-23). This is a **stated caveat on a live figure, not a correction**
— no served artifact is being rewritten by this print.

---

## 6. WHAT I AM NOT DOING, AND WHY

- **No repoint.** RIDER 1 sequences the print first; and FINDING B changes the target, so executing
  the repoint as written would have been wrong independent of sequencing. **The repoint target needs
  COO's word before RPS-3** (the TO names 08335338; measurement says 08242234).
- **No touch to the false Rule-25 dormancy marker.** COO's GO scopes the marker-census re-run to the
  COO lane. I did not modify the marker. **It is now doubly load-bearing:** it declares "no live
  reader after 2026-08-18" over a prefix I have just measured as the live basis of a client-facing
  figure serving **today**.
- **No alarm/monitor built** (standing moratorium). The −$1.94M/day drift and the ~49-day fail-closed
  runway are stated here as findings, not wired to anything.

---

## 7. EVIDENCE — instruments and vintages

| Claim | Instrument | Vintage |
|---|---|---|
| WS-E custody rule replicated | `build_mdpf_wse_49f_non_model_aua.py:564-596` read at source | HEAD `fb79e6a4cd` |
| legacy partition set (634, newest 20260723) | `s3api list-objects-v2`, client-side unique count | 2026-08-27T16:1xZ |
| successor partitions + newest 2026-08-26 | `s3api list-objects-v2`, re-read raw after the regex miss | 2026-08-27T16:2xZ |
| all `partner_custody_total` figures | `boto3.get_object` → `pandas.read_parquet`, WS-E rule applied | 2026-08-27T16:3xZ |
| account-set overlap | set arithmetic on `account_id`, zero-padding normalised | 2026-08-27T16:3xZ |
| served figures + drift | `s3://opal-data-mdpf/mdpf/feeds/non_model_aua/49financial/`, 18 of 65 partitions | 2026-08-27T16:4xZ |
| basis flag is live | `ssm get-parameter /mdpf/custody_source` → `schwab` | 2026-08-27T16:3xZ |
| staleness in trading days | `lib/trading_calendar.py` `trading_days_behind` | 2026-08-27 |

**Grain:** every dollar figure is a partition-level sum over the named key, not a reported or
recalled value. **Coverage:** denominators printed beside every number (rows read, positions summed,
accounts, partitions swept, partitions read of total). **State:** the served-artifact reads are the
APPLIED layer — the stored parquet WS-E actually published, not the producer's self-report.

**Not claimed:** I have not measured whether any downstream consumer (portal, WS-A aggregation)
re-derives or caches `non_model_aua` independently — the caveat scope above is stated over the WS-E
feeder partitions I read, not over every surface that may quote the figure.


---

## 8. FINDING B HARDENED — MULTI-VINTAGE EQUIVALENCE (added 2026-08-27T16:5xZ)

Section 3 rested on **one** vintage. A single-date cent-match is exactly the kind of evidence that can
be a coincidence of one day's book, so I widened the denominator before letting the blocking claim
stand.

**Population:** 514 vintages common to all three prefixes (legacy 634, 08242234 566, 08335338 538),
spanning **2024-07-08 .. 2026-07-23**. **Sample: 10 of 514, every 57th** — spread across the full
two-year overlap, not clustered.

| vintage | LEGACY | 08242234 | delta | 08335338 | delta |
|---|---|---|---|---|---|
| 2024-07-08 | 659,361,846.17 | 659,361,846.17 | **0.00** | 662,351,391.98 | +2,989,545.81 |
| 2024-09-26 | 737,355,351.44 | 737,355,351.44 | **0.00** | 743,286,601.14 | +5,931,249.70 |
| 2024-12-17 | 811,845,500.61 | 811,845,500.61 | **0.00** | 819,438,639.42 | +7,593,138.81 |
| 2025-03-12 | 926,913,910.22 | 926,913,910.22 | **0.00** | 927,412,843.76 | +498,933.54 |
| 2025-06-03 | 1,017,468,019.21 | 1,017,468,019.21 | **0.00** | 1,026,805,981.40 | +9,337,962.19 |
| 2025-08-25 | 1,111,679,055.18 | 1,111,679,055.18 | **0.00** | 1,120,692,539.24 | +9,013,484.06 |
| 2025-11-13 | 1,256,721,892.00 | 1,256,721,892.00 | **0.00** | 1,268,056,804.09 | +11,334,912.09 |
| 2026-02-06 | 1,425,183,755.61 | 1,425,183,755.61 | **0.00** | 1,448,053,487.44 | +22,869,731.83 |
| 2026-04-30 | 1,553,684,292.84 | 1,553,684,292.84 | **0.00** | 1,601,119,110.42 | +47,434,817.58 |
| 2026-07-23 | 1,641,269,345.33 | 1,641,269,345.33 | **0.00** | 1,696,352,525.05 | +55,083,179.72 |

**Exact match to the cent vs legacy: `08242234` = 10/10. `08335338` = 0/10.**

Two things this adds that the single-vintage arm could not:

1. **The match is not a coincidence of one book-date.** Ten independent vintages over two years, every
   one exact to the cent, across a book that tripled in size (659M -> 1.64B). A wrong-account
   hypothesis cannot survive that.
2. **The 08335338 divergence is not noise — it GROWS**, roughly 3.0M (2024-07) -> 55.1M (2026-07).
   That is the signature of a genuinely different and differently-growing book, not a reconciliation
   gap or a rounding artifact. **Both arms of the control can fail and only one does** — the negative
   arm (08335338) diverges on every single sampled date, which is what makes the positive arm's
   10/10 informative rather than vacuous.

**This is also the equivalence check FINDING C says the repoint owes**, executed at 10 vintages
instead of one: on the correct account, `sum(market_value_settled_unsettled)` over `fact_rps` with
`ticker_symbol` cash-exclusion reproduces the legacy `sum(market_value)` over `rps` with `ticker`
cash-exclusion **exactly**, at every date tested. The column mapping in FINDING C is therefore
value-preserving, and the repoint's only remaining semantic question is the account — which is
FINDING B, held on COO's word.
