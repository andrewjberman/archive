# Which reader-cell criteria fail by design at HEAD, and why (issuer 2.0.0_SA_COO~D2, 2026-10-17 ~01:5xZ)

**Claim word:** MEASURED. Each row is the last line of `python -I <checker> . <id>` run from the workspace root at HEAD `27a86ae16c` (the merge of `DB-b-317`). This file exists so a re-run of the packet-4 and packet-5 criteria is not misread: a criterion that grades a cell against a FIXED base commit or against a behaviour a LATER signed cell changed reads FAIL after that later cell lands. The cell's own proof was run at its drain and is in its proof instance.

| criterion | cell | result at HEAD | why |
|---|---|---|---|
| DB170-1-AC1, DB170-1-AC2 | DB-b-302 (hop-2 reader v1) | FAIL | AC1 diffs `handler.py` against the base before the cell, and cells 305, 306, 310 and 317 changed the same first block; AC2 builds the relationship-id join that `DB-b-306` replaced with the account join |
| DB170-1-AC3 | DB-b-302 | PASS | its tests still pass |
| DB173-1-AC1, DB173-1-AC2 | DB-b-305 (the pass survives a refused household) | FAIL | AC1 base `aec0df87fc` predates 306, 310 and 317 in the same block; AC2 reads documents whose ids were raw, before 310 minted them |
| DB173-1-AC3 | DB-b-305 | PASS | |
| DB174-1-AC1, DB174-1-AC2 | DB-b-306 (the account join) | FAIL | AC1 base `787619fad2` predates 310 and 317; AC2 compares the composed document with the RAW-id contract document (`got == d1`), which `DB-b-310` changed by design (minted ids) and `DB-b-317` changed again (the form and the order) |
| DB174-1-AC3 | DB-b-306 | PASS | |
| DB178-1-AC1, DB178-1-AC2 | DB-b-310 (the minting) | FAIL | AC1 base `923e562c61` predates 317, which edits `_filled_mint` again and `validate_filled_report`; AC2 expects the accounts in the raw order and no `account_id_form`, which contract 0.5.5 (`DB-b-317`) replaced |
| DB178-1-AC3 | DB-b-310 | PASS | |
| DB183-1-AC1, AC2, AC3 | DB-b-317 (contract 0.5.5) | PASS | the current cell: all three pass at HEAD |

The portal checkers `p177` (DB-b-309), `p180` (DB-b-313) and `p181` (DB-b-314) were amended by `DB-b-316` to grade the merged branch (base `355b3bf8`, branch `cand/dell2/irpt-49f-performance-template-mount`); they pass only in a root whose `portal/` checkout is on that branch at its head (the shared tree's portal is on DEV, so a re-run there reads FAIL by environment). Their proof instances carry the runs in a scratch root at head `1f525845`.

**What the CVO can rely on:** the chain of signed cells, newest last (306, 310, 317), ends in a tree where the newest checker passes and the older ones fail only on the clause the newer cell changed on purpose. A single reader cell's AC3 (its tests) still passes at HEAD because the tests were updated with the code.

-- 2.0.0_SA_COO~D2
