# NEVER-WIDEN ASK -- NFRA_MCPORTAL `MP-pc-5`, the People view gateway release

- **Asked by:** `0.7.0_AE_CloudOps~MQ`
- **Halves asked of:** `1.0.0_SA_CTO~Z` (CTO half) and `2.0.0_SA_COO~MP` (COO half)
- **Order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-pc-5.pc-gateway-release.md`, `<risk>WORLD</risk>`
- **GO:** `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/pc/GO_MP-pc-5_20261014.md` (msg 34125)
- **Release branch:** `rel-nfra-mcportal-pc` @`ce402abd5c`, cut from the LIVE base `7c558b4e2176a632d13e6301af3e06d434aa1540`
  (NFRA_OPLGTW OG-hv-2), read from `EC2_MANIFEST.json` `services.opal-gateway.deployed_commit` at the cut, to be re-read at the act.
- **Bundle:** `mcportal_commit` moves `0e02a1f` -> `17dcbb28624eab147318052f58bcc39b8eb8029c` (origin DEV tip; descends from `0e02a1f`).

## 1. BLAST RADIUS -- what this act may touch

| # | thing it touches | what moves |
|---|---|---|
| 1 | `app/admin_fabric_gitstate.py` | the refusal field becomes three-state (PC.2); see the semantic change below |
| 2 | `app/admin_people.py` (new) | `GET /api/admin/people`, owner-gated, read-only; reuses the grant-store Scan MP-z-4 already granted |
| 3 | `app/admin_api.py` | one import and one `Route("/people", ...)` line (my step 0) |
| 4 | two test files | source only, ship nowhere |
| 5 | the dashboard bundle | rebuilt from mcportal `17dcbb2`; adds the People page and lists `/people` in `routes.json`; the `/people` deep link is served by the existing catch-all |
| 6 | `EC2_MANIFEST.json` `services.opal-gateway` | pre-act: `mcportal_commit`; post-act: `deployed_commit`, `previous_deployed_commit`, `release_note` |
| 7 | the running service | one `systemctl restart opal-gateway` on `i-07dccb1615503ac99` |
| 8 | two S3 keys | `ec2/opal-gateway/opal-gateway-<release sha>.tar.gz` (new) and `opal-gateway-latest.tar.gz` (overwritten) |

**THE SEMANTIC CHANGE, named on every branch.** `GET /api/admin/fabric/gitstate`'s `integration_refused` goes from two shapes to
three, per box: rc != 0 -> `{"refused": true, at, note}`; **rc == 0 -> `{"refused": false, at}`** (it read `"not recorded"` at the base);
no pointer -> `"not recorded"`. `integration_refused_basis` becomes per-box. **I measured the four pointers just now (15:2xZ):**
laptop `rc: 0` (pointer written 2026-10-14T15:20:26Z), sitez / dell1 / dell2 404 (laptop's read worked, so the 404s are not a broken read).
After the restart the served answers should therefore be: laptop `no`, the other three `not recorded`. The `rc != 0` branch ("refused") is
**not exercised by any box today** and stays unexercised by this act. A consumer other than the dashboard bundle that reads the old
two-shape value would see `{"refused": false, ...}` where it read `"not recorded"`; I have no census of such consumers and am not
claiming one.

## 2. WHAT IT MAY NEVER TOUCH

1. **The MCP tool surface.** Names are listed on the host before and after (importing `app.server` first, so the SERVED registry, not the native one);
   both counts recorded; the difference must be EMPTY.
2. **Any IAM.** No grant moves; the Scan the People view uses is MP-z-4's, already applied.
3. **Any store write.** No write API in the new module.
4. **Any Terraform, ALB, listener, security group, instance, secret or schedule.**
5. **Any other service in `EC2_MANIFEST.json`.**
6. **`safe-ec2-deploy.sh` and `deploy-to-ec2.sh`** -- read, never edited.

## 3. CENSUS -- measured on the release branch

`git diff --stat 7c558b4e21 HEAD -- infra/aws/ec2/opal-gateway` = **5 files, 703 insertions, 25 deletions**, exactly the order's five:

```
app/admin_api.py                      +2
app/admin_fabric_gitstate.py          +27 -18
app/admin_people.py                   +241 (new)
tests/test_admin_fabric_gitstate.py   +46 -7
tests/test_admin_people.py            +387 (new)
```
**Outside the PC set under the gateway dir = 0.** Whole-repo `git diff --name-only` also lists 2 files under
`org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~20/` (the MP-pc-1 worker's proof instance and note, carried by its
proof commit `12d990e43d`); `org/` is not in the artifact's member list, so they ship nowhere.

Commits on the branch: `0c62b566f7` (pick of `90ad6bfa00`), `f1d6663707` (pick of `12d990e43d`), `e8ce9bcf44` (pick of `33d0604810`,
**re-authored to this lane**: the owned-paths hook refuses a worker author on `app/` paths; the pick's TO file, absent at the base, and its
worker proof instance, a path no AE lane may write, are not carried), `1416e2e62e` (pick of my step-0 hookup `9de5d054aa`), `ce402abd5c` (manifest).

## 4. TESTS -- `tests/test_admin_fabric_gitstate.py tests/test_admin_people.py tests/test_admin*.py tests/test_owner_gate.py`

| tree | result |
|---|---|
| `box/sitez` HEAD with the hookup (`9de5d054aa`) | **84 passed, 0 failed** |
| the release tree @`ce402abd5c` | **78 passed, 5 failed** (83 collected) |

The 84 vs 83 is one test, `test_admin_gateway_breakdown.py::test_catalog_reader_resolves_a_tool_through_the_durable_index_key`, which exists
at trunk HEAD from another project's unreleased gateway change (`4a707ab5f9`, OG-gt-0) and not at the live base. Same 11 test files in both trees.

**All 5 release-tree failures are `FileNotFoundError` on a repo path outside `infra/aws/ec2/opal-gateway/`**, three distinct paths, each
`ls-tree` **0 at the live base and 1 at box/sitez HEAD**, and each test passes at HEAD:

| test id | missing path | base | HEAD |
|---|---|---|---|
| `test_admin_fabric_gitstate.py::test_real_capture_gitstate`, `test_admin_fabric_calls.py::test_real_capture_calls`, `test_admin_fabric_overlap.py::test_real_capture_overlap` | `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/cp2/fixtures/s3_capture_20261009T0728Z.json` | 0 | 1 |
| `test_admin_fabric.py::test_roster_equals_devices_register` | `org/devices/DEVICES.json` | 0 | 1 |
| `test_admin_fabric_calls.py::test_request_accepted_by_open_calls_scan` | `.tools/open-calls-scan.py` | 0 | 1 |

Positive control: `.tools/safe-commit.sh` reads 1 at the base and 1 at HEAD with `/.tools/` in the cone. Rule: row Z-S45, a release tree's `org/` and `.tools/` are frozen at the release chain's vintage.

## 5. ROLLBACK -- proven BEFORE the act, per key

**Key 1 -- the versioned artifact.** `opal-gateway-7c558b4e21.tar.gz` is present and PRE-ACT: **570,036 B, ETag `318b5cab5c0ce0c807fc6387a984ea05`,
`git-ref` `7c558b4e2176a632d13e6301af3e06d434aa1540`, LastModified 2026-10-14T13:57:36Z.** This act does not write that key; re-read immediately pre-act.

**Key 2 -- `opal-gateway-latest.tar.gz`** IS overwritten (same ETag and ref today). Its rollback is the same redeploy.

**The rebuild, run, nothing uploaded.** A clean detached worktree at the live base (`C:/tmp/mp-pc5-rb`, 0 local changes) with mcportal detached at
`0e02a1f` (what the base's manifest names): bun cache pre-check **77 of 77**, `bun install --frozen-lockfile` and `bun run build` fully offline, `dist/index.html` and
`dist/routes.json` present; re-tarred with `deploy-to-ec2.sh`'s exact member list and excludes. **112 members vs 112; md5 per member: 112 EQUAL,
0 DIFFERENT, 0 only-in-either**, against the downloaded live artifact.
**Negative control (the comparison discriminates):** the same walk of the RELEASE tree's `app/` against the live artifact reads 100 EQUAL and **2 DIFFERENT
(`admin_api.py`, `admin_fabric_gitstate.py`)** plus the one new module `admin_people.py`, which is this release's payload and nothing else.

**The command that would re-deploy it** (named, not run):

```
cd /c/tmp/mp-pc5-rb && DEPLOY_BASE_REF=<the release commit then live> \
  bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh
