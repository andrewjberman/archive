# MDPF_CANON round 4 -- the fold cell's AC1 and AC3 against two rules the code cites (2.0.0_SA_COO~D1, 2026-10-11 ~05:5xZ)

Input: `ledger/ROUND_ANALYSIS.round3.md` @ae094ea51d section 3 item 2 (AC1 W8-S2, AC2 W8-S3, AC3 W8-S4) and section 2 (W8-S4 ruling).
AC2 is cut as ruled. AC1 and AC3 each reverse a behaviour the producer's own comments cite as ruled. Read at HEAD (`git show`/Read of
the committed file, 2026-10-11 ~05:5xZ); nothing here was run.

## AC1 (no by_model entry with a nonzero count that no firm holds at the date)

- The two entries are exactly `SMA_COUNT_PRESERVE_KEYS = ("opal_growth_sma", "opal_div_sma")`
  (`data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py:1679`).
- The comment above it (:1667-1678) cites "CTO ruling 20260723T051427Z (SMA frontier seam, shape (i)-EXTENDED; FLAG-2 co-sign
  extension)": when the frontier advances with the SMA value and the count source cannot supply a frontier count, "the last known count
  CARRIES FORWARD, wearing its own in-band `count_as_of` (a lagged number wearing its date is honest; implied-current is the B7 class)".
  The preserve is enumerated to exactly these two keys.
- The code that does it: :2621-2630 (`entry["count_as_of"] = preserved_from`).
- CN-c-1's basis measures the same fact: global count at 2026-10-08 equals its 2026-07-17 value, which equals 49financial's
  2026-07-17 value (`X2_GLOBAL_BASIS.md`, Method, zero-firm entries). The entry wears its date; the basis counted it as held by zero firms.
- AC1 as ruled makes those counts None at every date no firm holds them. That removes the figure FLAG-2 was made to keep.

## AC3 (global account-distribution composes each firm leg at its own key date, or refuses)

- `build_firm_distribution("global")` folds cottonwood from a sidecar (`data/mdpf/scripts/gold/dim_mdpf_account_distribution.py:439-444`).
- `_cottonwood_sidecar` (:335-420) already refuses a sidecar whose `value_date` is older than cottonwood's roster-declared window in trading
  days ("CTO ruling 20260805T173510Z"; "the window is read from the roster, never hardcoded"; a wider window is forbidden).
  Inside the window the sidecar is folded.
- The CVO's reading of W8-S4 (`ADJUDICATION_v3`): the global object keyed 2026-10-08 carries cottonwood's 2026-10-07-keyed units, 7 of 7.
  That is one trading day. The build would have refused outside the declared window, so the object existing at all is the evidence that the
  existing rule accepted it (the window's value was not read here).
- `meta.cottonwood_fold` (:481-488) names the fold and its source key; it carries no `value_date`, so the lag is not stated in-band.
- Cottonwood's declared cadence is slower than the global frontier ("declared cadence (D+2) is SLOWER than the global frontier",
  `dim_mdpf_aggregate_aua_timeseries.py:2291-2293`). A refusal whenever the leg is not at D would refuse the global object on most days
  and serve the prior as-of. The aggregate series carries the opposite ruling for the same leg: "Just roll Cottonwood forward if we don't
  have data for it, take the last good figure" (:2324-2326, via 1.0.0_SA_CTO~Z 033107Z).

## Two ways to cut it

- **A (recommended): keep both rules and make the lag visible.**
  - AC3: add the sidecar's `value_date` (and its age in trading days) to `meta.cottonwood_fold`, so the object names the vintage of the leg
    it folded. No served value moves; a key is added under `meta`.
  - AC1: no fold change. The entries already wear `count_as_of`. The basis's min-firms rule is stated to count a labelled carry as a carry.
- **B: reverse both as ruled.** Counts go None where no firm holds them and the global account-distribution refuses on a lagging leg. This
  moves served output on most days (never-widen pair) and reverses two rulings that cite Andrew's word, so it wants his answer first.

AC2 (the additive identity stated and asserted after the folds) is independent of both and is cut now.
