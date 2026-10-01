# Never-widen request for TX-r-3 (Tax SMA activation) -- the blast radius, measured

**Author:** 4.0.0_SA_CRO (Chief Research Officer), MDPF_TAXSMA FAST lease
**For:** `1.0.0_SA_CTO` and one `2.0.0_SA_COO` seat (TX-r-3 AC3, gate G-W). This file is the request; it signs nothing.
**Measured:** 2026-10-01 04:3xZ, candidate code at the commit carrying this file, by
`org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/4.0.0_SA_CRO/probes/tx_r_3_blast_radius.py`: two full builds in one
process, both dry-run with ZERO S3 writes, one with Tax off (as deployed) and one with Tax on (real workbook rows,
real custodian tables, in-memory stores).

## The order's sentence is too narrow

TX-r-3 AC3 asks the sign-off to name "both served keys". That was written for contract 0.5.0. At 0.6.0 Tax moves
9 of the Gold function's 16 documents (4 scopes x 4 types). A sign-off naming two keys would not cover the act.

## What moves when Tax is ON and complete (denominator 16 documents; process-time fields excluded)

| Scope | Document | Result | What changes |
|---|---|---|---|
| 49financial | aggregate-aua-timeseries | CHANGED, 6 fields | total 1,743,965,549.58 -> 1,762,733,661.93; Tax 18,768,112.35; the `tax` member joins by_model; four extension fields |
| 49financial | aum-metrics | CHANGED, `total` | total 1,743,965,549.58 -> 1,762,733,661.93; `tax_additive_aum` added |
| 49financial | category-views | CHANGED, `nodes`, `sums` | SMA 20,927,264.62 -> 39,695,376.97; Client unchanged; total as above |
| global | aggregate-aua-timeseries | CHANGED, 6 fields | total 2,066,937,285.42 -> 2,091,754,766.55; Tax 24,817,481.13 (49financial 18,768,112.35 + Cottonwood 6,049,368.78) |
| global | aum-metrics | CHANGED, `total`, `meta` | total as above; a fourth fee-basis component `taxsma` |
| global | category-views | CHANGED, `nodes`, `sums` | SMA 20,927,264.62 -> 45,744,745.75; Client unchanged; total as above |
| cottonwood | aggregate-aua-timeseries | CHANGED, 5 fields | NO total moves (541,913,026.79 both ways); the `tax` member joins by_model; four extension fields |
| cottonwood | category-views | CHANGED, `nodes` | SMA 0.00 -> 6,049,368.78; Client 362,884,540.60 -> 356,835,171.82; total unchanged |
| inflection | aggregate-aua-timeseries | CHANGED, 4 fields | NO value moves; the four extension fields are added (null values, basis NOT_APPLICABLE) |
| cottonwood | aum-metrics | IDENTICAL | |
| inflection | aum-metrics, category-views | IDENTICAL | |
| all four | account-distribution | IDENTICAL | |

Run facts: both builds green, 16 of 16 documents built, 0 errors. The Tax-on build's own run today read FAILED
(`SOURCE_UNAVAILABLE`: the 2026-09-30 custodian partitions had not landed at 04:3xZ), so the figures above are the
2026-09-29 valuation, measured on knowledge day 2026-09-30 and served from history.

## The branches a sign-off has to cover

1. **Tax complete on the frontier date:** the table above.
2. **Activation day itself:** an account counts only from its first observation, and the valuation date is the
   prior session, so on day one no dollar moves. The four timeseries documents still gain the extension fields and
   49financial and global gain a `tax` member with null values. Dollars arrive on the next trading day's run.
3. **A day Tax cannot be read, after the first complete day:** the 49financial and Global totals carry the last
   complete Tax figure, labelled `CARRIED_LAST_COMPLETE` with its date (Andrew-direct 2026-09-30 18:3xZ). Unit-tested;
   NOT exercised on real data.
4. **A Cottonwood Tax account that gains a model assignment:** Cottonwood's Tax is withheld that day (overlap
   control) and its last complete figure carries. Unit-tested; the real data has 0 such accounts of 47.
5. **Tax off (today):** nothing moves. Measured at TX-r-1 on the deployed function, 16 of 16.

## Addendum 2026-10-01 17:3xZ -- now asked, on Andrew's word to activate (record @28e5589af0)

- **The code is deployed.** The Gold function runs pin 8ade880fad since 15:00Z: the table above is that code (measured
  at 04:3xZ on the same candidates). Activation adds environment and a secret value only, no code.
- **It meets the HEALGAP hookup's condition 3.** The 2026-10-02 13:30Z run is that deploy's leg V2, whose trigger
  rolls back on "any served change outside the five Cottonwood dates and Global's same five". Activated before it,
  that run also carries branch 2 above (extension fields; a null `tax` member at 49 Financial and Global; Tax-off
  values unchanged). So this request also asks `1.0.0_SA_CTO` to amend that trigger to admit exactly the Tax changes
  named here, or to rule that activation waits for the leg's read.
- **When dollars first appear.** Branch 2 holds on 10-02; the Saturday and Sunday runs fail the Tax read on Black
  Diamond's late Friday file (STATUS Parked) and carry nothing; the first run with Tax dollars is **Monday 2026-10-05
  13:30Z** (valuation 10-02), unless Andrew rules that the first observation also covers the prior business day.

## What is NOT in this request

- **The writer count per served key.** Not measured here. The signer reads it: the Gold function writes the dated
  documents under `portal/gold/mdpf/` in `opal-data-assets`; the publisher function copies each to the served plane.
- **The rollback per key.** TX-r-3 AC10 exercises it once at activation (capability off, switch OFF). Whether a
  dated document already written with Tax can be rewritten the same day under the conditional-immutable put is
  UNMEASURED.
- **The served plane itself.** These are the Gold function's shaped documents. The publisher's rollout switch adds
  two stamp fields to category-views and gates nothing else, so the Gold capability, not the switch, moves the dollars.
- The code measured is a CANDIDATE. The deployed functions run e8994f23af, which has neither Cottonwood change and
  still carries the valuation-date defect fixed in this commit.
