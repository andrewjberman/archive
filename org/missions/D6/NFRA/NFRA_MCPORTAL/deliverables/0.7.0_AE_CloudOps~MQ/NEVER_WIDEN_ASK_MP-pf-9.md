# NEVER-WIDEN ASK -- NFRA_MCPORTAL `MP-pf-9`, the bundle-only gateway release (Gateway page at 390 px)

- **Asked by:** `0.7.0_AE_CloudOps~MQ`
- **Halves asked of:** `1.0.0_SA_CTO~Z` (CTO half) and `2.0.0_SA_COO~MP` (COO half)
- **Order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-pf-9.gateway-page-bundle-only-release.md`, `<risk>WORLD</risk>`; amendment A1 @`66a4be01d8` (msg 35003, the six AssertionErrors named)
- **GO-PREP:** msg 34994 (stage 1 only: no ledger, no deploy until the issuer's second message)
- **Release branch:** `rel-nfra-mcportal-pf` @`3cc7017f1f` (worktree `C:/tmp/mp-pf-rel`), cut from the LIVE base `38fe44d5cb8d37b6007fb7e5fa47a25316e01054`
  (NFRA_MCPINDEX MX-r-15 v3, `~MI`). Live ref read 2026-10-16T12:31Z from `opal-gateway-latest.tar.gz` metadata `git-ref`; it is to be RE-READ at the act.
- **Bundle:** `EC2_MANIFEST.json` `services.opal-gateway.mcportal_commit` `090b9cdc85ce3463e73915e68b44f4c21053a71c` -> `c66ca82952c01575968d16cc736cdabe36606572` (origin mcportal DEV tip).

## 1. BLAST RADIUS -- what this act may touch

| # | thing it touches | what moves |
|---|---|---|
| 1 | the dashboard bundle on the host | `index.html` is replaced; two assets are added (`assets/index-BRnJX9Mi.css`, `assets/index-DbObnWYp.js`); the served `index.html` then names those two instead of `index-pbBdUBWu.css` / `index-DzjZpju-.js` |
| 2 | `routes.json` | UNCHANGED (sha256 `e6d4a9ac...` in both builds) |
| 3 | `EC2_MANIFEST.json` `services.opal-gateway` | pre-act: `mcportal_commit` (the release commit); post-act: `deployed_commit`, `previous_deployed_commit`, `release_note` |
| 4 | the running service | one `systemctl restart opal-gateway` on `i-07dccb1615503ac99` |
| 5 | two S3 keys | `ec2/opal-gateway/opal-gateway-<release sha>.tar.gz` (new) and `opal-gateway-latest.tar.gz` (overwritten) |

**What the bundle swap is.** The Gateway page at mcportal `c66ca82952` fixes the page scrolling sideways at 390 px on real data (row Z-S64): an index list that holds an
unbroken ~65-character name scrolls inside its own box. The new build's JS file has the SAME content as the old one (sha256 `52466cff...`, only the file name differs); the
CSS and `index.html` differ.
**No Python, no gateway code, no tool added or removed.** The old assets stay on the host as they are (12 `assets/` files there today); this act does not delete one.

## 2. WHAT IT MAY NEVER TOUCH

1. **The MCP tool surface.** Names listed on the host before and after (importing `app.server` first, so the SERVED registry, not the native one); both counts recorded; the difference must be EMPTY.
2. **Any IAM.** No grant moves.
3. **Any store write.** None in the release.
4. **Any Terraform, ALB, listener, security group, instance, secret or schedule.**
5. **Any other service in `EC2_MANIFEST.json`.**
6. **`safe-ec2-deploy.sh` and `deploy-to-ec2.sh`** -- read, never edited.

## 3. CENSUS -- measured on the release branch

- `git diff --stat 38fe44d5cb HEAD` = ONE file: `infra/aws/ec2/EC2_MANIFEST.json | 2 +-` (1 insertion, 1 deletion; the pin).
- `git diff --stat 38fe44d5cb HEAD -- infra/aws/ec2/opal-gateway` = **NOTHING.**
- `MCPORTAL_RESOLVE_ONLY=1 bash infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` from the release tree prints `MCPORTAL-RESOLVED: <dir> @c66ca82952c01575968d16cc736cdabe36606572`.
- `ops/bun_cache_precheck.py bun.lock` against the `c66ca82952` lockfile: **77 of 77**; no package is fetched.
- How the release commit was made: the release tree's own `.tools/safe-commit.sh` refused on its frozen vintage (`NAMING ERROR ... KeyError: 'interval_form'`: the tree's `lib/` and `org/standards/NAMING_SCHEMA.json` are
  from different vintages). I ran the TRUNK's `.tools/safe-commit.sh` from inside the release tree instead: `NAMING-GATE: PASS 0 graded`, `committed 3cc7017f1f`. No gate was skipped or overridden.

## 4. TESTS -- `tests/test_admin*.py tests/test_owner_gate.py`, run in the release tree

**11 failed, 98 passed (109 collected).** Every failure is in a named class; there is no other.

**Five `FileNotFoundError` on a repo path outside `infra/aws/ec2/opal-gateway/`**, three paths, each `git ls-tree` **0 at the live base and 0 in the release tree, 1 at `box/sitez` HEAD**, and each test passes in the main tree at `box/sitez` HEAD:

| test id | missing path |
|---|---|
| `test_admin_fabric.py::test_roster_equals_devices_register` | `org/devices/DEVICES.json` |
| `test_admin_fabric_calls.py::test_real_capture_calls`; `test_admin_fabric_gitstate.py::test_real_capture_gitstate`; `test_admin_fabric_overlap.py::test_real_capture_overlap` | `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/cp2/fixtures/s3_capture_20261009T0728Z.json` |
| `test_admin_fabric_calls.py::test_request_accepted_by_open_calls_scan` | `.tools/open-calls-scan.py` |

**Six `AssertionError`, named by amendment A1 (msg 35003), failing identically at the live base** (the release tree is the live base plus the pin; neither failing file reads `EC2_MANIFEST`; I also reproduced the same six in the main tree at `box/sitez` HEAD, 6 failed / 74 passed over the six affected files; the issuer reproduced 6 failed / 37 passed). Cause per the issuer: the landed catalog declares a source for every tool, so tests expecting `undeclared` or pinning the inventory to `m365` are stale; their repair is the issuer's cell, not this release. Row `NFRA_MCPORTAL-Z-S67`.

- `test_admin_gateway_breakdown.py::test_every_live_tool_in_exactly_one_channel`
- `test_admin_gateway_breakdown.py::test_real_server_tool_inventory`
- `test_admin_people.py::test_people_lists_every_candidate_even_holding_nothing`
- `test_admin_people.py::test_cadence_reads_absent_with_reason`
- `test_admin_people.py::test_real_server_people_inventory`
- `test_admin_people.py::test_people_principal_never_leaks_into_other_fields`

## 5. ROLLBACK -- proven BEFORE the act

**The live bundle is the build of mcportal `090b9cdc85`.** Rebuilt from a clean detached mcportal worktree (`C:/tmp/mp-pf-mcp-old`, 0 local changes, HEAD `090b9cdc85ce3463e73915e68b44f4c21053a71c`), bun cache pre-check 77 of 77, `bun install --frozen-lockfile` (10 s) and `bun run build` (6 s), nothing uploaded. The host's `/opt/opal-gateway/dashboard/` was read over SSM, read-only (command `c1f37d09-d2fe-41d7-8aac-4f4a97cdbb87`, Success). **sha256, full 64 hex, build vs host: ALL FOUR EQUAL.**

| member | sha256 (host = old build) | new build (`c66ca82952`) |
|---|---|---|
| `index.html` | `a0ee33db3f2e23d748c3d24c43e55606d9bf77e1bea0e6a9b6851dd7721b802c` | `5a6e2eee...` DIFFERENT |
| `routes.json` | `e6d4a9ac3ce7d275158a56c490b586076cc0e728ae01501d5a0c88cba70207f1` | equal |
| `assets/index-pbBdUBWu.css` | `cd4abeddeb288651544763bb9919f030e239e8274c6fe44ede0c37a464ebbaa1` | `index-BRnJX9Mi.css` `120ae5bb...` DIFFERENT |
| `assets/index-DzjZpju-.js` | `52466cffc886f76eb1562351543fd31959392e18445f877d49d103a2447289fb` | `index-DbObnWYp.js` same content, new name |

**Negative control (the comparison discriminates):** the same members of the `c66ca82952` build (`C:/tmp/mp-pf-mcp-new`) differ from the host in `index.html` and the CSS, as the order says. The host's `index.html` names exactly `assets/index-DzjZpju-.js` and `assets/index-pbBdUBWu.css`; the host service reads `active`.

**Versioned artifact (PRE-ACT, to be re-read immediately before the act):** `opal-gateway-38fe44d5cb.tar.gz` 883,434 B, ETag `df5cba50f8b9fed87e224ec54c6d966b`, `git-ref` `38fe44d5cb8d37b6007fb7e5fa47a25316e01054`, LastModified 2026-10-16T12:18:42Z (equal to `-latest`). This act does not write that key.

**The command that re-deploys the previous pin** (named, not run). The rollback tree is a clean detached worktree at the live base, `C:/tmp/mp-pf-rb` @`38fe44d5cb`, whose manifest names `mcportal_commit` `090b9cdc85` (checked: 1 hit):

```
cd /c/tmp/mp-pf-rb && DEPLOY_BASE_REF=<the release commit then live> \
  bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh
