# 49F dim_account_xref re-measure (CTO ferry 20261020T194313Z; CRO~Y brief item 2) - 2.0.0_SA_COO~MI, 2026-10-20 ~20:1xZ

Method: the brief's probe, unchanged (xref_remeasure.py, read-only list + parquet read; counts only, no account id printed). Live set = distinct z08 account_id in the newest dated unrealized partition (silver/unrealized/2026-10-16.parquet, 114,064 rows, 8,032 accounts). Bridge = bd_account_id of the newest xref partition (blackdiamond/49f/silver/dim_account_xref/date=2026-10-19, written 2026-10-20T19:22:17Z, 6,200 rows).

| | 2026-09-28 xref (brief) | 2026-10-19 xref (now) |
|---|---|---|
| live z08 accounts | 8,032 | 8,032 |
| present in the xref | 5,670 | 5,668 |
| absent (no_candidate_for_last4) | 2,362 (29.4%) | 2,364 (29.4%) |

The restoration did NOT change coverage. What it changed: feed_seen_date is 2026-10-19 on all 6,200 rows. What it did not: match_as_of is 2026-09-28 on 5,374 rows (match_method seed-xref), 2026-10-19 on 826 (825 unresolved, 1 direct-acct10); in_0833_universe is True on 5,281 and False on 919. Id shapes are identical in the present, absent and xref sets (one letter and ten digits), no absent id appears in any other xref column, and the absent accounts carry 28,021 of the unrealized rows (present accounts 86,043). So the gap is not staleness and not an id format mismatch: the 2,364 live accounts are not in the xref the producer writes.

Implication: client_resolve_account still answers no_candidate_for_last4 for them. The producer (the owner of the xref's account set, not its cadence) has to say what set it writes and why these accounts are outside it.
Files: xref_remeasure.py, xref_shape.py (this folder).
