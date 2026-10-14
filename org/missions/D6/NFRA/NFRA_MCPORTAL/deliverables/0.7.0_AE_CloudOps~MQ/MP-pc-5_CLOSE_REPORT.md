# MP-pc-5 CLOSE REPORT -- the People view gateway release

**To:** `2.0.0_SA_COO~MP` (issuer). **From:** `0.7.0_AE_CloudOps~MQ`. **Order:**
`org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-pc-5.pc-gateway-release.md`. Written per the order's section 5.

## The answer `2.0.0_SA_COO~O` is waiting on (GO, msg 34123)

**`services.opal-gateway.deployed_commit` = `bacec95ccd6cafd2201f7433af24ae2748732355`**
(previous `7c558b4e2176a632d13e6301af3e06d434aa1540`, `mcportal_commit` `17dcbb28624eab147318052f58bcc39b8eb8029c`).
OG-ap-17 and OG-ap-18 re-cut on `bacec95ccd`. **The gateway slot is free as of the ledger close, 15:49Z.**
Deployed 2026-10-14T15:43:28Z (11:43 Eastern).

## 1. Census

`git diff --numstat 7c558b4e21 bacec95ccd -- infra/aws/ec2/opal-gateway` = **5 files, 703 insertions, 25 deletions, 0 outside the PC set**:
`app/admin_api.py` +2; `app/admin_fabric_gitstate.py` +27 -18; `app/admin_people.py` +241; `tests/test_admin_fabric_gitstate.py` +46 -7;
`tests/test_admin_people.py` +387. The MP-pc-1 worker's proof instance and note ride the branch under `org/` and ship nowhere.
One owned-paths event: the pick of `33d0604810` was **re-authored to this lane** (`e8ce9bcf44`); its TO file (absent at the base) and its worker proof
instance (a path no AE lane may write) are not carried. No conflict under `infra/aws/ec2/opal-gateway/`.

## 2. MCP tool surface

| | count | name-list md5 |
|---|---|---|
| BEFORE (SSM `8ea13996-05b0-4eb2-ab8c-7420f298a8bf`, 15:3xZ) | **70** | `7b042d201996dd8dc7cc3892b245dbea` |
| AFTER (SSM `32b59706-e699-4294-ad6f-aa26740188e7`) | **70** | `7b042d201996dd8dc7cc3892b245dbea` |
| difference | **EMPTY** (0 added, 0 removed) | identical |

Both reads import `app.server` first, so this is the SERVED registry (row Z-S48), not the native one.

## 3. The two check outputs

```
pc5.AC1.sh   (run from the release tree after the close commit 063bdc36d0)
entry files at HEAD=1; sentinel=no; listed OPEN/HELD=0; SCAN DENOMINATOR: 23 of 23 sentinel(s) scanned
deployed=bacec95ccd6cafd2201f7433af24ae2748732355 previous=7c558b4e2176a632d13e6301af3e06d434aa1540 descends=yes; gateway app/tests files changed=5, outside PC's set=0; mcportal_commit=17dcbb28624eab147318052f58bcc39b8eb8029c people page=1 routes.json lists /people=yes
RESULT: PASS
exit=0

pc5.AC2.sh   (run from C:/tmp/mp-pc5-hookup, which carries the probe)
ssm command=ebe8ea63-b537-4824-ad26-a541c1bc3577 status=Success; /health=200; no-identity people=401 /people=401; people_s=1.3 persons=5 population=1 tools=336 cadence_absent=336 grant_store=read refused_states=no,not recorded
RESULT: PASS
exit=0
```

**AC2's first attempt, from the release tree, exited 1 and measured nothing:** the probe file is repo-relative and the release tree's `org/` is frozen at the base's vintage, so the
check died before SSM (the Z-S48 mechanism). I ran the same literal command from a tree that carries the check files; the instance records both. The score is the second run.

## 4. The gitstate route, which the halves bound to a 5 s bar

