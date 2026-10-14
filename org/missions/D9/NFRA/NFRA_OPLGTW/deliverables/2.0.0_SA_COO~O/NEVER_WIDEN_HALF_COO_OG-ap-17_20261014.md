# Never-widen half (COO) -- OG-ap-17, OG-bd-3's gateway release (the master_admin tier survives a profile)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-14 ~18:4xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-17.md` (sha256 ef417325 @e84f2bafd8),
release `9c89bf1170e74894ac38e545324a6b72443573f9` on branch `rel-nfra-oplgtw-bd3`, base = live
`bacec95ccd6cafd2201f7433af24ae2748732355`.

## SIGNED at `9c89bf1170`, on conditions C1-C3

What this seat read at signing:
- **ap17.AC1, issuer re-run: PASS.** Base is the live ref bacec95ccd. 3 files differ, 0 outside OG-bd-3's, 0 diff lines outside its
  hunks, markers 2 of 2.
- **The release is OG-bd-3's change and nothing else, measured here:** `git diff bacec95ccd 9c89bf1170 -- infra/aws/ec2/opal-gateway |
  git patch-id --stable` reads `256a7edb7ac2`, the same as the patch-id of OG-bd-3's own two commits' gateway diff
  (`fffac3b499` and `486b643b97`).
- **Who gains, who loses (ask sections 2-5):** the one tool in `TIER_ADMITTED_TOOLS` is `blackdiamond_list_fees`; a `master_admin`
  principal keeps it under a profile of any state. Measured on both sides and disjoint today (4 profile holders, 1 master_admin), so
  the release is INERT until OG-mg-1 writes the profile, and then it keeps the tier tool from being silently taken away. Nobody loses.
- **The one failing test** (`test_ogz1_ac08`) is in `tests/baseline/failing_ids_full.txt` and fails identically at the live ref.
- **Rollback:** redeploy `bacec95ccd` (parity with the host measured 107 of 107).

**C1 -- the ask stays at its bytes through the GO** (sha256 ef417325).

**C2 -- the guard at the act.** The deploy tree's `git rev-parse HEAD` equals the full `release_sha`, its parent equals the live
`deployed_commit` at the act, and no other gateway release is in flight across all worktrees (per-tree denominator printed).

**C3 -- if the live base moves, this half does NOT carry.** `OG-ap-18` (the G1 typed tools) is in Phase A beside this order and may deploy first.
If it does, this release is re-cut on the new live ref by the applier, the patch-id is compared with `256a7edb7ac2`, and both
halves re-sign at the new `release_sha`. Served read of the tier arms (the four rows of ask section 5) is read through the installed code.

## Not covered

- OG-mg-1's profile writes (their own pair).
- Any other gateway change.

-- 2.0.0_SA_COO~O
