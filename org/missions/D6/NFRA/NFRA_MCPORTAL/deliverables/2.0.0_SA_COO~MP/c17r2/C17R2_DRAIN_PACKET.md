# NFRA_MCPORTAL -- C17 ROUND 2 DRAIN PACKET (L8 input) -- 2.0.0_SA_COO~MP, 2026-10-14 ~02:4xZ

**Workstream:** C17, round 2: the bounded git-state read made structural with a per-box integrate pointer. The rows
behind it are Z-S37 to Z-S40, and Z-S40 option (c) is the pointer. **Risk:** WORLD on the release cell (MP-n-4), and
LOCAL/SERVED on the build cells. **Judgment criteria:** none this round.

## Orders: 4 of 4 terminal

| Order | What it built | Drained / landed |
|---|---|---|
| MP-n-2 | the gateway reader: `_refused` reads `box=<B>/last_integrate.json`, one get per box, with no window scan | worker `9d42320595`, drained @a0b6ed638e |
| MP-n-3 | the producer: `.tools/fabric-gitstate.py` writes the pointer on `--mode integrate` only | worker `aa1e12bdcb` / `3eb2c2c20d`, drained @2bf26f182e |
| MP-n-5 | the deploy helper keeps `previous_deployed_commit` (the recurring wrapper defect from MP-x-4, MP-r-2, MP-n-1 and MP-z-5) | worker `b739bbc9f9`, drained @4c7e933975 |
| MP-n-4 | the gateway release of MP-n-2 | LIVE at `b0c75d24f11808d1de4f70fcca5d39216282054a` (previous `7eff14b2e6`). Ledger `nfra-mcportal-c17r2-release` CLOSED 3 of 3, landed @af71482ff8. Manifest record @dfc2e769f1. AC1 PASS, AC2 PASS, instance VALID |

`python .tools/round-close-check.py --project NFRA_MCPORTAL --round 2 --workstream C17` at ~02:3xZ reads: 4 orders, 4
complete, proof_ok 4, judgment 0, reviewer `3.0.0_SA_CVO~Z` present, **verdict=MAY-CLOSE**.

## The one real run (the outcome's real entry point)

**On the host (the assignee's AC2, SSM):** the SERVED module's cold `_compute` under the instance role, against the
live store, read **1.3 s / 136 body fetches, recorded=4**, against the 5 s bar. The base `7eff14b2e6` read **9.7 s /
1,336** at the issuer's dry run.

**On this box (issuer, ~02:3xZ):** the released module `app/admin_fabric_gitstate.py` (blob equal to the release, 2 of 2
files) ran `_compute()` from `infra/aws/ec2/opal-gateway` against the LIVE store
`s3://opal-313476888478-globgrph/fabric/activity/v1/gitstate/`:

| box | integration_refused | unpushed | record at |
|---|---|---|---|
| laptop | not recorded | 0 | 2026-10-14T02:37:19Z |
| sitez | not recorded | 0 | 2026-10-14T02:32:25Z |
| dell1 | not recorded | 0 | 2026-10-14T02:34:25Z |
| dell2 | not recorded | 0 | 2026-10-14T02:26:12Z |

The cold read on this box was **2.2 s**: a different box, a different credential plane and a different network path from
the host's 1.3 s. Both are far under the bar.

**"not recorded" on 4 of 4 is the designed reading, measured and not assumed.** Laptop HAS a pointer (rc 0, written
01:01:57Z), and the module's rule makes rc 0 read "not recorded". sitez, dell1 and dell2 have NO pointer: `head-object`
returned 404 (rc 254) on each, with every box's `latest.json` reading rc 0 as the control. The writer fires on
`--mode integrate` only. **Never exercised this round:** the refusal branch (rc != 0). No box records a refusal, and
no cell may write a pointer. The COO half of MP-n-4, condition B-1, records the before and after: 4 of 4 unchanged.

## Rows filed this round, or touching it

- `Z-S49` (OBSERVATION, INERT): the live gateway record was inconsistent after MX-r-11 v2. It was CORRECTED IN PART by
  `Z-S50`: `previous_deployed_commit` `ad2acc0a93` DID serve (MX-r-11 v1, 22:51Z-23:49Z). The stale `release_note` was
  fixed by its owner, NFRA_MCPINDEX's `0.7.0_AE_CloudOps~MI`, @642fe57f1d.
- `Z-S50` (OBSERVATION, INERT): the correction above.
- MP-n-4's step 1 used Amendment 1 @46d8c2160d (the Z-S45 mechanism, applied before the GO). Two release-tree failures
  were admitted on it, each shown with its `ls-tree` 0/1 counts.
- The two never-widen halves crossed once on the AC2 rollback rule: withdrawal @b40848b9c9, then adoption of the CTO's
  amended rule @28683249be. This was resolved before the act. It changed no grade.

## Not done here

- C17 round 2 adds no judgment criterion. Andrew sees the faster panel at the one MC Portal sitting (call 21d9), which
  also grades FWD-20 (GW round 1, MP-z-6) and the CP2 close run (MP-q-1).
- GW round 1 is NOT closing with this packet: MP-z-6 is staged on Andrew's read.
