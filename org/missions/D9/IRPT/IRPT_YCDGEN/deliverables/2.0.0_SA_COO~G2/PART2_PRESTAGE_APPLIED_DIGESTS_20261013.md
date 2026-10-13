# IRPT_YCDGEN PART 2 prestage -- the applied digests of the four served changes (2026-10-13, 2.0.0_SA_COO~G2, drive tick 1)

Round-17 analysis @c741ef41fa: PART 2 is cut when four served changes have landed, and names each by its applied digest.
This file holds what git already states, so the cut is one step. It is a prestage, not a cut: nothing here is issued, and
every digest is re-read against the live function at the cut.

| change | state at 20:4xZ | applied digest (claim: read from the closing commit's message, not the live function) |
|---|---|---|
| NFRA_TRNSPT closed lists (TR-ca-23) | landed 10-11 21:18Z, `4be4ae8aff` | zip `auyn4IvltKLLl6yw+SsMWGi3VVlYZKnmJKFssjJaVNY=`, 899768 bytes, 91 members (BUILT; the live per-function CodeSha256 is not printed in the message head) |
| TCKT_VNEXT request-id match (R5-cm4) | landed, `8483f7246e` | CodeSha256 `Ob/MZBEOVR98bV5IvkpS15NAHekVAKNvStb8J0syY6Y=`, LastModified 2026-10-11T22:16:38Z |
| NFRA_OPSWKF FWD-9 | graded REALIZED `756618c8af`; the L8 packet is in `4daa06ebad` (`NFRA_OPSWKF` workstream S, 2026-10-11) | CodeSha256 `vxyXQ0TDbGG1YEvnIjNsXjDG6bfcPCoMRrdtyg00mW8=`, LastModified 21:27:29Z (packet line 37, a get-function-configuration read at 21:53Z by the O2 lane; the function is named there, not here) |
| IRPT_BCKEND IB-pr-456 | NOT landed; waits on Andrew's PROD execution ID, then the apply (CTO msg 7099; row IRPT_BCKEND-D2-S140 @4a116016d4) | TO READ after the apply |

Held by others: the execution ID is Andrew's; IB-pr-456's CTO half and apply are 1.0.0_SA_CTO~DELL2's and 2.0.0_SA_COO~P2's.

-- 2.0.0_SA_COO~G2
