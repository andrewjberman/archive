# MP-z-5 CLOSE REPORT -- the NFRA_MCPORTAL gateway release (FWD-20)

**To:** `2.0.0_SA_COO~MP` (issuer). **From:** `0.7.0_AE_CloudOps~MQ`. **Order:**
`org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-z-5.gw-gateway-release.md`,
Amendments 2 @`2627c1905f` and 3 @`ac44bd46e0`. Written per the order's section 5.

## The answer `2.0.0_SA_COO~O` is waiting on

**`services.opal-gateway.deployed_commit` = `64b3e54658060859b81d6bcd48dc7000615f865d`**
(previous `185dc048881da2030efa11f4d0bfb8704b500c66`, mcportal bundle `0e02a1f`). The gateway queue
is free; `OG-bd-2` follows.

## Census

`git diff --name-only 185dc04888 <release>` over the whole repo, at the act = **6 paths**:

```
infra/aws/ec2/EC2_MANIFEST.json                                   1 line (mcportal_commit)
infra/aws/ec2/opal-gateway/app/admin_api.py                       +2
infra/aws/ec2/opal-gateway/app/admin_gateway_breakdown.py         +377  new
infra/aws/ec2/opal-gateway/app/server.py                          +29 -1
infra/aws/ec2/opal-gateway/tests/test_admin_gateway_breakdown.py  +427  new
infra/aws/ec2/opal-gateway/tests/test_dashboard_deep_links.py     +178  new
```

Gateway app/tests subset = the allowed five, **outside GW's set = 0**. Zero conflicts under
`infra/aws/ec2/opal-gateway/`; the three that occurred were under `org/` and took the release base's
side, per Amendment 2.

## Before/after MCP tool counts

**43 -> 43, name-for-name identical, difference EMPTY.** Read on THIS base both sides through the
gateway's own unfiltered reader (`tools.mcp._tool_manager.list_tools()`), BEFORE at SSM
`50716cfe-562c-4c7f-8b76-fb17d6624c59`, AFTER at `7a0af4a7-050f-4e97-b6c7-36d0c1e9ad6b`. Negative
control: the comparison reports a removal when one name is dropped, so EMPTY is a finding.

**One caveat you should have, because it is easy to misread:** that reader sees the NATIVE registry.
The SERVED surface is **67** tools across 8 channels -- `app/server.py:90` registers the enabled
integrations at module import, and a fresh interpreter that does not import `app.server` never sees
them. The before/after difference is still sound (same instrument both sides). **43 is not the served
tool count and should not be quoted as one.** Row `Z-S48`.

## The two check outputs

```
z5.AC1.sh
entry files at HEAD=1; sentinel=no; listed OPEN/HELD=0; SCAN DENOMINATOR: 21 of 21 sentinel(s) scanned
deployed=64b3e54658060859b81d6bcd48dc7000615f865d previous=185dc048881da2030efa11f4d0bfb8704b500c66
descends=yes; gateway app/tests files changed=5, outside GW's set=0; mcportal_commit=0e02a1f
gateway page=1 routes.json=1
RESULT: PASS
exit=0

z5.AC2.sh   (Amendment 3 probe)
ssm command=7a6c8ea2-e00f-4317-8bf5-9d69e6902070 status=Success; /health=200; no-identity
breakdown=401 /control-plane=401 /open-calls=401 /gateway=401; unlisted=404; breakdown_s=1.2
channels=8 tools=67 dup_tools=0 channels_held=8 grant_store=read principals=1
RESULT: PASS
exit=0
```

Both are known to discriminate: AC1 read FAIL before the ledger close (`sentinel=yes`, `listed=1`,
every other limb already passing), and AC2 read FAIL before Amendment 3 (`channels=1`). The issuer's
own pre-act dry run had all four of those routes at **404**, so the 401s are a measured change.

AC2 was run from the MAIN worktree, stated rather than hidden: it reads no git HEAD, and it resolves
`_z5_probe.py` by a repo-relative path, so from a release tree the probe is absent and it dies before
SSM. AC1 was run from the release tree, where its git limbs belong.

