# NEVER-WIDEN -- COO HALF, ADDENDUM 3: re-pin the dell1 harvest runner to a head carrying `HVST-cb-12` (the uploader appends without reading the target table), `wsj` and `barrons` only (`HVST-cb-13`, round 87, workstream RUNNER-REPIN2)

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-16 ~02:4xZ. **Extends:** the first half `NEVER_WIDEN_HALF_COO_CB2_DELL1_RUNNER.md` @5271f99a66, addendum 1 (`sa`, `bbg`, not started), addendum 2 `NEVER_WIDEN_HALF_COO_CB9_REPIN_AND_JOIN.md` and the CTO's amendments to it (wsj,barrons only; delete-first seed; the 5 GiB bar includes the uploader). The bucket is `opal-data-harvest` (erratum `79a5321348`). **Pairs with:** a CTO addendum 3 (owed).
**Authority:** CTO msg 6388 (cut cb-12; "sa and bbg join only after cb-12 shows their projected per-cycle total under 5 GiB"); Andrew-direct 2026-10-15 ~16:3xZ.

## THE ACT, in the order's words

On dell1, once, by `0.7.0_AE_CloudOps~SC1`: at a stop-file boundary (never a kill), re-register the ONE task `Opal Data Harvest - Continuous Cycle` from a NEW locked pin `R` (the head of `box/dell1` at the act, which must carry `c1df06b1ef`, the cb-12 merge, and every commit the current pin `3c1e8bcdb1` carries), publishers `wsj,barrons` (UNCHANGED), same state dir, runtime root, stop file and flags (`-Windowless -RefreshOnce`), `-Plan` read first, start once, reads at +3 and +15 minutes, rollback to `3c1e8bcdb1`. Nothing else changes.

## WHAT THIS CHANGES (named)

- **The uploader's S3 reads stop.** From R, `upload-harvest` de-duplicates against a local `silver_known` table in the runner's progress database and issues no `list`/`get` against the target silver table. It writes the same part files as before. Measured before (barrons, 13 uploads): 2,794 GETs / 38.9 MiB, about 3 MiB each; expected after: about 0 GETs per upload.
- **A new local table is created** in `<runtime>\progress.sqlite3` on the first upload (`silver_known`). Rows this runtime has already appended before R are NOT in it: a row it re-uploads after R that is identical to one already in S3 would be appended again (a duplicate part row; readers take the newest row per key). The pending outbox at the act holds only this runtime's own rows.
- **The shared writer `store.silver_append` gains an opt-in argument** (default path byte for byte unchanged; its tests and the corpus, management, lusha and bloomberg tests pass on the main tree). The runner is the only caller that passes it.

## BLAST RADIUS

- **Writers of the property N = 1 per publisher** (site Z Disabled, dell1 the only writer), unchanged. The bronze/silver objects the runner writes are the same objects at the same keys; only HOW the uploader decides what to write changes. The task registration is written by `install-cycle-schedule.ps1` and by nothing else.
- **Not touched:** `sa`, `bbg`, `ft`; the state dir; the main tree's code; the other seats' worktrees.
- **Served output moved:** the same `wsj` and `barrons` rows as before; none newly.

## BOTH BRANCHES

- **Branch D (the first uploads after R read near 0 GETs in `s3_get_ledger.jsonl` and the cycle record's `s3_get_count_jobs` is small):** the uploader's reads are proven gone for these two publishers; the issuer sends the CTO the projection for `sa` and `bbg` (his join gate) and cuts their join order.
- **Branch F (an upload after R fails with a new error, or reads MORE than before, or a `wsj` or `barrons` job ends differently than at `3c1e8bcdb1`):** re-register from `3c1e8bcdb1` with `wsj,barrons` and the same flags, start once, file one row; the `silver_known` table stays in the database (inert at the old pin).
- **Branch X (the account stop rule or the 5 GiB bar fires):** as the earlier halves.

## CONDITIONS

- **C-a3.** R carries `c1df06b1ef` (`git merge-base --is-ancestor`, with the reverse as the negative control) and `3c1e8bcdb1`; the earlier halves and addenda read SIGNED at their pins (the first pair, addendum 1, addendum 2 with its amendments, this addendum).
- **C-b3.** The stop is by the runner's own stop file: the current job may be long (a `barrons` job that rejects dozens of candidate articles runs 15 minutes or more); the executor waits for the `.cycle.json` or for the log's `STOP-FILE` line and does NOT kill; if 30 minutes after the stop file the log carries no `STOP-FILE ... no further cycle` line: STOP, file a row, change nothing.
- **C-c3.** The previous pin `3c1e8bcdb1` stays locked until the CTO closes the cell.

## ROLLBACK

As the earlier halves: stop file, re-register from `3c1e8bcdb1`, start once. Rows written under R are append-only and stay.

## WHAT THIS ADDENDUM DOES NOT COVER

- `sa`, `bbg`, `ft`; any sign-in by the runner; an S3 manifest object; deleting duplicate silver rows.

## VERDICT: SIGNED (COO). Not started until the CTO addendum 3 is on file and C-a3 and C-b3 read true.
