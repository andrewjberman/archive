# IRPT_DASHBD rounds 99 and 100, workstream B -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-14 ~02:0xZ)

**Two cells, both LOCAL, both read-and-count; no served byte moved, nothing deployed, counts and words only in the repo.** `DB-b-185` (round 99, ~150; drained @9c17abd199) and `DB-b-186` (round 100, ~151; drained @4f2c8bc565). Round-close `verdict=MAY-CLOSE` for each (orders=1, judgment=0). Round 98 is NOT terminal: `DB-b-184` is drained (@48fc80194b) but `DB-b-183`, the FDRXX apply, is known-held on dell1's ledger SC-e-97 (CTO msg 7399).

## DB-b-185 -- CASH_USD to cash (round 99): built, counted, then reverted on the CTO's ruling

The cell changed the synthetic sweep-cash ticker's special case to serve the cash class (4 lines, 58 tests, a mutant that failed) and counted what moves: 0 of 4,315 served positions carry the ticker; this seat re-read the newest holdings_lots snapshot itself (1,314,777 lots, exact ticker count 0). Five consumers or lists assume fixed_income for it (E_25 twice, B_01b by name rule, two infra lists). The CTO ruled the change cost with no gain (msg 7422); it was reverted @0f8d33c431 (classifier equal to the round-96 pin again, sha256 `e7385264...`, 33 tests pass) and row IRPT_DASHBD-D2-S25 disarms the CVO's row W147-S3. `DB99-1-AC1` was graded PASS at the drain and is not re-runnable now, by design. No CASH_USD pair was written.

## DB-b-186 -- how the CASH-ticker lots classify (round 100)

`DB100-1-AC1` PASS, re-run by this seat. The canonical table's rows were re-read by this seat: ticker `CASH` is `cash` / `Cash`; `CASH_USD` is `fixed_income` / `Cash` (its row is never read, because the special case answers first). Of 1,314,777 lots in the 2026-10-09 snapshot, 11 carry the ticker `CASH`: 4 accounts, 7 open, 4 closed, none with the description `CASH`, so the Investor Reporting special case does not fire and those lots go to the canonical branch. The gold classifier returns `cash` for them. Advisor Intelligence: none of the 4,315 served positions in the 189 of 194 files read carries the ticker (NOT_ESTABLISHED for these lots). Investor Reporting: NOT_ESTABLISHED (the accepted publication refuses an unscoped load at the reader's request-count bound); by code the canonical branch serves `cash`. So these lots already class as cash everywhere the code reads; the worker's recommendation to change the `CASH_USD` override is NOT adopted, since no lot carries that ticker.

## Open

- What Andrew meant by "Cash as a ticker should be CASH" is NOT established: it is not a class change for these lots. A display or label reading needs his words (which page, what it showed); asked of the CTO.
- Andrew's FDRXX smoke item closes on `2.0.0_SA_COO~P2`'s after-read of the IR holdings rule (CTO msg 7410), and on the FDRXX apply for the Advisor Intelligence pages.
- Push state: LOCAL on box/dell2.

-- 2.0.0_SA_COO~D2
