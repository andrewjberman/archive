# RULE_LEDGER_ADDENDUM.md -- IRPT_DASHBD round 91, TO-DB-b-171 (worker 0.9.0_WK_IRPT_DASHBD~137), dated 2026-10-13

RULE_LEDGER.md is NOT edited. This addendum is written under its section 6, because the rule as written proved
unworkable after the read started: its reason (1) BD_INCOME_PER_LOT returned no day, and the cause is in the TEST.

## 1. What the first run measured (counts only; the official record is the run of RULE_LEDGER.md as written)

- Of the 23 differing days, 12 carry Black Diamond income that is an integer multiple (3 to 6) of the served income.
- All 12 have two or more income rows on the day. None has a single income row.
- On 9 of the 12 days every income row carries ONE transaction_id; on 3 of the 12 the rows carry two or more.
- The as-written TEST of reason (1) requires at least two DISTINCT transaction_id values among the income rows. It
  therefore admitted 3 of the 12 multiple days, and the correction of those 3 did not close them within 0.01 pp
  under the as-written TEST path (see the official record: 0 days took any reason).

## 2. Diagnosis

A per-lot split is several income rows of one transaction: one row per lot, all sharing the transaction identifier.
The as-written clause tests the opposite of the reason's meaning. The reason is about the number of rows, not about
distinct identifiers.

## 3. The two readings

Reading A (the rule as written, RULE_LEDGER.md section 1 (1)). This is the official record,
LEDGER_ROWS_23_DAYS.json: 0 days take BD_INCOME_PER_LOT; 0 of 7 accounts close with reasons; all 23 days UNEXPLAINED.

Reading B (this addendum). Reason (1) BD_INCOME_PER_LOT, TEST replaced by:
- a(d) is not zero; at least two rows of R(d) carry income not zero; and there is an integer k >= 2 with
  tie(I(d), k * a(d)), k the nearest integer to I(d) / a(d).

The CORRECTION (BD income set to a(d); b'(d) = b(d) - (I(d) - a(d)) / m(d)), the closed-list order, every other reason's
TEST and CORRECTION, the window test and the negative arm are unchanged from RULE_LEDGER.md.

Reading B is measured only in the private folder of worker 137, by a copy of ledger_rows.py that differs from the
tracked module in that one clause. Its counts are reported beside reading A. It is not the record and does not alter
the record's per-account figures.

## 4. Scope

This addendum changes no served value, reads no new row, and rules nothing. The disposition of the two readings is
the CTO's.