```
That is the manifest edit back to `090b9cdc85` and the same deploy. If another release lands before a rollback, the rollback tree is re-cut on the then-live ref first (the stale-base guard refuses otherwise).

**Rollback TIME.** Neither script has a dry-run or no-op mode, so the bound is the release's own pull-and-restart, timed at the act and recorded in the close report. Measured offline here: the old bundle builds in ~16 s (install 10 s, build 6 s).

## 6. READ-BACKS -- independent of the deploy's rc

- `/health` polled immediately after the restart.
- **AC1** (`pf9.AC1.sh`) and **AC2** (`pf9.AC2.sh`): the order's literal invocations, after the close commit.
- **MCP tool surface:** before/after names on the host, both counts, difference EMPTY.

## 7. THE FAILURE BRANCH -- stated now so the two halves cannot contradict (MP-n-4's lesson)

My reading of the order, which I follow unless a half says otherwise in words both halves repeat:

- **ROLL BACK AT ONCE** (named command, ledger closed as rolled back, stop): `/health` not 200 within 90 s; or the before/after tool-name difference is non-empty; or `/` or `/gateway` answers a no-identity request with anything other than 401/403.
- **NO ROLLBACK; grade FAIL as measured and open a row:** AC2's bundle limbs alone miss (the host `index.html` or CSS does not equal the build of `c66ca82952`, or `index.html` does not name exactly the two assets) while `/health`, the tool surface and the 401/403 limb all hold. The old bundle is one redeploy away and the issuer decides.
- **The CTO half covers the act only if `deployed_commit` read at the act is `38fe44d5cb`** (and the S3 `-latest` `git-ref` equals it). Otherwise a new ask. At 12:2xZ the `~MI` ledger entries `nfra-mcpindex-r15-catalog-release`, `-v2` and `-v3` all read OPEN on this box; G-REL9's second condition (no `opal-gateway` release open) is the issuer's to confirm at the GO.

## 8. WHAT IS ASKED

Each half, citing this ASK by path and commit:

- `1.0.0_SA_CTO~Z` -- the CTO half.
- `2.0.0_SA_COO~MP` -- the COO half.

Please state in the half your disposition of **section 7's two branches** and of the **live-ref condition**. A refused half STOPS the act.
