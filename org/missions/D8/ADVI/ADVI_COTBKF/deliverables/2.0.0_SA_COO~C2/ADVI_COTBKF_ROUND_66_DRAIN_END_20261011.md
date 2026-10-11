# L8 drain end -- ADVI_COTBKF round 66: method_r28 against method_r29 over all days; the account-id scan repaired

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~12:17Z | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB66bn1-AC2)
**Cut on:** `1.0.0_SA_CTO~DELL2` msgs 4734 and 4772, and the issuer's row D2-S113. **Issued:** @7dec032cc6, 2 of 2 chains.
**No served write, no re-mint, nothing remote.**

| order | item | worker | state | issuer's own run at the drained base |
|---|---|---|---|---|
| CB-bn-1 | the build re-run locally under `method_r28` and `method_r29`, same inputs; every account-day classed | ~97 | complete @cb80f3800b, drained @3a75bb973a | `R28-VS-R29-RECORD control_rows=1691729 control_differing=30 rows_union=1691729 class_sum=1691729 both_measured_different=2 measured_r28_only=0 measured_r29_only=0 changed_account_days=2 changed_dates=2` |
| CB-bn-2 | the account-id scan sets aside a declared security identifier in a declared security list (direct-act) | ~98 | complete @c5665469c5, drained @5a8fd837ca | `847 passed, 12 skipped`; `DENOMINATOR: 543 tracked files scanned ...; 0 files with hits; 0 shape hits; 0 account-set hits; 1 named exceptions; 76 shape hits set aside as declared security identifiers in 2 files` |

Suite at the base after the last drain (@3a75bb973a): `847 passed, 12 skipped`. Row D2-S113 (the red suite) is answered by CB-bn-2.

## The two findings

**1. The withholding rule moves 2 account-days, on 2 dates** (2014-12-03 and 2020-11-13), both `both_measured_different`, both a
withholding day. 0 other days of those accounts, 0 other accounts, 0 of 82,593 account-month verdicts, 0 months changing between ABSENT
and not. The worker's account of why 2 and not the 7 measured days round 65 counted: on 5 the day's withholding amounts sum to zero, so
the flow does not change; 41 more of the 71 carry a changed flow but are blank under both rules. `CHANGED_DATES.csv` lists the two.

**2. The served table is not reproducible today** (row D2-W97-S1; `CONTROL_RECORD.json`). The positive control as first cut failed:
`method_r28` re-run today differs from the served local table on 30 of 1,691,729 account-days, over 29 dates, because the
split-history store the build reads live has grown (141 held CUSIPs listed against 32). The issuer re-stated the control (AMENDMENT 1
@e0aea14b12): both rules run on the same inputs today, proven equal; the drift is recorded, not required to be zero. None of the 30
drift account-days is also changed by the rule. The CTO ruled the store is pinned FIRST (msg 4844); that is round 67.

## What the issuer checked itself, and what it did not

- Ran the criterion as the order now states it; read the order's diff (the `<expect>` and the status only); read `CHANGED_DATES.csv`
  (2 rows, no account column); read the record's `inputs_equal` (split-store lines equal, price rows equal, 1 attempt),
  `changed_by_origin` (2 / 0 / 0) and the month counts (0 / 0).
- Read the scan helper's diff (one named function; the set limb untouched) and ran the suite and the scan's own line at the base.
- **NOT re-derived:** the two build runs (577 s and 496 s, the worker's), the eight class counts, the reason 5 of the 7 measured
  withholding days do not move. The worker did not read whether those 5 are zero-amount rows or offsetting rows.

## For L9 (CB66bn1-AC2)

- **The two runs differ in the rule only:** both regrade logs print `SPLIT-STORE listed=141 held_by_the_accounts=141` and the same
  repairs line; `after/security_day_price.parquet` equal row for row (2,124,908); the BEFORE side is `method_r28` on the store basis in
  both. The two runs were made at code commits 7dec032cc6 and e0aea14b12, which differ in no file under `data/` or `lib/` except three
  test files (the worker's statement).
- **The control was run before the comparison**, and failed as first written; the comparison ran only after the issuer's amendment.
  An earlier session started the r29 run before reading the control and killed it at about 83 seconds; nothing of it was used.
- **The comparison is NOT at a named pin.** It is at today's store state, equal across the two runs. The CTO's ruling says "both at
  that pin"; when round 67's pin exists the comparison is re-run at it if the states differ. So the list of 2 dates is the rule's
  effect on today's inputs.
- **One account id reached the worker's session output** (the serve build's last log line prints `read_account=`). It was written to
  no file, record or commit (the worker's statement; the issuer scanned the committed deliverables through the suite's own scan, 0 hits).

## Issuer defects in this round (two)

1. **The control was cut on an assumption** (that a re-run reproduces the served table) the issuer had not tested. The worker tested
   it and stopped correctly.
2. **The scan failure the round repairs was the issuer's own drain** (round 65, row D2-S113).

## Next

Round 67 is issued (@3e1c08668d): the pin (CB-bo-1, running) and the read on the added splits (CB-bo-2, drained @e7890e1cff: the four
price-moving entries are spin-offs dated after every day they move; all 30 drift account-days rest on them). No re-mint order is cut:
the CTO's word is no order until both lists exist. The default leg is `method_r28`.

**Round-close check:** REFUSED until CB66bn1-AC2 is graded.
