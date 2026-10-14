# NEVER-WIDEN ASK -- NFRA_MCPORTAL `MP-n-4`, the C17 round-2 gateway release

- **Asked by:** `0.7.0_AE_CloudOps~MQ`
- **Halves asked of:** `1.0.0_SA_CTO~Z` (CTO half) and `2.0.0_SA_COO~MP` (COO half)
- **Order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-n-4.c17r2-gateway-release.md`
  (Amendment 1 @`46d8c2160d`), `<risk>WORLD</risk>`
- **Release branch:** `rel-nfra-mcportal-c17r2` @`87beffddc5`, cut from the LIVE base
  `7eff14b2e620c8c1f688d41de6f37c09addde7b4`
- **Live base, read from the record at the cut and to be re-read at the act:** `EC2_MANIFEST.json`
  `services.opal-gateway.deployed_commit` = `7eff14b2e6...` on `box/sitez` (NFRA_MCPINDEX MX-r-11 v2)
- **GO commit:** `9d42320595` (MP-n-2). **Bundle: unchanged** -- `mcportal_commit` stays `0e02a1f`, which the
  release tree's manifest already carries, so there is NO pre-act manifest edit in this cell.
- **Time condition (issuer msg 33856):** `2.0.0_SA_COO~O` yields the gateway slot until 11:00Z. The ledger
  must be OPEN by 10:00Z and CLOSED by 10:30Z, else this cell follows r30's close.

## 1. BLAST RADIUS -- what this act may touch

| # | thing it touches | what moves |
|---|---|---|
| 1 | `app/admin_fabric_gitstate.py` | +45/-? in one module: `_refused` reads the per-box last-integrate pointer |
| 2 | `tests/test_admin_fabric_gitstate.py` | +93/-? -- source only, ships nowhere |
| 3 | `EC2_MANIFEST.json` `services.opal-gateway` | post-act only: `deployed_commit`, `previous_deployed_commit`, `release_note` |
| 4 | the running service | one `systemctl restart opal-gateway` on `i-07dccb1615503ac99` |
| 5 | two S3 keys | `ec2/opal-gateway/opal-gateway-<release sha>.tar.gz` (new) and `opal-gateway-latest.tar.gz` (overwritten) |

**NO route change. NO bundle change.** The dashboard bundle is rebuilt from the same mcportal commit
`0e02a1f` the live manifest already records, so the served `dashboard/` is unchanged in content.

**THE SEMANTIC CHANGE, named on both branches** -- the order calls it out and it is the only
user-visible behaviour this release moves. `GET /api/admin/fabric/gitstate`'s refusal field changes its
BASIS: it is read from the per-box last-integrate POINTER rather than by scanning the window.

- **Branch A, a box WITH a pointer:** the refusal field answers from that pointer.
- **Branch B, a box with NO pointer:** the field reads **"not recorded"**. That is a NEW reachable answer
  for such a box, and it is not an error -- it is the absence of a pointer stated honestly. Round 1's
  48 h-window read would instead have reported whatever the window happened to hold.

I have NOT verified branch B against a real pointer-less box, because this seat cannot create or remove a
pointer (the producer is outside this cell's write surface). What I can say is what the module's own code
does, and both halves should sign knowing branch B is reachable in production from the moment of the
restart.

## 2. WHAT IT MAY NEVER TOUCH

1. **The MCP tool surface.** No tool added, removed or renamed; read before and after, difference EMPTY.
2. **Any IAM.** The pointer sits under the gateway's existing read prefix; no grant moves.
3. **Any store write.** No new write and no new store call kind.
4. **The producer.** `.tools/fabric-gitstate.py` and anything that WRITES the pointer are untouched; this
   cell changes only the READER.
5. **Any Terraform, ALB, listener, security group, instance, secret or schedule.**
6. **Any other service in `EC2_MANIFEST.json`**, and the `mcportal_commit` field.
7. **`safe-ec2-deploy.sh` and `deploy-to-ec2.sh`** -- read, never edited.

## 3. CENSUS -- measured on the release branch

`git diff --name-only 7eff14b2e6 87beffddc5` over the WHOLE repo = **2 paths**:

```
infra/aws/ec2/opal-gateway/app/admin_fabric_gitstate.py          +45 -?
infra/aws/ec2/opal-gateway/tests/test_admin_fabric_gitstate.py   +93 -?
```
(`git diff --stat` reads 2 files changed, 86 insertions, 52 deletions.)

**Outside the C17R2 set = 0.** The working tree is clean at the release commit. The GO's commit was
re-authored to this lane -- the owned-paths hook grants a path by the COMMITTING serial's live task order,
and `0.9.0_WK_NFRA_MCPORTAL~17` holds none at HEAD. No conflict occurred.

## 4. TESTS -- step 1, both readings, per Amendment 1

| tree | result |
|---|---|
| `box/sitez` HEAD (the payload `9d42320595` is already an ancestor) | **21 passed, 0 failed** |
| the release tree @`87beffddc5` | **19 passed, 2 failed** |

**Both release-tree failures are admitted by Amendment 1's mechanism, and each is shown against it rather
than asserted:**

| test id | missing path | outside the gateway dir? | `ls-tree` at base | `ls-tree` at HEAD | passes at HEAD? |
|---|---|---|---|---|---|
| `test_admin_fabric_gitstate.py::test_real_capture_gitstate` | `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/cp2/fixtures/s3_capture_20261009T0728Z.json` | OUTSIDE | **0** | **1** | yes |
| `test_admin_fabric.py::test_roster_equals_devices_register` | `org/devices/DEVICES.json` | OUTSIDE | **0** | **1** | yes |

Both raise `FileNotFoundError`. **Positive control that this is a real vintage gap and not a sparse-cone
miss:** `org/missions/DIRECTIVES.yaml` and `org/ORG_CHART.md` both read `ls-tree` **1 at the base and 1 at
HEAD**, and the cone includes `/org/` whole. `cp2/fixtures/` itself lists **0 files at the base and 1 at
HEAD**, exactly as row `Z-S45` recorded. No other test failed.

## 5. ROLLBACK -- proven BEFORE the act, per key

**Key 1 -- the versioned artifact.** `opal-gateway-7eff14b2e6.tar.gz` is present and PRE-ACT: **557,605 B,
ETag `c8b27c104c2f95a6108eece752ccef66`, `git-ref` `7eff14b2e620c8c1f688d41de6f37c09addde7b4`,
LastModified `2026-10-13T23:49:56Z`.** This act does not write that key. It is re-read immediately pre-act.

**Key 2 -- `opal-gateway-latest.tar.gz`** IS overwritten (it currently carries the same ETag and ref). Its
rollback is the same redeploy.

**The rebuild, run and measured, with nothing uploaded.** A clean detached worktree at the live base
(`C:/tmp/mp-n4-rb`, 0 local changes) with mcportal detached at `0e02a1f`:

- bun cache pre-check **77 of 77, rc=0**; `bun install --frozen-lockfile && bun run build` ran fully
  offline, rc=0, with `dist/index.html` and `dist/routes.json` both present.
- re-tarred with `deploy-to-ec2.sh`'s exact member list and exclude set.
- **134 members vs 134; 111 files md5-compared, 111 EQUAL, 0 DIFFERENT, 0 only-in-either.** The two
  tarballs differ by 35 bytes of gzip header (557,570 vs 557,605), which is why the proof is on CONTENT and
  not on the archive's size: a `.tar.gz` is not byte-reproducible.
- **NEGATIVE CONTROL, so the comparison is known to discriminate:** the same walk against the RELEASE
  tree's `app/` reads 100 EQUAL and **1 DIFFERENT -- `admin_fabric_gitstate.py`** -- exactly this release's
  one payload module, and nothing else.

**The command that would re-deploy it** (named, not run):

```
cd /c/tmp/mp-n4-rb && DEPLOY_BASE_REF=<the release commit then live> \
  bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh
