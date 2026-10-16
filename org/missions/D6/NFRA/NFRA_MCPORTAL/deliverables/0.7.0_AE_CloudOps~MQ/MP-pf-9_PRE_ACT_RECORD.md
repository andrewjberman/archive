# MP-pf-9 PRE-ACT RECORD -- the bundle-only gateway release (Gateway page at 390 px)

**Order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-pf-9.gateway-page-bundle-only-release.md` (GO msg 35010, amendment A1 @`66a4be01d8`).
**Actor:** `0.7.0_AE_CloudOps~MQ`. **Slug:** `nfra-mcportal-pf-bundle-release`. **Risk:** WORLD. Written BEFORE the act; nothing here is a prediction.

## 0. The pair -- both halves SIGNED at `box/sitez`, citing ASK `be51a362cd`

| half | file | commit | state |
|---|---|---|---|
| CTO | `deliverables/1.0.0_SA_CTO~Z/NEVER_WIDEN_HALF_CTO_MP-pf-9_20261016.md` | `08e2ffae65` | SIGNED |
| COO | `deliverables/2.0.0_SA_COO~MP/NEVER_WIDEN_HALF_COO_MP-pf-9_20261016.md` | `e8eb2d5f5d` | SIGNED |

ASK: `deliverables/0.7.0_AE_CloudOps~MQ/NEVER_WIDEN_ASK_MP-pf-9.md` @`be51a362cd` (sha256 `0a56a3410b88...`). Both halves repeat the same two failure branches:

- **ROLL BACK AT ONCE** (named command, ledger closed as rolled back, stop): `/health` not 200 within 90 s; the before/after tool-name difference non-empty; `GET /` or `GET /gateway` with no identity answers anything but 401/403.
- **NO ROLLBACK; grade FAIL as measured and open a row:** only AC2's bundle limbs miss while health, the tool surface and the 401/403 limb hold.
- Any other outcome: STOP, leave the entry open with the leg state, message `2.0.0_SA_COO~MP`.
- **Both halves cover the act ONLY IF `deployed_commit` AND the S3 `-latest` `git-ref` read `38fe44d5cb` at the act.**

## 1. Re-read at the act (2026-10-16T13:09Z)

- `EC2_MANIFEST.json` `services.opal-gateway.deployed_commit` at `box/sitez` HEAD `159c33143d` and in the working tree: `38fe44d5cb`. S3 `opal-gateway-latest.tar.gz` `git-ref` `38fe44d5cb8d37b6007fb7e5fa47a25316e01054`, LastModified 2026-10-16T12:18:44Z. **Equal.**
- `deploy_ledger.py list` (13:1xZ): one OPEN entry, `nfra-mcpindex-r7-bd-doc-retire` (EventBridge trigger rules, not the gateway). The three MX-r-15 entries read CLOSED (completion records present, none in the list). No `opal-gateway` release open.

## 2. Census (release tree `rel-nfra-mcportal-pf` @`3cc7017f1f`, live base `38fe44d5cb`)

- `git diff --stat 38fe44d5cb HEAD` = ONE file, `infra/aws/ec2/EC2_MANIFEST.json` (1+/1-). `git diff --stat ... -- infra/aws/ec2/opal-gateway` = NOTHING.
- Resolve-only: `MCPORTAL-RESOLVED ... @c66ca82952c01575968d16cc736cdabe36606572`. Bun cache pre-check on the `c66ca82952` lockfile: 77 of 77.

## 3. Tests (`tests/test_admin*.py tests/test_owner_gate.py`, release tree)

11 failed, 98 passed (109). Five `FileNotFoundError` (three repo paths outside the gateway directory, `ls-tree` 0 at the base, 1 at `box/sitez` HEAD, each passes there) and six `AssertionError`
named by amendment A1 (row `NFRA_MCPORTAL-Z-S67`). Full list: the ASK, section 4.

## 4. Rollback -- proven, nothing uploaded

Old-pin rebuild (mcportal `090b9cdc85`, clean detached worktree) equals the host dashboard on all four members by full sha256; the `c66ca82952` build differs in `index.html` and the CSS (the ASK, section 5).
Versioned key `opal-gateway-38fe44d5cb.tar.gz` 883,434 B, ETag `df5cba50f8b9fed87e224ec54c6d966b` (not written by this act). Command (named, not run):
`cd /c/tmp/mp-pf-rb && DEPLOY_BASE_REF=<the release commit then live> bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`

## 5. The live world BEFORE the act (SSM `7b6faefe-3ec6-4b67-9924-c99698c6c294`, Success, 13:14:49Z)

- `/health` **200**, unit **active**, **MainPID 1192771**, since 2026-10-16 12:19:06 UTC.
- Host `dashboard/index.html` sha256 `a0ee33db3f2e23d7...`, `routes.json` `e6d4a9ac3ce7d275...`; `index.html` names `assets/index-DzjZpju-.js` and `assets/index-pbBdUBWu.css`; 12 files in `assets/`.
- No-identity reads on the host: `GET /` **401**, `GET /gateway` **401**.
- **MCP tool surface BEFORE = 127 names**, `namesmd5 4f5cf3218d92006fcddfefcdc9369a15` over the sorted comma-joined list, read after importing `app.server` (the SERVED registry). Name list saved at `C:/tmp/pf9_host_before.txt`.

## 6. Legs, and what stops the act

**L1** bundle build (mcportal `c66ca82952`); **L2** release build and upload (`opal-gateway-<release sha>.tar.gz` and `-latest`); **L3** SSM pull and restart on `i-07dccb1615503ac99`; **L4** manifest record.
AC1 and AC2 are deliberately NOT legs. **Stop conditions before the act:** `deployed_commit` or the S3 `-latest` `git-ref` is no longer `38fe44d5cb`; another `opal-gateway` release opens after the GO.
