# IRPT_DASHBD round 118 (the CTO's analysis answering round 113, msg 8000), workstream B-49F -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-15 ~05:2xZ)

**Three orders, all LOCAL; nothing served moved, nothing written to AWS, nothing scheduled or deployed; counts, hashes and words only in the repo; the client gold and the QA parquet stay in the private folder `C:/dev/_irpt_private_evidence_20261009/`.** Issued @485629a40e. Drained: `DB-b-231` (~186, merged @524ba1f162), `DB-b-230` (~185, merged @00a48e7d7e) and `DB-b-232` (~185, merged @17e300d554, with the module repairs). On the landed tree `DB118-1-AC1` to `AC3`, `DB118-2-AC1`, `DB118-3-AC1` and `AC2` all PASS (the criterion `DB118-3-AC3` was struck, below), and so do the ten earlier live criteria of rounds 110 to 113 (two needed a re-pin, below). `round-close-check` reads **MAY-CLOSE** (0 judgment criteria, all proofs structurally VALID). Push state: every merge and amendment is ON origin box/dell2 (fetch read, origin @f590d02d75) except my last commit `34272a71e6` (the r110 and r111 re-pin), which is LOCAL until the next box-sync.

## What the cells found

- **`DB-b-230` (hop 1, the gold table `filled_report_values`):** a firm-neutral gold script `data/assets/scripts/gold/irpt_reporting/filled_report_values.py` writes the contract's filled report as ROWS (13 columns; one row per household x member x row x series point; the value, a text, or the absent kind and its words) at the firm's gold address from `address()`, with a source-ends rule (a member that needs a day after its source's newest partition is SOURCE_BREAK naming the frontier) and `to_rows` / `rows_to_document` that round-trip the contract's `{household, values}`. Contract 0.5.2 carries the table (`gold_table`). One private QA run, 49 Financial, as_of 2026-10-13: 25 households, 29,294 rows (27,454 measured, 424 text, 1,416 absent); every household carries all 117 members plus the seven reserved document rows; the household ending value equals the gold sum for both probed households. 21 tests (18 plus the three repair tests).
- **`DB-b-231` (the flow-guard READ):** on 2026-04-21 the account gold has 5,902 rows and 943 GRADED_DISAGREED (tolerance 0.001244 from the manifest): **941 are VALUE (the value moved, no flow, and the price return did not move with it), 2 FLOW_AND_VALUE, 0 FLOW**; 928 of the 943 have a positive gap, 722 are within 1 percent, 209 within 5 percent, 12 above, and only 3 reverse the next day. The next five dates (07-02, 10-13, 09-22, 10-06, 09-16) are 26, 9, 16, 9 and 19 rows, also VALUE-led. Totals over the six dates: 1,022 = VALUE 1,009, FLOW_AND_VALUE 11, FLOW 1, NEITHER 1. So the 04-21 breakage is the value against the holdings price return on that day, not the flow: the question for the next read is which holdings price moved.
- **`DB-b-232` (the Cottonwood reader):** an adapter `adapters/cottonwood_report_reader.py` that reads only the Cottonwood gold prefixes and refuses any other firm's (15 tests, three `test_refuses_*` negatives), and contract 0.5.3 (a Cottonwood source on all 36 account-return members, the household key from `account_dim`, `holdings_performance_daily` recorded unread). **Its two QA runs could not be made (criterion `DB118-3-AC3` struck by Amendment 2, row `W185-S9`):** the Black Diamond account key of the household frame (11 characters, 999 accounts) and the Cottonwood `account_return_daily` frontier partition's key (the Commonwealth custodian's number, 8 or 9 characters, **12 accounts** at 2026-06-22) have zero overlap, and the Cottonwood gold `account_dim` holds no object (its pair is unsigned). The reader refused correctly.

## What this seat read for itself

I re-ran every criterion in each worker's tree and again on the landed tree, re-validated each proof instance with its full id set, re-ran lint on the changed files, and re-ran the ten criteria of rounds 110 to 113 (8 matched; `DB110-2-AC1` and `DB111-2-AC1` read FAIL on the contract's pinned hash after the contract moved, and PASS after I re-pinned them through the lineage, as r105, r106 and r109 do). The flow-guard checker recounts every number from the gold itself (its own read-only GETs of the six dates and their neighbours, equal to the unit). I did not open any QA row against the gold beyond the checker's two probed households. No pages. **Not a grade.**

## Issuer errors this round (mine, disclosed)

- **Round 105 never reached the contract text.** DB-b-202 ruled that the activity and net-gain members print the same folds as the value summaries; the contract text kept sourcing them to the activity table, and DB-b-230 said the contract wins. So in the QA table all 402 `act.*` rows and all 125 `hold.net_gain_*` rows are absent (the activity table holds 5 trading days). Row `D2-S56`. The repair (contract 0.5.4 plus the module) is in my next issuance, before the table is scheduled or written.
- **DB-b-230 left the module 49-Financial-shaped** (the crosswalk columns and no presence test for sibling tables) and an empty-lot fold returning 0: found by DB-b-232, repaired inside it (Amendment 1), row `W185-S8` disarmed in `D2-S62`.
- **DB-b-232 asked for QA runs that no data could carry**, because I had not read the return table's key against the household key: struck (Amendment 2).

## Rows held (owners named)

`W185-S1` to `S5` and `S6` to `S9`: dispositioned in `D2-S56` and `D2-S62`; `W185-S8` (ARMED, mine) DISARMED. `W182-S1` (the commit gate's client-data list absent on dell2, owner 0.0.0_AB_MSTR) still stands; this seat's identifier scans stand in. No ARMED row has a dark owner.

## What goes to the CTO (one ask, in the slug)

Cottonwood cannot yet yield a household report: its household key is the Black Diamond account key, its history table is keyed by the Commonwealth custodian's number and holds 12 accounts at the frontier, and its gold `account_dim` is unapplied. The ruled Black Diamond input for `account_return_daily` (ask 8040, round-117 ruling 3) would key new rows by the Black Diamond account key and so join. **May the next cells be (a) that producer input, keyed by the Black Diamond account key, and (b) a READ of whether a map from the Commonwealth number to the Black Diamond account key exists in the Black Diamond silver, which the history before 2026-06-23 needs?** Carried as data facts: the contract repair above; the 04-21 read (the next read is which holdings price moved).

## What this does to the FWD outcomes

Inputs to `FWD-2`, `FWD-11` and `FWD-21`: none is met. Hop 1's table exists LOCAL for 49 Financial; `~P2`'s deploy legs wait on the first cloud write (a later order for the applier) and on the contract repair. Grading is the CTO's at L10.

## Open

**Andrew:** the as-of approval row `dell2-20261014T195533Z-90a9` (client-facing) and call a252 (the 49 Financial disclosure file). **This seat:** the L3 read of the classifier ledger (the BD platinum positions had not been rewritten as of 02:30Z; the next nightly run is 23:00Z), and `DB-b-183`.

-- 2.0.0_SA_COO~D2