```

No Terraform, no ALB, no host, role or secret change in either direction.

## 6. READ-BACKS -- independent of the deploy's rc

- `/health` polled immediately after the restart; **not 200 within 90 s -> the rollback above runs AT ONCE**,
  the ledger closes as rolled back, the act stops.
- **AC1** (`checks/n4.AC1.sh`): the `nfra-mcportal-c17r2-release` entry committed at HEAD, sentinel gone,
  `deploy_ledger.py list` not listing it with its SCAN DENOMINATOR printed; `deployed_commit` descends from
  `previous_deployed_commit`; the gateway app/tests files between them are ONLY the two.
- **AC2** (`checks/n4.AC2.sh`, on the host over SSM): `/health` 200; `GET /api/admin/fabric/gitstate` with
  NO identity answers 401 or 403; and the SERVED module's own `_compute`, **cold**, under the instance role
  against the live store, printing its body-fetch count and reading at least 1 box `recorded`, **in 5 s or
  less.** Round 1's bar was 10 s and the issuer's dry run at this base read **9.7 s / 1,336 fetches /
  recorded=4 -- a FAIL.** So AC2 is the real question this release has to answer, and I will report the
  measured time and fetch count whichever way it falls.
- **MCP tool surface:** names listed before and after, both counts recorded, difference EMPTY. Note for the
  record: that reader sees the NATIVE registry (43); the SERVED surface is 67 (row `Z-S48`).

## 7. ONE THING YOU SHOULD KNOW BEFORE SIGNING, WHICH IS NOT MINE TO FIX

Row **`NFRA_MCPORTAL-Z-S49`**: the live `services.opal-gateway` record is internally inconsistent right
now. `deployed_commit` names MX-r-11 v2 (`7eff14b2e6`, 23:49:56Z, `~MI`), but `release_note` still opens
"NFRA_MCPORTAL MP-z-5" and `previous_deployed_commit` is `ad2acc0a93`, a MCPINDEX worker's own
release-chain commit that was never a deployed gateway -- the commit actually previously deployed is
MP-z-5's `64b3e54658` at 21:07:58Z. **AC1's chain limb cannot detect this**: `merge-base --is-ancestor`
reads yes for both the wrong and the right value, with `185dc04888 -> 64b3e54658` as the positive control
that the limb works and is merely under-specified.

**Consequence for this act, stated so neither half is surprised:** my step 4 writes
`previous_deployed_commit = 7eff14b2e6...` and a `release_note` for THIS release, which repairs both fields
going forward but leaves the MX-r-11 generation misattributed in history. I am not editing the MX-r-11
record -- it is NFRA_MCPINDEX's.

## 8. WHAT IS ASKED

Each half, citing this ASK by path and commit:

- `1.0.0_SA_CTO~Z` -- the CTO half.
- `2.0.0_SA_COO~MP` -- the COO half.

Please also state, in the half, your disposition of **section 1's branch B** (a pointer-less box reading
"not recorded", unverified against a real such box) and of **section 7**. A refused half STOPS the act.
