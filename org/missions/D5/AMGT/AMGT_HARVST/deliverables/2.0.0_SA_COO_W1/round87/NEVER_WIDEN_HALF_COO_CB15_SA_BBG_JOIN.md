# NEVER-WIDEN -- COO HALF, ADDENDUM 4: `sa` and `bbg` join the dell1 harvest runner after the uploader fix is proven (`HVST-cb-15`, round 87, workstream RUNNER-JOIN)

**Signer:** `2.0.0_SA_COO~W1`, drafted 2026-10-16 ~03:3xZ UTC while `HVST-cb-13` runs. **Extends:** the first half `NEVER_WIDEN_HALF_COO_CB2_DELL1_RUNNER.md`, addendum 1 `NEVER_WIDEN_HALF_COO_CB2_ADDENDUM_1_SA_BBG.md` (the nature of `sa` and `bbg`: `sa` rides a person's sign-in, `bbg` rides the 2026-09-11 Secrets session and is never refreshed; CTO addendum `ledger/NEVER_WIDEN_ROUND87_CB2_CTO_HALF_ADDENDUM_1_SA_BBG.md` with C-i, C-j, C-k), addendum 2 and 3. The bucket is `opal-data-harvest` (erratum). **Pairs with:** a CTO addendum 4 (owed).
**Authority:** Andrew-direct 2026-10-15 ~16:3xZ ("including Seeking Alpha + Bloomberg"); CTO msg 6353 and 6388 (`sa` and `bbg` join only after the fix shows their projected per-cycle total under 5 GiB).

## THE ACT, in the order's words

On dell1, once, by `0.7.0_AE_CloudOps~SC1`, AFTER `HVST-cb-13`'s evidence reads TRUE (condition C-a4): at a stop-file boundary, with the runner STOPPED, seed the local record for the two new publishers (`python -m lib.opal_data_harvest.seed_silver_known seed --runtime-root <runtime> --publishers sa bbg`, dry-run first; the snapshot file merges by table), then re-register the ONE task from the CURRENT pin (no code change) with `-Publishers wsj,barrons,sa,bbg`, same state, runtime root, stop file and flags, start once, read at +3 and +15 minutes, check for duplicates from the restart time, rollback to `wsj,barrons`.

## WHAT THIS ADDS (named)

- **Two more publishers' production rows change writer from site Z to dell1** (`sa`, `bbg`); site Z's runner is Disabled (formal read-back on file). The first-half condition of one writer per publisher is read again at this act for the two prefixes (site Z wrote `sa` until about 18:25Z on 2026-10-15, its own record).
- **A one-time seed read of the new tables:** `sa` `article` 1367 parts / 80.4 MiB and `listing_hit` 1592 parts / 284.2 MiB; `bbg` `article` 747 parts / 202.2 MiB and `listing_hit` 4 parts / 0.1 MiB (LIST sizes of 2026-10-16): about 567 MiB once, with the runner stopped. After it the uploads read none.
- **`sa` is held by a person's sign-in, not a script:** its profile was signed in by Andrew on 2026-10-15 ~20:1xZ; its expiry makes every `sa` job end `sign_in_refused` (class `expired`), a recorded finding, never a repair (the runner never signs `sa` in, never reaches the Kimi-VL authenticator). **`bbg`** runs on the Secrets session captured 2026-09-11, never refreshed; the Google credential is never reached.
- **Order inside a pass** (`cycle_runner.PUBLISHERS`): `bbg`, `wsj`, `barrons`, `sa`; a stop status ends THAT publisher's cycle and the runner goes to the next.

## BLAST RADIUS

- **Writers of the property N = 1 per publisher**, as before; the task registration is written by `install-cycle-schedule.ps1` only.
- **What it touches in the world:** vendor requests to `seekingalpha.com` and `bloomberg.com`; S3 writes of bronze and silver for the two prefixes; minimised Chrome windows on dell1; NO sign-in by the runner for either.
- **Not touched:** `ft`; the Google credential; the Kimi key; `wsj` and `barrons` settings; the main tree's code; other seats' worktrees.
- **Served output moved:** the `sa` and `bbg` rows that feed `AMGT_RESAPP`'s Chatter axis and the news layer change writer.

## BOTH BRANCHES

- **Branch D (the first uploads read about 0 GETs for `sa` and `bbg`, `check` reads `DUPLICATES=0`, R7's per-cycle projection for each is under 5 GiB):** the join stands; the issuer reports the first productive cycle per publisher (the E2 proof by the ledger) to the CTO and, through MSTR, to site Z.
- **Branch F (a duplicate, an upload error that did not occur for `wsj` and `barrons`, or R7 above 5 GiB for a publisher):** re-register with `wsj,barrons` only, file one row; the seeded records stay.
- **Branch G (CTO C-j):** two consecutive `bbg` legs ending `bot_check` or `TargetClosedError` drop `bbg` by re-registration, finding to the CTO; `sa` unaffected.
- **Branch E (an `sa` expiry):** recorded finding for the issuer; Andrew signs in again; no sign-in by any other hand.

## CONDITIONS

- **C-a4.** `HVST-cb-13` is COMPLETE and its evidence reads TRUE: the first uploads under the new pin read about 0 GETs per upload (ledger), `check` reads `DUPLICATES=0` over parts written after the restart, the 5 GiB bar holds for `wsj` and `barrons`.
- **C-b4.** Site Z's Disabled read-back is on file and the S3 read for the `sa` and `bbg` prefixes shows no site Z write after 2026-10-15T19:04:24Z other than the `sa` objects written before it (print the newest `LastModified` per prefix).
- **C-c4.** The `sa` profile still reads signed in: one `run --no-sign-in` for `sa`, `BA` ends `complete_candidates` with more than 0 accepted, run BEFORE the stop and not while the runner holds the `sa` profile (the runner has no `sa` yet, so it does not). If it reads logged out, `sa` is left out and Andrew is asked.
- **C-d4.** The seed for `sa` and `bbg` is run with the runner stopped, dry-run first, and `rows_without_hash` reads 0 for every table; `check --since` opens AFTER the seed (the restart T0).

## ROLLBACK

Stop by the stop file, re-register `wsj,barrons` from the same pin, start once; the `silver_known` rows and the snapshot stay; rows written for `sa` and `bbg` are append-only and stay.

## WHAT THIS ADDENDUM DOES NOT COVER

- `ft`; any sign-in by the runner for `sa` or `bbg`; an in-profile sign-in for `sa` (a candidate cell); a challenge repair in a minimised window; deleting duplicate silver rows.

## VERDICT: SIGNED (COO). Not started until the CTO addendum 4 is on file and C-a4 to C-d4 read true.
