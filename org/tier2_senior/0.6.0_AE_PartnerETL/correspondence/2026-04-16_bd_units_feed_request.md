# BD Escalation: Units Field for UNREALIZED_DAILY Report

**Task Order:** ADVI_ROLLUP.SL-AE1  
**Date:** 2026-04-16  
**Author:** 0.6.0_AE_PartnerETL  
**Status:** DRAFTED — pending Andrew pre-ACK before send

---

## Contact Route

**Primary contact:** Black Diamond (SS&C) partner support  
**Account:** `AndrewBerman49F` on `bd3.bdreporting.com` (49 Financial BD account)  
**BD support portal:** support.bdreporting.com (or via account manager assigned to the 49 Financial / Opal Capital account)  
**Cc:** andrew@opalinvest.com, 49 Financial operations team  

NOTE: Opal accesses BD via 49 Financial's BD subscription. The account manager
for 49 Financial's BD account is the correct escalation contact. If unknown,
Andrew should check the BD partner portal or email support@bdreporting.com
referencing account `49financial` / Opal Capital.

---

## Pre-Send Investigation Summary

Before drafting, AE audited both of the candidate feeds:

### Feed 1: Fees_OpalCapital_Daily (bronze/fees/)
- Most recent file: `Fees_OpalCapital_Daily_2026-04-14_to_2026-04-14.xlsx`
- Columns (34 total): TransactionID, Trade Date, Settle Date, Relationship ID,
  Account Number, AccountID, Original Account Number, Account Display Name,
  Account Name, Original Account Name, Account Owner Type, Account Owner,
  AssetID, Asset Name, Asset Display Name, **Units**, Market Value,
  Transaction Fee, Income, Account Fee, Tax Status, Billing Account Custodian,
  Billing Account, Billing End Date, Billing Start Date, Flat Fee, Basis Points,
  Fee Schedule Level, Fee Schedule Rate Type, Fee Schedule Type, Fee Schedule
  Description, Account Fee Schedule, Account Billable, CUSIP
- Units column: PRESENT and fully populated (750/756 rows non-zero)
- Ingestion: convert_fees_to_silver.py already maps Units->units
- VERDICT: Units here = fee billing transaction quantity (not holdings snapshot)

### Feed 2: UNREALIZED_DAILY_YYYY-MM-DD.xlsx (forwardfill_v2/unrealized/)
- Most recent file: `UNREALIZED_DAILY_2026-04-13.xlsx`
- Columns (14 total): Open Date, Unit Cost, Inherited Date, Relationship ID,
  Account Number, AccountID, AssetID, Asset Name, Last Dividend,
  Original Asset Name, Asset Display Name, Symbol, Ticker, CUSIP
- Units column: ABSENT
- Silver output: silver/unrealized/{date}.parquet has 93,707 rows per day
  with (open_date, unit_cost, account_id, asset_id, cusip) but NO quantity
- VERDICT: This is the gap. Need Units (quantity held per lot) here.

### Why Units from UNREALIZED_DAILY is needed
BD's sub-custody sleeve accounts (PCRA Trust, SWTC TTEE, retirement sleeves)
land in silver/unrealized but do NOT fire Transfer In transactions into
silver/transactions. Gold's FIFO replay therefore can't open lots for these
accounts. The fix (ADVI_SLEEVE) seeds opening lots from silver/unrealized rows,
but needs quantity to compute market_value = qty * price. Without it, we must
infer quantity from cost-basis apportionment (Path 3 fallback), which breaks
on $0-cost-basis rows (CASH, MONEY MARKET, inherited lots).

Diagnostic case: Jones z0817905851 -- silver/allocations $2,396,510,
gold/holdings_lots $82,423, delta $2.31M. 14 BD-reported lots in ULN,
zero Transfer In events. Firm-wide impact: ~$35-50M of underreported AUA
concentrated in 403 mapped-no-RPS sleeve accounts.

---

## Draft Email

**To:** [BD account manager / support@bdreporting.com]  
**From:** andrew@opalinvest.com  
**Cc:** [49F ops contact]  
**Subject:** Data Enhancement Request: Units Column in Unrealized Gains/Losses Export

---

Hi [Name],

I am writing to request an enhancement to our daily Unrealized Gains/Losses
(UGL) data export that Opal Capital receives through our 49 Financial BD account.

**What we currently receive:**

Our daily `UNREALIZED_DAILY_YYYY-MM-DD.xlsx` export contains 14 fields:
Open Date, Unit Cost, Inherited Date, Relationship ID, Account Number,
AccountID, AssetID, Asset Name, Last Dividend, Original Asset Name,
Asset Display Name, Symbol, Ticker, CUSIP.

**What we need:**

We need a `Units` (quantity) column added to this daily export -- the number
of units/shares held for each open tax lot per account.

Specifically, for each row in the unrealized report, we need:
  - Account ID  (already present)
  - Asset ID    (already present)
  - Open Date   (already present)
  - Unit Cost   (already present, cost basis per unit)
  - **Units** = quantity of shares/units held in this lot (NEW)

Note: our `Fees_OpalCapital_Daily` report already includes a `Units` column.
We are requesting the equivalent field in the unrealized lots report.

**Why this matters:**

We use the unrealized lots report to reconstruct holdings for sub-custody
accounts (PCRA Trust, SWTC TTEE, and similar retirement sleeves). These accounts
report positions through the allocations/unrealized feeds but do not generate
Transfer In transaction events, so we cannot derive quantity from transactions
alone. Without quantity in the unrealized export, we must use cost-basis
apportionment as a proxy, which fails on $0-cost-basis positions (CASH,
MONEY MARKET, inherited lots).

**Format options (in order of preference):**

1. Add `Units` as a new column in the existing `UNREALIZED_DAILY` export
   (same file, one additional column) -- simplest and preferred.
2. Provide a separate daily report with (AccountID, AssetID, Open Date, Units)
   alongside the existing UGL report.
3. An S3 drop of the above in CSV or Parquet format if XLSX is not suitable
   for this data volume.

**Volume note:** Our current UNREALIZED_DAILY files are approximately 25 MB
each (93,000+ rows), so a single additional column should not materially
affect file size or export runtime.

Could you let us know:
1. Whether `Units` is an available field in BD's UGL/Data Mining export schema?
2. If yes: can you update our `UNREALIZED_DAILY` template to include it?
3. If no: what is the process to request this as a platform enhancement?

We are happy to jump on a call to discuss if that is easier.

Thanks,
Andrew Berman
Opal Capital
andrew@opalinvest.com

---

## Tracking

**Channel to use:** Email + BD support portal ticket  
**Response tracking:** Open a GitHub issue under opal-invest/opal-infra titled
"BD UNREALIZED_DAILY: waiting on Units field from BD" once email is sent.
Reference ticket # in ADVI_SLEEVE project JSON.  
**Expected response timeline:** 2-5 business days for template config questions;
4-6 weeks if a platform enhancement request is required.  
**If no response in 5 business days:** Follow up with 49F ops team directly.  
**Path 3 fallback:** DS's cost-basis apportionment (ADVI_SLEEVE SL-P0) remains
active and ships to shadow mode while we await BD response.
