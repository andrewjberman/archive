# 49 Financial tie-out against Black Diamond -- round 1

**For:** `1.0.0_SA_CTO`'s ruling (PRD ADDENDUM v0.2 ruling 11, C-TIEOUT, C-FLOWTIME)
**By:** `0.4.0_DS_ClientPlatform~S`, 2026-10-01 | **Record:** `TIEOUT_49F_BLACKDIAMOND_R1.json`
**Vendor calls:** 0 | **overlap_before_pull:** 5

---

## The table

| account | period (effective) | BD daysHeld | Opal days used / in period | gaps | BD TWR | Opal END | Opal START | Opal MID | abs_diff (START) |
|---|---|---|---|---|---|---|---|---|---|
| acct#89d0916a | 2026-03-16 .. 2026-06-30 | 74 | 65 / 73 | 8 | -8.1346% | -9.9161% | -9.7580% | -9.7872% | 1.6233% |
| acct#89d0916a | 2026-03-16 .. 2026-08-28 | 116 | 104 / 115 | 11 | -5.7099% | -6.0299% | -5.8650% | -5.8954% | 0.1551% |
| acct#89d0916a | 2026-04-08 .. 2026-06-30 | 58 | 54 / 58 | 4 | -8.1799% | -9.8772% | -9.8772% | -9.8772% | 1.6973% |
| acct#89d0916a | 2026-07-01 .. 2026-08-28 | 42 | 39 / 42 | 3 | +2.6385% | +4.3139% | +4.3139% | +4.3139% | 1.6754% |
| 0076459710 | 2026-07-08 .. 2026-08-28 | 38 | 34 / 38 | 4 | +12.7830% | +9.1259% | +9.1259% | +9.1259% | 3.6572% |

**Summary (preferred convention START):** median **1.6754%**, p90 **3.6572%**, max **3.6572%**.
**Per convention medians:** END 1.6973%, START 1.6754%, MIDPOINT 1.6754%.
**flow_convention_ran:** `END` -- what the served gold is computed under, and it stays END.
**flow_convention_preferred:** `START` **mechanically; read it as UNDETERMINED.**
**proposed_tieout_tolerance:** **0.0370** (the preferred convention's p90 rounded up to the next 5 bp).

## The sentence

**The proposed tolerance is 3.70% and this cell recommends AGAINST adopting it as a tie-out bar.**
It is the rule executed faithfully, but the quantity it is a percentile *of* is not a disagreement
between two calculations of the same thing: Opal's geometric link **excludes the account-days it
withheld** while Black Diamond's return covers its full `daysHeld`, so the difference is dominated
by *which days each series counts*. The clearest case is account 0076459710, where Opal links 34 of
38 days to +9.1259% against BD's +12.7830% over all 38 -- and the withheld days include the
**$1,108,201.80 inception funding**. A 3.7% bar on a client-facing return would enshrine that
mismatch as acceptable agreement.

## Why the convention preference is not a measurement

END, START and MIDPOINT differ **only** on days where `external_flow` is non-zero; on a zero-flow
day all three reduce to `V_t / V_(t-1) - 1` and are the *same number*. Across these five periods
there are **10 flow-bearing account-days and exactly ONE** survives into the eligible population
(2026-03-25, account acct#89d0916a, flow $448,559.28). Three of the five periods have **zero**. START and MIDPOINT are
therefore identical on **three of the five** periods -- the three with no eligible flow day --
and their **medians** coincide exactly, because the median of five values lands on one of those
non-discriminating periods. START's median margin over END is 0.000218941: one day, one account.

**The circularity is the part that will not fix itself:** a convention differs only where there is
a flow, and a flow large or unreconciled enough to matter is exactly what drives `day_quality` to
`LARGE_FLOW`, `FLOW_UNRECONCILED` or `NOT_MEASURABLE`. The eligible population is selected
*against* the signal. Amendment 3's one-population rule is right -- it retired the earlier defect
of scoring a guard-substituted series against raw candidates -- and it cannot manufacture
discriminating days the gold withholds.

## What was NOT measured

- **Three of five roster accounts never enter.** Only 3 of 5 carry a `bd_internal_id` at all;
  0035940058 and 0091939812 are `pending_resolution`, absent from `dim_account_xref`, so no vendor
  response maps to them. 0084073310 carries an id but has no landed response.
- **5,314 of 5,318 landed responses were skipped** -- their relationships carry no roster row
  (refusal clause; denominator printed in the record).
- **Four calendar-year ranges (2024, 2025) are vendor-absent**, not zero: `daysHeld 0` and an empty
  `timeWeightedReturns`. Skipped as absent.
- **No fresh vendor pull was made.** `overlap_before_pull` is 5, and amendment 1 admits a pull only
  *below* 5.
- **The gold was not re-emitted.** The served daily returns stand on END until the CTO rules; a
  re-emit under another convention is a new `method_version` and a round-2 cell.

## Corroboration worth recording

Black Diamond's own `startDate` equals this seat's independently measured gold inception on **both**
mapped accounts: acct#89d0916a -> 2026-03-16 and 0076459710 -> 2026-07-08. Those dates were measured
from the custodian's balance partitions by `first_data_dates()` before any vendor file was read.
Separately, BD reports `shortAllocation 0.4557` on acct#89d0916a, corroborating row S9's finding that
the Tax SMA product is short by design.

## Routed

Both findings, their measurements and four candidate remedies are row **`IRPT_DASHBD-S10`**,
`disarm_owner 1.0.0_SA_CTO`. The recommendations: do not adopt 3.70%; treat the preferred convention
as undetermined; compare like day sets or rename what the tie-out reports; and the enrichment that
would settle it needs a ruling, not cell work.
