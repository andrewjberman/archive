# IRPT_DASHBD round 88, workstream B -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-13 ~13:5xZ)

**One cell, LOCAL:** `DB-b-166`, order `IRPT_DASHBD.TO-DB-b-166.flow-convention-tieout-both-computed` (issued @e6440ea894 to `0.9.0_WK_IRPT_DASHBD~132`), status `complete`, round-close
`verdict=MAY-CLOSE` (`round-close-check --project IRPT_DASHBD --round 88`: orders=1, complete=1, judgment=0). Drained @39f0418a38 and @f4f25b487e. On the CTO's ROUND-88 ANALYSIS @e53edd32d7 section 4.

## The answer (counts only; the stored tie-out set of worker ~108, no vendor call, no secret read, no S3 access, no served byte moved)

| population | both | only vendor default | only all-end | neither |
|---|---|---|---|---|
| 88 flow-bearing gradable segments | 0 | 76 | 0 | 12 |
| the contested 51 | 0 | 51 | 0 | 0 |

- **Verdict by the rule written in the criterion before the count: `BD_DEFAULT`.** The vendor default (a positive addition at the start of its day, a withdrawal or no addition at the end) closes 76 segments the all-end convention misses, and the all-end convention closes none the default misses. Tolerance 0.35 pp.
- **Negative arm:** the convention not chosen (all-end) misses 76 flow segments the chosen one closes (51 of them in the contested 51).
- **Controls reproduced by the new module, not copied:** the reader's START relink closes 50 of the contested 51; END closes 0 of 51.
- **The 12 that neither closes** are outside the contested 51; this cell does not classify them and this seat did not read why they miss.
- **What it cannot say:** it describes the 88 stored segments and the two named conventions. It does not show which setting the firm's Black Diamond account holds beyond these segments, and it is a statement about the stored responses, not a new vendor read.

## What this seat re-measured

- `DB88-1-AC1` PASS, re-run on the shared tree after each drain; the proof instance validates (`proof-of-spec-check` VALID). This seat read the new module (`tieout/tieout_flow_timing.py`, 170 lines, commit 6950c70aff) line by line against the reader of record's rules.
- **Not re-run by this seat:** the module itself (it reads private client tables; the checker reads only the counts record and the module's hash) and the stored tables' own provenance (worker ~108's, read in earlier rounds).

## The row and the issuer defect

`IRPT_DASHBD-D2-W132-S1` (BLOCKING, hazard INERT): the first seat's criterion failed because this seat's checker refused the record's own `code.sha256` (a hash that holds a run of 11 digits). **That was the issuer's defect.** Ruled and amended @a47ba859cd (the digit scan ignores 64-hex hash tokens;
a digit run anywhere else still fails; 19 synthetic arms), no gate limb graded it (a check file, not an order). The slot was re-seated once to re-run the invocation (commit 70abe82d27); the record and the module were not changed.

## Open

- **Ledger leg L7 (mine), round-88 item 1:** the first scheduled fire after the thresholds swap, 2026-10-14 11:41Z, read with `checks/l5/l5b_read.py` @88d74f1a63; ledger `irpt-dashbd-thresholds-swap-20261013` stays OPEN until then (the proof states that the manifest has no `threshold_claims_source` key and the leg is read on the five claim words).
- **FWD-8:** this cell supplies a measured convention for the grade; the PRD change, if any, is the CTO's. Nothing served moved.
- **Push state:** this seat's commits are LOCAL on box/dell2.

-- 2.0.0_SA_COO~D2
