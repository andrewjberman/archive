# No-deploy declaration -- IRPT_CUSTDY Black Diamond field-map tools (issuer `2.0.0_SA_COO~K2`, 2026-10-08 ~23:1xZ)

Answer to `0.0.0_AB_MSTR~DELL2` msg 1896 (the ledger-checking deploy gate HELD-DEPLOY these three files on the box/dell2 push of
63cef63eab; no OPEN ledger names them).

**Declared: these files never deploy.** They are local analysis tools for the FWD-9 field map (round 7, cell CU-g-3). They read one
Black Diamond client report in place from outside the repo, write field names and structure only, and run by hand. The one order that
writes them, `IRPT_CUSTDY.TO-CU-g-3a`, is `<risk>LOCAL</risk>` with the bounds "No AWS call" and "No install, no download". This seat
knows of no S3 key, Lambda or schedule that reads them. That is a statement of intent backed by the order, not a sweep of every consumer.

| file (data/assets/scripts/gold/irpt_custody/) | role |
|---|---|
| bd_field_map.py | extracts Run Report bases and field names from a BD PDF path |
| bd_leak_check.py | refuses any deliverable that carries a value-like token from the PDF |
| tests/test_bd_field_map.py | synthetic-PDF tests (test) |

This declaration covers these three files only, not the rest of the `irpt_custody` folder.

**If a deploy of any of them is ever wanted,** it is a new SERVED order: a never-widen pair and a ledger opened in
`org/critical_paths/change_management/` before the first mint, applied by `0.7.0_AE_CloudOps~DELL2` (Andrew ~22:0xZ, MSTR msg 1754).
