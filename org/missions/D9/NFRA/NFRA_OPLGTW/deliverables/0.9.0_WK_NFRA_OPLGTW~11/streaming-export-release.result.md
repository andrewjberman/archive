# OG-x-3 result -- narrow release of OG-x-2's streaming export (0.9.0_WK_NFRA_OPLGTW~11)

Release commit `4248b70b3911129588b96b32a4f74072151a8750` (rel-nfra-oplgtw-stream-export-v2, LOCAL) = the live gateway tree
(`7c7ebe14d3`, gateway tree `01264d4d90` = release `f791522306`) + only `0c3d545002`'s 9 gateway files. Deployed to
`i-07dccb1615503ac99` by `safe-ec2-deploy.sh` at 2026-09-29T05:22Z (service restarted 05:22:10Z); ssm
`ce0c7581-f646-4d20-b6b5-e927d3cf7f79` Success. Artifact `opal-gateway-4248b70b39.tar.gz` (+ latest).

## GO-time reads (unchanged from PHASE A)
Census over 92 worktrees: no gateway sentinel open except the superseded og-r-1 slug (`census_open_deploys_phaseB_go2.txt`).
Host: 76 of 76 files = 7c7ebe14d3's tree, 27 `.env` keys, `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph opal_discover
portal_index`, 51 tools (sorted diff empty), `/health` 200, service unrestarted since 03:25:06Z.

## Verify (read-only SSM at 05:23Z, within 90 s of the restart)
`/health` 200, service active; engine.py `b06a27f7...`, integration.py `f436630c...`, export.py `c9943e78...`,
envelope.py `651359f1...`, download_routes.py `74f8843e...` = 4248b70b39's bytes 5 of 5; 76-file host manifest = 4248b70b39's
tree 76 of 76 (`host_manifest_recut.txt` is the before; only the 4 schwab app files changed); tool list AFTER = BEFORE (51,
sorted diff empty); `ENABLED_INTEGRATIONS` unchanged (no `schwab`); 27 `.env` keys. Nothing rolled back.

## Record
EC2_MANIFEST.json (LF, 6 lines): `3152461491` (deployed_commit 4248b70b39, deployed_at 2026-09-29T05:22:18Z, release_note),
corrected by `1f15da8f48`: `previous_deployed_commit` = `f791522306` (the value CLOUD carried before this act), because xr.AC2
needs the previous commit to be an ancestor and the served deploy-only twin 7c7ebe14d3 is not; the release_note names 7c7ebe14d3
as the tree that was served. The issuer's GO named 7c7ebe14d3; this is a deliberate departure, one line, easy to reverse.
The wrapper's own manifest edit sat unstaged as a whole-file CRLF rewrite in /c/tmp/og-x3-rel2 and was not used.
Ledger `nfra-oplgtw-stream-export-release`: opened `7ca65d7885` before the act, closed `71c9c85205`, 4 of 4 legs proven.

## Criteria (re-run as written at HEAD 8c000d12ad, after the issuer's amendment A3)
Proof instance VALID (rc=0), all three PASS by output; the order is flipped `complete`.
- AC1 PASS: `entry files at HEAD=2; sentinel at HEAD=no; listed OPEN/HELD=0; SCAN DENOMINATOR: 13 of 13 sentinel(s) scanned` / `RESULT: PASS` / `exit=0`.
- AC2 PASS: `deployed_commit=4248b70b39... previous=f791522306... descends=yes; gateway files shipped 9, outside OG-x-2's set 0; streaming export carried 1` / `RESULT: PASS` / `exit=0`.
- AC3 PASS: `ssm command=5f17cf01-4b7a-4756-9bcd-14979af43d84 status=Success; /health=200; streaming export on host 1; schwab files equal deployed_commit 4 of 4; ENABLED_INTEGRATIONS unchanged=yes` / `RESULT: PASS` / `exit=0`.
Earlier runs (HEAD 1f15da8f48, before A3): AC1 and AC2 printed RESULT: PASS but their `<expect>` could not match (S9); AC3 FAIL on two stale
premises (S8). Both rows are DISARMED by amendment A3 @8c000d12ad (the issuer's ruling; the criteria were the defect). The manifest's
`previous_deployed_commit` = `f791522306` is ruled correct.

## Rows this order filed
S4 (stale og-r-1 sentinel copies, ruled STALE), S5 (artifact key of the deploy-only tree, ruled INERT), S6 (MX-r-4 ledger,
BLOCKING then cleared), S7 (MP-a-2 sentinel, BLOCKING then cleared), S8 (xr.AC3 premises), S9 (AC1/AC2 <expect> form).
