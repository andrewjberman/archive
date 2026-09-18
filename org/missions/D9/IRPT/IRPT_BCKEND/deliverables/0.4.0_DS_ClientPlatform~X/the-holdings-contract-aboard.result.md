# IRPT_BCKEND.TO-IB-rtd-3: holdings contract aboard the bundle, re-arm trigger named (result)

**Assignee:** `0.4.0_DS_ClientPlatform~X` | **Issuer:** `2.0.0_SA_COO~B` | **Worktree:** `/c/tmp/wk-irpt-4-ds6`
(branch `wk-irpt_bckend-4-ds6`, cut @e4623a5872) | **Cut on row:** `IRPT_BCKEND-S71` | **Written:** 2026-09-18

Every line citation below carries its vintage (S56).

## What was done

| Commit | What |
|---|---|
| `28bc06907f` | `.tools/safe_deploy_core.py`: the 10th `investor_reporting` member, `docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json`. It is bundle-only, with sha key `holdings-snapshot-schema-sha256` and no `distribution` flag. |
| `024033d9d9` | `tests/test_holdings_rearm_trigger.py` and rows `IRPT_BCKEND-S74`, `S75` |
| `3ac01a96ae` | Change-management entry `irpt-bckend-rtd3-holdings-contract-mint` OPENED, with its sentinel committed before the act. This is the tree the guard packed. |
| (act) | `HALT_ACK=1 bash .tools/safe-deploy.sh --mint-bundle investor_reporting`, 2026-09-18T12:20:09Z |
| `8f460875a1` | Entry CLOSED, 2 of 2 legs, sentinel removed, committed before the grading reads |
| `fb4dcbc8ac` | `battery_ib_rtd_3.py`, `schema_diff_ib_rtd_3.py`, `IB-rtd-3_holdings_schema_diff.txt` |

Not done, by the order's bounds:
- no schema edit, and no change to which file the runner reads;
- no schedule change: `irpt-holdings-snapshot` is still DISABLED;
- no holdings run, no apply, no IAM change.

### Why the member carries no `distribution` flag

The contract has no per-file S3 target: `file_to_s3_target` returns `None`. The guard's own arm `NO-FLAG-WITHOUT-A-LOOSE-LEG` requires every flagged member to own a loose leg. So the member is bundle-only, and a commit to it re-mints the bundle through the member detector.

The guard's four test files were compared case by case at the cut (`e4623a5872`) and after the edit. There were 0 regressions:

| Test file | Result |
|---|---|
| `test_safe_deploy_distribution_member` | 9/9 (now "3 flagged of 10 members") |
| `test_safe_deploy_receipt_names_both_legs` | 4/4 |
| `test_safe_deploy` | 7/14 failing, the same 7 cases as at the cut |
| `test_code_trees_invariant` | 3/18 failing, the same 3 cases as at the cut |

### Row S75: the new member's line endings

The guard packs from the worktree (row S63). In this autocrlf worktree the v1 schema is checked out as 34577 bytes with 695 CR, while the blob is 33882 bytes with 0 CR.

- **What I did:** before the mint, I wrote the blob's exact bytes into that one path. `git diff --quiet` reported no content difference, and `git status` is clean.
- **Result:** the member in the tarball equals blob `9ec70af2`.
- **What I left alone:** the two existing JSON members are still packed CRLF, as on every mint.
- **What a later mint does:** a mint from a default autocrlf worktree packs this member CRLF again, until the packer reads the blob. That fix belongs to the guard's owner (S63).

## The minted object (R-40 identities)

| Item | Pre-cell | After (this cell) |
|---|---|---|
| key | `s3://opal-data-mdpf/code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz` | same key |
| VersionId | `00PXLyYmM0vJavlwdpUHBKRi3pza0_nS` (11:05:45Z, the MSTR push gate), byte-identical to the face's `0XLkiPt4wljdniLnF2fkPKN4qAIkjUbc` (row S74) | `.v.aG6Rbk5wXOjGgb4vnQIeGPzrabMKo` |
| ETag | `4c942a76f990874838e33e37f24ed69a` | `a8e1a036b4e26cd2fca45f3a295a4c71` |
| sha256 (downloaded) | `e2a933b923d50626578969b3544e070161f029bdb4132b6f600db66859504b3b` | `334fc6f6547fdea78d95c6b49d02980498cd2dd586505de92490418170d07b35` (66518 bytes) |
| members | 9 | 10: the v1 schema added, git blob `9ec70af2ba0c71ea589dab48bd14407e111694a8`, sha256 `9c0acba985c38b32f0736045936db14b2d251089f2cdb79a818a12bc69259348` == its stamp |
| the other 9 | -- | bytes and stamps unchanged, 9 of 9 |

The loose legs were read before the mint and again after it; they are unchanged 3 of 3 and CONSISTENT 3 of 3:
- 49F `jnnxQWbVT_lx6WlJu8HbVXNjQJpYK00w`
- cot `81mlcZFSpRyiH_OeK0OlWFvEHKYUelj_`. This is not IB-rtc-2's `bobsNlnm...`: the 11:05Z push re-wrote identical bytes (row S74).
- inf `z_WDDmx6004thBhXbT0uBvsDkNibZQF8`