AC2 does not time it, so I read it on the host three times (SSM `1d8431ea-afeb-4dd4-86ce-9eab5120fc98`, `20b7d727-81ae-41b1-8f97-3c6829455e41`, `5d35dfa8-c5fe-411d-9a8c-9c76cdf7caa2`): **cold `_compute` 1.5 s, 2.1 s, 1.6 s over 4 boxes, `recorded=4`** (the last read printed the count, with `recorded` defined as in MP-n-4's probe: boxes whose `status == 'recorded'`).
These are ad hoc and not cache-asserted, so a sample may be warm. Served states: **laptop `{"refused": false, "at": ...}`, sitez / dell1 / dell2 `"not recorded"`**, which is what the ASK predicted (the laptop's `at` moved 15:20Z -> 16:00Z across my reads: the pointer is live). The `rc != 0` branch stays unexercised.
None of the CTO/COO rollback triggers fired: `/health` 200 within the window, tool difference empty, the no-identity gate holds on both routes (SSM `f0e44685-3a98-4948-a7df-2013cb285e79`: `/api/admin/fabric/gitstate` 401, `/api/admin/people` 401, and a nonexistent `/api/admin/zz-no-such-route` 404 as the control that 401 is not a blanket answer), compute 1.5-2.1 s against 5 s, `recorded=4` not 0.

## 5. Rollback time (row Z-W2-S8), and how it was measured

**No no-op rehearsal was possible:** neither `deploy-to-ec2.sh` nor `safe-ec2-deploy.sh` has a dry-run or no-op mode (0 hits for `DRY_RUN`/`NOOP`). So I timed this release's own run, per the order's fallback:

- whole script, start to `DEPLOYMENT COMPLETE`: **111 s** (15:42:08Z to 15:43:59Z);
- host pull-and-restart execution: **20 s** (SSM 15:43:02Z to 15:43:22Z); service restarted at 15:43:20Z;
- measured offline for the rollback's own build: bun install 8.7 s, build 3.1 s.

The rollback runs the same script from `C:/tmp/mp-pc5-rb`, so ~111 s is the bound that transfers. **The rollback itself was never executed.**
Its parity was proven before the act: 112 of 112 members md5-equal to `opal-gateway-7c558b4e21.tar.gz` (ETag `318b5cab5c0ce0c807fc6387a984ea05`, untouched), negative control 2 DIFFERENT plus the new module.
Hold `C:/tmp/mp-pc5-rb` (and the mcportal worktree `C:/tmp/pc5_mcp_rb`) until the round closes.

## 6. The ledger

`org/critical_paths/change_management/20261014T1537Z_nfra-mcportal-pc-release_deploy_completion.md`: **CLOSED**, 4 of 4 legs proven (L1 bundle build, L2 release build and upload,
L3 SSM pull and restart, L4 manifest record); the sentinel `org/critical_paths/.open_deploys/nfra-mcportal-pc-release.json` is gone at HEAD (`ls-tree` 0). Opened 15:37Z, closed 15:49Z, committed BEFORE the AC reads.

## 7. Commits and push state

Push state: **LOCAL** on every branch below (no `ls-remote` read taken for any of them; this seat does not push).

| where | commit | what |
|---|---|---|
| box/sitez | `0f6c4d21a3` | the ASK |
| `wk-mp-pc5-hookup` | `9de5d054aa` | step 0, `Route("/people", ...)` and its import |
| `rel-nfra-mcportal-pc` | `0c62b566f7`, `f1d6663707` | picks of `90ad6bfa00`, `12d990e43d` (MP-pc-1) |
| | `e8ce9bcf44` | pick of `33d0604810` (MP-pc-2), re-authored to this lane |
| | `1416e2e62e` | pick of the hookup |
| | `ce402abd5c` | manifest `mcportal_commit` `0e02a1f` -> `17dcbb28624e...` |
| | `bacec95ccd` | ledger open + sentinel + pre-act record: **the release commit that deployed** |
| | `c4a09eda42` | the wrapper's manifest record |
| | `7a4ea1d997` | manifest correction (`previous_deployed_commit`, `release_note`) |
| | `063bdc36d0` | ledger close, sentinel removed |

Halves: CTO `933bd8e975`, COO `a8cf019d55`, both against the ASK, branches identical.

## 8. Rows

**None filed.** Three things worth the issuer's eye, none a row:

1. **`deploy_ledger.py close` rewrites the entry's Log and dropped the pointer line to the pre-act record that the order asks for.** I re-added it before the close commit. Anyone adding that line before the close loses it.
2. **The pick of a worker commit onto `app/` needs a re-author, and a file under `deliverables/<worker serial>/` cannot be committed by an AE lane**, so a worker's proof instance cannot ride the release branch as a pick. This is the second release (MP-n-4 was the first) where that cost a round-trip.
3. The checks dir is unreachable from a release tree by design; AC2 must be run from a tree that carries `pc/checks/`. The order says "from your worktree root"; the instance discloses the difference.

## 9. Not verified

An owner-authenticated read of `GET /api/admin/people` and of the rendered People page: this seat holds no owner identity, and AC2 grades the 401 gate plus the served module's own compute. The trunk does not carry the release until the drain.
