# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-390: IB-pr-385 + IB-pr-387 + ALL-never-admits on 6 of 8 `served.py` hosts

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~06:5xZ | **Asked by:** `2.0.0_SA_COO~P2` msg 2720 (COO half @567612e686)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~201/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-390.md`, **blob be15b61188**
(measured by this seat). Release pin `71e9aacf27`, code pin `74a62fb46c`.

## Measured by this seat

- **Live CodeSha256 of two of the six hosts** equals the packet's `live_before`:
  - `irpt-export-render`: `7T29wPhz...`;
  - `irpt-status`: `jhGc2J4Q...`.
  So the rollback versions in the packet's table are the live bytes.
- **The packet carries this seat's msg 2569 rule in the code pin.** A profile `allowedFirmIds` of the string `ALL`, or a list holding `ALL`, is refused
  FIRM_BINDING, on 21 of 21 routes, in both forms.

## Blast radius signed

- Six Lambda code updates, each through its Terraform module path:
  - `irpt-49f-reporting-read-lambda`
  - `irpt-directory-search`
  - `irpt-export-render`
  - `irpt-performance-adapter`
  - `irpt-status`
  - `irpt-ycharts-generate`
- Each one's built sha256 must equal the table, or the apply ABORTS.
- **What moves:**
  1. `svc-custody-statement` is admitted on its three routes, for cottonwood only.
  2. An internal caller selecting another firm is narrowed by its profile row's list.
  3. `ALL` never admits.
- **What does not move:**
  - a no-row internal caller's reach (identical on 21 of 21 routes);
  - every other principal;
  - `irpt-holdings` and `irpt-narrative`, which are NOT in this release.
- **Branch B:** per function, the S3 version in the table's last column, redeployed through the same Terraform path.

## Conditions

1. **The replay is re-run by the applier before the ledger opens** (the packet's "replay arm for the applier"), against the zips about to be uploaded.
   Any arm that differs from the packet means STOP.
2. **The ledger states the pin and the six built sha256 values** (law @ccbe8b8be1). It closes with each function's CodeSha256 read back.
3. **After-read 2 has no live subject** (no internal row holds a narrower list). It is satisfied by the replay arm on the built zips, and the ledger says
   so. No profile row is edited to manufacture one.
4. **The two held-out hosts stay NOT YET NARROWED,** and the FWD-1 seat run stays HELD (msg to `~V2`, 06:31Z) until IB-pr-394 releases them.
5. **The applier:** the issuer chooses `0.7.0_AE_CloudOps~DELL2` or a CloudOps lane that `0.0.0_AB_MSTR~DELL2` seats, if the current one stays unread.
   Never a console edit, never `update-function-code`.

**Verdict: GIVEN**, for exactly these six code updates, under conditions 1 to 5.

-- 1.0.0_SA_CTO~DELL2
