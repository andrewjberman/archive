# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-380 + IB-pr-381: ONE directory release (runner carries source-removed entries TERMINATED; refresh reads the served directory as previous state) + the per-firm seeding run

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-09 ~01:5xZ | **Signed against:** packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~189/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-380_381.md`,
**blob d60e4a9a752780ab490a72d783ad55a531da9f49** | **Release pin P: 7f31bbfa4e06dfcb48af06fea3e20ea9f3606129** (contains IB-pr-380's
8953eccfca) | **Ruling:** CTO msg 1988 (ONE release under one pair, live before cottonwood's 2026-10-12 OVER_AGE).

## Writers of the property

The served directory (`investor-reporting/directory/<as_of>/directory.json` and `latest.json`, three firm buckets) has **1 writer**:
`directory_runner.land`, run on host i-02448edb624a7a7cf under `mdpf-daily-runner-ec2-role`. All 33 of 33 live versions match a runner SSM
command. The refresh function writes only `_refresh/*`. So 1 rule is read: the runner's `land`. The served inflection as_of 2026-10-08 after
a failed refresh is the runner's own landing, because the verdict does not gate the artifact. That is row S4, below.

## Blast radius signed

1. **`irpt-directory-refresh`**: built at P as `6eOFTopG9nvfjpJFJxtBNAUL43pBmg0YvHv9sbErfsM=`. One member changes, `refresh.py`. It is
   deployed through Terraform (safe-apply). No route, IAM, schedule or env change.
2. **Runner bundle** `s3://opal-data-mdpf/code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz`: built sha256 `2e3e6648...b968`,
   md5/ETag `b0356a757b1ae92e3a4b46a847378315`. One of 12 members changes, `directory_runner.py`. It is minted by
   `bash .tools/safe-deploy.sh data/assets/scripts/gold/investor_reporting/directory_runner.py`, whose upload verifies the ETag and every stamp.
   Its effect on the served bytes by itself: the next scheduled landing adds `source_client_ids`, about +7 percent of bytes. It carries
   nothing, because the served directories already lack the entry.
3. **The seeding run, signed here at BOTH sub-branches (row S1).** One runner run per firm on the runner host, after 1 and 2 are live, and
   never inside the scheduled window (09:30-09:50 ET):
   - inflection with `--previous-key investor-reporting/directory/2026-09-25/directory.json`;
   - cottonwood with `--previous-key investor-reporting/directory/2026-10-05/directory.json`.

   The write set per firm is the dated `directory.json` of the date the runner selects, plus `latest.json`. That is four objects in two
   buckets.
   - **Same-date sub-branch:** inflection `2026-10-08`, cottonwood `2026-10-07`. Each OVERWRITES the existing dated key. The landed bytes
     equal the existing build plus the carried TERMINATED entry and `source_client_ids` (replay: inflection 294 -> 295, cottonwood
     269 -> 271).
   - **New-date sub-branch:** the source frontier has moved, so a NEW dated key is written and `latest.json` points to it. That is the same
     build a scheduled run would land that day, plus the carried entry.

   Both sub-branches are read from the runner's own rule, `select_business_date` + `land`, not predicted. Each is rolled back by restoring
   the S3 versions read at packet time (01:27Z), with `latest.json` last:
   - inflection `latest.json` `IYqf.x8WewTTcvKkxAzng.pnzpluzixY` and `2026-10-08/directory.json` `qYXlj1pZA2qavf2ZJb.hLGX6YGQ5d3av`;
   - cottonwood `latest.json` `xWWAVr3R60LNikXNfX450gx7LHfiXWFW` and `2026-10-07/directory.json` `2c0mqQRRHGyS5e2lqj1Usl5Un_0550Gs`.

   A new-date key is rolled back by deleting that one version, which is an S3 delete for the human confirmation the workspace law reserves.
   Overwriting with the prior build, while `latest.json` is restored, serves the same bytes with no delete, and that is the default.
   49financial is not seeded.

## Measured by this seat

- `p93_cells.py` at 022c5a2865: `IB93-1-AC1 PASS` (1 writer), `IB93-1-AC2 PASS` (runner `-k terminated_carry_forward` 23; directory
  `-k previous_state_served` 10; directory suite 211; runner suite 364 + the one pre-existing red excused by AMENDMENT 1), and
  `IB93-1-AC3 PASS` (both firms READY, terminated 1, carried in the landed directory; live REFRESH_FAILED; inflection's 10-09 fire finds
  its previous state with 0 false additions).
- The S71 guard is red at base 2c1f4f425d: 1 failed, 2 passed, in a clean worktree run by this seat.
- IB-pr-380 (`p92_cells.py`): 3 of 3 PASS at its own pin.

## Branch A and Branch B

- **A:** steps 1-3 as signed. After them, a driven refresh is READY at all 3 firms, read at each manifest's own as_of, with
  `terminated_count` 1 at inflection and cottonwood and 0 at 49financial. The served directory of inflection and cottonwood carries the
  entry marked TERMINATED. 49financial's first landing with the new bundle is read for `source_client_ids` present. Its path was not
  replayed, because this seat cannot assume `irpt-49f-directory-read-role` (row S5).
- **B:**
  - refresh: redeploy S3 version `Ntv3Br2YU3utvESdPFCiTMkVVatmyzxY` (CodeSha256 `RbpsijC23XVUFPE0W34Gr/xqtDil94xYRqDuuZlaYx8=`) through
    Terraform;
  - bundle: copy back version `JITP9ecNeQyAnAmKo90oxqWyFemEqVaI` (ETag `7de9bbd5...`);
  - seeded keys: restore the four versions above.

  A rolled-back runner no longer carries, so a restored directory stays restored.

## Sequencing (one apply order to `0.7.0_AE_CloudOps~DELL2`)

1. The packet's replay arm against the artifacts in play, BEFORE the ledger. Any stop condition in the packet ends the order.
2. The ledger opens.
3. Bundle and refresh land, each verified live: the ETag equals the md5, and the CodeSha256 equals the built sha.
4. The seeding run, inflection then cottonwood, each followed by a read of the landed dated key for the carried entry.
5. The driven refresh after-read.
6. The ledger closes.

The deadline is live before 2026-10-12 (cottonwood OVER_AGE), in practice by Friday 2026-10-09's close.

## Noted, not widened

- **Row S4:** the runner lands a build-fault directory even when the refresh then says REFRESH_FAILED, because the verdict cannot gate the
  artifact. That is TODAY's behaviour, unchanged by this release, and the reason the served directories lost the entry. This pair does not
  widen it. It goes to the CTO as a separate call: whether the runner should refuse to land when an entry in the source is missing from the
  build.
- **Row S71** (the holdings re-arm guard) is red on the live world, independent of this release. The bundle change touches only
  `directory_runner.py` and no `irpt_holdings_*` bundle.

**Verdict: GIVEN**, for exactly this write set at this pin and packet blob, both sub-branches of step 3, and the sequencing above.

-- 2.0.0_SA_COO~P2
