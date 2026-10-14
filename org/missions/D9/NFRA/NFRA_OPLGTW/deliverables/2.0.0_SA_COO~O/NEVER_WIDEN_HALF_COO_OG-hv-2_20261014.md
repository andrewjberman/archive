# Never-widen half (COO) -- OG-hv-2, the harvest read grant and the gateway release of `harvest_list` / `harvest_read`

By: `2.0.0_SA_COO~O` (issuer), 2026-10-14 ~13:4xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-hv-2.md` (sha256 9283dd71, read
at `013844d3e6` and at the working tree: equal), release `7c558b4e2176a632d13e6301af3e06d434aa1540` on branch
`rel-nfra-oplgtw-hv`, base = live `90967e39ba4bdca17c6f84d9806c29cc67f8482e`; grant file
`infra/aws/terraform/opal-gateway/harvest_read_iam.tf` (sha256 52e2ed23, equal at both reads).

## SIGNED at `7c558b4e21`, on conditions C1-C3

What this seat read at signing:
- **hv2.AC1, issuer re-run: PASS.** Base is the live ref 90967e39ba (manifest `deployed_commit`). 7 files differ, 0 outside
  OG-hv-1's seven. `harvest_read.py` byte-equal to HEAD. Grant: 24 of 24 object prefixes = `SERVED_PREFIXES`, 24 of 24 in the
  list condition, 0 non-read actions, 0 bucket-wide ARNs, builder name present, attached to the internal reader role.
- **The release is OG-hv-1's change and nothing else, measured here:** `git diff 90967e39ba 7c558b4e21 --
  infra/aws/ec2/opal-gateway | git patch-id --stable` reads `aa0b9e3505c3`, the same as OG-hv-1's own gateway diff
  (`4e26a29872~1..4e26a29872`).
- **Who gains and who loses** (ask section 2): W1, the gateway's reach grows to 24 harvest prefixes for Opal principals only,
  `raw/` included (Andrew, call 8). W2, `gateway-global-internal-reader-role` gains its own read on `opal-data-harvest`; its
  trust policy names exactly one assumer, `opal-gateway-role`. Nobody loses a grant.
- **The honest risk is read as the ask states it:** the Opal-only boundary is a code gate (`_is_opal_user`), not an IAM
  gate. This half signs on it because `test_oghv1_ac02` and `ac04` hold it and AC2's live negative arms exercise it.
- **Order of acts** (ask section 0): the grant first (it creates no reachable state before the code lands), then the
  deploy. This half covers BOTH orders' branches only in that order.
- **Rollback** (ask section 9): ACT 1 `delete-role-policy` of the one name; ACT 2 redeploy `90967e39ba`, whose parity with
  the host is measured at 105 of 105.

**C1 -- the ask stays at its bytes through the GO.** sha256 9283dd71 for the ask and 52e2ed23 for the grant file. A byte
that moves re-opens all three halves.

**C2 -- the served read is real.** `W/HV2_SERVED.json` comes from `harvest_read` through the INSTALLED code on the host, and
the IAM simulation (`role` = `gateway-global-internal-reader-role`, `packs` allowed, `wsj_harvest` allowed, the unlisted
control `implicitDeny`) is read after the apply. A simulate alone never closes AC2.

**C3 -- the queue, the window and the targeting.**
- ACT 1 is `safe-apply` targeted at `aws_iam_role_policy.int_reader_harvest_read` ONLY, and the plan read immediately
  before it shows 1 to add, 0 to change, 0 to destroy. Any other line is a STOP. (`market_update_gateway_put` in the same
  directory is deliberately never applied; an untargeted apply would land it.)
- ACT 2 runs inside 11:00Z-23:00Z, with the ledger entry and sentinel opened first, and only while live `deployed_commit` is
  still `90967e39ba` with no other gateway release in flight across all worktrees (per-tree denominator printed). If the
  live base moved, this half does NOT carry: the release is re-cut on the new base, hv2.AC1 re-runs, the diff's patch-id is
  compared to `aa0b9e3505c3`, and the halves re-sign.

## Not covered

- Any typed harvest tool (the G1 cells ride `OG-ap-18`, their own ask).
- AC3, the real asset manager's call (judgment, `3.0.0_SA_CVO~Z`).
- Any other gateway change, any catalog edit, any grant-store write.

-- 2.0.0_SA_COO~O
