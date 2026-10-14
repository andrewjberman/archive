# MP-n-4 PRE-ACT RECORD -- the C17 round-2 gateway release

**Order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-n-4.c17r2-gateway-release.md`
(Amendment 1 @`46d8c2160d`). **Actor:** `0.7.0_AE_CloudOps~MQ`. **Slug:** `nfra-mcportal-c17r2-release`.
**Risk:** WORLD. Written BEFORE the act; nothing here is a prediction.

## 0. The pair -- both halves SIGNED at `box/sitez` HEAD, and they AGREE only after an amendment

| half | file | commit | state |
|---|---|---|---|
| CTO | `deliverables/1.0.0_SA_CTO~Z/NEVER_WIDEN_HALF_CTO_MP-n-4_20261014.md` | signed `55db595800`, **amended `e77ac5d642`** | SIGNED |
| COO | `deliverables/2.0.0_SA_COO~MP/NEVER_WIDEN_HALF_COO_MP-n-4_20261014.md` | signed `7699a36c1e`, **adopts the amendment `28683249be`** | SIGNED |

ASK: `deliverables/0.7.0_AE_CloudOps~MQ/NEVER_WIDEN_ASK_MP-n-4.md` @`3f7f1097e7`. Both cite it.

**The halves first CONTRADICTED each other on the AC2 failure branch** -- the CTO said roll back, the COO
said do not -- and this seat refused to adjudicate between two signed halves, raising it instead (msg
33877/33878) before the act rather than discovering it mid-failure. The resolution, read from the bytes at
HEAD and not from the messages:

- An AC2 **time** FAIL is graded FAIL and reported as measured, **with NO rollback**, provided `/health`
  and the tool surface hold.
- **The rollback DOES run** if the measured cold `_compute` is **SLOWER than the base's 9.7 s**, or if
  **0 boxes read `recorded`**.
- A FAIL under the bar but no worse than the base opens a row.

## 1. Census -- the whole repo

`git diff --name-only 7eff14b2e620c8c1f688d41de6f37c09addde7b4 87beffddc5` = **2 paths**:

```
infra/aws/ec2/opal-gateway/app/admin_fabric_gitstate.py
infra/aws/ec2/opal-gateway/tests/test_admin_fabric_gitstate.py
```

`--stat`: 2 files changed, 86 insertions, 52 deletions. **Outside the C17R2 set = 0.** No conflict. The GO
commit `9d42320595` was re-authored to this lane, because the owned-paths hook grants a path by the
COMMITTING serial's live order and `0.9.0_WK_NFRA_MCPORTAL~17` holds none at HEAD.

**No pre-act manifest edit:** the release tree already carries `mcportal_commit = 0e02a1f`, which the
order requires be left as the live manifest records it.

## 2. Test counts -- step 1, per Amendment 1

| tree | result |
|---|---|
| `box/sitez` HEAD (the payload is already an ancestor) | **21 passed, 0 failed** |
| the release tree @`87beffddc5` | **19 passed, 2 failed** |

Both release-tree failures are admitted by Amendment 1's mechanism, each shown against it:

| test id | missing path | outside the gateway dir | `ls-tree` base | `ls-tree` HEAD | passes at HEAD |
|---|---|---|---|---|---|
| `test_admin_fabric_gitstate.py::test_real_capture_gitstate` | `.../2.0.0_SA_COO~MP/cp2/fixtures/s3_capture_20261009T0728Z.json` | yes | **0** | **1** | yes |
| `test_admin_fabric.py::test_roster_equals_devices_register` | `org/devices/DEVICES.json` | yes | **0** | **1** | yes |

Both raise `FileNotFoundError`. **Positive control:** `org/missions/DIRECTIVES.yaml` and `org/ORG_CHART.md`
read `ls-tree` **1 at the base and 1 at HEAD** with `/org/` whole in the cone, so this is a vintage gap and
not a sparse-cone miss. `cp2/fixtures/` lists **0 files at the base, 1 at HEAD**. No other test failed.

## 3. Rollback -- proven, nothing uploaded

- **Versioned key, re-read immediately pre-act:** `opal-gateway-7eff14b2e6.tar.gz` -- **557,605 B, ETag
  `c8b27c104c2f95a6108eece752ccef66`, `git-ref` `7eff14b2e620c8c1f688d41de6f37c09addde7b4`, LastModified
  `2026-10-13T23:49:56Z`.** Unchanged, and not a key this act writes.
- **Rebuilt from a clean tree** (`C:/tmp/mp-n4-rb`, detached at the base) with mcportal at `0e02a1f`: bun
  cache pre-check 77 of 77 rc=0, build fully offline, re-tarred with `deploy-to-ec2.sh`'s exact member list
  and excludes. **134 members vs 134; 111 files md5-compared, 111 EQUAL, 0 DIFFERENT, 0 only-in-either.**
  The archives differ by 35 bytes of gzip header (557,570 vs 557,605), which is why the proof is on CONTENT:
  a `.tar.gz` is not byte-reproducible.
- **NEGATIVE CONTROL:** the same walk against the RELEASE tree's `app/` reads 100 EQUAL and **1 DIFFERENT,
  `admin_fabric_gitstate.py`** -- exactly this release's one payload module.
- **One benign divergence, declared rather than ignored:** `git status` in the rollback tree reads
  `M mcportal`, because that is a GITLINK and I checked the bundle out there. The base records
  `fa1ff9693b...` (mcportal PROD) while the manifest says `0e02a1f`. It does not matter, and the script says
  why at `deploy-to-ec2.sh:44`: *"mcportal dashboard source: the MANIFEST's commit, never whatever the
  checkout happens to be at"* -- `MCPORTAL_WANT` is read from `EC2_MANIFEST.json` at `:57`. No tracked
  source file is modified.
- **Command** (named, not run): `cd /c/tmp/mp-n4-rb && DEPLOY_BASE_REF=<the release commit then live> bash
  infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`

## 4. The live world BEFORE the act (SSM `6928443d-a229-41c7-9326-03f2a315c2a6`, Success)

- `deployed_commit` on `box/sitez` = **`7eff14b2e620c8c1f688d41de6f37c09addde7b4`**, equal to the cut base
  (COO condition 2). `/health` **200**, unit **active**, **MainPID 1080008**.
- **MCP tool surface BEFORE = 67 names** (`md5 dbc48e6991b924a380b886da0714ac22` over the sorted
  comma-joined list). This read imports `app.server` first, so it is the **SERVED** registry, not the
  43-name native one -- the correction row `Z-S48` earned on MP-z-5, applied here from the start.
- **Cold-ish `_compute` = 8.1 s over 4 boxes.** This is NOT the AC2 figure and is not used as one: my
  ad-hoc probe does not assert an empty body cache, so 8.1 s may be a warm sample. **The authoritative
  base figure is the issuer's 9.7 s via the real probe**, and that is the number the rollback guard compares
  against.

### Condition B-1, the BEFORE half of the four-row table

Every box reads `integration_refused = 'not recorded'` under the ROUND-1 basis, which is the window-scan
rule the deployed code still uses:

| box | `integration_refused` BEFORE | basis BEFORE |
|---|---|---|
| laptop | `not recorded` | newest integrate pass within 48 h decides; history older than the window is not read |
| sitez | `not recorded` | same |
| dell1 | `not recorded` | same |
| dell2 | `not recorded` | same |

**So all four already read "not recorded" before this release.** The COO half measured the pointer itself
as PRESENT for laptop and ABSENT (404) for sitez, dell1 and dell2, so after the act laptop is the one box
whose answer CAN change basis, and the other three keep the same words for a different reason. The AFTER
half of this table goes in the close report.

## 5. Legs, and what stops the act

The order names three, and this record uses exactly those three. **AC1 and AC2 are deliberately NOT legs:**
on MP-z-5 a verify leg that cited AC1 could not close, because AC1's first limbs read the sentinel that
only the close removes. That circularity is not repeated here; the checks are graded in the close report
and the proof-of-spec instance.

1. **L1** release build + upload -- `opal-gateway-<release sha>.tar.gz` and `-latest.tar.gz`.
2. **L2** SSM pull + restart on `i-07dccb1615503ac99`.
3. **L3** manifest record -- `deployed_commit`, `previous_deployed_commit` = `7eff14b2e6...`, `release_note`.

**STOP / ROLLBACK conditions:** `/health` not 200 within 90 s. A non-empty MCP tool-name difference. A cold
`_compute` SLOWER than 9.7 s, or 0 boxes `recorded`. `deployed_commit` no longer `7eff14b2e6` at the act.
Any failing test id outside the two named above.

**Time condition:** the ledger must be OPEN by 10:00Z and CLOSED by 10:30Z (issuer msg 33856;
`2.0.0_SA_COO~O` yields the gateway slot until 11:00Z). This record is written at ~01:2xZ.