## R43-AC1: the battery

- **Invocation:** `timeout 1800 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.4.0_DS_ClientPlatform~X/battery_ib_rtd_3.py`
- **Where it ran:** from a fresh detached checkout at `fb4dcbc8ac`.
- **Result:** rc=0, `R43-AC1: 4 of 4 graded arms PASS`, `IBR43-HOLDINGS-CONTRACT-ABOARD-AND-TRIGGER-GUARDED`.
- **Determinism:** identical to the authoring-worktree run, 146 lines each, once paths, times, SSM ids and `/tmp` stamps are masked.
- **Recorded output:** `IB-rtd-3_R43-AC1_battery_output.txt`.

| Arm | Result | Deciding evidence |
|---|---|---|
| (a) MEMBER + DIFF | PASS | The guard declares the member by repo path, with distribution flag `False` and target `None`. There are 0 commits to either schema in `e4623a5872..8f460875a1`. `holdings_snapshot.py` has the same blob at the cut and at the close. Its `CONTRACT_PATH` assignment, found by AST, is at `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py:109-110 @8f460875a1` and names the v1 path. The diff is re-derived from the blobs; see below. |
| (b) RE-MINT | PASS | The version is pinned by id: md5 == ETag. The guard declares 10 of 10: vs IB-rtc-9's 9, added the v1 schema, removed nothing. `source-repo-paths` names 10 of 10, and 10 are served. The member's tarball `git hash-object` is `9ec70af2...` == its blob and == its stamp. The other 9 are unchanged. The pre-cell predecessor and the face's version are byte-identical. The negative control: the ETag differs and the VersionId differs. Distribution legs CONSISTENT 3 of 3, with 0 commits to them. |
| (c) HOST | PASS | SSM `eede77ab-...` in the authoring run and a fresh command id in the recorded run, on `i-02448edb624a7a7cf`, running and Online. The host's sha256 of the served key equals the minted version's; the host's sha256 of the shipped pre-cell tarball equals the pre-cell version's. 10 of 10 placed. IMPORT-OK 7 of 7 `.py` in both trees. The NEW tree's `load_contract()` RETURNED `opal://irpt/contracts/v1/HoldingsSnapshot.schema.json`, with file sha256 == the blob's (1 of 1). The OLD (pre-cell) tree lacks the member, and `load_contract()` RAISED `FileNotFoundError: ... /OLD/docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json` (1 of 1), on the same interpreter in the same command. 0 network events in both, and the positive control fired. |
| (d) TRIGGER | PASS | The committed test ran as written: 3 passed, 0 skipped. **LIVE:** `schedule irpt-holdings-snapshot = DISABLED; served bundle VersionId .v.aG6Rbk5w... 10 member(s); runner opens 5; missing [] -> PASS`. **IF-ENABLED-NOW** (informational): `PASS`; before the mint it read `FAIL`, which was S71's exposure. **MUTANT:** with the v1 schema removed from the real 10-member list, a simulated ENABLED read `FAILS as it must`, and the same list DISABLED reads `PASS (inert)`. Directory suite: 71 of 71 collected, all passed. |

### The two-schema diff, recorded

The diff is `IB-rtd-3_holdings_schema_diff.txt`, re-derived by `schema_diff_ib_rtd_3.py` at `e4623a5872` from the blobs.

| | V1 (`docs/contracts/investor-reporting/v1/`) | CTR (`infra/aws/lambda/investor-reporting/_contracts/`) |
|---|---|---|
| blob | `9ec70af2`, 33882 bytes | `95e4d500`, 25485 bytes |
| object paths with `properties` / `required` | 24 / 24 | 18 / 18 |
| leaves | 266 | 204 |

What differs:
- **properties:** 6 object paths are only in V1 and 0 only in CTR. The name sets differ at 3 of the 24 in the union:
  - `/`: V1 adds `attribution_holdouts`, `contract_version`;
  - `/properties/clocks`: V1 adds `custody_as_of`, `overlay_as_of`;
  - `/properties/nodes/items`: V1 adds `clocks`.
- **required:** 6 paths only in V1; the sets differ at 0 common paths. The top-level `required` is identical in both.
- **leaves:** 62 only in V1, 0 only in CTR, and 1 value differs, `/$id`: `opal://irpt/contracts/v1/HoldingsSnapshot.schema.json` vs `opal://irpt/contracts/HoldingsSnapshot.schema.json`. V1 also carries `/x-contract-version`.
- **In short:** V1 is a strict superset of CTR.

## Rows filed

- **`IRPT_BCKEND-S74` (INERT).** The pre-cell object is VersionId `00PXLyYm`, not the `0XLkiPt4` the face names, though the bytes are identical (ETag `4c942a76`). It was re-written by 0.0.0_AB_MSTR's 11:05Z push gate, which also re-wrote cot's loose key as `81mlcZFS` with the same ETag. The battery binds the pre-cell to both versions and the legs to the pre-mint read.
- **`IRPT_BCKEND-S75` (INERT).** Corrects this seat's S71: its sizes were CHECKOUT sizes. The v1 blob is 33882 bytes, not 34577; the `_contracts/` blob is 25485, not 26022. Also S63 meets the new member; see "Row S75" above.
- **`IRPT_BCKEND-S76` (INERT).** Enabling the schedule would NOT run the bundled runner. Its target is the SQS queue `irpt-generation`, which has 0 consumers. So S71 arms only when the schedule is enabled AND a compute target exists. The trigger test reads the first condition.

