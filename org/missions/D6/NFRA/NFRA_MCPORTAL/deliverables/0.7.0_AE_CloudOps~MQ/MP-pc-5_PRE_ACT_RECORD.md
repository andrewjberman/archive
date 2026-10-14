# MP-pc-5 PRE-ACT RECORD -- the People view gateway release

**Order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-pc-5.pc-gateway-release.md` (GO msg 34125).
**Actor:** `0.7.0_AE_CloudOps~MQ`. **Slug:** `nfra-mcportal-pc-release`. **Risk:** WORLD. Written BEFORE the act; nothing here is a prediction.

## 0. The pair -- both halves SIGNED at `box/sitez` HEAD, and they AGREE word for word

| half | file | commit | state |
|---|---|---|---|
| CTO | `deliverables/1.0.0_SA_CTO~Z/NEVER_WIDEN_HALF_CTO_MP-pc-5_20261014.md` | `933bd8e975` | SIGNED |
| COO | `deliverables/2.0.0_SA_COO~MP/NEVER_WIDEN_HALF_COO_MP-pc-5_20261014.md` | `a8cf019d55` | SIGNED |

ASK: `deliverables/0.7.0_AE_CloudOps~MQ/NEVER_WIDEN_ASK_MP-pc-5.md` @`0f6c4d21a3` (sha256 `54222b09...` per the CTO half). Both cite it.
Read in full at HEAD, not from the messages. The two failure branches are identical in both halves:

- **ROLL BACK AT ONCE** (named command, ledger closed as rolled back, stop): `/health` not 200 within 90 s; the before/after tool-name
  difference non-empty; `GET /api/admin/fabric/gitstate` stops answering 401/403 to no identity, or its cold compute exceeds 5 s, or it reads 0 `recorded`.
- **NO ROLLBACK; grade FAIL as measured and open a row:** only AC2's People limb misses (compute over 30 s, fewer than 2 persons, cadence claim not
  "absent" on every tool, or the refused-states limb) while `/health`, the tool surface and the gitstate route hold. The COO half adds the input-state
  case: if the laptop pointer reads `rc != 0` or is absent at the act, AC2's refused-states limb misses on the input, which is this branch.
- **The CTO half covers the act only if `deployed_commit` read at the act is `7c558b4e21`.** Otherwise a new ask.

## 1. Census -- the gateway directory

`git diff --numstat 7c558b4e21 ce402abd5c -- infra/aws/ec2/opal-gateway` = **5 files**: `app/admin_api.py` +2; `app/admin_fabric_gitstate.py` +27 -18;
`app/admin_people.py` +241; `tests/test_admin_fabric_gitstate.py` +46 -7; `tests/test_admin_people.py` +387. **Outside the PC set = 0.**
Whole-repo diff also lists the MP-pc-1 worker's proof instance and note under `deliverables/0.9.0_WK_NFRA_MCPORTAL~20/`; `org/` is not in the artifact.

## 2. Tests

| tree | result |
|---|---|
| `box/sitez` HEAD + hookup `9de5d054aa` | **84 passed, 0 failed** |
| release tree `ce402abd5c` | **78 passed, 5 failed** (83 collected; the 1-test gap is `test_admin_gateway_breakdown.py::test_catalog_reader_resolves_a_tool_through_the_durable_index_key`, which exists only at trunk) |

All five are `FileNotFoundError` on three repo paths outside the gateway directory, each `ls-tree` 0 at the base and 1 at HEAD (Z-S45): the `cp2/fixtures/s3_capture_20261009T0728Z.json`
capture (3 tests), `org/devices/DEVICES.json` (1), `.tools/open-calls-scan.py` (1). Positive control `.tools/safe-commit.sh` 1/1.

## 3. Rollback -- proven, nothing uploaded

- **Versioned key, to be re-read immediately pre-act:** `opal-gateway-7c558b4e21.tar.gz` -- 570,036 B, ETag `318b5cab5c0ce0c807fc6387a984ea05`, `git-ref` `7c558b4e2176a632d13e6301af3e06d434aa1540`, LastModified 2026-10-14T13:57:36Z.
- **Rebuilt from a clean tree** `C:/tmp/mp-pc5-rb` (detached at the base), mcportal `0e02a1f`: bun pre-check 77 of 77; offline install and build; **112 members vs 112, 112 EQUAL, 0 DIFFERENT**.
  **Negative control:** release `app/` vs the live artifact = 100 EQUAL, 2 DIFFERENT (`admin_api.py`, `admin_fabric_gitstate.py`) plus new `admin_people.py`.
- **Command** (named, not run): `cd /c/tmp/mp-pc5-rb && DEPLOY_BASE_REF=<release commit then live> bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
- **Rollback TIME (Z-W2-S8):** neither script has a dry-run or no-op mode (0 hits for `DRY_RUN`/`NOOP`), so the bound is the release's own pull-and-restart, timed at the act and recorded in the close report.

## 4. The live world BEFORE the act (SSM `8ea13996-05b0-4eb2-ab8c-7420f298a8bf`, Success)

- `/health` **200**, unit **active**, **MainPID 1107125**, since 2026-10-14 13:57:58 UTC.
- md5 `admin_fabric_gitstate.py` = `a5ac99dc2e4868b207a2d0833fe84a30` (the base's); `admin_people.py` absent; the served `routes.json` lists `/people` 0 times.
- **MCP tool surface BEFORE = 70 names**, `md5 7b042d201996dd8dc7cc3892b245dbea` over the sorted comma-joined list, read after importing `app.server` (the SERVED registry, row Z-S48). Name list saved at `C:/tmp/pc5_host_before.txt`.
- Pointers (15:2xZ): laptop `rc: 0` (at 2026-10-14T15:20:26Z); sitez, dell1, dell2 404. Expected served states after: laptop `no`, the other three `not recorded`.

## 5. Legs, and what stops the act

The order names four: **L1** bundle build; **L2** release build and upload (`opal-gateway-<release sha>.tar.gz` and `-latest`); **L3** SSM pull and restart on `i-07dccb1615503ac99`;
**L4** manifest record (`deployed_commit`, `previous_deployed_commit`, `mcportal_commit`, `release_note`). **AC1 and AC2 are deliberately NOT legs** (MP-z-5's close/verify circularity).

**STOP conditions before the act:** `deployed_commit` is no longer `7c558b4e21` at the act, or the S3 `-latest` `git-ref` is not `7c558b4e2176a632d13e6301af3e06d434aa1540`; any test failure outside the five above;
a conflict under `infra/aws/ec2/opal-gateway/`.
