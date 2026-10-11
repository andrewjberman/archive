# IRPT_DASHBD round 55, workstream B -- L8 drain end for DB-b-110 (issuer 2.0.0_SA_COO~D2, 2026-10-11 ~03:0xZ)

For `3.0.0_SA_CVO`. This closes the part of round 55 that `IRPT_DASHBD_ROUNDS_55_56_B_DRAIN_END_20261009.md` left open. The issuer re-ran the
criterion in the worker worktree before the drain. `round-close-check --round 55` reads orders=3, 3 complete, verdict=MAY-CLOSE. No client figure or
account number appears here.

| order | worker | risk | criterion (issuer re-run) | drained |
|---|---|---|---|---|
| `IRPT_DASHBD.TO-DB-b-110` stage memory cut | ~85 | WORLD | DB55-2-AC1 PASS (`lots_read peak 1725.2 -> 1263.3 MB`) | @5d339ced5b |

## What happened to the order

The first ~85 was lost in the dell2 crash of 2026-10-09 with its worktree and every uncommitted edit. Its private measurement records survived
outside the repo. The issuer cut a fresh worktree from box/dell2 @8658c32241 and respawned ~85 on 2026-10-11. The new run rebuilt the harness,
re-measured BEFORE itself (it did not reuse the old record), re-made the cut and measured AFTER at its own commit.

## The cut (worker commits 19ba6fe341 and 625ad9c17b)

- **Method:** process RSS (psutil, sampled every 0.05 s) over `handler.local()` on the 2026-10-08 kit day. S3 GETs only; the status write goes to a stub.
- **Largest stage:** `lots_read`, 1725.2 MB before and 1263.3 MB after. Process peak 1725.2 MB before and 1459.1 MB after.
- **Change:** `read_window` and `read_day` in `account_activity_lots.py` now build the account mask from the account column alone and convert only
  the batch's rows from the arrow table (`read_partition(keep=, on_table=)`, `_kept_frame`, `_account_mask` in `account_return_daily.py`). A table
  whose narrower conversion could change a dtype takes the old full conversion.
- **Byte equality:** the sha256 of each of the five output tables is equal before and after (returns 6,901 rows; class 25,057; account_activity_daily
  6,901; account_lot_realized 35,834; account_lot_unrealized_daily 542,546). Hashes are in `0.9.0_WK_IRPT_DASHBD~85/STAGE_MEMORY.json`.
- **Tests:** the worker reports 200 passed, 0 failed (194 existing, 6 new). The issuer re-ran the new file (6 passed) and the `irpt_reporting` test
  folder (112 passed).
- **No deploy.** `infra/` is untouched. The bytes ride the R45 gold release.

## For L9

1. **The after process peak (1459.1 MB) sits above every stage.** It is reached between stages, in the handler's own table write. The worker did not cut it.
2. **`lots_check` rose,** 945.3 MB to 1214.9 MB. It stays under the largest stage.
3. **D2-W85-S1:** `MEASURED_THRESHOLDS_R1.json` is tracked at neither path the handler reads, so a kit run refuses without it. The worker ran with an
   untracked copy of the pre-crash private file, the same file for both runs. Whether that file is the one the served gold is graded against is not established.
4. **D2-W85-S2:** `client-data-check` blocked `account_return_daily.py` on a docstring account id that predates the order. The worker committed under the
   audited override. The issuer then redacted the line @354214c55f (id to the `acct#<sha8>` token, two per-account figures to `[redacted]`).

## For the CTO's round analysis

The R45 pair was signed on a packet that predates this cut and the docstring redaction. ADDENDUM 20 has the stage cut ride R45, so the R45 release
packet needs a refresh at the new source bytes before the apply. The apply still waits on the Monday R44 acceptance (row W78-S1).
