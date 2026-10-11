# L8 drain end -- ADVI_COTBKF round 67: the split store is pinned; the splits the grown store added are read

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~13:04Z | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB67bo2-AC2)
**Cut on:** `1.0.0_SA_CTO~DELL2` msg 4844 (pin first; the 30 drift days are a second change). **Issued:** @3e1c08668d, 2 of 2 chains.
**No served write, no re-mint, nothing written remotely.**

| order | item | worker | state | issuer's own run at the drained base |
|---|---|---|---|---|
| CB-bo-1 | the build reads the split store at a named instant by object version, refuses an unpinned read, records what it read (direct-act) | ~99 | complete @04b6a484f1, drained @e6645ff9cd | `866 passed, 12 skipped`; `SPLIT-STORE-PIN-RECORD refuses_without_flag=True proof_a_rows=1691729 proof_a_differing=0 proof_a_held=32 proof_b_price_rows_equal=True proof_b_digest_equal=True proof_b_minutes_apart=30` |
| CB-bo-2 | the splits added since the served run: which move a price, and whether each is real and dated before the days it moves | ~100 | complete @60978aee8a, drained @e7890e1cff | `ADDED-SPLITS-RECORD held_listed_then=32 held_listed_now=141 added=109 price_moving_cusips=4 price_points=3034 drift_returns=28 drift_blank_reasons=2 classes=['REAL_AND_BEFORE']` |

## The issuer's own acts on the pin (CTO msg 4844 item 1: "two runs of r28 an hour apart print equal output")

- **An unpinned read refuses.** Issuer run of the valuation with `--cash-leg method_r28` and no flag, at the base:
  `REFUSED: the split store is read only at a named instant; pass --split-store-as-of`; no data directory was created.
- **An hour apart, equal.** The worker's first valuation run at `as_of=2026-10-11T11:55:40Z` began 12:00:40Z. The issuer ran the same
  step at the same pin from the base tree, into its own folder with its own copy of the price cache: start 13:01:16Z, end 13:03:30Z,
  rc 0. Its line: `SPLIT-STORE-PIN address=s3://opal-data-assets/yahoo/global/silver/price_history/ as_of=2026-10-11T11:55:40Z
  listed=141 held=141 sha256=c414ea2b56a6596affb78d17dafcee3a82845c862a09ed6df649fd09e80811ae`, identical to the worker's; its
  `security_day_price.parquet` sha256 `695a3b2067533504200f76dad338861f6533f12c34780a100e805badb2022dda`, equal to both of the
  worker's runs (issuer `sha256sum` of all three). 60.6 minutes start to start. The valuation step, not the whole chain.
- **Read:** the product diff (version-aware list and get in the census helper; `load_store_splits` takes `as_of` and refuses without
  it; the pin sidecar; the manifest field), 5 files, 451 insertions.

## What the issuer did NOT re-run

- **Proof A** (the round-66 control, now passing): the full `method_r28` chain at `as_of=2026-10-09T11:52:52Z` reproduces the served
  local table on 1,691,729 of 1,691,729 rows, 32 held CUSIPs, the same repairs line as the served log. The worker's run (587 s and
  361 s). The instant is the modification time of the first file the served regrade wrote; the served manifest records no read time.
  The store's version listing shows one fixed 32-partition state from 2026-10-09T02:39:06Z to 2026-10-10T02:33:17Z, so the result does
  not turn on the minute; the two neighbouring instants were checked on the listing, not run through the chain.
- **The added-splits measurement:** every count and class in CB-bo-2's record beyond its totals.

## For L9 (CB67bo2-AC2)

The four price-moving entries, each classed REAL_AND_BEFORE by the worker: 00206R102 (2022-04-11, 1.324, 649 points), 438516106
(2025-10-30, 1.061, 1,876), 460146103 (2021-10-01, 1.056, 392), 717081103 (2020-11-17, 1.054, 117). The evidence it gives is
independent of the store: the custodian's own cost-adjustment rows on exactly each date with a second security contributed the same
day; own quantity unchanged across the date; the traded price dropping across it; the factor implied by two price sources matching
the store's ratio to three decimals. Every moved point lies before its date. All 30 drift account-days rest on these: 28 returns in one
account on the first, 2 blank reasons on the second.

**Three things for the grade, as the worker states them:**
- **These are SPIN-OFFS, not share splits** (row D2-W100-S1): the ratio is a price factor, not a share count. Whether the rule should
  scale closes for a spin-off is a question it left to the CTO and did not decide.
- For 00206R102 the one-day close ratio (0.8132) is 7.7 percent away from 1/1.324; the factor is confirmed by the two-source ratio,
  not by that one day.
- The independence of the second price source from the first, upstream, is not proven.

## Rows of the round

- D2-W99-S1 (OBSERVATION): in a fresh worktree the regrade stops at its report step for want of five untracked inputs (round 22/24/27
  grades, movers, causes) that exist only in one worktree's scratch. They feed the report, not the tables.
- D2-W99-S2 (OBSERVATION): the as-traded price input carries a column stamped from the price store's CURRENT LastModified, a second
  live read. It does not reach the returns; that file's hash is not reproducible.
- D2-W100-S1 (OBSERVATION): the spin-offs, above.
- D2-W97-S1 (BLOCKING, round 66): answered by CB-bo-1's Proof A. Its close is the reviewer's.

## Where this leaves the re-mint (the CTO's "no order until both lists exist")

- **List 1, the withholding rule:** 2 account-days on 2 dates (round 66, `CHANGED_DATES.csv`), measured on today's store state, not at
  a pin. At the served instant's pin the store differs from today's (32 against 141 partitions), so the comparison has NOT been run at
  the pin the CTO's ruling names. It is one more run of `method_r29` at `as_of=2026-10-09T11:52:52Z` against Proof A's `method_r28`.
- **List 2, the grown store:** 30 account-days on 29 dates (`DRIFT_DATES.csv`), all on four spin-offs classed real.
- **Not decided here:** which pin a re-mint uses (the served instant, or today's with the 30 named), whether spin-off factors are
  applied at all, and the default leg. No re-mint order is cut. The mint adapter does not yet copy the pin into the mint's manifest.

**Round-close check:** REFUSED until CB67bo2-AC2 is graded.
