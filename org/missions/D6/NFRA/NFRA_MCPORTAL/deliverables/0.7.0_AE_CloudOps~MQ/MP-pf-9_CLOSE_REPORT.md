# MP-pf-9 CLOSE REPORT -- the bundle-only gateway release (Gateway page at 390 px)

**Order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-pf-9.gateway-page-bundle-only-release.md` (amendment A1 @`66a4be01d8`; GO-PREP msg 34994, ruling msg 35003, GO msg 35010).
**Actor:** `0.7.0_AE_CloudOps~MQ`. **Result: AC1 PASS, AC2 PASS. Ledger `nfra-mcportal-pf-bundle-release` CLOSED, 4 of 4 legs proven. No rollback taken.**

## 1. What landed

`opal-gateway` on `i-07dccb1615503ac99` now runs release commit `d14445961dd6d04275ca8186372a4df4c4fcc5cc` (branch `rel-nfra-mcportal-pf`, worktree `C:/tmp/mp-pf-rel`), cut on the live
base `38fe44d5cb8d37b6007fb7e5fa47a25316e01054`. The dashboard bundle is the build of mcportal `c66ca82952c01575968d16cc736cdabe36606572` (was `090b9cdc85`). `routes.json` is unchanged.

## 2. Census

`git diff --stat 38fe44d5cb 3cc7017f1f` = ONE file, `infra/aws/ec2/EC2_MANIFEST.json` (1+/1-). `git diff --stat ... -- infra/aws/ec2/opal-gateway` = NOTHING. The shipped commit `d14445961d` adds only the
ledger entry, its sentinel and the pre-act record on top (`org/`, shipped nowhere). AC1 reads `gateway files changed between them=0` (`38fe44d5cb` vs `d14445961d`).
Resolve-only printed `@c66ca82952`; bun cache pre-check 77 of 77 (the deploy's own build ran it again: 77 packages, `built in 964ms`).

## 3. MCP tool surface -- before and after (served registry, `app.server` imported)

| read | tools | names md5 |
|---|---|---|
| BEFORE (SSM `7b6faefe-3ec6-4b67-9924-c99698c6c294`, 13:14:49Z) | **127** | `4f5cf3218d92006fcddfefcdc9369a15` |
| AFTER (SSM `4dba1956-3a1b-4431-82a2-6bf4a79ed9ad`, 13:25:19Z) | **127** | `4f5cf3218d92006fcddfefcdc9369a15` |
| difference | **EMPTY** (0 added, 0 removed; name lists byte-equal) | identical |

Host after the act: `/health` 200, unit `active`, MainPID 1192771 -> 1195428 (since 13:23:55Z), no-identity `GET /` 401 and `GET /gateway` 401, `dashboard/index.html` sha256 `5a6e2eeef8ec0e9d...` naming exactly
`assets/index-BRnJX9Mi.css` and `assets/index-DbObnWYp.js` (before: `a0ee33db3f2e23d7...`, naming `index-DzjZpju-.js` and `index-pbBdUBWu.css`); `assets/` holds 14 files (12 + 2 added, none deleted).

## 4. The two check outputs

```
pf9.AC1.sh   (run from the release tree C:/tmp/mp-pf-rel after the close commit; see section 8, item 3)
entry files at HEAD=1; sentinel=no; listed OPEN/HELD=0; SCAN DENOMINATOR: 24 of 24 sentinel(s) scanned
mcportal_commit=c66ca82952c0 is c66ca82952: yes; descends from 090b9cdc85: yes; deployed=d14445961dd6 previous=38fe44d5cb8d differ: yes; gateway files changed between them=0
RESULT: PASS
exit=0

