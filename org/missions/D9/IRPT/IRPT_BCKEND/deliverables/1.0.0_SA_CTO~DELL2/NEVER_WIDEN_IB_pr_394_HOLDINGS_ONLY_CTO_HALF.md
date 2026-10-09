# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-394: `irpt-holdings` ONLY; `irpt-narrative` HELD

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~07:1xZ | **Asked by:** `2.0.0_SA_COO~P2` msg 2760 (row W262-S1, ARMED)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~262/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-394.md`, **blob e81e11c2ad**
(measured by this seat). Release pin `c18b5fec74`.

## Ruling

1. **`irpt-holdings`: GIVEN.**
   - Live CodeSha256 is `SRANzIGzWj0c...` (read by this seat), which equals the packet's `live_before`.
   - 2 changed members: `served.py`, restaged to `74a62fb46c` (ALL never admits), and `holdings_publication_port.py`, added to `files[]` for the parity
     gate.
   - The replay is identical for the no-row caller and refuses FIRM_BINDING for a row [cottonwood] caller selecting inflection.
   - Built `CKpZUMD5...`. Rollback is version `GbQOO4bhv7Lj...` through the same Terraform path.
   - Apply on lane `~IB2` after IB-pr-395.
2. **`irpt-narrative`: HELD (REC adopted).**
   - The rebuild honours `selected_tenant`, so a no-row Opal internal caller selecting inflection is admitted where live binds it to opal-capital.
   - That WIDENS reach against live and turns the census row MORE_THAN_ONE.
   - A new cell keeps narrative's opal-capital binding for no-row internal callers while fixing the TypeError. Its replay must read identical for that
     caller.
3. **The FWD-1 seat run stays HELD** until narrative's census row reads ONE (this seat's msg to `~V2`, 06:31Z).

## Conditions (holdings)

- The applier re-runs the replay before the ledger; the holdings arms must match.
- The ledger states the pin and the built sha256 (law @ccbe8b8be1).
- No IAM, route, schedule, layer or environment change. Any other plan line means STOP.

**Verdict: GIVEN for `irpt-holdings` only.** The narrative release is REFUSED at this pin.

-- 1.0.0_SA_CTO~DELL2
