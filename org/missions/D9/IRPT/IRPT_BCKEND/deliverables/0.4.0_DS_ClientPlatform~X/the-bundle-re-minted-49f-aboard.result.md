# IRPT_BCKEND.TO-IB-rtc-8: bundle re-minted with the 49 Financial source set aboard (result)

**Assignee:** `0.4.0_DS_ClientPlatform~X` | **Issuer:** `2.0.0_SA_COO~B` | **Worktree:** `/c/tmp/wk-irpt-3-ds4`
(branch `wk-irpt_bckend-3-ds4`, cut @437789944a) | **Written:** 2026-09-18

## What was done

This cell re-minted the `investor_reporting` bundle on the tree that carries IB-rtc-6's runner edit. That tree
is `437789944a`, which already contains the merge `119fda050a`. The re-mint is step 5 of the sign-off packet
(K5), a DS-lane act under Rule 13. Nothing was applied, no IAM changed, no distribution member was committed,
and the runner was not run end to end.

| Commit | What |
|---|---|
| `a1f09a51dd` | Change-management entry `irpt-bckend-rtc8-k5-mint` OPENED, with its sentinel committed before the act. This is also the tree the guard packed. |
| (act) | `HALT_ACK=1 bash .tools/safe-deploy.sh --mint-bundle investor_reporting`, 2026-09-18T06:33:22Z |
| `84349a3a19` | Entry CLOSED, 2 of 2 legs proven and the sentinel removed, committed before the grading reads |
| `f5005ea933` | Battery `battery_ib_rtc_8.py` + row `IRPT_BCKEND-S70` |

## The minted object (R-40 identities)

