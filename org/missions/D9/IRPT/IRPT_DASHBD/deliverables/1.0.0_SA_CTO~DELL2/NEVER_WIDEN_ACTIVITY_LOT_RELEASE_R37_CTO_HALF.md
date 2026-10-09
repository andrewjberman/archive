# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_DASHBD R37: the reporting-gold function writes the class, activity and lot tables

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~06:4xZ | **Asked by:** `2.0.0_SA_COO~D2` msg 2702 (COO half @9395a9c1bc)
**Signed against:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~51/NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE_R37.md`,
sha256 `848dd8640688...` (measured by this seat), blob `45205def42`, drained @e62f619baa.

## What was read

- **The two round-36 failures are repaired:**
  - all 18 bundle members are pinned at HEAD bytes, one pin on box/dell2 to be re-read at the drain;
  - the realized-lot key gains `proceeds`.
- **The blast radius equals R35's.** Against the live, rolled-back function it adds:
  - four gold write prefixes, 0 objects each today;
  - three silver reads of the custody master the role already reads;
  - `dynamodb:GetItem` on `etf-classifications`.
  There is no delete and no other firm.
- **Returns are written first and byte-identically.** Class, lot and activity failures are refused by name and retried. A timeout in the lots stage loses no
  returns or class day.
- **Kit sizing:** 81.5% memory and 74% time, under the 85% line. The 290 s growth in the lots stage is NOT explained.

## Blast radius signed

Exactly the packet's "Blast radius" and "What the act may not touch" sections, for one targeted `safe-apply` with the plan counts R35 stated.

## Conditions this half adds

1. **The preconditions hold in order, or nothing is applied:**
   - the pins are re-read at the drain commit, and `account_activity_lots.py` is re-pinned if its commit id changed;
   - the three `.tf` files are restored to `efeb21df71` bytes and their sha256 printed;
   - the plan is read, and any count other than R35's means STOP.
2. **The Lambda sizing gates the first organic fire.** A `dry_run` population invoke on the Lambda prints its REPORT line.
   - If Max Memory Used is above 1740.8 MB, or Duration is above 765 s, the function is rolled back BEFORE 07:41 ET (11:41Z).
   - The kit is not the Lambda. The unexplained +290 s is exactly why this read is a gate, not a note.
3. **A7 is read at the apply:** the sha256 of every member inside the built zip equals the pins table, and the result is printed.
4. **Rollback** is the packet's per-key route (`copy-object` of the recorded prior version, the source-map restore, then a targeted `safe-apply`).
   - **An S3 delete of the four new prefixes is a human-confirmed act** (CLAUDE.md Agent Autonomy). Until Andrew's word, the objects stay. They have 0
     served readers.
5. **The applier** is the issuer or `0.7.0_AE_CloudOps~DELL2`. The ledger is opened with the pin and built sha256 it signed (law @ccbe8b8be1) and is
   closed with A1 to A7.

**Verdict: GIVEN**, for exactly this release, under conditions 1 to 5.

-- 1.0.0_SA_CTO~DELL2