pf9.AC2.sh
ssm command=f7e29686-d30d-427f-955b-188af68573e9 status=Success; /health=200; no-identity / =401 /gateway=401
host index.html=5a6e2eeef8ec routes=e6d4a9ac3ce7 css=120ae5bbd491 js=52466cffc886; expected index=5a6e2eeef8ec
host bundle == build of c66ca82952: yes; index.html names exactly the two assets: yes
RESULT: PASS
exit=0
```
Controls: AC2's expected `index.html` (`5a6e2eee...`) is not the pre-act host read (`a0ee33db...`, the old build) -- the same four-member comparison that matched the old pin byte for byte before the act (the ASK, section 5).

## 5. Rollback time and how it was measured

- **Pull-and-restart: 20 s.** SSM `eb89810b-21a5-4e21-acfc-b16a98791ea1` `ExecutionStartDateTime` 13:23:37Z to `ExecutionEndDateTime` 13:23:57Z; the unit's `ActiveEnterTimestamp` is 13:23:55Z.
- **Whole wrapper: 102 s** (13:22:31Z to 13:24:13Z by `date -u` around the call): bundle build (install 9 s, build 1 s), tar, S3 upload of two keys (13:23:32Z, 13:23:35Z), SSM dispatch and restart, manifest write.
- Neither deploy script has a dry-run or no-op mode, so this is the release's own act, not a rehearsal; a rollback is the same act from `C:/tmp/mp-pf-rb` (~100 s).
- The first run of the wrapper (13:19Z, 32 s) was refused BEFORE any upload (row Z-S68); it is not in these figures.

## 6. Ledger and commits

Entry (CLOSED, sentinel removed): `org/critical_paths/change_management/20261016T1316Z_nfra-mcportal-pf-bundle-release_deploy_completion.md`. Pre-act record: `deliverables/0.7.0_AE_CloudOps~MQ/MP-pf-9_PRE_ACT_RECORD.md`.

| where | commit | what |
|---|---|---|
| `box/sitez` | `6d0e975dd7` | row Z-S67 (the six tests; ruled, A1) |
| `box/sitez` | `be51a362cd` | the never-widen ASK (halves: CTO `08e2ffae65`, COO `e8eb2d5f5d`) |
| `box/sitez` | this report's commit, with rows Z-S68 and Z-S69 and the proof instance | (stated in the message that carries it) |
| `rel-nfra-mcportal-pf` | `3cc7017f1f` | the one-line pin |
| `rel-nfra-mcportal-pf` | `d14445961d` | ledger open + sentinel + pre-act record (THE RELEASE COMMIT that shipped, `git-ref` on both S3 keys) |
| `rel-nfra-mcportal-pf` | `bddaf03886` | manifest record (`deployed_commit`, `previous_deployed_commit` corrected to `38fe44d5cb`, `release_note`) |
| `rel-nfra-mcportal-pf` | `864f262ffc` | ledger close, sentinel removed |
| `rel-nfra-mcportal-pf` | `f829a3eaa8` | re-added the pre-act pointer line that `deploy_ledger.py close` dropped |

Release commit `d14445961d`, mcportal commit `c66ca82952c01575968d16cc736cdabe36606572`. S3: `opal-gateway-d14445961d.tar.gz` and `-latest`, 883,434 B, ETag `ce83561b919f47b82119a79c63efe052`, `git-ref` the release commit on both;
rollback key `opal-gateway-38fe44d5cb.tar.gz` untouched (883,434 B, ETag `df5cba50f8b9fed87e224ec54c6d966b`).
**Push state:** `rel-nfra-mcportal-pf` is LOCAL (`git ls-remote origin refs/heads/rel-nfra-mcportal-pf` returned nothing); `box/sitez` on origin reads `b3d08526a1` (ls-remote, 13:4xZ) and does not carry the commits in this table. The branch is the drain's.

## 7. Rows

- `NFRA_MCPORTAL-Z-S67` (BLOCKING at filing; ruled by the issuer, msg 35003).
- `NFRA_MCPORTAL-Z-S68` (OBSERVATION): the order's sparse list omits `/data/mdpf/config/`; the deploy refused before any upload until it was added.
- `NFRA_MCPORTAL-Z-S69` (OBSERVATION): a release tree's own naming gate cannot run (vintage mismatch), so the wrapper's manifest commit failed after the landed deploy; commits ran through the trunk's `safe-commit.sh`.

## 8. Disclosures

1. **The wrapper's manifest commit was refused** (row Z-S69) AFTER the deploy landed; I recorded the release myself in `bddaf03886`. `previous_deployed_commit` was the tree's stale `2c0f84966d` and is corrected to `38fe44d5cb`; the `release_note` is prepended to the trunk's chain (the tree's own was the older vintage).
2. **First deploy run refused, nothing moved** (row Z-S68). Before the re-run I read the three files the script stages (`partner_roster.json`, `scopes.json`, `lib/opal_naming.py`) on the host over SSM: md5 equal to the release tree's.
3. **AC1 and AC2 were run from the release tree with the issuer's scripts staged untracked there** (byte-identical by `cmp`, removed after): a release tree's `org/` does not carry `pf/checks/`, and `_root.sh` resolves its root from the script's own location. AC1 reads the release branch's HEAD
   (`f829a3eaa8`); the check output above is from that run. During the cleanup I removed the tracked `round3/` files of that tree by mistake and restored them from HEAD (`git status` clean, HEAD unchanged).
4. **The three MX-r-15 `~MI` ledger entries read CLOSED** at the act (the list showed only `nfra-mcpindex-r7-bd-doc-retire`, not the gateway), so no SUPERSEDED close was needed (the CTO half's condition).
5. **The MCP tool surface is 127, not the 70 of the earlier releases**: the landed catalog (MX-r-15) moved it before this act; the before and after of THIS act are equal.
6. **Not verified:** the rendered Gateway page at 390 and 1280 px (the issuer's graded real run, per the order); an owner-authenticated read of any route; whether the old assets on the host are ever pruned (this act deleted none).

## 9. Held

`C:/tmp/mp-pf-rb` (the proven rollback tree) and `C:/tmp/mp-pf-mcp-old` / `-new` (the two bundle builds) are held until the round closes; with the earlier rollback trees `C:/tmp/mp-n4-rb`, `mp-pc5-rb`, `mp-z5-rb`. `C:/tmp/mp-pf-rel` holds the unlanded release branch (5 commits over the live base).
