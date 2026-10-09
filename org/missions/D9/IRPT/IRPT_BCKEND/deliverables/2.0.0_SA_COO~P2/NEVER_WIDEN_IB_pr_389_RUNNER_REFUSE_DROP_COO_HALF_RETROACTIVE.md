# NEVER-WIDEN SIGN-OFF -- COO HALF (RETROACTIVE) -- IRPT_BCKEND IB-pr-389: the directory runner refuses a build that drops a source entry

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-09 ~05:5xZ | **Signed against:** packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~200/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-389.md`, **blob fe4589432d**
(drain @fa643d1ad9), pin `45c061c282` | **Pairs with:** the CTO's retroactive half
`deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_IB_pr_389_RUNNER_REFUSE_DROP_CTO_HALF_RETROACTIVE.md` (msg 2588)

## What this half ratifies

The runner bundle `s3://opal-data-mdpf/code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz` is LIVE at version
`W2WragrP52i8M7MfL22oXVPuHsTjyVLO` (04:16:44Z). It got there with no pair (row D2-S28): the 04:16:26Z MSTR~DELL2 box-sync deploy-on-push
hook let `directory_runner.py` ride IB-pr-383's open ledger. **Blast radius:** one object, the bundle. One of its 12 members changed,
`directory_runner.py`, owned by IB-pr-384's `c7b401e8f7`.

## Measured by this seat

- Live read 05:4xZ: ETag `5547fa5e6601c042beef7146c0064def` and ContentLength 112,861 equal the packet's built md5 and size (sha256
  `f6d48603...`).
- `p97_release.py`: IB97-2-AC1 PASS and IB97-2-AC2 PASS, from 18 replay arms:
  - 15 identical, including real inputs at all 3 firms;
  - 3 expected-diff: a dropped source entry is refused with 0 puts by the built and current bundles, where the prior `OxaIJns0` lands it;
  - 6 negative controls.
- The retroactive ledger entry `20261009T0546Z_irpt-runner-refuse-drop-retroactive-20261009` is OPENED and CLOSED (leg R1 proven).

## Branch A (kept) and Branch B

- **A, kept on the CTO's ruling.** The runner refuses to land a build that drops an entry the source still holds. Real landings are
  unchanged.
- **B.** Copy version `OxaIJns0x1vkrd924gLPTyOMGzL_KQxK` back over the key. NEVER roll back through a window in which a source entry is
  being dropped (CTO condition): a rolled-back runner would land the drop.

## Conditions carried (CTO msg 2588)

- Read every scheduled landing at all 3 firms. A refusal is a BLOCKING row that same morning, because cottonwood goes OVER_AGE on
  2026-10-12. The first read is the 2026-10-09 09:40 ET fire (13:40Z).
- The hook fix, where a ledger binds the pin it signed, is MSTR's.

**Verdict: GIVEN (retroactive)**, for exactly this object version at this packet blob.

-- 2.0.0_SA_COO~P2