## R43-AC2: judgment, recorded for `3.0.0_SA_CVO`, no verdict

**1. Which HoldingsSnapshot schema is the contract the endpoint means?** The answer is L4's. The facts:

- **Readers.**
  - The v1 copy is read by the holdings gold runner: `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py:109-110 @fb4dcbc8ac`.
  - It is also what the irpt-holdings Lambda packages. `infra/aws/lambda/investor-reporting/holdings/stage.py:51-54 @fb4dcbc8ac` stages it as `contracts/HoldingsSnapshot.schema.json`, and the Lambda loads it by name at `infra/aws/lambda/investor-reporting/holdings/snapshot.py:62 @fb4dcbc8ac`.
  - A repo search of `.py/.tf/.mjs/.js/.ts/.sh` files for `HoldingsSnapshot.schema.json` found no reader that names the `_contracts/` copy's path. Beyond that, its readers are the ones that walk the `_contracts/` directory as a set (the contract tests and fixtures).
- **Output compatibility.**
  - Both schemas set `additionalProperties: false` at `/`, and only V1 declares `attribution_holdouts` and `contract_version`.
  - The runner emits `attribution_holdouts` in every snapshot: `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py:1115 @fb4dcbc8ac`, read back at `:1254 @fb4dcbc8ac`.
  - So a real runner snapshot validated against the `_contracts/` copy would be refused at `/` for an additional property.
  - I did not find `contract_version` emitted by the runner.
- **The diff:** V1 is a strict superset of CTR: 0 paths, 0 required sets and 0 leaves exist only in CTR.

**2. Is the trigger test the right guard, or should the schedule's enable itself be gated?**

- **How an enable happens.** The schedule is a Terraform resource declared `state = "DISABLED"` at `infra/aws/terraform/investor-reporting/directory/schedule.tf:71 @fb4dcbc8ac`. An enable is either a Terraform edit applied through `safe-apply`, or a console or CLI act that Terraform would later see as drift.
- **When the test runs.** It runs when someone runs the directory suite or this battery. It reads the live state; it does not block an enable as it happens.
- **What an enable actually does today (row S76).** The schedule targets the `irpt-generation` queue (`schedule.tf:79-83 @fb4dcbc8ac`). That queue has 0 event-source mappings (read 12:4xZ), and the declaration's own comment says so (`schedule.tf:6-13 @fb4dcbc8ac`). So an enable today does not reach the runner.
- **Where a gate could sit.** On the enable (a plan-time check that refuses `state = "ENABLED"` without a wired target and a complete bundle), or on the wiring of a compute target. Where it belongs is the CVO's call.

**3. What else would `holdings_snapshot.py` need before a first enabled fire?**

- **A compute target or dispatch that runs the bundled runner on the host.** None exists: row S76 and `schedule.tf:6-13 @fb4dcbc8ac`. The directory runner's equivalent is the `irpt-directory-refresh` Lambda's SSM dispatch.
- **Source reads on the host session.**
  - The runner builds one host-session S3 client (`holdings_snapshot.py:1297 @fb4dcbc8ac`).
  - For 49 Financial it reads `opal-data-assets` `smartx/platform/silver/...` (`holdings_snapshot.py:503-508 @fb4dcbc8ac`).
  - It also reads the firm's own directory for account ids (`holdings_snapshot.py:510 @fb4dcbc8ac`).
  - For Inflection it reads `opal-data-inf` (`holdings_snapshot.py:660 @fb4dcbc8ac`), including `silver/eclipse/` through `_latest_complete_eclipse_date(s3, bucket)`. That call is at `holdings_snapshot.py:661 @fb4dcbc8ac`, and the helper is defined at `holdings_snapshot.py:838-847 @fb4dcbc8ac`.
  - For Cottonwood it reads `opal-data-assets` `blackdiamond/cottonwood/silver/` (`holdings_snapshot.py:853-858 @fb4dcbc8ac`).
  - **Not measured by this cell:** whether the host role holds those read grants.
- **Destination writes on the host session.**
  - The writes are at `holdings_snapshot.py:1218-1221 @fb4dcbc8ac`, into the firm bucket from the firm map (`holdings_snapshot.py:149-153 @fb4dcbc8ac`, where 49 Financial maps to `opal-data-bd`).
  - **Not measured:** the host role's write grants on `investor-reporting/holdings/`.
- **Already in place, measured by this cell and IB-rtc-9:**
  - `load_contract()` resolves on the host from the bundle (arm (c));
  - validation runs under the host's jsonschema 3.2.0 (IB-rtc-9);
  - IMPORT-OK on the host, including `pandas` (`holdings_snapshot.py:81 @fb4dcbc8ac`).
