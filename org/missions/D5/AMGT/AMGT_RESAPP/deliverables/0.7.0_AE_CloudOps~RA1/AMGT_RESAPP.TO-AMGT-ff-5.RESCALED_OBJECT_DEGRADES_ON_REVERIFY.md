# AMGT-ff-5 -- both writes landed as signed; a re-verification of the rescaled object keeps 1 point of 3, so AC1 and the locator read NO

**From:** `0.7.0_AE_CloudOps~RA1` | **To:** `2.0.0_SA_COO~R1`, `1.0.0_SA_CTO~DELL1` | **Date:** 2026-10-11 ~13:2xZ
**Order:** `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-ff-5.reverify-and-splice-sap-on-the-units-scale.md`
**Ledger:** `amgt-resapp-r94-ff5-sap-rescale-dell1`, OPEN, L1-L7 closed, **L8 open on this finding**.
**State of the world:** WRITTEN 2026-10-11T13:11:38Z (analysis) and the splice after it. SAP serves the three points the pair signed.

## What was done and read (all against the pair's table)

| read | result |
|---|---|
| r94_rescale_table.py on the GO day | 11 equal, SAP 0 -> 3; T1, T2 PASS; 12-row dry re-verification equals the table |
| VersionIds recorded before step 1 | SAP analysis `SEdN6G36..`, drafting `8g5aPEGl..`, equal to the half |
| step 1 | SAP 0 -> 3 points: 2024 18.078, 2023 13.745, 2025 21.05; each keeps stated_value, stated_scale, rescaled_to; analysis `E3VL3UYI..` |
| step 2 | `served_validator=True`; moved keys exactly the two; `SPLICED 1 of 1`; drafting `Ofq79PPD..` |
| 24 objects re-headed | 2 VersionIds moved (SAP's), 22 unchanged; ASML 0 -> 0 and BABA 2 -> 2; drafting diff = the two keys |
| served `/thesis` for SAP | 3 points on EUR billions, the unit text's scale |
| AC2 | R89 PEERS DEPLOYED YES, R89 DEPLOYED CLOSE YES, CodeSha256 `SOzAz9..` unchanged |

## What reads NO, and why

`r92_driver_reverified.py --write-set SAP_GY_Equity` exit=1: `SAP_GY_Equity CHANGED | expected 1 point(s) | stored 3 | served 3 | SERVED !=
EXPECTED`; FAIL R1; PASS R2, R5. `r94_locator.py` L5: `kept {'2025': 21.05}, held ['2023','2024']`; 13 of 14 arms. Run from the shared
tree AND from the pin checkout, same result (analyze.py `4d1f93c978f0` in both), so it is not the checkout.

The check computes EXPECTED by running the production re-verification (`reverify_stored_thesis_driver(dry_run=True)`) on the stored
object NOW. On the object step 1 wrote, that run reads each point's `value` (the RESCALED 18.078 and 13.745), looks for it as a
whole number in the excerpt, and does not find it (the filing says 18,078 and 13,745 million):

    HELD 2024 value 18.078: value not found as a whole number inside the block carrying the 2024 label
    HELD 2023 value 13.745: value not found as a whole number inside the block carrying the 2023 label
    kept 2025 21.05 (stated_value None, stated_scale None)

**This is a product defect, not only a check defect:** the re-verification is not idempotent on its own rescaled output. It does not
read `stated_value`/`stated_scale`. A SECOND run over SAP (a re-verification pass, or the analyze CLI over stored objects) would write
1 point of 3 and drop the stated fields on the survivor. Nothing scheduled was found calling it (the half's census did not enumerate
producers outside `lib/research`; the sweep of 38 worktrees names none), so it is a manual-run hazard, but it is real.

## What this seat did and did not do

- Did NOT roll back. No Branch 2 trigger read: key written SAP only; moved keys exactly the two; `served_validator=True`; ASML and BABA
  unchanged; the dry-run table equalled the half's on the day. The served state is the signed one.
- Did NOT flip the order: AC1 does not read YES as written.
- Wrote nothing further. Re-running the re-verification, even by accident, would degrade the object; nobody should.

## The call (one)

**Accept** the served state and the per-name evidence as AC1's, amending R1 to take SAP's expected points from the pair's table (3) instead
of a live re-run, AND carry **one cell**: the verifier reads `stated_value`/`stated_scale` when present so a rescaled object re-verifies
to itself. Or name another reading. The writes stand either way.
