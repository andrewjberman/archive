# IRPT_BCKEND round 1, workstream ~PE (49 Financial's candidate screen run offline) -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~13:0xZ). To: 3.0.0_SA_CVO~IRPT. One order, issued @8d6cf63777 on the CTO's msg 8256: IB-pr-573 `complete` (merged @dbfd95217d). `python .tools/round-close-check.py --project IRPT_BCKEND --round 1 --workstream "~PE"` reads `MAY-CLOSE`. I re-ran IB212-1 AC1 to AC3 on the worker tree: all PASS; the proof instance is VALID.
Push state: LOCAL on `box/dell2`. **READ ONLY: the gate ran offline in a scratch script on synthetic nodes; nothing was published, bypassed or written; the account is described by class only.**

## What the CVO needs to know

- **My order's premise failed, and the worker said so.** I ordered the 49 Financial candidate's per-account screen run offline to name the filter that drops the account. There is no such filter in play: the account has ONE row on the 2026-10-12 `dim_balance` partition and NONE on 2026-10-13, so it is not a key of the candidate partition the builder iterates, and no screen ever sees it. **It is a source gap on the candidate date** (measured), not a screen drop. Why the partition omits it, and whether it returns later, are not read (the cause is inferred).
- **The gate works as designed:** `evaluate_publish_gate` at HEAD, called as `run_firm` calls it, REFUSES with `account_lost` at `holdings_snapshot.py` line 3058; the exemption reads TERMINATED entries only, and the account is ACTIVE. **It is not Cottonwood's condition** (Cottonwood's account has no-position rows and the validator refuses an empty frame at line 403), so one screen fix does not cover both firms.
- **Remedies read in the code:** a source correction re-landing the account's custody row for 2026-10-13 if the account is live at the custodian (no change to the screen, validator or guard); or a custodian-confirmed TERMINATED mark, which the directory shows is not the case today (ACTIVE).
- **Open (the next read):** whether the gap persists on 2026-10-14 (today's candidate): if the account is back, the refusal clears on its own.
- **Row:** disposition row D2-S197 (names the source gap; D2-W413-S1 resolved as to cause).

## Judgment criteria

None this round (judgment=0).
