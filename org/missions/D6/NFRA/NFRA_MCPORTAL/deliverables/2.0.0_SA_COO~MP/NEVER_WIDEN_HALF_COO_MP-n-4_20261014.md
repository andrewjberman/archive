# NEVER-WIDEN HALF (COO) -- NFRA_MCPORTAL.TO-MP-n-4 -- SIGNED, with two dispositions

**Signer:** `2.0.0_SA_COO~MP` (the issuer), 2026-10-14 ~01:1xZ.
**ASK:** `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~MQ/NEVER_WIDEN_ASK_MP-n-4.md` @`3f7f1097e7`,
read whole. Release branch `rel-nfra-mcportal-c17r2` @`87beffddc5` on live base
`7eff14b2e620c8c1f688d41de6f37c09addde7b4`. GO commit `9d42320595`. Bundle unchanged (`0e02a1f`).

## What this half signs

The ASK's sections 1 and 2, unchanged. One module ships: `app/admin_fabric_gitstate.py`. Its test is source only. There
is no route change and no bundle change; there is one restart and there are two S3 keys. It may not touch the MCP tool
surface, any IAM, any store write, the producer `.tools/fabric-gitstate.py`, any Terraform or other infrastructure, any
other manifest service, `mcportal_commit`, or the two deploy scripts.

## The blast radius, read by this seat

- **Census.** `git diff --stat 7eff14b2e6 87beffddc5` over the whole repo reads 2 files, +86/-52: the module and its
  test. This matches ASK section 3, and the change is GO commit `9d42320595` alone.
- **Tests.** The release-tree failures are 2, and both meet Amendment 1's mechanism as the ASK shows it: each is a
  `FileNotFoundError` on a path outside the gateway dir, `ls-tree` 0 at the base and 1 at HEAD, and the test passes at
  HEAD (21/0 there). There is a positive control as well. Admitted.

## Disposition of ASK section 1, branch B -- "not recorded" for a box with no pointer: ACCEPTED, with this seat's measurement

The order names this behaviour in its own blast radius ("boxes with no pointer read 'not recorded'"). It is the C17R2
semantic the decomposition was cut on, so it is not a widening. The ASK says branch B is unverified against a real box,
so this seat measured it, at ~01:1xZ, with `head-object` on `opal-313476888478-globgrph`
`fabric/activity/v1/gitstate/box=<B>/last_integrate.json`, return code read on each:

| box | pointer |
|---|---|
| laptop | PRESENT (rc 0), LastModified 2026-10-14T01:01:57Z, 187 B |
| sitez | ABSENT (rc 254, 404) |
| dell1 | ABSENT (rc 254, 404) |
| dell2 | ABSENT (rc 254, 404) |

The control: every box's `latest.json` reads rc 0, written between 00:56Z and 01:04Z, so the reader can see the prefix.
A `list-objects-v2 --query KeyCount` read returned `None` for all four, including laptop, whose head succeeded. That
instrument is broken through the shim and was discarded. The writer puts the pointer on `--mode integrate` only
(`.tools/fabric-gitstate.py:21`).

**So, from the restart, branch B is the answer for 3 of 4 boxes. It is not an edge case.** Condition B-1: in the close
report, record each box's `integration_refused` value from the served `_compute` BEFORE the act and AFTER it, with a
four-row table. A box that changes from a stated refusal to "not recorded" is named as such. The table is so that
Andrew's Control Plane read at the MC Portal sitting (call 21d9) is not surprised by it. Nothing in this condition
blocks the act.

## Disposition of ASK section 7 (row Z-S49, the misattributed live record): ACCEPTED as stated

Step 4 writes `previous_deployed_commit = 7eff14b2e6...` and this release's own `release_note`, which repairs both
fields going forward. The MX-r-11 generation's history (`previous_deployed_commit` `ad2acc0a93`, a release-chain commit
that never served, where `64b3e54658` was the real previous) belongs to NFRA_MCPINDEX's record. This seat tells
`2.0.0_SA_COO~MI` so. MP-n-4 does not edit it. That AC1's chain limb cannot detect a wrong-but-ancestral value is
noted, and it is the same instrument limit for every GW and C17 release. It is not changed mid-round.

**CORRECTION (this seat, 2026-10-14 ~01:1xZ, after `2.0.0_SA_COO~MI` msg 33876).** The paragraph above is wrong on one
point: `ad2acc0a93` DID serve. It was MX-r-11 v1, live from 22:51Z to 23:49Z: the `-latest` git-ref read 22:51:29Z, and
the host census read 107/107 at 23:32Z (SSM 62336125). The chain is `64b3e54658 -> ad2acc0a93 -> 7eff14b2e6`, so the
live record's `previous_deployed_commit` is correct. Only the stale `release_note` stands, and `0.7.0_AE_CloudOps~MI` is
correcting it. The signature is unaffected, because step 4 still writes `previous = 7eff14b2e6` forward.

## Conditions

1. **Time:** open the NEVER-2 entry no later than 10:00Z and close it by 10:30Z, or do not start (issuer msg 33856;
   `2.0.0_SA_COO~O` msg 33855).
2. Re-read the rollback key `opal-gateway-7eff14b2e6.tar.gz` (ETag `c8b27c104c2f95a6108eece752ccef66`) and the
   manifest's `deployed_commit` immediately pre-act. If the live commit is no longer `7eff14b2e6`, STOP and re-cut.
3. Condition B-1 above.
4. ~~A FAIL there is a finding to report, not a reason to roll back~~ **WITHDRAWN 2026-10-14 ~01:1xZ (0.7.0_AE_CloudOps~MQ
   msg 33878).** The CTO half @55db595800 says "if it fails, report it measured and roll back". The two halves are a
   conjunction, so the stricter one governs. If AC2 misses the 5 s bar, report the measured cold time and the fetch
   count, then ROLL BACK with the named command.
   **SUPERSEDED the same minute, because the messages crossed. This half now ADOPTS the CTO half as amended @e77ac5d642
   (msg 33882), word for word, so the two halves agree.** An AC2 time FAIL is graded FAIL and reported as measured, with
   NO rollback, provided `/health` and the tool surface hold. Guard: a cold `_compute` SLOWER than the base's 9.7 s, or
   0 boxes recorded, means the rollback runs. A FAIL that is no worse than the base opens a row.

## Verdict

**SIGNED.** This half binds the blast radius above. Branch B is accepted, with its 3-of-4 measurement. Section 7 is
accepted as stated.
