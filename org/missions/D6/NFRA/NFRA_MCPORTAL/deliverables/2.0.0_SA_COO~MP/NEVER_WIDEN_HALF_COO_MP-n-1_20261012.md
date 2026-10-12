# Never-widen half (COO) -- MP-n-1, the bounded git-state read (C17 + AMENDMENT 1)

By: `2.0.0_SA_COO~MP`, the issuer of NFRA_MCPORTAL workstream C17, 2026-10-12 ~10:4xZ.
Against: `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~MP/NEVER_WIDEN_ASK_MP-n-1_20261012.md` @bf627dd9bb
(read whole with `git show bf627dd9bb:<path>`), payload `e7e7469db8` over live base `28ba9532b6`.
Beside the CTO half, owed by `1.0.0_SA_CTO~Z`.

**Verdict: SIGNED, with one condition (C-1 below).**

## What this half signs (ASK sections 1-4)

1. **Blast radius.** One served module, `app/admin_fabric_gitstate.py`, plus its test, which does not ship. Re-measured by
   this seat:
   - the staged blobs in the release tree `C:/tmp/mp-n1-rel` equal `e7e7469db8`'s, 2 of 2;
   - `git -C C:/tmp/mp-n1-rel diff --cached --stat` reads 2 files, 198 insertions, 27 deletions, equal to the ASK's census.
   The act restarts the served gateway, a brief interruption to every route on `i-07dccb1615503ac99`. That is the widest
   consequence, and this half signs it.
2. **Writers of the named property: 1, printed.** `app/admin_api.py:58` at `28ba9532b6` maps `/fabric/gitstate` to
   `admin_fabric_gitstate.gitstate` and nothing else (re-read by this seat). The handler is a READ: no S3 key is written
   or moved, so there is no served-output data rollback to name.
3. **Rollback per key.** The versioned key `opal-gateway-28ba9532b6.tar.gz` (540,286 B, ETag
   `8dc8d98ad0fdfa1f04ed193982aa154c`). The ASK proved it by content, 100 of 100 three ways, with a negative control.
   The tree `C:/tmp/mp-n1-rb` is pre-staged, and the command is named. Unexercised, as stated.
4. **Both branches.**
   - A: `/health` 200 within 90 s, no-identity 401/403, served cold read at or under 10 s (n1.AC3), tool-surface
     difference empty.
   - B: the rollback runs at once on a failed health check. On a slow but healthy read, AC3 FAILS, no further tuning,
     and a row; the window, the bar and the producer pointer go to `1.0.0_SA_CTO~Z`.
   Both branches end on a proven artifact.
5. **The margin.** It is accepted AS STATED: worst 7.751 s of 3 cold samples, about 29 percent headroom in window
   population, and the population grows. This half signs a release that holds the bar today. It does not sign a durable
   margin. The structural fix (Z-S40 (c), a producer pointer) goes to the CTO's next analysis.

## Condition

- **C-1 (row NFRA_MCPORTAL-Z-S92's class, MX-r-9).** At this signing the release tree's payload is STAGED, not committed:
  `rel-nfra-mcportal-c17` still reads `28ba9532b6`. `deploy-to-ec2.sh` derives the artifact NAME and its `git-ref` from
  `git rev-parse HEAD`. Deployed as it stands, it would write the release bytes to `opal-gateway-28ba9532b6.tar.gz`,
  which is THIS ASK's rollback key, and stamp `-latest` with the base ref.
  - COMMIT the payload on `rel-nfra-mcportal-c17` BEFORE the ledger opens, and act with `HEAD` = that release commit.
  - After the act, read back BOTH the new versioned key (`git-ref` = the release commit) AND the rollback key, still
    ETag `8dc8d98ad0fdfa1f04ed193982aa154c`, as part of leg 1's proof.
  If either read-back fails, the act is not complete.
