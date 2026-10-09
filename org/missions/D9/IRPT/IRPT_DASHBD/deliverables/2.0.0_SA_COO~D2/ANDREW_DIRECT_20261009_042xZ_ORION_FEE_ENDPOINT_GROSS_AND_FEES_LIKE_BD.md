# ANDREW-DIRECT 2026-10-09 ~04:2xZ -- Orion's fee endpoint: gross and fees for Inflection, sliced as Black Diamond is

**Received by:** `2.0.0_SA_COO~D2`, in its own terminal (dell2)

**Verbatim:**

> "We need to figure out Orion's fee endpoint. All of these advisor data vendors have slicing for advised/supervised or
> non-advised/unsupervised or total, as well as billed unbilled and total. Black Diamond does it that way and I know Orion does too, so
> its important to make sure that we are getting gross and fees for them, just like how we manage it for Black Diamond"

**What it changes.** Round 36's Inflection cell (TO-DB-b-72, drained @9e6b077faa) tied out against Orion's own TWR, read as
*Before-Tax, Net of Fees, Annualized, Rolling 3-Year*:
- gross gave 24 of 562 within 0.35 pp;
- with the fee left inside the return, 421 of 562.

Row W49-S2 asked which basis grades. This order answers it: Inflection is handled as 49 Financial's Black Diamond is.
- A **gross** return, plus the **fees** as their own figures, from Orion.
- Both sliced:
  - advised/supervised vs non-advised/unsupervised vs total;
  - billed vs unbilled vs total.

**What this repo already knows** (issuer read, ~04:2xZ):
- **Gross vs net.** `data/inf/manual_api/PATH_DISCOVERY.md:124`: `Performance.GrossOfFees` / `NetOfFees` are query-level options, not
  paths. Gross is requested with `Performance.Value` and the gross `performanceOptionId` in `contextChange`. So Orion can return a
  gross TWR. Round 36 read the net one.
- **Fees paid.** `PATH_DISCOVERY.md:181`: `Activity.Value` with `activityOptionId` 11 is Advisory Fees Paid.
- **Billing.** `PATH_DISCOVERY.md:160-175`: `Billing.FeeAmount`, `AnnualFeePercent`, `FeeScheduleName`, bill period dates, `BillCycle`.
  - `Asset.IncludedInBilling` is the billed/unbilled flag, noted as `"Error:Not supported"` for some accounts (line 158).
- **Existing code.** `data/inf/manual_api/orion_billing_dim.py` (the pull) and `data/inf/scripts/silver/build_billing_dim.py` (to
  `silver/api_dims/billing/`). The one fee-classification home is `data/inf/scripts/gold/lib/fee_classification.py`.
- **Not found in the notes:** the advised/supervised vs non-advised/unsupervised slicing on Orion. It is the first read the next cell owes.

**Routing.** Sent to `1.0.0_SA_CTO~DELL2` for the round-37 analysis as an FWD-11 enrichment (C-TIEOUT, the FWD-8 basis per firm). The
COO cuts it from that analysis.