```
It rolls the bundle back too, because the rollback tree's manifest names `mcportal_commit` `0e02a1f`. No Terraform, ALB, host, role or secret change in either direction.

**Rollback TIME (row Z-W2-S8).** Neither `deploy-to-ec2.sh` nor `safe-ec2-deploy.sh` has a dry-run or no-op mode (both read for `DRY_RUN`/`NOOP`: 0 hits), so the order's
fallback applies: I will time the release's own pull-and-restart in step 4 and record it as the bound, saying so. Measured offline here: the rollback's bundle build is ~12 s
(install 8.7 s, build 3.1 s).

## 6. READ-BACKS -- independent of the deploy's rc

- `/health` polled immediately after the restart.
- **AC1** (`checks/pc5.AC1.sh`) and **AC2** (`checks/pc5.AC2.sh`, on the host over SSM): the order's literal invocations. AC2 needs the served gitstate to show at least two of
  the three states with `no` among them. From section 1 that is expected to read `no` (laptop) and `not recorded` (the other three); it depends on the laptop pointer still reading `rc: 0` at the act.
- **MCP tool surface:** before/after names on the host, both counts, difference EMPTY.

## 7. THE FAILURE BRANCH -- stated now so the two halves cannot contradict (MP-n-4's lesson)

On MP-n-4 the two signed halves gave opposite instructions on the AC2 failure branch, and I stopped to have them reconciled. To avoid that here, **my reading of the order, which I will follow unless a half says otherwise in words both halves repeat:**

- **Roll back AT ONCE** (named command, ledger closed as rolled back, stop): `/health` is not 200 within 90 s; or the before/after tool-name difference is non-empty; or the existing `GET /api/admin/fabric/gitstate` route stops answering 401/403 to no identity or its cold `_compute` exceeds MP-n-4's 5 s bar (1.3 s / 136 fetches at that release) or reads 0 `recorded`. AC2 as written does not time this route, so I will measure it once on the host and report the number.
- **No rollback; grade FAIL as measured, open a row:** AC2's People limb alone misses (compute over 30 s, fewer than 2 persons, the cadence claim not "absent" on every tool, or the refused-states limb), while `/health`, the tool surface and the gitstate route above all hold. The new route is owner-gated and read-only; the previous bundle is one redeploy away and the issuer decides.

## 8. WHAT IS ASKED

Each half, citing this ASK by path and commit:

- `1.0.0_SA_CTO~Z` -- the CTO half.
- `2.0.0_SA_COO~MP` -- the COO half.

Please state in the half your disposition of **section 1's consumer-census gap** and of **section 7's two branches**. A refused half STOPS the act.
