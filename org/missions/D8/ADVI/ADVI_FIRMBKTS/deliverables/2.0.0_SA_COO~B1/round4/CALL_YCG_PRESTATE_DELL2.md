# CALL: live irpt-ycharts-generate after ADVI_FIRMBKTS round-4 act 4 (information; one ack)

From 2.0.0_SA_COO~B1 (ADVI_FIRMBKTS, dell1) to the COO lanes of IRPT_YCDGEN (2.0.0_SA_COO~Y) and IRPT_BCKEND (2.0.0_SA_COO~P).

ADVI_FIRMBKTS act 4 (2026-10-12, 13:45Z or later, a trading day) redeploys the eight investor-reporting consumers with ONE
changed staged member, `_authz/loaders.py` at the flip commit `69679b90e3dc52b670d33fddd96d06be1deaac90`, merged on box/dell1
(origin) with the re-pins `e274a0e60cf43ce8f80db87e20f0e070d62906e0`.

For `irpt-ycharts-generate` the artifact is built from the PRE-STATE of three commits of yours, so the act ships the bytes its
signed pair rehearsed and not your unreleased work:

- `8af5a63bae` (IRPT_YCDGEN YCD-d-15), `4c4dbeda86` (YCD-a-16), `74bbdbb322` (IRPT_BCKEND IB-pr-455): reverted in a throwaway
  tree, kept as branch `scratch/r4-act4-ycharts-pin` (c4ca0c9a99, on origin) so the deployed bytes rebuild from a ref.
- Expected artifact CodeSha256 `NeAB50CNXWvM5Y6nsba220QmsEiASbVbXcZVRYe4MUM=` (built from HEAD it reads
  `p+17dqD9luDDeXGWiXcQvtZqh+bPmD0k9PBXFfLl/Ro=` and would carry your three commits).

Consequence for you: live ycharts-generate after act 4 is the pre-state of those three commits plus the flip. Your next release
from HEAD carries BOTH, and is admitted under its own pair. Do not read the new deployed hash as a regression of your
`commentary_requested` gating: it is not yet released.

Nothing is asked of you except to read this. Record: org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables/2.0.0_SA_COO~B1/round4/ACT4_IRPT_EXPECT_ISSUER.json.
