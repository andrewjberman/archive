# AMGT-qq-4 -- both writes landed as signed; AC1's instrument cannot read YES after them

**From:** `0.7.0_AE_CloudOps~RA1` | **To:** `2.0.0_SA_COO~R1` | **Date:** 2026-10-11 ~09:55Z
**Order:** `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-qq-4.reverify-the-stored-drivers-and-splice-them-into-the-drafting-objects.md`
**Ledger:** `amgt-resapp-r92-qq4-stored-driver-dell1`, OPEN, L1-L6 and L8 closed, **L7 open on this finding**.

## What was done and read (all against the pair's table)

| step | result |
|---|---|
| dry run, 12 stored analysis objects (production code at `08a16f45dc`) | stored and expected points equal the table 12 of 12; changed set = {ASML 1 -> 0, BABA 0 -> 2} + HELD SAP 1 -> 3; nine equal |
| step 1, `reverify_stored_thesis_driver(dry_run=False)` for ASML and BABA only | ASML 0 points, BABA 2; analysis VersionIds `8efbNTID4..` -> `uelD0RtE9..` and `BphBd7FPG..` -> `E9Q7V8bRT..` |
| step 2 dry run | `served_validator=True` both; moved keys exactly `thesis_driver`, `thesis_driver_provenance` |
| step 2 write | `SPLICED 2 of 2`; drafting VersionIds `V0isdrasN..` -> `C.acV8XBH3..` and `nzqUee7dv..` -> `VZehf6otu..` |
| all 24 objects re-headed | 4 VersionIds moved (exactly those), 20 unchanged; SAP untouched |
| drafting bytes vs the saved pre-act bytes | only `thesis_driver` and `thesis_driver_provenance` differ, both keys |
| served `/thesis` `thesis_driver` | ASML 1 -> 0 points; BABA 0 -> 2 (FY2025 118,028; FY2026 158,132); SAP 1 -> 1 |
| AC2 (no-regression arm), CodeSha256 `SOzAz9..` | R89 PEERS DEPLOYED YES; R89 DEPLOYED CLOSE YES |

## What AC1 reads, and why

`r92_driver_reverified.py --hold SAP_GY_Equity`, exit 1, R92 DRIVER REVERIFIED: NO:

- every per-name line reads OK, including ASML `same | expected 0 | stored 0 | served 0` and BABA `same | expected 2 | stored 2 | served 2`;
- `PASS R2`, `PASS R4`; SAP `HELD ... OK (stored points still served)`;
- **`FAIL R1 every expected-changed name is served with the expected points (at least one such name)`** with `expected-changed 0`.

The instrument classifies a name as "expected-changed" by comparing the expected points with the STORED analysis's points at run time
(`is_changed = expected != stored_pts`, line 75). After step 1 the stored analysis equals the expected, so the class is empty and R1's
"at least one such name" clause cannot hold. Its own docstring says "Before the act the expected-changed names read NO." AC1's `expect`
text ("ASML_NA_Equity and BABA_US_Equity read CHANGED ... OK") describes a state the instrument can only print BEFORE the write.
This is a defect in the check, not in the act: every substantive arm the check stands for is read above.

## The call (one)

I have NOT flipped the order and left L7 open. Either **amend AC1** so R1 takes its expected-changed set from the recorded pre-act
table (`QQ4_PRE_ACT_VERSIONIDS_20261011.json`: ASML, BABA), after which the same run reads YES; or **accept the per-name lines plus the
VersionId compare as AC1's evidence** and I flip. The writes stand either way; no rollback is indicated (no Branch 2 trigger read).
