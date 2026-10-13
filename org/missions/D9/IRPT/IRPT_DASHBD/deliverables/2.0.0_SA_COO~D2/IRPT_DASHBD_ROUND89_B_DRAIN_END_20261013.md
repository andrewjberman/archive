# IRPT_DASHBD round 89, workstream B -- drain-end and FWD-8 grade read (issuer 2.0.0_SA_COO~D2, 2026-10-13 ~15:0xZ)

**One cell, LOCAL:** `DB-b-167`, order `IRPT_DASHBD.TO-DB-b-167.reasons-for-the-twelve-segments-neither-convention-closes` (issued @a59641ddb8 to `0.9.0_WK_IRPT_DASHBD~133`), status `complete`,
round-close `verdict=MAY-CLOSE` (`round-close-check --project IRPT_DASHBD --round 89`: orders=1, judgment=0). Drained @885009b760 and @b70da0aa6a. On the CTO's ROUND-89 ANALYSIS @8208cabf27 section 4 and msg 6956.

## What the cell found (counts only; the stored tie-out set of worker ~108; no vendor call, no secret read, no S3 access, no served byte moved)

| of the 12 segments neither convention closes | count |
|---|---|
| `MISSING_PRICE` | 0 |
| `FLOW_ABSENT_ONE_SIDE` (taken, re-closed at 0.35 pp) | 1 |
| `FLOW_ON_NON_TRADING_DAY` | 0 |
| `INCOME_OFF_FLOW_DAY` | 0 |
| `BD_ACCRUED_INCOME` (taken, re-closed at 0.35 pp) | 4 |
| `UNEXPLAINED` | 7, one segment in each of 7 accounts; `combined_only` 0 |

- The rule file was committed before the read (99d37085ba) and its bytes are bound by hash in the record. Every reasoned segment re-closed within 0.35 pp with its cause corrected (5 of 5); the uncorrected control reads 0 of 12.
- **The accrual identity holds on all 12**, but its correction closes only 4 (one more was taken earlier in the list by `FLOW_ABSENT_ONE_SIDE`); the other 7 keep the earlier record's finding ("accrual identity holds, restated return outside 0.35 pp"). Row `IRPT_DASHBD-D2-W133-S1` (OBSERVATION) names them in counts.
- **Variance from the analysis's list (issuer ruling, decomposition section 91):** the closed list added `BD_ACCRUED_INCOME`. Without it, all 12 would read UNEXPLAINED although 5 sit in the earlier ruled class.
- **This seat reproduced the counts** by running the tracked module on the shared tree (no record argument): the same six counts, 12 of 12 reproduced, 88 flow segments, 84 accounts behind them. This seat read the rule file and the whole module.
- Two issuer defects, both mine, both ruled and amended with no gate limb graded (a check file, not an order): `p88_round88.py` (a sha256 held a digit run; @a47ba859cd, round 88) and `p89_round89.py` (the range of `population.accounts`; @0fd0b865ea). The slot was re-seated once to re-run the invocation; the record, rule and module were not changed.

## FWD-8 grade read (item 3, this seat's; per account and window)

**Grain, stated first:** the windows are the 90 stored segments (86 accounts); every count above is at SEGMENT grain. FWD-8's ACCEPT is worded at DAY grain ("every day they disagree carries a stated reason"). No cell of this project
measured days that disagree inside a segment that closes within tolerance; this read does not claim them.

| clause | read | source |
|---|---|---|
| agreement within 0.35 pp under `BD_DEFAULT` | 76 of the 88 flow-bearing segments agree (51 of them the contested 51); 12 do not | DB-b-166 (`FLOW_CONVENTION_TIEOUT.json`), re-run by this seat; reproduced by this seat's module run |
| the 2 no-flow segments | 2 of the 90 carry no flow day; read by this seat with scratch scripts (not a tracked cell, counts only): both miss uncorrected and both pass the accrual identity and close when it is applied | scratch read, `BD_ACCRUED_INCOME` |
| a stated reason for every disagreement | of the 14 segments that disagree (12 + 2): 7 carry a stated reason that re-closes (4 + 2 accrual, 1 flow absent on one side); **7 carry none (UNEXPLAINED)** | DB-b-167 |
| guard (a misdated or missing deposit never shows as a huge gain or total loss) | cited, not re-run: the guard cells `DB-b-15` (census) and `DB-b-160` (`GUARD_INTERPLAY.json`); this seat did not re-read their grading for this note | decomposition, `0.9.0_WK_IRPT_DASHBD~129` |
| label ("time-weighted, net of fees" gone everywhere the new figures show) | NOT GRADED here: the C-LABEL switch is IRPT_BCKEND's page under its own order and halves (PRD line 283, read by this seat; the switch itself was not read) | PRD |

**Grade: FWD-8 is NOT REALIZED.** At segment grain, 7 accounts have a segment with no stated reason (UNEXPLAINED), so the "every disagreement carries a stated reason" clause is unmet for them; the other 79 accounts of the 86 are met on the agreement and reason clauses. The 7 are a finding of the
earlier record too (accrual identity holds, restated return outside 0.35 pp), not a new defect. Nothing served moved; the tolerance (0.35 pp) is Andrew's ruling of 2026-10-09.

## Open

- **Ledger leg L7 (mine), carried:** the first scheduled fire after the thresholds swap, 2026-10-14 11:41Z, `checks/l5/l5b_read.py` @88d74f1a63; ledger `irpt-dashbd-thresholds-swap-20261013` stays OPEN until then.
- **For the CTO's next analysis:** what to do with the 7 (a further closed-list reason the stored columns cannot show, a day-grain read, or a vendor read for those 7 accounts, which needs its own word under card 5); and whether the 2 no-flow segments belong in the round's population.
- **Push state:** this seat's commits are LOCAL on box/dell2.

-- 2.0.0_SA_COO~D2
