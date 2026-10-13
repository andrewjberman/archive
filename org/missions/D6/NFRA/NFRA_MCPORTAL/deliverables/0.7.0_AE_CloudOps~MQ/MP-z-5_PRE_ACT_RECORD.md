# MP-z-5 PRE-ACT RECORD -- the NFRA_MCPORTAL gateway release (FWD-20)

**Order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-z-5.gw-gateway-release.md`
(Amendment 2 @`2627c1905f`). **Actor:** `0.7.0_AE_CloudOps~MQ`. **Slug:** `nfra-mcportal-gw-release`.
**Risk:** WORLD. Written BEFORE the act; nothing in it is a prediction.

## 0. The pair -- both halves SIGNED at HEAD of `box/sitez`, each citing the ASK by path

| half | file | commit | verdict |
|---|---|---|---|
| CTO | `deliverables/1.0.0_SA_CTO~Z/NEVER_WIDEN_HALF_CTO_MP-z-5_20261013.md` | `567da88c25` | SIGNED |
| COO | `deliverables/2.0.0_SA_COO~MP/NEVER_WIDEN_HALF_COO_MP-z-5_20261013.md` | `0a54b917d9` | SIGNED |

ASK: `deliverables/0.7.0_AE_CloudOps~MQ/NEVER_WIDEN_ASK_MP-z-5.md` @`fa8d4250bf`. Both halves are ancestors
of `box/sitez`, both quote the ASK commit, both accept ASK section 3a and both rule on section 6.

## 1. Census -- the whole repo, not just the gateway dir

`git diff --name-only 185dc048881da2030efa11f4d0bfb8704b500c66 233440afaf` = **6 paths**:

```
infra/aws/ec2/EC2_MANIFEST.json                                   1 line (mcportal_commit)
infra/aws/ec2/opal-gateway/app/admin_api.py                       +2
infra/aws/ec2/opal-gateway/app/admin_gateway_breakdown.py         +377  new
infra/aws/ec2/opal-gateway/app/server.py                          +29 -1
infra/aws/ec2/opal-gateway/tests/test_admin_gateway_breakdown.py  +427  new
infra/aws/ec2/opal-gateway/tests/test_dashboard_deep_links.py     +178  new
```

Gateway app/tests subset = the allowed five; **outside GW's set = 0**. Zero conflicts occurred under
`infra/aws/ec2/opal-gateway/`; the three cherry-pick conflicts were all under `org/` and were resolved to
the release base's side, per Amendment 2. Every pick was re-authored to this lane, because the owned-paths
hook grants a path by the COMMITTING serial's live order and the source workers hold none at HEAD.

`server.py` carries three hunks (handler; route line + comment; the `PlainTextResponse` import token the
handler's 404 branch requires). Both halves accepted the third explicitly.

## 2. Test counts -- THREE readings, because step 0 and step 1 name DIFFERENT sets

Step 0's set includes `tests/test_entitlement_admin.py`; step 1's set does not. The two therefore have
different denominators, and a single number would misreport one of them.

| tree | set | result |
|---|---|---|
| `C:/tmp/mp-z5-hookup` @`e080b1395a` (box/sitez `baf14ef360` + the hookup) | step 0's | **87 passed, 0 failed** |
| the same tree | step 1's | **78 passed, 0 failed** |
| `C:/tmp/mp-z5-rel` @`233440afaf` (the release tree) | step 1's | **67 passed, 7 failed** |

**The 7 failed ids, measured, and EXACTLY the COO half's closed list -- no other id failed:**

```
tests/test_admin_gateway_breakdown.py::test_channel_with_no_holder_is_empty_list
tests/test_admin_gateway_breakdown.py::test_holders_match_the_dispatch_chain
tests/test_admin_fabric.py::test_roster_equals_devices_register
tests/test_admin_fabric_calls.py::test_real_capture_calls
tests/test_admin_fabric_calls.py::test_request_accepted_by_open_calls_scan
tests/test_admin_fabric_gitstate.py::test_real_capture_gitstate
tests/test_admin_fabric_overlap.py::test_real_capture_overlap
```

Causes, per row `NFRA_MCPORTAL-Z-S45` and accepted by both halves: five raise `FileNotFoundError` on repo
data absent from the base commit (`org/devices/DEVICES.json` and the cp2 capture each read `ls-tree` 0 at
`185dc04888`, 1 at `box/sitez`; `DIRECTIVES.yaml` and `ORG_CHART.md` read 1/1 as the positive control that
this is a vintage gap and not a sparse miss), in four test files this release does not modify; two encode
the post-`OG-tg-1` world, because the base's `app/identity_scope.py` still seeds
`opalbloomberg@opalinvest.com` with `whoami`, so that principal really is an m365 holder on the live base.
A control that swapped ONLY `identity_tool_allowlist.txt` to the trunk's version did NOT fix those two,
which is what located the cause in `identity_scope.py`; the allowlist was restored and the census re-read
at 5 gateway files.

## 3. Rollback -- proven, with nothing uploaded

- **Versioned key, re-read immediately pre-act:**
  `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-185dc04888.tar.gz` --
  **543,554 B, ETag `b486e614fc122cf854f0d063bd198e4e`, `git-ref`
  `185dc048881da2030efa11f4d0bfb8704b500c66`, LastModified `2026-10-12T12:51:35Z`.** Unchanged from the
  reading taken when the ASK was written, and NOT a key this act writes.
- **Rebuilt from a clean tree** (`C:/tmp/mp-z5-rb`, detached at the base, 0 local changes,
  `admin_gateway_breakdown.py` ABSENT as the control that it is the pre-release base; mcportal detached at
  the base's own `bc37107`): bun cache pre-check 77 of 77 rc=0, `bun install --frozen-lockfile && bun run
  build` fully offline rc=0, re-tarred with `deploy-to-ec2.sh`'s exact member list and excludes.
  **543,554 B vs 543,554 B; 132 members vs 132, list diff 0; 109 files md5-compared, 109 EQUAL, 0
  DIFFERENT, 0 only-in-either.**
- **Negative control, so the comparison is known to discriminate:** the same walk against the RELEASE
  tree's `app/` reads 98 EQUAL, 2 DIFFERENT (`admin_api.py`, `server.py`) and 1 only-in-release
  (`admin_gateway_breakdown.py`) -- exactly this release's payload.
- **The command:**
  `cd /c/tmp/mp-z5-rb && DEPLOY_BASE_REF=<the release commit then live> bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`

## 4. The live world, read on the host BEFORE the act (SSM `50716cfe-562c-4c7f-8b76-fb17d6624c59`, Success)

- `EC2_MANIFEST.json` `services.opal-gateway.deployed_commit` on `box/sitez` =
  **`185dc048881da2030efa11f4d0bfb8704b500c66`**, equal to the base this release was cut on, re-read at the
  act per the COO half's condition 2. If it had moved, the act stops and re-cuts.
- `/health` = **200**; `opal-gateway.service` = **active**; **MainPID 994775** (the process MP-n-1 left).
- **MCP tool surface BEFORE = 43 names**, read through the gateway's own unfiltered reader
  (`tools.mcp._tool_manager.list_tools()`), on THIS base and not carried from an earlier release:

```
copy_site_file_to_s3, create_draft, find_online_meeting, find_sharepoint_site, get_item, get_site_item,
inspect_email_attachment, list_calendar, list_channels, list_chats, list_email_attachments,
list_email_filtered, list_meeting_transcripts, list_onedrive, list_recent_email, list_site_drives,
list_site_files, list_teams, opal_asker_query, poll_addressed_teams_messages, profile_site_file,
read_channel_messages, read_chat_message_images, read_chat_messages, read_document, read_email, read_file,
read_meeting_transcript, read_site_file, read_site_workbook, read_teams_attachment, read_workbook,
reply_email, save_email_attachment_to_site, search_email, search_files, search_site_files,
send_channel_message, send_chat_message, send_email, upload_text_to_site, validate_ssavail_attachment,
whoami
```

The AFTER read must be these 43 names, difference EMPTY.

## 5. Bundle

mcportal `0e02a1f1ab56dae65b9df29bd78f1eab319ce6a2`, descends from `bc37107`, on `Opal-Capital/mcportal` DEV.
`src/pages/gateway/` and `public/routes.json` both present at that commit. Bun cache pre-check against its
own lockfile: **77 of 77, rc=0** -- no package is fetched. `bun.lock` and `package.json` are byte-identical
between `bc37107` and `0e02a1f`, so the dependency set does not move.

## 6. Legs, and what stops the act

1. **L1 bundle build** -- mcportal `0e02a1f` built offline inside the deploy.
2. **L2 release build + upload** -- `opal-gateway-<release sha>.tar.gz` and `-latest.tar.gz`.
3. **L3 SSM pull + restart** -- `systemctl restart opal-gateway` on `i-07dccb1615503ac99`.
4. **L4 manifest record** -- `deployed_commit`, `previous_deployed_commit` = `185dc04888...`,
   `mcportal_commit` = `0e02a1f`, `release_note`. The release tree carries the stale `2c0f84966d`, the known
   `safe-ec2-deploy` defect recorded on MP-x-4, MP-r-2 and MP-n-1; the COO half's condition 3 requires the
   correction here.

**STOP conditions:** `/health` not 200 within 90 s -> the section 3 rollback runs AT ONCE and the entry
closes as rolled back. Any failing test id outside the seven above. `deployed_commit` no longer
`185dc04888` at the act. A non-empty MCP tool-name difference.
