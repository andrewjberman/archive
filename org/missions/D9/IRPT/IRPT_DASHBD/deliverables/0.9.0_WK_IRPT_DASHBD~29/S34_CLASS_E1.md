# S34_CLASS_E1 -- class of the 440 accounts whose BD split halves do not recompose (counts and percentages only)

Population: 440 accounts (recompose.within false in TIEOUT_SPLIT_E1). Landed objects read: 880 of 880. Vendor calls 0.

| cause_class | accounts | share |
|---|---|---|
| fee_or_basis_between_pulls | 437 | 99.3% |
| other:net_twr_chain_over_tolerance_with_days_flags_and_basis_agreeing | 3 | 0.7% |
| total | 440 | 100.0% |

Rule (first match wins): missing/zero half, annualized, days or held-flags off, then fee/basis iff the NET halves chain to the full NET within 0.35 pp, else other.

Reading: 437 of 440 (99.3%) have net returns that chain inside tolerance with day counts and flags agreeing; the gross gap is the fee add-back (fees / average of begin and end value) evaluated on three different bases. 18 have an ending value of 0 on the full range (add-back denominator is half the opening value); 30 carry a negative fee on at least one of the three points.

Gross gap pp: min 0.35, median 0.49, p75 0.81, p90 1.98, max 724.16. Over 1 pp: 98 (22.3%); over 10 pp: 14 (3.2%).

Largest gap (724.16 pp): left -0.5274, right 0.0134, full -7.7627, chained -0.5211 (gross). Class fee_or_basis_between_pulls; net chain gap 0.0000 pp. The gap is the full-range fee add-back on a closing account (negative fee, average value is half the opening value).

Overlap with right-half misses: right_misses 1834, in_s34 306, outside_s34 1528 (of the 440 S34 accounts, left tied 386, right tied 134).

Control: round-18 full gross re-derived from the landed full point for all 440; mismatches 0.
