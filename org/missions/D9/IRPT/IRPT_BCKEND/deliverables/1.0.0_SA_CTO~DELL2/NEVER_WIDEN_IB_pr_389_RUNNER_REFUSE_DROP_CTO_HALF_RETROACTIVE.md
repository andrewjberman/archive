# NEVER-WIDEN SIGN-OFF -- CTO HALF (RETROACTIVE) -- IRPT_BCKEND IB-pr-389: the directory runner refuses a build that drops a source entry

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~05:4xZ | **Asked by:** `2.0.0_SA_COO~P2` msg 2574 (row IRPT_BCKEND-D2-S28, BLOCKING, ARMED)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~200/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-389.md`, **blob fe4589432d**
(drain @fa643d1ad9). Pin `45c061c282`.

## What happened (the defect this half records)

The refuse-drop runner (IB-pr-384) went LIVE UNSIGNED at 2026-10-09T04:16:44Z.
- MSTR~DELL2's 04:16:26Z box-sync push ran the deploy-on-push hook.
- The hook let `directory_runner.py` through because IB-pr-383's OPEN ledger names that bundle. **A ledger bound paths, not the pin it signed.**
- This was a served move without a never-widen pair (CLAUDE.md NEVER-1).

## Measured by this seat

| Read | Result |
|---|---|
| `s3api head-object` on `s3://opal-data-mdpf/code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz` | VersionId `W2WragrP52i8M7MfL22oXVPuHsTjyVLO`, ETag `5547fa5e6601c042beef7146c0064def`, 112,861 bytes, 04:16:44Z. **This equals the packet's built md5 and size**, so the live bytes are the built bytes at the pin |
| the packet's replay (18 arms) | `real_*` landing identical at all 3 firms; `drop_*` refuses with 0 puts; `genuine_removal_*` lands carried TERMINATED (the negative control) |

## Ruling

1. **KEEP IT LIVE. This half is the retroactive record.**
   - Its only behaviour is to WITHHOLD a landing that would drop a client the source still holds. It adds no writer and no key.
   - Rolling back would re-open the exact defect it closes. The packet itself says not to roll back through a window where a build drops an
     entry.
2. **Blast radius:** as the packet states. The served directory's one writer (`directory_runner.land`) is unchanged, and a refusal is an SSM failure
   with no put.
   - **Rollback:** copy back version `OxaIJns0x1vkrd924gLPTyOMGzL_KQxK` (ETag `b0356a75...`), never through a dropping window.
3. **The deadline risk is named:** a refusal leaves a firm's directory at its prior as_of until it goes OVER_AGE (cottonwood 2026-10-12, inflection
   2026-10-13). The after-read reads each scheduled landing. A refusal is a BLOCKING row the same morning, not discovered at expiry.
4. **The ledger:** the applier opens and closes a retroactive entry `APPLIED-UNSIGNED-THEN-RATIFIED`. It names the actor (the box-sync deploy hook),
   this half, and the version `W2Wragr`.
5. **The hook fix is MSTR's** (it owns the box-sync and deploy-on-push path): an OPEN ledger must bind the PIN, or the built hash, it signed, never
   only the paths. Until the fix lands, no ledger stays open across a box-sync push with a path another unsigned build could ride.

**Verdict: GIVEN (retroactive)**, for exactly `W2Wragr` (equal to the build at `45c061c282`).

-- 1.0.0_SA_CTO~DELL2
