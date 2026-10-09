# Commonwealth flow-month DIFF classes (CB-r-3)

Every DIFF month (|computed - reported| > 0.05 points) that carries an external-flow row, classed by its dominant flow type (largest summed abs flow / account value that day) and the size band of that type's largest row. Nothing is fixed here. Months graded MATCH with a flow: 316 (the same class rule, for the DIFF share).

| type | band | DIFF months | median abs diff (pct pts) | MATCH months | DIFF share | DIFF months with a qty x close row |
|---|---|---|---|---|---|---|
| lo | over 10% | 252 | 32.8817 | 76 | 0.768 | 5 |
| li | over 10% | 111 | 53.2192 | 80 | 0.581 | 0 |
| li | 1-10% | 108 | 4.2378 | 65 | 0.624 | 0 |
| li | under 1% | 106 | 1.3067 | 26 | 0.803 | 0 |
| lo | 1-10% | 94 | 3.8414 | 24 | 0.797 | 0 |
| lo | unsized | 73 | 18.5812 | 1 | 0.986 | 0 |
| lo | under 1% | 57 | 0.5816 | 4 | 0.934 | 0 |
| li | unsized | 56 | 1.7306 | 40 | 0.583 | 1 |

## Three example accounts of the largest class (lo/over 10%)

### account acct#ef1f3927, month 2019-02

computed -32.5264 pct vs reported 0.17 pct: diff -32.6964 pct points (class lo/over 10%)

| date | type | flow | value that day | prev day value | pct of value | valued from | day return |
|---|---|---|---|---|---|---|---|
| 2019-02-21 | lo | -20000.0 | 21438.38 | 61438.38 | 93.291 | amount | -0.325529 |

### account acct#638a682f, month 2019-01

computed -33.0271 pct vs reported 0.04 pct: diff -33.0671 pct points (class lo/over 10%)

| date | type | flow | value that day | prev day value | pct of value | valued from | day return |
|---|---|---|---|---|---|---|---|
| 2019-01-31 | lo | -4624.48 | 4746.79 | 13992.62 | 97.423 | amount | -0.330271 |

### account acct#05dd4a9d, month 2023-07

computed -32.7146 pct vs reported -0.18 pct: diff -32.5346 pct points (class lo/over 10%)

| date | type | flow | value that day | prev day value | pct of value | valued from | day return |
|---|---|---|---|---|---|---|---|
| 2023-07-14 | lo | -455.68 | 484.11 | 1395.47 | 94.127 | amount | -0.326542 |

FLOW-DIFF-CLASSES diff_flow_months=857 classes=8 largest=lo/over 10% largest_months=252 examples=3
