# IRPT_DASHBD round 127, workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-15 ~22:3xZ)

**One order (a LOCAL build), drained and graded on the LANDED tree; no vendor call, nothing written to AWS, nothing deployed, no client data.** Issued @b73f58d17e (merged @7ae9f2afd3), drained: `DB-i-14` (~314, merged @c7d980af1b). On the merged tree, with contract 0.4.2 at HEAD, `DBI127-1-AC1`, `AC2` and `AC3` PASS and 90 tests pass across the adapter, wrapper and contract-042 test files (the worker reported 35 + 28 for the module's two files). The proof instance reads VALID. `round-close-check --project IRPT_DASHBD --round 127 --workstream B-IN` reads **MAY-CLOSE** (1 order, 0 judgment criteria). Push state: LOCAL on box/dell2, not read against origin.

## The gap before this merged (named, not suppressed)

Contract 0.4.2 landed (`~D2`, merge 6ac152c83a) before this order merged. In that gap the module on trunk read red: **4 module tests failed and 58 passed** (1 in the adapter's file, 3 in the wrapper's), and the round-125 checker's AC3 failed (its AC1 and AC2 still passed because they read the contract file, though `VENDOR_REPORTED` was already outside the 0.4.2 enum). The worker measured the same 4 on a scratch copy of trunk. They are green now. Round 125's criteria stay superseded by `checks/r127`.

## What changed

- Orion PRESENT rows write `return_basis` `TWR`; provenance is the `source` column (`orion`), which 0.4.2's `source_provenance` maps to vendor-computed. The `VENDOR_REPORTED` constant and its comments are gone.
- `market_value_eod_claim` is a declared column of the table, 25 declared fields in all, hashing to the contract's `schema_hash_with_optional`; `inferred` or `measured` on a PRESENT row, null on an ABSENT row; the run record's `claim_placement` retired and its `market_value_eod_claim_counts` stay (13 inferred, 4 measured on the golden).
- `contract_version` is read from the contract file (0.4.2). The wrapper now REFUSES a contract that does not declare the claim column, with count 1 and nothing written (my design choice, stated in decomposition section 13, decision (a)).
- The W311-S3 test line: an account seen only on a dropped day is still counted.

## What the issuer read for itself

Re-ran the three criteria and the proof in the worker's tree (PASS), merged through `safe-merge.sh`, re-ran the criteria and the three test files on the merged tree (PASS, 90 passed), checked the changed files for stale `VENDOR_REPORTED`, `claim_placement` and `RUN_RECORD` terms (none), and scanned them for identifier-length digit runs (none). The commit gate printed that the hashed account-id list is absent on this box, so no commit gate screens for client ids; the four files hold synthetic values only. **Not a grade.**

## Rows

Seat row `D2-S98` disarms `~D2`'s worker row `W221-S3` (the module no longer disagrees with the contract). No worker row from this round. No ARMED row of mine remains open on this workstream except the feed-landing pair `D2-S60` and `D2-S61`.

## Open

The first real-row run waits on `~P2`'s apply of the feed (IB-pr-596 at CloudOps IB2). The contract's L9 grade of 0.4.2 is the CVO's.

**Andrew:** nothing from this workstream.

-- 2.0.0_SA_COO~I2
