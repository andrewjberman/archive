# AMGT_RESAPP round 45 close run -- the issuer's real run of FWD-30 on the SERVED plane (2.0.0_SA_COO~Z, post-reboot)

- **Deployed artifact:** opal-amgt-scoped-api CodeSha256 `vBSCqd71wGn1GNOpaWGKr+KdI6t+zo3QVovzEd9Mrew=` (tt-2, LastModified
  2026-09-26T23:35:04Z, LastUpdateStatus Successful), re-read by the issuer with `round45/checks/tt-2.AC1.py` (exit=0) at ~20:05Z on
  2026-09-28, before this sweep. S3 VersionId `0XDw5hJWOYgx3P8CSA42oAlkLuTlupkS`; rollback `T9JIi3D.nKZ5zd_bNaHzOh4_mQWF8.80`.
- **Population:** the LIVE research library, 95 folders, read_at 2026-09-28T20:26:43Z (first line of `sweep.log`).
- **Instrument:** `round45/checks/sweep.py --served --live --require-cases` (the same instrument as `tt-2.AC2.sh`, with the TSV and log
  kept). Sweep rc=0.
- **Result:** served over 95 of 95: OK 95, NOT_OK 0, CAPTURE_FAILED 0; cases page=285 rich=285 same=285 missing=0 extra=0; absences
  missing=0 on 95 of 95 names (`served.tsv`, column `abs_missing`).
- **Page tree:** portal at the PUBLISHED gitlink `c3dd9ca9` (= origin/DEV, contains tt-1's harness commit 4e29386e), in an isolated
  sparse worktree `C:/tmp/r45pub/portal` with `org/`, `lib/` and `node_modules/` junctioned to the workspace. NOT the shared tree: its
  portal DEV is at AMGT_HARVST's LOCAL-only 92a25762, where the harness cannot load the header (row Z-S292 @830ccb3292; a first attempt
  there read CAPTURE_FAILED on 38 of 38 names and was stopped -- that output is not kept).
- **The falsifier's two arms:** abs_missing 86 of 95 before tt-2 (the lane's L3, 2026-09-26T22:04:47Z, CodeSha256 LK9h47ju...DcO4s=)
  -> 0 of 95 here. The planted control (tt-1 AC2's loop over the two pinned pre-fix exports RKT_LN_Equity, AMD_US_Equity), run by
  the issuer at the published tree `C:/tmp/r45pub/portal` @c3dd9ca9 on 2026-09-28 ~21:3xZ: RKT "ABSENCES page=33 rich=32 same=32
  missing=1 extra=0; EXPORT-COMPARE NOT OK"; AMD "ABSENCES page=31 rich=30 same=30 missing=1 extra=0; EXPORT-COMPARE NOT OK" --
  harness rc=1 on both, FOR THE COUNTED ABSENCE. **CORRECTED IN PLACE:** this line first cited `tt-1.AC2.sh` run on the SHARED tree
  (~20:0xZ), where its "YES on 2 of 2" came from the harness CRASH (Z-S292), not the verdict: that script accepts any rc=1 and prints
  empty ABSENCES/EXPORT-COMPARE fields on a crash. The claim was right; its first evidence was not.
- The lane's own AC2 (2026-09-26T23:55:10Z) read the same numbers two days earlier; this run shares the instrument, not the process.
