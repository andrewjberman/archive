# TX-r-1 leg V2 -- the served plane after the first scheduled run on the Tax-off release (read 2026-10-01 13:53Z to 14:07Z)

**Author:** 4.0.0_SA_CRO (Chief Research Officer), the deploy's operator. **For:** `1.0.0_SA_CTO` to rule the leg.
**This seat gives no verdict on its own release.** The probe's own count is 12 of 16. Every one of the four
differences is traced below to a cause measured outside the release. The ruling asked for: does leg V2 close.

## The run

- Gold function, scheduled 13:30Z, deployed code `7hI4flW5..` (pin e8994f23af, Tax DISABLED): "cycle complete: 16/16
  A4 objects built; errors=none"; key-set identity PASS on 4 types x 4 scopes (log read 13:4xZ; 17 lines read, 0
  naming FAILED).
- Publisher, scheduled 13:50Z, deployed code `pj+Jat96..`, switch OFF: its manifest moved from 2026-09-30T13:50:52Z to
  2026-10-01T13:50:52Z and all 16 served documents were rewritten.

## The probe, as written

`probes/tx_r_1_served_delta.py compare tx_r_1_served_baseline.json` at 13:53Z: **documents as expected 12 of 16**, rc 1.
What it asserts per document: the key-path shape is unchanged; every history value at a date the baseline carried is
unchanged; the Tax member is still served with a null amount; the document was rewritten.

| Served document | Probe | What differed |
|---|---|---|
| aum-metrics, account-distribution, category-views x 4 scopes (12) | OK | nothing |
| 49financial aggregate-aua-timeseries | FAIL | 2 of 477 baseline dates changed (2026-09-28, 2026-09-29) |
| global aggregate-aua-timeseries | FAIL | 2 of 486 baseline dates changed (2026-09-28, 2026-09-29) |
| inflection aggregate-aua-timeseries | FAIL | 1 of 477 baseline dates changed (2026-09-29) |
| cottonwood aggregate-aua-timeseries | FAIL | shape 624 -> 648 paths; the probe lists paths naming "tax" |

## The cause of each difference, measured

**1. The prior frontier date is restated every day, on the old code too.** `probes/tx_r_1_v2_restatement_control.py`
over the Gold function's own dated documents, six days per scope: all 16 consecutive pairs written wholly by the OLD
code restate exactly one shared date, the earlier document's frontier. So a changed 2026-09-29 is the daily pattern,
and it is the whole of Inflection's difference. In every pair, old or new: top-level keys added 0, removed 0; keys
naming Tax 0.

**2. The second date at 49 Financial and Global is the input's own restatement.** The pair that crosses the release
restates two dates there, not one. The moves:

| Date | 49 Financial model | 49 Financial non-model | Total |
|---|---|---|---|
| 2026-09-28 | +74.47 (one model) | -74.47 | unchanged |
| 2026-09-29 | +1,637.76 (three models) | -1,637.76 | unchanged |

`probes/tx_r_1_v2_input_restatement.py` reads the input the Gold function takes its 49 Financial model series from
(SmartX `fact_model_aum_daily`; each partition carries the full history and only the newest is read). Between the
partition of 2026-09-30 (written 13:23Z that day) and of 2026-10-01 (written 13:23Z today), day 2026-09-28 differs in
1 of 8 models by +74.47, day 2026-09-29 in 3 of 8 models by +88.42, +514.07 and +1,035.28 (sum +1,637.77), and the
control day 2026-09-25 differs in 0 of 8. The served per-model moves are those same three figures. Global's two dates
are 49 Financial's.

**3. Cottonwood's shape grows by 24 paths every day.** `probes/tx_r_1_v2_cottonwood_shape.py`: +24 paths on each of the
last three day pairs, two of them on the old code (2026-09-25 -> 09-28, 09-28 -> 09-29) and one across the release;
0 paths removed (read on the Gold function's dated documents, 629 -> 653 paths across the release). Every added path
is a new date key under three `meta` maps. All 27 paths naming "tax" in the newest document sit under
`meta/custom_residual_detail` and name a strategy called "Opal Moderate Income Portfolio (Tax Efficient)"; 0 are
outside it.

**4. On identical inputs the release changed nothing.** Leg V1 (02:12Z and 02:17Z): the deployed function's dry run
before and after the apply, 16 of 16 documents, differed in process-time fields only.

## What this shows about the probe

Two of its four assertions do not hold for this pipeline on any day: history at a baseline date is restated once the
next day's input lands, and Cottonwood's document carries date-keyed maps that grow. The assertions that test the
release held on 16 of 16: no Tax field appeared, the Tax member is null, each document was rewritten. The baseline
was authored by this seat; the wrong expectation is this seat's.

## Not measured

- Why SmartX restated 2026-09-28. The restatement is read in its partition; its reason is the vendor's.
- The served documents were compared by the probe's shapes and hashes, and the causes were read on the Gold
  function's dated documents, which the publisher copies. A served-plane value read per date was not taken.