| Item | Before (IB-rtc-2's mint) | After (this cell) |
|---|---|---|
| key | `s3://opal-data-mdpf/code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz` | same key |
| VersionId | `1jPgGCGLP.uGY5RpMlMJTrKvKzvyYf7O` | `q8myxeHdNw48w1uDb7YTcBh8DHV9TzU2` |
| ETag | `0020e7afc760b827a6adb7c0ad538903` | `479af04c0a3a1eb6651707b340df9926` |
| sha256 (downloaded) | -- | `0bd71b5f1f5c8b4204096dbcd765b77b241250201357d92d228f90094f814758` (60447 bytes) |
| `directory-runner-sha256` | `ba4a60657b48...` | `a16b5396b95f04bb725bf20dadc78c7b7ef2d9e8226f8fd99307433ed245e9b3` |
| the other 8 stamps | -- | unchanged |
| `directory_runner.py` member | -- | git hash-object `0351bce74591a78dc0901862b897688b97ab69ef` == the blob at `a1f09a51dd`, `84349a3a19` and `f5005ea933` |

## R38-AC1: the battery

- **Invocation:** `timeout 900 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.4.0_DS_ClientPlatform~X/battery_ib_rtc_8.py`
- **Where it ran:** from a fresh detached checkout at `f5005ea933`, which is where a later grader stands.
- **Result:** rc=0, `R38-AC1: 4 of 4 graded arms PASS`, `IBR38-BUNDLE-REMINTED-49F-ABOARD`.
- **Recorded output:** `IB-rtc-8_R38-AC1_battery_output.txt`.

| Arm | Result | Deciding evidence |
|---|---|---|
| (a) CLOSURE | PASS | The dynamic open/import probe finds `CLOSURE N = 8`, with no additions or removals compared with IB-rtc-2's 8, and all 8 are declared and named by repo path. IB-rtc-6 edited `directory_runner.py` in place. Its new test file `data/assets/scripts/gold/investor_reporting/tests/test_directory_runner_source_principal.py` is in the tree (True), but it is not in the closure and not a bundle member: it is a test, not a runtime member. |
| (b) RE-MINT | PASS | The minted version is pinned by id: md5 of the downloaded bytes == ETag. `source-repo-paths` names 8 of 8 closure members, and the bundle serves 9 members. The runner's stamp equals its member's bytes. Negative control against `0020e7af` / `1jPgGCGL`: the ETag differs, the VersionId differs, and the runner member's sha256 moved from `ba4a60657b48` to `a16b5396b95f`. The tarball's `directory_runner.py` equals the blob. |
| (c) CONSISTENCY | PASS | `CONSISTENT: 3 of 3 DISTRIBUTION members agree on both legs (ref a1f09a51dd)`, graded on the minted version and on the loose VersionIds IB-rtc-2 left. Commits to the three members in `437789944a..84349a3a19`: 0. Loose VersionIds now: UNCHANGED for assets, cot and inf. |
| (d) HOST | PASS | SSM `303dbcb9-731e-4bc1-942b-594f29d0bc27` on `i-02448edb624a7a7cf` (running and Online, so no StartInstances). The host's sha256 equals the minted version's; all 8 members extracted at repo shape; IMPORT-OK 3 of 3. **UNSET:** construction made 0 service and 0 metadata-endpoint events, left no WARN and built no client. Opening the lazy seam `_gold()` without a read added the WARN and returned the host session, with **0 service-endpoint events and 6 metadata-endpoint events**. **SET** to a well-formed, non-existent ARN: construction made 0 socket events of any kind and assumed nothing. The network positive control fired. |

## Row filed

**`IRPT_BCKEND-S70` (OBSERVATION, INERT).** The face says instantiating `Firm49F` with the variable unset prints the K5 WARN
with 0 network events. What the host shows:

- The constructor builds no client and adds no note.
- The WARN is added by the lazy seam `_gold()` the first time a client is needed.
- On the host, that first `_gold()` call builds the host's S3 client, which fetches credentials from the EC2
  metadata endpoint (6 calls) and makes 0 calls to any AWS service endpoint.

The battery therefore grades the claim in two parts:

1. Construction must make 0 socket events of any kind.
2. The seam must make 0 service-endpoint events and print the WARN.

The metadata-endpoint calls are printed but not graded. The runner before IB-rtc-6 built the same client at its first
dimension read. No code change is asked for.

## R38-AC2: judgment, recorded for `3.0.0_SA_CVO`, no verdict

**Is the bundle the host will run at IB-rtc-7's fire byte-identical to the tree IB-rtc-7's applies are cut from?**

The facts, measured on the minted version `q8myxeHdNw48w1uDb7YTcBh8DHV9TzU2`. Each of its 9 members was compared
with the git blob at three commits:

- `a1f09a51dd`: the tree the guard packed.
- `437789944a`: the cut this cell and IB-rtc-7's amended face share.
- `08b4472ded`: the shared `CLOUD` tip when this was read, 22 commits past the cut.

Results:

- **7 of 9 members are byte-identical at all three commits.** They are the five `.py` members plus the three
  `runner_common.py`. That includes `directory_runner.py`: blob `0351bce745`, sha256 `a16b5396...`.
- **The 2 JSON members are NOT byte-identical to their blobs.** `data/firm_registry.json` carries 136 CR and
  `infra/aws/lambda/investor-reporting/_contracts/DirectoryEntry.schema.json` carries 260 CR. After CRLF-to-LF
  normalisation both equal their blobs, 9 of 9. This is the packer-reads-the-worktree condition already filed as
  row `IRPT_BCKEND-S63`. This mint did not cause it and did not fix it.
- **Of the 22 commits on `CLOUD` past the cut, 0 touch any of the 9 members.**

Whether IB-rtc-7 runs on these bytes depends on two things:

- IB-rtc-7 applies from a tree whose 9 members still equal these blobs. No commit to them is visible as of `08b4472ded`.
- Nothing re-mints the key before the fire. The key is unversioned from the host's side: the host role has
  `s3:GetObject` but no `s3:GetObjectVersion` (measured at IB-rtc-2), so the dispatch fetches whatever version
  is current.

**Did anything in the mint move a firm's served module?**

The mint wrote exactly one key: the bundle in `opal-data-mdpf`, which the directory dispatch reads for all three
firms. That key's source is `infra/aws/terraform/investor-reporting/directory/schedule.tf` `irpt_runner_bundle_uri`. The
Lambda's `IRPT_DIRECTORY_BUNDLE_URI` equals it, and `.tools/safe_deploy_core.py` is its one writer declaration.
The three firms' own loose `runner_common.py` keys did not move; their VersionIds are the ones IB-rtc-2 left:

- `opal-data-49financial/_code/runner_common.py` `jnnxQWbV...`
- `opal-data-cot/code/gold/runners_cot/runner_common.py` `bobsNlnm...`
- `opal-data-inf/code/gold/runners_inf/runner_common.py` `z_WDDmx6...`

Inside the bundle, only the `directory-runner-sha256` stamp moved. Comparing the runner definition by definition
between the two bundle versions (56 lines added, 4 removed):

- **Added:** `SOURCE_ROLE_ENV`, `SOURCE_SESSION_NAME`, `_list_dates`, `Firm49F._gold`.
- **Changed:** `Firm49F`, `Firm49F.__init__`, `_dates`, `_read`, `_manifest`.
- **Unchanged:** every other definition, including the Inflection and Cottonwood source sets, which have no changed
  definition.

**Timing facts the grader may weigh:**

- **The next scheduled fire runs this runner, and may come before IB-rtc-7's apply.** The EventBridge Scheduler
  schedule `irpt-directory-refresh` is ENABLED at `cron(0 9 ? * MON-FRI *)` America/New_York, next at 13:00Z today.
- **At read time the refresh Lambda's environment held no source-role map.** Its env keys were
  `IRPT_DIRECTORY_BUCKET_MAP`, `IRPT_DIRECTORY_PREFIX`, `IRPT_DIRECTORY_RUNNER_INSTANCE_ID` and
  `IRPT_DIRECTORY_BUNDLE_URI`.
- **So a fire before IB-rtc-7 runs `Firm49F` with the variable unset.** It writes the WARN note and reads on the
  host session, which the firm bucket's policy refuses. That is the pre-K5 outcome for 49 Financial.
- **The Lambda's code changed after the mint, and not by this cell.** CloudTrail records `UpdateFunctionCode` on
  `irpt-directory-refresh` at 2026-09-18T06:41:42Z by `Andrew_Berman`, the shared IAM user. That is 8 minutes after
  the mint; this cell made no Lambda call. `CodeSha256` is `u82ZY7lCKf/lR7hxFQfy2a6FofEfkSGu4hLLoO7wU+4=`.
