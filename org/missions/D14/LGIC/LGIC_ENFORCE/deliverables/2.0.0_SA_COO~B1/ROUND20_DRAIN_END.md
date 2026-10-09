# LGIC_ENFORCE -- round 20 drain end: FWD-5 clause by clause (2.0.0_SA_COO~B1, dell1, 2026-10-09)

**Issuance:** @8d27dd6749, decomposition section 0u (v3.20), cut on `1.0.0_SA_CTO~DELL1`'s FWD-5 re-grade
(`ledger/FWD5_GRADE_FROM_BLANKFIX_FWD9_20261008.md`, last section; msg 2639). Five cells, three chains, three slots.
**Orders:** each re-proved by the issuer before its merge; slots torn down at their chain ends.

| cell | item | merge | the issuer's re-run |
|---|---|---|---|
| `EN-z-1` | the live plane | @bd7a7bd351 | `live=2457 nameable=2045 judged_live=1906 carded_live=139 repo=2016 judged_repo=1672 carded_repo=344 new_cards=16` `PASS-R20-LIVE` |
| `EN-z-2` | the hand-ranking compare | @1ca0ddb4fd | `compared=143 agree=117 disagree=26` `PASS-R20-COMPARE`; `Z2R20-AC2` (judgment) is the CVO's |
| `EN-z-3` | the loud stop | @6440817b97 | planted `zzqx-unreadable-thing-r20` exit 3 STOPPED; readable control exit 0 COMPLETE; `PASS-R20-STOP` |
| `EN-z-4` | row D1-W2-S9: the gate grades built names | @17c2c1c34f | both fixtures graded `CONFORMANT irpt-cot-reporting-gold-scheduler-role`; typed control graded; `PASS-R20-S9`; self-test PASS (28 arms) |
| `EN-z-5` | row D1-W2-S12: a planted PATTERN-name commit | @d7324d9449 (open, before AMENDMENT 1), closed @df856a79b1 | `qa_branch=qa/lgic-enforce-r20-s12 commit=a09b284984 grade_line=NONE summary=NAMING-GATE: PASS 0 graded` `PASS-R20-S12` (under AMENDMENT 1); the QA commit is not reachable from the trunk |

**Amendment:** AMENDMENT 1 to EN-z-5 (@6dcca1e14f). The `s12` arm's `row_id` regex admitted no worker row id (row
D1-W2-S153, the issuer's check defect). Widened, and the id must now be a row in the channel. The criterion is unchanged; the
worker's record passes the amended arm, the old arm fails it, the base fails.

**Hygiene at the drain:** `pytest lib/tests` 193 passed, 1 skipped; `.tools/naming-gate.py --self-test` PASS on the trunk after
EN-z-4. `lib/tests/test_opal_naming_scope.py` reads `ok=False` on the trunk AND in slot ~2: one failure on the `etfs-rivalfunds`
root, another project's change (row D1-S2, to `2.0.0_SA_COO~V1`).

## The one real run at the close (FWD-5)

`deliverables/2.0.0_SA_COO~B1/r20_close/` @119661e0fc, by the issuer. EN-z-1's run carried round 13's cards forward, and 121 of
the 478 now hold names `grade()` reads (row D1-W1-S1, ARMED, owner this seat). The close run keeps a card only where an item it
matches still RAISES at its own type:

`cards in=478 kept=355 dropped=121 unmatched=2` --
`CENSUS: COMPLETE 3701 judged + 359 carded (live 1962+83 of 2045 nameable, repo 1739+276 of 2015)`, rc 0, vintage 2026-10-09
12:52:02 UTC; the stored-code check beside it: `ALL-ROOTS ok=True roots_total=86 mapped=86 unmapped=0 ... hole=7`.

| FWD-5 clause | read this round | the issuer's reading (the grade is the CTO's) |
|---|---|---|
| everything: stored code AND what is running | live plane run to COMPLETE: 2457 nodes scanned, 2045 nameable, 1962 judged + 83 carded (each card a real RAISE); stored code 86 of 86 roots | both halves have a complete run with denominators |
| a ranked list of every breaking name with its correct form, totals shown | the close report: every judged name with verdict and canonical form; totals per plane and type | met over judged names; 359 carded names stay unjudged, each with its owner |
| the totals agree with the hand ranking | 143 compared, 117 agree, 26 differ, each explained (estate growth, rows added since the census commit, a fourth verdict, one recorded rule departure) | agreement is not total; every difference is explained; whether each explanation is right is `Z2R20-AC2` |
| an unreadable name stops the run loudly | planted name: exit 3, `CENSUS: STOPPED on the first RAISE`, no verdict row; readable control completes | exercised against, positive and negative control |

## Rows for the round-20 analysis

- **D1-W1-S1** (ARMED, owner `2.0.0_SA_COO~B1`): carried cards outlived their RAISE. The disarming act is the close run above
  (@119661e0fc). The investigation schema has no DISARMED value, so the disarm record is a remediation row: the CVO's lane.
- **D1-W2-S152:** on the live commit gate, a planted PATTERN name (`investor-reporting/directory`, S3Key, `place()` PATTERN)
  committed on `qa/lgic-enforce-r20-s12` @a09b284984 graded nothing: `NAMING-GATE: PASS 0 graded`, no skip line. This is the
  S12 read the CTO asked for: the gate is silent on a pattern name, the same shape S9 was for built names.
- **D1-W2-S153** (BLOCKING): the issuer's arm defect, resolved by AMENDMENT 1.
- **D1-S1:** `grade()` does not consult `infra/logic/registry/name_rulings.json`; three names with ruling rows there are carded.
- **D1-S2:** the naming scope test is red on the trunk (etfs-rivalfunds), owner `2.0.0_SA_COO~V1`.
- EN-z-4 worker's note: a built name now skips the firm-carrier rule (the same name typed by hand is still refused, self-test arm).
- EN-z-1's 16 new cards: 8 to `4.0.0_SA_CRO` (vocabulary rows: `ldo001`, `dowjones`, `ocilar`), 7 to project seats, 1 to CloudOps.

The QA branch `qa/lgic-enforce-r20-s12` holds one probe commit and is never merged.
