# Removal receipts, call 5982 (IRPT_ANLREQ throwaway folders), 2026-10-15 ~05:2xZ

By `0.0.0_AB_MSTR~DELL2` on dell2. Authority: CTO ruling `CTO_RULING_DELL2_5982_IRPT_ANLREQ_THROWAWAY_FOLDERS_ON_D503_20261015.md`,
msgs 8068, 8074, 8075 (site Z ruled XA-20261015T050145Z-7f22 (b) at 05:05Z). Rule applied per path: read that the head is contained in
`box/dell2` and that the tree is clean (a modified `portal` pointer is not counted), then remove. One line per path.

## Removed (8)

| path | head | in box/dell2 | clean | action |
|---|---|---|---|---|
| wk-irpt-anlreq-120 | 35a0ff9daa | yes | yes | REMOVED |
| wk-irpt-anlreq-122 | 515f45f396 | yes | yes | REMOVED |
| wk-irpt-anlreq-74 | db1dea2a1c | yes | no: 1 file (worker ~78 amendment-1 edit of r22/PORTAL_FILE_NAME_CANDIDATE.json) | REMOVED on the ruling and COO~Y2 msg 8085. Its facts are in tracked `2.0.0_SA_COO~Y2/r22/PORTAL_FILE_NAME_CANDIDATE_AMEND1.json` @7ff2ede6ac (on origin/CLOUD, cites portal 73f9d64ca0, which is on portal origin/DEV). |
| irpt-release-r30/w131/trunk | 109f4671bb | yes | yes | REMOVED |
| irpt-release-r29b/wt-control-4279513f | 4279513f95 | yes | yes | REMOVED |
| irpt-release-r29b/wt-control-97d2d4be | 97d2d4bede | yes | yes | REMOVED |
| irpt-release-r29b/wt-release-ebbadcb0 | ebbadcb0e1 | yes | yes | REMOVED |
| irpt-release-r31s/wt-control-15a387dd36 | 15a387dd36 | yes | yes | REMOVED |

## Held (3): the tree is not clean, so the ruling's test is not met

| path | head | in box/dell2 | the one modified file | action |
|---|---|---|---|---|
| irpt-release-r30/w131/control | 0c0ae5a8f5 | yes | infra/aws/lambda/ci/lambda-source-map.json (27 insertions, 13 deletions) | HELD |
| irpt-release-r30/w131/release | 109f4671bb | yes | infra/aws/lambda/ci/lambda-source-map.json (4 insertions, 4 deletions) | HELD |
| irpt-release-r31s/wt-control-d39886e4aa | d39886e4aa | yes | infra/aws/lambda/ci/lambda-source-map.json (6919 insertions and 6919 deletions, a whole-file rewrite) | HELD |

All three read as build-worktree source-map stamps, but I have not shown that nothing in them is wanted. One ask to the CTO: say these three are throwaway and I remove them.

## Update, CTO msg 8095 (row S185): two of the three held were ruled throwaway and removed

| path | head | in box/dell2 | clean | action |
|---|---|---|---|---|
| irpt-release-r30/w131/control | 0c0ae5a8f5 | yes | no: source-map stamp; the CTO read its pins and shas already on trunk | REMOVED |
| irpt-release-r31s/wt-control-d39886e4aa | d39886e4aa | yes | no: source-map stamp; the CTO read its pins and shas already on trunk | REMOVED |
| irpt-release-r30/w131/release | 109f4671bb | yes | no | KEPT by the CTO: its stamp for irpt-ycharts-generate (pins 83eb798a, 5be427ba) is not on trunk; row IRPT_BCKEND-D2-S185, owner ~P2, held until ~P2 disarms |

So the first table's three "HELD" lines now read: two removed, one kept.

## Update 2, CTO msgs 8121, 8131, 8132: the third was removed, then the release was withdrawn; no loss

| path | head | in box/dell2 | clean | action |
|---|---|---|---|---|
| irpt-release-r30/w131/release | 109f4671bb | yes | no: source-map stamp | REMOVED at ~05:58Z under the CTO's 05:57Z release (8121). The CTO withdrew it at 05:59Z (8131; COO~Y2 8129 said the stamp is the IB-pr-456 build input, not the R29c record). My removal had already finished, so it could not be stopped. |

No loss, checked by recomputation at 06:0xZ. The stamp named uploads.py at 83eb798a (full 83eb798a0870a5e5fd6c46f31b38762accda6eee) and
interactive_access.py at 5be427ba (full 5be427ba7642f8ac244c92bcd55631e48605d6a9). Both commits are contained in box/dell2. The sha256 of
`infra/aws/lambda/investor-reporting/intake/uploads.py` at 83eb798a recomputes to 48f39329ea4c947d... and of
`infra/aws/lambda/investor-reporting/_scope/interactive_access.py` at 5be427ba to d416e3755d587b14..., equal to the values quoted by the CTO and
COO~Y2. Control: the same files at the trunk map's old pins (15a387dd36, f09b802cdc) recompute to f85e8c9b... and c28d9a74..., equal to trunk's
map. So the removed stamp is exactly reproducible from the two pins. The worktree itself is not recoverable.

## Not named by the ruling, left alone
`C:/dev/r30-control`, `C:/dev/r30-release`, `C:/dev/irpt-release-r28/wt-r30-release`, `irpt-release-r29/*` (KEEP), `wk-irpt-anlreq-102` and
`rel-anlreq-r4` (KEEP), the plain folders (act d8ae, Andrew's). Each removed worktree leaves a ~24 KB `portal/` stub holding a symlink to the shared
portal `node_modules`; I did not remove the stubs, because a recursive delete could follow that link into the live checkout.