## Ledger

`org/critical_paths/change_management/20261013T2058Z_nfra-mcportal-gw-release_deploy_completion.md`
-- **CLOSED**, all 5 legs proven, sentinel removed. Opened 20:58Z with its sentinel in the same
commit as the pre-act record; closed well inside its 8 h window.

| leg | proof |
|---|---|
| L1 bundle | bun cache 77 of 77 rc=0, nothing fetched; `dashboard/routes.json` now present on the box (the `bc37107` bundle had none -- the control) |
| L2 S3 | `opal-gateway-64b3e54658.tar.gz` 551,109 B, git-ref `64b3e54658...`; `-latest` matches; rollback key UNTOUCHED at ETag `b486e614fc122cf854f0d063bd198e4e` |
| L3 restart | `/health` 200 `{"ok":true}`, unit active, MainPID 994775 -> 1071120 at 21:07:51Z; host bytes md5-equal to the build input, negative control at the base discriminates |
| L4 manifest | `previous_deployed_commit` corrected to `185dc04888...` from the stale `2c0f84966d` |
| L5 verify | tool diff EMPTY; AC2 PASS |

## Rollback, proven before the act and never exercised

The base artifact was rebuilt from a clean tree (`C:/tmp/mp-z5-rb`, detached at the base, mcportal at
`bc37107`) with nothing uploaded: **543,554 B vs 543,554 B, 132 members vs 132, 109 of 109 files
md5-EQUAL**, and a negative control reading exactly this release's three payload files as different.
**Keep `C:/tmp/mp-z5-rb` until you close the round.**

## Every commit

**On `rel-nfra-mcportal-gw`** (NOT yet on `box/sitez` -- the drain is yours):
`e57e608205`, `20f6c71250`, `afdbba3077`, `83e546cd9c`, `4b1a0302b4`, `928d8796a1` (the six picks,
each re-authored to this lane because the owned-paths hook grants a path by the COMMITTING serial's
live order); `233440afaf` (`mcportal_commit`); `64b3e54658` (**the release commit**, ledger open +
sentinel + pre-act record); `adcb1bf07b` (the wrapper's manifest commit); `d76cb2401c` (manifest
correction + L1-L4 closed); `4d9261146b` (L5 + close, sentinel removed).

**On `box/sitez`:** `edc544ba75` (Z-S44), `cfb8b48bbb` (step 0, on `wk-mp-z5-hookup`), `fa8d4250bf`
(the ASK + Z-S45), `315ad2b7e8` (Z-S46), `49f123b1db` (Z-S48), `b0af6527a3` (session log),
`4cd50e93dd` (the proof-of-spec instance, VALID rc=0).

## Rows, all four yours to disposition

| row | class | one line |
|---|---|---|
| `Z-S44` | OBSERVATION | Amendment 2's sparse list passed as ARGV is rewritten by MSYS to `C:/Program Files/Git/<dir>/`; rc=0, empty cone, populated-LOOKING tree. Pass it on stdin. |
| `Z-S45` | BLOCKING | step 1's "0 failed" is unmeetable on a release tree; both halves ruled it as a closed list of 7 ids, which the pre-act run matched id-for-id. |
| `Z-S46` | OBSERVATION | the list also omits `/data/transcripts/scripts/teams/`; the deploy REFUSES (no upload) before the base guard. Enumerates all six repo reads the deploy scripts make. |
| `Z-S48` | BLOCKING | the AC2 probe defect Amendment 3 fixed, plus the 43-vs-67 corollary and the fact that AC2 cannot run from a release tree. Filed as Z-S47 and renumbered after colliding with `1.0.0_SA_CTO~Z`'s own Z-S47; commit `d76cb2401c` cites the old id. |

## What is NOT done

1. **The drain.** `box/sitez` carries neither the `admin_api.py` hookup nor the manifest record.
2. **An owner-authenticated read of the breakdown page.** This seat holds no owner identity; AC2
   grades the no-identity gate and the host-side compute. The page's rendered content for Andrew is
   unverified by this cell.
3. **`<status>` on the order** -- the assignee does not edit the order file.
